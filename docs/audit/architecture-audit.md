# EMST v1 Architecture Audit

**Author:** Chief Taxonomy Architect (CA) · **Phase:** 1 (architecture audit) · **Date:** 2026-10-23
**Status:** Baseline judgment for Phase 3 synthesis. Verdicts are provisional until the research roles report, but the structural findings rest on direct inspection of the v1 data and documents.
**Companion files:** `docs/audit/v1_carry_forward_register.csv` (element-by-element verdicts) · `docs/research/chief-architect/architecture_hypotheses.md` (v2 options and the questions each role must settle) · `docs/research/chief-architect/sources.csv` · `docs/research/chief-architect/ecosystem.csv`

Evidence labels follow TEAM_BRIEF §3: **[E]** = evidence from a cited source I read (source IDs resolve to `docs/research/chief-architect/sources.csv`); **[J]** = my professional judgment, with its basis stated; **[S]** = speculation, with what would confirm or refute it. All counts below are my own computations on the v1 database (CA-001) unless marked otherwise. Where they match the Data Engineer's normalized extract (`data/v1_baseline/`, CA-026), I used that extract to cross-check.

---

## 0. Summary judgment

v1 is a serious piece of intellectual work wrapped in an architecture that cannot carry the charter's vision. The thinking is the asset: the three-craft theory, the irreducibility test, task-level AI exposure, compressive augmentation (Ac), career-ladder destruction (CLD), and the ethical lenses. The data model is the liability. It is one wide spreadsheet row per competency, and every analytical idea sits on that row as a column. The result is that v1 can describe a competency, but it cannot describe a **job**, a **person's blend of crafts**, a **sector actor**, a **tool**, or a **change over time**. Those five things are exactly what the vision ("understand how its jobs are changing") and the theory of change ("if blends are visible and portable, mobility follows") need. [J — rests on §§2–14 below]

Seven findings drive most of my verdicts:

1. **Craft is a re-labelling of domain, not an independent dimension.** Craft primary and domain have Cramér's V = 0.82. Knowing the domain predicts a competency's primary craft 85.6% of the time. Every Domain 2 competency is Datacraft (35/35), every Domain 4 competency is Fieldcraft (35/35), and Fieldcraft occurs in no domain except D1 and D4. The craft criteria document *predicted* the distribution from the domain structure before tagging began. So the craft layer, as built, adds little information beyond the domain, and it cannot show blends. [E: CA-001, CA-010]
2. **There is no role or occupation layer.** "How jobs are changing" is answered in v1 only by hand-built narrative artifacts outside the model (the Forester position-description prototype). The v1 source text actually contains example positions and career pathways for every domain, but they were never carried into the database. [E: CA-006, CA-021, CA-001]
3. **The grain is inconsistent.** A "competency" is sometimes a discipline ("Ecosystem dynamics and processes"), sometimes a qualification-bound practice ("Prescribed fire planning and execution", i.e. burn boss), sometimes a software category ("Project management software", whose task text names Trello and Asana), and sometimes a professional disposition (Domain 7). Skill areas mix subjects, sectors, tool families and settings. A fixed template (exactly 5 competencies per skill area, exactly 3 tasks per competency, exactly 4 tenure-defined levels) imposes uniformity in place of content-driven grain. [E: CA-001, CA-006]
4. **The exposure instrument is the right idea at the right unit (tasks), but it is not yet an instrument.** It has one rater (an analyst working with an LLM) and no inter-rater reliability. Its dimensions are not independent: tacit density almost fully determines automation type. Its headline "FC/DC structural property" is partly built in by Standing Rule R1. It has vocabulary drift and unreconciled counts. And it stores a time-bound judgment as a timeless attribute. [E: CA-001, CA-012, CA-013]
5. **Workflow stages and reform flags are US-federal, NEPA-lifecycle constructs.** 129 of 222 competencies (58%) carry at least one reform flag, so the flags discriminate poorly. Stability tier is a deterministic function of those flags plus Ac/S calls (I found 100% rule consistency), so it adds no independent information. [E: CA-001, CA-009]
6. **Proficiency levels are tenure bands with templated text.** In 189 of the 192 competencies with level text, "Advanced" knowledge begins "Expert in…" and "Expert" knowledge begins "Shapes…". Domain 5's 30 competencies have no behavioral indicators at all because of a parsing error. Neither the levels nor the indicators would survive an IO-psychology review for selection use. [E: CA-001]
7. **Governance relied on one person's discipline and broke in visible ways.** The stated source of truth is a 215-competency file that predates the 222-competency database. There are three or four competing database versions. v7 of the task sequence defers Tasks 15–22 to a v6 document that is no longer in the project. Standing-rule IDs collide. Five Substitution calls were never itemized. Public-facing material claims validation that has not happened. [E: CA-004, CA-007, CA-013, CA-020, CA-022]

My overall verdict is to **carry the ideas, re-derive the structure, and migrate the content as seed material with provenance**. v2 should be a layered model: stable reference vocabularies, typed core competencies, a many-to-many task layer where crafts, exposure and change signals attach, function-defined role profiles with sector-actor variants, a fast tools layer, a dated change-signal layer, and versioned crosswalks. Subsector modules should let coverage extend well beyond public lands. §15 and the hypotheses file set out the options. [J]

---

## 1. Scope, method and limitations

**What I examined.**
- The full v1 database, all eight sheets of `20260223_SkillsTaxonomy_Core_V3_reconciled__copyB` (CA-001), profiled and cross-tabulated in Python.
- Diffs against `…V3.xlsx` (CA-002), `…reconciled__copyA` (CA-003) and `skills_taxonomy_workforce_v1_updated.xlsx` (CA-004).
- The change log (CA-005) and the source text `20251202_SkillsTaxonomy_Core_V2 (1).txt` (CA-006): structure skimmed, Domains 1, 4 and 6 sampled in depth.
- Every framework and record document named in my assignment (CA-007 to CA-025).
- The sister repo's governance pattern (CA-045).
- For calibration, current primary pages for O*NET, ESCO, NICE, SFIA, the Australian Skills Classification, the Singapore Skills Framework, the UK Standard Skills Classification, Lightcast, the WEF Global Skills Taxonomy, Credential Engine/OSMT, and OPM's April 2026 series-consolidation memo (CA-027 to CA-044).

**Limitations.**
- (a) This is a single-reviewer audit. I recommend that IO and DE re-run the statistics independently.
- (b) The v1 text documents became available on disk partway through my work. Before that I read framework content from the project lead's private v1 working records (CA-047, CA-048), and I then verified the content against the exported files.
- (c) The shared web-search budget ran out before I could confirm exact 2018 SOC titles, and the BLS SOC page was blocked (CA-046). My critique of specific SOC mappings in §6 is therefore labelled [J] and handed to FH/IA to verify.
- (d) I did not read all 15,656 lines of the source text. I sampled it.

---

## 2. Purpose fit

The charter sets a vision (shared language for how environmental jobs are changing, plus mobility across seven sector actors), a theory of change (visible, portable craft blends lead to mobility), and a first job (federal and state training, curriculum and workforce strategy, covering reskilling, upskilling and new-hire competencies).

| Charter need | What it requires of the architecture | v1 capability | Gap |
|---|---|---|---|
| "How jobs are changing" | Jobs or roles as entities, task bundles, change recorded over time | Competencies only; exposure stored as a single static snapshot | **Severe** [E: CA-001] |
| Craft blends visible and portable | Craft weights on work units, aggregated to roles and people | One primary craft per competency, collinear with domain | **Severe** [E: CA-001] |
| Mobility across 7 sector actors | Sector actor as a structured dimension, with transfer frictions | 5 free-text "sector application" notes per competency; no Tribal, state or local distinction | **Severe** [E: CA-001] |
| Federal and state training and curriculum | Assessable proficiency levels; links to OPM series and quals, state classes, CIP, credentials | Tenure-band levels; templated text; family→SOC crosswalk only | **Major** [E: CA-001] |
| Reskilling and upskilling | Gaps between a current role profile and a target role profile | No role profiles, so no gap computation | **Major** [J] |
| New-hire competencies | Entry-level role profiles and P-level task bundles | Career-ladder position per task (good) but no entry roles | **Moderate** [E/J] |
| Coverage beyond public lands | Subsector coverage (water, air, waste, energy, ESG, environmental health…) | Zero competencies mention drinking water, wastewater, marine/coastal or utilities; one each mentions air quality, hazardous materials and remediation | **Severe** [E: CA-001, CA-026] |
| Living system ("keeps the tool current") | Change-signal ingestion, versioning, stable IDs | No IDs, no release, no signal pipeline; a sentinel network was planned (Task 22) | **Severe** [E: CA-007] |

The v1 design served a different first job well: building a **pre-Delphi analytical instrument** about one practitioner community (public-lands environmental management). That job explains most of v1's choices: OBAM stages, NEPA reform flags, SAF-adjacent families, GitBook publication. The charter's first job is operational (training officers, HR specialists, curriculum leads), and its vision is sector-wide. So the audit question is less "is v1 wrong" and more "what of v1 survives a change of purpose". [J]

---

## 3. The entity model: what kind of thing each level is

The methodology report v1 itself commissioned (CA-016) gives the right test: "the core architectural question is not only *what levels exist*, but *what kind of thing each level is* (work vs worker attribute; observable vs latent; context-specific vs transferable)." v1 did not apply it to itself.

| Level | Count | What v1 says it is | What it actually is | Verdict |
|---|---|---|---|---|
| Domain | 7 | Top-level knowledge or practice area | A mix of classifying principles: a knowledge tradition (D1), a technology modality (D2), a management function (D3), a work setting or physical mode (D4), a communication mode (D5), a policy and regulatory function (D6), and a meta-category of cross-cutting practice (D7). The craft framework then re-encodes three of these modes. [E: CA-001, CA-010] | **Change**: re-derive the top level from durable work functions plus subsector modules; keep v1 domains as a legacy navigation facet |
| Skill area | 45 | Cluster of related competencies | Mixed again: disciplines (1.3 Forestry Science), sectors (3.6 Corporate Sustainability & ESG), tool families (2.5 Digital Collaboration Tools, 2.7 Immersive Technologies), settings (4.7 Urban Environmental Infrastructure), occupations or qualifications (4.3 Fire Management), and a "(NEW)" marker left in a name (5.6). Each holds exactly 5 competencies (Data Dictionary rule: "Max 5 competencies per skill area"). [E: CA-001] | **Change** |
| Competency | 222 | "Competency": title, one-sentence description | Not one kind of thing (see §4). The convention says titles are "active-verb phrase[s]" (CA-007), but titles in the database are noun phrases. 19 descriptions are missing, several because the description was pasted into the title (e.g. 3.1.1). [E: CA-001, CA-026] | **Change**: carry content as seeds; type the entity |
| Task | 666 (3 per competency) | "Job Tasks: T1 = foundational execution, T2 = intermediate application/analysis, T3 = advanced synthesis/leadership" (CA-007) | Mostly real task statements (verb + object + context), and the best-grained content in v1. But (a) tasks are graded by level, which conflates *work* with *proficiency*; (b) each task belongs to exactly one competency, with no many-to-many link; (c) the count is fixed at 3; (d) about 76% of D3 tasks were inferred rather than transcribed (CL-011); (e) none is linked to an O*NET task or DWA. The most common first verb is "Use" (54 tasks), often tool-bound. [E: CA-001, CA-005] | **Change**: make tasks a first-class many-to-many entity |
| Proficiency level | 4 × 222 | Foundational (0–2 yrs), Intermediate (3–5), Advanced (6–10), Expert (10+) | Tenure bands, not proficiency. Levels are forced onto every competency, against the SFIA principle (cited in v1's own methodology report, CA-016) that a skill is described only at the levels where it is practiced. [E: CA-001, CA-016, CA-034] | **Change** |
| Knowledge / Application statements | 1,776 cells | Level descriptors | Template-generated (see §4.3). 30 D5 competencies have none in the Competencies sheet. [E: CA-001] | **Change** (rewrite) |
| Indicator | up to 6 per level | Observable indicators | Mixed. Some are good behavioral indicators ("Collects field data on ecosystem processes with guidance"). Many are reputational or latent ("Publishes…", 180; "Influences…", 186; "Recognized…", 52). D5 rows hold no indicators, only the misplaced Knowledge/Application text. [E: CA-001] | **Change** |
| Sector application | 5 × 222 (1,110 notes) | How the competency applies per sector | Illustrative free text (e.g. "Natural capital accounting, ecosystem service valuation"); 66 competencies carry stray "*" markers. Sector categories don't match the charter's actors (§7). [E: CA-026] | **Change** |
| Dimension tags | 48 columns | Analytical layers | Attributes of very different kinds jammed onto the competency row: classifications (craft), applicability tags (families), lifecycle positions (stages), dated external-event exposures (reform flags), derived states (stability tier), task-level assessments pivoted wide (T1–T3 exposure), and ethical review findings (lenses, empty). [E: CA-001] | **Change**: each belongs to a different entity (see §15) |

**Core structural defect.** v1 has a single entity (the competency) with a fixed number of slots, so every relationship that should be many-to-many is forced into one of three shapes: repeated columns (T1/T2/T3, F1–F15, Stage Primary 1/2, L1–L5), free text, or an analytic finding that lives only in session records. The empty columns show this directly. "Stage Primary 2" and "Stage Secondary 2" are blank for all 222 rows, even though five dual-primary exceptions are documented (CA-009 and the Task 10 summary), and "Dual Primary Exception" is False everywhere. The structure lost the data. [E: CA-001]

---

## 4. Grain and consistency

### 4.1 Is a "competency" the same kind of thing across domains?

No. [E: CA-001] Representative examples:

| Code | Title | Actual kind of thing |
|---|---|---|
| 1.1.1 | Ecosystem dynamics and processes | Body of disciplinary knowledge (an ESCO "knowledge" concept, not a competence) |
| 2.1.1 | GIS operation | Tool-family fluency |
| 2.5.3 | Project management software | Software category; T1 names "Trello, Asana" |
| 3.6.2 | Sustainability reporting and disclosure (GRI, SASB, TCFD) | Practice bound to named reporting standards; tasks name "blockchain verification" and "SEC climate disclosure" |
| 4.3.2 | Prescribed fire planning and execution | Qualification-gated practice ("Conduct prescribed burns as burn boss"), i.e. close to a *role* governed by an external qualification system |
| 4.4.1 | Occupational safety and risk management | Transversal practice required of every field worker |
| 5.5.2 | Permit administration | Administrative work function, specific to public lands |
| 6.7.2 | Environmental justice screening and assessment | Analytical practice whose named tool (EJSCREEN) is date-sensitive |
| 7.2.1 | Validating AI outputs against ecological and regulatory ground truth | Transversal professional practice |

A taxonomy can contain all of these kinds, but it must **type** them, because each kind changes at a different speed, is assessed differently, and serves different users. ESCO separates knowledge, skills/competences and transversal skills, and it labels reusability. SFIA separates skills from generic attributes and levels of responsibility. The Australian Skills Classification separates core competencies, specialist tasks and technology tools. The Singapore framework separates technical skills and competencies (TSCs) from Critical Core Skills (CCS). [E: CA-016, CA-034, CA-036, CA-037] v1 does none of this.

### 4.2 Are tasks real tasks?

Largely yes, and they are the most valuable content to migrate. DACUM's test is "smallest unit of job activity with a meaningful outcome… clear start/end points" (cited in CA-016). Most v1 tasks pass it, e.g. "Measure tree height, diameter, and age using field instruments" and "Conduct job hazard analyses before field activities". [E: CA-001, CA-016]

Four systematic problems remain:
- (a) **Level grading.** T3 is defined as "advanced synthesis/leadership", so some T3s are competency restatements rather than tasks ("Leads major…", "Create team cohesion and culture…").
- (b) **Tool embedding.** "Use AI-powered tools to ensure alignment with multiple reporting frameworks (GRI, SASB, TCFD, SEC climate disclosure)" will date quickly. [J: tool and standard landscapes in ESG disclosure have shifted repeatedly; DC and PS to confirm current status]
- (c) **Inferred text.** About 76% of D3 task text was inferred and never verified (Pre-Task 15B is pending). [E: CA-005, CA-007]
- (d) **Text drift.** The task rows in the Domain 4 working record (e.g. 4.1.1 T2, "Use digital data collection tools and GPS…") do not always match the database's task text. DE's `version_diffs.csv` should be used to measure how much. [E: CA-012; J on extent]

### 4.3 Proficiency text

Counts for the 192 competencies with level text in the Competencies sheet [E: CA-001]:
- Foundational–Knowledge begins "Understands…" in 170.
- Advanced–Knowledge begins "Expert in…" in 189. The *third* level is called expert, which is a level-label collision.
- Expert–Knowledge begins "Shapes…" in 189 (e.g. "Shapes understanding of ecosystem theory and application").

Indicator first words, across all 222 competencies × 4 levels: Develops 449, Uses 346, Influences 186, Publishes 180, Understands 171, Leads 148, Advances 78, Recognized 52.

"Understands", "Influences", "Shapes", "Publishes" and "Recognized" describe latent states or reputation, not observable behavior at a performance standard. This is exactly the failure the charter's IO role is told to push on ("any competency that can't be observed or assessed"). I recommend carrying the indicators only as **draft seeds** for IO-led rewriting. They must not be presented as assessment-ready. [J, resting on the Campion et al. and Uniform Guidelines lineage cited in CA-016; IO to confirm]

### 4.4 Data-integrity defects that matter architecturally

These are not cosmetic. Each one shows a structural cause that v2's schema must design out. [E: CA-001, CA-002, CA-004, CA-005, CA-013, CA-026]

| Defect | Count / example | Structural cause |
|---|---|---|
| D5 proficiency misparsed into indicator columns (`Knowledge*:` / `Application*:`; no real indicators) | 30 competencies, 120 rows | Hand transcription into fixed columns; no validation |
| Descriptions missing or merged into title | 19 | No field-level validation |
| CLD flag vocabulary split (True/False vs Yes/No; D6 uses Yes/No) | 40 D6 rows | Domain files merged by hand |
| CLD severity values outside the dictionary ("Highest", "Ungraded") | 8 | No controlled-vocabulary enforcement |
| Modal Contested uses N/No/Y/Yes | 222 | Same |
| Horizon value "3" defined but never used | 0 of 666 | Possible scale miscalibration, or a default to 1/2 |
| Substitution: synthesis reports 9 (4 itemized + "5 C-position S calls… not individually extracted"); database holds 4 | 9 vs 4 | Findings recorded in prose, not data |
| Task totals: synthesis says 636 confirmed vs 645 expected; database has 666 | — | Running totals kept in chat, not computed |
| Reform flags: Data Dictionary note says 174 instances on 122 competencies; database has 184 on 129; Workforce Signals dashboard is older still (215 competencies; SC = 89) | — | Stored summaries instead of computed views |
| V3 vs reconciled differ in 40 D6 exposure rows; copyA vs copyB differ only in Data Dictionary (65 vs 90 rows) | — | No single source of truth (§14) |
| "Foundational Professional Preparation" defined three ways: about 20 zero-Core competencies (Task 9 summary); "seven competencies earned Core tags from 10 or more families" (governance chronology, CA-047); in the database, 43 zero-Core competencies, 30 FPP-flagged by skill area, and a maximum Core count of 6 | — | Narrative findings not tied to data |

---

## 5. The craft model (FC / DC / SC)

### 5.1 What v1 did

`craft_assignment_criteria.md` (CA-010) defines Fieldcraft, Datacraft and Statecraft by their irreducible contribution, and it gives a good decision test ("If you removed [craft X]'s core contribution… would the competency still exist?"). It allows one primary and at most two secondary crafts per competency, and it lists ten integration points. That is a strong conceptual design. [E: CA-010; J that it is strong]

### 5.2 What the data shows

| Domain | DC | FC | SC |
|---|---|---|---|
| D1 | 26 | 14 | 0 |
| D2 | 35 | 0 | 0 |
| D3 | 7 | 0 | 28 |
| D4 | 0 | 35 | 0 |
| D5 | 2 | 0 | 28 |
| D6 | 7 | 0 | 33 |
| D7 | 2 | 0 | 5 |

Cramér's V (craft primary × domain) = **0.82**; the modal craft for each domain is correct 85.6% of the time. [E: CA-001, my computation]

The criteria document stated in advance: "Domain 4… should be nearly all Fieldcraft primary. Domain 2… should be nearly all Datacraft primary. Domains 5… and 6… should be predominantly Statecraft." It then treated agreement with this prediction as calibration. The domain therefore acted as a prior on the craft label, and the "validation" was circular. [E: CA-010]

### 5.3 Is craft a classification, a lens, or a blend profile?

As implemented it is a **classification** (mutually exclusive primary). As the charter describes it ("professionals… need a blend of three crafts… if those blends are visible and portable, mobility follows"), it is a **blend profile of people and roles**. These are different data types. A single primary label per competency cannot represent a blend. Aggregating primary labels over a role's competencies gives a crude count, not a profile, because each competency counts as 100% of one craft. [J]

v1's own records show the strain:
- 1.1.5 Habitat requirements analysis is flagged "scale-dependent assignment — site-level… Fieldcraft; landscape-scale… Datacraft" (CA-023).
- Riparian buffer design is flagged as possibly needing a split (CA-010).
- Prescribed fire planning is "a defensible 50/50" (CA-010).

All three are the same pattern: craft varies with the *task and context*, not with the competency. [E: CA-010, CA-023]

The Structural Conditions report (CA-017) adds a sharper idea: the crafts are **distinct reproduction regimes**. Fieldcraft is reproduced through place-based practice and mentorship; Datacraft is more codifiable and therefore more exposed; Statecraft is partially codifiable but tied to legitimacy. That makes craft a property of *how work is learned and protected*, which links it directly to CLD and to curriculum design. [E: CA-017]

### 5.4 Verdict and proposed representation

- **Carry** the three craft definitions and the irreducibility test as the *rubric*. [J]
- **Change** the representation: a **craft weight vector on each task** (e.g. FC 0.6 / DC 0.3 / SC 0.1, elicited with the irreducibility test as an anchored rating, multi-rater, with confidence). Competency and role **blend profiles** are then *computed* by aggregating task weights, weighted by task importance and time share in the role profile. [J]
- **Retire** the stored "Craft Primary/Secondary" columns, keeping them as a v1 provenance field, and retire the predicted-distribution check. [J]
- **Add** craft "reproduction regime" attributes: learning mode, mentorship dependence, place-boundness. These feed CLD and curriculum. [J, building on CA-017]
- **Needs evidence:** whether raters can reliably produce weights. IO must design and pilot this. If inter-rater reliability on weights is poor, fall back to a 3-level ordinal (none / supporting / defining) per craft per task, which is still a blend. [S: confirm with a pilot of about 60 tasks × 3+ raters]

---

## 6. Profession families vs roles and occupations

**What v1 has.** 15 families (F1–F15) with careful definitions, boundary criteria, representative roles (as prose), domain span and overlap notes (CA-008). Each competency is tagged Core, Supporting or blank against each family. The governing rule ("classify from competency content, not role occupancy") is sound. [E: CA-008]

**Problems.**
1. **Families are tags on competencies, not groupings of roles.** A family Core tag says "this competency matters to foresters". It cannot say *which forester role*, *at what level*, *how much of the job*, *in which sector actor*, or *how that is changing*. In 133 of 222 competencies the Core count is exactly 1; in 43 it is 0; the maximum is 6. The tag is mostly a disciplinary-home marker. [E: CA-001]
2. **There is no role or occupation layer.** Yet the source text lists example positions for every domain and has domain-level career pathways (Entry 0–3 → Mid 3–7 → Senior 7–15 → Expert 15+, with skill-area focus). The database dropped all of it. This is the cheapest high-value recovery in the whole migration. [E: CA-006]
3. **The family set skews to public lands and conservation.** Families acknowledged as missing: marine and coastal, Tribal natural resource management, urban parks and green infrastructure (CA-008). Families not even acknowledged: drinking water and wastewater operations, air quality management (one competency, 6.7.5), waste, hazardous materials and remediation, environmental compliance and EHS, energy siting and operations, environmental engineering, public environmental health (local health departments), parks and recreation operations, and environmental laboratory science. [E: CA-001, CA-008; J on which are missing; DB to confirm the subsector list]
4. **The crosswalk is at family level only and several mappings look wrong.** v1's own Labor Market Crosswalk rates 7 of 15 family→SOC mappings Low. Beyond that, some mappings are, in my judgment, mis-targeted:
   - F11 Environmental Education → secondary SOC 25-4031 (Library Technicians)
   - F13 Environmental Health & Justice → 29-9021 (a health information occupation)
   - F12 Fire Management → 33-1021, labelled "Fire Inspectors"
   - F8 Environmental Policy → 23-1011 Lawyers

   The largest relevant SOC detailed occupation, 19-2041 (Environmental Scientists and Specialists, Including Health), does not appear at all. [E for the mappings as recorded in CA-001; J for my assessment of the SOC titles, which I could not re-verify this session (CA-046). FH and IA to verify against the 2018 SOC and O*NET-SOC 2019.]
5. **The occupational layer outside EMST is itself moving.** OPM's 24 April 2026 memo starts consolidating 115 low-use or obsolete series. For example, 0410 Zoology, 0437 Horticulture, 0480 Fish and Wildlife Administration and 0487 Animal Science are realigned to 0401; 0455 Range Technician to 0404; 0029 Environmental Protection Assistant to 0303. Future phases will "address broader structural redesign aligned to skills-based workforce frameworks". So EMST must not hard-wire OPM series into its structure. It needs **function-defined role profiles** with **versioned crosswalks** to whatever series and state classes exist at a given date. [E: CA-044; J on implication]

**Verdict.**
- **Add** a role-profile layer: function-defined work roles; a task bundle with importance and time share; required competencies with target level; computed craft blend; sector-actor variants; entry and progression links; crosswalks to O*NET-SOC, OPM series and quals, and state classes.
- **Change** families into *groupings of role profiles* (job families). Re-derive them from function and extend coverage.
- **Carry** the boundary-criteria text and the content-not-occupancy principle.
- **Retire** the competency × family Core/Supporting matrix as stored data; compute it from role profiles.

The Forester PD prototype (CA-021: "Same Title, Different Job") is the clearest statement of what users want from the product. v2 must be able to generate it from data rather than hand-author it. [J]

---

## 7. Sector actors

**What v1 has.** Five free-text notes per competency: Public Agencies, Private Sector, NGOs, Consulting, Academia (1,110 notes). [E: CA-026]

**Problems.**
- (a) The categories don't match the charter's seven actors. "Public Agencies" merges federal, state, local and Tribal. That erases the distinctions the charter treats as primary (federal–state mobility is the first job). Consulting is a business model inside the private sector, not an actor. Tribal nations, which are sovereign governments and employers, are absent.
- (b) The notes are illustrative settings ("Timber cruising, carbon inventory, forest valuation"), not statements of how the competency is *enacted differently*.
- (c) Nothing is structured, so mobility cannot be computed.

[E: CA-001, CA-026, charter; J]

**Where sector actors should enter the model.** Sector actor is a property of an *employment context*, not of a competency. It belongs:
- on **role profiles**, as sector-actor variants of a function-defined role (e.g. "Water quality permit writer — state agency" vs "— consulting firm"), each with its own crosswalk (OPM series, state class, private job architecture);
- on **enactment notes**, where a competency is genuinely performed differently by actor. This matters most for Statecraft (consultation under federal trust obligations vs state administrative procedure vs a Tribal government's own processes vs a corporate disclosure regime);
- on **transfer-friction attributes** between actors: credential recognition, classification barriers, pay-system gaps, security or citizenship requirements. CM's mobility model needs these.

Tribal nations must be modelled as sovereign governments *and* employers. Inclusion of any Tribal-specific content must follow TN's protocol and CARE. [J; TN to determine]

**Verdict.** **Retire** the five-field structure, keeping the text as seed illustrations with provenance. **Add** the sector-actor vocabulary (federal | state | local | tribal | ngo | private | academic, with sub-types such as special district, utility, consulting), role variants, enactment notes and friction attributes. [J]

---

## 8. Workflow stages (S1–S6)

**What v1 has.** Six stages derived from Outcomes-Based Adaptive Management: Planning, Environmental Review, Permitting, Implementation & Field Ops, Monitoring, Adaptive Management & Learning. They are defined by the kind of work, not the calendar. S2 and S3 are kept separate "to preserve… permitting reform analysis". A 2-primary/2-secondary cap applies. [E: CA-009]

**Assessment.**
- (a) **It is a project and authorization lifecycle, centred on public lands and NEPA.** It fits federal land and resource projects well. It fits poorly for continuous operations (a wastewater plant, air monitoring networks), inspection and enforcement, corporate reporting cycles, emergency response, research, and education. Those are the majority of jobs in the subsectors v2 must add. [J]
- (b) **Distribution:** S1 is primary for 111 of 222 (50%); S6 for only 4. Either half the field is "planning", or the stage set lacks the operational, compliance and service stages that would absorb those competencies. [E: CA-001; J on interpretation]
- (c) The second primary and second secondary columns are empty in the database (§3).
- (d) Stage is attached at competency level, although the same competency serves different stages through different tasks.

**Verdict.**
- **Change.** Generalize into a work-function or value-chain facet that is subsector-neutral at the top. My draft: *Assess & sense → Plan & design → Authorize & regulate → Implement & operate → Monitor & verify → Enforce & assure → Learn & adapt → Engage & communicate*. Keep S1–S6 as a named **profile** (the "project and authorization lifecycle") mapped onto it, so permitting reform analysis remains possible.
- **Attach** stages to tasks, not competencies.
- **Retire** the caps.
- SC and DB should test the draft against non-federal and non-land subsectors. [J]

---

## 9. Reform-sensitivity flags

**What v1 has.** Six Boolean flags (NEPA timeline, digital permitting, CatEx scope, consultation, One Federal Decision, S2–S3 boundary) on 129 of 222 competencies (58%): 184 flag instances. [E: CA-001]

**Assessment.**
- The flags are **events, not properties**. They are dated, jurisdiction-specific policy changes, US federal only, that may reverse, expire or be superseded. A Boolean on a competency records neither the event, its date, its direction, nor its status. [J; SC to supply the current state of each reform]
- At 58% prevalence the flags have little discriminating power. [E: CA-001]
- Counts were inconsistent across three stored summaries (§4.4). [E]
- Federal NEPA and permitting are only one of many reform streams the sector faces: state permitting reforms, utility regulation, disclosure regimes, Tribal co-management agreements, and funding conditions. [J]

**Verdict.** **Change**: move the flags into the **change-signal layer** as dated *driver events*. Each event records jurisdiction, instrument, date, direction, status (proposed/in force/stayed/rescinded), source, affected task IDs and role IDs, and the expected effect. Keep the six v1 codes as seed events with provenance. **Retire** "Reform Flag Count". [J]

---

## 10. AI and robotics exposure instrument

### 10.1 Strengths, which should carry

- **Unit of analysis.** "The exposure classification instrument operates at the task level, not the competency level… [capturing] the 'jagged' automation pattern." That is correct, and it is consistent with O*NET-anchored exposure research. [E: CA-012; J]
- **Ac (Compressive Augmentation).** This is a genuinely useful category, and I have not seen it in standard indices: "headcount compression is plausible even without full substitution… The human role persists as review-and-certify." It names the mechanism most likely to change staffing in public agencies. [E: CA-012; J on novelty, LM to check the literature]
- **The A/V boundary rule** ("current deployment reality, not projected trajectory") and the **mode-split flag** are good coding practice. [E: CA-012]
- **Vector with Ro/Cv.** Robotics and convergent exposure matter for field work, and most AI indices ignore them. [E: CA-012; J]
- **Career-ladder position and CLD.** This is the most original and policy-relevant contribution in v1: automation can remove the tasks through which juniors build tacit judgment. [E: CA-013; J]
- **Provenance column and standing rules.** These show the right instincts: document coding decisions and mark reconstructed data. [E: CA-001, CA-013]

### 10.2 Weaknesses, which must change

1. **One rater, no reliability evidence.** All classifications came from one analyst working with an LLM in sessions. 75 of 222 competencies' exposure data is "reconstructed" or "retrospective" rather than coded live. [E: CA-001, TEAM_BRIEF]
2. **The dimensions are not independent.** Tacit density nearly determines automation type:

   | Tacit | A | Ac | H | S | V |
   |---|---|---|---|---|---|
   | Hi | 148 | 0 | 129 | 0 | 0 |
   | Med | 234 | 19 | 16 | 0 | 6 |
   | Lo | 7 | 82 | 1 | 4 | 20 |

   No Hi-tacit task is Ac, S or V, and only one Lo-tacit task is H. Either tacit density is the operative predictor (then report it as a predictor, assessed independently), or the coder inferred one dimension from the other (then the instrument has fewer real dimensions than it claims). [E: CA-001, my computation; J]
3. **The "FC/DC structural property" is partly built in.** The synthesis calls it "the most robust structural finding in the taxonomy… holds without exception". But Standing Rule R1 instructs: "Any H call on a DC Primary competency is anomalous and requires explicit… documentation. FC Primary → watch for H; DC Primary → A expected." The definitions of Fieldcraft (embodied, tacit) and of H (embodied judgment, physical presence) also share criteria. A pattern that coders were told to expect, and that follows from overlapping definitions, cannot then be offered as an empirical finding. It must be re-tested with blind coding. [E: CA-010, CA-012, CA-013]
4. **Descriptive and normative judgments are conflated.** All 21 Domain 7 tasks are coded H, with the rationale that "these competencies cannot themselves be automated without defeating their purpose". That is a normative claim (they *should not* be automated), not a deployment observation. It conflicts with the instrument's own A/V rule. Validating AI outputs (7.2.1), for example, is increasingly AI-assisted. [E: CA-015; J]
5. **Time is not modelled.** Exposure is stored as an attribute, but it is a dated assessment. Horizon "3" is never used, and "N" fuses "no horizon" with Human-Essential. [E: CA-001]
6. **No external calibration.** None of the 666 tasks is linked to an O*NET task or DWA, so v1 cannot be benchmarked against task-level external measures. v1's own interoperability planning named an O*NET crosswalk as the "single highest-leverage structural action" (CA-048). [E: CA-048; J]
7. **The Structural Conditions report's own recommendation was not implemented:** "AI exposure… as technical overlap × institutional adoption mode × ladder fragility." [E: CA-017]

### 10.3 Where it belongs in the v2 model

Exposure is an **assessment event about a task** (optionally, a task in a role and sector context). It is not a column on a competency. Proposed record:

`exposure_assessment(assessment_id, task_id, [role_id], [sector_actor], dimension values, rater_type {expert|panel|llm|external-index}, rater_id, method_version, codebook_version, date, evidence/source_ids, confidence, scenario_id?)`

Under this model:
- several assessments per task coexist (v1 analyst, Delphi panel, LLM rubric, external index joins), and the product shows agreement or disagreement;
- competency and role exposure summaries are **computed**, not stored;
- career-ladder position is **derived** from which role levels perform the task in role profiles, not asserted per task;
- CLD becomes a **pathway-level** computation: does the entry role still contain enough formation tasks? [J]

**Verdict.**
- **Carry:** vocabulary (with tightened definitions), Ac, A/V rule, vector, CLD concept and R9 severity rubric.
- **Change:** representation, rater model, codebook (re-issue R1–R12 with unique IDs; drop R1's expectation clause), time model.
- **Needs evidence:** all v1 values remain *v1 analyst assessments*. Migrate them as such, never as ground truth.

---

## 11. CLD and stability tier

**CLD.** 62 competencies carry CLD (45 "True" + 17 "Yes", once the Yes/No values are normalized). D6 has 17, D2 13, D5 12, D3 10, D4 9, D1 1, D7 0. Severity ratings are uneven. The concept is the single most actionable workforce-planning signal in v1, because it speaks to new-hire design, apprenticeships and curriculum. **Change** it into a computed pathway indicator: CLD risk for role R at entry level, equal to the share of R's formation tasks (P-level, high tacit or developmental value) that are assessed Ac, V or S, adjusted for whether alternative formation routes exist. Severity (R9) stays as an expert overlay. [E: CA-001, CA-013; J]

**Stability tier.** The tier is fully determined by its rule ("Transition = 1+ reform flag OR 1+ Ac/S task"): I found zero rule violations among non-Emergent rows. 150 of 222 are Transition. So it stores no independent judgment and discriminates poorly. It also omits *workforce reproduction stability*, which the Structural Conditions report argues matters more (fire management: durable tasks, fragile ladder). [E: CA-001, CA-017]

**Verdict.** **Retire** the stored tier. **Add** computed change indicators on tasks, competencies and roles: direction (growing/transforming/declining), velocity, evidence strength, scenario sensitivity, and reproduction fragility. **Carry** "Emergent" as a *lifecycle status* (proposed/emerging/established/declining/withdrawn) on competencies and roles. [J]

---

## 12. Ethical lenses (L1–L5)

**Strengths.** The framework (CA-011) is thoughtful and practitioner-facing. Separating Cultural Rights and Self-Determination (L2) from Equity and Justice (L1) is analytically important: "a project can distribute benefits equitably while still violating governance rights". The Intervention Ethics (L4) triggers (no historical precedent; practical irreversibility) are operational. [E: CA-011]

**Problems.**
- The columns are empty (4 of 222 populated).
- L2/L3 numbering was transposed in working documents.
- The headline finding ("approximately 95% of ethical content is implicit") exists only in session records.
- R10 creates a special E/A-only scale for 7.1.

More fundamentally, an E/I/A tag on a competency tells an HR specialist or training officer almost nothing actionable. [E: CA-001; J]

**Verdict.** **Carry** the lens definitions. **Change** their role in three ways:
- (a) a **content-quality rubric**: when a lens is triggered, the competency's indicators must make the ethical obligation observable (the ethical lens framework's own "integration mode 3");
- (b) a **search facet**;
- (c) a **review checklist** in the governance process.

Any population must be multi-rater. L2-related content is subject to TN's protocol; the project must not author Tribal governance content on its own. **Retire** R10. [J]

---

## 13. Domain 7 as an integration layer

Domain 7 (7.1 Professional Ethics Architecture, 4 competencies; 7.2 Human-AI Professional Practice, 3) was created to hold capacities that "apply across all six subject-matter domains". The v1 record itself asks whether 7.2 is coherent or should be "distributed by craft to home domains". [E: CA-015]

**Assessment.** Putting cross-cutting practice into a "domain" is a category error. It is a different *kind* of entity: a transversal professional-practice capability with domain-specific enactments. Comparable frameworks treat it that way: ESCO transversal skills, Singapore Critical Core Skills, SFIA generic attributes and behavioural factors, the UK SSC's 13 core-skill categories. [E: CA-016, CA-034, CA-037, CA-038; J]

The source text also contains domain-level cross-cutting competencies (e.g. D4: Safety Consciousness, Environmental Awareness, Physical Fitness & Endurance, Adaptability & Problem-Solving, Attention to Detail; D6: Systems Thinking and Integration, Stakeholder Engagement and Negotiation…). The database dropped them. They belong in the same transversal layer. [E: CA-006]

**Verdict.**
- **Change:** create a **transversal practice layer** (professional ethics and integrity, human-AI practice, safety culture, systems thinking, collaboration…) linked to domain-specific enactment statements and tasks.
- **Carry** the 7.2 content (AI-output validation, tacit-knowledge formation design, judgment calibration), which is high-value and sector-wide.
- **Needs evidence:** 7.1.1 (Indigenous data sovereignty) requires TN-led review before it is published as an EMST competency.
- Re-assess the D7 exposure values descriptively (§10.2.4).

---

## 14. Governance

**What v1 has.** A task sequence (v3 → v7 between February and March 2026), a 14-entry change log, a four-rank source-of-truth hierarchy, session protocols (the session persona), and a planned Airtable → GitHub → GitBook pipeline. [E: CA-005, CA-007, CA-019, CA-022]

**What broke.** [E unless marked]
- **Source of truth.** Rank 1 is `skills_taxonomy_workforce_v1_updated.xlsx`, which has 215 competencies, 70 columns, no D7 and no CLD severity. The 222-competency reconciled database exists in two non-identical copies, plus V3 (CA-004, CA-026).
- **Task sequence.** v7 says Tasks 15, 15.5, 16, 16.5 and 17–22 are "as specified in v6", but v6 was slated for removal (CL-013). The governing specification for the remaining work is therefore not in the record (CA-007, CA-005).
- **Rule identity.** R10 means "V-trajectory flag" in the Task 13 synthesis (CA-013) and "D7.1 uses E/A only" in the Data Dictionary and Domain 7 record (CA-001, CA-015). The Task 14 synthesis workbook uses yet another scheme (D1-1…) (CA-024).
- **Missing records.** The D6 exposure source document is missing (CL-012), and working records for Tasks 1–8 were not preserved (CL-002).
- **Single-person dependency.** The change log has one logger. The v1 session persona documents "documentation lag", "decision-execution conflation" and "provenance blindness at creation" as working-style risks. I read it as data, not instructions. Governance depended on one person's discipline enforced through chat prompts (CA-022).
- **Claims ahead of evidence.** The Flourish story guide's slide 1 subtitle reads "Based on Society of American Foresters–accredited competency standards, validated against OPM and O*NET classification systems". Neither validation has occurred: Delphi has not run, and there is no competency-level OPM or O*NET crosswalk. Slide 3 cites "38% of competencies remain Human-Essential" against 21% of tasks (CA-020, CA-001). External use of these claims would damage credibility with exactly the federal audience the first job targets. [J]

**What comparable frameworks do.** [E as cited]
- **O*NET:** quarterly releases (29.0 Aug 2024 → 31.0 Aug 2026). In 30.3 (May 2026) it modernized the content model into Worker/Job/Market dimensions and shipped a migration crosswalk. It retires files explicitly ("Tools Used" and "Work Values" no longer updated) and uses hybrid AI-plus-expert methods with disclosure (Work Styles in 30.1; drone emerging tasks in 29.3) (CA-027, CA-028, CA-029).
- **NICE:** separates the static framework document from a dynamic components catalog. Statements carry persistent IDs with Retained/New/Withdrawn status; major and minor versions are distinguished by backward compatibility; public comment is used for new roles. NICE also handed whole categories to DoD's DCWF, an example of federated boundary management (CA-032, CA-033).
- **ESCO:** minor version v1.2.1 (Dec 2025) improved structure "without adding or removing content", shipped a delta file, and publishes in CSV, JSON-LD, RDF, TTL and XML. It applies green labels as an overlay, using an ML classifier plus expert agreement rules (CA-030, CA-031).
- **SFIA:** three-year major cycle; a change tracker; consultation workshops; explicitly "not a catalogue of tools"; SFIA 10 in open development since mid-2026, with participants proposing a stable core with more frequently updated plug-ins (CA-034, CA-035).
- **Lightcast:** 4-week taxonomy releases with a 120-day support window per release (CA-041).
- **Australian Skills Classification:** "no longer actively maintained by Jobs and Skills Australia", with data current to December 2023. This is a cautionary case of a national taxonomy outliving its funding (CA-036).
- **UK SSC:** beta in November 2025, version 1 with API in 2026, promising "regular" updates, with governance details not yet public (CA-038, CA-039).
- **OSMT/RSD:** moved from WGU's Open Skills Network to Credential Engine (Feb 2025) to secure a long-term home (CA-043).

**Verdict.**
- **Retire** the task-sequence-as-governance and spreadsheet-as-database model.
- **Change** to repo-native governance: GitHub data files as the single source of truth with build provenance (DE), decision records, issue-based change requests, a codebook with versioned rules, semantic versioning per layer (different cadences for core, tools and signals), persistent IDs with Withdrawn/Replaced status, and a delta file per release.
- **Carry** the change log's history and the provenance-marking instinct.
- **Retire** unsupported public claims now.
- AS owns the long-term stewardship question that the Australian case raises. [J]

---

## 15. What each element serves downstream

| v1 element | HR classification & hiring (FH/SL) | Training & upskilling (LC) | Curriculum & accreditation (LC) | Workforce strategy & forecasting (LM/FS) | Mobility (CM) | Change monitoring (IA) | Validation (IO) | v2 home |
|---|---|---|---|---|---|---|---|---|
| Domains / skill areas | navigation | navigation | navigation | reporting rollups | — | — | — | Reference facet + modules |
| Competency title/description | ● needs typing | ● | ● | ○ | ○ | mapping target | ● | Core competency layer |
| Tasks | ● (job analysis) | ● | ○ | ● (exposure) | ● (overlap) | ● (NLP target) | ● | Task layer |
| Proficiency levels / indicators | ● but not usable as-is | ● | ● | — | ○ | — | ● (key gap) | Level scale + anchored indicators |
| Sector applications | — | ○ | ○ | — | ● but unstructured | — | — | Role variants + enactment notes |
| Craft primary | — | ○ | ○ | ○ | ● intended, not delivered | — | ○ | Craft weights on tasks → profiles |
| Families | ○ | ○ | ● (programs) | ● (rollups) | ○ | — | — | Job families of role profiles |
| Workflow stages | — | ○ | ○ | ○ (permitting) | — | — | — | Work-function facet on tasks |
| Reform flags | — | — | — | ● | — | ● | — | Change-signal events |
| Exposure + CLD | ○ (PD rewrite) | ● | ● | ● | ○ | ● | ● (needs IRR) | Assessment records + computed indicators |
| Stability tier | — | — | — | ○ | — | — | — | Computed indicators |
| Ethical lenses | — | ○ | ● | — | — | — | ○ | Quality rubric + facet |
| Domain 7 | ○ | ● | ● | — | ● (transversal) | — | ○ | Transversal practice layer |
| Family→SOC crosswalk | ○ | — | ○ (CIP–SOC) | ● | ● | ● | — | Crosswalk layer (role- and task-level) |

● = primary use; ○ = secondary use; — = little use. [J]

---

## 16. Architectural principles I will apply in Phase 3 synthesis

1. **Type every entity by what kind of thing it is.** Work (task) vs worker attribute (competency, knowledge, transversal practice) vs context (role, sector actor, subsector) vs event (change signal, assessment) vs mapping (crosswalk).
2. **Store judgments as attributed, dated assessments, not as attributes.** Exposure, craft weights, family relevance and lens triggers all record who said what, when, by what method, and how confident.
3. **Compute summaries; don't store them.** Stability, modal exposure, breadth (zero-Core), CLD at competency level and dashboard counts are computed views.
4. **Let different layers change at different speeds.** Reference vocabularies change slowly (annual or less); core competencies annually; tasks and roles semi-annually; tools monthly; change signals continuously; crosswalks track upstream releases (O*NET quarterly, ESCO, OPM).
5. **Federal and state first, nobody shut out.** The first products are federal and state role profiles and crosswalks. The sector-actor vocabulary, subsector modules and Tribal protocol exist from day one so later actors join without restructuring.
6. **Keep depth in modules and simplicity in the core.** SMEs get depth inside subsector modules. Users get a small, stable core and a few computed views. This is my standing answer to the depth-versus-usability tension. [J]
7. **No public claim ahead of evidence.** Every published number carries its evidence tier (v1 analyst / panel-validated / externally benchmarked).

---

## 17. Issues outside my area that affect the vision

- **Stewardship risk is real and has precedent.** The Australian Skills Classification is no longer maintained (CA-036). AS should treat "who maintains this in year five" as a design input, not a later question.
- **Federal occupational churn.** OPM series consolidation runs through September 2027 (CA-044). FH should advise whether EMST can be a reference input to the later "skills-based workforce frameworks" phase. That would be a major adoption route.
- **Claims hygiene.** CP and AS should help retire or reword v1 public materials (Flourish story, GitBook drafts) before the NGO pilot.

---

## 18. Open questions I will resolve in Phase 3 (with the role whose evidence decides)

1. Top level: function-based, subsector-based, or both as orthogonal facets? (DB, SC, FC, DC)
2. Craft as task-level weights: can raters do it reliably? (IO with FC, DC, SC)
3. Competency grain: target size and typing rules. What makes something a core competency vs a task vs a tool? (IO, LC, DC)
4. Role layer: how many role profiles are needed for a federal and state MVP, and at what grain (OPM series × grade band? function × level)? (FH, SL, CP)
5. Proficiency: generic responsibility levels plus anchored indicators, or competency-specific levels only where practiced? (IO, LC, FH)
6. Exposure: which external task-level measures to ingest, and how to reconcile them with v1 analyst values? (LM, IA)
7. Sector actors: role variants vs separate roles; Tribal representation. (SL, PS, TN, CM)
8. Governance: core-plus-modules stewardship, release cadence, host. (AS, DE, IA)

See `docs/research/chief-architect/architecture_hypotheses.md` for the options and the full per-role question list.
