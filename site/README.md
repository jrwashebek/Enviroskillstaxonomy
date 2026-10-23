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
| 1 | `tools/prepare-release.mjs` | Runs `scripts/build_release.py --profile preview` into `.cache/release/` unless the cached build is newer than `data/`, `vocab/`, `scripts/` and `validation/display_gates.yaml`. It takes a few minutes on first run. If a fresh build fails, the previous one is kept and every page shows a build warning. It also prepares two computed views, each labelled as a stop-gap (CR-CP-001): the federal-applicability view (WP-05 prototype), and the WP-08 generated HR views (read-only). |
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

`tools/test-checks.mjs` seeds 16 violations into a fixture page and confirms that the checker reports each one.

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
| **View 1: How this role is changing** | `/roles/<role>/<variant>/` | `RoleProfile`, `RoleVariant`, `Task`, display gate view, v1 `ExposureAssessment` (drawer only), watch signals, instruments |
| **View 2: Gap check** (local-only) | `/gap-check/<role>/<variant>/`, `/gap-check/competencies/`, `/gap-check/team/` | competency targets, indicators |
| **View 3: Where it can lead** (exploratory) | `/pathways/<role>/<variant>/`, `/pathways/` | computed overlaps between draft role profiles, X11 translation seed, frictions and pathways when present |
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
- **Module content out of default HR views.** Module and non-established competency content is kept out of the default HR views and placed in a collapsed, labelled section.
- **Credentials never stated as requirements.** Credential gates are never presented as requirements. A credential appears as "may be involved (agent-drafted link)" only when its issuer is verified; others are counted, not shown.
- **Proposed realignments.** Series that OPM has proposed for realignment read "proposed, not final".
- **No recommended pathways.** Pathways are never "recommended".

## Placeholders and limits

- **Preview profile.** No IDs are minted yet, so the explorer shows release `2.0.0-dev` built with the internal preview profile, which includes drafts. Every page says so.
- **No v2 assessments.** No v2 multi-rater assessment exists, so every "how is this changing" value is "assessment pending".
- **No external context.** External index context is absent: those records are third-party licensed and excluded from releases.
- **Stop-gap computed views.** Federal applicability (WP-05 prototype) and the HR views (WP-08 generators) are stop-gaps until `build_release.py` emits them (CR-CP-001).
- **Exports.** Exports are CSV and print-to-PDF. DOCX exports (IDP, PD skeleton) are not built.

Licence: Apache-2.0 for this code; data and standard text CC0 1.0. USWDS is in the public domain, with its fonts under the SIL Open Font License.
