"""Mechanically verified original-text evidence; never infers category relevance.

Offsets are zero-based, half-open Unicode code-point indexes. Proposals are
untrusted normalized intervals with an exact normalized quote. This service
only establishes literal text provenance, not semantic or model correctness.
"""
from __future__ import annotations

from dataclasses import dataclass

from src.core.services.text_classification.text_preprocessor import (
    PREPROCESSOR_VERSION,
    PreprocessedText,
    preprocess_text,
)
from src.infrastructure.di.inject import inject


class EvidenceValidationError(ValueError):
    """An evidence proposal or an existing evidence record is not trustworthy."""


@dataclass(frozen=True, slots=True)
class EvidenceCandidate:
    normalized_start: int
    normalized_end: int
    normalized_quote: str


@dataclass(frozen=True, slots=True)
class VerifiedEvidence:
    start: int
    end: int
    quote: str
    normalized_start: int
    normalized_end: int
    preprocessor_version: str


_MAX_EVIDENCE_ITEMS = 64  # Resource limit for this internal operation, not a business threshold.


@inject
class EvidenceService:
    """Restore and validate original quotes from independently proposed spans."""

    def __init__(self) -> None:
        pass

    @staticmethod
    def _source(processed: PreprocessedText) -> PreprocessedText:
        if type(processed) is not PreprocessedText or processed.version != PREPROCESSOR_VERSION:
            raise EvidenceValidationError("Invalid preprocessing version or source")
        # Defend against caller-supplied altered offsets, text or normalized content.
        if processed != preprocess_text(processed.original_text):
            raise EvidenceValidationError("Preprocessed source integrity mismatch")
        return processed

    def extract(self, processed: PreprocessedText,
                candidates: list[EvidenceCandidate] | tuple[EvidenceCandidate, ...]) -> tuple[VerifiedEvidence, ...]:
        source = self._source(processed)
        if not isinstance(candidates, (list, tuple)) or len(candidates) > _MAX_EVIDENCE_ITEMS:
            raise EvidenceValidationError("Invalid evidence collection")
        result: list[VerifiedEvidence] = []
        seen: set[tuple[int, int]] = set()
        for candidate in candidates:
            if type(candidate) is not EvidenceCandidate:
                raise EvidenceValidationError("Invalid evidence candidate")
            start, end = candidate.normalized_start, candidate.normalized_end
            if type(start) is not int or type(end) is not int or not (0 <= start < end <= len(source.normalized_text)):
                raise EvidenceValidationError("Evidence interval out of bounds")
            normalized_quote = source.normalized_text[start:end]
            if (type(candidate.normalized_quote) is not str or
                    not normalized_quote.strip() or candidate.normalized_quote != normalized_quote):
                raise EvidenceValidationError("Evidence quote does not match normalized text")
            source_span = source.source_span(start, end)
            interval = (source_span.start, source_span.end)
            if interval in seen:
                raise EvidenceValidationError("Duplicate evidence span")
            seen.add(interval)
            result.append(VerifiedEvidence(
                start=source_span.start,
                end=source_span.end,
                quote=source.original_text[source_span.start:source_span.end],
                normalized_start=start,
                normalized_end=end,
                preprocessor_version=PREPROCESSOR_VERSION,
            ))
        return tuple(result)

    def verify(self, original_text: str, evidence: VerifiedEvidence) -> None:
        if type(original_text) is not str or type(evidence) is not VerifiedEvidence:
            raise EvidenceValidationError("Invalid original source or evidence")
        if (type(evidence.start) is not int or type(evidence.end) is not int or
                type(evidence.normalized_start) is not int or type(evidence.normalized_end) is not int or
                type(evidence.quote) is not str or evidence.preprocessor_version != PREPROCESSOR_VERSION or
                not (0 <= evidence.start < evidence.end <= len(original_text)) or
                not evidence.quote.strip() or original_text[evidence.start:evidence.end] != evidence.quote):
            raise EvidenceValidationError("Original evidence quote or span mismatch")
        processed = preprocess_text(original_text)
        start, end = evidence.normalized_start, evidence.normalized_end
        if not (0 <= start < end <= len(processed.normalized_text)):
            raise EvidenceValidationError("Normalized evidence interval out of bounds")
        span = processed.source_span(start, end)
        if (span.start, span.end) != (evidence.start, evidence.end):
            raise EvidenceValidationError("Evidence normalization mapping mismatch")
        if not processed.normalized_text[start:end].strip():
            raise EvidenceValidationError("Evidence cannot consist only of whitespace")

    def verify_many(self, original_text: str,
                    evidence: tuple[VerifiedEvidence, ...] | list[VerifiedEvidence]) -> None:
        if not isinstance(evidence, (list, tuple)) or len(evidence) > _MAX_EVIDENCE_ITEMS:
            raise EvidenceValidationError("Invalid evidence collection")
        seen: set[tuple[int, int]] = set()
        for item in evidence:
            self.verify(original_text, item)
            interval = (item.start, item.end)
            if interval in seen:
                raise EvidenceValidationError("Duplicate evidence span")
            seen.add(interval)
