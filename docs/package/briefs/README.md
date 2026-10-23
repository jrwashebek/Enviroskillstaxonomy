# Role-change briefs: how 13 environmental roles are changing

*EMST v2 sector-facing package (WP-14) · as of 2026-10-23 · licence CC BY 4.0 · status: draft awaiting WP-15 sign-off on date-sensitive statements*

These two-page briefs are for supervisors, training officers, HR specialists and programme leads in federal, state, local, NGO and private organizations. Each one covers a single role on the three EMST v2 pilot corridors. It describes who does the work, how the work is done today, what is changing and why, what stays human, what to learn next, how people enter the role, where it can lead, and what you can do now.

Every brief comes from EMST v2 records: the role profile and its variants, the generated Federal Series Profile and State Class View, the role-change view, the exploratory learning pathways and the verified-facts register. A brief adds no data of its own. Where a brief and the explorer differ, the explorer and the data release are authoritative.

## The briefs

| Corridor | Brief | Role | Primary work |
|---|---|---|---|
| COR-1 Field entry to monitoring and geospatial | [R01](R01-conservation-corps-member.md) | Conservation corps member | Building and treating land in supervised crews |
| COR-1 | [R02](R02-field-resource-technician.md) | Field resource technician | Collecting field data and samples to protocol |
| COR-1 | [R03](R03-monitoring-data-technician.md) | Monitoring and data technician | Running sensors and checking data quality |
| COR-1 | [R04](R04-geospatial-remote-sensing-analyst.md) | Geospatial and remote sensing analyst | Turning imagery and spatial data into decision products |
| COR-1 | [R05](R05-ground-truth-validation-steward.md) | Ground-truth and validation steward (emerging) | Judging whether remote and AI products can be trusted |
| COR-2 Fire operations to fuels and fire intelligence | [R06](R06-wildland-fire-operations.md) | Wildland fire operations (crew to supervisor) | Suppression and prescribed-fire operations |
| COR-2 | [R07](R07-fuels-prescribed-fire-specialist.md) | Fuels and prescribed fire specialist | Planning fuels treatments and prescribed burns |
| COR-2 | [R08](R08-fire-intelligence-analyst.md) | Fire intelligence analyst | Fire detection, behaviour prediction and decision support |
| COR-3 Restoration to review, permitting, compliance and programme management | [R09](R09-restoration-project-lead.md) | Restoration and land stewardship project lead | Delivering restoration projects and adapting them |
| COR-3 | [R10](R10-environmental-review-specialist.md) | Environmental review specialist | Analysing the effects of proposed actions |
| COR-3 | [R11](R11-environmental-permit-writer.md) | Environmental permit writer | Writing enforceable permits |
| COR-3 | [R12](R12-environmental-compliance-inspector.md) | Environmental compliance inspector | Inspecting against permits and rules |
| COR-3 | [R13](R13-resource-program-manager.md) | Resource programme manager | Running programmes, budgets and partnerships |

The corridors and roles are the P1 set fixed in ADR-0006 and listed in `docs/decisions/mvp_role_set.csv`.

## How to read the evidence labels

EMST v2 is early. Most of what these briefs say about tasks and change was drafted by AI agents and has not yet been tested with practitioners. The labels show how much weight each statement can carry.

| Label | What it means | What you can use it for |
|---|---|---|
| **Agent draft** (evidence label **S**) | An AI agent drafted or rated the value. The model and prompt are recorded (`raterType = llm`, `validationStatus = draft`), and no person has reviewed it. Task lists, time shares, the critical, needed-at-entry and formation flags, target levels and change claims all carry this label. | A starting point to test with your own staff. It is not a job analysis, not SME agreement and not a Delphi result. |
| **Assessment pending** | No multi-rater v2 assessment exists yet for how exposed the task is to change. Every task in every brief carries this label today. | Read the change column as a hypothesis to watch, not a measurement. |
| **Watch signal** (reliability A–D) | A dated piece of evidence, such as a headcount series, a posting count, a deployment register entry or a capability benchmark, linked to the task or role. Reliability: A = official primary data; B = credible secondary analysis of primary data; C = a single board, listing or trade press; D = unverified. | Context. Under ADR-0028, a change indicator moves only when two independent families of evidence agree, the change persists or is deployed, the match is close, the driver matches and a named person has reviewed it. **No indicator has moved for any role.** |
| **Driver** | What the evidence says is causing the change: AI, sensing technology, automation and robotics, policy reform, fiscal, workforce capacity, demographic, climate. | Separating AI from budget and policy effects. The 2025–26 contraction of public environmental staffing is tagged fiscal and policy. None of it is tagged AI. |
| **Verified fact** (IDs such as `V1-05` or claim IDs such as `WF-06`) | Checked against a primary or traceable source on 2026-10-23 (`docs/research/_verification/ALL_key_facts.csv`; `docs/methods/claims_register.csv`). Date-sensitive facts carry a re-check date. | Citing in your own documents, with the date. |
| **[J]** | Judgment by a named EMST role, with its basis stated. | Planning assumptions to calibrate. |
| **Proposed** | Not final. Example: OPM's April 24, 2026 list of series proposed for realignment. | Never describe it as done. |
| **Exploratory** | A learning pathway built from the difference between two role profiles and not yet checked against observed career moves. No pathway is labelled "recommended" until it passes the validation gate in ADR-0023 §5. | Designing development, not steering people. |
| **Held** | Withheld from release. Tribal role variants and Tribal-related content are held under ADR-0007 until a Tribal Advisory Council, constituted by Tribal governments and inter-Tribal organizations, exists and approves. The briefs say where a variant is held and nothing more. | Nothing. Held items are counted, not described. |

**Proficiency levels** (`vocab/proficiency_levels.yaml`): **L1 Supervised** (work is checked; uses approved tools under prescribed checks), **L2 Independent** (standard assignments; verifies tool outputs against independent evidence), **L3 Senior** (non-routine work; decides when not to use a tool; reviews others' AI-assisted products), **L4 Lead/Expert** (sets the technical approach; designs verified human-AI workflows; certifies others), **L5 Strategic** (defined only where SME panels confirm strategic demand). Role levels map to bands: entry L1–L2, journey L2–L3, senior L3–L4, lead L4.

**Flags in the task tables** (agent drafts, to be verified by a qualified person): **C** critical; **E** needed at entry; **F** formation task, meaning work through which people learn the judgment the role depends on. Time shares are each task's share of the whole role across all its levels.

**Change types** (`vocab/change_types.yaml`): *new* (work with no earlier analogue), *emerging* (growing but not yet established), *transforming* (established work whose tools or standards are changing materially; each brief says whether the change compresses the work or adds to it), *stable*, *declining*. Role-level change types include *entry path at risk*: the entry roles or formation tasks that feed a role are disappearing.

## What these briefs do not do

- **No v1 statistics.** Exposure values and percentages from EMST v1 were assigned by a single analyst with LLM assistance. They appear only in the explorer's evidence drawer, labelled "v1 single-analyst prior, LLM-assisted, unvalidated — not for decisions". Sector-facing documents use them only as methodology history (project lead decision Q7, 2026-10-23).
- **No external index scores.** Occupation-level AI-exposure indices (Eloundou et al.; Microsoft "Working with AI") match these roles only broadly. They are shown only in the explorer's evidence drawer and are excluded from release until their licence terms are verified (ADR-0027 amendment; ADR-0029 §9). BLS 2025–35 projections are cited as context only. They are not evidence that skills are changing.
- **No selection use.** The briefs, the views and every EMST v2 value are for describing and developing work (use tiers *describe* and *develop*). They are not a classification basis, not a job analysis and not for reduction-in-force, rating or selection decisions. Any selection use needs the employer's own job analysis (5 CFR 300.103 still requires job analysis and a rational relationship to performance [SEL-02]).
- **No credential or sign-off claims.** A variant may list a credential or sign-off authority, but the briefs do not present it as fact until a verified source is attached (SPEC §10 rule 8).
- **No recommendations about people.** Pathways are exploratory. "What you can do now" lists actions for organizations, not judgments about individuals.
- **Nonpartisan.** The briefs describe instruments and their verified status, such as rules removed, proposed or litigated. They do not argue for or against any of them (ADR-0016 §6).

## Where the content comes from

| Content | Source in the repository |
|---|---|
| Role definition, variants, task bundle, competency targets | `data/v2/core/roles/`, `data/v2/core/variants/`; fire roles in `data/v2/modules/forest/` (WP-08) |
| Federal series and state classes | `docs/build/WP-08/generated/federal-series/`, `docs/build/WP-08/generated/state-class/` (generated; WP-09 crosswalks X4, X5) |
| What is changing | `docs/build/WP-08/generated/change_view/<role>.json` (WP-08 atoms joined with WP-10 signals) |
| Pathways and formation provisions | `docs/build/WP-07/staging/pathways/`, `docs/build/WP-07/formation_provisions.csv` (exploratory; WP-07) |
| External facts | `docs/research/_verification/ALL_key_facts.csv`, `docs/methods/claims_register.csv` |
| Signal method and the evidence rule | `docs/methods/CHANGE_SIGNALS.md` |
| Scenarios and no-regret moves | `docs/research/strategic-foresight/scenarios.md` §8 |

To challenge or correct anything in a brief, use the explorer's "challenge this" route (`site/_site/challenge/`) or the contribution guide (`docs/governance/CONTRIBUTING.md`).

## Licence

Text: CC BY 4.0. Cite as: *EMST contributors, "How this role is changing: <role>", EMST v2 role-change brief, 2026-10-23 draft, CC BY 4.0.* The data the briefs draw on is CC0 1.0. Third-party material keeps its own terms (`docs/governance/LICENSING.md`).
