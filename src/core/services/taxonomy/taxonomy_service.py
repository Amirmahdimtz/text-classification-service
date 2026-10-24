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
