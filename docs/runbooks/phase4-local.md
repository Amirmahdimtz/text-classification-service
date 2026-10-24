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
