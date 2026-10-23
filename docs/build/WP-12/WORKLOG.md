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
- 15:10 Scaffolded `site/` (Eleventy 3.1.6, USWDS 3.14.0, axe-core 4.14.0, playwright-core 1.63.0, js-yaml 4.1.1; exact pins,
  `npm install --ignore-scripts`; versions chosen at least 14 days old except where noted in the security packet).
  `tools/prepare-release.mjs` (preview build into `.cache/release`, WP-05 venue prototype into `.cache/venue`),
  `tools/vendor.mjs` (USWDS stylesheet + the 50 files it references; refuses external URLs), `tools/sbom.mjs`
  (`npm sbom` CycloneDX 1.5, runtime and build trees), `tools/serve.mjs` (127.0.0.1 only, no logging, security headers).
- 15:40 `lib/model.mjs`: view model from bundle + computed views; display gate fail-closed; v1 values only as task
  drawer rows; module records flagged; federal applicability only from the computed venue view.
- 16:10 Pages: home, roles (index, role, variant = View 1), gap check (index, chosen-competency mode, per-variant,
  team grid = View 2), pathways (index with X11 translation seed, per-variant = View 3), what's coming (View 4),
  federal series (index + 79 profiles), state and local classes (index + 38 views), competencies (index + 232 pages),
  module sections, evidence, challenge, privacy, accessibility, security, download, search, 404. First build: 382 pages
  in about 3 s. WP-08 roles not yet present: empty states render.
- 16:40 `tools/check-output.mjs` (static: fetches, CSP, JS APIs, release ID, notice, figure badges, v1-drawer
  containment, claims hygiene, Tribal triggers outside policy text, held keys, personal data, HR disclaimers,
  "assessment pending", pathway notice) and `tools/test-checks.mjs` (16 seeded violations, each detected).
  `tools/browser-checks.mjs` (playwright-core + local Chromium + axe-core 4.14.0): network capture, axe WCAG 2.2
  A/AA (details closed and open), reflow at 320 px, focus visibility, gap-check save/clear/reopen round trip with a
  sentinel note, team-grid minimum cell of 5, search without requests. First full run: 0 axe violations on 50 pages.
- 16:50 WP-08 roles appeared (37 RoleProfiles, variants in core and module areas). Rebuilt the preview release
  (10,749 records; held 122, third-party-index 102, placeholder targets 57 excluded by the release gate). Role, variant,
  gap-check and pathway pages now generate (839 pages).
- 17:10 Fixes from review of WP-08 data and notes: (a) credential gates and sign-off are verified facts (SPEC §10.5
  rule 8): shown only when the credential issuer is verified (19 of 93), otherwise counted as "not shown"; (b) time
  shares renormalized within each role level (WP-08 note); (c) WP-08's task-level "reshaping claims" and
  externalContext are NOT rendered: the former are agent change judgments without a multi-rater study (display gate:
  agent values never render), the latter are third-party-licensed values excluded from release outputs; (d) pathways
  grouped by destination role with per-sector variants; (e) Federal Series Profile and State Class View pages now
  render WP-08's generated views (`docs/build/WP-08/generated/`, rules proposed in CR-FH-001), every ID re-checked
  against the release bundle; module or non-established content goes into a collapsed, labelled section (ADR-0018:
  modules out of default HR views; applied to competency content, not to module-homed roles themselves).
