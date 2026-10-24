# Phase 4 — Windows PowerShell independent verification

Scope: Phase 4 Core-only original evidence/controlled excerpts/review-only policy validation, Phase 1–3 regression and existing real isolated PostgreSQL baseline. Nothing below tests actual ML quality, confidential reports, reviewer DB schema or real taxonomy.

Prerequisites: Windows PowerShell, Python 3.12, Docker Desktop/PostgreSQL 17 for optional existing DB suite, authorized isolated `phase2_test` only. Never share credentials, full DSNs, sensitive report excerpts, private model paths or logs.

For first checkout (only if no local checkout exists):

```powershell
git clone https://github.com/Amirmahdimtz/text-classification-service.git
cd text-classification-service
```

For an existing checkout, review local changes first; don't discard them:

```powershell
git status --short
git switch main
git pull --ff-only origin main
git log -1 --format="%H %s"
```

Once in the repository root, create the environment if necessary:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m compileall -q src tests tools
.\.venv\Scripts\python.exe tools/verify_phase1_docs.py
.\.venv\Scripts\python.exe -m pytest -q tests/test_phase4_evidence.py tests/test_phase4_decision.py
.\.venv\Scripts\python.exe -m pytest -q -m "not postgres"
```

Expected: zero exit from compile/docs validator, all Phase 4 synthetic tests pass, previous independent regression remains green; optional scikit-learn-dependent tests can skip if `requirements-ml.txt` was not installed. Do not add pass totals from overlapping suites.

For real PostgreSQL regression, **first** follow `docs/runbooks/phase2-local.md` to provision/configure only the pre-existing isolated `phase2_test` database. Re-use its already verified PostgreSQL Docker setup; never run against production or a customer DB. Do not print `TEST_DATABASE_URL` or delete Docker volumes. Once the private environment variable has been configured:

```powershell
.\.venv\Scripts\python.exe -m pytest -q -rs -m postgres
```

No Phase 4 migration exists; no new Phase 4 database test can pass until reviewer contract/schema is approved. Do not run an unapproved `--autogenerate` to invent tables. Do not run Phase 6 server commands until permission and actual data/artifacts exist.

Share sanitized: `git log -1` SHA, `git status --short` result, Python version, test totals/errors, docs validator output, PostgreSQL test totals and CI link. Redact all hostnames/paths that reveal private infrastructure, tokens, DSNs, auth headers, dataset content and secret values.

## Dependency-security parity after the Phase 4 security patch

The repository requirements now pin `fastapi==0.134.0`, `starlette==1.3.1` and `pytest==9.0.3`. From the repository root, use an isolated Python 3.12 virtualenv and the pinned requirement files above. Inspect `git status --short` before pulling; never discard local changes. To prevent Windows self-update locking, update pip in the *target* venv via a different working Python interpreter, as described in the actual owner Windows evidence:

```powershell
$target = "..\\.venv-phase4-security-v2\\Scripts\\python.exe"
$runner = ".\\.venv\\Scripts\\python.exe"
Test-Path $target
& $runner -m pip --python $target install --upgrade "pip==26.2.2"
& $target -m pip install -r requirements-dev.txt
& $target -m pip install "pip-audit==2.10.1"
& $target -m pip check
& $target -m pip_audit --local --vulnerability-service osv --strict --timeout 60
$LASTEXITCODE
```

Run these only when `Test-Path` is `True` and the target is the intended isolated test environment. An activated `.venv` may yield an audit warning when targeting another interpreter; check the scanner's target path and results. A successful `pip check` is not a security scan. If OSV/network is unavailable, report `NOT RUN/INCOMPLETE` and the sanitized error, not `PASSED`. Never print passwords, DSNs, confidential reports or private host details. Do not treat a clean vulnerability scan as proof of model correctness.
