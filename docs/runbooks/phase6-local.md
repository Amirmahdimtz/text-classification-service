# Phase 6 — restricted independent Windows and server verification

**Authorization:** ADR-014 restricted P6-02/04/06/12 only. No sensitive organizational reports, secrets, model deployment, migration against business data, destructive backup or Production release. Git, PowerShell, Python **3.13** (CI reference), optional Docker Desktop and isolated PostgreSQL 17.

## Checkout without overwriting local work

First checkout only:

```powershell
git clone https://github.com/Amirmahdimtz/text-classification-service.git
cd text-classification-service
```

Existing checkout: inspect `git status --short` first; if dirty, stop and preserve changes before switching/pulling. Never reset hard, force-push or delete work.

```powershell
git status --short
git switch main
git pull --ff-only origin main
git log -1 --format="%H %s"
```

## Independent compile, DI, HTTP, config and security regression

```powershell
py -3.13 --version
py -3.13 -m venv .venv
$py = ".\.venv\Scripts\python.exe"
& $py -m pip install -r requirements-dev.txt
& $py -m pip check
& $py -m compileall -q src tests tools
& $py tools/verify_phase1_docs.py
& $py tools/verify_phase6_security.py
& $py -m pytest -q tests/test_configuration.py tests/test_lifespan.py tests/test_phase5_host.py tests/test_phase6_hardening.py tests/test_di.py tests/test_web.py tests/test_logging.py
& $py -m pytest -q -m "not postgres"
```

Expected: compile/validators exit 0; tests PASS, optionally SKIP sklearn-only tests when optional ML dependency is absent. Targeted tests overlap full independent count. `/health/ready` reports **database-only readiness** with `X-Readiness-Scope: database` on 200 or 503, not model readiness. If Python 3.13 is missing, report actual installed version; do not mark run PASS.

## Live isolated PostgreSQL/Docker/Alembic

Follow the actual [Phase 2 local procedure](phase2-local.md) for an interactive **uncommitted** local password, environment variables `DEV_POSTGRES_PASSWORD`, `COMPOSE_DATABASE_URL`, `DATABASE_URL` and isolated `TEST_DATABASE_URL` ending in `*_test`. Never print or share variable contents.

```powershell
& $py -m pytest -q -rs -m postgres
$env:DATABASE_URL = $env:TEST_DATABASE_URL
& $py -m alembic -c src/infrastructure/alembic/alembic.ini current
& $py -m alembic -c src/infrastructure/alembic/alembic.ini upgrade head
docker compose ps
```

Execute only when the verified isolated test DB is available. Otherwise mark PostgreSQL/Compose and migration smoke `BLOCKED/NOT RUN`. Existing Alembic has no approved business revisions; smoke may create version bookkeeping but must not run on customer DB. Stop containers using `docker compose stop`; never delete volumes without approval.

## Optional offline dependency scan (network required)

```powershell
& $py -m pip install -r requirements-ml.txt "pip-audit==2.10.1"
& $py -m pip check
& $py -m pip_audit --local --vulnerability-service osv --strict --timeout 60
```

CI already runs these pinned checks on the commit; Windows local must be reported separately. OSV network failures or vulnerabilities are not PASS. The bounded signature scanner and OSV do not certify enterprise AuthN/AuthZ, tenant IDOR, privacy or historical leaked secrets.

## Evidence to share safely

Redacted SHA and git status (no private filenames), Python version, exact test pass/fail/skip totals, validator status, Docker `ps` health, HTTP 200/503 and readiness scope header, Alembic exit status, security scan exit code and exact GitHub run URL. Never provide DSNs, passwords, tokens, Authorization headers, confidential text, HMAC keys, sensitive file paths or raw production logs.

## SERVER_MODEL — mandatory but not yet permitted

Owner-approved lawful Train/Validation/Test/Gold/OOD, signed taxonomy/label mode, secure business API/schema, actual model/decision release, permitted CPU/GPU/server, SLO/RPO/RTO and reviewer identities are prerequisites. Only when authorized: execute real model, Gold/per-class/OOD/calibration/groundedness, E2E, reviewer/IDOR, load/stress/soak/backup/restore/rollback and UAT. No runnable release/server script is claimed to exist yet for these gates; see [actual offline ML tools and limitations](phase3-server.md) and [Phase 6 debt ledger](../phase-6-execution.md). All remain BLOCKED/DEFERRED until genuinely executed.
