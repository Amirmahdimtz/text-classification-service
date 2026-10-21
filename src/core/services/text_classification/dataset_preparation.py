"""Data-governed offline profiling, overlap audit and reproducible dataset splitting.

Never writes raw reports or per-report hashes into a public manifest.
Approval, label semantics and split ratios are explicit inputs, not defaults.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
import hmac
import json
import math
import re
from typing import Iterable

from src.core.services.text_classification.text_preprocessor import preprocess_text, PREPROCESSOR_VERSION


class DatasetValidationError(ValueError):
    """Input invalid, unauthorized or potentially leaking between partitions."""


@dataclass(frozen=True)
class DatasetRecord:
    report_id: str
    group_id: str
    text: str
    labels: tuple[str, ...]
    occurred_at: datetime | None


def parse_records(lines: Iterable[str], *, approved_codes: set[str],
                  label_mode: str, taxonomy_version: str) -> tuple[DatasetRecord, ...]:
    if label_mode not in ("single-label", "multi-label"):
        raise DatasetValidationError("Explicit approved label_mode required")
    if not approved_codes or not taxonomy_version.strip():
        raise DatasetValidationError("Approved category codes and taxonomy version required")
    records: list[DatasetRecord] = []
    seen_ids: set[str] = set()
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except (ValueError, TypeError) as exc:
            raise DatasetValidationError(f"Invalid JSON at line {line_number}") from exc
        if not isinstance(row, dict):
            raise DatasetValidationError(f"Invalid record at line {line_number}")
        rid, gid, content, labels = (row.get(k) for k in ("report_id", "group_id", "text", "labels"))
        if (not isinstance(rid, str) or not rid.strip() or rid in seen_ids or
            not isinstance(gid, str) or not gid.strip() or
            not isinstance(content, str) or not content.strip() or
            not isinstance(labels, list) or not labels or
            any(not isinstance(label, str) or label not in approved_codes for label in labels) or
            len(set(labels)) != len(labels) or
            (label_mode == "single-label" and len(labels) != 1)):
            raise DatasetValidationError(f"Invalid fields/labels or duplicate ID at line {line_number}")
        if row.get("taxonomy_version") != taxonomy_version:
            raise DatasetValidationError(f"Taxonomy mismatch at line {line_number}")
        occurred = None
        if row.get("occurred_at") is not None:
            try:
                occurred = datetime.fromisoformat(row["occurred_at"])
                if occurred.tzinfo is None or occurred.utcoffset() is None:
                    raise ValueError("Offset required")
            except (ValueError, TypeError) as exc:
                raise DatasetValidationError(f"Invalid occurred_at at line {line_number}") from exc
        records.append(DatasetRecord(rid, gid, content, tuple(sorted(labels)), occurred))
        seen_ids.add(rid)
    if not records:
        raise DatasetValidationError("Empty dataset")
    return tuple(records)


def _shingles(text: str) -> frozenset[str]:
    tokens = re.findall(r"[^\W_]+", text.lower(), flags=re.UNICODE)
    if len(tokens) < 4:
        return frozenset()
    return frozenset(" ".join(tokens[i:i + 3]) for i in range(len(tokens) - 2))


def split_records(records: tuple[DatasetRecord, ...], *, seed: int,
                  ratios: tuple[float, float, float], temporal: bool = False,
                  similarity_threshold: float = 0.9,
                  max_candidates: int = 2_000_000) -> dict[str, tuple[DatasetRecord, ...]]:
    """Join incident/duplicate/near-duplicate components BEFORE assigning splits.

    Similarity is token 3-shingle Jaccard and deliberately limited to >=4 tokens.
    Exceeding candidate safety budget raises rather than silently skipping pairs.
    """
    if not records or not isinstance(seed, int) or any(not math.isfinite(r) or r <= 0 for r in ratios) or len(ratios) != 3 or abs(sum(ratios) - 1) > 1e-9:
        raise DatasetValidationError("Three positive split ratios summing to 1 and a seed required")
    if not 0 < similarity_threshold <= 1 or max_candidates < 1:
        raise DatasetValidationError("Invalid similarity audit bounds")
    if temporal and any(record.occurred_at is None for record in records):
        raise DatasetValidationError("Temporal split requires an aware event time for every record")
    parents = list(range(len(records)))

    def root(i: int) -> int:
        while parents[i] != i:
            parents[i] = parents[parents[i]]
            i = parents[i]
        return i

    def union(i: int, j: int) -> None:
        a, b = root(i), root(j)
        if a != b:
            parents[max(a, b)] = min(a, b)

    by_group: dict[str, int] = {}
    by_exact: dict[str, tuple[int, tuple[str, ...]]] = {}
    inverted: dict[str, list[int]] = defaultdict(list)
    shingles_cache: list[frozenset[str]] = []
    comparisons = 0
    for index, record in enumerate(records):
        prev_group = by_group.setdefault(record.group_id, index)
        union(index, prev_group)
        norm = preprocess_text(record.text).normalized_text
        digest = sha256(norm.encode("utf-8")).hexdigest()
        existing = by_exact.get(digest)
        if existing is not None:
            if existing[1] != record.labels:
                raise DatasetValidationError("Conflicting annotations for exact duplicate text")
            union(index, existing[0])
        else:
            by_exact[digest] = (index, record.labels)
        shingles = _shingles(norm)
        candidate_indices: set[int] = set()
        for item in shingles:
            candidate_indices.update(inverted[item])
        comparisons += len(candidate_indices)
        if comparisons > max_candidates:
            raise DatasetValidationError("Near-duplicate candidate budget exceeded; manual audit required")
        for other in candidate_indices:
            previous = shingles_cache[other]
            similarity = len(previous & shingles) / len(previous | shingles)
            if similarity >= similarity_threshold:
                union(index, other)
        shingles_cache.append(shingles)
        for item in shingles:
            inverted[item].append(index)
    components: dict[int, list[int]] = defaultdict(list)
    for i in range(len(records)):
        components[root(i)].append(i)
    groups = list(components.values())
    if len(groups) < 3:
        raise DatasetValidationError("Insufficient independent groups for three-way split")
    if temporal:
        groups.sort(key=lambda g: (max(records[i].occurred_at for i in g), min(records[i].report_id for i in g)))
    else:
        groups.sort(key=lambda g: sha256(f"{seed}:{min(records[i].report_id for i in g)}".encode()).digest())
    n = len(groups)
    train_end = max(1, min(n - 2, round(n * ratios[0])))
    validation_end = max(train_end + 1, min(n - 1, round(n * (ratios[0] + ratios[1]))))
    split_group_sets = (groups[:train_end], groups[train_end:validation_end], groups[validation_end:])
    output = {}
    for name, subset in zip(("train", "validation", "test"), split_group_sets):
        output[name] = tuple(records[i] for g in subset for i in g)
        if not output[name]:
            raise DatasetValidationError("Empty split")
    return output


def build_private_manifest(splits: dict[str, tuple[DatasetRecord, ...]], *,
                           fingerprint_key: bytes, authorization_reference: str,
                           taxonomy_version: str, label_mode: str,
                           seed: int, ratios: tuple[float, float, float], temporal: bool) -> dict:
    if len(fingerprint_key) < 32 or not authorization_reference.strip() or not taxonomy_version.strip():
        raise DatasetValidationError("Strong HMAC key and authorization/taxonomy references required")
    manifest = {
        "schema_version": "dataset-audit-v1", "preprocessor_version": PREPROCESSOR_VERSION,
        "authorization_reference": authorization_reference, "taxonomy_version": taxonomy_version,
        "label_mode": label_mode, "seed": seed, "ratios": list(ratios), "temporal": temporal,
        "splits": {},
    }
    for name in ("train", "validation", "test"):
        if not splits.get(name):
            raise DatasetValidationError("Required split is missing or empty")
        records = splits[name]
        canonical = json.dumps(sorted([
            [r.report_id, r.group_id, r.text, list(r.labels), r.occurred_at.isoformat() if r.occurred_at else None]
            for r in records
        ]), ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        fingerprint = hmac.new(fingerprint_key, canonical, "sha256").hexdigest()
        counts = Counter(label for record in records for label in record.labels)
        manifest["splits"][name] = {
            "count": len(records), "label_counts": dict(sorted(counts.items())),
            "min_codepoints": min(len(r.text) for r in records),
            "max_codepoints": max(len(r.text) for r in records),
            "hmac_sha256": fingerprint,
        }
    return manifest
