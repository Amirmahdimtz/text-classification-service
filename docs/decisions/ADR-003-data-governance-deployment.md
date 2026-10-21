# ADR-003 — Data governance and inference deployment
**Status:** PROPOSED / NOT APPROVED
**Owners:** Security lead, data custodian and operations
**Context:** Political/organizational reports and model-derived evidence can be confidential. No legal basis, location or infrastructure facts provided.

## Options
A. Private/on-prem or segregated controlled inference under organization network and key policy (candidate when confidentiality demands).
B. Authorized private cloud within specified residency/network boundary (needs formal risk assessment).
C. External public hosted inference (NOT permitted without explicit contractual/data-owner approval and risk mitigations).

## Interim requirement
No real training/report data committed to public GitHub or transmitted to external model/telemetry provider. Traceable permitted purpose, redacted logging, secrets in approved secret store/environment, encrypted transport and scoped access. Retention/deletion and training permission are separate sign-offs.

## Open questions
Data categories, lawful basis, approved environments/vendor and service accounts, egress rules, keys, permitted anonymization, retention and audit policy. Phase 2 security integration and Phase 3 data work BLOCKED until approvals.
