from hashlib import sha256
import json
import pytest

from src.infrastructure.ml.artifact_manifest import ArtifactValidationError, load_verified_manifest
from src.core.services.text_classification.text_preprocessor import PREPROCESSOR_VERSION


def _release(tmp_path):
    payload = b'{"format_version":"tfidf-linear-json-v1"}'  # Test-only, not a runnable model.
    (tmp_path / "classifier.json").write_bytes(payload)
    digest = sha256(payload).hexdigest()
    manifest = {
        "manifest_version": "model-release-v1", "model_version": "test-model-1",
        "model_identifier": "test-only", "artifact_filename": "classifier.json",
        "artifact_sha256": digest, "artifact_format": "tfidf-linear-json-v1",
        "preprocessor_version": PREPROCESSOR_VERSION, "taxonomy_version": "test-tx-1",
        "dataset_fingerprint": digest, "training_config_sha256": digest,
        "evaluation_reference": "local-test-only", "dependency_version": "sklearn-test",
        "provenance_reference": "test-fixture", "tokenizer_version": None,
        "tokenizer_sha256": None, "decision_policy_version": None,
    }
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return manifest


def _verify(path):
    return load_verified_manifest(path, expected_taxonomy_version="test-tx-1",
                                  expected_preprocessor_version=PREPROCESSOR_VERSION)


def test_valid_manifest_and_hash(tmp_path):
    data = _release(tmp_path)
    result = _verify(tmp_path)
    assert result.artifact_sha256 == data["artifact_sha256"]
    assert result.decision_policy_version is None


def test_tampered_artifact_and_taxonomy_rejected(tmp_path):
    _release(tmp_path)
    (tmp_path / "classifier.json").write_text("tampered")
    with pytest.raises(ArtifactValidationError, match="integrity"):
        _verify(tmp_path)
    with pytest.raises(ArtifactValidationError, match="Taxonomy"):
        load_verified_manifest(tmp_path, expected_taxonomy_version="wrong",
                               expected_preprocessor_version=PREPROCESSOR_VERSION)


def test_path_traversal_and_unsafe_files_rejected(tmp_path):
    manifest = _release(tmp_path)
    manifest["artifact_filename"] = "../outside.json"
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(ArtifactValidationError, match="filename"):
        _verify(tmp_path)


def test_missing_metadata_and_invalid_tokenizer_rejected(tmp_path):
    manifest = _release(tmp_path)
    del manifest["provenance_reference"]
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(ArtifactValidationError, match="missing"):
        _verify(tmp_path)
    manifest["provenance_reference"] = "test-only"
    manifest["tokenizer_version"] = "tok-v1"
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(ArtifactValidationError, match="Tokenizer"):
        _verify(tmp_path)
