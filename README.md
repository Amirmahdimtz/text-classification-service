# Text Classification Service

Production-grade, auditable classification of reports against an approved, versioned taxonomy, with evidence-grounded explanations.

**Current project state:** PHASE_2_IMPLEMENTED_AWAITING_VERIFICATION. The repository now includes an executable FastAPI/DI/PostgreSQL foundation. Real DB, migration and Docker verification remain pending. No approved taxonomy, trained classifier, sensitive-data endpoint, or verified ML/service quality is claimed.

## Architecture contract

Implementation must follow `Host → Application → Core → Infrastructure` and `Controller → Service → Repository → PsqlDbContext` with the project's mandatory architecture guide. Future production code must comply with its constructor dependency injection, `@inject` auto-discovery, DTO, SQLAlchemy Async, and Alembic conventions.

## Phase 1 documentation

See [phase status](docs/phase-status.md), [requirements](docs/requirements.md), [taxonomy contract](docs/taxonomy-spec.md), [API contract proposal](docs/api-contract.md), [evaluation plan](docs/model-evaluation-plan.md), and [security threat model](docs/security-threat-model.md).

All API routes, schemas, roles, categories, thresholds and operational limits marked **PROPOSED / TBD** require explicit owner approval before production implementation. Do not commit real sensitive reports, credentials, private datasets or large model artifacts to this public repository.

## Phase 2 foundation

See the [technical execution ledger](docs/phase-2-execution.md) and [Windows PowerShell runbook](docs/runbooks/phase2-local.md). Only `/health/live` and `/health/ready` are exposed. `DATABASE_URL` must be supplied via the environment; startup intentionally fails when the database is not available. All business schemas and sensitive endpoints remain blocked by approval-dependent contracts. Run `python -m pytest -q -m "not postgres"` for independent tests after installing `requirements-dev.txt`.
