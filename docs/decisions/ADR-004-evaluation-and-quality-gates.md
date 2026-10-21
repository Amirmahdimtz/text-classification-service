# ADR-004 — ML evaluation protocol and acceptance gates
**Status:** PROPOSED / NOT APPROVED
**Owners:** ML lead, product/quality owner and employer
**Context:** Model choice and claims of production readiness require reproducible evidence, not model reputation or arbitrary confidence.

## Options
A. Frozen group/time-aware Train/Validation/Gold Test comparison with baseline, encoder and calibrated decision policy (recommended).
B. Random report-level split without leakage grouping (not acceptable for repeated incidents).
C. Unsupervised similarity only as probability (not acceptable as calibrated confidence).

## Proposed protocol
Record permitted data/provenance and frozen splits; train baseline TF-IDF linear and candidate encoder under same evaluation; tune on validation only. Report macro-F1, per-class precision/recall with support, OOD, calibration/ECE, coverage/selective risk, evidence groundedness and latency/throughput. Independent Gold Test used after selection, never for iterative tuning. Artifact/dataset fingerprint and environment required.

## Blocking choices
Numerical per-class floors, coverage/risk, OOD cost, explainability acceptance, minimum test support, p95/p99, RPS, service availability and server/hardware budget are TBD. No trained/evaluated model is asserted in Phase 1.
