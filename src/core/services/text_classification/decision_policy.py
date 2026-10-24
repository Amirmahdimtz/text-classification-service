"""Fail-closed decision semantics and draft policy structure validation.

This does not publish a policy, calibrate scores, classify, decide OOD, or
authorize reviewers. Only a review-only proposal can pass the local contract
validator; automatic decisions remain blocked pending governed releases.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite

from src.infrastructure.di.inject import inject


class DecisionStatus(str, Enum):
    AUTO_CLASSIFIED = "AUTO_CLASSIFIED"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"


class ScoreKind(str, Enum):
    RAW_MODEL_SCORE = "RAW_MODEL_SCORE"
    CALIBRATED_PROBABILITY = "CALIBRATED_PROBABILITY"


class DecisionContractError(ValueError):
    """Malformed policy or proposal that could misrepresent a prediction."""


class DecisionDependencyError(RuntimeError):
    """Model, governed policy, or mandatory decision evidence unavailable."""


@dataclass(frozen=True, slots=True)
class DecisionPolicyDraft:
    version: str
    taxonomy_version: str
    calibration_version: str | None = None
    category_thresholds: tuple[tuple[str, float], ...] = ()


@dataclass(frozen=True, slots=True)
class DecisionProposal:
    status: DecisionStatus
    predicted_category: str | None = None
    final_category: str | None = None
    score_kind: ScoreKind | None = None
    score: float | None = None
    confidence: float | None = None


@inject
class DecisionPolicyService:
    """Checks untrusted drafts, never authorizes real business decisions."""

    def __init__(self) -> None:
        pass

    @staticmethod
    def validate_draft(draft: DecisionPolicyDraft) -> None:
        if type(draft) is not DecisionPolicyDraft:
            raise DecisionContractError("Invalid decision policy shape")
        for value in (draft.version, draft.taxonomy_version):
            if type(value) is not str or not value.strip() or len(value) > 128:
                raise DecisionContractError("Policy identity is missing or invalid")
        if draft.calibration_version is not None and (
            type(draft.calibration_version) is not str or not draft.calibration_version.strip() or
            len(draft.calibration_version) > 128
        ):
            raise DecisionContractError("Invalid calibration version")
        if not isinstance(draft.category_thresholds, tuple) or len(draft.category_thresholds) > 1024:
            raise DecisionContractError("Invalid per-category thresholds")
        if draft.category_thresholds and draft.calibration_version is None:
            raise DecisionContractError("Thresholds require an explicit calibration version")
        seen: set[str] = set()
        for entry in draft.category_thresholds:
            if not isinstance(entry, tuple) or len(entry) != 2:
                raise DecisionContractError("Invalid category threshold entry")
            category, threshold = entry
            if (type(category) is not str or not category.strip() or len(category) > 128 or
                    category in seen or type(threshold) is not float or
                    not isfinite(threshold) or not 0 <= threshold <= 1):
                raise DecisionContractError("Invalid or duplicate calibrated threshold")
            seen.add(category)

    def validate_review_only(self, proposal: DecisionProposal, *,
                             model_ready: bool, policy: DecisionPolicyDraft | None,
                             taxonomy_version: str | None) -> DecisionProposal:
        """Validate a *non-persisted* review-only proposal; not an approval token.

        Failure of the model is an exception, not NEEDS_REVIEW/OUT_OF_SCOPE.
        The caller must independently authenticate and authorize any real flow.
        """
        if model_ready is not True or policy is None:
            raise DecisionDependencyError("Model and decision policy must be available")
        self.validate_draft(policy)
        if type(taxonomy_version) is not str or policy.taxonomy_version != taxonomy_version:
            raise DecisionDependencyError("Decision taxonomy compatibility missing")
        if type(proposal) is not DecisionProposal or type(proposal.status) is not DecisionStatus:
            raise DecisionContractError("Invalid decision proposal")
        if proposal.status is not DecisionStatus.NEEDS_REVIEW:
            raise DecisionDependencyError("Automatic and out-of-scope decisions require approved policies")
        if proposal.final_category is not None:
            raise DecisionContractError("A review-only proposal cannot set a final category")
        if (proposal.predicted_category is not None and
            (type(proposal.predicted_category) is not str or not proposal.predicted_category.strip())):
            raise DecisionContractError("Invalid predicted category")
        if proposal.score_kind is None:
            if proposal.score is not None or proposal.confidence is not None:
                raise DecisionContractError("Scores require an explicit kind")
        elif type(proposal.score_kind) is not ScoreKind or proposal.score is None:
            raise DecisionContractError("Invalid score kind or missing score")
        else:
            if type(proposal.score) not in (float, int) or not isfinite(proposal.score):
                raise DecisionContractError("Invalid score value")
            if proposal.predicted_category is None:
                raise DecisionContractError("A category score requires a proposed category")
            if proposal.score_kind is ScoreKind.RAW_MODEL_SCORE:
                if proposal.confidence is not None:
                    raise DecisionContractError("Raw model scores cannot be confidence")
            else:
                raise DecisionDependencyError("Calibrated probability requires an approved release")
        if proposal.confidence is not None:
            raise DecisionDependencyError("Confidence requires an approved calibrated release")
        return proposal
