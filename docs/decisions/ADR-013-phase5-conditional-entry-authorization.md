# ADR-013 — Conditional authorization for independent Phase 5 entry

**Status:** CONDITIONAL_PROGRESSION_APPROVED — TECHNICAL_SCOPE_ONLY (2026-10-24).
**Destination:** Phase 5 (End-to-End Integration, Quality & Resilience), **NOT STARTED**.
**Authorization basis:** Project owner's explicit request for a technical go/no-go decision and verified phase-gate evidence. This record is **not** the separately required `فاز ۵ را شروع کن` execution command. Does not grant employer approval for unknown contracts, data use, or production.

## Context and verified gate evidence

Prior official phase marker: `PHASE_4_IMPLEMENTED_AWAITING_VERIFICATION` (unchanged); Phase 3 likewise `PHASE_3_IMPLEMENTED_AWAITING_VERIFICATION`. No signed real taxonomy, label cardinality, business API contract, reviewer AuthN/AuthZ/schema/retention, authorized corpus/Gold, calibration targets or deployed model exist. A complete Phase 4 acceptance marker would be false. The Local-First progression policy in ADR-008/010 and approved Implementation Plan v1.1.0 permits separately authorized development of genuinely independent Phase 5 pieces.

- **Source:** GitHub `main` `3425d3826bddbfcc43afa11f5fd423dc40e03551`.
- **Remote CI:** [Run 40094157624](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40094157624) **SUCCESS** in all four jobs. Independent **76 PASSED**, 1 SKIPPED (optional `sklearn`), 3 DESELECTED; offline ML **27 PASSED** (overlaps); live isolated PostgreSQL **3 PASSED**, 1 SKIPPED, 76 DESELECTED, Docker rebuild/API health and Alembic empty-schema smoke PASSED; dependency-security `pip check` PASSED and `pip-audit` OSV **No known vulnerabilities found** at scan time. No reviewer-specific schema/DB integration exists.
- **Owner Windows local evidence:** original Phase 4 **30 PASSED**, independent regression **77 PASSED**, isolated PostgreSQL **3 PASSED**; isolated patched dependency candidate FastAPI 0.134.0 / Starlette 1.3.1 / pytest 9.0.3 / pip 26.2.2, Phase 4 **30 PASSED**, independent **76 PASSED** / 1 SKIPPED, PostgreSQL **3 PASSED**, OSV audit exit 0. These checks do not establish model accuracy, genuine category relevance or reviewer safety.

## Alternatives and decision

- Claim full Phase 4 complete / open public model-review API: **rejected**, required real gates and approved business/security contracts missing.
- Block every Phase 5 engineering task: **rejected**, independent existing-runtime/contract/failure checks are testable with safe fixtures and isolated PostgreSQL.
- **Chosen:** `CONDITIONAL_PROGRESSION_APPROVED` for the following narrowly limited work **after a separate explicit Phase 5 start command**:
  - **P5-01 subset:** Validate and, if needed, harden integration boundaries of *existing* Host → Application → Core → Infrastructure, DI discovery, provider lifecycle and failure paths. No public classifier/reviewer route, dependency substitution or fake model.
  - **P5-06 subset:** Fail-closed unavailable-model/DB/timeouts, safe request/error handling and security regression for existing approved entrypoints. Do not invent numeric rate-limit or request-size policy for unapproved business endpoints.
  - **P5-07 subset:** Regression/contract tests on existing `/health/live`, `/health/ready`, request ID and error surfaces; no invented classification v1 contract.
  - **P5-11 subset:** Real existing isolated PostgreSQL for DB-down/recovery paths and synthetic test-only fault injection for missing secrets, cold/not-ready model, timeout, partial-operation failures; no fake success in production.
  - **P5-12 subset:** Accurate runbooks, implementation notes, error-contract and deferred verification ledger for scoped implementation.
  - Any further independent subtask requires verifying it has no unapproved policy/schema/identity dependency before execution.

## Exclusions and mandatory backlog

- **BLOCKED:** P5-02 real final classification/review DTO or endpoint; P5-03/04 production persistence/idempotency; P5-05 AuthN/AuthZ and record isolation; unapproved P5-06 throttling targets; new external P5-07 classification contract; P5-08 integration requiring real authorized inference/reviewer workflow, unless employer explicitly approves the necessary contracts and security boundaries.
- **DEFERRED/NOT RUN:** P5-08 true real model+API+DB+review E2E; P5-09 Gold and version compatibility; model-dependent P5-10 load/stress/latency; carried P3 model training/benchmark/calibration and P4 groundedness/reviewer transaction/concurrency. Synthetic test doubles cannot turn these PASSED.
- **Risk owners:** Employer/product/taxonomy—taxonomy/cardinality/versioned API/criteria/thresholds; Security + Data Governance/Reviewer—AuthN/AuthZ/tenant/record scope/audit/retention/feedback rights; ML + Data Owner—lawful split/Gold/OOD/calibration/model; Engineering + Ops—transaction/concurrency, serving/capacity/rollback, continuous dependency scan R-17. **Latest settlement: Phase 6 before final acceptance**, preferably earlier when prerequisites become available.

## Enforcement and next steps

1. Keep `PHASE_4_IMPLEMENTED_AWAITING_VERIFICATION`; **do not** write `PHASE_4_COMPLETE_READY_FOR_PHASE_5`.
2. Record this separate `CONDITIONAL_PROGRESSION_APPROVED` in `docs/phase-status.md`; it authorizes only specified independent Phase 5 development after the separate owner command **`فاز ۵ را شروع کن`**.
3. Before Phase 5 work, re-evaluate `main`, latest CI/security, current risks and dependency contracts and issue the mandatory start report. Do not silently expand scope.
4. Full Phase 6 employer production acceptance remains `PROJECT_PRODUCTION_READY_ACCEPTED` only after actual gated evidence. This ADR neither begins Phase 5 nor approves release.
