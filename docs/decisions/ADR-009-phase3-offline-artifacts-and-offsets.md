# ADR-009 — Offset-preserving normalization and safe offline baseline

Status: ACCEPTED_TECHNICAL_SCOPE_ONLY (2026-10-21); employer's data, category, label semantics and runtime platform remain NOT APPROVED.

Context: Phase 3 independent code can be verified before legally permitted labeled data and deployment resources exist.

Decision: normalize limited Persian Arabic Yeh/Kaf and whitespace with explicit original Unicode half-open codepoint spans (fa-offset-v1). Require caller-supplied approved category list, label cardinality, taxonomy ID, group identifiers, seed and split ratios. Cluster exact and candidate near-duplicates before splitting and fail closed when detectable cross-split leakage or near-duplicate comparison budget occurs; HMAC fingerprints and aggregate reports stay in private storage.

For an optional single-label baseline use char 2–5 TF-IDF and LinearSVC. Serialize reproducible JSON vectorizer coefficients and validate artifact/validation-report hashes; never deserialize executable pickle/joblib. Scores are raw selected-class margins (NOT probability), confidence always null. The independent @inject provider loads and warms once explicitly, with no classifier HTTP route until approval. Sensitive char ngrams may leak content: derived weights and dataset always stay outside git and access controlled.

Alternatives rejected: arbitrary Unicode composition that corrupts offsets, naive report-level random splits, plain unsalted per-document public hashes, untrusted pickle, fake production model, automatic fallback to OUT_OF_SCOPE. Near-duplicate shingle similarity is heuristic, not semantic guarantee.

Consequences: Baseline configuration is experiment code, not selected deployment, threshold or label policy. Frozen approved data and hardware are still required for true P3 quality gate. ADR-007 final model selection remains DEFERRED. A change to evidence offset behavior needs a new preprocessing version and regression tests.
