"""Independent structural tests: no validated taxonomy/model/threshold fixtures."""
import math

import pytest

from src.core.services.text_classification.decision_policy import (
    DecisionContractError, DecisionDependencyError, DecisionPolicyDraft,
    DecisionPolicyService, DecisionProposal, DecisionStatus, ScoreKind,
)
from src.infrastructure.di.reflection import discover_providers


def _draft():
    return DecisionPolicyDraft("test-draft-v1", "test-taxonomy-v1")


def test_status_contract_is_distinct_from_infrastructure_failures():
    assert {s.value for s in DecisionStatus} == {"AUTO_CLASSIFIED", "NEEDS_REVIEW", "OUT_OF_SCOPE"}
    service = DecisionPolicyService()
    proposal = DecisionProposal(DecisionStatus.NEEDS_REVIEW, predicted_category="test-category",
                                score_kind=ScoreKind.RAW_MODEL_SCORE, score=-1.25)
    assert service.validate_review_only(proposal, model_ready=True, policy=_draft(),
                                        taxonomy_version="test-taxonomy-v1") is proposal
    for ready, policy, taxonomy in ((False, _draft(), "test-taxonomy-v1"),
                                    (True, None, "test-taxonomy-v1"),
                                    (True, _draft(), "wrong")):
        with pytest.raises(DecisionDependencyError):
            service.validate_review_only(proposal, model_ready=ready, policy=policy,
                                         taxonomy_version=taxonomy)


def test_final_categories_and_automatic_or_ood_decisions_fail_closed():
    service = DecisionPolicyService()
    for status in (DecisionStatus.AUTO_CLASSIFIED, DecisionStatus.OUT_OF_SCOPE):
        with pytest.raises(DecisionDependencyError):
            service.validate_review_only(DecisionProposal(status), model_ready=True,
                                         policy=_draft(), taxonomy_version="test-taxonomy-v1")
    with pytest.raises(DecisionContractError):
        service.validate_review_only(DecisionProposal(DecisionStatus.NEEDS_REVIEW, final_category="test-category"),
                                     model_ready=True, policy=_draft(), taxonomy_version="test-taxonomy-v1")


@pytest.mark.parametrize("proposal,expected", [
    (DecisionProposal(DecisionStatus.NEEDS_REVIEW, score=0.4), DecisionContractError),
    (DecisionProposal(DecisionStatus.NEEDS_REVIEW, predicted_category="test-category",
                      score_kind=ScoreKind.RAW_MODEL_SCORE, score=0.5, confidence=0.5), DecisionContractError),
    (DecisionProposal(DecisionStatus.NEEDS_REVIEW, predicted_category="test-category",
                      score_kind=ScoreKind.CALIBRATED_PROBABILITY, score=0.8), DecisionDependencyError),
    (DecisionProposal(DecisionStatus.NEEDS_REVIEW, predicted_category="test-category",
                      score_kind=ScoreKind.RAW_MODEL_SCORE, score=float("nan")), DecisionContractError),
    (DecisionProposal(DecisionStatus.NEEDS_REVIEW, score_kind=ScoreKind.RAW_MODEL_SCORE, score=0.2), DecisionContractError),
    (DecisionProposal(DecisionStatus.NEEDS_REVIEW, predicted_category=" "), DecisionContractError),
])
def test_score_semantics_and_invalid_proposals_rejected(proposal, expected):
    with pytest.raises(expected):
        DecisionPolicyService().validate_review_only(proposal, model_ready=True, policy=_draft(),
                                                     taxonomy_version="test-taxonomy-v1")


@pytest.mark.parametrize("draft", [
    DecisionPolicyDraft("", "test-v1"),
    DecisionPolicyDraft("policy-v1", ""),
    DecisionPolicyDraft("test", "test", category_thresholds=(("a", 0.6),)),
    DecisionPolicyDraft("test", "test", "cal-test", (("a", math.nan),)),
    DecisionPolicyDraft("test", "test", "cal-test", (("a", 0.5), ("a", 0.7))),
    DecisionPolicyDraft("test", "test", "cal-test", (("a", 1.4),)),
    DecisionPolicyDraft("test", "test", "cal-test", (("a", True),)),
])
def test_policy_draft_validation_rejects_unbounded_unversioned_or_invalid(draft):
    with pytest.raises(DecisionContractError):
        DecisionPolicyService.validate_draft(draft)


def test_policy_draft_validation_only_does_not_approve_thresholds():
    draft = DecisionPolicyDraft("test", "test", "test-calibration", (("test-category", 0.7),))
    DecisionPolicyService.validate_draft(draft)
    with pytest.raises(DecisionDependencyError):
        DecisionPolicyService().validate_review_only(
            DecisionProposal(DecisionStatus.AUTO_CLASSIFIED, predicted_category="test-category"),
            model_ready=True, policy=draft, taxonomy_version="test",
        )
    assert discover_providers()[DecisionPolicyService] is DecisionPolicyService
