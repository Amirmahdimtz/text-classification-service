"""Portable, JSON-only TF-IDF + LinearSVC baseline; scores are raw margins.

No pickle, joblib or arbitrary executable deserialization is accepted.
This is a benchmark candidate, not an approved final classifier.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from src.core.services.text_classification.text_preprocessor import preprocess_text, PREPROCESSOR_VERSION
from src.infrastructure.ml.artifact_manifest import load_verified_manifest, ArtifactValidationError


MODEL_FORMAT = "tfidf-linear-json-v1"


@dataclass(frozen=True)
class RawPrediction:
    category_code: str
    raw_margin: float
    score_type: str = "linear_svc_selected_class_margin"
    confidence: None = None


class TfidfLinearModel:
    def __init__(self, vectorizer, weights, intercepts, classes: tuple[str, ...]):
        self._vectorizer = vectorizer
        self._weights = weights
        self._intercepts = intercepts
        self._classes = classes

    @classmethod
    def from_verified_release(cls, release_dir: Path, *, taxonomy_version: str) -> "TfidfLinearModel":
        import numpy as np
        from sklearn.feature_extraction.text import TfidfVectorizer

        manifest = load_verified_manifest(
            release_dir, expected_taxonomy_version=taxonomy_version,
            expected_preprocessor_version=PREPROCESSOR_VERSION, expected_format=MODEL_FORMAT,
        )
        data = json.loads((Path(release_dir) / manifest.artifact_filename).read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("format_version") != MODEL_FORMAT:
            raise ArtifactValidationError("Invalid baseline model format")
        params = data.get("vectorizer")
        if not isinstance(params, dict) or params.get("analyzer") != "char" or params.get("ngram_range") != [2, 5] or params.get("sublinear_tf") is not True or params.get("lowercase") is not False:
            raise ArtifactValidationError("Incompatible TF-IDF configuration")
        vocab = data.get("vocabulary")
        classes = data.get("classes")
        if not isinstance(vocab, dict) or not vocab or not isinstance(classes, list) or len(classes) < 2 or len(set(classes)) != len(classes) or any(not isinstance(x, str) or not x for x in classes):
            raise ArtifactValidationError("Invalid class identities or vocabulary")
        if not all(isinstance(k, str) and isinstance(v, int) for k, v in vocab.items()) or sorted(vocab.values()) != list(range(len(vocab))):
            raise ArtifactValidationError("Non-contiguous vocabulary")
        idf = np.asarray(data.get("idf"), dtype=np.float64)
        weights = np.asarray(data.get("weights"), dtype=np.float64)
        biases = np.asarray(data.get("intercepts"), dtype=np.float64)
        nrows = 1 if len(classes) == 2 else len(classes)
        if idf.shape != (len(vocab),) or weights.shape != (nrows, len(vocab)) or biases.shape != (nrows,) or not all(np.isfinite(v).all() for v in (idf, weights, biases)):
            raise ArtifactValidationError("Invalid baseline tensor dimensions/values")
        if np.any(idf <= 0):
            raise ArtifactValidationError("Invalid inverse document frequency")
        vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 5),
                                     sublinear_tf=True, lowercase=False, vocabulary=vocab)
        vectorizer.idf_ = idf
        return cls(vectorizer, weights, biases, tuple(classes))

    def predict(self, texts: list[str]) -> list[RawPrediction]:
        import numpy as np
        if not texts or any(not isinstance(x, str) or not x.strip() for x in texts):
            raise ValueError("A non-empty batch of non-empty Unicode texts is required")
        normalized = [preprocess_text(text).normalized_text for text in texts]
        x = self._vectorizer.transform(normalized)
        margins = np.asarray(x @ self._weights.T + self._intercepts)
        if len(self._classes) == 2:
            flat = margins[:, 0]
            indexes = (flat > 0).astype(int)
            strengths = abs(flat)
        else:
            indexes = margins.argmax(axis=1)
            strengths = margins[np.arange(len(texts)), indexes]
        return [RawPrediction(self._classes[int(i)], float(score)) for i, score in zip(indexes, strengths)]
