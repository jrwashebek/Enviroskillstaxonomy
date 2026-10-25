# EMST v2 sector-facing package

*As of 23 October 2026 · for federal, state, local, NGO and private workforce leaders, HR and training staff, and
educators*

> **Status: draft for NGO-pilot preview (2026-10-23).** AI agents checked facts against sources, and some claims await
> register rows. Not yet reviewed by independent human experts. Date-sensitive statements (for example the series
> realignment proposal, the SPEED Act and S. 5653, Section 106, Part 108, Colorado SB 26-189, OFCCP and WOTUS) will be
> re-checked before external release.
>
> **Who wrote it.** This package was researched and drafted by a team of AI agents (Anthropic's Claude), each given a
> specialist role, working to a charter set by the EMST project lead. AI agents checked the facts against sources in
> October 2026. No independent human expert has reviewed the package yet. Role names such as "Chief Taxonomy
> Architect" are AI agent roles, not people.

The package explains how environmental jobs are changing and how EMST v2 could help organizations hire on merit and
skills, stay mission-ready and keep knowledge. It is built from outside evidence that AI agents checked against sources
and from EMST v2 records, which are themselves agent drafts. It uses no EMST v1 statistics except as methodology
history, under the project lead's decision. It holds back Tribal content until a Tribal Advisory Council approves. It
takes no position on the merits of any law, rule, executive action or budget; it recommends workforce-management
practices that EMST's foresight analysis judged to hold under every scenario it considered.

## Contents

| Item | Path | What it is | License |
|---|---|---|---|
| **Flagship report:** "How environmental jobs are changing" (draft 0.9.1) | `report/` (figure datasets in `report/figures/`, index `figures_index.csv`) | The long-form evidence report. It draws on checked outside evidence (federal capacity, AI deployment and availability, plan contents, projections, entry-path signals, the policy timeline) and on EMST v2's structure and planned pilot. Every figure is labeled with its evidence type and denominator. The career-ladder idea is presented as a hypothesis with its mechanism and the evidence status of each link. | CC BY 4.0 |
| **Role-change briefs** (13) | `briefs/` (index, evidence labels and glossary in `briefs/README.md`) | Short "How this role is changing" briefs for the 13 corridor roles. Each covers who does the work (employer types, titles, federal series with proposed realignments shown as proposed, state class examples); the work today (agent draft, with no time shares or flags); what is expected to change, with drivers and outside signals (every task change "assessment pending"); what stays with people; competencies to build next, with draft targets labeled as design statements; entry paths and formation; exploratory pathways; actions for supervisors, training officers, HR specialists and educators (and NGO program leads where relevant); and sources. The explorer also holds earlier, lower-depth drafts of 18 more roles and six emerging roles, which have no briefs. Air, water, wastewater, drinking-water, waste and environmental-health roles are not yet covered by any brief. | CC BY 4.0 |
| **Briefing deck content** (18 slides) | `deck/deck_content.md` | Headlines, body points or chart references, and speaker notes for a briefing framed by three mandates (merit and skills-based hiring, mission readiness, knowledge retention). Citations use the report's reference numbers. The arc runs: why now → what the evidence says → how roles are expected to change → what stays with people and the entry-path hypothesis → four futures and no-regret moves (agent drafts) → what EMST v2 is → how to use it → the planned pilot and design-partner track → limits → the ask. | CC BY 4.0 |
| **Interactive explorer** (companion) | `site/` (built pages in `site/_site/`) | A static, local-first site with four views of each role ("How is this role changing?", "Where are the gaps?" with ratings kept in a file on the user's device, "Where can this role lead?" (exploratory) and "What's coming"), plus Federal Series Profile and State Class View pages, an evidence drawer that shows v1 values only as labeled prior evidence, and a route for challenges. It holds the 13 corridor roles in full and 18 more roles at lower depth. It stores no personal data on a server and targets WCAG 2.2 AA. | Source code Apache-2.0; displayed data CC0 1.0; page prose CC BY 4.0 |
| **Forester position description, FES format** | `forester_pd_fes_draft.md` | A GS-0460 Forester PD regenerated from EMST v2 records, written at the full-performance end of the indicative journey band with a separate developmental statement. Each duty's percentage of time is left blank for the supervisor; no criticality or needed-at-entry flags are shown; factor levels, points and grade are left to the servicing classifier; standard header fields are blanks for the HR office. It is labeled **"DRAFT — SUBJECT TO CLASSIFICATION REVIEW"** with the disclaimer "not a classification basis / not a job analysis / not for RIF or rating decisions", and it reuses no v1 duty percentages or exposure calls. The Forester is not one of the 13 corridor roles; it is shown because EMST v1 included a Forester PD prototype, which this version replaces. | CC0 1.0 as a generated view of CC0 data (pending confirmation) |
| **HR and adoption kits** | `docs/adoption/` | **Design-partner packages** (`stage1b_design_partner_packages.md`), planned with potential partners, none committed: the 0400 Kit for 0401 and 0404 first (Federal Series Profiles, competency models, PD language library, task-level crosswalks from series proposed for realignment); a Job-Analysis Starter Pack for one Tier 2 natural-resources series; a federal-to-state crosswalk EMST proposes to test with a state partner; and a fire crosswalk. **NGO pilot design** (`stage1a_ngo_pilot_design.md`) and **pilot agreement template** (`pilot_mou_template.md`). **Expansion-gate metric definitions** (`gate_metrics_G1_G2.md`, `.csv`). **Commitment register** rules (`COMMITMENT_REGISTER.md`), the only source of any "committed" status; the register is empty. **Ecosystem Atlas** (`ECOSYSTEM_ATLAS.md`, `ecosystem_atlas.csv`), which lists connections EMST could make, not commitments. | Outlines and designs CC BY 4.0; templates, register schema, atlas data and package data files CC0 1.0 |

**Not in the package.** `docs/adoption/theory_of_change_one_pager.md` is an internal working document. Until the project
lead decides on its release, external materials quote only the charter sentence: "If those blends are visible and
portable, mobility follows." The underlying records and crosswalks live in `data/v2/`. The release bundle (EMST
2.0.0-rc.1, CC0 1.0; release notes and counts in `docs/release/2.0.0-rc.1/`) ships the records that passed the release
gate, their crosswalk mappings and the gated release views, including the Federal Series Profiles and State Class Views,
which apply EMST's display rule. The files under `docs/build/WP-08/generated/` are authoring previews of those HR views; they
are not the bundle and do not ship in it.

## Rules every package item follows

1. **Agent drafts are never presented as findings.** Task lists, formation flags, draft target levels, expected changes,
   driver tags, scenarios and no-regret moves were drafted by AI agents and are labeled as such, with hypothesis or
   judgment verbs. No change indicator has moved for any role: EMST's evidence rule needs two independent families of
   evidence, persistence, a close match, a matching driver and review by a named person.
2. **Some values are never shown.** Under EMST's display rule, sector-facing text gives no agent-drafted time shares,
   no importance ratings, no "critical", "needed at entry" or "distinguishing" flags, no target levels presented as
   findings, no AI-drafted craft ratings and no value on which human raters did not reach the agreement threshold. Work
   may be described in words, including which crafts it draws on.
3. **"Assessment pending"** is shown wherever no assessment by several independent human raters exists, which today
   means every task.
4. **Pathways are exploratory.** None is called "recommended" until it predicts real career moves clearly better than
   simple guesses.
5. **Corrected facts only.** Use the claims register's safe wording and avoid its "do not say" forms. Examples: series
   are "proposed for realignment", never "realigned". The SPEED Act and S. 5653 are separate pending bills. The January
   2027 fire standards align U.S. Wildland Fire Service and Forest Service federal qualifications. AEI's "77%" is never
   job automation. Selection validity is never "UGESP compliance". The self-assessment questionnaire rule always comes
   with its exceptions (seasonal positions, GS-4 and below, other OPM-authorized cases). The AmeriCorps settlement
   covers FY2026 in the coalition's jurisdictions only. Pennsylvania's equivalency is a list of federal titles that may
   count for certain Commonwealth titles, not a general rule. Budgets are not named as the cause of the 2025–26 federal
   contraction. Plan data are "components typed as monitoring" in western national-forest documents, not "monitoring
   requirements" or "durable demand".
6. **Federal, not public.** Where the evidence is federal, the text says "federal". Entry-job and field-craft claims
   are scoped to federal land agencies, and plan claims to western national forests.
7. **Not published:** claims with register status unverified or held, Tribal-held content, third-party exposure-index
   values, and posting-volume or "baseline" claims, because no October 2026 posting snapshot exists.
8. **No personal data.** Examples are synthetic, and aggregates have at least five people per cell.
9. **No implied participants.** No organization, jurisdiction or program is described as participating, partnering,
   piloting or committed. They appear only as examples, as context or as potential partners. The commitment register is
   empty.

## Licenses at a glance

- **CC BY 4.0:** report, briefs, deck, explorer prose, adoption narrative documents. Cite as: *EMST contributors,
  <title>, EMST v2 sector-facing package, 2026-10-23 draft, CC BY 4.0.*
- **CC0 1.0:** EMST data and generated views, including the role profiles, Federal Series Profiles, State Class Views
  and the Forester PD, plus templates and registers.
- **Apache-2.0:** code, including the explorer source and build scripts.
- **Third-party material:** its own terms (`docs/governance/LICENSING.md`). O*NET and ESCO text stays out of CC0 files,
  and licensed posting data appears only as permitted aggregates.

## Comment or correct

To comment, correct an error or ask about the pilot, open an issue at
[github.com/jrwashebek/Enviroskillstaxonomy/issues](https://github.com/jrwashebek/Enviroskillstaxonomy/issues).
