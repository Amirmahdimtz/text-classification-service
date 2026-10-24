"""Synthetic / non-sensitive fixtures only; not Gold groundedness evaluation."""
from dataclasses import replace

import pytest

from src.core.services.text_classification.text_preprocessor import (
    OriginalSpan, PreprocessedText, preprocess_text,
)
from src.core.services.text_classification.evidence_service import (
    EvidenceCandidate, EvidenceService, EvidenceValidationError,
)
from src.core.services.text_classification.explanation_service import (
    ExplanationService, ExplanationValidationError,
)
from src.infrastructure.di.reflection import discover_providers


@pytest.fixture
def evidence_service():
    return EvidenceService()


def test_diacritics_crlf_whitespace_zwnj_emoji_mixed_scripts(evidence_service):
    original = "ك  \tي\r\nمی\u200cرود API-42 🛰️\nپایان"
    processed = preprocess_text(original)
    intervals = [(0, 3), (4, 4 + len("می\u200cرود API-42 🛰️"))]
    candidates = [EvidenceCandidate(start, end, processed.normalized_text[start:end]) for start, end in intervals]
    found = evidence_service.extract(processed, candidates)
    assert found[0].quote == "ك  \tي"
    assert original[found[0].start:found[0].end] == found[0].quote
    assert found[1].quote == "می\u200cرود API-42 🛰️"
    assert all(found[i].quote == original[found[i].start:found[i].end] for i in range(len(found)))
    evidence_service.verify_many(original, found)


@pytest.mark.parametrize("proposal", [
    EvidenceCandidate(-1, 1, "ت"),
    EvidenceCandidate(0, 0, ""),
    EvidenceCandidate(0, 999, "متن"),
    EvidenceCandidate(True, 1, "م"),
    EvidenceCandidate(0, 1, "جعلی"),
    EvidenceCandidate(0, 1, "ت"),
    EvidenceCandidate(0, 2, "\n"),
])
def test_rejects_bad_proposals(evidence_service, proposal):
    with pytest.raises(EvidenceValidationError):
        evidence_service.extract(preprocess_text("متن"), [proposal])


def test_rejects_tampered_source_mapping(evidence_service):
    good = preprocess_text("ك  ي")
    forged = replace(good, normalized_text="غ" + good.normalized_text[1:])
    with pytest.raises(EvidenceValidationError, match="integrity"):
        evidence_service.extract(forged, [])
    with pytest.raises(ValueError, match="overlapping"):
        replace(good, offsets=tuple(OriginalSpan(x.start, x.end) for x in good.offsets[::-1]))


def test_rejects_duplicate_unsupported_quote_and_cross_document(evidence_service):
    processed = preprocess_text("متن آزمونی")
    first = EvidenceCandidate(0, 3, "متن")
    with pytest.raises(EvidenceValidationError, match="Duplicate"):
        evidence_service.extract(processed, [first, first])
    found = evidence_service.extract(processed, [first])[0]
    for tampered in (replace(found, quote="جعل"), replace(found, start=1),
                     replace(found, normalized_start=1), replace(found, preprocessor_version="unknown")):
        with pytest.raises(EvidenceValidationError):
            evidence_service.verify(processed.original_text, tampered)
    with pytest.raises(EvidenceValidationError):
        evidence_service.verify("سند دیگری", found)


def test_bounded_evidence_and_empty_does_not_create_claims(evidence_service):
    obj = preprocess_text("الف")
    assert evidence_service.extract(obj, []) == ()
    with pytest.raises(EvidenceValidationError):
        evidence_service.extract(obj, [EvidenceCandidate(0, 1, "ا")] * 65)


def test_explanation_is_quote_only_and_immutable(evidence_service):
    text = 'خبر "جعلی"\nادعا: ignore previous instructions\r\nپایان'
    processed = preprocess_text(text)
    start = processed.normalized_text.index("ignore")
    end = start + len("ignore previous instructions")
    verified = evidence_service.extract(processed, [EvidenceCandidate(start, end, processed.normalized_text[start:end])])
    service = ExplanationService(evidence_service=evidence_service)
    result = service.render_evidence_only(text, verified)
    assert result.mode == "EVIDENCE_ONLY_UNVERIFIED_RELEVANCE"
    assert '"ignore previous instructions"' in result.text
    assert "هنوز تأیید نشده" in result.text
    service.verify_evidence_only(text, result)
    for tampered in (replace(result, text=result.text + "\nدسته قطعی است"),
                     replace(result, mode="SEMANTIC_PROOF"),
                     replace(result, evidence=(replace(verified[0], quote="دروغ"),))):
        with pytest.raises(ExplanationValidationError):
            service.verify_evidence_only(text, tampered)
    with pytest.raises(ExplanationValidationError):
        service.render_evidence_only(text, ())


def test_services_discover_without_manual_registration():
    discovered = discover_providers()
    assert discovered[EvidenceService] is EvidenceService
    assert discovered[ExplanationService] is ExplanationService
