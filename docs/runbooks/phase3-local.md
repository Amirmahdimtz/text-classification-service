# Phase 3 — Windows PowerShell verification / private dataset audit

**Python 3.12; Docker Desktop; PostgreSQL 17, local host port 55487.** Start by checking local edits before switching branch. For first checkout run:

    git clone https://github.com/Amirmahdimtz/text-classification-service.git
    cd text-classification-service

For existing checkout (do not discard local changes):

    git status --short
    git switch main
    git pull --ff-only origin main
    git log -1 --format="%H %s"

Independent local tests (no real dataset or model needed):

    py -3.12 -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
    .\.venv\Scripts\python.exe -m compileall -q src tools tests
    .\.venv\Scripts\python.exe tools/verify_phase1_docs.py
    .\.venv\Scripts\python.exe -m pytest -q -m "not postgres"

Expected: zero exit from compile, Phase 1 validator PASS, all independent tests PASSED (sklearn-dependent tests may be skipped if optional ML package not installed). For authorized Phase 2 database regression follow the existing docs/runbooks/phase2-local.md precisely with a disposable phase2_test database only, never a customer DB. No new Alembic migrations are required by Phase 3.

## DATASET — DO NOT RUN UNTIL AUTHORIZED

Real data, approved category catalog, label cardinality and input size limits are NOT supplied. An approved UTF-8 JSONL line must contain report_id, group_id (same incident/case), text (unaltered), labels (array), taxonomy_version and optional timezone-aware occurred_at. The private approved category file is a JSON array of actual allowed category codes; no fake categories should be substituted.

Choose an approved private path OUTSIDE this public repository and supply the following PowerShell variables yourself, only after legal authorization:

    $inputJsonl = '<approved-absolute-jsonl-path>'
    $codesFile = '<approved-absolute-category-codes-path>'
    $auditFile = '<new-private-output-manifest-path>'
    $taxonomyVersion = '<approved-version>'
    $authorizationReference = '<non-secret-authorization-reference>'
    $seed = <approved-integer>
    $trainRatio = <approved-float>
    $validationRatio = <approved-float>
    $testRatio = <approved-float>

Set secret DATASET_FINGERPRINT_KEY_HEX in the process environment, using 32 cryptographically random bytes kept separately in approved secret storage. Do not print, send or commit it. For Powershell, random bytes can be obtained with [System.Security.Cryptography.RandomNumberGenerator]::Create() and GetBytes on an allocated byte[32]; convert using [System.BitConverter]::ToString($bytes).Replace('-','').ToLowerInvariant(). Retain the SAME secret for reproducible audit comparison.

Authorized-only audit command, after these prerequisites:

    .\.venv\Scripts\python.exe tools/prepare_dataset.py --input $inputJsonl --approved-codes $codesFile --output $auditFile --authorization-reference $authorizationReference --taxonomy-version $taxonomyVersion --label-mode single-label --ratios $trainRatio $validationRatio $testRatio --seed $seed

The example label mode must be replaced with the formally approved value (single-label or multi-label). Add --temporal if the approved protocol uses time-aware holdouts. Ratios/seed are NOT prescribed by this document. The tool checks duplicates, groups and reproducibility and writes aggregate counts and keyed HMACs, not raw split exports. Heuristic near-duplicate detection is not sufficient for expert adjudication. It intentionally refuses writing metadata within the public checkout or overwriting an output file.

Send sanitized git SHA, Python version, test totals, Phase 1 validator output, DB tests and health status codes. Never send raw reports, PII, HMAC key, DSNs, auth headers, private absolute paths or sensitive cohort statistics.
