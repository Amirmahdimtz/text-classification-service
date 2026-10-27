# Phase 5 — alignment audit for owner-provided Implementation Plan v1.2.0

**Review date:** 2026-10-27
**Normative inputs:** owner-uploaded `Text_Classification_Service_Implementation_Plan_FA_v1.2.0.md` (Project Source), full `Service_Architecture_Guide_FA.md`, reviewed GitHub `main` at `fc7638ba09c71d72061bb9d202947980c5695446` before the focused fix.
**Decision:** Plan v1.2.0 authorizes **dynamic/late-bound independent development**, NOT acceptance of an unimplemented classification/review feature. [ADR-016](decisions/ADR-016-dynamic-late-binding-policy.md) records this design/progression decision. Plan itself is a Project Source; this file does not claim it was copied to GitHub.

## Scope and exact Phase 5 status

| Plan domain | Independently implemented/tested (actual scope) | External dependency and mandatory real test | Current status |
|---|---|---|---|
| DYN-01 Taxonomy / label mode | Pure immutable draft add/revise/deactivate/impact, structural version check; synthetic unit/DI tests | Approved categories/cardinality, authorization, durable version registry/audit, publish/split/merge, compatible evaluated model | PARTIAL; CONTRACT_DEPENDENT_BLOCKED |
| DYN-02 API / persistence | Existing Host error/HTTP-negative contracts; PostgreSQL DbContext session and test-only atomic two-write rollback | Signed business DTO/versioned OpenAPI, Result/Evidence/Audit schema/Alembic, idempotency/review atomicity and real business E2E | PARTIAL; CONTRACT_DEPENDENT_BLOCKED |
| DYN-03 Security / privacy | Config/TLS/secret checks, redaction, negative tests confirming unapproved business/taxonomy/review routes are closed | Real IdP, record/tenant scope, retention/privacy approval and IDOR/authorized review security tests | PARTIAL; CONTRACT_DEPENDENT_BLOCKED |
| DYN-04 Data / model | Synthetic-only dataset leakage and preprocessing, artifact hashes, baseline/provider fail-closed and version validations | Lawful Train/Val/Gold/OOD, released model/decision/calibration, per-class/groundedness and end-to-end inference | PARTIAL; REAL_EVIDENCE_DEFERRED |
| DYN-05 Runtime / SLO | Existing DB-only health, provider concurrency/deadline/shutdown, CI Docker and isolated PostgreSQL | Model-ready health with actual release, approved server/workload/SLO, load/stress/soak/backup/restore, p50/p95/p99 | PARTIAL; REAL_EVIDENCE_DEFERRED |

The matrix documents only what is supported by repository code and observed CI. For the unapproved business API, there is **no** real classification endpoint or authenticated category administrator; the negative-route regression is not an authorization implementation.

## P5-01..P5-12 remaining task boundaries

- **P5-01/02/07:** Actual thin secure classification Controller→Service→Provider/Repository and final response/OpenAPI are **BLOCKED** by output/cardinality/auth contracts. Existing host/DI/error regression PASS is only a subset.
- **P5-03/04:** Business model schema, Alembic, Result/Evidence/Audit transaction, replay/idempotency TTL/conflicts are **BLOCKED**. The isolated temporary PostgreSQL two-write test is not equivalent to final business persistence.
- **P5-05:** Authentication, authorization, admin/reviewer roles, tenant/record access and IDOR are **BLOCKED**; closed endpoints and safe error logging currently tested.
- **P5-06:** Current safe timeouts, model/DB unavailable, headers and failure mapping tested; final approved request limits, real load/backpressure and operations policies remain pending.
- **P5-08/09/10:** Real authenticated model→DB→Review→Audit E2E, Gold/Explanation regression and real model performance **DEFERRED/NOT RUN**, blocking prerequisites listed above.
- **P5-11/12:** Existing lifecycle/disposal, failure and negative route tests, and scoped runbooks implemented; real reviewer concurrency/partial-commit security and final business/model runbooks still pending.

**P5 full DoD remains NO-GO.** It is permitted under Plan v1.2.0 to enter **only the explicitly approved independent Phase 6 scopes** with the required separate start command, without changing the Phase 5 marker.

## Targeted regression and evidence

- **Change:** `tests/test_phase5_host.py`, existing independent HTTP contract test now also requests `GET /api/v1/taxonomy/categories` and `POST /api/v1/taxonomy/categories` and asserts 404 + safe request headers while admin/readonly routes are not approved; no runtime API introduced.
- **Source commit:** [72eb5427](https://github.com/Amirmahdimtz/text-classification-service/commit/72eb5427a917ac0bb0315cd4c692d0a5a8d5b3a3).
- **REMOTE/AVAILABLE:** [GitHub Actions run 40464115968](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40464115968) on exact code SHA, completed SUCCESS all four jobs: independent **114 PASSED / 1 optional SKIPPED / 5 DESELECTED**; real isolated PostgreSQL **5 PASSED / 1 optional SKIPPED / 114 DESELECTED**; offline synthetic ML **30 PASSED** (overlapping), dependency `pip check` and strict OSV PASS at scan time; two existing dependency deprecation warnings.
- **LOCAL_USER latest source:** NOT RUN; previous Windows success occurred on older SHAs. No real MODEL/SERVER/GOLD/UAT result, no new migration, no permanent table.
- **Marker:** `PHASE_5_IMPLEMENTED_AWAITING_VERIFICATION`; **progression:** `CONDITIONAL_PROGRESSION_APPROVED` for ADR-014-only scope, Phase 6 NOT STARTED; **acceptance:** `PROJECT_PRODUCTION_READY_ACCEPTED` not issued.

## Three editorial ambiguities in v1.2.0 (not silently changed)

1. **§5.1** says some proposed routes remain provisional “تا پایان فاز ۱”, while §5.1.1 and §§6/11/12 defer external contract approval until the final Gate. Interpret that phrase as historical proposal timing, **not** an active requirement that current unknown API details be accepted. Recommend clarifying in a future Plan revision.
2. **§7 Phase 1 full DoD** still requires an approved taxonomy/mode, while v1.2.0 permits the same decisions to be late-bound. Keep the full DoD unchanged and use the **separate conditional progression** rule; do not retroactively relabel the historical Phase 1 marker without evidence.
3. **Risk R-02** mentions reducing an acceptance scope while awaiting data. This cannot mean lowering mandatory model quality/security or final Production criteria. Clarify as restricting the **development/evidence scope**, not weakening final acceptance.

These points are editorial reconciliation notes, **not** a unilateral replacement of the owner-supplied Plan or of customer approvals. If owner chooses a new Plan revision, update its text and future ADR references explicitly.

## Next safe actions and owners

- Engineering may continue only feature-independent tests, interface/DTO structural validation, Config fail-closed, version-impact diagnostics and documentation within the Phase 5 scope; avoid speculative business schemas or exposing management/classifier APIs.
- Product/Taxonomy, Security/Review, ML/Data Owner, and Operations must eventually approve the five DYN packages. Then Engineering implements the real features and executes actual tests. The mandatory final deadline is **before Phase 6 production acceptance**; if prerequisites never arrive, the final Gate stays BLOCKED.
