# Independent evidence review: *How environmental jobs are changing* (EMST v2 flagship, draft 0.9)

- **Reviewer:** independent red-team evidence reviewer (research methods, labour economics, public administration). I did not build any of the reviewed work.
- **Date:** 2026-10-23
- **Scope read:** `docs/package/report/flagship_report.md`; `claims_used.csv` (264 rows); `docs/methods/claims_register.csv` (96 rows, including `do_not_say`); `docs/methods/WP15_SIGNOFF.md`; `figures/*.csv`, `figures_index.csv` and `build_figures.py`; and, for derived claims, the underlying LM extracts (`docs/research/labor-market-ai-impact/omb_*`, `env_occupation_exposure_scores.csv`, `lmp_outputs/*`, `data/v2/signals/2026/*.jsonl`).
- **Method:** I checked 99 claims against their primary or cited sources by web fetch or search on 2026-10-23, and EMST-derived claims against the repository data they come from. I re-ran the figure build in a scratch copy of the repository. I did not edit the report.
- **Note for the rc.1 re-check:** federalregister.gov and public-inspection.federalregister.gov were reachable from this review session. The WP-15 sign-off said they were not, so the rc.1 re-check can read the Federal Register directly.

---

## 1. Summary verdict

**The numbers are mostly sound. The framing is ahead of the evidence in several high-visibility places.** 76 of the 99 claims I checked are accurate as written. Most federal workforce numbers, legal and policy status statements, BLS figures and AI-index figures match their sources exactly. The figure build is reproducible: re-running it gives byte-identical outputs.

The main problems are of a different kind:

1. **Two legal and policy statements are out of date.** The New Jersey environmental-justice (EJ) rules are now before the NJ Supreme Court. AmeriCorps reinstatements reached non-plaintiff states in July 2025.
2. **One wording rule is breached.** The Pennsylvania equivalency is stated as a general rule, which register row STATE-PA-02 forbids.
3. **The executive summary overstates agent judgments.** "Roles are being re-bundled", "AI and sensors are starting to compress" and "EMST tested … eight moves hold up" are all stronger than the evidence-status tables in sections 2.7 and 5.
4. **Several derived statistics are worded more strongly than EMST's own data support.** These are the occupation exposure ranks, the OMB bureau and type counts, "drafting assistants at USDA", and plan "monitoring requirements".
5. **The status box overstates verification.** It says the draft "uses only facts that passed EMST's verification pass and the WP-15 claims check". The report's own claim list contradicts this.
6. **Federal and western Forest Service data are generalized to "public" or sector-wide statements**, mainly in the executive summary.

None of these is fatal. Every one can be fixed with wording changes, plus one sensitivity analysis on the plan-monitoring figure.

**Recommendation:** fix the must-fix list in section 7 before the NGO-pilot preview, and keep the WP-15 condition that blocks external publication.

**Verdict counts (99 claims checked):**

| Verdict | Count |
|---|---|
| Accurate | 76 |
| Imprecise | 14 |
| Out of date | 3 |
| Wrong | 2 |
| Unsupported | 4 |

---

## 2. Table of checked claims

Locations use the report's section numbers ("Exec" means the executive summary). "Source checked" is what I actually read on 2026-10-23.

| # | Claim (as written, condensed) | Location | Source checked | Verdict | Fix |
|---|---|---|---|---|---|
| R01 | Federal civilian workforce fell from 2,313,216 (Sep 2024) to 2,035,344 (Jan 2026), −12%, about 278,000 | Exec 1; §1.2; F01 | PPS Fed Figures [2] | Accurate | None. Optionally note PPS's exclusions (USPS, Foreign Service, much of the intelligence community) and that PPS itself says "over 250,000" |
| R02 | USFS and NPS each lost more than a quarter; park rangers −34.1% | Exec 1; §1.2; F01 | PPS [2] | Accurate | None |
| R03 | Under-30 share fell from 8.9% to 7.9% | Exec 1; §1.2; F08 | PPS [2] | Accurate | None |
| R04 | EPA 12,849 at end of Jan 2026; more than 4,000 (24%) fewer than a year earlier | Exec 1; §1.2; F01 | Inside Climate News [3] | Accurate | None |
| R05 | About 2,000 EPA year-end leavers had a median 30.3 years of service, against 10.8 for stayers. Presented as "senior reviewers are leaving" | Exec 4; §1.2; §5 L3 | ICN [3] | Imprecise (framing) | The number is right. The source describes long-tenured staff leaving, mostly through Deferred Resignation Program retirements; it does not identify reviewers. Write "long-tenured staff" and cite the DRP driver |
| R06 | USFS hired no non-fire seasonals in 2025; committed on 12 Feb 2026 to 2,000 seasonals | Exec 1; §1.2; F08; L1 | Neguse/Huffman letter [4] | Accurate | The letter is dated 18 Mar 2026 and attributes the 2025 gap to "budget constraints". Cite that as positive evidence of the driver |
| R07 | OPM Director's tally of about 317,000 departures in 2025; not to be combined with PPS | §1.2 | Transport Topics/Bloomberg [25] | Accurate | None (it counts departures, not a net change, as the report implies) |
| R08 | USDA OIG: USFS lost 16% in 2025; 10,496 wildland firefighters on 11 May 2026 against an 11,300 goal | §1.2; §1.4 | NewsNation [26] | Accurate | None |
| R09 | NRCS down about 23.8%, Sep 2024 to Nov 2025 | §1.2; F01 | Agri-Pulse [27] | Accurate | None |
| R10 | EO 14356: Strategic Hiring Committee approves every vacancy; annual staffing plans with quarterly updates | §1.2 | govinfo DCPD [28] | Accurate | None |
| R11 | USWFS set up 12 Jan 2026 from four bureaus plus OWF and OAS; 5,780 personnel a year; USFS fire not moved | §1.2 | DOI USWFS page [29] | Accurate | None |
| R12 | USFS HQ to Salt Lake City; all nine regional offices to close; 15 state directors; 57 of 77 research facilities to close; relocations into 2027 | §1.2 | Government Executive [30] | Accurate | None |
| R13 | FY2026 Interior–Environment appropriations $42.56bn (−1.9%) against a $26.85bn request | §1.2 | CRS R48726 [32] | Accurate | The number is right; see reasoning issue 4.6 on "staffing fell steeply anyway" |
| R14 | Conservation Job Board: −29.4% postings, −43.8% paid internships, −42% AmeriCorps (Mar–Sep 2025, one board) | §1.2; F08; L1 | National Parks Traveler [33] | Accurate | None |
| R15 | AmeriCorps terminations enjoined in 24 states plus DC (5 Jun 2025); "the terminations persisted elsewhere". L1 says "reinstated only in plaintiff states" | §1.2; §5 L1 | Maryland Matters, MN AG [34]; Boston Globe 2025-07-17 | **Out of date** | In July 2025 AmeriCorps told grantees whose grants were terminated on 25 Apr 2025, including in non-plaintiff states, that they were eligible for reinstatement. Uptake is undocumented. Rewrite both places and add the event to F09 |
| R16 | 11 Sep 2026 settlement covers FY2026; litigation stayed to 1 Feb 2027 | §1.2 | MN AG [34] | Accurate | None |
| R17 | USFS trail miles maintained −22% in 2025; skills lost listed | §1.2; F08 | Schrier et al. letter [35] | Accurate | "Traditional masonry" paraphrases "traditional construction techniques like rock wall masonry"; acceptable |
| R18 | New York opened a portal for laid-off federal workers in Feb 2025 | §1.2 | WHEC [36] | Accurate | Minor: the portal is general state recruiting; the federal-worker targeting is the "You're Hired" initiative |
| R19 | "Pennsylvania counts federal experience as equivalent in its minimum qualifications"; 1,350 hires by Aug 2026 | §1.2; §7.2 | PA Office of Administration [37] | **Imprecise; breaches do_not_say** | The release says OA identified federal titles whose experience "might be used as equivalent experience for certain Commonwealth job titles". STATE-PA-02 forbids presenting this as a statewide rule. Write: "Pennsylvania's Office of Administration has identified federal job titles whose experience may count as equivalent for certain Commonwealth titles, and reports 1,350 hires with federal work experience since EO 2025-01 (March 2025)" |
| R20 | CEQ NEPA regulations removed by IFR effective 11 Apr 2025; adopted as final effective 8 Jan 2026 | §1.3 | govinfo 91 FR 618 [11] | Accurate | None |
| R21 | DOI final rule of 24 Feb 2026 keeps a slim 43 CFR 46; most procedures moved to the Handbook | §1.3 | FR 2026-03708 [11] | Accurate | None |
| R22 | USDA 7 CFR 1b effective 3 Apr 2026; 36 CFR 220 rescinded | §1.3 | FR public inspection 2026-06537 [11] | Accurate | None |
| R23 | *Seven County*: 8–0 judgment; five-justice majority; substantial deference on NEPA scope | §1.3 | Cornell LII [12] | Accurate | None |
| R24 | NEPA §112 fee of 125% (per counsel); EA in 180 days, EIS in one year; no public count of users | §1.3 | CEQ page; O'Melveny [41] | Accurate | None (CEQ gives no percentage; counsel does, as the report says) |
| R25 | SPEED Act passed the House 221–196 on 18 Dec 2025; pending in Senate EPW; not law | §1.3; §6.5 | The Lobby News mirror [42] | Accurate | Cite Congress.gov directly at rc.1 (see section 6) |
| R26 | S. 5653 unveiled 30 Sep 2026; no markup or floor vote; a different bill | §1.3; §6.5 | Akin Gump [43] | Accurate | Moving fact. Akin Gump reports floor consideration expected in early November, so re-check before any release |
| R27 | USFS objection rule final 13 Oct 2026; effective 12 Nov 2026 | §1.3 | FR public inspection 2026-20890 [44] | Accurate | None |
| R28 | ESA "harm" rescission final 14 Jul 2026, effective 14 Sep 2026; suits filed mid-July | §1.3 | FR 91 FR 43300 [45]; search (W.D. Wash. complaints) | Accurate | None |
| R29 | Endangerment-finding rescission effective 20 Apr 2026; petitions pending in the D.C. Circuit | §1.3 | FR 91 FR 7686; Jones Day [46] | Accurate | Optionally add that merits briefing was being deferred pending EPA action on a reconsideration petition (as of June 2026) |
| R30 | No final WOTUS rule; proposal 20 Nov 2025; supplemental 9 Sep 2026 | §1.3 | Harvard EELP [47] | Accurate | None |
| R31 | ACHP voted 24 Jul 2026 to advance a Section 106 rewrite; at OIRA; unpublished as of 9 Oct | §1.3 | Kelley Drye (2026-09-11) [48]; web search | Accurate | Moving fact; re-check after the November ACHP meeting |
| R32 | EOs 12898, 14096 and 14008 revoked in Jan 2025; CRS: EPA's statutory duties unchanged | §1.3 | CRS IF12922 [49] | Accurate | None |
| R33 | NJ EJ rules affirmed by the Appellate Division on 5 Jan 2026 | §1.3; F09 | Riker Danzig (2026-09-03); search results. The Lowenstein URL [50] was blocked in this session | **Out of date** | The NJ Supreme Court granted certification in July 2026; the rules remain in effect pending decision. Update the text, the F09 event and register EJ-02 |
| R34 | NY siting law applies disproportionate-burden review to applicable permits; SEQR amendments effective 12 Jun 2026 | §1.3 | NY DEC [51] | Accurate | None |
| R35 | OPM IFR (31 Jul 2026) removed UGESP references; 5 CFR 300.103 still requires job analysis; UGESP still codified | §1.3; §7.2 | eCFR part 300 (amended 91 FR 48236); OPM release [13] | Accurate | Cite 91 FR 48236 alongside the eCFR, which describes itself as unofficial |
| R36 | OFCCP rescission incl. 41 CFR 60-3 published 21 Aug 2026; effective 26 Oct 2026 | §1.3 | FR public inspection 2026-17114 [53] | Accurate | Moving fact (effective in three days). The rule rescinds 60-3 "solely to the extent" it was codified for EO 11246 |
| R37 | Colorado SB 24-205 never took effect; SB 26-189 signed 14 May 2026, effective 1 Jan 2027, notice and disclosure, covers employment | §1.3 | Eckert Seamans [54] | Accurate | None |
| R38 | Colorado AG interim draft rules 6 Oct 2026; comments and hearing 26 Oct | §1.3 | Akin Gump [55] | Accurate | Moving fact. The rules also implement HB 26-1263 (Chatbot Safety Act) |
| R39 | "The Congressional Research Service counts 540 Good Neighbor agreements in FY2025" | §1.3 | CRS R49480 [56] | Imprecise | The 540 are Forest Service GNAs only, from FS legislative-affairs data relayed by CRS; BLM does not report comparable counts. Write "CRS, citing Forest Service data, reports 540 Forest Service GNAs in FY2025, most of them with states". Leave any Tribal sub-count to TN |
| R40 | Reorganization leans on states; GNA a "critical tool" | §1.2 | Stateline/Source NM [31] | Accurate | Attributed to unnamed "foresters across the West"; acceptable as reported |
| R41 | 2026 season to 11 Oct: 63,884 fires and 9.0M acres; 133% and 145% of the 2016–2025 average | §1.4 | NIFC IMSR [57] | Accurate | None |
| R42 | USWFS–USFS aligned quals effective Jan 2027; NWCG PMS 310-1 updated 23 Jan 2026 | §1.4 | IQCS 2026 Transition Plan; NWCG [58] | Accurate | None (the WP-15 wording fix is applied) |
| R43 | FY2024 USFS drones flew 4,536 hours (+78%); aerial ignition treated 188,986 acres | §1.4 | FY24 FS UAS Report [59] | Accurate | The source also gives 4,525 hours in section 5; consider "about 4,500" |
| R44 | 99% of USFS trained pilots fly as a collateral duty | §1.4; §4.2 | Unmanned Systems Technology interview [60] | Accurate | The interview is undated (modified 2025-03-13). Give it as "c. 2024" |
| R45 | BLS projects firefighters +4% (2025–35); wildland not counted separately | §1.4 | BLS OOH | Accurate | None |
| R46 | SB 253: OAL approved 12 Oct 2026; Scope 1–2 due 10 Nov 2026; >$1bn revenue; Scope 3 from 2027; SB 261 enjoined | §1.5 | Morgan Lewis [14] | Accurate | None |
| R47 | EU Omnibus I in force 18 Mar 2026; CSRD >1,000 employees and >€450m; transposition by 19 Mar 2027 | §1.5 | Latham & Watkins [14] | Accurate | None |
| R48 | Trellis: 46% headcount or budget growth, 25% cuts, 58% higher compliance priority | §1.5 | Trellis [62] | Accurate | Source wording is "headcount and budgets" |
| R49 | LinkedIn: green hiring +7.7% against green skills +4.3%; 53% of green-skilled hires in non-green titles | §1.5 | LinkedIn Global Green Stocktake 2025 PDF [63] | Imprecise | The text gives "8% vs 4%" over the past two years. 53% (main text) conflicts with 51% (key findings) in the same report. Use the rounded values with the period, or cite the exact figure or page for 7.7/4.3, and note the 51/53 inconsistency |
| R50 | E2: clean energy net −36,949 US jobs in 2025 | §1.5 | Mercom India [64] | Accurate | Cite E2 *Clean Jobs America 2026* directly |
| R51 | Environmental scientist medians, May 2025: federal $116,110 … consulting $79,320 | §1.5 | BLS OOH [65] | Accurate | None |
| R52 | Microsoft: 200,000 Copilot conversations; information work most common and most successful | §1.1 | arXiv 2507.07935 v6 [7] | Accurate | Say "Bing Copilot (consumer)" conversations; this matters for the government-coverage caveat |
| R53 | Environmental scientists, climate policy analysts, sustainability specialists, planners, hydrologists and compliance officers "rank among the most exposed occupations in the economy"; hazmat workers, forest and conservation workers, firefighters, water operators and fish and game wardens "among the least" | Exec 2; §2.2; §2.7 | EMST `env_occupation_exposure_scores.csv`, built from Eloundou et al. [5] | **Imprecise (overstated)** | On EMST's own percentiles (human-rated β), environmental scientists are at the 98th, climate policy analysts 99th, sustainability specialists 97th, urban planners 90th, hydrologists 85th and compliance officers 81st. Fish and game wardens are at the 33rd and water operators the 28th, which is not "among the least". Foresters (59th), forest technicians (53rd) and range managers (65th) are mid-ranked. Give percentile bands ("top fifth" against "bottom third") and replace "splits … in two" with "a gradient from …" |
| R54 | Microsoft usage measure ranks most environmental occupations well below their capability exposure; the gap is widest for foresters and forest technicians | §2.3 | Same EMST file | Accurate | Reword as a relative-rank comparison ("rank lower on usage than on capability, relative to other occupations"), not "using AI less than exposure implies" (Exec 2) |
| R55 | Robots: about 74% of physical tasks (about 34% of hours) technically feasible; about 0.3% cost-competitive | §2.2 | Anthropic, *What work can robots do?* [68] | Accurate | Add that the ratings rely on Claude's own judgments. This is relevant to the report's Anthropic disclosure |
| R56 | Environmental tasks appear in AEI's first release with very small shares | §2.3 | HF README; EMST `aei_env_rows_seen.csv` [69] | **Out of date (evidence base)** | The statement is true of Feb 2025 data. Five later releases and the Mar 2026 observed-exposure data (which BLS uses) were not examined. Say so, or use the latest release |
| R57 | Claude.ai directive share 27% (first report), 39% (Aug 2025), 32% (Nov 2025) | §2.3 | AEI Sep 2025 and Jan 2026 reports [70] | Accurate | Add the Jan 2026 report URL; only the Sep 2025 URL is given |
| R58 | API: 77% of transcripts showed automation patterns "in September 2025"; not job automation | §2.3 | AEI Sep 2025 report [70] | Accurate | Minor: the report was published in Sep 2025 from Aug 2025 data. AEI calls "feedback loops" an automation mode, not "collaboration" |
| R59 | Census BTOS: 19.8% of businesses used AI (3 May 2026); 37% of firms with 250+ employees | §2.3 | Census story [71] | Accurate | Add the definition: "used AI in the past two weeks, in any business function" |
| R60 | OMB 2025 inventory: 3,611 use cases, 445 high-impact; DOI 247/129/0; USDA 162/86/4; EPA 29/14/2 | §2.4 | ombegov README (as of 2026-04-13) [8] | Accurate | None |
| R61 | "EMST counted 504 use cases in nine environmental bureaus" | §2.4; F02 source note | EMST extract `omb_ai_inventory_env_bureaus_2025.csv` | **Wrong (count)** | The 504 come from 11 units: USGS 187, NOAA 157, USDA NRE 76, EPA 29, USDA FPAC 20, FWS 11, BOR 8, BLM 7, BSEE 6, NPS 2 and BIA 1. Two of these are USDA mission areas, not bureaus. Write "eleven units (nine bureaus and two USDA mission areas)", and fix `wp10_signals.py`'s method string |
| R62 | "Most registered AI is classical machine learning" | Exec 2; F02 headline | Same extract | Imprecise | 232 of 504 is 46%, a plurality. It is 71% of the 329 records that report a type; NOAA's 157 records have no type. Write "most of the use cases that report a type (232 of 329)" |
| R63 | "Drafting and summarizing assistants are licensed at 10,000 or more users in EPA, the Department of the Interior and USDA" | Exec 2 | OMB consolidated COTS extract | Imprecise | EPA has several 10,000–50,000 drafting and summarizing rows. DOI's 50,000+ row is "improving written communications". USDA's only 10,000+ assistant row is "searching for agency information" (Copilot Chat, 50,000+). Use the §1.1/§2.4 wording ("drafting, writing, summarizing and search tools") |
| R64 | Four agentic use cases: three pilots and one pre-deployment | §2.4; F02 | Same extract | Accurate | None |
| R65 | CEQ data standard v1.2 (18 Aug 2025) | §2.4 | permitting.innovation.gov [72] | Accurate | None |
| R66 | PermitAI makes a search service available; a drafting benchmark with an AI developer has 102 test cases from 19 agencies | §2.4 | PNNL project page [72]; PNNL news release 2026-06-29 | **Unsupported by the cited source** | The figures are right but appear only in PNNL's 29 Jun 2026 release, not in [72]. The project page says the modules are "developing and testing". Cite the release |
| R67 | M-25-21/M-25-22 (Apr 2025); M-26-04 (11 Dec 2025) adds LLM contract terms | §2.4 | OMB M-26-04 PDF [73] | Accurate | None |
| R68 | OPM memo (27 Aug 2026): AI-drafted PDs generally not high-impact if the official independently reviews, revises and adopts; rating and ranking presumed high-impact | §2.4; §4.3; §7.2 | OPM CHCO memo [74] | Accurate | Add the memo's converse: adoption without substantive, documented review is to be treated as high-impact. It strengthens the report's point |
| R69 | NIST AI RMF 1.0 current; revision in progress, no date | §2.4 | NIST page [75] | Accurate | None |
| R70 | BLS 2025–35: +3.5% (170.3M to 176.2M); data scientists +34.6%; office and admin −4.0%, partly from AI-enabled automation | §2.5 | BLS release [61] | Accurate | None |
| R71 | Occupation projections: natural sciences managers +8.2 … water operators −6 | §2.5; F07 | BLS Table 1.2 and OOH | Accurate (9 of 11 re-read) | Environmental science and protection technicians (+7) and forest and conservation workers (−2) not re-read here. Label the "faster/about/slower" bands in the text as EMST's ±1-point convention, not BLS terms |
| R72 | BLS AI exposure categories: four levels; theoretical = FRS, Eloundou and Eisfeldt; observed = Anthropic and Microsoft; not forecasts | §2.5 | BLS page [76] | Accurate | None |
| R73 | Canaries: 22–25-year-olds in the most exposed occupations about 19% below trend (June 2026; 15% at the July 2025 vintage); via hiring; descriptive; ADP under-covers government | §2.6; §5 L4 | Stanford DEL [77] | Imprecise (omits material caveats) | Add the authors' own caveats: the gaps shrink when education is controlled, some differential trends predate generative AI, and the gaps are larger in ADP than in national benchmarks. All three bear on L4 |
| R74 | Anthropic Mar 2026: no systematic unemployment rise; job-finding into exposed occupations −14%, barely significant | §2.6; L4 | Anthropic labour-market impacts [78] | Accurate | None |
| R75 | "In Denmark, chatbot users saved on average 2.8% of work hours, with precisely estimated zero effects" | §2.6; §2.7; §5 | Humlum and Vestergaard, BFI WP 2025-56 [79] | Imprecise | Write "users reported saving". The 2.8% is self-reported (2024 survey). The confidence intervals rule out effects above 1% |
| R76 | The Budget Lab reports no clear labour-market effects yet | §2.6 | Budget Lab (tracker 2026-10-14) [80] | Accurate | None |
| R77 | "GDPval … includes no environmental occupations" | §2.6 | OpenAI GDPval [81] | Imprecise | GDPval includes compliance officers (13-1041), which this report treats as an environmental occupation (§2.2, F07). Write "no environmental science, natural-resource or field occupations" |
| R78 | WEF FoJ 2025: 39% of key skills to change by 2030; environmental stewardship in the top ten rising skills; 1,000+ employers | §2.6 | WEF Skills Outlook [82] | Accurate | The source says "core skills" |
| R79 | PwC: 62% AI-skill wage premium; 16% in government | §2.6 | PwC 2026 release [83] | Accurate | None |
| R80 | "Monitoring requirements average 30.7% of components in each 2012-rule plan, against 2.7% under the 1982 rule" (22.2% and 1.8% component-weighted); "durable demand" | §3.1; F05 | Rebuilt F05; LM `lmp_summary.json`; Chippewa NF plan ch. 4 citing 36 CFR 219.11(d) and 219.12(k) (1982 rule) | **Imprecise (arithmetic reproduces; interpretation not supported)** | The 1982 rule required plans to contain monitoring and evaluation requirements, yet only 28.6% of the corpus's 1982-rule plans have any monitoring component. The 1982 baseline is therefore likely an extraction or document-structure artefact (monitoring kept in separate guides; extraction method differs by era, as LM notes). One 2022 monitoring *evaluation report* (Idaho Panhandle) supplies 29% of all monitoring components. The means rest on 120 plans (84 and 36), not 154. Write "components typed as monitoring", run a sensitivity check that excludes monitoring-report files and plans with zero extracted monitoring, and drop "durable demand" from the F05 headline |
| R81 | Climate, data and models, and carbon rates higher in 2012-rule plans; CIs do not overlap | §3.1; F06 | F06 data | Accurate (arithmetic) | Same extraction caveat as R80 |
| R82 | "Since 30 September 2025, self-assessment questionnaires may be used only for minimum qualifications, not rating and ranking" | §7.2 | OPM CTCA implementation plan [100] | Imprecise | The plan lists exceptions for seasonal work, positions at GS-4 and below, and OPM-authorized uses. These exceptions cover much environmental entry hiring and should be stated |
| R83 | FY2025: 91.23% of DE announcements relied solely on self-report; FY2026 Q2: 34.3% used technical or off-the-shelf assessments | §7.2 | OPM Dec 2025 report; Jul 2026 plan [100] | Accurate | None |
| R84 | NRM is in Tier 2 "with no completion date" | §7.2 | OPM CTCA plan [100] | Imprecise | There is no tier-specific date, but the plan targets full implementation by the end of FY2028. Keep register FED-03's do_not_say while stating the overall target |
| R85 | OPM Apr 2026 series list (e.g., 0455 into 0404) is proposed; no final decision | §7.2 | OPM memo [102]; FEDweek 2026-04-27 | Accurate as far as verifiable | The memo said decisions would be finalized in May 2026; re-check before release |
| R86 | Workforce Pell: 150–599 clock hours over 8 to fewer than 15 weeks from 1 Jul 2026; governors with state boards identify occupations | §7.2 | ACTE [103] | Accurate | None |
| R87 | O*NET 31.0 (Aug 2026) current; 2028 SOC final planned for 2027 | §7.2 | O*NET What's New; BLS SOC page [105, 106] | Accurate | The SOC page still lists the 2nd FR notice as "TBD", so the 2027 date is at risk |
| R88 | DOL AI Literacy Framework: five content areas (names) | §4.5; §7.2 | DOL TEN 07-25 [94] | Accurate | None |
| R89 | OPM Federal Workforce Data site, monthly, since Jan 2026 | §5; §6.5 | OPM release [95] | Accurate | None |
| R90 | Burning Glass/HBS: only 37% of firms followed through; fewer than 1 in 700 hires | §7.1 | Higher Ed Dive [97] | Accurate | Cite the primary BGI/HBS report or the Harvard Project on Workforce post, as register SBH-01 requires |
| R91 | Colorado rewrote about 80% of classifications, yet non-degree hires stayed near 25% | §7.1 | Hechinger Report [98] | Accurate | The inference is weak: 2023 is the first data year, so there is no pre-reform baseline. See section 4.7 |
| R92 | ASDA bars federal funds for covered drones from 22 Dec 2025; the FCC Covered List bars only new authorizations | §4.2 | Holland & Knight [92] | Accurate | The H&K article covers only the FCC action. Cite the ASDA (FY2024 NDAA) or a source that covers it |
| R93 | Part 108 at OIRA since 10 Jul 2026; unpublished as of 21 Oct 2026 | §4.2; §6.4–6.5 | PickDrones (2026-09-08) [92]; DroneXL (updated 2026-10-21) | Accurate | The cited source is dated 8 Sep and cannot support "21 October". Cite reginfo.gov or a dated October source |
| R94 | "When Interior restricted drones, flights fell sharply (BLM 3,643 to 528, 2019–2023)"; butterfly monitoring moved on foot | §4.2 | GAO-24-106924 [91] | Imprecise (causal framing) | The numbers are right. GAO cautions that the changes "don't necessarily reflect the policies' precise effect". Add that caveat |
| R95 | February 2025 joint statement by four natural-resource societies | §8.5 | American Fisheries Society [108] | Accurate | None |
| R96 | Status box: the draft "uses only facts that passed EMST's verification pass and the WP-15 claims check"; About: "every external fact was checked … or, where marked, comes from a source an EMST lead read directly" | Header; About; Methods | `claims_used.csv` | **Wrong (internal contradiction)** | 13 references are only "read by role lead"; 24 external claims are not in the register; 38 rows are flagged "add to register / confirm". "Verified" means an AI agent's web check, and no human has fact-checked. Reword the status box to match the Methods paragraph and say who verified |
| R97 | "Rules … changed more in 2025–26 than in any comparable period since NEPA's original regulations" | §1.3 | None external (cites internal [39]) | Unsupported | Either count instruments by period from the L5 registry, or soften to "changed substantially" |
| R98 | "No court ruling on an AI-assisted environmental record had occurred as of October 2026" | §6.1; §6.5 | None | Unsupported (negative claim) | State the search (databases, terms, dates) or write "EMST found none in [search]" |
| R99 | "No source attributes them [the cuts] to AI" | Exec 1 | None (search-scope claim) | Unsupported as stated | Replace with the positive attributions found: DRP retirements (ICN [3]) and budget constraints (Neguse letter [4]) |

---

## 3. Verdict counts and patterns

- **Accurate (76):** almost every federal headcount, legal-status, BLS, AEI, OMB README and survey figure matches its source as worded. The WP-15 `do_not_say` list was applied well: no "13%", "77% of jobs", "realigned", "published" Part 108 or Section 106, "UGESP compliance", "coordination tripled", NEPATEC or PermitAI hours.
- **Imprecise (14):** mostly EMST-derived statistics worded more strongly than EMST's own data (R53, R61–R63, R80), secondary-source rounding (R49), and omitted caveats (R73, R75, R82, R94).
- **Out of date (3):** NJ EJ (R33), AmeriCorps reinstatement (R15), and the AEI evidence base (R56).
- **Wrong (2):** the "nine bureaus" count (R61) and the status-box verification claim (R96).
- **Unsupported (4):** R66 (the figures are right, but the cited source does not contain them) and R97–R99 (sweeping judgments or negative claims stated without a stated search or comparison).
- **Citation problems on otherwise accurate claims:** R92, R93, R90, R50, R25 and R57 (section 6).

---

## 4. Reasoning issues

### 4.1 "Capacity shock, not AI": sound as a judgment, overstated as a comparison

The evidence that federal environmental headcount fell for fiscal and policy reasons is strong (R01–R09, R99). But the claim that it is "the biggest force … not AI" compares a measured force with one that has not been measured: the report itself says no study measures AI's employment effects in environmental occupations.

The two are also not fully independent. The policy environment that produced the cuts is the one in which "substitution-first" pressure would arise, and the report's own scenarios treat AI-justified entry cuts as the main fragile strategy.

**Fix:** "The largest *measured* change in federal environmental jobs is a fiscal and policy capacity shock; AI's employment effect in these occupations has not been measured." Cite the positive driver evidence (DRP, budget constraints) instead of the negative "no source attributes".

### 4.2 The career-ladder hypothesis is framed as a hypothesis in §5, but not consistently in the executive summary

Section 5 is a model of good practice. It states the hypothesis, its links, the evidence status of each link, what would settle it and a publication rule. The executive summary item 4 also says "a hypothesis … not yet a finding".

But the same item then states as fact that "AI and sensors are starting to compress the tasks juniors learned on". That contradicts L2's status in §5 ("partly evidenced (capability and availability); use inside agencies and outcomes unknown"). It also calls departing EPA staff "senior reviewers", which the source does not support (R05). Section 4.5 states "the sector will have more data and fewer people who can tell whether it is right" as [J]; it should be [S].

**Fix:** use the L2 status language in the executive summary ("AI and sensors could compress …; actual use inside agencies is unmeasured") and relabel the §4.5 sentence as [S].

### 4.3 Agent-drafted judgments presented with finding-like verbs

The status box promises that no agent-drafted value is presented as a finding. The tables respect this: no ratings or craft blends are charted, and every role shows "no change indicator". The prose does not always respect it:

- **Exec 3:** "Roles are being re-bundled, not deleted" is a present-tense role-level change claim. It conflicts with §3.2 ("this report therefore states no role-level change as a finding") and with F10. "Not deleted" also sits awkwardly beside item 1: positions are being deleted, by reorganization and attrition. **Fix:** "Where AI touches these roles, the expected change is a shift in task mix rather than elimination (judgment); meanwhile budgets and reorganization are removing positions."
- **Exec 5 and §6:** "EMST **tested** workforce strategies … Eight moves **hold up** in all four … the strategy that **fails** most often". The scenarios and the wind-tunnel verdicts were produced by an AI agent (the Strategic Foresight Lead), with no human foresight panel. "Tested" implies an empirical procedure.

  There is also circularity. SC4 is *defined* as "junior roles are cut on the assumption that AI will carry the load; AI under-delivers". Substitution-first therefore "fails badly" in SC4 by construction, and SC2 is defined by AI being pulled back.

  **Fix:** "EMST's foresight lead (an AI agent; not yet reviewed by a human panel) assessed eight moves as robust across the four scenarios." Note that the scenario definitions partly determine the verdict on substitution-first.
- **§3.2 COR-1 to COR-3 and the §3.3 column header "Getting quicker":** these are labelled [J] but written in the indicative. **Fix:** "expected to get quicker (judgment)".
- **"Verified" and "role lead" are agent roles.** The verification passes and "read by role lead" checks were done by AI agents. The status box says the report was drafted by agents but does not say the fact-checking was. A reader will reasonably assume "verified" means human-checked (R96).

### 4.4 Generalizing from federal and western Forest Service data

The report is careful in the body: Tribal caveat, "one board", "the corpus is narrow", and §8.2. The executive summary is less careful:

- "The biggest force on **public** environmental jobs" rests on federal data only. State and local governments employ a large share of environmental scientists, technicians and operators, and EMST has no state or local headcount series (§8.2). Write "federal".
- "Policy and budgets are removing entry jobs now" (Exec 4). L1 itself says state, local, NGO and private entry hiring is unmeasured. Add "in federal land agencies and corps".
- **OpenLMP:** 95.3% of components are Forest Service plans, all in western states, and the 1982-versus-2012 comparison is 100% Forest Service. "The durable demand is therefore for indicator design, evaluation and reporting" (§3.1) and the F05 headline generalize to environmental work broadly. They should be scoped to "western national-forest plans". The measurement concern in R80 also applies.
- **Field-craft evidence (§4.2)** is entirely Forest Service and Interior (drones, pilots, GAO). "The field moves, it does not vanish" should be scoped to federal land agencies.
- **Compliance officers (13-1041)** is a broad SOC that is mostly non-environmental. Using it as an environmental occupation in the exposure ranks and in F07 inflates the "regulatory occupations are highly exposed" signal. Use O*NET 19-2041/13-1041 detail where possible, or caveat it.

### 4.5 Exposure "split in two"

EMST's own percentile file (R53) shows a gradient, not two clusters. Foresters, forest technicians, range managers, park naturalists and environmental technicians sit between the 50th and 78th percentiles.

The "usage below exposure" statement is a comparison of relative ranks across two indices built on the same O*NET base. It is not an absolute usage-versus-capability gap. The report also withholds the values, citing licence terms, so readers cannot check the executive-summary claim.

The BLS AI exposure categories are U.S. government public-domain data that combine both theoretical and observed exposure. They offer a licence-free way to publish the profile now (§2.5 says they have not been ingested).

### 4.6 Appropriations and staffing: a temporal mismatch

"Money and capacity have come apart … Staffing fell steeply anyway" sets FY2026 appropriations (enacted 23 Jan 2026) against staffing losses that mostly happened in FY2025 under a full-year continuing resolution, before the FY2026 bill. The conclusion (capacity, not dollars, is the operative uncertainty) may still hold. But the sentence implies the FY2026 money arrived and staffing fell despite it.

**Fix:** compare FY2025 enacted funding with FY2025 staffing, or say that appropriations stayed near prior levels while hiring controls (EO 14356 and earlier freezes) and deferred resignations drove the decline.

### 4.7 The mobility evidence is weaker than presented

- **Colorado (R91):** 2023 is the first year of data, after reforms began, so "stayed near 25%" cannot show that reclassification had no effect.
- **Burning Glass (R90):** this concerns private firms' degree requirements, not public classification.

Both are reasonable cautions, but neither directly tests "visibility drives mobility". **Fix:** present them as "evidence that announcing skills-based policy does not by itself change who is hired", with the baseline caveat.

### 4.8 Sweeping and negative claims without a stated method

"Changed more … than in any comparable period since NEPA's original regulations" (R97), "no court ruling on an AI-assisted environmental record" (R98), "no study yet measures AI's employment effects in environmental occupations", "EMST found no standing coalition" and "GDPval, the best-known benchmark". Each needs either a stated search (where, which terms, as of when) or softer wording. These are exactly the claims that hostile readers test first.

---

## 5. Figure issues

**Rebuild.** I copied `data/` and `docs/` into a scratch directory and ran `python3 -I build_figures.py` from the copied figures folder. It exited 0, and all 10 datasets and `figures_index.csv` are byte-identical to the committed files. I did not run it inside the repository, to avoid touching the report folder.

| Figure | Headline matches data? | Issues and fixes |
|---|---|---|
| F01 | Yes. The 12%, the more-than-a-quarter rows, −34.1%, −24% and −23.8% all match their sources | "The two largest land-management agencies" is true by staff, not by acreage (BLM manages the most land), so say "by staff". The "not an AI effect" clause is an attribution, not data: label it J in the index, or cite DRP and budget constraints. The −25.0 values are EMST encodings of a lower bound; the chart spec handles this, but a CSV reader may plot them as exact |
| F02 | Partly. "61 of the 347 … in production" matches. "**Most** AI … is classical machine learning" does not hold for all 504 (46%) | Write "most of the use cases that report a type (232 of 329)". The source note's "nine environmental bureaus" is wrong: there are 11 units (R61). The evidence label "E (external sources read and verified)" misdescribes an EMST extract and classification; use "EMST derivation from E source; unreviewed" |
| F03 | Yes | Keyword-classified and overlapping (noted). The NEPA regex `permit` is broad. NOAA's 157 records have no stage and fall in "not deployed or unreported"; say so in the headline note. Same evidence-label point as F02 |
| F04 | Yes, but only because "search" is included | `build_figures.py` asserts that all three departments appear (`assert {…} == {"USDA","DOI","EPA"}`). The keyword list includes "knowledge retrieval", without which USDA drops out. The headline is technically true, but the executive summary's "drafting and summarizing assistants" in USDA is not (R63) |
| F05 | The numbers match; the interpretation does not follow | "A durable demand for monitoring design, evaluation and reporting" is an inference, with no scope statement in the headline (western national forests) and a likely 1982-era extraction artefact (R80). n is 84 and 36 plans, not the 154 in §3.1. Add the sensitivity check, scope the headline, and change the evidence label to "EMST derivation" |
| F06 | Yes | The normal-approximation CI gives an impossible negative lower bound (at-risk species, −0.61); use a bootstrap or Poisson interval. The extraction caveat from R80 applies |
| F07 | Yes | The "faster / about / slower" labels are EMST's ±1-point bands (noted in the index but not in §2.5 text). Data scientists are a reference, not an environmental occupation; label them so. See the compliance-officer scope point in §4.4 |
| F08 | Yes | None beyond the AmeriCorps context (R15) |
| F09 | **No.** "Policy instruments reshaped review, authorization, hiring and disclosure work faster than any technology did" cannot be read from a timeline that contains no technology adoption data | Rewrite the headline as "At least N dated policy changes in 2025–26 altered review, authorization, hiring and disclosure rules, and more are scheduled for 2027." Add the NJ Supreme Court certification (July 2026) and the AmeriCorps July 2025 reinstatement notices. The Schedule Policy/Career "final 2026-02-06" event is not in register FED-06's text (which gives effective 2026-03-09); I did not check it |
| F10 | Mostly | "Cross all three crafts" depends on craft ratings that are agent drafts and are deliberately not charted. Write "designed to cross all three crafts" |

**Pipeline points:**

- **`check()` accepts records with status `superseded` as usable** (`if status not in ("verified", "corrected", "superseded", …)`). A superseded fact should fail the build.
- **The Methods claim is overstated.** It says the script "checks every hard-coded value against its verification record and fails if a record changes". The needle check confirms a string still appears; it does not detect other edits, and several values are not needle-checked (F02 cells other than the totals, F05/F06 CIs, the F01 lower-bound encodings). Write "checks key values against their verification records".
- **The F09 filter admits an event if *any* source is a WP-15 ID**, even when its other sources are unverified SC rows (for example, the objection rule with SC-009). Acceptable here, but document it.

---

## 6. Citation issues

| Ref | Issue | Fix |
|---|---|---|
| [72] | The DraftNEPABench figures (102 cases, 19 agencies, with OpenAI) are not on the cited PNNL project page or the CEQ page | Cite the PNNL news release of 29 Jun 2026 ("PermitAI public–private partnership speeds environmental review drafting tasks") |
| [92] | The PickDrones article is dated 8 Sep 2026 and cannot support "unpublished as of 21 October". The Holland & Knight article covers only the FCC, not the American Security Drone Act | Cite reginfo.gov or a dated October source for Part 108, and the ASDA statute (FY2024 NDAA) for the drone-funds bar |
| [42] | A non-official mirror (The Lobby News) is the sole source for a moving legislative fact | Cite Congress.gov at rc.1, as WP-15 requires |
| [97] | Secondary trade press, although register SBH-01 says to cite the primary BGI/HBS report | Replace with the BGI/HBS report (Feb 2024) or the Harvard Project on Workforce post |
| [64] | Secondary (Mercom India) | Cite E2 *Clean Jobs America 2026* |
| [70] | The 32% (Nov 2025) figure comes from the Jan 2026 report, whose URL is not given | Add https://www.anthropic.com/research/anthropic-economic-index-january-2026-report |
| [50] | The URL ends "…environmental-law-litigatio"; search results show the slug ending "…litigation". It could not be fetched (permission timeout), so it may be truncated or dead. The source is also out of date (R33) | Check the URL and add a source for the NJ Supreme Court certification |
| [63] | 7.7% and 4.3% are not in the report text (which says 8% vs 4%); 53% and 51% conflict within the source | Cite the page or figure, or use the rounded figures |
| [56] | Attributed to CRS without noting that CRS relays Forest Service data | "CRS, citing Forest Service legislative affairs data" |
| [13] | The eCFR describes itself as unofficial | Add 91 FR 48236 (FR Doc 2026-15586) as the primary citation |
| [60] | Undated interview | Give "c. 2024 (page modified 2025-03-13)" |
| [4] | The press release is dated 23 Mar; the letter is dated 18 Mar 2026 | Cite the letter date for the 12 Feb commitment |
| [37] | The URL slug is truncated as published | It resolves; no change needed |

**URLs that resolved in this session:** [2], [3], [4], [7], [8], [11] (all three), [12], [13], [14] (both), [25]–[37], [41], [43]–[47], [48] (Kelley Drye), [49], [51], [53]–[63], [65], [68]–[83], [91], [94]–[95], [98], [100], [102], [103] (ACTE), [105]–[106] and [108].

**Not fetched:** [5] (GitHub), [48] (ACHP news page), [52], [103] (BillTrack50) and [50] (blocked).

I have not supplied replacement URLs except those I actually read in this session (PNNL release, AEI Jan 2026 report, Riker Danzig, Boston Globe, DroneXL).

---

## 7. Prioritized must-fix list

### Before the NGO-pilot preview

1. **Status box and About (R96).** Reword to match the Methods paragraph. State that verification was done by AI agents on 2026-10-23, that 13 references were read but not re-verified, and that 38 claims still need register rows. Complete those 38 WP-15 rows; this review has checked most of them (see section 2).
2. **New Jersey EJ (R33).** Add that the NJ Supreme Court granted certification in July 2026 and the rules remain in effect pending decision. Update F09 and register EJ-02.
3. **AmeriCorps (R15).** Remove "the terminations persisted elsewhere" and L1's "reinstated only in plaintiff states". Add the July 2025 reinstatement-eligibility notices to non-plaintiff grantees.
4. **Pennsylvania (R19).** Replace the general-rule wording, which breaches register STATE-PA-02 `do_not_say`.
5. **Executive summary items 3 to 5 (§4.2–4.3).**
   - Item 3: change "roles are being re-bundled, not deleted" to an expected task-mix shift, and acknowledge that positions are being cut.
   - Item 4: use L2's evidence status, not "starting to compress", and replace "senior reviewers" with "long-tenured staff".
   - Item 5: replace "tested … hold up" with an agent-assessed robustness judgment, and note the circularity on substitution-first.
6. **Exposure ranks (R53, §4.5).** Replace "among the most / least exposed in the economy" with percentile bands. Drop "splits … in two". Consider publishing from the public-domain BLS categories.
7. **OMB counts (R61–R63).** Change "nine bureaus" to eleven units. Change "most registered AI is classical ML" to "most of those that report a type". In the executive summary, change "drafting and summarizing assistants … USDA" to "drafting, writing, summarizing and search tools".
8. **Plan monitoring (R80, F05).** Change "monitoring requirements" to "components typed as monitoring". Disclose the n (84 and 36 plans). Add a sensitivity check without monitoring-report files and without plans that have zero extracted monitoring. Scope the headline to western national forests. Drop "durable demand" until the 1982 extraction question is resolved.
9. **Scope words (§4.4).** "Public environmental jobs" becomes "federal". The entry-job and field-craft claims are scoped to federal land agencies.

### Before external release

10. **Merit hiring (R82, R84).** Add the questionnaire exceptions (seasonal work, GS-4 and below) and the plan's FY2028 overall target.
11. **Missing caveats.** R73 (Canaries: education, pre-trends, benchmarks), R75 (self-reported), R77 (GDPval includes compliance officers), R94 (GAO causal caveat), R55 (Claude-rated robot estimates) and R39 (Forest Service-only GNA count).
12. **Citations.** Fix [72], [92], [42], [97], [64], [70], [50] and [63] (section 6).
13. **Figures.** Rewrite the F09 headline. Fix the F02 "most" and the bureau count. Relabel F02, F03, F05 and F06 as EMST derivations. Make the build fail on `superseded`. Soften the Methods claim about the build checks.
14. **Unsupported sweeping and negative claims (R97–R99, §4.8).** Add a search statement or soften.
15. **Appropriations sentence (§4.6).** Fix the temporal comparison.
16. **Moving facts to re-read, all within the next four weeks:** OFCCP effective date (26 Oct), Colorado hearing (26 Oct), S. 5653 floor action (expected early November), Section 106 after the 10 Nov ACHP meeting, the USFS objection rule (12 Nov), Part 108, the OPM series decision, SB 253 after 10 Nov, and the SOC 2028 schedule. The Federal Register was reachable from this session, so read it directly.

### Carry-over note

Several of these corrections affect statements that probably also appear in the companion Skills Taxonomy research and literature project: NJ EJ status, AmeriCorps, Pennsylvania equivalency, and the exposure-rank wording. They should be propagated there for consistency.
