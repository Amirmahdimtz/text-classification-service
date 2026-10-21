import argparse
import json
import pytest
from tools.prepare_dataset import run
from src.core.services.text_classification.dataset_preparation import DatasetValidationError


def test_offline_dataset_audit_outside_checkout(tmp_path, monkeypatch):
    monkeypatch.setenv("DATASET_FINGERPRINT_KEY_HEX", "ff" * 32)
    source = tmp_path / "reports.jsonl"
    with source.open("w", encoding="utf-8") as handle:
        for i in range(9):
            handle.write(json.dumps({"report_id": f"r{i}", "group_id": f"e{i}",
                "text": f"متن ساختگی فقط برای تست {i}", "labels": ["TEST"],
                "taxonomy_version": "test-release"}, ensure_ascii=False) + "\n")
    codes = tmp_path / "codes.json"
    codes.write_text('["TEST"]')
    output = tmp_path / "audit.json"
    args = argparse.Namespace(input=source, approved_codes=codes, output=output,
        authorization_reference="test-only", taxonomy_version="test-release", label_mode="single-label",
        ratios=[0.6, 0.2, 0.2], seed=10, temporal=False)
    result = run(args)
    assert result["records"] == 9
    assert json.loads(output.read_text())["schema_version"] == "dataset-audit-v1"
    with pytest.raises(DatasetValidationError, match="overwrite"):
        run(args)
    monkeypatch.delenv("DATASET_FINGERPRINT_KEY_HEX")
    with pytest.raises(DatasetValidationError, match="KEY"):
        run(args)
