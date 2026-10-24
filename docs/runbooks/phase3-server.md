# Phase 3 — Controlled server ML verification

Status: BLOCKED until category version, annotation guideline, single/multi-label approval, data rights, permitted server and numerical quality gates exist. This runbook gives actual commands only for files that already exist; it does not claim a full encoder trainer/OOD evaluator was implemented.

## Available software

- requirements-ml.txt: optional pinned scikit-learn 1.8.0 plus existing runtime dependencies.
- tools/train_baseline.py: char-ngram TF-IDF + balanced LinearSVC, fit TRAIN only, report VALIDATION only, JSON-only artifact and checked hash; no pickle or GPU dependency.
- src/infrastructure/ml/tfidf_linear_model.py: real baseline loader with raw selected-class SVC margins and null confidence.
- src/infrastructure/text_classifier_provider.py: independent @inject warm-once singleton lifecycle with capacity, timeout, batch and shutdown. No live API controller, no active production artifact.

On an authorized private server, after the private dataset audit in phase3-local.md, configure $releaseDir (new approved private location outside git) and $modelVersion (new immutable run identifier) and preserve the original HMAC key.

    python -m pip install -r requirements-ml.txt
    python -m pytest -q tests/test_baseline_model.py tests/test_text_classifier_provider.py
    python tools/train_baseline.py --input $inputJsonl --approved-codes $codesFile --audit-manifest $auditFile --release-dir $releaseDir --authorization-reference $authorizationReference --taxonomy-version $taxonomyVersion --model-version $modelVersion --seed $seed --ratios $trainRatio $validationRatio $testRatio

Add --temporal only if the audited split also had it. Model CLI explicitly requires single-label and fails closed if the audit or HMAC differs. No TEST data is fitted or evaluated by the baseline script. The validation report's classifier-only prediction latency is NOT API/service P95 and not a production benchmark. No external report text is sent through this CLI.

## Evaluation / benchmark still to implement and execute when approved

1. Freeze groups, dates, licenses, category definitions and untouched independent Gold Test before training.
2. On authorized hardware compare baseline and licensed Persian/multilingual encoders with identical splits, preproc version and common per-class metrics; collect memory, CPU/GPU, wall-time and carbon/cost as applicable.
3. Study actual input lengths before choosing chunking, overlap or aggregation. Record truncation risk and offset validity.
4. Evaluate confusable/rare/ambiguous/mixed-language/short and temporal sets; collect true independent OOD negatives.
5. Fit calibration on VALIDATION only, then assess ECE/reliability, coverage/selective risk and category thresholds. Raw margin is not probability.
6. Lock model and policy, then run independent Gold TEST ONCE, reporting Macro-F1, per-class support/P/R/F1, confusion, OOD error, calibrated risk and uncertainty.
7. Measure real cold/warm load, model timeout, batch/concurrency, memory, P50/P95/P99, throughput and sustained/recovery behavior. Verify authenticated deployment and release rollback only after operational approval.

There are currently no commands for encoder training, Gold/OOD evaluation or full stress because such programs and environment have not been implemented/approved. Inventing a runnable command would mislead the operator.

Return securely only reviewed aggregated benchmark reports, complete version and hash metadata, test/CI links, permitted error codes and sanitized capacity evidence. Never expose model artifacts containing confidential character ngrams, original datasets, credentials, or the HMAC key.

## Temporal holdout integrity

For an authorized dataset audited with `--temporal`, the splitter now preserves entire incident/near-duplicate components and requires strict chronological separation between train, validation and test. It may move ratio cut points or fail closed when no valid triple partition exists. Treat rejection as a split design/data adjudication task for the ML/data owner; do not disable the guard. This cannot replace real semantic leakage review and Gold verification due in Phase 6.
