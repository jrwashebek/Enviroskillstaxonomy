# EMST v2 sector-facing package

*WP-14 · Phase 4 Sprint S3 · as of 2026-10-23 · for federal, state, local, NGO and private workforce leaders, HR and training staff, and educators*

> **Status.** WP-15's first pass (2026-10-23, `docs/methods/WP15_SIGNOFF.md`) cleared the package for **internal drafts and the NGO-pilot preview only**. External publication waits until AS co-signs and the moving facts (series realignment, SPEED Act and S. 5653, Section 106, Part 108, Colorado SB 26-189, OFCCP, WOTUS) are re-checked before the rc.1 build. Every external claim cites a verified source with a register ID (`docs/methods/claims_register.csv`). Every EMST value about tasks, time shares, flags, targets or change is an **agent draft** (evidence label S) and is labelled as one.

The package explains how environmental jobs are changing and how EMST v2 can help organizations hire on merit and skills, stay mission-ready and keep knowledge. It is built from verified external evidence and EMST v2 records. It uses no EMST v1 statistics except as methodology history (project lead decision Q7). It holds back Tribal content (ADR-0007), and it takes no position on any policy (ADR-0016 §6).

## Contents

| Item | Path | What it is | Licence |
|---|---|---|---|
| **Flagship report:** "How environmental jobs are changing" | `report/` (figure datasets in `report/figures/`, index `figures_index.csv`) | The long-form evidence report. It draws on verified external evidence (public capacity, AI deployment and availability, plan requirements, projections, entry-path signals, the policy timeline) and on EMST v2's structural findings and pre-registered pilot plans. Every figure is tier-labelled with its denominator. The career-ladder finding is presented as a hypothesis with its mechanism and evidence status. Being written in parallel by a separate WP-14 writer; the deck and briefs reuse its figure datasets F01–F10. | CC BY 4.0 (ADR-0027 §5) |
| **Role-change briefs** (13) | `briefs/` (index and evidence labels in `briefs/README.md`) | Two-page "How this role is changing" briefs for the 13 priority roles on the three pilot corridors. Each covers who does the work (sector actors, titles, federal series with proposed realignments shown as proposed, state class examples); the work today (agent draft); what is changing, with drivers and evidence status ("assessment pending" throughout); what stays human; competencies to build next and at what level; entry paths and formation; exploratory pathways in and out; actions for a supervisor, a training officer and an HR specialist; and sources. | CC BY 4.0 |
| **Briefing deck content** (18 slides) | `deck/deck_content.md` | Headlines, body points or chart references, and speaker notes with sources for a mandate-framed briefing (merit and skills-based hiring, mission readiness, knowledge retention). The arc runs: why now → what the evidence says → how roles are changing → what stays human and the entry-path hypothesis → four futures and no-regret moves → what EMST v2 is → how to use it (federal HR, states, NGOs, educators) → the pilot and design-partner offer → limits → the ask. | CC BY 4.0 |
| **Interactive explorer** (companion) | `site/` (built pages in `site/_site/`) | A static, local-first site. It shows, for the 13 priority roles: View 1 "How is this role changing?"; View 2 "Where are the gaps?", where ratings stay in a file on the user's device; View 3 "Where can this role lead?" (exploratory); View 4 "What's coming". It also hosts Federal Series Profile and State Class View pages, an evidence drawer showing v1 values only as labelled prior evidence, and a "challenge this" route. It stores no personal data server-side and targets WCAG 2.2 AA, with a security packet (`site/security/`). | Source code Apache-2.0; displayed data CC0 1.0; page prose CC BY 4.0 |
| **Forester position description, FES format** | `forester_pd_fes_draft.md` | GS-0460 Forester PD regenerated from EMST v2 records at the journey level (indicative GS-9 to GS-11). Major duties carry indicative percentages of time, and Factor 1–9 narratives are drafted with factor levels and points left blank for the servicing classifier. It is labelled **"DRAFT — SUBJECT TO CLASSIFICATION REVIEW"** with the disclaimer "not a classification basis / not a job analysis / not for RIF or rating decisions". It reuses no v1 duty percentages or exposure calls. | CC0 1.0 as a generated view of CC0 data (`docs/governance/LICENSING.md` §1) [J; CA to confirm] |
| **HR and adoption kits** | `docs/adoption/` | **Stage 1b design-partner packages** (`stage1b_design_partner_packages.md`): the 0400 Kit for 0401 and 0404 first (Federal Series Profiles, competency models, PD language library, task-level crosswalks from series proposed for realignment); a Job-Analysis Starter Pack for one Tier 2 natural-resources series; a federal-to-state crosswalk to be validated with Pennsylvania; and a fire crosswalk. **Stage 1a NGO pilot design** (`stage1a_ngo_pilot_design.md`) and **pilot MOU template** (`pilot_mou_template.md`). **Gate G1/G2 metric definitions** (`gate_metrics_G1_G2.md`, `.csv`). **Commitment register** rules (`COMMITMENT_REGISTER.md`), the only source of any "committed" status. **Ecosystem Atlas** (`ECOSYSTEM_ATLAS.md`, `ecosystem_atlas.csv`), which lists connections EMST could make, not commitments. | Outlines and designs CC BY 4.0; templates, register schema, atlas data and package data files CC0 1.0 (`docs/governance/LICENSING.md` §2) |

**Not in the package.** `docs/adoption/theory_of_change_one_pager.md` is an internal working document. Until the project lead decides Q6, external materials quote only the charter sentence: "If those blends are visible and portable, mobility follows." The underlying records, generated HR views and crosswalks live in `data/v2/` and `docs/build/WP-08/generated/` and ship in the release bundle under CC0 1.0.

## Rules every package item follows

1. **Agent drafts are never presented as findings.** Task bundles, time shares, critical, needed-at-entry and formation flags, target levels, change claims and driver tags carry evidence label S. No change indicator has moved for any role, because the ADR-0028 evidence rule needs two independent signal families, persistence, a close match, a matching driver and named human review.
2. **"Assessment pending"** is shown wherever no multi-rater v2 assessment exists, which today means every task.
3. **Pathways are exploratory.** None is "recommended" until it passes the validation gate in ADR-0023 §5.
4. **Corrected facts only.** Use the register's safe wording and avoid its `do_not_say` forms. Examples: series are "proposed for realignment", never "realigned". The SPEED Act and S. 5653 are separate pending bills. The January 2027 fire standards align USWFS and USFS federal qualifications. AEI's "77%" is never job automation. Selection validity is never "UGESP compliance".
5. **Not published:** claims with register status `unverified` or `held`, Tribal-held content, third-party exposure-index values, and posting-volume or "baseline" claims, because no October 2026 posting snapshot exists (WP-15 §2).
6. **No personal data.** Examples are synthetic, and aggregates carry n ≥ 5.
7. **No organization is described as committed** without a dated entry in the commitment register.

## Licences at a glance

- **CC BY 4.0:** report, briefs, deck, explorer prose, adoption narrative documents. Cite as: *EMST contributors, <title>, EMST v2 sector-facing package, 2026-10-23 draft, CC BY 4.0.*
- **CC0 1.0:** EMST data and generated views, including the role profiles, Federal Series Profiles, State Class Views and the Forester PD, plus templates and registers.
- **Apache-2.0:** code, including the explorer source and build scripts.
- **Third-party material:** its own terms (`docs/governance/LICENSING.md` §5). O*NET and ESCO text stays out of CC0 files, and licensed posting data appears only as permitted aggregates.

## Feedback

Errors, challenges and corrections go through the explorer's "challenge this" route or `docs/governance/CONTRIBUTING.md`.
