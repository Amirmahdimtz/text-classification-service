# ADR-018 — Shared PostgreSQL recovery assurance before TLS rollout

**Status:** PROPOSED / DOCUMENTATION-ONLY — not an authorized shared-service change (2026-10-28).
**Phase:** Phase 6, restricted independent P6-12 documentation under [ADR-014](ADR-014-phase6-conditional-technical-entry.md); P6-07 real backup/restore drill remains BLOCKED.
**Related:** [ADR-017](ADR-017-shared-server-staging-boundary.md), [Recovery and TLS operations runbook](../runbooks/phase6-shared-postgres-backup-tls.md), [Phase 6 ledger](../phase-6-execution.md).

## Verified observations versus unknowns

Owner-provided read-only SSH evidence on Ubuntu 24.04.1 reports shared PostgreSQL 17 `shared-postgres-postgres-1`, Docker network `simorgh-db-net` with four attached containers; exact IPv4/IPv6 loopback-only HBA TCP `trust` rules and final all-network `scram-sha-256` rule; host port 5432 NOT_PUBLISHED; PostgreSQL listening on all container interfaces. The live `ssl` setting is **off**, and configured server TLS cert/key files were **MISSING_OR_UNREADABLE** for OS user `postgres`. The cluster has a writable Docker volume at `/var/lib/postgresql/data` and a read-only password-secret mount; do not reveal secret contents.

Owner's aggregate query found **4 connectable non-template databases totaling 38 MB** and **360 GB free on the same host filesystem** at the observation time. `archive_mode=off`, `archive_timeout=0`, `wal_level=replica`, `full_page_writes=on`; no current WAL archiver success recorded. A generic timer named `dpkg-db-backup` is *not* a PostgreSQL backup. Limited service/cron filename searches yielded no PostgreSQL backup evidence. Independent backups/snapshots, off-host storage, approved RPO/RTO, scheduled retention and a successful isolated restore are all **NOT VERIFIED**, not proven absent.

## Decision and alternatives

1. **Chosen for design, not execution:** keep the existing shared PostgreSQL architecture, prepare an owner-approved backup/recovery plan and actually prove an isolated restore **before** changing shared PostgreSQL TLS. After change approval, install a trusted server certificate with a valid `shared-postgres` DNS SAN, protect private keys outside Git, verify PostgreSQL is TLS-enabled and validate client `ssl=verify-full` and project-specific DB/role isolation. Shared vLLM and other project containers must remain untouched.
2. **Candidate A — authorized logical backup per database:** consider `pg_dump` custom-format with protected required role/tablespace metadata, independent encrypted off-host copy, retention and restore drill, **only if** Ops/Data Owner approve the actual scope and recovery objectives tolerate loss since the last successful backup. A logical dump does not offer continuous PITR or a proven cluster-wide instant.
3. **Candidate B — physical base backup + continuous WAL archiving/PITR:** assess if RPO/RTO or operational needs demand point-in-time recovery. Current `archive_mode=off` does **not** support that recovery path; new configuration, storage lifecycle, monitoring and possibly a coordinated restart would require separate approval. No ad hoc WAL-setting changes are permitted.
4. **No independent off-host storage:** the shared-service TLS change remains **BLOCKED**. A temporary encrypted local copy, if independently authorized for investigation, does not satisfy protection against host/disk loss and is not an accepted substitute for off-host recovery.
5. **Alternate PostgreSQL instance:** reconsider if shared-database maintenance or isolation is unacceptable to other projects; requires a separately approved resource/security/deployment plan. Do not silently instantiate a second DB.

## Mandatory approvals and acceptance evidence

| Gate | Required evidence | Owner and deadline |
| --- | --- | --- |
| REC-01 | Scope/rights for data of each project sharing PostgreSQL; permitted backup operator and confidentiality/access classification | Data Owners + Security; before any extraction |
| REC-02 | Approved RPO/RTO and policy for backup method, encryption, protected keys, retention, off-host destination and resource budget | Ops + Security + Product; before backup |
| REC-03 | Actual backup success, cryptographic inventory without secrets, independent off-host copy and successful **isolated restore**, including required roles/schema/application compatibility | Ops + Data Owner; before shared TLS change |
| REC-04 | Inventory of dependent clients, maintenance window, expected downtime, last-known-good Compose/config and tested rollback preserving volumes/data | Ops + service owners; before shared TLS change |
| TLS-01 | Trusted CA, valid server cert DNS SAN, private-key filesystem permissions, verified `ssl=on`, actual client `verify-full` handshake, non-TLS rejection for new project's DB/role and rollback evidence | Ops + Security; before staging DB connection |
| RELEASE-01 | Dedicated least-privilege staging database/role, reviewed immutable image, model/business/privacy gates and employer approval | Engineering + Product/ML/Security/Ops; before Production acceptance |

**Status:** All REC-01..04 remain NOT VERIFIED/BLOCKED; TLS-01 remains BLOCKED due to SSL off and missing/unreadable materials. This document does not approve `pg_dump`, snapshot, role/DB creation, certificate generation, `pg_reload_conf`, Docker recreation or Production deployment. Existing P3/P4/P5 phase markers and ADR-014 restricted Phase 6 authorization remain unchanged; `PROJECT_PRODUCTION_READY_ACCEPTED` is BLOCKED.

## References

- PostgreSQL 17 [Backup and Restore](https://www.postgresql.org/docs/17/backup.html)
- PostgreSQL 17 [SQL Dump](https://www.postgresql.org/docs/17/backup-dump.html)
- PostgreSQL 17 [Secure TCP/IP Connections with SSL](https://www.postgresql.org/docs/17/ssl-tcp.html)
- PostgreSQL 17 [Client Authentication and pg_hba.conf](https://www.postgresql.org/docs/17/auth-pg-hba-conf.html)

## Off-host storage selection checkpoint (2026-10-28)

Owner read-only host inspection showed no known remote FS mounts and no `restic`, `rclone`, `aws`, `pgbackrest` or `barman` executable in the invoking PATH. This means backup tooling/destination is **not confirmed on this host**, not that external storage or independently managed backups do not exist. **Proposed preferred candidate:** HTTPS S3-compatible external Object Storage with a client-encrypted restic repository and separately protected credentials/keys, subject to Ops/Data Owner/Security provider/data-jurisdiction approval and HTTPS reachability. This supplements—not replaces—PostgreSQL-consistent dumps and genuine isolated restore verification. If off-host endpoint, custody and authorization cannot be supplied, **REC-02/03 BLOCKED**; do not substitute the shared server's 360 GB free space as disaster recovery. No provider chosen, tools installed or data copied; phase status unchanged.
