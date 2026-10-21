"""Authorized local-only dataset audit. No dataset is uploaded or committed."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from src.core.services.text_classification.dataset_preparation import (
    DatasetValidationError, parse_records, split_records, build_private_manifest,
)


def run(args: argparse.Namespace) -> dict:
    repo = Path(__file__).resolve().parents[1]
    input_path = args.input.resolve(strict=True)
    codes_path = args.approved_codes.resolve(strict=True)
    destination = args.output.resolve()
    if repo == destination or repo in destination.parents:
        raise DatasetValidationError("Refusing to write dataset metadata inside public repository")
    if not args.authorization_reference.strip() or not args.taxonomy_version.strip():
        raise DatasetValidationError("Authorization and approved taxonomy reference required")
    raw_key = os.environ.get("DATASET_FINGERPRINT_KEY_HEX", "")
    try:
        key = bytes.fromhex(raw_key)
    except ValueError:
        key = b""
    if len(key) < 32:
        raise DatasetValidationError("DATASET_FINGERPRINT_KEY_HEX must hold at least 32 secret bytes")
    codes = json.loads(codes_path.read_text(encoding="utf-8"))
    if not isinstance(codes, list) or any(not isinstance(c, str) or not c for c in codes) or len(set(codes)) != len(codes):
        raise DatasetValidationError("Approved codes must be a unique list of non-empty strings")
    with input_path.open("r", encoding="utf-8") as handle:
        records = parse_records(handle, approved_codes=set(codes), label_mode=args.label_mode,
                                taxonomy_version=args.taxonomy_version)
    ratios = tuple(args.ratios)
    splits = split_records(records, seed=args.seed, ratios=ratios, temporal=args.temporal)
    manifest = build_private_manifest(splits, fingerprint_key=key,
                                      authorization_reference=args.authorization_reference,
                                      taxonomy_version=args.taxonomy_version, label_mode=args.label_mode,
                                      seed=args.seed, ratios=ratios, temporal=args.temporal)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise DatasetValidationError("Refusing to overwrite existing audit manifest")
    with destination.open("x", encoding="utf-8") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return {"status": "completed", "records": len(records), "manifest_path": str(destination)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Privately audit an approved local JSONL dataset")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--approved-codes", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--authorization-reference", required=True)
    parser.add_argument("--taxonomy-version", required=True)
    parser.add_argument("--label-mode", choices=("single-label", "multi-label"), required=True)
    parser.add_argument("--ratios", type=float, nargs=3, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--temporal", action="store_true")
    args = parser.parse_args()
    try:
        result = run(args)
    except (OSError, ValueError, json.JSONDecodeError):
        parser.exit(2, "Dataset audit failed: invalid input, authorization or split configuration\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
