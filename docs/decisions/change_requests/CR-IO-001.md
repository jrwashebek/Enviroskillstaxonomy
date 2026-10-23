# CR-IO-001: Fields and semantics needed to make the indicator publication rules machine-checkable

- **From:** IO (A8), WP-11 · **To:** CA (decider), DE and IA (schema, WP-01) · **Date:** 2026-10-23 · **Type:** X (structural; schema) · **SemVer impact:** minor (new optional field; typed values for an existing field)
- **Affects:** SPEC §5.2 `levels[].publicationRuleChecks`, §5.3 `Indicator`; `vocab/proficiency_levels.yaml#publication_rules`; `validation/indicator_lint_rules.yaml` (PUB-11, PUB-12, PUB-14, tier requirements); lint waiver register location
- **Evidence label:** J (IO; the rules come from ADR-0004 §3 and SPEC §8.2; the gaps are found by implementing them in `validation/lint_indicators.py`)

## Problem

1. **Typing of `publicationRuleChecks`.** SPEC §5.2 names `publicationRuleChecks{existence, distinctness, assessability, consensus}` but gives no value type. Booleans cannot express "not yet tested", and at rc.1 PR-1 (existence: job-analysis data) and PR-4 (consensus: Delphi) are untested for every level. A `true` typed by an agent would claim human evidence that does not exist.
2. **PR-2 distinctness is not checkable.** IO's rule says adjacent levels must differ on a *named* attribute, and the author records it "in notes". There is no field for it.
3. **Tier mapping is implicit.** ADR-0024 §3 requires consensus (placement ≥ 70% modal, IQR ≤ 1) for `develop` and `select`, while `describe`-tier levels can be published before any Delphi. SPEC §8.2 says indicators exist only at levels passing all four rules. These read inconsistently for a describe/develop-grade rc.1.
4. **Lint waivers have no home.** The closed record schema (SPEC §4) rightly forbids a waiver field on Indicator.

## Proposed change

1. Type `publicationRuleChecks.<rule>` as `pass | fail | pending | not-applicable`, each optionally with `evidence[]` (Source, study or Delphi round IDs).
   - CI rejects `pass` on existence unless an indicator at that level has `validationStatus ≥ job-analysis-confirmed`.
   - CI rejects `pass` on consensus unless `validationStatus ≥ panel-retained`.
   - Implemented as PUB-14 in `validation/lint_indicators.py`.
2. Add optional `Indicator.distinguishingAttribute` ∈ {ATT-AUT, ATT-GUI, ATT-CPX, ATT-SCO, ATT-KNO, ATT-AUG, ATT-FOR}: the attribute on which this indicator differs from the adjacent lower level. It is required for indicators above `levelSpan.min` once the record is `candidate`.
3. Ratify the tier mapping in `validation/indicator_lint_rules.yaml#publication_rules.tier_requirements`:

| Tier | PR-1 existence | PR-2 distinctness | PR-3 assessability | PR-4 consensus | Indicator OBS-4 minimum |
|---|---|---|---|---|---|
| describe | pass or pending | pass | pass or pending | pass or pending | ≥ 2 |
| develop | pass or pending | pass | pass (≥ 2 indicators at OBS-4 = 3) | pass | ≥ 2, with evidence plan |
| select | pass | pass | pass | pass | 3, double-coded by humans, no lint flags |

   Views show "level placement pending validation" wherever PR-1 or PR-4 is `pending`.
4. Fix the waiver register's home. Proposed: `data/v2/registers/lint_waivers.csv`, with the columns in `validation/indicator_lint_rules.yaml#waivers` (default today: `validation/waivers/indicator_lint_waivers.csv`). Waivers are keyed to the record ID, rule ID and normalized-text SHA-256, and are signed only by human pseudonymous IDs.

## Consequences if not accepted

The linter treats `true` as `pass` and still applies PUB-14. PR-2 is checked only by the B08 cross-level comparison. Develop-tier competencies cannot show that PR-4 is pending, which pushes either over-claiming or under-publishing.
