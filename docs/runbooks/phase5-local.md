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


## Owner Windows dependency-security follow-up — 2026-10-24

The owner completed the steps immediately above in the project virtualenv. The recorded output confirms pip upgrade from `25.0.1` to `26.2.2`, existing `pip-audit==2.10.1`, `pip check`: `No broken requirements found`, and strict OSV local audit: `No known vulnerabilities found`. See [Phase 5 execution evidence](../phase-5-execution.md). **Local installed-dependency sub-gate PASSED at scan time**; earlier follow-up request to perform these four operations has been satisfied.

On future Python dependency updates, repeat the existing `pip check` and `pip_audit` commands and relevant functional/integration regressions. Retain the redacted output and command exit statuses. Optional ML packages not installed in this venv are outside `--local` coverage; the separate CI `dependency-security` job evaluates the installed ML closure. A successful package audit remains separate from business AuthN/AuthZ, real model quality and Production release acceptance.

## Post-audit Phase 5 lifecycle fix — optional owner Windows re-verification

A targeted Phase 5 correctness review changed `src/host/app.py` and `src/infrastructure/text_classifier_provider.py` (with test-only fault/concurrency regressions) at [source fix fda5b106](https://github.com/Amirmahdimtz/text-classification-service/commit/fda5b1062010ccbf10e8715195c496b378f95e6c). [CI 40100292584](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40100292584) PASSED all jobs; **no owner Windows post-fix rerun has yet been supplied**. For the latest `main`, after inspecting `git status --short` and preserving any local changes, follow the existing `git switch main` and `git pull --ff-only origin main` instructions above. Run the same installed venv's exact commands:

```powershell
$py = ".\.venv\Scripts\python.exe"
& $py -m compileall -q src tests tools
& $py -m pytest -q tests/test_phase5_host.py tests/test_text_classifier_provider.py
& $py -m pytest -q -m "not postgres"
# Only with the preconfigured approved isolated *_test database:
& $py -m pytest -q -rs -m postgres
```

The duplicate targeted tests overlap the full independent suite; don't sum totals. Return only sanitized command exits, test counts and SHA (never `DATABASE_URL` or `TEST_DATABASE_URL`). No model training or confidential data is needed. A conditional Phase 6 entry decision for narrow independent work is separately recorded in [ADR-014](../decisions/ADR-014-phase6-conditional-technical-entry.md); it does not start Phase 6.

## Owner Windows post-fix verification — 2026-10-24

Owner completed post-audit checks on the correct repository at `684bbbdf88f959f8197b56321ae3136a53355db5`: Python 3.12.10; compilation PASSED; targeted Phase 5 Host/Provider **11 PASSED**; full independent **85 PASSED / 4 DESELECTED**; live isolated PostgreSQL **4 PASSED / 85 DESELECTED**; no failures, only 2 established dependency deprecation warnings. Targeted tests overlap with the full independent suite. The previous `Windows post-fix NOT RUN` statement above is historical and **superseded** by this checkpoint; [Phase 5 ledger](../phase-5-execution.md) contains detailed evidence and gate boundaries. No new manual retest is requested for this exact code solely to discharge this local regression debt.

## Phase 5 explicit completion request — final bounded closeout assessment (2026-10-24)

A newer provider concurrency guard was committed at [source 28afaefb](https://github.com/Amirmahdimtz/text-classification-service/commit/28afaefbbd33ab05fcacba37a1c35ca316d1b47e) with [CI 40102628553](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40102628553) SUCCESS. **Owner Windows post-fix test NOT RUN for this new SHA** (previous Windows run was on `684bbbdf`). When testing the updated checked-out `main` with no uncommitted changes and the same isolated `*_test` PostgreSQL, run existing regression commands earlier in this file. Expected functionality: `InferenceUnavailableError` and no leaked semaphore permit if shutdown races a capacity wait. This does not test a real model or authorize a business API. Required external approval and full completion blockers are itemized in [Phase 5 closure audit](../phase-5-closure-audit.md).

## Engineering-owned Phase 5 backlog follow-up — 2026-10-24

New source [2ac58f4](https://github.com/Amirmahdimtz/text-classification-service/commit/2ac58f419752f52540d146ef5b1126abc68c5) adds a negative Host/DI configuration regression and a real isolated PostgreSQL synthetic two-write atomicity test. [CI 40103494346](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40103494346) PASSED with 86 independent/5 PostgreSQL, plus separately run optional offline ML. To verify locally against the latest source, first inspect and preserve uncommitted work, then fast-forward `main` as already shown above and use:

```powershell
$py = ".\.venv\Scripts\python.exe"
& $py -m compileall -q src tests tools
& $py -m pytest -q tests/test_phase5_host.py
& $py -m pytest -q -m "not postgres"
# Only when TEST_DATABASE_URL privately points to the disposable *_test database:
& $py -m pytest -q -rs -m postgres
```

The new DB test uses **only a temporary table** in the isolated test DB and discards it; it does not create business tables, run a migration, alter or remove customer records. The targeted Host tests are included in the independent suite and should not be added again to totals. Report only sanitized SHA/test counts and exit codes; never share `TEST_DATABASE_URL`, data, model or secrets. Windows local tests for this exact SHA have not been reported and are **NOT RUN**.

## Phase 5 owner final-completion demand — verified independent scope, hard DoD boundary (2026-10-24)

The P5-06 provider now uses one total timeout for capacity wait plus inference. See [source 79062be3](https://github.com/Amirmahdimtz/text-classification-service/commit/79062be3bcfb5a1a95a870642abac432ae7a91db), [CI 40104414514](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40104414514) SUCCESS. The user's older Windows results do not validate this newest source SHA; latest-code LOCAL_USER **NOT RUN**. In the verified repo root, after preserving local changes and safely fast-forwarding main (instructions above), use the existing `$py` to run:

```powershell
$py = ".\.venv\Scripts\python.exe"
& $py -m compileall -q src tests tools
& $py -m pytest -q tests/test_text_classifier_provider.py tests/test_phase5_host.py
& $py -m pytest -q -m "not postgres"
# Only with authorized TEST_DATABASE_URL pointing to the isolated *_test database:
& $py -m pytest -q -rs -m postgres
```

These tests require no confidential reports, real Gold or GPU, and targeted tests overlap the independent group. Do not send DSN/passwords. Actual model/authorized reviewer/API/Gold and capacity verification cannot be done using this synthetic test environment. See [real acceptance evidence prerequisites](../phase-5-acceptance-inputs.md).

## Owner-directed dynamic taxonomy foundation — 2026-10-24

Independent taxonomy draft tests are included in the normal non-PostgreSQL suite and do not require external data, business API, model or DB. Once the latest `main` is safely fast-forwarded after preserving local changes, run from the existing Windows project virtualenv:

```powershell
$py = ".\.venv\Scripts\python.exe"
& $py -m compileall -q src tests tools
& $py -m pytest -q tests/test_taxonomy_drafts.py
& $py -m pytest -q -m "not postgres"
```

[CI 40105875237](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40105875237) independently passed the new tests and existing PostgreSQL/ML/security jobs. Targeted taxonomy tests overlap the independent count. Latest local Windows retest NOT RUN. The new Core service is **draft-only**: no administrative HTTP route, approved database model, Migration or release publish operation exists; do not substitute it for real organization-managed production taxonomy. Authorization/retention/schema and real model/version transition tests remain BLOCKED/DEFERRED.


## Latest Phase 5 dynamic-taxonomy revision regression — 2026-10-24

The internal Core `TaxonomyService.assess_revision` now checks safe structural transitions between adjacent dynamic category drafts. [Commit 4908ca18](https://github.com/Amirmahdimtz/text-classification-service/commit/4908ca1862f9417dc316e995b2770c1212febc24) passed [CI #40107406832](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40107406832) on the exact source SHA. **Local Windows testing on this latest SHA is NOT RUN**.

From the actual checked-out project root, inspect `git status --short` and preserve local changes before `git switch main` and `git pull --ff-only origin main`. Using the existing verified Windows venv:

```powershell
$py = ".\.venv\Scripts\python.exe"
& $py -m compileall -q src tests tools
& $py -m pytest -q tests/test_taxonomy_drafts.py
& $py -m pytest -q -m "not postgres"
# Only with the preconfigured disposable *_test PostgreSQL database:
& $py -m pytest -q -rs -m postgres
```

Report SHA and sanitized command results only; never return DSNs, passwords or report data. Taxonomy-focused tests overlap the independent suite and do not prove real model compatibility, secure category administrator CRUD or publication. All customer-owned runtime/model/security gates remain in [Phase 5 acceptance inputs](../phase-5-acceptance-inputs.md).
