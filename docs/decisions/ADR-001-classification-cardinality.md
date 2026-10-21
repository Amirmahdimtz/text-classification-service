# ADR-001 — Classification cardinality and outcomes
**Status:** PROPOSED / NOT APPROVED
**Owners:** Employer/product, taxonomy owner, review owner, ML lead
**Context:** Reports may contain multiple topics. API, annotation format and metrics depend on one vs many labels.

## Options
A. Single-label primary category with separate NEEDS_REVIEW and OUT_OF_SCOPE statuses. Simpler schema/macro-F1, but needs business-specific dominant-topic and tie-breaking rules.
B. Multi-label result set with per-label thresholds, revised annotations/metrics and more complex review workflow.
C. Hierarchical classification, only with an approved hierarchical taxonomy.

## Proposed direction (not decision)
Use A only as evaluation hypothesis from implementation plan; cannot encode category of a multi-topic report without approved rubric. Status semantics: AUTO_CLASSIFIED requires valid calibration and evidence; NEEDS_REVIEW abstains; OUT_OF_SCOPE is governed out-of-taxonomy judgment, not an additional label. Infrastructure outages remain errors.

## Consequences and approval
Select A or B; publish examples of multi-topic/ambiguous cases and evaluator metric, tie-breaker and review capacity. API DTO and model training must not freeze until owner sign-off. Decision remains BLOCKED.
