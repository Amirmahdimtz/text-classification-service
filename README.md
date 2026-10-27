# Text Classification Service

Production-grade, auditable classification of reports against an approved, versioned taxonomy, with evidence-grounded explanations.

**Current project state:** Phase 6 STARTED for the independent P6-02/04/06/12 subscopes permitted by ADR-014. Formal Phase 3/4/5 markers remain IMPLEMENTED_AWAITING_VERIFICATION; Production Acceptance is BLOCKED. The repository now includes an executable FastAPI/DI/PostgreSQL foundation. GitHub CI has now verified real isolated PostgreSQL connectivity, Docker/API startup and the Alembic empty-revision smoke path; approved business schemas and Windows-local verification remain pending. Phase 3 independent Persian preprocessing, dataset audit, optional baseline trainer, artifact verifier and bounded ML provider exist. No approved taxonomy, real trained organizational classifier, sensitive-data endpoint, calibrated confidence or verified model quality is claimed.

## Architecture contract

Implementation must follow `Host → Application → Core → Infrastructure` and `Controller → Service → Repository → PsqlDbContext` with the project's mandatory architecture guide. Future production code must comply with its constructor dependency injection, `@inject` auto-discovery, DTO, SQLAlchemy Async, and Alembic conventions.

## Phase 1 documentation

See [phase status](docs/phase-status.md), [requirements](docs/requirements.md), [taxonomy contract](docs/taxonomy-spec.md), [API contract proposal](docs/api-contract.md), [evaluation plan](docs/model-evaluation-plan.md), and [security threat model](docs/security-threat-model.md).

All API routes, schemas, roles, categories, thresholds and operational limits marked **PROPOSED / TBD** require explicit owner approval before production implementation. Do not commit real sensitive reports, credentials, private datasets or large model artifacts to this public repository.

## Phase 2 foundation

See the [technical execution ledger](docs/phase-2-execution.md) and [Windows PowerShell runbook](docs/runbooks/phase2-local.md). Only `/health/live` and `/health/ready` are exposed. `DATABASE_URL` must be supplied via the environment; startup intentionally fails when the database is not available. All business schemas and sensitive endpoints remain blocked by approval-dependent contracts. Run `python -m pytest -q -m "not postgres"` for independent tests after installing `requirements-dev.txt`.

**Latest CI evidence:** [Phase 2 run 39597986175](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/39597986175): 20 independent tests and 3 real PostgreSQL integration tests passed; Docker startup and empty-revision Alembic commands passed. No customer schema, authentication policy, classifier or Production acceptance is implied. Production DB DSN configuration enforces `ssl=verify-full`.


## Phase 3 — Offline ML groundwork only

Read [execution/blocked ledger](docs/phase-3-execution.md), [private Windows audit](docs/runbooks/phase3-local.md), [approved-server model runbook](docs/runbooks/phase3-server.md) and [real benchmark status](docs/phase-3-benchmark-report.md). New offline ML dependencies are separately pinned in requirements-ml.txt, not added to the live API image. Model artifacts and any lawful/private datasets must never enter public git. Current marker is PHASE_3_IMPLEMENTED_AWAITING_VERIFICATION; previous technical Phase 2 gate remains valid and Phase 4 independent Core implementation has started and remains awaiting verification. Phase 5 independent resilience/HTTP/isolated PostgreSQL tests are described in [the Phase 5 ledger](docs/phase-5-execution.md) and [Windows runbook](docs/runbooks/phase5-local.md); no final business API, model quality or unrestricted Phase 6 approval is claimed. See [Phase 6 execution](docs/phase-6-execution.md) and [local runbook](docs/runbooks/phase6-local.md).
