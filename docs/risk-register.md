# P1-12 — Risk register and decision dependencies
**Reviewed:** 2026-10-24 | **Status:** Active; severity qualitative until organization risk scoring approved.

| ID | Risk / impact | Severity | Decision owner | Mitigation or evidence required | State |
|---|---|---|---|---|---|
| R-01 | No approved taxonomy → impossible valid label contract | Critical | Employer / taxonomy owner | category definitions, boundary positives/negatives, version and signature | BLOCKED |
| R-02 | No permitted gold/train reports → cannot evaluate/train honestly | Critical | Data owner + ML | documented lawful dataset, quality review, frozen split | BLOCKED |
| R-03 | Duplicate cases across splits → overstated quality | High | ML lead | group/time leakage audit and fingerprints | OPEN (Phase 3) |
| R-04 | Long/atypical Persian reports → lost evidence and latency | High | ML + product | length profiling, offset-preserving chunk benchmark | OPEN (Phase 3) |
| R-05 | Uncalibrated scores → confidently wrong auto labels | High | ML + product | calibration/coverage/risk policy, nullable score | BLOCKED targets |
| R-06 | Unsupported explanations → audit/credibility failure | High | ML + review owner | original span validation, human groundedness test | OPEN (Phase 4) |
| R-07 | Sensitive political reporting exfiltration | Critical | Security + data owner | classification, private boundary, approval, egress/redaction tests | BLOCKED |
| R-08 | In-place taxonomy/model edits → unrepeatable decisions | High | Taxonomy/model managers | immutable versions/manifests, release rollback | OPEN |
| R-09 | No inference resources/capacity targets → downtime and overload | High | Ops + employer | deployment topology, RPS/SLO, GPU/CPU budget and load tests | BLOCKED |
| R-10 | DI/Discovery mistakes in unimplemented architecture | Medium | Engineering | build convention-based skeleton Phase 2; import/DI test | OPEN (Phase 2) |
| R-11 | Multi-row commits / reviewer race → partial or lost history | High | Engineering + review owner | single atomic transaction, scoped idem, optimistic lock | OPEN (Phase 2/4/5) |
| R-12 | No signed numeric acceptance goals → no defensible release | Critical | Employer + product/ML/Ops | per-class, coverage, availability, latency targets | BLOCKED |
| R-13 | Single/multi-label remains unapproved → breaking API/model design | Critical | Product + employer | decision on case policy and annotation units | BLOCKED |
| R-14 | Retention and deployment geography unapproved → legal/operational uncertainty | Critical | Security + data governance | GOV-01..07 signoff | BLOCKED |
| R-15 | Public repository leakage via fixtures or docs | High | Engineering + security | no real data, credential scan before publish; minimize examples | MITIGATED DESIGN, continuous |
| R-16 | Real model quality or runtime failures discovered late under Local-First | High | ML lead + project owner + operations | Evidence debt ledger and early testing when approved, mandatory Phase 6 closure | OPEN / PHASE 6 |

**Escalation:** Critical BLOCKED items prevent Phase 1 full acceptance or production-facing implementation. Deferral to later phases is documented dependency, never an implicit waiver. Risk owner and approval evidence must be recorded in phase-status and ADRs.


## Phase 3 risk review (2026-10-21)

- R-01/R-02/R-12/R-13/R-14: critical unresolved employer-controlled taxonomy, data rights, quality target, label cardinality and confidential-data policy. BLOCKED; owner employer/product/data-security.
- R-03: code now clusters grouped reports and exact/candidate near duplicates and rechecks split disjointness; **residual semantic leakage risk HIGH**, expert case-level audit and Gold freeze BLOCKED; owner ML/data.
- R-04/R-05: no observed length distribution or validated calibration; code preserves long text and does not invent confidence; real latency/threshold evidence BLOCKED; owner ML/ops.
- R-07/R-15: derived model JSON vocabulary can expose sensitive character sequences; release and dataset must remain private; offline CLI forbids output under repo and Git ignore protects common private artifact types. Full authorized exfiltration audit remains BLOCKED.
- R-08/R-09: artifact/evaluation SHA-256 and version checks, bounded warmup provider implemented; actual secure registry, signature, real load/performance, rollback BLOCKED; owner ops/security.
- R-10: Phase 3 provider discovery and existing Phase 2 DI/CI regressions reviewed; future controller/production inference connection NOT IMPLEMENTED (depends on auth/API contract).

## Local-first risk update (2026-10-24)

- R-03: Temporal group-boundary overlap was corrected and checked with two new synthetic regressions in [CI 40077902341](https://github.com/Amirmahdimtz/text-classification-service/actions/runs/40077902341). Real semantic duplicate, group/time audit remains BLOCKED without authorized data. **Owner:** ML lead and data owner; **review deadline:** by Phase 6, preferably before training.
- R-16: Gold/OOD/model benchmarks, calibration, actual groundedness, model E2E, load and rollback remain DEFERRED/NOT RUN. **Owners:** ML, employer/product, security and operations; **prerequisites:** approved taxonomy, lawful dataset, model/server and agreed quality targets; **deadline:** Phase 6 acceptance. See [phase-status ledger](phase-status.md).
- Local-first conditional progression is scope-limited by [ADR-010](decisions/ADR-010-local-first-and-conditional-phase-progression.md). Critical schema/AuthN/privacy/taxonomy decisions remain BLOCKED where applicable.
