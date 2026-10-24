# ADR-011 — Literal evidence-only rendering and fail-closed Phase 4 decision boundary

**Status:** ACCEPTED_TECHNICAL_SCOPE_ONLY (2026-10-24) under explicit owner Phase 4 command and ADR-010 conditional scope. **Not:** approval of taxonomy relevance, reviewer access, model/calibration policy, external dataset use, schema or production release.
**References:** Architecture Guide, Plan v1.1.0 P4-01..10, ADR-008/009/010, proposed ADR-001/005/006.

## Context and alternatives

Phase 3 provides reversible `fa-offset-v1` normalization, not verified category evidence or a calibrated decision. Customer category criteria and review identity/schema are still unavailable. Producing fluent category narratives, accepting raw margins as probability, activating numeric threshold examples or exposing unauthenticated review mutations would create fake production behavior.

Alternatives considered: (a) invent category-specific heuristics/reviewer tables now (rejected: unapproved contracts and privacy risk), (b) stop all Phase 4 work (rejected: independently testable literal integrity exists), (c) implement evidence-only structural services plus gated decision validation (chosen).

## Decision

1. Core evidence accepts only bounded, exact normalized quote/span proposals consistent with a freshly verified `PreprocessedText`; produces original Unicode code-point `[start,end)` quotes, and rechecks spans before any rendering. It does **not** find category relevance by itself.
2. Explanation service emits a deterministically regenerable, safely quoted Persian **evidence-only transcript** carrying the explicit marker `EVIDENCE_ONLY_UNVERIFIED_RELEVANCE` and no category claim. It rejects empty evidence or changes to quote, span or narrative. It is **not** a production category justification and should not be substituted for Gold-validated category explanations.
3. Draft decision-policy structure may be validated but never equated with an approved, cryptographically/operationally verified release. Automatic classification, OOD determination, confidence and final reviewer decisions remain disabled. Only a non-persisted, non-authoritative `NEEDS_REVIEW`-shaped proposal can pass local structural checks; absence of runtime readiness/policy/taxonomy compatibility is an exception. No HTTP path publishes this proposal.
4. Review permission, transition, optimistic locking, audit transaction, final-category persistence and feedback ingestion stay BLOCKED pending formal contracts. No synthetic production tables/roles/endpoints are added.
5. Services follow existing Core feature convention and `@inject` discovery. An `__init__.py` is necessary specifically for `pkgutil.walk_packages` to descend into the existing Phase 3 Core feature directory; classes with zero dependencies use explicit `__init__` to satisfy the existing injector.

## Consequences / mandatory future verification

Pure integrity tests can pass with non-sensitive synthetic text; they establish no semantic relevance, privacy permission, calibration, Gold groundedness or real reviewer safety. Before use beyond internal scope, bind evidence to authenticated report/version and approved taxonomy/model/policy, implement authorized transactional reviewer workflow and test real PostgreSQL concurrency, evaluate Gold groundedness and calibration/coverage on permitted datasets, and perform end-to-end server verification no later than Phase 6.

Previous `PHASE_3_IMPLEMENTED_AWAITING_VERIFICATION` marker is unchanged. Phase 4 remains `PHASE_4_IMPLEMENTED_AWAITING_VERIFICATION` until real gates are met. Phase 5 is not authorized by this ADR.
