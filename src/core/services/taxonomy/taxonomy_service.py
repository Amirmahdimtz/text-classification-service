"""Immutable taxonomy draft operations; no public catalog or publication is enabled.

Category definitions are organization-managed inputs, never hard-coded labels.
This module contains no persistence, user authorization, model training or
publish side effects; approved versions require a separate governed boundary.
"""
from __future__ import annotations

from dataclasses import dataclass, replace

from src.infrastructure.di.inject import inject


class TaxonomyValidationError(ValueError):
    """Invalid draft structure, identity or category transition."""


class TaxonomyCompatibilityError(RuntimeError):
    """A model cannot safely interpret a different taxonomy revision."""


@dataclass(frozen=True, slots=True)
class TaxonomyCategory:
    code: str
    title: str
    definition: str = ""
    inclusion_criteria: tuple[str, ...] = ()
    exclusion_criteria: tuple[str, ...] = ()
    positive_examples: tuple[str, ...] = ()
    negative_examples: tuple[str, ...] = ()
    active: bool = False


@dataclass(frozen=True, slots=True)
class TaxonomyDraft:
    version: str
    parent_version: str | None
    categories: tuple[TaxonomyCategory, ...]


@dataclass(frozen=True, slots=True)
class TaxonomyRevisionImpact:
    """Structural delta only; does not approve a taxonomy or compatible model."""

    parent_version: str
    draft_version: str
    added_codes: tuple[str, ...]
    deactivated_codes: tuple[str, ...]
    revised_codes: tuple[str, ...]
    model_revalidation_required: bool


def _category_metadata(category: TaxonomyCategory) -> tuple[object, ...]:
    return (
        category.title, category.definition, category.inclusion_criteria,
        category.exclusion_criteria, category.positive_examples,
        category.negative_examples,
    )


def _valid_text(value: object, *, can_be_empty: bool = False) -> bool:
    return (
        type(value) is str
        and (can_be_empty or bool(value.strip()))
        and (not value or value == value.strip())
        and not any(ord(char) < 32 or ord(char) == 127 for char in value)
    )


def _validate_category(category: TaxonomyCategory) -> None:
    if type(category) is not TaxonomyCategory:
        raise TaxonomyValidationError("Invalid taxonomy category")
    if not _valid_text(category.code) or not _valid_text(category.title):
        raise TaxonomyValidationError("Category code and title are required")
    if not _valid_text(category.definition, can_be_empty=True):
        raise TaxonomyValidationError("Invalid category definition")
    if type(category.active) is not bool:
        raise TaxonomyValidationError("Invalid category activation state")
    for field in (
        category.inclusion_criteria, category.exclusion_criteria,
        category.positive_examples, category.negative_examples,
    ):
        if type(field) is not tuple or any(not _valid_text(item) for item in field):
            raise TaxonomyValidationError("Invalid category criteria or examples")


def _validate_draft(draft: TaxonomyDraft) -> None:
    if type(draft) is not TaxonomyDraft or not _valid_text(draft.version):
        raise TaxonomyValidationError("Invalid taxonomy draft")
    if draft.parent_version is not None and not _valid_text(draft.parent_version):
        raise TaxonomyValidationError("Invalid parent taxonomy version")
    if draft.parent_version == draft.version:
        raise TaxonomyValidationError("A new version must differ from its parent")
    if type(draft.categories) is not tuple:
        raise TaxonomyValidationError("Taxonomy categories must be immutable")
    seen: set[str] = set()
    for category in draft.categories:
        _validate_category(category)
        if category.code in seen:
            raise TaxonomyValidationError("Category identities cannot be reused")
        seen.add(category.code)


@inject
class TaxonomyService:
    """Pure, convention-discovered operations for draft taxonomy revisions.

    These methods cannot publish a release or authorize an organization.
    A persistence-backed release/approval workflow is intentionally blocked
    until the employer approves identity, access and retention contracts.
    """

    def __init__(self) -> None:
        pass

    def start_draft(self, version: str, *, previous: TaxonomyDraft | None = None) -> TaxonomyDraft:
        if not _valid_text(version):
            raise TaxonomyValidationError("A valid draft version is required")
        if previous is not None:
            _validate_draft(previous)
            if version == previous.version:
                raise TaxonomyValidationError("Cannot edit an earlier revision in place")
        draft = TaxonomyDraft(
            version=version,
            parent_version=previous.version if previous is not None else None,
            categories=previous.categories if previous is not None else (),
        )
        _validate_draft(draft)
        return draft

    def add_category(self, draft: TaxonomyDraft, category: TaxonomyCategory) -> TaxonomyDraft:
        _validate_draft(draft)
        _validate_category(category)
        if category.active:
            raise TaxonomyValidationError("New categories must remain inactive pending approval")
        if any(item.code == category.code for item in draft.categories):
            raise TaxonomyValidationError("Category code already exists, including inactive codes")
        updated = replace(draft, categories=(*draft.categories, category))
        _validate_draft(updated)
        return updated

    def deactivate_category(self, draft: TaxonomyDraft, code: str) -> TaxonomyDraft:
        _validate_draft(draft)
        if not _valid_text(code):
            raise TaxonomyValidationError("Category code is required")
        if not any(item.code == code for item in draft.categories):
            raise TaxonomyValidationError("Category not found")
        # Do not physically delete or rewrite existing revision objects.
        categories = tuple(
            replace(item, active=False) if item.code == code else item
            for item in draft.categories
        )
        updated = replace(draft, categories=categories)
        _validate_draft(updated)
        return updated

    def revise_category(self, draft: TaxonomyDraft, category: TaxonomyCategory) -> TaxonomyDraft:
        """Revise a category in an untrusted draft, not a published release."""
        _validate_draft(draft)
        _validate_category(category)
        previous = next((item for item in draft.categories if item.code == category.code), None)
        if previous is None:
            raise TaxonomyValidationError("Category not found")
        if previous.active != category.active:
            raise TaxonomyValidationError("Activation cannot be changed by editing category details")
        updated = replace(
            draft,
            categories=tuple(
                category if item.code == category.code else item for item in draft.categories
            ),
        )
        _validate_draft(updated)
        return updated

    def list_categories(self, draft: TaxonomyDraft, *, active_only: bool = False) -> tuple[TaxonomyCategory, ...]:
        _validate_draft(draft)
        if type(active_only) is not bool:
            raise TaxonomyValidationError("Invalid category filter")
        return tuple(item for item in draft.categories if item.active or not active_only)

    def assess_revision(
        self, previous: TaxonomyDraft, draft: TaxonomyDraft,
    ) -> TaxonomyRevisionImpact:
        """Check the structural safety of a forked draft before any approval.

        This is an offline consistency check, not a publish or promotion action.
        Models must always be revalidated when the taxonomy version changes.
        """
        _validate_draft(previous)
        _validate_draft(draft)
        if draft.parent_version != previous.version or draft.version == previous.version:
            raise TaxonomyValidationError("Taxonomy revision must name its exact parent")
        before = {item.code: item for item in previous.categories}
        after = {item.code: item for item in draft.categories}
        if before.keys() - after.keys():
            raise TaxonomyValidationError("Historical category identities cannot be removed")
        added = []
        deactivated = []
        revised = []
        for code, current in after.items():
            original = before.get(code)
            if original is None:
                if current.active:
                    raise TaxonomyValidationError("New categories cannot be activated by a draft")
                added.append(code)
                continue
            if not original.active and current.active:
                raise TaxonomyValidationError("Category reactivation requires an approved workflow")
            if original.active and not current.active:
                deactivated.append(code)
            if _category_metadata(original) != _category_metadata(current):
                revised.append(code)
        return TaxonomyRevisionImpact(
            parent_version=previous.version,
            draft_version=draft.version,
            added_codes=tuple(sorted(added)),
            deactivated_codes=tuple(sorted(deactivated)),
            revised_codes=tuple(sorted(revised)),
            model_revalidation_required=True,
        )

    def check_model_compatibility(
        self, draft: TaxonomyDraft, *, model_taxonomy_version: str,
        model_category_codes: tuple[str, ...],
    ) -> None:
        """Validate identities only; never certify a release or ML model quality."""
        _validate_draft(draft)
        if not _valid_text(model_taxonomy_version) or model_taxonomy_version != draft.version:
            raise TaxonomyCompatibilityError("Model taxonomy version is incompatible")
        if (type(model_category_codes) is not tuple or
            any(not _valid_text(item) for item in model_category_codes) or
            len(set(model_category_codes)) != len(model_category_codes)):
            raise TaxonomyCompatibilityError("Model category identities are invalid")
        active = {item.code for item in draft.categories if item.active}
        if not active or set(model_category_codes) != active:
            raise TaxonomyCompatibilityError("Model category identities do not match active taxonomy")
