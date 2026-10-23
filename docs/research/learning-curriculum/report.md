# Learning & Curriculum Design: Making EMST Usable for Learners, Instructors and Programs

**Role:** Learning & Curriculum Design Strategist (LC) · **Phase:** 2 · **Date:** 2026-10-23
**Evidence labels:** [E] evidence from a source I read (IDs in `sources.csv`) · [J] my professional judgment, with its basis · [S] speculation, with what would confirm it.
**Lanes referenced:** IO (assessment and validity), CM (mobility), IA (credential data standards and NLP), FH/SL (federal and state classification), FC/DC/SC (crafts), DB (subsector coverage), TN (Tribal protocol), CP (privacy and accessibility), AS (adoption).

---

## 1. Summary

1. **Learners and instructors need a learning unit that EMST does not yet publish: one competency at one level, written as observable outcomes with conditions and criteria.** I call it a competency-level outcome (CLO). Accreditors already work at this grain:
   - SAF states each minimum competency as one capability at one depth ("knowledge of", "an understanding of", "an ability to").
   - SAF programs map courses to competencies on an Introduce / Reinforce / Emphasize-Apply scale [E: LC-001].

   EMST v1 has the raw material (222 competencies, 888 level rows, 4,852 indicators), but not in usable form:
   - 63% of the knowledge statements start with unobservable verbs ("Understands", "Expert in", "Shapes").
   - Only 5.8% of indicators state a criterion or standard.
   - 82% of competencies with parsed expert indicators include "Publishes…" at the top level [E: LC-031].

2. **The best v1 content for learning is Domain 7.2** (validating AI outputs, calibrating judgment, designing formation workflows). It is observable, conditional and includes escalation behavior. It should be the writing model for v2 and the basis of the first pathway to build: an AI and data-practice baseline for all staff (LC-PW-06) [J].

3. **A pathway is the gap between a verified current profile and a target role profile, not a family profile.** CM's analysis shows that a forester (F1) lacks 23 of the data-science family's (F7) core competencies. A reskilling pathway into a remote-sensing role needs about 8 of them, at specific levels [E: LC-037; J]. This is why the role layer CA proposes (L3) is a prerequisite for pathway work.

4. **Career-ladder destruction (CLD) signals translate directly into learning design.** Entry tasks that v1 tags as human-essential with high tacit density need supervised repetitions. Entry tasks tagged compressive or substituted need a "by-hand quota" before learners move to a review-and-certify role. Every data- or AI-heavy pathway needs a field ground-truth component and a statecraft accountability component [J; rules R6–R7 in `pathway_template.md`].

5. **Accreditation coverage is a practical test of EMST's reach beyond public lands, and it fails outside forestry.** Of the content criteria I mapped:
   - SAF: 29 of 50 fully covered by v1.
   - ABET environmental engineering program criteria: 1 of 6.
   - EHAC environmental health: 2 of 5.
   - NAAEE: 1 of 6.

   v1 has no tree or plant identification competency (which SAF requires), and nothing on water/wastewater treatment operations, epidemiology, food protection or vector control (which EHAC requires) [E: LC-001, LC-002, LC-005, LC-031; `accreditation_emst_crosswalk.csv`].

6. **Credentials should be issued at bundle grain**: 3–8 CLOs that make up one work function, aligned to EMST IDs through Open Badges 3.0 and CLR 2.0.
   - Per-CLO badges would add noise to a market that already holds 1,850,034 credentials, 1,022,028 of them badges [E: LC-016, LC-017].
   - Stacking short credentials shows modest positive returns, though the evidence is not specific to the environmental sector [E: LC-018].

7. **New federal funding rules make short environmental-technician programs fundable if they are designed for it.**
   - Workforce Pell (final rule 2026-05-19): 150–599 clock hours, at least 8 and fewer than 15 weeks, 70% completion and 70% placement, a value-added-earnings test, and governor approval [E: LC-019, LC-021].
   - DOL Circular 2026-04 lets Registered Apprenticeship related instruction use Workforce Pell, with up to 49% of instruction delivered by an ineligible provider such as the employer or sponsor [E: LC-020].
   - EO 14278 set a goal of 1 million new active apprentices [E: LC-022].

8. **The binding constraint on good pathways is likely evaluator and mentor capacity, not course seats.** Performance-based formation, as in NWCG position task books, needs qualified people to observe and sign off. Federal staffing fell sharply in 2025–26 [E for staffing declines: LC-028; J for the effect]. EMST has no competency for the people who run that formation (candidates LC-C-01 and LC-C-02).

**Biggest trade-off.** Faster, AI-assisted pathways reduce time-to-productivity. Formation rules (by-hand quotas, field calibration, supervised repetitions) make pathways longer and consume scarce mentor time, but they are what keep judgment forming in the next generation. I recommend paying that cost and measuring it (§10).

---

## 2. Scope, method and limits

**What I did.**
- Read `CHARTER.md`, `TEAM_BRIEF.md`, CA's audit and architecture hypotheses [LC-050, LC-051], and the relevant v1 docs [LC-032–LC-036, LC-052].
- Read the full SAF Accreditation Handbook (2024), 90 pages [LC-001].
- Analyzed the v1 baseline quantitatively (`scripts/v1_lo_analysis.py`).
- Used CM's transferability outputs [LC-037] and the sister repo's verified permitting research [LC-030].
- Ran about 16 web searches and about 30 deep reads of web documents.

**Limits, stated plainly.**
- **The team's shared web-search budget ran out early in my work.** After that, WebFetch was limited to URLs already surfaced in the conversation, and several primary URLs were refused:
  - the O*NET OnLine CIP crosswalk;
  - the NWCG PMS 310-1 page;
  - the AI-tutoring papers in *Scientific Reports* and *PNAS*.
  - Consequences:
    - **The official CIP 2020–SOC 2018 mapping table was not retrieved.** Every row in `cip_soc_env_crosswalk.csv` carries `nces_check=verify` [LC-013].
    - **AI-enabled learning evidence, conservation-corps and AmeriCorps funding status, and federal training institutions** (NCTC, DOI University, EPA's training institutes APTI and NETI, ITEP, ARSET) **are from prior knowledge, labeled [J] or [S], and marked `unverified`.** I could not check 2025–26 changes to AmeriCorps and corps funding. That is a gap CM or AS should close.
  - The searches the team can run next are listed in §12.
- **SOC 2018 codes and titles** in the crosswalk and in my corrections to v1 are entered from professional knowledge [LC-038, unverified]. CA reached the same doubts about v1's mappings independently [E: LC-050 §6].
- **Third-party accreditation text is paraphrased, not copied.** Criterion IDs follow each accreditor's numbering so readers can check the authoritative wording.

**Sources I chose and why.**
- Accreditors' own documents (SAF, ABET, AAEES, EHAC, NAAEE) over summaries, because accreditors decide what programs must evidence.
- Federal primary texts (EO 14278, SO 3448, DOL Circular 2026-04, USFS testimony) for policy status.
- One peer-reviewed causal-leaning study on stackable credentials [LC-018] rather than advocacy claims.

**Named sources that turned out outdated.**
- NAAEE's 2019 professional-development guidelines are superseded by its 2025 *Environmental Educator Knowledge and Skills* guidelines [E: LC-008], which I could not read.
- "NCSE" is now the Global Council for Science and the Environment (GCSE) [E: LC-011].
- The IES curriculum census [LC-010] uses 2012 data.

---

## 3. What a learner and an instructor need from EMST

**A learner** (a new hire, a reskilling technician, a federal employee in transition) needs five things:
1. **A translation of what they already have** (job history, quals, credentials) into EMST competency-levels, backed by evidence. Without this, the system wastes the learner's time re-teaching what they know (template R10).
2. **A target** expressed as a role profile, plus the gap. "You need 7.2.1 at Intermediate and 2.1.2 at Intermediate" is actionable. "Join family F7" is not.
3. **For each gap: what good performance looks like** (observable outcomes and examples), where to learn it (`training_providers_register.csv`), how it will be assessed, and what recognition follows.
4. **A portable record** of what they have demonstrated: CLR 2.0 or Open Badges 3.0, aligned to EMST IDs, so a second employer can read it [E that the standards support alignment: LC-015, LC-016].
5. **Durability signals** showing which competencies are stable and which are changing, so they invest wisely. The v1 stability tier is rule-determined and should be replaced with computed change indicators [E: LC-050 §11].

**An instructor or training officer** needs eight things:
1. Level descriptors that are about autonomy and complexity, not tenure (§5.3).
2. Outcome statements with conditions and criteria, plus a bank of performance examples (indicators).
3. Assessment blueprints and rubrics, owned by IO, with the context each competency must be assessed in (field, data/desk, stakeholder, legal-administrative, incident).
4. A curriculum-map format that also satisfies accreditors. SAF's Education Summary uses Introduce / Reinforce / Emphasize-Apply, so EMST should too [E: LC-001 Section III].
5. Authentic cases across sector actors. v1's 1,110 sector notes average 6.2 words, too thin to teach from [E: LC-031].
6. Tool training kept separate from competency, with expiry dates (CA's R-4).
7. Change notices when the taxonomy or the law moves. v1's NEPA indicators still cite CEQ regulations that were removed in January 2026 [E: LC-030].
8. Demand data showing which competencies employers and plans need (LM's demand-signal work).

---

## 4. Landscape (verified as of 2026-10-23 unless labeled)

### 4.1 Program and occupation classifications

- **CIP 2020 and the CIP–SOC crosswalk.** The 2020 NCES/BLS guidelines are the authoritative statement of method [E: LC-012]. A mapping requires a *direct* relationship: the program teaches knowledge and skills directly applicable to the occupation and meets its entry or licensure requirements. The guidelines warn against several uses:
  - treating the crosswalk as a record of graduates' actual outcomes;
  - assuming every completer qualifies for every mapped job;
  - counting associate-level completers as supply for bachelor's-level occupations.

  Those warnings matter for EMST: a CIP→SOC→EMST crosswalk is a *design* artifact, not a supply measure [J].
- **SOC 2028.** BLS's revision page (modified 2026-09-30) says the committee is still reviewing input from the first notice (June 2024), with a second notice "TBD" and a final structure planned for 2027 [E: LC-014]. The page mentions no environmental or green occupations and no CIP–SOC update. EMST's crosswalk layer must be versioned to absorb SOC 2028 [J]. A second-notice comment period would be an opportunity to argue for codes such as remote-sensing technicians or wildland fire [S].
- **The v1 family→SOC table has errors that matter for curriculum.**
  - 19-1012 is labeled "Farm & Home Mgmt Educators"; 19-1012 is Food Scientists.
  - 33-1021 is labeled "Fire Inspectors"; 33-1021 is supervisors of firefighting.
  - Environmental health is mapped to a health-information code.
  - 19-2041 Environmental Scientists and Specialists, the largest environmental-science SOC occupation, is missing.

  [J on SOC titles, LC-038 unverified; CA independently flags the same, LC-050 §6.] `cip_soc_env_crosswalk.csv` replaces that table with 97 CIP→SOC rows covering 47 CIP codes. Each row carries v1 families, computed v1 domains, and a pathway or accreditor note.

### 4.2 Accreditation

- **SAF (Accreditation Handbook, revised 2024; standards 2021; procedures accepted 2024-08-02)** [E: LC-001]. Four standards: Forest Technology, Forestry, NREM, Urban Forestry. Five criteria each: purpose and learning outcomes; administration; faculty; curriculum; student development. Features that matter for EMST:
  - Programs publish **5–9 program learning outcomes** linked to curriculum competencies (C1-1, C1-2).
  - **Syllabi must state course learning outcomes** (C4-2).
  - Courses must be **sequentially integrated** (C4-4).
  - **Integrative components** (communication, critical reasoning, systems connections, professional behavior and safety, ethics) are developed across the curriculum (C4-5 to C4-9).
  - **Disciplinary minimum competencies** are written in three tiers: knowledge / understanding / ability.
  - One requirement is the clearest accreditation hook for EMST 7.2.1: graduates must use contemporary technology *and recognize when application results fall outside a reasonable range* (Forestry C4-B.2; Forest Technology C4-B.6).
  - **Transfer credit** may be granted for "work/life experience" when faculty judge it equivalent to course outcomes (C2-6). This is the opening for recognition of prior learning.
  - Programs must **facilitate internships or work experience** (C5-5).
  - Self-evaluation uses an **Education Summary workbook** mapping courses to competency areas on the I/R/E scale (Section III).
  - SAF also requires Forest Technology graduates to navigate *without battery-powered devices* (C4-B.5 guidance). EMST should keep that durable field skill.
- **ABET EAC, 2026–27** [E: LC-002, LC-003].
  - The general student outcomes 1–7 include outcome 7, acquiring and applying new knowledge, which has no EMST counterpart.
  - Environmental Engineering program criteria require math and sciences; material and energy balances; fate and transport across air, water and soil; hands-on labs in more than one focus area; design considering risk, uncertainty, sustainability and life cycle; and professional practice and regulatory roles.
  - Proposed changes for 2027–28 reviews add interactions with biota, computational tools in design, and economics and ethics.
  - Separate Ecological Engineering criteria exist.
- **ABET ETAC Environmental Engineering Technology** [E: LC-004].
  - Associate-level topics: field and lab measurement; permit applications and reports; QC and basic statistics; professional practice; regulatory roles; unit-process operation.
  - Baccalaureate adds risk analysis and unit-process design.
  - This tier is the best fit for state technician roles.
- **EHAC (requirements in force July 2025)** [E: LC-005].
  - Separate courses in epidemiology, statistics and toxicology.
  - Cross-cutting areas: risk; management; administrative law; environmental justice.
  - Technical List 1 (required exposure): air, food protection, occupational health, solid and hazardous waste, water and wastewater, zoonotic and vector-borne disease.
  - At least a **180-hour practicum**.
- **NAAEE** [E: LC-007, LC-008, LC-009]. NAAEE accredits state environmental-education certification programs, which must be criteria-based. The core competencies adopted in 2006 have six themes. The 2025 guidelines replace the 2019 professional-development guidelines, and the crosswalk should be redone against the 2025 text.
- **Interdisciplinary environmental and sustainability programs have no specialized accreditor.**
  - GCSE's 2013 census rated systems thinking, technical communication, field and lab research, collaboration and informatics as the most important undergraduate skills [E: LC-010; 2012 data].
  - A 2024 scan of 100 institutions found 91 with sustainability-related programs, mostly framed by the Wiek/Brundiers key competencies, and found that career pathways are unclear to students [E: LC-011, low quality].
  - These programs are where an EMST map adds the most value, because nothing else structures their outcomes for employers [J].

**Coverage test** (`accreditation_emst_crosswalk.csv`, 73 rows; 69 content and 4 process). The fully-covered counts below are the totals reported in §1 point 5.

| Accreditor | Content criteria mapped | Full | Partial | None |
|---|---|---|---|---|
| SAF (four standards) | 50 | 29 | 15 | 6 |
| ABET EAC (EnvE + SO-7) | 6 | 1 | 5 | 0 |
| ABET ETAC (EnvET) | 2 | 0 | 2 | 0 |
| EHAC | 5 | 2 | 3 | 0 |
| NAAEE | 6 | 1 | 5 | 0 |

The pattern matches the brief's finding that v1 skews to public lands and forestry. It also gives DB a concrete, accreditor-anchored list of gaps:
- tree and plant identification (SAF);
- forest operations, wood products and scaling (SAF);
- forest certification (SAF);
- fate and transport and treatment design (ABET);
- treatment operations (ETAC, EHAC);
- epidemiology, food protection, vector control (EHAC).

### 4.3 Credentials and records

- **Open Badges 3.0** became final on 2024-05-29. It is built on W3C Verifiable Credentials, supports alignment to skills frameworks and competencies, and embeds criteria and evidence [E: LC-016].
- **CLR 2.0**, developed alongside it, packages many achievements with their alignments. **CASE** publishes frameworks with identifiers that credentials can reference. **LER-RS** (HR Open) links records to hiring systems [E: LC-015].
- IA owns the data-model choice. From the learning side, the requirement is simple: every EMST CLO and bundle needs a stable URI that a badge's alignment field can point to, and the version must travel with it [J].
- **Market noise.** Credential Engine counts 1,850,034 U.S. credentials: 264,099 degrees, 486,352 certificates (apprenticeships are counted here), 1,022,028 badges, 3,384 micro-credentials, 14,331 licenses and 6,892 certifications [E: LC-017].
- **Stacking evidence.** In Virginia administrative data, stacking community-college credentials raised employment about 4 percentage points and quarterly wages about 4%. Returns were larger for people who return after a short certificate [E: LC-018; health-heavy, not environmental].
- **Workforce Pell** (final rule dated 2026-05-19, effective 2026-07-20) [E: LC-019, LC-021]:
  - 150–599 clock hours, at least 8 and fewer than 15 weeks;
  - 70% completion and 70% placement;
  - tuition no higher than value-added earnings;
  - governor approval with workforce-board consultation;
  - academic credit toward a certificate or degree;
  - at most 25% of a program delivered by ineligible providers (up to 49% for Registered Apprenticeship).

  The rules leave open how competency-based or field-heavy hybrid programs fit the clock-hour framework [E: LC-021]. That uncertainty matters for field programs [J].

### 4.4 Registered Apprenticeship

- **Policy.** EO 14278 (2025-04-23) directs a plan to "reach and surpass 1 million new active apprentices", expansion to new occupations, and a review of workforce programs that includes AI upskilling and alternative credentials [E: LC-022].
- **RA and Pell.** DOL Circular 2026-04 (2026-09-08) explains how sponsors can use Workforce Pell for related instruction [E: LC-020]:
  - governor in-demand determinations are automatically met;
  - on-the-job learning can count up to 49% under written agreements;
  - RA completion certificates are portable but not always stackable.
- **Water is the clearest environmental case.** NRWA runs registered apprenticeships through state affiliates, typically about 2 years [E: LC-025, LC-024]. Since September 2025 it has awarded EPA-funded apprentice and mentor stipends ($1.45 million by March 2026) [E: LC-023].
- **Elsewhere the evidence is thinner.** I found no verified registered apprenticeship for environmental technicians, remote-sensing technicians or environmental-health specialists this session [J: absence of evidence in my limited search]. These are candidates for EMST-aligned work-process schedules (P-LC-10).
- **Fire is a different model.** Wildland fire runs on NWCG's interagency qualification system, not RA (§4.6).

### 4.5 Conservation corps

Corps are a primary paid entry pathway into land-management work, and v1's structural analysis treats entry pipelines as fragile [J: LC-034]. **I could not verify the 2025–26 status of AmeriCorps and corps funding** (search budget exhausted). This must be checked before the pathways treat corps as a reliable feeder. The register entries (TP-029, LC-E-24) are marked [S].

### 4.6 Federal and state training institutions

- **NWCG** is the strongest performance-based qualification model in the sector [J: LC-033; the PMS 310-1 page was blocked, LC-044]:
  - minimum training, experience, fitness and currency;
  - position task books that list tasks, require *observed* performance, and require evaluation in the right context (wildfire tasks on wildfires).
  - It is "professionalization without licensure" [J: LC-034].

  EMST should borrow its evidence pattern (template R5), not its incident-bound scope.
- **The U.S. Wildland Fire Service (USWFS).** DOI Secretarial Order 3448 (January 2026) consolidates the BIA, BLM, NPS and FWS fire programs, plus the Office of Wildland Fire and the Office of Aviation Services. It directs the Department to *"establish an integrated wildland fire intelligence and data capability"* [E: LC-026]. The Forest Service's fire program did not move; the Senate asked for a feasibility study [E: LC-027, LC-028]. The new chief's stated priority is training the next generation of incident-management-team members [E: LC-028].
- **USDA Forest Service.** The FS is reorganizing: headquarters to Salt Lake City, state-based leadership, operations service centers, unified research, and consolidation of support functions with USWFS. It reports 571 Good Neighbor agreements across 39 states [E: LC-029]. Federal–state training partnerships will run through a changing organization [J].
- **Other federal institutions (unverified this session).** FWS NCTC, DOI University, NPS and BLM training centers, EPA's APTI, NETI and Watershed Academy, NASA ARSET, and ITEP (for Tribal environmental professionals) appear in the register from prior knowledge. Their 2026 offerings and capacity after reorganizations were not checked. Engagement with ITEP or any Tribal program must go through TN's protocol.
- **State training** is highly variable: agency academies, operator certification boards, inspector delegation. This is SL's lane. I list generic rows only.

### 4.7 AI-enabled learning: evidence status

I could not read the key recent studies this session. What I recall, labeled [S] until re-read:
- A small randomized trial in an undergraduate physics course found a carefully designed AI tutor outperformed in-class active learning [LC-041].
- A large field experiment in high-school mathematics found that unguarded generative-AI help raised practice scores but lowered later unassisted performance. A tutor-style version with guardrails mitigated the harm [LC-042].
- Simulation-based learning has meta-analytic support in higher education [LC-043].

None of these is environmental. The design implications I draw are [J]:
1. AI tutors are a reasonable mode for knowledge outcomes and adaptive practice.
2. Unguarded AI assistance during *formation* is a risk. Hence the by-hand quotas.
3. The most valuable AI-enabled mode for this sector is the **seeded-error validation drill**. The learner reviews AI or tool output with known errors, and detection and the documented rationale are scored. It trains exactly the competency (7.2.1) that accreditors (SAF C4-B.2) and agencies (CEQ's oversight emphasis) now require.

Public corpora such as PNNL's DraftNEPABench (102 EIS drafting tasks across 19 agencies) can seed drill banks [E: LC-030]. Immersive simulation is seen in v1 sources as a training accelerant for fire rather than an operational replacement [J: LC-033].

---

## 5. How useful is v1 for curriculum work?

The analysis is reproducible with `scripts/v1_lo_analysis.py` on `data/v1_baseline/`. Verdicts are in `v1_assessment.csv` (30 rows).

### 5.1 Proficiency statements as learning outcomes

- **Knowledge statements: change.**
  - 563 of 888 (63.4%) begin with non-observable leads.
  - By level: Foundational "Understands" 170; Advanced "Expert in" 189 (a level-label collision, LC-050); Expert "Shapes" 189 [E: LC-031].
  - Intermediate ("Applies…") is fine.
- **Application statements: carry.** 99% start with an action verb (Supports, Conducts, Designs, Leads). They work as one-line level summaries once the Expert rows are rewritten [E].
- **Domain 5 (30 competencies, 120 rows) is misparsed.** The knowledge and application text sits in indicator cells, so D5 has no usable indicators. Ironically, the misparsed D5 text is among the best-written: it uses autonomy cues such as "with supervision" and "Independently". Repair it, do not discard it [E: LC-031; DE lane].

### 5.2 Indicators as outcome seeds

- **Foundational and Intermediate indicators: carry as seeds.** They are mostly action verbs; Apply-band verbs account for about 37–38% of rows.
  - Only 282 of 4,852 (5.8%) state any criterion or standard.
  - Only 25 state supervision or independence.

  Every outcome derived from them needs a condition and a criterion added (template R2) [E].
- **Advanced indicators** often read as position duties ("Develops agency NEPA procedures"). They are good for role profiles and capstones, weak as course outcomes [J].
- **Expert indicators are academically biased.** 158 of the 192 competencies with parsed expert indicators (82%) include a "Publishes…" indicator. "Influences" and "Recognized" are also common [E]. A practitioner who becomes a recognized agency or field authority without publishing is mis-described. Expert should be *recognized* through evidence, never taught [J].
- **About 27 indicators, mostly in D4, are credentials or course completions, not behaviors.** Examples: S-130/S-190, RXB2, FAA Part 107, HAZWOPER levels, WFR, CDL, ISA [E].
  - For learning purposes they belong in an evidence-equivalence register (P-LC-07), not in indicators.
  - The 4.4.4 HAZWOPER rows appear to mix site-worker training hours with emergency-response levels. Verify against 29 CFR 1910.120 [J; LC-039 unverified].
- **Date-sensitive names should move to the tools and standards layer** with dates. Examples: 6.1.4 citing CEQ regulations; 6.7.2 naming EJ screening tools; 7.1.3 citing "NEPA scientific integrity requirements" [J; E for CEQ: LC-030].

### 5.3 Levels

v1 levels are tenure bands (0–2, 3–5, 6–10, 10+ years). For curriculum this is the single most consequential defect: a competency-based pathway cannot target "6–10 years" [J; consistent with LC-050 §4.3]. The template uses responsibility-based descriptors (Foundational, Intermediate, Advanced; Expert recognized only), with years kept as a typical-time note. IO owns validation and the number of levels.

### 5.4 Tasks, sector notes and analytical layers

- **Tasks (666): carry.** They are the natural unit for work samples, task books and simulations [J; CA agrees they are real tasks, LC-050 §4.2]. Add an explicit typical-level field per task.
- **Sector application notes: change.** At a mean of 6.2 words, they are context labels, not cases. Expand them into short scenario prompts per sector actor [E: LC-031].
- **Task 13 exposure tags: carry for design use.** Automation type, tacit density and career-ladder position directly drive work-based-learning share and by-hand quotas. Pending IO's inter-rater reliability study, they are design prompts, not funding rules [J].
- **Stability tier: change.** CA finds it is rule-determined [E: LC-050 §11]. Credential currency should instead follow computed change velocity or lifecycle status.
- **D7.2 (7.2.1–7.2.3): carry as the writing model.** 7.2.2, "Designing workflows for tacit knowledge formation", is the competency supervisors and training officers need to turn CLD signals into practice.

### 5.5 Coverage for curriculum use

Accreditor-required content absent from v1 is listed in §4.2. Separately, there is **no workforce-learning competency** at all: no "task book", "evaluator" or "prior learning" anywhere in v1. Mentoring appears only inside 43 indicators [E: LC-031]. These lead to candidates LC-C-01 and LC-C-02. v1's 5.4.2 "Curriculum design for environmental education" targets public education, not workforce learning.

---

## 6. Academic alignment method

### 6.1 Steps (with IA's NLP pipeline)

1. **Ingest.**
   - Program learning outcomes (PLOs), course learning outcomes (CLOs in the academic sense) and syllabi.
   - Where available, the program's accreditation Education Summary (SAF) or student-outcome mapping (ABET).
   - Prefer CASE packages when institutions publish them [J; IA lane].
2. **Candidate retrieval (IA).**
   - For each outcome statement, retrieve candidate EMST competency-levels by semantic similarity to competency descriptions, tasks and indicators.
   - Classify the *level* from the verb, the condition and the scope. Use the template's verb bands and SAF's knowledge / understanding / ability tiers as features.
   - Record match type (exact, close, broad, narrow, related) and confidence [J].
3. **Human review.** A faculty member and a practitioner review low-confidence matches and every claimed Intermediate-or-above match. Use a gold set of 3–5 programs per accreditor, double-coded, to measure agreement before scaling. IO and IA set the agreement statistic.
4. **Assign I/R/E per course.** The program marks Introduce, Reinforce or Emphasize-Apply for each mapped CLO, reusing SAF's scale [E: LC-001] so one map serves both purposes.
5. **Produce four outputs for the program:**
   - (a) a coverage heatmap of CLO × course;
   - (b) a sequence check: is each CLO introduced before it is applied? (SAF C4-4);
   - (c) a gap list against target role profiles and demand signals (LM's plan and posting data);
   - (d) an accreditation-ready table that cites the accreditor's criterion IDs via `accreditation_emst_crosswalk.csv`.
6. **Version and publish.** Pin the EMST version and the accreditor-standard version. Re-run when either changes.

### 6.2 What programs need

| Need | Universities | Community and technical colleges |
|---|---|---|
| Show employers what graduates can do | Map PLOs to role profiles for internships and placement | Map certificates to entry roles for hiring agreements |
| Accreditation evidence | Reuse the EMST map in SAF, ABET or EHAC self-studies | ETAC; SAF Forest Technology |
| Funding eligibility | — | Workforce Pell: in-demand justification, 70/70, credit toward a degree [E: LC-019] |
| Articulation and stacking | Accept EMST bundle credentials and agency training for credit (SAF C2-6 hook) | Certificate → AAS → BS ladders; RA related instruction |
| Work-based learning | Internships required by SAF (C5-5) and EHAC (180 h) | Apprenticeship partnerships |
| Faculty development | Writing observable outcomes; designing validation drills | Same, plus employer co-teaching |
| Current demand data | Which competencies are growing or changing | Which tools employers use (tool layer, with expiry) |

### 6.3 Accreditation hooks to pursue (AS to broker)

1. Offer SAF's education policy review committee (EPRC) an EMST curriculum-map template as an optional companion to the Education Summary at SAF's next standards review [J].
2. Ask SAF to read C4-B.2 / Forest Technology C4-B.6 explicitly as AI-output validation (7.2.1) [J].
3. Use the ABET EnvE proposals for 2027–28 (computational design tools, ethics) as the opening to map 7.2.x [J].
4. Use EHAC List 1 as the coverage spec for an environmental-health module (DB).

### 6.4 The crosswalk file

`cip_soc_env_crosswalk.csv` has 97 rows covering 47 CIP codes across the series 01, 03, 04, 13, 14, 15, 22, 26, 30, 40, 43, 44, 45 and 51.
- `emst_v1_families` is LC judgment.
- `emst_v1_domains` is *computed*: the domains holding at least 15% of the listed families' Core competencies. Domain 3 is under-represented by construction, because v1 makes it Core only for F14 and F15.
- Notes give O*NET-SOC detailed titles where SOC is too coarse (for example 19-4099.03 Remote Sensing Technicians; 13-1199.05 Sustainability Specialists) and link rows to pathways and accreditors.
- **Every row must be checked against the official NCES file before it is used in any funding or supply analysis.**

---

## 7. The pathway template and six worked examples

`pathway_template.md` defines:
- **the CLO unit** (§1);
- **responsibility-based level descriptors** (§2);
- **the pathway record** (§3: header, entry profile, target profile, gap, outcomes, modes, assessment plan, sequence, recognition, duration and cost, exposure notes, equity and sovereignty, evaluation, provenance);
- **14 rules.**

The rules that matter most:
- **R1:** teach only the gap.
- **R2:** outcome formula with verb bands.
- **R3:** every outcome traces to an indicator, or a change request is raised.
- **R4–R5:** performance assessment, coded to the right context.
- **R6:** craft balance: no pixel without plot; no model without a decision owner.
- **R7:** formation protection: supervised repetitions, by-hand quotas, and a work-based-learning share scaled by tacit density.
- **R8:** tools in their own layer.
- **R10:** recognition of prior learning, per CLO.
- **R11:** credentials at bundle grain, with currency set by change velocity.
- **R13:** evaluation metrics.

`example_pathways.md` works six pathways with v1 codes, levels, sample outcomes tied to indicator IDs, modes, assessments, credentials, and duration and cost signals:
- **LC-PW-01:** state environmental-scientist onboarding, 12 months.
- **LC-PW-02:** NEPA specialist upskilling for AI-assisted review, 60–80 h. Built on the 2026 procedural changes and CEQ's technology requirements [E: LC-030].
- **LC-PW-03:** timber cruiser or field technician reskilling into remote-sensing inventory or fire intelligence. Built on SO 3448's intelligence mandate [E: LC-026] and SAF Forest Technology's existing imagery competencies [E: LC-001].
- **LC-PW-04:** federal biologist moving to state agency or consulting. RPL carries most of the load; sector frictions are taught explicitly.
- **LC-PW-05:** water operator upskilling for sensor-based monitoring. Uses NRWA apprenticeship and Workforce Pell; depends on candidate competencies.
- **LC-PW-06:** three-tier AI and data-practice baseline.

---

## 8. Answers to CA architecture questions

### LC-Q1. At what grain do curriculum designers and accreditors need competencies and levels? (DP-3, DP-4)

**Answer: one competency at one level, expressed as 2–5 observable outcomes with conditions and criteria (the CLO), supported by task statements for assessment design.**
- [E: LC-001] SAF writes its minimum competencies at exactly this grain. "An ability to design and implement forest inventories" (Forestry C4-B.5) is one capability at one depth. SAF's verb tiers (knowledge of / understanding of / ability to) act as a three-step level scale. Programs evidence each competency by mapping courses with I/R/E.
- [E: LC-002, LC-004, LC-005] ABET and EHAC specify content areas and outcomes at a similar or coarser grain. None goes to the task level; tasks matter for assessment design, not for accreditation mapping.
- [J] Under CA's hybrid, the internal spine can be tasks and statements, as long as the *user-facing competency* carries anchored level outcomes. The curriculum user needs: (a) the competency (L1) with a definition stable across versions; (b) per-level outcome anchors; (c) links to the L2 tasks that serve as work samples and task-book items. A competency without level anchors is not usable by an instructor. An atomic statement graph without competency views is not usable either.
- **DP-4 (levels).** Generic responsibility levels with competency-specific anchors suit curriculum best. They let a program say "Intermediate" consistently across competencies while still giving anchored examples [J]. Three trainable levels plus a recognized Expert level are enough. SAF effectively uses three, and v1's Expert level is mostly reputation [E: LC-001, LC-031]. IO decides on validity grounds.
- **Typing (DP-3).** Curriculum needs CA's typing: knowledge-type entries (for example 1.1.1) are taught and assessed differently from practice competencies (for example 6.1.2), and tool-family entries (for example 2.1.1) need the tools layer [J; consistent with LC-050 §4.1]. Transversal practice (D7, safety, communication, ethics, systems thinking) maps onto SAF's *integrative* components (C4-5 to C4-9), which are developed across the curriculum rather than in a single course [E: LC-001]. That correspondence is a strong argument for a typed transversal layer.

### LC-Q2. How should competencies link to credentials (Open Badges, CLR, CTDL), and does the transversal layer help program design?

**Answer:**
1. **Publish identifiers.** Each competency and each competency-level anchor gets a persistent URI, published in a framework format credential systems can reference (CASE, and CTDL competency frameworks; IA decides the mechanics) [E that OB 3.0/CLR 2.0 support alignment to framework identifiers: LC-015, LC-016].
2. **Issue at bundle grain.** Credentials are issued for **bundles** of 3–8 CLOs forming a work function, never for single CLOs or whole competencies [J; R11]. Each credential's alignments list every CLO URI and the EMST version, plus the evidence type and assessment context. Rationale: 1.85 million credentials already exist [E: LC-017], and stacking evidence rewards meaningful, stackable units [E: LC-018].
3. **Anchor bundles to functions.** Candidate anchors are the Five Functional Positions (sensing, structuring, analyzing, integrating, deciding) [J: LC-036] or CA's generalized work functions. A bundle is therefore a *view*: computed from role profiles and the CLO layer, versioned, and not a new taxonomy level.
4. **Set currency by change.** A credential's refresh interval follows the computed change velocity or lifecycle status of its CLOs (for example Emergent 2 years, Stable 5 years) [J].
5. **Map external credentials.** Map NWCG quals, FAA Part 107, state operator grades, HAZWOPER, and professional certifications (CWB, PWS, GISP, REHS) to CLOs in an evidence-equivalence register. This is how recognition of prior learning works, and how EMST connects to credentials it does not issue [J; P-LC-07]. About 27 v1 indicators already encode such equivalences implicitly [E: LC-031].

**Does the transversal layer help program design? Yes, strongly.**
- [E: LC-001] SAF requires integrative components across the curriculum, and ABET outcomes 3, 4, 5 and 7 are transversal [E: LC-002].
- [J] A typed transversal layer lets one program map communication, ethics, safety, systems reasoning and human-AI practice once, across courses, instead of rediscovering them in every disciplinary competency.
- [E: LC-037] The transversal D7 competencies (7.1.3, 7.1.4, 7.2.2) are the strongest cross-family bridges in CM's analysis. That makes them the most portable credential content, and the right first bundle (LC-PW-06) [J].

### LC-Q3. How should CLD signals turn into learning-path design, e.g. deliberate formation tasks?

**Answer: compute formation tasks from task tags, then apply four design responses.**

- **Definition.** A *formation task* is a task at career-ladder position P (entry) with tacit density Hi or Med. It is the work through which juniors historically acquired judgment.
- **Response by automation type** (template R7 and §7):
  1. **H (human-essential) formation tasks** (for example 1.3.2 T1, measuring trees; 1.2.4 T1, collecting water samples; 5.5.3 T1, listening to public concerns): deliver through work-based learning with observed assessment. Do not replace them with online modules.
  2. **A (augmented) formation tasks:** teach the augmented workflow, but assess with a validation drill as well as with the tool.
  3. **Ac, V or S formation tasks** (for example 6.4.4 T2 comment-theme analysis, S; 6.1.1 T2 comparing laws, S; 5.1.1 T1–T2 drafting, Ac; 2.2.5 T1–T2 metadata, Ac): require a **by-hand quota**, N unaided products before review-and-certify credit. N is set so the learner can recognize the tool's characteristic errors. Then teach the oversight role.
  4. **Every pathway containing formation tasks** requires a supervisor formation plan (7.2.2 at Intermediate for the supervisor) and a mentor.
- **Basis.** [J: v1's structural analysis of "apprenticeship collapse" and the Forester PD prototype's call for calibration assignments, LC-034, LC-035]; [S until re-read: experimental evidence that unguarded AI help harms unassisted performance, LC-042].
- **What the model must hold.** For CA's computed pathway-level CLD indicator to be useful to LC:
  - tasks need career-ladder position, tacit density and automation assessments as attributed, dated records (L5);
  - role profiles (L3) need to mark which tasks are formation tasks *for that role*;
  - the system needs a field for **alternative formation routes**, meaning what replaces the lost practice (simulation, calibration assignment, rotation), so the CLD indicator can be adjusted when a credible alternative exists [J; aligns with LC-050 §11].
  - A pathway can then report "formation coverage": the share of a role's formation tasks with a designed route.
- **What remains uncertain.** The quota sizes, the work-based-learning thresholds (≥50% of hours for Hi tacit tasks, ≥30% for Med) and the reliability of the tags themselves. The pilot should test these against time-to-proficiency and 90-day transfer.

---

## 9. Proposals

- **P-LC-01: Publish CLOs as part of the standard (change).** For each competency × trainable level, EMST v2 publishes 2–5 observable outcomes with condition and criterion, each tied to persistent indicator IDs. Rewrite all "Understands / Expert in / Shapes" statements. Write in the style of D7.2. *Why:* every curriculum and training use depends on it; v1 is 63% non-observable at the knowledge layer [E: LC-031].
- **P-LC-02: Decouple levels from years (change; with IO).** Use responsibility-based descriptors. Expert is recognized, not taught. Retire the Expert "Publishes…" bias. *Why:* competency-based pathways cannot target tenure [J].
- **P-LC-03: Adopt the pathway template and a pathway registry (add).** IDs LC-PW-NN, pinned to EMST versions, built from role-profile deltas (R1). The six worked pathways become the pilot set. LC-PW-06 and LC-PW-01 come first for the federal and state MVP and the NGO pilot [J].
- **P-LC-04: Add learning-design attributes to competencies and tasks (add).** Required: assessment context code; recommended modes; typical hours per level step; prerequisite edges; formation flag (computed); typical level per task. *Why:* these are the fields an instructor needs, and most can be computed from L2/L5 data [J].
- **P-LC-05: Make exposure-informed learning rules normative but provisional (add).** Use the formation-task definition and responses in §8 (LC-Q3) as design rules, reviewed after IO's inter-rater study and the pilot [J].
- **P-LC-06: Credentials at bundle grain, aligned to EMST URIs (add; with IA).** Use Open Badges 3.0 and CLR 2.0, bundles anchored to work functions, and currency set by computed change velocity [E: LC-015–LC-018; J].
- **P-LC-07: Evidence-equivalence register (add; IO validates).** Map external quals and credentials to CLOs for recognition of prior learning. Seed it from the ~27 credential-type v1 indicators and `training_providers_register.csv` [E: LC-031; J].
- **P-LC-08: Maintain accreditation crosswalks as versioned artifacts (add).** SAF (all four standards), ABET EAC and ETAC, EHAC, NAAEE (re-map against the 2025 guidelines), and the Wiek/Brundiers competencies for sustainability programs. The curriculum map reuses SAF's I/R/E scale. Starter: `accreditation_emst_crosswalk.csv` [E: LC-001–LC-009].
- **P-LC-09: Replace the family→SOC table with a versioned CIP–SOC–EMST crosswalk (change).** Fix the four mis-targeted v1 mappings, add 19-2041 and related codes, verify against the official NCES file, and prepare for SOC 2028. Starter: `cip_soc_env_crosswalk.csv` [E: LC-012, LC-014; J].
- **P-LC-10: Fill accreditor-anchored coverage gaps (add; DB and CA decide placement).**
  - Tree and plant identification (LC-C-03).
  - Forest operations, wood products and certification.
  - Treatment operations (LC-C-05) and OT cybersecurity (LC-C-06, [S]).
  - Environmental-health operations (LC-C-07).
  - Non-electronic navigation inside 2.1.3.
  - Ground-truth calibration (LC-C-04).
  - Write EMST-aligned work-process schedules for environmental-technician and water-operator apprenticeships [E: LC-001, LC-004, LC-005].
- **P-LC-11: Add workforce-learning competencies for supervisors and training officers (add).** Performance-based qualification design (LC-C-01), on-the-job mentoring and evaluation (LC-C-02), and elevate 7.2.2. *Why:* evaluator capacity is the binding constraint [J; LC-R-05].
- **P-LC-12: Build LC-PW-06 first (add).** The three-tier AI and data-practice baseline, with a shared seeded-error validation drill bank across agencies (DraftNEPABench-type public material plus agency documents) [E: LC-030; J].
- **P-LC-13: Move date-sensitive names to dated layers (change).** CEQ regulation references, named EJ tools, and named courses and credentials inside indicators [E: LC-030; J].
- **P-LC-14: Program-mapping service (add; with IA).** NLP-assisted mapping of PLOs and syllabi to CLOs, with human review, gold-set evaluation, and four outputs (coverage, sequence, gaps against demand, accreditation table) [J].
- **P-LC-15: Learning evaluation metrics wired to CM's outcome metrics (add).** Outcome attainment, time-to-proficiency, 90-day transfer, credential acceptance by a second employer, and completion by subgroup [J].

---

## 10. Disagreements and trade-offs

1. **Efficiency versus formation (the biggest trade-off).**
   - AI-assisted workflows let agencies shorten onboarding and reskilling, which matters when staff are scarce [E for staffing declines: LC-028].
   - My formation rules (by-hand quotas, field calibration time, supervised repetitions) lengthen pathways and use mentor time, the scarcest resource.
   - I recommend paying the cost for formation tasks only, measuring it, and relaxing quotas where pilot data show no loss of unassisted performance [J]. Managers optimizing throughput will push back. 7.2.2 exists to argue the case (`7.2.2:intermediate:I4`).
2. **Granularity versus usability.**
   - CLOs are assessable but too many for learners to navigate: 222 × 3 trainable levels.
   - Bundles are usable and credentialable, but they add a governed layer that could drift from the taxonomy.
   - I propose bundles as computed, versioned *views* of role profiles, not a stored level [J]. CA decides.
3. **With IO (anticipated).**
   - IO will rightly want few, validated, assessment-ready indicators. Instructors want rich example banks.
   - Proposal: two tiers. *Assessment anchors* are validated by IO. *Instructional examples* are unvalidated and labeled as such.
   - Training-only use can proceed with rubric calibration; selection use waits for validity evidence [J].
4. **With DC and PS on tools.**
   - The tool layer (R8) protects durability, but learners and employers hire on tool names [J; PS lane].
   - Compromise: tool modules are first-class *learning* objects with expiry dates and tool-agnostic competency credit.
5. **With FC on AI-heavy pathways.**
   - I agree with the push against underrating outdoor judgment. R6 (no pixel without plot) and LC-PW-03's 20–30% field-time rule are my concrete answer.
   - The trade-off is that remote-sensing reskilling takes longer and costs more than a desk-only certificate.
6. **National standard versus regional emphasis.**
   - SAF lets programs emphasize regional priorities (for example the role of fire, laws, species) [E: LC-001].
   - EMST pathways should allow regional and state *profiles* on a shared CLO core, not regional competencies [J; SL to test].
7. **With v1.**
   - Tenure-based levels, the Expert reputation bias, and family-level SOC mapping should all change.
   - v1's task layer, exposure tags and D7.2 are more valuable for learning than v1 itself recognized [J].

---

## 11. Issues outside my area that affect the vision

- **Staffing losses and reorganization (FH, AS).** Federal public-land staffing fell by double-digit percentages in several western states, the Forest Service is reorganizing, and the USWFS boundary is unsettled [E: LC-028, LC-029, LC-027]. All of this cuts the supply of mentors, details and evaluators that work-based learning needs.
- **Corps funding (CM, AS).** AmeriCorps and corps funding status in 2025–26 is unverified. Corps are a key entry pipeline and possibly an equity-critical one [S].
- **Domain 5 data repair (DE).** All 30 D5 competencies have misparsed proficiency text [E: LC-031].
- **Tribal sovereignty (TN).** Any learning content touching Tribal consultation (6.5.1), Indigenous knowledge (5.3.2) or data sovereignty (7.1.1) needs TN's protocol. Simulations must not appropriate real Tribal positions. ITEP engagement is TN-led.
- **Learner-record privacy and accessibility (CP).**
  - CLR and LER records in agency systems are person-level data, and Privacy Act and state-law implications follow.
  - All learning content must meet Section 508/WCAG.
- **Third-party text licensing (AS, DE).** Accreditation crosswalks paraphrase and cite. Reproducing accreditor text would need permission.
- **Post-employment ethics for federal-to-private moves (FH).** These must be taught in LC-PW-04, and FH should supply the current rules.
- **Workforce Pell for field programs (SL, AS).** How field-heavy hybrid and competency-based programs fit the clock-hour and week rules is unresolved [E: LC-021]. State workforce boards will decide in practice.

---

## 12. Open questions for the Chief Taxonomy Architect

1. Will v2 publish CLOs (level-anchored outcomes) **inside the standard (L1)**, or as a separate learning layer that can change faster? I recommend inside L1, with instructional examples outside it (§10.3).
2. Will bundles be a governed view computed from role profiles (my recommendation), or a stored entity?
3. Do you accept three trainable levels plus a recognized Expert level (pending IO)?
4. Which accreditor-anchored gaps (§4.2) go into the core and which into subsector modules? In particular: tree and plant identification, treatment operations, and environmental-health operations.
5. Should EMST seek recognition from SAF's EPRC (and later ABET and EHAC) as an optional mapping framework in Phase 4? Doing so commits us to stable versioning on the accreditors' review cycles.
6. Which role profiles will exist first? LC-PW-01 and LC-PW-02 need a state environmental scientist and a NEPA specialist profile in L3.

**Searches to run when budget allows** (to close my evidence gaps):
- the official NCES CIP 2020–SOC 2018 file;
- the current NWCG PMS 310-1 and GISS/IRIN task books;
- AmeriCorps and corps funding in 2025–26;
- current offerings of NCTC, DOI University, EPA APTI and NETI, NASA ARSET and ITEP;
- re-reading LC-041 and LC-042;
- NAAEE's 2025 guidelines;
- registered apprenticeships in environmental-technician occupations.

---

## 13. Files in this folder

| File | What it is |
|---|---|
| `report.md` | This report (the harness refused my direct write; the coordinator saves it) |
| `pathway_template.md` | Reusable pathway template: CLO unit, level descriptors, fields, rules R1–R14, mode and assessment codes, exposure-informed design |
| `example_pathways.md` | Six worked pathways (LC-PW-01 to LC-PW-06) |
| `cip_soc_env_crosswalk.csv` | 97 CIP 2020 → SOC 2018 → EMST v1 family/domain rows (47 CIP codes). All rows are `nces_check=verify` |
| `accreditation_emst_crosswalk.csv` | 73 rows mapping SAF, ABET EAC/ETAC, EHAC and NAAEE criteria (paraphrased) to v1 codes, with coverage and gap notes. Extra file documented here |
| `training_providers_register.csv` | 32 providers; unverified entries are marked in `offerings` |
| `v1_assessment.csv` | 30 verdicts on v1 elements for curriculum use |
| `candidate_competencies.csv` | 7 candidates (LC-C-01 to LC-C-07) |
| `role_signals.csv` | 7 role signals (LC-R-01 to LC-R-07) |
| `ecosystem.csv` | 29 entities (accreditors, credential standards, funds, programs, datasets) |
| `sources.csv` | 52 sources, including unverified and blocked ones, with reasons |
| `scripts/build_lc_crosswalks.py` | Builds both crosswalks from curated tables and the v1 baseline; validates every v1 code and family |
| `scripts/build_lc_registers.py` | Builds sources, ecosystem, providers, v1 assessment, candidates and role signals; validates schema vocabularies and that every source ID resolves |
| `scripts/v1_lo_analysis.py` | Reproduces the v1 proficiency and indicator statistics in §5 |

To reproduce, run these from the repo root:
```
python3 -I docs/research/learning-curriculum/scripts/build_lc_crosswalks.py
python3 -I docs/research/learning-curriculum/scripts/build_lc_registers.py
python3 -I docs/research/learning-curriculum/scripts/v1_lo_analysis.py
```