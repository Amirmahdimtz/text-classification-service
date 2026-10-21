# P1-05 / P1-11 — Data governance and privacy
**State:** PROPOSED safeguards; organizational Data Classification, data owner approval and geographic residency BLOCKED.

## Data inventory and classification (owner must confirm)
| Asset | Candidate sensitivity | Storage/transmission principles | Approval needed |
|---|---|---|---|
| Original report text and attachments (if approved later) | Potentially sensitive/confidential political reporting | least privilege, encrypted transport/at rest according to policy, restricted access | actual classification and lawful purpose |
| Annotated labels and expert decisions | Sensitive derived data; linkage can reveal source | access-bound, immutable provenance, authorized audit | authorized reviewers and retention |
| Inference evidence and explanations | Derivative excerpts may be equally sensitive | minimize and permission-check; do not log text | data owner + reviewer |
| Dataset manifests/split identifiers | Metadata may be linkable | hashed identifiers with access controls; never publish raw case IDs | dataset custodian |
| Metrics/traces/logs | Operational, potentially linkable | no raw report/PII/secret as label or event | security/operations |
| Model artifacts | May encode sensitive training information | controlled artifact storage, fingerprints, release approvals | data/security + ML |

## Purpose and rights
- Processing purpose: report classification and auditable human review. Training, fine-tuning, evaluation, export, analytics and vendor processing are separate purpose/permission decisions.
- Explicit documented legal basis, controller/custodian, organizational security classification, residency, permissible source datasets and onward transfer approval required before ingesting real text.
- Default posture: DO NOT export confidential text, labels, embeddings or fragments to third-party inference/telemetry services without signed permission and vendor/security review. Private/on-prem runtime is a candidate, NOT approved topology.
- No sensitive report, dataset, credential, token, sample, file-based export or heavyweight model artifact in public GitHub, CI logs or example API schemas.

## Lifecycle and retention (pending approvals)
1. Ingest only fields on data contract allowlist and authorized owner scope.
2. Store report body and evidence only as needed for traceability under approved encryption/access controls; minimize duplication.
3. Log structured IDs and sanitized event metadata. Enforce retention/deletion on all copies, caches, annotations, backups and derived artifacts as feasible/legal.
4. Create documented delete vs legal-hold policy; reconcile deletion with immutable audit by retaining minimal sanitized decision metadata where lawful.
5. Backup storage, access, key rotation, cross-region transfer, anonymization, redaction and incident response must match organizational policy.
6. Access reviews, revoke offboarded identities, record data processing changes. Include service accounts and DB principals.

## Required decisions
| ID | Question | Owner | If unresolved |
|---|---|---|---|
| GOV-01 | Data classification, report contents, data owner and legal basis | Employer/data owner | No real input processing |
| GOV-02 | Approved development/training/evaluation/test sources and extraction permission | Data owner/security | Phase 3 blocked |
| GOV-03 | Residency, permitted network egress and external ML inference | Security/operations | No external transmission |
| GOV-04 | Retention and deletion schedule incl. immutable audit and backup | Data governance/legal | Persistence design non-final |
| GOV-05 | Authorized roles, tenant boundaries, redaction and exception handling | Security/product | API/RBAC non-final |
| GOV-06 | Allowed usage of reviewer corrections for retraining | Product/data owner | No automatic retraining |
| GOV-07 | Incident response, notification obligations and contact | Security/operations | Production release blocked |

## Verification plan
Review data-flow map; integration tests for role/scope, export prevention, log redaction, retention/deletion, access expiry, backup policy and egress policy in controlled environments. Phase 1 has no real data or services to execute these tests.
