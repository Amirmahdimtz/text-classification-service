# Phase 4 — Execution ledger: grounded evidence, gated decisions and human review

**Start:** explicit owner command, 2026-10-24. **Baseline main:** `64588fda0cc88194d888cc2ee32a67e7c444fe23`. **Prior marker:** `PHASE_3_IMPLEMENTED_AWAITING_VERIFICATION`. **Progression:** `CONDITIONAL_PROGRESSION_APPROVED` for independent Phase 4 only (ADR-010). **Phase 4 implementation marker:** `PHASE_4_IMPLEMENTED_AWAITING_VERIFICATION` (technical partial scope; not feature completion).

## Root causes and scope boundary

The approved Phase 3 preprocessor maps normalized spans to original Unicode code points, but no Phase 4 Evidence/Explanation service existed. Model artifacts and raw margins do not constitute calibrated confidence. No employer-approved taxonomy, category criteria, review permissions/identity, physical business schema, retention or real gold data exists. Creating public classification/review endpoints, business models or threshold policies would therefore freeze unapproved contracts and violate fail-closed security. All delivered implementation here is **Core-only**; no API route, SQL/DB migration, test-only model in production or artificial employer categories.

## Task ledger (P4-01..P4-10)

| Task | State | Evidence / remaining scope |
|---|---|---|
| P4-01 | IMPLEMENTED + TESTED (independent) | EvidenceService validates versioned PreprocessedText integrity, normalized candidate boundaries/quote, original [start,end) codepoint spans and quote round-trip; duplicate and malformed intervals rejected. An evidence candidate source still requires an approved ML/annotation pipeline. |
| P4-02 | BLOCKED / DEFERRED real semantics | No category inclusion/exclusion definitions, taxonomy or approved adjudicated examples. Mechanical matching **does not** imply category relevance. Owner: employer/taxonomy and ML. |
| P4-03 | PARTIAL + TESTED | ExplanationService produces deterministic **EVIDENCE_ONLY_UNVERIFIED_RELEVANCE** excerpt with JSON-escaped verbatim quotes and explicit caveat; does **not** provide category-specific explanation. Controlled category/criteria explanation BLOCKED until approval. |
| P4-04 | PARTIAL + TESTED | Evidence-only output is regenerated and equality-verified; quote/offset tampering, unsupported additions and zero-evidence generation rejected. Gold groundedness/semantic hallucination evaluation BLOCKED. |
| P4-05 | PARTIAL + TESTED | Immutable DecisionPolicyDraft validates version strings and finite unique per-category numerical thresholds, requiring a calibration version; validation **never approves** draft, calibrates margins or activates any thresholds. Real calibration, coverage/selective risk and binding to approved release DEFERRED. |
| P4-06 | PARTIAL + TESTED | DecisionStatus types distinct from exceptions; review-only local proposal requires model readiness, a versioned draft and matching taxonomy; any AUTO_CLASSIFIED or OUT_OF_SCOPE, final category, confidence or unauthenticated policy is gated. No production status is emitted. Provider/DB exceptions are not converted into business statuses. |
| P4-07 | BLOCKED | Reviewer claim/approve/correct workflow and AuthN/AuthZ/record permissions not approved. Concurrency/authorization implementation would invent a business contract. Owner: security, review owner, product. |
| P4-08 | BLOCKED | No approved category/review/audit physical schema, actor scope or retention. Atomic reviewer transaction, migration and DB review tests cannot be implemented legitimately. Existing generic PsqlDbContext.transaction is not a review transaction. Owner: product, data/security, engineering. |
| P4-09 | BLOCKED | Feedback provenance/approval and approved training reuse rules absent. No automatic training ingestion. Owner: data owner/ML and review owner. |
| P4-10 | PARTIAL + TESTED (independent) | Synthetic adversarial Unicode, tampered offsets/quotes, unsupported claims, raw score semantics, draft versioning and DI discovery tests. Real reviewer races/AuthZ, PostgreSQL business-schema paths and model/Gold adversarial work BLOCKED. |

All task statuses describe **independent source changes**; passing synthetic tests does not establish semantic grounding or model accuracy.

## Implementation and architecture

- Created `src/core/services/text_classification/__init__.py` specifically because the existing `pkgutil.walk_packages` provider scanner only descends into importable packages. Pure Phase 3 modules remain otherwise unchanged.
- Created `evidence_service.py`, `explanation_service.py`, `decision_policy.py` under the existing Core feature. Services are `@inject` providers; constructor wiring uses the existing project DI. The two dependency-free services have explicit no-argument constructors because the existing injector cannot infer inherited `object.__init__(*args, **kwargs)`.
- Created `tests/test_phase4_evidence.py` and `tests/test_phase4_decision.py`; all values are non-sensitive, test-only synthetic fixtures.
- No HTTP Controller, DTO, SQLAlchemy Model, Repository, Alembic migration, secrets, dataset or active model change. Previous `src/infrastructure/text_classifier_provider.py` still raises typed `InferenceUnavailableError` and `InferenceTimeoutError`; Phase 4 does not intercept or misrepresent them.

## Actual verification

| Environment / check | Result | Limits |
|---|---|---|
| Local builder Python 3.13.5 — new Phase 4 module compilation | PASSED | Isolated local working tree with copies of existing preprocessing/DI source; not a full GitHub checkout |
| Local builder — `python -m pytest -q tests/test_phase4_evidence.py tests/test_phase4_decision.py` | **30 PASSED** | New synthetic tests in isolated reconstructed workspace; GitHub CI remains authoritative for full repository |
| REMOTE independent full regression, DI and offline ML | PASSED — run 40079884573 on c46679be5b0328e747d350e5ef7da4759762c3f5: independent 75 passed/1 skipped/3 deselected; offline ML 27 passed | Suites overlap; synthetic/offline tests do not prove model accuracy |
| REMOTE isolated PostgreSQL integration | PASSED — same run: 3 passed/1 skipped/75 deselected; Docker health + Alembic smoke succeeded | Existing 3 DB tests only; no Phase 4 reviewer schema/transaction exists |
| LOCAL_USER Windows Python 3.12 and isolated PostgreSQL 17 | **PASSED** — owner-provided PowerShell logs: Phase 4 **30 PASSED**, independent regression **77 PASSED/3 DESELECTED**, existing PostgreSQL **3 PASSED/77 DESELECTED**; compile and 27-document validator PASSED | Source SHA `326fe1bc`; application code only; no Phase 4 reviewer schema or business integration was tested |
| SERVER_MODEL Gold, calibration, review/corpus, real E2E/load | BLOCKED / DEFERRED | Approved taxonomy, dataset, security and deployed model required by Phase 6 |

## Security and residual risks

- No raw report is logged, sent externally or persisted by added components; extraction operates only on supplied in-process text.
- Original quote check rejects unsupported literal evidence; no semantic relevance or external provenance is established. Equivalent substrings at the same offset in another document cannot establish report identity: secure report/version binding belongs to approved persistence and AuthZ.
- Evidence-only output is explicitly **not** a category explanation. Client use as automated classification justification is prohibited until future semantic validation.
- Draft policy metadata is not authenticated or approved merely because it passed structural validation; must not be supplied directly from untrusted API input. There is no active production decision policy.
- R-01/02/05/06/07/08/11/12/13/14/16 remain material. No model decision, customer-data processing or reviewer persistence is authorized.

## Phase 6 verification backlog / owner / unblock conditions

| Task IDs | State | Risk owner | Prerequisite and latest checkpoint |
|---|---|---|---|
| P4-01/02/03/04/10 Gold relevance, original offsets, hallucination assessment | BLOCKED/DEFERRED | Taxonomy owner, reviewers, ML, data owner | Signed criteria, lawful Gold excerpts, approved model/report versions, category-specific manual adjudication; Phase 6 |
| P4-05/06 real decisions and OOD policy | BLOCKED/DEFERRED | Employer/product, ML | Approved label mode, calibrated validation scores, threshold and OOD rules, coverage/risk goals; Phase 6 |
| P4-07/08 review/Audit and concurrent revisions | BLOCKED | Security, employer/review owner, engineering | AuthN/AuthZ, tenant/record scope, schema, retention, review policy; approve before real DB/Migration/API work, verify by Phase 6 |
| P4-09 feedback quality and training rights | BLOCKED | Data governance, review owner, ML | Expert agreement, retention/legal processing and dataset promotion authorization; Phase 6 |
| Carried P3-01..12 and future P5-08..10 model evidence | DEFERRED/BLOCKED | ML, data owner, operations, security | Private authorized dataset, taxonomy, serving artifact, server capacity and signed gates; Phase 6 |

## Acceptance checklist

- [x] Independent evidence offsets and quote validation code with adversarial tests (local isolated verification and GitHub CI passed).
- [x] No unsupported category explanation presented as verified.
- [x] Raw margins remain non-probabilistic; auto/OOD status issuance gated.
- [x] No unapproved public endpoint, AuthZ, schema, migration or production fake.
- [x] Full repository CI on baseline implementation (run 40079884573) and score-validation hardening (run 40080190182).
- [x] Owner Windows/Python 3.12 and isolated PostgreSQL parity verified on `326fe1bc` with sanitized logs.
- [ ] Approved taxonomy/criteria, calibrated release, semantic Explanation Gold and real OOD.
- [ ] Approved reviewer AuthN/AuthZ, immutable audit schema, atomic review/concurrency integration.
- [ ] Real server/model E2E/rollback/load and customer acceptance in Phase 6.

**Progression note:** Do not issue `PHASE_4_COMPLETE_READY_FOR_PHASE_5`. Any **future** independent Phase 5 conditional progression requires fresh owner command, adequate CI/local security/DB evidence and separately recorded scope, risk/debt and authorization. This phase does not start Phase 5.

## GitHub Actions verified source revision

- **Implementation commit:** [c46679be5](https://github.com/Amirmahdimtz/text-classification-service/commit/c46679be5b0328e747d350e5ef7da4759762c3f5); from original `64588fda`, fast-forward with 11 scoped changed files and no migration.
- **[GitHub Actions run 40079884573](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40079884573): SUCCESS.** `independent`: 75 PASSED, 1 SKIPPED (optional ML), 3 DESELECTED (PostgreSQL). `ml-independent`: 27 PASSED (overlapping earlier tests). `integration`: 3 real PostgreSQL PASSED, 1 SKIPPED, 75 DESELECTED; API Docker startup/health and empty Alembic upgrade smoke succeeded. These counts **must not be added together**. The 29 original independent Phase 4 cases are included in the 75; the later hardening test brings the count to 30/76.
- **NOT RUN:** Real reviewer PostgreSQL/concurrent AuthZ tests (blocked schema), real model/Gold/threshold/groundedness/latency tests (blocked external inputs), real server rollback. Owner Windows verification completed separately; see security remediation entry below.
- **No false completion:** `PHASE_3_IMPLEMENTED_AWAITING_VERIFICATION` unchanged; Phase 4 remains `PHASE_4_IMPLEMENTED_AWAITING_VERIFICATION`. This Phase 4 scope is not a complete reviewer/explanation feature or authorization to start Phase 5.

## Final Phase 4 hardening regression (supersedes earlier per-commit counts)

- Root cause: an arbitrarily large Python integer passed as an in-process draft model score could raise `OverflowError` at `math.isfinite` rather than a deliberate validation error. Because the actual `RawPrediction.raw_margin` contract is `float`, Phase 4 now rejects every non-`float` score before `isfinite`. A synthetic `10 ** 1000` negative regression test was added. This is strictly within Phase 4 score/failure semantics.
- **Hardening code commit:** [390220a93325f115d6e6193c792f9de83905c35e](https://github.com/Amirmahdimtz/text-classification-service/commit/390220a93325f115d6e6193c792f9de83905c35e) (fast-forward, only decision-policy code and test).
- **[CI run 40080190182](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40080190182): SUCCESS on that exact SHA.** Independent 76 PASSED, 1 SKIPPED, 3 DESELECTED; offline ML 27 PASSED; existing isolated real PostgreSQL 3 PASSED, 1 SKIPPED, 76 DESELECTED. CI also ran compile/docs-validator, Docker health and Alembic empty-schema smoke. **Suites overlap** and are not additive. This is software integrity only, not production model or reviewer approval.
- Local isolated builder with the hardening patch: 30 Phase 4 tests PASSED; owner Windows local verification PASSED (owner-supplied logs on `326fe1bc`); no approved reviewer DB schema exists.

## Phase 4 follow-up: dependency vulnerability remediation (2026-10-24)

- **Root cause:** `main` at `326fe1bc` pinned FastAPI `0.128.2`, indirectly installing Starlette `0.50.0`; pytest was `9.0.2`. The owner's `pip-audit 2.10.1` scans surfaced **five distinct** Starlette advisories, **one distinct** pytest advisory, and **six distinct** pip `25.0.1` advisories (duplicate rows counted once per advisory). The first production requirements scan FAILED; the subsequent OSV local scan of the original virtualenv FAILED; a full requirements-dev PyPI query was INCOMPLETE due network timeouts, not PASSED.
- **Isolated Windows reproduction (LOCAL_USER):** Python `3.12.10`, external `..\\.venv-phase4-security-v2` with FastAPI `0.134.0`, explicitly pinned Starlette `1.3.1`, pytest `9.0.3`, pip `26.2.2`; pip compatibility **PASSED**, 30 Phase 4 tests **PASSED**, independent 76 **PASSED** / 1 **SKIPPED** (optional `sklearn`) / 3 **DESELECTED**, real existing isolated PostgreSQL 3 **PASSED** / 1 **SKIPPED** / 76 **DESELECTED**; Python compile and 27-file docs check **PASSED**. Counts overlap. Owner's `pip-audit --local --vulnerability-service osv --strict --timeout 60` returned **No known vulnerabilities found**, exit `0`; the tool noted a different active parent `.venv`, but its target interpreter was the `v2` environment. No customer reports or real model/Gold were involved.
- **Codebase fix:** Pin tested FastAPI/Starlette/Pytest versions in requirements, pin pip `26.2.2` in the Docker build step, and add a fail-closed GitHub Actions `dependency-security` job. The CI job installs pinned pip and `pip-audit==2.10.1`, installs **production + development + optional ML** requirements, runs `pip check` and queries OSV over the installed dependency closure. The scan is live and may fail when OSV is unreachable; that must be reported as unavailable verification, not clean.
- **Scope / gaps:** Windows smoke verifies an isolated candidate, not the release image's production security. GitHub CI on the *patched repository SHA*, container/API/Alembic, and the new OSV gate must be verified independently. The Starlette TestClient `httpx`/`httpx2` and AnyIO deprecation warnings remain non-failing compatibility debt; do not silently change the untested client library. Vulnerability scans report **known advisories at scan time**, not a comprehensive penetration test.
- **Boundary remains:** P4-02/03/04/05/07/08/09/10 gated real taxonomy, semantic Gold, calibration, AuthN/AuthZ, review concurrency/audit and feedback rights are still BLOCKED/DEFERRED for actual authorized work, at latest by Phase 6. The marker is **`PHASE_4_IMPLEMENTED_AWAITING_VERIFICATION`**, not complete; this correction does not authorize Phase 5.
- See [ADR-012](decisions/ADR-012-phase4-dependency-security-remediation.md) and [risk R-17](risk-register.md).

## GitHub security hardening verification (authoritative REMOTE/AVAILABLE evidence)

- **Dependency and CI implementation commit:** [37482f89b37dfa981a92b119e9a105caf18db8ef](https://github.com/Amirmahdimtz/text-classification-service/commit/37482f89b37dfa981a92b119e9a105caf18db8ef). **Documentation/ADR evidence commit:** [dbbef9dfd11d4cea61ce50eff58abbc95ba34448](https://github.com/Amirmahdimtz/text-classification-service/commit/dbbef9dfd11d4cea61ce50eff58abbc95ba34448).
- **[GitHub Actions run 40093998343](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40093998343): SUCCESS on `dbbef9df`**. Four jobs succeeded: `independent` 76 PASSED / 1 SKIPPED / 3 DESELECTED; `ml-independent` 27 PASSED; `integration` 3 existing real isolated PostgreSQL PASSED / 1 SKIPPED / 76 DESELECTED, Docker build/start/health and Alembic smoke PASSED; `dependency-security` `pip check` PASSED and OSV audit reported `No known vulnerabilities found`. Tests overlap and must not be summed. Python in CI was 3.13.16 (owner Windows candidate was 3.12.10).
- **Assessment:** R-17 known vulnerable dependency set was mitigated in declared requirements and rebuilt image in this CI run; an automated fail-closed scanner now guards future pushes. This is **not** a declaration that all security issues are absent; network-failed scans must remain unresolved and unknown future advisories are not pre-approved.
- **Unchanged Phase 4 gate:** Independent code/software verification is PASSED; real category semantics, authenticated reviewer lifecycle, concurrency/audit and calibrated model/Gold/server checks remain BLOCKED/DEFERRED per P4 task ledger, to be genuinely resolved by Phase 6. **No `PHASE_4_COMPLETE_READY_FOR_PHASE_5`, no Phase 5 progression authorization and no Phase 5 execution.**
