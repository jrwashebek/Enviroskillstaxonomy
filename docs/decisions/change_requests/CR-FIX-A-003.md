# CR-FIX-A-003: Data and script corrections that the evidence review requires outside the report lane

- **From:** Fix-A (AI agent, report editor, package fix pass) · **To:** LM (signals, `docs/methods/scripts/`), SC (instruments and events), DE (data build), FC (field-craft research text) · **Date:** 2026-10-23 · **Type:** data and script corrections · **SemVer impact:** patch (record text, provenance and two new events)
- **Affects:** `data/v2/signals/2026/openlmp.jsonl`, `data/v2/signals/2026/omb-ai-inventory-2025.jsonl`, `data/v2/signals/2026/bls-ep-2025-35.jsonl`, `data/v2/events/*.jsonl`, `data/v2/instruments/instruments.jsonl`, `docs/methods/scripts/wp10_signals.py`, `docs/methods/scripts/wp10_lmp.py`, `docs/research/field-craft/report.md`
- **Evidence label:** E (docs/review/evidence_review.md R15, R33, R61, R80 and §5; WP15_report_corrections.md §C)

## Problem

The report, figures and claims register now carry the corrected facts. Several upstream records still carry the old ones. The figure build works around three of them explicitly, and two register `do_not_say` entries cannot yet be enforced by the explorer's output check.

## Proposed changes

1. **OpenLMP monitoring signal** (`openlmp.jsonl`, `seed:sig/openlmp/monitoring-share-2012-vs-1982`): the editorial note says "Robust to weighting … this is demand for indicator design, evaluation and reporting", and the text uses "monitoring requirements". The evidence review (R80) and Fix-A's sensitivity check show the gap does not survive excluding documents that are monitoring evaluation reports (17 of 36) or stand-alone monitoring plans (5 of 36). Among plan documents only, the shares are 10.0% and 2.8%, and the bootstrap intervals overlap (see `docs/package/report/figures/f05_plan_monitoring_share_by_rule.csv`). Rewrite the note, say "components typed as monitoring", and consider lowering `directionConfidence`. Once the phrase is gone, re-quote "monitoring requirements" in register PLAN-01 `do_not_say` with single quotes so the explorer check enforces it.
2. **Interval method** (`wp10_lmp.py`): replace the normal-approximation `ci95` (mean ± 1.96 SE, which gives an impossible negative bound for at-risk species) with a plan-level percentile bootstrap. `build_figures.py` already does this: seed 20261023, 10,000 resamples.
3. **OMB signal and method string** (`omb-ai-inventory-2025.jsonl`; `wp10_signals.py`): "nine environmental bureaus" should be "eleven environmental units (nine bureaus and two USDA mission areas)" (R61). Then re-quote the phrase in register OMB-02 `do_not_say` with single quotes.
4. **Two DriverEvents to add** (`data/v2/events`), with instrument updates:
   - `seed:ins/americorps-grant-terminations`, 2025-07: notices to grantees terminated on 2025-04-25, including those in non-plaintiff states, that they are eligible for reinstatement (register WF-06; Boston Globe 2025-07-17).
   - `seed:ins/nj-ej-law`, 2026-07: the NJ Supreme Court grants certification; the rules remain in effect pending appeal (register EJ-02; Riker Danzig 2026-09-03).

   `build_figures.py` adds both to F09 as hard-coded rows checked against the register. Remove them from the script once the events exist.
5. **Superseded provenance:** the BLS signals cite V4-07 (status superseded), and the Colorado events cite CP-043 and IO-034 (superseded). `build_figures.py` replaces them with BLS-01 and AIGOV-02 through `SUPERSEDED_SUCCESSORS`. Please cite the current records in the data.
6. **Field-craft research text** (`docs/research/field-craft/report.md`, around lines 26 and 209): replace "field staff who also fly" and "absorbed into field roles" with the register RPT-14 wording (WP15_report_corrections §C), so the forms do not re-enter later drafts.
