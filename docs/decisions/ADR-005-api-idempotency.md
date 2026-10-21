# ADR-005 — API v1, error semantics and idempotency
**Status:** PROPOSED / NOT APPROVED
**Owners:** Product/API owner, security and review owner
**Context:** Duplicate submits/review actions and inconsistent status mapping can corrupt audit or leak report existence.

## Options
A. Versioned synchronous classify + result retrieval + review + published taxonomy read, with scoped idempotency and optimistic review locking (proposed).
B. Async job API with queue and polling (defer unless real SLA/workload requires it).
C. No idempotency or unconditional retries (unacceptable for persistent audited workflow).

## Proposed rules
Controllers auto-mounted under /api/v1/{feature}, never double-prefix. Typed Pydantic DTO, authorized record-level access, 401/403/404/409/413/422/429 and sanitized 5xx. Explicit errors for runtime/DB failures. Idempotency namespace authenticated owner + endpoint + key + payload fingerprint, atomic persisted mapping; replay returns same logical result, conflict gives 409. Reviewer expected revision prevents lost writes. Scores must disclose semantic kind, never raw cosine as probability.

## Owner action
Approve actual routes, DTO fields and limits, auth protocol, idempotency TTL/replay semantics, success code, API compatibility and 404-vs-403 privacy behavior. API contract is a proposal, not generated OpenAPI.
