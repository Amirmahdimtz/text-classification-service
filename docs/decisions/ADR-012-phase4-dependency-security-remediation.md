# ADR-012 — Phase 4 dependency-security remediation and CI evidence gate

**Status:** ACCEPTED_TECHNICAL_SCOPE_ONLY (2026-10-24, explicit owner request to fix Phase 4 defects).
**Scope:** Approved code/dependency security hygiene only; **not** approval of taxonomy, reviewer authorization, model, sensitive data, Phase 4 completion or Phase 5 start.
**References:** Architecture Guide, implementation plan v1.1.0, ADR-008, ADR-010, ADR-011; Phase 4 owner Windows verification logs.

## Problem and evidence

On GitHub `main` at `326fe1bc`, FastAPI `0.128.2` selected Starlette `0.50.0`. Pytest was pinned `9.0.2`; the user's original environment contained pip `25.0.1`. Owner OSV/PyPI scans reported five distinct Starlette, one pytest and six pip advisory IDs (raw rows included duplicates). The existing Actions workflow ran unit/ML/PostgreSQL/Docker, but had no vulnerability gate. Timeouts during separate early scans were incomplete evidence, not clean results.

## Decision and bounded implementation

1. Pin `fastapi==0.134.0`, `starlette==1.3.1` and `pytest==9.0.3` in their existing requirements files. These exact versions were first installed/tested on Windows Python 3.12, not chosen from hypothetical compatibility.
2. Pin `pip==26.2.2` in Docker's build environment, not as an application `requirements.txt` dependency. Keep `pip-audit==2.10.1` solely in a dedicated CI security job.
3. Add a fail-closed OSV `pip-audit --local --strict` scan covering the installed production, development and optional offline ML dependency closure, with `pip check` preceding it. Scanner network unavailability is **not** a pass; later advisory disclosures require remediation and recheck.
4. Preserve existing Core/DI/host code and all Phase 4 business gate exclusions. Do not add fake policy, taxonomy, reviewer schema or endpoint. The `httpx`/`httpx2` and AnyIO warnings are compatibility follow-ups rather than justification for unverified dependency swaps.

## Verification and follow-up

- **Owner Windows isolated candidate:** Phase 4 unit 30 PASSED; independent regression 76 PASSED / 1 optional ML SKIPPED / 3 DESELECTED; live isolated PostgreSQL 3 PASSED / 1 optional ML SKIPPED / 76 DESELECTED; docs/compile PASSED; installed-environment OSV reported no known advisories, exit 0.
- **GitHub patched SHA:** [Actions 40093998343](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40093998343) succeeded on `dbbef9df` with all four jobs: independent regression, offline ML, real isolated PostgreSQL/Docker/API/Alembic, and `dependency-security`. The security job checked the installed development/production/ML dependency closure with `pip check` plus OSV (`No known vulnerabilities found`). This proves CI verification of the committed dependency policy at the time, **not** production release security or business acceptance.
- **Residual:** P4-02/03/04/05, P4-07/08/09 and real model/Gold/server E2E remain BLOCKED/DEFERRED; verification checkpoint by Phase 6. This ADR does not authorize Phase 5 conditional progression or change `PHASE_4_IMPLEMENTED_AWAITING_VERIFICATION`.
