# ADR-007 — Model choice and inference runtime deployment
**Status:** DEFERRED UNTIL PHASE 3 BENCHMARK / NOT APPROVED
**Owners:** ML lead, operations and data security
**Context:** Encoder vs baseline vs retrieval, CPU/GPU choice, batching and runtime topology depend on permitted report distributions and measured SLO.

## Options to benchmark
A. Statistical TF-IDF + Linear Classifier, reproducible baseline.
B. Fine-tuned Persian/multilingual encoder, after training/evaluation and licensing check.
C. Additional embedding retrieval only if incremental quality/evidence benefit is shown.
Runtime: isolated service vs dedicated process; model loaded/warmed outside request path, CPU/GPU/config determined from real capacity and security constraints.

## Non-negotiable requirements
No placeholder or unconditional fallback to weaker unverified model; no per-request artifact loading or blocking event loop; manifest links model/tokenizer/preprocess/policy/taxonomy/dataset fingerprint. Readiness reflects actual load and warmup; timeout produces infrastructure error. Long document strategy benchmarked with original evidence offsets.

## Decision event
After real Phase 3 comparison, security approval and runtime latency/load evidence, choose actual versioned candidate and record benchmark results in a new accepted decision. This ADR intentionally does not choose a final model or provider.
