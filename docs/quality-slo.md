# P1-10 — Quality, SLO and measurement contracts
**Status:** Definitions proposed; ALL numerical acceptance thresholds TBD / BLOCKED pending owners, sample size and hardware.

## Metric definitions and ownership
| Metric | Operational definition and population | Owner / acceptance gate |
|---|---|---|
| Macro-F1 | Mean of per-category F1 on untouched labeled gold set; declare undefined/zero-division conventions and missing classes | ML + product: target TBD |
| Per-class precision/recall/F1 | TP/(TP+FP), TP/(TP+FN), harmonic mean with support and confusion matrix | Category owner + ML: per-category minima TBD |
| Calibration | Reliability curve, ECE with pre-registered bins, Brier/log-loss if probabilities issued | ML: maximum error TBD |
| Coverage | Portion of eligible reports accepted for automated decision; report by category, time, length and protected data slices only when lawful | Product/review: minimum TBD |
| Selective risk | Error rate among AUTO_CLASSIFIED cases at each chosen coverage/threshold; confidence intervals | Product/review: max TBD |
| OOD | False in-scope acceptance rate, OOD recall, and precision on approved negative set | Product/ML: targets TBD |
| Evidence/explanation | Exact original-text span validity; grounded claims, unsupported-claim rate, human judgment vs explicit category criteria | ML/review: threshold TBD |
| Latency p50/p95/p99 | Per-request wall time from ingress to response and segmented process timings; warm vs cold reported separately | Ops/product: limits TBD |
| Throughput/concurrency | Sustained accepted RPS, max concurrent, payload length distribution and error rate at target load | Ops: limits TBD |
| Availability | successful eligible response over defined measured window and allowed maintenance/exclusion contract | Ops/business: % / period TBD |
| Recovery | RPO/RTO, model rollback and DB restore success under fault injection | Ops/security: TBD |

## Measurement safeguards
- Partition cohorts: short/long documents, language mix, critical/rare/confusable classes, OOD, reviewer disagreements, temporal shift and valid vs malformed inputs.
- Use the exact frozen released taxonomy and model/policy; include versions, timestamps, CI for metrics and category support.
- Separate transport/server error rates from classification abstention and from genuinely OOD results.
- Define latency endpoints, success criteria, maintenance exemptions and synthetic vs representative load before formal SLO reporting.
- No blanket percentage is meaningful absent class costs, prevalence, confidence and representative workload.
- Observability must avoid raw report content in metrics labels and logs; alerts on error spikes, readiness, resource exhaustion, drift review (not accuracy assertion without labels).

## Decision/acceptance worksheet
Product and taxonomy owners: quality minima per class, OOD misclassification costs, automation coverage/review capacity.
Security/data owner: permissible datasets, test handling and logging/retention.
Operations: hardware budget, max input bytes/tokens, peak RPS, p95/p99, availability measurement, RPO/RTO, on-call.
ML lead: confidence intervals, sample size justification, calibration method, drift monitoring and retrain evaluation gates.

**Quality Gate:** No class-specific numerical accuracy, latency/availability or release-acceptance claims until decision owners sign these values and benchmark evidence meets them.
