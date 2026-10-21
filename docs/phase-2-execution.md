# Phase 2 execution and technical acceptance ledger

**Started by explicit project-owner command:** 2026-10-21
**Initial GitHub main:** `39b02e2e4b558ddf454c3117a250872af1716d32`
**Prior marker:** `PHASE_1_COMPLETE_READY_FOR_PHASE_2` (verified)
**Architecture:** Host → Application → Core → Infrastructure, with convention-based @inject DI and isolated PostgreSQL sessions. No commercial Classification API/model/taxonomy is implemented in this phase.

## Scope decisions

The repository initially contained Phase 1 design docs, ADR-001..008, and `tools/verify_phase1_docs.py`; `src`, requirements, tests, migrations and CI did not exist. All business-specific schemas/API and authorization providers remain blocked by external decisions (ADR-001..007 proposed; ADR-008 accepted only for phase governance).

| Task | Implementation | Technical evidence / remaining gate |
|---|---|---|
| P2-01 | Python 3.13 FastAPI factory, environment validation, version-pinned dependency manifest | Independent config/startup unit coverage; real DB startup LOCAL_USER |
| P2-02 | @inject, annotation constructor resolution, convention scan, singleton/transient and strict controller import errors | Unit tests; test fixtures are not production providers |
| P2-03 | SQLAlchemy Async engine/sessionmaker, PsqlDbContext, shared engine, BaseRepository and atomic transaction context | Real PostgreSQL PASSED in isolated GitHub CI (2 integration tests); Windows-local evidence pending |
| P2-04 | No unapproved physical business tables created | BLOCKED DEC-01, DEC-02, DEC-08, DEC-11 |
| P2-05 | Transaction context available in Infrastructure; no fabricated idempotency table/API | Live PostgreSQL rollback path PASSED in CI; scoped idempotency policy BLOCKED DEC-07/11 |
| P2-06 | Runtime controller discovery only; no invented taxonomy CRUD/API | BLOCKED DEC-01, DEC-06, DEC-07 |
| P2-07 | Fail-closed config; no exposed sensitive routes; env-only DB credentials; redacted log allowlist; safe headers; no permissive CORS | Identity/RBAC/TLS topology, audit and rate-limit policy BLOCKED DEC-06/08 |
| P2-08 | Structured allowlisted logs, server-generated request ID, distinct liveness/readiness, DB-dependent startup and shutdown | Unit checks and real Docker startup/DB readiness PASSED in CI; Windows-local parity pending |
| P2-09 | Alembic async metadata environment with no business revisions | Alembic current/upgrade head PASSED against disposable CI PostgreSQL with empty revision graph; business migration/drift BLOCKED by schema approval |
| P2-10 | CI for Python compile, docs regression and independent tests; opt-in DB marker | GitHub Actions independent and integration jobs PASSED; dependency install and Phase 1 regression verified |
| P2-11 | Non-root Dockerfile; local-only development Compose DB and API health dependency | Docker image build, compose start and API readiness PASSED in GitHub CI; Windows-local parity pending |
| P2-12 | `docs/runbooks/phase2-local.md` with Windows PowerShell test and recovery commands | Documentation reviewed; local reproducibility needs owner evidence |

## Remaining externally owned decisions

| ID | Owner | Required input | Affected tasks | Continue independent work? | Status / risk / next action |
|---|---|---|---|---|---|
| DEC-01 | Employer/taxonomy | Approved catalog and release version | P2-04/06 | Yes | BLOCKED; incorrect categories; supply signed catalog |
| DEC-02/03 | Product/review | Cardinality and multi-topic/review rules | P2-04/05/06 | Yes | BLOCKED; invalid result shape; decide policy |
| DEC-04 | Data/security | Authorized representative dataset | Future Phases 3+ | Yes | BLOCKED; no data handling; provide legal basis |
| DEC-05 | Product/ops | Input envelope and load | P2-07, future | Yes | BLOCKED; unbounded sensitive ingress not exposed; agree limits |
| DEC-06 | Security/product | IdP, principals, RBAC, tenant/record isolation | P2-06/07 | Yes | BLOCKED; unauthorized access risk; specify identity contract |
| DEC-07 | API/product | Final endpoints, idempotency TTL/key namespace, response semantics | P2-05/06 | Yes | BLOCKED; compatibility/race risk; approve API |
| DEC-08 | Data/legal/security | Residency, retention, encryption, permitted topology | P2-04/07/09/11 | Yes | BLOCKED; disclosure risk; security decision |
| DEC-09 | ML/product | Quantitative quality targets | Later Phase 3+ | Yes | BLOCKED; no release claims |
| DEC-10 | Operations | Throughput, latency, RPO/RTO, infrastructure | P2-11, later | Yes | BLOCKED; capacity/recovery TBD |
| DEC-11 | Engineering/data | Physical DB IDs, FK, tenant/audit retention, migration policy | P2-04/05/09 | Yes | BLOCKED; schema corruption risk; approve schema |
| DEC-12 | Project owner | Governance of phase approvals | Phase gates | Yes | RESOLVED by ADR-008; final sign-off Phase 6 |

## Verification status semantics

- `PASSED` means a test was actually executed and produced confirming output; a test double validates control flow only, never a live ML model or PostgreSQL.
- `NOT RUN` means execution environment lacks a required runner/dependency; do not reinterpret as a pass.
- `BLOCKED` means necessary policy/schema/data is not approved; no substitutes are permitted.
- Local independent unit-test evidence (Python 3.13.5 with installed FastAPI 0.128.2, SQLAlchemy 2.0.50, Alembic 1.18.4): `python -m compileall -q src tests` EXIT 0; `python -m pytest -q -m 'not postgres'` **17 PASSED, 1 DESELECTED**. This does not include PostgreSQL, driver installation or actual lifespan startup. GitHub Actions status must be separately checked.
- `PHASE_2_IMPLEMENTED_AWAITING_VERIFICATION` is the permitted marker for implemented independent foundations lacking real PostgreSQL, migrations, startup and Docker/CI evidence; the technical complete marker requires those verifications or separately tracked signed exceptions consistent with ADR-008.

## Verified GitHub Actions evidence (2026-10-21)

- **Source commit:** `2b4c258819182819777120ae530f5c398d3fc9f7`.
- **Workflow:** [Phase 2 independent checks](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/39597343384), conclusion **success**.
- **Independent job — PASSED:** Python 3.13 dependency install including asyncpg 0.32.0; source/test compile; Phase 1 regression validator `PASS: 27 required files`; pytest `17 passed, 2 deselected`.
- **Integration job — PASSED:** real PostgreSQL 17 started via Docker Compose, API Docker image built/non-root configured, `/health/live` and `/health/ready` returned HTTP 200; disposable `phase2_test` created; `pytest -q -m postgres`: `2 passed, 17 deselected`, including a live ASGI lifespan and rollback probe.
- **Alembic — PASSED smoke execution:** `python -m alembic -c src/infrastructure/alembic/alembic.ini current` and `upgrade head` completed on the disposable database. The revision graph is deliberately **empty**; this proves CLI/config/DB connectivity, **not** approved schema migration, FK constraints, drift freedom or safe production rollback.
- **Warnings:** Starlette `TestClient` emits a third-party AnyIO alias deprecation warning. The workflow also emitted Node.js deprecation warnings from existing action versions. No failed test was reported; lifecycle risk merits future dependency review.
- **Security:** CI password generated dynamically per job (not stored in repository); Compose DB/API bind host loopback; confidential datasets/tokens were not introduced. Source and selected GitHub blobs scanned for high-risk key/token patterns; this does not replace a full supply-chain or penetration audit.
- **Still NOT RUN:** Windows PowerShell local parity, production TLS/Vault integration, real approved migration and rollback drill, dependency vulnerability audit, tenant/RBAC/access checks (no approved protected endpoints), SLO/load.
- **Still BLOCKED:** DEC-01..11 as described above; no model/classifier/evidence provider. Marker remains `PHASE_2_IMPLEMENTED_AWAITING_VERIFICATION` until remaining required verification/authorizations are addressed.

## Latest verification — 2026-10-21 (supersedes earlier test counts)

- **Implementation commit:** [`4541a172cee34801e8e385e4385e1d17c9708651`](https://github.com/Amirmahdimtz/text-classification-service/commit/4541a172cee34801e8e385e4385e1d17c9708651).
- **GitHub Actions run:** [39597986175](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/39597986175) — **completed / success** for both jobs.
- **REMOTE/AVAILABLE independent:** dependency installation, compile and Phase 1 documentation regression **PASSED**; `pytest -q -m "not postgres"`: **20 passed, 3 deselected**. Host startup pass/fail unit tests use a test-scoped engine double and are not live DB evidence.
- **REMOTE/AVAILABLE real integration:** Docker Compose created PostgreSQL 17 and built/ran the backend image; live health/readiness checks succeeded; `pytest -q -m postgres`: **3 passed, 20 deselected**. Verified bounded transaction/rollback, real FastAPI lifespan with DB and `BaseRepository` create/read/update/delete using a PostgreSQL TEMPORARY table; no employer data involved.
- **REMOTE/AVAILABLE migration smoke:** Alembic `current` and `upgrade head` executed successfully on disposable PostgreSQL. Still **no approved migrations or business tables**: no claim of schema correctness, FK tests, revision rollback or drift verification.
- **Security hardening:** production DSN now requires `ssl=verify-full` and malformed DSNs trigger sanitized configuration errors; regression tests added. Production IdP/RBAC, Vault/TLS topology, secrets governance, audit, risk acceptance and third-party vulnerability auditing remain **BLOCKED/NOT RUN**, with no sensitive API exposed.
- **Warnings:** Starlette/AnyIO `TestClient` deprecation and GitHub Actions Node 20 deprecations are recorded as future dependency-maintenance risks; no test failure.
- **LOCAL_USER:** Windows PowerShell installation, Docker/DB/health/Alembic parity and sanitized logs must still be executed or provided by owner (runbook). **SERVER_MODEL:** deferred to Phase 3+ under approved data/model/server; none run in Phase 2.
- **Gate:** `PHASE_2_IMPLEMENTED_AWAITING_VERIFICATION` remains in force. No claim of Production Readiness or entry into Phase 3.

## Phase 2 port regression correction and technical gate — 2026-10-21

- **Root cause:** owner changed `compose.yaml` host PostgreSQL bind from `5432` to `55487` on commit `174237e9c974e60263a6c7d48a8fede18b5283d9`. GitHub Actions still used host `5432` for `DATABASE_URL`/`TEST_DATABASE_URL`; [run 39603066787](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/39603066787) FAILED its three DB tests (`ConnectionRefusedError`). The API container itself reached readiness: the failure was in the CI runner's host-side database DSNs, not an observed PostgreSQL or FastAPI defect.
- **Fix commit:** [`72b26d9a973fe5030c992a6fc64801062b5e8ca3`](https://github.com/Amirmahdimtz/text-classification-service/commit/72b26d9a973fe5030c992a6fc64801062b5e8ca3) changed only Compose and the CI workflow. The `POSTGRES_HOST_PORT` variable has default `55487` (preserving the owner's Windows port), while Docker-internal `db:5432` is unchanged. CI uses the same host port in its two DSNs and asserts that the published Compose port matches, preventing this specific regression.
- **REMOTE/AVAILABLE:** [run 39604867559](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/39604867559) on fix commit **completed/success** for both jobs. Independent: `20 passed, 3 deselected`, plus compile and Phase 1 validator `PASS: 27`. Integration: Docker/API/DB readiness PASSED, real PostgreSQL `3 passed, 20 deselected`, Alembic empty-revision CLI smoke PASSED. Known third-party Starlette/AnyIO deprecation warning remains non-blocking.
- **LOCAL_USER evidence (2026-10-21; owner-provided Windows PowerShell):** Python 3.12 venv/dependencies PASSED; compile PASSED; documentation validator `PASS: 27`; independent `20 passed, 3 deselected`; PostgreSQL 17 container `healthy` on host `127.0.0.1:55487`, API `alive`/`ready`; `3 passed, 20 deselected` against isolated `phase2_test`; Alembic `current` and `upgrade head` returned without CLI errors. Local output was for the previous host-port-only commit; the new Compose default preserves its published port. The revised configuration's CI verification is a separate recorded result; repeat owner-side checks after pull for final local parity.
- **Acceptance limits / deferred scope:** P2-04 (actual commercial schema), P2-05 idempotency, P2-06 taxonomy API, P2-07 IdP/RBAC/business audit, P2-09 schema migrations and rollback tests remain explicitly **BLOCKED** by DEC-01/02/06/07/08/11. Dependency vulnerability audit, authorized identity negative tests, actual migrations, and production recovery/backup remain NOT RUN; no released classifier or sensitive report ingestion. These are not silently accepted as complete. Security baseline is limited to the configured fail-closed/no-business-ingress scaffold and tested safe logging/DB-TLS policy.
- **Internal technical gate decision (ADR-008):** `PHASE_2_COMPLETE_READY_FOR_PHASE_3` applies **only to the dependency-independent Phase 2 foundation** verified above. It is not full functional/security acceptance, customer approval, or `PROJECT_PRODUCTION_READY_ACCEPTED`. Actual Phase 3 supervised training/evaluation is still BLOCKED until approved taxonomy, authorized data and evaluation inputs arrive. Phase 3 requires a new explicit user command and cannot begin automatically.
