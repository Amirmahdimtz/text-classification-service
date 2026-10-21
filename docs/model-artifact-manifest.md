# Phase 3 artifact/preprocessing contract

## Model release manifest version model-release-v1

Required: manifest_version, model_version, model_identifier, artifact_filename, artifact_sha256, artifact_format, preprocessor_version, taxonomy_version, dataset_fingerprint, training_config_sha256, evaluation_reference, evaluation_sha256, dependency_version, provenance_reference. Both tokenizer_version and tokenizer_sha256 must be populated together or both absent/null. decision_policy_version may be null until approved. For the optional baseline, artifact_format=tfidf-linear-json-v1 and preprocessor_version=fa-offset-v1.

Exact model and evaluation-report SHA-256 content checks run before acceptance, along with file traversal/symlink/size protection. Baseline loader also validates model format, class and TF-IDF vocabulary shape, finite weights and expected taxonomy. SHA is not a cryptographic signature of provenance or official release approval; a signed release, real tokenizer, secure artifact registry and operational rollback verification are future approved work.

This baseline uses JSON vocabulary/coefficients, never unsafe Python pickle/joblib. A model may reveal character substrings of sensitive reports: DO NOT commit derived artifacts to this public repository.

## fa-offset-v1

Input is unmodified Unicode text; normalize Arabic Yeh/Kaf (including Alef Maksura Yeh) to Persian, horizontal whitespace runs to a space, CRLF and Unicode breaks to LF. Preserve ZWNJ, mixed scripts, punctuation, dates, numbers, technical tokens, source line boundaries. Every normalized code point maps onto a zero-based, half-open span in original Python Unicode code points. source_slice(start,end) is the original evidence, not normalized evidence. NFC composition is not applied to avoid arbitrary offset changes. This is necessary groundwork for Phase 4 grounded evidence, NOT itself a grounded explanation.

## dataset-audit-v1

JSONL report_id, group_id, text, labels, taxonomy_version, optional timezone-aware occurred_at. Caller must supply an actual approved category list, cardinality, split ratios, seed, taxonomy release, permission reference and private HMAC key. Seeded group/time-aware splits include exact duplicate and near-duplicate candidate clustering and fail on disallowed annotation conflicts or group/ID/text leakage. Output PRIVATE aggregation contains counts, per-label supports, length extrema and keyed HMAC-SHA256 split fingerprints. This is not an export of train/validation/test records, not proof against semantic duplicates, and not an approved dataset or training permission.

An immutable real release must be created outside the public checkout, staged in private storage and selected/rolled back explicitly after verified model, security and operational gates. There is currently no production active release.
