# Phase 6 — shared Ubuntu server: safe staging preparation

**Status: PREPARED ONLY.** Source: owner-reported Ubuntu 24.04 host; Docker/Compose/NVIDIA Toolkit; shared PostgreSQL 17 and external simorgh-db-net; shared vLLM on port 8000 with unverified model readiness. This runbook does **not** certify live access, TLS, credentials, model, SLO or Production. See [ADR-017](../decisions/ADR-017-shared-server-staging-boundary.md) and [Phase 6 gate ledger](../phase-6-execution.md).

## Architecture and isolation

- Project path on host: /srv/projects/text-classification-service/; all shared services stay under their existing /srv paths and retain their own lifecycle.
- The **new separate** deploy/compose.staging.yaml has just an API service, project name text-classification-service-staging, external network simorgh-db-net, and a **loopback-only configurable host port**, not port 8000.
- There is **no PostgreSQL**, vLLM or GPU service in this Compose file. Server GPU and shared Qwen vLLM are not required for this independent API/DB infrastructure smoke; an LLM is not automatically an authorized classifier or grounded explanation source.
- The repository root compose.yaml remains **development-only** and must never be run against this shared host for staging/Production.

## Step A — inspection without modifying shared services

Run in an authorized SSH shell on the server. Commands inspect only; they do not create containers, directories, networks, databases or GPU allocations. Never share private SSH keys, passwords, full inspect/config output, connection strings or sensitive neighboring project names.

~~~bash
uname -srmo
sed -n '1,6p' /etc/os-release
docker --version
docker compose version
docker info --format '{{.ServerVersion}}'
docker network inspect simorgh-db-net --format '{{.Name}} {{.Driver}}'
docker ps --filter 'name=shared-postgres' --format 'table {{.Names}}\t{{.Status}}'
ls -ld /srv /srv/ai-inference /srv/shared-postgres /srv/projects
df -h /srv
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader,nounits
ss -lnt '( sport = :8000 )'
~~~

**Report only redacted outcomes**: Ubuntu release, Docker/Compose present, network present, PostgreSQL health status **if exact container identification is confirmed**, /srv capacity, GPU memory availability, and port 8000 in-use yes/no. nvidia-smi or exact directory names may differ; record NOT RUN/BLOCKED, not PASSED. A reported Docker hostname shared-postgres is **not enough** to verify network membership, certificate SAN, DB account privileges or server TLS.

## Step B — reproducible repository and static safety checks

On the server, only **after Ops authorizes creating the separate project checkout directory**, use the established repository checkout procedure in [Phase 6 local runbook](phase6-local.md): first clone if absent; for an existing checkout review git status --short, then git switch main and git pull --ff-only origin main. Do not overwrite work or use reset/force-push. Pin and record the source SHA; do not treat a future source commit as automatically accepted.

On a workstation/CI with Python and requirements-dev already installed, from the repository root:

~~~bash
python -m compileall -q tools/verify_stage_config.py tests/test_phase6_staging.py
python -m pytest -q tests/test_phase6_staging.py
python tools/verify_stage_config.py
~~~

The last command verifies the **static profile** without requiring a server, Docker or secrets. A PASSED result is **not** a successful deployment or network/TLS test.

## Step C — approvals and runtime prerequisites before staging start

Ops/Security must first verify in the actual shared PostgreSQL and Docker environment:

1. A **separate, approved** staging database and least-privilege role for this project, with no write access to other projects. No schema reset, Volume change, privileged migration or use of production/customer data.
2. Server-authenticated PostgreSQL TLS, trusted CA root and hostname verification: the certificate must match the approved service name (initial owner-provided candidate shared-postgres), and the credential-bearing DATABASE_URL must use postgresql+asyncpg with ssl=verify-full. If the actual shared service cannot support verified TLS, **STOP/BLOCK**; do not downgrade SSL, turn off host verification or silently use another DB.
3. An Ops-controlled environment file **outside the checkout**, readable only by its intended operator/service, holding DATABASE_URL (never committed or printed). The staging profile injects ENV_TYPE=production independently. The root CA file must be approved and readable by the non-root container user.
4. A reviewed immutable OCI image reference of the form registry/repository@sha256:<64-hex-digest> with provenance. Image signing, SBOM/release contract and actual migration state require separate signoff. The current development Docker build is not a production-approved release.
5. Explicit **Ops-approved** values for TCS_STAGING_CPUS, TCS_STAGING_MEMORY (m or g units), TCS_STAGING_PIDS, and an unused loopback-only TCS_STAGING_PORT other than 8000; do not steal GPU/CPU reservations from other services.

Variables required in the operator shell (values intentionally **not** provided here): TCS_STAGING_IMAGE, TCS_STAGING_ENV_FILE, TCS_STAGING_DB_CA_FILE, TCS_STAGING_CPUS, TCS_STAGING_MEMORY, TCS_STAGING_PIDS, TCS_STAGING_PORT. Do not put these in tracked files or send their values over chat. Runtime checker validates format/permissions, **not certificate validity or actual SQL authentication**.

After authorized setup and with requirements-dev available:

~~~bash
python tools/verify_stage_config.py --runtime
docker compose -f deploy/compose.staging.yaml config --quiet
~~~

Never run docker compose config **without** --quiet when an environment file may contain credentials. A failing preflight is BLOCKED; do not bypass it. Running these checks does not start containers or change the shared database.

## Step D — separate change approval before staging deployment

This repository preparation does **not** authorize a server deployment. Operations must approve the exact checkout SHA, image digest, target directory, scope of the API-only smoke, network/firewall configuration and rollback path before **any** start/recreate action. Do not run the root compose.yaml. Under an authorized staging-only change, the profile is operated through docker compose -f deploy/compose.staging.yaml ... with explicit operator controls; no new shared database/vLLM containers are part of it. Never expose the local bound API port on a public interface. Database-only X-Readiness-Scope: database (HTTP 200/503) cannot prove model readiness, real inference E2E or UAT.

## Step E — what must still happen before Production Acceptance

- P6-01/03: approved digested release, provenance, SBOM and gated image promotion/rollback.
- P6-02/06: actual verified PostgreSQL TLS, key/secret lifecycle, tenant/record AuthN/AuthZ, IDOR, privacy, audit and network/egress review.
- P3/P4/P5 carried debt and P6-04/05/10: lawful Train/Validation/Gold/OOD, signed Taxonomy and Decision Policy, valid model artifact, calibrated/grounded inference, integrated API/DB/reviewer workflow, real P50/P95/P99/load/stress/soak against authorized workload.
- P6-07/08/09/11/12/13: approved RPO/RTO, isolated backup/restore drill, dashboards/on-call, drift/retrain governance, real UAT, handover and employer sign-off.

No real model release, secure business API, production-specific schema migration or authorized representative dataset has been provided. All such gates remain BLOCKED/DEFERRED; **do not interpret staging config as readiness to serve customer reports**. PROJECT_PRODUCTION_READY_ACCEPTED remains BLOCKED.

## Shared PostgreSQL recovery and TLS change dependency

The existing shared database has `ssl=off`; configured server certificate/key are missing or unreadable. Recovery and off-host storage have **not** been verified. Before starting any staging API, follow the separate [shared PostgreSQL backup/restore and TLS change gate](phase6-shared-postgres-backup-tls.md) (proposed [ADR-018](../decisions/ADR-018-shared-postgres-recovery-tls-plan.md)). This link is **documentation only**, not approval to run backups, change shared database mounts or restart PostgreSQL.
