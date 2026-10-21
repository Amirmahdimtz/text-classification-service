# P1-11 — Security threat model (design stage)
**Scope:** HTTP ingress, identity, review, PostgreSQL, model runtime, training/evaluation, deployment, observability and public repository. **Status:** Proposed mitigations; security sign-off pending.

## Trust boundaries and assets
Client/untrusted report → authenticated FastAPI ingress → Application authorization → Core policy → isolated Infrastructure PostgreSQL/ML runtime. Admin/reviewer and offline training have distinct authorization boundaries. Sensitive assets: report text, evidence snippets, organizational taxonomy, reviewer identities, gold labels, model artifacts, credentials, API keys and audit records. Deployment security zone/residency is TBD.

## Threat and mitigation register
| Threat | Boundary / impact | Proposed control | Verification |
|---|---|---|---|
| Spoofed caller or leaked credentials | Anonymous access to confidential reports | approved AuthN (JWT/OIDC/mTLS TBD), short-lived credentials, rotation, fail closed | unauthenticated/expired token tests |
| Broken object-level authorization (IDOR) | Read report by guessing classification_id | tenant/report/assignment checks in Service/Repository access, deny-by-default | cross-tenant/cross-user negative tests |
| Privilege escalation | Submitter publishes taxonomy/model or claims review | least-privilege RBAC, role separation, audited dual approval for publish | role matrix negative tests |
| Prompt injection in report | Malicious text instructs explanation/LLM/runtime | treat report as untrusted DATA; evidence checks, structured outputs, do not execute instructions | adversarial report fixtures |
| Exfiltration by external inference/telemetry | Report/embedding leaves approved network | block outbound by default; explicit vendor/security approval; redaction | network egress and log review |
| Log/data leakage | Secrets/PII in traces, error responses, CI | structured redacted logs, strict allowlist metrics, sanitized errors, no raw text | log/trace snapshot tests |
| Request flooding, large payload, parser abuse | CPU/GPU exhaustion or API failure | byte/token limits, throttling, concurrency/timeout/backpressure, input validation | load and malformed/oversize tests |
| Tampered model/taxonomy or supply chain | Silent wrong decisions/data theft | signed/checksummed releases, restricted promotions, dependency scan, immutable manifests | artifact verification/rollback drill |
| DB injection or transaction race | Corrupted state or unauthorized changes | SQLAlchemy parameterized queries, transaction isolation, optimistic revision, scoped idempotency | concurrency/injection tests |
| Unauthorized dataset reuse / memorization | Privacy breach in training/evaluation | provenance/licensing control, isolated train access, release review, prevent raw public artifact | governance audit and leakage tests |
| Audit history tampering | Unable to reconstruct expert decisions | append-only events, restricted writes, integrity/backup controls | authorization and recovery tests |
| Secrets committed to public GitHub | Credential compromise | no secrets in examples, staged diff scan, repository scanning, revoke on incident | pre-commit and repo scan |
| Availability dependency failure | False success or business OUT_OF_SCOPE | model/DB readiness, classified infra errors 503/504, no silent downgrade | provider-down fault injection |

## Abuse controls and policy
- TLS in transit; at-rest encryption and key ownership TBD. Secret resolution through approved environment/Vault, never tracked YAML values.
- Authenticate identities before authorization; require scoped permissions for results and audit.
- Apply transport limits before heavy tokenization, resource quotas for inference, and defensive parsing; no stored user-supplied HTML execution.
- Preserve evidence offsets and original text mapping securely. Explanations must not manufacture facts or use untrusted text as command.
- Separate model training from serving; model artifact loading is controlled and not per HTTP request.
- Record correlation IDs rather than report text; restrict access to diagnostics with retention limits.
- Use sanitized test fixtures until real-data processing permission is documented.

## Open security gates
Security owner must sign AuthN protocol, identity/tenant mapping, encryption/key management, outbound ML policy, retention, deployment topology, incident response and security acceptance tests. Threat model requires re-review after API/model architecture decisions and before Production.
