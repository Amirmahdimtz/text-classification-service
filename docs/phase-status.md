# Phase status
**Project:** text-classification-service
**Current phase:** PHASE 3 — Persian NLP, Dataset & Classification Engine
**Marker:** PHASE_3_IMPLEMENTED_AWAITING_VERIFICATION
**Previous verified marker:** PHASE_2_COMPLETE_READY_FOR_PHASE_3
**Status as of:** 2026-10-21
**Next phase:** NOT STARTED — Phase 4 needs a separate explicit user command and Phase 3 real model/data gate verification
**Documentation snapshot verified:** 0834bfe31be38a618981d1b814254b7282bb51d6 (GitHub main; 26 Phase 1 documents/tool files added after README initialization).

## Revised phase-gate decision (ADR-008)
The project owner has specified that **employer/customer formal acceptance occurs once, at the end of Phase 6**, not at every intermediate phase. The Phase 1 technical gate is accepted based on verifiable documentation and recorded LOCAL_USER checks. This marker authorizes **readiness for permitted Phase 2 foundational work only**; it is not approval of unresolved business requirements, taxonomy, privacy, APIs, schema choices or release. See [ADR-008](decisions/ADR-008-phase-acceptance-governance.md). Phase 2 began by explicit user instruction on 2026-10-21; independent foundation code is implemented. Technical integration verification remains open.

## Scope actually delivered
Phase 1 originally initialized the repository for documents only; Phase 2 now adds executable foundation and tests. Technical contracts and proposed policies for requirements/RBAC, taxonomy structure, classification cardinality, input/annotation/gold split, API v1, conceptual ERD/persistence, ML benchmark/calibration, SLO, security/data governance, architecture, ADRs and risk/backlog are present. They are NOT approved runtime specifications or evidence of a working classifier.

## Acceptance and blocker pointers
- [Phase 1 acceptance packet](phase-1-acceptance.md): P1-01..P1-13, exact owner decisions DEC-01..12, DoD checklist.
- [Risk register](risk-register.md): critical/high blockers and owners.
- [Repository assessment](repository-assessment.md): initial empty-repo evidence.
- [Phase 2 backlog](phase-2-backlog.md): planning only, no executable Phase 2 implementation.
- ADRs 001–007 are **PROPOSED or DEFERRED**, not employer-approved; **ADR-008 is accepted only for the phase-approval workflow**.

## Verification ledger
| Environment | Check | Result / current limitation |
|---|---|---|
| REMOTE/AVAILABLE | GitHub initial repository/permissions/branch state | PASSED assessment (empty repository confirmed before initialization) |
| REMOTE/AVAILABLE | 27 committed-file paths, Markdown links, fenced blocks, ADR statuses, phase marker and limited credential patterns | PASSED via GitHub blob/tree inspection in five batches; not a comprehensive secret/security scan |
| LOCAL_USER | Clean git status, HEAD matching main at 841256f480fda68c84c737dd291481ec88cb1a4a, Python stdlib docs validator | PASSED (owner-supplied Windows PowerShell logs, 2026-10-21); result is documentary verification, not an application test |
| LOCAL_USER | FastAPI/DI/PostgreSQL integration | NOT RUN: no runtime in Phase 1 |
| SERVER_MODEL | Training/Gold inference/calibration/explanation/load | BLOCKED/NOT RUN: actual approved taxonomy, dataset, model and server absent |

## Technical readiness and open dependencies
Phase 1 internal technical documentation gate is **PASSED**, with external/business input gaps explicitly deferred and owned by DEC-01..DEC-12. No real taxonomy catalog, annotated dataset, signed security policy, numerical product SLO, employer sign-off, or ML/runtime evidence has been provided; those are not represented as completed or approved. These gaps BLOCK only work items that require them (in particular taxonomy-specific DB/API decisions, sensitive data usage and Phase 3 model work), not independent Phase 2 engineering. Formal employer acceptance remains required in Phase 6. Next phase starts only upon a separate explicit user command.

## Phase 2 update — 2026-10-21

- **Marker:** PHASE_2_IMPLEMENTED_AWAITING_VERIFICATION; the independent foundation is implemented, not verified for live PostgreSQL/Docker/Alembic.
- **Evidence:** Python 3.13.5 local builder compile passed; 17 independent tests PASSED. GitHub Actions run 39597343384 PASSED: independent 17 tests, live PostgreSQL 2 tests, Docker build/start/health and Alembic empty-revision smoke. No approved business schema migration, security identity integration or Windows-local verification is claimed.
- **Deliverables:** FastAPI Host/lifecycle, strict configuration, @inject auto-discovery, SQLAlchemy async infrastructure and bounded sessions, BaseRepository, transaction context, Alembic empty metadata environment, sanitized logs/correlation, health/readiness, CI, Docker, tests and PowerShell runbook.
- **Blocked items:** physical taxonomy/report/results schema and revisions, business APIs, customer-specific auth/RBAC, scoped idempotency, data/retention/network approval (DEC-01..11). No fake model/provider/classification implemented.
- **Detailed task matrix:** [Phase 2 execution ledger](phase-2-execution.md); [Windows verification commands](runbooks/phase2-local.md).
- **Next:** Obtain LOCAL_USER Windows parity evidence; external owner approvals are still required for schemas/AuthN/RBAC and production-sensitive functionality. No Phase 3 start implied.

**Remote CI evidence (Phase 2):** [successful run 39597343384](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/39597343384) on commit `2b4c258819182819777120ae530f5c398d3fc9f7`: 17 independent tests + 2 real PostgreSQL tests passed, Docker/API health and Alembic empty-graph checks succeeded. Status remains awaiting verification for unresolved customer-governed functionality and required environment-specific checks.

**Latest Phase 2 verified CI:** [successful run 39597986175](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/39597986175) on `4541a172cee34801e8e385e4385e1d17c9708651`: independent 20 passed; actual PostgreSQL 3 passed (including BaseRepository CRUD); Docker and Alembic empty-revision smoke succeeded. Production config now enforces verified TLS mode. Outstanding decisions and LOCAL_USER Windows parity mean final marker stays `PHASE_2_IMPLEMENTED_AWAITING_VERIFICATION`.

## Phase 2 internal technical acceptance — 2026-10-21 (supersedes earlier open verification notes)

- **Technical gate:** `PHASE_2_COMPLETE_READY_FOR_PHASE_3` under [ADR-008](decisions/ADR-008-phase-acceptance-governance.md), solely for the independent, non-sensitive production foundation. Phase 1 prior marker remains `PHASE_1_COMPLETE_READY_FOR_PHASE_2`.
- **GitHub CI:** Port mismatch in owner's `174237e9` commit made [run 39603066787](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/39603066787) fail integration. Corrected in [`72b26d9`](https://github.com/Amirmahdimtz/text-classification-service/commit/72b26d9a973fe5030c992a6fc64801062b5e8ca3). [Run 39604867559](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/39604867559) succeeded in both CI jobs: 20 independent, 3 live-PostgreSQL tests, Docker health and Alembic empty-graph smoke.
- **Windows verification:** Owner-provided Python 3.12 evidence: independent 20/20 and live PostgreSQL 3/3, compile and Phase 1 docs validator passed; PostgreSQL 17 healthy on host port 55487, API alive/ready; Alembic CLI commands exited without error. The new configurable-port commit was verified in CI; a Windows pull/retest of that exact commit remains recommended.
- **Hard limits:** Schema/physical migrations, customer AuthN/AuthZ, taxonomy endpoints, idempotency, retention, audit policy, vulnerability review, RBAC and production rollback are **NOT accepted**; see [the Phase 2 execution ledger](phase-2-execution.md) and DEC-01..11. Those changes require approved external inputs; no sensitive reports may be ingested. No server/model/Gold evaluation ran in Phase 2.
- **Phase 3 dependency gate:** Actual training/benchmark requires approved taxonomy, legitimate representative annotated dataset and evaluation thresholds. This technical marker is **not** permission to fabricate inputs or begin Phase 3 without a fresh owner command. The employer's final acceptance remains Phase 6.


## Phase 3 independent implementation — 2026-10-21

- **Owner start command:** Explicitly authorized Phase 3 on 2026-10-21. Entry technical marker PHASE_2_COMPLETE_READY_FOR_PHASE_3 validated against main and successful phase2 CI run 39604867559.
- **Marker:** PHASE_3_IMPLEMENTED_AWAITING_VERIFICATION. This is an implementation/partial-gate marker, not a completion or production claim.
- **Independent code:** offset-preserving Persian text normalization, original segments, dataset group/time/exact/near-duplicate split auditing with private HMAC fingerprints, local authorized-only audit CLI, optional statistical TF-IDF + LinearSVC baseline training on TRAIN with VALIDATION reporting, portable JSON artifact/model loader with SHA-256 integrity and no pickle, explicit @inject Infrastructure inference provider with warmup, batch, timeout, readiness and graceful close. No public classifier HTTP route, unapproved DB model or migration was introduced.
- **QA:** Python 3.13.5 development workspace 25 Phase 3 tests PASSED with optional scikit-learn 1.8.0; isolated fixture metrics are not model quality evidence. Existing GitHub CI includes Phase 1/2 regression and now a third offline ML job. Exact live run URL/outcome must be checked before claiming last commit green; see GitHub Actions.
- **External gates:** DEC-01, DEC-02/03, DEC-04, DEC-05/09, DEC-08, DEC-10 remain BLOCKED. No employer-signed taxonomy/cardinality, authorized training/Gold/OOD data, calibrated probabilities, numerical targets, permitted model environment or real release. **Real baseline/encoder benchmark, Gold macro-F1, OOD, calibration, real inference/load and production rollback are NOT RUN.**
- **Records:** [Phase 3 execution](phase-3-execution.md), [Private Windows audit](runbooks/phase3-local.md), [Server ML runbook](runbooks/phase3-server.md), [Artifact specification](model-artifact-manifest.md), [Benchmark status](phase-3-benchmark-report.md), [ADR-009](decisions/ADR-009-phase3-offline-artifacts-and-offsets.md).
- **Gate:** Remain PHASE_3_IMPLEMENTED_AWAITING_VERIFICATION until all technical and model requirements receive genuine evidence. No permission to start Phase 4 without a separate explicit owner command. Employer's formal final acceptance remains Phase 6 per ADR-008.
