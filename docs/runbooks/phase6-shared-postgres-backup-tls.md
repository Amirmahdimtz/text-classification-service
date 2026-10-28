# Phase 6 — shared PostgreSQL recovery and TLS change gate

**State:** PLAN ONLY / NOT AUTHORIZED FOR EXECUTION. This runbook belongs to the independent P6-12 operational documentation scope under [ADR-014](../decisions/ADR-014-phase6-conditional-technical-entry.md). Its backup/restore operation (P6-07), TLS mutation and staging deployment have **not** been executed or approved. Refer to [ADR-018](../decisions/ADR-018-shared-postgres-recovery-tls-plan.md), [ADR-017](../decisions/ADR-017-shared-server-staging-boundary.md) and [Shared-host staging runbook](phase6-shared-server-staging.md).

## 1 — Evidence snapshot (reported by owner, 2026-10-28)

| Attribute | Evidence | Limitation |
| --- | --- | --- |
| Shared DB | postgres:17, shared-postgres-postgres-1, simorgh-db-net, 4 attached containers | 4 network attachments != 4 active DB consumers |
| DB scope/size | 4 databases, aggregated size 38 MB | excludes WAL, full backup footprint and restore workspace |
| Host free space | 360 GB on same 491G filesystem | NOT off-host disaster-recovery capacity |
| Persistent data | Docker RW volume mounted at /var/lib/postgresql/data, matches active PGDATA | a volume is not a backup |
| Secrets | RO bind at /run/secrets/postgres_password | do not read/copy/disclose secret |
| Network | PostgreSQL 5432 NOT_PUBLISHED on host; listens inside its container on all interfaces | container-to-container access exists through shared network |
| Authentication | TCP trust exact loopback IPv4/IPv6; other networks match SCRAM rule in on-disk HBA view | effective loaded rules / neighbor access still need review |
| TLS | ssl=off; configured server cert/key MISSING_OR_UNREADABLE to postgres user | actual CA/SAN/key and live handshake NOT VERIFIED |
| Recovery | archive_mode=off, no archived WAL evidence; dpkg-db-backup is not a PostgreSQL backup | external logical backups/snapshots unknown |
| Independent application tests | 128 pytest non-postgres PASSED on Ubuntu 3.12.3 after sklearn installed; 5 PostgreSQL DESELECTED | no live shared-host DB integration or model accuracy |

Never show unredacted `docker inspect` environment, Compose config, DB connection strings, private keys, backup scripts or real report contents in tickets or chat.

## 2 — Immediate safe preflight (READ-ONLY)

Do not run these probes against an unexpected target; verify that the named PostgreSQL container is the authorized shared resource. No credentials are required for these commands beyond the operator's already-approved local Docker access.

~~~bash
# Confirm Docker target, availability and active PGDATA without reading data rows.
sudo -n docker ps --filter 'name=shared-postgres' --format 'table {{.Names}}\t{{.Status}}'
sudo -n docker exec --user postgres shared-postgres-postgres-1 psql \
  -X -v ON_ERROR_STOP=1 -d postgres -At -c 'SHOW ssl;'
sudo -n docker exec --user postgres shared-postgres-postgres-1 psql \
  -X -v ON_ERROR_STOP=1 -d postgres -At -c 'SHOW archive_mode;'
sudo -n docker exec --user postgres shared-postgres-postgres-1 psql \
  -X -v ON_ERROR_STOP=1 -d postgres -At -c 'SHOW data_directory;'
~~~

Capture only a redacted results summary. These checks DO NOT establish backup existence, actual TLS viability, restore success or client isolation.

## 3 — Backup method selection, with a firm stop condition

**No off-host destination confirmed:** STOP. Do not dump another project's database into /srv, a git checkout, temporary Docker volume, unrestricted bucket or shared vLLM directory. Ask the Storage/Ops owner to designate an independent, protected destination and approved encryption/key custody. A same-host filesystem with 360 GB free is not an adequate disaster-recovery substitute.

**Destination and rights confirmed:** Engineering/Ops must record the *allowed database set*, separate Data Owner consent, data classification, access and key management, backup operator identity, schedule, immutable/retention policy, agreed RPO/RTO and recovery test location **without exposing credentials or neighboring project identities in public repo**.

Choose based on approved objectives:
- **Logical per-database custom dump:** viable for modest-size databases when scheduled snapshot-style recovery is adequate; ensure schema/extension/ownership/roles/tablespace dependencies can be reconstructed. Do not dump all four databases or global role/password-verifier material without separate rights.
- **Physical backup + WAL archive:** required to evaluate genuine PITR, additional archive retention and monitoring; current `archive_mode=off` makes that path unavailable. Requires separate design/authorization and operational impact analysis. `full_page_writes=on` and `wal_level=replica` do not independently make PITR available.
- **Unapproved/unknown goals:** remain BLOCKED; neither method counts as a tested recovery policy.

A data-owner-authorized operator may later implement the chosen method in a separately reviewed change; **no runnable export/restore command for real shared databases is authorized by this document**.

## 4 — Required isolated Restore drill before any shared TLS change

The backup is not accepted until the authorized operator restores it in a **separate isolated PostgreSQL instance** using a separate writable test volume, approved isolated network and bounded CPU/RAM/disk budget; that instance must not be reachable by shared project clients. Use no customer reports unless explicitly approved.

Record only non-sensitive evidence:
1. Backup timestamp, approved scope, source PostgreSQL major version, encryption/access verification and manifest/checksum; do not publish secret hashes of passwords or row content.
2. Restore target version, full restore exit status, missing role/extension/ownership/permission errors and sanitized schema consistency checks; no write into the shared production PostgreSQL.
3. Recovery duration and data freshness compared with **approved** RTO/RPO; if targets unknown, status is BLOCKED rather than PASSED.
4. Scheduled retention and at least one independent/off-host encrypted recovery copy; test retrieving it rather than merely inspecting its existence.
5. Failure drill and documented rollback for the restoration environment only; never delete/overwrite shared PostgreSQL volumes or mount points.

A verified test restore of one permitted DB does not prove ability to recover all other projects, restore globals or replay WAL/PITR.

## 5 — Shared PostgreSQL TLS change proposal (NOT a run command)

**Pre-change** (Ops + Security + affected service owners): confirm REC-01..04, service dependencies, valid recovery checkpoint, maintenance approval, affected consumers, configured `pg_hba.conf` order, existing Compose file and volume mapping, read-only secret-mount behavior, approved CA lifecycle and monitored rollback.

**Certificate policy:** use an approved CA and server certificate whose DNS SAN covers `shared-postgres` (or an approved alternate actual Docker DNS hostname). Store private key outside Git, readable only by the PostgreSQL OS identity with PostgreSQL-compatible permissions; use read-only controlled mount. Do not use `ssl=verify-ca`, `sslmode=prefer`, hardcoded certificate bypasses or an untrusted self-signed certificate as a substitute for `verify-full`.

**Deployment mechanics:** existing cert/key were not readable. Creating new bind mounts can require recreating the existing shared PostgreSQL container and a planned service interruption; do not assert `pg_reload_conf()` alone can attach missing mounts. Plan first-connection and rollback probes for all actual consumers. The client application's production DSN continues to require `ssl=verify-full`.

**HBA policy for the new project:** use scoped `hostssl` SCRAM authentication for a dedicated DB/role and controlled originating network, with an earlier scoped `hostnossl` REJECT if the existing broad `host ... scram-sha-256` rule would otherwise allow plaintext fallback. Validate PostgreSQL first-match ordering. Do not edit other projects' HBA rules without their compatibility review. The client's `verify-full` additionally validates server identity; `hostssl` alone does not.

**Post-change acceptance (real and separately approved):** server reports `ssl=on`, verified peer identity and TLS connection from staging network, positive dedicated least-privilege auth, negative plaintext auth, no cross-database privilege, unaffected authorized existing clients, backup/rollback continuity and clean PostgreSQL health. A successful database-only `/health/ready` is not model readiness.

**Rollback:** approved prechange versioned Compose/config/cert/HBA inventory and safe reversion strategy must preserve the existing RW PGDATA volume and secrets; no `docker compose down -v`, `docker volume rm`, force reset or unreviewed shared restart. If change fails, halt API exposure and execute only the previously approved Ops rollback procedure; log each action and effect on consumers.

## 6 — Owner handoff and evidence checklist

| Check | Current state | Owner / checkpoint |
| --- | --- | --- |
| Authorized backup data scope | BLOCKED | Ops + each Data Owner / before any export |
| Off-host encrypted storage and key custody | UNKNOWN/BLOCKED | Ops + Security / before any export |
| RPO/RTO and backup frequency/retention | TBD/BLOCKED | Product + Ops / before choosing method |
| Last actual backup and isolated successful restore | NOT VERIFIED/NOT RUN | Ops / before shared TLS mutation |
| Shared client impact and approved maintenance/rollback | NOT VERIFIED/BLOCKED | Ops + other service owners / before TLS mutation |
| Trusted CA/private key/SAN and TLS server activation | BLOCKED | Ops + Security / before staging DB connection |
| Dedicated project database and role | BLOCKED | Ops + Security / before staging |
| PostgreSQL integration and app API container | NOT RUN | Engineering / once all preceding gates pass |
| Real classification model, privacy, Gold/OOD and UAT | BLOCKED/DEFERRED | Product/ML/Security/Employer / before Production acceptance |

**Do not confuse** independent suite PASSED or documentation prepared with P6-07 restore drill PASSED. P3/P4/P5 remain IMPLEMENTED_AWAITING_VERIFICATION; Phase 6 remains IN PROGRESS / RESTRICTED; PROJECT_PRODUCTION_READY_ACCEPTED remains BLOCKED.

## 7 — Authoritative references

- PostgreSQL 17 [Backup and Restore](https://www.postgresql.org/docs/17/backup.html)
- PostgreSQL 17 [SQL Dump](https://www.postgresql.org/docs/17/backup-dump.html)
- PostgreSQL 17 [pg_restore](https://www.postgresql.org/docs/17/app-pgrestore.html)
- PostgreSQL 17 [Secure TCP/IP with SSL](https://www.postgresql.org/docs/17/ssl-tcp.html)
- PostgreSQL 17 [pg_hba.conf](https://www.postgresql.org/docs/17/auth-pg-hba-conf.html)
