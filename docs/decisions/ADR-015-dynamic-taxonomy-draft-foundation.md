# ADR-015 — Organization-managed dynamic taxonomy foundation

**Status:** OWNER_DIRECTED_DESIGN_REQUIREMENT — TECHNICAL_DRAFT_ONLY (2026-10-24)
**Scope:** Existing Phase 5 independent engineering; does **not** authorize Phase 6 start, final Taxonomy publication, a production admin API, or processing employer datasets.
**Owner decision:** Category definitions are **not** hard-coded. An organization must be able to add categories, make them inactive/retired and introduce new versions; design as much of the surrounding workflow dynamically as permitted while employer specifics remain unknown.
**Supersedes:** The implicit assumption that a category catalog could be static at compile time, if held anywhere. It does **not** settle the still-PROPOSED ADR-002 publication/approval policy, label cardinality (ADR-001), tenant identity/privacy or physical schema.
**References:** Architecture Guide, Implementation Plan v1.1.0 FR-02/FR-10/§3.1/§8/§11, [ADR-002](ADR-002-taxonomy-lifecycle.md), [ADR-014](ADR-014-phase6-conditional-technical-entry.md).

## Decision and safety boundaries

- Implement **immutable Core draft values and pure operations** under `src/core/services/taxonomy/taxonomy_service.py`: draft from prior revision, dynamic category addition (inactive by default and enforced), explicit metadata revisions within a draft (without changing activation), category deactivation rather than physical deletion, identity preservation, validation and active-category/model-version consistency check.
- Existing revisions are immutable. Deactivated IDs remain reserved and historical categories persist; any semantic change must be a new version with explicit future impact assessment. Do not recycle an inactive category code.
- No hard-coded real category names, labels, numbers, taxonomy, label-mode or probability thresholds are introduced. All category details are external inputs. Offline tests use **synthetic-only** categories.
- A draft or successful structural validation **does not** equal an approved/published taxonomy or an accurate model. No inference route or automatic classification is activated. The existing model manifest's `taxonomy_version` remains required, and mismatches must fail closed. The new Core check compares IDs only and does not prove semantics, provenance, reviewer authorization or model performance.
- **No persistent CRUD, API admin endpoint, AuthN/AuthZ or SQLAlchemy model/migration** in this stage: tenant/organization key, approval actor roles, code format and lifecycle decisions, edit audit trail, request/response schema, retention, conflict/versioning strategy and real registry still require employer/security approval. An in-memory draft is NOT a substitute for durable production category management.
- Keep `ADR-002` PROPOSED: the employer must still approve publication semantics, merge/split mapping, code/label rules, audit/retention, repository schema, release activation, model compatibility and who may add/retire categories.

## Delivery, risk and follow-up

The only new runtime code is an internal, pure, convention-discovered Core Service and immutable value records (no controller, no persistence provider). Tests prove structural constraints and unchanged revision objects but **not** real organization CRUD or lifecycle acceptance. Dependencies and API boundaries are unchanged. Risk of rework in the final schema/authorization remains HIGH; owner Employer/Product/Taxonomy + Security/Review, target: as soon as approved contracts are available, mandatory before Phase 6 production acceptance. Real training/retraining/calibration of model for changed labels is ML/Data Owner's deferred obligation; a category activation never silently updates a model.

**Phase Marker:** `PHASE_5_IMPLEMENTED_AWAITING_VERIFICATION` unchanged.
**Progression:** `CONDITIONAL_PROGRESSION_APPROVED` remains only the narrow independent Phase 6 scope already authorized by ADR-014. **Phase 6 NOT STARTED.**
