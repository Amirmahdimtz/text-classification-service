# ADR-014 — Conditional technical authorization for limited independent Phase 6 entry

**Status:** `CONDITIONAL_PROGRESSION_APPROVED` — TECHNICAL_SCOPE_ONLY (2026-10-24)
**Destination:** Phase 6 — Deployment, Production Hardening & Final Acceptance (**NOT STARTED**)
**Origin:** Phase 5 `PHASE_5_IMPLEMENTED_AWAITING_VERIFICATION` (**unchanged**).
**Authority:** Project owner's explicit request to audit Phase 5, repair available defects, and determine readiness for the next phase. This is a technical permission decision, **not** the distinct `فاز ۶ را شروع کن` command and **not** employer/Production approval.
**References:** approved Implementation Plan v1.1.0 §§6/11/12/13, Architecture Guide, ADR-008, ADR-010, ADR-013, [Phase 5 execution ledger](../phase-5-execution.md) and [Risk Register](../risk-register.md).

## Evidence and remaining real blockers

- **Source entering audit:** `e73d0bf074c077ca6cb2a52ecf99b7af4e07cb2a`; four-job [CI run 40099532832](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40099532832) SUCCESS. Owner Windows local evidence for earlier Phase 5 source `2129d174...`: **82 independent PASSED**, **4 live isolated PostgreSQL PASSED**, doc/compile PASSED; later owner-reported local pip `26.2.2`, `pip check` PASSED, strict OSV `No known vulnerabilities found` at scan time.
- **Phase 5 gate audit found three fixable lifecycle bugs:** DI remained bootstrapped if Controller discovery/mount raised in `create_app()`; failed DB engine disposal could skip `shutdown_di()`; concurrent model warmup and provider close could retain a model reference after close. Corrected only existing Host/Infrastructure code, added test-only fault/race regressions in `tests/test_phase5_host.py` and `tests/test_text_classifier_provider.py`.
- **Corrected code SHA:** `fda5b1062010ccbf10e8715195c496b378f95e6c`; [CI run 40100292584](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40100292584) completed SUCCESS in all four jobs: independent **84 PASSED / 1 SKIPPED / 4 DESELECTED**; actual isolated PostgreSQL **4 PASSED / 1 SKIPPED / 84 DESELECTED**; offline synthetic ML **28 PASSED** (overlapping); Docker/API/Alembic smoke successful; `pip check` PASSED and OSV **no known vulnerabilities** at scan time. No new business tables/migrations/routes. The corrected SHA has **no new owner Windows post-fix test evidence**; repeat the existing local commands when convenient. No production runtime/model quality is claimed.
- **Critical external omissions persist:** signed category taxonomy and single/multi-label decision, approved API result schema, customer AuthN/AuthZ and reviewer isolation/retention, physical business DB model/idempotency/audit transaction, lawful dataset and Gold/OOD, calibrated decision thresholds and groundedness review, approved real model release and performance/SLO targets, server/runtime permissions, backup/RPO/RTO, UAT. P5-02..05, business-specific P5-06/07, P5-08/09/10, and real P5-11 review/concurrency/partial commit remain BLOCKED/DEFERRED; P3/P4 real verification debt remains.

## Alternatives

1. Set `PHASE_5_COMPLETE_READY_FOR_PHASE_6` and authorize full Phase 6: **REJECTED**; actual Phase 5 DoD conditions are unmet.
2. Start model/service deployment, exposure or acceptance using stubs: **REJECTED**, violates fail-closed and employer-owned contracts.
3. Block all Phase 6 activities: **REJECTED FOR INDEPENDENT SCOPE ONLY**, because software/DB/security checks have passed and contract-independent validation can proceed safely without customer data.
4. **Chosen:** narrow `CONDITIONAL_PROGRESSION_APPROVED` limited to the scopes below. Authorization alone **does not start Phase 6**.

## Allowed Phase 6 work, only after a fresh explicit owner start command

- **P6-02 subset:** Independent validation of current existing environment separation, fail-closed config parsing, secret non-disclosure and developer/test/production guardrails **without enabling Vault, changing production secrets or assuming an employer network topology**.
- **P6-04 subset:** Regression of *existing* API/DB health/readiness, lifecycle/DI shutdown and safe failure handling. **Do not** assert that current DB-only `/health/ready` proves model readiness, and do not open any inference route.
- **P6-06 subset:** Current dependency scanner, source/fixture secret scan, redacted logging, safe error/DI/network-failure regressions on test-only non-sensitive inputs. No false assertion of actual identity, tenant isolation or privacy certification.
- **P6-12 subset:** Evidence-only release/operations documentation, independently executable test runbooks, reproducibility/dependency ledger and explicit deferred-acceptance backlog; **no fabricated deployment, artifact, model card or test report**.

**Exclude** any code/config change that activates public business endpoints, introduces business schemas or authorizes confidential data/real model loading before employer approval. Additional independent P6 work would require its own safety/dependency decision.

## Blocked, deferred, risk owner and deadline

- **P6-01 (full), P6-03, model portion of P6-04, P6-05, business AuthZ portion of P6-06, P6-07/08/09/10/11/13**: BLOCKED/DEFERRED pending actual signed specs, infrastructure, model, legal data and relevant human sign-offs; no endpoint/release approval is granted. Documentation-only or independent subsets are separately named above; all other tasks remain out of scope.
- **Risk ownership:** Employer/Product/Taxonomy (taxonomy, label/cardinality, API, thresholds, business acceptance); Security + Data Governance/Reviewer (identity, RBAC, retention, rights, audit/PII); ML + Data Owner (lawful Train/Validation/Gold/OOD, model artifact and calibrated benchmarks); Engineering + Ops (atomic transactions, DI/runtime, capacity, TLS, deployment, migration, backup/restore, rollback).
- **Checkpoint:** Complete and genuinely verify carried P3/P4/P5 and Phase 6 customer/model/security/UAT backlog **before Phase 6 final acceptance**; re-evaluate whenever licensed inputs become available. Testing on synthetic fixtures cannot count as a valid model benchmark or AuthZ sign-off.
- **Local recheck debt:** owner Windows Phase 5 independent suite and isolated PostgreSQL on code SHA `fda5b106...` **NOT RUN** at this review; remote equivalent on that SHA PASSED. Owner: Engineering. Prerequisite: local checkout current `main` and disposable `*_test` DB; checkpoint prior to final verification/acceptance.

## Decision enforcement

1. Preserve `PHASE_5_IMPLEMENTED_AWAITING_VERIFICATION`, `PHASE_4_IMPLEMENTED_AWAITING_VERIFICATION`, `PHASE_3_IMPLEMENTED_AWAITING_VERIFICATION`. Do **not** claim `PHASE_5_COMPLETE_READY_FOR_PHASE_6`.
2. Record separate `CONDITIONAL_PROGRESSION_APPROVED` in `docs/phase-status.md` naming this ADR and safe destination scope; historical Phase 6 blocked-entry note predates actual Phase 5 implementation and remains audit history.
3. Require the distinct owner command `فاز ۶ را شروع کن` before executing **any** Phase 6 work, then refresh `main`, CI/security, prerequisites and the exact remaining safe scope.
4. **No `PROJECT_PRODUCTION_READY_ACCEPTED`** until full real Phase 6 evidence plus authorized employer acceptance.
