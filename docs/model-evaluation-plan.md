# P1-09 — ML architecture and benchmark protocol
**Status:** Evaluation design only, no approved data, models, experiment results or deployment architecture.
**Owner:** ML lead with product, taxonomy and data-security approval.

## Candidate comparison, same dataset and test protocol
| Candidate | Why evaluate | Risks / decision evidence |
|---|---|---|
| Statistical baseline: TF-IDF + Linear Classifier | reproducible, inexpensive interpretable comparator | sparse context, imbalanced/long documents; measured macro/per-class F1 |
| Fine-tuned Persian/multilingual encoder | context representation and category-boundary candidate | training/privacy/compute, latency, token length; compare same held-out data |
| Embedding/retrieval-assisted approach (optional) | useful if evidence/nearest-reference retrieval proves incremental value | leakage, index access/updates, similarity not probability |
| Long-document variants | full length vs evaluated chunking/aggregation | lost evidence, duplicated chunks, inference cost and offsets |
| Explanation approach | explicit extraction/rule-grounded evidence, optional validated rewrite | unsupported claims, sensitive leakage, span mismatches |

No final model/encoder, architecture, GPU, threshold or library release is selected until evidence exists.

## Data lineage and reproducibility
Use approved train/validation/untouched test, optionally temporal holdout + OOD set. Freeze taxonomy/guideline, dedup/group-by-incident split, report class prevalence and rare-class support. Record dataset content fingerprint, permission, split seed/group hashes, preprocessing/tokenizer version, code revision, hyperparameters, environment, artifact hash and evaluation configuration. PII must not enter publicly visible artifacts or logs.

## Training/evaluation sequence
1. Data profiling: class balance, source, length distributions, mixed scripts, near-duplicate/incident leakage and annotation agreement.
2. Train-only preprocessing fitting; compare baseline and encoder under same label definitions, training budget accounting and evaluation partitions.
3. Validation-only hyperparameter selection, error analysis, per-category threshold selection and calibration. Never calibrate or optimize on Gold Test.
4. OOD handling: evaluate known negatives, borderline reports, novelty and abstention; false acceptance vs needs-review; no infrastructure outage disguised as OOD.
5. Evidence: verify source spans after normalization and chunking; score citation precision/recall on expert-annotated evidence plus groundedness and unsupported claim rate.
6. Benchmark under realistic short/long documents, concurrency, cold/warm split and deployment hardware; measure preprocess/inference/explanation/DB p50/p95/p99, throughput and resource use.
7. Lock candidate configuration, run independent Gold Test once, report uncertainty intervals (e.g. group-aware bootstrap where justified), per-class breakdown, support and all failure cases.
8. Document comparison and reason for selected model, ethical/security assessment, runtime isolation and rollback; stage a versioned release manifest and readiness behavior.

## Confidence and decision
Calibrated probability is eligible only after validated calibration (temperature/Platt/isotonic as supported by candidate method and data volume). Evaluate reliability diagrams, ECE with declared binning, Brier score or log loss as suitable. Similarity/cosine/raw logits are NOT probabilities. Null confidence or explicitly typed raw score when calibration fails. Report coverage C(threshold) and selective risk R(threshold) on decided subset; examine risk per critical category and class prevalence. High-confidence unsupported evidence should still trigger review under approved policy.

## Acceptance reporting (blank until actual experiment)
Mandatory columns: run_id; code/model/tokenizer/preprocessing/taxonomy/policy versions; train/val/test fingerprints and disjointness; class supports; macro-F1; per-class precision/recall/F1; calibration and ECE methodology; OOD false-accept/recall; coverage/selective risk curve; explanation groundedness/span accuracy; P50/P95/P99; RPS; hardware/cost; confidence intervals; failed cases; approved gate thresholds and PASS/FAIL.

**All numerical targets are TBD and all evaluation results = NOT RUN/BLOCKED.** Phase 3 requires approved real data, appropriate server/resources and frozen metrics; no simulated results count as validation.
