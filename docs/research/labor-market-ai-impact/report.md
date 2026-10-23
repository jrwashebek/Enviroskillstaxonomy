# Labor Market & AI-Impact Research — EMST v2, Phase 2

**Role:** LM, Labor Market & AI-Impact Research Lead · **Date:** 2026-10-23 · **Folder:** `docs/research/labor-market-ai-impact/`

Labels: **[E]** evidence I read (source IDs in `sources.csv`); **[J]** my professional judgment, with its basis stated; **[S]** speculation, with what would confirm or refute it. "Via XX-nnn" means another role read that source and I did not re-read it (status `unverified` in my `sources.csv`).

---

## 0. Summary

**What the evidence shows**

1. **Environmental work has two exposure profiles, not one.** On the most widely used task-level measure (Eloundou et al.), the analytical, regulatory and planning occupations rank among the most exposed in the whole economy: Environmental Scientists and Specialists at the 98th percentile, Climate Change Policy Analysts 99th, Sustainability Specialists 97th, Urban and Regional Planners 90th, Hydrologists 85th, Compliance Officers 81st. The field and operations occupations rank among the least exposed: Hazardous Materials Removal Workers 10th, Forest and Conservation Workers 17th, Firefighters 22nd, Water/Wastewater Operators 28th, Fish and Game Wardens 33rd. [E: LM-008; my computation, `env_occupation_exposure_scores.csv`] The common framing that environmental work is "protected by its field character" holds only for the field half.
2. **The indices agree on the ranking but not on what it means.** Across 773 occupations, six scores from three index families correlate at Spearman ρ = 0.70–0.91 between distinct measures (0.98 between the two AIOE variants). Within the 24 core environmental occupations the range is 0.73–0.98. [E: LM-008, LM-009, LM-010; `index_agreement_spearman.csv`] They share an O*NET base, so they agree on ordering. They answer different questions, though: *could* AI do this, *is* AI used for it, did employment change, and what do employers expect.
3. **Environmental work is under-represented in usage data relative to its capability exposure.** The usage-based Microsoft score ranks 20 of 24 environmental occupations below their theoretical (Eloundou) percentile. The gap is about 40 or more percentile points for Foresters, Forest and Conservation Technicians, Natural Sciences Managers and Fire Prevention Specialists. [E: LM-009, LM-008] In the AEI task file, environmental tasks do appear, but each accounts for only 0.002–0.02% of conversations. [E: LM-007, partial view] Part of the gap is sampling: consumer and developer platforms see little government work. Part is likely real adoption lag. The data cannot yet separate the two. [J]
4. **Federal environmental agencies show two waves of AI.** Enterprise generative-AI tools for drafting, summarizing and search are licensed close to agency-wide: EPA reports 10,000–50,000 users for drafting and summarization, and DOI and USDA report 50,000+ for some tools. Custom AI is mostly classical machine learning for science and monitoring, and only 61 of 347 stage-reported use cases are deployed. Of 504 use cases in environmental bureaus, five concern NEPA or permitting, and none of those is deployed. [E: LM-027, my counts]
5. **The dominant 2025–26 labor-market shock to the public environmental workforce is fiscal and policy-driven, not AI.** Colleagues' sources report large losses: USFS 16% to more than 25% depending on the base used, NPS more than 25%, park rangers −34%, NRCS −24%, and EPA staffing at 40-year lows. They also report a halt to non-fire seasonal hiring in 2025, an under-30 share of 7.9%, and growth only in wildland fire, alongside the new U.S. Wildland Fire Service. [E via FH/FS/FC/AS: LM-028–LM-037] These numbers swamp any AI signal in federal headcount data for 2025–26. [J]
6. **There is no environment-specific causal evidence of AI employment effects.** The best outcome evidence comes from private payroll data. In the most-exposed occupations, workers aged 22–25 are about 19% below the counterfactual by June 2026, through reduced hiring, concentrated where usage automates rather than augments. That evidence is descriptive, and ADP under-covers government. [E: LM-005, LM-006] For environmental roles, the entry-level effect is a plausible hypothesis, not a finding. [S]
7. **Land management plans reveal where demand is growing.** Compared with 1982-rule plans, 2012-rule plans devote 12 times the share of components to monitoring (22% vs 1.8%). Per 1,000 components they mention at-risk species about 40 times as often, climate about 10 times, ecological integrity about 8 times, partnerships 5 times and Tribal interests 3 times. Grazing language falls. [E: LM-017; `lmp_outputs/`] Plans state *what* to monitor far more than *how*: remote sensing is named in 3 of 1,506 monitoring questions, eDNA in 3 and LiDAR in none. Technology change will therefore show up in protocols, position descriptions and postings, not in plan text. [E/J]
8. **The v1 exposure instrument is right in concept and needs re-construction.** External calibration is feasible. In an analyst-curated pilot of 60 v1 tasks matched to O*NET:
   - 30% of v1 tasks have no O*NET analogue. These are candidate *new work*.
   - The direction of v1 labels broadly agrees with external labels. 11 of 13 matched Ac tasks are rated exposed, and 7 of 10 matched H tasks are rated unexposed.
   - v1 "A" mixes LLM-augmented desk work with tool-assisted physical work.
   - The four S calls are rated exposed but are not corroborated by evidence of deployment.
   - External task labels are themselves unstable. Where two O*NET tasks were plausible matches, their human labels differed in 13 of 21 cases. [E: `v1_onet_pilot_curated_summary.txt`]

**What I propose (top five)**

- P-LM-01: separate exposure into three constructs: technical exposure by vector, deployment mode, and staffing outcome.
- P-LM-02: build a human-curated, versioned EMST-task → O*NET-task crosswalk before any calibration.
- P-LM-04: accept S, V and Horizon-1 claims only when there is evidence of deployment.
- P-LM-06: recast career-ladder destruction (CLD) as a computed, pathway-level indicator that records its driver.
- P-LM-07: set a two-family evidence rule for change signals. Full list in §8.

---

## 1. Scope, method, limits

**Questions.** I addressed the five assigned research questions plus the Chief Architect's (CA's) four LM questions (§7).

**Method.**
- Seven web searches before the team-wide search budget ran out, then 13 WebFetch reads of URLs those searches had surfaced (one further fetch was blocked).
- Cloning of four GitHub repositories holding primary data:
  - OpenAI GPTs-are-GPTs labels (LM-008)
  - Microsoft Working-with-AI v1.1 (LM-009)
  - Felten–Raj–Seamans AIOE (LM-010)
  - the OMB 2025 Federal AI Use Case Inventory (LM-027)
- A full quantitative pass on the local OpenLMP corpus (LM-017).
- A 60-task calibration pilot against the v1 baseline (LM-020).
- Every analysis is a script in `scripts/` and reproduces deterministically from the cloned data (§12).

**Limits, stated plainly.**
- The Hugging Face egress was blocked, so I could not download the AEI dataset. I read the release list (LM-001) and a truncated view of one task file (LM-007). The pilot uses Eloundou and Microsoft task labels; the AEI join is fully designed (§5.4) but not executed.
- The primary page of Anthropic's March 2026 "observed exposure" study (LM-026) could not be fetched because the permission request timed out. I rely on two secondary accounts (LM-004, LM-012) and one critique (LM-013).
- After the search budget ran out I could not retrieve current releases of WEF, LinkedIn, Lightcast, BLS 2024–34, OECD, Stanford AI Index, Indeed, PwC, McKinsey, ILO, Yale Budget Lab, Humlum–Vestergaard, USEER, IEA, IRENA or E2. I appraise their *methods* from professional knowledge [J] and list them as `unverified`. I quote no statistics from them except where a colleague's source carries the figure.
- The BLS projections I read are the 2022–32 vintage (LM-011), superseded by 2024–34.
- Federal workforce figures come from FH, FS, FC and AS sources I did not re-read. They conflict in places (USFS −16% vs >25%), which is itself a finding about how signal bases must be defined (§6).

---

## 2. Research question 1: appraisal of the AI-exposure and labor-impact evidence

Full rows are in `index_appraisal.csv` (34 entries). The evidence falls into five families. Each answers a different question and fails in a different way.

### 2.1 Capability or "theoretical" exposure: could AI do this task?

**Eloundou et al. ("GPTs are GPTs", Science 2024).** Human annotators and GPT-4 rated 19,265 O*NET task statements:
- E0: no exposure.
- E1: an LLM alone can cut task time by at least half at equal quality.
- E2: exposure only with complementary software.

A separate GPT-4 rubric rates automation from T0 to T4. [E: LM-008; rubric wording J, from the paper LM-048 which I did not re-read]

*Strengths.* It is task-level, uses a transparent rubric, publishes open labels, and joins natively to O*NET. E1 is an operational definition of "task-time compression", which is exactly the mechanism v1 calls Ac (§5).

*Weaknesses.*
- It measures feasibility, not adoption.
- The ratings date from 2023, before agentic tools.
- The raters were not occupational subject-matter experts.
- The scale covers only LLM-cognitive exposure, so it is blind to robotics and to sensing, which is the vector that matters most for field environmental work.
- Labels are unstable at the level of a single task. In my pilot, where a v1 task had two plausible O*NET matches, the human labels disagreed in 13 of 21 cases; for example, "mediate community disputes" (planners) is rated E2 while "mediate agreements among rangeland users" (range managers) is rated E0. [E: pilot]

*Use.* Ingest as an attributed "theoretical LLM exposure" assessment through the crosswalk, aggregated over several matches with the spread reported, never as a single-match label.

**Felten–Raj–Seamans AIOE / LM-AIOE.** This links AI application categories to O*NET abilities and aggregates to occupations. [E: LM-010, LM-046]
- It is ability-level, so it cannot see variation between tasks inside an occupation, and it does not distinguish augmentation from automation.
- It uses SOC 2010 codes for several environmental technicians and OHS occupations (19-4091, 19-4093, 29-9011). A naive SOC 2018 join silently drops them; I had to add a vintage map. [E]
- Use: context only.

**Webb (patent–task overlap), ILO generative-AI index, McKinsey MGI, MIT/ORNL Iceberg.** These are context-grade. Webb's robot measure is a useful comparator for the robotics vector. The ILO index is the bridge for ISCO/ESCO adopters. MGI's "technical automation potential" is often misread as job loss. [J; LM-049, LM-050, LM-061, LM-067 unverified]

### 2.2 Usage: is AI actually used for this task?

**Anthropic Economic Index (AEI).** [E: LM-001, LM-003; release statistics via LM-004]

*Releases:*
- 2025-02-10: initial, with O*NET task mappings and the automation/augmentation split.
- 2025-03-27: Claude 3.7 Sonnet data and clusters.
- 2025-09-15: geography and first-party API.
- 2026-01-15: "economic primitives" (complexity, human and AI skill in education-years, autonomy, success).
- 2026-03-24: learning curves.
- 2026-06-26: "Cadences", with monthly aggregates, an artifact classifier, Cowork data and linked survey responses.
- Undated folders `labor_market_impacts` (occupation exposure; task penetration for about 18,000 tasks per LM-015) and `robot_exposure`.

*Method.* A classifier running on Claude (Clio) maps sampled conversations to O*NET tasks and to collaboration modes. Directive and feedback-loop modes count as automation; task iteration, learning and validation count as augmentation.

*Strengths.* It is the only open, repeated, task-level measure of actual use with an automation/augmentation split.

*Weaknesses I weigh most:*
1. *Sampling frame.* It covers consumer and developer users of one vendor, and government tenants are not sampled. For public-sector environmental work, absence means "not observed here", not "not used".
2. *Shifting definitions and denominators.* The reported augmentation share moves between 57% (launch), 52% (November 2025) and a third-party re-aggregation of 78.7% (LM-015), depending on what is filtered. Cross-release comparisons must hold the definition fixed.
3. *Classifier validity.* The task classifier's accuracy against a published human gold set was not visible in what I read. I may have missed it.
4. *Conflict of interest.* A vendor measures use of its own product (LM-013). EMST is also being built with Claude, which deepens this (§10).

*Use.* Ingest task penetration and mode shares as dated, attributed assessments, with sub-threshold counts treated as "insufficient evidence".

**AEI "observed exposure" (March 2026).** This weights theoretical feasibility by observed, work-related, automation-leaning use. Secondary accounts report no unemployment effect in the highest-exposure occupations, a tentative slowdown for 22–25-year-olds, and 30% of workers with zero observed exposure. [E via LM-012, LM-004; primary LM-026 not read] Critics note its reliance on BLS projections, a short window and Claude-only usage. [E: LM-013] Its concept, *observed* rather than *possible*, is the right direction for EMST. Its usage base under-represents agencies.

**Microsoft "Working with AI" (v1.1, NeurIPS 2026).** About 200,000 Bing Copilot conversations are mapped to 332 O*NET intermediate work activities (IWAs), separately as the user's goal and as the AI's action, with completion and scope. It gives an applicability score per SOC code and, in v1.1, a physical flag for each O*NET task. [E: LM-009, LM-047] It is valuable because it separates *assisting* from *performing*, and the physical flag is the only open task-level physical classification. Its weaknesses are a single platform, IWA-level coarseness, and the authors' own caution that applicability is not impact.

### 2.3 Early outcome studies: did employment change?

**Brynjolfsson, Chandar and Chen, "Canaries" (ADP payroll; August 2026 update).** [E: LM-005, LM-006]
- Workers aged 22–25 in the two most-exposed quintiles are about 19% below the counterfactual (June 2026), up from 15% at the July 2025 data vintage.
- The adjustment comes through hiring, not separations, with little change in pay.
- It is concentrated where usage *automates*; where usage complements, employment is flat or rising, especially for experienced workers.
- The gap survives exclusion of tech firms and controls for interest rates and remote work.
- With firm-time fixed effects, the relative decline appears in 2024, not 2022.
- The authors call it descriptive. Gaps shrink with education controls. ADP estimates exceed national-survey benchmarks, and the discrepancy is concentrated in education, health and **public administration**.

This is the strongest evidence for v1's CLD intuition, and it says nothing direct about public agencies. [J]

**Yale Budget Lab; Humlum and Vestergaard; BLS Employment Projections with AI case studies.** [J; LM-051–LM-053 unverified]
- Yale finds no broad shift in occupational mix through 2025.
- Humlum and Vestergaard find widespread chatbot adoption, small time savings and no detectable effects on earnings or hours in Denmark. That is the key benchmark against reading v1's Ac as headcount loss.
- BLS adds judgment-based AI adjustments for a few occupations.

None isolates environmental occupations, which are too small for reliable CPS cells. [J]

### 2.4 Posting and expectation measures: what employers seek or expect

- **WEF Future of Jobs 2025** is an employer-expectation survey of large firms and context only. (Summary seen via FS: LM-041; primary unverified.)
- **LinkedIn green-skills research.** The latest figure available to the team is the 2024 green-talent gap (LM-042, outdated). Its platform bias against field, seasonal, Tribal and many public workers is severe for EMST.
- **Lightcast** is granular and timely but proprietary; its Open Skills taxonomy is a crosswalk target.
- **Indeed Hiring Lab** and **Burning Glass Institute** are posting- and career-path-based, and the latter is a potential partner for entry-path signals (via AS: LM-043).
- **PwC AI Jobs Barometer** is correlational vendor work built on AIOE.

[J; unverified releases]

### 2.5 Verdict

| Question the measure answers | Best current measure | Fit for environmental work | Use in EMST |
|---|---|---|---|
| Could AI do the task? | Eloundou E-labels (task) | Good coverage; blind to robotics and sensing | Ingest, attributed, aggregated |
| Is AI used for it? | AEI task penetration and modes; Microsoft IWA metrics | Under-samples government and field work | Ingest, attributed, with "insufficient evidence" rule |
| Is it deployed in the employer? | OMB AI inventory; enterprise tool licences | Direct for federal; nothing comparable for most states | Ingest as deployment stage |
| Did employment change? | Canaries-type admin-data designs | No environmental cut; government outside ADP | Benchmark; replicate on OPM FWD |
| What will employers seek? | Postings (Lightcast, USAJOBS), WEF | Postings usable; WEF context only | Ingest posting content; WEF watch |

[J, resting on §2.1–2.4]

---

## 3. Research question 2: environment-specific evidence

### 3.1 Which environmental occupations appear in the indices, and what they show

All 33 occupations in `env_occupations_in_scope.csv` are covered by Eloundou (O*NET-SOC level) and Microsoft (SOC level). AIOE covers them once the SOC 2010 codes are mapped. [E] Three patterns follow.

1. **Bimodality** (§0.1). [E] Within the analytical cluster, only 4% of Environmental Scientists' O*NET tasks are rated E0, against 90% for Forest and Conservation Workers. The physical-task share runs from 10% (Environmental Scientists) to 82% (Forest and Conservation Workers) and 86% (HazMat). [E: LM-008, LM-009]
2. **The usage gap is widest where field context and analysis mix.**

   | Occupation | Eloundou percentile | Microsoft usage percentile |
   |---|---|---|
   | Foresters | 59th | 20th |
   | Forest and Conservation Technicians | 53rd | 6th |
   | Forest Fire Inspectors and Prevention Specialists | 61st | 12th |
   | Natural Sciences Managers | 77th | 38th |

   [E] Planners (90th / 94th) and Atmospheric Scientists (93rd / 92nd) show no gap. [E] My reading: the gap is largest for roles whose analytical tasks are embedded in agency systems (timber sale, inventory, fire prevention) that consumer chatbots do not see. [J]
3. **AEI presence.** Rows for 19-2041 (.00, .01, .03), 19-1031, 19-1013, 19-2042, 19-2043, 19-2021, 19-5011, 11-9121.02 and 13-1199.05 appear in the February 2025 task file, at 0.002–0.02% of conversations each. Industrial Ecologists' systems-analysis task is the largest at 0.02%. [E: LM-007, `aei_env_rows_seen.csv`] I saw no forestry, wildlife, fire or field-technician rows in the partial view, which covered tasks alphabetically only up to "co…". **Their absence is not evidence of zero use.** [J]

### 3.2 Green-jobs measures

I could not retrieve current releases of O*NET Green Economy, DOE USEER, IEA, IRENA or E2 (all `unverified`). Methodologically, they measure **energy** employment, not natural-resource or environmental-protection work. The O*NET green designations (2009 onward) are aging labels, not demand measures. [J] For EMST they serve as context for an energy module (DB lane). On the question "are environmental jobs growing or declining", they are largely silent outside energy. **This is a measurement gap, not a finding of stability.** [J] In the private sector, colleagues report that sustainability functions in large firms grew more often than they shrank in 2026 (46% vs 25%), with compliance rising as a priority (via PS: LM-040). [E via PS]

### 3.3 The public environmental workforce, 2025–2026

I did not re-read these sources. Colleagues (FH, FS, FC, AS) assembled them, and I cite them because they are the decisive context for any AI attribution.

- **Contraction.** The executive-branch civilian workforce fell 12% (September 2024 → January 2026). USFS and NPS each lost more than 25%. Park rangers fell 34.1%, student-trainee occupations fell, and the under-30 share is 7.9%. Only wildland fire management grew (via FH: LM-028). An alternative estimate puts USFS at −16% in 2025, from USDA OIG data (via FH: LM-029). NRCS fell 23.8% (via FS: LM-030), and EPA staffing reached 40-year lows; departing staff have a median tenure of about 30 years against about 11 for those remaining (via FS: LM-031). About 317,000 federal departures occurred in 2025 (via FH: LM-032).
- **Entry paths.** There was no non-fire seasonal hiring in 2025, with 2,000 seasonals committed for 2026, and trail miles maintained fell 22% (via FC: LM-033, LM-034).
- **Reorganization.** The U.S. Wildland Fire Service was established in January 2026, with about 5,780 federal and about 900 Tribal personnel (via AS: LM-035). USFS is moving its headquarters to Salt Lake City and closing regional offices and most research stations (via AS: LM-036). States are taking on a larger role through Good Neighbor Authority (via AS: LM-037).
- **Hiring regime.** Under EO 14356, strategic hiring committees approve each vacancy and agencies file annual staffing plans (via FH: LM-038). States have recruited former federal staff (via SL: LM-039).

**Implications.**
- (a) Federal headcount data for 2025–26 cannot be used to detect AI effects in environmental occupations. The policy shock dominates. [J]
- (b) The two USFS estimates (16% vs >25%) differ because of base definitions: all staff vs permanent, fire vs non-fire, and on-board count vs net change. Every headcount signal in EMST must declare its base. [J]
- (c) The entry rung that v1's CLD analysis worries about is being removed by hiring policy *now*, while generative AI is simultaneously becoming available agency-wide (§4.3). When hiring resumes under staffing plans, managers may not refill entry tasks that AI now compresses, so a policy shock could turn into a permanent ladder change. [S] *Confirm or refute:* compare GS-5/7 accessions in 0400-series environmental occupations in 2027–28 with 2023–24, conditioning on budget.

### 3.4 Known vs assumed

| Claim | Status |
|---|---|
| Analytical environmental occupations are among the most LLM-exposed in the economy | **Known** [E] |
| Field environmental occupations have low LLM exposure | **Known** [E]; robotics and sensing exposure **unmeasured** |
| Environmental workers use AI less than their exposure implies | **Partly known** [E for consumer/Copilot usage]; true workplace use **unknown** |
| AI has reduced environmental employment | **No evidence either way** [E: absence]; the public-sector shock is policy-driven |
| Entry-level environmental hiring is falling because of AI | **Assumed** [S]; private analogue evidence only |
| Ac tasks will compress headcount | **Assumed** [S]; Danish evidence shows time savings without headcount effects |
| Sensing (drones, acoustic, eDNA, imagery) is displacing field survey labor | **Assumed** [J]; no index measures it; plan text silent |

---

## 4. Research question 3: demand signals

### 4.1 Land management plans: quantitative pass

**Data and method.** I read the data dictionary and vocabularies first. [E: LM-018]
- 217 plan files, 154 of them non-empty; 58,544 components.
- 95.3% are USDA Forest Service (55,807 components); 2,737 are state forest/trust agencies.
- All are in western states.
- By framework: 1982 rule 40,906; 2012 rule 13,733; state 2,529; other 1,376.

Script: `scripts/lmp_demand_signals.py`; outputs: `lmp_outputs/`. [E: LM-017]

*Measurement choices.*
1. Counts are of **extracted components**. Segmentation differs by extraction method (section, table, code) and by era, so I report shares within era and per 1,000 components.
2. Theme tags cover about 10% of components, so themes are keyword-inferred and flagged as such.
3. Acronyms are matched case-sensitively. An earlier run let "IMPROVE" match "improve" and "Spectrum" match "Recreation Opportunity Spectrum"; both were corrected.
4. I introduced the **monitoring question** as the atomic unit (1,506 questions across 45 plans and 37 units) because raw "monitoring" components include report-table fragments. A single 2022 monitoring evaluation report (Idaho Panhandle) supplies 29% of all monitoring components.

**Findings.**

*(a) The 2012 Planning Rule created a monitoring workload.* Monitoring is 22.2% of components in 2012-rule plans against 1.8% in 1982-rule plans. The median 2012-rule plan has 34 monitoring components; the median 1982-rule plan has none. [E] Monitoring questions concentrate on:

| Theme | Share of monitoring questions |
|---|---|
| Vegetation | 17% |
| Recreation | 17% |
| Fire and fuels | 14% |
| Aquatics | 13% |
| Water | 12% |
| Wildlife | 12% |
| Timber | 10% |

Themes overlap, so shares sum to more than 100%. [E]

*(b) Plans name outcomes and reporting, not field methods.* The most-named method family in monitoring questions is reporting and data systems (16%). Then come aquatic sampling (5.4%), visitor-use and social monitoring (5.0%), partner or citizen involvement (5.0%), adaptive-management triggers (3.5%), invasive inventory (3.3%), BMP implementation (3.0%) and inventory plots (2.9%). Remote sensing appears in 3 questions, eDNA in 3 and LiDAR in none. [E] **Implication:** plans create durable demand for indicator design, evaluation and reporting. How field data are gathered, which is where sensing and AI arrive, is specified in protocols and technical guides that the corpus does not hold. [J]

*(c) Coordination intensity tripled.* Per 1,000 components, comparing 2012-rule with 1982-rule plans:

| Touchpoint | 1982 rule | 2012 rule |
|---|---|---|
| Partnership | 10.0 | 31.4 |
| Tribal | 10.0 | 27.3 |
| Cross-boundary | 4.5 | 13.8 |
| State agency | 4.6 | 10.1 |
| Grazing authorization | 2.2 | 5.2 |
| Consistency requirement | 1.1 | 3.4 |
| ESA consultation | 1.0 | 2.3 |

Good Neighbor and shared-stewardship language appears in only 21 components in total. These instruments operate through agreements, not plans, so **plans are a poor signal for them**. [E/J]

*(d) The direction of plan content has changed.* Mention rates per 1,000 components, 1982 rule → 2012 rule:

| Term | 1982 rule | 2012 rule | Change |
|---|---|---|---|
| At-risk species / species of conservation concern | 0.3 | 11.7 | ×40 |
| Ecosystem services | 0.1 | 2.3 | ×15 |
| Carbon | 0.3 | 4.1 | ×14 |
| Climate change | 1.8 | 16.9 | ×9.6 |
| Ecological integrity / resilience | 4.4 | 37.3 | ×8.4 |
| Remote sensing / LiDAR / drones | 0.4 | 2.6 | ×6.3 |
| Partnership / collaboration | 7.7 | 39.2 | ×5.1 |
| Data / models | 15.0 | 70.0 | ×4.7 |
| Tribal | 8.5 | 26.2 | ×3.1 |
| Monitoring | 39.6 | 112.9 | ×2.9 |
| Grazing | 46.1 | 34.4 | ×0.75 |
| Adaptive management | 5.6 | 3.1 | ×0.54 |

[E] The adaptive-management decline is probably inflated in the 1982-rule era by Northwest Forest Plan "Adaptive Management Area" designations. [J]

*(e) Data and model dependencies are mostly agency classifications and corporate systems.* Number of plans referring to each (field or text):

| Dependency | Plans |
|---|---|
| Scenery classes (SIO/VQO) | 68 |
| Recreation Opportunity Spectrum | 62 |
| Hydrologic models / water yield | 53 |
| Natural range of variation | 37 |
| FS corporate systems (NRIS, FACTS, INFRA, TIM) | 28 |
| Fire regime / FRCC | 26 |
| National Visitor Use Monitoring (NVUM) | 24 |
| SIMPPLLE / Spectrum | 19 |
| Forest Inventory and Analysis (FIA) | 18 |
| CWA 303(d) | 18 |
| Watershed Condition Framework | 17 |
| LANDFIRE | 14 |
| LiDAR | 5 |
| FSim | 3 |
| FVS | 1 |

[E] FVS is ubiquitous in practice but nearly absent from plan components. Analysis models live in the planning record and the EIS, not in plan direction. [J] **The tools layer (L4) cannot be populated from plan components; it needs EIS and planning records, PDs and postings.** [J]

*(f) What plans require of standards.* Recreation (15% of standards and guidelines), roads and access (13%), wildlife (11%), timber (9%), grazing (7%), riparian (7%) and fire (7%) dominate binding direction. [E] Recreation, travel management, grazing and minerals authorizations are large, durable workloads that **v1 barely represents** (v1 has 5.5.1 visitor services and 5.5.2 generic permit administration). This underlies candidates C-LM-02 to C-LM-04. [E/J]

**Implied workforce competencies** (codes are v1; full mapping in `lmp_outputs/*.csv`):
- monitoring program design and evaluation (3.1.5, 3.2.5, new C-LM-01)
- resource data stewardship and interpretation of agency reference datasets (2.2.1, 2.2.3, 1.3.2, new C-LM-04)
- coordination and Tribal engagement (5.2.5, 6.5.1–6.5.4)
- recreation and authorization administration (new C-LM-02, C-LM-03)

[J]

**Representativeness.** These are USFS western-forest signals. DB's separate subsector pass on the same corpus (`domain-bench/lmp_subsector_demand_signal.csv`) confirms how thin water, air and other subsectors are. Extending the method to BLM resource management plans, state wildlife action plans, TMDLs and NPDES permits, and state forest plans is the obvious next step (P-LM-08). [J]

### 4.2 Position descriptions and job postings

- **USAJOBS.** I could not reach the USAJOBS APIs this session. Since 2025, federal posting *volume* reflects the hiring freeze, EO 14356 staffing-plan approvals and the Merit Hiring Plan more than labor demand (via FH: LM-038). Volume is therefore a **policy signal**; the duties and qualification text is the **content signal**. [J] The right design is a baseline snapshot of announcements for the core series (0401, 0408, 0454, 0455, 0460, 0462, 0486, 0819, 0028, 1301, 0456) with duties text versioned, then differenced quarterly by IA's extraction pipeline. [J]
- **Position descriptions.** The v1 "forester PD transformation" page is an illustrative composite, not a real PD with an identifier. It cannot serve as evidence that PDs are being rewritten. [E: inspection of legacy file] I found no evidence of systematic PD rewrites for AI in environmental series. **The evidence is thin; this is a gap, not a negative finding.**
- **State postings.** SL found current examples: a Caltrans Environmental Scientist posting (CEQA/NEPA document preparation) and Michigan EGLE environmental quality analyst postings. These are the right raw material for posting-content signals. [E via SL]

### 4.3 Deployment evidence: the OMB AI inventory as a demand-side signal

Own counts from the 2025 inventory (LM-027; `omb_ai_inventory_env_*.csv`):
- **504 use cases** in environmental bureaus: USGS 187, NOAA 157, USDA Natural Resources and Environment (which includes USFS) 76, EPA 29, USDA Farm Production and Conservation (which includes NRCS) 20, FWS 11, BOR 8, BLM 7, NPS 2.
- 232 are classical ML, 34 computer vision and 32 generative AI.
- Of the 347 with a reported stage (NOAA did not report stages), 61 are deployed (18%). The rest are pilot or pre-deployment.
- Function clusters:

| Function | Use cases | Deployed |
|---|---|---|
| Species and wildlife detection | 89 | 11 |
| Remote sensing / imagery | 63 | 11 |
| Generative-AI drafting / summarization / chat | 41 | 4 |
| Hydrology / water | 36 | 10 |
| Forecasting | 33 | 2 |
| Fire | 31 | 8 |
| NEPA / environmental review / permitting | 5 | 0 |
| Public comment | 3 | 1 |

- The consolidated commercial off-the-shelf (COTS) file shows drafting, summarizing and search tools at near-workforce scale: EPA M365 Copilot / Azure OpenAI at 10,000–50,000 users for drafting, summarizing, writing quality, code and knowledge retrieval; DOI writing tools at 50,000+; USDA Copilot Chat at 50,000+.

[E]

**Reading.** Generic documentation compression (v1's Ac zone) is available at the level of tool access across the main federal environmental agencies now. Specialized substitution in environmental review (v1's S zone) is not deployed. Science-pipeline ML (v1's DC zone) is mostly piloting. [E/J]

---

## 5. Research question 4: appraisal of the v1 exposure instrument

### 5.1 What v1 did and what the data show

v1 classified **666 tasks** (the synthesis reports 645) on five dimensions. [E: LM-019, LM-021, LM-022] The database distribution is:

| Dimension | Values |
|---|---|
| Automation type | A 389, H 146, Ac 101, V 26, S 4 |
| Tacit density | Hi 277, Med 275, Lo 114 |
| Career ladder | C 467, P 184, X 15 |
| Vector | AI 516, none 143, Cv 6, Ro 1 |
| Horizon | 1: 394, N: 143, 2: 129, 3: never used |

The synthesis reports 9 S calls and 136 H calls; the database holds 4 S (after the Pre-15A reclassification) and 146 H. [E]

**Collinearity.**
- No Hi-tacit task is Ac, S or V. All 101 Ac tasks are Horizon 1. All H tasks but three are Horizon N.
- The dimensions are not independent judgments; one was inferred from another. [E; agrees with CA audit LM-025]

**The "FC/DC structural pattern" is contradicted by the database.** The synthesis claims H calls arise only from FC- or SC-primary competencies, with one anomaly. The database holds **9 H tasks on DC-primary competencies**. Standing rule R1 also instructed coders to expect the pattern. [E: LM-019, LM-022] Retire it as a finding.

**Vocabulary drift.** CLD values appear as both True and Yes. Severity values include "Highest" and "Ungraded", which the data dictionary does not define. [E]

### 5.2 Validity of each construct against the literature

- **A / Ac / H / S / V.** This conflates three constructs that the literature measures separately:
  1. *technical exposure*: Eloundou E-levels, Webb, robot indices;
  2. *deployment mode*: who executes, matching AEI's directive vs collaborative modes and Microsoft's AI-action vs user-goal;
  3. *labor outcome*: canaries, Humlum–Vestergaard.

  The A/V "current deployment" rule is good coding practice. The single code still forces a coder to answer all three at once. [J]
- **Ac.** CA asked whether Ac is novel. Its measurable core, "time investment substantially reduced, human reviews and certifies", is close to Eloundou's E1 criterion (time cut by at least half at equal quality) and to the "labor-saving augmentation" idea in task-based economics. [E: LM-048, LM-074; J] v1's original step is the inference "headcount compression plausible" for public agencies. That inference is not supported as a task property. Whether time savings reduce headcount depends on demand elasticity, budget rules and statutory workload. Bessen's work on demand elasticity and the Danish null on earnings and hours show that time savings can coexist with stable employment. [J; LM-073, LM-051 unverified] In agencies, freed time can also become backlog reduction, for example under NEPA timelines, rather than cuts. **Keep Ac as a task-level time-compression rating. Move staffing to a role- or organization-level outcome.**
- **H.** This mixes a descriptive claim (no current technical pathway) with a normative one (must remain human for accountability). External labels rate some v1 H tasks as exposed: three of ten matched H tasks are E2, including mediation and stakeholder engagement for land use. [E: pilot] Keep both, as separate fields.
- **Tacit density.** The literature treats tacit or experience requirements as a moderator, and it can be partly measured (O*NET job zone, related experience, work-context descriptors) or panel-rated. In the pilot, Lo-tacit tasks are exposed in 17 of 19 cases and Hi-tacit tasks in 5 of 11. That is predictive but far from deterministic, unlike the near-deterministic pattern in v1. [E]
- **Career-ladder position.** This should be derived from which role levels hold the task in role profiles (grade band, job zone), not asserted per task. [J; agrees with CA]
- **Vector.** AI / Ro / Cv misses **sensing**: the replacement of in-person observation by imagery, acoustic arrays, camera traps, eDNA and sensor networks. For environmental fieldcraft this is the main technology vector, and no general index measures it. [J] The federal inventory confirms its weight: species-detection and remote-sensing cases are the largest environmental clusters. [E: LM-027] Anthropic's September 2026 robot task index is the first candidate external calibrator for Ro. It is unread (LM-070).
- **Horizon.** Replace it with dated assessments plus observed deployment stage. [J]
- **CLD.** The concept is the most policy-relevant part of v1, and the strongest outcome study supports its *private-sector* mechanism. [E: LM-005] Two changes:
  1. *Driver attribution.* The 2025–26 public-sector ladder damage is fiscal and policy-driven (§3.3).
  2. *A second mechanism.* "Top-of-ladder loss" occurs when senior reviewers leave (EPA median departing tenure ≈ 30 years) and the review-and-certify function that keeps Ac from becoming S loses its people. [E via FS; J]

  Compute CLD at the pathway level, as CA proposes.
- **Stability tier.** Retire it as a stored field and compute it from signals. [J]

### 5.3 Pilot: v1 labels against external task labels

**Design** (`scripts/v1_onet_calibration_pilot.py`, `pilot_candidates.py`, `pilot_curated_compare.py`).
- A stratified sample of 60 v1 tasks (seed 20261023): all 4 S, 8 V, 16 Ac, 16 A and 16 H, spread across domains.
- Automated lexical matching (TF-IDF) to all 19,265 O*NET 27.x tasks produced mostly wrong pairs. I judged about a quarter semantically right; for example, "mediate land-use disputes" matched gambling supervisors. That alone shows **naive automated crosswalking fails**. [E]
- I then generated the top 7 candidates per task from environment-related O*NET-SOC codes (2,902 tasks) and curated matches by judgment. Each was recorded as equivalent, close, partial or none, with notes and alternatives (`v1_onet_pilot_curation.csv`). Curation is a single-analyst [J] act and needs a second coder.

**Results** (`v1_onet_pilot_curated_summary.txt`). [E for counts; J for interpretation]

1. **Crosswalk shape.** 5 equivalent, 17 close, 20 partial and **18 none (30%)**. "None" clusters in tasks about:
   - AI-specific work (AR/VR export, AI design tools, AI adoption governance)
   - Indigenous data sovereignty and Tribal consultation
   - ecological transformation and range of variability
   - carbon and biodiversity markets
   - acoustic sensor deployment
   - logic models

   These are exactly the places where O*NET lags new environmental work. The EMST crosswalk will be many-to-many and mostly partial.
2. **Ac.** 11 of 13 matched Ac tasks are rated exposed (E1 4, E2 7), and 10 of 13 sit at T2–T4 on the GPT-4 automation rubric. This is directional agreement.
3. **H.** 7 of 10 matched H tasks are E0, and 9 of 10 sit at T0–T1. Three H tasks are E2 (mediation, land-use stakeholder engagement, cross-functional field scheduling). The capability exists, but authority stays human.
4. **S.** All 4 are rated exposed (2 E1, 2 E2), but none at T4 (full automation): one T1, two T2, one T3. Combined with zero deployed NEPA or permitting AI in the federal inventory, **S is not corroborated**. Downgrade to Ac with an S-watch until deployment evidence exists.
5. **A.** Of 9 matched A tasks, 3 are E0 and 6 are physical (Microsoft flag): soil sampling, seed-drill operation, interpretive displays. v1 "A" includes tool-assisted physical work that LLM-exposure measures read as unexposed. The construct needs splitting by vector.
6. **Tacit.** Lo-tacit tasks are exposed in 17 of 19 cases, Hi-tacit in 5 of 11. **Career ladder:** P tasks are more often E0 (9 of 22) than C tasks (4 of 20), because entry work is physical. The ladder risk sits in *desk* entry tasks.
7. **External labels are noisy.** Where a second O*NET task was a plausible match, human labels differed in 13 of 21 cases. **Never attach a single-match label; aggregate and show spread.**

### 5.4 Calibration design for Phase 3 (full scope)

1. **Crosswalk all 666 v1 tasks and all v2 tasks** to O*NET tasks.
   - Generate candidates with embeddings plus TF-IDF, restricted to the role family's O*NET-SOC pool.
   - Two independent coders record match type and a confidence for each pair; adjudicate.
   - Target weighted κ ≥ 0.6 on match type.
   - Pin the O*NET version and keep a mapping to each new release (O*NET is on 30.x–31.0 per AS: LM-045).
   - Store as an L6 crosswalk artifact.
2. **Attach external assessments** to each matched O*NET task, each with its release ID:
   - Eloundou human and GPT-4 labels and the T-rubric;
   - AEI task penetration, directive, feedback-loop, iteration, learning and validation shares, and success, per release;
   - Microsoft IWA metrics, via the O*NET task → DWA → IWA files;
   - the Microsoft physical flag;
   - the robot task index, after review.
3. **Aggregate per EMST task.** Use means weighted by match type and similarity, report dispersion, and give a "no external analogue" flag where nothing matches.
4. **Agreement analysis** against v1 analyst labels, using pre-registered ordinal mappings:
   - H < A < Ac < V/S against E-beta, the T-rubric and AEI directive share;
   - report Spearman and weighted κ.
   - Disagreements go to the Delphi, not to automatic overwrite.
5. **Deployment context.** Add sector-actor deployment stage: the OMB inventory for federal, state AI inventories where they exist, and the enterprise tool availability bands.
6. **Decision rules.** A task is labelled "automation-leaning" only if at least two independent families agree: theoretical (E1 or T3+) **and** observed (AEI directive share above the economy median for matched tasks **or** registered deployment). Otherwise it is "augmentation-leaning" or "insufficient evidence".
7. **Re-run each release** and store each run as a new dated assessment, never overwriting.

[J; the design rests on §5.3]

---

## 6. Research question 5: the v2 change-signal layer (L5)

### 6.1 What is measured, from where, how often

| Measure | Native unit | Source | Cadence | Notes |
|---|---|---|---|---|
| Theoretical exposure (LLM) | O*NET task | Eloundou labels (LM-008) | Static; new runs if re-rated | Aggregate across matches |
| Task usage share and collaboration modes | O*NET task | AEI releases (LM-001) | Per release (now monthly aggregates) | Insufficient-evidence rule |
| Applicability (assist vs perform) | IWA → SOC | Microsoft (LM-009) | Per release | Context on tasks |
| Robotics exposure | Task | AEI robot_exposure (LM-070); Webb | Per release | Review before ingest |
| Sensing/field-technology adoption | Task × agency | Agency programme reports (e.g. USFS UAS, FC-002), protocols, AI inventory | Annual | No index exists; EMST must build it |
| Deployment stage | Function × agency | OMB AI inventory (LM-027); state inventories | Annual | Gate for S/V claims |
| Enterprise tool availability | Agency | OMB COTS file | Annual | Availability ≠ use |
| Posting volume | Title or series × geography | USAJOBS (LM-076); state boards; Lightcast | Weekly ingest, quarterly summary | Federal volume = policy signal |
| Posting/PD content (skills, tools, duties) | Posting → task / L4 tool | IA extraction pipeline | Quarterly | Main "new work" detector |
| Plan requirements | Plan component → task | OpenLMP (LM-017) | On plan revision | Monitoring questions as unit |
| Headcount, accessions, separations, under-30, trainee series | Series × agency × grade | OPM FWD (LM-044) | Monthly data, quarterly summary | Declare base (perm/seasonal; fire/non-fire) |
| Employment and wages | SOC × area | BLS OEWS | Annual | Benchmark |
| Projections | SOC | BLS EP (LM-053) | Annual (September) | Baseline |
| Worker-reported time savings and preferences | Task × role | NGO pilot cohort survey; WORKBank-style HAS (LM-069) | Per pilot wave | Direct Ac evidence |

[J]

### 6.2 How augment / automate / new is labelled, with uncertainty

- **Automate-leaning.** Observed directive or system-executes use *and* theoretical exposure *and* registered deployment. Staffing consequences are a separate, role-level outcome signal: fewer postings or accessions for the task-bearing role while workload is stable.
- **Augment-leaning.** Observed use dominated by collaborative modes, or tool requirements added to postings without a volume decline, or worker-reported time savings with the role intact.
- **New.** Tasks with no O*NET analogue (30% in the pilot) that appear with rising frequency in postings, PDs or plans. Examples: AI-output validation, MRV for carbon and biodiversity credits, Indigenous data governance, plan monitoring evaluation. Also new titles, following the Autor et al. method of detecting new work through new title entries. [J; LM-075 unverified]
- **Uncertainty.** Each label carries:
  - (i) the number of independent signal families agreeing;
  - (ii) the weakest crosswalk match type on the path;
  - (iii) sample adequacy, for example AEI counts above threshold;
  - (iv) a driver tag: AI, sensing, automation/robotics, policy reform, fiscal, demographic, market.

  The display shows the components and a computed summary, so no single label hides the disagreement. [J]

### 6.3 How signals attach

Signals attach at their **native unit** and roll up through crosswalk weights by computation, never by storing an inherited value:
- usage and exposure → tasks;
- posting content → tasks and L4 tools;
- headcount → series and role profiles;
- BLS → occupation;
- plan requirements → tasks.

[J; agrees with CA's "computed, not stored"] A proposed record:

`change_signal(signal_id, target_type, target_id, measure, value, unit, baseline_value, period_start, period_end, geography, sector_actor, source_id, source_release, method_version, crosswalk_path, crosswalk_min_match_type, direction{augment|automate|new|grow|decline|stable}, direction_confidence{low|med|high}, driver[], evidence_label, status{watch|active|retired}, reviewer, review_date)`

---

## 7. Answers to CA architecture questions (§6 of `architecture_hypotheses.md`)

**Q1. Which task-level exposure or usage measures are sound enough to ingest as attributed assessments on EMST tasks, and which only as context? (DP-8)**

- **Ingest as attributed assessments, keyed to O*NET task and release:**
  - Eloundou human and GPT-4 E-labels and T-rubric. Sound: task-level, transparent, open. Noisy at the single-task level, so ingest the aggregate. [E: LM-008; pilot]
  - AEI task penetration and collaboration-mode shares. Sound for observed use, with sampling caveats; ingest with an "insufficient evidence" rule. [E: LM-001; J]
  - Microsoft IWA metrics and the task physical flag. [E: LM-009]
  - OMB deployment stage, as a sector-actor-specific attribute on *functions*, not tasks. [E: LM-027]
- **Context only:**
  - AIOE, LM-AIOE, Webb, ILO: occupation- or ability-level.
  - MGI, Iceberg, PwC, WEF: opaque or expectation-based.
  - BLS projections: occupation baseline.

  [J]
- **Benchmarks, not assessments:** canaries, Yale and Humlum–Vestergaard outcome studies. [J]
- **Label v1 values** as `rater_type = expert-analyst (v1, single rater, LLM-assisted)` assessments, coexisting with the others. [J; agrees with CA audit §10.3]

**Q2. Is there external evidence that corroborates or refutes v1's Ac and CLD patterns in environmental work?**

- **Ac: partial corroboration at the capability and availability level; no corroboration at the staffing level.**
  - Matched Ac tasks are externally rated exposed (11 of 13) and mostly T2+ (10 of 13). [E: pilot]
  - Generative-AI drafting and summarization tools are licensed near agency-wide at EPA, DOI and USDA. [E: LM-027]
  - No source shows environmental headcount falling because of task compression. Federal headcount changes in 2025–26 have a policy explanation. The Danish evidence warns that time savings need not cut headcount. [E via others; J]
- **CLD: the mechanism is corroborated in private payroll data; the public-sector pattern is not attributable to AI.**
  - Young workers in automation-leaning, high-exposure occupations lost ground through reduced hiring. [E: LM-005]
  - In federal environmental agencies the entry rung *is* collapsing (seasonal halt, under-30 share 7.9%, trainee series down), but through hiring policy. [E via FH/FC]
  - Senior attrition adds a top-of-ladder mechanism v1 lacks. [E via FS]
  - I found no evidence of PD rewrites or posting shifts that remove entry-level environmental tasks *because of AI*. **The evidence is thin.**
  - *Would settle it:* GS-5/7 accession rates in 0400-series occupations after hiring normalizes; posting-content diffs for entry series; NGO-pilot time-use data. [S]

**Q3. What minimum evidence standard should a change-signal record meet before it moves a role's change indicator?** [J]

1. **Two independent signal families** pointing the same way. Families are: capability, observed use, deployment, postings or PDs, headcount, plan requirements, and worker report. Two indices built on the same data family count as one.
2. **Persistence:** at least two consecutive periods, or one period plus a registered deployment.
3. **A traceable crosswalk path** with minimum match type "close". Partial matches can only raise a "watch".
4. **A declared base and driver tag.** Fiscal and policy shocks are tagged so they do not masquerade as AI effects.
5. **Human review** by a named reviewer.

A signal meeting fewer of these conditions sets status = watch and is shown but does not move the indicator.

**Q4. Does environment-specific evidence support distinguishing augmented / automated / new work at the task level, or only at the occupation level?**

- **Today, only at the occupation level for *outcomes*, and at the task level for *exposure and observed use*.**
  - Every outcome study is occupation- or quintile-level, and none has an environmental cut. [E]
  - Task-level exposure exists for every environmental O*NET task (Eloundou, Microsoft). Task-level observed use exists but is sparse for environmental tasks (AEI). [E]
  - Deployment evidence exists at the level of function × agency. [E]
- **"New work" can only be detected at the task level**, through tasks with no O*NET analogue and rising mentions in postings, PDs and plans. Occupation data are blind to it by construction. [J; pilot 30% none]
- **So:** label tasks with *exposure and use direction*. Label roles and occupations with *outcomes*. Keep the two separate in the data model, which supports the CA's task spine (Option B internal) with role-level outcome signals. [J]

---

## 8. Proposals

- **P-LM-01. Split exposure into three constructs.** (Change.)
  - (a) Technical exposure by vector: LLM-cognitive, robotics, **sensing**.
  - (b) Deployment mode by sector actor: human executes, human supervises, system executes.
  - (c) Staffing outcome at role or organization level.

  Each is a dated, attributed assessment. Why: v1's single code conflates them (§5.2), and the pilot shows the conflation (§5.3 items 5 and 6).
- **P-LM-02. Build the EMST-task → O*NET-task crosswalk as a curated L6 artifact before any calibration.** (Add.) Two coders, match types, a pinned O*NET version and κ reporting. Priors from the pilot: 30% none, mostly partial. Automated lexical matching alone is unacceptable.
- **P-LM-03. Ingest list for DP-8.** (Add.) Ingest Eloundou, AEI and Microsoft at task level, and OMB deployment stage at function level. Use AIOE, Webb, ILO, WEF, PwC, MGI and Iceberg as context only, and the outcome studies as benchmarks (§7 Q1).
- **P-LM-04. Gate S, V and "deployed now" claims on deployment evidence.** (Change.) Downgrade v1's 4 S calls to Ac with an S-watch until a registered deployment and observed directive use exist.
- **P-LM-05. Create a sensing and field-technology tracker.** (Add.) No index measures how sensors, imagery, eDNA and acoustic arrays replace field observation. Build it from agency programme reports, protocols and the AI inventory's species and remote-sensing clusters. Co-own with FC and DC.
- **P-LM-06. Recast CLD as a computed, pathway-level indicator with driver attribution** and a top-of-ladder-loss mechanism. (Change.) Monitor with OPM FWD (accessions, under-30 share, trainee series), and replicate the canaries design on federal environmental series once hiring normalizes.
- **P-LM-07. Adopt the change-signal record and the two-family evidence rule** (§6.3, §7 Q3). (Add.)
- **P-LM-08. Make plan requirements a standing demand signal.** (Add.)
  - Use monitoring questions and standards by theme and method as units.
  - Report rule-era trend analyses.
  - Extend to BLM RMPs, state wildlife action plans, TMDLs and NPDES permits, and state forest plans.
  - Add EIS and planning records for tool (L4) dependencies.
  - Script: `scripts/lmp_demand_signals.py`.
- **P-LM-09. Posting and PD content signals.** (Add.) Take a USAJOBS and state-board baseline snapshot (October 2026) for the core series, diff duties text quarterly through IA's pipeline, and treat federal posting volume as a policy signal.
- **P-LM-10. Rebuild the labor-market crosswalk** at O*NET-SOC 8-digit level plus OPM series and state classes, many-to-many, attached to role profiles. (Change.) Fix the verified errors:
  - 19-1012 is Food Scientists and Technologists;
  - 33-1021 is mistitled as Fire Inspectors (it is First-Line Supervisors of Firefighting and Prevention Workers);
  - 29-9021 and 25-4031 are poor fits.

  Use the O*NET-SOC details that exist for "no SOC" families (13-1199.05, 11-1011.03, 19-2041.01–.03, 15-1299.02, 19-2099.01). [E: LM-011, LM-008]
- **P-LM-11. Add candidate competencies C-LM-01 to C-LM-06** (`candidate_competencies.csv`):
  - plan monitoring programs;
  - recreation and visitor use;
  - resource-use authorizations;
  - stewardship of authoritative data and models;
  - knowledge continuity through attrition;
  - evidence-based workforce planning (borderline).
- **P-LM-12. Commission environment-specific evidence.** (Add.)
  - (a) An environmental task evaluation suite in the style of GDPval and DraftNEPABench, with DC.
  - (b) A request to Anthropic and Microsoft research teams for environmental-occupation cuts, plus a possible Economic Futures grant (ECO-LM-04).
  - (c) A time-use and AI-use survey in the NGO pilot cohort; this is the only route to direct Ac evidence.
  - (d) A worker-preference module modelled on WORKBank, with CM's panel.
- **P-LM-13. Data hygiene.** (Retire, change.)
  - Retire the "FC/DC structural pattern" finding.
  - Treat the database as authoritative over the synthesis counts (666 vs 645 tasks; S 4 vs 9; H 146 vs 136).
  - Normalize CLD vocabulary.
  - Map SOC 2010 to 2018 explicitly in every index join.

---

## 9. Disagreements and trade-offs

- **With v1 (the analyst record).** I would downgrade all S calls. I also read the "relational core is automation-resistant" finding as normative. Capability measures rate some relational tasks as exposed. What is resistant is *accountability*, which is a governance choice that can change. [E/J] Trade-off: protecting the relational core by definition is comforting and easy to communicate, but it may hide real compression of preparatory relational work, such as meeting summaries and comment synthesis.
- **With the CA audit.** I agree on almost every point (§10 of the audit). On Ac novelty I differ slightly. The concept is close to Eloundou E1. v1's contribution is the public-agency staffing hypothesis, which belongs at the role level, not the task level.
- **With FC (anticipated).** Field judgment is protected from *LLM* exposure, and the data confirm that. But (a) the desk half of environmental work is among the most exposed in the economy, and (b) the *sensing* vector does reach field survey work, unmeasured. Trade-off: emphasising fieldcraft protects a valued identity but could leave early-career field-to-office pathways (inventory → analysis) unprepared.
- **With IA (anticipated).** Automated extraction scales, but my pilot shows lexical matching is right only about a quarter of the time on environmental task text. Trade-off: cost and speed vs validity. I recommend human-in-the-loop crosswalks for the core and automation only for candidate generation and drift detection.
- **Multi-source signals vs "usable tomorrow".** HR users want one label per role, and I want components and confidence shown. Proposed resolution: one computed headline per role (direction plus confidence), with drill-down to components. CA decides.
- **Theoretical vs observed measures.** Consumer usage under-samples government, so observed measures *understate* environmental exposure, while theoretical measures *overstate* near-term change. Keeping both increases complexity but avoids systematic bias in either direction. [J]
- **Conflict of interest.** The best usage data come from an AI vendor, and EMST is being built with that vendor's model. Trade-off: data quality vs perceived independence. Triangulate with Microsoft and agency data, and disclose (§10).

---

## 10. Issues outside my area that affect the vision

- **The first users are in a contracting system.** Federal and state training offices face hiring restrictions and senior attrition. The taxonomy's near-term value may lie more in *redeployment, cross-training and knowledge continuity* than in new-hire pipelines. (FH, SL, CM, AS) [J]
- **Data access for the repo pipeline.** Hugging Face was unreachable from the build environment. A reproducible signal pipeline needs an approved data-access path, or mirrored, licensed snapshots with provenance. (DE)
- **Independence and disclosure.** Using Claude to build EMST while ingesting Anthropic's usage data needs an explicit disclosure and a triangulation rule in governance. (AS, CP)
- **Tribal workforce invisibility.** National indices and FWD do not see Tribal natural-resource employment, except the roughly 900 Tribal fire personnel noted in USWFS. Any Tribal signal must follow TN's protocol. (TN)
- **Corpus skew.** The plan-requirement signal is 95% USFS western forests, so coverage beyond public lands needs other requirement corpora. (DB)
- **Privacy.** Series × grade × age headcount cells at small units can identify individuals; signal publication needs minimum cell sizes. (CP)

---

## 11. Open questions for the Chief Taxonomy Architect

1. Do you accept splitting exposure into technical exposure / deployment mode / staffing outcome (P-LM-01) as the DP-8 model?
2. Do you accept the two-family, two-period evidence rule (§7 Q3) as the gate for moving role change indicators?
3. Should v1's 4 S calls be migrated as Ac with an S-watch, with the original call kept as a v1 analyst assessment (P-LM-04)?
4. Which O*NET version anchors the crosswalk? Eloundou labels sit on O*NET 27.x tasks and O*NET is now at 30.x–31.0. I propose anchoring on the current release and carrying an explicit 27.x mapping for the Eloundou labels.
5. Will Phase 3 fund a two-coder crosswalk of about 666 + v2 tasks? That is the binding cost of any external calibration.
6. Should plan-requirement signals weight plans equally or by component count? Component counts over-weight long plans and monitoring reports; Idaho Panhandle 2022 alone supplies 29% of monitoring components.

---

## 12. Files written (all in `docs/research/labor-market-ai-impact/`)

| File | What it is |
|---|---|
| `report.md` | This text. The write was refused by the harness, so it is returned to the coordinator |
| `sources.csv` | 76 sources; read vs cross-referenced vs unverified marked in `accessed` and `status` |
| `index_appraisal.csv` | 34 indices, datasets and studies appraised (research question 1 schema) |
| `env_occupations_in_scope.csv` | 33 environmental occupations with exposure and trend signals (research question 2 schema) |
| `ecosystem.csv` | 35 ecosystem entities |
| `role_signals.csv` | 13 role signals |
| `v1_assessment.csv` | 18 verdicts on v1 elements |
| `candidate_competencies.csv` | 6 candidates |
| `env_occupation_exposure_scores.csv` | Percentiles on Eloundou, Microsoft and AIOE, plus BLS 2022–32 values |
| `index_agreement_spearman.csv` | Rank agreement among indices |
| `aei_env_rows_seen.csv` | AEI environmental task rows seen, mapped to O*NET-SOC |
| `omb_ai_inventory_env_bureaus_2025.csv` | Federal AI use cases in environmental bureaus |
| `omb_ai_inventory_env_function_counts.csv` | Use-case counts by function and deployment |
| `omb_cots_ai_env_departments_2025.csv` | COTS AI tools in environmental departments |
| `lmp_outputs/` | Component profile, monitoring by theme and method, monitoring questions, standards, coordination touchpoints, authoritative data, rule-era comparison, concentration, unmapped data values, summary |
| `v1_onet_pilot_matches.csv`, `v1_onet_pilot_summary.txt` | Automated-match pilot (shown as a failure case) |
| `v1_onet_pilot_candidates.txt`, `v1_onet_pilot_curation.csv`, `v1_onet_pilot_curated.csv`, `v1_onet_pilot_curated_summary.txt` | Curated pilot |

Scripts in `scripts/` (run with `python3 -I`):
- `lmp_demand_signals.py` (no arguments)
- `env_occupation_exposure.py <ext_dir>`
- `index_agreement.py <ext_dir>`
- `v1_onet_calibration_pilot.py <ext_dir> <v1 tasks.csv>`
- `pilot_candidates.py <ext_dir>`
- `pilot_curated_compare.py <ext_dir>`
- `aei_rows_to_onet.py <ext_dir>`
- `omb_inventory_env.py <inventory repo>`
- builders: `build_sources.py`, `build_index_ecosystem.py`, `build_occ_signals_assessment.py`

`<ext_dir>` holds clones of `openai/GPTs-are-GPTs`, `microsoft/working-with-ai` and `AIOE-Data/AIOE` under `<owner>_<repo>/repo/`. The OMB inventory is `ombegov/2025-Federal-Agency-AI-Use-Case-Inventory`. All re-runs reproduced identical outputs, and all seven schema CSVs parse with headers matching the TEAM_BRIEF schemas.