# Independent recheck: EMST v2 sector-facing package after the fix pass

*Checker: independent AI agent (Anthropic's Claude); did not write or fix any of this package · 2026-10-23 ·
scope: `docs/package/README.md`, `report/flagship_report.md` (draft 0.9.1) with `report/figures/` and `claims_used.csv`,
`briefs/` (README and R01–R13), `deck/deck_content.md`, `forester_pd_fes_draft.md`; the explorer (`site/_site/`) only
where a must-fix names it. No package file was edited. Helper scripts are in the session scratchpad
(`/tmp/claude-0/-home-claude/fbbe9940-26ca-5e5a-9a05-1e06b16da4ee/scratchpad/recheck/`). The fixers' logs were treated
as claims to test; discrepancies are listed at the end. This recheck is itself an AI-agent check, not a human review.*

---

## 1. Verdict

**Ready for the NGO-pilot preview after a short edit pass; not ready for external release.**

- Of the 33 ordered items (12 package must-fixes, 16 evidence must-fixes, 5 WP-15 required corrections), **28 landed,
  5 are partial and none is missing**. Every partial item has its core fix in place; what remains is a residue or a
  decision only the project lead can take.
- The fixes broke nothing structural. All 118 report references resolve, all 56 deck citation numbers exist in the
  report and support their slides, every internal link resolves, no `{{EMST_CONTACT}}` placeholder is left, every
  document carries the authorship statement and exactly one GitHub Issues call to action, and no single-quoted
  `do_not_say` form appears in substance. All 12 report numbers I spot-checked match their register rows.
- **Two new must-fixes** should go in before a preview link reaches the NGO cohort. (N1) The package README says the
  generated HR views ship in the release bundle, but those files still print the agent-drafted duty percentages and
  critical/needed-at-entry flags that were removed from the PD. (N2) The explorer still renders the unverified REG-06
  rescission headline as an instrument title on six pages.
- About ten should-fix edits are listed in section 6. Most are one-line changes.

---

## 2. Must-fix tables

Legend: **Landed** = the ordered fix is present in every location the review named. **Partial** = the core fix is in
place but a named element is still missing or wrong. **Missing** = not done. Residues found outside the named locations
are logged as new issues (section 5) and cross-referenced.

### 2.1 Package review must-fixes (`docs/review/package_review.md`)

| # | Issue | Status | Evidence (file:line, quoted) | Remaining |
|---|---|---|---|---|
| PKG-1 | Time shares and C/E flags that the display rule withholds | **Landed** | R01:28 "This is a selection; EMST shows no time shares."; R01:30 "\| Task \| Formation task \|" (same in all 13); forester_pd_fes_draft.md:30 "### 1. Inventory forest resources and assess forest conditions (___%)"; report:465 "Percentages of time, criticality and needed-at-entry flags are left to the supervisor and the job analysis."; README:31 "Each duty's percentage of time is left blank for the supervisor"; deck:250 "they show no time shares"; deck:360 "Fields for time share, criticality and entry needs stay empty in public views" | Residue in words at R03:70 (N5). The generated HR views the README says ship still print the values (N1). |
| PKG-2 | "Verified" status lines contradicted by the claim lists | **Partial** | report:8 "**Status: draft for NGO-pilot preview (23 October 2026).** AI agents checked facts against sources. Every external reference is now tied to a claims-register row, but 10 of those rows record limits"; README:6, deck:7, briefs/README:5 and every brief header use the generic line; report:57–61 five register-mapped labels; deck "awaiting WP-15" table gone (deck:487 is now "Before presenting: re-check these moving facts"); R11/R12 "submitted for WP-15" gone | Refs 7 (report:564) and 92 (report:649) say "register-verified" but cite verified-partial rows RPT-02 and UAS-01, so the status-line count of 10 should be 12 (N3). Explorer: REG-06 headline still rendered as an instrument title (N2). |
| PKG-3 | AI authorship hidden behind role titles | **Partial** | Authorship statement in every document (report:10; README:11–14; deck:11–14; briefs/README:9–12; each brief colophon, e.g. R02:144–147; PD:5); report:377 "EMST's foresight agent (the AI agent in EMST's Strategic Foresight Lead role) drafted four scenarios"; R01:104 "EMST's curriculum draft estimates" | §5 rule not rewritten: report:350 "Those roles are AI agents, so that step alone would be AI checking AI. A change has been requested ...; the decision is pending." (CR-FIX-A-001, **decision for the project lead**). Status line report:8 names "sign-off by EMST's adoption lead" without saying it is an AI agent role (N4). |
| PKG-4 | Agent drafts presented as findings | **Landed** | report:24 "**3. Policy is moving faster than technology, and AI's effect on roles is still a hypothesis.**"; report:296 "Could get quicker where tools are used (capability evidence; not observed)"; deck:230 "### Slide 9. Hypothesis: the new work is checking"; deck:247–248 "The drafts were written by agents that had read the same evidence, so their agreement with it is not independent confirmation."; deck:285 "This is the career-ladder hypothesis"; R13:70 "AI drafting tools are now available for entry tasks that form judgment" | — |
| PKG-5 | "Budgets" named as a cause | **Landed** | deck:82–83 "followed personnel, hiring and grant decisions, not AI. Appropriations fell far less than staffing, and most of the decline came before the FY2026 spending bill."; report:20 "These changes followed personnel, hiring and grant decisions ... Appropriations fell far less than staffing [32]."; figures_index F01 "The sources tie the decline to personnel and hiring actions"; briefs/README:59 | R09:45 still sets FY2026 funding against 2024–26 losses (N6). |
| PKG-6 | Internal acronyms and IDs | **Landed** | Role acronyms replaced, e.g. R02:86 "EMST's foresight analysis (a desk exercise by an AI agent, not yet reviewed by a human panel)"; series-fit glossary briefs/README:96–97; IDs confined to technical notes (e.g. R01:174, deck:509, PD:142, report:552) | Reference list still carries WP-10, WP-08, WP-14 and Q-codes (NH1). |
| PKG-7 | Questionnaire rule without exceptions | **Landed** | report:466 "except for seasonal positions, positions at GS-4 and below, and other OPM-authorized cases"; deck:57–59; deck:399–400; R01:129–131; deck:61–63 "which is not a date for natural resources specifically" | — |
| PKG-8 | Call to action leads nowhere | **Partial** | One GitHub Issues CTA in each of the 18 documents (e.g. report:540, deck:482–483, README:83–84, PD:138, R01:171–172); deck:440–447 gives funding status, what participants give and get, selection and open-call timing; report:483 "It is not yet funded" | The "How to take part" block the review ordered is only in the deck. The report and briefs lack what participants give, eligibility, the pilot agreement template and a reply-by date (N7). The explorer has no public URL. |
| PKG-9 | Truncated PD text | **Landed** | 0 "…" in forester_pd_fes_draft.md; full duty sentences, e.g. PD:32; provenance footer PD:142 | — |
| PKG-10 | Explorer build and output check fail | **Landed** | `check-output.mjs` run on a scratch copy of `site/`: "[check] OK: 782 pages, 852 files, 1108 figures with badges, 2178 v1 drawers, 821 outbound links (navigation only), 0 problems" | Not rebuilt here (the build deletes `_site/`). PLAN-01 "monitoring requirements" still renders on 26 explorer pages (deferred, CR-FIX-A-003). |
| PKG-11 | Jurisdictions presented as participants | **Landed** | R03:24 "a sample of states, one county environmental health department and one municipal utility; no agency has been involved"; deck:411–412; README:32 "a federal-to-state crosswalk EMST proposes to test with a state partner"; deck:456 "No organization has committed."; no "Corps Network" anywhere | — |
| PKG-12 | AmeriCorps settlement overstated | **Landed** | report:108 "covers FY2026 in those jurisdictions only; it does not cover programs elsewhere. ... Corps leads should check whether their state is in the coalition."; R01:89–92; R01:125–126 | Deck cites [111] for the settlement (NH8). |

### 2.2 Evidence review must-fixes (`docs/review/evidence_review.md` §7)

| # | Issue | Status | Evidence (file:line, quoted) | Remaining |
|---|---|---|---|---|
| EVD-1 | Status box and About (R96) | **Landed** | report:8 (above); report:10 "AI agents checked the facts against sources in October 2026"; report:47 "The claims list ... records, for each claim, the claims-register row behind it, or flags that it still needs one"; claims_used.csv: 280 claims, 143 with register rows, 137 EMST-record only, none awaiting a row | Label residue N3. |
| EVD-2 | New Jersey EJ (R33) | **Landed** | report:138 "the New Jersey Supreme Court granted certification in July 2026, and the rules remain in effect while that appeal is pending [113]"; R10:100–102; deck:172–173; F09 csv:51; register EJ-02 corrected | — |
| EVD-3 | AmeriCorps reinstatement (R15) | **Landed** | report:108 "In July 2025 AmeriCorps also told grantees ... including programs in states that had not joined the litigation, that they were eligible for reinstatement"; report:354 "then reinstated in the plaintiff states and offered for reinstatement elsewhere in July 2025"; F09 csv:19 | — |
| EVD-4 | Pennsylvania (R19) | **Landed** | report:114 and :473 "has identified federal job titles whose experience may count as equivalent for certain Commonwealth titles"; R11:113–115; R12:115–116; deck:412–414 | — |
| EVD-5 | Executive summary items 3–5 | **Landed** | report:24 (item 3); report:26 "AI and sensors could compress the tasks juniors learned on; their actual use inside agencies is unmeasured ... long-tenured staff"; report:28 "a desk exercise drafted by an AI agent ... That verdict partly follows from how the scenarios are defined" | — |
| EVD-6 | Exposure ranks (R53) | **Landed** | report:22 "fall in the top fifth ... in or near the bottom third"; report:193 "### 2.2 Exposure: a gradient, not one number"; report:195 BLS categories named as the license-free route | figures_index NOT-BUILT-1 still titled "Two exposure profiles" (NH7). |
| EVD-7 | OMB counts (R61–R63) | **Landed** | report:22 "eleven federal environmental units (nine bureaus and two USDA mission areas) ... 232 of the 329 use cases that report a type"; report:215 units listed with counts | Deck slide 4 title (deck:103) still reads "Most registered environmental AI is science work" (N8). |
| EVD-8 | Plan monitoring (R80, F05) | **Landed** | report:266 "this section describes western national forests only ... 84 written under the 1982 Planning Rule and 36 under the 2012 rule"; report:268 "That gap does not survive a closer look ... their 95% intervals overlap"; figures_index F05 headline; no "durable demand" or "monitoring requirements" in package text except as named wrong forms (README:60–61) | — |
| EVD-9 | Scope words (§4.4) | **Landed** | report:20 "The largest measured change in federal environmental jobs"; report:26 "In federal land agencies and conservation corps"; report:318 "### 4.2 Field craft in federal land agencies" | report:518 "thinning of the public workforce" (NH6). |
| EVD-10 | Merit hiring (R82, R84) | **Landed** | report:466–467 exceptions and "the plan's governmentwide target for full implementation is the end of FY2028"; FED-03 wrong form absent | — |
| EVD-11 | Missing caveats | **Landed** | report:240 Canaries caveats; :242 "users reported saving"; :243 GDPval includes compliance officers; :320 GAO caveat; :197 "these are Anthropic estimates, and they rely partly on ratings made by Anthropic's own model"; :148 "540 Forest Service Good Neighbor agreements" | — |
| EVD-12 | Citations | **Partial** | [114] PNNL release (report:671); [115] reginfo.gov and [116] FY2024 NDAA §1825 via FHWA (report:672–673); [97] Harvard Project on Workforce (report:654); [70] January 2026 URL (report:627); [63] rounded values (report:163) | [42] still a mirror, "Congress.gov itself to be read before release" (report:599); [64] still trade press (report:621); [50] URL "may be truncated and could not be re-opened" (report:607). Before external release. |
| EVD-13 | Figures | **Landed** | F09 headline rebuilt from data (recount: 50 dated actions, 11 other steps, 6 scheduled for 2027 — matches); F02/F03/F05/F06 labeled "EMST derivation"; build_figures.py:102–127 fails on `superseded`; report:550 "checks key values against their verification records ... it does not check every cell" | — |
| EVD-14 | Sweeping and negative claims | **Landed** | report:118 "changed substantially in 2025–26 [J; 39]"; report:387 "(a not-found result, not a systematic docket search)"; report:22 "EMST's labor-market review found no study"; report:538 "In its October 2026 scan EMST found no standing environment-sector coalition" | — |
| EVD-15 | Appropriations timing (§4.6) | **Landed** | report:102 "Most of the staffing decline described above came before that bill, during 2025" | Residue in R09:45 (N6). |
| EVD-16 | Moving facts re-read | **Partial** | Each moving fact carries "as of 23 October 2026" and a re-check-after date (report:126, :127, :136, :143, :144, :160, :320, :467, :490); Methods list report:548; deck:487–499 | Re-reads are mostly not yet due (earliest 26 October). Fix-A could not read the Federal Register for OFCCP, the objection rule or Section 106. Block external release until done. |

### 2.3 WP-15 required corrections (`docs/methods/WP15_report_corrections.md` §A)

| Claim | Status | Evidence (file:line, quoted) |
|---|---|---|
| C008 (A1) | **Landed** | report:22 "Commercial AI tools are licensed at 10,000 or more users in EPA (drafting, summarizing and search tools), the Department of the Interior (a writing tool) and USDA (a search and knowledge-retrieval assistant)"; deck:131–133 same |
| C078 (A2) | **Landed** | report:154 "Flying is mostly a secondary duty: the agency's national UAS program manager has said that 99% of its trained pilots are collateral-duty pilots, whose primary job is something else [60]." |
| C155 (A3) | **Landed** | report:320 "drones, which so far are added to existing jobs more than they create new ones: 99% of Forest Service trained pilots fly as a collateral duty alongside another primary job [60]" |
| C122 (A4) | **Landed** | report:243 "GDPval, a widely cited benchmark ... covers 44 occupations; none is in environmental science, forestry or environmental engineering, though it includes compliance officers" |
| C177 (A5) | **Landed** | report:360 "In Danish data, chatbot time savings have so far shown no measurable effect on earnings or recorded hours [79]." |

`claims_used.csv` carries the new wording for all five rows. The old forms ("field staff who also fly", "absorbed into
field roles", "best-known", "drafting and summarizing assistants", "time savings show no effect") appear nowhere in the
package.

**Totals: 28 landed · 5 partial (PKG-2, PKG-3, PKG-8, EVD-12, EVD-16) · 0 missing.**

---

## 3. Sweep results

| Sweep | Result |
|---|---|
| (a) Single-quoted `do_not_say` phrases | 73 phrases extracted from 124 register rows, 296 raw substring hits. All were reviewed in context. **No substantive breach.** The hits are common words ("final", "deployed", "maintain", "MIT" inside "commitment"), safe forms that the register quotes ("components typed as monitoring"), or the README and deck naming a wrong form as one to avoid ("never 'realigned'", "never 'UGESP compliance'"). The RPT-05 "more than a quarter" hits never share a sentence with the 16% (report:96 keeps it in its own bullet: "should not be compared with it"). The double-quoted forms "nine environmental bureaus" and "monitoring requirements" are absent from package text, but the explorer still renders the second on 26 pages (deferred). |
| (b) Time shares, flags, craft ratings | No duty or task time share, no "critical", "needed at entry" or "distinguishing" flag and no craft rating in any package file. "Critical" appears only in task wording (R13:31, :99), staffing language (report:407) and "Lawshe critical values" (report:518). "20–30% field time" (report:339, R02:98, R04:65) is a provisional pathway-design rule, not a role time share. Residue in words: R03:70 "Most field time goes to instruments" (N5). Outside the package text: `docs/build/WP-08/generated/federal-series/0460.md:23–30` prints "— 14%" and "*(critical, needed at entry)*", and README:36–37 says these files ship (N1). |
| (c) verified / validated / cleared for the package | None. Uses are scoped: "register-verified" defined at report:10 and :57–59; "verified labels" (report:322) and "verified issuer" (PD:134) are ordinary uses. |
| (d) Placeholders and calls to action | No `{{EMST_CONTACT}}` in `docs/package/` or `site/src/`; the only occurrence is in fixlog_A. Each of the 18 documents has exactly one CTA linking to https://github.com/jrwashebek/Enviroskillstaxonomy/issues, and no other email address or contact URL appears. Report:30 and :483 point to the §8.5 CTA, which exists (report:540). |
| (e) Authorship statement | Present in all 18 documents. The report, README, deck, briefs README and all 13 briefs carry the full statement (some line-wrapped). The PD (PD:5) uses a faithful shortening: "Drafted by a team of AI agents (Anthropic's Claude) working to a charter set by the EMST project lead; not yet reviewed by independent human experts." |
| (f) Internal IDs in reader-facing text | Body text is clean: no seed IDs, COR-n, R-codes, SC/NR/CM codes, role acronyms or SKOS codes. IDs remain only in the technical notes (allowed) and in report reference entries: ref 24 "WP-10 method note" (report:581), ref 85 "(WP-08)" (:642), ref 99 "EMST WP-14." (:656), ref 107 "Project lead decisions Q1, Q2, Q5, Q7" (:664) (NH1). |
| (g) Cross-document consistency | Consistent across report, deck, briefs and README: the questionnaire rule with its three exceptions and the FY2028 target, New Jersey EJ, Pennsylvania, the F05 plan-monitoring result, OMB counts (504; 232/329; 61/347; 0 of 5) and federal workforce numbers (2,313,216 → 2,035,344; 12%; "more than a quarter"; 34.1%; EPA 12,849/−24%). Small drifts: AmeriCorps "it does not cover programs elsewhere" (report:108) vs "programs elsewhere have no equivalent protection" (R01:91, deck:292); R09:45 keeps the appropriations-timing mismatch the report fixed (N6); deck slide 4's title vs RPT-27 (N8). |
| (h) Deck citations | All 56 bracketed numbers exist in the report's 118-entry reference list, and each supports its slide. Exceptions: deck:292 cites [111] (the July 2025 reinstatement notices) for the 2026 settlement; deck:369 (the charter quote) and deck:427 ("claims no alignment") carry no citation where the report uses [21] and [89] (NH8). [D1] and [D2] are listed at deck:503–507. |
| (i) Internal links | All 27 markdown links resolve, and every repository path in the README, briefs and report references exists, except `docs/build/WP-07/staging/pathways/` (briefs/README:143). Pathway records now live in `data/v2/core/pathways/` and `data/v2/modules/forest/pathways/` (NH2). |
| (j) Personal data or the project lead's name | No personal name for the project lead; every credit reads "the EMST project lead". Named public officials and paper authors in citations are not personal data. Note: the mandated CTA URL contains the GitHub handle "jrwashebek", which identifies an individual account (NH11; decision for the project lead). |

### 3.1 Spot-check of report numbers against register rows

| Report text (file:line) | Register row | Match |
|---|---|---|
| 2,313,216 → 2,035,344, "about 278,000 or 12%" (report:91) | WF-01 | Yes (277,872; 12.0%) |
| EPA 12,849, "24% fewer than a year earlier" (report:94) | WF-03 | Yes |
| NRCS "down about 23.8% from September 2024 to November 2025" (report:95) | RPT-07 | Yes |
| $42.56 billion, 1.9% below FY2025, request $26.85 billion (report:102) | WF-09 | Yes |
| 540 Forest Service Good Neighbor agreements, "most of them with states" (report:148) | RPT-11 (426 with 39 states) | Yes |
| 63,884 fires, 9.0 million acres, 133% and 145% (report:152) | FIRE-01 | Yes |
| 4,536 drone hours, "78% more", 188,986 acres (report:154) | RPT-13 (from 2,553 hours: +77.7%) | Yes |
| 504 use cases; 232 of 329; 175 untyped; 61 of 347 deployed (report:215) | OMB-02, RPT-27 | Yes |
| 30.7% vs 2.7%; 22.2% vs 1.8%; plans only "about 10% (14 plans) and 3% (81 plans)"; 24 of 84; 29% (report:268) | PLAN-01 (10.0% vs 2.8%) | Yes |
| 91.23% and 34.3% of delegated-examining announcements (report:466) | FED-02 | Yes |
| Young-worker gap 19%; original 13%; revised 15% (report:240) | IDX-02 | Yes |
| Environmental scientist medians $116,110 / $83,500 / $81,580 / $80,500 / $79,320 (report:169–173) | RPT-18 | Yes |

12 of 12 match. The brief task counts ("Of the role's N draft tasks, the other M carry no drafted change claim") also
match the generated change views for R02–R13.

---

## 4. Cold read as a federal or state training officer

The package now reads as an honest draft. The status box, the authorship colophon and the "first draft for your staff
to correct" banner tell a reader what to trust before any number appears. The hypothesis framing of §5 now runs through
the executive summary, the deck and the briefs. The briefs' supervisor, training-officer and educator actions are
concrete and usable this season. What still confused or snagged on a cold read:

1. **The status line names a sign-off gate without saying who holds it.** Report:8 says "external publication also
   waits for sign-off by EMST's adoption lead". That lead is an AI agent role (TEAM_BRIEF.md:87), so the line repeats
   the "AI checking AI" pattern PKG-3 flagged (N4).
2. **"Reliability A" on EMST's own counts.** Eight briefs label the keyword-classified function counts "reliability A",
   which briefs/README.md:58 defines as "official primary data". The figures index already relabels the same
   counts "EMST derivation" (N9).
3. **Jargon in the federal HR section.** Report:468 says "use formation flags and protect suggestions". An HR reader
   will not know what a "protect suggestion" is (N10).
4. **An implied human panel.** Report:535 mentions "the practitioner panel's veto on usefulness" as if the panel exists.
   The deck says it is "still to be recruited" (deck:458–459) (N11).
5. **No way in for the NGO reader of the report.** The report tells an NGO lead about the pilot, but what they would
   give, how they apply and by when appear only in deck slide 17 (N7).

---

## 5. New issues

| ID | Severity | File:line | Problem | Exact fix |
|---|---|---|---|---|
| N1 | **must-fix** | docs/package/README.md:36–37; docs/build/WP-08/generated/federal-series/0460.md:23–30 (and the other generated federal-series and state-class files) | README:36–37 says "The underlying records, generated HR views and crosswalks live in `data/v2/` and `docs/build/WP-08/generated/` and ship in the release bundle under CC0 1.0." Those generated views print "**Major duties (indicative % of time, agent draft)**", "— 14%" and "*(critical, needed at entry)*", the exact values the PD fix removed. The README's own rule 2 (README:45–48) says such values are never shown. | Either apply the display gate in the FSP and SCV generators (CR-FIX-B-001) and regenerate before the bundle ships, or replace README:36–37 with: "The underlying records ship in the release bundle under CC0 1.0. The generated Federal Series Profiles and State Class Views are withheld from the bundle until they apply EMST's display rule; use the explorer's versions, which do." |
| N2 | **must-fix** (if the explorer link goes to the cohort) | site/_site/federal-series/0401, 0408, 0028, 0340; whats-coming; roles/r13-resource-program-manager/federal | The pages render "Rescission of unobligated IRA conservation and staffing funds (P.L. 119-21) (constrains this work; Unverified — not for citation (claims register REG-06))". PKG-2 warned that labeling this headline does not withhold it, and README:64 says unverified claims are not published. Fix-C withheld REG-06 as a signal but not as an instrument. | In the explorer (Fix-C lane), render instruments tied to REG-06 the way signals are already handled: "1 unverified instrument withheld (claims register REG-06)". Rebuild and rerun `check-output.mjs`, then confirm with `grep -rl "IRA conservation" site/_site` that it returns nothing. |
| N3 | should-fix | report:8, :564, :649 | Refs 7 and 92 carry the full "register-verified" label but cite verified-partial rows RPT-02 and UAS-01, so the status-line count of 10 is too low. | Ref 7: "(register-verified in part 2026-10-23: IDX-01, RPT-02)". Ref 92: "(register-verified in part 2026-10-23: UAS-01, UAS-02)". Report:8: replace "but 10 of those rows record limits" with "but 12 of those references are verified only in part". |
| N4 | should-fix | report:8 | "external publication also waits for sign-off by EMST's adoption lead [1]" reads as a human gate. | "external publication also waits for sign-off by EMST's adoption lead, an AI agent role [1]". |
| N5 | should-fix | briefs/R03-monitoring-data-technician.md:70 | "Most field time goes to instruments" is an agent-drafted time-share claim, stated as fact. | Replace with "Field time is expected to shift toward instruments (agent draft)". |
| N6 | should-fix | briefs/R09-restoration-project-lead.md:45 | "Appropriations fell far less than staffing: FY2026 Interior–Environment funding was 1.9% below FY2025 [3]" repeats the timing mismatch that EVD-15 fixed in the report (report:102). | "Appropriations fell far less than staffing: FY2026 Interior–Environment funding, enacted in January 2026 after most of the decline, was 1.9% below FY2025 [3]". |
| N7 | should-fix (PKG-8 residue) | report §8.5 (after report:538); briefs/README.md:127–130 | The ordered "How to take part" block is only in the deck (deck:440–447). | Add a short box to report §8.5 that copies deck:440–447: a named lead with about 0.1 FTE; kickoff, monthly cohort calls, office hours, peer pairing, a request-a-role route and a tiered stipend if funded; an open call planned for November 2026 – January 2027 with a three-person panel; the pilot agreement template (`docs/adoption/pilot_mou_template.md`). Add one line to the briefs README pointing to it. A reply-by date and eligibility need a **project lead decision** (CR-FIX-B-002). |
| N8 | should-fix | deck/deck_content.md:103 | The slide 4 title "Most registered environmental AI is science work, and most of it is not deployed" sits close to RPT-27's wrong form and is looser than its own headline. | "Classical machine learning for science is the largest type of registered environmental AI, and most use cases are not deployed". |
| N9 | should-fix | R02:46, R03:44, R04:46, R06:47, R08:48, R10:65, R11:44, R12:47 | "(2025 inventory, EMST keyword classification; reliability A)" grades an EMST derivation as "official primary data". RPT-28 forbids presenting the families as OMB's own classification. | Replace with "(2025 inventory; family counts are EMST's keyword classification of official data, not OMB's)". At R10:65, replace "(2025 inventory; reliability A)" the same way. |
| N10 | should-fix | report:468 | "use formation flags and protect suggestions" is jargon. | "use the formation flags and the tasks EMST's draft profiles mark for protection [28, 17]". |
| N11 | should-fix | report:535 | "with the practitioner panel's veto on usefulness" implies an existing human panel. | "with a veto on usefulness for a practitioner panel still to be recruited". |
| N12 | should-fix | site (explorer, 16 pages) | The explorer shows "Good Neighbor Authority incl. EXPLORE Act amendments", which the PD dropped for lack of a checked citation (PKG-18(g)). | Apply the PD's `plain_instrument()` treatment in the explorer, or register the citation (CR-FIX-B-003). |
| N13 | should-fix | site (explorer) | `vocab/scenarios.yaml` text still renders "intelligent customers" and "intelligent-customer capacity" (PKG-16). | Change to "informed buyers" and "informed-buyer capacity" via CR-FIX-C-001 item 3. |
| NH1 | nice-to-have | report:581, :642, :656, :664 | WP-nn and Q-codes remain in reference entries. | Ref 24: "Change signals, instruments and external exposure evidence: method note". Ref 85: delete "(WP-08)". Ref 99: "EMST (AI agents)." in place of "EMST WP-14.". Ref 107: "Project lead decisions (and defaults for open questions)". |
| NH2 | nice-to-have | briefs/README.md:143 | `docs/build/WP-07/staging/pathways/` does not exist. | Replace with `data/v2/core/pathways/`, `data/v2/modules/forest/pathways/`. |
| NH3 | nice-to-have | report:22, :215; deck:117 | "nine bureaus" counts EPA, an independent agency, as a bureau. | "nine agencies and bureaus and two USDA mission areas", with register OMB-02 updated to match. |
| NH4 | nice-to-have | R10:63–71 | The change table omits the transforming task "Determine whether an action needs an assessment or a full statement" (6 tasks carry claims; 5 are shown). | Add the row, or change the count line to "the table shows five of the six tasks with drafted change claims; the other 25 carry none". |
| NH5 | nice-to-have | R01:52 | R01 lacks the task-count line that the other 12 briefs carry. | Add: "Of the role's 29 draft tasks, the other 25 carry no drafted change claim." |
| NH6 | nice-to-have | report:518 | "thinning of the public workforce" (the evidence is federal). | "thinning of the federal workforce". |
| NH7 | nice-to-have | report/figures/figures_index.csv:12 | NOT-BUILT-1 is titled "Two exposure profiles", which EVD-6 retired. | "Exposure gradient (capability and usage indices)". |
| NH8 | nice-to-have | deck:292, :369, :427; R01:91 | [111] is cited for the settlement; two statements carry no citation; the AmeriCorps wording drifts from the report. | deck:292 "[34, 111]" → "[34]"; add "[21]" after the charter quote at deck:369 and "[89]" at deck:427; align R01:91 and deck:292 to report:108 ("it does not cover programs elsewhere"). |
| NH9 | nice-to-have | PD:51, :70 | British "modelled" from the data labels (deferred by Fix-B). | Fix the data label, or map it to "modeled" in the view. |
| NH10 | nice-to-have | deck:459–460 | A stray line break: "and requires / EMST identifiers". | Join the lines. |
| NH11 | nice-to-have (**decision**) | all CTAs, e.g. report:540 | The mandated URL embeds what appears to be an individual's GitHub handle. That is not a breach (the project lead chose the route), but it sits awkwardly with "credit only the EMST project lead". | Project lead to decide whether to move the repository to an organization account before external release. |
| NH12 | nice-to-have | docs/methods/claims_register.csv (RPT-27) | RPT-27 is an EMST computation but has status "verified"; its sibling RPT-28 is "derived". | Set RPT-27 to "derived". |

### 5.1 Fixer-log claims that did not hold

- **fixlog_A, row 112:** says the report's CTA is "{{EMST_CONTACT}}". The report actually carries the GitHub link
  (report:540). The log is stale; the output is right.
- **fixlog_A, orchestrator note:** "All 118 references are tied to register rows (10 of them only in part)." In fact 85
  external references are tied (33 are EMST records with no row, as the report itself correctly says), and 12, not 10,
  rest on partial rows (N3).
- **fixlog_B, summary:** "no time share ... appears in any of these files." The R03:70 residue (N5) is a time-share
  claim in words.
- **fixlog_C, row 27:** "Signals tied to unverified register rows are withheld entirely." That is true for signals, but
  the same REG-06 claim still renders as an instrument title (N2).
- The other log claims I tested held: the WP-15 wording is verbatim, F09's counts reproduce, the brief task counts match
  the data, the explorer check passes, the PD has no truncation, and `claims_used.csv` has 280 rows with 0 awaiting a
  register row.

---

## 6. Edits needed before the NGO-pilot preview

1. **N1:** apply the gate to the generated FSP and SCV files, or change README:36–37 so they are not said to ship.
2. **N2:** withhold the REG-06 instrument title in the explorer, then rebuild and rerun `check-output.mjs` before any
   explorer link goes out.
3. **N3 and N4:** relabel refs 7 and 92; correct the status-line count (12); identify the adoption lead as an AI agent
   role.
4. **N5, N6, N8, N9:** the one-line fixes in R03:70, R09:45, deck:103 and the eight "reliability A" cells.
5. **N7:** add the "How to take part" box to report §8.5 and a pointer in the briefs README.
6. **N10 and N11:** report:468 and report:535 wording.

**Decisions for the project lead** (named here because they block items marked partial):

- the §5 publication rule (CR-FIX-A-001: named human reviewers before the career-ladder hypothesis can be published as
  a finding);
- a reply-by date, eligibility and what participants receive (CR-FIX-B-002);
- whether the CTA should move to an organization account (NH11).

**Before external release, not the preview:** EVD-12 citation upgrades ([42] Congress.gov, [64] E2 primary, [50] URL);
EVD-16 moving-fact re-reads on or after their dates; reading the FED-10 memo content; the deferred SME-QA/USA Hire and
Public Lands Corps rows (CR-FIX-B-003).

**Carry-over:** the corrections Fix-A and Fix-B already flagged for the companion Skills Taxonomy project (NJ EJ,
AmeriCorps July 2025 notices and the coalition-only settlement, Pennsylvania wording, exposure percentile bands,
plan-monitoring sensitivity, the display rule) still apply. Add N1's point: generated HR views must not carry time
shares or flags.
