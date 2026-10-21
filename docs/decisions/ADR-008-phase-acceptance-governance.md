# ADR-008 — Internal technical phase gates; external acceptance only at project completion
**Status:** ACCEPTED_BY_PROJECT_OWNER (process decision only, 2026-10-21)
**Supersedes:** Employer/customer sign-off as an automatic prerequisite of every intermediate phase, including the P1-13 and Phase 2 entry-gate wording in the original implementation plan.
**Does not supersede:** mandatory technical verification, evidence-based quality gates, architecture guide, employer-owned data access permissions, security restrictions, or final production acceptance.
**Evidence of request:** Direct instruction from project owner in project conversation, 2026-10-21. This approval is NOT employer approval of any functional specification or dataset.

## Context and conflict
The baseline plan initially required customer/product-owner acceptance at each phase, including a signed taxonomy and customer sign-off for Phase 1. The project owner clarifies that the employer will only provide **formal acceptance after the complete six-phase project**. Therefore, waiting for customer signatures between phases would unnecessarily halt independent engineering work. Per the plan's precedence rule, the latest explicit project-owner instruction supersedes this procedural requirement. The baseline implementation-plan document remains a historical source; this ADR records the authorized override.

## Decision
1. End of each Phase 1..5 uses **INTERNAL TECHNICAL VERIFICATION**, based on files/commit history, completed phase work, tests and recorded limitations. No employer acceptance signature is expected at these intermediate gates.
2. **PHASE_N_COMPLETE_READY_FOR_PHASE_N+1** means the documented technical deliverables for that phase are sufficiently verified for the *permitted, dependency-independent scope* of the next phase; it does **not** mean customer approval, or that unverified/model-dependent work is complete.
3. **PROJECT_PRODUCTION_READY_ACCEPTED** at the end of Phase 6 still requires real integrated/server/model evidence, quality gates, privacy/security sign-off, UAT and **formal employer/customer acceptance**. Engineering and the assistant may not grant that acceptance.
4. Input-dependent decisions remain named, owned, tracked and BLOCKED/TBD; do not invent categories, sample reports, policies, secrets, model accuracy or numerical SLOs.
5. **Just-in-time dependencies:** Work can proceed when independent, but no actual sensitive-data ingestion, final API behavior, final schema dependent on label cardinality/tenant/privacy policy, deployment release, model training/evaluation or employer-specific semantics before corresponding authorizations and inputs exist. Where a missing input prevents a particular work item, record that item BLOCKED without stopping unrelated foundation tasks.
6. Every phase is still started **only on explicit user instruction** ("فاز N را شروع کن"); a technical-ready marker is not a start command. Previous phase tests, deferred risks and missing external evidence are carried forward.
7. Implemented but unverified functionality retains PHASE_N_IMPLEMENTED_AWAITING_VERIFICATION; model/server-related evidence cannot be replaced with mocks or document lint.

## Application to Phase 1
- Verified technical documentation tree and owner-reported local validator PASS at commit 841256f480fda68c84c737dd291481ec88cb1a4a; no runtime/model tests were applicable to this phase.
- Phase 1 documentation and internal review are technically complete **with explicit external and downstream workstream dependencies**, so PHASE_1_COMPLETE_READY_FOR_PHASE_2 is appropriate under this newly approved process gate.
- Taxonomy catalog, single/multi-label choice, sample data rights, security/identity constraints, numerical acceptance targets and employer signatures remain NOT APPROVED and NOT PROVIDED.
- Phase 2 can begin with architecture/bootstrap/DI/testable infrastructure only after new explicit instruction; do not freeze a DB classification schema or exposed auth/API assumptions whose prerequisites are still undecided.

## Alternatives and consequences
- Previous approach: formal employer sign-off after every phase — infeasible in the customer's approval workflow; unnecessarily stalls development.
- Chosen approach: internal, auditable gates with explicit deferred external approvals — permits safe engineering work, but requires strict dependency tracking and prohibits treating technical completion as business acceptance.
- Eliminating all intermediate validation — rejected, as it conceals technical failures and violates the production-grade test strategy.

**Final external acceptance phase:** Phase 6 only. No change to project scope or software architecture.
