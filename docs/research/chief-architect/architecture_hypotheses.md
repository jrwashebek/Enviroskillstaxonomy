# EMST v2 Architecture Hypotheses (PROVISIONAL)

**Author:** Chief Taxonomy Architect (CA) · **Date:** 2026-10-23 · **Status:** PROVISIONAL. These are working hypotheses written to focus Phase 1 research. They are not decisions. I will resolve them in Phase 3 against the evidence the research roles produce. Disagree openly; tell me which hypothesis your evidence breaks.

Read with: `docs/audit/architecture-audit.md` (the v1 findings these options respond to) and `docs/audit/v1_carry_forward_register.csv`.

Labels: [E] evidence (source IDs in `sources.csv`), [J] judgment, [S] speculation.

---

## 1. Design requirements any option must meet

Each requirement comes from the charter, the team brief, or a v1 failure documented in the audit.

| # | Requirement | Why |
|---|---|---|
| R-1 | Represent **jobs/roles** and their change over time | Vision: "how its jobs are changing"; v1 has no role layer [E: audit §6] |
| R-2 | Represent **craft blends** on work units and aggregate them to roles and people | Theory of change; v1 craft is collinear with domain [E: audit §5] |
| R-3 | Represent **sector actors** as structured context, with transfer frictions | Mobility across 7 actors; v1 has 5 free-text notes [E: audit §7] |
| R-4 | Keep **durable capability** separate from **fast tool fluency** | Team brief §6; 27 v1 competencies embed tools or standards [E: audit §4] |
| R-5 | **Observable, assessable** proficiency | First job (HR, training); v1 levels are tenure bands [E: audit §4.3] |
| R-6 | **Task-level** exposure and change signals, each dated and attributed | v1 instrument is right in concept, wrong in representation [E: audit §10] |
| R-7 | **Persistent IDs, versioning, crosswalks as artifacts** | Interoperability; upstream churn (O*NET quarterly; OPM consolidation to Sep 2027) [E: CA-027, CA-044] |
| R-8 | **Coverage beyond public lands** without bloating the core | Lead decision; v1 has zero drinking-water, wastewater, marine or utility competencies [E: audit §6] |
| R-9 | **Usable tomorrow** by an HR specialist, a training officer, a curriculum lead and an early-career worker | Team brief §6 [J: means a small number of views, not the full graph] |
| R-10 | **Governable** by many organizations over many years | Charter (adoption, stewardship); ASC shows a national taxonomy can go unmaintained [E: CA-036] |

---

## 2. Three architecture options

All three share a common substrate. That substrate is non-negotiable in my current judgment [J]:

- **Persistent opaque IDs.** v1 codes are kept as aliases.
- **Typed entities.** Each entity is typed by kind: work, worker attribute, context, event, or mapping.
- **A task layer.** Tasks are many-to-many with competencies and roles, and exposure assessments attach to them.
- **A tools layer** that is separately versioned.
- **A change-signal layer** made of dated events.
- **A crosswalk layer** made of versioned artifacts.

The options differ in **which entity is the spine**, **where users enter**, and **how coverage and governance scale**.

### Option A — Competency hub, layered (evolutionary)

**Shape.** Typed core competencies stay the central entity. Tasks link to competencies (many-to-many). Role profiles reference competencies, each with an importance and a target level. Crafts are weights on tasks, and the system rolls them up to competencies and roles. Proficiency is a generic level scale plus competency-specific anchors at the levels where the competency is practiced.

```
Reference vocab ─┬─ Core competencies (typed) ◄──► Tasks ◄── exposure assessments, craft weights, signals
                 │          ▲                          ▲
                 │          └──── Role profiles ───────┘ (importance, level, sector-actor variants)
                 └─ Tools layer ──► Tasks        Crosswalks ──► roles, tasks, competencies
```

**Strengths.**
- Closest to v1, so migration is fastest and the most v1 content is reused.
- Matches the language federal and state HR already uses: OPM competency models, state class specs, competency-based training. [J; FH and SL to confirm]
- Easiest for curriculum leads. [J]

**Weaknesses.**
- Competencies are the most abstract and hardest-to-validate unit. Raters disagree more on abstract descriptors than on tasks, which is why O*NET applies extra safeguards to skills ratings. [E: CA-016]
- It risks re-creating v1's grain problem.
- Mobility and exposure analysis still depend on the task layer, so the "hub" is partly cosmetic.

**Best if:** FH and SL find that agencies will adopt only competency-model-shaped artifacts, and IO finds a competency grain that can be assessed.

### Option B — Task-and-role graph (NICE / O*NET pattern)

**Shape.** Atomic statements are the spine: Task, Knowledge and Skill statements in NICE style, or tasks plus detailed work activities (DWAs) in O*NET style. Work roles are bundles of tasks and knowledge/skill statements. Competencies become *curated views*: named clusters of statements that serve HR, training and curriculum. Crafts are weighted at the task level. Proficiency comes from levels of responsibility (SFIA-like), applied to role levels.

```
Work functions ─► Tasks / Knowledge / Skill statements (atomic, persistent IDs)
                        ▲              ▲
           Work roles (bundles + levels)   Competency views (curated clusters for users)
```

**Strengths.**
- Highest analytical power. Exposure, NLP mapping from postings, position descriptions (PDs) and plans, O*NET and Anthropic Economic Index (AEI) joins, and task-overlap mobility metrics all operate natively.
- NICE shows this pattern can run a fast-changing field in a federal context. It does so with persistent statement IDs, retained/new/withdrawn status, and boundary hand-offs to the DoD Cyber Workforce Framework (DCWF). [E: CA-033]
- "How jobs are changing" becomes "how a role's task bundle and exposure profile change between versions", which can be computed.

**Weaknesses.**
- Large inventory: NICE carries about 2,100 statements for one field. [E: CA-033] Environmental management across many subsectors could be several times larger. [S]
- Heavy burden on subject-matter experts (SMEs).
- Least legible to early-career workers and to many HR users.
- Risk of fragmentation into near-duplicate statements without strong editorial control.

**Best if:** IA and LM show that the main adoption value is data interoperability and analytics, and IO finds that tasks validate far more reliably than competencies.

### Option C — Federated core + subsector extensions (modular)

**Shape.**
- A small, stable sector-wide **core** containing: reference vocabularies (crafts, levels of responsibility, sector actors, work functions); a transversal practice layer; and roughly 100–250 durable cross-subsector competencies with their tasks.
- **Subsector extension modules** (water and wastewater, air, waste and remediation, energy, forestry, fire, marine, ESG, environmental health, …). Each uses the shared schema with namespaced IDs, has a named steward (a professional society, agency consortium or university center), and has its own review cycle.
- **Fast layers** (tools, signals) updated monthly or continuously.

```
CORE (annual): vocab · transversal practice · core competencies+tasks · level scale · sector actors
  ├── module: water/wastewater (steward X)  ├── module: fire (steward Y)  ├── module: ESG (steward Z) …
FAST (monthly): tools/methods/standards · change signals          CROSSWALKS (track upstream releases)
```

**Strengths.**
- Scales coverage to many subsectors without a central team writing everything.
- Puts depth where SMEs want it and keeps the core simple for adoption.
- Aligns governance with the bodies that already hold legitimacy in each subsector.
- Echoes the NICE–DCWF federation [E: CA-033] and the "stable core with domain plug-ins" idea raised in SFIA 10 consultation workshops (attendee proposals, not SFIA decisions). [E: CA-034]
- Best fit for a multi-organization standard. [J]

**Weaknesses.**
- Governance-heavy: module stewards, conformance rules, conflict resolution.
- Module quality will be uneven.
- Cross-module mobility needs a shared task and competency spine, or it fragments.
- Risk of forks.
- Slower to a credible federal and state MVP unless the first modules are commissioned centrally.

**Best if:** AS finds credible stewards and DB confirms that subsector communities have their own standards to bring.

---

## 3. Trade-off summary

| Criterion | A: Competency hub | B: Task-role graph | C: Federated core+modules |
|---|---|---|---|
| R-1 roles and change over time | Medium | **High** | Medium–High (if spine is shared) |
| R-2 craft blends | Medium (needs tasks anyway) | **High** | High (inherits spine) |
| R-3 sector actors and mobility | Medium | **High** | High |
| R-4 durable vs tools | High | High | High |
| R-5 assessable proficiency | Medium (abstract unit) | High at task, lower at role | Varies by module |
| R-6 exposure and signals | Medium | **High** | High |
| R-7 interoperability | Medium | **High** | High (namespacing) |
| R-8 coverage | Low–Medium (central authoring) | Medium | **High** |
| R-9 usability tomorrow | **High** | Low (needs views) | Medium–High |
| R-10 multi-org governability | Medium | Medium | **High** (but costly) |
| Migration effort from v1 | **Low** | High | Medium |

[J — each cell is my provisional rating; the research roles should challenge them]

---

## 4. Provisional lean (not a decision)

My current lean is a **hybrid**. I will keep or drop it depending on what the research roles find. [J]

- **Internal spine:** B's task-and-role graph, because R-1, R-2, R-3, R-6 and R-7 all depend on it. Every option needs the task layer anyway.
- **User-facing packaging:** A's typed core competencies, because that is how people hire and train. A competency is a curated, assessable cluster of task and knowledge statements with anchored levels.
- **Coverage and governance:** C's federation. A small core is centrally governed. Subsector modules get stewards. Fast layers run on their own cadence.

As layers:

| Layer | Contents | Cadence (hypothesis) | Main owners of evidence |
|---|---|---|---|
| L0 Reference vocabularies | Crafts (with reproduction-regime attributes), level-of-responsibility scale, sector actors and sub-types, work functions (generalized from S1–S6), subsectors, jurisdictions | Annual or slower | CA, FC/DC/SC, IO, SL/TN/PS |
| L1 Core competencies and transversal practice | Typed, durable capabilities; transversal practice (ethics and integrity, human-AI practice, safety culture, systems thinking); anchored indicators | Annual | IO, LC, FC/DC/SC |
| L2 Tasks (and knowledge statements) | Atomic work statements, many-to-many with L1 and L3; craft weights; work-function tags; crosswalked to O*NET tasks and DWAs | Semi-annual | FC/DC/SC, DB, IA |
| L3 Role profiles | Function-defined roles; task bundles (importance, time share); competency targets; computed craft blend; sector-actor variants; entry and progression links; lifecycle status | Semi-annual | FH, SL, PS, TN, CM |
| L4 Tools, methods and standards | Software, instruments, models, protocols, reporting frameworks → tasks | Monthly | DC, FC, PS |
| L5 Change signals and assessments | Exposure assessments (attributed, dated), posting, PD and plan-requirement signals, policy events, foresight scenarios; computed change indicators incl. CLD and reproduction fragility | Continuous, with review | LM, FS, IA, SC |
| L6 Crosswalks | O*NET-SOC and tasks, ESCO, OPM series and quals, state classes, CIP, credentials, private job architectures; match type and confidence | Track upstream | IA, FH, SL, LC, PS |
| Modules | Namespaced extensions across L1–L4 for subsectors | Steward-defined, inside core rules | DB, AS |

### How sector actors enter (hypothesis)

Sector actor is **context, not content**. A role profile has sector-actor *variants* that share a function and a core task bundle but differ in tasks, authority, crosswalks and frictions. Competencies get *enactment notes* only where the actor changes the performance itself, which matters most for Statecraft (federal trust-responsibility consultation, state administrative process, Tribal government processes, corporate disclosure). Tribal nations are modelled as sovereign governments and employers, and inclusion follows TN's protocol. Transfer frictions between actors are first-class attributes. [J]

### Crafts: profiles, not tags (hypothesis)

Each task carries a craft weight vector, elicited with v1's irreducibility test as the anchored rubric, rated by several raters, and carrying a confidence value. Competency and role blends are computed. Craft "reproduction regime" attributes record how each craft is learned and lost, and they feed CLD and curriculum design. The fallback, if weights prove unreliable, is a 3-level ordinal per craft per task (none / supporting / defining). [J; S on reliability — IO pilot decides]

### What gets computed rather than stored

Stability, breadth (the v1 "zero-Core" idea), family relevance, competency-level exposure summaries, CLD at the pathway level, craft blends, and all dashboard counts. [J]

---

## 5. Decisions I expect to make in Phase 3 (named decision points)

- **DP-1** Spine entity: competency (A) vs statement graph (B) vs hybrid.
- **DP-2** Top-level organization: work functions × subsector modules (orthogonal facets), or a single hierarchy.
- **DP-3** Competency typing rules and target grain (what counts as core competency vs task vs knowledge vs tool).
- **DP-4** Proficiency model: generic responsibility levels plus anchors vs competency-specific scales; number of levels.
- **DP-5** Craft representation: weights vs ordinal; elicitation protocol.
- **DP-6** Role-profile grain for the federal and state MVP, and the first role set.
- **DP-7** Sector-actor representation and the Tribal protocol boundary.
- **DP-8** Exposure model: which external measures to ingest; how v1 analyst values are labelled; scenario conditioning.
- **DP-9** Governance: core and module stewardship, release cadences, change process, host.
- **DP-10** Disposition of each v1 element (finalizing the carry-forward register).

---

## 6. Architectural questions each role's findings should settle

Please address the questions for your role code explicitly, either in your report's "Open questions for the Chief Taxonomy Architect" section or in a short section titled "Answers to CA architecture questions". Evidence-labelled answers are most useful. "The evidence is thin" is a valid answer.

### LM — Labor Market & AI-Impact
1. Which task-level AI exposure or usage measures (e.g. Anthropic Economic Index task shares, Eloundou-style rubrics, Felten AIOE, O*NET-linked indices) are methodologically sound enough to **ingest as attributed assessments** on EMST tasks, and which only as context? (DP-8)
2. Is there any external evidence that can corroborate or refute v1's **Ac** (compressive augmentation) and **CLD** patterns in environmental work, e.g. staffing changes, posting shifts in entry-level roles, PD rewrites?
3. What minimum evidence standard should a **change-signal** record meet before it moves a role's change indicator?
4. Does evidence specific to the environmental sector support distinguishing **augmented / automated / new work** at the task level, or only at the occupation level?

### FS — Strategic Foresight
1. What **scenario structure** should the change-signal layer carry, e.g. v1's investment × adoption-mode matrix or something better? Should exposure assessments be scenario-conditioned? (DP-8)
2. How should the model represent **roles that don't exist yet**: emerging role profiles with lifecycle status "proposed", or placeholder task bundles?
3. What **horizon-scanning cadence and intake** should feed L5, and who reviews it?

### FC — Field Craft
1. Can Fieldcraft be expressed as **weights on tasks** without losing what matters (judgment earned outdoors)? What anchors would raters need? (DP-5)
2. Which field competencies are **durable**, and where is field technology changing the task bundle versus only the tools layer?
3. How can **place-based tacit knowledge** be made observable for assessment without reducing it to protocol? Which **reproduction-regime** attributes (mentorship, seasons in the field, place-boundness) matter?
4. Is the v1 claim that "H arises only from FC/SC" supported or an artifact of how the coding was set up? (See audit §10.2.3.)

### DC — Data Craft
1. Where exactly is the line between **durable data competencies** and **tool fluency** (L1 vs L4)? Please give a rule, not just examples. (DP-3)
2. Are responsible-AI capabilities (validation of AI outputs, model risk, provenance) **transversal practice** or Datacraft competencies, or both, with enactments?
3. What progression from data literacy to expert modelling fits a **level-of-responsibility** scale? (DP-4)

### SC — Statecraft
1. Does Statecraft vary across sector actors enough to need **actor-specific competencies**, or is it one competency with **actor-specific enactments**? (DP-7)
2. Is the generalized work-function facet (assess → plan → authorize → implement/operate → monitor → enforce → learn → engage) adequate across federal, state, local, Tribal and private contexts? What replaces the six US-federal reform flags as **dated driver events**?
3. What does **teachable, observable** Statecraft look like at each level?

### DB — Domain Expert Bench
1. What is the **subsector list** for v2 modules, and which subsectors have their own standards or credential bodies that could act as stewards? (DP-2, DP-9)
2. Where does a sector-wide generalization (core competency or task) **break** in your subsector?
3. Is "domain" the right top level, or should **work functions × subsectors** be orthogonal facets?

### FH — Federal Human Capital
1. What **grain** does skills-based hiring need: task, competency with proficiency, or role? What can an HR specialist use *tomorrow*? (DP-6)
2. Which OPM artifacts must the role layer crosswalk to (series, qualification standards, competency models, assessments), and how should the crosswalk track the **April 2026 series consolidation** and later redesign phases? [E: CA-044]
3. Please verify or correct the v1 family→SOC mappings flagged in audit §6.
4. What proficiency scale would OPM-aligned users accept? (DP-4)

### SL — State & Local
1. What does a minimum role layer need to look like to **crosswalk to 50 state classification systems**? Role variants or separate roles?
2. Which state and local roles (utilities, special districts, county environmental health) must be in the MVP?

### TN — Tribal Nations & Sovereignty (simulated; flags what needs real consultation)
1. How should Tribal nations enter the model: as sovereign governments and employers (sector actor), as a jurisdictional context, or both? What must **not** be included? (DP-7)
2. What review and consent protocol must apply before content like v1's 7.1.1 (Indigenous data sovereignty) or any L2 material is published?
3. What data-governance rules apply to change signals that touch Tribal programs?

### PS — Private Sector
1. What units do private employers hire and pay on (roles, certifications, skills), and how should private **job architectures** crosswalk to EMST role profiles?
2. Which v1 competencies don't translate into private hiring terms, and the reverse?

### IO — Job Analysis & Validation
1. Which spine (competency vs task statement) can be **validated** to a defensible standard first? (DP-1)
2. Can raters reliably produce **craft weights**? Please design the pilot (tasks × raters) and the agreement statistic. (DP-5)
3. Should proficiency use generic levels of responsibility plus behavioral anchors, or competency-specific levels only where practiced? How many levels? (DP-4)
4. What is the **minimum validity evidence** for a v2.0 release used in training versus one used in selection?

### LC — Learning & Curriculum
1. At what grain do curriculum designers and accreditors (SAF, ABET, CIP-mapped programs) need competencies and levels? (DP-3, DP-4)
2. How should competencies link to **credentials** (Open Badges, CLR, CTDL), and does the transversal layer help program design?
3. How should CLD signals turn into **learning-path design**, e.g. deliberate formation tasks?

### CM — Career Mobility & Workforce Voice (simulated voices; flags what needs real practitioners)
1. Which similarity basis predicts real transitions best: **task overlap, competency overlap, or craft-blend vectors**? What does that require of L2 and L3?
2. What **transfer-friction** attributes between sector actors must be first-class?
3. What outcome metrics should decide expansion beyond the pilot, and what data must the model hold to compute them?

### IA — Interoperability & Skills Intelligence
1. What standard mapping fits the layered model (CASE, CTDL/RSD, SKOS/JSON-LD, HR Open, IEEE 1484.20.3)? What is the **ID scheme**, and how are namespaced modules handled? (DP-9)
2. What should the **NLP mapping target** be (task statements vs competencies)? How will confidence and drift be recorded in L5?
3. Crosswalk artifact design: match types, confidence, and version-tracking against O*NET quarterly releases and ESCO.

### CP — Compliance & Product/UX
1. Which **three views** does the first user need (e.g. role change view in the style of the Forester PD prototype, gap view, pathway view), and what does each require from the data model? (R-9)
2. What privacy constraints apply if role profiles or signals ever touch person-level data?

### AS — Adoption & Stewardship
1. Is the **federated core-plus-modules** governance credible? Who are candidate stewards and a long-term host? (DP-9)
2. What change process and release cadence will adopters commit to?
3. How do we avoid the Australian Skills Classification outcome (no longer maintained)? [E: CA-036]

### DE — Data Engineering & Repository Steward
1. Can the schema enforce the entity typing, controlled vocabularies and provenance rules in the audit, so that v1's vocabulary drift cannot recur?
2. Which fields are **stored** and which are **computed views**? Please propose build-time computation for the list in §4.
3. How will v1 provenance (v1 code, sheet, row, version, provenance code) be carried on every migrated record?

---

## 7. What would change my mind

- If **IO** finds that competency-level ratings reach acceptable reliability and task-level craft weights do not, I move toward Option A, with crafts kept as an ordinal at the competency level.
- If **FH and SL** find that agencies cannot use anything except competency-model artifacts in the near term, user-facing packaging dominates. The task graph stays internal.
- If **AS** finds no credible module stewards, Option C collapses into central authoring with modules as editorial sections only.
- If **IA and LM** find that the external task-level measures worth ingesting are anchored to O*NET tasks and DWAs, the task layer must be designed crosswalk-first. That strengthens Option B.
