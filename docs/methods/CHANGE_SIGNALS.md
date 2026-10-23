# Change signals, instruments and external exposure evidence: WP-10 method note

- **Owner:** LM (A9), with FS · **WP:** WP-10 (change-signal and exposure seeding) · **Date:** 2026-10-23 · **Status:** draft for CA integration
- **Decision basis:** ADR-0008 (exposure and change model), ADR-0015 (lifecycle and watch), ADR-0019 (linker quality), ADR-0028 (change-signal layer), SPEC §5.12–§5.16, §11, §14, §16; `vocab/exposure_instrument_v2.yaml`, `vocab/driver_mechanisms.yaml`, `vocab/change_types.yaml`, `vocab/scenarios.yaml`, `vocab/evidence_labels.yaml`
- **Builder:** `docs/methods/scripts/build_wp10.py` (deterministic; regenerates every record and the counts)
- **Counts:** generated in `docs/methods/generated/wp10_counts.json`. This note types no record counts.
- **Licence:** CC0-1.0

Evidence labels follow the team standard. **[E]** means a cited source read, with the ID resolving in a `sources.csv` or V-pass key-facts file. **[J]** means LM/FS judgment, with its basis stated. **[S]** means speculation, with what would settle it.

---

## 1. What WP-10 seeds, and where it lives

| Record type | Location (AUTHORING_GUIDE §2) | Source of content |
|---|---|---|
| `Instrument` (L5 registry) | `data/v2/instruments/instruments.jsonl` | SC's 34 instruments (`docs/research/statecraft/policy_landscape_2026.csv`), corrected by V2/V4. Also the new instruments WP-10 names and verified FH, FC, SL and fiscal instruments. Disposition of every SC row: `docs/methods/generated/sc_instrument_disposition.csv` |
| `DriverEvent` | `data/v2/events/<yyyy>.jsonl` | Dated events behind each instrument; `currentStatus` is computed from them and never stored |
| `ChangeSignal` | `data/v2/signals/2026/<source>.jsonl` | Standing demand signals (OpenLMP, OMB AI inventory, OPM-data headcount, a postings board), BLS 2025–35 projections, review-tooling deployment and capability, policy watch, FS weak signals that feed watch items, and scenario-signpost readings |
| `WatchItem` | `data/v2/core/watch-items/seed-watch-<cand>.yaml` | DC-CAND-17, PS-C19 and FS-C16. TN-C13 stays held and is not authored (§9) |
| `ExposureAssessment` (external index) | **staged:** `docs/methods/staging/assessments-external/` | Eloundou et al. and Microsoft "Working with AI" occupation aggregates, attached to MVP roles. Staged because the schema accepts only task-grain assessments (CR-LM-002) |
| v1 exposure and tag values | `data/v2/assessments/emst-v1-*/` (DE, WP-02) | Referenced, not duplicated (§8) |
| Evidence-rule CI test | `docs/methods/ci/` | Reference implementation, synthetic cases and a regression on the real seed (§4) |
| Claims register | `docs/methods/claims_register.csv` | WP-15 seed: every date-sensitive fact the package is likely to use (§12) |

The WP-10 brief named the write lane as `data/v2/signals/`, `data/v2/assessments/external/` and `docs/methods/`. DE's validator places `Instrument`, `DriverEvent` and `WatchItem` elsewhere and raises `E-LOCATION` under `signals/`. The seed follows the authoring guide, as the brief instructs when DE's tools exist. CR-LM-003 asks the CA to ratify that lane. With this layout `scripts/validate_v2.py` reports no errors or warnings on any WP-10 record.

## 2. Record design

### 2.1 Common to every L5 record

- `status: draft`, a `seed:` key, `layer: L5` and `module: core`.
- `provenance.method: llm-assisted` (`import` for transcribed external values), with `toolVersion`, `promptVersion` and `reviewStatus: unreviewed`.
- Agents are recorded as `emstagent:A9-LM@claude-opus-5-5` and `emstagent:wp10-builder@…`. No person is named anywhere (ADR-0012).
- **Evidence labels.** Every `ChangeSignal` carries `evidenceLabel: S` until a human reviews it (SPEC §5.14; build plan §1.2). Its `provenance.evidenceLabel` is `E` because the measured value comes from a source that was read. A `DriverEvent` is labelled `E` when its date and status rest on a verified fact, or `J` when only the day of signing rests on general knowledge (e.g. FAST-41, the FRA 2023, the EXPLORE Act). The direction tag on an event (`expands`/`contracts`/`reshapes`) is an agent judgment and is unreviewed.
- **Sources.** `sources[]` cite IDs the validator resolves today: V-pass fact IDs (`V1-xx` … `V4-xx`) or role `sources.csv` rows. The exact page read is in `docs/methods/sources.csv` (`LM-101`…`LM-153`). The mapping is `docs/methods/scripts/wp10_common.py#RESOLVE`. CR-LM-001 §9 asks DE to load `docs/methods/sources.csv` directly.

### 2.2 ChangeSignal fields

All SPEC §5.14 fields are filled. Choices worth knowing:

- **Targets.** Work functions, modes and sector actors are L0 terms (`targetType: VocabularyTerm`, e.g. `vocab:work_functions#WF-MONITOR`).
  - Roles are the planned MVP role keys, `mvp-role:R14-forester` (an ExternalRef to `docs/decisions/mvp_role_set.csv`). No reference dangles before WP-08 authors RoleProfile seeds; CR-LM-001 §10 covers the re-point.
  - Instruments are `seed:ins/…`. Signpost readings target `vocab:scenarios#SP-NN`, using the notations proposed in CR-LM-001 §8.
  - Agency headcount targets `vocab:sector_actors#federal`, with the agency named in the label, until an organization target exists (CR-LM-001 §4).
- **Occupation-level series** (BLS projections, external indices) are attached to **each MVP role that lists the SOC code**, with a two-step `crosswalkPath`: native SOC, then role → SOC from `mvp_role_set.csv` until X3 exists. `crosswalkMinMatchType` is `skos:closeMatch` for single-SOC roles without a caveat and `skos:broadMatch` otherwise. Under ADR-0028 a broad match can raise a watch but never move an indicator. Occupations with index values but no MVP role are listed in `docs/methods/staging/assessments-external/unattached_occupations.txt`.
- **Reliability A–D** (`vocab/change_types.yaml#signal_reliability`):
  - **A:** primary official data read directly, e.g. the OMB inventory, BLS, NIFC, the Federal Register.
  - **B:** credible secondary with a traceable primary basis, e.g. PPS or ICN analyses of OPM data, OpenLMP extractions, law-firm summaries of rules.
  - **C:** a single board, a single listing or trade press.
  - **D:** unverified.
- **Driver tags.** Every signal declares at least one. Headcount, posting and appropriations signals are tagged `fiscal`, `policy-reform` and/or `workforce-capacity`, never `AI` unless a source attributes the change to AI. BLS projections carry `other`, because BLS does not attribute occupation projections to drivers in the sources read.
- **Novelty, corroboration and impact** follow FS's coding (`horizon_scanning_protocol.md` §6). `priorityScore` is computed, never stored.
- **Interim encodings.** Signal family, independence key, impact, registered deployment, signposts informed, baseline and component-weighted sensitivity are carried as `notation` entries with `EMST-` schemes. The schema does not type them yet (CR-LM-001).
- **No personal data.** `personalData: false` on every signal. Only aggregates are stored: no posting text, names, contacts or person-level rows.
- **Tribal quarantine.** Signals that characterize Tribal programmes carry `careFlag`, `tribalPrograms`, `indigenousDataFlag`, `approvalStatus: pending-tribal-review` and `sensitivity: restricted-governed`, and are excluded from release.

### 2.3 Instruments and driver events

- **`instrumentType`** follows SPEC §5.16. Bills are `statute` with only `introduced`/`passed-chamber` events, so their computed status cannot read as law. Department-level Secretarial Orders are typed `executive-order`; CR-LM-001 §7 proposes `agency-order`.
- **`jurisdiction`** uses ISO-style codes: `US` (federal), `US-CA`, `US-CO`, `US-TX`, `US-FL`, `EU`.
- **`mechanisms`** use the L0 driver mechanisms DM-01…DM-19. Where SC's `driver_mechanisms.csv` named the instrument, its mapping is kept; otherwise the mapping is LM's [J]. Example: the OFCCP and OPM selection-procedure rules map to DM-16 workforce-capacity, because no selection-procedure mechanism exists. That gap is flagged for IO.
- **`statusAfter`** uses the controlled set listed in CR-LM-001 §5.
- **Scheduled future events** are recorded with their published date and a `reviewBy` the day after. Examples: OFCCP's rescission effective 2026-10-26; the Forest Service objection rule effective 2026-11-12.
- **Pre-publication actions** have no event type. The Section 106 rewrite at OIRA and the FAA Part 108 final rule at OIRA are therefore recorded as policy-family watch signals targeting the instrument (CR-LM-001 §6).
- **`reviewBy`** is 2026-12-15 for moving or contested facts (before the rc.1 build), 2027-04-23 for settled recent events and 2027-10-23 for historic baselines. SC's quarterly refresh (P-SC-14) owns the registry from here.

### 2.4 Corrections applied to SC's registry

The V2 and V4 corrections are binding.

- **CEQ regulations.** Removal final, effective 2026-01-08.
- **DOI.** The "DOI NEPA Handbook", not "516 DM 1".
- **Seven County.** "8–0 judgment; 5-justice majority opinion", not 5–3.
- **SPEED Act.** Passed the House 221–196; pending in Senate EPW.
- **ESA "harm" rescission.** Final 2026-07-14, effective **2026-09-14**, litigated.
- **GHG endangerment rescission.** Effective 2026-04-20; D.C. Cir. Nos. 26-1037 and 26-1061, replacing the unconfirmed case names.
- **WOTUS.** Still proposed; supplemental proposal of 2026-09-09.
- **CEQ data standard.** "v1.2".
- **Section 106.** NPRM at OIRA.
- **California SB 253/261.** OAL approval 2026-10-12; first reports due 2026-11-10; SB 261 enjoined.
- **EU Omnibus I.** In force 2026-03-18.
- **CEQA.** AB 130/SB 131, now verified.
- **New instruments:**
  - Colorado SB 26-189, replacing SB 24-205, which never took effect.
  - OFCCP rescission of 41 CFR 60-3 (with the other EO 11246 parts), effective 2026-10-26.
  - OPM's interim final rule removing UGESP references (2026-07-31).

SC rows that were not re-verified in a V pass keep the SC source, say "not re-verified" in `editorialNote` and carry the pending re-check date: DOT and EPA NEPA procedures, the ESA 4(d)/4(b)(2) rules, Florida 404, the USFS objection rule and Roadless proposal, the SEC climate rules and the ePermit Act.

- **Split:** SC's grouped rows are split one instrument per agency or regime, so status computes per instrument (PI-NEPA-06, PI-TECH-01, PI-DISC-01, PI-FOR-02).
- **Reclassified:** PI-TECH-04 (PermitAI) is a set of tools, so it is L4 under T-7. It is recorded as a deployment signal and handed to DC.
- **Not seeded:** PI-SEPA-02 is an unverified placeholder; SL/DB will supply per-state instruments.
- **Held:** PI-TRIBE-01 and PI-TRIBE-02.

## 3. Signal families and independence

The ADR-0028 families are capability, observed use, deployment, postings or PDs, headcount, plan requirements and worker report. The seed adds three labels:

- **policy:** counts toward role-change indicators (ADR-0028 §3).
- **projection:** official projections; context only, never counts.
- **workload:** demand pressure such as fire-season acres; context only, never counts.

**Finding: BLS's AI exposure categories are not an independent family** [E: LM-151 → V4-07]. BLS builds "theoretical" exposure from the median percentile of Felten–Raj–Seamans, Eloundou et al. and Eisfeldt et al. It builds "observed" exposure from Anthropic (Massenkoff and McCrory) and Microsoft (Tomlinson et al.) usage data, then clusters occupations into four relative categories. BLS says the categories are not forecasts and do not separate automation from augmentation.

So a BLS "observed" category cannot corroborate AEI or Microsoft usage, and BLS "theoretical" adds nothing independent of Eloundou. The rule therefore checks **upstream providers**, not just family labels. The provider table is `docs/methods/ci/evidence_rule.py#PROVIDERS`; CR-LM-001 §2 proposes moving it to `vocab/`.

**Disclosure.** EMST is built with an Anthropic model and treats Anthropic's usage data as one family among several. No indicator may rest on it alone (ADR-0008 §4) [J].

## 4. The evidence rule as a CI test

`docs/methods/ci/evidence_rule.py` implements ADR-0028 §2. A signal set moves an indicator `(target, direction, driver)` only if ER-1 to ER-5 all hold; otherwise the outcome is `watch`.

- **ER-0 (exclusions before counting).** `personalData ≠ false` invalidates the evaluation. Quarantined signals (Tribal flags), v1-analyst assessments (prior evidence only), retired signals and other directions are excluded.
- **ER-1 (independence).** Two counting families must be present, with disjoint upstream providers. Policy-family signals do not count toward skill-change indicators. This is LM's conservative reading of "cannot alone move a skill-change indicator" [J; CA to confirm].
- **ER-2 (persistence).** Either two distinct periods of the same measure, or a registered deployment.
- **ER-3 (match quality).** Every counted signal needs weakest match `skos:exactMatch` or `skos:closeMatch`.
- **ER-4 (driver).** Every counted signal must carry the indicator's driver, so a fiscal headcount decline cannot pair with an AI capability signal to "show" automation. External AI-exposure indices count as AI-driven by construction.
- **ER-5 (named human review).** Review status must be `reviewed`, `validated` or `gold`, by a `pid:` or `panel:` reviewer. Software agents do not qualify.

`evidence_rule_cases.yaml` holds labelled **synthetic** fixtures, one or more per clause, covering:

- two families agreeing;
- two vendors in one family;
- one vendor across two families;
- BLS observed paired with Microsoft;
- v1 prior evidence;
- a broad match;
- one period without a deployment, and one period plus a registered deployment;
- a fiscal shock against an AI indicator;
- agent-only review;
- disagreeing directions;
- a Tribal flag;
- personal data;
- the policy family on a skill-change indicator;
- projections;
- the interim notation encoding.

`test_evidence_rule.py` also runs the rule over the real seed. It asserts that **no seeded signal moves any indicator**, which holds because none has had human review. It also checks that every seeded signal has a recognised family, driver tags, reliability, source release and `personalData: false`, and that every Tribal-flagged signal is quarantined. Run it with `python3 -m pytest -q docs/methods/ci/`. DE should port it into `tests/` and the build's indicator rule (CR-LM-001 §3).

## 5. Standing demand signals

### 5.1 Plan requirements (OpenLMP)

**Method.** `docs/methods/scripts/wp10_lmp.py` reads OpenLMP 0.1.0 (catalog 2026-10-21, CC0) read-only. It reuses the keyword and coordination-tag definitions from LM's Phase 2 script, so the two passes are comparable.

Following ADR-0028 §4, the **headline weights each plan equally**: the share or rate is computed within each plan, then averaged across plans, with a 95% CI of mean ± 1.96 SE. The component-weighted value is kept as the sensitivity check.

This is a **cross-era comparison** of plans written under the 1982 and 2012 Planning Rules. It is not a time series of the same plans. About 95% of components come from USFS plans, all in western states [E: LM-017].

**Results** [E: LM-144 derivation from LM-017]:

| Measure (per 1,000 components unless a share) | 1982-rule plans, plan-equal | 2012-rule plans, plan-equal | Component-weighted 1982 → 2012 | Reading |
|---|---|---|---|---|
| Monitoring components, share | 0.027 (CI 0.007–0.047) | 0.307 (0.194–0.420) | 0.018 → 0.222 | Robust: monitoring and evaluation workload created by the 2012 rule |
| Climate-change mentions | 2.3 | 20.0 | 1.8 → 16.9 | Robust |
| Data or model mentions | 14.1 | 80.6 | 15.0 → 70.0 | Robust |
| Carbon mentions | 0.14 | 1.44 | 0.29 → 4.08 | Direction robust; small base |
| At-risk species / SCC mentions | 1.1 | 5.6 | 0.3 → 11.7 | Weak (CIs touch) |
| Remote sensing / LiDAR / drone mentions | 0.38 | 1.33 | 0.42 → 2.62 | Weak; plans name outcomes, not methods |
| Partnership touchpoints | 11.9 | 24.9 (CIs overlap) | 10.0 → 31.4 | Grow, low confidence |
| Cross-boundary touchpoints | 4.7 | 5.0 | 4.5 → 13.8 | **Flat under plan-equal weighting** |
| State-agency touchpoints | 6.2 | 4.3 | 4.6 → 10.1 | **Falls under plan-equal weighting** |

**Correction to LM Phase 2** [E/J]. "Coordination intensity about tripled" was a component-weighted result. It is driven partly by a few large 2012-rule plans; under the ADR's plan-equal headline only partnership touchpoints rise, and weakly. The monitoring finding strengthens under plan-equal weighting.

Tribal touchpoints were computed and are **quarantined** (careFlag); TN decides whether and how they are shown.

**Limits.**
- Mentions measure what plans name, not obligations.
- Theme tags cover about 10% of components.
- Plans are a poor signal for agreements such as GNA and shared stewardship, which work through agreements rather than plans.
- Extending the series to BLM RMPs, state wildlife action plans, TMDLs, NPDES permits and state forest plans remains P-LM-08.

### 5.2 Federal AI use-case inventory (OMB, 2025 cycle)

**Method.** LM's Phase 2 extract covers nine environmental bureaus, keyword-classified into function families. "Deployed" means `development_stage = deployed` only; OMB's README pools deployed and piloted, and NOAA reported no stages [E: LM-027; V4-15].

Signals were recorded per function family:

- species and wildlife detection;
- remote sensing;
- water;
- fire;
- forecasting;
- bureau-built generative AI;
- inspection and compliance;
- NEPA and permitting;
- public comment.

One further signal covers commercial generative-AI drafting tools licensed at 10,000+ users in EPA, DOI and USDA.

**Reading** [E/J]:
- The deployed AI is mostly classical ML and computer vision for science pipelines.
- Generic drafting compression is available at tool-access level across the main environmental departments.
- **None of the five NEPA/permitting use cases is deployed.** This is a counter-signal to automation claims about review work; registration and licences are not use.

**Next reading:** the 2026 inventory, around the turn of the year.

### 5.3 Headcount (OPM data)

**Interim seed.** OPM Federal Workforce Data (data.opm.gov) replaced FedScope in January 2026 with monthly data [E: V1-16]. It could not be read this session, so the seed uses verified secondary analyses of OPM data [E: V1-01…V1-04]:

- federal civilian workforce down 12%, September 2024 to January 2026;
- USFS and NPS each down more than a quarter;
- park rangers down 34.1%;
- under-30 share down from 8.9% to 7.9%;
- EPA at 12,849;
- no USFS non-fire seasonal hiring in 2025.

Every headcount signal is tagged fiscal, policy-reform or workforce-capacity. **None is tagged AI.**

**Standing FWD pull (for DE/IA; monthly data, quarterly summary).**
- Units: series × agency × grade band.
- Series: 0401, 0404, 0408, 0454, 0455, 0456, 0457, 0458, 0460, 0462, 0482, 0486, 0819, 0028, 1301, 1315, 1340, plus the series in the FH register.
- Measures: headcount, accessions, separations, under-30 share, trainee and entry-grade (GS-5/7) share.
- Base declared: permanent vs seasonal, fire vs non-fire.
- Mirror the extracts with provenance (ADR-0028 §4 data continuity).

### 5.4 Official projections (BLS 2025–35) and BLS AI exposure categories

**Projections.** The 2025–35 projections (released 2026-08-27) were read from Table 1.2 and from OOH pages, where Table 1.2 rows were unreadable in the fetch tool [E: LM-145…LM-150 → V4-07]. Each value is attached to the MVP roles that list the SOC.

Selected results against an all-occupation average of +3.5%:

| Direction | Occupation | 2025–35 change |
|---|---|---|
| Faster | data scientists | +34.6% |
| Faster | natural sciences managers | +8.2% |
| Faster | environmental science and protection technicians | +7% |
| Faster | environmental engineers | +6.3% |
| Faster | environmental scientists | +6% |
| Faster | conservation scientists | +5.3% |
| About average | compliance officers | +3.8% |
| About average | zoologists and wildlife biologists | +3.6% |
| About average | firefighters (wildland not counted separately) | +4% |
| Slower | foresters | +2.2% |
| Decline | forest and conservation workers | −2% |
| Decline | water and wastewater operators | −6% |

Projections are context: the `projection` family never counts toward the evidence rule. They replace LM Phase 2's 2022–32 figures, which are superseded.

**Not yet read:** hydrologists, planners, forest and conservation technicians, hydrologic technicians, OHS specialists and fish and game wardens.

**AI exposure categories.** Per-occupation values exist only in an XLSX file (`bls.gov/emp/ind-occ-matrix/ai-exposure-categories.xlsx`). Neither the fetch tool nor the shell proxy could retrieve it. **Ingestion is pending**; DE should mirror the file. When ingested:
- "theoretical" values are coded as family capability, lineage `bls-ai-exposure-theoretical`;
- "observed" values are coded as family observed-use, lineage `bls-ai-exposure-observed`;
- both are attached to roles at occupation grain (CR-LM-002).

### 5.5 October 2026 postings baseline (USAJOBS and state boards): **not taken**

Fetches of USAJOBS search (LM-152) and Washington State's NEOGOV board (LM-153) were declined in this session, so **no posting baseline exists yet**. This is a gap, not a finding. The only postings evidence in the seed is one board's 2025 year-over-year change (Conservation Job Board [E: V1-14]). The snapshot specification for IA/DE follows.

- **Federal.**
  - Pull open announcements via the USAJOBS Search API (key required) for the series in §5.3 on a fixed date in October 2026, with a second pull in January 2027.
  - Keep only derived aggregates by series × grade band × agency × state × appointment type (permanent, term, seasonal, student/Pathways):
    - announcement counts;
    - counts of duties-text and qualifications-text hashes, for quarterly diffs;
    - counts of tool and AI mentions from IA's extractor, with `linkerQuality`.
  - Store no announcement text, no contacts and no names (ADR-0012).
  - Federal posting **volume** is a **policy** signal (EO 14356 staffing plans, the Merit Hiring Plan), not labour demand (ADR-0028 §4). Duties text is the content signal.
- **State.** Use one or two of the X5 pilot states (PA, TX, WA). Apply the same aggregates by class code and agency for the environmental class families in SL's sample, plus one county environmental health department and one municipal utility if their boards allow automated reading.
- **Private and NGO boards.** These are licensed or one-board sources. Label the scope, as for the Conservation Job Board.

## 6. External-index assessments

**Grain.** Each record attaches an index's published occupation value to the MVP roles that list the code, never to a single EMST task (XR-06). The LM pilot found single external labels disagreed in 13 of 21 two-match cases [E: LM pilot]. Task-level joins wait for X2.

**Ingested (staged):**
- **Eloundou et al.** Capability family: human and GPT-4 β, percentiles and the E0/E1/E2 distribution of the occupation's O*NET tasks.
- **Microsoft "Working with AI" v6.** Observed-use family from one platform's usage: applicability and the non-physical variant [E: LM-008, LM-009, V4-02].

**Not ingested, and why:**
- **AEI usage shares and `labor_market_impacts`.** The occupation files were not retrieved; Hugging Face was unreachable in Phase 2 and was not attempted again.
- **BLS AI categories.** XLSX not retrievable (§5.4), and they are a composite of the same families.
- **AIOE, LM-AIOE, Webb, ILO WP 140 and WEF.** Context only (ADR-0008 §4).
- **Canaries.** Benchmark only: the ~19% young-worker gap is descriptive, works through reduced hiring and under-covers government [E: V4-03].
- **OMB deployment stage.** Recorded as deployment signals on functions (§5.2), not as assessments on tasks.

**Language rule** (binding on every text) [E: LM-071 correction]. AEI's "77% of API transcripts show automation patterns" means directive plus feedback-loop collaboration in API traffic. It is not job automation and not task automation, and it must never be described that way. Usage data under-sample government work; theoretical exposure overstates environmental field work. Both are shown, as components.

## 7. What the seed says about how environmental jobs are changing

Each statement below is a watch-status reading, not an indicator movement. Nothing in the seed has had human review.

1. **[E] The 2025–26 contraction of the public environmental workforce is fiscal and policy-driven, not AI.** USFS and NPS each lost more than a quarter of staff. Park rangers fell 34%. EPA is at 12,849. The federal under-30 share fell to 7.9%. USFS hired no non-fire seasonals in 2025. Conservation internship postings fell 44% on one board. The entry rung is thinning through hiring policy and budgets. That is a career-ladder risk with a non-AI driver attribution (ADR-0008 §6).
2. **[E] AI in federal environmental agencies is mostly science-pipeline ML plus generic drafting tools available at scale; environmental review is not automated.** The deployed clusters are species detection, remote sensing, water and fire. Drafting assistants are licensed to tens of thousands of users. No NEPA or permitting AI is registered as deployed, and the review-AI services offered to agencies (PermitAI) are availability, not registered deployment. Desk documentation is where compression is available now. Specialist substitution is not observed.
3. **[E] Plans written under the 2012 rule demand monitoring and evaluation, climate analysis and data or models far more than older plans**, robust to weighting. The claimed tripling of coordination is mostly a weighting artifact. The durable demand is for indicator design, evaluation and reporting, not for particular field methods.
4. **[E] Official projections for 2025–35** show analytical and technician occupations growing about as fast as or faster than average (environmental scientists +6%, technicians +7%, data scientists +35%). Foresters are slow (+2.2%). Forest and conservation workers (−2%) and water and wastewater operators (−6%) decline. Projections are context, not evidence of skill change.
5. **[E] Policy instruments are reshaping review and authorization work faster than technology.**
   - CEQ rules removed; agency-specific procedures in force.
   - Seven County deference in force; SPEED Act pending.
   - ESA "harm" rescission in force but litigated.
   - Section 106 rewrite at OIRA, so s.106 and ESA consultation become the critical path when NEPA accelerates.
   - California's SB 253 reports due 2026-11-10.
   - Selection-procedure law shifting: OFCCP rescission 2026-10-26; OPM's UGESP-reference removal; Colorado SB 26-189 from 2027-01-01. EMST's selection-adjacent kits must rest on job analysis, never on "UGESP compliance".
6. **[S] Agentic AI supervision is forming but unevidenced in environmental work** (DC-CAND-17 watch). Signals: a drafting-agent benchmark built on 19 agencies' documents; only administrative agentic deployments in USDA, DOI and EPA; and a marketplace recruiting agency veterans to build agent training environments. It would be confirmed by environmental agentic use cases reaching deployed stage in the 2026 inventory, or by posting duties naming agent supervision.

## 8. v1 prior evidence

DE's WP-02 migrated every v1 exposure and tag value as `raterType: v1-analyst`, `raterId: v1-analyst-01`, `confidence: low`, with misalignment flags (`data/v2/assessments/emst-v1-task13/`, `emst-v1-cld/`, `emst-v1-reform/` and the others). WP-10 references these files and does not duplicate them.

- They are **prior evidence only**: never shown as v2 values, never aggregated into public numbers and never counted by the evidence rule (ER-0; test case C05).
- v1's six reform flags (DE's `emst-v1-reform`) are the frozen historical seed the instrument registry replaces. Their mechanism mapping is in `vocab/driver_mechanisms.yaml#v1_flag_seed_events`.

## 9. Watch items

| Watch item | Hypothesized entity | Signals | Counter-signal (recorded in `scopeNote`) |
|---|---|---|---|
| `seed:watch-DC-CAND-17` | Supervise agentic AI workflows in environmental analysis | Benchmark (capability), inventory agentic cases (deployment), marketplace recruiting (postings) | No environmental agentic deployment in the 2026 inventory and no posting duties naming agent supervision, or absorption by AI-output validation (DC-CAND-01/-13) |
| `seed:watch-PS-C19` | Price and disclose AI-augmented environmental services | Consulting AI comment tools (deployment), M-26-04 LLM contract terms (policy) | No change in hour-based billing or disclosure clauses through the 2027 review |
| `seed:watch-FS-C16` | Translate climate-risk data into navigable adaptation options for communities | Disaster-cost dataset discontinued then revived by an NGO (policy), IRA rescissions (policy) | No state or local postings naming the function in the baseline or the next two diffs; rewritten v1 1.5.3 covers it |

All three are `outcome: open`, with review by 2027-10-23; they lapse without new evidence (ADR-0015).

- **Promotion to `proposed`** requires at least three independent signals of at least two types from at least two sector actors, or a mandate with an effective date. DC-CAND-17 is closest.
- **TN-C13** is held. It is listed in `data/v2/governance/tribal_hold.yaml`, and no record or signal is authored for it.

## 10. Scenario signposts

Readings target the proposed signpost notations SP-01…SP-12, assigned in the order of `vocab/scenarios.yaml`. Each records `pointsToward` as a draft for FS's quarterly triage.

**Read:**
- SP-01: under-30 share; points toward thin-fragmented capacity.
- SP-02: FY2026 appropriations at 1.59 × the request; a stabilizer.
- SP-03: conservation entry postings.
- SP-05: high-impact environmental AI uses (DOI 0, USDA 4, EPA 2).
- SP-08: FireSat operational.
- SP-09: Part 108 still at OIRA.
- SP-10: 2026 acres at 145% of the 10-year average.
- SP-11: a discontinued disaster-cost dataset.

**Not read** (owner in brackets):
- SP-04, appellate decisions on AI-assisted records [FS/SC; monthly docket scan]. No systematic search was run, so no zero is recorded.
- SP-06, AI-in-review procurements [PS/IA; SAM.gov].
- SP-07, contract obligations vs FTE [FS; USAspending].
- SP-12, Tribal co-stewardship agreements [only via the Tribal Council].

## 11. Limits

- No posting baseline: USAJOBS and the state board were blocked (§5.5). No OPM FWD series pull. BLS AI-category XLSX not retrieved. AEI occupation files not ingested. Headcount relies on verified secondary analyses of OPM data.
- External assessments are staged, not in the validated tree (CR-LM-002). Role targets are planned keys, not RoleProfile records (CR-LM-001 §10).
- The plan-requirement series is USFS-western and cross-era. Mentions are not obligations.
- Several SC registry rows are not re-verified (§2.4). FS weak signals were recoded only where watch items or signposts cite them; FS owns the full register.
- Every signal, tag, direction, reliability grade and driver attribution is unreviewed agent output (`evidenceLabel: S`). No value here is SME agreement, Delphi retention or job-analysis confirmation.
- Environmental-sector evidence on AI *outcomes* remains thin. No study has an environmental cut, and none of the seeded signals is causal.

## 12. Claims register (WP-15 seed)

`docs/methods/claims_register.csv` has these columns:
- `claim_id`, `topic`
- `claim` (safe wording)
- `do_not_say` (the common wrong form)
- `source_ids`, `verification_id`, `verified_on`
- `status` (verified, corrected, verified-partial, unverified, derived, held)
- `owner` (role code)
- `recheck_by`
- `used_in`, `note`

Moving facts carry 2026-12-15 so they are re-checked before the rc.1 build. Settled facts carry 2027-02-15, before the rc.1 release. Scheduled facts carry the day after their date, e.g. OFCCP 2026-10-27. Annual series carry their next release window. WP-15 adds every claim used in WP-08 kits, WP-12 views, WP-13 and WP-14 as those are drafted. Zero unverified claims may remain in released artifacts.

## 13. Reproduce

```bash
python3 docs/methods/scripts/build_wp10.py          # regenerate all WP-10 records + generated counts
python3 scripts/validate_v2.py                      # DE validator: WP-10 records report no issues
python3 -m pytest -q docs/methods/ci/               # evidence-rule cases + seed regression
python3 docs/methods/scripts/build_wp10.py --promote-external   # only after CR-LM-002 is accepted
```

**Change requests:**
- CR-LM-001: evidence-rule fields and L5 vocabulary gaps.
- CR-LM-002: occupation-to-role grain for external-index assessments.
- CR-LM-003: WP-10 lane versus the guide layout.
