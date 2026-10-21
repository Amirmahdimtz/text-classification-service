# P1 — Product requirements and acceptance traceability
**Status:** DESIGN_PROPOSED / owner review required. **Scope:** دسته‌بندی گزارش‌های متنی در Taxonomy مصوب همراه با استدلال مبتنی بر شاهد؛ محصول نهایی Production-grade است، نه Demo.

## Boundaries
درخواست معتبر می‌تواند متن گزارش و metadata مجاز را منتقل کند؛ نتیجه باید Category قابل رهگیری، وضعیت تصمیم، شواهد دقیق از متن اصلی، نسخه‌های اثرگذار و تاریخچه بازبینی را حفظ کند. زبان فارسی/مختلط فرض ارزیابی است نه قرارداد تأییدشده. Multi-label، تحلیل احساسات، تولید خبر، topic modeling آزاد و پیش‌بینی مواضع افراد بدون درخواست رسمی خارج از دامنه‌اند.

## Roles and RBAC — proposal, not authorization policy
| Capability | Submitter | Reviewer | Taxonomy manager | Model manager | Service admin |
|---|---|---|---|---|---|
| Submit report / view own permitted result | Own-scope | Assigned-scope | No by role alone | No by role alone | Operational access only |
| Claim/review/correct category | No | Assigned-scope | No by role alone | No | No by role alone |
| Read published taxonomy | Yes | Yes | Yes | Yes | Yes |
| Draft/publish/retire taxonomy | No | No | Yes + dual approval for publish | No | No |
| Validate/promote/rollback model | No | No | No | Yes + controlled approval | Operate approved deployment only |
| Manage service config/incident | No | No | No | No | Yes (least privilege) |
| Read audit | Own events when allowed | Assigned actions | Taxonomy events | Model events | Security-approved scope |

A user may hold multiple roles only through audited identity mapping. All record-level access requires report/tenant scope checks; knowing an ID does not grant access. Service-to-service identities, tenant isolation, approval separation and exact authorization claims remain TBD (owner: security + product).

## Functional requirements
| ID | Requirement | Priority | Accountable owner | Verification | Status |
|---|---|---|---|---|---|
| FR-01 | Validate input report, identifiers, text and metadata | Must | Product/API | DTO boundary + negative contract tests | Proposed |
| FR-02 | Versioned, active/inactive approved categories | Must | Product/Taxonomy | lifecycle and compatibility tests | BLOCKED taxonomy |
| FR-03 | Reversible Persian preprocessing preserving evidence offsets | Must | ML | Unicode/offset fixtures | Proposed |
| FR-04 | Predict only a category in selected published taxonomy | Must | Product/ML | category/version mismatch tests | BLOCKED taxonomy |
| FR-05 | Explicitly typed score; no uncalibrated probability | Must | ML | calibration checks and response schema | Proposed |
| FR-06 | Separate auto/review/out-of-scope decisions | Must | Product/Review | boundary/OOD policy tests | BLOCKED decision |
| FR-07 | Grounded explanation with validated source spans | Must | ML/Review | quote fidelity and human assessment | Proposed |
| FR-08 | Persist, retrieve and trace result/version/evidence | Must | Engineering | PostgreSQL transaction/access tests | Proposed |
| FR-09 | Human review and immutable correction history | Must | Review owner | concurrent reviewer and audit tests | Proposed |
| FR-10 | Reproducible model/taxonomy/policy/preprocess versions | Must | ML/Engineering | manifest/hash compatibility tests | Proposed |
| FR-11 | Authenticated/authorized versioned API and safe retry | Must | API/Security | OpenAPI + AuthZ + idempotency tests | BLOCKED approvals |
| FR-12 | Monitor system outcomes and verified review feedback | Must | Ops/ML | metrics/logging redaction checks | Proposed |
| FR-13 | Evaluated, approved, rollback-capable releases | Must | Model manager | staged promotion/rollback test | BLOCKED infrastructure |

## Non-functional requirements
| ID | Subject | Priority | Accountable owner | Verification | Status |
|---|---|---|---|---|---|
| NFR-01 | Macro-F1 / per-class quality on independent gold | Must | Product/ML | frozen test evaluation | BLOCKED target/data |
| NFR-02 | p50/p95/p99 latency for realistic documents | Must | Operations | representative load measurement | BLOCKED SLO |
| NFR-03 | Throughput, concurrency, size and batch envelope | Must | Operations/Product | capacity tests | BLOCKED envelope |
| NFR-04 | Failure handling, timeout, resilience, no false success | Must | Engineering/Ops | DB/model-down fault injection | Proposed |
| NFR-05 | AuthN, AuthZ, TLS, secrets, audit, rate limiting | Must | Security | penetration/negative/security tests | BLOCKED policy |
| NFR-06 | Classification, retention, deletion and export policy | Must | Data owner | governance and erasure tests | BLOCKED policy |
| NFR-07 | Release and dataset fingerprint reproducibility | Must | ML/Engineering | replay/version/hash audit | Proposed |
| NFR-08 | Migration, backup, recovery and rollback | Must | Ops | isolated restore/recovery drill | BLOCKED RPO/RTO |
| NFR-09 | Readiness, metrics, trace and request correlation | Must | Ops | failure readiness and redacted log tests | Proposed |
| NFR-10 | Versioned backwards compatibility / taxonomy evolution | Must | Product/Engineering | release compatibility tests | BLOCKED taxonomy |

## Acceptance evidence and traceability
- Detailed subcontracts: taxonomy-spec, classification-policy, data-contract, annotation-guideline, api-contract, database-design, model-evaluation-plan, quality-slo, security-threat-model and data-governance.
- Documents and examples are proposals until reviewed; no field widths, targets or sample categories are official.
- Review packet must include taxonomy examples, task-policy selection, approved data usage, API/RBAC, evaluation targets, infra/security and owner sign-off. See phase-status for exact outstanding decisions.
