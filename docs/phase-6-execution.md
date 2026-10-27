# Phase 6 — restricted technical execution and final acceptance ledger

**Entry audit (2026-10-27):** Owner's explicit `فاز ۶ را شروع کن` command. Connected GitHub `main` entry SHA `c33914beeaa443f9f69ce4e2ef95eddd7d652a01`; [pre-change CI #52](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40464565247) SUCCESS. Authenticated read/write permissions confirmed. Normative: Architecture Guide, owner Plan v1.2.0, ADR-008/010/014/015/016, [Phase 5 alignment](phase-5-v1.2-alignment.md), [closure audit](phase-5-closure-audit.md), [phase status](phase-status.md) and [risk register](risk-register.md).

**Scope:** `CONDITIONAL_PROGRESSION_APPROVED` under ADR-014 applies **only** to contract-independent P6-02, P6-04, P6-06, P6-12 subsets. This start command does NOT approve a real deployment, extend Phase 6 scope, close P3–P5, or provide employer production acceptance.

## P6-01..13 mandatory task and gate matrix

| Task | Current independent work / remaining status | Owner / prerequisite to close at final Phase 6 Gate |
| --- | --- | --- |
| P6-01 | Full release+image/model/taxonomy/policy+SBOM manifest BLOCKED / NOT RUN | ML + Engineering/Ops; approved complete release artifacts, provenance and signed versions |
| P6-02 | Independent config: reject malformed/ambiguous DSN, preserve env separation and production verified-TLS rule; full Vault/secrets/network policy BLOCKED | Engineering; Security/Ops approve actual TLS credentials, topology, secret storage and deployment |
| P6-03 | Full CI/CD approval, promotion and rollback BLOCKED / NOT RUN | Ops/Security; approved environment, release and migration/rollback procedure |
| P6-04 | Independent DB-only health-scope header and existing DI/disposal/shutdown checks; real model-ready/in-flight server recovery BLOCKED | Engineering; ML/Ops provide approved released model, model E2E, approved environment |
| P6-05 | Real load, stress, soak, p50/p95/p99 DEFERRED / NOT RUN | ML/Ops; permitted representative workload, hardware and approved SLO |
| P6-06 | Independent known-signature source scanning, CI dependency OSV and redaction regression; actual AuthN/AuthZ, IDOR, privacy penetration/security sign-off BLOCKED | Engineering; Security/Data Governance authorize IdP, tenant/record scope, data rights, tests |
| P6-07 | Backup/restore drill and RPO/RTO BLOCKED / NOT RUN | Ops/Data Owner; approved backup policy, disposable restore environment, signed targets |
| P6-08 | Model observability, real dashboard/on-call/alerts BLOCKED / NOT RUN | Ops; permitted telemetry, approved SLO and ownership |
| P6-09 | Quality drift and auditable retrain governance BLOCKED / NOT RUN | ML/Data Governance; authorized reference data, trigger policy and review approval |
| P6-10 | Independent real Gold/OOD, calibrated decision, groundedness BLOCKED / NOT RUN | Product/ML/Data Owner; lawful Gold, signed taxonomy/model/quality targets |
| P6-11 | Customer UAT BLOCKED / NOT RUN | Employer/Product/Review; authorized UAT and integrated working release |
| P6-12 | Independent documentation, exact local commands and debt ledger; final API/schema/model card/deployment/recovery handover BLOCKED | Engineering/Ops; actual model, secure API, release and operational evidence |
| P6-13 | Formal acceptance and authorized handover BLOCKED / NOT RUN | Employer/Security/ML/Ops; all mandatory P3–P6 evidence and written approval |

## Carried verification ledger — exact obligations, owners and Phase 6 deadline

| Task IDs | Status and cause | Risk Owner | Required verification before final Phase 6 acceptance |
| --- | --- | --- | --- |
| P3-01/03/04 | BLOCKED: no lawful real corpus, case adjudication and frozen test | ML/Data Owner | Authorized corpus, label/group/time leakage audit, reproducible train/validation/test and baseline |
| P3-05/06/07/08 | DEFERRED / NOT RUN: encoder, document-length profile, Gold/OOD, calibrated thresholds unavailable | ML/Product/Data Owner | Fair encoder comparison, Macro-F1/per-class, long/rare/OOD cases, validation-only calibration, coverage/risk |
| P3-09..12 | DEFERRED / NOT RUN: actual approved release/server unavailable | ML/Ops/Security | Hash+compatibility, real warm inference, timeout/load/rollback, CPU/GPU latency |
| P4-02/04/05/10 | BLOCKED/DEFERRED: category criteria/Gold review/approved decision policy absent | Product/Review/ML | Actual evidence relevance and groundedness, unsupported explanation rejection, calibrated risk/threshold tests |
| P4-07/08/09 | BLOCKED: no reviewer AuthN/AuthZ, record schema, retention or feedback rights | Security/Review/Product/Data Owner | Authorized review and immutable audit, concurrency, atomicity, lawful feedback reuse |
| P5-01..07/11/12 dependent | BLOCKED: no signed API DTO/schema/idempotency/privacy/identity | Product/Security/Engineering | Authenticated v1 API and record IDOR, versioned DTO, real PostgreSQL Result+Evidence+Audit transaction, reviewer conflicts |
| P5-08/09/10 | DEFERRED / NOT RUN: actual secure service/model/Gold/workload absent | Engineering/ML/Ops | API→real Model→PostgreSQL→Review→Audit E2E, independent Gold regression, representative load/stress/recovery |

**Deadline:** All mandatory real-model/Gold, review, security, persistence and server evidence must be executed and failures corrected **before P6 final acceptance**; synthetic test outcomes are not substitutes. Actual contracts DYN-01 Product/Taxonomy, DYN-02 Product/Engineering, DYN-03 Security/Data Governance, DYN-04 ML/Data Owner and DYN-05 Ops remain TBD/BLOCKED. Late decisions require impact review, approved migration and regression.

## Independent implementation and evidence discipline

- Config hardening: reject malformed URL ports, fragments and raw control/whitespace before engine construction; errors never echo DSN. Existing production TLS `ssl=verify-full` retained.
- Health/readiness: response body/status unchanged; additional `X-Readiness-Scope: database` header explicitly limits /health/ready to PostgreSQL. It is **not model readiness**.
- Security: bounded static source signature scanner (`tools/verify_phase6_security.py`) in independent CI, existing OSV strict dependency check, redacted logger and tests. Scanner cannot replace full secret history scan/security assessment.
- Files/tests: see source Commit diff after push; no business schema/migration, inference API, model artifact, secret or sensitive dataset introduced.
- **At document writing:** new tests and new CI **NOT RUN** (source SHA not yet published), Windows LOCAL_USER **NOT RUN**, SERVER_MODEL **BLOCKED/DEFERRED**. Entry green CI #52 is historic, not proof of these changes. Add exact new source SHA/run only after CI completes.
- Environment-specific execution: [Phase 6 Windows runbook](runbooks/phase6-local.md); authorized existing offline CLI capabilities and missing real evaluation scripts: [Phase 3 server guide](runbooks/phase3-server.md). Do not invent future server commands.

**Markers:** P3/P4/P5 `IMPLEMENTED_AWAITING_VERIFICATION` unchanged; Phase 6 **IN PROGRESS / RESTRICTED** is a descriptive development state, not final completion. `PROJECT_PRODUCTION_READY_ACCEPTED` **BLOCKED** pending full real evidence and written employer acceptance.

## Verified CI and focused remediation — 2026-10-27

**Source SHA:** [`813a8b08179fbf8c06dce4d09ea8296b7aee014a`](https://github.com/Amirmahdimtz/text-classification-service/commit/813a8b08179fbf8c06dce4d09ea8296b7aee014a). [GitHub Actions run #54](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40467522160) completed SUCCESS **all four jobs on this exact SHA**:

| REMOTE / AVAILABLE job | Actual commands / evidence | Result |
| --- | --- | --- |
| independent | `python -m compileall -q src tests tools`; `python tools/verify_phase1_docs.py`; `python tools/verify_phase6_security.py`; `python -m pytest -q -m 'not postgres'` | Compile PASSED; doc validator 27 required files PASS; bounded source scan 43 files PASS; 123 PASSED / 1 SKIPPED / 5 DESELECTED / 2 WARNINGS |
| integration | `docker compose config --quiet`, Docker build/start and API smoke (`/health/live`, DB-only `/health/ready`); `python -m pytest -q -m postgres`; `python -m alembic -c src/infrastructure/alembic/alembic.ini current` and `upgrade head` against CI-created isolated `phase2_test` | 5 PASSED / 1 SKIPPED / 123 DESELECTED / 2 WARNINGS; Docker/API/Alembic smoke PASSED; no business schema revision |
| ml-independent | `python -m compileall -q src tools tests`; offline synthetic ML test modules in CI workflow | 30 PASSED, overlaps independent test modules; **not real model quality** |
| dependency-security | `python -m pip check`; `python -m pip_audit --local --vulnerability-service osv --strict --timeout 60` | No broken requirements; no known vulnerabilities **at scan time** |

**Root cause and correction:** First [CI #53](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40467358784) on source `52d46ec...` FAILED independent signature-scan step: an *environment-variable reference*, not a hard-coded credential, inside the approved CI-generated PostgreSQL DSN matched the literal-secret rule. Focused follow-up [commit `813a8b0`](https://github.com/Amirmahdimtz/text-classification-service/commit/813a8b08179fbf8c06dce4d09ea8296b7aee014a) excludes shell interpolation for that specific signature and adds explicit negative regression. Other three jobs of #53 PASSED; #54 repeated **all four** and PASSED. The scanner remains intentionally bounded, not a full historical secrets audit.

**Verification debt unchanged:** LOCAL_USER Windows source `813a8b0` **NOT RUN**; authorized SERVER_MODEL dataset/Gold/OOD, model E2E, authentic reviewer AuthN/AuthZ, production recovery/load/backup and UAT **BLOCKED/DEFERRED / NOT RUN**. Two existing Starlette/httpx and AnyIO dependency deprecation warnings remain. No employer Security/Privacy/ML acceptance occurred. `PROJECT_PRODUCTION_READY_ACCEPTED` stays **BLOCKED**.
