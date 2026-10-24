"""Controlled evidence-only rendering; semantic category explanation is gated.

No category claims are produced. Relevance to employer-approved inclusion and
exclusion criteria requires a separate validated contract and Gold evaluation.
"""
from __future__ import annotations

from dataclasses import dataclass
import json

from src.core.services.text_classification.evidence_service import (
    EvidenceService,
    VerifiedEvidence,
)
from src.infrastructure.di.inject import inject


class ExplanationValidationError(ValueError):
    """No verified evidence, or unsupported/tampered explanation content."""


_PREAMBLE = (
    "نقل‌قول‌های زیر عیناً از متن اصلی استخراج شده‌اند. "
    "ارتباط آن‌ها با دسته‌بندی هنوز تأیید نشده است."
)


@dataclass(frozen=True, slots=True)
class EvidenceOnlyExplanation:
    text: str
    evidence: tuple[VerifiedEvidence, ...]
    mode: str = "EVIDENCE_ONLY_UNVERIFIED_RELEVANCE"


@inject
class ExplanationService:
    def __init__(self, evidence_service: EvidenceService):
        self._evidence_service = evidence_service

    def render_evidence_only(self, original_text: str,
                             evidence: tuple[VerifiedEvidence, ...]) -> EvidenceOnlyExplanation:
        if not isinstance(evidence, tuple) or not evidence:
            raise ExplanationValidationError("Cannot explain without verified evidence")
        self._evidence_service.verify_many(original_text, evidence)
        lines = [_PREAMBLE]
        for index, item in enumerate(evidence, 1):
            # JSON string escaping makes embedded newlines/quotes unambiguous.
            quote = json.dumps(item.quote, ensure_ascii=False)
            lines.append(f"{index}. [{item.start}, {item.end}): {quote}")
        return EvidenceOnlyExplanation("\n".join(lines), evidence)

    def verify_evidence_only(self, original_text: str,
                             explanation: EvidenceOnlyExplanation) -> None:
        if type(explanation) is not EvidenceOnlyExplanation or explanation.mode != "EVIDENCE_ONLY_UNVERIFIED_RELEVANCE":
            raise ExplanationValidationError("Unsupported explanation mode")
        try:
            expected = self.render_evidence_only(original_text, explanation.evidence)
        except (ValueError, TypeError):
            raise ExplanationValidationError("Explanation evidence is invalid") from None
        if explanation != expected:
            raise ExplanationValidationError("Explanation contains unsupported or modified content")
