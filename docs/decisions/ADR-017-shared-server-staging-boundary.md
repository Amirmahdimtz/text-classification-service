# ADR-017 — Shared Ubuntu server: API-only staging preparation boundary

**Status:** PROPOSED — owner-requested preparation, NOT Production deployment or employer authorization (2026-10-27).
**Phase:** 6 restricted independent P6-02/P6-04/P6-06/P6-12, pursuant to ADR-014; no P6-03/P6-05/P6-07/P6-13 activation.
**Source of infrastructure facts:** project-owner description, **not SSH-verified**.
**Normative references:** [ADR-014](ADR-014-phase6-conditional-technical-entry.md), [ADR-016](ADR-016-dynamic-late-binding-policy.md), [Phase 6 execution](../phase-6-execution.md), [shared server staging runbook](../runbooks/phase6-shared-server-staging.md).

## Context and new input

Owner reports an Ubuntu 24.04 host, RTX 3090 (24 GB), 94 GB RAM, Docker/Compose/NVIDIA Toolkit, existing shared PostgreSQL 17, a shared vLLM endpoint (Qwen3-8B-AWQ, alias shared-llm, availability NOT VERIFIED), and the existing external Docker network simorgh-db-net. Server hosts multiple independent projects, with this project's intended directory under /srv/projects/text-classification-service/.

The repository's original compose.yaml starts its **own** development PostgreSQL and uses localhost port 8000. It cannot be repurposed unchanged on this shared host. The newly provided host topology is an operational input for a staging design, **not** evidence of approved database credentials, TLS trust, permitted deployment, business taxonomy, valid classification model, resource quota, SLO or data rights.

## Decision / bounded preparation

1. Add an **opt-in, API-only, non-public** staging Compose profile. Never edit existing shared PostgreSQL or vLLM Compose projects and never create a second PostgreSQL/vLLM service.
2. Connect only to the reported **external** simorgh-db-net. The live database must be a dedicated project-specific database and least-privilege role, provisioned and approved by Ops; the service hostname must match the approved TLS certificate. Do not install credentials in Git or share them in logs. ENV_TYPE=production enforces ConfigReader's ssl=verify-full DSN rule; this is *not* proof of a working TLS handshake.
3. Require an approved image with **immutable digest** and an externally managed environment/CA file, explicit local-only non-8000 host port and Ops-approved CPU/RAM/PID limits. Add read-only root filesystem, no new privileges, dropped capabilities and limited temporary storage.
4. Readiness verifies **database scope only**, with X-Readiness-Scope: database. A healthy staging container is **not** proof that model classification, explanation or Production is ready.
5. Do not connect to vLLM, request GPU access, load models, expose classification APIs, mutate physical business schema or run production migrations without their separate approved design and prerequisites.
6. Implementation is repository preparation **only**: no SSH login, deployment, secret installation, server changes, TLS verification, model evaluation or customer signoff is represented by this ADR.

## Alternatives and safety decisions

- Reuse development Compose unchanged: **REJECTED** (duplicated DB and host-port conflict).
- Point at shared PostgreSQL without certificate/least-privilege verification: **REJECTED** (TLS/auth boundary unknown).
- Connect automatically to shared Qwen vLLM as classifier: **REJECTED** (no approved model, quality benchmark, evidence/decision policy or resource contract).
- Expose API publicly or declare Production ready from DB-only liveness: **REJECTED**.
- Prepare fail-closed staging profile and operator-reviewed runbook: **CHOSEN FOR PREPARATION ONLY**.

## External blockers, owners and checkpoint

| Gate | Status / required actual evidence | Risk owner / deadline |
| --- | --- | --- |
| HOST-01 | NOT RUN: authorized SSH/host inspection, directory permissions, network membership, conflicting ports and resource allocation | Ops; before any staging deployment |
| HOST-02 | BLOCKED: project-specific DB/role, PostgreSQL server-auth TLS root certificate matching shared-postgres or approved verified hostname, actual secure TCP test | Ops/Security; before staging DB connection |
| HOST-03 | BLOCKED: reviewed immutable image digest, provenance/SBOM, approved staging environment secret location and quota | Engineering/Ops/Security; before staging deployment |
| HOST-04 | BLOCKED: model/taxonomy/policy/artifact and business schema/API/AuthZ plus lawful Gold/OOD and real E2E | Product/Taxonomy, ML/Data Owner, Security; before final Phase 6 acceptance |
| HOST-05 | DEFERRED: actual model+server benchmark, backup/restore, rollback, UAT, written Production handover/approval | ML/Ops/Employer; before final Phase 6 acceptance |

**Phase status:** P3/P4/P5 IMPLEMENTED_AWAITING_VERIFICATION unchanged; ADR-014 CONDITIONAL_PROGRESSION_APPROVED unchanged; Phase 6 IN PROGRESS / RESTRICTED; PROJECT_PRODUCTION_READY_ACCEPTED BLOCKED.
