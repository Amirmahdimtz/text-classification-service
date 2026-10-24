"""Dynamic taxonomy drafts: synthetic definitions and no external data."""
import pytest

from src.core.services.taxonomy.taxonomy_service import (
    TaxonomyCategory, TaxonomyCompatibilityError, TaxonomyDraft,
    TaxonomyService, TaxonomyValidationError,
)
from src.infrastructure.di.bootstrap import bootstrap_di, resolve


def category(code: str = "SYNTH-A", *, active: bool = False) -> TaxonomyCategory:
    return TaxonomyCategory(
        code=code, title="Synthetic test category", definition="Synthetic definition",
        inclusion_criteria=("Synthetic inclusion",),
        exclusion_criteria=("Synthetic exclusion",),
        active=active,
    )


def test_dynamic_addition_keeps_previous_revision_unchanged():
    service = TaxonomyService()
    initial = service.start_draft("draft-v1")
    first = service.add_category(initial, category())
    newer = service.start_draft("draft-v2", previous=first)
    second = service.add_category(newer, category("SYNTH-B"))
    assert initial.categories == ()
    assert first.categories == (category(),)
    assert newer.categories == first.categories
    assert second.parent_version == "draft-v1"
    assert [c.code for c in service.list_categories(second)] == ["SYNTH-A", "SYNTH-B"]
    assert service.list_categories(second, active_only=True) == ()


def test_deactivation_keeps_identity_and_historical_revision():
    service = TaxonomyService()
    previous = TaxonomyDraft("release-v1", None, (category(active=True),))
    revision = service.start_draft("draft-v2", previous=previous)
    disabled = service.deactivate_category(revision, "SYNTH-A")
    assert previous.categories[0].active is True
    assert disabled.categories[0].active is False
    assert disabled.categories[0].code == "SYNTH-A"
    assert service.list_categories(disabled, active_only=True) == ()


def test_inactive_category_code_cannot_be_recycled():
    service = TaxonomyService()
    draft = service.add_category(service.start_draft("draft-v1"), category())
    with pytest.raises(TaxonomyValidationError, match="already exists"):
        service.add_category(draft, category())


def test_new_category_cannot_be_active_without_approval():
    with pytest.raises(TaxonomyValidationError, match="inactive"):
        TaxonomyService().add_category(
            TaxonomyService().start_draft("draft-v1"), category(active=True)
        )


@pytest.mark.parametrize("bad", ["", " ", " v1", "v1 ", "v1\x00"])
def test_invalid_revision_identity_fails_closed(bad):
    with pytest.raises(TaxonomyValidationError):
        TaxonomyService().start_draft(bad)


def test_same_version_and_missing_category_are_rejected():
    service = TaxonomyService()
    draft = service.start_draft("draft-v1")
    with pytest.raises(TaxonomyValidationError, match="earlier revision"):
        service.start_draft("draft-v1", previous=draft)
    with pytest.raises(TaxonomyValidationError, match="not found"):
        service.deactivate_category(draft, "SYNTH-A")


@pytest.mark.parametrize(
    "bad_category",
    [
        TaxonomyCategory(code="", title="x"),
        TaxonomyCategory(code="A", title=""),
        TaxonomyCategory(code="A\n", title="x"),
        TaxonomyCategory(code="A", title="x", active="yes"),
        TaxonomyCategory(code="A", title="x", inclusion_criteria=["not a tuple"]),
        TaxonomyCategory(code="A", title="x", negative_examples=("",)),
    ],
)
def test_category_validation_fails_closed(bad_category):
    with pytest.raises(TaxonomyValidationError):
        TaxonomyService().add_category(
            TaxonomyService().start_draft("draft-v1"), bad_category
        )


def test_read_only_compatibility_check_rejects_taxonomy_drift():
    service = TaxonomyService()
    previous = TaxonomyDraft("release-v1", None, (category(active=True),))
    with pytest.raises(TaxonomyCompatibilityError, match="version"):
        service.check_model_compatibility(
            previous, model_taxonomy_version="release-v0",
            model_category_codes=("SYNTH-A",),
        )
    with pytest.raises(TaxonomyCompatibilityError, match="do not match"):
        service.check_model_compatibility(
            previous, model_taxonomy_version="release-v1",
            model_category_codes=("SYNTH-B",),
        )
    with pytest.raises(TaxonomyCompatibilityError, match="identities are invalid"):
        service.check_model_compatibility(
            previous, model_taxonomy_version="release-v1",
            model_category_codes=("SYNTH-A", "SYNTH-A"),
        )
    service.check_model_compatibility(
        previous, model_taxonomy_version="release-v1",
        model_category_codes=("SYNTH-A",),
    )


def test_di_discovers_taxonomy_service_without_manual_registration():
    bootstrap_di()
    assert isinstance(resolve(TaxonomyService), TaxonomyService)


def test_draft_shape_duplicate_identities_cannot_be_read():
    bad = TaxonomyDraft("draft-v1", None, (category(), category()))
    with pytest.raises(TaxonomyValidationError, match="cannot be reused"):
        TaxonomyService().list_categories(bad)


def test_category_metadata_can_be_revised_in_new_draft_without_changing_history():
    service = TaxonomyService()
    previous = TaxonomyDraft("release-v1", None, (category(active=True),))
    draft = service.start_draft("draft-v2", previous=previous)
    revision = TaxonomyCategory(
        code="SYNTH-A", title="Revised synthetic title",
        definition="Revised synthetic definition", active=True,
    )
    edited = service.revise_category(draft, revision)
    assert edited.categories[0].title == "Revised synthetic title"
    assert previous.categories[0].title == "Synthetic test category"
    assert edited.version == "draft-v2" and edited.parent_version == "release-v1"
    assert draft.categories == previous.categories


def test_category_edit_must_not_silently_activate_or_replace_identity():
    service = TaxonomyService()
    draft = service.add_category(service.start_draft("draft-v1"), category())
    with pytest.raises(TaxonomyValidationError, match="Activation"):
        service.revise_category(draft, category(active=True))
    with pytest.raises(TaxonomyValidationError, match="not found"):
        service.revise_category(draft, category("UNLISTED"))



def test_revision_impact_reports_dynamic_changes_deterministically():
    service = TaxonomyService()
    previous = TaxonomyDraft(
        "release-v1", None,
        (category("SYNTH-B", active=True), category("SYNTH-A", active=True)),
    )
    draft = service.start_draft("draft-v2", previous=previous)
    draft = service.deactivate_category(draft, "SYNTH-A")
    draft = service.revise_category(
        draft,
        TaxonomyCategory(
            code="SYNTH-B", title="Updated synthetic title",
            definition="Synthetic definition", active=True,
        ),
    )
    draft = service.add_category(draft, category("SYNTH-C"))
    impact = service.assess_revision(previous, draft)
    assert impact.parent_version == "release-v1"
    assert impact.draft_version == "draft-v2"
    assert impact.added_codes == ("SYNTH-C",)
    assert impact.deactivated_codes == ("SYNTH-A",)
    assert impact.revised_codes == ("SYNTH-B",)
    assert impact.model_revalidation_required is True
    assert previous.categories[0].title == "Synthetic test category"


def test_revision_without_category_changes_still_requires_model_version_validation():
    service = TaxonomyService()
    parent = TaxonomyDraft("release-v1", None, (category("SYNTH-A", active=True),))
    child = service.start_draft("draft-v2", previous=parent)
    report = service.assess_revision(parent, child)
    assert report.added_codes == report.deactivated_codes == report.revised_codes == ()
    assert report.model_revalidation_required is True


@pytest.mark.parametrize("mode", ["delete", "reactivate", "activate-new", "unlinked"])
def test_revision_validation_rejects_unsafe_transitions(mode):
    service = TaxonomyService()
    parent = TaxonomyDraft(
        "release-v1", None,
        (category("SYNTH-A", active=False), category("SYNTH-B", active=True)),
    )
    new = service.start_draft("draft-v2", previous=parent)
    if mode == "delete":
        new = TaxonomyDraft("draft-v2", "release-v1", (category("SYNTH-A"),))
    elif mode == "reactivate":
        new = TaxonomyDraft(
            "draft-v2", "release-v1",
            (category("SYNTH-A", active=True), category("SYNTH-B", active=True)),
        )
    elif mode == "activate-new":
        new = TaxonomyDraft(
            "draft-v2", "release-v1",
            (*parent.categories, category("SYNTH-C", active=True)),
        )
    else:
        new = TaxonomyDraft("draft-v2", "unrelated-version", parent.categories)
    with pytest.raises(TaxonomyValidationError):
        service.assess_revision(parent, new)
