# CR-IA-002: `semapv:LLMBasedMatching` is not a valid SSSOM 1.0 value — reconcile ADR-0022's "SSSOM 1.0" acceptance with agent-drafted rows

- **From:** IA (A2), WP-09 · **To:** CA (decider); DE (validator, release build) · **Date:** 2026-10-23 · **Type:** X (standard conformance) · **SemVer impact:** none for data; acceptance wording
- **Affects:** ADR-0022 §1 and WP-09 acceptance ("every set validates against SSSOM 1.0"); `vocab/mapping_predicates.yaml#justifications`; `scripts/validate_v2.py` SSSOM checks; `scripts/build_release.py` SSSOM export
- **Evidence label:** E (schema test below)

## Problem

ADR-0022 requires SSSOM 1.0 mapping sets *and* lists `semapv:LLMBasedMatching` among the justifications, and the EMST vocabulary allows it. The SSSOM 1.0 JSON Schema (`sssom-schema 1.0.0`, used by `sssom-py 0.4.15`) restricts `mapping_justification` to a closed pattern — MappingReview, ManualMappingCuration, LogicalReasoning, LexicalMatching, CompositeMatching, UnspecifiedMatching, SemanticSimilarityThresholdMatching, LexicalSimilarityThresholdMatching, MappingChaining. `LLMBasedMatching` (with `AgentBasedMatching`, `EmbeddingBasedMatching` and others) appears only in the SSSOM 1.1 development schema (mapping-commons/sssom `main`, 2026-10-09) [E: `sssom validate` on the X3 sets, 2026-10-23; V4-13: 1.1 is alpha only].

So an honest agent-drafted row cannot be strictly SSSOM 1.0-valid. The two 1.0-valid alternatives are worse: `ManualMappingCuration` misstates agent output as human curation (ADR-0024 §5 forbids presenting agent ratings as human work); `UnspecifiedMatching` is not in the EMST vocabulary and discards the provenance that ADR-0019 §4 needs.

## Proposed change

1. Keep `semapv:LLMBasedMatching` in EMST sets (truthful; in vocab).
2. Restate the acceptance as: "every set validates against the SSSOM 1.0 schema, with the SSSOM 1.1 `semapv` justification values in `vocab/mapping_predicates.yaml` accepted; re-validated against SSSOM 1.1 when it is final." `pipelines/crosswalks/validate_sets.py` already reports both a strict 1.0 result and the 1.0-plus-1.1-values result, with the count of affected rows.
3. When a human reviewer confirms a row, the row's justification becomes `semapv:MappingReview` (1.0-valid), so reviewed subsets are strictly 1.0-valid; only unreviewed agent drafts carry the 1.1 value.
4. DE's release export may optionally write a strict-1.0 rendering with `UnspecifiedMatching` plus an `other` key `original_justification=semapv:LLMBasedMatching` for consumers whose tooling rejects 1.1 values.

## Consequences if not accepted

Either the WP-09 acceptance cannot be met by any agent-drafted set, or agent drafts must be mislabelled as human curation.

## CA ruling

- **Ruling:** **accept items 1–3; accept item 4 as optional** · **Date:** 2026-10-23 · **Decider:** CA · **Recorded in:** ADR-0022 (amendment), PHASE4_BUILD_PLAN WP-09 acceptance (amended), `vocab/mapping_predicates.yaml` (annotated), SPEC §15, ADR-0029 §12, DECISION_LOG `CR-IA-002`
- **Note:** this CR arrived during the CA's integration session and is ruled with the others.

1. **Keep `semapv:LLMBasedMatching`** on unreviewed agent-drafted rows. It is truthful. Labelling agent output `ManualMappingCuration` would present agent work as human curation (ADR-0024 §5), which is forbidden.
2. **Acceptance restated:** every set validates against the SSSOM 1.0 schema, with the SSSOM 1.1 `semapv` justification values listed in `vocab/mapping_predicates.yaml#justifications_sssom_1_1_only` accepted as a declared extension, and is re-validated against SSSOM 1.1 when it is final. Each set reports both results (strict 1.0, and 1.0 plus the extension) and the count of affected rows, as `pipelines/crosswalks/validate_sets.py` does.
3. **Reviewed rows:** when a named human reviewer confirms a row, its `mapping_justification` becomes `semapv:MappingReview`, with `reviewer_id`. **Addition:** the row keeps `original_justification=semapv:LLMBasedMatching` in the SSSOM `other` slot, so the provenance ADR-0019 §4 needs survives review. Selection-use subsets are therefore strictly 1.0-valid, because selection requires two human reviewers (ADR-0022).
4. **Optional strict-1.0 rendering:** DE may emit `sssom/strict-1.0/<set>.sssom.tsv` as an extra generated export, with `semapv:UnspecifiedMatching` plus `other: original_justification=semapv:LLMBasedMatching`. It is a convenience rendering for tooling that rejects 1.1 values, never a source file, and is not needed for rc.1.
