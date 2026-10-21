import pytest

sklearn = pytest.importorskip("sklearn")  # Optional SERVER_MODEL dependency.
from src.core.services.text_classification.dataset_preparation import DatasetRecord, DatasetValidationError
from src.infrastructure.ml.tfidf_linear_model import TfidfLinearModel
from tools.train_baseline import train_baseline


def test_reproducible_json_baseline_and_margin_contract(tmp_path):
    train = tuple(DatasetRecord(f"tr-{i}", f"tr-g-{i}",
         "سیستم نرم افزار سرور و شبکه سالم است" if i % 2 else "کتاب شعر داستان ادبیات و فرهنگ",
         ("TEST_SOFTWARE",) if i % 2 else ("TEST_LITERATURE",), None) for i in range(12))
    valid = tuple(DatasetRecord(f"val-{i}", f"val-g-{i}",
         "سیستم شبکه و سرور" if i % 2 else "داستان شعر و کتاب",
         ("TEST_SOFTWARE",) if i % 2 else ("TEST_LITERATURE",), None) for i in range(4))
    kwargs = dict(model_version="test-model", taxonomy_version="test-taxonomy",
                  dataset_fingerprint="0" * 64, authorization_reference="test-fixture",
                  seed=123, max_features=250)
    report = train_baseline(train, valid, release_dir=tmp_path / "release1", **kwargs)
    model = TfidfLinearModel.from_verified_release(tmp_path / "release1", taxonomy_version="test-taxonomy")
    predictions = model.predict([v.text for v in valid])
    assert all(x.score_type == "linear_svc_selected_class_margin" and x.confidence is None for x in predictions)
    assert all(x.category_code in {"TEST_LITERATURE", "TEST_SOFTWARE"} for x in predictions)
    assert report["evaluation_split"] == "validation" and report["not_gold_test"]
    other = train_baseline(train, valid, release_dir=tmp_path / "release2", **kwargs)
    assert other["confusion_matrix"] == report["confusion_matrix"]
    assert (tmp_path / "release1" / "classifier.json").read_bytes() == (tmp_path / "release2" / "classifier.json").read_bytes()
    with pytest.raises(DatasetValidationError, match="overwrite"):
        train_baseline(train, valid, release_dir=tmp_path / "release1", **kwargs)
