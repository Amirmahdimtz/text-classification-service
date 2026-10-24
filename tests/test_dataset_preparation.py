from datetime import datetime, timezone
import json
import pytest

from src.core.services.text_classification.dataset_preparation import (
    DatasetRecord, DatasetValidationError, build_private_manifest,
    parse_records, split_records,
)


CODES = {"category-a", "category-b"}  # TEST FIXTURE ONLY, never business taxonomy.


def _records(n=12):
    return tuple(DatasetRecord(str(i), str(i), f"Unrelated subject {i} distinctive", ("category-a",), None) for i in range(n))


def test_parse_validates_taxonomy_and_cardinality():
    row = {"report_id": "1", "group_id": "event-1", "text": "نمونه متن آزمون", "labels": ["category-a"], "taxonomy_version": "test-v1"}
    records = parse_records([json.dumps(row, ensure_ascii=False)], approved_codes=CODES,
                            label_mode="single-label", taxonomy_version="test-v1")
    assert records[0].text == row["text"]
    with pytest.raises(DatasetValidationError, match="duplicate ID"):
        parse_records([json.dumps(row)] * 2, approved_codes=CODES,
                      label_mode="single-label", taxonomy_version="test-v1")
    row["labels"] = ["category-a", "category-b"]
    with pytest.raises(DatasetValidationError):
        parse_records([json.dumps(row)], approved_codes=CODES,
                      label_mode="single-label", taxonomy_version="test-v1")
    assert len(parse_records([json.dumps(row)], approved_codes=CODES,
                             label_mode="multi-label", taxonomy_version="test-v1")) == 1


def test_group_duplicate_and_near_duplicate_cannot_leak():
    records = list(_records())
    records[1] = DatasetRecord("1", "0", "Group sibling", ("category-a",), None)
    records[5] = DatasetRecord("5", "5", records[2].text, ("category-a",), None)
    records[7] = DatasetRecord("7", "7", "this is a long report detailing a specific event with evidence",
                               ("category-a",), None)
    records[8] = DatasetRecord("8", "8", "this is a long report detailing a specific event with evidence!",
                               ("category-a",), None)
    splits = split_records(tuple(records), seed=42, ratios=(0.6, 0.2, 0.2))
    def bucket(identifier):
        return next(name for name, rows in splits.items() if identifier in {row.report_id for row in rows})
    assert bucket("0") == bucket("1")
    assert bucket("2") == bucket("5")
    assert bucket("7") == bucket("8")
    again = split_records(tuple(records), seed=42, ratios=(0.6, 0.2, 0.2))
    assert splits == again
    assert len({r.report_id for batch in splits.values() for r in batch}) == len(records)


def test_conflicting_exact_annotation_fails_closed():
    items = list(_records())
    items[1] = DatasetRecord("1", "1", items[0].text, ("category-b",), None)
    with pytest.raises(DatasetValidationError, match="Conflicting"):
        split_records(tuple(items), seed=1, ratios=(0.5, 0.25, 0.25))


def test_temporal_split_and_missing_time():
    with pytest.raises(DatasetValidationError, match="event time"):
        split_records(_records(), seed=1, ratios=(0.5, 0.25, 0.25), temporal=True)
    dates = tuple(DatasetRecord(str(i), str(i), f"t {i}", ("category-a",),
                   datetime(2026, 1, i + 1, tzinfo=timezone.utc)) for i in range(8))
    output = split_records(dates, seed=1, ratios=(0.5, 0.25, 0.25), temporal=True)
    assert max(r.occurred_at for r in output["train"]) < min(r.occurred_at for r in output["validation"])
    assert max(r.occurred_at for r in output["validation"]) < min(r.occurred_at for r in output["test"])



def test_temporal_split_relocates_boundaries_for_spanning_group():
    # An incident beginning on day 1 and ending on day 6 must not appear in
    # VALIDATION while TRAIN contains days 2..5 (the previous algorithm did).
    days = [(1, "spanning"), (2, "two"), (3, "three"), (4, "four"),
            (5, "five"), (6, "spanning"), (7, "seven"), (8, "eight"),
            (9, "nine")]
    records = tuple(DatasetRecord(str(index), group, f"unique {index}",
                    ("category-a",), datetime(2026, 1, day, tzinfo=timezone.utc))
                    for index, (day, group) in enumerate(days))
    splits = split_records(records, seed=17, ratios=(0.5, 0.25, 0.25), temporal=True)
    assert all(splits[name] for name in ("train", "validation", "test"))
    assert max(r.occurred_at for r in splits["train"]) < min(r.occurred_at for r in splits["validation"])
    assert max(r.occurred_at for r in splits["validation"]) < min(r.occurred_at for r in splits["test"])
    assert sum(r.group_id == "spanning" for r in splits["train"]) == 2
    assert splits == split_records(records, seed=17, ratios=(0.5, 0.25, 0.25), temporal=True)


def test_temporal_split_rejects_irreconcilable_intervals_and_tied_times():
    days = [(1, "long"), (2, "two"), (3, "three"), (4, "four"),
            (5, "five"), (6, "six"), (7, "seven"), (8, "eight"), (9, "long")]
    records = tuple(DatasetRecord(str(index), group, f"unique {index}",
                    ("category-a",), datetime(2026, 1, day, tzinfo=timezone.utc))
                    for index, (day, group) in enumerate(days))
    with pytest.raises(DatasetValidationError, match="strictly chronological"):
        split_records(records, seed=9, ratios=(0.5, 0.25, 0.25), temporal=True)
    tied = tuple(DatasetRecord(str(i), f"group-{i}", f"unique {i}",
                 ("category-a",), datetime(2026, 1, 1, tzinfo=timezone.utc)) for i in range(8))
    with pytest.raises(DatasetValidationError, match="strictly chronological"):
        split_records(tied, seed=9, ratios=(0.5, 0.25, 0.25), temporal=True)

def test_manifest_hmac_counts_without_report_text_or_ids():
    splits = split_records(_records(), seed=99, ratios=(0.5, 0.25, 0.25))
    kwargs = dict(fingerprint_key=b"a" * 32, authorization_reference="approved-test-ref",
                  taxonomy_version="test-v1", label_mode="single-label", seed=99,
                  ratios=(0.5, 0.25, 0.25), temporal=False)
    manifest = build_private_manifest(splits, **kwargs)
    assert manifest == build_private_manifest(splits, **kwargs)
    assert manifest["splits"]["test"]["count"] > 0
    assert manifest["splits"]["train"]["p95_codepoints"] > 0
    assert manifest["splits"]["train"]["p50_whitespace_tokens"] >= 1
    assert manifest["splits"]["train"]["script_counts_heuristic"]["latin"] > 0
    assert "Unrelated subject" not in str(manifest)
    with pytest.raises(DatasetValidationError):
        build_private_manifest(splits, **{**kwargs, "fingerprint_key": b"weak"})


def test_budget_fail_closed_instead_of_skipping_comparisons():
    items = tuple(DatasetRecord(str(i), str(i), f"common common common common {i}",
                                ("category-a",), None) for i in range(10))
    with pytest.raises(DatasetValidationError, match="budget"):
        split_records(items, seed=1, ratios=(0.5, 0.25, 0.25), max_candidates=1)
