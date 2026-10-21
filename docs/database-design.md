# P1-08 — PostgreSQL persistence design and conceptual ERD
**Status:** PROPOSED conceptual schema only. No actual SQLAlchemy classes, Alembic revision, SQL DDL or tables in Phase 1.
**Mandatory execution design:** Controller → Service → Repository → PsqlDbContext; shared AsyncEngine/sessionmaker, short-lived AsyncSession, no multi-operation commit leakage.

## Entities and relationships
~~~mermaid
erDiagram
    TAXONOMY_VERSIONS ||--o{ CATEGORIES : defines
    REPORTS ||--o{ CLASSIFICATION_RESULTS : receives
    MODEL_RELEASES ||--o{ CLASSIFICATION_RESULTS : generated_by
    TAXONOMY_VERSIONS ||--o{ CLASSIFICATION_RESULTS : version_for
    CLASSIFICATION_RESULTS ||--o{ CLASSIFICATION_EVIDENCE : substantiates
    CLASSIFICATION_RESULTS ||--o{ CLASSIFICATION_REVIEWS : amended_by
    REPORTS ||--o{ AUDIT_EVENTS : concerns
    CLASSIFICATION_RESULTS ||--o{ AUDIT_EVENTS : audited
~~~
Audit events can also target taxonomy/model publish actions without report or result; diagram edges represent optional conceptual linkage, not non-null foreign keys.

| Entity | Core conceptual fields / constraints |
|---|---|
| taxonomy_versions | immutable version string, status, publish/effective timestamps, approved_by reference, unique version |
| categories | taxonomy_version FK, stable category identity/code, title, criteria, examples metadata, lifecycle; unique(version, code) |
| reports | stable report ID, principal/tenant access scope, original text or protected storage reference, metadata allowlist, retention state, timestamps |
| model_releases | release ID, model/tokenizer/preprocess/policy versions and hashes, taxonomy compatibility set, evaluation fingerprint, state |
| classification_results | unique result ID, report FK, taxonomy_version FK, model_release FK, predicted category with matching taxonomy, status, score semantics, policy version, timestamps, idempotency scope/fingerprint, logical revision |
| classification_evidence | result FK, original-text half-open span, evidence quote or protected reference, provenance, criterion mapping, offset convention/version |
| classification_reviews | result FK, reviewer principal reference, previous/new decision, reason, revision, created_at; append-only business audit |
| audit_events | actor, principal scope, action, target/ref, decision outcome, timestamp, sanitized metadata and immutable history |

Possible separate principal/role storage is deferred pending organization Identity Provider. Category references may require composite FK (taxonomy_version,category_code), not a cross-version bare code. Datatypes (UUID/ULID), sizes, indexing, FK cascade, soft/hard erase, partitions and storage encryption remain TBD after approved retention/schema.

## Cross-entity invariants
1. An accepted classification's taxonomy version matches its selected category definition and model release compatibility.
2. Original prediction and release manifest remain immutable when reviewer changes final decision; amendments are appended and revision advanced atomically.
3. Evidence start/end refer to the original report version and are validated before persistence.
4. Tenant and record visibility enforced in authorized repository query path; no ID-based bypass.
5. Audit events are minimized and never store full sensitive report content by default.
6. Idempotency scope uniqueness depends on authenticated tenant/principal, endpoint, key and payload fingerprint under approved retry window.

## Transaction boundaries
- One atomic DB transaction persists report reference (as required), classification result, all evidence, scoped idempotency entry and audit event. Either COMMIT all or ROLLBACK all.
- Reviewer decision: optimistic revision check + review append + final category update + audit append in ONE transaction. Conflict returns typed 409; no last-write-wins.
- Taxonomy publication: verify completeness and approval, transition version and audit atomically; immutable released versions.
- BaseRepository CRUD may commit independently and MUST NOT be chained to simulate multi-row atomicity; implement a feature-specific transaction method under Infrastructure using one AsyncSession.
- Inference execution occurs outside long DB-held transactions; at publication time verify active release compatibility and deterministic idempotency/retry semantics.
- Backup/restore/retention must preserve audit referential history within legal constraints.

## Migration and acceptance strategy
Phase 2: implement approved minimum schema using actual repository SQLAlchemy Base and Alembic metadata imports; add FK, UNIQUE, CHECK and indexes, test clean upgrade and migration drift in isolated PostgreSQL; test rollback method safely on disposable DB. Any destructive data migration needs explicit approval and recovery plan. No schema created here.
