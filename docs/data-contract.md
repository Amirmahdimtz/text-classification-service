# P1-05 — Report input, quality and evidence contract
**Status:** PROPOSED; limits, data classes and permitted metadata pending product/data security owners.

## Logical report request
- report_id: client stable identifier or server generated identifier, uniqueness scope/format TBD.
- request_id / correlation_id: generated/propagated per request; must not include sensitive data.
- report_text: required, non-empty Unicode text; JSON over UTF-8; trim only for validation and never silently mutate original report.
- source, event_time, locale/language, organization or tenant scope: optional candidate metadata, inclusion requires actual business need and privacy approval.
- taxonomy_version: explicit published version or explicitly agreed server pinned default; never silently select incompatible release.
- idempotency_key: optional/proposed request-scoped retry key; privacy-neutral random token; scope and TTL TBD.
- provenance and consent/legal_basis: references handled in governance, not unrestricted client-supplied authority.
- attachments, OCR, PDFs and bulk upload: out-of-scope for v1 proposal until requested.

## Validation and representation
| Area | Required contract / unresolved parameter |
|---|---|
| Serialization | JSON UTF-8; reject invalid encoding/type and malformed JSON |
| Empty | Reject null, whitespace-only, zero meaningful characters; normalize only for assessment |
| Size | Maximum bytes, Unicode code points, and token/chunk budget = TBD after corpus and capacity |
| Identifiers | Allowed format, collision policy, tenant uniqueness = TBD; reject path traversal/control characters |
| Language | Persian with Latin/mixed-script tests as candidate baseline; actual permitted languages = TBD |
| Timestamps | ISO 8601 offset-aware candidate; timezone convention = TBD |
| PII | Sensitive fields and access scope require data-owner classification |
| Quality | Duplicate and near-duplicate handling, OCR errors, mixed reports, boilerplate and truncated inputs logged as quality flags without exposing text |

## Evidence integrity
Original immutable text (subject to retention) is source of truth. Preprocessing must record reversible mapping to original text positions. Proposed evidence convention: Unicode code-point, zero-based, half-open [start,end), validated by original_text[start:end] == evidence_text; for API offsets final convention needs approval. Redaction in storage/external views must not invalidate audit-traceable offsets without a documented versioned transform.

## Consent, lifecycle and access
No real report sample has been supplied; data use for training/evaluation, transfer, storage duration, deletion and processing locality remain BLOCKED. Client cannot override authorization by setting owner/tenant metadata. See data-governance and security-threat-model.
