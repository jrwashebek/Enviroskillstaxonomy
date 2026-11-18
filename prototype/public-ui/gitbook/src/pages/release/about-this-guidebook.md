---
path: release/about-this-guidebook.md
title: About this guidebook
description: How this guidebook is built from the same release as the explorer, what is checked before each update, and what it does not hold.
---

This guidebook is a reading layer for EMST. It explains how to read and use EMST. It is not where EMST is kept or changed.

## How it is built

- These pages are built from release {{release}} by the same build as the [EMST explorer](explorer:/), with the same display rules. A figure here and the same figure in the explorer always match.
- The pages are written to GitHub first and then copied to GitBook. The copy goes one way only. Nobody edits these pages in GitBook. A fix goes into the files on GitHub, and the next build updates both sites.
- Every count on these pages comes from the release files. None is typed by hand.

## What is checked before each update

Scripts check every page before it is copied to GitBook. If a check fails, nothing is copied, and the site keeps its last good version. The scripts check:

- the claims list, a list of things EMST must not say because they could not be confirmed;
- that no page shows or describes held content;
- that no page recommends a career move, says that someone qualifies, or states a change in the work as fact;
- that every link works and every page is in the menu;
- that headings, tables and links follow the accessibility rules;
- the reading level, which aims for US grade 8 or lower.

## What is not here yet

- **Pages for each role, competency and subject module.** They will be built from each release, like these pages. Until then, they are in the explorer.
- **Tasks.** All {{tasks}} tasks stay in the explorer, on each role's and competency's page.
- **Compare, employer versions and downloads.** These need the explorer's own code.

## Who made it

AI agents drafted these pages, working to rules set by the EMST project lead. No person has reviewed them yet. [How EMST was made](page:start-here/how-emst-was-made.md)
