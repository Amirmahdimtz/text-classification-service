"""Fail-closed, content-addressed ML release manifest validation.

Loading verifies artifact integrity and declared compatibility; it is not a
cryptographic signature or independent verification of dataset provenance.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import re


class ArtifactValidationError(ValueError):
    """Malformed, tampered, missing or incompatible release."""


_HEX_SHA256 = re.compile(r"[0-9a-f]{64}\Z")


@dataclass(frozen=True)
class ArtifactManifest:
    manifest_version: str
    model_version: str
    model_identifier: str
    artifact_filename: str
    artifact_sha256: str
    artifact_format: str
    preprocessor_version: str
    taxonomy_version: str
    dataset_fingerprint: str
    training_config_sha256: str
    evaluation_reference: str
    evaluation_sha256: str
    dependency_version: str
    provenance_reference: str
    tokenizer_version: str | None
    tokenizer_sha256: str | None
    decision_policy_version: str | None


def _validate_release_name(name: str) -> bool:
    return bool(name and name not in (".", "..") and Path(name).name == name and
                "/" not in name and "\\" not in name and "\x00" not in name)


def load_verified_manifest(release_dir: Path, *, expected_taxonomy_version: str,
                           expected_preprocessor_version: str,
                           expected_format: str = "tfidf-linear-json-v1",
                           max_artifact_bytes: int = 256 * 1024 * 1024) -> ArtifactManifest:
    """Only relative, regular, size-bounded artifacts within release_dir are allowed."""
    if not expected_taxonomy_version or not expected_preprocessor_version or max_artifact_bytes <= 0:
        raise ArtifactValidationError("Expected compatibility parameters required")
    root = Path(release_dir).resolve(strict=True)
    try:
        metadata_file = root / "manifest.json"
        if metadata_file.is_symlink() or metadata_file.stat().st_size > 65536:
            raise ArtifactValidationError("Manifest is unsafe or too large")
        data = json.loads(metadata_file.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ArtifactValidationError("Manifest must be a mapping")
        required = ("manifest_version", "model_version", "model_identifier", "artifact_filename",
                    "artifact_sha256", "artifact_format", "preprocessor_version",
                    "taxonomy_version", "dataset_fingerprint", "training_config_sha256",
                    "evaluation_reference", "evaluation_sha256", "dependency_version", "provenance_reference")
        if any(not isinstance(data.get(k), str) or not data[k].strip() for k in required):
            raise ArtifactValidationError("Manifest has missing required metadata")
        if data["manifest_version"] != "model-release-v1":
            raise ArtifactValidationError("Unsupported manifest version")
        if data["taxonomy_version"] != expected_taxonomy_version or data["preprocessor_version"] != expected_preprocessor_version:
            raise ArtifactValidationError("Taxonomy or preprocessing mismatch")
        if data["artifact_format"] != expected_format:
            raise ArtifactValidationError("Unapproved artifact format")
        if not _validate_release_name(data["artifact_filename"]) or data["artifact_filename"] == "manifest.json":
            raise ArtifactValidationError("Invalid artifact filename")
        for key in ("artifact_sha256", "dataset_fingerprint", "training_config_sha256", "evaluation_sha256"):
            if not _HEX_SHA256.fullmatch(data[key]):
                raise ArtifactValidationError("Invalid fingerprint format")
        for key in ("tokenizer_version", "tokenizer_sha256", "decision_policy_version"):
            if data.get(key) is not None and (not isinstance(data[key], str) or not data[key].strip()):
                raise ArtifactValidationError("Invalid optional version field")
        if bool(data.get("tokenizer_version")) != bool(data.get("tokenizer_sha256")):
            raise ArtifactValidationError("Tokenizer identity must include both version and hash")
        if data.get("tokenizer_sha256") and not _HEX_SHA256.fullmatch(data["tokenizer_sha256"]):
            raise ArtifactValidationError("Invalid tokenizer hash")
        artifact = root / data["artifact_filename"]
        if artifact.is_symlink() or not artifact.is_file() or artifact.resolve(strict=True).parent != root:
            raise ArtifactValidationError("Artifact must be a regular file in release directory")
        size = artifact.stat().st_size
        if size == 0 or size > max_artifact_bytes:
            raise ArtifactValidationError("Artifact size invalid")
        digest = sha256()
        with artifact.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
        if digest.hexdigest() != data["artifact_sha256"]:
            raise ArtifactValidationError("Artifact integrity mismatch")
        if not _validate_release_name(data["evaluation_reference"]):
            raise ArtifactValidationError("Invalid evaluation report filename")
        evaluation = root / data["evaluation_reference"]
        if evaluation.is_symlink() or not evaluation.is_file() or evaluation.resolve(strict=True).parent != root or evaluation.stat().st_size > 8 * 1024 * 1024:
            raise ArtifactValidationError("Evaluation report missing or unsafe")
        if sha256(evaluation.read_bytes()).hexdigest() != data["evaluation_sha256"]:
            raise ArtifactValidationError("Evaluation report integrity mismatch")
        return ArtifactManifest(**{k: data.get(k) for k in ArtifactManifest.__dataclass_fields__})
    except (OSError, ValueError, TypeError, UnicodeError) as exc:
        if isinstance(exc, ArtifactValidationError):
            raise
        raise ArtifactValidationError("Cannot validate model release") from None
