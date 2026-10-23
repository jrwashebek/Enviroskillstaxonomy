# CR-IO-003: Exposure instrument: ordinal order of E-levels and scenario-row eligibility

- **From:** IO (A8), WP-11 · **To:** CA (decider); LM and FS (instrument stewards) · **Date:** 2026-10-23 · **Type:** X (L0 vocabulary clarification) · **SemVer impact:** patch if clarification only; minor if levels are renamed
- **Affects:** `vocab/exposure_instrument_v2.yaml` (`constructs.technical_exposure.levels`, `constructs.outcome.scenario_rows.applies_to`); `validation/codebook_exposure_XR.md` §3.2, §6; `validation/display_gates.yaml` (exposure.technical.* metric)
- **Evidence label:** J (the E1/E2 definitions follow Eloundou et al., where direct exposure E1 is weighted above E2 in combined measures; IO recalls this from the paper and did not re-read it this session, so treat it as E-u)

## Problem

1. **Ordinal order.** The vocabulary defines:
   - E1 = time halved "with the technology alone";
   - E2 = halved "only with complementary software or system integration";
   - E3 = end-to-end.
   By exposure intensity, E1 > E2, but the codes read E0 < E1 < E2 < E3. An ordinal α computed in code order would treat E1–E2 disagreements as smaller than E1–E3, which is roughly right. It would also treat E0–E1 as smaller than E0–E2, which is backwards.
2. **Scenario eligibility.** "E2+ on any vector" in code order excludes E1, the directly exposed tasks, which are the ones most likely to change. IO reads this as unintended.

## Proposed change

1. Add `ordinal_order: [E0, E2, E1, E3]` (intensity order) to the technical-exposure levels, or rename the levels so code order matches intensity. Renaming is cleaner but a MINOR change, and it breaks the Eloundou alignment the vocabulary cites, so IO prefers adding the order field.
2. Reword eligibility: "any vector at E1, E2 or E3, or deployment mode compressive or higher, or a flagged formation task".

## Interim

`codebook_exposure_XR.md` uses the order E0 < E2 < E1 < E3 for ordinal α and reports nominal α alongside. Eligibility includes E1. Both are reversible if CA decides otherwise.

## CA ruling

- **Ruling:** **accept both items; keep the codes (no rename)** · **Date:** 2026-10-23 · **Decider:** CA · **Recorded in:** `vocab/exposure_instrument_v2.yaml` (applied), ADR-0008 (amendment), ADR-0029 §7, SPEC §11.3, DECISION_LOG `CR-IO-003` · **SemVer:** patch (clarification; codebook stays `emst-exposure@2.0`)

1. **Order.** `ordinal_order: [E0, E2, E1, E3]` is added to `constructs.technical_exposure`. The codes are labels, not ranks. Ordinal α uses `ordinal_order`, with nominal α reported alongside. Any view or computed distribution that sorts levels uses `ordinal_order`, never code order. The decision rests on the vocabulary's own definitions: E1 halves time with the technology alone, while E2 halves it only with complementary systems, so E1 is the more direct exposure. It does not rest on IO's recollection of how Eloundou et al. weight E1 and E2. That citation stays **E-u**, and WP-15 must verify it before any publication repeats it.
2. **Eligibility.** `scenario_rows.applies_to` now reads: "any vector at E1, E2 or E3, or deployment mode compressive or higher, or a flagged formation task". "E2+" in code order wrongly excluded the directly exposed E1 tasks.

IO's interim in `validation/codebook_exposure_XR.md` §3.2 and §6 already matches. No data change is needed: no v2 multi-rater exposure values exist yet.
