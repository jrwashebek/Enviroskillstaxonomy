# EMST v2: Career Mobility, Theory of Change & Workforce Voice (CM). Phase 2 Report

**Role:** Career Mobility & Theory of Change Lead, convening the Workforce Voice & Cross-Sector Practitioner Panel (CM)
**Date:** 2026-10-23 · **Status:** Phase 2 findings for the Chief Taxonomy Architect (CA)
**Labels:** [E] evidence (CM source IDs in `sources.csv`), [J] expert judgment, [S] speculation.

**Simulated-voice notice.** An AI agent simulates the Workforce Voice panel in this phase. Everything below about workers'
experience comes from *published* evidence and is labelled. Nothing here speaks for practitioners, Tribal nations or any
community. The real panel is designed in `practitioner_panel_design.md`, and its first job is to correct this report.

---

## 0. Summary

**Verdict on the theory of change.** "If craft blends are visible and portable, mobility follows" is **necessary but not sufficient,
and its weakest link is 'visible'.**

1. **Visibility on its own rarely moves people.**
   - Only 37% of firms that announced skills-based hiring followed through. The net effect was fewer than 1 in 700 hires (CM-011) [E].
   - Removing degree requirements alone added about 2 percentage points of non-degree hires (CM-014) [E].
   - Colorado rewrote ~80% of its classifications, yet its share of hires without degrees stayed flat at 25% (CM-012) [E].
   - Skills frameworks report uptake, not mobility: national systems (ASC, ESCO), NICE and the LER pilots (CM-020–CM-027) [E].
   - What moves hiring is embedding skills **in the instruments that gate movement**: credential mapping, applicant tracking, trained managers, assessed qualifications (CM-014, CM-050) [E].
2. **Portability is mostly a property of institutions on a pathway, not of skills.** The frictions are qualification gates, appointment type, pay and retirement systems, licensure, geography and demand [E/J, §2.3].
3. **In 2025–26 the binding constraint is demand and the destruction of on-ramps, not invisibility.**
   - The federal workforce fell 12%. The Forest Service and the National Park Service each lost more than a quarter of staff (CM-028) [E].
   - Non-fire seasonal hiring stopped for a season (CM-039) [E], and AmeriCorps-funded corps were cut (CM-043) [E].
   - Work is moving between sector actors faster than people are: federal sites are going to counties and state agencies (CM-029, CM-034) [E].

**What the computation shows** (v1 family tags; preliminary, single-analyst data):
- v1's 15 families form **two islands**: a field/science cluster and a statecraft/human-systems cluster. **None** of the 33 above-chance family links crosses between them, and the split holds in 150/150 community-detection runs [E: computed].
- **Field craft is the hardest blend to enter.** Other families hold, on average, 7.6% of a field-dominant family's Core requirements, versus 15.9% in the reverse direction [E: computed].
- The gaps from field into statecraft families are dominated by **one teachable bundle**, the D5.2 collaboration competencies: stakeholder analysis, facilitation, collaborative decision-making, conflict resolution and partnerships [E: computed].
- The most portable competencies are where AI is compressing entry tasks. 36% of the top-25 bridges carry career-ladder-destruction (CLD) flags, against 28% overall [E: computed].

**Restated, testable theory of change** (`logic_model.md`) [J]: blends made visible *in gate instruments*, plus reduced frictions on
*demand-backed pathways*, increase cross-actor movement and knowledge retention, and so protect environmental work where it is
co-delivered or devolved.

**Expansion gates** (`metrics_framework.csv`):
- **G1 (NGO pilot → federal/state):** "does this help me?" pass rate ≥70% overall and ≥60% in *every* stratum; real-artifact use at ≥50% of pilot orgs; pathway view validated against observed moves (AUC ≥0.70) or labelled exploratory; partner commitments; zero misuse.
- **G2 (→ whole sector):** a credible contribution story for higher cross-actor hire rates versus comparison units; no widening of equity gaps; gate-instrument integration in ≥2 federal agencies and ≥5 states; five years of stewardship funding.

---

## 1. Scope, method and limits

**What I did.**
- Read CHARTER, TEAM_BRIEF, the v1 database and normalized baseline, v1 family definitions, Five Functional Positions, the Structural Conditions and fire workforce syntheses, the CLD registers, and CA's audit and hypotheses.
- Computed a reproducible transferability analysis (`transferability_analysis.py`).
- Reviewed published evidence on skills visibility and mobility, structural barriers, and worker experience.
- Built the logic model, metrics, personas and panel design.

**Limits that matter.**
- **The search budget ran out partway through.** The team-wide web-search limit was exhausted after 11 of my searches. Many direct fetches were then declined by the permission gate. Blocked:
  - journals.plos.org and royalsocietypublishing.org (Dawson et al.; del Rio-Chanona et al.);
  - grassrootswildlandfirefighters.com, diversegreen.org (Green 2.0) and data.opm.gov;
  - gao.gov, hbs.edu, nga.org, bcg.com and Colorado's dashboard.

  I read 24 external pages and 11 v1/internal documents. I also cross-reference 23 sources that other roles read and recorded (FH, FC, FS, AS); `sources.csv` marks each "not re-read by CM" and names the role that read it. Method claims about the labor-economics similarity literature are therefore **[J]** (professional knowledge, not re-verified), and fire and diversity lived-experience evidence is thinner than it should be. This is a gap, not a finding about the world.
- **v1 secondary syntheses** (CM-007, CM-009, CM-072) carry unresolvable citation placeholders. I use them only as weak secondary evidence ([E-weak]).
- **No new primary data.** No career-history data were available, so no transferability claim here has been validated against an observed move. That is the central methodological gap (§3.5).

---

## 2. Testing the theory of change

### 2.1 The claim, decomposed

The charter's sentence (CM-001) bundles four causal links. Each needs its own test (full table of assumptions A1–A12 in `logic_model.md`):
- visibility → recognition (by workers and by employers);
- recognition → movement;
- portability (the rules allow the move);
- mobility → environmental outcomes.

### 2.2 Evidence that visibility and skills-based approaches increase mobility

**Skills-based hiring outcome studies.** This is the strongest evidence base, and it mostly says *announcement ≠ practice*.

- **BGI and Harvard Business School (Feb 2024):** 11,300 roles at large firms (CM-010, CM-011) [E].
  - Only 3.6% of roles dropped a degree requirement.
  - In those roles, the share of hires without a degree rose about 3.5 percentage points.
  - The net effect was 0.14 percentage points: fewer than 1 in 700 hires in 2023.
  - Of firms that announced changes, 37% were "leaders", 45% changed "in name only" and 18% "backslid".
- **BGI and OneTen, "Credential Fluency" (Mar 2026):** more than 1,000 employers; I read a secondary summary (CM-014) [E].
  - Removing degree requirements alone raised non-degree hiring by about 2 points.
  - Firms in the top decile of credential fluency were 11 points more likely to hire credentialed workers. Credential fluency means mapping credentials to roles, building them into applicant tracking, and training hiring managers.
  - **This is the most important single finding for EMST:** the lever is operational embedding, not publication.
- **US state governments:**
  - At least 26 states have dropped or reduced degree requirements. 61% of state postings still require a degree, versus 70% in the private sector (CM-013) [E].
  - Pennsylvania de-degreed ~92% of positions, and ~60% of new hires lack a degree (CM-013) [E].
  - Colorado devoted $700k and three staff and rewrote ~80% of its classifications. Yet the share of hires without degrees stayed at 25% (1,588 people) in both 2023 and 2024 (CM-012) [E].
  - Maryland and Pennsylvania track applicants, not hires, so their outcomes cannot be measured (CM-012) [E].
  - Practitioners name the barriers: managers still prefer degrees; job descriptions must be rewritten by hand; job seekers must learn to articulate skills in employers' terms; and laid-off federal staff are bringing degree filters back (CM-012) [E].

**Learning and employment records (LERs) and digital credentials.** Pilots report technical portability and badge counts, not hiring or mobility outcomes [E].
- A JFF pilot produced 476 accounts and 1,936 badges. Employers met the badges "with confusion" (CM-019).
- University of Phoenix ran a wallet hand-off test with a ~30-student focus group (CM-018).
- The original LER white paper lists IBM, Walmart and Salesforce pilots without metrics (CM-017).

**National skills systems.**
- **SkillsFuture** is the one system with outcome studies [E]:
  - Work-Study Programme graduates earned ~9% more than comparable graduates after 1–2 years, falling to ~6%. Certificate graduates earned ~11% more, and the premium was sustained (CM-015).
  - Earlier studies found a 5.8% premium for WSQ training (CM-016).
  - The comparison groups are matched but not causally identified. These are evaluations of *training programmes*, not of the skills framework as a mobility instrument.
- **Australia:** the Australian Skills Classification was decommissioned after its December 2023 update. Its successor, the National Skills Taxonomy, is still in consultation (CM-020, CM-021) [E]. Australia's two transition-similarity tools were never validated against observed moves:
  - the ASC "Skills Transitions" (BERT embeddings plus cosine similarity; CM-022);
  - *Reskilling Australia* (2019), which used cosine ≥0.8 on O*NET plus job ads and found "viable transitions" for 96.4% of workers in declining jobs (CM-023).
- **ESCO** measures success by downloads, user mix and qualifications covered. Greek public employment services use it for profiling, but their two-way matching tool had not launched by mid-2025 (CM-024, CM-025) [E].

**NICE Framework adoption.** NIST treats adoption as a line of inquiry (CM-026) [E]. The only quantitative outcome claim I found is a vendor survey: firms aligning to NICE were "57% more likely" to be satisfied with filling roles (370+ leaders, self-report, correlational; CM-027) [E, Low quality]. **NICE is a good model for versioning, not evidence that frameworks increase mobility** [J].

**Assessment.** No study I found shows that publishing a skills framework, on its own, increased movement between employers or
sectors [E: absence across CM-010 to CM-027]. The positive evidence comes from programmes that combine a framework with training
(SkillsFuture) or with hiring operations (credential fluency; Pennsylvania-type rule changes paired with new practice). **EMST's
theory of change must therefore run through the gate instruments** (FH and SL lanes) and through learning paths (LC lane) [J].

### 2.3 Counter-evidence: barriers are structural

| Barrier | What I could establish | Label |
|---|---|---|
| **Minimum qualifications and degree screens** | Federal "positive education" requirements hard-code degree or credit requirements in 0460 Forestry, 0482, 0486 Wildlife Biology, 1315, 1340 and 1360 (CM-007, secondhand). State classifications still require degrees in 61% of postings (CM-013) | [E-weak]/[E] |
| **Assessment format** | Federal hiring is moving from self-ratings to technical assessments: USA Hire expands from 138 to 412 series, and 34.3% of delegated-examining announcements used technical assessments in FY26 Q2 (CM-050). Merit Hiring Plan essay questions are in litigation (CM-051). Assessments can *help* mobility if their content is competency-based, which is EMST's best federal lever | [E] |
| **Seasonal and temporary appointments** | No non-fire seasonal hiring at USFS in 2025; 2,000 seasonals committed for 2026, all titled forestry technician, with short application windows (CM-039, CM-041) | [E] |
| **Pay and benefits** | ESG and finance-adjacent roles pay on private norms and can drain experienced public staff (CM-007, secondhand). Federal–state retirement portability (FERS vs state defined-benefit vesting) is a plausible major friction for mid-career moves, but **not evidenced this session** | [E-weak]/[J] |
| **Licensure and certification** | Fire's NWCG qualifications are portable across federal, state, Tribal and contract fire. Federal fire qualification standards align from January 2027 (CM-049). Professional engineer, geologist, state forester and water-operator licences are not evidenced this session (DB's lane) | [E]/[J] |
| **Veterans' preference** | 27.9% of federal staff are veterans (CM-028). Preference shapes federal referral lists; its effect on cross-actor movers is not evidenced here | [E]/[J] |
| **Security clearance and citizenship** | Relevant to defence and energy environmental roles; not evidenced this session | [J] |
| **Geography and housing** | Remote, costly duty stations limit who can take field roles. GAO and USDA documents are cited secondhand (CM-007); the GAO report itself was blocked (CM-063) | [E-weak] |
| **Networks** | Open calls over-recruit the networked. Referral hiring dominates small NGOs and consultancies; not evidenced here | [J] |
| **Discrimination and inclusion** | Green 2.0's 2024 report recorded the first decline in staff of colour at NGOs (CM-007, secondhand; Green 2.0 blocked, CM-061). The leadership "green ceiling" is long documented (CM-070, secondhand) | [E-weak] |
| **Demand** | Federal: 386,826 separations vs 122,598 accessions to January 2026, against ~250,000 hires in a typical year (CM-028). States: Colorado and Maryland froze hiring in summer 2025 (CM-012) | [E] |
| **Tenure and accountability regime** | Schedule Policy/Career moved ~8,000 positions, 97% at GS-15 and above (CM-052). Final RIF regulations were issued in September 2026 (as recorded by FH) | [E] |

### 2.4 The 2025–26 context: forced mobility and devolving work

The theory of change imagined *pull* mobility: people choosing moves that blends make visible. The evidenced reality of
2025–26 is ***push* mobility and devolution of work**:
- **People pushed out.** The federal workforce fell from 2,313,216 (September 2024) to 2,035,344 (January 2026), a 12% drop (CM-028) [E].
  - Separations included 136,822 deferred resignations and 10,436 reductions in force (CM-028) [E].
  - Probationary firings hit early-career trail crews, biologists, NEPA coordinators and wilderness rangers (CM-035) [E].
  - The Forest Service lost about 6,000 employees in 2025 (CM-029, citing NRDC) [E].
- **Work moved between actors.** The Forest Service turned to state and community partners (CM-034) [E].
  - Pitkin County will run the Maroon Bells Scenic Area from 2027 (CM-029) [E].
  - Colorado Parks and Wildlife took Sweetwater Lake in 2024 (CM-029) [E].
- **States and partnerships tried to absorb people.** States recruited displaced federal staff (CM-045) [E], and a partnership formed to place them in state and local government (CM-044) [E].

**Implications** [J]:
- The most urgent mobility job is **translation and crediting** for people already moving: "what is my work called there, and does it count?" Recommending new moves comes second.
- **Knowledge continuity** is a mobility outcome in its own right. When work changes hands between actors, the knowledge has to move even if the person doesn't.
- The 2025–26 displacement is a **natural experiment** for validating transfer models. Aggregate data on federal→state hires by former series and new class (P-CM-12) would be the first real validation set EMST could get.

### 2.5 Verdict

| Link | Holds? | Why |
|---|---|---|
| Visible blends → workers recognise their transferable skills | **Plausible, untested** | Practitioners say articulation is a barrier (CM-012) [E-weak]; must be tested with the panel (M-09) |
| Visible blends → employers hire across actors | **Does not hold on its own** | Announcement ≠ practice (CM-011, CM-014) [E]; holds only when embedded in gate instruments (A3′) |
| Portability | **Partly holds, varies by pathway** | Fire qualifications portable; positive-education, appointment and pay frictions real; retirement portability unverified |
| Mobility → environmental outcomes | **Unevidenced** | The need is evidenced (devolution, skill loss: CM-029, CM-040); the effect is [S] |
| Entry pipelines replenish field craft | **Currently failing** | On-ramps cut (CM-039, CM-043); under-30 share 7.9% (CM-028) [E] |

The theory of change is worth keeping as a north star. It should be **operated as the conditional version** in `logic_model.md`, with
contribution analysis and a pre-registered failure condition. If no targeted pathway shows a documented artifact chain after 12
months and the panel's usefulness test fails, the pathway features stop at the pilot.

---

## 3. Transferability: methods and a preliminary computation

### 3.1 Methods review (judged, not summarised)

All of the following are [J] unless cited. The primary papers were blocked this session (CM-057–CM-059); my judgements rest on
professional knowledge of this literature.

- **O*NET-based skill distance** (cosine or Euclidean distance on importance/level vectors across 35 skills, knowledge areas and work activities).
  - *Strengths:* public and comparable across occupations.
  - *Weaknesses:* coarse. Generic skills dominate, so most professional occupations look similar. It is symmetric, but real transitions are not. It is rarely validated, as the two Australian deployments show (CM-022, CM-023) [E].
- **Skill-driven recommendations (Dawson, Williams & Rizoiu 2021; CM-057).** They use revealed-comparative-advantage weighting, so each skill's importance is relative to how common it is. The measure is asymmetric, and it is validated by predicting observed transitions in career data.
  - *Lesson for EMST:* **weight by specificity, model direction, and validate against observed moves.**
- **Occupational mobility networks (del Rio-Chanona et al. 2021; CM-058).** Edges come from *observed* CPS occupation-to-occupation flows, not skill similarity. The network's structure shapes how shocks propagate into unemployment.
  - *Lesson:* revealed flows beat inferred similarity where flows can be observed. Similarity is needed where flows are sparse (new roles, small occupations, sector-actor variants invisible in SOC data).
- **Frank et al. (2019; CM-059)** argue that skill-network structure and local labor-market context constrain mobility.
  - *Lesson:* add place and demand to any pathway score.
- **Worker-flow data.** CPS occupation transitions (EC-CM-03) and LEHD Job-to-Job flows by sector (EC-CM-02) exist. OPM Federal Workforce Data, monthly since January 2026, has separations and accessions by series (CM-054).
  - *Weakness:* SOC and NAICS codes cannot see sector-actor *variants* of the same function, such as a state permit writer versus a consulting permit writer [J].
- **Career histories (LinkedIn, Lightcast, Revelio).** These give rich role-to-role transitions.
  - *Weakness:* coverage is biased against field, seasonal and rural workers. Those are exactly EMST's hardest pathways [J].
- **Career-lattice network analysis.** Useful for describing lattices and finding bridges and gatekeeper roles. It is only as good as the edges.

**Methodological conclusion** [J]: no single basis is sufficient. EMST needs:
- importance-weighted, asymmetric **task overlap** on its own role profiles;
- adjusted by **friction penalties** and **local demand**;
- **calibrated and validated against observed moves** wherever they can be found.

### 3.2 What I computed

**Input.** v1 family tags: 222 competencies × 15 families; 1,002 assignments (247 Core, 755 Supporting), cross-checked against `data/v1_baseline/family_assignments.csv` with 0 mismatches (CM-003, CM-004). Also craft primary/secondary and CLD flags.

**Measures.** Weights are Core = 1 and Supporting = 0.5.
- **Primary:** weighted Jaccard, Σmin/Σmax.
- **Alternatives:** cosine, and a specificity-weighted Jaccard using idf = ln(15 / number of families tagging the competency).
- **Sensitivity:** Supporting weight 0.25 or 0.75; Core-only.
- **Null model:** 2,000 permutations that preserve each family's tag counts, reported as a z-score. This controls the size effect, since large families otherwise look similar to everything.
- **Directional coverage:** the share of a destination family's Core competencies the origin holds, scored 1 for Core and 0.5 for Supporting.
- **Communities:** Louvain clustering (seeded), checked for stability over 150 runs and against hierarchical clustering. Betweenness is computed on a backbone that keeps only edges with z > 2.
- **Bridging score:** each competency's contribution to between-community similarity.
- **Craft blend per family:** primary craft weighted 1, secondary 0.5, with evenness as normalised entropy.

**Outputs:** `family_similarity_matrix.csv`, `family_pairs.csv` (all 210 ordered pairs with every measure and the destination-Core gap list), `bridging_competencies.csv`, `family_craft_blend.csv`, `transferability_summary.json`. The script is deterministic: identical hashes across reruns.

### 3.3 Results

**1. Two islands** [E: computed].
- The **field/science** cluster is F1 Forestry, F2 Wildlife & Fisheries, F3 Ecological Restoration, F4 Water, F5 Conservation Science, F6 Climate, F7 Data Science, F10 Sustainable Agriculture and F12 Fire.
- The **statecraft/human-systems** cluster is F8 Policy, F9 Land Use Planning, F11 Education, F13 Environmental Health & Justice, F14 Corporate Sustainability and F15 Conservation Finance.
- Co-assignment was ≥0.67 within clusters and **0.00 between them** across 150 Louvain runs. At a finer resolution, the field cluster splits into a field-management core {F1, F2, F3, F4, F10, F12} and a science/data group {F5, F6, F7}.
- **All 33 above-chance family pairs fall within a cluster.** The best cross-cluster pair, Conservation Science–Environmental Policy (J = 0.21), sits *at or below chance* (z = −0.9).
- Strongest links: Forestry–Restoration (J = 0.62, z = 14.1), Forestry–Fire (0.45, z = 12.4), Wildlife–Water (0.52, z = 11.3), Policy–Planning (0.47, z = 11.1).
- Modularity is modest (0.16) because generic competencies connect everything at low weight. The *beyond-chance* structure, however, is fully split.

**2. Direction matters, and field craft is the hard direction to enter** [E: computed].
- Coverage between clusters:
  - field families already hold **14.3%** of statecraft families' Core;
  - statecraft families hold **6.1%** of field families' Core.
- Into field-dominant families (F1–F4, F10, F12), other families hold **7.6%** of Core, versus **15.9%** in the reverse direction.
- Examples:
  - Forestry holds 36% of Climate Science's Core; Climate Science holds 0% of Forestry's.
  - Conservation Science holds 50% of Environmental Health & Justice's Core; the reverse is 18%.
  - Environmental Policy is missing 10 of 11 Wildlife & Fisheries Core competencies (population dynamics, survey techniques, species identification and so on).
- This matches the Structural Conditions view of field craft as a place-based, mentorship-dependent "reproduction regime" (CM-007; CA audit CM-071) [J]. **Pathways *into* field roles must be built (seasons, corps, apprenticeships); they cannot just be made visible** [J].

**3. Blends are asymmetric** [E: computed].
- Field-management families (F1–F4, F10, F12) have even three-craft blends (evenness 0.91–0.99). For example, Forestry is FC 38 / DC 38 / SC 24, and Fire is FC 47 / DC 33 / SC 20.
- Statecraft-cluster families hold almost no field craft: FC 0.7–6.9% (Policy 1.4%, EH&J 0.7%, Corporate Sustainability 4.3%).
- Environmental Data Science is DC 68%.
- The charter's "blend of three crafts" describes *field professionals* in v1's tags. It does not describe policy, ESG, finance or education professionals. Either those roles really lack field craft, or v1 under-tagged it. That is a question for FC and the panel [J].

**4. Craft blends cannot be the similarity basis** [E: computed].
- Blend vectors correlate 0.74 (Spearman) with task-overlap similarity, so they capture the two-island split.
- But they cannot separate destinations within an island: 31% of family pairs have blend cosine ≥0.95. Forestry, Restoration and Water are effectively identical by blend.

**5. Bridging competencies** [E: computed].
- **Cross-cutting (Domain 7).** These are the top seven bridges, 54% of cross-community Core bridges: 7.1.3 Regulatory professional integrity; 7.1.4 AI governance; 7.2.2 Designing for tacit-knowledge formation; 7.1.1 Indigenous data sovereignty; 7.2.3 Calibrating judgment with AI; 7.1.2 Intervention authorisation; 7.2.1 Validating AI outputs.
  - **Caveat:** they were designed and tagged as cross-cutting in February 2026, so their bridging is partly built in. They are not independent evidence of portability.
- **Broad management foundation.** 3.1.1 Project planning, 3.1.2 Budget and 3.1.3 Risk are Core in *no* family but Supporting in 10. These are the most portable working skills in v1, and they are invisible in Core-only views.
- **Statecraft connectors:** 5.3.2 Indigenous knowledge integration (handled only on holders' terms; TN); 5.2.5 Partnerships; 6.1.2 Compliance; 6.1.4 NEPA; 6.5.1 Tribal consultation; 6.5.2 Federal-state-local coordination.
- **Data-craft connectors:** 2.4.3 Decision support; 2.1.1 GIS (broad foundation); 6.3.2 Ecosystem-services assessment (the only Core bridge into Conservation Finance); 1.5.4 Carbon cycle science.

**6. One bridge kit closes most of the field→statecraft gap** [E: computed; J on design].
- From Fire, Wildlife and other field families into Policy and Planning, the missing destination-Core list is led by the same five competencies: 5.2.1 Stakeholder analysis, 5.2.2 Facilitation, 5.2.3 Collaborative decision-making, 5.2.4 Conflict resolution and 5.2.5 Partnerships. Regulatory basics (6.1.x) follow.
- Fire holds **0 of 13** Land Use Planning Core competencies. Yet v1's own definitions name Fire–Planning overlap in community wildfire protection planning (CM-005). That is a likely tagging gap on a high-demand pathway (v1_assessment).
- A "collaboration bridge kit" is a concrete, testable first learning path (P-CM-06, LC lane).

**7. Portability and entry-level compression coincide** [E: computed from v1's single-analyst CLD].
- CLD flags cover 28% of competencies overall, but:
  - 36% of the top-25 bridges;
  - 50% of the broad-foundation competencies (including 3.1.2 Budget, rated High);
  - 37% of statecraft-primary competencies, versus 20–22% for field and data craft.
- Families with the highest share of CLD-flagged Core: Education 50%, Conservation Finance 44%, Planning 38%, Data Science 33%, Policy 27% (five High or Highest).
- **The entry tasks that teach the most transferable skills are where AI is compressing learning first** [J: v1's flags need LM's external corroboration]. Mobility and CLD are the same problem seen from two ends.

**8. Tagging artifacts the computation exposed** [E: computed].
- Generic digital collaboration competencies (2.5.1 Virtual meetings, 2.5.2 Document management, 2.5.3 Project management software, 2.5.5 Workflow design) are tagged *only* to Environmental Data Science. That makes data craft look non-portable when these are everyone's tools.

### 3.4 Pathway examples (from `family_pairs.csv`)

| Origin → destination | Coverage of destination Core | Reverse | Main gaps |
|---|---|---|---|
| Forestry → Fire | 70% | 55% | none (Fire's Core fully held at ≥ Supporting) |
| Fire → Forestry | 55% | 70% | 1.3.2 Mensuration; 1.3.5 Timber planning; 4.7.2 Urban forestry |
| Fire → Land Use Planning | 0% | 5% | all 13: 5.2.1–5.2.5; 6.2.1 Comprehensive planning … |
| Wildlife → Policy | 25% | 9% | 16/30: 5.2.1–5.2.5; 6.1.1 Policy analysis … |
| Conservation Science → Policy | 42% | 23% | 11/30: 6.1.2 Compliance; 6.1.3 Permitting; 6.1.5 Enforcement; 6.4.2 Drafting … |
| Corporate Sustainability → Climate | 18% | 21% | 7/11: 1.5.3 Adaptation planning; 1.7.3 Refugia … |
| Education → EH&J | 32% | 20% | 6.7.1 Risk assessment; 6.7.2 EJ screening; 6.7.4 Toxicology … |

### 3.5 Limits, stated honestly

1. **Single analyst.** Tags were assigned by one analyst with an LLM, with no inter-rater reliability. The structure is only as good as the tags (CM-003).
2. **Families are not jobs.** Similarity between disciplinary identities is not similarity between jobs a person could move between. There is no role, level, time share or importance.
3. **No sector-actor dimension.** All 1,110 sector notes are filled in, so they carry no signal. **v1 cannot compute the charter's question:** mobility between federal, state, local, Tribal, NGO, private and academic employers.
4. **The Core definition encodes distinctiveness.** It asks what is distinctive to a professional identity (CM-005), so Core-only similarity understates transfer by design. Core-only rankings correlate only 0.51 with Core+Supporting rankings. The results therefore depend on Supporting tags, which were assigned more loosely.
5. **Domain 7 bridges partly by construction.** See §3.3, point 5.
6. **Public-lands skew.** Water and wastewater, air, waste and energy have no families (CA audit).
7. **No validation.** Nothing here has been tested against an observed move. Treat every number as a **prior** to be replaced by role-level, validated measures (M-03).

What survives these limits [J]: the *direction* of the field-entry asymmetry and the collaboration bridge-kit pattern. Both match independent reasoning about how field craft is learned, and both are cheap to test with the panel's career histories.

---

## 4. Metrics and expansion gates

Full definitions are in `metrics_framework.csv` (30 metrics, each with level, data source, baseline method, threshold, the decision it informs, collection burden and label). The thresholds are proposals that the real panel must co-sign before the pilot (M-28).

**Gate G1: NGO pilot → federal and state agencies.** All of the following must hold:
- M-06 "Does this help me?" ≥70% overall and **≥60% in every stratum**. The panel holds a veto.
- M-07 ≥80% task completion; SUS ≥68.
- M-08 EMST IDs used in a real gate artifact at ≥50% of pilot orgs; ≥30% repeat use.
- M-03 pathway view validated (AUC ≥0.70 and beating naive baselines by ≥0.05), **or** shipped labelled "exploratory".
- M-02 friction register complete for every pre-registered pathway.
- M-05 Section 508/WCAG and privacy clearance.
- M-10 at least 2 federal and 3 state partner agreements.
- M-11 zero misuse incidents.
- M-28 panel ratification by majority within every stratum.

**Gate G2: federal/state → whole sector.** All of the following must hold:
- M-14 cross-actor hire rate up against comparison units, with a documented artifact chain and an external reviewer rating the contribution story "credible".
- M-15 and M-16 movers' time-to-productivity and 12-month retention at parity or better.
- M-17 **no widening** of equity gaps; early-career, seasonal and corps strata at parity.
- M-18 EMST IDs in live artifacts at ≥2 federal agencies and ≥5 states; ≥80% crosswalk coverage of targeted series and classes.
- M-19 no entry role on a pilot pathway below the formation-task threshold without mitigation.
- M-25 adopters in ≥5 actor types. Tribal participation follows TN's protocol and is never a target to hit.
- M-29 at least five years of stewardship funding.
- M-30 quarterly refresh of the change-signal pipeline.

**Leading indicators to watch from day one:**
- M-20 entry-cohort volume: seasonal, corps, apprentice and trainee starts vs 2024. A fall of more than 25% triggers a field-pathway warning.
- M-26 portability of posting language.
- M-27 degree-only screens on target pathways.

**Why these gates hold the team to outcomes** [J]:
- Every G1 item is a behaviour (task completion, real artifacts, validated predictions) or a safeguard. None is a count of things the project built.
- G2 requires a *contribution story* tested against rival explanations X1–X8 (`logic_model.md` §4): freeze lifting, hiring reform, grant cuts, AI and labour-market slack.

---

## 5. Workforce Voice synthesis (published evidence only)

### 5.1 Federal and state employees in transition
- **Scale and composition** [E]:
  - 386,826 federal separations and 122,598 accessions to January 2026; Forest Service, NPS and CDC each down more than 25% (CM-028).
  - About 317,000 departures in 2025: deferred resignation ~144k, attrition ~129k, involuntary ~24k (CM-037, as recorded by FH).
  - USFS: about a quarter of the non-fire workforce left by May 2025 (CM-034); the workforce fell 16% in 2025 (CM-038); White River NF went from 169 to 111 year-round staff (CM-029).
  - NPS lost about 1,700 staff (~9%) in early 2025 (CM-056).
  - Proposed legislation cites a 17% loss across public-land agencies (CM-053).
- **Who went first** [E]: probationers, meaning early-career staff. Firings of at least 3,400 at USFS and about 2,300 at DOI included trail crews, biologists, NEPA coordinators and wilderness rangers (CM-035).
- **Where people went:**
  - States recruited displaced federal staff, and a partnership formed to place them in state and local government (CM-044, CM-045) [E].
  - USFS later asked resigned workers to come back for fire season (CM-042) [E].
  - No public data show how many actually moved or into which roles. **This is the largest evidence gap for the theory of change**, and a data request EMST can make (P-CM-12).
- **Employee organisations** [E]: unions are litigating hiring-process changes (AFGE v. Kupor; CM-051). Bills propose a RIF moratorium for public-land agencies (CM-053). NFFE and other union statements were not accessed this session.
- **State side** [E]: hiring freezes in Colorado and Maryland (CM-012) mean state staff are absorbing devolved work through upskilling, not new hires (persona 6).

### 5.2 Early-career entry barriers
- The federal under-30 share is 7.9%, against 19.4% of the US labour force (CM-028) [E]. Student-trainee occupations fell (as recorded by FH from CM-028) [E].
- The seasonal first rung was closed in 2025 and reopened narrower in 2026: all positions titled forestry technician, with short application windows (CM-039, CM-041) [E].
- Unpaid internships and access to field experience act as economic filters (CM-007, secondhand) [E-weak].
- AI-exposed occupations show early-career employment declines (CM-069 via CM-009, secondhand; LM's lane) [E-weak].
- v1 flags CLD on 28% of competencies, concentrated in statecraft entry tasks [J: single-analyst] (§3.3).

### 5.3 Conservation corps alumni outcomes
- The Corps Network has 140 member corps and serves more than 22,000 young people a year (CM-031) [E]. Its April 2026 Service to Career framework centres pathway mapping, credentials, post-service placement and alumni supports (CM-032) [E].
- **No published alumni outcome data were found** on the pages I could read (CM-031–CM-033) [E: absence]. The corps-data page failed to load.
- Disruption [E]: AmeriCorps cuts of $400M; corps hours on the Pacific Crest Trail fell from about 19,000 to about 4,000 (CM-043). FY2026 status is under litigation with a stay to 1 February 2027 (CM-046). Land-trust placements are affected (CM-047).
- Whether noncompetitive federal hiring eligibility for corps service still works in 2026 is **unverified** (also flagged by FC).

### 5.4 Seasonal and wildland fire workforce
- **Firefighter staffing** [E]: 10,496 firefighters on board against an 11,300 goal, plus about 10,000 non-fire staff with fire qualifications (CM-038).
- **Collateral-duty capacity** [E]: roughly 1,400–1,600 fire-qualified non-fire staff left (CM-036, CM-039). As non-fire field staff shrink, so does the surge "militia".
- **Reorganisation** [E]: the US Wildland Fire Service was stood up in January 2026 (CM-048), with qualification alignment due January 2027 (CM-049). Intra-federal fire mobility should get easier.
- **Lived-experience testimony was not reached.** Grassroots Wildland Firefighters (CM-060) and the GAO barrier report (CM-063) were both blocked, so pay, mental-health and housing barriers rest on secondhand v1 synthesis (CM-007) [E-weak].
- **Fire's qualification model is portable** [J, CM-072]: NWCG Position Task Books give observable, performance-based qualifications that work across federal, state, Tribal and contract fire. This is a **model** for portable qualification in the rest of the sector.

### 5.5 Career movers across sector actors
- **Evidence specific to environmental work is thin** [E: absence]. I found no study of environmental professionals' cross-actor moves. Practitioner reporting from skills-based hiring names the barriers: articulation, manager preference and degree filters (CM-012) [E].
- The private compensation pull toward ESG and finance roles is asserted in v1 (CM-007) [E-weak].
- The computation suggests movement *out of* field roles into statecraft and data roles is easier than movement into field roles (§3.3) [E: computed, unvalidated].

### 5.6 Diversity and inclusion
- Green 2.0 (CM-061) could not be accessed. The 2024 decline in NGO staff of colour is known only secondhand (CM-007) [E-weak].
- No public demographic impact assessment of the 2025–26 federal reductions was found (CM-007 notes the same gap) [E: absence].
- The panel design's equity metric (M-17) and composition targets are built to measure this rather than assume it.

### 5.7 Loss of institutional knowledge
- Named skills were lost in one season: equipment operation and rock masonry, with trail miles maintained down 22% (CM-040) [E].
- Devolved sites change hands (CM-029) [E].
- v1's CLD concept and the Five Functional Positions framework (CM-006) explain the mechanism: the tasks through which juniors learn are the ones being cut or automated [J].
- v1 has **no competency for knowledge continuity across institutional handoffs**, hence candidate CC-CM-01 and the panel's knowledge-capture pilot (method 5.8).

### 5.8 What only real practitioners can tell us
- Whether translation and crediting really is the top need (the cross-persona pattern in `personas.md`).
- Which frictions actually blocked their moves.
- Whether "craft" language means anything to them.
- What they would never put into a tool during a RIF.
- What Tribal professionals need: TN's protocol only, and **no Tribal persona was drafted**.

---

## 6. The real practitioner panel (summary of `practitioner_panel_design.md`)

**Composition.** 28 standing members across eight strata, plus up to 8 rotating subsector seats:
- cross-actor movers (5);
- federal and state staff in transition (5);
- early-career (4);
- corps alumni (3);
- seasonal and fire (3);
- employee organisations (3);
- HR, training and curriculum intermediaries (3);
- Tribal professionals (2 reserved, filled **only** via TN's protocol, otherwise left empty).

**Cross-cutting targets:**
- at most 40% from forestry, fire and public lands;
- at least 40% rural;
- at least 5 members without a 4-year degree;
- at least 2 veterans.

**Decision rights.** The design makes the panel's answer bind:
- a usefulness veto at G1. CA can override it only with a written point-by-point response and a second vote; if that vote fails, the decision escalates to the project lead;
- stratum quorum on every gate vote;
- practitioner objections that require a written CA response within 15 working days;
- co-signed thresholds;
- reserved Delphi seats, with ratings reported by stratum.

**Methods:** career-history interviews (critical-incident), diary studies, usability sessions on the persona tasks, card sorts, metric sensemaking, misuse red-teaming, and a knowledge-capture pilot.

**Safeguards:** pay for everyone; ethics clearance for federal and state members (CP); anonymity by default; IRB-type review; trauma-informed interviewing; data minimisation.

---

## 7. Answers to CA architecture questions (§6 of `architecture_hypotheses.md`)

### Q1. Which similarity basis predicts real transitions best: task overlap, competency overlap or craft-blend vectors? What does that require of L2 and L3?

**Answer: importance-weighted, asymmetric task overlap on role profiles.** Adjust it for frictions and demand, and validate it
against observed moves. Use competency overlap for *explanation*. Use craft blends to *describe* and *design* pathways (what kind of
learning a gap needs), not to measure similarity.

- **Craft-blend vectors are too coarse** [E: computed]. They separate the two islands (Spearman 0.74 with task-overlap similarity) but not destinations within one: 31% of family pairs have blend cosine ≥0.95. With three dimensions, Forestry, Restoration and Water are indistinguishable.
- **Competency overlap at v1's grain depends on tag semantics** [E: computed]. Core-only and Core+Supporting rankings correlate only 0.51. Distinctiveness-based tags understate transfer.
- **Task overlap** is the grain at which the evidence-backed methods work (RCA weighting, asymmetry, validation; CM-057, CM-058 [J: not re-read]) and at which O*NET joins and flow data become available (CA's Option B).
- **But no inferred similarity is trustworthy until it is validated.** Australia shipped two unvalidated tools (CM-022, CM-023) [E]. Make M-03 a release gate for any "recommended" pathway.

**What this requires of L2 (tasks):**
- persistent task IDs;
- task-to-competency links;
- crosswalks to O*NET tasks and DWAs (to borrow SOC-level flow data);
- career-ladder position (P/C/X) and formation-task flags (for pathway-level CLD).

**What this requires of L3 (roles):**
- per-role **importance and time-share weights** on tasks, and a target level per competency;
- **sector-actor variants** sharing a function ID;
- crosswalk IDs to OPM series, state classes, SOC and private job architectures;
- **entry and progression links** between roles;
- a computed **directional coverage** score as the user-facing measure ("you already hold 42% of this role's core work"), which is more legible than Jaccard;
- a **validation table** of observed transitions at minimal grain (from-variant, to-variant, year, region bucket), stored separately with privacy controls (CP and DE);
- a pathway score of the form similarity × (1 − friction penalty) × local demand, with every component inspectable.

### Q2. Which transfer-friction attributes between sector actors must be first-class?

Each friction is a record on an **actor pair and a pathway (role-variant pair)** with these fields: `friction_type`, `direction`,
`severity` (blocking / costly / minor), `basis` (statute / regulation / policy / practice), `movable_by` (Congress / OPM /
state HR / employer / worker), `mitigation` (e.g. an assessment substitute, an IPA assignment), `evidence_label`, `source_id` and
`as_of`.

Minimum first-class types:
1. **Qualification gate:** positive-education requirements; specialized experience and time-in-grade; state class minimum qualifications. [E: CM-007, CM-013]
2. **Assessment format:** USA Hire or SME-QA technical assessment; essays; state exam; private interview. [E: CM-050, CM-051]
3. **Licence or certification required, and whether it is recognised across jurisdictions:** PE, PG, state forester registration, water and wastewater operator, pesticide applicator, NWCG qualifications. [E for NWCG: CM-049; J for others; DB]
4. **Appointment type and status:** seasonal, temporary or term; competitive status and reinstatement; noncompetitive eligibility (corps, veterans' authorities, Schedule A); probation reset on moving; Schedule Policy/Career. [E: CM-039, CM-052; J]
5. **Pay system and level mapping:** GS or state range vs private; the expected pay delta by level. [J]
6. **Retirement and benefits portability:** FERS deferred annuity; state defined-benefit vesting and service-credit purchase; health coverage continuity. [J: high priority to verify]
7. **Veterans' preference** (federal and state). [E: CM-028 share; J effect]
8. **Security, suitability and citizenship.** [J]
9. **Geography and housing:** duty-station remoteness; relocation support. [E-weak: CM-007]
10. **Seasonality and application windows.** [E: CM-041]
11. **Credential recognition:** corps service, military, Tribal credentials, foreign credentials. [J]
12. **Post-employment and ethics restrictions:** federal-to-private and consulting moves. [J]
13. **Bargaining-unit seniority and benefit loss.** [J]
14. **Information and network access:** where jobs are posted; referral hiring. [J]

Tribal-specific frictions (e.g. Tribal preference in hiring, sovereign HR systems) are **not** defined by CM. TN's protocol
decides what, if anything, the model records [J].

### Q3. Which outcome metrics should decide expansion beyond the pilot, and what data must the model hold to compute them?

The metrics and gates are in §4 and `metrics_framework.csv`. The model (or its governed side stores) must hold:
- (a) **role profiles with actor variants and crosswalk IDs**, versioned (M-01, M-18);
- (b) the **friction register** (M-02);
- (c) the **pathway graph** with predicted scores and validation statistics (M-03);
- (d) an **artifact registry** recording which partner PDs, class specs, postings, assessments and learning records embed which EMST IDs and when. This is the backbone of the contribution chain (M-08, M-18);
- (e) **entry-role formation-task indicators** and **entry-cohort counts** (M-19, M-20);
- (f) the **observed-transition validation table** (consented, minimal, separated from identity);
- (g) a **metrics store** with baselines, comparison units and pre-registration (M-13–M-17);
- (h) the **panel decision log** (M-28).

The model should **not** hold person-level identity or HR records. Partners supply aggregates. The few person-level validation
records are consented, minimised and stored separately (CP to specify) [J].

---

## 8. Files in this folder

| File | What it is |
|---|---|
| `report.md` | This report |
| `logic_model.md` | Testable theory of change; logic model; assumptions A1–A12 with [E]/[J]/[S] and confirm/refute evidence; external factors; contribution-analysis plan |
| `metrics_framework.csv` | 30 metrics incl. expansion gates G1 and G2 |
| `personas.md` | 9 evidence-based composite personas plus 1 Tribal placeholder (not drafted), each with "does this help me?" test questions |
| `practitioner_panel_design.md` | Design of the real panel: composition, recruitment, pay, cadence, methods, conflict of interest and anonymity, binding decision rights |
| `transferability_analysis.py` | Reproducible computation (run: `python3 -I docs/research/mobility-workforce-voice/transferability_analysis.py`) |
| `family_similarity_matrix.csv` | 15×15 weighted-Jaccard matrix |
| `family_pairs.csv` | All 210 ordered pairs: all measures, null z, directional coverage, destination-Core gaps |
| `bridging_competencies.csv` | 222 competencies ranked by cross-community bridging, with type, CLD and craft |
| `family_craft_blend.csv` | Craft blend, evenness, community, centrality and CLD exposure per family |
| `transferability_summary.json` | Headline numbers quoted here |
| `role_signals.csv` | 16 entry-path-at-risk, skill-shift and role signals |
| `v1_assessment.csv` | 15 verdicts on v1 elements from a mobility perspective |
| `ecosystem.csv` | 25 entities: mobility data, research programmes, employee organisations, corps networks, policies |
| `candidate_competencies.csv` | 3 candidates (knowledge continuity; cross-system translation; co-delivery work) |
| `sources.csv` | 72 sources, incl. blocked and unverified ones marked as such |
| `scripts/write_metrics.py`, `scripts/write_csvs.py` | Generators for the structured CSVs (properly quoted) |

---

## Proposals

- **P-CM-01 Adopt the restated, testable theory of change and the contribution-analysis plan** (`logic_model.md`). Pre-register 10–15 pathways and the failure condition before the pilot starts. *Why:* the charter version promises an effect the evidence does not support unconditionally (§2). [E/J]
- **P-CM-02 Make "visibility in gate instruments" the product strategy.** Prioritise exports EMST can put into PDs, class specs, postings, USA Hire and SME-QA assessment content, IDPs and learning records over browse-only views. Measure use with the artifact registry (M-08, M-18). *Why:* embedding, not announcement, moves hiring (CM-014, CM-011); the federal gate is moving to assessments (CM-050). [E]
- **P-CM-03 Validate before recommending.** No pathway is labelled "recommended" until it passes M-03. Until then the pathway view is "exploratory" and the default is translation and gap views. *Why:* unvalidated similarity tools were shipped and then retired elsewhere (CM-020–CM-023). [E]
- **P-CM-04 Set the similarity basis.** Use importance-weighted, asymmetric task overlap on L3 role variants; show directional coverage to users; compute pathway score = similarity × (1 − friction) × demand. Craft blends are descriptive only. *Why:* §3.3 points 2 and 4; §7 Q1. [E/J]
- **P-CM-05 Make the transfer-friction register first-class** (schema in §7 Q2). CM maintains it with inputs from FH, SL, PS and DB, plus TN for anything Tribal. Verify retirement portability first. [J]
- **P-CM-06 Build two bridge learning paths first, with LC.**
  - (a) **Field→statecraft "collaboration bridge kit":** 5.2.1–5.2.5 plus 6.1.x basics. It is the common gap for fire and field staff moving to planning, policy or co-delivery roles.
  - (b) **Statecraft→field immersion:** seasons, corps or apprenticeship, because field craft is the hardest direction to enter.

  Measure both with M-21. [E: computed; J]
- **P-CM-07 Protect the on-ramps.** Track entry-cohort volume (M-20) and pathway-level formation tasks (M-19) as leading indicators. Ask FC, LC and FS to design formation tasks into entry role profiles. The tool should flag any entry role that has lost its learning tasks. *Why:* portability and CLD coincide (§3.3 point 7); on-ramps are being cut (CM-039, CM-043). [E/J]
- **P-CM-08 Make knowledge continuity a v2 capability.** Add candidate CC-CM-01 and pilot a handover protocol with 2–3 partner units where work is devolving. [E need; J design]
- **P-CM-09 Seat the real Workforce Voice panel with binding decision rights** before the pilot: usefulness veto, stratum quorum, co-signed thresholds. Its first acts are to rewrite the personas and co-sign the gates (`practitioner_panel_design.md`). [J]
- **P-CM-10 Adopt a misuse policy before any person-level feature ships.** EMST outputs may not be used to rank or select individuals for RIF or adverse action. Co-write the policy with employee organisations; CP reviews it. Any incident pauses expansion (M-11). [S risk; J]
- **P-CM-11 Adopt expansion gates G1 and G2 as specified,** including the pre-registered "pathway features stop" condition. [J]
- **P-CM-12 Use the 2025–26 displacement as the first validation dataset.** Through AS and SL, ask partner states and the federal-to-state placement partnership (CM-044) for aggregate counts of hires with prior federal service, by former series and new class. Ask FH about an OPM EHRI research agreement. [E that the mechanism exists; J on feasibility]
- **P-CM-13 Retire family-level similarity as a deliverable.** Keep this computation only as a baseline prior for M-03 and as a diagnostic for tagging gaps. Have SMEs re-check Fire↔Planning, and the generic digital tools tagged only to Data Science. [E]
- **P-CM-14 Surface "mobility without changing employer" in the pathway view.** Show IPA assignments, co-delivery agreements, NWCG qualification portability, and corps or veteran hiring authorities where they are verified as current. *Why:* these are existing cross-actor channels that need no new rules. [J]

## Disagreements & trade-offs

- **With the charter wording.** "Mobility follows" from visibility is not supported. I propose the conditional version.
  - *Trade-off:* a narrower promise against credibility with federal and state adopters and funders who will ask for outcome evidence.
- **With CA's "crafts as profiles" (agree) and any use of craft blends as the mobility engine (disagree).** Three crafts are a powerful communication device and a weak similarity measure (§3.3 point 4).
  - *Trade-off:* the charter's elegant framing against predictive power. Keep crafts for explanation and pathway design.
- **With CA's hybrid spine (support B internally).** Mobility needs importance-weighted task bundles on role variants, which multiplies SME burden.
  - *Proposal:* depth over breadth. Build the 10–15 pre-registered pathways fully before broad coverage.
  - *Trade-off with DB and AS on coverage breadth.*
- **With v1 Domain 7.** Carry it, but do not cite its bridging as evidence of portability; it is partly built in.
- **Panel veto versus CA's authority.** The charter has CA resolve disputes, and it also says practitioners' answer outweighs elegance. My design reconciles the two with a veto that CA can override through a written answer, a second vote and escalation.
  - *Trade-off:* governance friction against legitimacy with the people the tool serves.
- **Speed versus evidence in 2026.** Displacement creates pressure to roll out fast. I propose a **fast track limited to translation and crediting**, which is low-risk and needs no prediction, while recommendation features wait for M-03.
  - *Trade-off:* slower headline features.
- **Validation versus privacy (with CP and DE).** Validation needs real career histories, and privacy rules restrict them.
  - *Trade-off:* minimum-grain, consented, separately stored records versus none. Without them the pathway claims cannot be tested.
- **With LM on CLD.** I lean on v1's single-analyst CLD flags for the portability–compression finding. LM may judge them too weak until corroborated externally. I accept that, and label the finding [J] until LM corroborates it.

## Issues outside my area that affect the vision

- **CP / FH.** Ethics rules may restrict paid panel participation by federal and state employees; clear this before recruitment.
- **FH / SL / AS: data access.** Pathway validation needs an OPM EHRI research agreement and state HR data-sharing.
- **AS: corps and AmeriCorps instability.** This threatens the field-craft on-ramp, the hardest direction of mobility (CM-043, CM-046). Funders should know this.
- **CP / AS: misuse.** In a RIF and accountability-reform environment (CM-052), skills data can be turned against workers. This is a trust and adoption risk for the whole tool.
- **TN.** No Tribal persona was drafted, Tribal panel seats are filled only via TN, and pathway views must not list Tribal positions unless a nation chooses to.
- **LM.** Corroborate (or refute) the claim that CLD concentrates in statecraft and portable foundation competencies, using entry-level posting and staffing data.
- **IO.** Craft-weight reliability decides whether blends may be shown about individuals (M-04).
- **DB.** Water and wastewater operator certification and other licences are probably the biggest frictions outside public lands, and my computation cannot see them.
- **All roles.** The team-wide search budget ran out. Key primary sources still to retrieve: Grassroots Wildland Firefighters testimony, Green 2.0's latest report, GAO's fire workforce reports, NGA's Colorado case study, the HBS/BGI retention findings, Dawson et al. and del Rio-Chanona et al.

## Open questions for the Chief Taxonomy Architect

1. **Charter interpretation (decision point).** Do you adopt the restated theory of change in `logic_model.md` as the project's operating version, keeping the charter sentence as the north star?
2. **DP-9 (governance).** Will the panel's G1 usefulness veto, with your written-override procedure, be adopted?
3. **DP-6 (first role set).** Will the first role set be chosen to cover the 10–15 pre-registered pathways? My candidates:
   - federal field technician → county or state-park technician;
   - fire → county wildfire planner;
   - federal NEPA coordinator → state environmental review;
   - corps alum → agency technician;
   - wildlife graduate → consulting biologist;
   - state water-quality specialist → co-delivery coordinator;
   - ESG analyst → state climate office;
   - plus water/wastewater and air pathways from DB.
4. **Scope of v2.0.** Is pathway *recommendation* in scope for v2.0 at all, or only translation, gap and role-change views until M-03 passes?
5. **Ownership.** Who owns the friction register? I propose CM, with FH, SL, PS and DB contributing and TN holding a veto on anything Tribal.
6. **DP-7 and DE.** Does v2 store the consented observed-transition validation table in a governed side store, or only aggregate validation statistics in the repo?
7. **Families.** Given that the two-island structure depends on how v1 tags were assigned, should families survive only as navigation groupings of role profiles (your audit's lean), or be dropped from user-facing views entirely?
