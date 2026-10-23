# WP-12 worklog — Product: explorer and views (A10a, CP)

Started 2026-10-23 (S2). Agent `emstagent:A10a-CP@wp-12` (model claude-opus-5-5). Lane: `site/`, `docs/build/WP-12/`,
`docs/decisions/change_requests/CR-CP-NNN.md`. No edits to `data/`, `schema/`, `scripts/`, `vocab/`.

## Inputs read
CHARTER, TEAM_BRIEF, PHASE4_BUILD_PLAN §1 and WP-12, ADR-0012, ADR-0015, ADR-0016, ADR-0027 (+ CR-LM-002/CR-IO-002
amendments), PROJECT_LEAD_DECISIONS (Q4 default, Q7), `validation/display_gates.yaml`, my Phase 2 `mvp_spec.md`,
AUTHORING_GUIDE, `scripts/build_release.py`, the "For WP-12" notes in WP-03, WP-05, WP-06, WP-07 worklogs
(WP-04 and WP-09 have none addressed to WP-12; their hand-offs were read for context).

## Design decisions (with reasons)
- **Data path.** The site never reads `data/v2/` directly. `npm run build` runs `scripts/build_release.py --profile
  preview` into `site/.cache/release/` (or uses `EMST_RELEASE_DIR`), then generates pages from the bundle and the
  computed views (`views/display_gate.json`, `effective_use_tier.json`, `change_indicators.json`,
  `inverse_links.json`, `assessment_staleness.json`). So the release gate (Tribal hold, third-party licence,
  quarantine, placeholder targets) is applied before any page exists. Preview profile is required because nothing is
  minted yet; every page says so.
- **Search: Pagefind replaced by a whole-index local search.** Pagefind fetches index chunks and result fragments
  chosen by the query, so a static host's access log would see query-derived requests. That breaks "no network request
  carries user-entered data" (ADR-0012 standing rules). The explorer loads one prebuilt index file before the user
  types and matches in the browser. Deviation from `mvp_spec.md` §8 recorded here and in the security packet.
- **No browser storage.** Gap-check ratings live in memory and leave only as a file the user saves. No localStorage
  draft (spec allowed one); a leave-page warning protects unsaved work.
- **Federal applicability.** No computed `venueApplicability` view exists in `build_release.py` yet (CR-SC-001 pending).
  The site reads `views/venue_applicability.json` if the release has it, else the WP-05 prototype computed view, labelled
  as a prototype; never from records. CR-CP-001 asks DE to port it.

## Log
