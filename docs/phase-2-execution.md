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
| P2-03 | SQLAlchemy Async engine/sessionmaker, PsqlDbContext, shared engine, BaseRepository and atomic transaction context | Real PostgreSQL LOCAL_USER required; no Postgres available on current runner |
| P2-04 | No unapproved physical business tables created | BLOCKED DEC-01, DEC-02, DEC-08, DEC-11 |
| P2-05 | Transaction context available in Infrastructure; no fabricated idempotency table/API | PostgreSQL rollback test LOCAL_USER; idempotency policy BLOCKED DEC-07/11 |
| P2-06 | Runtime controller discovery only; no invented taxonomy CRUD/API | BLOCKED DEC-01, DEC-06, DEC-07 |
| P2-07 | Fail-closed config; no exposed sensitive routes; env-only DB credentials; redacted log allowlist; safe headers; no permissive CORS | Identity/RBAC/TLS topology, audit and rate-limit policy BLOCKED DEC-06/08 |
| P2-08 | Structured allowlisted logs, server-generated request ID, distinct liveness/readiness, DB-dependent startup and shutdown | Unit HTTP checks; real startup/DB LOCAL_USER |
| P2-09 | Alembic async metadata environment with no business revisions | Real clean DB/check/drift BLOCKED pending approved schema and local DB |
| P2-10 | CI for Python compile, docs regression and independent tests; opt-in DB marker | GitHub Actions outcome must be checked after commit; local CI dependency installs unverified |
| P2-11 | Non-root Dockerfile; local-only development Compose DB and API health dependency | Docker build/run LOCAL_USER; not executed in current runner |
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
