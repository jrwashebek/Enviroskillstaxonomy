# EMST design system

The visual and interaction layer for the EMST public interface prototype. It sits beside `DESIGN_SPEC.md` (what to build), `DATA.md` (data shapes) and the content guide (words).

- **See it:** `app/gallery.html`. Serve `app/` over HTTP (for example `python3 -m http.server -d app`), because Chromium will not load an external SVG sprite from `file://`.
- **Check it:** `node tools/check-contrast.mjs` (exit 1 on any failure).
- **Reference behaviour:** `app/assets/js/gallery.js` implements the combobox, tabs, sortable table, copy, print and theme switch. Port the logic into `ui.js` and `main.js` with `h()`; the gallery script is not loaded by the app.

## Contents

1. [Principles](#1-principles)
2. [Files, loading and budgets](#2-files-loading-and-budgets)
3. [Tokens](#3-tokens)
4. [Type](#4-type)
5. [Layout](#5-layout)
6. [Icons](#6-icons)
7. [Components](#7-components) (header, search, navigation, footer, page header, status line, on this page, cards, figures, badges, pending, evidence ladder, use-tier path, level chips and ladder, tabs, drawers, data table, comparison, notices, buttons and links, filters, empty and loading)
8. [Print](#8-print)
9. [Accessibility checklist](#9-accessibility-checklist)
10. [Mapping to `ui.js`](#10-mapping-to-uijs)
11. [Known limits](#11-known-limits)

---

## 1. Principles

EMST is a field notebook for a whole sector, written in pencil. Beyond being clear, the interface has one job: to show how sure we are about each thing on the page, without burying people in disclaimers.

| Visual rule | Meaning | Where |
|---|---|---|
| **Dotted outline and pen mark** | Drafted by AI agents and not reviewed ("pencil"). | `.badge--draft`, `.notice--draft`, release strip |
| **Hatched area, dashed outline, hourglass, words** | A value held back until a reliability study passes ("unsurveyed ground"). Never a zero, never a blank. | `.pending`, `.pending--block` |
| **Dashed outline and lock** | A use that this release does not support (develop, select). | `.tier--locked`, `.is-locked` ladder steps, disabled buttons |
| **Solid line** | Done or established. Reviewed work will be drawn in solid ink when it exists. | ladder done steps, `.badge--ok` |
| **Double rule** | Held with respect: the Tribal content hold. Quiet, never an error style. | `.notice--hold` |
| **Square corners** | A label you read. | `.badge` and its variants |
| **Round (pill) corners** | A chip you can press. | `.chip`, `.chip-remove` |
| **Ruled margin** | Wide pages keep navigation and record facts in a margin column, ruled off by one light-green line. | `.with-margin` |

Colour only reinforces. Every status reads correctly in greyscale, in print and in Windows high contrast (`forced-colors`).

**Not a government site.** There is no ".gov" banner, eagle, seal or agency blue. The footer says EMST is independent and not endorsed by any agency. The calm, ruled, plain look is meant to be familiar to federal and state HR users without implying endorsement.

---

## 2. Files, loading and budgets

```
app/assets/css/tokens.css      fonts and design tokens (light, dark)
app/assets/css/base.css        reset, type, links, focus, layout primitives
app/assets/css/components.css  every component below
app/assets/css/print.css       print only
app/assets/fonts/              4 WOFF2 files and their OFL licences
app/assets/icons.svg           sprite: 43 symbols, 24px grid, 2px stroke
```

In every page `<head>`, in this order:

```html
<link rel="preload" href="assets/fonts/public-sans-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/tokens.css">
<link rel="stylesheet" href="assets/css/base.css">
<link rel="stylesheet" href="assets/css/components.css">
<link rel="stylesheet" href="assets/css/print.css" media="print">
```

Add `class="js"` to `<html>` from the boot script (`document.documentElement.classList.add("js")`). Only the mobile navigation toggle depends on it; without it the navigation list is always shown.

**Theme.** Light is the default. Dark follows the device (`prefers-color-scheme: dark`). To force a theme, set `data-theme="light"` or `data-theme="dark"` on `<html>`. Do not store the choice (no storage is allowed); the gallery switch is for review only.

**Budgets (measured on 30 October 2026):**

| Asset | Size | Budget |
|---|---|---|
| CSS, 4 files, uncompressed | 39.9 KB (tokens 4.7, base 5.2, components 27.0, print 3.0) | ≤ 40 KB |
| Fonts, 4 WOFF2 files | 85 KB (Public Sans 400, 400 italic, 600; Merriweather 400) | ≤ 160 KB |
| Icon sprite | 11 KB | |

The CSS is written one rule per line to stay within budget. Any new rule must fit the budget: reuse a component before adding one.

---

## 3. Tokens

All colours are hex so that `tools/check-contrast.mjs` can compute every pair. Never write a raw colour in a component; use a token.

### 3.1 Naming rules (the contrast check depends on them)

| Pattern | What it is | Checked against | Minimum |
|---|---|---|---|
| `--bg`, `--bg-*` | Page surfaces | | |
| `--fg`, `--fg-*` | Text usable on any surface | every `--bg*` and every `--st-*-bg` | 4.5:1 |
| `--ui-*` | Non-text marks (borders of controls, focus ring, rails, fills) | every `--bg*` | 3:1 |
| `--G-fg*`, `--G-bg*`, `--G-ui*` | A group G (for example `header`, `btn-primary`, `sel`, `focus`, `hbtn`) | each other within G | 4.5:1 text, 3:1 marks |
| `--st-*-fg`, `--st-*-bg` | Status groups (`ok`, `info`, `warn`, `danger`, `draft`) | within the group, and the fg on every `--bg*` | 4.5:1 |
| `--deco-*` | Decorative lines and shadows. Never carries meaning. | exempt | |
| `--cat-*` | Chart slots | the dataviz palette validator | see 3.4 |

The check also fails if the two dark blocks differ, if one theme lacks a token the other has, or if a stylesheet uses a custom property that `tokens.css` does not define. Result on 30 October 2026: **180 pairs, 0 failures**. The closest pair is `--ui-border` on `--bg-hatch` (3.38:1 light, 3.42:1 dark).

### 3.2 Colour

The brand family (forest ink `#16241E`, green `#2E6B50`, light green `#8FC2A6`, paper `#F5F3EC`, rule `#D6DBD2`) is kept. The muted text is darkened from `#5B6660` to `#4E5A54`, and links to `#22573E`, so that text keeps at least 5.9:1 on every light surface for crews reading phones in sunlight. The dark theme is derived, not inverted: the brand ink becomes the dark card surface, the light green becomes the primary, and a warm amber marks focus.

| Token | Light | Dark | Use |
|---|---|---|---|
| `--bg` | `#F5F3EC` | `#0E1713` | Page |
| `--bg-surface` | `#FFFFFF` | `#16241E` | Cards, tables, inputs, panels |
| `--bg-wash` | `#ECEAE1` | `#1B2B24` | Footer, release strip, row hover |
| `--bg-tint` | `#E4EFE8` | `#1F3A2E` | Selected, current, active option |
| `--bg-hatch` | `#DEDACD` | `#2B4136` | Hatch lines of pending (text sits on it) |
| `--fg` | `#16241E` | `#EEF1EA` | Text |
| `--fg-muted` | `#4E5A54` | `#AEB9B2` | Secondary text |
| `--fg-link` | `#22573E` | `#9FCDB3` | Links |
| `--ui-border` | `#6B766F` | `#85938B` | Control outlines, dashed and pending outlines |
| `--ui-primary` | `#2E6B50` | `#8FC2A6` | Current markers, rails, primary fills |
| `--ui-strong` | `#16241E` | `#EEF1EA` | Heavy rules, done steps, the E mark |
| `--ui-focus` | `#16241E` | `#FFC85C` | Focus ring |
| `--header-bg` / `--header-fg` / `--header-fg-muted` / `--header-ui` | `#16241E` / `#F5F3EC` / `#B8C4BD` / `#FFC85C` | `#16241E` / `#EEF1EA` / `#AEB9B2` / `#FFC85C` | Ink header; amber focus ring in it |
| `--hbtn-bg` / `--hbtn-fg` | `#8FC2A6` / `#16241E` | `#8FC2A6` / `#0E1713` | Search button in the header |
| `--btn-primary-bg` / `-bg-hover` / `-fg` | `#2E6B50` / `#245A42` / `#FFFFFF` | `#8FC2A6` / `#A9D3BC` / `#0E1713` | Primary button, target rung |
| `--sel-bg` / `--sel-fg` | `#2E6B50` / `#FFFFFF` | `#8FC2A6` / `#0E1713` | Selected chip |
| `--focus-bg` / `--focus-fg` | `#FFD873` / `#16241E` | `#FFC85C` / `#0E1713` | Highlighter on focused links, skip link |
| `--st-ok-*` | `#E3F0E7` / `#1F5A3E` | `#173326` / `#9FD3B4` | Established |
| `--st-info-*` | `#E3EEF3` / `#1D5873` | `#142A35` / `#9CCBE3` | Emerging, info notice |
| `--st-warn-*` | `#FAEFD2` / `#7A4D00` | `#2D2410` / `#F0C46A` | Watch, caution notice |
| `--st-danger-*` | `#F8E4DE` / `#9B2C1F` | `#351B16` / `#F4A99A` | Form errors only (none in the prototype yet) |
| `--st-draft-*` | `#FFFFFF` / `#474D53` | `#16241E` / `#C5CBD0` | AI-drafted ("pencil" graphite) |
| `--deco-rule` | `#D6DBD2` | `#2E3F37` | Hairlines |
| `--deco-rule-strong` | `#16241E` | `#4F7A64` | Rule under the navigation, over the footer |
| `--deco-margin` | `#8FC2A6` | `#3B6B53` | The margin rule |

### 3.3 Space, shape, motion

| Token | Value | Notes |
|---|---|---|
| `--sp-h` `--sp-1` `--sp-2` `--sp-3` `--sp-4` `--sp-5` `--sp-6` `--sp-8` | 4, 8, 16, 24, 32, 40, 48, 64 px | 8px grid; `--sp-h` is the half step for tight insides. Components use the same values as rem literals to save bytes. |
| `--r-tag` / `--r-ctl` / `--r-pill` | 2px / 4px / 999px | Labels / controls and boxes / pressable chips |
| `--focus-w` | 3px | Focus ring width (offset 2px) |
| `--target-min` / `--target-touch` | 24px / 44px | Minimum target / primary touch controls |
| `--measure` | 68ch | Prose width |
| `--page-max` / `--gutter` / `--margin-col` | 76rem / 16–32px / 15rem | Page frame |
| `--dur-2`, `--ease` | 220ms | Only the drawer chevron moves; reduced motion turns it off |

### 3.4 Chart colours (`--cat-1` … `--cat-6`)

For charts that need categories, such as the six employer types. Assign in this order and never cycle: 1 federal, 2 state, 3 local, 4 NGO, 5 private, 6 academic.

| Slot | Light | Dark |
|---|---|---|
| 1 green | `#067D4D` | `#3FA270` |
| 2 blue | `#2365A8` | `#5890CD` |
| 3 rust | `#C25430` | `#D26A49` |
| 4 violet | `#5E499D` | `#8271C2` |
| 5 ochre | `#C89522` | `#B78A2C` |
| 6 plum | `#A64C88` | `#BA649C` |

Validated with the dataviz `validate_palette.js` on 30 October 2026, with this order chosen by enumerating every order with green first:

- light, on `#FFFFFF` and on `#F5F3EC`: all checks pass; worst adjacent CVD ΔE 16.8, normal-vision ΔE 18.1. Slot 5 is 2.7:1 on white, so a chart using it must carry direct labels or its table.
- dark, on `#16241E` and on `#0E1713`: all checks pass; worst adjacent CVD ΔE 14.7, normal-vision ΔE 16.8; all slots at least 3:1.
- Under all-pairs (scatter, maps, small multiples), only slots 1 and 2 may appear together: green and rust collapse for protanopes (ΔE 4.6). With more series, facet the chart instead.

Every chart also needs a table (spec R-rule) and direct labels; colour is never the only key.

---

## 4. Type

- **Public Sans** (400, 400 italic, 600) for everything people read and use.
- **Merriweather** (400) for page and section titles (h1, h2), the brand name, citations and big figures. It is the field-guide voice, and is used sparingly.
- No monospace face is shipped. Codes and IDs use Public Sans with tabular figures (`.id`, `.num`).

| Role | Element or class | Size (320 → 1280px) | Face |
|---|---|---|---|
| Display (home only) | `.display` | 36 → 56 | Merriweather 400 |
| Page title | `h1`, `.h1` | 30 → 44 | Merriweather 400, line height 1.15 |
| Section title | `h2`, `.h2` | 24 → 32 | Merriweather 400 |
| Sub-section | `h3`, `.h3` | 20 → 24 | Public Sans 600 |
| Small heading, card title | `h4`, `.h4` | 18 → 20 | Public Sans 600 |
| Lede | `.lede` | 18 → 20, line height 1.5, max 60ch | Public Sans 400 |
| Body | `body` | 16 → 17, line height 1.6 | Public Sans 400 |
| Meta, badges, labels | `.meta`, `--step--1` | 14 | Public Sans 400 or 600 |

The scale is fluid (`clamp`) with a rem floor, so browser zoom and text resizing still work. Labels are sentence case; never all caps. Prose sits in `.prose` (68ch).

---

## 5. Layout

```html
<main id="main" tabindex="-1">
  <div class="container">
    <div class="page-head">…</div>
    <div class="with-margin page-body">
      <aside class="with-margin__side"><nav class="toc">…</nav></aside>
      <div class="with-margin__main">
        <section class="section" id="tasks" aria-labelledby="h-tasks">
          <div class="section__head"><h2 id="h-tasks">The work</h2><p class="meta">35 tasks</p></div>
          …
        </section>
      </div>
    </div>
  </div>
</main>
```

- `.with-margin` becomes two columns at 64rem (1024px) with the ruled margin; below that it stacks.
- `.section` sets each section on a hairline; children are spaced 24px, and h3/h4 inside get more space above.
- Primitives: `.stack` (16px between children), `.stack-lg` (32px), `.cluster` (wrapping row, 8px gap; works on `ul`), `.prose`, `.panel` (white box).
- Reflow: nothing scrolls sideways at 320px except inside `.table-scroll`.

---

## 6. Icons

43 symbols drawn for EMST on a 24px grid with 2px round strokes:

`emst-mark` (brand: contour lines of a hill), `search`, `arrow-right`, `chevron-down`, `external`, `download`, `info`, `alert`, `check`, `lock`, `hourglass` (pending), `draft` (AI-drafted: pen drawing a dashed line), `unreviewed` (eye with slash), `eye` (watch), `user-group`, `compare`, `route`, `signal`, `book`, `leaf`, `flame`, `droplet`, `building`, `scales` (not for decisions), `copy`, `print`, `flag` (suggest a correction), `close`, `filter`, `layers`, `clock`, `menu`, `sort`, `sort-asc`, `sort-desc`, `target` (target level), `established`, `emerging`, `match-close`, `match-nested` (broad or narrow), `match-related`, `match-none`, `plus`.

```html
<svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#hourglass"/></svg>
```

- Sizes: `.icon` 20px; `.icon--sm` 16px; `.icon--lg` 24px. Inside badges, chips and listboxes icons are 16px automatically.
- Icons are always decorative (`aria-hidden="true"`). The words next to them carry the meaning. An icon-only button carries `aria-label`.
- **Building with `h()`:** create `svg` and `use` with `document.createElementNS("http://www.w3.org/2000/svg", …)`.
- **AI-drafted icon decision:** a pen drawing a dashed line ("drafted in pencil"), not a robot or sparkle. A robot reads as a gimmick and a sparkle as marketing; both describe the tool rather than the state of the record. The eye with a slash is kept for "not yet reviewed" when review is shown on its own (crosswalk rows).

---

## 7. Components

Every example below is in `gallery.html` with real release content.

### 7.1 Skip link and release strip

The release strip is the standing disclosure on every page (release ID and use notice).

```html
<a class="skip-link" href="#main">Skip to main content</a>
<div class="release-strip">
  <div class="container release-strip__inner">
    <svg class="icon icon--sm" aria-hidden="true" focusable="false"><use href="assets/icons.svg#draft"/></svg>
    <p>Release <span class="id">2.0.0-rc.1</span> is drafted by AI agents and not yet reviewed by a person. Not for hiring, classification or performance decisions. <a href="#/about/use">What this means</a></p>
  </div>
</div>
```

- The skip link is the first focusable element. `<main>` has `tabindex="-1"` so it can take focus.
- Do keep the strip to one or two sentences. Don't add a close button: the notice must persist.

### 7.2 Site header and search (ARIA 1.2 combobox)

```html
<header class="site-header">
  <div class="container site-header__bar">
    <a class="brand" href="#/">
      <svg class="brand__mark" aria-hidden="true" focusable="false"><use href="assets/icons.svg#emst-mark"/></svg>
      <span><span class="brand__name">EMST</span><span class="brand__full">Environmental Management Skills Taxonomy</span></span>
    </a>
    <form class="search" role="search" id="site-search" novalidate>
      <label class="search__label" for="q">Search roles, tasks, competencies and series codes</label>
      <div class="search__row">
        <div class="combobox">
          <input class="search__input" id="q" type="search" role="combobox" aria-expanded="false"
                 aria-controls="q-list" aria-autocomplete="list" aria-describedby="q-help"
                 autocomplete="off" spellcheck="false" placeholder="Try: prescribed fire, 0462">
          <ul class="listbox" id="q-list" role="listbox" aria-label="Search suggestions" hidden></ul>
        </div>
        <button class="search__btn" type="submit"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#search"/></svg><span>Search</span></button>
      </div>
      <p class="vh" id="q-help">Suggestions appear as you type. Use the up and down arrow keys to move through them and Enter to open one.</p>
      <p class="vh" role="status" aria-live="polite" id="q-status"></p>
    </form>
  </div>
</header>
```

Open listbox, grouped by kind, with "See all results" last:

```html
<ul class="listbox" id="q-list" role="listbox" aria-label="Search suggestions">
  <li role="none"><ul role="group" aria-labelledby="q-g0">
    <li role="none" class="listbox__group-label" id="q-g0">Roles</li>
    <li class="listbox__option" id="q-opt-0" role="option" aria-selected="false">
      <span class="listbox__title">Fuels and prescribed <mark>fire</mark> specialist</span>
      <span class="listbox__ctx">Forest module</span>
    </li>
  </ul></li>
  <li class="listbox__option listbox__all" id="q-opt-all" role="option" aria-selected="false">See all results for "fire"</li>
</ul>
```

Behaviour (see `gallery.js`, and spec §3.3):
- Suggestions from 2 characters, at most 8, grouped in the spec's order, "See all results" last.
- ArrowDown opens and moves; ArrowUp moves; Enter activates the active option, or all results when none is active; Escape closes (a second Escape clears); Tab closes.
- Focus stays in the input. The active option is `aria-selected="true"` and named by `aria-activedescendant`. Prevent `mousedown` default on options so the input keeps focus.
- Announce "N suggestions" in the polite status after a 500 ms pause.
- Highlight matched words with `<mark>` built from text nodes; never `innerHTML`.
- States: default; focused (amber ring in the header); expanded; active option (tint plus a 4px bar); no results (close the listbox, set `aria-expanded="false"`, and show the message in a `role="status"` element tied to the input with `aria-describedby`):

```html
<div class="listbox listbox--static listbox__empty" id="q-empty" role="status">
  <p>No matches for "arborist apprentice".</p>
  <p>Try fewer words, a task such as "collect water samples", or a series code such as 0462.</p>
</div>
```

- **Search page variant:** add `search--page` to the form and put it on the page instead of the header. `listbox--static` puts the list in the flow (results pages, gallery).
- Don't put the query in the URL (spec). Don't show an empty listbox: an empty `role="listbox"` is an ARIA error.

### 7.3 Primary navigation

```html
<nav class="site-nav" aria-label="Main">
  <div class="container site-nav__inner">
    <button class="site-nav__toggle" type="button" aria-expanded="false" aria-controls="nav-list">
      <svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#menu"/></svg>Menu
    </button>
    <ul class="site-nav__list" id="nav-list">
      <li><a class="site-nav__link" href="#/roles" aria-current="page">Roles</a></li>
      <li><a class="site-nav__link" href="#/competencies">Competencies</a></li>
    </ul>
  </div>
</nav>
```

- Current item: `aria-current="page"`, shown by a 4px green bar (left bar and tint on mobile).
- Below 48rem with `.js` on `<html>`, the list is hidden until the toggle adds `is-open` to the list and sets `aria-expanded="true"`.

### 7.4 Footer

```html
<footer class="site-footer">
  <div class="container site-footer__grid">
    <div class="site-footer__about">
      <p class="site-footer__brand"><svg class="icon icon--lg" aria-hidden="true" focusable="false"><use href="assets/icons.svg#emst-mark"/></svg>EMST</p>
      <p>The Environmental Management Skills Taxonomy is an independent, open project. It is not a government website, and no agency has endorsed it.</p>
      <p>Release <span class="id">2.0.0-rc.1</span>, 25 October 2026. Data: CC0 1.0. Credit: EMST project lead.</p>
    </div>
    <nav aria-labelledby="ft-project"><h2 class="site-footer__h" id="ft-project">Project</h2><ul><li><a href="…">…</a></li></ul></nav>
    <nav aria-labelledby="ft-policy"><h2 class="site-footer__h" id="ft-policy">Use and policy</h2><ul>…</ul></nav>
  </div>
</footer>
```

Do keep the "not a government website" sentence. Don't use personal names; the credit is "EMST project lead".

### 7.5 Page header

```html
<div class="page-head">
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <ol><li><a href="#/">Home</a></li><li><a href="#/roles">Roles</a></li><li><span aria-current="page">Field resource technician</span></li></ol>
  </nav>
  <p class="page-head__kind"><span>Role profile, core module</span><span class="id">ROL-ZJFCC09</span></p>
  <h1 tabindex="-1">Field resource technician</h1>
  <p class="lede">Collects vegetation, wildlife, water and soil data to protocol …</p>
  <div class="page-head__status status-line">…</div>
</div>
```

- `.page-head__kind` is the spec's "eyebrow": record kind in sentence case plus its ID. It is not an all-caps label.
- On route change, focus the H1 (`tabindex="-1"`) and announce the change (spec).
- Separators are drawn by CSS and hidden from screen readers.

### 7.6 Status line (`ui.statusLine`)

```html
<div class="status-line">
  <span class="badge tier tier--describe"><span class="tier__steps" aria-hidden="true"><i class="on"></i><i class="on"></i><i></i><i></i></span><span><span class="badge__pre">Use tier </span>Describe</span></span>
  <p><strong>Use for</strong> describing work, workforce planning and curriculum mapping. <strong>Not for</strong> hiring, classification or performance decisions.</p>
  <span class="badge badge--draft"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#draft"/></svg>AI-drafted, not yet reviewed</span>
  <a href="#/role/…/about">About this record</a>
</div>
```

One per record, under the H1. `{compact: true}`: use only the two badges and the link.

### 7.7 On this page

```html
<nav class="toc" aria-labelledby="toc-title">
  <h2 class="toc__title" id="toc-title">On this page</h2>
  <ol class="toc__list">
    <li><a class="toc__link" href="#tasks" aria-current="true">The work</a></li>
    <li><a class="toc__link" href="#competencies">Competencies</a></li>
  </ol>
</nav>
```

Sticky in the margin column on wide screens; two columns above the content on narrow ones. Set `aria-current="true"` on the section in view (an IntersectionObserver is enough; see `gallery.js`). Hash links inside the hash-routed app must not change the route: handle them with `scrollIntoView` and focus the section heading.

### 7.8 Cards

The whole card is one link; the title link's `::after` covers the card, and the focus ring is drawn around the card.

```html
<ul class="card-list">
  <li>
    <article class="card">
      <p class="card__kind"><span>Role</span><span class="id">ROL-ZJFCC09</span></p>
      <h3 class="card__title h4"><a class="card__link" href="#/role/field-resource-technician">Field resource technician</a></h3>
      <p class="card__summary">Collects and records field observations and samples to protocol …</p>
      <dl class="card__meta">
        <div><dt>Tasks</dt><dd>35</dd></div>
        <div><dt>Competencies</dt><dd>24</dd></div>
        <div><dt>Levels</dt><dd>Entry, journey</dd></div>
      </dl>
      <div class="card__badges cluster">…tier badge… …draft badge…</div>
    </article>
  </li>
</ul>
```

- Competency card: add `card--comp` (green top rule instead of ink) and show the level span:

```html
<div><dt>Levels</dt><dd><span class="span"><span class="span__cells" aria-hidden="true"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i></i></span>L1 to L4</span></dd></div>
```

- Do keep exactly one link in a card. Don't put buttons or other links inside it; put them after the list.

### 7.9 Figures (`figBadges`)

```html
<ul class="cluster">
  <li class="panel fig"><p class="fig__n num">1,317</p><p class="fig__label">tasks</p>
    <span class="badge badge--compact ev ev--e"><span class="ev__mark" aria-hidden="true">E</span><span><span class="vh">Evidence label E: </span>Sourced</span></span></li>
</ul>
```

Every figure carries its badges in the compact form (spec). Every number must come from `app/data/`. Merriweather's figures are old-style (3, 4, 5, 7, 9 descend); that is deliberate for figures, and tables use tabular Public Sans.

### 7.10 Badges

Shared base: `.badge` (square corners, 28px tall, 14px semibold). `.badge--compact` is 24px tall and 13px, for figures and table cells.

**Use tier.** Four steps filled to the tier: exploratory 1, describe 2. Develop and select are not reached in this release.

```html
<span class="badge tier tier--describe"><span class="tier__steps" aria-hidden="true"><i class="on"></i><i class="on"></i><i></i><i></i></span><span><span class="badge__pre">Use tier </span>Describe</span></span>
<span class="badge tier tier--exploratory"><span class="tier__steps" aria-hidden="true"><i class="on"></i><i></i><i></i><i></i></span><span><span class="badge__pre">Use tier </span>Exploratory</span></span>
<span class="badge tier tier--locked"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#lock"/></svg><span>Develop: not yet available</span></span>
```

Mark filled steps with `class="on"`; the count must match the tier.

**Evidence label.** The letter's frame carries the meaning: E solid, J outlined, S dashed. The words are always shown.

```html
<span class="badge ev ev--e"><span class="ev__mark" aria-hidden="true">E</span><span><span class="vh">Evidence label E: </span>Sourced</span></span>
<span class="badge ev ev--j"><span class="ev__mark" aria-hidden="true">J</span><span><span class="vh">Evidence label J: </span>Judgment</span></span>
<span class="badge ev ev--s"><span class="ev__mark" aria-hidden="true">S</span><span><span class="vh">Evidence label S: </span>Speculation</span></span>
```

(The vocabulary's labels are E "Evidence", J "Expert judgment", S "Speculation"; take the shown words from `content.js` `evidence`.)

**Lifecycle of the work.**

```html
<span class="badge badge--ok"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#established"/></svg>Established</span>
<span class="badge badge--info"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#emerging"/></svg>Emerging</span>
<span class="badge badge--warn"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#eye"/></svg>Watch</span>
```

**Provenance.**

```html
<span class="badge badge--draft"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#draft"/></svg>AI-drafted, not yet reviewed</span>
<span class="badge badge--nfd"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#scales"/></svg>Not for decisions</span>
```

`badge--nfd` labels v1 analyst values in the evidence drawer.

**Crosswalk match.** The glyph shows how much the two concepts overlap (close: large overlap; broad or narrow: nested; related: touching; none: apart). Every row in this release also carries "Unreviewed AI match".

```html
<span class="badge match"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#match-close"/></svg>Close match</span>
<span class="badge match"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#match-nested"/></svg>Broad match</span>
<span class="badge match"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#match-nested"/></svg>Narrow match</span>
<span class="badge match"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#match-related"/></svg>Related match</span>
<span class="badge match"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#match-none"/></svg>No match</span>
<span class="badge badge--draft"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#unreviewed"/></svg>Unreviewed AI match</span>
```

Use plain words from `content.js` `match`, never the SKOS terms (spec: no "closeMatch" in visible text).

Do: one badge per fact. Don't: invent a badge colour, or use a badge as a button.

### 7.11 Assessment pending (`ui.pendingSummary`)

The display gate holds importance, time share, critical, needed at entry, craft, work function and exposure. Held values never appear as numbers, blanks, dashes or zeros.

**Section summary (the default).** One per section that has held values, after the list or table. Never one per row (spec).

```html
<div class="pending pending--block">
  <div class="pending__label">
    <svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#hourglass"/></svg>
    <p class="pending__title">Not yet assessed: importance, time share, critical, needed at entry, craft blend and exposure to automation</p>
    <p class="pending__text">0 of 35 tasks assessed. These values appear only after a multi-rater reliability study passes. Until then nothing is shown, not even a zero.</p>
    <a href="#/about/held-values">Why some values are held back</a>
  </div>
</div>
```

**Single value.** Only where one value stands alone, such as a fact on a task page:

```html
<dt>Time share</dt><dd><span class="pending"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#hourglass"/></svg>Assessment pending</span></dd>
```

- The hatch is decoration; the dashed outline, hourglass and words carry the meaning, so it survives print and forced colours.
- Don't reuse the hatch for anything else. Empty states use a solid frame; locked uses dashes without hatch.

### 7.12 Evidence ladder (`ui.evidenceLadder`)

Where a record sits on draft → AI-checked → human-reviewed → validated → in production. Done steps are filled with a check, the current step has a ringed node, bold label and the words "Current step", future steps are dashed and hollow. Horizontal from 40rem, vertical below.

```html
<div class="ev-ladder">
  <h3 class="ev-ladder__title" id="evl">Review path for this record</h3>
  <ol class="ev-ladder__steps" aria-labelledby="evl">
    <li class="ev-ladder__step is-done"><span class="ev-ladder__node" aria-hidden="true"><svg class="icon" focusable="false"><use href="assets/icons.svg#check"/></svg></span><span class="ev-ladder__label">Drafted by AI agents<span class="vh">: done</span></span></li>
    <li class="ev-ladder__step is-current" aria-current="step"><span class="ev-ladder__node" aria-hidden="true"></span><span class="ev-ladder__label">AI-checked</span><span class="ev-ladder__here">Current step</span></li>
    <li class="ev-ladder__step"><span class="ev-ladder__node" aria-hidden="true"></span><span class="ev-ladder__label">Human-reviewed<span class="vh">: not yet</span></span></li>
    <li class="ev-ladder__step"><span class="ev-ladder__node" aria-hidden="true"></span><span class="ev-ladder__label">Validated<span class="vh">: not yet</span></span></li>
    <li class="ev-ladder__step"><span class="ev-ladder__node" aria-hidden="true"></span><span class="ev-ladder__label">In production<span class="vh">: not yet</span></span></li>
  </ol>
  <p class="ev-ladder__note meta">Automated checks have run on this record. No person has reviewed it yet.</p>
</div>
```

Map review status to the current step from `ev.r` and `ev.v` (see `DATA.md`). If a record has had no automated check, the current step is the first one and no step is done.

### 7.13 Use-tier path

The same ladder shows what a record may be used for. Reached tiers are done, the record's tier is current, develop and select are locked.

```html
<div class="ev-ladder">
  <h3 class="ev-ladder__title" id="tiers">What this record may be used for</h3>
  <ol class="ev-ladder__steps" aria-labelledby="tiers">
    <li class="ev-ladder__step is-done"><span class="ev-ladder__node" aria-hidden="true"><svg class="icon" focusable="false"><use href="assets/icons.svg#check"/></svg></span><span class="ev-ladder__label">Exploratory<span class="vh">: allowed</span></span><span class="ev-ladder__desc">Foresight and curriculum exploration.</span></li>
    <li class="ev-ladder__step is-current" aria-current="step"><span class="ev-ladder__node" aria-hidden="true"></span><span class="ev-ladder__label">Describe</span><span class="ev-ladder__here">This record</span><span class="ev-ladder__desc">Workforce analytics, planning and curriculum mapping.</span></li>
    <li class="ev-ladder__step is-locked"><span class="ev-ladder__node" aria-hidden="true"><svg class="icon" focusable="false"><use href="assets/icons.svg#lock"/></svg></span><span class="ev-ladder__label">Develop</span><span class="ev-ladder__desc">Training, task books, development plans and self-assessment. <b>Not yet available in this release.</b></span></li>
    <li class="ev-ladder__step is-locked">…Select…</li>
  </ol>
</div>
```

### 7.14 Level chips and the proficiency ladder (`levelChip`, `levelLadder`)

```html
<span class="badge level-chip"><span class="level-chip__code">L3</span>Senior</span>
```

```html
<ol class="levels" aria-labelledby="comp-title">
  <li class="level">
    <div class="level__rung" aria-hidden="true">L1</div>
    <div class="level__body">
      <h4 class="level__name"><span class="vh">Level 1: </span>Supervised</h4>
      <p class="level__desc">Works under direct or close direction; work is checked.</p>
      <ul class="level__indicators"><li>Records the attribute at each pre-selected validation point …</li></ul>
    </div>
  </li>
  <li class="level is-target">
    <div class="level__rung" aria-hidden="true">L2</div>
    <div class="level__body">
      <p class="level__target"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#target"/></svg>Target level for Field resource technician, journey level</p>
      <h4 class="level__name"><span class="vh">Level 2: </span>Independent</h4>
      …
    </div>
  </li>
  <li class="level is-undefined">
    <div class="level__rung" aria-hidden="true">L5</div>
    <div class="level__body"><h4 class="level__name"><span class="vh">Level 5: </span>Strategic</h4><p class="level__none">Not defined for this competency.</p></div>
  </li>
</ol>
```

- Show all five levels; levels outside the competency's span are `is-undefined` (dashed rung, "Not defined for this competency").
- The target is marked by shape (filled, ringed rung), a flag icon and the words "Target level for …", not by colour alone.
- Indicators are AI drafts; say so once above the ladder.

### 7.15 Tabs: employer variants (`ui.tabs`)

```html
<h3 class="h4" id="h-variants">How this role differs by employer</h3>
<div class="tabs">
  <div class="tabs__list" role="tablist" aria-labelledby="h-variants">
    <button class="tabs__tab" type="button" role="tab" id="tab-fed" aria-selected="true" aria-controls="panel-fed">Federal</button>
    <button class="tabs__tab" type="button" role="tab" id="tab-state" aria-selected="false" aria-controls="panel-state" tabindex="-1">State</button>
    …Local, NGO, Private, Academic…
  </div>
  <section class="tabs__panel" role="tabpanel" id="panel-fed" aria-labelledby="tab-fed" tabindex="0">…</section>
  <section class="tabs__panel" role="tabpanel" id="panel-state" aria-labelledby="tab-state" tabindex="0" hidden>…</section>
</div>
```

- Roving tabindex; Left and Right (also Up and Down) move and select; Home and End jump. Selection follows focus.
- Optional count in a tab: `<span class="tabs__count">28</span>`.
- On wide screens the selected tab is an index tab joined to its panel; under 40rem the tabs become a wrapping grid of buttons with the selected one tinted and underlined.
- The order is fixed: federal, state, local, NGO, private, academic. Never a Tribal tab (Tribal hold).

### 7.16 Disclosure and evidence drawer (`ui.disclosure`)

Native `<details>`; no script needed.

```html
<details class="drawer">
  <summary class="drawer__summary">
    <svg class="icon drawer__chev" aria-hidden="true" focusable="false"><use href="assets/icons.svg#chevron-down"/></svg>
    <span class="drawer__title">v1 prior evidence (2 records)</span>
    <span class="badge badge--nfd"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#scales"/></svg>Not for decisions</span>
  </summary>
  <div class="drawer__body">
    <p class="prose">These codes were assigned in EMST v1 by one analyst working with an AI assistant …</p>
    <dl class="facts"><dt>Drafted by</dt><dd>AI agents (LLM-assisted)</dd><dt>Review</dt><dd>Not yet reviewed by a person</dd></dl>
  </div>
</details>
```

- v1 analyst values appear only inside a drawer labelled "Not for decisions".
- `.facts` is a two-column term list from 30rem.
- Before printing, open all drawers (`beforeprint`) and restore them afterwards (`afterprint`); see `gallery.js`.

### 7.17 Data table

```html
<div class="table-scroll" role="region" aria-labelledby="cap-tasks" tabindex="0">
  <table class="data-table data-table--sticky">
    <caption id="cap-tasks">Tasks for Field resource technician<span class="data-table__hint">First 5 of 35 tasks. Select a column heading to sort.</span></caption>
    <thead><tr>
      <th scope="col" class="is-sortable" aria-sort="ascending"><button class="sort" type="button">Task<svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#sort-asc"/></svg></button></th>
      <th scope="col" class="is-sortable num"><button class="sort" type="button">Competencies<svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#sort"/></svg></button></th>
      <th scope="col">Role levels</th>
    </tr></thead>
    <tbody>
      <tr><th scope="row">Adapt the vegetation sampling layout when …</th><td class="num">1</td><td>Journey</td></tr>
    </tbody>
  </table>
</div>
```

- Hairline rules, no zebra stripes, a 2px rule under the header. Numbers are right-aligned with tabular figures (`.num` on the `th` and `td`).
- `data-table--sticky` keeps the first column in place while the table scrolls inside `.table-scroll`. The scroller is focusable and labelled so keyboard users can scroll it; a soft shadow at the right edge shows there is more.
- Sorting: a `button.sort` in the header; put `aria-sort` only on the sorted column; switch the icon among `sort`, `sort-asc` and `sort-desc`; say the sort in the caption hint.
- Tables have a 32rem minimum width and scroll on phones rather than squeeze. Every chart needs one of these as its text equivalent.
- Don't put a per-row pending mark in a column; use the section summary (7.11).

### 7.18 Comparison

```html
<div class="compare">
  <div class="compare__roles">
    <div class="compare__role"><span class="key" aria-hidden="true"></span><div><p class="meta">First role</p><h3 class="h4"><a href="#/role/…">Field resource technician</a></h3><p class="meta">24 competencies</p></div></div>
    <div class="compare__role compare__role--b"><span class="key key--b" aria-hidden="true"></span><div><p class="meta">Second role</p><h3 class="h4"><a href="#/role/…">Conservation corps member</a></h3><p class="meta">18 competencies</p></div></div>
  </div>
  <figure class="overlap">
    <figcaption class="overlap__caption">How their competencies overlap</figcaption>
    <svg class="overlap__bar" viewBox="0 0 31 1" preserveAspectRatio="none" aria-hidden="true" focusable="false">
      <rect class="overlap__seg overlap__seg--a" x="0" y="0" width="13" height="1"/>
      <rect class="overlap__seg overlap__seg--shared" x="13" y="0" width="11" height="1"/>
      <rect class="overlap__seg overlap__seg--b" x="24" y="0" width="7" height="1"/>
    </svg>
    <ul class="overlap__legend">
      <li><span class="key" aria-hidden="true"></span><span>Only Field resource technician: <strong class="num">13</strong></span></li>
      <li><span class="key key--shared" aria-hidden="true"></span><span>Shared: <strong class="num">11</strong></span></li>
      <li><span class="key key--b" aria-hidden="true"></span><span>Only Conservation corps member: <strong class="num">7</strong></span></li>
    </ul>
    <p class="overlap__text">11 of the 31 competencies across both roles are shared. 13 are only in Field resource technician and 7 are only in Conservation corps member.</p>
  </figure>
  <div class="compare__lists">
    <section class="compare__col" aria-labelledby="cmp-a"><h4 id="cmp-a"><span class="key" aria-hidden="true"></span>Only Field resource technician<span class="count">13</span></h4><ul><li>…</li></ul></section>
    <section class="compare__col" aria-labelledby="cmp-s"><h4 id="cmp-s"><span class="key key--shared" aria-hidden="true"></span>Shared<span class="count">11</span></h4><ul>…</ul></section>
    <section class="compare__col" aria-labelledby="cmp-b"><h4 id="cmp-b"><span class="key key--b" aria-hidden="true"></span>Only Conservation corps member<span class="count">7</span></h4><ul>…</ul></section>
  </div>
</div>
```

- The bar is a Venn-free, proportional strip: the `viewBox` width is the union count, and each `rect` uses the counts as `x` and `width`. SVG attributes are allowed by the CSP; `style=""` is not. White gaps separate segments without colour.
- The order is the same everywhere: only A, shared, only B. Colours: `--cat-1`, `--ui-strong`, `--cat-2` (validated adjacent pair).
- The sentence in `.overlap__text` is required: it is the text equivalent.
- Add the spec's caveat ("shares N of M…", never "recommended") from `content.js`.

### 7.19 Notices (`ui.notice`)

```html
<div class="notice notice--use" role="note">
  <svg class="icon notice__icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#scales"/></svg>
  <div class="notice__body">
    <h3 class="notice__title">Not for selection, classification or performance decisions</h3>
    <p>EMST describes work. It is not a selection instrument, not a classification basis, not a job analysis, and not for reduction-in-force, adverse action or performance-rating decisions.</p>
  </div>
</div>
```

| Spec kind | Class | Icon | Look |
|---|---|---|---|
| `info` | `notice--info` | `info` | Blue tint, left rule |
| `caution` | `notice--warn` | `alert` | Ochre tint, left rule |
| `hr` (HR disclaimer) and the use notice | `notice--use` | `scales` | White, ink frame, heavy left rule |
| `exploratory` (pathways, AI drafts) | `notice--draft` | `draft` or `route` | Dotted graphite frame |
| `held` (Tribal hold) | `notice--hold` | none | Double rule, serif title, no tint |

The Tribal hold notice quotes `core.status.held.policy` verbatim and shows only the count. Never use warning or error styling for it, and never add an icon that suggests a problem or invents cultural imagery.

```html
<div class="notice notice--hold" role="note" data-emst-policy="indigenous-statement">
  <div class="notice__body">
    <h3 class="notice__title">Records held for Tribal consent</h3>
    <p>…policy text, verbatim…</p>
    <p><span class="num">163</span> records related to Tribal employers are held …</p>
  </div>
</div>
```

Use `role="note"` for standing notices and `role="status"` only for messages that appear after an action.

### 7.20 Buttons and links

```html
<button class="btn btn--primary" type="button"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#compare"/></svg>Compare roles</button>
<button class="btn btn--secondary" type="button">See where this role leads</button>
<button class="btn btn--tertiary" type="button">Clear all filters</button>
<button class="btn btn--secondary btn--icon" type="button" aria-label="Print this page"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#print"/></svg></button>
<button class="btn btn--secondary btn--small" type="button">Small</button>
<button class="btn btn--primary" type="button" aria-disabled="true"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#lock"/></svg>Self-assessment: not yet available</button>
```

- Buttons are 44px tall. `btn--small` is 32px with a fine pointer and 44px with a coarse one.
- Prefer `aria-disabled="true"` (still focusable, with a reason in its label) to `disabled`. Disabled looks dashed, like locked.
- Links in text are always underlined. Focused links get a highlighter wash and a 3px ring.

**Download link** (file type and size, from the data):

```html
<ul class="dl-list"><li><a class="dl-link" href="downloads/competencies.csv" download><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#download"/></svg><span><span class="dl-link__text">Competencies</span><span class="dl-link__meta">CSV, 126 KB</span></span></a></li></ul>
```

**Copy citation:**

```html
<figure class="citation">
  <blockquote class="citation__text" id="cite-1">EMST project lead (2026). Environmental Management Skills Taxonomy, release 2.0.0-rc.1 [Data set]. https://github.com/jrwashebek/Enviroskillstaxonomy</blockquote>
  <figcaption class="btn-row">
    <button class="btn btn--secondary btn--small" type="button" data-copy="cite-1"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#copy"/></svg><span>Copy citation</span></button>
    <span class="meta" role="status" aria-live="polite"></span>
  </figcaption>
</figure>
```

Copy with `navigator.clipboard.writeText`; on success, change the label to "Copied" with a check for 2.5 seconds and announce "Citation copied". On failure, tell people to select and copy the text.

**Suggest a correction** (GitHub Issues; no query string):

```html
<a class="btn btn--secondary" href="https://github.com/jrwashebek/Enviroskillstaxonomy/issues/new/choose" rel="noopener"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#flag"/></svg>Suggest a correction<span class="vh"> (opens GitHub Issues)</span><svg class="icon icon--sm" aria-hidden="true" focusable="false"><use href="assets/icons.svg#external"/></svg></a>
<p class="meta">Opens GitHub Issues. You need a free GitHub account. Please do not include personal information.</p>
```

### 7.21 Filters and facets (`ui.chips`, `ui.liveCount`)

```html
<fieldset class="facet">
  <legend class="facet__legend">Employer type</legend>
  <div class="chips">
    <label class="chip"><input class="chip__input" type="checkbox" name="actor" value="federal" checked><span class="chip__face"><svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#check"/></svg>Federal<span class="chip__count">28</span></span></label>
  </div>
</fieldset>
<fieldset class="facet">
  <legend class="facet__legend">Lifecycle of the work</legend>
  <ul class="checklist">
    <li><label class="check"><input class="check__input" type="checkbox" name="lc" value="established" checked><span>Established</span><span class="check__count">30</span></label></li>
  </ul>
</fieldset>
<div class="result-bar">
  <p class="result-bar__count" role="status" aria-live="polite">Showing 12 of 37 roles</p>
  <button class="chip-remove" type="button"><span class="vh">Remove filter: </span>Federal<svg class="icon" aria-hidden="true" focusable="false"><use href="assets/icons.svg#close"/></svg></button>
  <button class="btn btn--tertiary btn--small" type="button">Clear all</button>
</div>
```

- Chips are real checkboxes (or radios for single choice, as in "Group by"), so they work with keyboard and assistive technology without script. A checked chip is filled and shows a check mark: shape plus colour.
- Checkboxes in lists are native with `accent-color`, 20px, in a 36px row (44px on touch screens).
- Update the live count after each change; never move focus.

### 7.22 Empty and loading

```html
<div class="empty">
  <span class="empty__icon" aria-hidden="true"><svg class="icon" focusable="false"><use href="assets/icons.svg#filter"/></svg></span>
  <h3 class="empty__title h4">No roles match these filters</h3>
  <p>Remove a filter, or search for a task instead. Some roles are described for only a few employer types.</p>
  <div class="btn-row"><button class="btn btn--secondary" type="button">Clear all filters</button></div>
</div>
```

```html
<div class="panel" aria-busy="true">
  <p class="loading" role="status">Loading competencies</p>
  <div class="skeleton" aria-hidden="true"><span class="skeleton__line"></span><span class="skeleton__line"></span><span class="skeleton__line"></span></div>
</div>
```

- Empty is a solid frame with a way forward. It must never look like pending (hatched).
- Data loads quickly from local files; show loading only if a shard takes longer than about 300 ms. The skeleton pulse stops under reduced motion.

---

## 8. Print

`print.css` targets US letter. It:
- hides the skip link, release strip, navigation, search, "On this page", buttons, chips, filters, tab lists, loading states and anything with class `no-print`;
- turns the header into a one-line masthead and forces black on white in both themes;
- prints the destination of every link in the main column after its text, as `<address>`;
- removes table scroll frames, keeps rows whole and repeats header rows; the first column takes 38%;
- keeps every status shape (dashed pending, solid E mark, filled done steps);
- adds "Page N of M" at the bottom right (Chromium 131 and later; other browsers skip it).

Every printable page must include the release block, which is hidden on screen:

```html
<div class="print-only print-meta">
  <p>EMST release 2.0.0-rc.1 (25 October 2026). Printed from <a href="https://…/#/role/field-resource-technician">EMST: Field resource technician</a>.</p>
  <p>Drafted by AI agents and not yet reviewed by a person. Not for selection, classification or performance decisions.</p>
</div>
```

Give the page link readable text (not the URL), because the address is printed after it. Open evidence drawers on `beforeprint` and close them on `afterprint`. Only the selected employer tab prints. For a role, print order is: header and status line, tasks, competencies table, then the pending summary.

---

## 9. Accessibility checklist

- **Contrast:** all token pairs pass in both themes (`tools/check-contrast.mjs`). Text on a status tint uses `--fg` or the status `-fg`, never a third colour.
- **Focus:** 3px ring, 2px offset, never removed; amber in the header and in dark mode; links also get a highlighter wash. Cards draw the ring around the whole card. Tabs, sort buttons and scrollers draw it inside.
- **Targets:** at least 24×24px everywhere; 44px for buttons, navigation, tabs, search, options and (on touch screens) chips, checkboxes and small buttons.
- **Reflow:** checked at 320px and 390px; only table scrollers scroll sideways. Absolutely positioned helpers inside scrollers are contained (`.table-scroll` is positioned).
- **Motion:** only the drawer chevron and the skeleton move; both stop under `prefers-reduced-motion`.
- **Forced colours:** checked with Chromium's `forced-colors: active`. Fills that carry meaning (tier steps, level span, E mark, done steps, keys, selected chip, active option, target) are redrawn in system colours; the overlap bar uses CanvasText and GrayText.
- **No colour alone:** every status has words, and a shape or icon (see section 1).
- **Language:** sentence case, plain words, no all-caps labels.

---

## 10. Mapping to `ui.js`

| `ui.js` function (spec §3) | Classes |
|---|---|
| `pageHeader` | `.page-head`, `.breadcrumb`, `.page-head__kind`, `.lede`, `.page-head__status` |
| `statusLine` | `.status-line` with `.tier` and `.badge--draft` |
| `pendingSummary` | `.pending--block`, `.pending__label`, `.pending__title`, `.pending__text` |
| `evidenceLadder` | `.ev-ladder` (7.12) |
| `provenance` | `.drawer`, `.facts` |
| `recordActions` | `.btn-row`, `.btn`, `.dl-link`, `.citation` |
| `matchType`, `crosswalkList` | `.badge.match`, `.badge--draft` with `unreviewed`, or a `.data-table` |
| `levelChip`, `levelLadder` | `.level-chip`, `.levels`, `.level`, `.is-target`, `.is-undefined` |
| `badge`, `figBadges` | `.badge` and variants, `.badge--compact`, `.fig` |
| `notice` | `.notice` and the variants in 7.19 |
| `disclosure` | `.drawer` |
| `tabs` | `.tabs`, `.tabs__list`, `.tabs__tab`, `.tabs__panel` |
| `chips` | `.facet`, `.chips`, `.chip`, `.chip__input`, `.chip__face`; `.checklist`, `.check` |
| `onThisPage` | `.toc` |
| `card`, `emptyState`, `liveCount` | `.card`, `.card--comp`, `.empty`, `.result-bar__count` |
| `jargon` | `<abbr title>` (dotted underline). Also expand the term in text on first use: a title is hover-only. |

---

## 11. Known limits

- **Merriweather** is shipped exactly as USWDS distributes it, because its licence reserves the font name for unmodified files. Its Latin subset lacks the ʻokina and macrons (for example in Hawaiian place names); those characters fall back to Georgia inside headings. Public Sans covers them.
- **Merriweather figures** are old-style and it has no tabular figures. Keep numbers in tables and meta in Public Sans.
- **The sprite** needs HTTP(S). If the prototype must open from `file://`, inline the sprite once at the top of `index.html` (`<svg hidden>…</svg>`) and use `href="#id"`.
- **Page numbers in print** need Chromium 131 or later.
- **Not yet tested** with real users, screen readers on mobile, or Windows high-contrast themes other than Chromium's emulation. Sunlight legibility is reasoned from contrast ratios, not field-tested.
