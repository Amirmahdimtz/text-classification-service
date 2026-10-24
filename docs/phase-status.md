# Phase status
**Project:** text-classification-service
**Current phase:** PHASE 4 — Grounded Explanation, Decision Policy & Human Review
**Marker:** PHASE_4_IMPLEMENTED_AWAITING_VERIFICATION
**Previous Phase 3 marker (unchanged):** PHASE_3_IMPLEMENTED_AWAITING_VERIFICATION
**Previous verified marker:** PHASE_2_COMPLETE_READY_FOR_PHASE_3
**Status as of:** 2026-10-24
**Progression Authorization:** `CONDITIONAL_PROGRESSION_APPROVED` for the independent Phase 4 entry only (ADR-010); explicit owner Phase 4 start received on 2026-10-24; **NOT** authorization for Phase 5.
**Next phase:** Phase 5 NOT STARTED; requires a separate owner command and independently justified, recorded progression gate. Real model verification remains deferred to Phase 6.
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

## Phase 3 temporal correction and local-first decision — 2026-10-24

- **Formal marker (unchanged):** `PHASE_3_IMPLEMENTED_AWAITING_VERIFICATION`. **Separate progression authorization:** `CONDITIONAL_PROGRESSION_APPROVED` for independent Phase 4 only. Phase 4 NOT STARTED; requires explicit owner command. See [ADR-010](decisions/ADR-010-local-first-and-conditional-phase-progression.md).
- **Correction:** [7fcbfa7](https://github.com/Amirmahdimtz/text-classification-service/commit/7fcbfa711c32b8170be7a4b243306e0d30f40fdc) makes temporal split boundaries strictly chronological over full incident/duplicate components; impossible partitions fail closed.
- **REMOTE/AVAILABLE:** [GitHub Actions 40077902341](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40077902341) SUCCESS on correction SHA: independent 46 PASSED, 1 SKIPPED, 3 DESELECTED; real isolated PostgreSQL 3 PASSED, 1 SKIPPED, 46 DESELECTED; offline ML 27 PASSED. Jobs share tests; these counts must not be added together.
- **LOCAL_USER:** Owner-provided Windows Python 3.12 logs on earlier SHA: compile and docs validation PASSED, 45 independent tests PASSED, 3 PostgreSQL integration tests PASSED. New temporal regression was REMOTE PASSED, Windows re-run NOT RUN.
- **Phase 4 allowed scope:** original-text Evidence offsets, mechanical span/quote fidelity, fail-closed failure semantics and isolated non-sensitive tests. **Blocked pending business decisions:** category relevance, thresholds/calibration, AuthN/AuthZ, review permissions, physical DB schema, confidential data or public classifier route.

### Mandatory deferred verification ledger (latest Phase 6)

| Tasks | Status / reason | Risk owner | Required evidence / latest deadline |
|---|---|---|---|
| P3-01/03 real data, class supports, semantic and temporal leakage | BLOCKED: no approved corpus | ML lead and data owner | Authorized labeled corpus/annotation and expert case audit by Phase 6 |
| P3-04/05 baseline, encoder, Macro-F1 and per-class | DEFERRED / NOT RUN: dataset, label mode, licenses and compute absent | ML lead and product owner | Approved train/validation/Gold, fair comparison by Phase 6 |
| P3-06/07 long documents, rare/ambiguous, OOD and temporal Gold | DEFERRED / NOT RUN: no adjudicated representative cases | ML lead and data owner | Curated authorized Gold/OOD cohorts by Phase 6 |
| P3-08 and P4-05 calibration/coverage/risk | DEFERRED / NOT RUN: no real scores or approved policy | ML lead and product owner | Validation-only calibration and independent Gold verification by Phase 6 |
| P3-09..12 real artifact and inference/load/rollback | DEFERRED / NOT RUN: no approved model/runtime | ML lead, operations and security | Secure server, approved artifact/SLO, real performance and rollback by Phase 6 |
| P4-02/04/10 real explanation relevance and fidelity | BLOCKED: no signed taxonomy or adjudicated examples | Taxonomy owner, reviewers and ML | Groundedness/unsupported-evidence evaluation by Phase 6 |
| P5-08/09/10 real integrated E2E, Gold regression and stress | DEFERRED / NOT RUN: real model/server prerequisites missing | Engineering, ML and operations | Integrated server checks, fixes and regression by Phase 6 |

This progression is NOT a Phase 3 completion gate, does NOT approve sensitive-data processing, and does NOT imply Production Readiness.

## Phase 4 independent implementation — 2026-10-24

- **Entry:** owner explicitly requested Phase 4 while the Phase 3 marker remained `PHASE_3_IMPLEMENTED_AWAITING_VERIFICATION`; `CONDITIONAL_PROGRESSION_APPROVED` is valid only for Phase 4's independent scope under ADR-010. Initial actual main HEAD `64588fda0cc88194d888cc2ee32a67e7c444fe23`; source CI run 40078427070 SUCCESS.
- **Phase 4 implementation marker:** `PHASE_4_IMPLEMENTED_AWAITING_VERIFICATION`, not `PHASE_4_COMPLETE_READY_FOR_PHASE_5`. This marker describes independent Core work; actual employer-governed task scope is still partial/blocked. Phase 5 is NOT STARTED and NOT AUTHORIZED by Phase 4 changes.
- **Implementation:** original-offset EvidenceService, controlled evidence-only literal transcript and mechanical verification, versioned decision-policy **draft** structural validator and review-only proposal semantics. `AUTO_CLASSIFIED`/`OUT_OF_SCOPE`, confidence, final category and semantic category justification remain gated. No Controller, DB schema, Alembic migration, reviewer entity, production model, unapproved AuthZ or confidential dataset.
- **Detailed Phase 4 task ledger and acceptance:** [Phase 4 execution](phase-4-execution.md), [ADR-011](decisions/ADR-011-phase4-evidence-only-and-decision-gate.md), [Windows/DB instructions](runbooks/phase4-local.md).
- **Verification:** Python 3.13.5 isolated builder: 30 Phase 4 synthetic tests PASSED; this is *not* entire-repository evidence. GitHub run 40080190182 SUCCESS on 390220a93325f115d6e6193c792f9de83905c35e: independent 76 PASSED/1 SKIPPED/3 DESELECTED; offline ML 27 PASSED (overlap); isolated live PostgreSQL 3 PASSED/1 SKIPPED/76 DESELECTED, Docker and Alembic smoke succeeded. Windows Python 3.12 owner-run independent, Phase 4 and PostgreSQL tests PASSED (owner PowerShell logs at source SHA `326fe1bc`); real Gold/model evaluation NOT RUN.

### Phase 4 deferred verification register (must close by Phase 6 acceptance)

| Task/Test | State / risk | Risk owner | Unblock evidence / checkpoint |
|---|---|---|---|
| P4-02, P4-03 semantic reasons, P4-04 and P4-10 Gold hallucination/groundedness | BLOCKED / DEFERRED: no criteria, signed taxonomy or Gold | Employer/taxonomy, ML, expert reviewers, data owner | Published inclusion/exclusion criteria, lawful Gold review spans and independent adjudication; Phase 6 |
| P4-05 and P4-06 real threshold, OOD and calibrated auto decision | BLOCKED / DEFERRED: no approved label mode/model/validation/policy | Employer/product + ML | Calibrated validation probabilities, per-category risk/coverage gates, OOD criteria, versioned approved policy; Phase 6 |
| P4-07 Reviewer workflow AuthN/AuthZ, claim/correct/approve/concurrency | BLOCKED: no identity, tenant, reviewer permission policy | Security and employer/review owner | AuthN/AuthZ + record-scoped permissions, state machine/review requirements, real concurrency test; Phase 6 |
| P4-08 review result, immutable audit and PostgreSQL atomic transaction | BLOCKED: no physical schema, record retention or transaction idempotency contract | Employer/product, data/security, engineering | Signed ERD, lifecycle and retention; migration with real isolated PostgreSQL tests and audit; Phase 6 |
| P4-09 reviewer feedback downstream training rights | BLOCKED: no feedback governance or permitted reuse | Data governance, review owner, ML | Provenance, adjudication, consent/legal rights and approved split promotion; Phase 6 |
| Carried Phase 3 model/data/Gold/OOD and future Phase 5 server E2E/load | DEFERRED/NOT RUN | ML, data, security, operations | Real approved model, dataset, taxonomy and controlled server; Phase 6 |

The prior Phase 3 verification debt remains open as documented above; local synthetics never establish real model performance. Neither ADR-010 nor ADR-011 authorizes use of sensitive reports.

### Phase 4 final hardening evidence — 2026-10-24

- [Code hardening 390220a](https://github.com/Amirmahdimtz/text-classification-service/commit/390220a93325f115d6e6193c792f9de83905c35e) prevents oversized non-float score input from triggering unhandled numerical overflow. [Actions 40080190182](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40080190182) **SUCCESS**: independent 76 PASSED/1 SKIPPED, offline ML 27 PASSED (overlaps), real isolated PostgreSQL 3 PASSED/1 SKIPPED, Docker/Alembic startup healthy.
- No Phase 4 real reviewer schema/permission transaction has been tested; P4-07..09 remain BLOCKED, model-dependent P4-02/04/05/10 remain DEFERRED until Phase 6. Phase 3 marker and Phase 4 partial marker remain unchanged, and there is **no Phase 5 progression approval**.

## Phase 4 local verification and dependency-security correction — 2026-10-24

- **Source verification (owner LOCAL_USER on original SHA `326fe1bc`):** clean `main`; Phase 4 30 PASSED; full independent 77 PASSED / 3 DESELECTED; real isolated PostgreSQL 3 PASSED / 77 DESELECTED; compile and Phase 1 documentation validator PASSED. Previous `Windows NOT RUN` entries for Phase 4 software verification are superseded by this evidence. The baseline has no approved review-schema DB tests.
- **Dependency vulnerability discovery:** `pip-audit` reported 5 distinct Starlette `0.50.0`, 1 pytest `9.0.2` and 6 pip `25.0.1` OSV/PyPI advisory IDs; initial scanner findings FAILED the baseline supply-chain review. Earlier failed development scans were network errors, not evidence of security.
- **Isolated patched Windows candidate:** FastAPI `0.134.0`, Starlette `1.3.1`, pytest `9.0.3`, pip `26.2.2`; `pip check` PASSED; Phase 4 30 PASSED; independent 76 PASSED / 1 SKIPPED / 3 DESELECTED; PostgreSQL 3 PASSED / 1 SKIPPED / 76 DESELECTED; OSV local scan returned `No known vulnerabilities found`, exit 0. The optional baseline `sklearn` test was SKIPPED locally but the separate CI offline ML job previously ran it. Windows checks do not prove semantic quality or reviewer permissions.
- **Repository remediation:** Pinned patch versions in requirements and Docker; added a GitHub Actions OSV dependency audit covering production/development/offline ML dependency closure. The security/CI gate **PASSED** in [GitHub Actions run 40093998343](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40093998343) on patched documentation SHA `dbbef9dfd11d4cea61ce50eff58abbc95ba34448`: independent 76 PASSED / 1 SKIPPED / 3 DESELECTED, offline ML 27 PASSED, real isolated PostgreSQL 3 PASSED / 1 SKIPPED / 76 DESELECTED, container build/API health/Alembic smoke PASSED, and `dependency-security` `pip check` + OSV **No known vulnerabilities found**. R-17 is **MITIGATED** at the scan time; future scans remain mandatory. This CI verifies engineering security hygiene only, not real explanation/review/model acceptance. [ADR-012](decisions/ADR-012-phase4-dependency-security-remediation.md).
- **Phase governance (unchanged):** `PHASE_4_IMPLEMENTED_AWAITING_VERIFICATION`; predecessor Phase 3 marker remains unchanged. No `CONDITIONAL_PROGRESSION_APPROVED` for Phase 5 exists. P4-02/04/05/07/08/09 and actual model/Gold/reviewer concurrency gates remain BLOCKED/DEFERRED with their prior risk owners and checkpoint **no later than Phase 6**.

## Conditional Phase 5 entry authorization — 2026-10-24

**Technical decision:** `CONDITIONAL_PROGRESSION_APPROVED` **only for the contract-independent, non-sensitive Phase 5 scope** defined in [ADR-013](decisions/ADR-013-phase5-conditional-entry-authorization.md). This decision followed the project owner's explicit request for a go/no-go judgment; it is **not** the separately required command `فاز ۵ را شروع کن`. **Phase 5 remains NOT STARTED.**

- **Previous marker remains:** `PHASE_4_IMPLEMENTED_AWAITING_VERIFICATION`. Previous Phase 3 marker also remains `PHASE_3_IMPLEMENTED_AWAITING_VERIFICATION`; neither is a full-completion claim. **No** `PHASE_4_COMPLETE_READY_FOR_PHASE_5`.
- **Verified GitHub source / evidence:** `main` at `3425d3826bddbfcc43afa11f5fd423dc40e03551`; [CI run 40094157624](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40094157624) completed **SUCCESS** in all four jobs: independent 76 PASSED / 1 optional ML SKIPPED / 3 DESELECTED; offline ML 27 PASSED; isolated live PostgreSQL 3 PASSED / 1 optional ML SKIPPED / 76 DESELECTED, rebuilt Docker/API health and Alembic smoke PASSED; dependency-security `pip check` PASSED and OSV `No known vulnerabilities found` at scan time. Test sets overlap. Owner Windows 3.12 local evidence on pre-security SHA and isolated patched dependency candidate: Phase 4 30 PASSED, independent 76 PASSED / 1 SKIPPED, PostgreSQL 3 PASSED, patched OSV exit 0. This is independent software integrity, **not** model quality, reviewer authorization or sensitive-data permission.
- **Permitted after a fresh explicit owner Phase 5 start command:** P5-01 limited existing Host/Application/Core/Infrastructure DI and composition/negative-path tests (no unapproved classifier/reviewer endpoint); P5-06 only bounded, fail-closed failure semantics and non-sensitive runtime security checks for approved existing entrypoints, no invented numerical rate limits or policy; P5-07 contract and backward-compatibility tests of **existing** health/readiness/request-ID/error behavior only; P5-11 infrastructure-down/model-unavailable/secret-missing failure regression using non-sensitive fixtures and isolated PostgreSQL, with Test Doubles **only in tests**; P5-12 scoped documentation and verification/runbooks. Other independent hardening requires a fresh dependency/security review before inclusion.
- **Blocked production-facing Phase 5 work:** P5-02 final classification DTO/schema and public inference routes; P5-03/04 atomic business persistence and idempotency; P5-05 record-scoped AuthN/AuthZ; P5-06 business/tenant rate-limit thresholds; P5-07 new external OpenAPI v1 classification contract; P5-08 real API+model+review E2E, pending signed taxonomy/cardinality/API/schema/identity/privacy/reviewer rules and lawful release inputs. No fake production provider, labels, thresholds, reviewer or storage contracts.
- **Deferred model/server verification, deadline Phase 6:** P5-08 real integrated inference/review E2E, P5-09 Gold/Explanation/Decision/version regression, model-dependent P5-10 latency/load; carried P3/P4 real data/leakage/Gold/OOD/calibration, groundedness and reviewer concurrence/audit. Owners: Employer/Product/Taxonomy (label, API, threshold); Security/Review Owner/Data Governance (AuthN/AuthZ, retention, approval and access); ML/Data Owner (authorized train/Gold/OOD, model release/calibration); Engineering/Ops (DB transaction, concurrency, runtime, load, rollback). Genuine evidence, tests and employer Phase 6 acceptance required. See [risk register](risk-register.md) and [Phase 4 ledger](phase-4-execution.md).
- **Safety:** no approval for data processing, business-model schema, public classifier API, category decisions, publication or production readiness. A separate, explicit `فاز ۵ را شروع کن` command is mandatory before any Phase 5 implementation.
