# Text Classification Service

Production-grade, auditable classification of reports against an approved, versioned taxonomy, with evidence-grounded explanations.

**Current project state:** Phase 1 — Requirements, Taxonomy & Detailed Design. This repository initially contains specifications only; no executable classification service, approved taxonomy, trained model, or verified service quality is claimed.

## Architecture contract

Implementation must follow `Host → Application → Core → Infrastructure` and `Controller → Service → Repository → PsqlDbContext` with the project's mandatory architecture guide. Future production code must comply with its constructor dependency injection, `@inject` auto-discovery, DTO, SQLAlchemy Async, and Alembic conventions.

## Phase 1 documentation

See [phase status](docs/phase-status.md), [requirements](docs/requirements.md), [taxonomy contract](docs/taxonomy-spec.md), [API contract proposal](docs/api-contract.md), [evaluation plan](docs/model-evaluation-plan.md), and [security threat model](docs/security-threat-model.md).

All API routes, schemas, roles, categories, thresholds and operational limits marked **PROPOSED / TBD** require explicit owner approval before production implementation. Do not commit real sensitive reports, credentials, private datasets or large model artifacts to this public repository.
