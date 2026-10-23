# CR-DC-001: Match L4 `productExamples` case-sensitively in the typing lint

- **From:** DC (A4), WP-04 · **To:** DE (A1; owner of `scripts/validate_v2.py` and `schema/lint/typing_lexicon.yaml`), CA (decider) · **Date:** 2026-10-23 · **Type:** X (lint rule) · **SemVer impact:** none for data
- **Affects:** `scripts/validate_v2.py` (`Validator._term_rx`, the loop that adds `data/v2/tools/tools.jsonl#productExamples` to `self.products`); `schema/lint/typing_lexicon.yaml`; `data/v2/tools/tools.jsonl` (WP-04)
- **Evidence label:** E for the code behaviour (read in `scripts/validate_v2.py` on 2026-10-23); J for the examples of collisions

## Problem

1. `validate_v2.py` adds every `productExamples` entry of length ≥ 3 to the L4 product lexicon with `_term_rx({"term": ex})`. No `cs` key is passed, so the pattern is compiled with `re.I`. Any draft competency, task, indicator, knowledge statement or enactment note that contains the word in any case fails with `E-LINT-TYPING`.
2. Many environmental product names are also ordinary words in environmental text: InVEST (*invest*), Slack (*slack water*), Confluence (*river confluence*), Zonation (*vegetation zonation*), Raven (the bird), Unity (*unity of command*), Python (*Burmese python*), Clay (*clay soil*), Watershed (carbon software; *watershed*), Fulcrum, MAPLE (*maple*), Zoom, SWAT, Excel, Asana.
3. IO's linter (`validation/lint_indicators.py`) already matches products case-sensitively. The two checks therefore disagree.
4. One existing lexicon term has the same problem: `{term: Field Maps}` has no `cs` flag, so the generic phrase "field maps" is flagged as a product.

**Interim (WP-04):** these names are recorded in each tool's `scopeNote` ("Further product names …") and not in `productExamples`. The L4 seed is complete, but the lint cannot catch these names in L1/L2 text.

## Proposal

1. Compile `productExamples` case-sensitively by default (`_term_rx({"term": ex, "cs": True})`), matching IO's linter. A tool row may opt into case-insensitive matching only for names that are not ordinary words (a later optional `productExamplesCaseInsensitive` field, if the CA wants one).
2. Set `cs: true` on `Field Maps` (and review the other multi-word terms) in `schema/lint/typing_lexicon.yaml`.
3. After 1 lands, WP-04 moves the names listed under item 2 from `scopeNote` into `productExamples`. That is a data-only change.

## Not asked

- No change to how L5 instrument names are matched.
- No change to the T-4 rule. A tool class (GIS, UAS, lidar) may still be named in L1/L2 text when it changes the work condition.
