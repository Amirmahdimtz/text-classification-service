"""Offline reproducible baseline builder for approved single-label report data.

Does not select a production model, calibrate confidence or evaluate the Gold Test.
Only train and validation input is accepted. Writes JSON, never pickle.
"""
from __future__ import annotations

import argparse
import os
from hashlib import sha256
import json
from pathlib import Path
from time import perf_counter

from src.core.services.text_classification.dataset_preparation import (
    DatasetRecord, DatasetValidationError, parse_records, split_records, build_private_manifest,
)
from src.core.services.text_classification.text_preprocessor import PREPROCESSOR_VERSION, preprocess_text
from src.infrastructure.ml.tfidf_linear_model import MODEL_FORMAT, TfidfLinearModel


def train_baseline(train: tuple[DatasetRecord, ...], validation: tuple[DatasetRecord, ...], *,
                   release_dir: Path, model_version: str, taxonomy_version: str,
                   dataset_fingerprint: str, authorization_reference: str,
                   seed: int, max_features: int = 200_000) -> dict:
    """Train only on provided training rows; use validation only for reporting."""
    import numpy as np
    import sklearn
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.svm import LinearSVC
    from sklearn.metrics import precision_recall_fscore_support, confusion_matrix

    if not train or not validation or not model_version or not taxonomy_version or not authorization_reference:
        raise DatasetValidationError("Training prerequisites missing")
    if max_features < 10 or len(dataset_fingerprint) != 64:
        raise DatasetValidationError("Invalid training configuration or fingerprint")
    if any(len(row.labels) != 1 for row in (*train, *validation)):
        raise DatasetValidationError("Single-label-only baseline: cardinality approval required")
    if len({r.report_id for r in train} & {r.report_id for r in validation}):
        raise DatasetValidationError("Train/validation identifier leakage")
    if len({r.group_id for r in train} & {r.group_id for r in validation}):
        raise DatasetValidationError("Train/validation group leakage")
    labels = sorted({r.labels[0] for r in train})
    if len(labels) < 2 or any(row.labels[0] not in labels for row in validation):
        raise DatasetValidationError("Training requires >=2 classes and compatible validation labels")
    root = release_dir.resolve()
    repo = Path(__file__).resolve().parents[1]
    if repo == root or repo in root.parents:
        raise DatasetValidationError("Refusing to create model artifacts within the public checkout")
    if root.exists():
        raise DatasetValidationError("Refusing to overwrite an existing release directory")
    cfg = {"classifier": "LinearSVC", "classifier_class_weight": "balanced", "seed": seed,
           "vectorizer": {"analyzer": "char", "ngram_range": [2, 5], "sublinear_tf": True,
                          "lowercase": False, "max_features": max_features},
           "preprocessor_version": PREPROCESSOR_VERSION}
    norm_train = [preprocess_text(row.text).normalized_text for row in train]
    norm_valid = [preprocess_text(row.text).normalized_text for row in validation]
    vectorizer = TfidfVectorizer(**{**cfg["vectorizer"], "ngram_range": tuple(cfg["vectorizer"]["ngram_range"])})
    x_train = vectorizer.fit_transform(norm_train)
    classifier = LinearSVC(class_weight="balanced", random_state=seed)
    classifier.fit(x_train, [r.labels[0] for r in train])
    x_valid = vectorizer.transform(norm_valid)
    start = perf_counter()
    predictions = classifier.predict(x_valid)
    latency_seconds = (perf_counter() - start) / len(validation)
    y = [row.labels[0] for row in validation]
    p, r, f, support = precision_recall_fscore_support(y, predictions, labels=labels, zero_division=0)
    report = {"evaluation_split": "validation", "sample_count": len(validation),
              "macro_f1": float(np.mean(f)), "per_class": {
                  label: {"precision": float(p[i]), "recall": float(r[i]), "f1": float(f[i]),
                          "support": int(support[i])} for i, label in enumerate(labels)},
              "confusion_matrix": confusion_matrix(y, predictions, labels=labels).tolist(),
              "labels": labels, "classifier_predict_seconds_per_sample": latency_seconds,
              "latency_scope": "classifier.predict only (excludes preprocessing/vectorizer)",
              "not_gold_test": True, "confidence_calibrated": False}
    data = {"format_version": MODEL_FORMAT, "vectorizer": {k: cfg["vectorizer"][k] for k in
             ("analyzer", "ngram_range", "sublinear_tf", "lowercase")},
            "vocabulary": {k: int(v) for k, v in vectorizer.vocabulary_.items()}, "idf": vectorizer.idf_.tolist(),
            "weights": classifier.coef_.tolist(), "intercepts": classifier.intercept_.tolist(),
            "classes": classifier.classes_.tolist()}
    serialized = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    config_hash = sha256(json.dumps(cfg, sort_keys=True).encode("utf-8")).hexdigest()
    report_bytes = (json.dumps(report, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    manifest = {"manifest_version": "model-release-v1", "model_version": model_version,
                "model_identifier": "tfidf-linear-svc-baseline", "artifact_filename": "classifier.json",
                "artifact_sha256": sha256(serialized).hexdigest(), "artifact_format": MODEL_FORMAT,
                "preprocessor_version": PREPROCESSOR_VERSION, "taxonomy_version": taxonomy_version,
                "dataset_fingerprint": dataset_fingerprint, "training_config_sha256": config_hash,
                "evaluation_reference": "validation-report.json", "evaluation_sha256": sha256(report_bytes).hexdigest(),
                "dependency_version": f"scikit-learn-{sklearn.__version__}",
                "provenance_reference": authorization_reference, "tokenizer_version": None,
                "tokenizer_sha256": None, "decision_policy_version": None}
    root.mkdir(parents=True, exist_ok=False)
    (root / "classifier.json").write_bytes(serialized)
    (root / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (root / "validation-report.json").write_bytes(report_bytes)
    restored = TfidfLinearModel.from_verified_release(root, taxonomy_version=taxonomy_version)
    if [r.category_code for r in restored.predict([v.text for v in validation])] != list(predictions):
        raise RuntimeError("Serialized baseline disagrees with training estimator")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a permitted baseline without touching Gold Test")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--approved-codes", type=Path, required=True)
    parser.add_argument("--audit-manifest", type=Path, required=True)
    parser.add_argument("--release-dir", type=Path, required=True)
    parser.add_argument("--authorization-reference", required=True)
    parser.add_argument("--taxonomy-version", required=True)
    parser.add_argument("--model-version", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--ratios", type=float, nargs=3, required=True)
    parser.add_argument("--temporal", action="store_true")
    parser.add_argument("--max-features", type=int, default=200000)
    args = parser.parse_args()
    try:
        key = bytes.fromhex(os.environ.get("DATASET_FINGERPRINT_KEY_HEX", ""))
        codes = json.loads(args.approved_codes.read_text(encoding="utf-8"))
        if not isinstance(codes, list) or not codes or any(not isinstance(c, str) or not c for c in codes):
            raise DatasetValidationError("Invalid approved-code catalog")
        with args.input.open("r", encoding="utf-8") as handle:
            records = parse_records(handle, approved_codes=set(codes), label_mode="single-label",
                                    taxonomy_version=args.taxonomy_version)
        ratios = tuple(args.ratios)
        splits = split_records(records, seed=args.seed, ratios=ratios, temporal=args.temporal)
        expected = build_private_manifest(splits, fingerprint_key=key,
            authorization_reference=args.authorization_reference, taxonomy_version=args.taxonomy_version,
            label_mode="single-label", seed=args.seed, ratios=ratios, temporal=args.temporal)
        frozen = json.loads(args.audit_manifest.read_text(encoding="utf-8"))
        if frozen != expected:
            raise DatasetValidationError("Frozen audit manifest does not match training input/split")
        report = train_baseline(splits["train"], splits["validation"],
             release_dir=args.release_dir, model_version=args.model_version,
             taxonomy_version=args.taxonomy_version,
             dataset_fingerprint=expected["splits"]["train"]["hmac_sha256"],
             authorization_reference=args.authorization_reference, seed=args.seed,
             max_features=args.max_features)
    except (OSError, ValueError, RuntimeError, ImportError):
        parser.exit(2, "Baseline training failed: invalid input, environment or incompatible artifact\n")
    print(json.dumps({"status": "validation_only", "trained_model_version": args.model_version,
        "macro_f1": report["macro_f1"], "release_dir": str(args.release_dir)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
