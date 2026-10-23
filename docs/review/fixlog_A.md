# Fix pass A: flagship report, figures, claims lists (2026-10-23)

Agent: Fix-A (AI agent, report editor). Lane: `docs/package/report/**` and `docs/methods/claims_register.csv`.
Inputs: `docs/review/FIX_PASS_BRIEF.md`, `docs/review/evidence_review.md` (EVD), `docs/review/package_review.md` (PKG),
`docs/methods/WP15_report_corrections.md` (WP15).

Status values: **fixed**; **softened** (claim reduced or removed because no corrected fact and source were available);
**deferred** (with reason); **n/a** (issue does not touch the report or figures).

| Issue | File | What changed | Status |
|---|---|---|---|
| PKG-2 / EVD-1 (R96) | flagship_report.md front matter | Status box replaced with the brief's status line (adapted), "verified/cleared" wording removed; About rewritten to say AI agents ran the checks and the claims list records the register row behind each claim | fixed |
| PKG-3 | flagship_report.md front matter, About | Brief's authorship statement added; "verified" defined as an AI-agent check; [J] relabeled "judgment by EMST's AI agents" | fixed |
| PKG-2 | flagship_report.md About, References | Reference labels replaced by five labels mapped to the register (register-verified with date and rows / in part / source read, not yet register-verified / EMST derivation / EMST record) | fixed |
| PKG-6 | flagship_report.md About | Short glossary of terms added | fixed |
| PKG-26 | flagship_report.md Exec summary | Ask added to "What EMST v2 offers"; "Start here" box by reader added (content drawn from sections 6.3, 7.2 and 4.5) | fixed |
| PKG-5 / EVD-15 (§4.1, §4.6, R99) | flagship_report.md Exec 1; §1.2 | "Capacity shock … fiscal and policy drivers … no source attributes them to AI" replaced by "largest measured change … contraction"; mechanisms named with citations (deferred resignations [3], hiring controls [28], grant terminations [34]); appropriations paragraph rewritten so FY2026 money is not set against earlier staffing losses; "budgets" no longer named as a cause | fixed |
| EVD-9 (§4.4) | flagship_report.md Exec 1, Exec 4, §1.1 | "public" changed to "federal"; entry-job claim scoped to federal land agencies and corps | fixed |
| EVD-6 (R53, §4.5) | flagship_report.md Exec 2 | "Splits in two / among the most and least exposed in the economy" replaced by percentile bands (top fifth, in or near bottom third, middle), no exact values (licence hold) | fixed |
| WP15-C006 / EVD R54 | flagship_report.md Exec 2 | B4 wording applied, plus "a comparison of ranks, not of absolute use" | fixed |
| EVD-7 (R61, R62) / PKG-14 | flagship_report.md Exec 2 | "Nine bureaus" → eleven units (nine bureaus and two USDA mission areas); "most registered AI is classical ML" → largest type, 232 of 329 that report a type | fixed |
| WP15-C008 / EVD-7 (R63) | flagship_report.md Exec 2 | A1 wording applied verbatim | fixed |
| EVD-14 (§4.8) | flagship_report.md Exec 2, Exec 3 | "No study yet measures…" attributed to EMST's labor-market review as a not-found result | softened |
| PKG-4 / EVD-5 (item 3) | flagship_report.md Exec 3 | Rewritten as PKG-4 text: policy faster than technology [J]; AI effect on roles a hypothesis; expected task-mix shift, not elimination; positions are being removed | fixed |
| EVD-5 (item 4) / EVD R05 | flagship_report.md Exec 4 | L2 evidence status used ("could compress … use inside agencies is unmeasured"); "senior reviewers" → "long-tenured staff … mostly through deferred-resignation retirements" | fixed |
| EVD-5 (item 5) / PKG-27 | flagship_report.md Exec 5 | "Tested … hold up … fails" → desk exercise by an AI agent, not reviewed by a human panel, "judged robust"; circularity of the substitution-first verdict stated | fixed |
| PKG-16 | flagship_report.md Exec 5 | "informed customers" → "informed buyers" | fixed |
| PKG-1 | flagship_report.md front matter | Status box states that no time shares, importance or entry flags, target levels or craft ratings are shown | fixed |
| EVD R01 | flagship_report.md §1.2 | PPS exclusions noted (optional fix) | fixed |
| EVD R07 | flagship_report.md §1.2 | OPM Director's tally described as departures, not a net change | fixed |
| PKG-24 (16% vs 25%) | flagship_report.md §1.2 | USDA OIG 16% moved to its own bullet with period/base caveat and "OIG document not read" | softened |
| EVD R06 / [4] | flagship_report.md §1.2 | Letter date 18 Mar 2026 and the agency-cited reason (budget constraints) for the 2025 seasonal decision given, attributed to the letter | fixed |
| EVD-3 (R15) / PKG-12 | flagship_report.md §1.2 | "Terminations persisted elsewhere" removed; July 2025 reinstatement-eligibility notices added with new source [111]; settlement scoped to the 23 AGs and two governors and FY2026; advice to check coalition membership | fixed |
| EVD-4 (R19) | flagship_report.md §1.2 | Pennsylvania wording replaced with the review's text (STATE-PA-01/02) | fixed |
| EVD R18 | flagship_report.md §1.2 | New York portal reworded as recruiting laid-off federal workers into state jobs | fixed |
| EVD-14 (R97) / PKG-23(d) | flagship_report.md §1.3 | "Changed more … than in any comparable period" → "changed substantially" [J] | softened |
| EVD-16 / PKG-29 | flagship_report.md §1.3, §1.5 | As-of and re-check-after dates added to S. 5653, USFS objection rule, Section 106, OFCCP, Colorado hearing, SB 253 | fixed |
| EVD-2 (R33) | flagship_report.md §1.3 | NJ Supreme Court certification (July 2026) and "rules remain in effect pending appeal" added with new source [113] | fixed |
| PKG-23(c) | flagship_report.md §1.3 | Legal names given for EO 12898, EO 14096, EO 14008, New Jersey's Environmental Justice Law and New York's Environmental Justice Siting Law | fixed |
| EVD R36 | flagship_report.md §1.3 | OFCCP rescission of 60-3 "to the extent codified for EO 11246" | fixed |
| EVD R38 | flagship_report.md §1.3 | Colorado draft rules also implement the chatbot safety act | fixed |
| EVD-11 (R39) | flagship_report.md §1.3 | GNA count attributed to CRS citing Forest Service data; Forest Service GNAs only; BLM has no comparable count | fixed |
| EVD-12 ([42]) | flagship_report.md §1.3, refs | CRS R49485 (2026-10-09) added as a government source for House passage [112]; Congress.gov itself still to read at rc.1 | softened |
| WP15-C078 | flagship_report.md §1.4 | A2 wording applied verbatim | fixed |
| WP15-C082 / EVD R48 | flagship_report.md §1.5 | B3 wording applied | fixed |
| EVD R49 / EVD-12 ([63]) | flagship_report.md §1.5 | LinkedIn figures given as rounded values with the period; 51%/53% inconsistency noted | fixed |
| EVD R50 / EVD-12 ([64]) | flagship_report.md §1.5 | E2 figure marked as trade-press report; E2 primary report not found this session | deferred: E2 report URL not located; cite at rc.1 |
| EVD R52 | flagship_report.md §1.1 | "Bing Copilot (consumer)" conversations; government-coverage caveat | fixed |
| EVD-6 (R53, §4.4, §4.5) | flagship_report.md §2.2 | Heading "Two exposure profiles" → "Exposure: a gradient, not one number"; percentile bands instead of "most/least exposed in the economy"; compliance-officer breadth caveat; public-domain BLS categories named as a license-free route [J] | fixed |
| EVD-11 (R55) / PKG-35 | flagship_report.md §2.2 | Robotics figures labeled Anthropic estimates relying partly on Anthropic's own model's ratings | fixed |
| EVD R56 | flagship_report.md §2.3 | AEI statement scoped to February 2025 data; later releases and March 2026 observed-exposure data stated as not examined | fixed |
| EVD R54 | flagship_report.md §2.3 | Microsoft comparison reworded as a relative-rank comparison | fixed |
| EVD R58 | flagship_report.md §2.3 | 77% figure: "directive and feedback-loop modes, both classed as automation"; September 2025 report on August 2025 data | fixed |
| EVD R59 | flagship_report.md §2.3 | Census BTOS definition added ("used AI in any business function in the previous two weeks") | fixed |
| EVD-7 (R61, R62) / PKG-14 | flagship_report.md §2.4 | Eleven units named with counts; type shares given over the 329 typed use cases; 175 untyped incl. all NOAA | fixed |
| PKG-14 | flagship_report.md §2.4 | Interior and USDA licences described as department-wide, with the tool type at each | fixed |
| EVD-12 ([72]) / EVD R66 | flagship_report.md §2.4 | PermitAI and DraftNEPABench figures now cite the PNNL release of 2026-06-29 [114]; "AI developer" named as OpenAI per the release | fixed |
| EVD R68 | flagship_report.md §2.4 | Converse of the OPM memo added (adoption without substantive, documented review is high-impact) | fixed |
| EVD R71 | flagship_report.md §2.5 | Faster/about/slower groups labeled as EMST's ±1-point convention, not BLS categories; data scientists labeled as reference only; compliance-officer breadth caveat | fixed |
| PKG-15 / EVD-11 (R73) | flagship_report.md §2.6 | One wording for the young-worker gap (19% June 2026; original 13%; vintage revised to 15%); authors' caveats added (education controls, pre-trends, ADP vs national benchmarks) | fixed |
| EVD-11 (R75) | flagship_report.md §2.6 | Humlum: "users reported saving" (2024 survey); CIs rule out effects above 1% | fixed |
| WP15-C120 | flagship_report.md §2.6, ref [80] | B1 wording and reference applied | fixed |
| WP15-C122 / EVD-11 (R77) | flagship_report.md §2.6 | A4 wording applied verbatim | fixed |
| EVD R78 | flagship_report.md §2.6 | "key skills" → "core skills" | fixed |
| WP15-L220 | flagship_report.md §2.7 | B5 wording applied verbatim | fixed |
| EVD-6 / PKG-5 | flagship_report.md §2.7 | Table rows reworded (top fifth; federal decline followed personnel, hiring and grant decisions) | fixed |
| EVD-14 (§4.8) | flagship_report.md §2.1, §2.6 | "None has / No outcome study has an environmental cut" → "EMST found none" | softened |
| EVD-8 (R80) / PKG-13 | flagship_report.md §3.1 | Heading → "What newer plans require"; "monitoring requirements" → "components typed as monitoring"; n disclosed (84 and 36 documents of 154); scoped to western national forests; sensitivity check run (17 of 36 2012-rule documents are monitoring evaluation reports, 5 stand-alone monitoring plans; plans only: about 10% vs 3%, intervals overlap); 1982 extraction caveat (24 of 84 older plans have any monitoring component); "requirement, not a funded workload"; "durable demand" dropped | fixed |
| EVD R81 | flagship_report.md §3.1 | Content-rate claim kept; bootstrap intervals still do not overlap, including among plan documents alone | fixed |
| PKG-22 | flagship_report.md §3.2 | One line explains the explorer's 18 further lower-depth roles and six emerging roles | fixed |
| PKG-6 | flagship_report.md §3.2 | COR-1/2/3 replaced by corridor names; "sector-actor variants" → "variants by employer type" | fixed |
| EVD-13 (F10) / §5 | flagship_report.md §3.2 | "Cross all three crafts" → "designed to cross all three crafts" | fixed |
| EVD §4.3 (COR-1 to COR-3) | flagship_report.md §3.2 | Corridor change statements rewritten with "EMST expects" / [J] | fixed |
| PKG-4 / EVD §4.3 | flagship_report.md §3.3 | Column headings → "Could get quicker where tools are used (capability evidence; not observed)" and "Expected to become more central (judgment)"; private-employer paragraph attributed to EMST's private-sector analysis [S] | fixed |
| EVD-9 (§4.4) | flagship_report.md §4.2 | Heading and opening sentence scope field-craft evidence to federal land agencies | fixed |
| WP15-C155 | flagship_report.md §4.2 | A3 wording applied verbatim | fixed |
| WP15-C156 / EVD-11 (R94) | flagship_report.md §4.2 | B2 wording applied verbatim, plus GAO's caveat that the changes do not necessarily reflect the policies' precise effect | fixed |
| EVD-12 ([92]) | flagship_report.md §4.2, refs | Drone-funds bar now cites the statute via FHWA guidance quoting FY2024 NDAA §1825 [116] ("buy or operate"; "maintain" dropped as not in that text); Part 108 status now cites reginfo.gov EO 12866 record RIN 2120-AL82, pending review as of 2026-10-23 [115] | fixed |
| EVD §4.2 | flagship_report.md §4.5 | "The sector will have more data…" relabeled [S] and conditional; "Foresight work" → "EMST's foresight analysis" | fixed |
| PKG-5 / EVD-5 | flagship_report.md §5 | Hypothesis box: "fiscal and policy shock" → personnel, hiring and grant decisions (federal land agencies and corps); "senior reviewers" → long-tenured staff | fixed |
| PKG-3 | flagship_report.md §5 | Publication rule stated as it stands (AI roles), flagged as AI checking AI, and the requested human-reviewer change noted (CR-FIX-A-001) | fixed |
| EVD-3 (R15) | flagship_report.md §5 link 1 | "Reinstated only in plaintiff states" removed; July 2025 offers to non-plaintiff grantees added [111] | fixed |
| PKG-6 | flagship_report.md §5 | L1–L5 → links 1–5 | fixed |
| EVD-11 (R73) | flagship_report.md §5 link 4 | Canaries caveats added | fixed |
| WP15-C177 | flagship_report.md §5 | A5 wording applied verbatim | fixed |
| PKG-27 / EVD-5 (item 5) | flagship_report.md §6.1–6.4 | "Foresight lead built" → foresight agent drafted, no human panel; "Wind-tunnelling" → "Stress-testing (desk analysis)" with an explicit note that no workshop or panel reviewed it and that the substitution-first verdict partly follows from the scenario definitions; no-regret list introduced as the foresight analysis's judgment | fixed |
| PKG-6 | flagship_report.md §6 | SC1–SC4 → scenario names; NR-1…8 and CM-1…7 ID columns → plain numbering | fixed |
| EVD-14 (R98) | flagship_report.md §6.1, §6.5 | "No court ruling … had occurred" → EMST's foresight review found none (a not-found result, not a docket search) | softened |
| PKG-1 | flagship_report.md §7.1 | Data-model bullet says time share, criticality, needed-at-entry and target fields stay empty in public views | fixed |
| EVD §4.7 (R90, R91) | flagship_report.md §7.1 | Mobility evidence framed as "announcing skills-based policy does not by itself change who is hired"; BGI/HBS figures per SBH-01 (37% drove nearly all change, 45% in name only, fewer than 1 in 700 hires in 2023); private-firm scope; Colorado baseline caveat | fixed |
| EVD-12 ([97]) | refs | Higher Ed Dive replaced by the Harvard Project on Workforce post (primary authors' summary), as SBH-01 requires | fixed |
| PKG-1 | flagship_report.md §7.2 | Federal HR first bullet rewritten as PKG-1 text (no time shares or flags; left to supervisor and job analysis) | fixed |
| PKG-7 / EVD-10 (R82) | flagship_report.md §7.2 | Questionnaire rule now gives exceptions (seasonal, GS-4 and below, OPM-authorized); percentages scoped to delegated examining | fixed |
| EVD-10 (R84) | flagship_report.md §7.2 | Tier 2 "no date" kept; plan's governmentwide FY2028 target added (FED-03 do_not_say respected) | fixed |
| EVD-16 (R85) | flagship_report.md §7.2 | OPM series decision marked "as of 23 October 2026; to be re-checked" | fixed |
| PKG-17(b) | flagship_report.md §7.2, §7.3 | RIF memo named by title and date only (FED-10) with "do not use EMST profiles for competitive levels or retention" | fixed |
| PKG-17(e) | flagship_report.md §7.2 | Bargaining line added without new factual claim ("check with your labor-relations office") | softened |
| PKG-17(a) | flagship_report.md §7.2 | SME-QA and USA Hire not added: no register row or verified source | deferred: needs a verified source and register row |
| PKG-17(c) | report | Read the FED-10 memos' content before release (report cites titles and dates only) | deferred: memo content not read this pass |
| PKG-17(d) | flagship_report.md §7.3 | Essay/political-designation sentence spelled out per ADR-0016 (Merit Hiring Plan essay questions; Schedule Policy/Career) | fixed |
| PKG-17(f) | report | Job-Analysis Starter Pack effort estimate | deferred: no estimate exists in EMST records |
| PKG-19 | flagship_report.md §7.2 | State officer bullet now says air, water, wastewater, drinking-water, waste and environmental-health roles exist only as lower-depth drafts with no briefs yet, and to check EPA-provided training status [J] | softened: no dated plan for the missing briefs exists to cite |
| EVD-4 (R19) | flagship_report.md §7.2 | "As Pennsylvania does through equivalency" replaced with the STATE-PA-01 wording | fixed |
| PKG-20 / PKG-8 | flagship_report.md §7.2 | NGO bullets: exit portfolios added; pilot "planned", not yet funded, stipends depend on funding being sought; pointer to the single contact line | fixed |
| PKG-20 | report | Public Lands Corps hiring authority not named: no verified terms in the register | deferred: needs a verified source and register row |
| PKG-21 | flagship_report.md §7.2 | Educator bullets: field-practicum rules pointed to as course design; proficiency levels in plain words [118]; no target level shown as a finding | softened: one-page educator guide, counts and SAF/ABET/CIP roadmap are new content outside an editing pass |
| EVD-16 (R87) | flagship_report.md §7.2 | SOC 2028 schedule at risk ("second FR notice to be determined") | fixed |
| PKG-39 | flagship_report.md §7.3, §8.3 | AUC and α thresholds rewritten in plain words | fixed |
| PKG-6 | flagship_report.md §8.1, §8.5 | `validationStatus = draft`, "2.0.0-rc.1", "Gate G1" and "wildcard" replaced by plain words | fixed |
| PKG-11 | flagship_report.md §8.5 | Design-partner track described as potential partners (none committed); federal-to-state crosswalk "EMST proposes to test with a state partner" | fixed |
| PKG-33 | flagship_report.md §8.5 | Timeline already sorted by start date (Nov 2026, Jan 2027, Feb 2027, Mar 2028, 2029); no change | n/a |
| PKG-8 | flagship_report.md §8.5 | Single CTA: "To comment, correct an error or ask about the pilot: {{EMST_CONTACT}}." Other asks point to it | fixed |
| EVD-14 (§4.8) | flagship_report.md §8.5 | Coalition statement dated to EMST's October 2026 scan (RPT-25 do_not_say respected) | softened |
| PKG-6 / PKG-3 | flagship_report.md Methods | WP-14/WP-15 removed; build described as AI-agent drafting and checking; two later reviews described as not by independent human experts; technical note on identifiers added | fixed |
| EVD-13 / EVD §5 pipeline | flagship_report.md Methods | "Checks every hard-coded value … fails if a record changes" → "checks key values … fails if a record changes, is withdrawn or is superseded; does not check every cell" | fixed |
| EVD-16 | flagship_report.md Methods | Moving-facts list completed with dates (OFCCP, Colorado, SB 253, Section 106, objection rule, S. 5653, SPEED, Part 108, OPM series, SOC) | fixed |
| PKG-30 | flagship_report.md (whole) | US spelling throughout body (program, labor, behavior, labeled, license, favor, signaling); "sector actor" → "employer type"; formation glossed | fixed |
| PKG-24 | report | OPM Federal Workforce Data not pulled; §8.2 now says headcount rests on secondary analyses of OPM data | deferred: data pull is outside the report lane |
| PKG-23(b) | report | Government's stated rationale for each major action not added: would need new primary-source claims | deferred: needs sourced register rows |
| PKG-36 | refs | CRS mirrors (everycrsreport) kept; congress.gov URLs not fetched this pass | deferred: congress.gov URLs not verified |
| PKG-34 | report | SPEED Act wording in the report is already the single "pending in the Senate EPW Committee" form | n/a |
| EVD-13 (§5 pipeline) | figures/build_figures.py | `check()` now rejects status `superseded`; every `source_ids` cell passes through `cite()`, which fails on a superseded ID unless `SUPERSEDED_SUCCESSORS` names the current register row (CP-043, IO-034 → AIGOV-02; V4-07 → BLS-01), and that row is itself checked. Tested: superseded IDs without a successor stop the build | fixed |
| EVD-13 (§5 pipeline) | figures/build_figures.py | Docstring softened: "key hard-coded values … needle check … does not check every cell" | fixed |
| EVD §5 F01 / PKG-5 | figures/f01, figures_index.csv | Headline: "two largest land-management agencies by staff"; "fiscal and policy shock, not an AI effect" → personnel and hiring actions named, AI effect unmeasured, evidence label "E for values; J for attribution"; bound rows now have blank `value_pct` and a separate `value_pct_bound` so they cannot be plotted as exact | fixed |
| EVD-13 / EVD-7 / PKG-14 (F02) | figures/f02, figures_index.csv | Headline: "largest type … 232 of the 329 that report a type; 175 report none"; source note lists the eleven units with counts (computed and asserted); evidence label → EMST derivation; new check against register RPT-27 and corrected OMB-02 | fixed |
| EVD-13 (F03) | figures_index.csv | NOAA's 157 records (no stage) named in the headline and note; broad `permit` pattern noted; label → EMST derivation; check against new row RPT-28 | fixed |
| EVD §5 F04 / EVD R63 | figures_index.csv, f04 | Headline names the USDA (search/knowledge-retrieval) and Interior (writing tool) rows; note says the USDA row exists only because of the "knowledge retrieval" keyword and that bands are department-wide; column renamed `license_or_user_band` | fixed |
| EVD-8 (R80) / EVD-13 (F05) | figures/f05, extract_openlmp_plans.py, openlmp_plan_level_extract.csv | F05 rebuilt with five rows: headline plus four sensitivity variants (no monitoring reports; plans only; no zero-monitoring documents; both), n per era, bootstrap intervals; headline scoped to western national forests, "durable demand" dropped, document-type finding stated; label → EMST derivation. Build asserts the extract reproduces the stored plan-equal means and n | fixed |
| EVD §5 F06 | figures/f06 | Normal-approximation CIs (negative lower bound) replaced by seeded percentile bootstrap; plans-only columns added; headline adds that content differences hold among plan documents and partnership rises distinguishably only there; label → EMST derivation | fixed |
| EVD R71 / EVD §4.4 (F07) | figures/f07, figures_index.csv | `role_in_figure` column (data scientists = reference only; compliance officers = broad occupation); band column renamed `emst_band_relative_to_average` and labeled as EMST's convention | fixed |
| EVD §5 F08 / PKG-5 | figures_index.csv | Headline scoped to federal land agencies and corps, "fiscal and policy reasons" removed; AmeriCorps context (Jun 2025 injunction, Jul 2025 reinstatement offers, coalition-only settlement) added to the note; letter date corrected | fixed |
| EVD-13 / EVD-2 / EVD-3 (F09) | figures/f09, figures_index.csv | Headline rewritten from the data (50 dated policy actions and 11 other steps in 2025–26; 6 scheduled for 2027) and says the timeline cannot show policy outpacing technology; AmeriCorps July 2025 notices and NJ Supreme Court certification (July 2026) added, checked against WF-06 and EJ-02; Colorado rows cite AIGOV-02 instead of superseded CP-043/IO-034; Part 108 row cites the OIRA record status; filter rule (any WP-15 source admits an event) documented | fixed |
| EVD-13 (F10) | figures_index.csv | "Cross all three crafts" → "designed to cross"; role code "CA" removed | fixed |
| PKG-6 | figures_index.csv | Role codes (LM, AS/CP, IO, CA) removed from source notes and labels; US spelling | fixed |
| EVD-13 | figures/ | Rebuilt with `python3 -I docs/package/report/figures/build_figures.py`; three consecutive runs give byte-identical outputs | fixed |
| EVD-12 ([70]) / EVD R57 | refs | AEI January 2026 report URL added (32% figure re-read by Fix-A) | fixed |
| EVD-12 ([50]) | refs, §1.3 | Lowenstein URL could not be opened (docx search hit unreadable); reference notes the possibly truncated URL; decision date corroborated by new reference [113]; label "register-verified in part" | softened |
| EVD-12 ([56]) | refs | CRS attribution notes it relays Forest Service legislative-affairs data | fixed |
| EVD-12 ([13]) / EVD R35 | refs | 91 FR 48236 (FR Doc 2026-15586) named as the official text; eCFR described as unofficial | fixed |
| EVD-12 ([60]) / EVD R44 | refs | Interview dated "c. 2024 (page modified 2025-03-13)" | fixed |
| EVD-12 ([4]) / EVD R06 | refs | Press release date and letter date (2026-03-18) both given | fixed |
| PKG-2 ([26]) | refs | NewsNation reference says the OIG document itself was not read | fixed |
| EVD R43 | report §1.4 | "About 4,500" not adopted: WP-15 §C decided to keep 4,536 (summary table value) | n/a |
| EVD R29 | report §1.3 | Optional D.C. Circuit briefing note not added | n/a (optional) |
| EVD-16 (primary-source check) | report §4.2, refs [115] | Part 108 confirmed still pending at OIRA on 2026-10-23 (reginfo.gov). federalregister.gov API was blocked for Fix-A, so OFCCP, objection rule and Section 106 were not re-read; future events carry as-of and re-check dates instead | softened |
| EVD-1 (register rows) | docs/methods/claims_register.csv | Of the 38 claims flagged "add to register / confirm", 29 already had RPT rows added by WP-15 after claims_used.csv was built; all 38 are now linked. New rows RPT-27 (AI type shares, R62) and RPT-28 (function families, F03). 50 existing rows updated from the review's verdicts (22 claim texts, 15 do_not_say entries, 5 statuses; see next rows) | fixed |
| EVD-2 / EVD-3 / EVD-4 | claims_register.csv | EJ-02 (NJ certification, status corrected), WF-06 (July 2025 notices; coalition-only settlement; new do_not_say), STATE-PA-01 (OA equivalency wording) and STATE-PA-02 (clarification and new do_not_say) updated | fixed |
| EVD-6/7/8/10/11 | claims_register.csv | RPT-01 (percentile bands), OMB-02 and RPT-04 (eleven units), PLAN-01 (sensitivity), FED-02 (exceptions), FED-03 (FY2028 target), FED-05, WF-03, WF-04, WF-07, RPT-11, RPT-15, IDX-01, IDX-02, IDX-04, IDX-05, AEI-02, AEI-03, NEPA-05, NEPA-08, UAS-01, UAS-02, SBH-02 and others updated; verification IDs `EVR-Rnn` point to the evidence-review rows | fixed |
| Cross-lane | claims_register.csv | Two new wrong forms that still appear in data/v2 signal text ("nine environmental bureaus", "monitoring requirements") are double-quoted so the explorer's output check does not yet fail on them; re-quote after CR-FIX-A-003 | deferred: orchestrator decision; data fix outside all lanes |
| EVD-1 / brief | docs/package/report/claims_used.csv | Regenerated from the edited report by a scratch script modeled on the original assembler (whose input file no longer exists): 280 claims, all 264 old IDs kept, 16 new (WP14-C265 to C280), 143 linked to register rows, 137 EMST-record only, 0 awaiting a register row; columns unchanged | fixed |
| Lane | docs/decisions/change_requests/CR-FIX-A-001..003.md | CRs for the human-reviewer publication rule (ADR-0027), eight new sources for sources.csv, and data/script corrections (OpenLMP and OMB signal text, CI method, two DriverEvents, superseded provenance, field-craft text) | fixed |
| Housekeeping | docs/package/report/handback_summary.md | Marked as superseded by draft 0.9.1 | fixed |

## Summary (generated from the table above)

- **Rows:** 141. **Fixed** 116 · **softened** 12 · **deferred** 9 · **n/a** 4.
- **WP-15 corrections:** all ten applied (C008, C078, C155, C122, C177 required; C120 with reference [80], C156, C082, C006 and line 220 recommended). None had been applied before this pass.
- **Deferred:** E2 primary report ([64]); SME-QA and USA Hire; reading the FED-10 memo content; a Starter Pack effort estimate; the Public Lands Corps authority; the OPM workforce-data pull; the government's stated rationale for each action; congress.gov URLs for CRS mirrors; enforcing two wrong forms until data/v2 is corrected. Each needs a verified source, new content or a change outside the report lane.
- **Change requests:** CR-FIX-A-001 (named human reviewers before the career-ladder hypothesis is published; ADR-0027), CR-FIX-A-002 (eight new sources for `docs/methods/sources.csv`), CR-FIX-A-003 (OpenLMP and OMB signal text, interval method, two DriverEvents, superseded provenance, field-craft text).
- **Length:** the report body grew from about 11,000 to about 13,900 words (counting tables and front matter, excluding references), mainly from caveats, the sensitivity result, the glossary and the start-here box.
- **Reproducing the outputs.** Figures: `python3 -I docs/package/report/figures/build_figures.py` (byte-identical over three runs; the plan-level extract is rebuilt by `extract_openlmp_plans.py` from `/home/claude/lmps`). Claims list: the scratch script `fixa_claims_used.py` (with `fixa_claims_override.py` and the pre-fix claims list as its ID map). Register: `fixa_register.py` (idempotent). The scripts are in the Fix-A scratchpad, as the original WP-14 assembler was.
- **For the orchestrator:**
  - The report's status line gives this file's own numbers. All 118 references are tied to register rows (10 of them only in part), so "13 references were read but not re-verified" is no longer true for the report. Other files may still need the template wording.
  - The F05 sensitivity check undercuts the plan-monitoring headline. The report and figures now say so; deck slide 7 and any brief that repeats "demand is moving toward monitoring" need the same change (Fix-B).
  - Carry over to the companion Skills Taxonomy project: NJ EJ status, the AmeriCorps July 2025 notices, the Pennsylvania wording, the exposure percentile-band wording and the plan-monitoring sensitivity result.

Addendum: F10's `context_signals_attached_watch` counts changed for four roles on rebuild (for example R02 18 → 17), because the role change views were regenerated upstream (16:53) after the original figure build (16:20). The rebuild reflects current data; no figure logic changed. F10 corridor names now match the report's corridor names (PKG-6; US spelling).
