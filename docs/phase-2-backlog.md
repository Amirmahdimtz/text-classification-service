# Phase 2 backlog — planning only, NOT authorized to start
**Entry gate:** PHASE_1_COMPLETE_READY_FOR_PHASE_2, approved API and minimum schema, security baseline decision, accessible dev/test environment, plus NEW explicit instruction to start Phase 2.

| Item | Deliverable | Dependency | Required verification |
|---|---|---|---|
| P2-01 | Actual runtime dependency versions, Host/config/boot | approved deployment/auth choices | import, config validation |
| P2-02 | DI @inject and controller auto-discovery | architecture guide | bootstrap/discovery tests incl. fail startup |
| P2-03 | PsqlDbContext, bounded AsyncSession, BaseRepository | approved PostgreSQL environment | real DB integration |
| P2-04 | Minimum persisted approved entities | signed conceptual/physical schema | FK/uniqueness/tenant isolation |
| P2-05 | Atomic persistence and scoped idempotency strategy | API and transaction ADR approval | concurrency/rollback tests |
| P2-06 | Approved taxonomy read/managing API components | approved taxonomy and RBAC | HTTP/DTO/permission tests |
| P2-07 | AuthN/AuthZ, ingress size, secrets, TLS/network | security sign-off | negative access/redaction tests |
| P2-08 | Health/readiness, structured correlation and metrics | infra logging decision | readiness/log tests |
| P2-09 | Alembic metadata/migrations | approved schema | isolated clean upgrade, drift checks |
| P2-10 | CI unit/import/static/security baseline | chosen runner/tools | recorded pipeline |
| P2-11 | Container and API/DB environment parity | deployment resource choice | start/stop integration test |
| P2-12 | Local ops, migration, recovery and secrets runbook | running environment | reproducible operator commands |

**Excluded:** fake classifier, trained model, real training/evaluation, grounded explanation engine, full production deployment, artificial passing tests. Model-heavy Phase 3+ tests must run on approved server/model environment, not user's laptop. Do not implement any of these tasks without explicit Phase 2 instruction.
