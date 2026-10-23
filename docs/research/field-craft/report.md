# Field Craft in EMST v2: definition, change, entry paths, safety and assessment

**Role:** Field Craft Lead (FC) · **Phase:** 2 · **Date:** 2026-10-23 · **Status:** research input for the Chief Taxonomy Architect (CA). This is not a decision.

**Labels.** [E] means evidence from a source I read; the source ID resolves in `sources.csv`. [J] means my professional judgment, and I say what it rests on. [S] means speculation, and I say what would confirm or refute it.

---

## Summary

**Definition.** Field craft is the capacity to perceive, measure, act and stay safe in a specific place. It means reading land, water, air and living systems directly, and producing the ground truth and physical interventions that all other environmental work depends on. It is formed through repeated, supervised exposure to real conditions and is shown by performance in the field, wherever the practitioner later applies it.

**Main findings**

1. **The representation is wrong, not the concept.** v1's Fieldcraft definition and irreducibility test are sound [J]. Storing one "primary craft" per competency hides blends that v1 itself had to work around:
   - five dual-primary exceptions and ten integration points;
   - a scale-dependency flag;
   - identical tools assigned to different crafts depending on the domain they sat in (2.3.2 vs 4.5.4; 2.3.3 vs 4.1.5) [E: FC-025, FC-026].

   I support CA's provisional model: crafts as weights on tasks, with two added attributes that weights alone lose. These are *field dependency* (must the work happen on site?) and *formation dependency* (was the expertise built in the field, even if the work is now done on a screen?).
2. **The v1 finding that "H arises only from FC/SC" is mostly a coding artifact.** I compared field-type tasks of the same kind under different parent crafts:
   - under FC-primary parents, 46% were coded H;
   - under DC-primary parents, 6% were;
   - the same task text, "Collect water samples…", is H/Hi under 1.2.4 but A/Med under 4.1.3 [E: FC-029; `scripts/h_artifact_check.py`].
3. **Field technology changes task bundles more than it removes field work.** Evidence is strongest for drones:
   - The USFS flew about 4,500 UAS hours in FY24, 99% of them by collateral-duty pilots, i.e. field staff who also fly [E: FC-002, FC-009].
   - UAS aerial ignition treated 188,986 acres and is replacing helicopters for ignition [E: FC-002, FC-010]. v1 coded fire as having "zero robotics vectors" [E: FC-027].
   - When Interior restricted drones, work went back to people on foot covering smaller areas [E: FC-001].
4. **Adoption is limited mainly by policy and money, not by what the technology can do** [E: FC-001, FC-003, FC-005, FC-008]. Three examples:
   - Federal drone restrictions: the American Security Drone Act from December 2025, the FCC Covered List from December 2025, and a 2026 FCC proposal reaching drones already in service.
   - Part 108 (BVLOS) was still not published as of July 2026.
   - Compliant aircraft cost several times more than the ones they replace.
5. **Entry paths are being cut now, by fiscal and policy shocks rather than by automation.**
   - In 2025 the USFS hired no non-fire seasonals and lost about a quarter of its non-fire workforce.
   - For 2026 it committed to 2,000 seasonals [E: FC-013, FC-014, FC-016].
   - AmeriCorps conservation corps lost about $400M [E: FC-021].
   - Trail miles maintained fell 22%, and the agency itself names lost skills [E: FC-015].

   v1's tacit-density "protection" and its CLD flag cannot see this [J].
6. **v1 misses large parts of the field workforce.** It has no wetland delineation, compliance inspection, contaminated-site field work, marine or boat work, utility vegetation management, air-monitoring station operation, biosecurity, chain of custody or sensor-network field operations [E: FC-029]. I propose 31 candidate competencies.
7. **Field craft can be assessed without counting years.** Fire task books, check rides, blind re-measurement against tolerances, observer calibration and paired field-versus-lab tests already exist [J; E for PTB mechanics via FC-030]. I provide 48 anchors across 12 competencies.

**Evidence limits.** The shared web-search budget ran out after my first eight searches. Unsurfaced URLs, including the BLS Occupational Outlook Handbook and NWCG PMS 310-1, were blocked. Sections 2, 4 and 5 therefore rest more on [J] than I would like. The standards I rely on are listed in `sources.csv` with status `unverified`, so a follow-up pass can confirm them (§0).

---

## 0. Method, sources and limits

**What I read**
- The charter and team brief.
- v1 documents in `legacy/v1/docs/`:
  - craft criteria (FC-025);
  - Task 11 craft record (FC-026);
  - D4 exposure record (FC-027);
  - D2 field-technology record (FC-028);
  - the wildland fire workforce report (FC-030);
  - Structural Conditions (FC-031);
  - the forester PD prototype (FC-032).
- The v1 database and the normalized baseline (FC-029).
- CA's `architecture_hypotheses.md` and `architecture-audit.md`.
- CM's `family_craft_blend.csv` (FC-034).

**Web evidence**
- 8 searches before the shared budget was exhausted.
- About 28 fetches of pages those searches surfaced.
- I chose:
  - federal audits and agency program data (FC-001, FC-002) for adoption, because they report scaled practice rather than pilots;
  - congressional letters and trade press quoting agency testimony (FC-013–FC-016) for 2025–26 staffing, because no agency workforce dataset for 2026 was reachable;
  - vendor and blog sources (FC-005, FC-008) only for regulatory dates I could cross-check, and I labelled their quality Low or Medium.

**Blocked**
- BLS OOH pages for forest and conservation technicians and for environmental science and protection technicians (FC-035, FC-036).
- NWCG PMS 310-1 (FC-037).
- LM should supply BLS technician series.

**Three analyses (reproducible; scripts in `scripts/`)**

1. Review of the 49 v1 FC-primary competencies. This covers text, indicators and exposure tags, plus a count of vague indicator verbs: 139 of 1,157 indicators begin with "Understands", "Expert in", "Shapes", "Provides" and similar.
2. A test of the H-only-from-FC/SC claim across all 666 tasks (`scripts/h_artifact_check.py`).
3. OpenLMP plan components (FC-033):
   - monitoring-program staffing in the Sierra and Sequoia NF plans (`scripts/lmp_monitoring_staffing.py`);
   - a crude lower-bound count of explicit field-survey, verification and inspection requirements (`scripts/lmp_field_requirements.py`).

   LM owns the full plan-demand analysis; mine is illustrative.

The `scripts/build_*.py` files regenerate every CSV in this folder.

**What is unverified, and what would confirm it.** Every program and standard marked `unverified` in `sources.csv` (FC-038 to FC-065) is cited from professional knowledge. Examples are the HAZWOPER supervised-field-day rule, FIA hot/cold/blind checks, AIM observer calibration, the spotted owl PAM program and the federal eDNA strategy. A verification pass should read each one. Where my claim depends on a detail, the text says so.

---

## 1. What field craft is

### 1.1 Definition (v2)

> **Field craft** is the capacity to perceive, measure, act and stay safe in a specific place — reading land, water, air and living systems directly, and producing the ground truth and physical interventions that other environmental work depends on. It is formed through repeated, supervised exposure to real conditions and is evidenced by performance in the field, wherever the practitioner later applies it.

What changes from v1 (FC-025):

1. **Ground truth becomes a defining output.** v1 listed "produces ground truth" as one indicator among four. In v2 it is a defining output, because every scaled remote product now depends on it [J].
2. **Craft is located by where the expertise is formed and validated, not only where the task is done.** This matters because more field-formed work now happens on screens: verifying AI species calls, reviewing drone imagery, reading sensor feeds [J].
3. **Safety and working with people on the land are named as components.** v1 put them in Domain 4.4 and in Statecraft respectively [J].

### 1.2 Seven components

| # | Component | What it is | Observable signs | How technology is changing it |
|---|---|---|---|---|
| FC-a | **Perceptual expertise** | Reading the site: identification, sign, condition, anomaly, across seasons and states | Correct IDs on blind tests; recognizing implausible records; detecting what is missing | AI suggests identifications; the human role shifts to adjudication, which still needs field-formed perception [J] |
| FC-b | **Measurement and sampling integrity** | Producing defensible data at the point of observation: protocol fidelity, calibration, QC, custody; knowing when conditions invalidate the protocol | Agreement with blind re-measurement or reference observer; clean blanks; justified deviations | Sensors automate measurement; the field task becomes keeping instruments valid (siting, drift, fouling) [J] |
| FC-c | **Situated judgment and intervention** | Deciding and acting in place with incomplete information: go/no-go, timing, triage, irreversible actions (felling, burning, excavation, capture) | Decisions documented against conditions; justified declines; outcomes | Decision support and models inform the decision; accountability and the act stay with the person on site [J] |
| FC-d | **Physical and operational skill** | Tools, machines, vehicles, vessels, aircraft (crewed and uncrewed), instruments; maintenance and improvisation; fitness | Field evaluations, check rides, sawyer levels | New platforms (UAS, machine control) add operating and supervising tasks [E: FC-002] |
| FC-e | **Risk management in uncontrolled environments** | Hazard recognition, lookouts-communications-escape routes-safety zones (LCES) thinking, job hazard analysis (JHA), emergency response, lone work, remote medicine | Site-specific briefings; stop-work calls; scenario performance | Technology removes some exposures and moves or creates others [E: FC-001] |
| FC-f | **Place knowledge and temporal depth** | Knowing a place's history, variability and reference conditions, built over seasons there; respecting others' place knowledge | Predictions about the site that prove right; reconciling records with field evidence | Remote archives help; staff turnover destroys it [J] |
| FC-g | **Working with people on the land** | Leading crews; reading the site together with landowners, permittees, contractors, volunteers and Tribal monitors; teaching field judgment | Crew QA trends; joint field visits; teach-back | Smaller crews and fewer entry hires make deliberate transfer central [E: FC-015; J] |

### 1.3 A revised test

v1's test asks whether a competency "could not be performed remotely, from data, or through institutional process" (FC-025). That location test will steadily reclassify field-formed expertise as data craft as tools move work off site [J]. I propose rating each **task** for field craft weight **2 (defining)** if it meets the presence test **and** at least one of the other two:

1. **Presence:** competent performance requires the practitioner's senses or body in the place at the time.
2. **Physical consequence:** the practitioner must manage consequences in the physical world in real time (safety, irreversible intervention).
3. **Ground-truth authority:** the output is the reference against which other data are judged.

Rate **1 (supporting)** where field knowledge catches errors but intermediate performance is possible without it.

Separately, record **formation dependency = yes** when the expertise needed must have been built through field exposure, even if the task is remote. This replaces v1's rule "assign FC-secondary liberally" (FC-025). That rule was the right diagnosis, but it was not an instrument anyone could act on [J]. The full rubric is in `craft_profile_rubric.csv`.

### 1.4 Boundary with data craft: the measurement chain

[J] The clearest line runs along the chain from the world to a decision.

```
place ──► observation/instrument ──► validated field record ──► dataset ──► analysis/model ──► decision product
 └────────── FIELD CRAFT owns ──────────┘   shared: design &   └──────── DATA CRAFT owns ────────┘
   (siting, perception, collection,          validation
    calibration, field QC, custody,
    in-situ verification)
```

**Rule of thumb:** *where would the error arise, and who would catch it?* If the error starts in contact with the physical world and can only be detected there, it is field craft. If it starts in structure, inference or modelling, it is data craft.

Blend zones where both are defining:

| Blend zone | Field craft part | Data craft part |
|---|---|---|
| Sampling and monitoring design | feasibility, site rules, access, what can be seen | statistical design, power |
| Validation of remote, model and AI outputs | reference data collection, cause of mismatch | accuracy statistics, model correction |
| Drone missions | flight, site hazards, ground control | photogrammetry, products |
| eDNA | contamination-free sampling, site and timing | assay, bioinformatics, interpretation |
| AI species detection | adjudication by field-formed experts | model training and evaluation |

### 1.5 Boundary with statecraft: acting in place versus making it stick

[J] Statecraft produces authorization and commitments across institutions. Field craft acts in place within, and as evidence for, that authorization. Blends:

- **Compliance inspection.** Observing and documenting is field craft. Legal authority and negotiation are statecraft.
- **Burn boss versus burn plan approval and smoke permits.**
- **Range field visits with permittees.** Reading the allotment together is field craft; the permit is statecraft.
- **Incident operations.** Line work is field craft; the incident management team to agency interface is statecraft.
- **Cultural resource field survey.** Field craft, with Section 106 as statecraft. Any Tribal-knowledge dimension is for TN.

v1 claims Domain 6 has "no point of contact with place-based embodied practice" (FC-026). v1's own tasks contradict this:
- 6.1.2 T1 "Conduct field inspections";
- 6.1.5 T1 "Respond to reports of environmental violations on managed lands";
- 6.7.5 T1 "Monitor air pollutant concentrations" [E: FC-029].

This is why CM's blend analysis gives the Environmental Policy and Environmental Health & Justice families about 1% field-craft weight (FC-034) [E]. That figure is an artifact of tagging, not a property of those jobs [J].

### 1.6 Position: competency-level primary craft is the wrong stored representation

**Position.** Store craft at the **task** level as three independent ordinal weights (0/1/2), plus `field_dependency` and `formation_dependency`. Compute competency and role blends from task weights, weighted by importance and time share in role profiles. Keep "dominant craft" only as a derived display field. [J]

Why:
1. **v1's own workarounds show the strain.** The evidence is in §1 and in the audit (FC-025, FC-026).
2. **Crafts change across a competency's task ladder.** In 1.1.2 Biodiversity assessment, T1 (design and implement protocols) is field plus data, T2 (analyse long-term data) is data, and T3 (report to policymakers) is statecraft [E: FC-029]. The single FC label hides the fact that the learning ladder *starts* in the field.
3. **Technology moves blends at the task level.** UAS ignition changes the firing task, not the whole prescribed fire competency [E: FC-002].
4. **The theory of change is about blends in people and roles.** Mobility analysis needs role-level blends. CM currently has to build them from primary labels, each counting as 100% of one craft (FC-034) [E].
5. **Workforce planning needs field dependency, which no craft label carries.** It drives duty stations, fitness, safety training and telework [J].

**Worked example** [J; v1 task text from FC-029]:

| Task | FC | DC | SC | Field dependency | Formation |
|---|---|---|---|---|---|
| 4.5.4/2.3.2 T1 Plan and fly a survey mission near crews | 2 | 1 | 1 | on-site-required | yes |
| 2.3.2 T3 Process imagery to orthomosaics | 1 | 2 | 0 | remote-capable | yes (ground-control and artifact judgment) |
| 6.1.2 T1 Conduct field inspections | 2 | 0 | 2 | on-site-required | yes |
| 7.2.1 T1 Evaluate AI species IDs against field observations | 2 | 1 | 0 | remote-capable | yes |

A role whose time splits 40/40/20 across the first two rows and a reporting task gets a computed blend. A label cannot give that.

**Trade-off.** Rater burden and reliability (IO). Mitigation:
- pre-fill from v1 (primary = 2, secondary = 1);
- re-rate only contested tasks and the ten v1 integration points;
- use a 3-level ordinal rather than continuous weights.

This is CA's fallback, and I recommend it as the *first* choice for field craft [J].

---

## 2. How field work is changing (evidence 2023–2026)

The full technology-by-technology table is in `field_tech_change_matrix.csv` (18 technologies). It covers what is automated, what is augmented, the new field tasks, what stays human, the change level, adoption status and barriers.

### 2.1 Seven patterns

1. **The field moves; it does not vanish.**
   - Observation shifts to *instrument stewardship* (siting, servicing, verifying sensors, recorders and cameras) and to *validation* (ground-truthing automated outputs) [J; E for drones: FC-002].
   - When the tools were taken away, field programs fell back on people on foot. Karner blue butterfly monitoring "shifted to on-foot staff covering a much smaller area" [E: FC-001].
2. **Technology is absorbed into field roles more than it creates separate roles.** 99% of USFS trained pilots are collateral-duty [E: FC-009]. The drone pilot is usually the botanist, fuels tech or hydrologist. This supports field-craft-primary treatment of UAS operation.
3. **Every automated monitoring system carries a calibration cost.** Lidar inventories need calibration plots. Classifiers need verified labels. Burn-severity maps need field checks [E for BAER practice in v1 notes: FC-027; J generally]. This creates *ground-truth work*. It is a natural learning role if designed as one (§3).
4. **Fewer, more skilled field visits.** Continuous sensors and remote targeting reduce routine visits. Remaining visits are for problems, calibration and judgment [J]. This raises the proficiency needed per visit and removes the easy repetitions novices learn on [J].
5. **Automation hits the primary-learning tasks first.** v1's CLD idea is right for data handling (FC-027, FC-028). In field work, though, the larger loss so far is whole entry jobs cut for fiscal and policy reasons (§3) [E: FC-014].
6. **Risk is moved, not removed** (§4) [E: FC-001].
7. **Adoption is gated by policy, procurement, money, connectivity and data systems more than by capability** (§2.3).

### 2.2 Drones and uncrewed systems (strongest evidence)

**Scale [E: FC-002]**
- USFS FY24: 17,255 flights (the report also states 16,898), 4,536 flight hours (up 78% from FY23), 342 aircraft and 371 pilots.
- Only 73% of trained pilots were current on training and proficiency.
- Natural-resource missions were 29% of hours: invasive weed mapping, timber and vegetation surveys, habitat, infrastructure inspection.
- Wildland and prescribed aerial ignition was about 855 hours and 188,986 acres.
- Qualification runs A-450 → S-373 → incident trainee → qualified UASP. Of 410 USFS UASP records, 172 were qualified and 160 were trainees.
- Aerial ignition operators work under the firing boss. Training takes 1.5–3 years [E: FC-009].

**Policy shocks [E: FC-001]**
- Interior's 2019–20 restrictions cut flights sharply between 2019 and 2023:
  - BLM 3,643 → 528;
  - FWS 1,340 → 689;
  - USGS 3,170 → 1,649.
- Average drone cost rose from about $2,600 to over $15,000. An ignition drone rose from about $52,000 to about $86,000.
- BLM stopped drone-based cultural resource monitoring.
- Some aerial ignition moved back to helicopters, which officials said raises personnel risk.
- The American Security Drone Act bars federal operation and procurement of certain foreign drones from December 2025.

**Further restrictions [E: FC-003, FC-004, FC-008]**
- In December 2025 the FCC added foreign-produced UAS and components to the Covered List. The action was forward-looking.
- Exemptions followed in January–March 2026.
- An August 2026 FCC proposal could reach already-authorized thermal, LiDAR and agricultural-spray drones (vendor-sourced, Low quality).
- For state and local fleets, a compiled estimate cites 467 restricted drones in 25 states and up to $2B national exposure (Medium-Low).

**Part 108 (BVLOS) [E: FC-005, FC-006]**
- NPRM August 2025; sent to OIRA July 2026; publication not verified as of today.
- It moves accountability from individual pilots to operator organizations, with required training programs and safety management systems for certificated operators.
- It defines an operations supervisor role and flight coordinators who can oversee multiple aircraft.
- Permitted limits: agriculture up to 10 active aircraft; aerial survey and civic-interest operations up to 25.
- [J] The field task changes from flying one aircraft to supervising several automated ones. This is v1's "V" (supervision) type, arriving through regulation rather than technology alone.

**Implication [J].** Durable competency: *operate and supervise uncrewed and automated field systems* (FC-C14). Platform, software and Part 107 or agency cards belong in the tools and credential layer. v1 4.5.4 and 2.3.2 should merge into FC-C14.

### 2.3 Other technologies (mostly [J]; external evidence not reachable this session)

| Technology | Field work it removes or reduces | Field work it adds | What stays human |
|---|---|---|---|
| Lidar and photogrammetry | Plot counts per estimate; manual height and canopy measurement | Calibration plots; deciding where plots are still needed; ground control | Species, defect, decay, regeneration, soils; knowing where remote metrics fail (FC-032) |
| eDNA | Many visual and capture surveys for presence | Contamination-controlled sampling; confirmation after detections | Field contamination control; interpreting detections in context |
| Passive acoustic monitoring | Night call-back surveys | Recorder siting and servicing; detection review | Verifying classifier calls; siting; follow-up |
| Camera traps + AI | Sorting blank images | Deployment and servicing; verifying labels; privacy handling | Difficult IDs; study design |
| Mobile data collection | Transcription | Form design with field users; device-failure procedures | Observation itself; noticing what the form doesn't ask |
| Continuous sensors (water, soil, weather) | Routine grab-sample visits | Siting, calibration, fouling and drift management; side-by-side checks | Recognizing physically wrong data; deciding when to sample manually |
| Low-cost air sensors | — (adds density) | Colocation, maintenance, community network support | Judging fitness for decisions |
| Satellite products | First-pass mapping and triage | Accuracy assessment and mismatch coding | Below-canopy and below-surface reality; site history |
| Robotics and autonomy (planting drones, machine control, winch-assist, fire robots) | Some planting, some operator functions | Supervising automation; new hazard controls | Terrain and soil reading; stop decisions; planting microsites [S on planting-drone outcomes] |
| AR / heads-up displays | — | Overlay verification | Reading the actual site |
| AI field assistants | Reference lookup; draft JHAs and reports | Verifying suggestions; teaching novices when not to trust them | Final ID and safety calls (FC-027 notes AI-drafted JHAs emerging) |

**Tool-layer or task-bundle?** [J] My test: if a practitioner proficient with the old method reaches the *same proficiency anchors* after brief familiarization, the change belongs in the tools layer (L4). If the anchors themselves change (new things to notice, new failure modes, new decisions, new people to coordinate with), the task bundle (L2) has changed. By this test:
- **Tools layer:** mobile data collection, GPS, field meters, AR, AI ID apps.
- **Task bundle:** drones, UAS ignition, BVLOS supervision, lidar inventory, PAM, camera-trap AI, continuous sensors, satellite validation, utility risk analytics.

### 2.4 Adoption: what is known and what is assumed

- **Known [E].** Adoption follows policy and price. DOI flights fell 50–86% under restriction, while USFS hours grew 78% in a year with domestic platforms (FC-001, FC-002). Agencies lean on contracted services where in-house capacity is constrained. Interior already contracted about 70% of crewed aviation missions and opened a call-when-needed UAS services contract in 2018 (FC-011, outdated but structural).
- **Known [E].** Qualification and currency are binding constraints: 73% of USFS pilots current, and ignition training takes 1.5–3 years (FC-002, FC-009). So are airworthiness practices "not yet aligned with traditional piloted aviation" (FC-009).
- **Judged [J].** For sensors, PAM, eDNA and camera traps, the binding barriers are:
  - maintenance budgets (capital grants buy sensors, not service visits);
  - data systems and security approvals for cloud apps;
  - connectivity in remote areas;
  - standards and regulatory acceptance (eDNA detections, low-cost air sensors);
  - staff time to verify AI output.

  I found no adoption studies in reach this session. The environmental-sector evidence base on field technology adoption is thin, and that is itself a finding.
- **Union and safety rules [S].** I found no evidence specific to environmental agencies on bargaining-unit or safety-rule constraints on field automation. Utilities and line-clearance contractors are the likely place to look (PS).

### 2.5 What stays irreducibly human (for now) [J]

- Deciding to act, or not to act, in an uncontrolled environment where life, safety or irreversible change is at stake: burn go/no-go, felling, capture, stop-work.
- Producing reference truth others rely on, and recognizing when the reference itself is compromised.
- Perceptual judgment in novel or ambiguous conditions: look-alikes, partial sign, disturbed sites, novel ecosystems.
- Face-to-face work with people on the land, where trust comes from walking the site together.
- Teaching all of the above to the next person.

"Irreducibly human" is not "un-augmented". Nearly every one of these tasks is now tool-assisted. That is why I recommend splitting v1's H into *presence required* and *automation type* (§8, Q4).

---

## 3. Entry paths at risk

### 3.1 Evidence (2025–26)

| Signal | Evidence |
|---|---|
| USFS non-fire seasonals | None hired in 2025 (budget). 2,000 committed for 2026, all titled forestry technician [E: FC-014, FC-016]. The FY2025 freeze was announced in October 2024 over a "half-billion-dollar funding gap", before the 2025 federal workforce actions [E: FC-022]. |
| District scale | Jackson RD 15 seasonals (2024) → 5 (2026); Teton Basin 9 → 2; 2025 = 0. Applications open about 10 days instead of a December opening [E: FC-016]. |
| Early-career staff | About 3,400 USFS probationary employees fired in February 2025, out of about 35,000 staff, across trails, timber and watershed restoration [E: FC-017]. "Probationary employees are more likely to do fieldwork" [E: FC-018, local report]. |
| Overall USFS | About 5,000 voluntary departures; about a quarter of the non-fire workforce lost [E: FC-013]. Up to 1,400 red-card holders left [E: FC-014]. |
| Trails | Miles maintained −22% in 2025. No seasonal trail crews or wilderness rangers. Lost skills: "equipment operation, rock wall masonry, volunteer coordination, project management" [E: FC-015]. |
| NPS | About 1,700 lost (~9%); clearance for up to 7,700 seasonals [E: FC-020]. |
| Conservation corps | About $400M AmeriCorps cuts across >1,000 programs. Corps terminated or cut 33%. PCT corps hours ~19,000 → ~4,000 [E: FC-021]. |
| Surge capacity | Non-fire staff with red cards (the "militia") are a hidden fire capacity. It shrinks with non-fire field roles [E: FC-019]. |
| Historical baseline | About a third of USFS employees were seasonal; NPS hired 8,000–10,000 seasonals a year [E: FC-023, 2017, outdated]. |

**Not evidenced here.** National technician employment trends (BLS blocked; LM to supply), and state, Tribal, NGO and private technician hiring. The federal contraction may partly shift field work to partners, contractors and states. Friends of the Bridger-Teton is hiring 17–18 seasonals [E: FC-016], and USFS testified "we're going to need a lot of help from our state partners, our community partners" [E: FC-013]. Whether that preserves learning depends on whether partner crews are supervised, assessed and recorded [J].

**Plan demand stays.** Recent plan monitoring programs (Sierra and Sequoia NF, 2023) list GS-5 and GS-7 aquatics and range technicians alongside GS-11 specialists, with notes that specialists "will need GIS support" [E: FC-033]. Monitoring obligations in plans assume a technician layer that is shrinking [J].

### 3.2 Mechanism [J]

Field craft reproduces through *graduated exposure*:
- many seasons of repetitive but varied field tasks (plots, surveys, trail work, saw work, holding line);
- done under experienced people;
- in many conditions;
- with feedback.

Seasonal and corps jobs were the sector's main supply of these repetitions. Two forces now act on them:

1. **Contraction (now).** The jobs and the supervisors disappear together. Tacit density gives no protection, so v1's exposure instrument is blind to this.
2. **Automation (next).** Sensors, AI triage and remote products remove the easiest repetitions: grab samples, call-back surveys, plot measurements, image sorting. These are the ones novices learn on.

If both continue, the sector will have more data and fewer people who can tell whether it is right. That is the failure mode the charter's data-heavy warning points to.

### 3.3 Where tacit expertise gets built instead (proposals)

1. **Ground-truth and sensor-service work as designated learning roles (P-FC-08).** Every remote-sensing, AI-monitoring or sensor program funds field validation and service visits anyway. Structure them as supervised entry roles: blind reference data, mismatch coding with a senior, rotation across sites and seasons. Use anchors FCA-GT-1/2 and FCA-SENS-1/2. [J]
2. **A multi-employer registered field technician apprenticeship (P-FC-09).** Agencies, states, Tribes, corps, NGOs and consultancies would share one competency standard and one evidence record. Model it on the Wildland Fire Apprenticeship Program and task-book logic [J; FC-062 unverified]. LC leads design; FH and SL the hiring links.
3. **A portable field evidence record (P-FC-10).** A task-book-style record for seasonal, corps and partner crews, so field seasons with any employer count toward qualification and hiring. Issue as Open Badges or CLR (LC, IA). Corps hiring authorities (Public Land Corps, Resource Assistants) already convert service into eligibility [J; FC-063 unverified].
4. **Entry-path health as a computed indicator (P-FC-11).** Per role, compute whether formation tasks remain in the entry role, and whether entry hiring exists. Attribute the driver (fiscal, policy, automation). This extends CA's pathway-level CLD.
5. **Field rotations for desk roles where formation dependency = yes, and analyst rotations for field technicians (P-FC-12)** [J].
6. **Formation-preserving automation design guidance for adopters (P-FC-13).** Keep a blind re-identification sample, manual calibration checks and periodic manual surveys at sensor sites. These are both QA and learning repetitions [J]. This complements v1 7.2.2, which designs such workflows.
7. **Rare-event simulation.** Escapes, floods and entrapments cannot be scheduled. Sand tables, exercises and after-action review libraries cover them [J].

---

## 4. Safety and the physical domain

### 4.1 Existing systems [J; standards unverified this session unless noted]

- **HAZWOPER (29 CFR 1910.120).** Requires classroom hours *plus supervised field experience* for site workers, and annual refreshers (FC-038). It is one of the few rules that requires embodied practice by regulation.
- **Wildland fire (NWCG PMS 310-1).** Training, experience, observed Position Task Books with incident-type coding, a fitness test and currency [E via FC-030; primary blocked, FC-037]. It is the most mature performance-based field qualification in the sector.
- **Saws.** Agency sawyer certification at tiered levels with field evaluation (FC-048).
- **Boats.** DOI MOCC (FC-049).
- **Aviation.** Interagency aviation training; for UAS, A-450 and S-373 [E: FC-002].
- **Remote medicine.** WFA, WFR and EMT certifications.
- **Heat.** A proposed OSHA standard (2024); current status not verified (FC-039).
- **Animal capture.** Animal-care protocols. Pesticides: state applicator licensing.

### 4.2 How technology changes risk profiles

- **Removes exposure** [E]: UAS ignition and UAS IR flights replace low, slow crewed flights (FC-010). Policy reversal returns the risk: "BLM and NPS shifted some aerial ignition to helicopters… raises risks to personnel" (FC-001).
- **Creates new hazards** [J]:
  - drones near crewed aircraft (the USFS lists counter-UAS and aircraft tracking as a program topic, FC-010);
  - lithium battery fires;
  - teleoperated or automated machines near people.
- **Automation complacency and skill decay** [J]: GPS dependence (v1 flagged it, FC-027); AI-drafted JHAs that skip the thinking (FC-027).
- **Lone work** [J]: smaller crews and fewer seasonals mean more lone or pair work. Satellite messengers mitigate this but don't replace a partner.
- **Heat and smoke** [J, S on regulation]: rising exposure; no federal standard yet verified.

### 4.3 Taxonomy implications

- Separate **field risk management (FC)** from **safety program management (SC or management)**. v1 4.4.1's Advanced and Expert levels drift into workers' compensation and compliance audits [E: FC-029].
- Add FC-C18 (navigation with and without digital aids), FC-C19 (heat, smoke and exposure) and FC-C27 (risk where people work alongside automated systems). Recast 4.4.3 SAR as a specialization.
- Certificates go in the credential layer as **inputs**. Proficiency is assessed by scenario and field evaluation. v1 4.4.2 defines levels by holding CPR, WFR or EMT [E: FC-029], and a card is not a performance.

---

## 5. Assessing field craft

### 5.1 What existing systems teach [J; E for PTB via FC-030]

| Mechanism | What it proves | Lesson for EMST |
|---|---|---|
| Position Task Books (fire) | Trainee is *observed* doing listed tasks, in the right context (wildfire vs prescribed), signed by a qualified evaluator | Code anchors by condition; require observation, not attestation |
| Check rides (aviation, UAS) | Normal and abnormal procedures performed in front of an evaluator | Include abnormal-event scenarios |
| Blind re-measurement (FIA hot/cold/blind checks) | Measurement agrees within stated tolerances | Tolerances (measurement-quality objectives) make "accuracy" observable |
| Observer calibration (AIM; IIRH) | Observers agree with a reference observer | Calibration records are ready-made evidence |
| Field evaluations and assistance visits (EPA NARS) | Crews follow protocol in the field | Audits double as assessment |
| Paired field and lab tests | Texture by feel vs particle-size analysis | Tacit skills can be scored against an independent reference |
| Supervised field days (HAZWOPER) and supervised field months (SOI archaeology standards) | Exposure under supervision | Exposure is a prerequisite, not proof |
| Graded practical ID tests (BSBI FISC; CIEEM levels) | Identification skill independent of tenure | Station-based ID tests are feasible at scale |

### 5.2 Design principles for field-craft anchors

1. **Behaviour under real conditions**, with the conditions stated (season, site type, disturbance).
2. **An independent reference** where possible: blind re-measurement, reference observer, lab result, recorded outcome.
3. **A named assessor type and method**: evaluator, QA crew, check ride, portfolio, audit.
4. **Reward correct uncertainty and justified refusal.** "Unknown, voucher collected" and "declined to fell" are evidence of proficiency.
5. **Test outcomes, not protocol steps.** Steps are necessary but not sufficient. The anchor should catch the person who follows the checklist and misses the hazard.
6. **Advanced and Expert levels show what the person does for others' performance**: calibrating observers, adjudicating disputes, designing protocols that pass audit. Reputation ("achieves recognition", "shapes practice") is not an anchor. 139 v1 FC indicators use such verbs [E: FC-029].
7. **No years.** Field seasons vary too much in exposure. Record exposure (seasons, sites, conditions) as a portfolio input, not as the level.
8. **Reuse existing QA evidence** so assessment costs little: calibration plots, check cruises, task books, audits.

### 5.3 The anchor file

`fieldcraft_proficiency_anchors.csv` contains 48 anchors at four levels (Foundational to Expert, matching v1 until IO and CA settle DP-4) across 12 competencies. Six are v1 competencies to carry or rewrite: 4.1.1, 1.3.2, 1.4.3/4.1.2, 4.1.4, 4.1.3, 4.5.2. Two are merged fire and safety competencies: 4.3.2/4.2.3 and 4.4.1. Four are candidates: FC-C01, C02, C14, C20. Thresholds are illustrative and tied to program measurement-quality objectives. IO must validate them.

### 5.4 Making place-based tacit knowledge observable without reducing it to protocol [J]

- **Prediction tests.** Walk the site and predict what the plot will show, where the gully will head-cut, where the burn will slop over; then check.
- **Seeded anomalies.** Planted errors in AI labels, data sheets or sites (FCA-ID-2).
- **Condition coverage.** Evaluate across seasons, disturbance states and sites, the way task books code incident type.
- **Teach-back.** Articulating cues to a novice is itself evidence (FCA-LEAD-1). Not all tacit knowledge can be articulated, so this complements rather than replaces performance.
- **Decision audits and after-action reviews.** Review documented calls against outcomes, including no-go decisions.
- **Place-tenure portfolios.** Seasons at a site and range of conditions seen, recorded as exposure evidence, never as the score.

None of these turns judgment into a checklist. They observe its *results* under varied conditions.

---

## 6. Review of v1 field-craft competencies

Full verdicts are in `v1_assessment.csv`: 49 competencies plus 22 framework elements.

### 6.1 Verdicts on the 49 FC-primary competencies

- **Carry: 21.** Examples: 1.3.1, 4.1.1, 4.1.4, 4.2.5, 4.3.1, 4.5.2.
- **Change: 27.**
- **Needs evidence: 1** (4.7.5, building systems O&M; DB to decide scope).
- **Retire: none.**

The content is largely sound field practice. The problems are structure, observability and coverage.

### 6.2 Findings

1. **Duplication by domain** [E: FC-029, FC-026]. Science versions (D1) and implementation versions (D4) of the same field capacity exist side by side:
   - 1.2.4/4.1.3; 1.2.5/4.2.4; 1.4.2/4.1.2;
   - 1.2.1/4.1.4/4.6.5; 4.2.3/4.3.2;
   - 2.3.2/4.5.4; 2.3.3–2.3.4/4.1.5; 2.3.5/4.4.5.

   Consolidate them. Tasks should span knowledge to execution.
2. **Tool-bound items** [J]:
   - 4.1.5 (apps and sync);
   - 4.5.4 (drones; Part 107 in the knowledge statement);
   - 4.6.2 (GPS-guided tractors);
   - 1.6.2 (eDNA is a method).

   Rewrite them as durable competencies (FC-C14, FC-C16, FC-C23) and move the tools to L4.
3. **Observability** [E: FC-029]. Foundational and Intermediate indicators are often concrete, e.g. 4.1.1 "Sets up monitoring plots according to protocols". Advanced and Expert indicators are often reputational. Safety competencies use certification as proficiency.
4. **Data defects** [E: FC-029]:
   - merged title/description in seven FC competencies (1.2.4, 1.3.1, 1.4.2, 1.4.3, 4.1.4, 4.3.1, 4.3.3);
   - no proficiency text for 5.3.2 or 5.3.3.
5. **Exposure coding** [E: FC-002, FC-010, FC-027]:
   - fire is coded "zero robotics vectors" although UAS ignition is scaled practice;
   - near-identical tasks are coded differently (see §8, Q4).

### 6.3 Missing field competencies (31 candidates; `candidate_competencies.csv`)

| Group | Candidates |
|---|---|
| Field side of data and AI | Sensor networks (C01); ground-truthing (C02); AI detection adjudication (C03); observer calibration and QA (C31); field records (C23); sample custody and QC (C24) |
| Regulatory and compliance field work | Compliance inspection (C04); contaminated sites (C05); wetland delineation (C06); air monitoring stations (C17); trace, PFAS and eDNA clean sampling (C16) |
| Subsector coverage beyond public lands (with DB) | Stream geomorphic assessment (C07); rangeland monitoring (C08); utility vegetation management (C09); invasive EDRR (C10); biosecurity (C11); boats and marine/coastal work (C12); cultural resource field survey, with TN (C13); wildlife and fish capture (C15); tree risk (C26); process-based restoration (C30); carbon MRV field plots (C29) |
| Safety and operations | Automated field systems (C14); navigation (C18); heat and smoke (C19); human-machine risk (C27); field campaigns and logistics (C28); post-disaster assessment (C25) |
| People and place | Crew leadership and judgment transfer (C20); working with landowners, permittees and communities (C21); site history and reference conditions (C22) |

Of these, 12 are transforming, 8 emerging and 11 stable. Durable ("stable") field competencies are under-represented in v1, not only emerging ones [J]. Evidence labels are mostly [J]: subsector demand evidence could not be gathered this session. DB, PS and SL should add demand evidence.

**Suggested federal/state MVP priority** [J]: C01, C02, C03, C04, C06, C14, C16, C20, C24, C31. These cut across most field roles and carry the technology change.

### 6.4 Role signals (`role_signals.csv`, 21 signals; 12 [E])

| Type | Roles |
|---|---|
| Entry path at risk | Seasonal forestry technician; corps member; probationary early-career field staff |
| Declining | Trail crew and wilderness ranger; collateral-duty red-card surge capacity |
| New | UAS aerial ignition operator; BVLOS operations supervisor; ground-truth / validation technician [S] |
| Splitting | Wildlife survey technician (PAM); camera-trap technician |
| Transforming | Water-quality technician; inventory crew; utility vegetation inspector; compliance inspector; DOI and state drone programs |
| Merging | Agency field work moving to partner and contractor crews |

---

## 7. Indigenous and local knowledge: recognition without extraction

TN leads on governance; nothing here speaks for any Tribal nation or community. What follows is how *field craft design* should avoid harm, plus flags for TN [J].

1. **Record relationships and roles, not knowledge content.** The taxonomy can name competencies such as "work alongside Tribal monitors on their terms" (C13) and "reconcile field data with knowledge holders who choose to share" (C22). It never writes Indigenous ecological knowledge into indicators, tasks or anchors.
2. **Knowledge holders' authority over assessment.** Where a competency touches Indigenous knowledge, the community defines whether, how and by whom it is assessed. Proficiency anchors must not score it.
3. **Community-controlled markers.** Use metadata showing *that* a role or context involves Indigenous knowledge, under community-controlled labels (Local Contexts TK labels are one model, FC-051) and CARE principles (FC-050). Whether to use any such marker is TN's call.
4. **Place-bound knowledge of long-tenure non-Indigenous practitioners** (ranchers, fishers, long-serving technicians) is recognized the same way. Use exposure and tenure evidence plus performance anchors (prediction tests), not codification of what they know.
5. **Do not claim qualification equivalence.** Cultural fire practitioners are not "uncertified burn bosses". EMST must not map cultural burning onto NWCG positions without the nations' direction (flag on FCA-RX-4).
6. **Reference libraries.** Sound, image and specimen libraries that feed AI may carry Indigenous names or locations of sensitive species and sites. Inclusion requires consent (flag on FCA-ID-4).

**Flags for TN:** C13 co-drafting; 5.3.2 and 5.3.3 blank proficiency; cultural fire; Tribal monitor roles on projects; sensitive-site location data in field data systems; Indigenous Guardians and Tribal field technician pathways as part of P-FC-09.

---

## 8. Answers to CA architecture questions (FC, §6)

### Q1. Can field craft be expressed as weights on tasks without losing judgment earned outdoors? What anchors do raters need? (DP-5)

**Yes, if three things accompany the weights.** [J, resting on the v1 evidence in §1.6 and the artifact test below]

1. **Task statements at the right grain.** v1 field tasks often hide the judgment inside "conduct survey". Split *executing to protocol* from *adapting or deciding in place* where both exist (e.g., 4.1.1 "sample plots" vs "adapt sampling when site departs from protocol assumptions"). Otherwise both get the same weight and the judgment disappears.
2. **Two attributes that are not craft weights:** `field_dependency` and `formation_dependency`. Without formation dependency, screen-based work that depends on field-formed expertise will drift to DC, and field craft will look like it is declining when it is being exercised remotely.
3. **Proficiency anchors carry the "how well".** Judgment earned outdoors shows up mostly in *how* a task is performed at higher levels: justified deviations, correct refusals, predictions. *Which* tasks carry it matters less. Weights say what kind of work it is; anchors say how good the performance is; reproduction attributes say how it is learned.

**Rater anchors.** Use `craft_profile_rubric.csv`: 0/1/2 per craft, with the three-part FC test and examples per level. Calibrate on the ten v1 integration points plus my four worked examples. Code tasks **blind to parent competency, domain and v1 craft label**, because the artifact test shows parent labels steered v1 coding [E: FC-029]. I recommend the 3-level ordinal as the first choice, not the fallback: raters can defend "defining vs supporting" and cannot defend 0.6 vs 0.7 [J; S until IO pilots].

### Q2. Which field competencies are durable, and where is field technology changing the task bundle versus only the tools layer?

**Durable** [J]:
- The seven components as competencies: identification; measurement and sampling integrity; situated decision and intervention; tool, machine, vessel and aircraft operation; field risk management; place and site-history reading; field leadership and judgment transfer.
- Their subsector applications: wetland delineation, stream assessment, rangeland monitoring, inspection, contaminated-site work, tree risk, fire.

**The test:** a change is tools-layer if a proficient practitioner meets the *same anchors* after brief familiarization. It is a task-bundle change if the anchors change.

- **Tools layer only:** mobile data collection, GPS, meters, AR, AI ID apps (as aids).
- **Task bundle changes** (with evidence level):

| Change | Evidence |
|---|---|
| Firing with UAS ignition | [E: FC-002, FC-010] |
| Flying becoming supervising multiple automated aircraft under Part 108 | [E: FC-005, FC-006] |
| Lidar-assisted inventory: fewer plots, more calibration and validation | [J] |
| PAM and camera-trap AI: deploy, service, verify instead of observe | [J] |
| Continuous water and air sensors: service and QA instead of routine sampling | [J] |
| Satellite and utility analytics: field verification and override | [J] |

Full list in `field_tech_change_matrix.csv` (`change_level`).

### Q3. How can place-based tacit knowledge be observed for assessment without reducing it to protocol? Which reproduction-regime attributes matter?

**Assessment.** See §5.4: prediction tests, seeded anomalies, condition coverage, teach-back, decision audits, and independent references (blind re-measurement, lab, reference observer). Assess outcomes under varied conditions, not adherence to steps. [J; E for task-book mechanics via FC-030]

**Reproduction-regime attributes that matter** (defined in `craft_profile_rubric.csv`) [J]:

1. **Mentorship dependence** (low/medium/high): supervised in-place repetitions needed.
2. **Cycle dependence** (none/seasonal/multi-year or rare-event): how many natural cycles a learner must see. Rare-event skills need simulation.
3. **Place-boundness** (general/ecosystem-type/site-specific). This is critical for mobility:
   - general field skill (saw, meters, navigation) is portable across actors and regions;
   - ecosystem-type skill (regional flora, fuel types) carries a re-learning cost across regions but not across actors in the same region;
   - site-specific knowledge is lost when people leave.

   CM's transfer-friction model should use this.
4. **Credential gate** (none/internal qualification/external certificate/license).
5. **Currency decay** (low/medium/high).
6. **Entry-path dependence**, computed: whether formation happens mainly in entry or seasonal roles. It feeds pathway CLD and entry-path health (P-FC-11).

### Q4. Is v1's "H arises only from FC/SC" supported, or an artifact of the coding set-up? (audit §10.2.3)

**Mostly an artifact. Not supported as an empirical finding.** [E: FC-029 via `scripts/h_artifact_check.py`; J on interpretation]

**H rate by parent craft, all 666 tasks**

| Parent craft | H rate | Count |
|---|---|---|
| FC | 32.7% | 48/147 |
| DC | 3.8% | 9/237 |
| SC | 31.6% | 89/282 (15 of the 89 are Domain 7's normative H calls) |

**Like-for-like comparison.** Keeping only field-type tasks (field verbs, no desk verbs; n=70; a crude keyword filter):

| Parent craft | Field-type tasks coded H |
|---|---|
| FC | 46% (17/37) |
| DC | 6% (1/17) |
| SC | 6% (1/16) |

Examples under DC parents coded A:
- "Assess fish populations using netting, electrofishing, or sonar" (1.4.5 T1, A/Hi);
- "Install soil moisture, temperature, and weather sensors in remote field sites" (2.3.1 T1, A/Hi);
- "Measure or estimate soil carbon stocks" (1.8.2 T1, A/Hi).

Under FC parents, "Measure tree height, diameter, and age using field instruments" (1.3.2 T1) is H/Hi.

**High-tacit tasks.**

| Parent craft | High-tacit tasks coded H |
|---|---|
| FC | 48% (35/73) |
| DC | 11% (8/75) |
| SC | 67% (86/129) |

Tacit density predicts H only when the parent is FC or SC.

**Within FC, inconsistency.** "Collect water samples to test for pollutants, pH, turbidity…" (1.2.4 T1) is H/Hi. "Collect water samples and conduct field measurements (temperature, pH, dissolved oxygen, turbidity)" (4.1.3 T1) is A/Med. Both were coded session-direct in different domain sessions.

**Interpretation.** The pattern follows standing rule R1 ("FC Primary → watch for H; DC Primary → A expected") and the shared criteria between the FC and H definitions, as the audit suspected. The H/A split is also conceptually muddled for field work: most field tasks are both presence-required *and* augmented.

**Recommendation**
- Drop R1's expectation clause.
- Re-code exposure blind to parent craft.
- Split H into two separate fields:
  - `field_dependency` (presence required), a task attribute;
  - automation type A/Ac/V/S, plus an explicit "no deployed tool performs any part of the core task" value used sparingly.

With that split, I expect field tasks to show *high presence and moderate-to-high augmentation*. That is a truer picture than "Human-Essential". [S: confirm with a blind recode of about 60 field tasks by 3 or more raters in IO's pilot]

---

## Proposals

| ID | Proposal | Type | Why |
|---|---|---|---|
| **P-FC-01** | Adopt the v2 field craft definition and seven components (FC-a … FC-g) as L0 vocabulary | change | §1.1–1.2 |
| **P-FC-02** | Store craft as task-level 0/1/2 ordinal weights per craft, plus `field_dependency` and `formation_dependency`; compute competency and role blends; keep dominant craft as a derived display only; retire stored Craft Primary/Secondary (keep as v1 provenance) | change | §1.6; Q1 |
| **P-FC-03** | Replace v1's location-based irreducibility test with the three-part test (presence / physical consequence / ground-truth authority); retire "assign FC-secondary liberally" | change | §1.3 |
| **P-FC-04** | Add reproduction-regime attributes (mentorship dependence, cycle dependence, place-boundness, credential gate, currency decay; computed entry-path dependence) per `craft_profile_rubric.csv` | add | Q3 |
| **P-FC-05** | Consolidate D1/D4 duplicate field competencies (§6.2) and retire the domain-context craft rule | change/retire | §6.2 |
| **P-FC-06** | Move tool-bound content (4.1.5, 4.5.4, 2.3.2–2.3.4, 4.6.2, eDNA as method) to L4. Create durable FC-C14 (automated field systems), FC-C16 (clean and genetic sampling) and FC-C23 (field records with integrity) | change/add | §2.3 test; §6.2 |
| **P-FC-07** | Add the 31 candidate competencies. MVP priority: C01, C02, C03, C04, C06, C14, C16, C20, C24, C31 | add | §6.3 |
| **P-FC-08** | Treat ground-truth, validation and sensor-service work as designated, supervised entry learning roles, using FCA-GT and FCA-SENS anchors | add | §3.3 |
| **P-FC-09** | Co-design (with LC, FH, SL, TN) a multi-employer registered field technician apprenticeship spanning agencies, states, Tribes, corps, NGOs and consultancies | add | §3.3 |
| **P-FC-10** | Specify a portable, task-book-style field evidence record (Open Badges/CLR; LC, IA) so partner, corps and seasonal field work counts toward qualifications and hiring | add | §3.1, §3.3 |
| **P-FC-11** | Compute an entry-path health indicator per role, with driver attribution (fiscal, policy, automation), extending CA's pathway-level CLD | add | §3.2 |
| **P-FC-12** | Recommend field rotations for desk roles whose tasks are formation dependent, and analyst rotations for field technicians | add | §3.3 |
| **P-FC-13** | Publish formation-preserving automation guidance for adopters (blind re-ID samples, manual calibration checks, periodic manual surveys) | add | §3.3 |
| **P-FC-14** | Split field risk management (FC) from safety program management; add C18, C19, C27; certificates as credential-layer inputs | change/add | §4.3 |
| **P-FC-15** | Replace years-based levels with observable anchors for field craft using the eight design principles; pilot with existing QA programs (AIM, FIA, NARS, NWCG evaluators) under IO | change | §5 |
| **P-FC-16** | Correct v1 exposure:<br>• reclassify ignition subtasks (A, Ro/Cv, horizon 1);<br>• drop R1's expectation clause;<br>• recode blind to parent craft;<br>• split H into presence plus automation type | change | Q4; §2.2 |
| **P-FC-17** | Re-profile inspection, compliance and monitoring tasks in D6 (6.1.2 T1, 6.1.5 T1, 6.7.5 T1, 6.3.5 T1) with FC weights; add C04 and C17; CM to re-run family blends | change/add | §1.5 |
| **P-FC-18** | Indigenous and local knowledge recognition rules (§7): record roles and relationships, not content; community-controlled markers; community authority over assessment. TN decides | add | §7 |
| **P-FC-19** | Use place-boundness to separate portable field method from place-bound knowledge in mobility and transfer-friction metrics (CM) | add | Q3 |
| **P-FC-20** | Register dated change-signal events in L5: ASDA (Dec 2025), FCC Covered List (Dec 2025) and the 2026 proposal, Part 108 publication, OSHA heat rule, annual seasonal hiring announcements, USFS UAS annual reports | add | §2.2, §3.1 |
| **P-FC-21** | Require Delphi and validation panels to include active field practitioners (technicians, crew leads, inspectors) in proportion to the field workforce, not only senior or desk experts | change | Disagreements |
| **P-FC-22** | Run a verification pass on all `unverified` sources (FC-035–FC-065) before Phase 3 decisions rely on them | add | §0 |

---

## Disagreements and trade-offs

1. **With DC: who owns screen-based work that depends on field expertise?** This covers AI species verification (C03), ground-truth design (C02), sensor networks (v1 2.3.1, DC-primary) and drone processing.
   - My position: these are FC-weighted, or at minimum `formation_dependency = yes`.
   - DC may reasonably say that validating a model is data craft.
   - **Trade-off:** if DC owns them with no formation flag, curricula and hiring will drop field exposure for these roles, and systematic errors will appear only in novel conditions (v1 already warned of this, FC-025). If FC owns them outright, DC competencies for model evaluation lose content.
   - **My proposed resolution:** rate both crafts as defining where true, and let `formation_dependency` carry the formation requirement. That moves the argument from labels to attributes.
2. **With DC: tools layer versus durable for drones and sensors.** DC's mission is to separate durable competencies from tool fluency, and I agree platform and software skills are L4. I disagree that UAS operation is *only* tool fluency. Flying or supervising automated systems near crews, aircraft and wildlife in uncontrolled environments is a durable field capability (C14) [E: FC-002, FC-009]. Trade-off: more L1 competencies versus understating a real change in field work.
3. **With SC: inspection and working with people on the land.** I place compliance inspection (C04) and joint field work with landowners and permittees (C21) as FC-primary blends with SC secondary. SC may argue that authority and relationships are the irreducible parts. Trade-off: if SC owns them, the field evidence skills go unassessed. Weights can rate both crafts as defining.
4. **With v1 (and partly the audit's framing): Human-Essential.** I argue H is the wrong concept for most field tasks, which are presence-required *and* augmented (Q4). Trade-off: losing a simple, persuasive "protected" category in exchange for a more accurate two-field model.
5. **With IO: cost and reliability of field assessment.** Observed field assessment is costly and condition-dependent. Written or online skills tests are cheaper and more standardized (relevant to skills-based federal hiring, FH). Trade-off: validity versus cost. My mitigation is to reuse existing QA records as evidence (principle 8). The tolerance-based anchors also need program-specific thresholds, which complicates a generic level scale.
6. **With LM and FS: what is driving change.** For field work right now, fiscal and policy shocks outweigh AI and automation [E: FC-014, FC-015, FC-021]. Signals and foresight should attribute drivers separately. Otherwise automation narratives will absorb a contraction story, and the taxonomy will point to "reskilling for AI" where the problem is that there are no entry jobs to learn in.
7. **With LC: simulation and VR as substitutes.** Simulation is right for rare events. It does not replace graduated field exposure for perceptual and situated skills [J]. Trade-off: scalable learning versus fidelity.
8. **With CM: blends from v1 tags.** CM's family blends inherit v1's under-tagging of field work in policy and health families (FC-034). I'd ask CM to treat current FC weights for F8 and F13 as provisional until P-FC-17 is applied.
9. **With the v1 Structural Conditions report and the panel process.** That report warned that, under contraction, validation panels will over-represent codifiable craft practitioners (FC-031). I agree and propose P-FC-21. Trade-off: recruitment effort and representativeness versus speed.

---

## Issues outside my area that affect the vision

- **Drinking water and wastewater operators** (DB, SL) are a very large, state-certified field workforce that v1 omits entirely. Field craft definitions apply, but the content must come from that subsector.
- **Partner and contractor crews are invisible in federal qualification records** (FH, IA). As field work shifts to partners (FC-RS20), mobility and qualification portability depend on record access (P-FC-10).
- **Privacy in field data** (CP): camera traps and drones capture people; sensitive species and cultural site locations sit in field apps. These need security, privacy and Tribal data governance (TN) review.
- **Procurement and supply** (PS, AS): domestic drone and sensor supply, compliant-fleet costs and maintenance budgets decide adoption more than capability [E: FC-001].
- **Housing, pay and duty stations** (FH, SL): v1's Structural Conditions report ties fire workforce reproduction to pay and housing (FC-031). The same applies to technicians.
- **Monitoring obligations in plans exceed shrinking technician capacity** (LM, SC). Plan monitoring programs assume GS-5/7 technicians (FC-033). Unmet monitoring weakens adaptive management and legal defensibility.
- **Verification debt** (orchestrator): this report could not verify many standards because the shared search budget ran out. Phase 3 should not treat `unverified` rows as evidence.

---

## Open questions for the Chief Taxonomy Architect

1. **DP-5.** Will you adopt `formation_dependency` as a separate task attribute (my recommendation), or should formation be expressed only through higher FC weights?
2. **DP-5.** Will the first IO pilot use the 3-level ordinal as the primary scale? I recommend it.
3. **DP-3 / DP-4.** Do proficiency anchors attach to L1 competencies, to L2 tasks, or both? Field anchors are most natural at the competency level with task-coded conditions.
4. **DP-2.** Which field competencies are core, and which go to subsector modules? I suggest core: C01, C02, C03, C14, C18, C20, C23, C24, C27, C31. Modules: wetlands, UVM, air stations, marine, rangeland, contaminated sites.
5. Credentials (Part 107, red card, HAZWOPER, sawyer, MOCC, ISA, applicator licences): L4 tools and standards, L6 crosswalks, or a distinct credential entity? They need links to tasks and should never stand in for proficiency.
6. Will EMST compute entry-path health (P-FC-11), and from what data (role profiles, hiring announcements, qualification-record aggregates)?
7. How should mobility metrics treat place-bound knowledge (P-FC-19)? Treating it as a transfer cost is honest. Treating it as non-transferable would understate mobility within regions.
8. Will you schedule a verification pass (P-FC-22) before Phase 3 decisions rely on the unverified standards?

---

## Files in this folder

| File | Contents |
|---|---|
| `report.md` | This report |
| `sources.csv` | 65 sources: 24 web sources read this session, 10 v1/team/internal, 3 blocked, 28 known but unverified |
| `candidate_competencies.csv` | 31 candidate competencies (FC-C01–C31) |
| `role_signals.csv` | 21 role signals (FC-RS01–RS21) |
| `v1_assessment.csv` | 71 verdicts: 49 FC-primary competencies plus 22 framework and boundary elements |
| `ecosystem.csv` | 34 entities (standards, programs, credentials, policies, tools, datasets) |
| `fieldcraft_proficiency_anchors.csv` | 48 observable anchors across 12 competencies |
| `craft_profile_rubric.csv` | Task-level craft weight rubric (0/1/2), field and formation dependency, reproduction-regime attributes |
| `field_tech_change_matrix.csv` | 18 field technologies: automated, augmented, new tasks, human core, change level, adoption, barriers |
| `scripts/h_artifact_check.py` | Reproduces the Q4 test from `data/v1_baseline/` |
| `scripts/lmp_monitoring_staffing.py` | Extracts specialist and technician staffing from OpenLMP monitoring tables |
| `scripts/lmp_field_requirements.py` | Lower-bound count of plan standards and guidelines with explicit field-survey, verification or inspection language: 200 of 25,894 normative components (0.8%) in 52 of 116 plans; regex-based and noisy |
| `scripts/lmp_monitoring_text_scan.py` | Exploratory keyword scan of plan monitoring components (method terms are rare in fragmentary text) |
| `scripts/build_*.py` | Regenerate each CSV in this folder from its row data, with vocabulary checks |
