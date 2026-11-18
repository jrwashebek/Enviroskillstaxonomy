# EMST on GitBook: build, check and connect

Project-lead decision Q17 (16 November 2026) brings GitBook back as a **reading layer** beside the explorer: a guidebook plus, later, a reference generated from each release. ADR-0020 (item 17) and ADR-0011 carry the amendment. This file covers phase 1, the guidebook, and how to connect it to GitBook.

GitBook is never the source of truth. The pages are built here, checked here and copied one way to GitBook. A fix always goes into this repository.

## What is where

| Path | What it is | Edit it? |
|---|---|---|
| `gitbook/src/pages/` | Pages written for the guidebook, in Markdown. Every count is a `{{token}}`; links to other pages are `page:` links, and links to the explorer are `explorer:` links. | Yes |
| `gitbook/src/config.json` | Addresses: the explorer (not online yet), the repository, Issues, the Markdown copy, GitBook's cookie statement. | Yes |
| `app/assets/js/content.js` | The explorer's copy. The guidebook reuses its about pages word for word: How to read EMST (split into one page per label), How EMST was made, Release status, Data and downloads, Corrections and contributing, Held records and the glossary. | Yes, for both sites at once |
| `app/data/*.js` | The explorer's data, built from the release by `tools/build-data.mjs`. The coverage pages and every count come from here. | No: rebuild it from the release |
| `gitbook/site/` | **Generated.** The folder GitBook's Git Sync reads: `.gitbook.yaml`, `README.md`, `SUMMARY.md` and the pages. | Never by hand |
| `tools/build-gitbook.mjs` | Builds `gitbook/site`. `--check` fails if the folder differs from a fresh build. | |
| `tools/check-gitbook.mjs` | The checks that must pass before any sync. Writes `docs/qa/gitbook-check.json`. | |
| `tools/preview-gitbook.mjs` | Renders the site as one HTML page that reads like GitBook, for review; `--axe` runs axe-core on every page. | |

## Commands

From the repository root, with Node 22:

```bash
node prototype/public-ui/tools/build-data.mjs        # only when the release changes
node prototype/public-ui/tools/build-gitbook.mjs     # writes prototype/public-ui/gitbook/site
node prototype/public-ui/tools/check-gitbook.mjs     # must exit 0 before any sync
node prototype/public-ui/tools/preview-gitbook.mjs /path/to/preview.html --axe   # optional review copy
```

The tools use `site/node_modules` (js-yaml, markdown-it, axe-core) and Playwright, as the explorer's own checks do.

## What the checks cover

`check-gitbook.mjs` fails on any of these:

- **Build drift.** `gitbook/site` is not exactly what the build makes. This also catches edits made in GitBook that synced back.
- **Structure.** `.gitbook.yaml` is wrong; `SUMMARY.md` misses a page, lists one twice or lists one that does not exist.
- **Page rules.** A missing description; not exactly one h1; a skipped heading level; unbalanced hint blocks; a missing release ribbon or footer; an unfilled token or unresolved link.
- **Links.** A broken page link or anchor; a link that is not https or carries a query string; vague link text; an image with no alt text; a malformed table.
- **Honesty rules**, the same as the explorer's `check-rendered.mjs`: the claims register; Tribal hold triggers outside the verbatim policy and statement; any description of held content; recommending a move; "you qualify"; jargon; email addresses and phone numbers. Added for the guidebook: change stated as fact, forecasts, and private or build-machine paths.
- **Figures.** The home page's counts must equal the release's `counts.json`.
- **Reading level.** A page whose sentences score above US grade 10 fails; above grade 8 is a warning. Lines of names (roles, modules) are not scored.

A seeded test (a page with "you qualify", a recommended move, a change stated as fact, a trigger word, a broken link, a query string, an email address and a private path) fails on every one of them.

Results for this build: 42 pages, 0 failures, 0 warnings, median reading grade 4.3. axe-core 4.14 on the preview: 0 violations on all 42 pages in light and dark, and no sideways scrolling at 375 pixels.

## Before connecting

These are conditions of decision Q17. None of them is done by the build.

1. **Account ownership.** The host organization already has a GitBook organization, and the project lead is a member. Before launch, the owner (admin) role and the billing should sit with the organization, not one person, and the project lead should have the admin role.
2. **GitBook's November 2026 security incident.** GitBook asked customers to finish the steps listed on its incident page (gitbook.com/status/security-incident-2026-11-03) before relying on Git Sync again. Do that first, including any re-authorization of the GitBook GitHub app.
3. **Which GitHub account.** The GitBook GitHub app must be installed on the account that holds this repository. Alternatively, move the repository to the organization's GitHub first (decision Q15).
4. **Plan.** Git Sync and a gitbook.io address work on GitBook's free plan. A custom font, logo or domain needs Essential or above. GitBook's Community plan is free for eligible non-profit and open-source projects and includes the Ultimate features except SAML (as listed in November 2026). Check whether EMST qualifies before paying for more.
5. **Explorer address.** While `explorerUrl` in `gitbook/src/config.json` is null, explorer pages and record names are written as plain text, and each page says the explorer is not online yet. Set the address once the explorer is public, then rebuild.
6. **Markdown copy.** `markdownCopy` in the config points at this branch. Change it when the guidebook moves to `main`.

## Connecting Git Sync

1. **Create a space** in the organization, named "EMST guidebook".
2. **Make a publishing branch.** Sync GitBook to a branch that changes only after the checks pass, not to a working branch:

   ```bash
   node prototype/public-ui/tools/build-gitbook.mjs --check \
     && node prototype/public-ui/tools/check-gitbook.mjs \
     && git push origin HEAD:refs/heads/gitbook-publish
   ```

   This is what makes the guidebook's statement true: "If a check fails, nothing is copied, and the site keeps its last good version." A GitHub Actions job can run the same three steps on each release later.
3. **Configure Git Sync** on the space: provider GitHub; this repository; branch `gitbook-publish`; project directory `prototype/public-ui/gitbook/site`. For the first sync, choose GitHub → GitBook.
4. **Keep it one way.** Give every member except one maintainer the reader role. If anyone edits in GitBook, the edit commits back to `gitbook-publish`, and the next `build-gitbook --check` fails. Revert that commit and put the fix in `gitbook/src`, `content.js` or the data.
5. **Publish the space** as a public site. Customize it to the Ground Truth look the project lead chose: primary colour pine `#23392f`, text font Source Serif 4, code font IBM Plex Mono. GitBook allows one text font, so Barlow Condensed and the field-note face appear only inside images.
6. **Leave these off:** the AI Assistant (phase 3 only, after its red-team question set passes) and any third-party integrations. If page feedback stays on, the privacy page already says where the answers go.
7. **Test accessibility before launch** (a Q17 condition):
   - keyboard only;
   - NVDA with Firefox and VoiceOver with Safari;
   - 400% zoom and a 320-pixel-wide window;
   - Windows high-contrast mode;
   - axe-core on the live pages.

   Record the results on the guidebook's Accessibility page (`gitbook/src/pages/release/accessibility.md`). GitBook publishes no WCAG conformance statement, so anything found in GitBook's own layout goes to GitBook and onto the known-limits list.
8. **Re-read GitBook's cookie statement.** The Privacy page quotes it: GitBook says it runs Google Analytics on the sites it hosts. Check that this is still true at launch.

## Phase 2 and 3

- **Phase 2: generated reference.** Pages for the 37 roles, 223 competencies and the subject modules, generated by the same tool from `app/data`, read-only, under three new SUMMARY groups. Tasks stay in the explorer. Role-change expectations enter only if decision Q16 allows. When record pages arrive, restore the "Pages and release files can differ in wording" section of Data and downloads, which phase 1 leaves out.
- **Phase 3: GitBook's AI Assistant.** Switched on only after it passes a red-team question set: questions about qualifying for jobs, recommendations and held content, with a person checking answers. It is switched off again on any failure.
