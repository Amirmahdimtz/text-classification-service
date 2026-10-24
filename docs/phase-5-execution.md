# Phase 5 — Independent integration and resilience execution ledger

**Date:** 2026-10-24  
**Start:** Explicit owner instruction `فاز ۵ را شروع کن`.  
**Initial main HEAD:** `f57281fba6af42af24791045b7c928d3b1a977d0`.  
**Entry decision:** [ADR-013](decisions/ADR-013-phase5-conditional-entry-authorization.md), `CONDITIONAL_PROGRESSION_APPROVED` for *named safe independent Phase 5 subscopes only*.  
**Previous official markers:** `PHASE_4_IMPLEMENTED_AWAITING_VERIFICATION`, `PHASE_3_IMPLEMENTED_AWAITING_VERIFICATION`; last full technical gate `PHASE_2_COMPLETE_READY_FOR_PHASE_3`.  
**Current marker:** `PHASE_5_IMPLEMENTED_AWAITING_VERIFICATION` (partial scope delivered; full Phase 5 NOT accepted).

## Root-cause audit and change boundary

The current server has two low-level HTTP routes (`/health/live`, `/health/ready`) and no business classification/reviewer Controller. `PsqlDbContext.ping_async` normally returns a boolean, but a unexpected DB health-check exception would escape the Host readiness endpoint and be mapped by global middleware to HTTP 500 instead of explicit not-ready 503. The request-context token reset also ran only on the normal middleware return path, rather than in `finally`, risking retention on cancellation/exception. These errors are independent of employer contracts, so they were corrected without changing business semantics.

The existing model provider is independently testable and refuses inference before a configured, validated release. It must not be wired to public inference routes or claimed ready without customer-approved model/taxonomy/identity/privacy inputs. The existing `/health/ready` is **DB-only**; no final model readiness is implemented. Core/infrastructure naming, `@inject` discovery, singletons, bounded sessions and `Controller → Service → Repository → PsqlDbContext` conventions remain unchanged.

## P5-01..P5-12 task matrix

| ID | State / actual work | Environment, residual condition and Risk Owner |
|---|---|---|
| P5-01 | PARTIAL, TESTED: existing DI/Host/DB/provider boundary preserved; negative API and model-unavailable contract regression | REMOTE; no public classifier wiring until signed API/AuthN, taxonomy and model; Engineering/Product/Security |
| P5-02 | BLOCKED: final classification Response DTO and API not invented | Employer/Product approve label cardinality, taxonomy and API version |
| P5-03 | BLOCKED: business Result/Evidence/Audit atomic persistence not implemented; generic transaction regression exists | Employer/Product/Engineering approve physical schema and audit/retention, then PostgreSQL multi-row rollback tests |
| P5-04 | BLOCKED: no business idempotency or reviewer retry workflow | Product/Engineering/Security approve request identity, namespace, conflict/TTL semantics |
| P5-05 | BLOCKED: no authorized principals/tenant/record-scoped API | Security/Employer approve IdP, RBAC/ABAC, record isolation and retention, then IDOR tests |
| P5-06 | PARTIAL, TESTED: DB readiness exceptions fail closed to redacted HTTP 503; global 500 redaction and safe headers regressions | REMOTE; customer request limits, timeout/backpressure policy and sensitive public API await approved parameters; Engineering/Security/Ops |
| P5-07 | PARTIAL, TESTED: contract regression for existing health paths, response headers, unavailable endpoints and hidden OpenAPI; no new v1 business contract | REMOTE; final DTO/OpenAPI backward compatibility BLOCKED pending Product/Employer approval |
| P5-08 | BLOCKED/DEFERRED/NOT RUN: no real API→Model→DB→Review→Audit E2E | SERVER_MODEL; model/taxonomy/privacy/identity/schema/reviewer approvals; Engineering/ML/Security/Ops; before Phase 6 acceptance |
| P5-09 | DEFERRED/NOT RUN: no Gold model/decision/explanation/version regression | SERVER_MODEL; authorized independent Gold and approved release; ML/Data Owner; before Phase 6 acceptance |
| P5-10 | DEFERRED/NOT RUN: no real inference latency/load/stress/soak | SERVER_MODEL; representative workload, model runtime and approved SLO/hardware; ML/Ops; before Phase 6 acceptance |
| P5-11 | PARTIAL, TESTED: synthetic DB readiness failure/recovery, HTTP 500 sanitization, missing model/unready provider; real isolated PostgreSQL connection refusal and recovery to independent test DB | REMOTE; actual business partial-commit, reviewer concurrency, real model timeout/E2E and infra-level outage drill remain BLOCKED/DEFERRED; Engineering/ML/Security |
| P5-12 | IMPLEMENTED for limited scope: this ledger, PowerShell runbook, status/risk update and truthful README | REMOTE docs; final business API, release, operation and model docs still blocked |

## Created / modified files

- **Modified:** `src/host/app.py` (safe readiness 503; middleware `finally` cleanup), `tests/test_postgres.py` (real isolated DB test), `tests/test_phase5_host.py` (test warning cleanup after first run), `README.md`, `docs/phase-status.md`, `docs/risk-register.md`.
- **Created:** `tests/test_phase5_host.py`, `docs/phase-5-execution.md`, `docs/runbooks/phase5-local.md`.
- **Migration:** NONE; no approved new SQLAlchemy business model or Alembic revision. Empty-graph smoke only.

## Verification evidence and interpretation

**Software source:** [commit 4c90b1d](https://github.com/Amirmahdimtz/text-classification-service/commit/4c90b1d125bd09117a0cb13c81b160b49cda3a1a).

**REMOTE/AVAILABLE — [GitHub Actions run 40097255880](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40097255880), SUCCESS, same source SHA:**

| Job | Commands represented in committed workflow | Actual result |
|---|---|---|
| `independent` | `python -m compileall -q src tests tools`; `python tools/verify_phase1_docs.py`; `python -m pytest -q -m 'not postgres'` | 80 PASSED, 1 SKIPPED (optional ML), 4 DESELECTED |
| `integration` | Docker Compose local API/PostgreSQL; `python -m pytest -q -m postgres`; Alembic `current` + `upgrade head` | 4 PASSED, 1 SKIPPED, 80 DESELECTED; Docker/API health and empty Alembic graph smoke SUCCESS |
| `ml-independent` | Offline synthetic ML suite listed in `.github/workflows/phase2-ci.yml` | 27 PASSED, overlapping other tests; not real model accuracy |
| `dependency-security` | `python -m pip check`; `python -m pip_audit --local --vulnerability-service osv --strict --timeout 60` | PASSED, no known vulnerabilities at scan time (not a full security sign-off) |

Test suite counts overlap; **do not add them**. Two pre-existing Starlette/httpx and AnyIO compatibility deprecation warnings persist; the new test-only collection warning found in the initial CI has been removed by renaming the fixture class. Reverify on the final SHA CI. This run contains live isolated PostgreSQL and Docker tests, **not** real customer schema, classifier, reviewer transaction, or ML Server.

**LOCAL_USER — owner-supplied Windows PowerShell test log for final source `2129d174c416adceeefa3a5de1740d6e9fc1667b`, 2026-10-24:** `git status --short` empty; origin `Amirmahdimtz/text-classification-service`, `main` up to date. `python -m pip install -r requirements-dev.txt` satisfied, `python -m compileall -q src tests tools` exited successfully, `python tools/verify_phase1_docs.py` PASS (27 required files), `python -m pytest -q tests/test_phase5_host.py` **5 PASSED**, `python -m pytest -q -m "not postgres"` **82 PASSED / 4 DESELECTED**, `python -m pytest -q -rs -m postgres` **4 PASSED / 82 DESELECTED**, without SKIPs or FAILs in either complete marker run. The PostgreSQL tests have isolated `*_test` database safeguards in source and were executed by the owner; this is genuine local database integration evidence, **not** a full business E2E. The five Host tests are included in the independent suite; do not double count. Two pre-existing warnings (Starlette/httpx and AnyIO BlockingPortal) do not fail these tests. Local Python interpreter version was **not printed** by this log; no version-specific parity assertion is made. `pip` remains **25.0.1** (outdated version noted by installer); local OSV scan/pip audit is **NOT RUN** for this final environment, and previously documented pip advisories require remediation/recheck before any security gate claim. See [Phase 5 Windows runbook](runbooks/phase5-local.md) and ADR-012.

**Final REMOTE source confirmation:** [GitHub Actions run 40097731345](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40097731345) SUCCESS on exact final SHA `2129d174c416adceeefa3a5de1740d6e9fc1667b` — independent 81 PASSED / 1 SKIPPED / 4 DESELECTED, isolated PostgreSQL 4 PASSED / 1 SKIPPED / 81 DESELECTED, offline synthetic ML 27 PASSED (overlap), and dependency compatibility/OSV scans PASSED. This remote clean audit applies to its **separate patched CI environment**, not to the owner's local pip 25.0.1 installation.

**SERVER_MODEL:** No approved taxonomy/dataset/model/server or numerical acceptance targets were provided. All genuine baseline/encoder, Gold/OOD/calibration, explanation groundedness, model-integrated API+review E2E, GPU/CPU capacity, release/rollback and load tests remain BLOCKED/DEFERRED/NOT RUN. Independent software fixtures cannot discharge them.

## Security, architectural and acceptance limits

- New tests use **non-confidential synthetic strings only**; fake engine or DI objects occur in tests, never Production.
- No secrets, test DSN or private report contents are added to Git; API never responds with exception strings.
- PostgreSQL test connects only to an explicitly named `*_test` database and a refused local port; does not shut down a server, drop tables, migrate schema or delete volumes.
- No changes to Core decision logic, DI auto-discovery or provider model selection. Missing model continues to fail closed.
- **Full Phase 5 DoD remains OPEN:** real model+API+Postgres+Review+Audit, authenticated record access, multi-row business atomicity, Gold regression, approved latency targets and model-dependent load all lack required contracts or evidence.
- **Official marker remains `PHASE_5_IMPLEMENTED_AWAITING_VERIFICATION`.** No `PHASE_5_COMPLETE_READY_FOR_PHASE_6` and no `CONDITIONAL_PROGRESSION_APPROVED` for Phase 6 is issued automatically. Final employer acceptance is Phase 6 only.

## Residual risk owners / evidence debt checkpoint

- Taxonomy/cardinality/classification semantics and quality targets: Employer/Product/Taxonomy (DEC-01/02/03/09).
- Real data rights, original evidence relevance/Gold/OOD and feedback provenance: Data Owner/ML/Expert Review (DEC-04).
- AuthN/AuthZ, tenant/record isolation, personal data retention/egress: Security + Employer Review Owner (DEC-06/08).
- Business physical schema, immutable audit, idempotency, reviewer race tests: Engineering + Product + Security (DEC-07/11).
- Runtime readiness, measured concurrency/latency and secure rollback: ML + Operations (DEC-10).
- **Latest closure checkpoint:** before Phase 6 final acceptance (prefer earlier if approved); re-evaluate each blocked subtask as soon as actual inputs are delivered. See [current risk register](risk-register.md).


## Owner Windows dependency-security follow-up — 2026-10-24

**Evidence source:** Owner-submitted PowerShell log from the existing project `.venv`, following the previously verified Windows run on `2129d174c416adceeefa3a5de1740d6e9fc1667b`. This is supplied **LOCAL_USER** evidence, not execution by the assistant or GitHub. The follow-up did not print a fresh Git SHA or `$LASTEXITCODE`; the command outputs show no errors and each command returned to the prompt.

| Security command | Actual owner-reported result | Status / scope |
|---|---|---|
| `py -3.12 -m pip --python .\.venv\Scripts\python.exe install "pip==26.2.2"` | Replaced pip `25.0.1` with `26.2.2` (`Successfully installed`) | PASSED; addresses the previously flagged local pip version only |
| `python -m pip install "pip-audit==2.10.1"` | Exact scanner version already satisfied in project venv | PASSED / PRESENT |
| `python -m pip check` | `No broken requirements found.` | PASSED; dependency installation consistency, not a security scan |
| `python -m pip_audit --local --vulnerability-service osv --strict --timeout 60` | `No known vulnerabilities found` | PASSED, owner-reported; applies to installed local package set at scan time, no claim about uninstalled optional dependencies |

**Updated local R-17 checkpoint:** Local dependency-compatibility and strict OSV audit evidence is now **PASSED for the scanned Windows virtualenv**, superseding its earlier `NOT RUN` at this checkpoint. Continuous OSV rechecks remain mandatory when packages, advisories or deployment environment change. No dependency update to application code or `requirements*.txt` was committed here. The earlier Windows functional regression **82 PASSED** and actual isolated PostgreSQL **4 PASSED** remain separate evidence; the user did not re-run them in this follow-up, and no new application test execution is claimed.

**Security boundary:** A clean dependency audit is not a Phase 5 full security gate, AuthN/AuthZ/IDOR review, data privacy approval, model review, production vulnerability attestation or SERVER_MODEL benchmark. Two existing Starlette/httpx and AnyIO deprecation warnings remain. **Marker: `PHASE_5_IMPLEMENTED_AWAITING_VERIFICATION`. No Phase 6 authorization.**

## Independent Phase 5 gate review and Root Cause repair — 2026-10-24

**Audit request:** owner directed detailed Phase 5 correctness review, corrections within approved scope, and explicit Phase 6 gate judgment. Read Architecture Guide, approved Plan 1.1.0 P5-01..P5-12, `main`, ADR-008/010/013, prior owner Windows evidence and CI.

| Finding | Root cause | Change / evidence | Residual |
|---|---|---|---|
| P5-01 factory partial failure | `web.mount(app)` happened outside the factory exception guard, so missing/import-failing Controller could retain DI bootstrap state | Moved mount under guarded cleanup; test proves `resolve()` fails after aborted factory, then a fresh factory succeeds | Real business Controllers still BLOCKED by employer identity/API contracts |
| P5-01/P5-11 shutdown partial failure | Failed DB engine disposal exited `finally` before `shutdown_di()` | Nested `finally` guarantees DI cleanup even if DB engine dispose fails; negative-path test with a test-only disposal error | Real infrastructure disaster/recovery drill remains SERVER_MODEL/Operations |
| P5-06/P5-11 provider lifecycle race | `close_async` cleared model without serializing against async warmup; warmup could later republish a closed model reference | Closing flag plus shared `_load_lock` synchronizes teardown after warmup; deterministic test-only event coordination tests the race and fail-closed predict | Actual release model and model-enabled Readiness still BLOCKED |

**Corrected source:** [commit fda5b106](https://github.com/Amirmahdimtz/text-classification-service/commit/fda5b1062010ccbf10e8715195c496b378f95e6c); **REMOTE evidence:** [GitHub Actions run 40100292584](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40100292584) all four jobs SUCCESS: independent 84 PASSED/1 SKIPPED/4 DESELECTED, live isolated PostgreSQL 4 PASSED/1 SKIPPED/84 DESELECTED, offline ML 28 PASSED (overlap), Docker/API/Alembic smoke PASSED, compatibility and strict OSV scan PASSED. The two Starlette/httpx and AnyIO compatibility warnings persist. Tests are synthetic for model behavior; real Gold/model evaluation **NOT RUN**.

**Corrected SHA LOCAL_USER:** Windows local independent/PostgreSQL rerun **NOT RUN** for the fix SHA; prior owner run 82 independent + 4 PostgreSQL PASSED on previous source and later pip/OSV security scan PASSED locally. To reverify, follow [Phase 5 Windows runbook](runbooks/phase5-local.md). Expected CI comparison is not a local pass assertion. No Phase 5 business Migration/Model/DTO/Controller added.

**Gate verdict:** Full Phase 5 `PHASE_5_COMPLETE_READY_FOR_PHASE_6`: **NO-GO** (actual task/DoD blockers P5-02..05, real P5-08/09/10, reviewer multi-record transaction/concurrency/IDOR, approved customer/API/ML data). Independent **limited** Phase 6 scope only: **CONDITIONAL GO** by [ADR-014](decisions/ADR-014-phase6-conditional-technical-entry.md) for P6-02/P6-04/P6-06/P6-12 narrowly specified subsets. No Phase 6 code was executed under this authorization; explicit `فاز ۶ را شروع کن` remains required, and no Production release/acceptance is allowed. R-01/02/05/06/07/11/12/13/14/16 remain blocked, owned per [risk register](risk-register.md), final closure checkpoint Phase 6 acceptance.

## Owner Windows post-fix verification — 2026-10-24

- **Evidence origin:** owner-provided local PowerShell log, project `text-classification-service` on `main` at `684bbbdf88f959f8197b56321ae3136a53355db5`; `git status --short` empty, `git pull --ff-only` successful. The verified commit **contains** the Phase 5 Host/Provider lifecycle corrections from `fda5b1062010ccbf10e8715195c496b378f95e6c` and the [ADR-014](decisions/ADR-014-phase6-conditional-technical-entry.md) technical-scope decision. The owner's interpreter log explicitly identifies Windows Python **3.12.10**, pytest **9.0.3**.
- **LOCAL_USER independent checks — PASSED:** `python -m compileall -q src tests tools` completed silently; `pytest -q tests/test_phase5_host.py tests/test_text_classifier_provider.py` **11 PASSED**, 2 known test-client deprecation warnings. Full `pytest -m "not postgres"` collected 89 tests, **85 PASSED / 4 DESELECTED**, 2 warnings and **0 FAILED**.
- **LOCAL_USER real isolated PostgreSQL — PASSED:** `pytest -q -rs -m postgres` **4 PASSED / 85 DESELECTED**, 2 warnings, **0 FAILED/SKIPPED** on this Windows checkout. Test code enforces an isolated `*_test` database and tests a refused local connection plus the available database; no production data or business transaction/schema acceptance is claimed. The 11 targeted tests overlap with the independent 85; the marker-separated 85 + 4 = **89 unique collected tests passed**. No executed test failures were reported.
- **Corroborating REMOTE/AVAILABLE:** [GitHub Actions run 40100632418](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40100632418) **SUCCESS** on exactly `684bbbdf88f959f8197b56321ae3136a53355db5`, independent **84 PASSED / 1 SKIPPED**, PostgreSQL **4 PASSED / 1 SKIPPED**, offline synthetic ML **28 PASSED**, dependency OSV/compatibility PASSED; jobs overlap. Windows ran the optional test successfully, explaining the independent count difference.
- **Supersedes:** earlier `LOCAL_USER NOT RUN` on the corrected-code SHA in the historical gate review above, **for software compilation, targeted regressions, independent suite and live isolated PostgreSQL only**. Previous owner-reported local strict OSV clean scan remains separately recorded; it was **not rerun in this particular log**. Real model/Gold/OOD/calibration, employer-owned taxonomy, AuthN/AuthZ, reviewer E2E, business atomicity and load/stress remain BLOCKED/DEFERRED.
- **Gate integrity:** `PHASE_5_IMPLEMENTED_AWAITING_VERIFICATION` retained. Only [ADR-014](decisions/ADR-014-phase6-conditional-technical-entry.md)'s narrowly scoped `CONDITIONAL_PROGRESSION_APPROVED` for independent future Phase 6 work remains in force; **Phase 6 NOT STARTED**, full Phase 5 DoD **NO-GO**, no `PROJECT_PRODUCTION_READY_ACCEPTED`.

## Phase 5 explicit completion request — final bounded closeout assessment (2026-10-24)

Owner requested full Phase 5 closure. See [formal task and acceptance audit](phase-5-closure-audit.md): final DoD still **BLOCKED/DEFERRED**, no signed category/business/security/data/model contracts; complete Marker cannot be issued. In the independently permitted runtime scope, discovered and fixed a post-capacity waiting/close race in `TextClassifierProvider.predict_async`; [commit 28afaefb](https://github.com/Amirmahdimtz/text-classification-service/commit/28afaefbbd33ab05fcacba37a1c35ca316d1b47e). [GitHub CI 40102628553](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40102628553) SUCCESS all four jobs: independent 85 PASSED/1 SKIPPED, real isolated PostgreSQL 4 PASSED/1 SKIPPED, offline synthetic ML 29 PASSED (overlap), Docker/API/Alembic, `pip check` and strict OSV PASS. Previous Windows test source differs and newest source local checks NOT RUN. Marker stays `PHASE_5_IMPLEMENTED_AWAITING_VERIFICATION`; Phase 6 only conditionally authorized in ADR-014, not started. **Migration: NONE**. No public Controller/DTO/business DB model, no training or sensitive data.

## Engineering-owned Phase 5 backlog follow-up — 2026-10-24

- **Fixed:** `create_app()` now validates `app.version` while the DI initialization cleanup guard is active. Test `test_factory_missing_version_metadata_cleans_di` asserts fail-closed constructor path and subsequent fresh bootstrap. [Source 2ac58f4](https://github.com/Amirmahdimtz/text-classification-service/commit/2ac58f419752f52540d146ef5b1126abc68c5).
- **Added REAL PostgreSQL integration:** `test_phase5_real_postgres_two_write_atomicity_and_rollback` in `tests/test_postgres.py` uses an isolated `*_test` database and a temporary table; failed two-write transaction rolls back both writes; successful transaction commits both. This is **generic PsqlDbContext transaction evidence**, not persisted approved business Result/Evidence/Audit, idempotency or reviewer concurrency.
- **CI:** [40103494346](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40103494346) SUCCESS exact code SHA: independent 86 PASSED/1 SKIPPED/5 DESELECTED; PostgreSQL 5 PASSED/1 SKIPPED/86 DESELECTED; offline synthetic ML 29 PASSED (overlap); Docker/API/Alembic smoke and dependency compatibility/strict OSV PASSED. **Latest Windows LOCAL_USER NOT RUN**; previous owner evidence on older SHA. No model evaluation, Gold regression, production Security review or load test occurred.
- **Remainder:** [formal task/DoD audit](phase-5-closure-audit.md) explicitly identifies owner and gate for every P5 task; engineer cannot instantiate customer-specific AuthZ/Taxonomy/Schema/data rights in place of their approval. New migrations: NONE. Production stubs: NONE. Full Phase 5: BLOCKED; narrow future Phase 6 progression per ADR-014 still conditional, not started.

## Phase 5 owner final-completion demand — verified independent scope, hard DoD boundary (2026-10-24)

- **P5-06 runtime defect:** Per-stage `asyncio.wait_for(timeout_seconds)` in `TextClassifierProvider.predict_async` could consume a full capacity-wait budget **plus** another full inference-execution budget. A monotonic deadline computed before capacity wait is now used for the remaining execution budget, with no worker-slot leak on deadline expiry. Test-only regression `test_provider_timeout_budget_is_shared_between_capacity_and_execution`. [Code commit 79062be3](https://github.com/Amirmahdimtz/text-classification-service/commit/79062be3bcfb5a1a95a870642abac432ae7a91db); [CI run 40104414514](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40104414514) 4/4 jobs SUCCESS — independent 87 PASSED/1 SKIPPED/5 DESELECTED, live isolated PostgreSQL 5 PASSED/1 SKIPPED, offline synthetic ML 30 PASSED (overlap), packaging compatibility/OSV PASS at scan time.
- **P5-12 acceptance/inputs:** [Phase 5 decision and real-evidence package](phase-5-acceptance-inputs.md) maps each missing authorization, accountable owner, allowed next coding scope and mandatory real tests. This is not an employer agreement or ML evaluation. No Migration/Model/DTO/Controller added. Latest-source local Windows regression **NOT RUN**, remote equivalent PASSED. Full P5-01/02/03/04/05/08/09/10 and contract-specific portions of P5-06/07/11/12 remain **BLOCKED/DEFERRED**, not passed by software fixtures.
- **Final gate:** `PHASE_5_IMPLEMENTED_AWAITING_VERIFICATION` remains official; [ADR-014](decisions/ADR-014-phase6-conditional-technical-entry.md) allows independent future Phase 6 work but does not start Phase 6 or authorize release.

## Owner-directed dynamic taxonomy foundation — 2026-10-24

Independent taxonomy development based on owner instruction is documented in [ADR-015](decisions/ADR-015-dynamic-taxonomy-draft-foundation.md): dynamic draft editing/activation-state safety, immutable earlier snapshots, stable identity preservation and model-version compatibility validation. Actual category set remains TBD, with **no real organization management API/persistence or publication**. [Code ed876e0](https://github.com/Amirmahdimtz/text-classification-service/commit/ed876e0a88d0a62c05e2b9c9ca3d669471003a31); [CI 40105875237](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40105875237) SUCCESS all 4 jobs (independent 106 PASSED/1 SKIPPED/5 DESELECTED; isolated PostgreSQL 5 PASSED/1 SKIPPED; offline synthetic ML 30 PASSED; dependency-security compatibility/OSV PASSED). New files `src/core/services/taxonomy/__init__.py`, `taxonomy_service.py`, `tests/test_taxonomy_drafts.py`, `docs/decisions/ADR-015-dynamic-taxonomy-draft-foundation.md`. **No Migration or external public API**. Current P5-02/03/04/05/08/09/10 and contract-dependent scope still BLOCKED/DEFERRED; local Windows testing on latest code NOT RUN.


## Owner full-completion follow-up — structural revision safety (2026-10-24)

**Request:** fully complete Phase 5. Fully read the approved Architecture Guide and Implementation Plan v1.1.0 §§3, 6, 11, 13/16; audited GitHub `main`, original P5 task matrix, ADR-001/002/005/006/013/014/015, independent tests and CI. This is a continuation of Phase 5, **not a new Phase 6 start**.

**P5-01/P5-11 safe engineering contribution:** Dynamic taxonomy revision safety is now checked by a pure Core operation `TaxonomyService.assess_revision(previous, draft)`. The checker requires correct parent linkage, preserved historical category IDs and an inactive state for newly introduced categories. It rejects implicit reactivation without an approved workflow; returns an immutable deterministic report of added/deactivated/revised codes. Every new taxonomy version is marked as requiring model compatibility revalidation, including version-only changes. No category definitions, roles or models have been invented. This **does not** authorize a publish/release and cannot close P5-02/03/05 or model-dependent P5-08/09.

**Code:** [4908ca18](https://github.com/Amirmahdimtz/text-classification-service/commit/4908ca1862f9417dc316e995b2770c1212febc24), changes only `src/core/services/taxonomy/taxonomy_service.py` and `tests/test_taxonomy_drafts.py`. No new Controller, Repository, Model, Migration or HTTP route.

**REMOTE/AVAILABLE actual test evidence:** [GitHub Actions #40107406832](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40107406832), exact SHA, 4/4 SUCCESS: independent **114 PASSED / 1 optional SKIPPED / 5 DESELECTED**; real isolated PostgreSQL **5 PASSED / 1 optional SKIPPED / 114 DESELECTED**; offline synthetic ML **30 PASSED** (overlap); Docker/API/Alembic smoke and dependency compatibility / strict installed-closure OSV PASSED. Two established Starlette/httpx and AnyIO deprecation warnings. **Latest Windows LOCAL_USER NOT RUN**; previously successful Windows logs refer to older code SHAs.

**Gate:** Full Phase 5 integration still **NO-GO**, because signed taxonomy/business DTO, physical Result/Evidence/Audit+Idempotency, AuthN/AuthZ/tenant and reviewer records, permitted real model, Gold/OOD and live performance environment are absent. `PHASE_5_IMPLEMENTED_AWAITING_VERIFICATION` remains. `CONDITIONAL_PROGRESSION_APPROVED` applies only to ADR-014's technical P6-02/04/06/12 subsets, and Phase 6 **NOT STARTED**. All P5-08/09/10 real verification debt remains due **before Phase 6 final acceptance**. See [input/approval package](phase-5-acceptance-inputs.md) and [task closure audit](phase-5-closure-audit.md).
