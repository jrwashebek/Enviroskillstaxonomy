# EMST Explorer: Accessibility Conformance Report (WCAG 2.2 Level AA)

- **Product:** EMST Explorer (Tier 1 static site), `site/` in the EMST repository
- **Version evaluated:** explorer 0.1.0, built from EMST release `2.0.0-dev`, preview profile. The release ID is stamped on every page.
- **Date:** 2026-10-23
- **Prepared by:** CP (Security, Privacy & Compliance Lead and Product & UX Lead), WP-12. ADR-0027 §4 assigns ACR sign-off to CP in Phase 4 and to the Steward thereafter.
- **Standard:** WCAG 2.2, Levels A and AA (W3C Recommendation; ISO/IEC 40500:2025). WCAG 2.2 AA is a superset of WCAG 2.0 AA, which Section 508 incorporates, and of WCAG 2.1 AA, which the ADA Title II rule requires. The Title II compliance dates are now 26 April 2027 and 26 April 2028. [E: CP-025, CP-012, CP-013]
- **Format:** the layout follows the ITI VPAT 2.5 WCAG table. Terms used: *Supports*, *Partially supports*, *Does not support*, *Not applicable*.

## Evaluation methods and their limits

1. **Automated rules.** axe-core 4.14.0 ran with the tags `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa` and `wcag22aa`.
   - Each sampled page was tested twice: as loaded, and with every `<details>` disclosure open, so hidden content was tested too.
   - The sample covers every template plus heavier instances: role-change, gap-check and pathways pages for several roles, federal series and state class pages, competency and module pages. The list is in `reports/browser-checks.json`.
   - Result: **0 violations**.
   - axe also returned "needs review" (incomplete) results for colour contrast, where it could not compute a background. Causes: text in grid-laid definition lists, a `<select>` with a background image, and SVG chart text. Those were checked by hand (1.4.3 below).
   - One best-practice item (`landmark-unique`) is reported; it does not count toward conformance.
2. **Scripted checks** (`tools/browser-checks.mjs`) on each sampled page:
   - reflow at 320 CSS px;
   - WCAG 1.4.12 text-spacing overrides at 320 px;
   - target size of at least 24 × 24 CSS px for every visible control outside running text;
   - visible focus on the first 12 Tab stops;
   - no requests to other origins.
3. **Static checks** (`tools/check-output.mjs`, every page):
   - one `<h1>` per page and no skipped heading levels, checked by a repository scan on 2026-10-23;
   - `lang="en"`;
   - a unique `<title>` naming the page and the release;
   - no inline styles, so user style sheets apply.
4. **Manual review.** An AI agent (CP) reviewed the templates, the client scripts and the colour palette.

**Not yet done, and required before this report can claim conformance:**

- testing with screen readers (NVDA with Firefox, JAWS with Chrome, VoiceOver on macOS and iOS, TalkBack);
- testing with voice control and screen magnification;
- sessions with assistive-technology users, planned for Round 2 of `docs/research/compliance-product/user_research_plan.md`.

Until those are done, criteria that depend on how assistive technology announces content are marked **Partially supports (AT testing pending)**. Automated tools find only part of WCAG failures. [J]

## Summary

| Level | Supports | Partially supports | Does not support | Not applicable |
|---|---|---|---|---|
| A (31 criteria; 4.1.1 is obsolete in WCAG 2.2) | 19 | 4 | 0 | 8 |
| AA (24 criteria) | 18 | 0 | 0 | 6 |

The four "Partially supports" entries are 1.1.1, 1.3.1 and 4.1.2, which await assistive-technology confirmation, and 2.4.4, where repeated "Check gaps" links depend on their list context. No known failure sits behind any of them, and no criterion is known to fail.

## Table 1: Level A

| Criterion | Conformance | Remarks |
|---|---|---|
| 1.1.1 Non-text Content | Partially supports (AT testing pending) | The only images are decorative USWDS icons in CSS and one SVG bar chart per role-change page. The chart is `aria-hidden` and has a visible caption stating its message, a text summary and a data table with the same values. Icon fonts are not used. |
| 1.2.1–1.2.3 Time-based media | Not applicable | No audio or video. |
| 1.3.1 Info and Relationships | Partially supports (AT testing pending) | Native headings, lists, tables (`caption`, `th scope`), `fieldset`/`legend` for every radio group (a nested legend per question), `label` on every input, `dl` for record fields, `details`/`summary` for disclosures. Tables in scroll regions are labelled `role="region"`. AT announcement of nested fieldsets has not been verified. |
| 1.3.2 Meaningful Sequence | Supports | DOM order equals visual order; no CSS reordering. |
| 1.3.3 Sensory Characteristics | Supports | Instructions name controls by their text ("Save to file"), never by position or colour. |
| 1.4.1 Use of Color | Supports | Use tier, evidence, lifecycle and "contested" are always text. Badge borders differ in pattern as well (solid, dotted, dashed, double). The chart uses a dot pattern plus a text label. |
| 1.4.2 Audio Control | Not applicable | No audio. |
| 2.1.1 Keyboard | Supports | Every function is reachable by keyboard: links, native buttons, radio groups, select, file inputs, `summary`. No custom widgets, no drag. The scripted Tab walk reached and showed focus on each sampled page. |
| 2.1.2 No Keyboard Trap | Supports | No modal widgets. The only dialog is the browser-native confirmation before "Clear everything" discards unsaved answers. |
| 2.1.4 Character Key Shortcuts | Not applicable | No single-key shortcuts. |
| 2.2.1 Timing Adjustable | Not applicable | No time limits. |
| 2.2.2 Pause, Stop, Hide | Not applicable | No moving, blinking or auto-updating content. Search results update only on input. |
| 2.3.1 Three Flashes or Below | Supports | No flashing content. |
| 2.4.1 Bypass Blocks | Supports | A "Skip to main content" link is the first focusable element and moves focus to `main`. Landmarks: header, nav (Main), nav (Breadcrumb), main, footer. |
| 2.4.2 Page Titled | Supports | `Page name · EMST Explorer · release`. Titles are unique across the build (role variants with the same sector carry their slice name). |
| 2.4.3 Focus Order | Supports | Follows reading order. After "See summary", focus moves to the summary heading, which comes later in the order. |
| 2.4.4 Link Purpose (In Context) | Partially supports (scripted region) | Links name their destination: role, competency, series or class titles. Repeated "Check gaps" links in pathway lists get their purpose from the list item ("Federal government (cross-sector move) … Check gaps"); an `aria-label` would be clearer. To be fixed in 0.2. |
| 2.5.1 Pointer Gestures | Supports | Single-pointer activation only. |
| 2.5.2 Pointer Cancellation | Supports | Native controls activate on up-event. |
| 2.5.3 Label in Name | Supports | Accessible names equal the visible labels; no `aria-label` overrides visible text. |
| 2.5.4 Motion Actuation | Not applicable | No motion input. |
| 3.1.1 Language of Page | Supports | `<html lang="en">`. |
| 3.2.1 On Focus | Supports | Focus never changes context. |
| 3.2.2 On Input | Supports | Choosing a role level updates the target text in place, with no change of context. Opening a file applies it and announces the result in a status region. |
| 3.2.6 Consistent Help | Supports | The same footer links ("Challenge a judgment", "Accessibility", "Privacy") appear in the same order on every page. |
| 3.3.1 Error Identification | Supports | File-open problems (wrong schema, different role variant, file too large) are described in text in a `role="status"` region. No form is submitted, so there is no other validation. |
| 3.3.2 Labels or Instructions | Supports | Every input has a visible label. The note field has a hint ("Do not type names or other personal details") tied by `aria-describedby`. |
| 3.3.7 Redundant Entry | Supports | Answers can be saved and reopened, so nothing has to be re-entered. |
| 4.1.2 Name, Role, Value | Partially supports (AT testing pending) | Native HTML elements only; no ARIA widgets. Live regions use `role="status"`. To verify with AT: announcement of the summary region, which is `hidden` until shown and then focused. |

## Table 2: Level AA

| Criterion | Conformance | Remarks |
|---|---|---|
| 1.2.4 Captions (Live), 1.2.5 Audio Description | Not applicable | No media. |
| 1.3.4 Orientation | Supports | No orientation lock. |
| 1.3.5 Identify Input Purpose | Not applicable | No input collects information about the user (name, e-mail and so on). Gap-check notes are free text about work. |
| 1.4.3 Contrast (Minimum) | Supports | Checked by hand where axe could not compute a value. Body text `#1b1b1b` on white is 17.2:1. Muted text `#565c65` is 6.7:1 on white, 5.9:1 on `#f0f0f0` and 6.0:1 on the banner `#faf3d1`. Links `#005ea2` are 6.7:1 on white and 5.9:1 on `#f0f0f0`. Banner text is 15.4:1. SVG chart text is `#1b1b1b` on white. |
| 1.4.4 Resize Text | Supports | Relative units, no fixed heights on text containers. 200% zoom is equivalent to the 640 px case, which falls within the tested 320 px reflow. |
| 1.4.5 Images of Text | Supports | None. |
| 1.4.10 Reflow | Supports | No horizontal page scroll at 320 CSS px on any sampled page. Wide data tables scroll inside their own labelled, focusable region, which the exception for data tables permits. Long IDs and hashes wrap. |
| 1.4.11 Non-text Contrast | Supports | Focus indicator: a 0.25rem `#1a4480` outline, 9.6:1 on white and about 8.5:1 on `#f0f0f0`. Form controls use USWDS borders (`#1b1b1b`). The chart's dot pattern is `#565c65` (6.7:1) with a `#1b1b1b` outline. Card borders (`#a9aeb1`) are decorative and are not needed to identify any control. |
| 1.4.12 Text Spacing | Supports | The scripted check applies the 1.4.12 overrides at 320 px: no loss of content or horizontal scroll. |
| 1.4.13 Content on Hover or Focus | Supports | No hover or focus pop-ups; no tooltips; nothing is shown only on hover. |
| 2.4.5 Multiple Ways | Supports | Main navigation, breadcrumbs, in-page links between views, A–Z lists and local search. |
| 2.4.6 Headings and Labels | Supports | Descriptive headings; one `h1` per page; no skipped levels. |
| 2.4.7 Focus Visible | Supports | A custom outline on all focusable elements; checked on the first 12 Tab stops per sampled page. |
| 2.4.11 Focus Not Obscured (Minimum) | Supports | No sticky or fixed headers, footers or overlays. |
| 2.5.7 Dragging Movements | Not applicable | No drag interactions; the pathway view is a list. |
| 2.5.8 Target Size (Minimum) | Supports | Buttons, radio labels, selects, summaries and links are at least 24 CSS px tall. Links get vertical padding; inline links in sentences fall under the exception anyway. Scripted check: 0 undersized targets on sampled pages. |
| 3.1.2 Language of Parts | Supports | All content is English. Record IDs and codes are not words in another language. |
| 3.2.3 Consistent Navigation | Supports | The same header navigation and footer on every page. |
| 3.2.4 Consistent Identification | Supports | The same badge text, the same "Assessment pending" label and the same control names throughout. |
| 3.3.3 Error Suggestion | Supports | File errors say what file is expected. |
| 3.3.4 Error Prevention (Legal, Financial, Data) | Not applicable | No legal, financial or data submissions. Clearing unsaved answers still asks for confirmation. |
| 3.3.8 Accessible Authentication (Minimum) | Not applicable | No authentication. |
| 4.1.3 Status Messages | Supports | Save, open, clear and search results are announced through `role="status"` (polite) regions without moving focus. |

## Uncertainty display (accessibility of meaning)

- Every number on screen carries a use-tier badge and an evidence badge in text, and `check-output.mjs` enforces this for every `[data-figure]`.
- Values that are not shown say why, using IO's labels word for word.
- The one chart type, a stacked bar, always has its table and its message in the caption.
- Comprehension testing of these labels is a release gate (`mvp_spec.md` §7.4). It has not been run.

## Known issues and plan

| # | Issue | Criterion | Plan |
|---|---|---|---|
| 1 | Screen-reader, voice-control and magnification testing not done | 1.1.1, 1.3.1, 4.1.2 (verification) | Round 2 sessions with assistive-technology users; then update this report |
| 2 | Repeated "Check gaps" links rely on their list-item context | 2.4.4 (AAA 2.4.9 would fail) | Add `aria-label`s naming the destination, in 0.2 |
| 3 | axe best-practice `landmark-unique`: several table regions share a label on some pages | best practice | Make region labels unique |
| 4 | Long pages (gap check with 20+ competencies) | usability, not conformance | Consider one competency per step (mvp_spec S2) after Round 1 |
| 5 | PDF export is browser print, so tagging depends on the browser | 1.3.1 for exported PDFs | Accessible tagged PDF and DOCX exports are future work |

Evidence files: `reports/browser-checks.json` (per page: axe violations and needs-review items, reflow, text spacing, target sizes, focus), `reports/check-output.json`.
