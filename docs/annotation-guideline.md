# P1-06 — Annotation guideline and gold dataset plan
**Status:** Protocol proposed; actual taxonomy, permitted samples and annotation staff are BLOCKED.

## Labeling unit and rubric
- Unit: a full original report and its exact taxonomy_version. For multi-label, revise rubric explicitly before collection.
- Annotator sees only least-privileged authorized report view, approved category definition, inclusion/exclusion examples, and adjudication notes.
- Annotation result records annotator pseudonymous ID, guideline version, timestamp, category/candidates, confidence as qualitative annotation-only signal, ambiguity flags, evidence spans on original text, and reason.
- Unknown/ambiguous/multi-topic/OOD must not be forced into a normal category; use an explicit proposed adjudication disposition separate from taxonomy.
- A completed annotation must cite a valid inclusion criterion and corresponding original-text span when reasonably available; impossible cases are flagged for policy review.

## Workflow
1. Create taxonomy and guideline baseline; train annotators on de-identified pilot examples with authorized access.
2. Double-label independent stratified pilot and intentionally difficult borderline/OOD items. Sampling count/coverage target TBD after data inventory.
3. Calculate inter-annotator agreement (e.g. Cohen's kappa for two raters, Krippendorff alpha if more raters and suitable data) and per-category confusion; report prevalence and disagreements.
4. Adjudicator reviews divergent labels; unresolved taxonomy ambiguities return to taxonomy owner. Preserve original votes and final adjudicated label; no blind overwrite.
5. Freeze gold set with taxonomy/guideline versions and source fingerprint. Exclude unapproved / disputed labels from benchmark or report their subset separately.
6. Reviewer corrections are candidates for later curation, NOT automatically added to training.

## Split and leakage controls
- Authorized datasets split train / validation / independent untouched test, optionally temporal holdout and explicit OOD evaluation; exact split proportions and group boundary must be chosen after real distribution review.
- Group by report family, near-duplicate, incident/event, originating case, source and any shared template; inspect time leakage. All near duplicates and same incident groups stay in one partition.
- Group/time split performed before fitting vectorizer, scaler, tokenizer adaptations, class weights or threshold optimization; transformations train-only.
- Deduplicate, fingerprint and record split seed, version, category histogram, time ranges, group IDs or privacy-safe hashes.
- Validation selects hyperparameters/calibration/decision thresholds. Gold Test is used once for independent assessment, never iterative tuning.
- Evaluate rare and overlapping classes explicitly; where support insufficient, mark category performance NOT ESTIMABLE rather than report misleading perfect scores.
- OOD negatives must be approved and held out with provenance; synthetic examples, if any, explicitly separate from acceptance set.

## Quality gates pending owner decision
Minimum annotated examples per class, agreement threshold, class coverage, Test freeze policy, permitted extraction, privacy and reviewer identities remain TBD/BLOCKED. Data integrity and consent checks precede every training/evaluation use.
