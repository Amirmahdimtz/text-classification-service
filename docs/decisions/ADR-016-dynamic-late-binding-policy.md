# ADR-016 — Dynamic / Late-Binding across organization-owned contracts

**Date:** 2026-10-27
**Status:** ACCEPTED_BY_PROJECT_OWNER_FOR_ENGINEERING_DESIGN_AND_PROGRESSION_ONLY
**Authority:** Owner-provided `Text_Classification_Service_Implementation_Plan_FA.md` **v1.2.0**, dated 2026-10-25, and owner's explicit instruction to adapt the current Phase 5.
**Scope:** Existing Phase 5 independent implementation and governed progression only. This ADR neither starts Phase 6 nor approves employer/business/security/data/model/server specifics.
**References:** mandatory `Service_Architecture_Guide_FA.md`, Plan v1.2.0 §§0.2.1, 6, 11–13, 15–17; ADR-001..008, ADR-010, ADR-013/014, [ADR-015](ADR-015-dynamic-taxonomy-draft-foundation.md), [Phase 5 v1.2 alignment](../phase-5-v1.2-alignment.md).

## Context

The organization has not supplied a finalized taxonomy, single/multi-label mode, authenticated business contract/schema, security/record authorization, lawful Train/Gold/OOD dataset, release model or SLO/runtime. Earlier work implemented contract-independent components and regression tests under the narrow Phase 5 scope authorized by ADR-013. Plan v1.2.0 explicitly mandates engineering for those independent scopes to progress while all five employer-owned packages can remain unresolved **until the final Phase 6 gate**. Unknown parameters do **not** mean production defaults, implicit approvals or passing real quality gates.

## Accepted design policy

1. **DYN-01 — Taxonomy and label mode.** Build category-neutral, immutable versioned draft validation and impact assessment; defer real labels, cardinality, tenant scope and publish authority. New/edited categories cannot enter live inference without approved taxonomy and compatible model/policy. Never erase past category identity.
2. **DYN-02 — API and persistence.** Build generic validation/error/DI/transaction infrastructure and isolated regression now. Do **not** expose invented business API or create business ORM/Alembic migration until owner-approved DTO, identity/record/retention and physical schema exist. API contracts are versioned, not free-form per request.
3. **DYN-03 — Security and privacy.** Default deny, redaction, TLS/secret configuration and negative access tests now. Operational Admin/Reviewer/Report APIs need real authenticated principal, record scope, permissions, data rights and security review; never infer them from configuration samples.
4. **DYN-04 — Data and model.** Keep preprocessing/offsets, leakage validation, artifact hashes, structural policy/provider/compatibility and fail-closed runtime testable with non-sensitive fixtures. No training on unlicensed data, no fake production provider, category, calibrated confidence, Gold result or automatic final decision.
5. **DYN-05 — Server and SLO.** Keep provider readiness, bounded concurrency/timeouts and infrastructure configuration independently verifiable. Defer actual capacity, GPU/CPU load, signed numeric targets, soak/recovery/rollback and final release assessment until a permitted representative environment exists.

The five packages may remain `TBD/BLOCKED` **during independent Phase 5 and at restricted Phase 6 entry**. However **each must be signed, implemented and genuinely verified before `PROJECT_PRODUCTION_READY_ACCEPTED`**. If they remain unknown, final acceptance is BLOCKED; the solution is not Production-ready, nor is a deferred test PASSED. If a late choice changes existing behavior, record impact/ADR, version compatibility, data migration where approved, and repeat regression.

## Evidence, authorization and safety guards

- **Technical foundation at source `72eb5427a917ac0bb0315cd4c692d0a5a8d5b3a3`:** Existing dynamic draft/service + revision impact, Host/DI, isolated PostgreSQL transaction, provider fail-closed and timeout tests. Added an HTTP contract regression explicitly checking that unapproved taxonomy read/management routes remain unavailable. This is **not real AuthN/AuthZ**: inaccessible endpoints cannot prove record isolation.
- [GitHub Actions 40464115968](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40464115968), exact source SHA, four jobs SUCCESS: 114 independent PASSED/1 optional SKIPPED, five isolated PostgreSQL PASSED/1 optional SKIPPED, 30 offline synthetic ML PASSED (overlapping), pip compatibility and strict OSV PASS at scan time. Existing two dependency deprecation warnings. Latest Windows LOCAL_USER not rerun; real model and final E2E/Gold/load tests not run.
- **Phase marker:** `PHASE_5_IMPLEMENTED_AWAITING_VERIFICATION` persists; missing P5 business/model/security acceptance cannot be waived.
- **Separate progression:** ADR-014's `CONDITIONAL_PROGRESSION_APPROVED` remains strictly confined to P6-02/04/06/12 independent subscopes. A separate explicit `فاز ۶ را شروع کن` command is required. **Phase 6 NOT STARTED**.
- **Deadline and ownership:** Employer/Product/Taxonomy (category/mode/business contracts); Security/Data Governance/Review (identity, privacy, audit); ML/Data Owner (legal Train/Gold/OOD, released model, evaluation); Engineering/Ops (approved DB/migrations, infrastructure, targets/observability). Enforce all real tests and customer acceptance by final Phase 6 Gate.

## Alternatives and decision scope

Rejected: hard-code representative organizational labels/roles/schema/model so Phase 5 appears complete; silently weaken model/authorization acceptance; build a generic unprotected admin CRUD or use synthetic model E2E as Production proof. Chosen: late-bound design with immutable versions, explicit fail-closed gates and evidence-backed **conditional** scope progression. No changes to layered architecture, Phase 1–6 order, employer authority, final testing or acceptance criteria.

**Implementation note:** Replacing/attaching Plan v1.2.0 as a Project Source is not itself a GitHub commit. This ADR and the linked phase/risk/verification docs are the actual synchronized repository record; historical v1.1.0 references in earlier ADRs remain a truthful record of their original basis.
