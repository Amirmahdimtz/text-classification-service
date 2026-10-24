# P1-03 — Taxonomy specification
**State:** SCHEMA_PROPOSED; category catalog BLOCKED until supplied and approved by employer / taxonomy owner.

## Category definition record
| Field | Meaning / validation contract |
|---|---|
| category_code | Stable unique organizational code; exact format and max length TBD |
| category_title_fa | Persian display title; non-empty, unique constraints within version TBD |
| definition | Positive semantic meaning, sufficiently discriminative |
| inclusion_criteria | Explicit inclusion rules linked to permitted evidence |
| exclusion_criteria | Exclusion rules including tricky confusable cases |
| positive_examples | Real, approved, legally usable and de-identified reference reports; none supplied |
| negative_examples | Reviewed close negatives; none supplied |
| boundary_notes | Pairs of similar categories and adjudication rules |
| lifecycle_state | draft / approved-published / retired proposal; final values require approval |
| version | Immutable taxonomy release identifier |
| stable_identity | Logical identity across versions; split/merge lineage must be recorded |
| effective_period | Effective/publish timestamp; clock/date semantics TBD |
| approvers / audit | Authorized approver(s), change reason and evidence |

## Workflow
1. Taxonomy manager receives employer-authored category records and applicable labeling policy.
2. Validate uniqueness, non-empty definitions, contradictory inclusion/exclusion, and overlaps; circulate boundary-case examples to reviewers.
3. Independent experts annotate sampled reports; adjudication lead records disagreements and resolves definition gaps.
4. Product + taxonomy owner approve a frozen release; never mutate a published semantic definition in place.
5. Classification must reference an immutable taxonomy_version and a category valid in that release. Historical results keep their original version.
6. For rename, split, merge or retire: write compatibility map and impact analysis; retrain/re-evaluate and approve publication; do not silently rewrite prior classifications.

## Versioning invariants
- Codes must not be recycled for unrelated semantic concepts; version + identity resolves historical meaning.
- A result cannot claim a Category absent/inactive for the chosen release.
- Different releases cannot be assumed label-equivalent; explicit approved mapping needed for benchmark comparisons.
- Published version edits require new release; retirement is not physical deletion of audit history.

## Acceptance package (currently missing)
Approved real category list, definitions, two-sided examples, boundary decisions, active/retired state, category ownership, version identifier, authorized signature, multi-topic examples and representative class distribution. No artificial categories are approved.

## Owner-directed dynamic taxonomy foundation — 2026-10-24

**Approved design requirement (not published taxonomy):** The organization must be able to add and deactivate categories dynamically; category names and membership may not be hard-coded in the classification implementation. Owner instruction 2026-10-24. Technical implementation is tracked in [ADR-015](decisions/ADR-015-dynamic-taxonomy-draft-foundation.md). **ADR-002 approval workflow/physical schema remains PROPOSED.**

**Delivered non-persistent Core logic:** `src/core/services/taxonomy/taxonomy_service.py`, discovered through `@inject` with no manual registration. `TaxonomyDraft` and `TaxonomyCategory` are immutable records. `start_draft()` forks a prior snapshot under a different version; `add_category()` reserves a new stable code **inactive by default**; `deactivate_category()` preserves identity and previous snapshots (no destructive delete); `list_categories()` filters active/inactive; `check_model_compatibility()` compares taxonomy version and active codes against model metadata, rejecting mismatches. Field validation rejects malformed/duplicated codes and control characters. Unit/DI tests use synthetic-only labels and do not imply publication.

**Required runtime workflow when approvals exist (NOT YET IMPLEMENTED):** Authorized manager creates a draft → edits category definitions and approved boundary rules → records identity and audit → designated approver publishes an immutable version → ML owner evaluates/retrains/approves compatible versioned model and policy → controlled model/taxonomy promotion and rollback → historical results retain old version and category codes. Admin CRUD and publication require AuthN/AuthZ, organization scope and approved PostgreSQL schema with Alembic migration. Physical delete of referenced/retired categories must not silently corrupt prior classifications.

**Still TBD/BLOCKED:** Real category list, code/title constraints, multilingual variants, exact organizational tenancy, who can edit/publish/retire, audit/retention, publish concurrency, split/merge lineage and policy for changed model labels, category examples/data permissions, API/DTO and UI. Label cardinality is independent and still unapproved (ADR-001). No positive model output is activated from an unapproved draft. No deployment artifact or Migration exists.

**CI Evidence:** [Commit ed876e0](https://github.com/Amirmahdimtz/text-classification-service/commit/ed876e0a88d0a62c05e2b9c9ca3d669471003a31), [run 40105875237](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40105875237) 4/4 jobs SUCCESS: independent 106 PASSED/1 SKIPPED/5 DESELECTED; real isolated PostgreSQL 5 PASSED/1 SKIPPED, offline ML 30 PASSED (overlap), strict OSV/compatibility PASSED at scan time. The added taxonomy tests are independent/synthetic; no persisted organization category CRUD or taxonomy publication verified.
