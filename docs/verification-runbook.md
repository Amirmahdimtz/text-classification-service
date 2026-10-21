# Phase 1 document verification runbook
**Purpose:** Check the actual committed documentation without model, GPU, DB or pip packages.

## First checkout
~~~bash
git clone https://github.com/Amirmahdimtz/text-classification-service.git
cd text-classification-service
git status --short
git log -1 --format="%H %s"
python tools/verify_phase1_docs.py
~~~
PowerShell: use the same Git commands; replace python with py -3 if python is not on PATH. Expect clean git status, an actual SHA and PASS from the document validator.

## Existing checkout — inspect changes before pulling
~~~bash
git status --short
git switch main
git pull --ff-only origin main
git log -1 --format="%H %s"
python tools/verify_phase1_docs.py
~~~
Do NOT run switch/pull over uncommitted changes without safeguarding them; stop and share status. Never use reset --hard or force push. Bash/zsh and PowerShell support these Git operations; interpreter may be python3 on Linux/macOS or py -3 on Windows.

## Interpretation
- Validator checks required paths, local Markdown links, ADR count, expected proposed status, phase marker and a limited high-risk secret pattern scan. PASS means documents are internally consistent at this level; it is NOT employer approval, security audit, API contract test or ML evaluation.
- No pip install, virtualenv, environment secret, Docker, PostgreSQL, server or migrations are needed/available in Phase 1.
- Send: git status --short, git log -1 --format="%H %s", complete validator output and any errors. Remove tokens, usernames tied to sensitive roles, report text and other secrets before sharing.
- If Python is unavailable, report that fact rather than marking test passed.

## Deferred checks
Phase 2: code compile/import, DI discovery, controller/openapi, PostgreSQL integration and migration with actual dependency versions. Phase 3+: Gold Dataset, ML runtime, calibration, explanation, performance and security-integration evidence on an authorized server with actual model artifacts. These are NOT RUN/BLOCKED now.
