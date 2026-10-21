# Phase 2 — Windows PowerShell verification runbook

**Scope:** Technical backend foundation only. This is not a classifier and does not accept real sensitive reports. Commands were designed against files committed in Phase 2; database/Docker commands require local evidence and must not be marked PASS without it.

## Prerequisites and checkout

Install Git, Python **3.13 x64**, Docker Desktop (for isolated PostgreSQL), and PowerShell. For a first checkout:

```powershell
git clone https://github.com/Amirmahdimtz/text-classification-service.git
cd text-classification-service
```

For an existing checkout, first inspect local work. **Stop if uncommitted edits exist**; do not overwrite them:

```powershell
git status --short
git switch main
git pull --ff-only origin main
git log -1 --format="%H %s"
```

Create an isolated environment:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m compileall -q src tests tools
.\.venv\Scripts\python.exe tools/verify_phase1_docs.py
.\.venv\Scripts\python.exe -m pytest -q -m "not postgres"
```

Expected: compilation exit code 0; Phase 1 validator `PASS`; independent tests `PASSED`. They do not prove a real DB connection or authentication, nor ML quality.

## Disposable development PostgreSQL

The Compose topology binds API and PostgreSQL **only to 127.0.0.1**; it is for a personal development machine, never a Production deployment. Set an uncommitted local password interactively. Environment variables live only in the current PowerShell process and should not be shared in logs:

```powershell
$secure = Read-Host "Choose disposable local PostgreSQL password" -AsSecureString
$env:DEV_POSTGRES_PASSWORD = [System.Net.NetworkCredential]::new('', $secure).Password
$escaped = [Uri]::EscapeDataString($env:DEV_POSTGRES_PASSWORD)
$env:COMPOSE_DATABASE_URL = "postgresql+asyncpg://phase2:${escaped}@db:5432/phase2_dev"
$env:DATABASE_URL = "postgresql+asyncpg://phase2:${escaped}@127.0.0.1:5432/phase2_dev"
$env:ENV_TYPE = "development"
docker compose up -d --build
docker compose ps
Invoke-RestMethod http://127.0.0.1:8000/health/live
Invoke-RestMethod http://127.0.0.1:8000/health/ready
```

Expected: both endpoints return `{ "status": "alive" }` and `{ "status": "ready" }` after database initialization; readiness must be HTTP 503 while DB is down. Startup fails closed on missing/malformed DSN or an unavailable database. Docker image is non-root; no model/provider and no business endpoints are installed.

**Integration database creation (new, isolated database only):**

```powershell
docker compose exec -T db psql -U phase2 -d phase2_dev -c "CREATE DATABASE phase2_test"
$env:TEST_DATABASE_URL = "postgresql+asyncpg://phase2:${escaped}@127.0.0.1:5432/phase2_test"
.\.venv\Scripts\python.exe -m pytest -q -m postgres
```

Expected: `2 passed` when the isolated PostgreSQL database is reachable; the test checks real session, transaction commit and rollback of a temporary-table creation. It does **not** prove production schema FKs, idempotency, or approved business transactions.

## Alembic groundwork

There are **no approved business models or revisions**. The following checks Alembic's configured engine and empty migration graph; it creates no business tables:

```powershell
$env:DATABASE_URL = $env:TEST_DATABASE_URL
.\.venv\Scripts\python.exe -m alembic -c src/infrastructure/alembic/alembic.ini current
.\.venv\Scripts\python.exe -m alembic -c src/infrastructure/alembic/alembic.ini upgrade head
```

Do this only on disposable `phase2_test`, not business/production DB. The actual `upgrade head` may create the Alembic version bookkeeping table; it is NOT a production schema migration. Do not run `stamp`, `revision --autogenerate`, downgrade, drop, delete volumes or reset a database without a reviewed migration and explicit approval. The future migration strategy: review models/metadata → create forward revision on isolated DB → `upgrade head` → drift check → recovery/backup plan → approved deployment. Rollback for data-bearing migrations needs an explicit safety review; no automatic destructive rollback is provided.

## Failure diagnosis and evidence to send

- Send redacted `git status --short`, `git log -1 --format="%H %s"`, compile/pytest output, Phase 1 validator result, `docker compose ps`, health HTTP status codes, and Alembic command outcomes.
- Share only sanitized log event names and exception **types**. Do not paste full `DATABASE_URL`, password, environment dumps, Authorization headers, DSNs, report text, SQL parameters with user data, or stack traces embedding those values.
- If server cannot start: verify Python version/dependencies, Docker health, `ENV_TYPE`, and that `DATABASE_URL` is set in the **same process**; never print its value. A 503 readiness response correctly indicates failed DB connectivity.
- For cleanup, stop containers via `docker compose stop`; **do not** run `down -v` or delete volumes unless you separately approve data loss. Backup, restore, retention, RPO/RTO and real production migration verification are blocked by DEC-08/10/11.

## Deferred technical and policy gates

- `LOCAL_USER`: Real PostgreSQL and Alembic, Docker build/start, startup/shutdown evidence and CI confirmation after push.
- `SERVER_MODEL`: No training, gold evaluation, model-inference, calibration, explanation or GPU/load test is appropriate in Phase 2. Their commands depend on Phase 3+ models and an approved secure server.
- `BLOCKED`: Approved physical taxonomy/report/result schema, identity provider and RBAC, audit/retention policy, real data and security topology. Never use this scaffold for confidential report ingestion without approval.
