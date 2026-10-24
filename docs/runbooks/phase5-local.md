# Phase 5 — Windows PowerShell / isolated PostgreSQL verification

**Scope:** ADR-013 independent Phase 5 host/DI, failure mapping, existing health HTTP contract, test-only model negative paths and PostgreSQL connection refusal/recovery. Does **not** run or certify real classifier/Gold, reviewer AuthN/AuthZ, business E2E, load or confidential data.

## Prerequisites and safe repository checkout

Use PowerShell, Git, Python 3.12 (owner's prior verified local runtime), and Docker Desktop + the existing PostgreSQL 17 Compose topology for isolated DB tests. Do not include any real reports or secrets in test input.

First checkout only:

```powershell
git clone https://github.com/Amirmahdimtz/text-classification-service.git
cd text-classification-service
```

Existing checkout: **first inspect and preserve uncommitted local work**. If `git status --short` shows changes, stop and reconcile without `reset --hard`, `clean` or forced checkout.

```powershell
git status --short
git switch main
git pull --ff-only origin main
git log -1 --format="%H %s"
```

## Independent tests (no PostgreSQL or ML artifact required)

Run from the actual repository root, with an isolated virtualenv:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m compileall -q src tests tools
.\.venv\Scripts\python.exe tools/verify_phase1_docs.py
.\.venv\Scripts\python.exe -m pytest -q tests/test_phase5_host.py
.\.venv\Scripts\python.exe -m pytest -q -m "not postgres"
```

Expect zero exit status and PASSED test results; the optional scikit-learn test may SKIP if `requirements-ml.txt` was not installed. Host tests use fake engines **inside tests only** and must not be interpreted as live DB or model E2E.

## Live isolated PostgreSQL, no destructive operations

Follow [Phase 2's actual disposable Compose/database setup](phase2-local.md) to configure Docker, `DATABASE_URL` and `TEST_DATABASE_URL` privately. Only use the dedicated `phase2_test` (suffix `_test`) database. Never send the values or invoke database resets. After the existing test DB is ready, run:

```powershell
.\.venv\Scripts\python.exe -m pytest -q -rs -m postgres
```

Expected: all PostgreSQL tests PASSED and no unexpected skips. The new `test_phase5_isolated_postgres_connection_failure_and_recovery` tries a refused `127.0.0.1:1` endpoint (no server shutdown or data change) and confirms a separate connection to the real isolated PostgreSQL test DB. It does not verify actual production outage recovery, reviewer concurrency or a business transaction.

If the test DB has already been established and the environment is set to that same isolated test DB, Alembic empty-revision checks are:

```powershell
$env:DATABASE_URL = $env:TEST_DATABASE_URL
.\.venv\Scripts\python.exe -m alembic -c src/infrastructure/alembic/alembic.ini current
.\.venv\Scripts\python.exe -m alembic -c src/infrastructure/alembic/alembic.ini upgrade head
```

There is no Phase 5 business migration. Do **not** run against a production/customer database, use autogenerate on unapproved metadata, drop schemas, run Docker volume deletion or try a destructive outage drill.

## Safe evidence to return

Share only (after redaction): clean/dirty `git status --short`, final HEAD SHA, Python version, test counts and any sanitized assertion failure, Docker `ps` statuses, HTTP status codes for `/health/live` and `/health/ready`, and Alembic exit status. Do not share passwords, any `DATABASE_URL` or `TEST_DATABASE_URL`, connection strings, private host addresses, report content, credentials, model artifacts, or full exception stack traces containing sensitive values.

## Server/model backlog (NOT RUN)

Real authorized train/Gold/OOD/calibration/groundedness, model warmup, classification→review→audit E2E, AuthZ/IDOR/tenant isolation, data-specific load/stress and backup/rollback require approved contracts, lawful data and secure server. No executable commands are invented here; see [Phase 3 server runbook](phase3-server.md) for the currently supported offline tooling, and [Phase 5 execution ledger](../phase-5-execution.md) for unresolved verification IDs. All such tasks stay BLOCKED/DEFERRED until authorized inputs exist.


## Local packaging security follow-up after owner Phase 5 test run

The owner reported 82/82 selected independent and 4/4 isolated PostgreSQL PASSED on the correct HEAD. Their installer notice identified `pip 25.0.1`, which [ADR-012](../decisions/ADR-012-phase4-dependency-security-remediation.md) previously associated with OSV advisories. Those passing tests do not constitute a local vulnerability audit. From the verified project root, and **only if the machine has Python 3.12 registered via `py -3.12`**, use an outside interpreter for the Windows target-environment pip upgrade to avoid self-replacement locking:

```powershell
$py = ".\.venv\Scripts\python.exe"
py -3.12 -m pip --python $py install "pip==26.2.2"
& $py -m pip install "pip-audit==2.10.1"
& $py -m pip check
& $py -m pip_audit --local --vulnerability-service osv --strict --timeout 60
```

`pip --python` must target the **same isolated project's** `.venv`; verify the environment before executing. If `py -3.12` is not available, stop and use a separately verified interpreter rather than guessing. OSV network errors/incomplete scans are NOT RUN/INCOMPLETE, **not** security PASS. Send only sanitized command exits and vulnerability IDs, never package environment variables, DSNs, credentials or confidential inputs. Re-run the Phase 5 independent and PostgreSQL tests if dependency versions are changed. Server/production and employer security acceptance remain separate gates.

