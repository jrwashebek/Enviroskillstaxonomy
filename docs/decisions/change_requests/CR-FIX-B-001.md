# CR-FIX-B-001: Apply display-gate 1.1.0 to the generated HR views and update the PD test

- **From:** Fix-B (AI agent, briefs/deck/PD editor, package fix pass) · **To:** FH (owner of the WP-08 view
  generators); DE (integration of `pipelines/views/` into `scripts/`); IO (display-gate steward) · **Date:** 2026-10-23 ·
  **Type:** code and test change · **SemVer impact:** patch (view output only; no data change)
- **Affects:** `pipelines/views/federal_series_profile.py`, `pipelines/views/state_class_view.py` and their outputs in
  `docs/build/WP-08/generated/federal-series/` and `state-class/`; `pipelines/views/tests/test_views.py`
  (`test_forester_pd_is_labelled`)
- **Evidence label:** J (raised by package review issue 1; display rule `validation/display_gates.yaml` 1.1.0)

## Problem

1. **Generated FSP and SCV Markdown still print gated values.** The display gate (`role_profile_values`,
   `job_analysis_values`, `hr_classification_min_status`) says time share and importance are not shown in a Federal
   Series Profile or State Class View until job analysis confirms them (label `fsp_time_share_notice`: "% time: set by
   the supervisor; EMST supplies none before job analysis."), and that critical, needed-at-entry and distinguishing
   values need a human reviewer. The explorer applies this. The generated `.md` and `.json` files do not: for example
   `docs/build/WP-08/generated/federal-series/0460.md` lists "Major duties (indicative % of time, agent draft)" with
   "— 14%" and "*(critical, needed at entry)*" flags, and the same appears for every series and state class. These files
   ship in the release bundle under CC0, and the role briefs point HR readers to "Federal Series Profiles". The briefs now
   say "the explorer's Federal Series Profile", but the generated files remain inconsistent with the gate.
2. **The PD test asserts a percentage.** `test_forester_pd_is_labelled` ends with `assert "%)" in pd  # major duties
   carry % time`. Under the gate the PD must carry no percentage. The regenerated PD (`forester_pd_fes.py@0.2.0`) gives
   each duty a blank slot `(___%)`, which is standard PD form and keeps the assertion true, but the assertion now tests
   for the wrong thing.

Both changes are outside Fix-B's lane (only `pipelines/views/forester_pd_fes.py` is in it).

## Proposed change

1. In `federal_series_profile.py` and `state_class_view.py`, route `pctTime`, `importance`, `critical`, `neededAtEntry`
   and `distinguishing` through `validation/display_gate.py#decide_role_value` (context `federal-series-profile` /
   `state-class-view`). Where the value is pending, print the gate's label instead of the value; order tasks and duties
   by record order, not by time share (gate `rollups` rule). Keep the values in the release-bundle records.
2. Replace the last line of `test_forester_pd_is_labelled` with checks that match the gate, for example:

   ```python
   assert "% time: set by the supervisor" in pd
   assert not re.search(r"\(\d+(\.\d+)?%\)", pd)          # no numeric duty percentages
   assert "…" not in pd                                    # no truncated statements (package review issue 9)
   assert "needed-at-entry tasks" not in pd.lower() and "critical tasks" not in pd.lower()
   ```

3. Optional: add a test that no generated FSP or SCV Markdown file contains a numeric "% of time" value while the
   underlying record is below `job-analysis-confirmed`.

## After a decision

Re-run `pipelines/views/build_views.sh`. The briefs and the PD need no further change. Minor, data-side: competency
labels in `data/v2` use British spellings ("modelled"), which appear verbatim in the PD's related-duty and Factor 1
lines; the package review (issue 30) asks for US spelling.
