# P1-04 — Classification task and decision policy
**Decision:** OPEN / BLOCKED; owner: product + taxonomy owner with reviewer and ML sign-off.

## Decision alternatives
| Alternative | Contract and metric consequences | Recommendation for review |
|---|---|---|
| single-label | Exactly one primary predicted category at most; Macro-F1 per class, standard confusion matrix; ambiguous cases may NEEDS_REVIEW | Document plan uses as baseline hypothesis, NOT approved |
| multi-label | Predicted category set, threshold per label, ambiguous combinations, different DTO/schema and micro/macro multilabel metrics | Choose only if employer requires multiple independent labels |
| hierarchical | Parent/child constraints and additional model/output contracts | Out-of-scope unless taxonomy shows hierarchy requirement |

## Proposed separation of concepts
- predicted_category: model proposal, always from published taxonomy version; nullable when not supportable.
- final_category: approved organization decision; reviewer action and audit preserve differences.
- AUTO_CLASSIFIED: candidate satisfied calibrated decision policy and sufficient valid grounded evidence, *if automation is approved*.
- NEEDS_REVIEW: ambiguous, insufficient evidence, conflicting categories, novel/mixed reports or below threshold.
- OUT_OF_SCOPE: explicit supported judgment that report lies outside taxonomy; status, not category.
- Infrastructure failure: ERROR response, never OUT_OF_SCOPE or fabricated classified result.

## Case handling — proposed, not finalized
- Multi-topic report: if single-label approved, apply employer's dominant-topic rule or require human review; never arbitrarily choose the first mention. If multi-label approved, revise schema and benchmarks first.
- Ambiguous similar categories: preserve ranked candidates internally only when policy permits, require reviewer and record rationale.
- No fitting category / OOD: route to validated OOD policy or NEEDS_REVIEW; only report OUT_OF_SCOPE when validated operational criterion and owner approval support it.
- Long reports: full-document processing or evaluated chunk aggregation retaining original offsets; truncation without disclosed behavior is prohibited.
- Empty, oversized, invalid text: typed validation error; do not classify.
- Calibration unavailable: do not emit fabricated confidence; possible score or null per approved API.

## Required sign-offs
Product decides single/multi label and dominant-topic behavior; taxonomy manager supplies tie-breaking rules; ML provides evidence on thresholds/OOD; review owner defines action queue and escalation; security defines access to review contents. All numeric thresholds remain TBD and versioned only after validation.
