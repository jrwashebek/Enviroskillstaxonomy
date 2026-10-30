# R2: User needs evidence base for the EMST public interface

**Role:** User-needs researcher (secondary research only) · **Date:** 30 October 2026 · **Status:** for the HCD lead
**Labels:** [E] I read the source (URL or repo path given) · [J] my judgment, with its basis · [S] speculation, with what would settle it.
**Nothing here comes from a real user of EMST.** It is published evidence about each group's work, plus judgment. Every persona, JTBD and unknown below is a hypothesis to test.

---

## Executive summary

1. **Federal HR already has an AI tool for position descriptions, and it is not EMST.** OPM's USA Class (inside USA Staffing since May 2026) drafts PD duties from existing PDs; managers verify and classifiers set factor levels [E]. A separate EMST PD builder would compete with a free in-workflow tool. EMST's realistic U5 role is reference language people copy or import [J].
2. **The federal assessment gap is real, but EMST cannot fill it yet.** Self-assessment may no longer rate or rank (since 30 September 2025), and every hire needs a validated, job-analysis-based assessment [E]. In FY2025, 91% of delegated-examining announcements still relied on self-report only, 15% of agencies had I-O psychologists, and OPM estimates ≥100 work hours per assessment [E]. No EMST record reaches develop or select; the interface must stop describe-tier content being used as assessment content [J].
3. **HR capacity has collapsed while the rules multiply.** About 7,600 federal HR managers left by March 2026 [E]. OPM is consolidating 115 series (0455 Range Technician → 0404; four others → 0401) and reissuing standards for 600+ series by end FY2027 [E]. Undated crosswalks will go stale within months [J].
4. **Skills-based hiring changed postings, not hires.** Fewer than 1 in 700 hires benefited in 2023; 45% of announcing firms were "in name only" [E]. Colorado rewrote ~80% of classes; non-degree hires stayed at 25% [E]. Expect scepticism of skills-based promises [J].
5. **People search by title, not code or competency** [E]. OPM now separates descriptive titles in announcements from official series titles [E]. Each group has its own codes and slang, and search must also normalise spelling: rc.1 uses "programme" 957 times and "behaviour" 164 times, while US titles use "program" and "behavior" (NWCG's Fire Behavior Analyst) [E: repo].
6. **Military-skills translators fail in ways EMST could repeat.** DoD's title-level crosswalk gave 1.5 civilian matches per occupation; a DOL task-based pilot found 14.1 but needed SME review to remove false ones; keyword matching produced absurd links [E]. Only 2% of HR professionals use translators [E]. Match at task level, show level, never say "you qualify" [J].
7. **Corps outcome data exist, contradicting the internal personas.** In a 2024 RTI evaluation of 16 programmes, 76% of alumni were employed at one year (31% of them in government) and 63% earned $10k–$50k; seasonal work, housing and pay were the barriers [E]. A 10 September 2026 settlement protects AmeriCorps FY2026–27 funds [E].
8. **Small NGOs have little time.** Only 6% of nonprofits rated leader development plans a strength (2011 data); 34% struggled with professional development in 2024 [E].
9. **Disclosing AI costs some trust; being exposed costs more** [E]. People read "AI-generated" as "no human involved"; naming the human role reduces the penalty [E]. Verbal uncertainty words drift towards 50% unless anchored [E]. EMST's tier words need "you may / you may not" examples [J].
10. **Reading level and phones set the floor.** 28% of US adults are at or below Level 1 literacy; 28% of those earning under $30k are smartphone-only [E].
11. **SMEs will not correct via GitHub unless it is easy and answered.** Rejected or unanswered newcomers leave [E]. NIST's GitHub comment process keeps email as a fallback [E], but the explorer build fails on any email address [E: repo].
12. **Top unknowns** (§14): misreading of tiers and "Assessment pending"; whether HR has any slot for EMST; the words people type; whether the phone-saved gap check works in the field; whether SMEs will contribute.

---

## 1. Method and limits

- **Sources.** About 70 web searches and 60 page reads, favouring primary sources (OPM, NWCG, USFS, NIST, ESCO, state HR sites, peer-reviewed papers); the five internal documents in the brief; and `dist/2.0.0-rc.1` for vocabulary.
- **The shared web-search budget ran out** before I could check Public Lands Corps hiring-authority hours, NASPE state workforce-planning material, O\*NET's licence, the FAIR principles and SOC 2018 titles. A follow-up session can close these.
- **Five URLs were blocked by permission timeouts and not read:** onetcenter.org/license_db.html; eforester.org/SAF/Main/Accreditation.aspx (I read another public SAF page); go-fair.org/fair-principles; bls.gov/soc/2018/major_groups.htm; the NIFC 0401 supplemental qualification standard PDF. Claims depending on them are labelled [J].
- **Not used:** the SAF Accreditation Handbook PDF (per instructions). The internal LC report quotes it; I do not rely on those passages.
- **Currency.** Federal hiring policy moved monthly in 2025–26. Anything dated before about August 2026 may have changed.

---

## 2. U5: Federal HR specialists, classifiers, training officers and workforce planners

### Context and stakes
- **The Merit Hiring Plan (29 May 2025) reset federal hiring** [E: OPM MHP resources]. Its main rules:
  - Rule of many final rule: published 8 September 2025, effective 7 November 2025, full compliance by 9 March 2026. Candidates are scored and ranked.
  - Cut-off scores based on assessments must be supported by job-analysis data.
  - OPM estimates each assessment takes at least 100 work hours to build [E: 90 FR 2025-17125].
  - Self-reported assessments may screen for minimum qualifications but not rate or rank. Waivers are rare and limited to GS-1 to GS-4 and seasonal roles. At least one validated skills-based assessment is required [E: OPM guidance, Feb 2026].
- **Practice lags policy.** In FY2025, 91.23% of delegated-examining announcements relied solely on self-report; 15% of 117 agencies had I-O psychologists; 21% (38% of CFO Act agencies) struggle to identify suitable assessment types [E: OPM Chance to Compete report, Dec 2025].
- **Competency models exist but are thin for this sector.** OPM's FWCI models cover 80 series, including **0404 Biological Science Technician** and **0462 Forestry Technician** at grades 5–11. OPM says agencies must still run their own job analyses [E: FWCI transmittal 2023].
- **Classification is being rebuilt.** There are 609 classification standards [E: OPM "Hiring is hard", May 2026]. On 24 April 2026 OPM proposed consolidating 115 series; in the 0400 group 0410, 0437, 0480 and 0487 move to 0401, 0455 to 0404 and 0459 to 4701 [E]. Standards update through September 2027; later phases address "skills-based workforce frameworks"; bargaining obligations apply [E].
- **Capacity has fallen.** About 7,600 federal HR managers left between January 2025 and March 2026; OPM opened an HR shared-service centre and is procuring a single HR system for 2027 [E: Federal News Network].

### Jobs to be done (hypotheses)
- When I review a manager's draft PD for a 0401 or 0404 position, I want plain, current task and knowledge language I can check the draft against, so I can spot missing or outdated duties before I classify. [J]
- When I build a technical assessment under the Merit Hiring Plan, I want a starting list of tasks and competencies that SMEs can cut and rate, so I can finish the job analysis in hours, not weeks. [J; need E]
- When a series I support is consolidated, I want to see which competencies and tasks the old and new series share, so I can explain the change to employees and the union. [J]
- When I write a staffing-plan justification for a Strategic Hiring Committee, I want a defensible description of what the role does that no one else on staff can do, so the hire is approved. [J; the internal FH document describes this trigger]

### Current tools and workarounds [E unless marked]
- **USA Staffing**, including **USA Class** (AI PD drafting from May 2026). USA Class supports only non-supervisory, single-standard 9-factor FES PDs. Supervisory, mixed-series and wage-grade PDs are not supported [E: USA Staffing help centre].
- **USA Hire** general-competency batteries, the **USAJOBS Agency Talent Portal**, shared certificates and pooled hiring [E: MHP resources].
- **OPM classification and qualification standards** and the Classifier's Handbook. OPM's December 2025 Project Manager PD templates came with a **competency crosswalk**, which shows OPM itself pairing PDs with competency models [E: OPM memo, 31 Dec 2025].
- **FWCI and MOSAIC competency models** [E].
- Agency standard-PD libraries, Word documents and spreadsheet crediting plans [J: standard practice; not verified this session].

### Pain points
- Fewer HR staff, more required steps (assessments, job analyses, cut scores) and little in-house assessment expertise [E].
- Standards and series in flux through FY2027, so reference content goes stale [E].
- Policy and litigation churn: the Merit Hiring Plan essay questions were challenged in *AFGE v. Kupor* [E: case listing]; I could not verify the status of the stay the internal FH document reports.
- PD writing is "hard and time-intensive", in OPM's own words [E].

### Vocabulary that matters for search [E from the sources above; J for completeness]
- **Documents and rules:** PD, major duties, FES, factor levels, Factor 1 "Knowledge required", series, grade, GS-xx, interdisciplinary PD, classification standard, qualification standard, specialized experience, selective factor, positive education requirement.
- **Hiring and workforce:** job analysis, 5 CFR 300.103, crediting plan, SME-QA, USA Hire, USA Staffing, USA Class, rule of many, category rating, cut score, shared certificate, CTAP/ICTAP, Strategic Hiring Committee, staffing plan, RIF, competitive level, IDP.
- **Series:** 0401, 0404, 0408, 0454, 0455 (→0404), 0456, 0457, 0460, 0462, 0482, 0486, 0028, 1315, 0025, 0819.
- **Title layers:** official titles (personnel records) versus descriptive titles (announcements), e.g. "AI/ML Engineer" for IT Specialist GS-2210 [E: OPM titling memo, 9 September 2025]. Search needs both.
- **Coverage gap:** rc.1's federal series views cover 13 series but not 0401 (target for four consolidated series), 0404 (FWCI model; target for 0455) or 0462 (FWCI model) [E: `dist/2.0.0-rc.1/views/federal_series_profiles/index.json`].

### Devices and connectivity
- Government laptops (PIV), desktop browsers, Word and USA Staffing [J]. Some agency networks may block GitHub or downloads [S; ask 5–6 federal HR staff].

### Trust and distrust
- **Builds trust:** CFR and OPM citations; dated, versioned crosswalks; exact series status (active or proposed realignment); explicit "not a job analysis / not a classification basis" wording; a USWDS look [J]. A method page matters: the SHRM–SIOP paper warns that undocumented competency models create evidentiary gaps and get used for unplanned purposes [E].
- **Destroys trust:** any claim of OPM alignment (already banned by ADR-0027), stale series, undisclosed AI drafting [E: §11].

### What EMST must never let them do
- Use it as a job analysis, classification basis or crediting plan.
- Take rating or ranking items or cut scores from it.
- Use it for RIF competitive levels, retention, Schedule Policy/Career designations, performance appraisal or CTAP/ICTAP well-qualified determinations.

### Evidence strength
- **Strong [E]** on rules, tools and capacity.
- **None** on how classifiers actually use competency content day to day. No ethnographic or survey study was found; this is a gap.

**Sources:** OPM Merit Hiring Plan resources https://www.opm.gov/policy-data-oversight/hiring-information/merit-hiring-plan-resources/ · Rule of Many final rule https://www.govinfo.gov/content/pkg/FR-2025-09-08/html/2025-17125.htm · Self-reported assessments guidance https://www.opm.gov/policy-data-oversight/hiring-information/merit-hiring-plan-resources/guidance-on-the-use-of-self-reported-assessments.pdf · Chance to Compete consolidated report https://www.opm.gov/about-us/reports-publications/agency-reports/chance-to-compete-act-of-2024-consolidated-report-to-congress.pdf · FWCI https://www.opm.gov/chcoc/transmittals/2023/Federal%20Workforce%20Competency%20Initiative%20-%20General%20Competencies%20and%20Competency%20Models.pdf · Series consolidation memo https://www.opm.gov/chcoc/latest-memos/modernization-and-consolidation-of-occupational-series.pdf · USA Class FAQ https://abrc-usastaffing.opm.gov/hc/en-us/articles/50990834676627-General-Questions · FEDweek on USA Class https://www.fedweek.com/federal-managers-daily-report/opm-launches-ai-tool-for-writing-position-descriptions/ · Excella case study (vendor) https://www.excella.com/wp-content/uploads/2026/07/Excella-OPM-USA-Class-Fast-Tracking-the-Future-of-Federal-Hiring-Case-Study.pdf · OPM "Hiring is hard" https://www.opm.gov/news/secrets-of-opm/hiring-is-hard/ · PM PD templates memo https://www.opm.gov/chcoc/latest-memos/implementation-of-opmʼs-project-management-position-description-templates-and-skills-based-hiring-guidance.pdf · Job titling memo https://www.opm.gov/chcoc/latest-memos/job-titling-guidance-in-alignment-with-executive-order-14170-and-the-merit-hiring-plan · HR shared services https://federalnewsnetwork.com/it-modernization/2026/03/opm-launches-new-hr-shared-service-center-for-agencies/ · 0401 qualification standard https://piv.opm.gov/policy-data-oversight/classification-qualifications/general-schedule-qualification-standards/0400/general-natural-resources-management-and-biological-sciences-series-0401/ · SHRM–SIOP competency modelling documentation https://www.siop.org/wp-content/uploads/2024/07/SHRM-SIOP_Competency_Modeling_Documentation.pdf · AFGE v. Kupor case listing https://clearinghouse.net/case/47255/

---

## 3. U4: State HR, classification and training officers

### Context and stakes
- **States run their own merit systems, with different formats** [E]. Washington's spec for Natural Resource Scientist 3 (516M) has Definition, Distinguishing Characteristics, Typical Work, Knowledge and Abilities, Legal Requirements, Desirable Qualifications and History (established 1970, revised 2023–2025). California fills Environmental Scientist (00100762) through a continuous online exam with a training-and-experience self-rating; a 70% pass puts candidates on a 12-month eligible list ranked by score, with veterans' preference.
- **Classification studies are large, consultant-led rewrites.** Nevada's 2024 study found more than 2,000 titles, proposed about 669, recommended "skill-based job descriptions" and kept working titles beside official ones [E].
- **Skills-based hiring is widespread on paper.** About 26 states have acted, yet 61% of state postings still require a degree; Maryland's no-degree postings rose from 32% to 47% (2022–2024) [E: Lightcast/NGA]. Colorado: ~80% of classes now emphasise skills, but non-degree hires stayed at 25%; Colorado and Maryland froze hiring in summer 2025 [E: CPR].

### Jobs to be done (hypotheses)
- When I run a classification study for environmental classes, I want a current description of tasks and knowledge by level that I can compare with our 20-year-old specs, so I can rewrite Typical Work and the minimum qualifications without starting from zero. [J]
- When displaced federal staff apply, I want to see how federal series work relates to our classes, so I can credit their experience fairly. [J; internal persona "Teresa"]
- When I plan training for a programme taking on devolved federal work, I want to know which competencies that work needs, so I can budget training instead of hiring during a freeze. [J]

### Current tools and workarounds
- Class-spec libraries, exam bulletins and consultants [E]; O\*NET, state LMI, manager interviews and position questionnaires [J; no usage evidence found].

### Pain points
- Thousands of near-duplicate titles [E: Nevada]; managers who still prefer degrees; slow manual rewriting of job descriptions; hiring freezes [E: CPR].
- Weak outcome tracking. CPR says Maryland and Pennsylvania track applicants, not hires; NGA/Lightcast says ~60% of Pennsylvania's new hires lack a degree. Unresolved.

### Vocabulary
- **Process:** class specification, class series, class code, allocation, reclassification, classification and compensation study, minimum qualifications (MQs), desirable qualifications, KSAs, Typical Work, exam bulletin, T&E evaluation, eligible list, working title, pay band, bargaining unit, merit system.
- **Titles:** Natural Resource Scientist 1–4, Environmental Specialist 1–5, Natural Resource Technician, Environmental Scientist, Senior Environmental Scientist (Specialist/Supervisory), Forester, Park Ranger [E for WA and CA; J for others]. Codes differ by state, so search needs state + title + code.

### Devices and connectivity
- Desktop, state IT, Word and PDF [J].

### Trust and distrust
- **Builds trust:** links to the official class spec (rc.1 has 38 state class records), dates, no alignment claim [J].
- **Destroys trust:** a crosswalk that looks like an official equivalency [J].

### What EMST must never let them do
- Treat a match as a class allocation or MQ equivalency; rank exam candidates; decide layoffs or bumping.

### Evidence strength
- **Moderate** on structures and outcomes; **weak** on classifier practice and state workforce planning (NASPE material surfaced but was not read before the search budget ran out).

**Sources:** WA OFM class spec 516M https://ofm.wa.gov/state-human-resources/compensation-job-classes/ClassifiedJobListing/Specifications/234 · CalHR Environmental Scientist exam bulletin https://calcareers.ca.gov/CalHrPublic/Exams/ExamBulletin.aspx?ExamControlId=1709 · Nevada classification and compensation study https://leg.state.nv.us/Division/Research/Documents/RTTL_2023_AB451_2024.pdf · CPR on Colorado https://www.cpr.org/2025/12/03/colorado-jobs-degrees-skills-based-hiring/ · Lightcast/NGA https://lightcast.io/resources/blog/nga-skills-based-hiring-data-snack

---

## 4. U6: Workforce boards, educators and curriculum designers

### Context and stakes
- **Colleges use labour-market information (LMI) mostly for programme review and new programmes;** two-year colleges often rely on it for final decisions because funders require it [E: Rutgers EERC 2023, 10 institutions, 50 interviews]. Barriers: data literacy, staff scepticism, vendor licence cost (one campus held 34 licences) and overload. Skills-to-curriculum mapping was early-stage almost everywhere [E].
- **Perkins V needs assessments.** Illinois' CLNA guidance points colleges to state data tools and employer advisory committees, not O\*NET [E].
- **O\*NET usage.** 3,500+ web-services users (1,015 education and research, 274 government and workforce, 1,018 commercial); 2.26 million database downloads to May 2023; uses include the Virginia Education Wizard and Kentucky's Future Skills Report [E: O\*NET OMB appendix].
- **DACUM is how many technical programmes get job content:** a facilitator leads 5–12 expert workers for about two days to chart duties, tasks, knowledge, tools and trends [E: Ohio State CETE].
- **SAF accreditation** covers forestry, urban forestry, NREM and forest technology; the public page calls it "not a ranking system" and lists an undescribed "2025 Standards Statement" [E]. I did not use the handbook.
- **Policy.** Workforce Pell for 8–15-week programmes began in July 2026 with governor approval and workforce-board consultation (search-result titles from ACTE, NCAN and states, plus internal LC-019; rule text not read). A WIOA reauthorisation expanding "Make America Skilled Again" block-grant pilots passed House committee in May 2026; later status unknown [E: NYEC].

### Jobs to be done (hypotheses)
- When an advisory committee asks for a new environmental-technician certificate, I want a task and competency list I can start a DACUM or validation session from, so the panel edits rather than invents. [J; DACUM premise E]
- When I map a curriculum, I want stable competency IDs at one level with observable outcomes, so course outcomes can point at something that will not change next term. [J]
- When a workforce board prioritises sectors, I want to know which environmental roles exist across employers and what they are called, so we can fund the right training. [J]

### Current tools and workarounds
- O\*NET; state LMI portals; vendor real-time LMI (Lightcast and others) [E: Rutgers].
- DACUM [E].
- Advisory committees [E].
- Accreditor templates and spreadsheets [J].

### Pain points
- Data literacy and cost [E].
- O\*NET occupations are too coarse for environmental roles [J; internal CP view, not tested].
- Accreditation cycles of years versus a taxonomy that is still in draft [J].

### Vocabulary
- CIP code (03.xxxx Natural Resources and Conservation); SOC code (e.g. 19-2041, 19-4071, 45-4011; [J], BLS page blocked); programme and course learning outcomes; curriculum map; CLNA; Perkins V; advisory committee; ETPL; in-demand occupation list; sector partnership; career pathway; stackable credential; Workforce Pell; Registered Apprenticeship; work process schedule; DACUM chart.

### Devices and connectivity
- Desktop, spreadsheets, LMS [J].

### Trust and distrust
- **Builds trust:** stable IDs and versions; sources per statement; practitioner validation, which is the DACUM norm [E].
- **Weakens trust:** AI drafting without practitioner review cuts against the DACUM premise; educators may treat EMST as a pre-panel draft at best [J].

### What EMST must never let them do
- Present EMST alignment as accreditation evidence, or a crosswalk as proof that graduates qualify (the CIP–SOC guidelines warn the same; internal LC report).
- Advertise programmes as "EMST-certified".

### Evidence strength
- **Moderate** on LMI use.
- **Weak** on how educators use competency models in curriculum design. No study found.

**Sources:** Rutgers EERC LMI report https://www.smlr.rutgers.edu/sites/default/files/Documents/Centers/EERC/Emerging%20Insights%20Report%20Final%20Formatted%205.3.23.pdf · ICCB CLNA guidance https://www.iccb.org/wp-content/pdfs/cte/CLNA-guidance-document-FINAL-1.pdf · O\*NET OMB Appendix C https://www.onetcenter.org/dl_files/omb2024/AppendixC.pdf · DACUM overview https://cete.osu.edu/wp-content/uploads/2021/02/DACUM-Overview-Brochure.pdf · SAF accreditation home https://eforester.org/Main/Certification_Education/Accreditation/Main/Accreditation/Accreditation_Home.aspx · NYEC WIOA update https://nyec.org/2026/05/may-2026-policy-spotlight-wioa-reauthorization-bill-passes-along-party-lines/ · DOL LMI Improvement grants briefs https://www.dol.gov/agencies/eta/research/publications/practitioner-briefs-evaluation-labor-market-information-lmi

---

## 5. U1: NGO and conservation-corps programme and training leads

### Context and stakes
- **The Corps Network** reports nearly 140 corps and 22,000+ young people (16–30) and recent veterans (to 35) a year; it accredits corps and passed through $12 million+ in FY2025 [E].
- **AmeriCorps.** April 2025 cuts of ~$400 million hit 1,000+ programmes (WisCorps cut a third of members; Pacific Crest Trail corps hours fell from 19,000 to ~4,000) [E: Backpacker]. A 24-state settlement of 10 September 2026 protects FY2026–27 funds and pauses litigation to 1 February 2027 [E: California AG].
- **USFS Resource Assistants Program:** a paid internship; completers gain two years of direct-hire or noncompetitive eligibility [E: USFS]. The Corps Network gives the threshold as 960 hours plus an associate degree or two-year certificate; Forest Service units select [E].
- **Development is weak in small NGOs.** In Bridgespan's diagnostic of 131 nonprofits, leader development plans scored 2.40/4 and 6% rated them a strength [E, ~2011]. In 2024, 34% struggled with professional development and 55% with competitive pay [E: Careers in Nonprofits].

### Jobs to be done (hypotheses)
- When I write a grant report or proposal, I want to describe what members learned in terms funders and agencies recognise, so the programme looks like a pathway, not just labour. [J; internal UC5]
- When a member finishes a term, I want a portable summary of what they did and at what level, so they can apply to state or federal entry jobs. [J; RTI shows members want help with federal applications, E]
- When I redesign season training, I want to see which tasks destination employers expect, so training points somewhere. [J]

### Current tools and workarounds
- Member service-hour logs, certification records (chainsaw, first aid), crew-leader training, partner job boards, AmeriCorps systems [J; RTI confirms certifications matter, E].
- No evidence found of NGOs using competency frameworks [gap].

### Pain points
- Funding instability [E].
- Low pay and housing for members [E: RTI].
- Thin staff time [E].
- Members' difficulty with federal applications [E: RTI].

### Vocabulary
- corps, corpsmember (TCN spelling), member, crew, crew leader, individual placement, term, hitch, season, service hours, education award, AmeriCorps, Public Lands Corps, Resource Assistant (RA), RAP, noncompetitive hiring eligibility, direct hire, accredited corps, 21CSC, TREX.
- rc.1's "Conservation corps member" profile has only "corps crew member" and "conservation crew member" as alternative labels. It lacks "corpsmember", "AmeriCorps member" and "Resource Assistant" [E: repo bundle].

### Devices and connectivity
- Office desktop or laptop for leads [J].
- Crews in the field, often with no signal [J; extent is S, see §8 and §14].

### Trust and distrust
- **Builds trust:** content that names corps work accurately, and recognition from agencies and funders [J].
- **Destroys trust:** content that ignores corps reality (seasonal, low pay), or that seems to grade members [J].

### What EMST must never let them do
- Rank, select or dismiss members or staff.
- Issue anything that looks like a credential or certification.
- Imply a hiring authority or eligibility.

### Evidence strength
- **Strong** on funding and context.
- **None** on whether leads want competency tools at all.

**Sources:** The Corps Network https://corpsnetwork.org/about-us/ · RAP (TCN) https://corpsnetwork.org/programs-initiatives/federal-lands-agreements/resource-assistants-program · RAP (USFS) https://www.fs.usda.gov/working-with-us/careers/resource-assistants-program · Backpacker https://www.backpacker.com/news-and-events/news/how-americorps-cuts-impact-trail-crews/ · CA AG settlement https://www.oag.ca.gov/news/press-releases/attorney-general-bonta-secures-settlement-protect-americorps · Bridgespan https://www.bridgespan.org/getmedia/9b4ee100-81d2-4116-8116-9e551976f6eb/DatapointEmployeeDevelopmentAWeakness.pdf · Careers in Nonprofits 2024 https://nlp.uiowa.edu/sites/nlp.uiowa.edu/files/2024-08/2024-Nonprofit-Salaries-Staffing-Trends_1.pdf

---

## 6. U3: Supervisors and crew leads

### Context and stakes
- **Fire already has a strong observed-performance model.** NWCG updated PMS 310-1 on 23 January 2026, and the "Next Generation" task book for Basic Faller (FAL3, April 2025) adds an evaluation guide with rating elements [E]. Task books need a qualified evaluator to sign off observed performance [J: long-standing practice].
- **Evaluator capacity is shrinking.** The Forest Service has lost close to 6,000 permanent staff since January 2025, including red-carded rangers and timber technicians [E: NPR, June 2026].
- **Self-ratings are weak evidence:** across 166 studies, self-assessed knowledge correlated about .34 (corrected) with actual learning, rising to ~.51 with practice and feedback [E: Sitzmann et al. 2010].

### Jobs to be done (hypotheses)
- When I sit down for an end-of-season or development conversation, I want a short, concrete list of what "ready for the next step" looks like, so we agree on it. [J]
- When I write or update a position description or crew job posting, I want accurate task language, so the posting matches the work. [J]
- When I plan crew training, I want to know which skills my crew lacks across the team, without exposing anyone's ratings. [J]

### Current tools and workarounds
- NWCG task books, IQCS records, saw-programme certifications [E]; IDP forms and Word templates [J; a DOI supervisor IDP guide surfaced but was not read].

### Pain points
- Time, evaluator scarcity and self-assessment bias [E].
- Fear that development records leak into appraisal (the internal FH document flags FY2026 appraisal changes; not verified).

### Vocabulary
- crew lead, crew boss, squad boss, assistant crew leader, engine captain, sawyer (A/B/C; FAL3, FAL2), S-212, red card, PTB, IQCS, evaluator, trainee, IDP [J for field terms; E for FAL3, PTB, PMS 310-1].

### Devices and connectivity
- Phone in the field, laptop at the station. The gap check saves a file, and saving and reopening files on phones is awkward [J; test it].

### Trust and distrust
- **Builds trust:** indicators that describe observable behaviour, like task books do [J].
- **Destroys trust:** vague or "reputational" indicators. The internal FH document says 38.4% of v1 Expert indicators are reputational.

### What EMST must never let them do
- Use gap results in performance ratings, discipline or crew selection.
- Compare named individuals in a shared view.

### Evidence strength
- **Moderate** on context; **weak** on supervisor practice outside fire.

**Sources:** NWCG PMS 310-1 2026 https://www.nwcg.gov/announcement/publications/2026-updates-to-the-nwcg-standards-for-wildland-fire-position-qualifications-pms-310-1 · NWCG PMS 212 / Next Gen PTB https://www.nwcg.gov/announcement/publications/nwcg-standards-for-wildland-fire-chainsaw-operations-pms-212-and-next-generation-position · NPR/OPB on USFS staffing https://www.opb.org/article/2026/06/18/as-western-fires-erupt-trump-s-forest-service-says-it-s-now-fully-staffed/ · Sitzmann et al. 2010 https://www.gwern.net/doc/psychology/cognitive-bias/illusion-of-depth/2010-sitzmann.pdf

---

## 7. U2: Early-career staff and corps members

### Context and stakes
- **Outcomes after corps service** [E: RTI for the National Park Foundation, August 2024; 540 members in 16 crew-based programmes, 162 alumni at one year]:
  - 84% in a job or education at one year; 76% employed; 31% of the employed in government; 63% earning $10k–$50k, 5% above $50k.
  - 77% of certification holders said it was or would be useful at work.
  - 76% grew more confident with federal applications, yet only 51% felt confident of gainful employment.
  - Seven of eight alumni refusing conservation jobs cited low wages; seasonal work and housing problems were the norm.
- This **contradicts** the internal "Jordan" persona, which says no outcome data were published.

### Jobs to be done (hypotheses)
- When my term ends, I want to see which real jobs (federal, state, county, NGO, contractor) use what I did, and what each calls it, so I can apply to the right ones. [J; supported by RTI barriers, E]
- When I'm choosing what to learn next, I want to know which certificate or experience opens the next door, so I don't waste a season. [J]
- When I write a résumé, I want words that HR will recognise for my tasks, so I can get past screening. [J; RTI shows résumé training raised confidence, E]

### Current tools and workarounds
- USAJOBS, conservation job boards, corps staff and alumni networks, résumé workshops [E: RTI for networks and training; J for the boards].

### Pain points
- Low pay, seasonal work, housing, federal application complexity [E]; few permanent entry jobs after 2025–26 hiring freezes [J; internal sources, not re-verified].

### Vocabulary
- "conservation jobs", "trail crew", "seasonal", "park ranger", "biological technician", "forestry technician", "GS-5", "pathways intern", "AmeriCorps", "crew member", "RA" [J]. Announcements are moving to descriptive titles, so U2 will meet both kinds [E: OPM titling memo].

### Devices and connectivity
- Phone first [J]. 15% of US adults are smartphone-dependent (28% under $30k income); rural home broadband is 73%, against 86% suburban [E: Pew, 2023 data].

### Trust and distrust
- **Builds trust:** honest pay and seasonality context, and peer or alumni voices [J; RTI shows peer learning valued, E].
- **Destroys trust:** jargon, and anything implying a guarantee [J].

### What EMST must never let them do
- Believe they are qualified or eligible because EMST says the tasks match.
- Share a gap-check file that an employer then uses to screen them.

### Evidence strength
- **Strong** on outcomes and barriers; **none** on tool use.

**Sources:** RTI/NPF full report https://corpsnetwork.org/wp-content/uploads/2024/08/RTI_NPF_ServiceCorpsEvaluation_Report_Final.pdf · Executive summary https://corpsnetwork.org/wp-content/uploads/2024/08/RTI_NPF_ServiceCorpsEvaluation_ES_Final.pdf · Pew 2024 https://www.pewresearch.org/internet/2024/01/31/americans-use-of-mobile-technology-and-home-broadband/

---

## 8. U8: Career changers and job seekers

### Context and stakes

**Veterans**
- **Why translators disappoint** [E: DOL VOW Act §222 pilot]. DoD's crosswalk compares job descriptions at a high level, links most military occupations to one or two civilian ones (average 1.5) and ignores pay grade. A task-based method found 14.1 matches on average and added a "Directly Related" link (~80% of duties shared), a typical minimum pay grade and an attainability rating. SME review was essential (a signal specialist's computer link was downgraded because that work was rare). Keyword matching failed absurdly (Navy "DC" matched to Washington, D.C. jobs), and civilian words like "officer" misled service members.
- **Employers' view** [E: SHRM survey of 1,076 HR professionals, 2024]: 58% find mapping military occupations to civilian classifications hard; 48% cite no standard method; only 2% use translators, but 71% would try one.
- **RAND (2017)** built toolkits for non-technical skills (leadership, decision-making) because military and civilian vocabularies differ [E].
- **SkillBridge.** From 31 March 2026, Air Force and Space Force participation drops from up to 180 days to 90–120 by rank [E]. No DoD-wide 2025–26 data found.

**Seasonal wildland firefighters**
- Interior's US Wildland Fire Service (Secretarial Order 3448; Phase 3 January 2026) excludes Forest Service fire, which needs Congress [E]. Congress funded the two separately in FY2026 and ordered a feasibility study, due 15 February 2027 [E: USFS]. The FY2027 request again proposes moving USFS fire [E].
- FY2026 funded a permanent pay fix and job series [E]. USFS reported 11,550 seasonal firefighters in June 2026, about 200 above goal; GAO names low pay and limited advancement as retention barriers [E].
- For a seasonal firefighter in October 2026, "which agency, which rules" is unsettled until at least February 2027 [J].

**Job seekers in general** [E]
- **Titles first.** Applicants search mainly by title and infer requirements from it; titles carry far more distinctions than SOC codes (25 times as many unique titles) [Marinescu & Wolthoff, via BLS MLR].
- **Mobile.** 61% of applications were on mobile in 2020; ~80% of searches for grounds and construction jobs started on mobile in 2017 [Appcast via HR Dive; Indeed].
- **Reading.** 28% of adults are at or below Level 1 literacy; 34% low numeracy (2023) [NCES PIAAC].
- **AI in hiring.** 71% oppose AI making final hiring decisions; 66% would not want to apply where AI helps decide [Pew, December 2022 data].

### Jobs to be done (hypotheses)
- When I leave the military or a fire season, I want to see which environmental jobs use the work I actually did, at my level, and what they are called, so I can search with the right words. [J; translator evidence E]
- When I find a target job, I want to know what to check before applying (degree rules, certifications, veterans' preference), so I don't waste an application. [J]
- When I'm a seasonal firefighter, I want to see year-round roles near fire (fuels, prescribed fire, fire planning, state forestry), so I can stay in the work. [J; the rc.1 "Fuels and prescribed fire specialist" role exists, E: repo]

### Current tools and workarounds
- O\*NET Military Crosswalk and My Next Move [J; noted in internal CP strategy].
- CareerOneStop, TAP, American Job Center staff (who use O\*NET to translate) [E: APPAM 2015], SkillBridge, USAJOBS, Indeed, LinkedIn [J].

### Pain points
- Title-based mismatch and too few matches [E].
- Uncertain agencies and rules in fire [E].
- Low literacy or numeracy for a minority of users [E].

### Vocabulary
- **Military:** MOS (Army, USMC), AFSC, Navy rating and NEC, DD-214, TAP, SkillBridge, veterans' preference, VEOA, 10-point preference [J].
- **Fire:** FFT2, FFT1, ICT5, engine captain, hotshot or IHC, helitack, smokejumper, red card, pack test or work capacity test, seasonal or "1039" appointments, permanent seasonal, 0462, 0456 [J, from long-standing NWCG and federal usage]. "Work capacity test" is confirmed on DOI pages [E].
- **US spelling.** NWCG's "Fire Behavior Analyst" will not match rc.1's "fire behaviour analyst" unless search normalises spelling [E: repo].

### Devices and connectivity
- Phone first. On a fire assignment, intermittent satellite links. BLM bought Starlink kits for fire crews in October 2025; the vendor described remote fire sites as having little connectivity [E, vendor claim].

### Trust and distrust
- **Builds trust:** specific, task-level matches with the reason shown, and the source employer's own job title [J; DOL pilot, E].
- **Destroys trust:** generic or absurd matches, the classic translator failure [E].

### What EMST must never let them do
- Treat a match as eligibility or qualification.
- Hand an employer a score.
- Assume a USFS-to-USWFS move keeps their qualifications. That is not yet decided [E].

### Evidence strength
- **Strong** on translator failure modes and search behaviour.
- **Moderate** on fire.
- **None** on career changers using taxonomies.

**Sources:** DOL VOW §222 pilot https://www.dol.gov/sites/dolgov/files/ETA/publications/Pilot_Study_Translating_Military_Skills_to_Civilian_Employment_Acc.pdf · SHRM 2024 veterans report https://shrm-res.cloudinary.com/image/upload/v1728927785/Foundation/Research_SHRM_Research_Report_on_Recruiting_and_Hiring_Veterans.pdf · RAND RR-1919 https://www.rand.org/pubs/research_reports/RR1919.html · APPAM 2015 https://appam.confex.com/appam/2015/webprogram/Paper14325.html · SkillBridge (Military Times) https://www.militarytimes.com/news/your-military/2026/04/03/airmen-guardians-to-follow-shorter-skillbridge-transition-assistance-timeline-to-match-their-rank/ · USWFS Phase 3 https://verticalavi.org/vai-daily/us-wildland-fire-service-phase-3-advances-under-doi/ · USFS feasibility study https://www.fs.usda.gov/inside-fs/leadership/contract-awarded-fire-feasibility-study · FY2027 request https://www.taxpayer.net/disaster/administration-continues-call-for-consolidated-wildfire-agency-in-fy2027-budget-request/ · GAO-24-107382 https://www.gao.gov/products/GAO-24-107382 · BLS MLR on Marinescu & Wolthoff https://www.bls.gov/opub/mlr/2017/beyond-bls/words-pack-a-punch-in-online-job-recruiting.htm · HR Dive/Appcast https://www.hrdive.com/news/mobile-job-applications-surpassed-desktop-in-2020-report-says/595891/ · NCES PIAAC 2023 https://ies.ed.gov/learn/press-release/u-s-adults-score-par-international-average-literacy-skills-below-international-average-numeracy-and · Pew AI in hiring https://www.pewresearch.org/internet/2023/04/20/ai-in-hiring-and-evaluating-workers-what-americans-think/ · Satellite Today (BLM Starlink) https://www.satellitetoday.com/connectivity/2025/10/06/ultisat-to-provide-starlink-to-bureau-of-land-management-for-fire-program

---

## 9. U7: Researchers, data users and developers

### Context and stakes
- **Integrators use APIs heavily.** O\*NET web services have 3,500+ registered users; commercial users (1,018) match education and research (1,015) [E].
- **ESCO implementers** (Textkernel, EURES) asked for regular terminology updates, fewer duplicate skills, shorter labels, provenance documentation and grouped version cycles [E: ESCO MSWG 2019]. ESCO v1.2 was a major release (273 new concepts, 990 alternative labels); member states sent 740 comments, 518 accepted and 135 partly [E]. A 2021 ESCO user survey ran, but I found no published results.
- **Stewards change.** The Open Skills Network's OSMT and Rich Skill Descriptors moved to Credential Engine in February 2025 [E]. Credential Engine publishes frameworks as linked open data (CTDL, CTDL-ASN, via CaSS); 1EdTech's CASE serves system-to-system exchange [E]. JEDx reports only design and bridge phases (2021–2023) [E], so job-data standards look immature [J].
- **NICE Framework versioning:** semantic versions, major releases at most yearly and minor at most twice yearly, public comment on both, change logs, earlier versions kept [E].

### Jobs to be done (hypotheses)
- When I join EMST to O\*NET, OPM or my own data, I want stable IDs, a crosswalk with confidence and provenance per row, and a changelog, so my analysis is reproducible across releases. [J; ESCO needs E]
- When I cite EMST, I want a version and a DOI-like identifier, so reviewers can find exactly what I used. [J]
- When I build a product, I want a clear licence and a machine-readable bundle, so legal review is quick. [J]

### Current tools and workarounds
- O\*NET database and web services; ESCO API and downloads; Lightcast Open Skills; CTDL registry; SKOS tools; Python and R [E for O\*NET and ESCO usage; J for the rest].
- **What rc.1 already ships:** JSON-LD, CSV with a datapackage, SKOS, SSSOM and delta files. This covers much of the need [E: repo].

### Pain points
- Undocumented provenance, duplicates and version churn [E: ESCO].
- Stewardship changes [E: OSN].
- Unclear licences [J; I could not read O\*NET's licence page; I believe it is CC BY 4.0, unverified].

### Vocabulary
- persistent identifier, URI, version, semver, changelog, delta, crosswalk, mapping, SSSOM, SKOS, JSON-LD, CTDL, CTDL-ASN, CASE, RSD, O\*NET-SOC, ISCO, ESCO URI, CIP, licence (CC BY 4.0, CC0), DOI, datapackage.

### Devices and connectivity
- Desktop, scripts, CI pipelines [J].

### Trust and distrust
- **Builds trust:** checksums (rc.1 ships SHA256SUMS), visible versioning, and honest flags such as "unreviewed AI match" on every crosswalk row [J].
- **Destroys trust:** silent ID changes [J].

### What EMST must never let them do
- Publish EMST-derived scores of individuals or occupations as validated.
- Strip use-tier and review-status fields when redistributing. Make those fields mandatory in every export [J].

### Evidence strength
- **Moderate** (from comparable taxonomies); **none** from EMST users.

**Sources:** O\*NET OMB Appendix C https://www.onetcenter.org/dl_files/omb2024/AppendixC.pdf · ESCO MSWG 2019 https://esco.ec.europa.eu/system/files/2021-07/5baec5da-824d-446a-8cec-91ae5fa3eebcMSWG_9-3_Measuring_the_success_of_ESCO.pdf · ESCO v1.2 MSWG deck https://esco.ec.europa.eu/system/files/2024-04/ESCO%20MSWG_ESCO%20v1.2.%20major%20version.pdf · ESCO newsletter 2021 https://esco.ec.europa.eu/system/files/2022-11/ESCO%20newsletter_November2021.pdf · WGU on OSN transition https://wgu.edu/newsroom/press-release/2025/02/osn-transition-rich-skills.html · Credential Engine explainer https://credentialengine.org/wp-content/uploads/2024/03/CE-Explainer-CTDL-CASE-CaSS.pdf · JEDx https://uschamberfoundation.org/workforce-development/JDX · NICE revisions https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center/about/nice-framework-revisions

---

## 10. U9: Practitioners and SMEs who would review or correct the taxonomy

### Context and stakes
- **Rejecting newcomers drives contributors away.** English Wikipedia's decline came from falling retention of *good-faith* newcomers, increasingly reverted by automated tools whose users joined discussion ~7% of the time (against ~60% for manual reverters) [E: Halfaker et al. 2013].
- **Open-source newcomers face 58 barriers;** the social ones are no reply, late reply, impolite reply, a reply too advanced for a beginner, and no mentor [E: Steinmacher et al. 2015].
- **GitHub suits code better than text:** a "very steep learning curve" for text collaboration and mostly passive consumption, though Issues help non-technical users raise ideas [E: Longo & Kelley 2015].
- **Comparable institutions keep simpler routes.** NIST uses GitHub Issues with a template (account required, pseudonyms allowed) and keeps email as "the traditional way" [E]. NICE takes change requests from anyone by email, acknowledges them, and records outcomes as Noted, Accepted, Accepted with Modification, Deferred or Rejected [E]. ESCO runs invite-only expert forums across 27 sectors and ran its v1.2 consultation as a one-month spreadsheet exercise returned by email [E].
- **Expert panels work but cost effort.** DACUM needs 5–12 experts for two days [E]. One Delphi case kept 100% response over eight rounds but needed up to 15 prompts per panellist and 17 months [E: Veugelers et al. 2020; single case].

### Jobs to be done (hypotheses)
- When I see something wrong about my job, I want to flag it in under two minutes without learning a new tool, so I actually do it. [J; barrier evidence E]
- When I take part in a validation panel, I want to know my time matters, what changed because of me, and how I'm credited, so I come back. [J; "You said, we changed" idea in the internal CP plan]
- When I disagree with an AI judgment, I want my disagreement recorded even if it doesn't win, so the record shows dissent. [J; internal CP plan: practitioner feedback is recorded as a low-weight assessment]

### Current tools and workarounds
- Email, professional-society listservs, Word track changes, spreadsheets [J; ESCO uses spreadsheets, E].

### Pain points
- Needing a GitHub account [E].
- Silence after a submission [E].
- Jargon [J].
- Fear of being identified when criticising an employer [S].

### Vocabulary
- "report a problem", "suggest a change", "comment", "feedback". GitHub terms such as "issue", "pull request" and "fork" are unfamiliar to most practitioners [J; Longo & Kelley E].

### Devices and connectivity
- Mixed. Practitioners will often spot errors on a phone [J].

### Trust and distrust
- **Builds trust:** visible responses, outcome categories (the NICE model) and a published changelog [E/J].
- **Destroys trust:** unanswered issues [E].
- **A design conflict.** The brief's rule of "EMST project lead, no personal names" may discourage experts who want credit [S; test it].

### What EMST must never let them do
- Change records directly without review.
- Post personal or personnel data, or protected site locations, in public issues [J; internal pilot design flags site-location risk].
- Submit Tribal knowledge outside the Tribal process.

### Evidence strength
- **Strong** on participation barriers in general; **none** on environmental practitioners specifically.

**Sources:** Halfaker et al. summary https://meta.wikimedia.org/wiki/Research:The_Rise_and_Decline · Steinmacher et al. 2015 https://www.ime.usp.br/~gerosa/papers/CSCW_2015.pdf · Longo & Kelley 2015 https://www.OpenSym.org/os2015/proceedings-files/p503-longo.pdf · NIST GitHub user guide https://pages.nist.gov/FederalProfile-8259A/github/ · NICE change requests https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center/nice-framework-change-requests · ESCO feedback mechanism https://esco.ec.europa.eu/system/files/2021-07/2e360c35-21d7-4f80-94f8-7b6c397ebfe97_-_ESCO_feedback_mechanism_MSWG.pdf · ESCO v1.2 consultation instructions https://esco.ec.europa.eu/system/files/2023-09/Consultation%20on%20ESCOV1.2.%20-%20Instructions.pdf · Veugelers et al. 2020 https://link.springer.com/article/10.1186/s12874-020-01029-4 · Site build rules: `/home/claude/emst/site/README.md` ("no e-mail addresses or phone numbers")

---

## 11. Cross-cutting needs

1. **Translation across employers, without implying eligibility.** Seven of nine internal personas ask "what is my work called elsewhere, and does it count?". Outside evidence supports the first half (mapping is genuinely hard [E: SHRM; DOL pilot]) and warns against the second (eligibility is set by qualification standards and merit rules [E: OPM 0401 standard; CA exam bulletin]). **Need:** task-level "what this is called" plus a "what to check" list, never a verdict [J].
2. **Titles as the front door.** Search must cover official and descriptive titles, series, class, NWCG and SOC codes, corps and fire slang, and British and American spellings [E: Marinescu & Wolthoff; OPM titling memo; repo counts].
3. **AI disclosure that names the human role.** Disclosing AI use lowers trust, but third-party exposure lowers it more [E: Schilke & Reimann 2025, 13 experiments]. An "AI-generated" label cut perceived accuracy by ~2.7 points (a "False" label: 9.3) because people assume full automation; describing human involvement reduced the effect [E: Altay & Gilardi 2024, N≈5,000]. **Need:** one plain sentence on what the AI did and what people did, including that no practitioner has reviewed any record yet [J].
4. **Uncertainty with anchors.** Numeric uncertainty barely dents trust; verbal uncertainty dents it more [E: van der Bles et al. 2020, N=5,780]. Verbal probability terms drift towards 50% unless numeric ranges sit beside them [E: Budescu et al. 2014, 24 countries]. **Need:** short definitions of each use tier and "Assessment pending", with "you may / you may not" examples on the same screen [J].
5. **Plain language on a phone.** 28% of adults at or below Level 1 literacy; 15% smartphone-dependent [E].
6. **Self-assessment starts a conversation; it does not measure.** Corrected r ≈ .34 [E: Sitzmann 2010]. The gap check should prompt evidence and a supervisor conversation [J].
7. **Scepticism about skills-based promises.** Fewer than 1 in 700 hires benefited; 3.6% of roles at large firms dropped a degree requirement (2014–2023); 37% of adopting firms followed through [E: HBS/BGI via HR Dive]. Colorado's numbers did not move [E].
8. **Method transparency.** Competency models fail when undocumented or used for unplanned purposes [E: SHRM–SIOP]; HR practitioners follow best practice unevenly [E: Loftis 2017, n≈328].
9. **Stability and versioning.** Dated releases and change logs (NICE, ESCO), because series and classes move through 2027 [E].

**Sources:** Schilke & Reimann 2025 https://ideas.repec.org/a/eee/jobhdp/v188y2025ics0749597825000172.html · Altay & Gilardi 2024 https://academic.oup.com/pnasnexus/article/3/10/pgae403/7795946 · van der Bles et al. 2020 https://research.rug.nl/en/publications/the-effects-of-communicating-uncertainty-on-public-trust-in-facts/ · Budescu et al. 2014 https://link.springer.com/10.1038/nclimate2194 · HBS/Burning Glass Institute (HR Dive summary) https://www.hrdive.com/news/employers-failing-at-skills-based-hiring/707897/ and report https://www.burningglassinstitute.org/s/Skills-Based-Hiring-02122024-vF-srmp.pdf · Loftis 2017 https://jewlscholar.mtsu.edu/items/88525b8d-8879-4b92-9b31-7093aff5ae79/full · SHRM–SIOP https://www.siop.org/wp-content/uploads/2024/07/SHRM-SIOP_Competency_Modeling_Documentation.pdf

---

## 12. Contradictions and tensions between groups

| # | Tension | Groups | Evidence | Design implication [J] |
|---|---|---|---|---|
| T1 | HR wants defensible, validated, job-analysis-ready content, but EMST has nothing at the develop or select tier | U5, U4 vs constraint 2 | Merit Hiring Plan rules [E]; rc.1 tier counts [E: brief] | Tell HR plainly what they *can* use now (describe-tier reference language, with sources). Do not offer assessment builders. |
| T2 | Job seekers want "do I qualify?" but EMST must not judge eligibility | U8, U2 vs U5, U4 | Translator failures [E]; qualification standards [E] | Show matches with reasons and a "check with the employer's rules" list. |
| T3 | Educators and researchers want stability; the taxonomy is a churning draft | U6, U7 | ESCO and NICE versioning [E] | Semantic versions, a deprecation policy and a stable-ID promise, even while content is draft. |
| T4 | HR needs legal caveats; U2 and U8 need plain, short text | U5 vs U2, U8 | PIAAC [E]; SHRM–SIOP [E] | Layered disclosure: one plain line, with detail on demand. Show the HR disclaimer only on HR pages, as the site already does. |
| T5 | Contributors want an easy channel and credit; the brief requires GitHub and no names, and the site forbids email addresses | U9 vs constraint 7 | Halfaker; Steinmacher; NIST email fallback [E]; site README [E: repo] | Decision for the project lead: a non-GitHub route and an opt-in credit policy. |
| T6 | NGO leads want quick wins; federal users want federal rigour | U1 vs U5 | Internal CP risk; NGO capacity [E] | Separate paths; do not load NGO screens with OPM detail. |
| T7 | Supervisors and planners want team views; workers and unions fear ranking | U3, U5 vs U2, worker reps | Internal "Sam" persona; brief | Aggregate-only team views with a minimum cell size and no names. |
| T8 | Federal HR works inside USA Staffing and USA Class; EMST is a separate site | U5 | USA Class [E] | Offer copy-and-paste and import-friendly outputs (plain text, CSV) rather than a parallel PD tool. |
| T9 | US users and official titles use American spelling; EMST uses British in places | all | Repo counts [E]; NWCG titles [J] | Normalise spellings in search. Consider American spelling for US labels. |
| T10 | Field-based users are offline and on phones; the gap check saves a file | U2, U3 | Pew [E]; vendor claim on fire connectivity [E] | Test file save and reopen on iOS and Android. Consider printable output. |
| T11 | Fire users need answers about USWFS now; policy is unsettled until 2027 | U8 | Feasibility study due 15 Feb 2027 [E] | Show "undecided as of [date]" rather than guess. |

---

## 13. Internal hypotheses compared with outside evidence

| Internal hypothesis (file) | Outside evidence | Verdict |
|---|---|---|
| Self-assessment questionnaires may not rate or rank after 30 September 2025 (hr_use_cases) | OPM guidance, Feb 2026 [E] | **Supported** |
| 91% self-report only in FY2025; 15% of agencies have I-O psychologists (hr_use_cases) | Chance to Compete report [E] | **Supported** |
| USA Hire expanded to 412 series in March 2026 (hr_use_cases) | OPM pages give 135 series (May 2025 appendix) and "all GS series" by January 2026 [E] | **Unreconciled** |
| EMST should fill the technical-assessment gap (hr_use_cases, workflow b) | The need is real [E], but rc.1 has no select-tier records [E: brief] | **Need supported; EMST cannot meet it now** |
| PD drafting workflow (a) and PD skeleton export (hr_use_cases; mvp_spec) | USA Class does AI PD drafting inside USA Staffing [E] | **Silent on USA Class — major gap**; reposition |
| 0455 realigned to 0404 (ngo_pilot_design) | OPM memo, April 2026 [E] | **Supported** |
| Fire staffing 10,496 against an 11,300 goal (personas) | 11,550 seasonals in June 2026, above goal [E] | **Outdated for 2026** |
| USWFS created; USFS fire not moved (learning-curriculum report; personas) | SO 3448; feasibility study due February 2027 [E] | **Supported** |
| No published corps alumni-outcome data (personas, "Jordan") | RTI/NPF 2024 evaluation [E] | **Contradicted** |
| AmeriCorps litigation runs into 2027 (personas; ngo_pilot_design) | Settlement of 10 September 2026; paused to 1 February 2027 [E] | **Supported, now clarified** |
| Corps noncompetitive eligibility unverified (personas) | RAP gives 2-year eligibility; TCN says 960 hours plus associate degree [E] | **Partly resolved** (RAP only; PLC not checked) |
| Colorado: 80% of classes rewritten, non-degree hires flat at 25% (personas) | CPR [E] | **Supported** |
| Maryland and Pennsylvania track applicants, not hires (personas) | CPR agrees; NGA/Lightcast reports about 60% of PA new hires without a degree [E] | **Contested** |
| "Enter by role, not by taxonomy" (product_strategy) | Title-first search [E]; OPM titling memo [E] | **Supported** |
| U7 is served by data, not the UI (product_strategy) | O\*NET web-services usage [E] | **Supported** |
| Small NGOs lack capacity, rated high risk (ngo_pilot_design) | Bridgespan; Careers in Nonprofits [E] | **Supported** |
| Mentor and evaluator capacity is the binding constraint (learning-curriculum report) | USFS lost about 6,000 permanent staff, including red-card holders [E] | **Indirectly supported** |
| "Challenge this" via GitHub *or email* (user_research_plan, T8) | NIST keeps email [E], but the site build forbids email addresses [E: repo] | **Conflicts with site rules** |
| Translation is the common need (personas; learning-curriculum report) | SHRM 58%; DOL pilot needed task-level matching plus SME review [E] | **Supported, with a warning** against title-to-title translation |

The internal documents are silent on USA Class, the 7,600 HR departures, reading level and smartphone dependence, and the AI-disclosure penalty.

---

## 14. Unknowns, ranked by risk, to validate with real people

| Rank | Unknown | Why it is risky | Suggested method [J] |
|---|---|---|---|
| 1 | Do users read use tiers, "Assessment pending" and "AI draft, not reviewed" correctly, and do they still act on draft content? | Misuse in hiring or classification, or total distrust | Scenario comprehension probes (like internal T3), 20–30 participants across U2, U3, U5 and U8. A/B test two disclosure wordings, one of which names the human role. Measure over-reliance. |
| 2 | Is there any slot for EMST in federal and state HR work beside USA Class, USA Staffing and consultants? | U5 and U4 may never adopt | Contextual inquiry with 6–8 federal and 6–8 state HR staff, walking through their last PD or class study (PRA-aware: direct observation). |
| 3 | What words do people type to find their job? | Search fails, so the site fails | Collect titles from 200–300 real postings (USAJOBS, state, corps boards) as desk work. Then run first-click and search tests with 30+ people, and open card sorts. |
| 4 | Does the gap check work on phones, in the field and offline, and does the saved file get reused? | Core U2 and U3 feature unused | In-season diary study (2–3 weeks), plus a device lab test of save and reopen on iOS and Android. |
| 5 | Will the "what it's called elsewhere" view mislead people about eligibility? | Repeats the translator failure; harm to job seekers | Task-based usability with veterans and seasonal firefighters. Measure false "I qualify" conclusions. |
| 6 | Will SMEs submit corrections, and through what channel? | Taxonomy stays unreviewed | A concierge experiment with 10–15 SMEs comparing a GitHub Issue form with an alternative channel. Measure completion, time and drop-off. |
| 7 | Do workers and unions see team views and gap data as surveillance? | Reputational and legal risk | Interviews with worker representatives, plus a misuse red-team workshop. |
| 8 | Is EMST's grain usable for curriculum mapping, and is AI drafting acceptable to faculty? | U6 rejects it | Mapping workshop with 2–3 programmes, comparing EMST with a DACUM chart. |
| 9 | Are IDs, licence, deltas and crosswalk provenance enough for integrators? | U7 forks or abandons | 5–8 developer interviews, plus a "join EMST to O\*NET in 30 minutes" task. |
| 10 | Can assistive-technology users and low-literacy users complete core tasks? | WCAG release gate; equity | Sessions with at least 2 AT users per round; readability checks on key pages. |

**What would settle the largest speculations:**
- Whether federal networks block GitHub [S]: ask 5–6 federal users.
- Whether experts want named credit [S]: one question in SME recruitment.
- How far field crews lack coverage [S]: diary study or field visit.
