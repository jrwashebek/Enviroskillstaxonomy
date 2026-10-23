# Task 12 Working Record: Exposure Instrument Finalization and Domain 4 Pilot
## Environmental Management Skills Taxonomy
### Stage 4: Exposure Classification
### Completed: February 2026
### Status: Complete — Instrument ratified; Domain 4 pilot table (105 tasks) confirmed

---

## Document Purpose

This record documents two outputs from Task 12:

1. **Instrument Finalization** — the ratified 5-dimension AI/robotics exposure classification instrument, including all controlled vocabularies, boundary criteria, and the four Data Dictionary additions arising from the Domain 6 stress test and Domain 4 pilot.
2. **Domain 4 Pilot Table** — the authoritative task-level exposure classification for all 35 Domain 4 competencies × 3 tasks (105 tasks), organized by skill area.

This document is the source of truth for:
- Instrument criteria to be applied in Task 13 (Domains 1–3 and 5)
- Domain 4 exposure classifications for database integration
- Flagged cases requiring practitioner validation or Delphi adjudication
- Career ladder destruction signals identified in Domain 4

**Companion documents:**
- Task sequence: `taxonomy_task_sequence_v3.md`
- Source taxonomy text: `20251202_SkillsTaxonomy_Core_V2__1_.txt`
- Domain 6 stress test findings: summarized in Section 2; full task table exists in prior session record only (see documentation gap flag)

---

## Section 1: Instrument Finalization

### 1.1 Instrument Overview

The exposure classification instrument operates at the **task level**, not the competency level. Each competency in the taxonomy carries three defined job tasks (drawn from the source taxonomy text). Each task receives five classification dimensions independently. This structure captures the "jagged" automation pattern — the analytical insight that AI and robotics affect specific tasks within a competency unevenly, and that a single competency may contain both Human-Essential and high-exposure tasks simultaneously.

**Application unit:** Each row in the classification table = one task within one competency.
**Standard structure:** 5 competencies per skill area × 3 tasks = 15 rows per skill area.
**Domain 4 total:** 7 skill areas × 15 rows = 105 rows.

---

### 1.2 Five Classification Dimensions — Ratified Controlled Vocabularies

#### Dimension 1: Automation Type

Classifies the current relationship between the task and automation — what automation does to this task at present deployment.

| Code | Label | Definition |
|------|-------|-----------|
| **S** | Substitution | The task can be fully performed by AI or robotic systems without meaningful human contribution. Human role has been or imminently will be eliminated. |
| **Ac** | Compressive Augmentation | AI tools substantially reduce the time or cognitive investment required for the task such that headcount compression is plausible even without full substitution. The human role persists as review-and-certify rather than primary execution. Distinct from S (human still required) and from A (compression is sufficient to affect staffing, not just efficiency). |
| **A** | Augmentation | AI or robotic tools assist the human practitioner, who remains the primary task executor. The tool improves speed, accuracy, or scale but does not displace the practitioner's core contribution. |
| **V** | Supervision | An automated system is the primary task executor. The human practitioner oversees the system's operation, monitors outputs, and intervenes when the system fails or produces anomalous results. |
| **H** | Human-Essential | The task cannot be meaningfully automated at current or foreseeable deployment. The irreducible contribution is embodied judgment, relational trust, contextual integration, or physical presence that resists formalization. |

**⚠️ A/V Boundary Criterion (Refinement 1 from Domain 6 stress test — ratified):**
Classify A vs. V based on **current deployment reality**, not projected trajectory. If the human practitioner is the primary task executor today — even if an automated system assists — classify A. If the automated system is the primary task executor today — even if the human remains in an oversight role — classify V. Projected trajectory toward V is captured by the Time Horizon dimension; do not conflate trajectory with current state.

**⚠️ Mode-Split Flag:** When the same task description encompasses both A-mode and V-mode deployment across different organizational contexts (e.g., manual field instruments vs. deployed sensor networks for water quality monitoring), flag the task for practitioner validation rather than resolving the ambiguity unilaterally. Use the modal deployment for the classification; document the mode-split in Notes.

---

#### Dimension 2: Tacit Knowledge Density

Classifies the degree to which successful task performance depends on embodied, experiential knowledge that resists formalization into protocols or algorithms.

| Code | Label | Definition |
|------|-------|-----------|
| **Hi** | High | Task performance depends substantially on tacit knowledge — pattern recognition, anomaly detection, contextual judgment, or embodied sensory engagement — that develops through field experience and cannot be acquired through protocol study alone. High tacit density provides structural protection against automation. |
| **Med** | Medium | Task performance combines procedural elements (learnable from protocol) with tacit elements (developed through experience). Both are required for competent performance; neither dominates exclusively. |
| **Lo** | Low | Task performance is primarily procedural and protocol-governed. Competence is achievable through instruction and practice within defined parameters without requiring substantial experiential development. |

---

#### Dimension 3: Career Ladder Position

Classifies where in the professional career ladder this task primarily lives — who is expected to perform it as a core responsibility.

| Code | Label | Definition |
|------|-------|-----------|
| **P** | Primary Learning | The task is primarily executed by entry-level and early-career practitioners (0–5 years experience) as part of foundational skill development. It is a core learning pathway task. Career ladder destruction risk is highest here — automation of P-position tasks may foreclose the development of tacit knowledge that supports more complex work at later career stages. |
| **C** | Contributing | The task is primarily executed by mid-career practitioners (3–8 years experience) with substantive professional autonomy. Requires developed judgment beyond foundational capability. |
| **X** | Peripheral | The task is primarily executed by advanced or specialist practitioners (8+ years, or specialized qualification required). Not a standard career ladder development task. |

**Note on P vs. C adjudication:** When ambiguous, consult the source taxonomy's proficiency level indicators. If foundational-level indicators describe the task (even imperfectly), classify P. If intermediate-level indicators are the first point where the task appears, classify C.

---

#### Dimension 4: Automation Vector

Classifies which type of automation technology is the primary exposure driver for this task.

| Code | Label | Definition |
|------|-------|-----------|
| **AI** | Artificial Intelligence | Primary exposure is from software-based AI: machine learning, natural language processing, computer vision, decision support algorithms, automated report generation, large language models. |
| **Ro** | Physical Robotics | Primary exposure is from physical robotic systems: autonomous vehicles, robotic manipulators, automated mechanical equipment, drone systems operating under autonomous control. |
| **Cv** | Convergent | The task faces **simultaneous** AI and physical robotics exposure within the same operational action. Both vectors are active at the same time on the same task; they cannot be separated within the task boundary. |
| **—** | None | No meaningful automation exposure at current or anticipated deployment. Used exclusively with Automation Type H (Human-Essential). |

**⚠️ Cv Boundary Criterion (confirmed in Domain 4 pilot — ratified):**
Assign Cv **only** when AI and physical robotics exposure are simultaneously active within the same task — when the AI and robotic components are operationally inseparable. Do **not** assign Cv when AI exposure and robotics exposure appear in different tasks within the same competency. The confirming paradigm cases from Domain 4:

- *4.5.4 T1 (drone operation):* The physical UAS (Ro) and the AI flight planning, obstacle avoidance, and automated modes (AI) are inseparable during the same flight operation → Cv
- *4.5.4 T2 (automated drone imagery capture):* Autonomous flight mission (Ro) and AI mission planning/geofencing (AI) operate simultaneously → Cv
- *4.6.2 T1 (GPS-guided precision planting):* Physical auto-steer tractor guidance (Ro) and AI prescription map management (AI) operate simultaneously during the same planting pass → Cv
- *4.6.2 T2 (integrated sensor management):* Physical yield monitors/drone platforms (Ro) and AI data stream analysis (AI) are used in combination for the same site-specific management decision → Cv

**Boundary test:** Can the AI exposure and the robotics exposure be operationally separated within the task? If yes → assign separate vectors to separate tasks. If no → assign Cv.

---

#### Dimension 5: Time Horizon

Classifies when the automation exposure is expected to reach meaningful professional impact — not when the technology exists, but when adoption reaches the level that affects practitioner workflows.

| Code | Label | Definition |
|------|-------|-----------|
| **1** | Deployed Now | Automation exposure is active at current deployment and is already affecting how practitioners perform this task in at least a substantial subset of professional contexts. |
| **2** | 3–5 Years | Automation is technically feasible and in early or pilot deployment, but has not yet penetrated the modal professional context. Expected to reach meaningful adoption within 3–5 years. |
| **3** | 5–10+ Years | Automation is technically possible but faces significant barriers to adoption (cost, regulatory, institutional, ecological complexity). Expected to reach meaningful deployment on a 5–10+ year horizon. |
| **N** | Human-Essential | No meaningful automation horizon. Used with Automation Type H. The task is structurally protected from automation by tacit knowledge density, relational requirements, or irreducible physical judgment. |

---

### 1.3 Standard Table Format

All task-level classification tables use this column structure:

| Competency Code | Competency Name | Task # | Task Description | Automation Type | Tacit Density | Career Ladder | Vector | Time Horizon | Notes |

**Notes column conventions:**
- Explain non-obvious classifications, especially H, Ac, V, and Cv calls
- Flag mode-split cases for practitioner validation
- Document Career Ladder Destruction signals where P-position tasks are classified S, Ac, or V
- Reference parallel cases in other skill areas where patterns recur
- Use **⚑ Delphi** flag for cases requiring expert panel adjudication

---

### 1.4 Flag Definitions

- **⚑ Delphi** — Flag for explicit Delphi panel presentation. Classification is defensible but contested, or requires practitioner ground-truth validation.
- **⚠️ Mode-Split** — The same task description encompasses both A-mode and V-mode deployment across different organizational contexts. Modal deployment used for classification; flag signals the need for practitioner validation.
- **◉ Career Ladder Destruction** — P-position task classified S, Ac, or V. Signals potential foreclosure of entry-level learning pathway through automation.
- **▶ Ro-Pending** — Robotics exposure is anticipated or emerging but not confirmed as modal deployment. Classification held at current-reality baseline pending practitioner validation.

---

### 1.5 Four Data Dictionary Additions from Task 12

These additions are to be integrated into the Data Dictionary sheet of `skills_taxonomy_workforce_v1.xlsx` before Task 13 begins.

**DD-1: A/V Boundary Criterion.** Classify based on current deployment reality. Human as primary executor = A. Automated system as primary executor with human oversight = V. Trajectory is captured by Time Horizon, not Automation Type.

**DD-2: Compressive Augmentation (Ac) Definition.** AI tools substantially reduce time or cognitive investment such that headcount compression is plausible without full substitution. Primarily affects administrative, documentation, and workflow coordination subtasks within otherwise Human-Essential competency clusters. Residual human role is review-and-certify, not primary execution.

**DD-3: Cv Boundary Criterion.** Simultaneous AI and physical robotics exposure on the same operational task. Both vectors inseparable within the task boundary. Do not assign Cv for AI in one task and robotics in another task within the same competency.

**DD-4: Domain 4 Pilot Findings Reference.** Zero Substitution across 105 tasks. 37% Human-Essential (physical execution tasks). Cv confirmed in drone operations (4.5.4 T1, T2) and precision agriculture (4.6.2 T1, T2). Ro-adjacent emerging in heavy equipment (4.5.3 T1, Time Horizon 2) and urban pipe inspection (4.7.3 T1, pending practitioner validation). Two primary career ladder destruction signals: 4.5.4 T2 (automated drone imagery capture, V/Cv/P) and 4.6.2 T1 (GPS-guided precision planting, V/Cv/P).

---

## Section 2: Domain 6 Stress Test Summary

### 2.1 Purpose and Scope

The Domain 6 (Policy, Planning & Regulatory Skills) stress test was the first application of the 5-dimension exposure instrument, conducted prior to the Domain 4 pilot. Domain 6 provided an opportunity to develop and calibrate the instrument against a governance-architecture domain where robotics exposure was not expected — enabling clean instrument testing of the AI, Ac, and Human-Essential categories before introducing the Ro and Cv complexity of field operations domains.

Domain 6 scope: 40 competencies × 3 tasks = 120 tasks across 8 skill areas (6.1–6.8).

### 2.2 Automation Type Distribution — Domain 6

| Type | Count | % | Notes |
|------|-------|---|-------|
| S (Substitution) | 9 | 7.5% | Concentrated in regulatory literature synthesis, compliance documentation, policy research, and comment triage tasks |
| Ac (Compressive Augmentation) | — | — | Identified as a needed category during stress test; retrospectively applicable to documentation-heavy tasks in 6.3 and 6.8 |
| A (Augmentation) | 64 | 53% | Dominant type; AI augments analysis, drafting, and regulatory research throughout |
| V (Supervision) | 11 | 9% | Primarily document management and workflow coordination with AI orchestration |
| H (Human-Essential) | 36 | 30% | Concentrated in tribal consultation, community engagement, stakeholder deliberation, and negotiation tasks |

### 2.3 Career Ladder Destruction Signals — Domain 6

Four tasks identified as near-term AI-addressable P-position tasks — all classified S, the only Substitution calls in the taxonomy to date:

| Code | Task Description | Type | Ladder | Notes |
|------|-----------------|------|--------|-------|
| 6.1.1 T2 | Regulatory literature synthesis | S | P | AI literature review tools at deployment threshold for regulatory research tasks |
| 6.1.2 T2 | Compliance documentation | S | P | AI document generation for standard compliance formats is deployed now |
| 6.4.1 T1 | Policy research synthesis | S | P | AI-assisted policy research and synthesis near-term substitutable |
| 6.4.4 T1 | Comment triage and categorization | S | P | AI comment classification and routing is deployed in public comment management systems |

### 2.4 Vector Distribution — Domain 6

Zero robotics (Ro) or Convergent (Cv) vectors across all 120 tasks — expected for a governance-architecture domain operating through documents, deliberation, and institutional relationships. This finding confirmed that Domain 6 was appropriate for instrument calibration rather than Ro/Cv testing, and that Domain 4 was the necessary stress test for physical automation vectors.

### 2.5 Instrument Refinements Arising from Domain 6

Two refinements were identified during the Domain 6 stress test and ratified before the Domain 4 pilot:

**Refinement 1 — A/V Clarifying Criterion:** During Domain 6 classification, ambiguity arose between Augmentation and Supervision when AI systems assisted with document workflows. The criterion was sharpened: classify based on current deployment reality (human vs. automated system as primary actor), with trajectory captured separately by Time Horizon.

**Refinement 2 — Compressive Augmentation (Ac) Category Added:** Administrative and documentation tasks in Domain 6 showed a pattern not captured by A or S: AI substantially reduced practitioner time investment without fully substituting the human role. The Ac category was added to capture this headcount-compression mechanism. Retrospective application to Domain 6 tasks flagged for database integration at Task 15/16.

### 2.6 Documentation Gap Notice

**⚠️ The full Domain 6 task-level classification table (120 rows) exists in a prior session record and has not been saved as a standalone project file.** This represents a documentation gap relative to the working record standard established by Tasks 10 and 11. 

**Recommended action at Task 13 close:** Produce a `domain6_task12_working_record.md` parallel to this document, reconstructing the Domain 6 table from session record. Alternatively, integrate Domain 6 task-level data directly into the Excel database during Task 13 database integration, treating the database as the authoritative record. Flag this decision point for Task 13.

---

## Section 3: Domain 4 Pilot Table

### Domain 4 Character Note

Domain 4 (Field Operations Skills) is the Fieldcraft-dominant domain: 80% of competencies carry Stage 4 (Implementation & Field Operations) as their Primary workflow stage tag, and nearly all competencies are Fieldcraft Primary under the craft assignment framework. This domain character has direct implications for exposure classification:

- **Physical execution tasks** are structurally protected from automation by the irreducibility of embodied, place-based judgment. Human-Essential classifications are expected and analytically defensible here in ways that Domain 6 governance tasks are not.
- **Monitoring and assessment subtasks** within implementation competencies are the primary AI Augmentation pathway — drone-assisted monitoring, AI image classification, remote sensing change detection, and digital data tools are deployed across all seven skill areas.
- **Administrative and documentation subtasks** are the primary Ac pathway — the same documentation compression pattern identified in Domain 6 administrative tasks appears in safety documentation, equipment management, and field reporting tasks throughout Domain 4.
- **Robotics (Ro) and Convergent (Cv) vectors** were absent from Domain 6 and are the primary stress-test targets for Domain 4. Cv confirms in drone operations (4.5.4) and precision agriculture (4.6.2). Ro-adjacent exposure is emerging but not yet dominant in heavy equipment and urban pipe inspection.

**Domain 4 Structure:** 7 skill areas, 5 competencies each, 3 tasks each = 105 tasks.

---

### Skill Area 4.1: Field Assessment & Monitoring

**Skill area character:** The monitoring and data collection foundation of Domain 4. Primary AI augmentation pathway is in digital data tools, drone-assisted assessment, and AI species/feature identification. Human-Essential classification concentrates in tasks requiring embodied sensory engagement — soil characterization by feel, wildlife sign interpretation, plant species identification in ambiguous cases. Ac appears in data transfer and cloud synchronization tasks. No robotics exposure at current deployment in 4.1.

| Competency Code | Competency Name | Task # | Task Description | Automation Type | Tacit Density | Career Ladder | Vector | Time Horizon | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 4.1.1 | Vegetation sampling and assessment | T1 | Establish vegetation monitoring plots; collect species composition, cover, density data | A | Hi | P | AI | 1 | Drone cover estimation and AI-assisted plot photography deployed now; ground-truth plot establishment and botanical judgment remain human-executed. Augmentation, not Substitution. |
| 4.1.1 | Vegetation sampling and assessment | T2 | Use digital data collection tools and GPS to record precise plot locations and measurements | A | Lo | P | AI | 1 | GPS and mobile apps (Survey123, Fulcrum) are standard augmentation. Task is largely procedural tool operation; tacit density is low. ⚑ Delphi: has digital data tool adoption compressed plot data collection crew sizes (Ac threshold)? |
| 4.1.1 | Vegetation sampling and assessment | T3 | Identify plant species in field using keys, apps, or expert consultation | A | Hi | P | AI | 1 | AI plant ID apps (iNaturalist, PlantNet) deployed widely. Verification of difficult taxa, look-alike species, and condition-based ecological judgment remains human-led. Classified A because verification judgment is the primary professional contribution. ⚑ Delphi: are practitioners accepting AI identification without independent verification? If yes, reclassify toward V. |
| 4.1.2 | Wildlife observation and sign interpretation | T1 | Conduct wildlife surveys using appropriate methods (transects, point counts, camera traps) | A | Hi | P | AI | 1 | Camera trap AI ID (Wildlife Insights, MegaDetector) and acoustic monitoring with AI species classification deployed. Physical transect and point count execution remains human. Classified A on survey execution component. |
| 4.1.2 | Wildlife observation and sign interpretation | T2 | Identify and interpret wildlife sign (tracks, scat, nests, feeding sign) | H | Hi | P | — | N | Sign interpretation requires embodied sensory engagement with landscape context. AI track recognition exists at low accuracy; behavioral interpretation of sign is not meaningfully automatable. **Paradigm Human-Essential case.** Among the strongest tacit knowledge claims in Domain 4. |
| 4.1.2 | Wildlife observation and sign interpretation | T3 | Use digital tools to document observations and manage wildlife data | A | Lo | P | AI | 1 | App-based documentation (eBird, iNaturalist, Survey123) is standard augmentation. Procedural tool use; low tacit content. |
| 4.1.3 | Water quality testing and aquatic surveys | T1 | Collect water samples and conduct field measurements (temperature, pH, DO, turbidity) | A | Med | P | AI | 1 | Calibrated probes/meters augment measurement; collection and QC judgment remain human. Med tacit: protocols standardized but anomalous reading recognition is field-developed. |
| 4.1.3 | Water quality testing and aquatic surveys | T2 | Conduct aquatic biological surveys (macroinvertebrates, fish, algae) | A | Hi | P | AI | 2 | eDNA sampling maturing and partially displacing physical macroinvertebrate surveys for presence/absence detection. Physical sorting, electrofishing, and algae ID remain human-executed. Time Horizon 2 because eDNA is at deployment threshold. ⚑ Delphi: how far has eDNA penetrated as primary method in practitioners' organizations? |
| 4.1.3 | Water quality testing and aquatic surveys | T3 | Use water quality sensors and data logging equipment | V | Med | P | AI | 1 | ⚠️ Mode-Split: deployed continuous monitoring sensor networks (sondes, data loggers) — the sensor is the primary data collector and the practitioner supervises. V is correct for deployed network mode. For single-measurement probe use in the field, A would apply. Classification reflects deployed network as the modal professional application at intermediate/advanced levels. **Flag for Delphi adjudication of mode boundary.** |
| 4.1.4 | Soil characterization and sampling | T1 | Describe soil profiles and horizons using standard terminology and methods | H | Hi | P | — | N | **Paradigm Human-Essential case.** Soil profile description requires standing in a pit, Munsell color under field light, structure and consistence assessment by hand, horizon sequence integration with drainage indicators. No current technology meaningfully automates this interpretive process. |
| 4.1.4 | Soil characterization and sampling | T2 | Collect soil samples for laboratory analysis (texture, nutrients, carbon, contaminants) | A | Med | P | AI | 1 | GPS-documented collection with app-based location and sample management. Physical collection is human-executed. ▶ Ro-Pending: automated soil coring systems exist in precision agriculture — not mainstream in environmental field operations. Flag for practitioner validation. |
| 4.1.4 | Soil characterization and sampling | T3 | Conduct field tests of soil properties (texture by feel, infiltration, compaction) | H | Hi | P | — | N | **Strongest tacit knowledge case in 4.1.** Texture by feel — rolling soil to estimate clay content from plasticity and grittiness — is a paradigm embodied skill that cannot be reproduced by any current technology. Human-Essential. |
| 4.1.5 | Digital data collection and management | T1 | Use mobile data collection apps to record field observations in real-time | A | Lo | P | AI | 1 | Apps (Survey123, Fulcrum, ODK) are deployed standard tools. Task is procedural tool operation; tacit content belongs to the observations being recorded, not the app use. |
| 4.1.5 | Digital data collection and management | T2 | Ensure data quality through validation, GPS accuracy checks, and photo documentation | A | Med | P | AI | 1 | Automated validation flags obvious errors; QC judgment — plausibility, adequacy, accuracy of GPS for monitoring purpose — remains human. **Reclassified from C to P (session record):** foundational data quality judgment is a P-level learning task even when performed imperfectly. |
| 4.1.5 | Digital data collection and management | T3 | Sync field data with office databases and GIS systems | Ac | Lo | P | AI | 1 | ◉ **Career Ladder Destruction — Ac/P.** Cloud sync and automated data pipeline tools have substantially compressed what was formerly manual data transfer and office-side entry work. Human role is workflow management and troubleshooting, not execution of transfer. Headcount compression in data management support roles plausible. |

---

### Skill Area 4.2: Land Management Implementation

**Skill area character:** The physical implementation backbone of Domain 4. Human-Essential classification is the dominant pattern: restoration planting, invasive removal, prescribed fire crew work, erosion control installation, trail construction, and trail maintenance are all embodied physical tasks with no meaningful automation at current deployment. AI Augmentation appears only in monitoring and adaptive management subtasks. Ac absent from 4.2. Zero robotics vectors. The 9 H / 5 A split reflects the skill area's essential function: authorized ecological action delivered by human hands in the landscape.

| Competency Code | Competency Name | Task # | Task Description | Automation Type | Tacit Density | Career Ladder | Vector | Time Horizon | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 4.2.1 | Restoration techniques and implementation | T1 | Implement restoration treatments including native planting, invasive removal, and soil amendments | A | Hi | P | AI | 1 | Planting layout apps, GPS-guided site marking, and species selection tools are deployed augmentation. Physical planting, grubbing, and amendment work remains human-executed. Tacit Hi: microsite condition reading (moisture pockets, aspect variation, planting depth) determines success. |
| 4.2.1 | Restoration techniques and implementation | T2 | Operate restoration equipment (seed drills, tree planters, mulch blowers) | A | Med | P | AI | 2 | GPS-guided auto-steer seed drills exist and are used in large-scale restoration seeding. ▶ Ro-Pending: In current conservation/restoration contexts, GPS-guided mechanized planters are not yet the modal deployment; practitioner operates equipment with GPS augmentation. Classified A now; reclassify to Cv if auto-steer adoption in restoration contexts has crossed supervision threshold. ⚑ Delphi: what is the actual adoption rate of GPS-guided planting equipment in practitioners' restoration work contexts? |
| 4.2.1 | Restoration techniques and implementation | T3 | Monitor restoration sites and adapt techniques based on success | A | Hi | C | AI | 1 | Drone imagery, remote sensing change detection, and AI-assisted cover analysis deployed. Adaptation decisions — reading why a treatment succeeded or failed — require tacit ecological judgment. C: monitoring and adaptive judgment emerge at intermediate proficiency; entry-level staff follow protocols. |
| 4.2.2 | Invasive species control | T1 | Implement invasive species control using mechanical, chemical, or biological methods | A | Hi | P | AI | 1 | AI-assisted detection and drone-based invasive mapping deployed for prioritization and targeting. Physical removal has no meaningful robotics exposure in conservation contexts. Chemical application via GPS-precision sprayers exists in agricultural contexts, not modal in environmental restoration. Tacit Hi: phenological timing and reinvasion risk judgment is field-developed. |
| 4.2.2 | Invasive species control | T2 | Use integrated pest management approaches minimizing environmental impacts | A | Med | C | AI | 1 | IPM decision support tools deployed augmentation. Integration judgment — tools, combination, timing — is where professional value lies. C: IPM strategy design requires intermediate ecology; entry-level practitioners follow prescribed methods. |
| 4.2.2 | Invasive species control | T3 | Monitor treatment effectiveness and adapt strategies | A | Med | C | AI | 1 | Drone monitoring, photo point analysis, AI vegetation change detection deployed. Trend interpretation and strategy adaptation require ecological judgment. C parallel to 4.2.1 T3. |
| 4.2.3 | Prescribed burning and fire management | T1 | Assist with prescribed fire operations following burn plans | H | Hi | P | — | N | **Paradigm Human-Essential case for 4.2.** No technology automates prescribed fire crew work — fireline maintenance, drip torch use, real-time fire behavior reading, situational awareness, escape route assessment. Among the highest tacit density in Domain 4. Primary site of foundational fire judgment development. |
| 4.2.3 | Prescribed burning and fire management | T2 | Monitor fire behavior and smoke during burns | A | Hi | C | AI | 1 | Fire weather data feeds (RAWS, spot forecasts), real-time perimeter mapping, smoke dispersion models deployed augmentation. Monitoring judgment integrates model outputs with direct sensory observation of current fire behavior. C: behavior analysis judgment is intermediate-level; entry-level practitioners observe and report. |
| 4.2.3 | Prescribed burning and fire management | T3 | Maintain fire equipment and ensure crew safety | H | Hi | P | — | N | Crew safety oversight — reading crew fatigue, recognizing behavioral safety signals, real-time escape route verification — is Human-Essential and cannot be delegated to technology. P: foundational safety awareness is the first professional capacity developed in fire practitioners. |
| 4.2.4 | Erosion control and watershed treatment | T1 | Install erosion control structures (check dams, wattles, silt fences) | H | Med | P | — | N | Physical erosion control structure installation has no AI or robotics penetration in environmental field operations. Med tacit: site-specific placement decisions (where drainage concentration points occur, slope angle requiring closer spacing) add field judgment. P: installation is entry-level core work. |
| 4.2.4 | Erosion control and watershed treatment | T2 | Implement bioengineering techniques for streambank stabilization | H | Hi | C | — | N | **Highest tacit density in 4.2.4.** Bioengineering (fascines, brush layers, live stakes, rootwads) requires reading bank hydrology, plant establishment dynamics, and integration of structural and biological mechanisms for site-specific conditions. No robotics or AI exposure. C: bioengineering judgment is intermediate-proficiency. |
| 4.2.4 | Erosion control and watershed treatment | T3 | Monitor erosion control effectiveness and adapt treatments | A | Med | C | AI | 1 | Drone surveys and AI-assisted change detection (photogrammetric volume change, gully detection) deployed. Adaptation decisions remain human. C pattern parallel to 4.2.1 T3 and 4.2.2 T3. |
| 4.2.5 | Trail construction and maintenance | T1 | Construct sustainable trail segments following design plans | H | Med | P | — | N | Physical trail construction has no AI or robotics exposure in current environmental field operations. Med tacit: sustainable construction requires terrain reading (water concentration, substrate stability) beyond design specs. P: physical construction technique is foundational. |
| 4.2.5 | Trail construction and maintenance | T2 | Maintain existing trails through brushing, drainage work, and tread repair | H | Med | P | — | N | Physical trail maintenance has no meaningful automation at current deployment. Maintenance judgment — recognizing deteriorating drainage features before erosion compounds — is Med tacit. P: standard foundational crew work and primary site of technique learning. |
| 4.2.5 | Trail construction and maintenance | T3 | Use appropriate tools and techniques for different trail types and conditions | H | Hi | C | — | N | Tool and technique selection for varied terrain and soil conditions — knowing when to excavate vs. fill, how to read substrate stability — is where trail expertise concentrates. Hi tacit: selection judgment is tacit and site-specific. C: tool selection and technique adaptation are intermediate-level proficiency. |

---

### Skill Area 4.3: Fire Management

**Skill area character:** The highest tacit density cluster in Domain 4. Fire management involves real-time situational judgment under life-safety conditions where the irreducibility test for Human-Essential is at its strongest. Six of 15 tasks are Human-Essential, concentrated in physical firefighting, firing operations, and burn boss execution. AI Augmentation appears in planning, modeling, BAER assessment, and monitoring subtasks. Zero robotics vectors. One X-position competency (4.3.2 T2, burn boss execution) — its Human-Essential and X classification means it carries no career ladder destruction risk.

| Competency Code | Competency Name | Task # | Task Description | Automation Type | Tacit Density | Career Ladder | Vector | Time Horizon | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 4.3.1 | Wildland firefighting | T1 | Construct and maintain fireline using hand tools or equipment | H | Hi | P | — | N | **Paradigm Human-Essential.** Fireline construction under dynamic fire conditions requires continuous situational awareness, real-time terrain and fire behavior reading, and crew coordination. Primary site of foundational firefighter tacit knowledge development. |
| 4.3.1 | Wildland firefighting | T2 | Implement firing operations to remove fuel ahead of fire | H | Hi | C | — | N | Firing operations require reading fire behavior, wind, and terrain in real time to direct ignition safely. C: firing leadership is an intermediate qualification (FFT1, squad boss level) requiring fire behavior judgment beyond entry-level. |
| 4.3.1 | Wildland firefighting | T3 | Mop up hot spots and ensure fire containment | H | Hi | P | — | N | Mop-up requires tactile and sensory reading of smoldering combustion — probing for heat below surface, ensuring containment under changing conditions. Experienced firefighters develop sensory read of heat, smoke, and fuel conditions. P: foundational skill that every firefighter develops regardless of qualification level. |
| 4.3.2 | Prescribed fire planning and execution | T1 | Develop comprehensive burn plans including objectives, prescriptions, and contingencies | A | Hi | C | AI | 1 | Fire behavior modeling software (BehavePlus, FOFEM, CONSUME) and smoke dispersion modeling deployed standard practice. Practitioner drives modeling and integrates with site knowledge. C: burn plan development is intermediate-level; entry-level practitioners assist with data collection. |
| 4.3.2 | Prescribed fire planning and execution | T2 | Conduct prescribed burns as burn boss ensuring objectives are met safely | H | Hi | X | — | N | **Strongest Human-Essential in 4.3.** Burn boss execution requires real-time synthesis of fire behavior, weather, smoke, crew positioning, public safety, and contingency activation — irreducibly human judgment under life-safety and resource-risk conditions. X: burn boss is advanced qualification (RXB1); career ladder destruction risk is not present at this position. |
| 4.3.2 | Prescribed fire planning and execution | T3 | Monitor fire effects and document burn outcomes | A | Med | C | AI | 1 | Drone aerial monitoring during and post-burn, AI-assisted vegetation analysis from burn imagery, digital documentation systems deployed. Monitoring judgment — reading whether fire effects meet objectives — remains human. Ac considered and rejected: documentation automation has not compressed crew positions in prescribed fire monitoring. |
| 4.3.3 | Fuels management | T1 | Assess fuels and develop treatment strategies (mechanical thinning, prescribed fire, grazing) | A | Hi | C | AI | 1 | LiDAR-derived canopy fuel data, FlamMap/FARSITE treatment effect modeling, AI-assisted fuel type classification from remote sensing deployed. Strategy development requires integrating ecological, operational, and fire behavior knowledge. C: fuels assessment and strategy development are intermediate-level proficiency. |
| 4.3.3 | Fuels management | T2 | Implement fuels treatments using appropriate methods and equipment | H | Med | P | — | N | Physical fuels treatment execution — hand thinning, pruning, chipping, mowing, pile burning — has no meaningful robotics or AI exposure in conservation/public lands contexts at current deployment. Mechanized equipment is operator-controlled. P: physical treatment implementation is core foundational work. |
| 4.3.3 | Fuels management | T3 | Monitor treatment effectiveness using fuel models and fire behavior analysis | A | Med | C | AI | 1 | Post-treatment fuel models, FlamMap re-runs, remote sensing change detection deployed. Effectiveness interpretation and adaptive strategy revision are human. C: fuel model interpretation is intermediate-level. |
| 4.3.4 | Fire weather and behavior analysis | T1 | Monitor fire weather and calculate fire danger indices | A | Med | P | AI | 1 | RAWS automated stations, fire danger calculators, fire weather platforms deployed standard tools. Human monitors, interprets, and acts on outputs. Med tacit: recognizing anomalous patterns and when indices diverge from observed conditions requires field judgment. P: weather monitoring is foundational for all fire practitioners during assignments. |
| 4.3.4 | Fire weather and behavior analysis | T2 | Predict fire behavior using weather, fuels, and topography data | A | Hi | C | AI | 1 | BehavePlus, FARSITE, FSPro, FlamMap deployed standard modeling tools. Professional value is in interpreting outputs against field conditions and recognizing when model assumptions fail — Hi tacit and human-irreducible. C: fire behavior prediction is intermediate-advanced proficiency (S-290, S-390 level). |
| 4.3.4 | Fire weather and behavior analysis | T3 | Brief fire personnel on expected fire behavior and weather trends | H | Hi | C | — | N | Briefings synthesize technical analysis with operational accountability — communicating what matters to whom under time pressure, with life-safety consequence. Hi tacit: reading what a crew needs vs. what is technically available, making synthesis credible in field conditions. C: briefing requires intermediate-level behavior analysis competence and authority. |
| 4.3.5 | Post-fire rehabilitation | T1 | Assess post-fire conditions and erosion risk using BAER protocols | A | Hi | C | AI | 1 | Satellite-derived burn severity mapping (dNBR), soil burn severity algorithms, ERMiT/WEPP erosion modeling deployed standard BAER tools. Ground-truthing of satellite data — verifying high-severity polygons against field conditions — is where Hi tacit concentrates. C: BAER assessment is intermediate-level proficiency. |
| 4.3.5 | Post-fire rehabilitation | T2 | Implement emergency stabilization treatments (mulching, seeding, barriers) | H | Med | P | — | N | Physical post-fire erosion control installation has no meaningful automation. Med tacit: urgency and timing judgment (window between containment and first rainfall) adds non-protocol knowledge. P: foundational implementation work with time-critical learning value. |
| 4.3.5 | Post-fire rehabilitation | T3 | Monitor post-fire recovery and adapt restoration approaches | A | Med | C | AI | 1 | Repeat drone surveys, satellite time-series analysis, AI-assisted vegetation recovery detection deployed. Adaptive interpretation — distinguishing expected recovery from concerning patterns — is human judgment. C: recovery monitoring requires intermediate post-fire succession ecology. |

---

### Skill Area 4.4: Safety & Emergency Response

**Skill area character:** The safety infrastructure layer of Domain 4, cross-cutting all field operations. Human-Essential classification concentrates in direct safety and emergency response tasks — crew safety oversight, remote field medical care, hazmat PPE use, and multi-agency incident coordination — none of which can be delegated to technology. The distinctive 4.4 pattern is the emergence of **Compressive Augmentation (Ac)** in administrative-overhead tasks: incident documentation, supply inventory management, maintenance scheduling, and pre-trip inspection records are all being compressed by AI-assisted reporting and digital management systems. Three Ac calls in 4.4 establish this as a recurring pattern across the domain's documentation layer.

| Competency Code | Competency Name | Task # | Task Description | Automation Type | Tacit Density | Career Ladder | Vector | Time Horizon | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 4.4.1 | Occupational safety and risk management | T1 | Conduct job hazard analyses before field activities | A | Hi | C | AI | 1 | Digital JHA templates and hazard checklist apps deployed; AI drafting of JHA documents from task descriptions is emerging. Defining contribution — recognizing non-obvious hazards in specific field conditions — is Hi tacit. C: leading JHAs requires intermediate-level risk recognition. ⚑ Delphi: if AI-assisted JHA generation compresses the cognitive work of hazard analysis, are early-career practitioners losing the developmental exercise of reasoning through risk independently? |
| 4.4.1 | Occupational safety and risk management | T2 | Ensure crew members use appropriate PPE and follow safety protocols | H | Hi | C | — | N | Behavioral safety management — reading crew fatigue, compliance gap under time pressure, injury-risk behavior — is Human-Essential. Relational and observational judgment not substitutable by technology. C: crew safety oversight requires supervisory authority and relationship knowledge at intermediate proficiency. |
| 4.4.1 | Occupational safety and risk management | T3 | Investigate incidents and near-misses to prevent recurrence | Ac | Med | C | AI | 1 | ◉ **Career Ladder Ac/C.** AI-assisted incident investigation report generation and root cause analysis frameworks increasingly producing first drafts. Investigation judgment — interviewing witnesses, reading physical scene, identifying systemic causes — remains human. Ac because documentation compression is real while investigation judgment is H. ⚑ Delphi: has AI-assisted incident documentation reduced the cognitive practice of constructing causal narratives in developing practitioners? |
| 4.4.2 | First aid and emergency medical response | T1 | Assess injuries and provide first aid in remote locations | H | Hi | P | — | N | Field trauma assessment and treatment in remote settings — reading injury severity without diagnostics, improvising treatment with available resources, evacuation decision-making — is Human-Essential. Hi tacit: wilderness medicine judgment develops through scenario training and field experience. P: basic first aid is a foundational competency expectation for all field practitioners. |
| 4.4.2 | First aid and emergency medical response | T2 | Coordinate medical evacuations when necessary | H | Hi | C | AI | 2 | Satellite communication tools, GPS coordinate sharing, digital evacuation planning tools deployed. Evacuation coordination judgment — patient stability, terrain and weather constraints, timing tradeoffs — remains Human-Essential. AI vector at Time Horizon 2: AI-assisted evacuation routing and helicopter coordination tools in development for wilderness contexts. C: evacuation coordination requires intermediate-level wilderness medicine authority. |
| 4.4.2 | First aid and emergency medical response | T3 | Maintain first aid supplies and medical certifications | Ac | Lo | P | AI | 1 | ◉ **Career Ladder Destruction — Ac/P.** Inventory management systems, certification tracking apps, and automated restocking alerts substantially compress manual inventory and certification calendar management. Administrative compression; low developmental consequence (physical maintenance skill is not compressed). |
| 4.4.3 | Search and rescue operations | T1 | Participate in search operations using established search patterns | A | Hi | P | AI | 1 | AI-assisted probability of area modeling (SARTopo, CalTopo with AI lost-person behavior prediction) and drone-assisted aerial search deployed. Physical search — navigating terrain, recognizing clues, pattern discipline under fatigue — remains human. P: foundational search participation is entry-level. |
| 4.4.3 | Search and rescue operations | T2 | Navigate to remote locations using map, compass, and GPS | A | Med | P | AI | 1 | GPS and digital navigation tools (CalTopo, OnX, Gaia) deployed standard augmentation alongside traditional navigation. Med tacit: route selection and terrain hazard judgment requires field experience. P: navigation is foundational for all field practitioners. ⚑ Delphi: has GPS augmentation begun to displace traditional navigation competence in early-career practitioners — creating a vulnerability in GPS-failure scenarios? |
| 4.4.3 | Search and rescue operations | T3 | Provide emergency care and assist with evacuation | H | Hi | P | — | N | Emergency care and physical evacuation assistance — assisting injured subject across terrain, real-time care decisions, group management under stress — is Human-Essential. Note: drone-based supply delivery to subjects before rescue team arrival is emerging but does not change task classification at current deployment. |
| 4.4.4 | Hazardous materials awareness and response | T1 | Identify potential hazardous materials in field settings | A | Med | P | AI | 1 | AI-assisted hazmat identification tools, digital SDS databases, drone-based remote assessment of suspected hazmat sites deployed. Recognition of potential hazard from sensory field cues remains human. P: hazmat awareness is foundational safety expectation. |
| 4.4.4 | Hazardous materials awareness and response | T2 | Implement appropriate containment and notification procedures | H | Med | C | — | N | Containment and notification judgment — severity assessment, response sequencing, resource determination under uncertainty — is Human-Essential. C: hazmat response beyond awareness (HAZWOPER Operations level) is intermediate proficiency. |
| 4.4.4 | Hazardous materials awareness and response | T3 | Use personal protective equipment for hazmat situations | H | Hi | P | — | N | PPE selection and use in active hazmat situations requires real-time contamination risk judgment, PPE limitation awareness, and donning/doffing under field conditions — tacit judgment that training creates and deployment tests. P: foundational safety competency. |
| 4.4.5 | Emergency communication and incident reporting | T1 | Use radios, satellite phones, and emergency beacons to communicate during incidents | A | Med | P | AI | 1 | Communication technology (satellite messengers, digital radio systems, dispatch integration apps) deployed standard augmentation. Communication judgment — priority, clarity, crisis communication under stress — is human. P: foundational communication competency for all field practitioners. |
| 4.4.5 | Emergency communication and incident reporting | T2 | Document incidents thoroughly following organizational protocols | Ac | Lo | C | AI | 1 | ◉ **Career Ladder Ac/C.** AI-assisted incident report drafting and standardized digital documentation platforms substantially compress incident documentation time. Lo tacit: reporting format is procedural; investigative judgment is in 4.4.1 T3. ⚑ Delphi: does AI compression of incident report writing reduce the cognitive practice of constructing narrative accounts, impairing analytical thinking development in contributing-level practitioners? |
| 4.4.5 | Emergency communication and incident reporting | T3 | Coordinate with emergency responders and dispatch centers | H | Hi | C | — | N | Multi-agency emergency coordination — managing information flows between field teams, dispatch, medical resources, and command — is Human-Essential. Hi tacit: experienced coordinators develop read of organizational dynamics, resource availability, and communication load management under active emergency. C: coordination requires intermediate ICS competence and institutional relationships. |

---

### Skill Area 4.5: Equipment Operation

**Skill area character:** The primary Ro and Cv stress-test zone for Domain 4. Hand tools (4.5.1) and power equipment (4.5.2) are straightforwardly Human-Essential — powered tools operated by expert human judgment are categorically distinct from autonomous robotic systems. The Ro boundary is tested at 4.5.3 (heavy equipment auto-steer, Ro/Time Horizon 2) and definitively confirmed at 4.5.4 (drone/UAS operations, Cv). Two V calls at P-position (4.5.4 T2) represent the primary career ladder destruction signal in this skill area: the foundational data collection task in drone-based environmental monitoring has been converted from skilled physical execution to automation supervision before practitioners develop the contextual judgment needed to supervise intelligently. Ac appears in administrative maintenance management tasks.

| Competency Code | Competency Name | Task # | Task Description | Automation Type | Tacit Density | Career Ladder | Vector | Time Horizon | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 4.5.1 | Hand tool proficiency | T1 | Select and use appropriate hand tools for vegetation management, trail work, and restoration | H | Med | P | — | N | Hand tool selection and use has no AI or robotics exposure at current deployment. Physical technique and selection judgment are purely tacit, developed through practice. P: most basic entry-level physical proficiency in Domain 4. |
| 4.5.1 | Hand tool proficiency | T2 | Maintain tools in safe working condition through sharpening and repair | H | Med | P | — | N | Tool maintenance is embodied physical skill — reading edge quality, identifying handle stress, knowing repair limits — with no meaningful automation. P: foundational equipment responsibility for all field staff. |
| 4.5.1 | Hand tool proficiency | T3 | Transport and store tools safely | H | Lo | P | — | N | Procedural task with minimal tacit content. H because no technology automates this physical responsibility. Lo tacit: protocols are well-specified. P: foundational safety behavior. Lowest analytical significance task in Domain 4 — present for taxonomy completeness. |
| 4.5.2 | Power equipment operation | T1 | Operate chainsaws safely for tree falling, bucking, and limbing | H | Hi | P | — | N | Chainsaw operation — felling decisions, hinge wood control, kickback avoidance, tree lean and stress reading — is among the most tacit and safety-critical physical skills in Domain 4. No automation exists for in-field chainsaw judgment. P: foundational chainsaw competency built through supervised practice. |
| 4.5.2 | Power equipment operation | T2 | Use string trimmers, brush cutters, and mowers for vegetation management | H | Med | P | — | N | Power equipment for vegetation management is physical skill with no meaningful automation in varied terrain and vegetation conditions of environmental field operations. Robotic mowers exist in commercial grounds maintenance but not in environmental field operations contexts. P: standard foundational field competency. |
| 4.5.2 | Power equipment operation | T3 | Maintain and troubleshoot small engines | A | Med | C | AI | 1 | Digital diagnostic tools, AI-assisted troubleshooting guides, manufacturer diagnostic software deployed augmentation. Hi tacit component in field diagnosis — reading vibration, smell, sound with limited tools — retained. C: engine troubleshooting emerges at intermediate proficiency; entry-level performs basic maintenance. |
| 4.5.3 | Heavy equipment and vehicle operation | T1 | Operate tractors, excavators, or skid steers for restoration or construction | A | Hi | C | Ro | 2 | ▶ Ro-Pending. GPS-guided auto-steer deployed at scale in agricultural contexts (Time Horizon 1 there). In environmental restoration and construction contexts — modal use case for this competency — GPS-guided auto-steer and semi-autonomous excavator/skid steer operation at Time Horizon 2 (3–5 years). Physical operation for ecological grading, channel reconstruction, and restoration earthwork requires continuous terrain-reading judgment that is Hi tacit. A rather than V at current deployment reality. **Not Cv:** AI image analysis is not simultaneously active with robotic guidance on this operational task at current deployment. ⚑ Delphi: what is the actual adoption rate of GPS-guided auto-steer in restoration-context heavy equipment? |
| 4.5.3 | Heavy equipment and vehicle operation | T2 | Drive four-wheel drive vehicles in off-road conditions | H | Hi | P | — | N | Off-road vehicle operation — reading surface stability, selecting lines, managing traction on slopes — is Hi tacit judgment developed through field experience. No meaningful automation at current deployment for off-road environmental field vehicles. P: basic vehicle operation is foundational for all field staff. |
| 4.5.3 | Heavy equipment and vehicle operation | T3 | Perform pre-trip inspections and basic maintenance | Ac | Lo | P | AI | 1 | ◉ **Career Ladder Destruction — Ac/P.** Digital pre-trip inspection checklists, telematics systems tracking vehicle condition, automated maintenance scheduling substantially compress manual inspection logging and fleet coordination. Physical inspection tasks remain; administrative coordination is Ac-compressed. Lo tacit: inspection procedure is protocol-driven. |
| 4.5.4 | Drone/UAS operation for field applications | T1 | Operate drones safely following FAA regulations for environmental monitoring | A | Med | P | Cv | 1 | **Cv — explicit boundary reasoning.** FAA-regulated drone operation involves simultaneous AI and robotic exposure on the same task: (1) the UAS is a physical robotic system being operated, and (2) AI flight planning, obstacle avoidance, and automated modes are active simultaneously. Both vectors are inseparable during the same flight operation → Cv. Med tacit: FAA compliance and safe flight are protocol-governed, but weather windows, terrain hazards, and subject wildlife behavior during flight add field judgment. P: drone operation is increasingly foundational with Part 107 certification as a baseline expectation. |
| 4.5.4 | Drone/UAS operation for field applications | T2 | Capture aerial imagery and video for site assessment or mapping | V | Med | P | Cv | 1 | ◉ **PRIMARY CAREER LADDER DESTRUCTION SIGNAL — V/Cv/P.** Modern drone platforms fly automated grid/orbit missions autonomously; the human supervises the automated flight, monitors for safety anomalies, and manages capture settings. The drone is the primary data collection actor during automated missions — V by current deployment reality. Cv: automated flight system (Ro) and AI flight planning/object avoidance (AI) are simultaneously active. P: image capture is an entry-level drone application and primary site of skill development — but automation supervision is not equivalent to learning experiential data collection judgment. Career ladder disruption mechanism: entry-level practitioners are placed in oversight roles over autonomous systems before developing the ecological and technical judgment needed to recognize when automated outputs are wrong. |
| 4.5.4 | Drone/UAS operation for field applications | T3 | Process drone data to create orthomosaics, 3D models, or vegetation maps | A | Med | C | AI | 1 | Photogrammetry software (Pix4D, Agisoft, DroneDeploy) automates primary processing pipeline; AI vegetation classification augments analysis. Practitioner configures parameters, QCs outputs, interprets results. C: data processing requires intermediate photogrammetry, GIS, and ecological interpretation. Note: T3 is Datacraft in character, crossing into Domain 2 territory — expected given hybrid nature of UAS competencies. |
| 4.5.5 | Equipment maintenance and repair | T1 | Perform scheduled maintenance on equipment and vehicles | Ac | Lo | P | AI | 1 | ◉ **Career Ladder Destruction — Ac/P.** Digital maintenance scheduling systems, telematics alerts, AI-assisted maintenance interval prediction substantially compress manual tracking and scheduling. Physical maintenance tasks (oil changes, filter replacement, lubrication) remain human-executed; administrative coordination is Ac-compressed. Lo tacit: scheduled maintenance follows manufacturer protocols. |
| 4.5.5 | Equipment maintenance and repair | T2 | Diagnose equipment problems and make repairs | A | Hi | C | AI | 1 | AI-assisted diagnostic tools, digital troubleshooting trees, manufacturer remote diagnostic systems deployed. Hi tacit in field diagnosis — reading vibration, smell, sound with limited tools, improvising repairs with available parts — irreducibly experiential. C: equipment diagnosis and repair emerges at intermediate proficiency. |
| 4.5.5 | Equipment maintenance and repair | T3 | Manage maintenance records and parts inventory | Ac | Lo | C | AI | 1 | Fleet management software, parts inventory systems with automated reorder points, digital maintenance record platforms substantially compress manual record-keeping. Administrative coordination. Lo tacit: data entry and inventory management procedural. C: maintenance program management requires intermediate understanding of equipment lifecycles and procurement. |

---

### Skill Area 4.6: Sustainable Agriculture Implementation

**Skill area character:** The highest-technology density cluster in Domain 4 and the primary Cv confirmation zone for precision agriculture. The contrast with 4.2 (9/15 Human-Essential) is analytically significant: 4.6 produces only 2 Human-Essential calls across 15 tasks. Both domains are Fieldcraft-primary by craft assignment, but the mechanization and sensor infrastructure of precision agriculture has dramatically shifted the automation exposure profile relative to conservation/restoration implementation. Two V calls at P-position (4.6.2 T1) constitute the second primary career ladder destruction signal in Domain 4. The Ac pattern appears in documentation and record-keeping tasks. Cv confirmed in 4.6.2 T1 and T2.

| Competency Code | Competency Name | Task # | Task Description | Automation Type | Tacit Density | Career Ladder | Vector | Time Horizon | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 4.6.1 | Regenerative practice implementation | T1 | Implement cover cropping, diverse rotations, and reduced tillage systems | A | Hi | P | AI | 1 | AI-assisted cover crop species selection tools, precision planting guidance, and tillage optimization software deployed augmentation. Ecological judgment — reading soil conditions, selecting species mixes, adapting timing to weather and cropping context — is Hi tacit and remains human-executed. P: cover cropping implementation is entry-level agricultural practice. |
| 4.6.1 | Regenerative practice implementation | T2 | Integrate livestock using rotational grazing or other regenerative approaches | H | Hi | C | AI | 2 | Livestock integration judgment — reading animal behavior, forage condition, water access, stress signals across paddock moves — is Hi tacit and Human-Essential at current deployment. AI grazing management apps and sensor-based paddock monitoring at Time Horizon 2. C: livestock integration requires intermediate agricultural ecology; entry-level practitioners follow prescribed rotation schedules. |
| 4.6.1 | Regenerative practice implementation | T3 | Monitor and adapt regenerative farming systems based on ecological indicators | A | Hi | C | AI | 1 | Digital monitoring platforms, AI-assisted soil health trend analysis, remote sensing vegetation indices deployed augmentation. Adaptive ecological judgment — why a system is or isn't performing and what to change — is Hi tacit. C: adaptive systems management requires intermediate agricultural ecology and systems thinking. |
| 4.6.2 | Precision agriculture technology use | T1 | Operate GPS-guided tractors and implements for precise planting and application | V | Med | P | Cv | 1 | ◉ **PRIMARY CAREER LADDER DESTRUCTION SIGNAL — V/Cv/P.** GPS-guided auto-steer tractors are deployed at scale in commercial agriculture. Auto-steer system executes precise field navigation autonomously; operator supervises, monitors for anomalies, manages headland turns. V by current deployment reality: automated system is primary task executor. Cv — explicit boundary reasoning: physical auto-steer guidance system (Ro) and AI prescription map management (AI) are operationally inseparable during the same planting pass → Cv. Med tacit: supervising automated operation requires field knowledge to recognize system failures, but substantially less tacit than non-automated equipment operation. P: equipment operation is entry-level in precision agriculture contexts. Career ladder disruption mechanism: entry-level practitioners develop automation supervision judgment rather than embodied equipment operation skills; the tacit substrate supporting intelligent supervision is not being formed. |
| 4.6.2 | Precision agriculture technology use | T2 | Use soil sensors, yield monitors, and drone imagery for site-specific management | A | Med | C | Cv | 1 | **Cv classification.** Soil sensors (AI-processed), yield monitors (GPS+sensor integration), and drone imagery (UAS + AI analysis) are used in combination for the same site-specific management decision. When used together as described, the same decision faces simultaneous AI and physical platform exposure → Cv. A rather than V: practitioner actively interprets and makes decisions from data streams rather than supervising an automated system. C: integrating multiple precision data streams requires intermediate understanding of soil-crop relationships and technology integration. |
| 4.6.2 | Precision agriculture technology use | T3 | Develop and implement variable rate application prescriptions | A | Med | C | AI | 1 | AI-assisted prescription generation software (using soil test data, yield maps, satellite imagery) produces variable rate maps for practitioner review and implementation. Practitioner contribution: agronomic plausibility judgment, site-knowledge adjustment, implementation oversight. ⚑ Delphi: in contexts where AI prescription generation is highly automated, has this crossed the Ac threshold — with agronomist time investment significantly compressed to review-and-certify? |
| 4.6.3 | Integrated pest management application | T1 | Scout crops for pests and monitor population levels against action thresholds | A | Hi | P | AI | 1 | AI-assisted pest identification apps, automated trap monitoring, drone-based crop scouting deployed augmentation. Physical scouting — walking fields, reading plant symptoms, finding early instar stages that automated systems miss — retains Hi tacit content. P: crop scouting is entry-level agricultural practice and primary site of pest identification skill development. |
| 4.6.3 | Integrated pest management application | T2 | Implement cultural, biological, and chemical pest control as part of IPM programs | A | Med | C | AI | 1 | IPM decision support tools guide treatment selection; precision application equipment with GPS targeting deployed. Physical implementation requires timing and dosage judgment. C: IPM strategy implementation requires intermediate pest ecology and agricultural systems knowledge. |
| 4.6.3 | Integrated pest management application | T3 | Document pest management activities and evaluate effectiveness | Ac | Lo | C | AI | 1 | ◉ **Career Ladder Ac/C.** Digital record-keeping platforms, AI-assisted effectiveness analysis, automated regulatory compliance documentation substantially compress IPM record-keeping and reporting. Lo tacit: documentation protocol-driven. Ac is cleaner here than in 4.4.1 T3 because effectiveness analysis itself is increasingly AI-assisted, compressing analytical time investment for mid-career IPM practitioners. |
| 4.6.4 | Irrigation management and water conservation | T1 | Schedule irrigation based on crop water needs, soil moisture, and weather | V | Med | C | AI | 1 | **V classification.** Weather-based automated irrigation controllers and AI-driven scheduling systems (ET models, soil moisture sensor networks, weather forecasts) deployed at scale in commercial agriculture and increasingly in conservation programs. Systems schedule and execute irrigation autonomously; practitioner oversees, reviews, and overrides when sensors or models fail. V by current deployment reality. C: irrigation system oversight requires intermediate understanding of crop water relationships; entry-level practitioners operate systems following established schedules. |
| 4.6.4 | Irrigation management and water conservation | T2 | Operate and maintain irrigation systems (drip, sprinkler, flood) | A | Med | P | AI | 1 | Automated systems control valves and timing; physical operation — leak checking, pressure testing, drip system clog management, sprinkler adjustment — remains human-executed. Med tacit: reading system performance from physical indicators. P: irrigation system operation is foundational agricultural practice. |
| 4.6.4 | Irrigation management and water conservation | T3 | Implement water conservation practices and technologies | A | Med | C | AI | 1 | Deficit irrigation scheduling tools, soil moisture-based automation, water use efficiency analytics deployed augmentation. Conservation technology implementation requires agronomic judgment for site-specific configuration. C: conservation technology implementation requires intermediate water management knowledge. |
| 4.6.5 | Soil health assessment and management | T1 | Conduct soil health assessments using field tests and laboratory analysis | A | Hi | P | AI | 1 | Soil health assessment apps, AI-assisted test result interpretation, digital field assessment tools deployed augmentation. Field tests — aggregate stability, infiltration, earthworm counts, slaking — require physical execution and site-reading judgment that is Hi tacit. P: soil health assessment is entry-level in agricultural conservation contexts. |
| 4.6.5 | Soil health assessment and management | T2 | Implement practices that build soil organic matter and biological activity | H | Hi | C | — | N | Soil health management implementation — cover crop termination timing, compost application rate and placement, reduced tillage adaptation to field conditions — requires ecological judgment about how current soil conditions should inform management choices. Irreducible Fieldcraft contribution: reading soil, crop, and weather interactions in real time. No meaningful automation at current deployment for adaptive implementation judgment. C: soil health management requires intermediate agricultural ecology. |
| 4.6.5 | Soil health assessment and management | T3 | Monitor soil health trends and adapt management | A | Hi | C | AI | 1 | AI-assisted soil health trend analysis, satellite-derived vegetation indices as soil biological activity proxies, digital monitoring platforms deployed augmentation. Adaptive management judgment — interpreting why metrics are or aren't improving — is Hi tacit. C: trend interpretation and adaptive response require intermediate ecological systems knowledge. |

---

### Skill Area 4.7: Urban Environmental Infrastructure

**Skill area character:** 4.7 operates at the intersection of ecological field work and built-environment systems maintenance. Urban forestry, green infrastructure, and stormwater management introduce the urban scale and commercial equipment context. Key findings from pattern hypothesis testing: (1) Green infrastructure installation confirms the 4.2 pattern — physical implementation is Human-Essential with AI augmentation appearing only in monitoring and performance subtasks, not installation execution. (2) Urban forestry equipment (aerial lifts, chippers, stump grinders) is operator-controlled powered equipment, categorically equivalent to 4.5.2 power equipment — **no Ro exposure confirmed.** (3) Urban tree health assessment confirms the Human-Essential hypothesis for ISA-standard sensory diagnosis. (4) One V call at 4.7.5 T3 (BMS monitoring) is at C-position and structurally parallel to 4.1.3 T3 sensor supervision. (5) One pending Ro validation at 4.7.3 T1 (commercial robotic pipe inspection).

| Competency Code | Competency Name | Task # | Task Description | Automation Type | Tacit Density | Career Ladder | Vector | Time Horizon | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 4.7.1 | Green infrastructure installation | T1 | Install bioswales, rain gardens, and permeable pavement for stormwater management | H | Med | P | — | N | **Confirms 4.2 pattern hypothesis.** Physical installation — excavating bioswale cells, placing media layers, establishing grading, setting permeable pavement substrate — has no meaningful AI or robotics exposure at current deployment. Urban construction equipment is operator-controlled. Med tacit: reading existing drainage patterns, soil conditions, and design intent against site reality. P: installation assistance is foundational entry-level work. |
| 4.7.1 | Green infrastructure installation | T2 | Construct green roofs and living walls | H | Hi | C | — | N | Higher tacit density than bioswale installation: reading structural load capacity, sequencing waterproofing/drainage/media layers with integrity judgment, plant selection for constrained rooftop conditions. No robotics or AI exposure. C: green roof/living wall construction requires intermediate building systems, horticulture, and waterproofing knowledge — source text confirms intermediate as the level for full green roof installation. |
| 4.7.1 | Green infrastructure installation | T3 | Monitor green infrastructure performance and maintain installations | A | Med | C | AI | 1 | Digital performance monitoring platforms (sensor networks, flow meters, infiltration monitoring), AI-assisted performance trend analysis, drone-based visual inspection deployed augmentation. Physical maintenance remains human-executed. C: performance interpretation and adaptive maintenance require intermediate stormwater system function knowledge. |
| 4.7.2 | Urban forestry operations | T1 | Plant and establish trees using appropriate techniques for urban conditions | H | Hi | P | — | N | Urban tree planting involves substantially higher tacit density than rural planting: reading soil compaction and drainage constraints, recognizing below-grade infrastructure conflicts not visible on plans, establishing aftercare appropriate to urban stress factors (heat island, drought, reflected radiation). Hi tacit: urban site-reading is qualitatively distinct from standard horticultural planting. P: planting is foundational entry-level work and primary site of urban site-reading skill development. |
| 4.7.2 | Urban forestry operations | T2 | Prune trees following ISA standards for health, safety, and structure | H | Hi | C | — | N | **Strongest tacit knowledge case in 4.7.** ISA-standard pruning requires reading tree architecture — branch attachments, included bark, decay presence at junctions — making irreversible cuts affecting structure for decades. No technology automates this judgment. **Ro-adjacency hypothesis test result: aerial lifts, chippers, and stump grinders are operator-controlled powered equipment, categorically equivalent to 4.5.2 power tools — not robotic systems.** Hi tacit: structural pruning judgment develops through ISA training and mentored field experience. C: structural pruning requires ISA Certified Arborist-level knowledge. |
| 4.7.2 | Urban forestry operations | T3 | Assess and manage urban tree health, pests, and diseases | H | Hi | C | AI | 2 | **Human-Essential at current deployment with AI augmentation trajectory — Time Horizon 2.** ISA-standard tree health assessment requires probing decay with mallet, reading crown dieback patterns, identifying pest frass, integrating visual and tactile cues into diagnosis. Embodied sensory engagement is irreplaceable at current deployment → H. AI tree health diagnostic apps (drone crown assessment, AI symptom identification from photos) advancing toward deployment → AI vector at Time Horizon 2. C: diagnosis requires ISA Certified Arborist-level knowledge. ⚑ Delphi: at what proficiency threshold does AI-assisted diagnosis adequately substitute for in-person assessment? |
| 4.7.3 | Stormwater system management | T1 | Inspect and clean stormwater infrastructure (catch basins, pipes, outlets) | A | Med | P | AI | 2 | ▶ Ro-Pending. Robotic pipe inspection systems (CCTV crawlers, robotic catch basin inspectors) are commercially deployed in municipal stormwater contexts. Human-conducted physical inspection remains the dominant mode across most settings in this competency's scope. A reflects modal deployment; Time Horizon 2 for Ro because robotic inspection penetration is accelerating. ⚑ Delphi: in municipal MS4 programs specifically, has robotic pipe inspection displaced human inspection as the primary method? If yes, reclassify to V/Ro. |
| 4.7.3 | Stormwater system management | T2 | Monitor stormwater quality and implement pollution prevention | A | Med | C | AI | 1 | Real-time stormwater quality sensors, automated sampling systems, AI-assisted discharge analysis deployed augmentation. Illicit discharge investigation — tracing sources through a system, reading visual/olfactory cues, smoke/dye testing — requires field judgment that is Med tacit. C: stormwater quality monitoring and pollution prevention require intermediate MS4/NPDES regulatory knowledge. |
| 4.7.3 | Stormwater system management | T3 | Maintain vegetated stormwater BMPs (bioswales, detention ponds) | A | Med | P | AI | 1 | Drone-based vegetation assessment, AI-assisted BMP performance monitoring, digital maintenance tracking deployed augmentation. Physical maintenance — mowing, sediment removal, replanting — remains human-executed. Med tacit: reading whether a BMP is performing as designed from vegetation condition and ponding patterns. P: physical BMP maintenance is foundational and entry-level site of urban stormwater skill development. |
| 4.7.4 | Urban habitat restoration | T1 | Remove invasive species and restore native plant communities in urban settings | A | Hi | P | AI | 1 | AI-assisted invasive species mapping (drone-based, satellite-derived), digital restoration planning tools, urban ecology databases deployed augmentation. Physical removal and native planting retains Hi tacit density: reading urban soil and hydrological conditions, selecting natives adapted to urban stressors, judging plant establishment under non-ideal conditions. P: urban restoration implementation is entry-level field work. Note: urban context raises tacit density relative to rural restoration — public safety constraints, community interface, and urban infrastructure interactions all require field judgment. |
| 4.7.4 | Urban habitat restoration | T2 | Create wildlife habitat features (brush piles, nest boxes, pollinator gardens) | H | Med | P | — | N | Physical habitat feature construction and installation has no meaningful AI or robotics exposure. Med tacit: placement judgment — nest box positioning, brush pile structure for shelter quality, pollinator planting bloom sequence — is field-developed ecological judgment that exceeds protocol specification. P: habitat feature installation is foundational field work accessible at entry level. |
| 4.7.4 | Urban habitat restoration | T3 | Engage urban residents in restoration through volunteer programs | H | Hi | C | — | N | Community engagement for urban restoration is Human-Essential: trust-building with diverse urban communities, volunteer safety management, cultural/linguistic navigation, reading group dynamics during restoration events. Hi tacit: effective urban community engagement requires reading social dynamics, adjusting communication style across community contexts, managing ecological goals against community ownership — irreducibly human relational judgment. C: community engagement program management requires intermediate facilitation and community development knowledge. |
| 4.7.5 | Green building systems maintenance | T1 | Maintain green roofs and living walls (irrigation, vegetation, drainage) | A | Med | P | AI | 1 | BMS with automated irrigation scheduling, sensor-based moisture monitoring, and remote system alerts deployed standard tools. Physical maintenance — inspecting growing media, replanting, cleaning drainage layers, checking membrane integrity — remains human-executed. A rather than V: BMS augments by monitoring and alerting; human executes maintenance response. Med tacit: reading plant health under rooftop stress and interpreting sensor data against visible plant condition. P: routine green system maintenance is foundational building operations work. |
| 4.7.5 | Green building systems maintenance | T2 | Service rainwater harvesting and greywater systems | A | Med | C | AI | 1 | Automated system monitoring, flow sensors, digital maintenance tracking deployed. Physical servicing — cleaning cisterns, checking filters, inspecting distribution lines, verifying disinfection function — remains human-executed. Med tacit: diagnosing underperformance against design expectations requires integrating monitoring data with physical inspection. C: rainwater/greywater system operation requires intermediate plumbing and water reuse regulatory knowledge. |
| 4.7.5 | Green building systems maintenance | T3 | Monitor building environmental system performance | V | Lo | C | AI | 1 | ⚠️ Mode-Split. Building management systems (BMS) conduct continuous automated monitoring of green roof moisture, rainwater cistern fill, living wall irrigation cycles, indoor air quality — generating performance dashboards. Practitioner reviews BMS outputs, identifies anomalies, initiates maintenance responses. BMS is the primary monitoring actor → V by current deployment reality. Lo tacit: BMS dashboard review is primarily procedural data interpretation. C: BMS oversight requires intermediate understanding of system performance parameters and failure modes. **Parallel to 4.1.3 T3 (water quality sensor supervision):** same mode-split applies — in organizations without sophisticated BMS, this task reverts to A. Flagging for Delphi adjudication alongside 4.1.3 T3. |

---

## Section 4: Domain 4 Pattern Summary

### 4.1 Automation Type Distribution — Full Domain 4 (105 tasks)

| Type | Count | % | Structural Notes |
|------|-------|---|-----------------|
| H (Human-Essential) | 39 | 37% | Concentrated in physical execution tasks across 4.2 (9/15), 4.3 (6/15), 4.4 (8/15), 4.5 (5/15), 4.7 (6/15). Near-absent in 4.6 (2/15) — the precision agriculture contrast finding. |
| A (Augmentation) | 48 | 46% | Distributed across all 7 skill areas. Primary pathway: monitoring/assessment subtasks within implementation competencies where drone, remote sensing, AI classification, and digital tools augment human-executed observation and judgment. |
| Ac (Compressive Augmentation) | 8 | 8% | Concentrated in documentation, administrative, and workflow coordination subtasks: safety records (4.4.1 T3, 4.4.5 T2), supply management (4.4.2 T3), maintenance scheduling (4.5.3 T3, 4.5.5 T1, T3), data sync (4.1.5 T3), IPM documentation (4.6.3 T3). **Absent from 4.7** — urban systems generate less administrative overhead from field work than fire/safety/equipment domains. |
| V (Supervision) | 5 | 5% | Water quality sensor networks (4.1.3 T3), automated drone mapping missions (4.5.4 T2), GPS-guided precision planting tractors (4.6.2 T1), automated irrigation scheduling (4.6.4 T1), BMS performance monitoring (4.7.5 T3). |
| S (Substitution) | 0 | 0% | **Zero across all 105 Domain 4 tasks.** The physical execution character of Domain 4 provides structural protection from full substitution that governance-documentation domains (Domain 6: 7.5% Substitution) cannot claim. |

**Domain 4 vs. Domain 6 contrast:**

| Type | Domain 4 | Domain 6 | Interpretation |
|------|---------|---------|---------------|
| S | 0% | 7.5% | Physical execution resists substitution; governance documentation does not |
| A | 46% | 53% | Augmentation is the dominant pattern in both domains |
| V | 5% | 9% | Sensor/BMS supervision in D4; document workflow supervision in D6 |
| H | 37% | 30% | Physical embodiment provides more H protection than governance work |
| Ac | 8% | ~8% est. | Documentation compression is structurally similar across domains |

### 4.2 Automation Vector Distribution — Full Domain 4

| Vector | Count | % | Notes |
|--------|-------|---|-------|
| — (None) | 39 | 37% | All H-classified tasks; no automation exposure |
| AI only | 52 | 50% | Augments monitoring, modeling, documentation, and identification tasks across all 7 skill areas |
| Cv (Convergent) | 4 | 4% | 4.5.4 T1, 4.5.4 T2 (drone operations); 4.6.2 T1, 4.6.2 T2 (precision agriculture). Confirms Cv as specific, identifiable condition — not a general property of equipment operation. |
| Ro (Time Horizon 2) | 1 | 1% | 4.5.3 T1 (heavy equipment auto-steer, Time Horizon 2, pending practitioner validation) |
| AI (Ro-Pending) | 1 | 1% | 4.7.3 T1 (urban pipe inspection — practitioner validation needed; may reclassify to V/Ro) |
| AI (Time Horizon 2–3) | 8 | 8% | Tasks where AI vector is confirmed but adoption is emerging rather than deployed |

**Key vector finding:** Cv appears in Domain 4 as anticipated — concentrated in drone operations and precision agriculture, exactly where the instrument predicted simultaneous AI and physical robotic system exposure. Ro-only exposure is minimal: physical equipment operated by expert human judgment is categorically distinct from autonomous robotic systems. The Cv boundary criterion holds cleanly across all Domain 4 cases.

### 4.3 Career Ladder Destruction Signals — Full Domain 4

| Code | Task | Type | Ladder | Severity | Notes |
|------|------|------|--------|----------|-------|
| 4.1.5 T3 | Cloud data sync | Ac | P | Low | Administrative compression; physical field data collection not compressed |
| 4.4.1 T1 | Job hazard analysis (AI-drafted) | A | C | Moderate | Developmental compression risk under Augmentation — cognitive practice of hazard reasoning may be bypassed; flagged for Delphi |
| 4.4.1 T3 | Incident investigation documentation | Ac | C | Moderate | Narrative reasoning compression; loss of investigative writing development |
| 4.4.2 T3 | First aid supply management | Ac | P | Low | Administrative compression; direct care skills not compressed |
| 4.4.5 T2 | Incident documentation | Ac | C | Moderate | Narrative reasoning compression; loss of account-construction development |
| 4.5.3 T3 | Pre-trip inspection records | Ac | P | Low | Administrative compression; inspection physical judgment not compressed |
| **4.5.4 T2** | **Automated drone imagery capture** | **V** | **P** | **High** | **Primary signal. Entry-level drone work converted to automation supervision before foundational data collection judgment is established. Career ladder disruption mechanism: automation supervision ≠ experiential skill building.** |
| 4.5.5 T1 | Scheduled equipment maintenance records | Ac | P | Low | Administrative compression; physical maintenance skills not compressed |
| 4.5.5 T3 | Maintenance records and parts inventory | Ac | C | Low | Administrative compression |
| **4.6.2 T1** | **GPS-guided precision planting** | **V** | **P** | **High** | **Primary signal. Entry-level precision agriculture converted to automation supervision before embodied equipment operation skills are established. Career ladder disruption mechanism parallel to 4.5.4 T2.** |
| 4.6.3 T3 | IPM documentation | Ac | C | Moderate | Analytical compression of effectiveness evaluation judgment |
| 4.7.5 T3 | BMS performance monitoring | V | C | Low-Moderate | Supervision of automated building monitoring; C-position reduces priority relative to P-position V signals |

### 4.4 Career Ladder Destruction Typology: Two Mechanisms

The Domain 4 pilot, in combination with the Domain 6 stress test, establishes that career ladder destruction operates through two structurally distinct mechanisms. Both matter for workforce development, but they require different interventions.

**Mechanism 1 — Cognitive Pathway Compression (Domain 6 pattern)**
Near-term AI substitution of early-career cognitive tasks that build analytical reasoning capacity. The affected tasks are governance-documentation tasks: regulatory literature synthesis, compliance documentation, policy research, comment triage. These tasks were the primary cognitive training ground for developing practitioners — the intellectual work of reading, synthesizing, and writing regulatory analysis that builds the practitioner's ability to reason about complex policy problems. When AI substitutes for this work, the development opportunity disappears. The practitioner may occupy the job title without developing the underlying analytical capacity. The long-term workforce consequence is a generation of practitioners who can oversee AI regulatory analysis without being able to evaluate its quality.

*Intervention:* Redesign early-career learning pathways to intentionally recreate the cognitive development that substituted tasks formerly provided — structured analysis exercises, mentor-reviewed analytical writing, deliberate practice in reasoning without AI assistance.

**Mechanism 2 — Embodied Pathway Displacement (Domain 4 pattern)**
Automation supervision replacing skill-building physical execution before the tacit knowledge substrate supporting intelligent supervision is established. The affected tasks are entry-level physical tasks now performed autonomously by drone systems (4.5.4 T2) or precision agriculture equipment (4.6.2 T1). These tasks are not cognitively complex — but they are experientially foundational. Flying a manual drone mapping mission teaches the practitioner to read terrain, weather, and subject behavior in ways that supervising an automated mission does not. Operating conventional farm equipment builds the embodied understanding of soil-machinery interaction that makes it possible to recognize when automated operation is producing incorrect results. When automation displaces this physical practice before the tacit substrate is formed, the practitioner supervises without comprehension — they can monitor the output but cannot evaluate its adequacy.

*Intervention:* Pair automation supervision responsibilities with deliberate embodied practice requirements. Require practitioners to demonstrate non-automated competency before being granted automation supervision roles. Design training scenarios where automated systems are disabled or degraded to force practitioners to operate without the automation they will routinely depend on.

---

## Section 5: Pending Practitioner Validation Items

The following items are flagged for Delphi panel adjudication or practitioner validation surveys. All classifications are defensible at current deployment reality but rest on assumptions about modal deployment or adoption rates that practitioners in specific profession families and sectors are better positioned to confirm.

---

**Item 1 — 4.1.3 T3: Water quality sensor supervision (V vs. A mode-split)**
*Classification held:* V (deployed continuous monitoring networks)
*The question:* Does the modal professional application of this task use deployed sensor networks (→ V) or single-measurement field probes used by the practitioner (→ A)? The V classification reflects advanced/intermediate practitioners managing sensor networks; the A classification would apply at foundational level. Practitioner validation needed by profession family context — particularly F4 (Water Resources) and F8 (Environmental Policy & Regulation) practitioners operating MS4 monitoring programs.
*Parallel case:* 4.7.5 T3 (BMS monitoring) carries the same mode-split flag and should be adjudicated simultaneously.

---

**Item 2 — 4.1.1 T3: Plant species identification — verification behavior trajectory**
*Classification held:* A (verification judgment retained as primary professional contribution)
*The question:* Are practitioners accepting AI identification (iNaturalist, PlantNet) without independent verification in practice? If yes as a widespread behavioral norm, the correct current-deployment classification is closer to V. The classification is anchored to the professional standard — verification is expected — not to observed field behavior. Delphi question: does practitioner identification behavior in your work context match the standard, or has AI tool adoption shifted identification toward unverified acceptance?
*Relevant profession families:* F1 (Forestry), F2 (Wildlife & Fisheries), F3 (Ecological Restoration), F5 (Conservation Science).

---

**Item 3 — 4.2.1 T2: GPS-guided planting equipment adoption rate in restoration contexts**
*Classification held:* A/AI/Time Horizon 2 (GPS-guided planting not yet modal in conservation/restoration)
*The question:* What is the actual adoption rate of GPS-guided auto-steer seed drills and mechanized planters in ecological restoration (vs. agricultural) contexts? If adoption has crossed the supervision threshold in restoration seeding programs, reclassify to Cv. Practitioner validation needed particularly from F3 (Ecological Restoration) and F1 (Forestry) practitioners doing large-scale reforestation and native seeding.

---

**Item 4 — 4.3.2 T2: Burn boss execution (Human-Essential confirmation)**
*Classification held:* H/X (Human-Essential, advanced qualification)
*The question:* Not a reclassification candidate — this is a Delphi confirmation question. Do practitioners with burn boss experience confirm that real-time burn execution judgment cannot be meaningfully delegated to technology at current or foreseeable deployment? This is a paradigm H case for the taxonomy's argument about tacit knowledge protection; practitioner confirmation strengthens the workforce forecasting argument.
*Relevant profession families:* F1 (Forestry), F3 (Ecological Restoration), F12 (Fire Management).

---

**Item 5 — 4.5.3 T1: Heavy equipment auto-steer in restoration contexts**
*Classification held:* A/Ro/Time Horizon 2
*The question:* What is the actual adoption rate of GPS-guided auto-steer and semi-autonomous operation for tractors, excavators, and skid steers in environmental restoration and construction — as distinct from commercial agriculture? If adoption has reached a level where V is the dominant mode in restoration earthwork contexts, reclassify to V/Cv.
*Relevant profession families:* F3 (Ecological Restoration), F4 (Water Resources), F1 (Forestry).

---

**Item 6 — 4.6.2 T3: Variable rate application prescription — Ac threshold**
*Classification held:* A (significant AI augmentation, human agronomic judgment retained)
*The question:* In contexts where AI prescription generation is highly automated, has the practitioner's analytical time investment been compressed to review-and-certify at the Ac threshold? Practitioner validation needed from F10 (Sustainable Agriculture) practitioners in commercial precision agriculture contexts where AI prescription tools (Climate FieldView, Granular, John Deere Operations Center) are at maximum maturity.

---

**Item 7 — 4.7.3 T1: Robotic pipe inspection penetration in municipal MS4 programs**
*Classification held:* A/AI/Time Horizon 2 (human-conducted inspection as modal deployment)
*The question:* In municipal MS4 programs specifically — where robotic CCTV inspection systems are most commercially mature — has robotic inspection displaced human inspection as the primary method for catch basin and pipe inspection? If yes, reclassify to V/Ro. Validation needed from F8 (Environmental Policy & Regulation) and F4 (Water Resources) practitioners in municipal stormwater management roles.

---

**Item 8 — Career Ladder Developmental Consequence Questions (all Ac calls in 4.4)**
*Competencies:* 4.4.1 T1 (JHA), 4.4.1 T3 (incident documentation), 4.4.5 T2 (incident reporting)
*The question:* AI assistance for safety documentation tasks compresses cognitive work that formerly required independent reasoning. Does AI-assisted JHA generation reduce the developmental value of hazard analysis practice for early-career practitioners? Does AI-assisted incident report drafting reduce the analytical practice of constructing causal narratives? These questions are not about reclassification but about workforce development consequence. Delphi framing: "In your organization, has AI assistance for safety documentation changed how new practitioners develop hazard analysis reasoning or incident investigation thinking?"
*Relevant profession families:* All field-oriented families; weight toward F1, F2, F3, F12.

---

**Item 9 — 4.5.4 T2 and 4.6.2 T1: Career ladder destruction validation**
*Competencies:* 4.5.4 T2 (automated drone imagery capture, V/Cv/P) and 4.6.2 T1 (GPS-guided precision planting, V/Cv/P)
*The question:* These are the two primary career ladder destruction signals in Domain 4. Delphi questions: (a) Do practitioners in drone-intensive roles confirm that entry-level practitioners primarily supervise automated missions rather than executing manual ones? (b) Has this changed how new practitioners develop the site-reading and monitoring judgment that experienced drone operators demonstrate? (c) Do precision agriculture practitioners confirm that entry-level operators primarily supervise auto-steer systems rather than developing embodied equipment operation skills? (d) Is there evidence that automation supervision without embodied practice produces practitioners who cannot recognize when automated outputs are wrong?
*Relevant profession families:* F2 (Wildlife & Fisheries), F5 (Conservation Science), F7 (Environmental Data Science) for drone questions; F10 (Sustainable Agriculture) for precision agriculture questions.

---

*Document status: Task 12 complete. Instrument ratified for Task 13 application. Domain 4 pilot table confirmed in session, February 2026. Next: Task 13 — Full Exposure Classification, Domains 1–3 and 5.*

*Cross-references: `taxonomy_task_sequence_v3.md` (task dependencies), `20251202_SkillsTaxonomy_Core_V2__1_.txt` (source taxonomy), `taxonomy_task11_working_record.md` (craft assignments, Domain 4), `taxonomy_task10_working_record.md` (workflow stage tags, Domain 4).*
