# ADR-002 — Taxonomy lifecycle and versioning
**Status:** PROPOSED / NOT APPROVED
**Owners:** Employer / taxonomy manager with product approval
**Context:** Changing category meaning can invalidate historic classifications and dataset labels.

## Options
A. Mutable single list (rejected design proposal: destroys audit traceability).
B. Immutable published taxonomy releases with draft→review→publish→retire and explicit split/merge lineage (recommended for approval).
C. External taxonomy registry integration (only if actual existing corporate registry is supplied and validated).

## Proposed controls
Stable category code/identity, definition, inclusion/exclusion, positive/negative examples and boundary rules per version; publish only after authorized review. Classification/model release must declare compatible taxonomy version. Never rewrite historic versions. An approved migration mapping is required for semantic changes.

## Owner decision needed
Provide actual categories, version naming, approvals, lifecycle states, export rights and class mapping policy. No category content or taxonomy version is assumed approved.
