# ADR-006 — Persistence, atomic transactions and audit
**Status:** PROPOSED / NOT APPROVED
**Owners:** Engineering architect, security/data owner and review owner
**Context:** Result, evidence, idempotency record and audit must agree despite process failures and concurrent reviewer actions.

## Options
A. One bounded SQLAlchemy AsyncSession transaction in Infrastructure for each multi-entity business commit (recommended).
B. Separate BaseRepository insert_async commits for each row (rejected: partial records on failure).
C. External distributed transaction/event system (do not add without proven need).

## Proposed guarantees
Shared Engine/sessionmaker in singleton PsqlDbContext; Repository remains persistence boundary; one transaction commits result, evidence and audit or none. Reviewer operation locks logical revision, appends change and updates current final category atomically. Keep immutable original prediction/version. Report/tenant isolation enforced on queries. Alembic metadata and migration review required in Phase 2, not created in Phase 1.

## Outstanding
Exact IDs, table column types, FK/UNIQUE/cascade, idempotency retention, audit immutability and deletion/legal-hold strategy need owner approval. Backup/restore and concurrency tests are required future evidence.
