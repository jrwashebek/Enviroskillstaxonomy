# Domain Expert Bench (DB): Subsector Coverage, Where Generalizations Break, and How Subsectors Enter v2

**Role:** Domain Expert Bench (DB), Phase 2 · **Date:** 2026-10-23 · **Folder:** `docs/research/domain-bench/`
**Labels:** [E] evidence from a source I read (source IDs resolve to `sources.csv`); [J] expert judgment (what it rests on is stated); [S] speculation (what would confirm or refute it is stated).

---

## 0. Summary

- **The environmental sector maps to 44 subsectors in 9 clusters.** The clusters are Water (6), Pollution control & materials (6), Environmental health (2), Energy & extractives (5), Climate, resilience & hazards (3), Markets, finance & corporate (2), Lands & living resources (11), Built environment (2), and Cross-cutting environmental practice (7). The last cluster holds work functions (review, inspection, EJ, education, research, labs, data), not subsectors. That distinction matters for the architecture (§7, §8). [J, built on v1 data E: DB-003/DB-004]
- **v1 coverage:** 11 subsectors Full, 22 Partial, 11 None. [E: DB-003, my coding in `subsector_coverage_map.csv`]
  - Full coverage clusters around v1's home ground: forestry, wildlife, fire, agriculture, restoration, markets, environmental review, education, research and data.
  - The **None** set is drinking water, wastewater, groundwater, hazardous waste, environmental public health, renewable siting, linear infrastructure, oil and gas, emergency management, marine/coastal and transportation environmental. It includes the largest public environmental workforces outside land management.
- **Federal and state priority gaps.** I rate 18 subsectors High priority for federal and state workforce strategy. v1 covers only **2 of the 18** fully (wildland fire and NEPA review), the two closest to its public-lands origin.
  - **None (6):** W01 drinking water, W02 wastewater, P03 hazardous waste, H01 environmental public health, C03 emergency management/hazard mitigation/floodplain, U02 transportation environmental.
  - **Partial (10):** W03, W04, W06, P01 air, P04 remediation, E04 mining/AML, C01, C02, L11 cultural resources, X02 compliance inspection.
- **Even v1's own demand corpus shows the gap** [E: DB-011]. Of 58,544 OpenLMP forest-plan components:
  - 1,377 mention minerals, mining or reclamation;
  - 1,288 mention water quality;
  - 835 mention cultural resources;
  - 480 mention energy/utility corridors;
  - 373 mention air quality or smoke.

  v1 has essentially no competencies for minerals or corridors and one for air.
- **Where v1 generalizations break worst** (`generalization_breaks.csv`):
  1. S1–S6 is a project-authorization lifecycle. It cannot represent continuous operations, disclosure cycles or incident response.
  2. Fieldcraft is defined around the *landscape*, which leaves out the embodied judgment of operators, inspectors and lab staff working on *engineered* systems.
  3. Proficiency as tenure bands collides with licensure grades and position qualifications.
  4. v1 implicitly assumes competency confers authority to act. In licensed subsectors a credential, not competence, gates the task.
  5. The sector-application fields miss the axis that organizes pollution-control careers: **regulatory position** (regulator, regulated entity, service provider, watchdog).
  6. NEPA reform flags have been forced onto non-NEPA work. 3.6.2 sustainability reporting carries "digital permitting" flags, and 6.7.5 air quality carries "NEPA timeline". [E: DB-003]
  7. The exposure picture is skewed toward AI because the robotics-exposed subsectors are absent. Only 7 of 666 v1 tasks carry a robotics or convergent vector. [E: DB-004]
- **Proposals.**
  - 55 candidate competencies (`DB-C01…C55`), 27 role signals, a 92-row credentials register, and 18 subsector modules with steward candidates.
  - Structurally: **orthogonal facets** (work function × subsector × competency type), a **governed core plus subsector modules** as the stewardship unit, two added work functions (*Operate & maintain*, *Respond & recover*), a **regulatory-position** facet, and **credential-gate** attributes.
- **Evidence limit, stated plainly.** The team's shared web-search budget was used up before I began, so I ran 0 of the 25–40 searches I had planned. Direct fetches of agency and issuer pages were refused because no one was available to approve them.
  - I could read: the BLS May 2025 OEWS release [DB-001/002], the v1 database and documents, and the OpenLMP corpus.
  - Everything about credentials, frameworks, current rules and AI adoption in specific subsectors is therefore **[J]**, resting on practitioner knowledge. Each of those claims points to a listed but unverified source (DB-020…DB-065) that forms a ready verification queue (P-DB-16). This is a finding about the state of DB's evidence, not a reason to hold back the structural conclusions. Those rest mostly on the v1 data, which I did read.

---

## 1. Scope, method and limits

**Plan.** The plan had four parts:
1. Build the subsector list from the brief's starting list and from the regulatory and employer structure of US environmental work.
2. Code v1 coverage by reading competency text, tasks, proficiency text, indicators and sector notes for each subsector (`scripts/v1_keyword_scan.py`), then judging the matches by reading them.
3. Pull workforce signals from BLS OEWS May 2025.
4. Verify credentials, frameworks and AI signals against primary issuer, agency and association sources.

**What happened.**
- Step 3 partly succeeded. The May 2025 OEWS release (published 2026-05-15) was readable for most professional and technical occupations [E: DB-001]. Production and installation rows were missing from the HTML extraction and misaligned in the PDF [DB-002], so I have **no verified May 2025 figure** for:
  - 51-8031 water/wastewater operators;
  - 47-4041 hazmat removal workers;
  - 53-7081 refuse collectors;
  - 47-2231 solar PV installers;
  - 49-9081 wind turbine technicians.

  The map gives recalled orders of magnitude for these, labeled [J] with "verify".
- Step 4 could not be done. Search returned "budget used up" on my first query. Fetches of EPA, BLS OOH and OEWS detail pages returned permission-required errors (DB-012 to DB-014).
- I used two extra local evidence sources:
  - the OpenLMP corpus, through `scripts/lmp_subsector_signal.py` [E: DB-011];
  - v1 tag and exposure data, used to test generalizations against real v1 assignments [E: DB-003/004].

**Why these sources.**
- OEWS is the authoritative US occupational employment series, and May 2025 is the latest release.
- The v1 database is what v2 migrates.
- OpenLMP is the only demand-side dataset on disk. The charter names plan requirements as a demand signal.

**Sources that are dated or a poor fit.**
- The O*NET Green Economy framing (2009–10) is outdated as a structure [DB-050].
- The DOL Water and Wastewater Competency Model is probably dated (2013–15) [DB-041].
- The v1 "Structural Conditions" report [DB-009] has unresolvable citation markers. I used it only for its credential-closure typology.

**What this is not.** It is not a consensus of subsector practitioners. The charter pictures a *rotating bench* of recognized practitioners. This is a single-agent synthesis written at practitioner depth. Every module needs real subsector SMEs and a Delphi round before any candidate competency enters a release (IO lane).

---

## 2. The subsector map

The full map is `subsector_coverage_map.csv`. For each of the 44 subsectors it gives a definition, SOC and NAICS codes, workforce signal, employers by sector actor, credentials, existing frameworks, AI/tech signal, v1 coverage and codes, gaps, priority, evidence label and sources. In the table below, v1 codes on "None" rows are incidental mentions only, such as sector notes.

| ID | Subsector | v1 | v1 codes (incidental where None) | Fed/state priority |
|---|---|---|---|---|
| W01 | Drinking water supply & treatment | None | 1.2.4, 4.1.3 | High |
| W02 | Wastewater collection, treatment & reuse | None | 1.2.4 | High |
| W03 | Stormwater & green infrastructure | Partial | 4.7.1, 4.7.3, 4.2.4, 1.2.5, 1.2.3 | High |
| W04 | Water resources, hydrology & supply planning | Partial | 1.2.3, 2.4.2, 4.6.4, 6.5.4 | High |
| W05 | Groundwater & hydrogeology | None | 1.2.3 | Medium |
| W06 | Surface water quality regulation, watershed & wetland programs | Partial | 1.2.4, 4.1.3, 6.1.2, 6.1.3, 6.3.3, 1.2.1 | High |
| P01 | Air quality management | Partial | 6.7.5, 6.1.1 | High |
| P02 | Solid waste, recycling & materials | Partial | 3.7.1–3.7.5 | Medium-High |
| P03 | Hazardous waste & materials | None | 4.4.4 | High |
| P04 | Contaminated sites & remediation | Partial | 4.4.4, 6.7.1, 1.2.2 | High |
| P05 | Chemicals, pesticides & toxics regulation | Partial | 6.7.4, 6.7.1, 4.6.3 | Medium-High |
| P06 | Industrial environmental compliance & EHS | Partial | 6.1.2, 4.4.1, 3.6.5 | Medium |
| H01 | Environmental public health services | None | 6.7.1 | High |
| H02 | EH science, toxicology & risk assessment | Partial | 6.7.1, 6.7.4, 6.7.3 | Medium |
| E01 | Renewable/clean energy siting & review | None | 6.1.3, 6.1.4, 1.4.2 | Medium |
| E02 | Transmission, pipelines & linear infrastructure | None | 4.7.2, 4.5.2 | Medium |
| E03 | Oil & gas EHS (incl. orphan wells) | None | – | Medium |
| E04 | Mining, reclamation & abandoned mine lands | Partial | 4.2.1, 4.2.4, 1.2.5, 1.1.3 | High |
| E05 | Energy management, efficiency & building decarbonization | Partial | 4.7.5 | Medium-Low |
| C01 | Climate mitigation, GHG accounting & carbon mgmt | Partial | 6.6.1, 1.5.4, 6.3.5, 6.8.3, 3.6.5 | High |
| C02 | Climate adaptation & resilience | Partial | 1.5.2, 1.5.3, 6.8.4, 1.7.3, 6.2.5 | High |
| C03 | Emergency mgmt, hazard mitigation & floodplain mgmt | None | 4.4.5, 4.3.1, 1.1.4 | High |
| M01 | Corporate sustainability & ESG reporting | Partial | 3.6.1–3.6.5 | Low (fed/state); High (private) |
| M02 | Environmental markets & conservation/climate finance | Full | 6.6.x, 6.8.x, 6.3.3, 6.3.5, 3.4.2 | Medium |
| L01 | Forestry | Full | 1.3.x, 4.5.2, 4.2.3 | Medium |
| L02 | Wildlife management & species conservation | Full | 1.4.1–1.4.4, 4.1.2, 1.1.5, 1.6.1 | Medium |
| L03 | Fisheries & aquatic resources | Partial | 1.4.1, 1.4.5, 1.6.2, 2.6.2 | Medium-High |
| L04 | Marine & coastal management | None | 1.4.5, 2.6.2 | Medium |
| L05 | Rangeland management | Partial | 4.1.1, 4.6.1, 1.8.4, 4.1.4 | Medium |
| L06 | Agriculture, soil & water conservation | Full | 1.8.x, 4.6.x, 1.2.1, 1.2.2 | Medium |
| L07 | Wildland fire | Full | 4.3.x, 4.2.3 | High |
| L08 | Ecological restoration & invasive species | Full | 4.2.1, 4.2.2, 1.1.3, 1.1.4, 1.7.1, 1.7.4 | Medium |
| L09 | Land conservation & land trusts | Partial | 6.3.3, 6.6.4, 5.2.5 | Low-Medium |
| L10 | Parks, protected areas & outdoor recreation | Partial | 5.5.x, 5.1.3, 4.2.5, 3.3.3, 5.4.5 | Medium |
| L11 | Cultural resources & historic preservation | Partial | 5.3.3, 5.3.2, 6.5.1 | High |
| U01 | Urban environment & planning | Partial | 6.2.1, 6.2.2, 6.2.4, 4.7.x | Medium |
| U02 | Transportation environmental | None | 6.1.4, 4.2.5 | High |
| X01 | Environmental review & impact assessment | Full | 6.1.4, 6.1.1, 6.4.3, 6.4.4, 6.1.3 | High |
| X02 | Compliance inspection & enforcement | Partial | 6.1.2, 6.1.5 | High |
| X03 | Environmental justice & community programs | Full | 5.3.5, 6.7.2, 6.7.3, 5.6.3, 5.6.5 | Medium |
| X04 | Environmental education, interpretation & communication | Full | 5.1.x, 5.4.x, 5.6.1 | Low-Medium |
| X05 | Environmental research & science | Full | D1 broadly, 5.6.2 | Medium |
| X06 | Environmental laboratory & analytical services | Partial | 2.2.3, 1.6.2, 4.1.3 | Medium |
| X07 | Environmental data, geospatial & informatics | Full | D2 | Medium |

### 2.1 Why this list (refine/merge/split decisions)

- **Water is split six ways, not one.** Utility operations (W01, W02) carry licensed-operator closure, grade ladders and a local-government employer base. Water quality regulation (W06) is a state-agency permitting and TMDL function. Hydrology and supply (W04) and groundwater (W05) have different regulators and credentials (PG, NGWA). v1's F4 merges all of these. [J, resting on the SDWA/CWA program structure: DB-020, DB-022]
- **Wetlands sit inside W06, not as a separate subsector.** Delineation through 404 permitting through mitigation is one regulatory chain. Its credential (PWS) and its market half (M02) are cross-referenced.
- **Pollution control is split by regulatory regime** (CAA, RCRA C/D, CERCLA, TSCA/FIFRA), plus P06 for the *regulated-entity* side (facility EHS). Regulatory regime is what separates the employers, credentials and career ladders. [J]
- **Environmental health is split** into local and state *services* (H01, REHS inspectors) and *science* (H02). In SOC both sit inside 19-2041 "including health", so OEWS cannot separate them. [E: DB-001 title; J on content]
- **Energy is split** into clean-energy siting (E01), linear infrastructure (E02), oil and gas (E03), mining (E04) and efficiency (E05). Demand drivers and regulators differ sharply. In 2025 these sub-segments moved in opposite directions (incentive phase-downs vs. orphan-well and AML funding). [J: DB-028, DB-029, DB-039]
- **Emergency management, hazard mitigation and floodplain management are merged** (C03). They share employers (local EM and floodplain administrators are often one office), FEMA as the federal counterpart, and the NIMS/NFIP regimes. [J]
- **The "X" cluster is functions, not subsectors.** Environmental review, inspection and enforcement, EJ, education, research, labs and data are practised *inside* every subsector. This is the single most important input to the architecture question (§7 Q3, §8).

### 2.2 Workforce size signals (what OEWS can and cannot see)

Verified May 2025 national employment [E: DB-001, DB-002]:

| Occupation group | May 2025 employment |
|---|---|
| Environmental scientists and specialists, incl. health (19-2041) | 89,250 |
| Environmental science and protection technicians, incl. health | 34,670 |
| Environmental engineers | 38,340 |
| Environmental engineering technicians | 12,190 |
| Conservation scientists | 25,950 |
| Foresters | 10,430 |
| Forest and conservation technicians | 30,410 |
| Zoologists and wildlife biologists | 18,120 |
| Hydrologists | 5,850 |
| Hydrologic technicians | 2,840 |
| Geoscientists | 23,470 |
| Urban and regional planners | 44,230 |
| Emergency management directors | 13,500 |
| Occupational health and safety specialists | 140,610 |
| Occupational health and safety technicians | 30,590 |
| Health and safety engineers | 21,450 |
| Compliance officers | 417,070 |
| Anthropologists and archeologists | 8,990 |
| Fish and game wardens | 5,770 |
| Mining and geological engineers | 6,080 |
| Epidemiologists | 12,090 |
| Chemists | 82,770 |
| Biological technicians | 69,620 |
| Pesticide applicators (vegetation) | 27,050 |
| Tree trimmers and pruners | 55,160 |
| Electrical power-line installers | 131,070 |
| Earth drillers (except oil and gas) | 19,450 |
| Forest fire inspectors and prevention specialists | 2,780 |

Three findings follow.

1. **The SOC system cannot count most subsectors.**
   - Environmental health is merged into 19-2041.
   - Environmental compliance inspectors are buried inside the 417,070 compliance officers.
   - Sustainability specialists are inside the 1,087,090 "business operations specialists, all other".
   - Stormwater, GI, siting, EM specialists and resilience staff have no code at all.

   v1's crosswalk note that "low-quality mappings indicate gaps in the labor market data infrastructure" [E: DB-003] holds far beyond the 15 families. [J]
2. **The largest headcounts are operations and field trades, not "environmental professional" SOCs** [J]. Water/wastewater operators (likely ~120k, unverified), refuse/recycling collectors, hazmat workers, tree trimmers (55k, much of it utility vegetation management), power-line installers. A taxonomy built around 19-xxxx science codes misses where most environmental work is actually done.
3. **The public employer is often local or state, not federal** [J]. Examples: utilities, health departments, air districts, MS4 permittees, floodplain administrators, state NPDES, RCRA and SMCRA programs. This matters for the federal-and-state-first audience. The federal workforce in pollution-control subsectors is a thin oversight layer over delegated state programs (state primacy or authorization). So a "federal and state" MVP that is federal-shaped will miss most of the state workforce (SL lane). [J: DB-020, DB-022–024]

---

## 3. Where sector-wide generalizations break

The full list is in `generalization_breaks.csv` (15 items, rated High/Medium). The worst breaks, with specific examples:

### 3.1 The S1–S6 workflow is one workflow among at least five

v1's stages are an outcomes-based adaptive-management and NEPA project lifecycle. In v1 data, S1 is primary for 111 of 222 competencies and S6 for only 4 [E: DB-004]. In non-land subsectors the work runs on different cycles.

- **Continuous operations** (W01, W02, P02, X06, E02): operate → monitor → adjust → maintain → report, every shift, with no project boundary. A treatment operator's defining act is closing a control loop on a living process. It is neither "implementing an authorized action" (S4) nor "monitoring whether it worked" (S5). It is both at once, continuously, under a permit, with the operator legally in responsible charge. [J: DB-020]
- **Compliance and enforcement** (X02, P01, W06, P05): inspect → determine violation → enforce or assist → verify return to compliance. v1 tags 6.1.5 Enforcement as S2 Environmental Review [E: DB-003], which misplaces the state inspector workforce.
- **Disclosure** (M01, C01): boundary and materiality → data and controls → calculation → assurance → board approval → publication, on an annual cycle. v1 tags 3.6.2 Sustainability reporting **S2 primary with "digital permitting" and "S2–S3 boundary" reform flags** [E: DB-003]. Those flags mean nothing for disclosure.
- **Incidents** (C03, P03, H01, W01): prepare → respond → recover → mitigate, at operational tempo under ICS. v1 has ICS only inside wildland fire (4.3.1, 4.2.3) [E: DB-003].
- **Air programs** run permit → SIP → monitor → enforce under the CAA. v1 tags 6.7.5 Air quality management **S2 with NEPA-timeline, consultation and S2–S3 flags** [E: DB-003]. The CAA is the governing regime; NEPA is incidental. [J: DB-023]

**Consequence.** Stage-filtered views, reform analysis and the stability tier (which is computed from reform flags) give false signals for these subsectors.

**Fix.** Keep S1–S6 as the named *project-authorization profile* (CA audit §8). Add workflow profiles for operations, compliance, disclosure and incident cycles, all mapped onto the CA's generalized work-function facet, with two functions added (§7, Q2).

### 3.2 Profession families miss most of the non-land workforce, and two merge different professions

- **F4 Water Resources** combines watershed science with utility operations and engineering. Utility operations differs in licensure, career ladder (certification grades I–IV tied to plant classification), employer and pay system. [J: DB-020]
- **F13 Environmental Health & Justice** combines REHS inspectors in local health departments (credential-gated, code-enforcement work) with EJ analysis and advocacy (no credential, NGO and state, CBPR work). Their crosswalks, pipelines and exposure profiles are different. [J: DB-044]
- **Missing families** that v1 does not even list as gaps: utility operations, pollution control and remediation, EHS, energy and extractives, emergency management, transportation environmental, cultural resources, and laboratory. v1 lists only marine, Tribal NRM and urban parks/GI. [E: DB-005; J on which are missing; consistent with CA audit §6]
- **The crosswalk has code–title errors** [E for the recorded mappings, DB-003; J for the codes, high confidence; titles confirmed in May 2025 OEWS, DB-001]:
  - 19-1012 is labelled "Farm & Home Mgmt Educators". 19-1012 is Food Scientists; the educators are 25-9021.
  - 33-1021 is labelled "Fire Inspectors". 33-1021 is First-Line Supervisors of Firefighting; inspectors are 33-2021/33-2022.
  - F13 is mapped to 29-9021, which is Health Information Technologists.
  - 25-4031 Library Technicians has nothing to do with environmental education.
  - This confirms CA audit §6 item 4.

### 3.3 Fieldcraft is defined around landscapes; much field judgment is about engineered systems

v1 defines fieldcraft as "tacit knowledge from being in the landscape" [E: DB-007]. Plenty of field judgment lives in engineered systems:

- the plant operator who knows a digester is souring from its smell and foam before the lab confirms it;
- the landfill manager reading cover and leachate conditions after a storm;
- the inspector who sees that a facility's records and floor don't match;
- the lab analyst who knows an instrument is drifting.

All of these are embodied, sensory, system-bound, slowly learned, and lost when people retire. Under v1's definition this work is either missing or would be coded Datacraft. v1 itself names Datacraft over-assignment as its most likely systematic error [E: DB-007, Rule 3].

**Proposal.** Broaden fieldcraft to "physical environmental systems, natural or engineered", and add the reproduction-regime attribute "licensed experience hours" (P-DB-12). FC decides; I flag the disagreement in §10.

### 3.4 Proficiency as tenure bands collides with how licensed and qualified subsectors define level

In W01, W02, C03, L07, P04 and H01, level is set by three things, not years:

- **certification grade tied to system complexity** (a Grade IV operator may run a large plant, a Grade I operator may not);
- **position qualification**, demonstrated in a task book (NWCG, NIMS NQS);
- **legal sign-off authority** (PE seal, PG, LSP opinion, SOI qualification).

[J: DB-020, DB-053, DB-058, DB-031]

These are the levels HR, regulators and workers already use in these subsectors. If EMST levels don't map to them, no one there will use EMST levels.

**Proposal.** Allow module-specific level anchors mapped to the core level scale, and record the grades and qualifications as credentials (P-DB-08).

### 3.5 Competency is not authority

Licensed subsectors legally separate the ability to do a task from the right to do it. Examples:

- the operator in responsible charge;
- a PE seal on a design;
- a PG on a groundwater report;
- an LSP or LSRP opinion that closes a site under state law;
- SOI-qualified archaeologists for Section 106;
- REHS or state registration for inspectors.

[J: DB-020, DB-031, DB-058] A mobility model that treats competency overlap as transferability will *overstate* how easily people move into these roles. It will also hide the credential reciprocity barriers between states, such as operator and PG licensure.

**Proposal.** Add credential-gate attributes on tasks and role profiles, plus transfer-friction records (P-DB-07). CM and IA own the modelling.

### 3.6 Sector-application fields miss "regulatory position"

The CA audit already retires the five v1 sector notes in favour of seven sector actors (§7). Pollution control needs one more axis.

The same competency is practised from different sides. Discharge permit compliance, for example, is practised by:

- the state permit writer;
- the utility or industrial compliance manager;
- the consultant who prepares applications;
- the NGO watchdog filing citizen suits.

One employer can sit on several sides at once. A city *regulates* as a health department and *is regulated* as a POTW and MS4 permittee.

The commonest career moves in these subsectors run regulator ↔ regulated entity ↔ consultant. [J] They are invisible without a **regulatory-position facet** on role profiles that is orthogonal to sector actor (P-DB-06).

### 3.7 Statecraft is generalized from federal NEPA and consultation; most pollution-control statecraft is state administrative practice

- In SDWA, CWA (NPDES), CAA (Title V/SIP), RCRA and SMCRA, states run the programs under delegation (primacy or authorization). [J: DB-020, DB-022–024, DB-028]
- The state counterpart of a federal NEPA coordinator is often a permit writer, an inspector or an enforcement case officer. That counterpart is defined by state administrative procedure and the federal–state oversight relationship, not by NEPA or ESA consultation.
- Federal-to-state mobility is the charter's first job. It needs actor-specific statecraft enactments (SC) and state program context on role variants (SL).

### 3.8 The exposure instrument is skewed by subsector selection

- v1 task vectors are AI 516, none 143, convergent 6, robotics 1, out of 666 [E: DB-004].
- The subsectors with deployed physical automation are absent. Examples [J]:
  - AI-vision robotic sorting at materials recovery facilities;
  - process control at treatment plants;
  - lab automation;
  - robotic and camera pipe inspection with computer-vision defect coding;
  - continuous emissions monitors.
- So the sector-wide claim that "environmental work is mostly AI-augmented, rarely substituted" is partly an artifact of coverage.
- Two subsector-specific mechanisms are also missing:
  - **Legal accountability limits substitution.** Licensure requires a human in responsible charge, so automation in plants takes the form of *supervision* (V), not substitution (S). [J]
  - **Career-ladder destruction can run through licensure.** Certification needs documented operating experience. If automation removes hands-on tasks, the time to certify may stretch or the experience may hollow out. [S; confirm with operator-certification board data on time-to-certify]

**Proposal.** Re-run exposure on module tasks before drawing sector-wide conclusions, and add a legal-accountability-constraint attribute (P-DB-13). LM and FS should know this before they generalize.

### 3.9 Reform flags: the wrong regime outside NEPA

Every High-priority gap subsector has its own regulatory drivers. None of them are NEPA:

- SDWA lead and PFAS rules [DB-021];
- methane standards [DB-029];
- state packaging EPR laws [DB-064];
- disclosure regimes [DB-033–035];
- FEMA program changes [DB-030];
- state cumulative-impact laws [DB-060].

Their status changed in 2025–26 (reconsiderations, extensions, rollbacks). That is a strong case for the CA's dated driver-event model (audit §9). Module stewards should curate their own regime event lists (P-DB-11). [J]

### 3.10 Where v1 generalizations hold

- 7.2 Human-AI practice is durable and transversal across subsectors. It needs an *operations enactment* (supervising automated control, DB-C03), not a subsector copy.
- 1.2.4 and 4.1.3 (water quality assessment and testing), 4.7.1 and 4.7.3 (GI and stormwater field work), and the D2 data competencies carry over.
- The craft irreducibility test works on subsector competencies once fieldcraft is broadened (25 of my 55 candidates are SC-primary, 15 FC, 15 DC).

---

## 4. Gap competencies (`candidate_competencies.csv`, DB-C01…C55)

I wrote 55 candidates, concentrated where federal and state priority meets None or Partial coverage:

| Area | Count |
|---|---|
| Pollution control | 13 |
| Water | 11 |
| Climate/EM | 8 |
| Energy | 6 |
| Lands | 5 |
| Cross-cutting | 4 |
| Markets/ESG | 4 |
| Environmental health | 3 |
| Built environment | 1 |

By change type: 34 transforming, 11 stable, 7 emerging, 3 new.

Every candidate is written as an observable performance, with the work products an assessor would examine (permit and fact sheet, inspection case file, QA records, shift logs, adopted plan). This follows the IO requirement. All are labeled J. Three (DB-C34, C50, C55) also draw on OpenLMP demand evidence [E: DB-011], noted in their rationale.

**Highest-priority candidates for the federal and state MVP:**

| Priority | Candidates | Why |
|---|---|---|
| Water utilities | DB-C01 drinking water process operation; DB-C02 wastewater/resource recovery; DB-C04 SDWA compliance; DB-C05 asset and capital management; DB-C06 OT security | Largest local workforce, no v1 coverage, licensure-defined levels |
| Regulatory craft (state) | DB-C07 discharge permits; DB-C12 air permits; DB-C24 multimedia inspection and case records; DB-C25 data-targeted compliance | The core state-agency jobs v1 cannot describe |
| Remediation and hazwaste | DB-C18 hazardous waste determinations and generator compliance; DB-C19 site assessment and CSM; DB-C20 remedy selection and long-term stewardship | Federal-facility cleanup and state cleanup programs; largest consulting segment |
| Environmental health | DB-C27 risk-based EH inspections; DB-C28 outbreak and emerging-hazard investigation; DB-C29 risk communication | Local health departments; climate-driven workload |
| EM and hazards | DB-C40 hazard mitigation planning; DB-C41 EHP review; DB-C42 environmental response in ICS; DB-C43 floodplain/NFIP administration | Federal role shifting to states and localities |
| Extractives | DB-C34 mine reclamation and AML; DB-C33 orphan wells | IIJA-funded state programs; strong forest-plan demand |
| Cultural and transport | DB-C50 Section 106 review and consultation; DB-C51 transportation environmental commitments | Every federal undertaking; state DOTs are large NEPA employers |

**Core vs module.** Several candidates are not subsector-specific once you look at their task core. They belong in the governed core with module enactments (P-DB-09):

- DB-C03 supervising automated control (water, waste, energy, labs);
- DB-C24 and DB-C25 inspection and targeting (every regulatory module);
- DB-C29 risk communication (EH, water, remediation, EM);
- DB-C05 asset management and DB-C06 OT security (all utilities and infrastructure).

I also propose two generalized core competencies built from module candidates:

- **"Draft and administer enforceable authorizations"**, from DB-C07, C12, C43, C47 and the mining and pesticide permits. These share applicability determination, condition drafting, the administrative record and public process.
- **"Operate within incident command"**, from DB-C42 and v1 4.3.1.

That is how the core stays small while modules stay deep.

---

## 5. Role signals (`role_signals.csv`, 27 rows)

These are labeled J (18) or S (9). The ones most relevant to the federal and state first job:

- **Water and wastewater operator: transforming** (DB-RS-01). Work moves toward supervising SCADA and AI control and toward OT security. **The operator-in-training path may be at risk** (DB-RS-02, [S]) through the licensure-experience mechanism in §3.8.
- **Compliance inspector: transforming** (DB-RS-09). Analytics and remote sensing do the targeting; inspectors move to evidence-grade follow-up. Fiscal pressure on inspection headcount adds to this.
- **State multimedia program staff: skill-shift** (DB-RS-26, [S]). As federal capacity contracted in 2025–26, states carry more permitting, monitoring and enforcement with flat budgets, which pushes toward cross-media generalists.
- **Emergency management specialist (state and local): transforming** (DB-RS-20, [S]). Federal restructuring shifts mitigation and recovery work downward.
- **Entry paths at risk:**
  - junior Phase I ESA professionals (records review and report drafting are highly compressible);
  - CRM archaeological technicians (LiDAR site models plus AI drafting);
  - local REHS (degree and registration gates plus climate-driven workload).
  - These show the v1 CLD mechanism in new subsectors.
- **New roles:**
  - lead service line inventory specialist;
  - orphan-well program manager;
  - utility vegetation management and wildfire mitigation specialist;
  - GHG verifier or assurance practitioner;
  - credit-integrity analyst;
  - chief heat officer.
- **Declining:** MRF manual sorters (robotic sorting deployed). Federal environmental research scientists (2025 restructuring; verify).

---

## 6. Credentials register (`credentials_register.csv`, 92 rows)

| Type | Rows |
|---|---|
| Certification | 53 |
| License | 19 |
| Certificate | 13 |
| Qualification | 7 |

Every row records issuer, the rule or practice that requires it, a renewal pattern, competency areas and notes. Every row is **[J] and needs verification**. URLs are domain-level and recalled, not fetched (DB-059).

Structural observations:

1. **Three closure types, and they behave differently for mobility** (this extends DB-009's typology to new subsectors) [J]:
   - **Legal licensure.** Operators, PE, PG, LSP, pesticide applicators, asbestos and lead, sanitarian registration in some states, floodplain administrators in some states.
   - **Regulation-mandated training records.** HAZWOPER, DOT hazmat, RCRA personnel training, MSHA, UST operator training, Method 9.
   - **Voluntary certification.** Most of the rest.

   Legal licensure creates hard state-by-state barriers. Mandated training creates cheap but universal gates. Voluntary certification is a hiring signal only.
2. **Credential exam blueprints are existing job-task analyses.** ABC, NEHA, IHMM, BCSP, BGC (CIH), ASFPM, IAEM, ISA, SAF, TWS, NCEES and ASBOG all run psychometric job analyses to build their exams. These are the best available validation evidence for module competencies, and they show which bodies are ready to steward a module (§7 Q1). Many are proprietary, so use needs agreements (AS and IA). [J]
3. **Some credentials are standard-bound and belong in the tools/standards layer (L4), not the core.** LEED AP, GRI, the IFRS FSA (status reportedly changing; verify) and NABCEP are examples. This applies the brief's durable-vs-tool principle to credentials. [J]
4. **Federal qualifications can work as mobility bridges.** The NRCS Technical Service Provider certification lets private and NGO staff deliver federal conservation planning. The SOI Professional Qualification Standards work the same way across federal, state, Tribal and private CRM practice. These are worth modelling as cross-actor "passports". [J]

---

## 7. Answers to CA architecture questions (§6 "DB")

### Q1. What is the subsector list for v2 modules, and which subsectors have their own standards or credential bodies that could act as stewards? (DP-2, DP-9)

**Answer.** Use the 44-subsector vocabulary in §2 as the L0 subsector facet. It should be polyhierarchical: a competency can carry several subsector IDs. Package the 37 non-X subsectors into **18 stewardable modules** (MOD-01 to MOD-17, with MOD-07 split into 07a and 07b). Treat the 7 X practice areas as the **governed core**; X06 laboratory is a judgment call between core and module. The full list with stewards, assets and readiness is `module_steward_candidates.csv`.

| Readiness | Modules | Basis |
|---|---|---|
| **Strong** (credential body with job analysis or exam blueprint + maintained body of knowledge + federal/state partner) | MOD-01 Water & wastewater utilities (AWWA, WEF, ABC, ASDWA); MOD-04 Waste, materials & remediation (SWANA, ASTSWMO, ITRC, IHMM); MOD-06 Environmental public health (NEHA, NACCHO, APHL); MOD-09 EM, hazard mitigation & floodplain (IAEM, NEMA, ASFPM, FEMA EMI, NQS); MOD-11 Forests, fire & rangelands (SAF, NWCG, SRM); MOD-12 Fish & wildlife (TWS, AFS, AFWA); lab (TNI, APHL) | [J: DB-041, DB-044, DB-048, DB-053, DB-054, DB-059] |
| **Moderate** | MOD-02 Water resources & quality regulation (ACWA, SWS, AIH, NGWA); MOD-03 Air (NACAA, AAPCA, A&WMA + EPA APTI curricula); MOD-05 Chemicals & EHS (AAPCO, BCSP, BGC, NAEM); MOD-10 ESG & markets (ISSP, IEMA, GRI, NMBA); MOD-14 Working lands & conservation (SWCS, NACD, ASA, SER, LTA); MOD-15 Parks & interpretation (NRPA, NAI); MOD-16 Cultural resources (NCSHPO, ACRA, SAA, RPA; NATHPO only via TN); MOD-17 Planning & transportation (APA, AASHTO) | [J] |
| **Weak** (proto-jurisdictions; central commissioning needed) | MOD-07a Extractives (IMCC, NAAMLP, IOGCC); MOD-07b Clean energy & energy management (IREC, NABCEP, AEE, ISA); MOD-08 Climate mitigation & adaptation (ASAP, US Climate Alliance, ICLEI); MOD-13 Marine & coastal (CSO, NOAA OCM, Sea Grant) | [J; consistent with DB-009's proto-jurisdiction finding] |

**Proposed waves.**
- **Wave 1 (federal and state MVP):** MOD-01, -02, -03, -04, -06, -09, plus v1-seeded MOD-11 and -12.
- **Wave 2:** extractives, clean energy, climate, chemicals/EHS, cultural, planning/transport, working lands.
- **Wave 3:** ESG/markets (private-led, PS), marine, parks.

**Caveat.** Steward *willingness* is AS's question. I can only say which bodies hold the standards, credentials and job analyses that would make them *credible* stewards. Readiness is weakest exactly where federal and state need is growing (climate, extractives, energy), so the "central commissioning first" weakness the CA names for Option C is real there.

### Q2. Where does a sector-wide generalization (core competency or task) break in your subsector?

**Answer.** See §3 and `generalization_breaks.csv` (DB-GB-01…15). The six most consequential:
- S1–S6 cannot represent operations, compliance, disclosure or incident cycles.
- Fieldcraft is landscape-only.
- Tenure-band levels conflict with licensure and qualification levels.
- Competency is treated as authority.
- Regulatory position is missing.
- Exposure is skewed by subsector selection.

**I tested the CA's draft work-function facet** (Assess & sense → Plan & design → Authorize & regulate → Implement & operate → Monitor & verify → Enforce & assure → Learn & adapt → Engage & communicate) against all 44 subsectors. [J]

- **It mostly holds.** "Authorize & regulate" works for both permit writers and applicants, *provided* a regulatory-position facet tells which side the role is on. "Enforce & assure" correctly takes in inspection, enforcement and third-party assurance.
- **Split "Implement & operate"** into **Build & implement** (restoration crews, construction, remediation installs, treatments done once) and **Operate & maintain** (plants, MRFs, networks, labs, assets). These are different job families with different ladders, credentials and exposure profiles. Merging them recreates the v1 S4 problem.
- **Add "Respond & recover"** for incident and emergency work. It runs at a tempo and under a command structure (ICS) unlike any deliberative function, and v1 has it only for fire.
- **Make "Report & attest" a sub-function of Monitor & verify.** Signed regulatory reports (DMRs, TRI, GHGRP, CCRs) and corporate disclosures carry legal attestation liability and an annual control cycle. Keeping them visible lets disclosure and compliance-reporting roles be found.
- **"Finance & transact"** (SRF and grant applications, mitigation-credit and easement transactions, green bonds) can sit under Plan & design for now. If M02 or MOD-14 SMEs find it orphaned, promote it. [S]

### Q3. Is "domain" the right top level, or should work functions × subsectors be orthogonal facets?

**Answer: orthogonal facets.** Retire the v1 domain as the top level and keep it as an alias facet for provenance.

v1 domains are *competency types* (science, technology, management, field operations, communication, policy). They are not areas of work. Treating them as the top level does two kinds of damage:

- **It scatters every subsector across six domains.** Water already sits in 1.2, 4.1, 4.7, 6.1 and 6.3, and air sits in 6.7 under "health & justice". [E: DB-003; `v1_keyword_scan_output.csv`]
- **It forces a bad choice when subsectors are added.** Either add them as new domains, which mixes two kinds of grouping, or scatter them further. Neither gives a steward a coherent unit. [J]

**Recommended facet set** (all on tasks; rolled up to competencies and roles where computed):

1. **Work function** (CA draft + the Q2 changes): what kind of work.
2. **Subsector** (44, clustered, polyhierarchical): which environmental system or regime. Modules are bundles of subsectors and the *stewardship unit*.
3. **Competency type** (knowledge / skill / practice / transversal): what kind of capability. This replaces v1 domains.
4. **Reusability level** (transversal / cross-subsector / subsector-specific / role-specific; ESCO-style [J: DB-010, DB-049]): this computes the core/module boundary.
5. **Workflow profile** (project-authorization, operations, compliance, disclosure, incident, research): named sequences over work functions.
6. **Regulatory position** (on role profiles): regulator, regulated entity, service provider, advocate/watchdog, researcher.
7. **Credential gate** (on tasks and roles) and **regime/driver events** (L5).

**A boundary rule for CA to consider (DP-2/DP-3):** a competency belongs in the **core** if the same task core is enacted in **three or more modules** and differs only in knowledge base or regulatory regime. Otherwise it belongs in the module. The core then carries *enactment notes* per module. Applied to my candidates, this rule moves about 8 of the 55 into the core (§4). [J; IO should test that raters agree on this rule]

**Trade-offs.**
- More facets mean more tagging and inter-rater reliability burden (IO).
- Polyhierarchical subsectors complicate counts and dashboards (CP).
- Module boundaries will be contested. GHG accounting is claimed by C01, M01 and P01; smoke management by P01 and L07; EHP review by C03, X01 and L11. That needs an explicit "home module + enactment" rule.
- Facets serve the task-graph spine (Option B) well, but HR users need curated views (Option A packaging), which agrees with the CA's hybrid lean.

---

## 8. Structural recommendation (for CA to decide)

**Recommendation: federated core plus subsector modules on a shared task spine, with orthogonal facets.** This agrees with the CA's provisional hybrid, with five DB-specific changes.

**Options compared.** Trade-offs [J]:

| Option | How subsectors enter | Pros | Cons |
|---|---|---|---|
| A. Subsector as domain | Add Water, Air, Waste … as domains beside v1's | Simple to explain; visible coverage | Mixes competency-type and system groupings; duplicates cross-cutting competencies in every subsector domain; count balloons; no clean steward unit |
| B. Subsector as tag only | Tag existing competencies with subsector IDs | Cheap; no structural change; good for filtering | Cannot hold subsector-specific competencies (operator process control) without stuffing them into the core; tag inflation; no stewardship unit |
| **C. Core + subsector extension modules, faceted** (recommended) | Core holds transversal and cross-module competencies with enactments; modules hold subsector-specific competencies, tasks, levels, credentials, regimes and role profiles; all share the task spine and facets | Keeps the core small; depth where SMEs want it; maps to existing stewards and their job analyses; supports federal/state wave sequencing; mobility computed on the shared spine | Governance-heavy; uneven module quality; boundary disputes; needs central commissioning where stewards are weak |

**The five DB-specific changes:**
1. **Subsector modules are bundles of subsectors**, not one module per subsector. Use 18 modules, not 44 (Q1).
2. **Cross-cutting practice areas (X01–X07) are core**, not modules. Each module enacts them.
3. **Module-specific level anchors** map licensure grades and position qualifications onto the core level scale (§3.4).
4. **Credential-gate and regulatory-position attributes** go in the shared schema, not left to modules (§3.5–3.6). Mobility depends on them being uniform.
5. **Regime driver events** are curated per module but use one shared event schema (§3.9).

**Sequencing for the first job.** Commission Wave-1 modules centrally (with steward co-authorship where available). Federal and state need there is high, and stewardship is strong in four of the six non-v1 modules. Seed MOD-11 and MOD-12 from v1, *outside* the core, so v1's public-lands depth does not re-skew the core. [J]

---

## 9. Proposals

- **P-DB-01: adopt the subsector vocabulary.** Adopt the 44-subsector, 9-cluster vocabulary (`subsector_coverage_map.csv`) as the L0 subsector facet, polyhierarchical. Treat cluster X as core practice areas, not subsectors. *Add.*
- **P-DB-02: 18 modules in three waves.** Organize subsector depth as 18 modules (`module_steward_candidates.csv`). Wave 1 = MOD-01, -02, -03, -04, -06, -09 + v1-seeded MOD-11, -12. *Add.*
- **P-DB-03: facets replace domains.** Make work function × subsector × competency type orthogonal facets, plus reusability level. Retire v1 domains as the top level and keep them as an alias facet. *Change.*
- **P-DB-04: extend the work-function facet.** Split "Implement & operate" into *Build & implement* and *Operate & maintain*. Add *Respond & recover*. Add *Report & attest* as a sub-function of *Monitor & verify*. *Change.*
- **P-DB-05: more workflow profiles.** Keep S1–S6 as the project-authorization profile. Add operations, compliance, disclosure and incident profiles. *Change.*
- **P-DB-06: regulatory-position facet.** Add regulator / regulated entity / service provider / advocate-watchdog / researcher on role profiles, orthogonal to sector actor. *Add.*
- **P-DB-07: credential gates and a credentials crosswalk.** Add credential-gate attributes (required credential, issuer, jurisdiction, legal basis) on tasks and roles. Make a credentials crosswalk (L6, CTDL-ready; IA) seeded from `credentials_register.csv` after verification. *Add.*
- **P-DB-08: module level anchors.** Allow module-specific level anchors (licensure grades, NWCG and NQS qualifications, sign-off authority) mapped to the core level scale. *Add.*
- **P-DB-09: promote cross-module competencies to the core.** Move DB-C03, C05, C06, C24, C25 and C29 into the core. Synthesize two core competencies, *Draft and administer enforceable authorizations* and *Operate within incident command*, with module enactments. *Add.*
- **P-DB-10: add the remaining candidates to modules.** After SME validation, prioritize water utilities (C01–C06), state regulatory craft (C07, C12, C24), remediation (C18–C20), environmental health (C27–C29), EM (C40–C43), extractives (C33–C34), Section 106 (C50) and transportation (C51). *Add.*
- **P-DB-11: regime driver events.** Replace NEPA reform flags on non-NEPA competencies (3.6.2 and 6.7.5 at minimum) with regime-specific dated driver events. Module stewards curate their event lists. *Change.*
- **P-DB-12: broaden fieldcraft.** Extend fieldcraft to physical environmental systems, natural or engineered. Add the reproduction-regime attribute "licensed experience hours". FC decides. *Change.*
- **P-DB-13: redo exposure on module tasks.** Re-run exposure assessment on module tasks before publishing sector-wide exposure conclusions. Add a legal-accountability-constraint attribute that bounds substitution. LM and FS. *Change.*
- **P-DB-14: fix the families.** Split F4 (watershed science vs utility operations) and F13 (EH services vs EJ). Add the missing job families as groupings of role profiles. *Change/Add.*
- **P-DB-15: fix the SOC crosswalk.** Correct the code–title errors and map environmental health to 19-2041. FH and IA verify. *Change.*
- **P-DB-16: verification pass.** Every DB claim resting on DB-020…DB-065 is [J] until fetched. Run a Phase 2b verification pass with web access before any DB content enters a release, starting with the Wave-1 module rows. *Process.*
- **P-DB-17: module-specific demand corpora.** Give the signal engine corpora per module: utility and state job postings, state class specs, NPDES and Title V permit conditions, disclosure rules. The only current corpus (OpenLMP) is forest plans. IA and LM. *Add.*
- **P-DB-18: v1 element changes.** Retire 3.4.3 (cryptocurrency). Merge the duplicates 6.6.5/6.8.2 and 6.6.3/6.8.3. Rewrite 3.6.2 regime-agnostically. Split 6.7.5 and 4.4.4. Details in `v1_assessment.csv`. *Change/Retire.*

---

## 10. Disagreements & trade-offs

- **With v1 (and possibly FC): fieldcraft's definition.** v1 ties fieldcraft to landscapes. I argue the irreducible element is embodied, system-bound judgment on *physical* systems, engineered ones included.
  - Trade-off: broadening risks diluting the "judgment earned outdoors" that FC exists to protect.
  - Mitigation: keep "place-bound" and "system-bound" as separate reproduction-regime attributes so the outdoor sense stays visible.
- **With the CA's sector-actor framing ("context, not content").** I agree for sector actor. But in pollution control, **regulatory position changes the task bundle**, not only how it is enacted: the permit writer drafts conditions, the permittee meets them. It needs its own facet, not enactment notes.
  - Trade-off: one more facet to tag and validate.
- **With the CA draft work-function facet.** I propose two additions and one sub-function (Q2).
  - Trade-off: a longer facet list against misclassifying two of the largest job families (operators and emergency responders).
- **With PS (anticipated): ESG priority.** I rate M01 Low for federal and state strategy and High for private. The first job is federal and state, and US federal disclosure work shrank after 2025, while California and international regimes keep private demand high. PS may weigh it higher.
  - Trade-off: sequencing ESG into Wave 3 delays the private-sector mobility story.
- **With DC (anticipated): OT cybersecurity.** I tag DB-C06 as DC-primary but argue it is closer to a *safety culture* transversal for operators than to data science.
  - Trade-off: placing it in DC risks making operators treat it as "IT's job".
- **Depth against simplicity.** 55 candidates plus 18 modules is a lot.
  - My mitigation is the three-module boundary rule and wave sequencing.
  - The risk is that Wave-1 modules alone roughly double the v1 competency count. That is acceptable only if the core stays roughly within the CA's 100–250 range and modules stay out of the default HR views.
- **Evidence.** Most of my subsector claims are [J] because no searching was possible. Disagreeing with any of them on evidence grounds is legitimate and expected. The structural conclusions (§3, §7, §8) rest mainly on [E] v1 data.

---

## 11. Issues outside my area that affect the vision

1. **State primacy (SL, FH).** In the pollution-control subsectors the state program *is* the regulator. A federal-and-state MVP has to model state programs as first-class, not as federal derivatives, or it will misdescribe the largest public environmental workforce outside land management.
2. **Data rights for credential job analyses (AS, IA).** The best validation evidence for modules is proprietary exam blueprints. This needs stewardship agreements, not scraping.
3. **Demand-signal skew (IA, LM).** The signal engine's only corpus is forest plans. Without module corpora it will reproduce the public-lands skew v2 exists to correct.
4. **Workforce voice (CM).** The simulated panel should include operators, inspectors, EH specialists and emergency managers. Their career barriers (licensure reciprocity, shift work, local pay) differ from those of land-management staff.
5. **Tribal utilities and environmental programs (TN).** Tribal water operators and environmental programs are large and distinct (Tribal operator certification; GAP-funded staff, DB-063). TN should set how they are represented. I have not drafted Tribal-specific content.
6. **Security (CP).** OT cybersecurity competencies must stay at the capability level. Vulnerability-specific content does not belong in an open taxonomy.
7. **Labor-market data (LM).** OEWS cannot separate most subsectors (§2.2). Workforce sizing for modules will need association surveys, state agency data and USEER-type datasets, each with its own quality issues.

---

## 12. Open questions for the Chief Taxonomy Architect

1. Do you accept the **three-module boundary rule** for core vs module (DP-2/DP-3), or do you prefer an IO-tested alternative?
2. Are the **X practice areas** (review, inspection, EJ, education, research, labs, data) core, as I propose? Is **laboratory** a module or core?
3. Will you add **Operate & maintain** and **Respond & recover** to the work-function facet, and **regulatory position** as a role-profile facet?
4. How should **licensure-defined levels** relate to the core level scale (DP-4)? I propose a mapping, not replacement. Do you agree?
5. **Wave-1 module order.** Do you agree that MOD-01, -02, -03, -04, -06 and -09 come before energy and climate, even though energy and climate are louder in the public discourse?
6. **Home-module rule for contested competencies** (GHG accounting, smoke management, EHP review). Single home with enactments elsewhere, or co-ownership?
7. **Verification.** Will you schedule a DB verification pass with web budget (P-DB-16) before Phase 3 synthesis relies on the [J] subsector rows?

---

## 13. Files written (all in `docs/research/domain-bench/`)

| File | Contents |
|---|---|
| `report.md` | This report (direct write was refused; returned to the coordinator to save) |
| `subsector_coverage_map.csv` | 44 subsectors × 17 fields (definition, SOC, NAICS, workforce signal, employers by actor, credentials, frameworks, AI/tech signal, v1 coverage and codes, gaps, priority, evidence, sources) |
| `credentials_register.csv` | 92 credentials (license / certification / certificate / qualification) |
| `candidate_competencies.csv` | 55 candidate competencies (DB-C01…C55), schema 5.2 |
| `role_signals.csv` | 27 role signals (DB-RS-01…27), schema 5.3 |
| `v1_assessment.csv` | 25 verdicts on v1 elements, schema 5.4 |
| `ecosystem.csv` | 50 associations, frameworks, funds, datasets (DB-ECO-001…050), schema 5.5 |
| `sources.csv` | 60 sources: 11 read, 3 blocked, 46 listed-unverified (verification queue), schema 5.1 |
| `module_steward_candidates.csv` | 20 rows: 18 subsector modules (MOD-01 to MOD-17, with MOD-07 split a/b), the core-practice row and the lab row; stewards, assets, readiness, wave (answers CA Q1) |
| `generalization_breaks.csv` | 15 documented breaks of v1 structures by subsector, with fixes (answers CA Q2) |
| `lmp_subsector_demand_signal.csv` | OpenLMP subsector term counts (58,544 components; USFS vs state agencies) |
| `v1_keyword_scan_output.csv` | v1 text keyword scan by subsector term group |
| `scripts/lmp_subsector_signal.py` | Reproduces the OpenLMP demand signal (regex; caveats in header) |
| `scripts/v1_keyword_scan.py` | Reproduces the v1 keyword scan from `data/v1_baseline/` (`--context` mode shows matches) |
| `scripts/build_*.py` | Generators for every CSV above (content is in the scripts; rerun to regenerate) |

To reproduce, run from any directory (no network needed):

```
python3 -I scripts/lmp_subsector_signal.py /home/claude/lmps > lmp_subsector_demand_signal.csv
python3 -I scripts/v1_keyword_scan.py > v1_keyword_scan_output.csv
```
