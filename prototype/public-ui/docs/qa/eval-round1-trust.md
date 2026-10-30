# Evaluation round 1: trust, honesty and content review

- **Evaluator:** "trust", an AI agent acting as an independent expert reviewer. No users took part, and no user quotes appear here.
- **Build:** prototype round 1, release 2.0.0-rc.1, 30 October 2026. The reviewer's scripts, rendered text, screenshots and exports were kept in the design working folder.
- **Severity:** Nielsen's 0–4 scale.

## Verdict per lens

| Lens | Verdict |
|---|---|
| **U5, federal HR and classification** | **Not yet safe.** The "You can't" lists and the HR notices are strong. But series pages read as OPM products: they show GS grade bands and "factor 1" knowledge, and the HR notice says the view supports "development and planning". "Not from OPM" appears only in the footer. |
| **U8, seasonal firefighter on a phone** | **Partly.** Compare carries "doesn't mean you qualify". The role page's "Where it can lead" lacks that caveat, and its N of M figures differ from Compare's. It also lists entry-level destinations. A search for "year-round" finds nothing relevant. |
| **U7, skeptical researcher** | **Partly.** All 30 numbers recomputed from `app/data` match the screen. But records that cite no source still say they were written "from sources". The page defines "N of M" in two ways, and internal codes leak. |

## Over-claiming

- **O1 (3). The HR notice claims a development use.** `core.text.hrDisclaimer` says "This view describes work for development and planning", but no record reaches the develop tier. The notice appears on the HR hub, every series and class page, the federal and state role tabs, Compare and the text export. On series pages it sits directly above "Explore only · Not for plans or decisions".
- **O2 (3). Explore-only content is offered for planning.** All 559 competency targets and 214 of 223 competencies are exploratory. Yet:
  - the home page offers "Find competencies and levels for a course or training plan";
  - the HR hub says levels can be copied into your own tools;
  - role pages place the competency table under the "Describe and plan" status line.
- **O3 (3). Provenance over-claim.** Every record says it was written "from sources", and the review ladder marks "checked facts against sources" as done. Yet these cite no source:
  - 37 of 37 roles;
  - 1,268 of 1,317 tasks;
  - 102 of 223 competencies.
- **O4 (3). Series and class pages read as government products.** They show "OPM series …" headings, FES "factor 1" language, and GS bands with no AI-judgment note on the series page. The only independence statement is the footer, near the bottom of the page.
- **O5 (3). "N of M" is inconsistent and reads as a requirement.** One Compare page gives "14 of 23" and "12 of 20". The role page says "12 of the 20 competencies that role needs", with no qualify caveat. The edge compares lead level with journey level and takes the best variant. Entry-level roles appear as destinations.
- **O6 (2). The footer implies review.** "No independent expert has reviewed them" suggests some other review took place.
- **O7 (2). What's changing.**
  - The no-regret moves come before their caveat.
  - "Nothing here is a forecast" sits beside projection signals.
  - "Roles that may be forming … appear only on this page" is false for two full profiles.
- **O8 (2). "Required" appears beside "may be involved"** in friction text.

## Under-informing

- **U1 (2). The CSV drops caveats.** It omits "assessment pending" (not zero) and "not a job analysis or classification basis".
- **U2 (2). Zeros hide links.** The series index shows "0" close links for 65 series; 28 of those have other AI-suggested links.
- **U3 (2). The ladders contradict each other.** The review ladder's "Cleared for a stated use: not yet" conflicts with the use ladder's "Describe and plan: this record".
- **U4 (2). Malformed measures.** "102 test cases (out of 19 agencies)" uses a sample size as a denominator, and "80.57 mentions per 1,000" shows decimals.
- **U5 (2). Internal codes leak.** Examples: "WP-10" (×10), "development_stage=" (×9), "ADR-0007" (×6), "SC-030", v1 file paths in the v1 drawer, and the grade-17.8 "default view" note.
- **U6 (1). Minor.**
  - "37 roles · Explore only" on the home figure, while 31 role pages say "Describe and plan".
  - "Order of this list" appears where there is no list.
  - The pending items run on as one comma list.
  - "—" is used for "no target".

## Caveat count (role page, disclosures closed)

- **Before the first task:** five caveat statements in three visual units: the ribbon, the status line and the badge. That meets the lean-layering requirement. One is redundant: the badge repeats the ribbon.
- **Whole page:** 21 caveat lines. The AI status appears five times. The HR notice appears twice, word for word. The pending notice appears twice.
- **Fatigue risk:** moderate. It comes from the duplicates.

## Plain language (interface text only, with record data excluded)

| Measure | Score |
|---|---|
| Flesch–Kincaid grade, all 615 blocks | 5.9 |
| SMOG | 9.1 |
| Dale–Chall | 6.3 |
| HR notice | grade 9.8 |
| Held policy plus statement | grade 9.1 |
| v1 drawer body | grade 9.1 |
| Pathways notice | grade 8.1 |
| HR default-view note | grade 17.8 |

## Tribal hold

- **Pass: `#/about/held`.** It shows exactly the policy, the count (163) and the release's Indigenous statement, with no Labels, Notices or "coming soon".
- **T1 (4). Held content described on competency pages.** Six enactment notes on two competency pages describe categories of held content. Examples: "Consultation content held under ADR-0007 §D is not authored here"; "Agreement types covered by the ADR-0007 hold route through held competencies". This makes the policy sentence "These pages neither show nor describe it" untrue. **The same notes render on the current public explorer** (for example `site/_site/competencies/cmp-8qwcq3r/`), so the issue is in the release data, not only the prototype.
- **T2 (3). Search mishandles hold terms.** "Tribal" is respelled to "trial". "Indigenous" and "tribe" get "EMST may not cover this work yet" with "Suggest a role or task we're missing", which implies "coming soon" and invites submissions.
- **L1 (2). Latent agent label.** The agent-name map in `ui.js` holds a "Tribal advisory (simulated)" label. No rc.1 record uses it, but it would present AI as a Tribal voice.

## Government look-alike (expert self-test against CT-0)

- **The statement is too low.** "Not a government website" first appears at y = 5,342 of 6,287 px on a phone, and no header names an owner.
- **Pushes towards "government":**
  - Public Sans with Merriweather, the USWDS default pairing;
  - a formal acronym wordmark;
  - "For HR and classifiers" in the navigation;
  - "OPM series" headings.
- **Pushes away:**
  - the green and cream palette;
  - no seal or banner;
  - the AI-draft ribbon;
  - the GitHub links;
  - the CC0 licence.
- **Expected CT-0 result:** marginal on home; likely a fail on series pages.

## Numbers

30 figures were recomputed from `app/data`, independently of the view code; **all match**. The failures are in how figures are labelled ("N of M", "out of"), not in where they come from.

## Ranked fixes, as proposed by the reviewer

1. Strip held-content sentences (`ADR-0007`, "held competencies", "content hold") at build time, and add a build test. Report it to the data owner.
2. Replace the HR notice with "describes work; not ready for training or development plans; any PD built from it is a draft subject to classification review".
3. Search: never respell hold terms. Return the held-records page as the single result, and suppress the "not covered yet" and "suggest" copy for them.
4. Series and class pages:
   - put "This page is not from OPM / {jurisdiction}" first;
   - H1 "0456 Wildland Fire Management", with the eyebrow "Federal job series · EMST draft notes";
   - band heading "Grades an AI agent suggested: GS-3 to GS-5 (not a classification)";
   - rename factor 1 to "Knowledge statements (AI draft; not FES factor levels)".
5. Explore-only wording:
   - on the home link ("Explore competencies and levels for a new course");
   - above the role competency table;
   - on the HR hub;
   - in the competency notice.
6. Provenance by source presence: "wrote this record from their own judgment; it cites no source"; ladder step 2 "Checked by scripts (no source to check against)".
7. "N of M": say "At lead level, this role has 12 of the 20 competencies the {destination}'s draft profile lists for journey level", add the qualify caveat, and drop or tag downward destinations.
8. Footer: "No person has reviewed them yet."
9. CSV: add `importance`, `time_share`, `critical` and `needed_at_entry` columns, each "Assessment pending (not zero)", and expand the notes column.
10. What's changing:
    - retitle the no-regret heading and put the caveat first;
    - say "EMST makes no forecast; some signals report others' projections";
    - fix the "only on this page" claim;
    - drop "required" beside "may be involved".
11. Series index "0 close · 14 other"; rename the ladder rung "Cleared for training or hiring input"; fix measure denominators and decimals.
12. Hide internal codes in default views. Move v1 file paths into a technical disclosure. Rewrite the default-view note.
13. Put the independence statement in the release strip on every page, and test a serif that isn't the USWDS default in CT-0.
14. Remove the latent Tribal agent label.
15. Fatigue:
    - show the HR notice once per page;
    - drop the duplicate AI badge where the ribbon shows;
    - put the pending items in bullets;
    - write "No target" for "—".
