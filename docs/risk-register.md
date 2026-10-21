# P1-12 — Risk register and decision dependencies
**Reviewed:** 2026-10-21 | **Status:** Active; severity qualitative until organization risk scoring approved.

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

**Escalation:** Critical BLOCKED items prevent Phase 1 full acceptance or production-facing implementation. Deferral to later phases is documented dependency, never an implicit waiver. Risk owner and approval evidence must be recorded in phase-status and ADRs.
