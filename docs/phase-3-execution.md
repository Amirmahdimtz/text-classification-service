# Phase 3 — Execution and technical gate

Started by explicit owner command on 2026-10-21. Initial main: 9d231cabfeaf92cabd43fd479c1e71bba26b3ae3. Previous marker: PHASE_2_COMPLETE_READY_FOR_PHASE_3 (ADR-008; CI 39604867559). **Current marker: PHASE_3_IMPLEMENTED_AWAITING_VERIFICATION.** No business model, data or production acceptance is claimed.

The Host → Application → Core → Infrastructure structure, discovery-based dependency injection and existing PostgreSQL/FastAPI foundation remain unchanged. Pure text and dataset logic belongs to Core. Verified artifact and model provider reside in Infrastructure, training/analysis tools outside API. No business API route, migration, database model, artificial taxonomy, fake provider, dataset/model artifact or Phase 4 workflow was introduced.

## Task ledger

| Task | Actual implementation | Remaining requirements |
|---|---|---|
| P3-01 Dataset analysis | Offline private audit: category counts, min/max text length, input/annotation checks | Real distribution, rare classes, token lengths and language mix BLOCKED without licensed corpus |
| P3-02 Persian NLP | fa-offset-v1 with Arabic Yeh/Kaf, Unicode whitespace, original text, codepoint offset roundtrip and segment boundaries | Synthetic unit tests PASSED; corpus-specific review BLOCKED |
| P3-03 Leakage | Group, exact and token-trigram near-duplicate clustering, optional time split, seed, private HMAC fingerprints and disjointness validation | Real data and expert duplicate adjudication BLOCKED; heuristic is not exhaustive |
| P3-04 Baseline | Optional scikit-learn TF-IDF + LinearSVC trainer, validation Macro-F1/per-class/confusion, JSON weights and reload check | Real training and quality evaluation BLOCKED |
| P3-05 Encoder selection | Same evaluation protocol recorded in existing model-evaluation-plan; ADR-007 remains deferred | Models/licenses, compute, approved data BLOCKED |
| P3-06 Long docs | Offset-preserving full input, no arbitrary truncation or unevidenced chunking | Distribution/benchmark BLOCKED |
| P3-07 Difficult/OOD | Existing protocol retained | Gold OOD/rare/ambiguous/temporal examples BLOCKED |
| P3-08 Calibration | LinearSVC raw selected-class margin, confidence null, no fabricated probability | Validation calibration/quality targets BLOCKED |
| P3-09 Model provider | Verified JSON-only loader and @inject infrastructure lifecycle provider | Real organizational artifact and deployment topology BLOCKED |
| P3-10 Reliability | Bounded worker/batch, explicit one-time load/warmup, timeout, unavailable state, shutdown; no HTTP route | Real model load/stress and integration BLOCKED |
| P3-11 Release/manifest | SHA-256 for model + evaluation report, taxonomy/preprocessor/format compatibility, bounded files and path integrity | Signed/provenance-controlled production release and rollback BLOCKED |
| P3-12 Tests | Independent Persian/offset, dataset, CLI, manifest, provider and optional baseline fixture tests; CI regression jobs | Full Gold, server, load and Windows owner verification NOT RUN/BLOCKED |

All category names and models inside tests are synthetic TEST-ONLY fixtures and are not employer taxonomy or valid benchmark statistics.

## Verification/environment

- LOCAL BUILDER / independent (Python 3.13.5, optional scikit-learn 1.8.0): 25 Phase 3 tests PASSED with python -m pytest -q tests in the isolated development workspace; compile also PASSED. The workflow on GitHub is the source of truth for combined repository regression.
- REMOTE / AVAILABLE: GitHub Actions workflow runs existing independent and real PostgreSQL/Docker/Alembic integration checks, plus an added offline ML job using synthetic fixtures and optional dependencies. Record exact workflow evidence after execution; fixture checks are not real data benchmarks.
- LOCAL_USER / Windows PowerShell Python 3.12, Docker Desktop PostgreSQL 17 host port 55487: compile, Phase 1 validation, unit/DI regression, real PostgreSQL integration and API health; require owner logs, not run on owner hardware here.
- SERVER_MODEL: genuine train/eval/encoder/OOD/calibration/long-doc/load/Gold/rollback remain BLOCKED/NOT RUN until authorized data, approved taxonomy/label mode, secure server and numerical gates.

## External owners, risks and gates

DEC-01 taxonomy owner: published categories/definitions/version; DEC-02/03 employer/product: label cardinality and ambiguous/multi-topic rules; DEC-04 data/legal/security: legally usable, private train/validation/Gold/OOD data and annotation instructions; DEC-05/09 employer/quality: report size, per-class targets, coverage and risk; DEC-08 privacy/security: location/retention/authorization; DEC-10 operations: hardware, concurrency, latency and resource budget. All are BLOCKED; see risk register.

**Acceptance checklist:** independent offset, split, baseline code, manifest, provider and fixture tests IMPLEMENTED; real data, approved taxonomy, valid baseline/encoder comparison, calibrated selective risk, server inference, OOD, load, end-to-end evidence and accepted numerical thresholds are NOT VERIFIED. Phase 3 cannot be marked COMPLETE or Phase 4 started without fresh owner command and required evidence. Formal customer acceptance remains Phase 6, per ADR-008.
