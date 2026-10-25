# Project lead decisions

Answers from the project lead to `questions_for_project_lead.md`. Each answer supersedes the question's default.

| Q | Decision | Answer | Date | Recorded from |
|---|---|---|---|---|
| Q1 | Tribal Advisory Council: (a) binding consent authority over inclusion, wording and release of Tribal-related content; (b) charter carve-out so the CA / Editorial Board cannot override the TAC in that category, default "withhold"; (c) Tribal reviewer compensation budgeted before first contact | **Accepted (all three)** | 2026-10-23 | Project lead, working session |
| Q2 | CC0 1.0 dedication of the v1 text the project lead authored (competency titles, descriptions, tasks, indicators, source text), so v2 records derived from it ship in the CC0 data files | **Accepted — CC0** (narrative publications CC BY 4.0; code Apache-2.0 per ADR-0013) | 2026-10-23 | Project lead, working session |
| Q5 | Rollout: Stage 1a NGO pilot and Stage 1b federal/state design-partner track run in parallel from 2027; nothing used in selection before selection-grade evidence | **Accepted — parallel tracks** | 2026-10-23 | Project lead, working session |
| Q7 | Sector-facing publications may cite v1 statistics | **Methodology history only** until re-derived under the v2 instrument with multiple raters (observability figures only after human double-coding with α ≥ .80) | 2026-10-23 | Project lead, working session |
| — | Repository history containing private working-session details | **Rewrite history** (private details and bulk build files removed; force-pushed) | 2026-10-23 | Project lead, working session |
| — | Package call to action | **GitHub Issues** on the repository | 2026-10-23 | Project lead, working session |
| — | How the package credits the human lead | **"EMST project lead" only**; no personal name in the package | 2026-10-23 | Project lead, working session |
| Q12 | Career-ladder hypothesis publication rule (ADR-0031, CR-FIX-A-001) | **Confirmed**: published as a finding only after named human reviewers (a qualified industrial-organizational psychologist and a labor economist) validate it, in addition to AI agent reviews; then co-published with a nonpartisan partner. Until then always presented as a hypothesis with its evidence status | 2026-10-24 | Project lead, working session |
| Q13 | Sign-off before any package material goes public beyond the pilot cohort | **The project lead signs, after at least one named human subject-matter reviewer has read the report and briefs.** AI agent checks (including the adoption-lead role) are advisory only | 2026-10-24 | Project lead, working session |
| Q14 | Role profiles fitted to each pilot organization (CR-FIX-B-002) | **Not added**; the pilot offer stays as designed (design §6, MOU Article 3) | 2026-10-24 | Project lead, working session |
| Q15 | Move the repository to an organization account before external release (package re-check NH11) | **Decide later**, when a host organization is chosen; the repository stays where it is for the pilot preview | 2026-10-24 | Project lead, working session |

## Still open (defaults apply until answered)

| Q | Default in force |
|---|---|
| Q3 Host, incubation, signatory | Project lead listed as signatory for Stage 1 documents; host call drafted, not issued; EPIC incubation shown as *to be confirmed* |
| Q4 DEI/EJ in federal default views | Mechanism built; federal default views show computed applicability with an explanatory note and no exclusions |
| Q6 Restated theory of change | Used internally; external documents quote the charter sentence |
| Q8 Governance bodies at rc.1 | Project lead acts as interim Editorial Board; CA decision log continues; no module described as stewarded |
| Q9 Funding the floor and compensation | Degradation ladder applies (sentinels at the year-five floor of 30; smaller panels reported as such; no Tribal outreach) |
| Q10 Retire task sequence v7; update project instructions | Repo follows the ADRs; companion-project descriptions flagged as v1 history |
| Q11 Lead-signed invitation to inter-Tribal organizations to help form a Tribal Advisory Council (added 2026-10-23) | No invitation drafted for sending; no contact; content hold stays; WP-13 formation procedure internal only |

## Note on the CC0 dedication (Q2)

This file records the project lead's decision to dedicate the v1 text to the public domain under
[CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/). The dedication covers the v1 content in
`legacy/v1/` and `data/v1_baseline/` authored by the project lead. It does not cover third-party material: the SAF
Accreditation Handbook is excluded and never redistributed, and upstream O*NET/ESCO text stays out of CC0 files per
ADR-0013. The project lead may add a signed statement to this file to make the dedication explicit for downstream
counsel.
