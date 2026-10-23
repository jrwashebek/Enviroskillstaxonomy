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
