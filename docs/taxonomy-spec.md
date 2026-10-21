# P1-03 — Taxonomy specification
**State:** SCHEMA_PROPOSED; category catalog BLOCKED until supplied and approved by employer / taxonomy owner.

## Category definition record
| Field | Meaning / validation contract |
|---|---|
| category_code | Stable unique organizational code; exact format and max length TBD |
| category_title_fa | Persian display title; non-empty, unique constraints within version TBD |
| definition | Positive semantic meaning, sufficiently discriminative |
| inclusion_criteria | Explicit inclusion rules linked to permitted evidence |
| exclusion_criteria | Exclusion rules including tricky confusable cases |
| positive_examples | Real, approved, legally usable and de-identified reference reports; none supplied |
| negative_examples | Reviewed close negatives; none supplied |
| boundary_notes | Pairs of similar categories and adjudication rules |
| lifecycle_state | draft / approved-published / retired proposal; final values require approval |
| version | Immutable taxonomy release identifier |
| stable_identity | Logical identity across versions; split/merge lineage must be recorded |
| effective_period | Effective/publish timestamp; clock/date semantics TBD |
| approvers / audit | Authorized approver(s), change reason and evidence |

## Workflow
1. Taxonomy manager receives employer-authored category records and applicable labeling policy.
2. Validate uniqueness, non-empty definitions, contradictory inclusion/exclusion, and overlaps; circulate boundary-case examples to reviewers.
3. Independent experts annotate sampled reports; adjudication lead records disagreements and resolves definition gaps.
4. Product + taxonomy owner approve a frozen release; never mutate a published semantic definition in place.
5. Classification must reference an immutable taxonomy_version and a category valid in that release. Historical results keep their original version.
6. For rename, split, merge or retire: write compatibility map and impact analysis; retrain/re-evaluate and approve publication; do not silently rewrite prior classifications.

## Versioning invariants
- Codes must not be recycled for unrelated semantic concepts; version + identity resolves historical meaning.
- A result cannot claim a Category absent/inactive for the chosen release.
- Different releases cannot be assumed label-equivalent; explicit approved mapping needed for benchmark comparisons.
- Published version edits require new release; retirement is not physical deletion of audit history.

## Acceptance package (currently missing)
Approved real category list, definitions, two-sided examples, boundary decisions, active/retired state, category ownership, version identifier, authorized signature, multi-topic examples and representative class distribution. No artificial categories are approved.
