# P1-07 — API v1 contract proposal
**State:** PROPOSED, not approved OpenAPI or an implemented endpoint. Applies only if single-label and the reference auto-discovery convention are confirmed.
**Base prefix:** WebService mounts /api/v1/{feature}; Controller.api() must not duplicate it.

## Proposed endpoints and authorization
| Method | Final logical path (proposed) | Scope | Responses |
|---|---|---|---|
| POST | /api/v1/text_classification/classify | submitter within authorized report scope | 200 result; typed 4xx/5xx |
| GET | /api/v1/text_classification/{classification_id} | record-scoped read (owner, assigned reviewer) | 200 / 403 / 404 |
| GET | /api/v1/taxonomy/categories | read published taxonomy allowed for caller | 200 |
| POST | /api/v1/review/submit | assigned reviewer + case permission | 200 / 403 / 409 |
| Admin publishing | ROUTE TBD after management design approval | taxonomy/model managers, separate approvals | NOT FINAL |

## Candidate request DTO semantics (not deployed)
ClassifyReportRequestDto:
- report_id: string? — optional client stable id; format/max TBD; never an authorization token.
- report_text: string — required, not blank; max bytes/codepoints TBD, validate both.
- taxonomy_version: string? — published version or approved pinned default; no implicit model mismatch.
- metadata: typed allowlist? — schema TBD; reject arbitrary personal fields.
- idempotency: in a validated Idempotency-Key header? — exact location and TTL subject to approval.
- request_id: server-generated correlation identifier; trusted inbound propagation only through safe allowlist.

ClassifyReportResponseDto:
- classification_id: string; report_id: string; request_id: string; status: enum proposed AUTO_CLASSIFIED | NEEDS_REVIEW | OUT_OF_SCOPE.
- predicted_category: {code:string, title:string} | null; final_category: {code:string,title:string} | null.
- score: {kind: CALIBRATED_PROBABILITY | RAW_MODEL_SCORE, value:number, calibration_version:string?} | null, with limits/meaning per kind documented. Prefer null to misrepresent score.
- evidence_spans: array {start:int, end:int, text:string, related_criterion_id:string?}; all spans must satisfy original_text[start:end] == text under adopted convention; empty when unsupported.
- explanation: string? — grounded only; no fabricated reason.
- model_version, taxonomy_version, preprocessing_version, decision_policy_version, tokenizer_version, release_manifest_digest: strings as applicable and never fake; version compatibility checked.
- reviewed_by, reviewed_at / decision history: **excluded from public classify response until data/minimization decision**.

ReviewSubmitRequestDto (proposal): classification_id, decision (approve | correct | escalate), final_category_code when applicable, reason, expected_version/ETag for optimistic concurrency, idempotency key. Preserve original prediction; reviewer identity comes from AuthN, not request payload.
TaxonomyCategoryResponseDto (proposal): code, title, definition, inclusion/exclusion criteria where authorized, taxonomy_version, active flag, effective date. Published categories only.

## Status semantics
AUTO_CLASSIFIED: validated business decision meeting category evidence/score policies, not a transport success synonym.
NEEDS_REVIEW: unresolved/inadequate category or evidence; does not imply model failure.
OUT_OF_SCOPE: governed taxonomy mismatch decision, never a fake fallback for runtime outage. This is NOT a category.
Model/DB timeout or unavailable: typed 5xx, not any classification status. predicted_category and final_category nullable; final_category is a separately auditable conclusion.

## Proposed error envelope
JSON error: {error: {code: string, message: string, request_id: string, retryable: boolean, details: object?}}. Never include raw report, stack trace, secret or unredacted subject identifiers.
| HTTP | Candidate code | Condition |
|---|---|---|
| 400 | MALFORMED_REQUEST | bad syntax/invalid correlation header |
| 401 | UNAUTHENTICATED | no valid authentication |
| 403 | FORBIDDEN | role/scope denies action |
| 404 | RESULT_NOT_FOUND / TAXONOMY_NOT_FOUND | no authorized visible resource; avoid existence oracle |
| 409 | REVIEW_VERSION_CONFLICT / IDEMPOTENCY_CONFLICT / TAXONOMY_VERSION_CONFLICT | optimistic lock, replay mismatch, version conflict |
| 413 | PAYLOAD_TOO_LARGE | validated ingress size ceiling |
| 422 | VALIDATION_ERROR | empty/invalid type/field/value |
| 429 | RATE_LIMITED | caller exceeds policy; safe Retry-After where applicable |
| 500 | INTERNAL_ERROR | unexpected infrastructure issue without exposing internals |
| 503 | MODEL_UNAVAILABLE / DATABASE_UNAVAILABLE | dependency unavailable; no silent downgrade |
| 504 | MODEL_TIMEOUT | inference timeout where gateway semantics apply |

Exact status mappings, async job support, response model fields, error naming, auth mechanism and codes require API/security/product approval. 404 vs 403 policy is security-specific.

## Idempotency and concurrency (proposed)
- Namespace a key by authenticated tenant/principal, endpoint, approved report identity and request payload fingerprint. Never use global unscoped keys.
- Exact replays return same persisted result if within TTL; conflicting payload under same scoped key yields 409.
- Enforce atomic unique token and result creation; for in-flight duplicate concurrency, serialize/wait or deterministic retriable conflict. No duplicate review/audit records.
- Review updates require expected revision (optimistic concurrency), immutable review event and permission recheck.
- TTL, storage and response-on-retry after model-version change are open owner decisions. Distinguish transient infrastructure retry from classification policy.

## API lifecycle / OpenAPI
- Contract first: after sign-off, realize with Pydantic v2 DTOs under application/{feature}/dtos, thin FastAPI Controller and explicit schema examples with NO real data.
- Verify generated OpenAPI response/error mapping, version headers, JSON UTF-8, authorization, 413/422 boundaries, idempotent retries and strict version compatibility.
- No implemented FastAPI application or emitted OpenAPI JSON exists in Phase 1; OpenAPI integration tests are planned Phase 5.
- Breaking v1 DTO/route changes require new version / employer approval and backwards-compatibility tests.
