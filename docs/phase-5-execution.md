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

