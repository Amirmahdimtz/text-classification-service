# Phase 5 — Required authorization and real-evidence handoff

**Date:** 2026-10-24
**Status:** EXTERNAL DECISIONS REQUIRED / NO CUSTOMER SIGN-OFF IMPLIED
**Use:** Decision/evidence request packet for completing the mandatory Phase 5 DoD without fabricating business schema, taxonomy, sensitive data permissions or real ML performance.
**Latest verified independent code source:** [79062be3](https://github.com/Amirmahdimtz/text-classification-service/commit/79062be3bcfb5a1a95a870642abac432ae7a91db); [CI 40104414514](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40104414514), all four jobs SUCCESS. **Not a fully working classification service.**
**Normative basis:** Implementation Plan v1.1.0 §11 (P5-01..P5-12), Architecture Guide, ADR-001..007 (proposals, not employer approvals), ADR-008/010/013/014 (process/scope only), [closure audit](phase-5-closure-audit.md).

## Required decisions and exact effect on engineering

| Decision/evidence package | Required owner and non-secret deliverable | Tasks unblocked after valid approval | Engineering implementation and real acceptance proof |
|---|---|---|---|
| TAXONOMY + OUTPUT | Employer/Product/Taxonomy Owner: published category IDs, inclusion/exclusion, lifecycle, single vs multi-label policy, ambiguity/OOD semantics, version and classification DTO/status/evidence fields | P5-01/02/07; subset P5-06/08/09 | Implement approved DTO and thin Controller→Service→Provider/Repository; reject wrong versions and inputs, publish versioned OpenAPI and contract tests. Do not invent labels. |
| IDENTITY + DATA SECURITY | Security/Data Governance/Review Owner: permitted environments and data use, identity provider/principal/tenant/record scope, reviewer roles, permission matrix, retention/deletion and audit requirements | P5-03/04/05/08/11 | Implement approved authorization, record-scoped repositories and review/audit workflows; prove unauthorized cross-record/tenant access fails (IDOR), append-only review audit and log redaction. No confidential data in GitHub. |
| BUSINESS PERSISTENCE + RETRY | Product/Security/Engineering Owners: actual entity/key types, relations, unique constraints, Result/Evidence/Audit lifecycle, idempotency namespace/replay/conflict/TTL and reviewer revision policy | P5-03/04/08/11 | Implement SQLAlchemy models + registered Alembic migration; one bounded async transaction for all dependent writes; PostgreSQL real business commit/rollback, duplicate replay/conflict, optimistic lock and concurrency tests. Existing synthetic TEMP-table checks are **not** the final proof. |
| MODEL + GOLD + DECISION | ML Lead/Data Owner/Product: approved data-use permission, frozen disjoint Gold/OOD, taxonomy-aligned versioned model+tokenizer+policy artifact, threshold/calibration rules, per-class and groundedness acceptance criteria | P5-08/09 and carried P3/P4 model gates | Warm real model without per-request load, integrate with authorized API, run independent Macro-F1/per-class/OOD/calibration/coverage-risk, span/explanation groundedness and release-version regression; no synthetic score as production confidence. |
| CAPACITY + SLO + TEST ENV | Operations/Security/Product: approved isolated execution topology, real workload profile, CPU/GPU budget, timeouts/request limits, throughput/latency/SLO targets, operational recovery access | P5-06/08/10/11 | Verify actual model+API+PostgreSQL+review/audit E2E, request/DB/runtime failure, in-flight and concurrent review, realistic P50/P95/P99/throughput/memory/CPU/GPU/load/stress, recovery and rollback. Never claim measurements without running. |

## Evidence registration and no-secret handoff

When decisions become available, record: **document/version, approving authorized role, scope, date, affected P5 task and tests, allowed environment, and confirmation that sensitive content is handled outside this public repository.** Do not paste real report text, full DSNs, credentials, secret tokens, private server addresses, dataset samples or model weights into GitHub issues, pull requests, test fixtures or this chat.

The Phase 5 **engineering implementation starts only when each work item's own approvals are provided**. Employer formal project acceptance is still reserved for the end of Phase 6 under ADR-008; customer-controlled business/security/data specifications must nonetheless be approved before dependent production behavior is built.

## Final Phase 5 acceptance tests, not substitutable by fixtures

1. Actual authenticated request → approved taxonomy model inference → validated evidence/decision → atomic PostgreSQL result/evidence/audit → authorized review/override → immutable audit readback, with version traceability.
2. Real PostgreSQL business migration and rollback/atomicity under injected mid-commit failure, idempotency collisions/replays and concurrent reviewer conflicts.
3. AuthN/AuthZ (tenant/record IDOR, least privilege, rejected credentials), privacy/retention boundaries and redaction with permitted representative test records.
4. Frozen Gold/OOD and actual model artifacts: model/threshold/taxonomy/version mismatch rejection, per-class and Macro-F1, selective-risk/calibration, original-text groundedness and no unsupported explanation claims.
5. Representative latency and throughput P50/P95/P99, timeout/backpressure, memory/CPU/GPU, cold/warm/restart/recovery with approved numeric targets; verified rollback and release compatibility.
6. Independent+integration+security+model E2E regression, runbooks and signed acceptance evidence for the mandatory technical gates.

Until these exist and actually PASS, **Phase 5 marker stays `PHASE_5_IMPLEMENTED_AWAITING_VERIFICATION`**. **ADR-014** permits only the separately recorded independent Phase 6 scope after the explicit owner start command; it is not a substitute for Phase 5 completion. **Phase 6 NOT STARTED; no production acceptance.**

## What is already verified (scope-limited)

- Host/DI/readiness/error redaction, provider cancellation/close race and cumulative capacity+inference timeout budget, source SHA `79062be3bcfb5a1a95a870642abac432ae7a91db`.
- Existing DbContext generic transaction and two synthetic writes with real isolated PostgreSQL; no approved business schema/migration.
- CI [40104414514](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40104414514): independent 87 PASSED/1 optional SKIPPED/5 DESELECTED; real PostgreSQL 5 PASSED/1 optional SKIPPED/87 DESELECTED, offline synthetic ML 30 PASSED (overlapping); Docker/API/Alembic checks and dependency security clean at scan time. Pre-existing two Starlette/httpx and AnyIO deprecation warnings remain. Latest source Windows LOCAL_USER regression/DB verification NOT RUN; earlier user Windows results apply to older code only.

**Risk owners and checkpoint:** Taxonomy/Product, Security/Data Governance/Review Owner, Engineering, ML/Data Owner and Operations as above. Execute all carried Phase 3/4/5 deferred tests with authorized actual inputs **no later than Phase 6 before final acceptance**, preferably immediately upon receipt.
