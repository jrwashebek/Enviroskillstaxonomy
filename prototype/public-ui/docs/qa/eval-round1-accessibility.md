# Evaluation round 1: accessibility (WCAG 2.2 AA)

- **Evaluator:** "a11y", an AI agent acting as an independent accessibility engineer.
- **Build:** prototype round 1, tested 30 October 2026, 21:55–22:15 UTC.
- **Method:**
  - axe-core run 122 times over 51 routes, in light theme, dark theme and at 320px;
  - accessibility-tree inspection;
  - keyboard journeys, reflow, 400% zoom and text spacing;
  - forced colours, target size, focus contrast and print.
- **Limits:** no real screen reader was run, and no people who use assistive technology took part.

## Verdict
**Not yet passing the release gate, but close.**
- axe-core found 0 violations.
- Manual testing found two success-criterion failures and three serious defects.
- All five were fixed in round 2 (see below).

## Failures and serious defects

| # | Issue | WCAG | Round 2 fix |
|---|---|---|---|
| 1 | Focused task-list links in the dark theme: light text on the yellow focus highlight, 1.35:1 (91 focus stops on 8 of 15 routes). Cause: an app-level colour rule overrode the focus colour. | 1.4.3 fail | The rule is wrapped in `:where()` and focus colour restored. Re-measured: dark text on the highlight. |
| 2 | Stale `aria-activedescendant` after typing in the header search | 4.1.2 fail | The active option resets on every rebuild. ArrowUp from none goes to the last option. |
| 3 | The skip link rewrote the address to `#main`. Reloading gave a blank page, and exports cited `#main`. | intent of 2.4.1 | In-page anchors never change the address. A first load with a non-route hash renders home. |
| 4 | Search suggestions unreadable in Windows contrast themes | forced-colours gate | The selected option is marked with an outline and bar, and matched text is shown bold and underlined. |
| 5 | Search and Compare announced only "… loaded" | 4.1.3 advisory | Views can return a specific announcement. Search and Compare provide one (round 2 view work). |

## Other issues and round 2 status

- **Fixed in shared code:**
  - the release strip now sits inside a labelled landmark;
  - Back restores focus to the element the user left from;
  - "On this page" comes after the content in the DOM, so there are fewer tab stops before the content;
  - notice titles are no longer headings by default, which fixes the outline;
  - the disclosure chevron rotates;
  - data-table hints sit outside the caption;
  - scroll regions are focusable only when they scroll;
  - the first live-count value is not announced;
  - level chips read "Proficiency level L3 …";
  - the issues address is printed;
  - search options have short accessible names, with no nested link and a correct plural;
  - in forced colours, the overlap bar's second segment is drawn as an outline.
- **Assigned to round 2 view work:**
  - "Show all" moves focus to the first newly shown item;
  - a page title for Compare;
  - the Compare column heading levels;
  - an SVG pattern for the overlap bar's second segment;
  - home figures with their nouns in one element;
  - filter links that work when opened in a new tab.

## Strengths confirmed
- No horizontal scroll at 320px or at 400% zoom; text-spacing test passed on 17 routes.
- No target-size failures.
- Text contrast passes in both themes, including the "pending" hatch.
- Tabs and filters follow the ARIA Authoring Practices.
- Focus moves to the H1 and the change is announced on every route change.
- Reduced motion is honoured.
- Printing a role includes every task, the release block and the URL.
- The accessibility statement is honest and claims no conformance.
