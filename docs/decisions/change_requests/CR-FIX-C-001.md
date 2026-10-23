# CR-FIX-C-001: Data, vocabulary and build changes the explorer fix pass needs outside `site/`

- **From:** Fix-C (AI agent, explorer engineer, package fix pass) · **To:** LM (signals, `docs/methods/scripts/`), FS (weak-signals file, `vocab/scenarios.yaml`), PS and CM (cross-sector mapping comments), FH (series register notes), IO and DE (display-gate activation), WP-15 register owner · **Date:** 2026-10-23 · **Type:** data, vocabulary and build corrections · **SemVer impact:** patch (record text and signal fields; no schema change except the optional scope field in item 1)
- **Affects:** `data/v2/signals/2026/*.jsonl` (opm-headcount, foresight, s2a-change-view-atoms, bls), `docs/research/strategic-foresight/weak_signals.csv`, `vocab/scenarios.yaml`, X11 translation mappings (`emst-public-private`), `data/v2/.../opm-series` register notes, `vocab/rules/display-gate@1.1.0.yaml`, `scripts/build_release.py`, `docs/methods/claims_register.csv` (PLAN-01, WF-02)
- **Evidence label:** E for what renders today (built explorer, 2026-10-23, `site/reports/check-output.json`); J for the proposed fixes
- **Raised by:** `docs/review/package_review.md` issues 6, 16, 30 and 31; Fix-C's checker change for issue 10

## Problem and what the explorer already does

The explorer now builds and passes its output check with 0 problems (782 pages). Fix-C changed only `site/`. The items below are text or fields the explorer renders, or rules it reads, that it must not rewrite itself.

1. **Signals are linked too broadly and graded from the CSV, not the source (package review issue 31).**
   - Eight signals target `vocab:sector_actors#federal` (agency headcounts, the OPM HR-staff figure, EPA's AI strategy, the IRA rescission headline). Before this pass every federal variant page listed all of them. The explorer now lists only signals about the role, its variant or its primary work function, and counts the employer-wide ones with a link to What's coming. Linking a headcount signal to the roles in the affected agency needs a scope the records do not carry.
   - Reliability grades were set by the agent that entered each signal. Rows that came from `docs/research/strategic-foresight/weak_signals.csv` carry grade A or B from the CSV rather than from the underlying source. The explorer now labels every grade "set by the AI agent that entered the signal; not yet re-graded from the underlying source".
   - **Proposed:** (a) re-grade `reliability` on every signal from its underlying source (vocab `signal_reliability` A–D), starting with the `seed:sig/foresight/ws-*` rows; (b) add an optional scope to agency-level signals, for example `scope: {agencies: [...], occupationSeries: [...]}` or a `targetId` on the agency, so the explorer can link them to roles in that agency or series. Once (a) is done, the explorer drops its "not yet re-graded" note.

2. **Internal codes in rendered record text (package review issue 6).** The explorer strips decision references from the release notice, but it does not rewrite record text. Still rendered:
   - X11 mapping comments: "Seeded from PS translation row; requires PS and CM confirmation" (every variant with a cross-sector translation row);
   - signal titles ending "…, attached to R10-environmental-review-specialist" (role-level copies in `s2a-change-view-atoms.jsonl`);
   - `sourceRelease` "docs/research/strategic-foresight/weak_signals.csv (2026-10-23)" (repository path shown as a source);
   - signal titles "Signpost SP-01 (AX-1): …" and the wildcard effect "Moves AX-2 quickly" (`vocab/scenarios.yaml`);
   - the series register note "FH judgment pending verification of the qualification standard" (WP-08 views; the explorer shows its own wording instead).
   - **Proposed:** write these in plain words ("requires review by EMST's private-sector and career-mobility agents"; the role's name, not its key; the source's own title; the axis name rather than AX-n).

3. **Scenario wording drifts from the report (package review issue 16).** `vocab/scenarios.yaml` gives SC3 as "agencies become intelligent customers" and no-regret move NR-6 as "Build intelligent-customer capacity". The report (draft 0.9.1) uses "informed buyer" and keeps SC3's "hollow state" risk in the summary. The explorer renders the vocabulary text as is. **Proposed:** adopt the report's wording in the vocabulary.

4. **The release's display-gate view is stamped 1.0.0 while the gates file is 1.1.0.** `validation/display_gates.yaml` says `version: 1.1.0, status: active`, but `vocab/rules/display-gate@1.1.0.yaml` is still `status: draft`, so `scripts/build_release.py` stamps `views/display_gate.json` as display-gate@1.0.0. The explorer applies the 1.1.0 role-profile rules itself (job-analysis values withheld; target levels labelled editorial draft) and its footer now says so. **Proposed:** complete the activation step the rule file names (IO), then have the build stamp 1.1.0 (DE).

5. **PLAN-01 "monitoring requirements": enforcement will catch unrelated text.** CR-FIX-A-003 proposes re-quoting this phrase with single quotes once the OpenLMP signal is rewritten. The explorer check would then enforce it everywhere. Besides the OpenLMP signal ("Monitoring requirements as a share of plan components…", What's coming), the phrase renders on about 25 more pages from three records that are not about plans: `seed:SL-C02` and its indicator `seed-sl-c02-l2-b` (permit limits, conditions and monitoring requirements) and `seed:dc-19-propose-tier` (a model risk tier's validation, review and monitoring requirements). **Proposed:** keep the register phrase double-quoted, and when the OpenLMP text is fixed let the explorer enforce PLAN-01 with a context pattern in `site/claims/do_not_publish.yaml`, for example `\bplans?\b[^.]{0,80}\bmonitoring requirements\b|\bmonitoring requirements\b[^.]{0,80}\b(land management|forest|2012-rule|1982-rule) plans?\b`. Fix-C can add it then.

6. **WF-02's "mixing" entry cannot be enforced.** WF-02's `do_not_say` reads "mixing with USDA OIG's 16% (different base)" with nothing quoted, so the new conflation check (lib/claims.mjs) has no term to match. RPT-05 already covers the same pair. **Proposed:** either quote it ("mixing with USDA OIG's '16%' (different base)") or leave RPT-05 as the enforcing row.

7. **Headcount measure implies precision.** The NPS and USFS headcount signals store `value: -0.25` with unit "share (upper bound: 'more than a quarter')". The explorer renders "-0.25 share (upper bound: 'more than a quarter')". PPS gives no exact figure, and −0.25 bounds the change from above, so the loss is at least a quarter. **Proposed:** set `value: null` and the unit to "more than a quarter (PPS gives no exact figure)", or label the value as a bound.

## What does not change

No explorer rule depends on these changes: each item fails closed or is labelled in the explorer today. When they land, the explorer needs no code change except dropping the "not yet re-graded" note (item 1) and adding the PLAN-01 context pattern (item 5).
