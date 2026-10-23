# Independent review: EMST v2 sector-facing package

*Reviewer: independent practitioner panel (simulated), not part of the build team · 2026-10-23 · scope: `docs/package/README.md`, `report/flagship_report.md` (draft 0.9), `briefs/` (README + R01–R13), `deck/deck_content.md`, `forester_pd_fes_draft.md`, plus the explorer as built. Read as five audiences in turn: a federal HR specialist (classification and staffing) at a land-management agency, a state DEQ training officer, an NGO programme lead (corps or watershed council), a university natural-resources programme director, and a skeptical journalist.*

**Method.** I read the package cold, as its audiences will, before opening any research or decision file. Afterwards I spot-checked about 20 claims against `docs/methods/claims_register.csv` and `docs/research/_verification/ALL_key_facts.csv`, read `report/handback_summary.md` and `figures/figures_index.csv`, and built the explorer. I did **not** independently re-verify external facts on the web. Severity: **must-fix** = do not release externally until fixed; **should-fix** = fix before rc.1 if at all possible; **nice-to-have**.

**Side effect to note.** Following the instructions, I ran `npm run build` in `site/`. It failed (issue 10), and its clean step had already deleted `site/_site/` (an untracked build output). I then built a scratch copy with a one-line shim (in my scratchpad, not the repo) to inspect the pages. `site/_site/` stays absent until the build is fixed and rerun.

---

## Verdicts by reader

**Federal HR specialist: not usable as it stands, though the framing is right.** The package gets the legal anchor right: job analysis under 5 CFR 300.103, never "UGESP compliance", and series shown as "proposed for realignment" rather than realigned. That is better than most vendor material. But the artifact I would actually pick up, the Forester PD, has sentences cut off mid-word ("site conditions and…"). It also carries duty percentages that EMST's own display rule says EMST must not supply. The self-assessment questionnaire rule is stated without its exceptions. And the package says nothing about SME-QA or USA Hire, the September 2026 RIF regulations, or collective bargaining. Fix those and the 0400 Kit offer becomes credible.

**State DEQ training officer: useful in parts, thin for a DEQ.** The permit-writer and inspector briefs (R11, R12) hold the most transferable training design in the package: unaided permits, seeded-error drafts, observed inspections, and budgeting evaluator time first. But only five of the 13 briefs touch regulator-side work, and none covers air, water, wastewater, drinking-water or waste staff, who make up most of a DEQ. The Pennsylvania model rests on a number that is not in the claims register. And "pilot jurisdictions (PA, TX, WA)" implies agreements that do not exist.

**NGO programme lead: closest to useful, and the most let down by the ask.** R01, R02 and the formation provisions describe how crews actually learn, and they give concrete actions for a season plan. But the pilot offer has no contact point. It does not say whether the pilot is funded or what participants get, and it asks for "0.1 FTE for ten months" for a 12-month pilot. It also drops the fact that the AmeriCorps settlement protects only coalition states. And the Public Lands Corps hiring authority, the federal fact my members most need, is never named.

**University programme director: least served.** The report's educator section is four bullets. There is nothing on v2's size or structure, no list of entry-level competencies, and no accreditation (SAF/ABET) or CIP-to-SOC plan, though the charter names all of these. No brief has an action for educators. The explorer exposes 31 role profiles that the package never explains. The ideas I would use, "no pixel without plot" (20–30% field time) and by-hand quotas before AI credit, are buried in §4.5.

**Skeptical journalist: careful on AI, exposed elsewhere.** The body is more careful about AI hype and doom than almost anything in this field, and the Anthropic conflict of interest is disclosed. The story I would write is a different one. AI agents wrote the package, AI agents "verified" it, and the "leads" who will "validate" the central hypothesis are also AI agents, yet after the opening status box the package never says this plainly. The second paragraph would cover:
- an executive summary and a deck slide that turn agent drafts into findings;
- a headline saying "budgets" caused the contraction, contradicted by the report's own appropriations figure;
- key federal facts sourced to letters from one party's members, a litigant's press release and an advocacy-outlet headline, while primary OPM data goes unused;
- "every claim verified" status lines that the package's own claim lists contradict.

---

## Issues

### Must-fix

**1. must-fix: The package publishes time shares and flags that EMST's own display rule withholds.**
- *Location:*
  - all 13 briefs, "The work today (agent draft)" tables ("Share of time" column and the C/E flags);
  - `forester_pd_fes_draft.md`: duty headings (14%, 13%, 11%…), every "Critical or needed-at-entry tasks" line, Factor 8 ("About 49% of the draft journey-level time share…"), and "Other information";
  - report §7.2, federal HR first bullet ("assembles major duties with indicative time shares… needed-at-entry flags");
  - package README, Forester PD row ("Major duties carry indicative percentages of time");
  - deck slide 9 notes ("The briefs give the time share of each task") and slide 14 body.
- *Problem:* The active display gate (`validation/display_gates.yaml` v1.1.0; CR-CP-001 B4; ADR-0030) and the built explorer both say: "% time: set by the supervisor; EMST supplies none before job analysis." They also say importance, time share, critical and needed-at-entry values "are not shown until a job analysis confirms them". The briefs README says that where a brief and the explorer differ, the explorer is authoritative. So the package prints exactly the numbers the system withholds. Worse, it prints them in the PD, the document a classifier is most likely to copy into a real position description. One-decimal shares for agent drafts (8.9%, 14.7%) also imply precision that does not exist.
- *Fix:*
  - In the briefs, drop the "Share of time" column and the C and E flags. Keep F (formation), which is an editorial value the gate allows, and list tasks in work order rather than by share.
  - In the PD, replace each percentage with "[% of time — set by the supervisor]" and delete the "Critical or needed-at-entry" lines and the 49% sentence.
  - Rewrite report §7.2 as: "Open the Federal Series Profile, which assembles draft major duties, task lists and Factor 1 knowledge statements from every federal role variant crosswalked to the series. Percentages of time, criticality and needed-at-entry flags are left to the supervisor and the job analysis."
  - Make the same change in the README and the deck.

**2. must-fix: Status lines say every claim is verified, but the package's own lists show otherwise.**
- *Location:*
  - package README Status ("Every external claim cites a verified source with a register ID") and rule 5;
  - report status box ("uses only facts that passed EMST's verification pass and the WP-15 claims check");
  - report reference labels "(verified; check: LM-0xx)";
  - deck slides 14 and 16, plus the closing table "Claims on this deck awaiting WP-15 entry";
  - briefs R11 and R12 (`[SL-080] … Not yet in the claims register; submitted for WP-15`);
  - explorer evidence drawer on every federal variant page (headline of REG-06 shown).
- *Problem:*
  - `report/handback_summary.md` says 35 report claims are not in the register. They include the NRCS −23.8% figure, the USDA OIG 16% figure, trail miles −22%, USFS drone hours and pilot share, the GAO drone findings, Trellis, E2, Census BTOS, Humlum, Yale, GDPval, AEI's first release, CRS's 540 Good Neighbor agreements, Pennsylvania's 1,350 hires, the New York portal, the skills-based-hiring results and the pay medians.
  - Several of these are labelled "verified" in the reference list, because the `check:` IDs are source IDs, not register rows. Register row RPT-05 says "OIG document not read", yet reference [26] reads "verified".
  - The explorer shows the headline "Unobligated IRA conservation, NPS hiring and USFS NEPA staffing funds rescinded (Unverified — not for citation)". The headline *is* the claim, so labelling it unverified does not withhold it.
- *Fix:*
  - Register-verify or cut every one of these before external release.
  - Rewrite the status lines to say what is true.
  - Replace the reference labels with three values that map to the register: **Register-verified (claim ID, date)**; **Source read, not yet register-verified**; **EMST record**.
  - Have the explorer suppress unverified signals entirely ("1 unverified signal withheld").
  - Remove the deck's "awaiting WP-15" table from any external copy.

**3. must-fix: AI-agent authorship is hidden behind human-sounding role titles.**
- *Location:*
  - report "About this report" ("comes from a source an EMST lead read directly");
  - references marked "read by role lead";
  - §5 publication rule ("only after EMST's industrial-organizational and labour-market leads validate it");
  - §6.1 ("EMST's foresight lead built four scenarios");
  - deck notes ("FS judgment", "LC judgment", "FH and AS have not yet confirmed");
  - briefs ("LC estimates…").
- *Problem:* The status box says AI agents wrote the report. Every later attribution uses a title a reader will take for a person. If the I-O "lead" is an agent, the publication rule for the career-ladder hypothesis means AI validating AI. This is the first thing a journalist will write about, and it will taint the parts that are genuinely careful.
- *Fix:*
  - Add one sentence to every piece: "EMST's 'leads' are AI agents assigned defined expert roles. 'Verified' means an AI agent checked the claim against the cited source on the date shown. No human fact-checker or subject-matter expert has reviewed this document."
  - Rewrite the §5 rule: "It will be published as a finding only after named human reviewers, a qualified I-O psychologist and a labour economist, validate it, and then co-published with a nonpartisan partner."
  - Use "EMST's foresight agent drafted…" in place of "EMST's foresight lead built…".

**4. must-fix: Agent drafts are presented as findings in the places readers read first.**
- *Location and rewrites:*
  - **Report executive summary, point 3.** "In the corridor roles EMST profiles first, change shows up as a shift in task mix. Producing first drafts… are getting quicker." This states the agent-drafted change views as observed fact, which the status box says the report never does. "Roles are being re-bundled, not deleted" also contradicts point 1: positions *are* being deleted (park rangers −34.1%), by policy. Rewrite as: "**3. Policy is moving faster than technology, and AI's effect on roles is still a hypothesis.** In 2025–26, rules and institutions changed review, authorization, hiring and disclosure work faster than any technology did [11–14]. Capability evidence suggests that desk tasks such as first drafts, compiling, comment coding and routine mapping can be done faster with AI, and that specifying, checking, signing and defending work would become more central. EMST's draft role profiles are built on that expectation, but no one has yet measured it in an environmental workplace [J; 6, 9, 10]."
  - **Report §3.3 column heading.** Change "Getting quicker (task-level time compression)" to "Could get quicker where tools are used (capability evidence; not observed)".
  - **Deck slide 9.** Change the title "The new work is checking" to "Hypothesis: the new work is checking". New headline: "EMST's draft role profiles, written by AI agents, expect the same new work in every corridor: checking AI and automated outputs. The pilot will test whether practitioners see it." In the notes, delete "The external evidence fits them" and write instead: "The drafts were written by agents that had read the same evidence, so their agreement is not independent confirmation."
  - **Deck slide 11 notes.** Change "This is the career-ladder finding" to "This is the career-ladder hypothesis".
  - **R13 competency table.** Change "AI is taking over entry tasks that form judgment" to "AI drafting tools are now available for entry tasks that form judgment".

**5. must-fix: "Budgets" are named as a cause of the contraction, against the report's own data.**
- *Location:*
  - deck slide 3 headline ("came from budgets and policy, not from AI"), with appropriations −1.9% listed beneath it as support;
  - report executive summary point 1 ("fiscal and policy drivers");
  - `figures_index.csv` headlines for F01 ("a fiscal and policy shock") and F08;
  - briefs README "Driver" row ("follows budgets and policy").
- *Problem:* Report §1.2 says Interior–Environment appropriations fell 1.9% while staff fell 12–25%: "Money and capacity have come apart." Putting the −1.9% under a "budgets" headline hands critics the rebuttal on the same slide. The verified drivers are personnel and hiring actions (separations, the hiring freeze and committee approvals, grant terminations), plus an agency-cited budget constraint for some decisions (V1-04, USFS seasonal hiring).
- *Fix:*
  - Deck slide 3 headline: "The 2025–26 fall in federal environmental staff followed personnel and hiring decisions, not AI and not appropriations: Interior–Environment funding fell 1.9% while the land agencies lost more than a quarter of their staff."
  - Executive summary point 1: "These changes followed personnel, hiring and grant decisions; appropriations fell far less than staffing [32]. No source attributes them to AI…"
  - Name the mechanisms factually, with primary citations (deferred-resignation offers, reductions in force, hiring freezes, EO 14356 approvals). That is both more useful and more neutral than "shock".

**6. must-fix: Internal acronyms and IDs make external text unreadable and, in one case, misleading.**
- *Location:*
  - **All 13 briefs:** "AS co-signature" in every header; "FS's no-regret move NR-1" (R02, R05, R09, R13); "FS's stress test" (R07); "SL's sample"; "LC estimates"; "X4 records `NoTermFound`"; `narrowMatch`, `relatedMatch`, `closeMatch`, `broadMatch`; `seed:R01-…`; "R37", "X11", "R23", "R31", "R35"; "WP-07 provisions"; "ADR-0023 §5"; "SPEC §10 rule 8"; "(editorial)"; "verified-partial"; repository paths in every Sources list.
  - **Deck notes:** "a CA decision", "LM's reading", "FH and AS", "report NOT-BUILT-2", "WP-15 §2.5", "Q3".
  - **Package README:** "AS co-signs", "rc.1", "[J; CA to confirm]", "Q6", "Q7", and "Being written in parallel by a separate WP-14 writer".
  - **PD:** "FH judgment".
- *Problem:* In this sector FS means the Forest Service, so "FS's no-regret move NR-1" reads as Forest Service policy, a misattribution to a real agency. CA reads as California and SC as South Carolina. The SKOS match codes mean nothing to an HR specialist. Process notes ("awaiting WP-15") tell outsiders the work is unfinished without telling them what to trust.
- *Fix:*
  - Replace the role acronyms with plain names, everywhere:
    - FS → "EMST's foresight analysis"
    - LC → "EMST's curriculum draft"
    - SL → "EMST's sample of state class plans"
    - CA, FH, AS, LM → the full role name (and see issue 3)
  - Replace the match codes with plain words:
    - closeMatch → "close fit"
    - broadMatch → "broader series"
    - narrowMatch → "more specific series"
    - relatedMatch → "partial fit"
    - NoTermFound → "no matching series"
  - Move ADR, WP and repository references into a single small-type "Provenance" footnote per brief.
  - Add a 10-line glossary to the briefs README and the report.

**7. must-fix: The self-assessment questionnaire rule is stated without its exceptions.**
- *Location:* report §7.2 ("Assessments" bullet); deck slide 2, first bullet; deck slide 15 notes ("Self-assessment questionnaires cannot rate and rank"). R01 has the exceptions.
- *Problem:* V1-09 records exceptions: seasonal positions, GS-04 and below, and OPM-authorized cases. The report and deck state the rule as absolute, and a federal HR reader will catch it at once. It also matters for the COR-1 seasonal technician pipeline, where the exception applies.
- *Fix:*
  - Use this wording everywhere: "Since 30 September 2025, under OPM's Merit Hiring Plan, self-assessment questionnaires may be used only to screen for minimum qualifications, not to rate and rank, except for seasonal positions, positions at GS-4 and below, and other OPM-authorized cases [100]."
  - On slide 2, delete "FY2028 is the governmentwide target" next to Natural Resources Management. Register FED-03 forbids implying NRM completion by FY2028.

**8. must-fix: The call to action leads nowhere.**
- *Location:*
  - deck slide 18 notes ("Contact route and signatory follow the project lead's pending decision on hosting (Q3)");
  - report §8.5 ("Challenge this report… through the EMST change-request route", with no URL);
  - package README "Feedback";
  - every brief ("`site/_site/challenge/`");
  - explorer `/challenge/` page (points to `docs/governance/CONTRIBUTING.md` with no repository URL).
- *Problem:* Every piece ends with an ask, and none tells the reader where to send anything. External readers cannot open repository paths. The NGO pilot offer does not say:
  - whether the pilot is funded (report §8.5 lists "Pilot funding" as a November 2026 to January 2027 task);
  - what participants receive;
  - how they are selected;
  - when the open call opens.
- *Fix:*
  - Hold external release until Q3 (hosting) is decided.
  - Then add a "How to take part" block to the report, deck and briefs, covering:
    - a named role mailbox and public URLs for the explorer and repository;
    - open-call dates and eligibility;
    - what participants give (named lead at 0.1 FTE) and what they get (facilitated sessions, profiles fitted to their roles, their data back, any stipend);
    - the MOU link;
    - a reply-by date.
  - If funding is not secured, say so: "Participation is unfunded unless the pilot funding sought by January 2027 is secured."

**9. must-fix: Truncated text makes the Forester PD unpresentable.**
- *Location:* `forester_pd_fes_draft.md`: the "Critical or needed-at-entry tasks" lines under duties 1–3 and 5–7, the Factor 6 task list, and both "Other information" lists. All are cut at about 90 characters with "…".
- *Problem:* A PD with sentences ending "…site conditions and…" cannot go to a classifier, a supervisor or a union. It reads as raw machine output and undermines the "PD language library" offer in the 0400 Kit. The cut lines also repeat the duty text word for word.
- *Fix:* Remove the truncation in `pipelines/views/forester_pd_fes.py` and delete the duplicate lines (they also breach issue 1). Keep the source-record provenance in a footer.

**10. must-fix: The explorer does not build, and its own output check fails.**
- *Location:* `site/` (the companion explorer, which the briefs README calls authoritative).
- *Problem:*
  - `npm run build` fails with `TypeError: (gs || []).map is not a function` at `site/lib/model.mjs:735` (`hrGates`).
  - The cause is that WP-08's federal-series JSON, regenerated at 16:53 today, now stores `credentialGates` as an object (`{shown: [], notShownUntilIssuerVerified: n}`), while the explorer expects an array.
  - With a one-line shim in a scratch copy, the build then fails `check-output.mjs` with 30 E4 errors ("RPT-05 wrong form 'more than a quarter'") on every federal variant page and on What's coming.
  - The checker treats the do_not_say for RPT-05 ("mixing with PPS's 'more than a quarter'") as a banned phrase. Yet the report, deck and briefs all use "more than a quarter".
- *Fix:*
  - Make `hrGates` read `.shown` and show the withheld count.
  - Change the RPT-05 check so it fires only when the 16% and the PPS figure appear together.
  - Rebuild, then rerun `check-output.mjs` before any preview link goes to the NGO cohort.

**11. must-fix: Named jurisdictions and organizations are presented as participants.**
- *Location:*
  - briefs R03, R04, R06, R07, R08 and R12 ("pilot jurisdictions (PA, TX, WA; one county environmental health department; one municipal utility)");
  - deck slide 16 ("State Class Views for pilot classes (PA, TX, WA…)"; "a federal-to-state crosswalk to be validated with Pennsylvania");
  - package README and report §8.5 ("to be validated with Pennsylvania");
  - deck slide 17 notes ("The Corps Network and the named agencies are candidates").
- *Problem:* Package rule 7 says no organization is described as committed without a register entry, and the commitment register is empty. "Pilot jurisdiction" and "validated with Pennsylvania" read as agreements. A Texas or Washington official seeing this would reasonably object. Naming a real organization as a "candidate" in notes that will travel puts it in an awkward position.
- *Fix:*
  - Use "Sample jurisdictions: EMST read their public class plans; no agency has been involved."
  - Use "a federal-to-state crosswalk EMST proposes to test with a state partner (Pennsylvania's published equivalency rule is the model)".
  - Remove the named candidates from every external copy.

**12. must-fix: The AmeriCorps settlement is overstated by omission.**
- *Location:* report §1.2, third "Entry pipelines" bullet ("An 11 September 2026 settlement covers FY2026 only"); R01 "What is changing" and "Entry paths" ("covers FY2026 only").
- *Problem:* The register's safe wording (WF-06) is "covers FY2026 *and the coalition only*". The 2026 settlement is with 23 state attorneys general and two governors (V1-05). Dropping the coalition limit tells a corps in a non-coalition state that it is protected for FY2026. That is the most decision-relevant fact for an NGO reader.
- *Fix:* "An 11 September 2026 settlement with 23 state attorneys general and two governors covers FY2026 in those jurisdictions only. Programmes elsewhere have no equivalent protection. The litigation is stayed until 1 February 2027 [34]. Corps leads should check whether their state is in the coalition."

### Should-fix

**13. should-fix: Monitoring requirements in plans are presented as growing demand.**
- *Location:* report §3.1 (heading "Where demand is growing: what plans require", and the closing paragraph "The durable demand is therefore…"); deck slide 7 headline ("Demand is moving toward monitoring…"); F05 headline ("a durable demand for monitoring design").
- *Problem:*
  - The data compare plans written under different rules; they are not a time series, as the report itself says.
  - The 2012 Planning Rule *requires* a monitoring programme, so the jump from 2.7% to 30.7% largely restates the rule.
  - A plan requirement is not a funded position: the same agency is closing 57 of 77 research facilities and has lost more than a quarter of its staff. Readers will see the gap.
- *Fix:*
  - Retitle §3.1 "What newer plans require".
  - Text: "Plans written under the 2012 rule, which requires a monitoring programme, devote far more of their components to monitoring (30.7% vs 2.7%, each plan weighted equally). That is a requirement, not a funded workload; whether agencies staff it is the open question [J]."
  - Deck headline: "Newer forest plans require far more monitoring, and official projections show technician and analyst occupations growing faster than average. Whether agencies fund that work is the open question."

**14. should-fix: Some deployment figures need clearer denominators.**
- *Location:* report executive summary point 2 and §2.4; deck slides 4 and 5; F02 headline.
- *Problem:*
  - "Most registered AI is classical machine learning": 232 of 504 is 46%. It is a majority only among the 329 use cases with a type; 175 are unclassified.
  - "Available to tens of thousands of federal environmental staff": the USDA and Interior licences are department-wide, not limited to environmental staff.
  - The "nine environmental bureaus" are never named.
- *Fix:* "Classical machine learning is the largest type (232 of the 329 use cases with a type; 175 are unclassified)." "Licensed at 10,000+ users at EPA, and department-wide at 50,000+ users for some tools at Interior and USDA." List the nine bureaus in the F02 and F03 notes.

**15. should-fix: The report and deck give different figures for the young-worker employment gap.**
- *Location:* report §2.6 ("15% at the July 2025 vintage"); deck slide 11 notes ("Do not… use the earlier 13% figure").
- *Problem:* The original August 2025 paper reported 13%, and the August 2026 update restates that vintage as 15% (V4-03). Readers who know the 13% figure will think one of the two documents is wrong.
- *Fix:* Use one sentence in both: "About 19% below trend as of June 2026 in the August 2026 update. The original 2025 paper reported 13%; the update revises that vintage to 15%."

**16. should-fix: The deck's scenarios and terms drift from the report's.**
- *Location:* deck slides 12–13; report §6.1 and §6.3; brief R05.
- *Problem:*
  - SC3: the report warns of "a hollow state that cannot judge vendor output", while the deck says "agencies become intelligent customers", which drops the risk and makes SC3 sound like a goal.
  - SC4: the report says "junior roles are cut… highest risk of irreversible loss", while the deck says "capacity survives in… refugia; outcomes diverge by state".
  - SC2 differs as well.
  - NR-6 is "informed-buyer" in the report and "intelligent-customer" in the deck and R05.
- *Fix:* Copy the report's scenario cell text into the deck word for word, and use "informed buyer" everywhere.

**17. should-fix: Federal HR material that is missing or cryptic.**
- *Location:* report §7.2 federal HR and §7.3; deck slides 2 and 15.
- *Problem:*
  - (a) SME-QA and USA Hire are never named, though they are the two routes where task-based job analysis plugs into Merit Hiring Plan assessments.
  - (b) OPM's 2 September 2026 CHCO memo "Final Regulations on Reduction in Force" (FED-10) is absent. The package says "not for RIF" everywhere but never tells HR that new RIF rules exist, which is exactly when someone will be tempted to use competency profiles in a RIF.
  - (c) The slide 2 notes admit the September–October 2026 OPM memos were read for "titles and dates only". That is not acceptable in a federal HR briefing.
  - (d) "EMST supplies no essay content and no help with political position designations" (§7.3) is cryptic.
  - (e) "Collective-bargaining obligations on PD changes are anticipated" ignores the 2025 changes to which units bargain at all.
  - (f) There is no effort estimate for the Job-Analysis Starter Pack.
- *Fix:*
  - Read the FED-10 memos before release.
  - Add a half-page federal HR box covering SME-QA and USA Hire, the RIF rule plus an explicit "do not use EMST profiles for competitive levels or retention", a bargaining line ("check with your labor-relations office; 2025 executive orders changed bargaining coverage"), and staff-hours for the Starter Pack.
  - Spell out the §7.3 sentence, if this is what ADR-0016 means: "EMST provides no content for the Merit Hiring Plan essay questions and does not support designating positions as policy-influencing."

**18. should-fix: The Forester PD does not have the structure a classifier needs.**
- *Location:* `forester_pd_fes_draft.md`.
- *Problem:*
  - (a) No duty reaches 25%. The largest item is the "Related duties (27%)" catch-all, so a classifier cannot find the grade-controlling duty.
  - (b) GS-9 and GS-11 are merged, with "At the upper end of the band" in each factor. FES needs one grade per PD, or a full-performance PD with a separate developmental statement.
  - (c) Duty 7 ("Identify regional plants and animals… before they enter the program database", 8%) reads as copied from a biological technician role.
  - (d) The related duties include "conduct environmental impact review" and "interagency consultation on protected species", which invites a series challenge.
  - (e) Standard header fields are missing: supervisory status, FLSA, position sensitivity, bargaining unit, competitive level, and conditions of employment (driver's licence, incident qualification or fire duty, arduous duty, remote duty station).
  - (f) "Positive education requirement: yes… (FH judgment pending verification)" is a well-known requirement. Verify it against the OPM 0460 qualification standard and state it plainly.
  - (g) "Good Neighbor Authority incl. EXPLORE Act amendments" needs a verified citation.
  - (h) The PD never explains why the Forester (R14, not a priority role) is the showcase.
- *Fix:* Generate a GS-11 full-performance PD with three to five duties, the largest at 25% or more, plus a separate GS-9 developmental statement. Add the header fields as blanks.

**19. should-fix: State DEQ readers get too little.**
- *Location:* report §7.2 state training officer; deck slide 16; briefs index.
- *Problem:*
  - Only R03 and R10–R13 are regulator-side, and air, water, wastewater, drinking-water, waste and environmental-health roles have no brief, though the explorer already holds draft profiles for them (R22, R24–R29).
  - There is nothing on the EPA-provided training states depend on (for example the NPDES Permit Writers' Course and the Air Pollution Training Institute), or on how EPA staffing losses affect oversight of and support to delegated states.
  - The Pennsylvania example rests on the unregistered 1,350-hire figure.
- *Fix:* Add a "state environmental agencies" box that points to the five relevant briefs and the explorer's draft air and water roles, gives a dated plan for those briefs, and tells readers to check the current status of EPA-provided training.

**20. should-fix: NGO readers miss their most useful facts.**
- *Location:* R01, R02 and R09 ("What you can do now"); report §7.2 NGO bullets; deck slides 17–18.
- *Problem:*
  - The Public Lands Corps noncompetitive hiring authority is not named; R01 says only "corps hiring authorities".
  - The brief actions are written for supervisors, training officers and HR specialists, with nothing for an NGO programme lead or grant writer.
  - "0.1 FTE for ten months" does not match a pilot running from March 2027 to February 2028.
  - What participants get is never stated.
- *Fix:*
  - Add an "NGO programme lead" action line to R01, R02 and R09. For example: "Cite EMST task IDs in your next grant report and in each member's exit portfolio, so a state or federal hiring office can read what they did."
  - Name the Public Lands Corps authority, with verified terms and how it interacts with EO 14356.
  - Reconcile the duration.

**21. should-fix: Educators get no structure and no actions.**
- *Location:* report §7.2 "An educator"; briefs (no educator actions).
- *Problem:* The report gives no v2 structure or counts (the explorer shows 31 role profiles, 158 core competencies and 74 module records) and no proficiency-level definitions (they appear only in the briefs README). There is no accreditation or CIP plan, no draft list of entry-level targets for graduates, and no mention of the 0460 positive education requirement as a curriculum constraint.
- *Fix:* Write a one-page educator guide covering:
  - v2 structure and counts;
  - levels L1–L5 in plain words;
  - the draft L1–L2 targets for each priority role;
  - how to map one course;
  - the "no pixel without plot" and by-hand provisions as field-practicum design;
  - a dated SAF/ABET/CIP roadmap.
  
  Add an "Educator" line to each brief.

**22. should-fix: The package never explains why the explorer has 31 roles rather than 13.**
- *Location:* package README (explorer row: "for the 13 priority roles"); deck slide 8; report §3.2.
- *Problem:* The explorer home page says "Role profiles with role-change pages: 31; 121 sector-actor variants; 6 more emerging roles". Readers arriving from the deck will meet R14–R37 with no explanation.
- *Fix:* Add one line: "The 13 corridor roles are profiled in full. The explorer also holds earlier drafts of 18 more roles (R14–R37) at lower depth."

**23. should-fix: The nonpartisan posture is overstated in places and undermined in others.**
- *Location:* package README ("it takes no position on any policy"); report §1.2–1.3 and §6.3.
- *Problem:*
  - (a) The package *does* recommend workforce policy: "protect a minimum entry cohort", "fund partner capacity alongside any devolution", equivalency rules.
  - (b) It describes the effects of 2025–26 actions but never the government's stated rationale for them (for example, the Forest Service's state-based model).
  - (c) It avoids the legal names of the instruments it discusses: New York's *Environmental Justice Siting Law* becomes "New York's siting law", and EO 12898 is described only as directing "analysis of cumulative burdens and distributional effects". Naming competencies by the work is sound; renaming laws is not. State readers cannot search for them, and both sides can read it as spin.
  - (d) "Rules… changed more in 2025–26 than in any comparable period since NEPA's original regulations [J]" is sweeping and unsupported.
- *Fix:*
  - README: "takes no position on the merits of any law, rule, executive action or budget; it recommends workforce-management practices that hold under every scenario it considered."
  - Give the stated rationale in one neutral clause per major action, cited to the primary announcement.
  - Use each instrument's legal name.
  - Cut the "more than any period" line, or support it with a count.

**24. should-fix: Load-bearing federal facts rest on weak or one-sided sources.**
- *Location:* report references [3], [4], [26], [34], [35], [42], [92]; briefs R01, R02 and R12.
- *Problem:*
  - USFS seasonal hiring rests on a letter from two House members (V1-04: "No USDA/USFS primary press release located"), and trail miles on another member's letter.
  - The EPA headcount comes from an article headlined "…After Trump Targets Its Public Health Experts".
  - The AmeriCorps status comes from a litigant's press release.
  - The SPEED Act status comes from a "Lobby News mirror" rather than Congress.gov, Part 108's status from a drone blog rather than reginfo.gov, and the regulatory status mostly from law-firm alerts.
  - Meanwhile OPM's Federal Workforce Data site has published monthly data since January 2026, and EMST has not pulled it (§8.2).
  - The Forest Service loss appears as both "more than a quarter" and "16%", explained only as a "different base".
- *Fix:*
  - Pull OPM data for the 0400 series, 0028, 0819, 0456 and 0462, and cite it as the primary source for the headline numbers.
  - Use Congress.gov, reginfo.gov, the Federal Register and court dockets.
  - Explain the 16% versus 25% gap (period, base, fire versus non-fire), or drop the 16%.

**25. should-fix: The "two-page" briefs are too long, and the evidence labels repeat until they say nothing.**
- *Location:* all briefs.
- *Problem:*
  - The briefs run 1,314–1,769 words, with four or five tables and a list of repository paths. That is three to four printed pages.
  - Every brief repeats the same 90-word "Read this first" box, and nearly every row of every change table says "Assessment pending", so the evidence column carries no information. The labels themselves are clear (the README table is good); the repetition makes them read as disclaimers.
  - Watch entries leave out the numbers the report has. R02 says only "registered AI species-detection use cases" where it could say "89 registered, 11 deployed".
- *Fix:*
  - Replace the box with a one-sentence banner: "A first draft for your staff to correct: written by AI agents and not yet checked by practitioners. Nothing here is a measurement."
  - Make "assessment pending" a note in the column header, and use the column for the external signal with its number and reliability, or "none yet".
  - Replace the source lists with one URL.

**26. should-fix: The report is hard to skim, and the executive summary contains no ask.**
- *Location:* report front matter.
- *Problem:* The report runs about 11,000 words plus 110 references, and the roughly 850-word executive summary is packed with numbers. There is no "start here" for each audience, and the executive summary never says what EMST is asking readers to do.
- *Fix:*
  - After the executive summary, add a half-page box: "If you are a federal HR specialist / state training officer / NGO programme lead / educator, do these three things this quarter".
  - Add one sentence with the ask to "What EMST v2 offers".

**27. should-fix: The deck slides into doom and overstates a desk exercise.**
- *Location:* deck slides 11, 13 and 2; report executive summary point 5.
- *Problem:*
  - Slide 11's headline says "tomorrow's seniors will not be able to tell when AI is wrong", where the report says "could".
  - Slide 13 says "Eight moves pay off in all four scenarios", where the report says they "hold up".
  - Point 5 says "EMST tested workforce strategies", but this was a desk exercise by an agent.
  - Slide 2's notes say "its target of 300+ series… appears unmet", a characterization based only on a memo index (FED-08 is verified-partial).
- *Fix:*
  - Slide 11: "…they may not be able to tell when AI is wrong."
  - Slide 13: "In EMST's desk analysis, eight moves hold up in all four scenarios. No practitioner workshop has reviewed them yet."
  - Slide 2: "OPM had published one competency-based standard (2210) as of 23 October 2026."

**28. should-fix: Individual briefs overreach or leak internal process.**
- *Location and fixes:*
  - **R10** says "machine-assisted coding is deployed" without evidence, while the report says none of the five NEPA and permitting use cases is deployed. Rewrite: "Machine-assisted comment tools are registered at some agencies [V4-15]; their deployment for environmental reviews is not established."
  - **R12** says "federal environmental staffing fell sharply… *so* more inspection work rests on state and local programmes", an unsupported causal claim (delegated states already do most inspections). Rewrite: "Most inspections are already done by delegated state and local programmes. With EPA staffing down 24%, federal oversight, training and backstop capacity for them is thinner [V1-03; J]."
  - **R05** cites BLS +7% for environmental science and protection technicians as context for a forming validation role. It is irrelevant; delete it.
  - **R07**'s "remote sensing mentions rise in plans" sits awkwardly next to report §3.1 ("rarely named"). Reconcile: "rise from a very low base and remain rare".
  - **R09**: delete "The linked fund-rescission signal… has not passed a verification pass… (awaiting WP-15)". It advertises an unverified claim.
  - **R11 and R12**: "Pay often moves in the other direction from the one people expect" is vague. Use the report's BLS medians.
  - **R13**: "Knowledge retention is a stated purpose of this package, so record what was captured, not who left" is unclear. Rewrite: "Record the knowledge captured, not personal details about who left."
  - **Deck slide 9**: the fire intelligence row's "being compressed: continuous spread modelling" contradicts R08. Change it to "Hand-worked spread predictions (models now run continuously)".

**29. should-fix: Some moving facts expire within days.**
- *Location:* report §1.3 (OFCCP 26 October 2026; the Colorado hearing on 26 October; the USFS objection rule on 12 November); deck slide 6.
- *Problem:* These items are written in the future tense and will be wrong within days of release.
- *Fix:* Write each as "As of 23 October 2026, … was scheduled to…". Put a visible "re-checked on [date]" line on slide 6 and in §1.3, and block release until the re-check is done.

**30. should-fix: British spelling and in-house jargon will grate on US readers.**
- *Location:* the whole package.
- *Problem:*
  - "programme", "labour", "behaviour", "analysed", "licence", "favour" and "centres" sit next to US proper names ("0340 Program Management", the file `R13-resource-program-manager`). To US federal and state readers this signals that the text was not written by peers.
  - Jargon such as "sector actor", "wind-tunnelling", "refugia" and "data and AI floor" adds friction.
- *Fix:*
  - Use US spelling throughout.
  - Say "employer type" for "sector actor".
  - Gloss "formation" every time as "on-the-job development of judgment".

**31. should-fix: Explorer evidence links are indiscriminate.**
- *Location:* explorer federal variant pages, for example `roles/r28-air-quality-specialist/federal/`.
- *Problem:* Every federal variant gets every federal headcount signal. The air-quality specialist page shows the NPS headcount, OPM's own HR-staff headcount (−35%) and the unverified IRA rescission headline. Rows from the weak-signals CSV are labelled reliability A ("Primary official… directly observed"). HR readers will see noise; a journalist will call it padding.
- *Fix:* Link signals only to roles in the affected agency or occupation, and grade reliability from the underlying source, not the CSV.

**32. should-fix: The briefs and the explorer describe the Tribal hold differently.**
- *Location:* briefs README ("Held items are counted, not described"); explorer footer ("not shown and not counted").
- *Fix:* Choose one rule and use it in both places.

### Nice-to-have

**33. nice-to-have: The timeline table is out of order.** Report §8.5 puts the "Jan – Dec 2027" row before "Feb – Mar 2027". Sort it by start date.

**34. nice-to-have: The SPEED Act status is worded two ways.** The report says "pending in the Senate EPW Committee"; R10 and deck slide 6 say "has had no Senate action". Use one wording.

**35. nice-to-have: One robotics statistic rests only on Anthropic.** The robotics figures (74% technically feasible, 0.3% cost-competitive) come solely from Anthropic research. The disclosure is good; add a second source or label the figure "Anthropic estimate".

**36. nice-to-have: Some references use mirrors.** Cite CRS reports from congress.gov rather than everycrsreport.com.

**37. nice-to-have: Slide 1 is a claim, not a title.** Use "How environmental jobs are changing, and what workforce leaders can do in 2027" and move the claim to slide 2.

**38. nice-to-have: One explorer label is stale.** The explorer's Federal Series Profile says the rule is "proposed (CR-FH-001; not yet in vocab/rules/)", but `vocab/rules/federal-series-profile@0.1.0.yaml` exists.

**39. nice-to-have: The pathway gate is jargon.** Report §7.3 and deck slide 17 use "AUC ≥ 0.70" and "α < .667". Say instead: "until it predicts real career moves clearly better than simple guesses" and "values that raters do not agree on are never shown".

---

## The five strongest things to keep

1. **The evidence taxonomy for AI.** Report §2.1 ("five kinds of evidence, five different questions") and §2.7 ("known, partly known, unknown") are the clearest short explanation of AI-exposure evidence I have seen for this sector. Together with "availability is not use" and the "77% is not job automation" warning, they inoculate readers against both hype and doom. Keep them nearly verbatim, and put §2.7 on a deck slide.
2. **The entry-path hypothesis as written in §5.** It is stated as a hypothesis, broken into links L1–L5 each with its own evidence status, paired with counter-mechanisms, and followed by "what would settle it" with concrete data sources. This is the model for how the whole package should treat agent drafts.
3. **The formation provisions and the supervisor and training-officer actions in the briefs.** Examples: 50 unaided identifications before AI aids are credited; two effects sections and two permits drafted unaided; 200 comments coded by hand; 10 hand calculations of fuel moisture; a month of automated flags reviewed by hand; 20–30% field time in remote-sensing reskilling; seeded-error drills. Practitioners will recognize these as how people actually learn. They are cheap to adopt this season and easy to test. This is the package's most usable content.
4. **Policy-status discipline.** The package keeps proposed separate from final, keeps the SPEED Act separate from S. 5653, notes that UGESP was removed from OPM's regulations but remains codified, keeps 5 CFR 300.103 as the anchor, describes series as "proposed for realignment", and dates every moving fact with a re-check. Keep the do_not_say approach. Just extend it to the omissions in issues 7 and 12.
5. **No-regret and contingent moves with named triggers.** §6.3–6.4 and slide 13 give a "start this quarter" column, plus a "risk if done too early" column for each contingent move. The wind-tunnel verdict that substitution-first is the most fragile strategy is actionable, falsifiable and neutral in form. The privacy-by-design gap check and the explicit "not for selection, RIF or rating" guardrails belong alongside these as reasons an agency could say yes.

---

*Claims checked against the register or key facts during this review: FED-02/V1-09 (questionnaire exceptions), FED-03/V1-17, FED-08, FED-10, WF-05, WF-06/V1-05, V1-04, IDX-02/V4-03, OMB-02, AEI-02, PLAN-01, SEL-01, SKL-03, CMP-01, CMP-03, FIRE-01, FIRE-02, EJ-01 and RPT-05. The display rule was checked in `validation/display_gates.yaml` v1.1.0. The explorer was built from a scratch copy with a one-line shim in `site/lib/model.mjs` (`hrGates`); no package or site source file was modified, and the only change to the repository is the build's deletion of the untracked `site/_site/`.*
