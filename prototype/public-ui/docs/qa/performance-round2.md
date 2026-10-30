# Performance, round 2: first load on slow networks

- **Author:** the performance engineer on the prototype team, an AI agent. Measured 30 October 2026, 22:25–23:30 UTC.
- **Problem (from `eval-round1-usability.md`, problem 1):** on Slow 3G with gzip, the route's H1 painted at 21–24 s; the old explorer takes 5.4 s. Budget: **8 s or less** for `#/` and a role page.
- **Result:** home H1 **4.9 s**, role H1 **7.8 s**, site chrome **4.9 s** on every route. Fast 3G: home 1.4 s, role 2.2 s.
- **Build measured:** `tools/build-app.mjs` inputs `d13793cf8a70bfd9` (including the coordinator's router, search, CSS and home edits).

## Results (gzip, cache disabled, 390 × 844)

Times are milliseconds from navigation. "Chrome" is when the styled site header is visible; before this round it appeared with the H1. "After" is the mean of 2 runs (the runs differed by 40 ms at most).

### Slow 3G (2,000 ms latency, 50 kB/s)

| Page | Before: chrome / H1 | **After: chrome / H1** | After: "Where it can lead" filled | Old explorer H1 |
|---|---|---|---|---|
| Home `#/` | 21,260 / 21,260 | **4,880 / 4,880** | | 5,449 |
| Role `#/role/rol-zjfcc09` | 21,232 / 23,795 | **4,856 / 7,792** | 11,669 (before 26,263) | |
| Role `#/role/rol-g0wbahh/federal` | 21,251 / 23,735 | **4,856 / 7,763** | 11,645 (before 26,207) | 5,413 |
| Competency `#/competency/cmp-vmk86p6` | 21,200 / 24,402 | **4,858 / 8,190** | | |
| What's changing `#/changing` | 21,245 / 24,294 | **4,857 / 8,037** | | |

### Fast 3G (562.5 ms latency, 180 kB/s)

| Page | Before: chrome / H1 | **After: chrome / H1** | Old explorer H1 |
|---|---|---|---|
| Home | 6,083 / 6,083 | **1,421 / 1,421** | 1,583 |
| Role `rol-zjfcc09` | 6,044 / 6,790 | **1,421 / 2,240** | |
| Role forester, federal | 6,065 / 6,805 | **1,419 / 2,243** | 1,586 |
| Competency | 6,086 / 7,012 | **1,421 / 2,349** | |
| What's changing | 6,091 / 7,050 | **1,416 / 2,323** | |

### Requests and bytes (Slow 3G run, gzip as transferred)

| Page | Before | After |
|---|---|---|
| Home | 38 requests, 260 KB | **11 requests, 234 KB** |
| Role | 40 requests, 296 KB | **13 requests, 270 KB** |
| Competency | 40 requests, 313 KB | **14 requests, 305 KB** |

App shell (HTML, CSS, JS, fonts and icons), gzip: **171 KB** of the 200 KB budget. `app.bundle.js` is 83 KB gzip (235 KB minified), down from 106 KB in 24 files.

## Method

The round 1 evaluator's `perf.js` (R4's method), unchanged in its essentials:
- **Throttling:** Chrome DevTools Protocol network emulation, with Slow 3G at 2,000 ms latency and 50 kB/s, and Fast 3G at 562.5 ms and 180 kB/s.
- **Cache:** disabled.
- **Viewport:** 390 × 844.
- **Server:** an in-process static server that gzips HTML, CSS, JS and SVG at level 6, because Python's `http.server` does not gzip.
- **H1 time:** when the route's `main h1` is in the DOM with a height, polled every 50 ms.

Added:
- **A stylesheet guard on the H1 time.** A prerendered H1 is in the DOM before the CSS arrives, so it counts only once the page's screen stylesheets have loaded. Until then the browser cannot paint it.
- **Chrome time.** When the styled header is visible.
- **"Where it can lead" time.** When the role page's `#paths` section stops being busy.

The script is kept as `tools/perf-first-load.cjs`. The "before" numbers came from the same script, run on the app as it stood at 22:25 UTC, before any change. They match round 1: 21.2 s and 23.7 s.

## Where the time went, and what changed

The bytes were never the problem. The problem was a chain of requests, each paying a 2 s round trip on Slow 3G. Under DevTools throttling, active downloads share the bandwidth equally. So once the chain is parallel, the H1 time is about two round trips plus all the bytes in flight divided by the bandwidth. Every extra KB (gzip) before the H1 costs about 20 ms on Slow 3G.

1. **One bundle.** esbuild bundles `main.js` and its 22 imports into `assets/js/app.bundle.js`: an ES module, minified, with a linked source map. The source map holds no sources; it points at the modules, which stay the source of truth. This replaces 24 requests discovered level by level.
2. **One stylesheet.** The 7 screen stylesheets are concatenated in their template order and minified into `assets/css/app.bundle.css`. The 8 links had exceeded Chrome's 6 connections per host. `print.css` stays separate, with `media="print"`.
3. **Head order (a new finding).** With a CSP `<meta>` in the page, Chrome did not fetch anything listed after a parser-blocking script until that script had run. We confirmed this by removing the meta in a test copy.
   - In practice, `core.js` and the bundle were requested 2.6 s late.
   - Every file the page fetches is now listed before `boot.js`, which comes last in `<head>`.
   - The template says so in a comment.
4. **`core.js` in parallel.** `<script src="data/core.js" defer fetchpriority="high">` sits in `index.html` before the module. Deferred scripts and modules run in document order, so `core` is registered before the bundle runs.
   - `lib/data.js` now also handles a data script that is still in flight. If a `<script src="data/X.js">` is already in the page and has no `data-done` mark, it waits for that script's load or error event. Only if the value is still missing does it add its own. This change runs to about 15 lines.
   - `boot.js` marks each data script with `data-done` when it loads or fails, using capture-phase listeners.
5. **Route data started early.** The build writes `<meta name="emst-early-data">`: a map from routes to data files, made from `core.js` with the same naming rules as `lib/data.js`.
   - It covers role pages, competency pages, What's changing and the HR pages.
   - `boot.js` reads the map and injects that one `<script src>` as soon as it runs, so the role file no longer waits for the bundle and `core.js`.
   - Data files, their names and their loading method are unchanged.
6. **Prerendered chrome and home page.** The build runs the real bundled app in Chromium at `#/` and copies the rendered `#site-top`, `#site-bottom` and `#main > .container` into `index.html`. Each top-level element is marked `data-prerender`.
   - `main.js` still replaces the chrome and the home page with identical live markup on boot. A pixel and computed-style comparison confirmed that the markup is identical.
   - On a deep link, `boot.js` adds `html.route-deep` before the first paint. One rule at the end of `app.css` then hides the prerendered home and shows a "Loading…" line in its place, using the router's own spinner markup. The home page therefore never flashes on a deep link.
   - With scripts off, the prerendered home is hidden too, and the `<noscript>` message shows as before.
7. **Fonts.** The `@font-face` rules move, unchanged, into `assets/css/fonts.bundle.css`, linked with `media="print"`. `boot.js` switches that stylesheet to `all`:
   - **at once on the home page**, so fonts load as before;
   - **on a deep link, once the route's H1 has rendered.** Otherwise the three font files, 64 KB, start at first paint and take bandwidth from the bundle and data at the end of the load. On the role page that cost 0.7 s: 8.44 s, or 8.53 s with the preload, against 7.72 s with the fonts deferred.
   - **The 400-weight preload is removed.** It put 21 KB in front of the H1: 8.17 s against 7.72 s.
   - **The italic face is kept and loads lazily.** `.level__none` uses it.
   - **`font-display: swap` is unchanged.** Text shows in the fallback font until the font arrives, so no paint ever waits for a font.
   - **With scripts off,** a `<noscript>` link loads the fonts.
8. **`paths.js` does not delay the role H1.** The role view calls `data.paths()` without awaiting it, and the call happens after `role.js` has its data. The request goes out with the H1's render, at 7.8 s on Slow 3G. Nothing awaits it, so `role.js` is not edited. The split below is proposed, not made.

### Waterfall after: role page, Slow 3G (seconds)

| File | Sent | Done | KB |
|---|---|---|---|
| `index.html` | 0.00 | 2.16 | 6.6 |
| `app.bundle.css`, `fonts.bundle.css`, `print.css`, `boot.js` | 2.08–2.10 | 4.14–7.14 | 17.5 |
| `data/core.js` | 2.10 | 6.90 | 60.0 |
| `app.bundle.js` | 2.10 | 7.77 | 83.5 |
| `data/role-rol-zjfcc09.js` (started by `boot.js`) | 4.95 | 7.53 | 10.3 |
| `icons.svg` | 4.95 | 7.17 | 2.4 |
| **H1 painted** | | **7.8** | |
| `data/paths.js`, then the three fonts | 7.81–7.84 | 11.55–11.70 | 89.8 |

Before, the chain was HTML, then `main.js`, then 21 modules level by level, then `core.js` at about 18 s, then the role file. In total there were 40 requests.

## Behaviour and accessibility checks

- **Rendered-page check:** `LIMIT=300 node prototype/public-ui/tools/check-rendered.mjs http://127.0.0.1:8841`, with the app served by the team's `serve.py`.
  - 300 routes, **0 console errors and 0 external requests**.
  - The rendered-text rules found nothing except the existing 121 "percent (review)" notes.
- **Production against development:** `index.html` and `dev.html` were compared on 10 routes, at 390 and 1280 px, in light and dark themes, after fonts had loaded.
  - Every element in `#app` has the **same computed style (colours, fonts, spacing) and position**: 40 of 40 pages, 122 to 3,959 elements each.
  - Full-page pixel diffs differ only by the page URL in the citation line and by sub-pixel shifts that come and go between runs.
- **Before boot and at boot:** 40 of 40 checks passed. The bundle was held back 2.5 s to create the window before boot.
  - **Chrome and home H1:** both visible before the bundle.
  - **Typing:** typing in the header search before boot keeps the text and the focus. The combobox then offers suggestions, the arrow keys work and Escape closes it.
  - **Enter before boot:** Enter does not leave the page. The search is sent again once the app is ready and opens `#/search`, with no CSP form-action error.
  - **Menu at 390 px:** it opens before boot, stays open after boot, and one click then closes it, with no double toggle.
  - **Focus:** focus reached with Tab before boot stays on the same control after boot. The first 25 tab stops are identical before and after boot.
  - **Scroll:** the scroll position on the home page is kept when it goes live.
  - **Deep links:** for role, role-with-employer and competency pages, the home page is hidden and "Loading…" is shown, with no H1. The route's data file is requested before the bundle arrives. `core.js` and the data file are each requested exactly once.
  - **A link followed before boot:** following the brand link shows the prerendered home. Navigation after boot moves focus to the H1.
  - **axe-core** (wcag2a, 2aa, 21a, 21aa, 22aa) found **0 violations** on the prerendered page before boot, on the live page, and on a deep link before boot.
- **Project rules:** still met.
  - The CSP `<meta>` is unchanged: `script-src 'self'`, with no inline script or style.
  - Every request is same-origin.
  - There is no `fetch`, storage or service worker.
  - The app has no `innerHTML`. The build reads `outerHTML` in Chromium at build time to serialise the prerender; nothing is parsed from strings at runtime.
  - `boot.js` never writes to `location`.

## Build steps

```sh
# once: install esbuild (exact version 0.28.2, pinned in tools/package.json and package-lock.json)
cd prototype/public-ui/tools && npm ci --ignore-scripts && cd -
# after any change to a module, a stylesheet, tools/index.template.html or app/data/core.js
node prototype/public-ui/tools/build-app.mjs                 # bundle, CSS, fonts CSS, dev.html, index.html with prerender
node prototype/public-ui/tools/build-app.mjs --check         # exit 1 if index.html or the bundles are older than their sources
node prototype/public-ui/tools/build-app.mjs --no-prerender  # without Chromium: empty chrome containers
```

- **esbuild installs without its postinstall script.** `npm ci --ignore-scripts` works with esbuild 0.28.2, which we checked from a clean directory. The binary ships in the platform package `@esbuild/linux-x64`, which the JS API finds on its own. The postinstall step only checks the binary and links it into `esbuild/bin` for speed. `tools/.gitignore` excludes `node_modules/`.
- **Edit the template, not the pages.** The page shell lives in `tools/index.template.html`. The build writes two pages from it:
  - **`app/index.html` (production):** the bundles, the early-data map and the prerender, stamped with a hash of its inputs;
  - **`app/dev.html` (development):** the unbundled `main.js` and each stylesheet. View developers should use `dev.html` so their edits show without a rebuild.
- **Rebuild after the data rebuild.** The prerender, the early-data map and the stamp are computed from `app/data/core.js` on every build, and nothing is hard-coded. After `build-data.mjs` runs, run `build-app.mjs` again so the prerendered release strip, the home figures and the map match the new data.
- **Measure again:** `node prototype/public-ui/tools/perf-first-load.cjs <label> slow3g 1 2 home,role,comp`.

## Risks and proposals

- **The role page has about 0.2 s of headroom.** Its critical path is HTML, CSS, `boot.js`, `core.js`, the bundle and the role file, about 180 KB gzip.
  - At about 20 ms per KB, roughly 10 KB more of app code or `core.js` would break 8 s.
  - The bundle grew by 4 KB gzip while this work was under way.
  - Recheck with `perf-first-load.cjs` before each research session.
  - The competency page (8.2 s) and What's changing (8.0 s) are already at the line.
- **Proposal for the lead: adopt the prerendered chrome.** `main.js` could attach its listeners to the prerendered chrome instead of replacing it. That would remove the bridge code in `boot.js`. It would also stop screen readers seeing the chrome nodes swapped once at boot, though they are identical.
- **Proposal for the lead and design: split the views.** Per-view code splitting would need dynamic `import()`, which DESIGN_SPEC §0 currently forbids. It would take about 30 KB gzip of other views off every first view.
- **Proposal for the data engineer: split `paths.js` by origin role.** The file is 676 KB raw and 26 KB gzip, and every role page loads all of it.
  - **Sizes:** split by origin role, the largest file is 4.7 KB gzip (133 KB raw, field resource technician) and the median is 2.6 KB. With only the fields the role view uses, the median is 0.3 KB.
  - **Slow 3G:** "Where it can lead" would fill about 1.5 s sooner, at about 10 s instead of 11.7 s.
  - **Without gzip,** 676 KB raw costs 13.5 s of transfer on Slow 3G.
  - **Who must change what:** Compare needs the edges in both directions, so it would load two files, or keep the whole file. That is a change to `compare.js` (developer C), so the split was not made in this round. The data build is also being changed by others right now.
  - **Suggested shape:** `build-data.mjs` writes `paths-<role>.js` registering `paths:<role>` and keeps `paths.js` until Compare moves. `lib/data.js` gains `pathsFrom(slug)`, and `role.js` changes one line.
