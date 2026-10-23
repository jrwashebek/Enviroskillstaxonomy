# EMST v2 Product Strategy

**Role:** CP (Product & UX Lead; Security, Privacy & Government Compliance Lead) · **Date:** 2026-10-23 · **Status:** proposal for CA

**Labels:**
- **[E]** cites a source I read, by ID in `sources.csv`.
- **[J]** is my judgment, with its basis stated.
- **[S]** is speculation, with what would confirm it.

**Related files:**
- `mvp_spec.md` holds the architecture, compliance constraints, screens, data model needs and the answers to CA's architecture questions.
- `user_research_plan.md` says how we learn.
- `compliance_matrix.csv` lists the 39 requirements behind the design rules.
- `report.md` summarizes the compliance findings, the architecture and the answers to CA's questions. The harness would not let this role write it directly, so I returned it to the coordinator for saving.
- The full text of the Proposals, Disagreements, Issues outside my area and Open questions is at the end of this file.

---

## 1. Vision and the job

**Vision (charter):** EMST becomes the shared language and tool the environmental sector uses to understand how its jobs are changing, and it helps people move between federal, state, local, Tribal, NGO, private and academic institutions. [E: CP-001]

**Product vision:** within two minutes of arriving, a training lead, HR specialist or early-career worker can answer three questions about a real role, with the evidence behind each answer visible:
1. What is changing in this role?
2. What should we learn next?
3. Where can this lead?

[J]

**What the product is not:**
- **A taxonomy browser.** v1's GitBook navigation began at domains and skill areas [E: CP-005]. Nobody arrives thinking "I need Skill Area 2.4". People arrive with a job title, a position description, a person, or a team. [J]
- **A hiring or screening tool.** Development and planning only (`compliance_matrix.csv` CR-19).
- **A place where people's data lives** (CR-01, CR-08).

**Why the product matters to the taxonomy.** The product is how the taxonomy gets tested against real work. Every confusion, missing task or wrong exposure judgment a user flags becomes evidence for the next release (`user_research_plan.md` §8). A taxonomy nobody uses stays unvalidated. [J]

---

## 2. Users and jobs-to-be-done

### 2.1 Status of these personas

These are **CP draft personas**. They are hypotheses built from:
- the charter's user list and the brief's "usable tomorrow" principle [E: CP-001, CP-002];
- v1's persona framework [E: CP-008];
- v1's pilot framing: permitting capacity, wildfire workforce pipelines, conservation corps to career pathways, and two to three western states [E: CP-009].

When I wrote them, CM had published transferability analyses but no personas [E: CP-010]. **CM's personas supersede these where they differ.** Neither set speaks for practitioners. The Workforce Voice panel is simulated, and these drafts must be validated in discovery research (`user_research_plan.md` Round 0). [J]

### 2.2 Persona table

| # | Persona (CP draft) | Sector actor | Core job-to-be-done ("When…, I want to…, so I can…") | v1 analogue [E: CP-008] | Phase |
|---|---|---|---|---|---|
| U1 | **Pilot program or training lead.** Runs staff development at an NGO: conservation corps, land trust, watershed council or restoration nonprofit | ngo | When a role on my team is changing (new sensing tech, new permitting rules), I want to see which tasks are shifting and what to train, so I can plan this season's development and help staff aim at state and federal jobs | Curriculum Designer; Team Architect | **Pilot: first user** |
| U2 | **Early-career worker or career mover.** Corps member, seasonal technician, veteran, mid-career pivot | ngo, state, federal, private | When I'm deciding my next move, I want to see which roles my experience leads to across organizations and what I'm missing, so I can pick training and applications that pay off | Career Navigator | Pilot (secondary) |
| U3 | **Supervisor or crew lead** | ngo, state, federal | When I do a development conversation, I want a shared, concrete list of competencies at the right level, so we agree on what "ready for the next level" means | (none) | Pilot (secondary) |
| U4 | **State training officer or curriculum lead** | state | When I redesign a training program, I want to know which competencies are growing and which tasks are being compressed, so I can retire stale modules and add new ones | Curriculum Designer; Pipeline Defender | Federal/state phase |
| U5 | **Federal or state HR specialist or classifier** | federal, state | When I rewrite a position description or build an assessment, I want competency language traceable to tasks and validated sources, so the PD is defensible and current | Team Architect (partial) | Federal/state phase |
| U6 | **Workforce planner** | federal, state | When I forecast needs, I want role-level change signals with honest uncertainty, so I can prioritize reskilling and hiring without overreacting to hype | Pipeline Defender | Federal/state phase |
| U7 | **Researcher or integrator.** Labor economist, vendor, academic program | academic, private | When I analyse or integrate, I want stable IDs, crosswalks and downloadable releases, so my work is reproducible and plugs into my systems | Infrastructure Builder | All phases (served by the data, not the UI) |
| U8 | **Accreditation or academic program lead** | academic | When I align a curriculum, I want competencies and levels I can map courses to, so graduates are ready for public-sector roles | Accreditation Aligner | Sector phase |
| U9 | **Tribal natural resource program director** | tribal | Defined by TN's protocol and by the nations themselves, not by this team | Sovereignty Practitioner | Only on TN's terms |

### 2.3 Why U1 is the first user

1. **Rollout order.** The NGO pilot comes first. [E: CP-001, CP-002]
2. **U1's job contains the federal and state job.** U1 plans development for a role and points people toward state and federal destinations. A state training officer (U4) does the same with different role variants. The views tested with U1 transfer, and they do not need to be rebuilt. [J]
3. **U1 can act without a compliance review.** An NGO lead can use a public, local-first tool tomorrow. Federal users can too, but their feedback needs PRA-aware research design (CR-12). Starting with U1 gets real usage data sooner. [J]
4. **U1 reaches U2 and U3.** The lead runs development conversations with supervisors and early-career staff, so one pilot organization exercises all three pilot personas. [J]

**Risk.** NGO pilot needs can pull the product away from federal and state needs; for example, NGOs care little about OPM series. **Mitigation:** each corridor ends in a state or a federal role variant with crosswalk codes, and FH and SL review every MVP screen before the federal and state phase. [J]

### 2.4 Jobs-to-be-done, mapped to the four core workflows

| Workflow | Primary JTBD | Personas | MVP? |
|---|---|---|---|
| (a) **"How is my job changing?"** Role-change view: task-level exposure, demand signals and emerging competencies, with uncertainty shown | Decide what to train, keep or redesign for a role | U1, U4, U6, U5, U2 | **Yes** |
| (b) **Career pathway and mobility map** across sector actors | Choose a realistic next role and the gap to close | U2, U1, U3, U4 | **Yes**, as a pathway view per role. The full map is in 1.2 |
| (c) **Skill-gap diagnosis** for an individual or team | Prioritize development and agree on readiness | U1, U3, U2, U4 | **Yes**: local-first individual check, plus a team grid from shared files |
| (d) **Builders**: position description, learning path, curriculum alignment | Produce an artifact others will use | U5, U4, U8, U1 | **Partial**: IDP export and a PD skeleton export in the MVP. The full PD builder is in 1.1 and curriculum alignment in 1.2 |

---

## 3. Product principles

1. **Enter by role, not by taxonomy.** Search accepts the titles people actually use (synonyms and alternative titles per role variant). The domain hierarchy is a facet, not a front door. [J; E on v1 navigation: CP-005]
2. **Show the change, then the evidence, then the detail.** Each page leads with a plain-language statement of what is changing, which USWDS also recommends [E: CP-027]. Evidence comes next, and full competency detail is one click down.
3. **Be honest about uncertainty.** Every judgment shows who made it, when, how, and how much raters agree. Single-rater values never become headline percentages. [J; E for the v1 problem: CP-004, CP-007]
4. **Development, not selection.** No ranking, scoring or screening of people. Outputs are drafts that humans adopt. [E for the federal basis: CP-022; J]
5. **Local-first, no accounts.** The user's data stays on the user's device or in the adopter's own systems. [J: CR-01, CR-08, CR-14]
6. **Accessible by construction.** Meet WCAG 2.2 AA. Every chart has a text statement and a table. No hover-only or drag-only interactions. [E: CP-025, CP-027]
7. **Federal-familiar, sector-neutral.** Use USWDS patterns so federal and state users trust and can rehost the site. Use sector-neutral language so NGO, Tribal, private and academic users are not shut out. [E: CP-026, CP-028; J]
8. **Generated, never hand-authored.** Every number traces to a stored, attributed record in a tagged release. The forester prototype was hand-written [E: CP-006]; v2 generates it. [E: CP-003]
9. **Small surface, deep data.** The UI shows 10–20 competencies per role, and the full model is downloadable. This is CA's "depth in modules, simplicity in the core" applied to the UI. [E: CP-003]
10. **The first user's workflow over completeness.** Ship three views that work end-to-end for 12–15 roles rather than 200 roles with thin pages. [J; charter: CP-001]

---

## 4. Positioning against existing tools

I could not re-check the current features of these tools this session, so this section is [J] from professional knowledge, labeled `unverified` in `sources.csv`. CA's audit cites O*NET's content-model safeguards, ESCO, SFIA, NICE and the Australian Skills Classification from sources CA read [E: CP-003].

| Tool | What it does well | Where it leaves environmental users short | EMST's stance |
|---|---|---|---|
| **O*NET OnLine and My Next Move** (DOL) [J: CP-061] | Authoritative national occupations; task statements; DWAs; open CC BY 4.0 data; web services | Occupation grain is coarse for environmental work (many roles fold into a few SOC codes); sector-actor differences are invisible; change signals are not task-level or dated; there are no cross-sector mobility frictions | **Crosswalk to it, don't compete.** Link EMST tasks to O*NET tasks and DWAs (IA). Show O*NET-SOC codes on destination roles so users can reach O*NET and labor-market data |
| **CareerOneStop**, including mySkills myFuture and Skills Matcher (DOL ETA) [J: CP-062] | Job-seeker tools; transferable-occupation suggestions; local training and credential finders | Same O*NET occupations; generic transfer logic; nothing organization-side for training leads | **Refer out** for local training, credential and job search. EMST supplies the domain-specific "what to learn" these tools lack |
| **Vendor skills clouds**: Workday Skills Cloud, Eightfold, SAP, Oracle [J: CP-066] | Inference at scale from employee data; integrated with HR processes | Proprietary, opaque, generic skill libraries; tied to one employer's data; procurement-heavy | **Be the content, not the platform.** Publish EMST in importable formats (IA) so agencies can load it into the systems they already authorized (Tier 2) |
| **Lightcast Open Skills** [J: CP-065] | Large generic skills library used across vendors | Generic and posting-driven; little environmental depth; no sector-actor model | Crosswalk where it helps analytics; respect licence terms |
| **ESCO** (EU) [J: CP-064] | Open, multilingual, separates knowledge, skills and transversal skills | EU occupational frame; not US public-sector structures | Typing precedent (CA); crosswalk later |
| **SkillsFuture Singapore Skills Framework** [J: CP-063] | Sector-specific skills maps with career pathways, the closest product precedent for "where can this lead" | National, government-run; a different labour-market structure | Borrow the pathway-map pattern and sector framing |
| **OPM tools and competency models** (FH lane) | Federal classification, qualification and assessment infrastructure | Built around series that OPM is consolidating through 2027 [E: CP-003]; not cross-sector | Supply competency and PD language traceable to tasks; versioned crosswalks to series |
| **v1 EMST** (GitBook, Airtable, Flourish) [E: CP-004, CP-005] | Distinctive analytical ideas (crafts, Ac, CLD); a compelling forester narrative | Analyst- and funder-oriented; claims ahead of evidence; not role-anchored; third-party platforms | Carry the ideas and the forester view; retire the platforms (`v1_assessment.csv`) |

**Positioning statement (draft):**

> For environmental training leads, HR specialists and workers in federal, state and partner organizations, EMST is the open reference that shows how specific environmental roles are changing, what to learn, and how to move between sectors. Unlike national occupation databases, it works at the grain of real environmental roles and shows its evidence. Unlike vendor skills clouds, it is open, vendor-neutral, and needs none of your people's data.

[J]

---

## 5. Roadmap

| Release | Audience | Scope | Gate to the next release |
|---|---|---|---|
| **0.x prototypes** (pilot weeks 1–8) | U1–U3 | Clickable prototypes of the three views on 3–4 roles | Round 1 task success of at least 70% on the core tasks; uncertainty comprehension of at least 70% |
| **1.0 MVP: Role Change & Development Planner** (pilot weeks 9–20) | U1–U3 at pilot NGOs | Three views; 12–15 role profiles on three corridors; IDP export; PD skeleton export; evidence pages; accessibility conformance report (ACR) | Success metrics in `mvp_spec.md` §11; ACR at WCAG 2.2 AA with no open Level A failures |
| **1.1 Federal and state** | U4–U6 | Full PD builder (human-adopts-draft pattern, CR-16); training-program view ("which modules to retire or add"); state and federal variants for all MVP roles; agency security packet; state readiness briefs | FH and SL acceptance; one state and one federal unit complete a real PD or training-plan revision |
| **1.2 Mobility** | U2, U4, CM | Full pathway map (corridor overview, frictions, observed transitions from consented or aggregate data); curriculum alignment export (LC) | CM's outcome metrics show movement or a credible intent signal |
| **2.x Sector** | U7, U8, local, private, academic; Tribal on TN's terms | Subsector modules (CA Option C); private and academic variants; Tier 2 kits | Stewardship committed (AS) |

---

## 6. Product risks

1. **Over-trust in single-analyst exposure labels.** A user may cut training because a task reads "Substitution". *Mitigation:* tier and agreement shown on every value; no aggregates; "what would change this" text; comprehension testing; hide values if users misread them. [J]
2. **The thin-content trap.** Twelve good roles beat 200 thin ones, but the pilot may ask for roles that are out of scope. *Mitigation:* a "request a role" path that feeds CA's backlog, and an honest list of the roles covered so far. [J]
3. **Self-assessment bias in the gap check.** *Mitigation:* behaviourally anchored indicators (IO), an optional supervisor rating, and framing results as conversation starters rather than verdicts. [J]
4. **Stale crosswalks.** OPM series consolidation and O*NET updates will move destination codes. *Mitigation:* show dated crosswalks, and regenerate them on each release (IA). [E: CP-003]
5. **Aesthetic rejection.** The v1 author found custom prototypes less attractive than Flourish [E: CP-009]. *Mitigation:* invest in visual design within USWDS tokens, and test appeal explicitly in Round 1. [J]
6. **Stewardship.** A tool nobody maintains loses trust fast. *Mitigation:* the static architecture keeps running costs low, but AS must name an owner. [E: CP-003]

---

## 7. v1 product assessment (summary; full verdicts in `v1_assessment.csv`)

- **Carry:**
  - the forester "Same Title, Different Job" prototype as the flagship view, generated from data [E: CP-006, CP-003];
  - v1's "pre-Delphi" disclosure habit, generalized into evidence tiers [E: CP-005];
  - the persona use contexts as seeds [E: CP-008].
- **Change:**
  - the persona set, merged with CM's and validated with users;
  - the license (resolve CC0 vs CC BY) [E: CP-005];
  - the palette: v1's red/amber/green severity scheme relies on hue [E: CP-004]; replace it with a tested palette plus text and patterns [J].
- **Retire:**
  - Airtable as the source of truth [E: CP-005, CP-009, CP-003];
  - GitBook as the public interface [E: CP-005, CP-009];
  - the Flourish story and its headline claims ("validated against OPM and O*NET"; "38% Human-Essential"; "68% in transition"; CLD counts that are now stale: 49 vs 62) [E: CP-004, CP-007, CP-003].

---

## Proposals

Numbering continues the CP series. Each proposal gives what to carry, change, retire or add, and why.

**P-CP-01 — Four-tier, compliance-minimizing architecture.**
- The tiers: Tier 0 open data core; Tier 1 static, local-first public explorer; Tier 2 run-it-yourself kits operated by adopters; Tier 3 hosted personnel-data service kept off the roadmap.
- *Why:* every heavy regime (FedRAMP, new ATO, SORN, PIA, GovRAMP) is triggered by holding agency or personal data. Accessibility, supply-chain and licensing duties remain and are cheap now. Detail is in `mvp_spec.md` §2. [E: CP-015, CP-016; J]

**P-CP-02 — Architectural invariant: the EMST steward holds no personal data.**
- Standing rules:
  - local-first computation;
  - no accounts, cookies or third-party requests;
  - no user input in URLs;
  - provenance on every judgment;
  - development use only.
- *Why:* this is cheap now and nearly impossible to restore once broken. [J: CR-01, CR-08, CR-13, CR-14]

**P-CP-03 — An "agency security packet" with every release.**
- Contents:
  - a FedRAMP and ATO applicability statement mapped to the M-24-15 exclusions;
  - a data-flow diagram;
  - an SBOM and checksums;
  - an SSDF practice mapping;
  - a voluntarily completed CISA attestation form;
  - Scorecard results.
- *Why:* M-26-05 replaced one federal attestation with agency-specific policies, so answer them all once. [E: CP-014, CP-016]

**P-CP-04 — A supply-chain baseline in CI from the first commit.** *Owner:* DE.
- What it includes:
  - OpenSSF Scorecard;
  - Actions pinned by commit SHA (OpenLMP pins by tag);
  - least-privilege tokens;
  - signed releases with provenance;
  - SBOM, Dependabot, and SECURITY.md with a disclosure policy.
- Target: Scorecard of 7 or higher by the end of the pilot. [E: CP-034, CP-011]

**P-CP-05 — Accessibility target of WCAG 2.2 AA.**
- One target meets Section 508 (WCAG 2.0 AA), ADA Title II (2.1 AA; April 26, 2027 and April 26, 2028) and HHS Section 504 (2.1 AA; May 11, 2026).
- Publish an ACR for each major release. Make exports accessible. Run CI checks plus manual assistive-technology testing. Publish an accessibility statement. [E: CP-012, CP-013, CP-025, CP-026]

**P-CP-06 — A development-use boundary and the "human adopts the draft" pattern** for every AI-assisted builder.
- Exports record that AI assisted and which release IDs were used.
- *Why:* this aligns with OPM's August 27, 2026 memo (PD drafting is generally not high-impact when officials review, revise and adopt it) and with 5 CFR 300.103. It is the durable mitigation under state AI-in-employment laws. [E: CP-022, CP-023; J: CP-043–CP-047]

**P-CP-07 — Tier 2 kits ship with compliance starters.** *Owner:* IA with CP.
- Each kit includes:
  - draft text for a privacy threshold analysis (PTA) and privacy impact assessment (PIA);
  - a data-element inventory for the SORN check;
  - aggregate defaults (minimum cell size of 5);
  - an AI system card and inputs for an impact assessment.

  [J: CR-07–CR-09, CR-15, CR-18, CR-28]

**P-CP-08 — Licensing.** *Owner:* DE and AS.
- Use CC0 for data and vocabularies, Apache-2.0 for code, and CC0 or CC BY 4.0 for documentation.
- Keep a register of third-party licences.
- Add a CARE governance flag that excludes content from open builds.
- Resolve the v1 CC0/CC BY contradiction before the first release. [E: CP-005, CP-011; J]

**P-CP-09 — Claims hygiene.** *Owner:* CP with AS.
- Every public number carries an evidence tier and its denominator: tasks or competencies.
- Retire the v1 Flourish headlines.
- Run a pre-publication checklist. [E: CP-004, CP-003, CP-007]

**P-CP-10 — Platforms.**
- Retire Airtable as the source of truth.
- Do not use GitBook or Flourish in the product.
- Allow Flourish only for one-off narratives built from a tagged release after a claims review. [E: CP-005, CP-009]

**P-CP-11 — Technology** (see `mvp_spec.md` §8).
- Build with Eleventy 3, with Astro as an equal alternative.
- Use USWDS 3 tokens and components, Pagefind search, build-time SVG charts with data tables, and small vanilla-JS islands.
- Host on GitHub Pages under a domain the steward owns, rehostable on .gov without changes. [E: CP-028, CP-035; J]

**P-CP-12 — The MVP is the Role Change & Development Planner.**
- Three views: role change, gap check, pathway.
- 12–15 role profiles defined by function × level, with sector-actor variants, on three corridors that end in state and federal roles. [J]

**P-CP-13 — An uncertainty display standard** (`mvp_spec.md` §7).
- Evidence-tier badges and an assessment-agreement count.
- Dated values and calibrated wording.
- No color-only encoding.
- No headline aggregates from single-rater data. [J: CP-071, CP-072]

**P-CP-14 — Analytics without PII.**
- No analytics script in the MVP.
- Measure usage through research sessions, release download counts and opt-in feedback.
- The site is ready for the Digital Analytics Program (DAP) if federally hosted. [E: CP-032; J]

**P-CP-15 — Research changes the taxonomy, not only the UI.**
- Findings are coded by layer.
- The same issue raised by at least 3 participants across at least 2 organizations becomes a change request to CA (`user_research_plan.md` §8). [J]

**P-CP-16 — PRA-aware, consent-based research.**
- Sponsor the research through the NGO or the coalition.
- When federal agencies co-sponsor, use direct observation and semi-structured methods.
- Limit standardized questionnaires to federal employees, or to fewer than 10 non-federal respondents unless a generic clearance applies.
- Keep raw research data out of the repo. [E: CP-029, CP-033]

**P-CP-17 — Stamp the release on every page and export.**
- Show the release ID and DOI.
- Version the client-side file formats so saved plans survive new releases. [J: CR-11, CR-39]

**P-CP-18 — A state readiness brief for each pilot state**, addressed to the CIO, CISO and ADA coordinator. SL completes the state-law table. [J: CR-24–CR-30]

**P-CP-19 — Strip PII when demand signals are ingested.** *Owner:* IA and LM.
- Remove names, position numbers and contact details.
- Store the derived signals plus source hashes. [J: CR-34]

**P-CP-20 — Defer skills inference from individuals' documents.** If it is ever built:
- it ships only as a Tier 2 kit;
- the person confirms each inferred skill;
- the evidence span is shown;
- nothing is stored by default;
- error rates are published.

  [J: CR-35]

---

## Disagreements and trade-offs

1. **With v1's platform plan: polish against control.**
   - v1's author found Flourish more attractive than custom prototypes [E: CP-009].
   - A static site built on USWDS trades some visual flash and no-code editing for reproducibility, accessibility, privacy, version control and familiarity to federal users.
   - I accept that trade and will meet the aesthetic bar through deliberate design. If pilot users reject the look, that is a finding to act on. It is not a reason to return to embedded charts. [J]
2. **With CM (anticipated): telemetry against privacy.**
   - Testing the theory of change at scale would benefit from tracking how users behave over time.
   - I propose no telemetry. Instead: consented research cohorts, opt-in follow-ups, and aggregates that agencies compute themselves.
   - The cost is slower, weaker causal evidence. The gain is entry into government environments without a privacy review. [J]
3. **With IA (anticipated): automated inference against self-rating.**
   - Inferring skills from résumés is the strongest feature for gap diagnosis.
   - I defer it (P-CP-20). Self- and supervisor rating against anchored indicators is slower and subject to bias, but it is transparent and involves no PII.
   - IO should judge whether that is good enough for development use. [J]
4. **With AS (anticipated): collaboration against data hosting.**
   - A shared team workspace would make the pilot smoother.
   - I propose sharing files through each organization's own tools: more friction, but no hosted personnel data. [J]
5. **With CA and LM: whether to show v1 exposure values.**
   - I propose showing them at task level with the tier "v1 single analyst, unvalidated", a "contested" marker where v1 flagged it (33 competencies [E: CP-007]), and a "challenge this" route. The pilot then becomes a validation channel.
   - They must never be aggregated into headline figures.
   - If comprehension testing shows users misread the tiers, the values should be hidden. [J]
6. **With FH and LC: the PD builder.**
   - The MVP ships only a PD skeleton export. The full builder comes in 1.1, for the federal and state phase.
   - The cost is that the pilot exercises less of what federal HR will use first. [J]
7. **With subject experts' appetite for depth.**
   - The UI shows only the subsets relevant to each role.
   - The full model stays one click away and downloadable. [J; CP-003 principle 6]
8. **Licensing.**
   - CC BY gives attribution and visibility, which matters for sustainability (AS). CC0 removes friction for agencies and vendors.
   - I lean toward CC0 for data and CC BY for narrative, with a strong "how to cite" convention. [J]

---

## Issues outside my area that affect the vision

- **Stewardship (AS).** Someone has to own the domain, the GitHub organization, the DOI account and the annual ACR in year five. A static architecture lowers the cost but still needs an owner. The Australian Skills Classification is a precedent. [E: CP-003]
- **Observable proficiency (IO).** The gap check is only as good as its indicators. Generic v1 statements cannot be meaningfully self-rated. [E: CP-003]
- **Tribal content (TN).** The product has a "not ours to show" flag (PC-8 in `mvp_spec.md`). TN must define the protocol behind it.
- **OPM series consolidation (FH).** Destination crosswalks will churn through September 2027, so pathway views must show crosswalk dates. EMST could become an input to OPM's skills-based framework phase. [E: CP-003]
- **Demand-signal licensing (LM, IA).** Licensed posting data cannot be published openly except as permitted aggregates. That limits how live the role-change view can be. [J]
- **Federal staff on GitHub (AS, DE).** Agencies need approved terms of service before staff can participate in an official capacity. Provide email and comment-period routes as well. [J]
- **Hosting headers (DE).** GitHub Pages cannot set CSP or HSTS headers. A host that can set them adds a third party, which is a trade-off DE should decide on. [J]
- **Unverified state AI laws (SL).** The October 2026 status of the Colorado, Illinois, California, Texas and NYC rules was not verified this session. SL should verify them before the federal and state phase. [J: CP-043–CP-047]

---

## Open questions for the Chief Taxonomy Architect

1. **Architectural invariant.** I suggest a new decision point, DP-11. Will "no personal data held by EMST" and the four-tier architecture (P-CP-01, P-CP-02) bind every role, including IA's skills-intelligence work?
2. **DP-6.** Do you accept function × level (entry, journey, lead) with sector-actor variants as the MVP role grain? Do you accept 12–15 profiles on three corridors as the role set?
3. **DP-8 display policy.** Can v1 analyst exposure values appear in the MVP with an "unvalidated" tier, or must they wait for multi-rater assessments?
4. **Licence.** Decide CC0 for data with DE and AS before the first public release.
5. **MVP scope.** Should the PD builder ship in 1.1 rather than the MVP? Or does FH's evidence say the federal phase needs it at launch?
6. **Owner of the ACR and accessibility.** Who signs and maintains the conformance report after the pilot? This is a release gate.
