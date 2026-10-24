# ADR-010 — Local-first development and conditional Phase 4 progression

**Status:** ACCEPTED_BY_PROJECT_OWNER_FOR_PROCESS_ONLY (2026-10-24)
**Scope:** Phase scheduling, not approval of taxonomy, confidential data, model quality or production release.
**References:** ADR-008 (employer acceptance at Phase 6); ADR-009 (Phase 3 offline artifacts); Phase 3 implementation plan v1.1.0.

## Decision

1. Develop dependency-independent Phase 3–5 features with isolated PostgreSQL, non-sensitive fixtures, Unit/Integration/API/DI/Security regression and GitHub Actions. No production test doubles or invented category outputs.
2. Real model training/selection, Gold/OOD evaluation, calibration, grounded explanation validation, model-integrated E2E, server load/stress and rollback remain mandatory. Without approved inputs, they are BLOCKED or DEFERRED until no later than Phase 6, and are not PASSED.
3. An independent green test gate and owner direction can authorize `CONDITIONAL_PROGRESSION_APPROVED` for a named safe scope, without closing `PHASE_3_IMPLEMENTED_AWAITING_VERIFICATION`.
4. Before implementing Phase 4, the owner must issue an explicit `فاز ۴ را شروع کن` command. This ADR is not that command.
5. Unknown AuthN/AuthZ, taxonomy, label cardinality, thresholds, physical persistence schema and data policies block dependent production functionality; missing real models fail closed.

## Phase 3 correction

The previous temporal split sorted incident components by their latest timestamp but selected ratio boundaries without checking their full date ranges, potentially mixing earlier validation examples with later training examples. The updated algorithm selects two chronologically safe boundaries without breaking incident/duplicate groups, or rejects the split.

**Correction:** https://github.com/Amirmahdimtz/text-classification-service/commit/7fcbfa711c32b8170be7a4b243306e0d30f40fdc

**Verified CI:** https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40077902341 — independent 46 PASSED/1 SKIPPED; isolated PostgreSQL 3 PASSED; offline ML 27 PASSED. Jobs have overlapping tests. Local owner Windows evidence before this correction: 45 independent PASSED and 3 PostgreSQL PASSED.

## Conditional progression

**Status:** `CONDITIONAL_PROGRESSION_APPROVED` for *independent Phase 4 scope only*; **Phase 4 NOT STARTED**.

**Permitted after explicit Phase 4 start:** P4-01 original-offset evidence extraction; P4-04 mechanical quote/span fidelity and unsupported-claim rejection; P4-06 error-state separation; other non-sensitive, contract-independent tests and logic.

**Not permitted without approvals:** P4-02 real taxonomy relevance, P4-05 calibrated thresholds/final categories, P4-07–09 real reviewer permissions, business schema and retention, real model classification endpoints or confidential data.

**Risk ownership and final deadline:** ML/data owners: dataset leakage, model benchmarks, OOD and calibration; employer/product: taxonomy and thresholds; security: privacy/authorization; operations: real inference runtime/load/rollback. Resolve and test all deferred P3–P5 gates by Phase 6 before employer production acceptance. See docs/phase-status.md and docs/risk-register.md.

**Reasoning:** Locally tested code may progress without unapproved real-model inputs, but synthetic fixtures cannot certify production model quality. Neither the architecture nor customer-owned requirements are changed.
