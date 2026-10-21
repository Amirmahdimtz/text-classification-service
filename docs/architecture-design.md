# P1 — Architecture and operational design boundaries
**Status:** Binding architectural pattern from Service_Architecture_Guide_FA.md; runtime realization deferred to Phase 2+.

## Layer responsibilities
- Host: FastAPI startup/lifespan, configuration selection, DI bootstrap, server and health readiness.
- Application: Pydantic HTTP DTO, thin Controllers, authentication/HTTP error mapping, auto-discovery /api/v1/{feature}.
- Core: classification orchestration, category/policy checks, preprocessing coordination, grounded explanation, review business workflows. No HTTPException or SQLAlchemy session in Core.
- Infrastructure: SQLAlchemy models/repositories/AsyncSession, Alembic, Vault/config/DI, and isolated ML provider to runtime.

~~~text
HTTP → Host / WebService → Application Controller → Core Service
                                            → Infrastructure Repository → PsqlDbContext → PostgreSQL
                                            → Infrastructure ML Provider → Inference Runtime
~~~

## Mandatory conventions
- Controller: src/application/{feature}/{feature}_controller.py; {Feature}Controller.api(): APIRouter.
- Service: src/core/services/{feature}/{feature}_service.py; async methods suffix _async.
- Repository: src/infrastructure/repositories/{feature}/{feature}_repository.py with BaseRepository for generic CRUD; queries remain here.
- DTO: src/application/{feature}/dtos/{feature}_dto.py (Pydantic); Models in src/infrastructure/models/ (SQLAlchemy).
- @inject for dependent Controller, Service, Repository and Infrastructure providers, with constructor type hints and package auto-discovery. Do not manually register discovered providers.
- bootstrap_di before WebService resolution; infrastructure → core → application scan order; verify imports and discovery at runtime.
- Shared AsyncEngine/sessionmaker; bounded per-operation Session; Infrastructure-owned atomic transaction for result+evidence+audit.
- ConfigReader, VaultService, PsqlDbContext are singleton infrastructure providers; other providers not singleton by default.
- No unnecessary interfaces, DDD, CQRS, Hexagonal/ports-adapters or substitute DI framework.
- Models imported into Alembic metadata; migrations committed and tested only when schema implementation begins.

## ML boundary
Inference Runtime loads artifacts once or by controlled release, never per request. Async API must not block event loop; networking/process approach and batching await measured runtime choice. Preprocessing must preserve original evidence offset mapping. Calibration/decision/explanation are distinct governed stages; infrastructure failures are not business OUT_OF_SCOPE.

## Deployment notes
TBD: AuthN strategy, secrets and Vault enabled mode, location, network segmentation, inference GPU vs CPU, queues, observability provider, CI runner, dependency versions and SLO. No executable stack or migration is generated in this design-only phase.
