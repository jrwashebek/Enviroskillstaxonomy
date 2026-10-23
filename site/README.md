# EMST Explorer (Tier 1, static and local-first)

The EMST Explorer is the public explorer for the Environmental Management Skills Taxonomy (work package WP-12; ADR-0012 Tier 1; ADR-0027). It is a set of pre-rendered pages generated from one EMST release build. It has:

- no server code and no accounts;
- no cookies, no browser storage and no analytics;
- no runtime third-party requests;
- no user input in URLs.

The gap check runs in the browser, and results leave the page only as a file the user saves.

## Build and view

You need Node 22, Python 3 with the repository's requirements, and this repository checked out.

```bash
cd site
npm ci --ignore-scripts      # exact pins from package-lock.json; lifecycle scripts never run
npm run build                # release build -> vendor USWDS -> SBOM -> pages -> output checks
npm run serve                # http://127.0.0.1:8080/  (local only, no logging)
npm test                     # seeded-violation test of the checker, output checks, browser checks
```

Without Node 22 on `PATH`, prefix the commands with `PATH=/opt/node22/bin:$PATH` (or wherever Node 22 is installed).

What `npm run build` does:

| Step | Script | What it does |
|---|---|---|
| 1 | `tools/prepare-release.mjs` | Runs `scripts/build_release.py --profile preview` into `.cache/release/` unless the cached build is newer than `data/`, `vocab/`, `scripts/` and `validation/display_gates.yaml`. It takes a few minutes on first run. If a fresh build fails, the previous one is kept and every page shows a build warning. It also prepares two computed views until the release emits them (CR-CP-001 A1–A2): federal applicability, computed by `tools/venue_view.py` with DE's registered rule venue-applicability@1.0.0 over the release records (the WP-05 prototype is only a fallback, and never shows "required basis"); and WP-08's generated HR views, read-only, with every ID re-checked against the bundle. |
| 2 | `tools/vendor.mjs` | Copies the USWDS 3 stylesheet and the 50 files it references into `src/assets/vendor/`. It refuses any stylesheet that references an external URL. |
| 3 | `tools/sbom.mjs` | Writes two CycloneDX 1.5 SBOMs (runtime and build) with `npm sbom`. |
| 4 | `tools/clean.mjs`, then Eleventy | Writes the site to `_site/`. |
| 5 | `tools/check-output.mjs` | Static checks on the built output. The build fails on any problem. On success it writes `_site/download/security/SITE_SHA256SUMS`. |

To build from a tagged release instead of the preview, run `EMST_RELEASE_DIR=../dist/2.0.0-rc.1 npm run build`. Nothing is rebuilt; the pages then show that release ID.

To rehost under a sub-path such as `/emst/`, run `EMST_PATH_PREFIX=/emst/ npm run build`.

`npm run build:portable` writes relative links, so the `_site/` folder also works when opened from disk.

## The test that greps for external fetches

`npm run check` (part of `npm run build` and `npm test`) reads every built file and fails on any of the following:

- **External URLs in fetching attributes.** An absolute or protocol-relative URL in `src`, `srcset`, `poster`, `data`, `action`, `formaction`, `ping`, `manifest`, `background` or `<link href>`.
- **Embedding elements.** Any `<iframe>`, `<embed>`, `<object>`, `<base>` or meta refresh.
- **External loads in CSS.** A CSS `url()` that points to another site, or any `@import`.
- **Network or storage code in JavaScript.** Shipped JavaScript that uses a network, storage or address-bar API: `fetch`, `XMLHttpRequest`, `sendBeacon`, `WebSocket`, `EventSource`, dynamic `import()`, a service worker, `localStorage`/`sessionStorage`/`indexedDB`, `document.cookie`, `history.pushState`, location writes or image beacons.
- **Absolute URL literals in JavaScript.**
- **Inline scripts and handlers.** Inline executable `<script>`, inline event handlers, or inline styles.
- **A missing or weakened CSP.** A page without the CSP `<meta>` containing `default-src 'self'`, `connect-src 'none'` and `form-action 'none'`.

Ordinary `<a href>` links to other sites, such as citations and official class specifications, are navigations the user chooses. They are counted, and they may not carry query strings.

The same script also runs the claims-hygiene and display rules:

- release ID and the use notice on every page;
- a use-tier badge and an evidence badge on every figure;
- v1 codes only inside the v1 evidence drawer;
- the three-part HR disclaimer on series, class and federal or state variant pages;
- "assessment pending" on role-change pages;
- "never a recommendation" on pathway pages;
- no retired claims (ADR-0027 §3);
- no Tribal-hold trigger terms outside marked policy statements;
- no held seed key;
- no e-mail addresses or phone numbers.

It also enforces the WP-15 sign-off (`docs/methods/WP15_SIGNOFF.md`, `docs/methods/claims_register.csv`):

- **Unverified or held register rows are mapped.** Every unverified or held row the explorer uses must be mapped in `claims/register_map.yaml`, and so must every signal that cites one of those rows' sources.
- **Unverified records are labelled or withheld.** Every mapped instrument title is followed by "Unverified — not for citation". A mapped signal is withheld entirely and only counted ("2 unverified signals withheld"), because a signal's headline is itself the claim (package review issue 2); if its title ever renders, the label must follow it.
- **Judgment dates do not appear.** Event days dated by judgment (REG-08) never appear.
- **Wrong forms fail the build.** No `do_not_say` wrong form appears. `lib/claims.mjs` parses the column (shared with the view model): single-quoted phrases of 12 or more characters fail anywhere; an item that starts "mixing …" (RPT-05: USDA OIG's 16% with PPS's 'more than a quarter') fails only where all its terms share one sentence, table cell or list item without a phrase such as "different base"; double-quoted phrases are recorded but not enforced while data still uses them, and the check lists where they still render. The context patterns in `claims/do_not_publish.yaml` cover short forms such as 'realigned' or 'final'.

`tools/test-checks.mjs` seeds 21 violations into a fixture page and confirms that the checker reports each one. It also checks five near-misses that must pass: 'more than a quarter' alone, the 16% figure distinguished from it, the two in separate sentences or table cells, and a double-quoted (deferred) register phrase, which must be reported but not fail.

`tools/browser-checks.mjs` loads 50 pages in a local Chromium (playwright-core with the browsers in `PLAYWRIGHT_BROWSERS_PATH`). On each page it:

- records every network request;
- runs axe-core against WCAG 2.0, 2.1 and 2.2 A/AA, with every disclosure closed and then open;
- checks reflow at 320 CSS px;
- checks that focus is visible on the first 12 Tab stops.

It also exercises the tools end to end:

- **Gap check.** It rates competencies, types a sentinel note, saves, clears and reopens the file. It asserts no request, no address-bar change, no cookie or storage, and that the sentinel appears only in the downloaded file.
- **Team grid.** It checks the minimum cell of 5: 4 files show nothing, 5 files show counts.
- **Search.** It checks that typing makes no request.

Reports are written to `reports/`.

## What is in the explorer

| View | Pages | Source in the release |
|---|---|---|
| **View 1: How this role is changing** | `/roles/<role>/<variant>/` | `RoleProfile`, `RoleVariant`, `Task`, display gate view, v1 `ExposureAssessment` (drawer only), watch signals, instruments (typed links and sensitivity edges); summary per role-change@0.1.0 |
| **View 2: Gap check** (local-only) | `/gap-check/<role>/<variant>/`, `/gap-check/competencies/`, `/gap-check/team/` | competency targets, indicators |
| **View 3: Where it can lead** (exploratory) | `/pathways/<role>/<variant>/`, `/pathways/` | pathway-edges@0.1.0 overlaps between draft role profiles, X11 translation seed, frictions and pathways when present |
| **View 4: What's coming** | `/whats-coming/` | watch items, emerging and proposed roles (P3 roles appear only here) and competencies, signals, change indicators, instruments and dated events, signposts, scenarios, no-regret moves |
| **Federal Series Profile** | `/federal-series/<code>/` | series register, X4, WP-08 generated profiles |
| **State Class View** | `/state-classes/<class>/` | state-class register, X5, WP-08 generated views |
| Competencies, modules, evidence, privacy, accessibility, security, download, search | | |

## Rules the pages follow

These are enforced in `lib/model.mjs` and checked in `tools/check-output.mjs`.

- **Only release records.** Pages are built from the release bundle, so held, third-party-licensed, quarantined and placeholder records never reach a page. IDs named by stop-gap views are re-checked against the bundle.
- **Fail-closed display gate.** A rated value renders only if `views/display_gate.json` says production or tentative. Otherwise the page shows IO's label text from `validation/display_gates.yaml`. No v2 study has reported yet, so every task says **assessment pending**. LLM craft and work-function ratings never render.
- **v1 values only in the drawer.** v1 analyst values appear only in each task's evidence drawer, labelled "v1 single-analyst prior, LLM-assisted, unvalidated — not for decisions". They are never counted and never used in a headline.
- **Badges on every figure.** Every figure carries a use-tier badge and an evidence badge. Agent drafts say so.
- **Computed federal applicability.** It is read only from the computed view, and nothing is excluded (Q4 default).
- **Module content out of default HR views** (CR-CP-001 ruling B5). Cross-role lists show core content only. Role-scoped views (role page, Federal Series Profile, State Class View) show the role's home-module content labelled "editorial section, not a stewarded module". Other modules and non-established items are placed in a collapsed, labelled section.
- **Editorial design values versus job-analysis values** (CR-CP-001 ruling B4; display-gate@1.1.0). Bundle membership, role levels, formation flags and target levels show as "editorial draft". Importance, time share, critical, needed-at-entry and distinguishing show "Assessment pending (job analysis)". View 1 counts tasks rather than shares. HR views list duties without percentages ("% time: set by the supervisor; EMST supplies none before job analysis"). The gap check ranks by gap size alone.
- **Claims register.** Instruments tied to unverified register rows show only their title and "Unverified — not for citation"; signals tied to them are withheld and counted. Signal direction and driver tags are agent drafts and are not shown. P3 roles appear only in What's coming.
- **Signals on role pages.** A role-change page lists signals about the role, its variant or its primary work function. Signals about an employer type as a whole (for example agency headcounts) are counted there and listed in What's coming (package review issue 31). Reliability grades are shown as set by the agent that entered the signal.
- **Federal applicability is computed.** Only instruments linked as *requiring* the work decide the value (venue-applicability@1.0.0). The WP-05 prototype fallback never shows "required basis" (CR-CP-001 ruling A1).
- **Credentials never stated as requirements.** Credential gates are never presented as requirements. A credential appears as "may be involved (agent-drafted link)" only when its issuer is verified in the release bundle; others are counted ("n credential gates not shown until the issuer is verified"). WP-08 views carry gates as `{shown, notShownUntilIssuerVerified}`; the explorer re-checks every shown gate against the bundle and adds the generator's withheld count.
- **Proposed realignments.** Series that OPM has proposed for realignment read "proposed, not final".
- **No recommended pathways.** Pathways are never "recommended".

## Placeholders and limits

- **Preview profile.** No IDs are minted yet, so the explorer shows release `2.0.0-dev` built with the internal preview profile, which includes drafts. Every page says so.
- **No v2 assessments.** No v2 multi-rater assessment exists, so every "how is this changing" value is "assessment pending".
- **No external context.** External index context is absent: those records are third-party licensed and excluded from releases.
- **Stop-gap computed views.** Federal applicability (registered rule run by the explorer over the release) and the HR views (WP-08 generators) are stop-gaps until `build_release.py` emits them (CR-CP-001 A1–A2, accepted).
- **Job-analysis values hidden.** Importance, time shares, critical and needed-at-entry flags stay hidden until reviewed (CR-CP-001 B4). Role-change summaries are task counts.
- **Not for external publication yet.** The WP-15 sign-off covers internal drafts and the NGO-pilot preview only, pending the remaining co-signature and the re-checks.
- **Authorship, status and comments.** Every page footer carries the package authorship statement (AI agents, working to a charter set by the EMST project lead; no independent human expert review yet) and the one call to action, a link to the repository's GitHub Issues page. The home page carries the package status line.
- **Exports.** Exports are CSV and print-to-PDF. DOCX exports (IDP, PD skeleton) are not built.

Licence: Apache-2.0 for this code; data and standard text CC0 1.0. USWDS is in the public domain, with its fonts under the SIL Open Font License.
