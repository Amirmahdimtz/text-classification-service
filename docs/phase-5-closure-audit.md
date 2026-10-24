# Phase 5 — Formal completion attempt, acceptance checklist and hard blockers

**Review date:** 2026-10-24
**Owner instruction:** `خب این مرحله را تمام کن` — interpreted as a request for **full Phase 5 completion**, not Phase 6 start or a waiver of its mandatory gates.
**Approved normative sources:** `Service_Architecture_Guide_FA.md`, `Text_Classification_Service_Implementation_Plan_FA.md` v1.1.0, ADR-008, ADR-010, ADR-013 and ADR-014.
**Reviewed repository main before repair:** `48950939f99e0c8996a2ea35db43d0152e5753a5`.
**Repair SHA:** `28afaefbbd33ab05fcacba37a1c35ca316d1b47e`, [source fix](https://github.com/Amirmahdimtz/text-classification-service/commit/28afaefbbd33ab05fcacba37a1c35ca316d1b47e).
**Gate outcome:** `NO-GO — PHASE_5_COMPLETE_READY_FOR_PHASE_6` is **not** justified. Official status stays `PHASE_5_IMPLEMENTED_AWAITING_VERIFICATION` for a completed and independently verified **subset only**.
**Phase 6:** NOT STARTED; previously accepted [ADR-014](decisions/ADR-014-phase6-conditional-technical-entry.md) remains valid **only** for its P6-02/04/06/12 independent subset and still requires explicit `فاز ۶ را شروع کن`.

## Independent issue corrected in this review

**P5-06/P5-11 — Shutdown while capacity wait:** `TextClassifierProvider.predict_async` checked `is_ready` before awaiting the semaphore. `close_async` could then clear the model while the caller waited. On acquiring a slot, the old implementation dereferenced `self._model.predict`, potentially raising an unexpected `AttributeError` and leaving the slot unreleased. The repair captures a local model after acquiring capacity, verifies `not _closed` and non-null model, returns typed `InferenceUnavailableError` while releasing the slot, and submits `model.predict` to the existing bounded executor. The synthetic-only concurrency regression is `test_provider_close_while_waiting_for_capacity_fails_closed_without_slot_leak`; no fake model was added to Production.

**REMOTE/AVAILABLE verified:** [Actions run 40102628553](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40102628553) on corrected source SHA, **four jobs SUCCESS**. Independent **85 PASSED / 1 SKIPPED (optional ML) / 4 DESELECTED**; real isolated PostgreSQL **4 PASSED / 1 SKIPPED / 85 DESELECTED**, Docker/API and empty Alembic smoke; offline synthetic ML **29 PASSED** (overlaps independent suite); dependency compatibility `pip check` PASS and strict installed-closure OSV `No known vulnerabilities found` at scan time. Two established Starlette/httpx and AnyIO deprecation warnings persist. No new tables, migration, business API or deployment.

**LOCAL_USER:** Owner Windows Python 3.12.10 evidence on **previous source** `684bbbdf88f959f8197b56321ae3136a53355db5`: 85 independent PASSED / 4 PostgreSQL PASSED, targeted host/provider 11 PASSED, pip compatibility and OSV previously PASSED. **New concurrency-fix SHA not yet rerun on Windows**: `NOT RUN` for latest-source local parity; REMOTE independently passed. See [Windows runbook](runbooks/phase5-local.md).

## Task-by-task completion ledger

| Phase 5 task | Status | Condition needed to close |
|---|---|---|
| P5-01 | PARTIAL / PASSED for current Host/DI boundary only | Employer-approved secure Controller → Service → Provider/Repository integration; no public business endpoints exist today |
| P5-02 | BLOCKED | Employer/Product approve taxonomy, label cardinality and final response DTO/status/evidence/version semantics |
| P5-03 | BLOCKED | Engineering + Product/Data Governance approve persistence, immutable audit and retention; then implement Result/Evidence/Audit and prove multi-row rollback with real PostgreSQL |
| P5-04 | BLOCKED | Product/Security approve idempotency namespace, retry/conflict semantics and record identity; implement and test real request/review retry cases |
| P5-05 | BLOCKED | Security/Employer approve IdP/principal model, roles/tenant/record isolation and retention; implement AuthN/AuthZ and adversarial IDOR/record tests |
| P5-06 | PARTIAL / PASSED for current safe failure paths | Final approved business API request-size/rate-limit/SLO/backpressure and real model timeout policy; verify live workload |
| P5-07 | PARTIAL / PASSED for existing health/error contracts | Approved v1 classification/reviewer DTO + OpenAPI schema and compatibility regression |
| P5-08 | DEFERRED / NOT RUN (actual E2E); BLOCKED prerequisites | Authorized model, taxonomy, secure API/review flow, actual PostgreSQL Result/Evidence/Audit persistence, approved test environment; integrated request→review→audit test |
| P5-09 | DEFERRED / NOT RUN | Authorized independent Gold/OOD, released model/decision/explanation versions and approved regression criteria |
| P5-10 | DEFERRED / NOT RUN | Representative authorized workload, model-capable compute, approved latency/throughput/capacity goals; measured stress/soak |
| P5-11 | PARTIAL / PASSED current DB unavailable/recovery, DI/middleware and missing-model/timeout unit paths | Business partial-commit, concurrent review, missing-secret scenarios in approved integration, and real model timeout/recovery drills still BLOCKED/DEFERRED |
| P5-12 | PARTIAL / DOCUMENTED for currently existing interfaces | Final API/error/feature flags/version compatibility, model/reviewer operational runbooks require approved final implementation |

## Acceptance (DoD) matrix

| Mandatory DoD | Verdict | Evidence / blocker |
|---|---|---|
| Actual request→result→review→audit E2E with real services | BLOCKED/NOT RUN | No authorized business API/reviewer workflow/model release |
| Atomic persisted Result/Evidence/Audit, no partial state | BLOCKED/NOT RUN | Missing employer-approved business schema and transaction logic; generic DB tests are not equivalent |
| Never convert security/infra errors into fake success or OUT_OF_SCOPE | PASSED for currently exposed existing paths only | Safe 503/unavailable/redacted 500 and provider fail-closed regressions; not final business API |
| Approved taxonomy/model compatibility + v1 data contract | BLOCKED/NOT RUN | Approved taxonomy, cardinality and external DTO absent |
| Real model/Explanation Gold regression | DEFERRED/NOT RUN | Lawful independent Gold and approved ML release absent |
| Measured p50/p95/p99, CPU/GPU, memory, throughput, soak | DEFERRED/NOT RUN | Approved targets, model hardware and representative workload absent |
| No runtime fake provider | PASSED for inspected independent code | Test doubles live only in tests; no production business classification route exists |

**Hard decision:** The required DoD is not complete, so changing the Marker to `PHASE_5_COMPLETE_READY_FOR_PHASE_6` would misrepresent the project. The existing scoped `CONDITIONAL_PROGRESSION_APPROVED` for Phase 6 is **not** a Phase 5 completion.

## External inputs, risk owners, and Phase 6 closure checkpoint

- **Employer / Product / Taxonomy:** signed category taxonomy, single/multi-label policy, API/DTO rules and numeric quality targets. Blocks P5-01/02/07/08/09 and the relevant contract-specific P5-06 work.
- **Security / Data Governance / Review Owner:** data-use authorization, privacy/retention, identity, RBAC/ABAC tenant/record scope, review/audit/idempotency approval. Blocks P5-03/04/05/08 and real P5-11 concurrency/atomic review tests.
- **ML / Data Owner:** lawful disjoint Train/Validation/Gold/OOD, real model artifact and tokenizer/taxonomy versions, calibration/groundedness criteria. Blocks P5-08/09, and all carried model-dependent P3/P4 gates.
- **Engineering / Operations:** approved PostgreSQL business schema, secured deployment/model compute, representative workload, capacity/SLO, failure/rollback environment. Blocks real P5-03/08/10/11 and final hardening.

**Earliest closure:** Re-run actual tasks as soon as approved inputs exist. **Mandatory latest checkpoint:** Phase 6, *before* final acceptance and production release; all deferred model/security/reviewer tests must then be executed and assessed, never treated as PASSED merely because CI is green.

**No secret, password, live DSN, private text, Gold data or unapproved model artifact is requested or committed.** This document does not change an employer contract or mark any test as PASSED without observed evidence.

## Engineering-owned Phase 5 backlog follow-up — 2026-10-24

**Owner request:** Complete the remaining work that the assistant/Engineering can perform without manufacturing external contracts. **Engineering-led result:** two safe independent improvements were implemented and verified; no employer/ML/Operations approval was fabricated.

1. **P5-01 factory creation failure (code+test):** `src/host/app.py` now resolves the required app version inside the existing DI factory exception guard. `tests/test_phase5_host.py::test_factory_missing_version_metadata_cleans_di` verifies that invalid/missing version metadata cleans the container and permits a clean retry. Existing Host/API surface is unchanged.
2. **P5-03/P5-11 independent atomicity evidence (test only):** `tests/test_postgres.py::test_phase5_real_postgres_two_write_atomicity_and_rollback` runs against the actual isolated PostgreSQL database. Two synthetic rows are written inside the existing `PsqlDbContext.transaction()` and deliberately rolled back on a middle failure; the test then proves that two successful writes commit atomically. It uses a temporary table and a connection-pinned, test-only session factory. **This proves infrastructure transaction semantics only.** The actual Result/Evidence/Audit model, business idempotency/unique constraints and reviewer write race are not implemented/verified without a signed schema; P5-03 as a feature remains BLOCKED.

**Verified remote code source:** [commit 2ac58f4](https://github.com/Amirmahdimtz/text-classification-service/commit/2ac58f419752f52540d146ef5be5b1126abc68c5); [CI run 40103494346](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40103494346) completed SUCCESS for all four jobs. Independent **86 PASSED / 1 SKIPPED / 5 DESELECTED**, real isolated PostgreSQL **5 PASSED / 1 SKIPPED / 86 DESELECTED**; synthetic offline ML **29 PASSED** (overlap); Docker API health and Alembic smoke PASS; dependency `pip check` PASS and strict OSV `No known vulnerabilities found` at scan time. Two existing Starlette/httpx and AnyIO deprecation warnings. No public HTTP business feature, permanent table, migration, or model deployment was added. **LOCAL_USER on this latest source SHA: NOT RUN**; older owner Windows evidence remains source-specific.

**Engineering responsibilities now bounded by external decisions:** Further code for P5-01..05/07/08 requiring actual Controller/DTO/AuthZ/schema/retention would freeze customer policy without approval. A production-grade implementation cannot be promised from fixtures. Product/Taxonomy must sign labels, cardinality and API response semantics; Security/Review/Data Governance must authorize IdP, data rights, tenant/record isolation, retention, real audit/idempotency; ML/Data Owner must provide lawful Gold/OOD and a versioned, evaluated model; Operations must supply representative compute/workload and approved SLO/release/recovery conditions. **As soon as approvals arrive**, Engineering is responsible for implementing the corresponding actual business API, migrations, atomic repositories, permission and concurrency tests, model integration and regression—not for making those employer decisions itself.

**Status separation:** Official Phase 5 marker stays `PHASE_5_IMPLEMENTED_AWAITING_VERIFICATION`; full Phase 5 DoD remains **NO-GO**. ADR-014's narrow independent `CONDITIONAL_PROGRESSION_APPROVED` for P6-02/04/06/12 remains valid, **Phase 6 NOT STARTED** until a new explicit owner command. Deadline for all deferred model/identity/business tests: **before Phase 6 final acceptance**.

## Phase 5 owner final-completion demand — verified independent scope, hard DoD boundary (2026-10-24)

A further independent P5-06 defect was corrected: waiting for provider capacity and model execution previously each had a fresh full timeout. The provider now measures one monotonic deadline and uses only the remaining budget, with a synthetic-only regression; [source commit 79062be3](https://github.com/Amirmahdimtz/text-classification-service/commit/79062be3bcfb5a1a95a870642abac432ae7a91db), [CI 40104414514](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40104414514) SUCCESS all four jobs (independent 87 PASSED/1 SKIPPED; real isolated PostgreSQL 5 PASSED/1 SKIPPED; offline synthetic ML 30 PASSED; dependency scan/compatibility PASSED). No actual model latency/Gold inference benchmark was run. This hardens only currently existing provider behavior and is **not** proof of P5-10.

The precise unresolved decisions, owners, dependent engineering work and non-substitutable real acceptance tests are packaged in [Phase 5 required inputs](phase-5-acceptance-inputs.md). Until these customer/product/security/data/model/runtime conditions exist and full DoD is really verified, full Phase 5 completion is **BLOCKED**, even though current independently accessible code/tests are green. Previous successful Windows runs belong to older source SHAs; latest-source Windows LOCAL_USER is **NOT RUN**. No hidden phase-marker upgrade or unapproved Phase 6 start.
