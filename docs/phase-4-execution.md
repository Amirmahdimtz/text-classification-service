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
| Local builder — `python -m pytest -q tests/test_phase4_evidence.py tests/test_phase4_decision.py` | **29 PASSED** | New synthetic tests in isolated reconstructed workspace; GitHub CI remains authoritative for full repository |
| REMOTE independent full regression, DI and offline ML | PENDING CI on Phase 4 commit | Record actual run/SHA; do not assume success |
| REMOTE isolated PostgreSQL integration | PENDING CI on Phase 4 commit | Existing 3 tests only; no Phase 4 business schema / reviewer transaction exists |
| LOCAL_USER Windows Python 3.12 and PostgreSQL 17 | NOT RUN on owner machine | Commands in `docs/runbooks/phase4-local.md`; sanitized owner logs needed |
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

- [x] Independent evidence offsets and quote validation code with adversarial tests (isolated builder verification; CI pending).
- [x] No unsupported category explanation presented as verified.
- [x] Raw margins remain non-probabilistic; auto/OOD status issuance gated.
- [x] No unapproved public endpoint, AuthZ, schema, migration or production fake.
- [ ] Full repository CI on exact Phase 4 commit and owner Windows/DB parity.
- [ ] Approved taxonomy/criteria, calibrated release, semantic Explanation Gold and real OOD.
- [ ] Approved reviewer AuthN/AuthZ, immutable audit schema, atomic review/concurrency integration.
- [ ] Real server/model E2E/rollback/load and customer acceptance in Phase 6.

**Progression note:** Do not issue `PHASE_4_COMPLETE_READY_FOR_PHASE_5`. Any **future** independent Phase 5 conditional progression requires fresh owner command, adequate CI/local security/DB evidence and separately recorded scope, risk/debt and authorization. This phase does not start Phase 5.
