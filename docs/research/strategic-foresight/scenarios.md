# EMST v2 Workforce Scenarios, 2026–2035

**Role:** Futurist / Strategic Foresight Lead (FS) · **Date:** 2026-10-23 · **Status:** Phase 2 research draft for the Chief Taxonomy Architect (CA)

**Companion files:** `drivers.csv` (D-xxx), `weak_signals.csv` (WS-xx), `role_signals.csv` (FS-RS-xx), `candidate_competencies.csv` (FS-C-xx), `scenario_stress_test.py` and `scenario_stress_test_v1.csv`, `sources.csv` (FS-xxx).

**Labels:** **[E]** evidence I read (source IDs given) · **[J]** my professional judgment (basis stated) · **[S]** speculation (with what would confirm or refute it).

Scenarios are not forecasts. They are a small set of plausible, internally consistent futures that let us test whether the taxonomy and the workforce strategies built on it hold up across what the next decade could become. A scenario set is good if each scenario is uncomfortable for somebody, if all four are plausible today, and if each has observable early indicators. I have tried to meet all three tests.

---

## 1. Method choices: which method answers which question, and why

| Question | Method used | Why this method, not another |
|---|---|---|
| What forces will shape environmental work through 2040? | **STEEP+V driver analysis** (38 drivers, each rated for direction and uncertainty) | Forces cut across technology, politics, climate, markets and values. A STEEP+V frame makes sure that values (legitimacy of AI, sovereignty, speed versus precaution) are not left out, as they usually are in workforce studies. [J] |
| What is already visible at the edge? | **Weak-signal scanning** (44 dated signals) | Postings and occupational statistics lag 2–5 years. Pilots, procurement, first-of-kind roles, court decisions and credentials appear earlier. [J; consistent with FS-032 on horizon scanning] |
| Which futures should the taxonomy be tested against? | **2×2 scenario matrix (intuitive-logics / "Shell" school)** on the two most impactful and most uncertain driver clusters | Workforce planners need a few memorable contrasting worlds more than probabilistic precision. Two axes keep the set small enough to use in a 2–3 hour session. Climate and other predetermined elements appear in every scenario rather than on an axis. [J; FS-032 describes the two-axis convention] |
| Do current strategies survive those futures? | **Wind-tunnelling** of three workforce strategies across the four scenarios | v1 put a strategy choice (augmentation vs substitution) on an axis. That makes the strategy untestable, because each scenario assumes its answer. Wind-tunnelling moves strategies off the axes so they can be tested. [J] |
| What happens downstream of one specific change? | **Futures Wheel** on "AI drafts most first-draft environmental reviews by 2029" | It is the most consequential near-term change for statecraft entry ladders (v1 CLD "Highest" cluster in D6). A Futures Wheel traces second- and third-order effects on roles and competencies. [J; method per FS-059] |
| How do new practices grow out of the current system? | **Three Horizons** applied to how the taxonomy itself works | It separates innovations that lead somewhere new (H2+) from those the current system absorbs (H2−). This distinction matters for credentials and AI-training labour markets. [J; method per FS-057] |
| Why do stakeholders disagree about which future is desirable? | **Causal layered analysis** (brief, used in facilitation) | The disputes are partly about worldviews: efficiency and throughput against stewardship and relationship. CLA makes these discussable in sessions with sector actors. [J; method per FS-058] |
| What should federal and state agencies do in the next 1–3 years? | **Backcasting** from a 2035 vision derived from the charter, then sorting moves into **no-regret** and **scenario-contingent with triggers** | Backcasting starts from the outcome the charter commits to (portable blended-craft workforce) and works back to decisions in time. Scenario screening then separates moves that are robust everywhere from moves to hold until signposts fire. [J; method per FS-060] |

Methods considered and not used: Delphi forecasting (IO runs the Delphi for content validation; a separate forecasting Delphi would duplicate panel burden) and quantitative system dynamics (the data are too thin to calibrate stocks and flows for a 2026 model; revisit when OPM entry and exit series are ingested). [J]

---

## 2. Assessment of the v1 scenario set

v1's scenarios are in `Structural Conditions of Environmental Management Professions.md` (FS-051). They use a 2×2 of **federal investment level** (sustained or expanded vs contracted or withdrawn) × **AI adoption mode** (augmentation-first vs substitution-first):

- A: capacity expansion plus hybridization
- B: throughput expansion plus ladder-collapse risk
- C: "thin state" plus augmentation triage
- D: austerity plus automation plus irreversible-loss risk

### What v1 got right (carry forward)

1. **Adoption mode is an organizational choice, not a technological inevitability.** This is the right framing, and it is consistent with the literature it cites. [E: FS-051]
2. **Career-ladder destruction and knowledge reproduction** are the central workforce risks, more than headcount. The 2025–26 evidence strengthens this. EPA staff who left had a median 30.3 years of service, against 10.8 for those who remain. [E: FS-003] Paid conservation internships fell 43.8% and AmeriCorps postings fell 42%. [E: FS-026]
3. **Crafts as reproduction regimes.** Fieldcraft is reproduced by place-based mentorship, datacraft is more codifiable, and statecraft is tied to legitimacy. [E: FS-051; carried in the CA register]
4. **Refugia institutions:** Tribal programs, state agencies with statutory mandates, extension and applied research centres, and endowed NGOs. These are already visible. The NOAA billion-dollar disaster database moved to Climate Central, run by its former NOAA lead. [E: FS-037]
5. **The austerity-bias warning for the sentinel network.** Under contraction, public field and statecraft holders have the least slack to participate, so validation drifts toward codifiable private datacraft. [E: FS-051] I build this correction into the protocol.
6. **Decision windows close by about 2028.** I agree, for the reasons in §8. [J]

### What does not hold (change)

1. **"Federal investment level" mis-specifies the variable.** FY2026 Interior–Environment appropriations were enacted at $42.56 bn: −1.9% year on year and about $15.7 bn above the President's request. [E: FS-019] Over the same period EPA lost 24% of staff, USFS lost about 13% net, NRCS lost about 24%, and Interior lost about 10,000 staff. [E: FS-003, FS-042, FS-020] Money and capacity have decoupled. The operative uncertainty is **public stewardship capacity**: people, authority, coordination, and entry pipelines. It is not dollars.
2. **The axis is federal-centric.** Devolution to states, Tribes and partners is now a budget structure, not rhetoric. USFS FY27 calls for "state-based leadership models". [E: FS-039] Capacity can fall federally while rising, or failing to rise, elsewhere. The v1 axis cannot represent that.
3. **Putting adoption mode on an axis makes strategy untestable.** If "augmentation-first" defines a scenario, you cannot ask whether augmentation-first is a good strategy in that world. Adoption mode belongs in the **strategy set** that gets wind-tunnelled (§6).
4. **The exogenous AI uncertainty is missing.** Whether AI-produced environmental analysis is **reliable and legitimate** in high-stakes, litigated, nonstationary settings is not settled:
   - Enterprise agentic projects are failure-prone: a forecast that more than 40% will be cancelled by end-2027, cited second-hand. [E: FS-054]
   - EO foundation models degrade with distance from their training region. [E: FS-012]
   - Practitioners stress that AI should only produce first-level work reviewed by humans. [E: FS-008]

   This uncertainty is outside any one agency's control. It belongs on an axis.
5. **No early indicators, no wildcards, no stress-test procedure.** The v1 scenarios ask the right questions, but they are not connected to signposts that would tell a workforce planner which world is arriving.
6. **The evidence base stops at 2025.** It needs to be refreshed with the 2026 record: USWFS, SPEED Act passage in the House, FY26 appropriations, the endangerment-finding repeal, the Roadless proposal, SB 253, Omnibus I, and FireSat operations.

**Verdict:** *change*. Keep v1's content insights (ladders, reproduction regimes, refugia, decision window, sentinel bias). Replace its axes. Move augmentation/substitution from an axis into the wind-tunnel strategy set. (See `v1_assessment.csv`.)

---

## 3. From drivers to axes

### 3.1 Impact × uncertainty screening

The 38 drivers in `drivers.csv` were screened on two judgments [J]:

- **Impact:** how much the driver changes which competencies the federal/state environmental workforce needs, and whether it can reproduce them.
- **Uncertainty:** how open the 2030–2035 outcome is.

| Cluster | Member drivers | Impact | Uncertainty | Treatment |
|---|---|---|---|---|
| **Public stewardship capacity** (people, authority, coordination, entry pipelines across federal, state, Tribal and local actors) | D-P01 federal contraction; D-P04 devolution; D-P08 congressional counterweight; D-E04 fiscal rescissions; D-P06 Tribal co-stewardship; D-S02 entry-pathway collapse; D-P05 fire reorganization | Very high | High | **Axis 1** |
| **AI reliability and legitimacy in environmental decisions** | D-T01 generative AI; D-T02 agentic AI; D-T03 EO foundation models; D-V01 legitimacy; D-P09 AI governance; D-P02 compressed review and litigation | Very high | High (capability is low-uncertainty; reliability and acceptance in high-stakes use are not) | **Axis 2** |
| Climate hazard intensification | D-N01, D-N02 | Very high | Low in direction (2026 YTD fire area 145% of the 10-year average, FS-034); high in annual severity | **Predetermined element** in all scenarios; severity extremes treated as wildcards |
| Retirement and tenure cliff | D-S01 | High | Low (it is happening) | **Predetermined element** |
| Regulatory oscillation | D-P03, D-V03 | High | High on any single rule, low on the pattern of oscillation | **Predetermined volatility**: competencies must be regime-durable in every scenario |
| Sensing and robotics | D-T04, D-T06, D-T07, D-T10 | Medium–high | Medium (timing driven by regulation and procurement) | Varies **within** scenarios; tracked by signposts |
| Disclosure, carbon and nature markets | D-E01, D-E02, D-E03, D-P07 | Medium for federal/state; high for private | Medium–high | Shapes **private and NGO demand within** scenarios; strongest in SC3 |
| Platforms and philanthropy substituting for public functions | D-E05, D-V04 | High | Medium | **Expressed through Axis 1** (it is how thin capacity gets backfilled) |

### 3.2 Why these two axes, and why they are independent

**Axis 1: public stewardship capacity**

- **Rebuilt & coordinated.** By about 2030, the combined federal, state and Tribal environmental workforce has stabilized or grown in the functions that matter, and entry cohorts are restored. Where work is devolved, funding, standards and mobility mechanisms go with it.
- **Thin & fragmented.** Attrition is not replaced and devolution is unfunded. Capacity varies widely between states, and contractors, platforms and volunteers fill gaps ad hoc.

The pole is about capacity and coordination, not location. A federal-led system and a devolved-but-resourced system both count as "rebuilt & coordinated". I chose this deliberately: the workforce consequences depend more on whether devolved capacity is resourced and connected than on which level of government holds it. [J; based on D-P04 and D-P08 evidence]

**Axis 2: AI reliability and legitimacy in environmental decisions**

- **Trusted & assured.** AI-assisted analyses are routinely accepted by courts, Tribes, regulators and publics when they are governed and documented. Routine-task tooling is reliable, and assurance regimes work.
- **Brittle & contested.** High-profile failures occur, courts remand AI-assisted records, agentic projects are cancelled, and models fail under nonstationary conditions. AI is confined to low-stakes uses.

**Independence test.**

- Axis 1 is driven mainly by appropriations politics, civil-service policy, state fiscal capacity and Tribal–federal relations.
- Axis 2 is driven mainly by technical reliability, case law, assurance standards and public trust.

The two interact, since a thin state may adopt AI faster, but neither determines the other, and all four combinations are plausible today. [J]

**Rejected axes**

- "Federal investment": money is not capacity (FS-019 against FS-003 and FS-042).
- "Augmentation vs substitution": this is a strategy, not an environment.
- "Climate severity": its direction is predetermined.
- "Market growth": secondary for the federal/state first audience.
- "Federal-centred vs devolved": folded into Axis 1 as variants. Each scenario notes its devolved variant.

### 3.3 The matrix

| | **AI trusted & assured** | **AI brittle & contested** |
|---|---|---|
| **Capacity rebuilt & coordinated** | **SC1: Assured Augmentation** | **SC2: Human Premium** |
| **Capacity thin & fragmented** | **SC3: Platform Stewardship** | **SC4: Patchwork Retreat** |

**Mapping to v1 (for continuity):**

- SC1 ≈ v1 A
- SC4 ≈ v1 D
- SC3 absorbs most of v1 B and C. Its failure mode is outsourcing to platforms rather than in-house substitution.
- SC2 has no v1 equivalent. v1 never imagined AI disappointing, which is a blind spot given the evidence on project cancellations and litigation risk.

**Predetermined elements in all four scenarios:**

- More fire and climate-hazard workload (FS-034)
- Expert retirements (FS-003)
- Regulatory oscillation between administrations (FS-016, FS-040)
- Growing Tribal assertion of governmental roles (FS-040)
- Continued private GHG-accounting demand from state and EU regimes (FS-015, FS-013)

---

## 4. The four scenarios (2030–2035)

Each scenario gives the workforce shape, craft dynamics, roles that grow and shrink, irreversible-loss risks, a devolved variant, and early indicators. Role IDs refer to `role_signals.csv`. All narrative content is **[J]** unless a source is cited.

### SC1: Assured Augmentation (capacity rebuilt & coordinated × AI trusted & assured)

**Storyline.** After the 2025–26 contraction, a run of bad fire years and permitting backlogs turns into bipartisan pressure to "staff the mission". Congress's FY26 "maintain staffing levels" directive (FS-049) is followed by enforceable staffing floors and entry-hiring authorities. Assurance practice matures:

- Agencies classify AI in permitting as high-impact under M-25-21-style rules (FS-031).
- The CEQ data standard reaches maturity (FS-007).
- Courts uphold AI-assisted reviews whose records document data lineage and human review.

States take on more delivery under funded, standardized agreements, and skills-based records let staff move between federal, state, Tribal and NGO posts.

**Workforce shape (2033).**

- Headcount is near 2024 levels but the composition differs. There are fewer people producing documents and more people:
  - specifying and reviewing AI-assisted analyses
  - collecting ground truth
  - running continuous intelligence (fire, water, air)
  - owning products
- Entry cohorts are restored through AI-augmented apprenticeships.

**Crafts.**

- **Data craft** demand rises, but in validation, model risk and reference data more than in hand analysis.
- **Field craft** becomes the bottleneck. Verification, labels, restoration implementation and fire operations do not scale digitally. The EO-embedding evidence shows labels and regional validation remain binding (FS-012).
- **Statecraft** concentrates on accountable sign-off, scoping judgment and intergovernmental agreements.

**Grow:**

- FS-RS-01 AI-assisted review lead
- FS-RS-02 model risk officer
- FS-RS-04 ground-truth steward
- FS-RS-05 fire intelligence analyst
- FS-RS-07 product owner
- FS-RS-08 drone program lead (once Part 108 lands)
- FS-RS-11 agreement manager
- FS-RS-09 digital-twin steward (late in the period)

**Shrink or reshape:**

- FS-RS-24 comment analyst
- FS-RS-23 routine GIS technician
- FS-RS-18 entry NEPA analyst: the role is redesigned, not abolished.

**Irreversible-loss risks.** These are moderate. The quiet risk is **validation without formation**: juniors who review AI output without ever having produced and defended analyses become seniors around 2035 who cannot tell when AI is wrong. A second risk is vendor lock-in on models the agencies cannot audit.

**Devolved variant.** States and Tribes hold more of the operating roles. Federal agencies become standard-setters and funders. Mobility tools are essential.

**Early indicators (pointing toward SC1).**

- OPM headcount in core environmental series stable or rising for 2+ consecutive quarters.
- Entry-grade hiring share recovering.
- RIF moratorium or staffing-floor language enacted (FS-048 model).
- Courts uphold AI-assisted environmental records.
- Agency AI inventories list governed high-impact permitting uses.
- Conservation internship postings recover toward 2024 levels (FS-026 baseline).

### SC2: Human Premium (capacity rebuilt & coordinated × AI brittle & contested)

**Storyline.** Capacity is rebuilt for the same political reasons as in SC1, but AI disappoints in the places that matter:

- A small number of high-profile remands find AI-assisted records deficient. This is speculative: no such ruling has occurred, and that absence is itself a signpost.
- Agentic pilots are cancelled at the rates enterprise analysts forecast (FS-054).
- Models trained on historical NEPA corpora (FS-008) reproduce obsolete analytic patterns that do not fit the post-Seven County, shorter-document regime.
- Tribal nations and publics reject AI summaries as a substitute for consultation (FS-040).

AI is confined to search, summarization and QA support.

**Workforce shape (2033).**

- Larger human teams and slower throughput.
- Experienced reviewers, consultation leads, field ecologists and fire leaders command a wage premium.
- Pressure from SPEED-type deadlines (FS-001) without AI throughput produces overtime, burnout and backlogs.

**Crafts.**

- **Field craft** and **statecraft** are premium.
- **Data craft** focuses on assurance and classical, transparent models.
- The tool layer changes slowly.

**Grow:**

- Senior environmental review and consultation roles
- FS-RS-12 knowledge continuity lead
- FS-RS-17 record specialist
- FS-RS-02 AI assurance officer (here a "brakes" function)
- FS-RS-11 agreement manager
- Field and fire operations

**Shrink:**

- Public-sector demand for AI product roles and AI-evaluation experts (FS-RS-10)
- Fewer digital-twin deployments

**Irreversible-loss risks.** Moderate:

- Capacity exists but retirements outpace training.
- "Capacity without speed" invites a political swing toward SC3 or SC4.

**Devolved variant.** States with strong civil services (and Tribal programs) become the leading employers of experienced practitioners. There is interstate competition for talent.

**Early indicators.**

- First court decisions remanding for AI-related record defects.
- Agencies withdraw AI use cases.
- Statutory or regulatory "human-produced analysis" requirements.
- Vendor contract cancellations.
- Professional societies issue restrictive AI practice standards.

### SC3: Platform Stewardship (capacity thin & fragmented × AI trusted & assured)

**Storyline.** Public capacity is not rebuilt, but AI and sensing work well. Delivery moves to:

- Consultancies with AI-flattened pyramids (FS-008, Jacobs tooling)
- Platforms and registries
- Philanthropy-backed alliances (FireSat: early-adopter data Q4 2026, global access 2028; FS-011)
- AI firms that have trained agents on recreated agency workflows (FS-038)

Agencies become **intelligent customers**. They procure, oversee and sign. Wealthy states build their own capacity; others depend on vendors. Private demand is strong in GHG/ESG (SB 253 first reports 10 Nov 2026; FS-015), MRV (FS-043) and utilities (FS-028).

**Workforce shape (2033).**

- A small, senior public core: legal accountability, procurement, contract oversight, a few validators.
- A large, AI-leveraged private delivery layer with a thin junior tier.
- Seasonal and contracted field crews.

**Crafts.**

- Public **statecraft** shifts to procurement, data rights and accountability.
- **Data craft** is externalized.
- **Field craft** is under-supplied and contracted, with high turnover, so place-based judgment is not retained.

**Grow:**

- FS-RS-02 model risk officer
- Procurement and data-rights roles (FS-C10)
- FS-RS-10 AI-evaluation experts (private)
- FS-RS-03 dMRV verifiers
- FS-RS-13 GHG data controllers
- FS-RS-05 fire intelligence (state, utility, private)
- FS-RS-21 utility fire-weather specialists

**Shrink:**

- Public GIS technicians (FS-RS-23)
- Comment analysts (FS-RS-24)
- Entry policy analysts (FS-RS-18)
- Public field technicians
- EJ program staff (FS-RS-27)

**Irreversible-loss risks.** High:

- **The hollow state.** Once in-house experts are gone, agencies cannot judge vendor output ("know what good looks like").
- Data and model rights are lost to platforms (D-V04).
- The field-craft ladder breaks.
- Place-based judgment sits with contractor staff who rotate out.
- Private entry ladders are also compressed by AI, so the sector as a whole, not just government, stops producing mid-career judgment.

**Devolved variant.** "Platform federalism": states buy the same few platforms, with homogenized methods and concentrated vendor power.

**Early indicators.**

- Contract obligations for environmental analysis rise while environmental-series FTE falls.
- AI inventories show vendor-operated high-impact uses.
- Detection and intelligence data offered by subscription.
- Expert-task AI-training markets grow (FS-038 pattern).
- Internship postings stay depressed.
- States issue "AI permitting" procurements.

### SC4: Patchwork Retreat (capacity thin & fragmented × AI brittle & contested)

**Storyline.** Junior roles are cut on the assumption that AI will carry the load, and then the AI under-delivers, leaving neither (the failure mode warned of in FS-054). Fire seasons at or above the 2026 pattern (FS-034) absorb what capacity remains. Permitting stalls in litigation. Datasets are discontinued (FS-037 pattern). Capacity survives in **refugia**:

- Tribal programs exercising self-governance
- State agencies with statutory mandates
- University extension and research centres
- Endowed NGOs
- Data nonprofits

Outcomes diverge sharply between states.

**Workforce shape (2033).** Federal programs are thin and fire-dominated. Most landscape, monitoring and community work is done by states, Tribes, NGOs and volunteers. The skills base varies widely by region.

**Crafts.**

- **Field craft** is in demand (fire, emergencies, recovery) but supply is collapsing.
- Relational **statecraft** that brokers across the patchwork becomes the scarce capability.
- **Data craft** is limited and often donor-funded.

**Grow (in demand):**

- Fire operations and FS-RS-05
- FS-RS-12 knowledge continuity
- FS-RS-11 agreement managers
- FS-RS-16 community science coordinators (as a substitute for paid monitoring)
- FS-RS-15 adaptation navigators (NGO and local)

**Shrink:**

- Most federal program roles
- Research (EPA ORD elimination plan; FS-003)
- EJ
- Long-term monitoring

**Irreversible-loss risks.** Highest:

- Fire leadership and incident qualifications. Cohort breaks take decades to repair (FS-051).
- Place-based forest and watershed judgment.
- Taxonomic identification skills.
- Tribal–federal relationship practice (GAO already finds cuts slowing co-stewardship; FS-020).
- Continuity of long-term monitoring records.
- EJ community trust.

**Devolved variant.** This is the default form of SC4.

**Early indicators.**

- Further RIFs; moratorium bills fail.
- Entry hiring in environmental series near zero for 2+ years.
- Repeated fire seasons above 140% of the 10-year average alongside falling fire staffing.
- AI project cancellations coinciding with court remands.
- Core datasets discontinued.
- State budget cuts to environmental agencies.

### 4.5 Wildcards (low probability, high impact; each can switch scenarios)

| ID | Wildcard | Likely effect |
|---|---|---|
| W1 | Catastrophic fire or flood year with mass casualties | Emergency rebuild (pushes toward SC1/SC2), or blame-driven reorganization |
| W2 | Landmark appellate ruling on an AI-assisted EIS, either way | Moves the Axis 2 position quickly |
| W3 | AI-caused environmental harm incident (e.g., a misclassified habitat leads to an unlawful take) | SC2/SC4 |
| W4 | Step change in agentic AI reliability | SC1/SC3 |
| W5 | USFS fire merged into USWFS (Congress has required a feasibility study; FS-049) | Fire-role redesign across ~10,000+ staff [S on the number] |
| W6 | Loss of a core public Earth-observation or monitoring program | SC3 (platform substitution) or SC4 |
| W7 | Recession that hits state budgets | Devolution fails; SC4 |

---

## 5. Futures Wheel: "By 2029, AI drafts most first-draft environmental reviews and comment summaries"

The centre event is anchored in WS-05, WS-11, WS-13 and WS-17. Effects ripple outward in three orders [J]:

1. **First order**
   - Drafting hours per document fall.
   - Review volume per reviewer rises.
   - Entry tasks (drafting, literature review, comment coding) shrink. v1 rates these CLD "Highest" on 6.1.1, 6.1.2, 6.4.1 and 6.4.4 (FS-055).
   - What a "record" must document changes (AI use, lineage).
   - Consultants re-price, with fewer junior billable hours.
2. **Second order**
   - Fewer junior hires in agencies and consultancies, so fewer people by 2033 who have built and defended an analysis.
   - The bottleneck moves upstream to scoping and field data (ground truth, surveys) and downstream to accountable sign-off.
   - Litigation shifts to AI provenance and the quality of responses to "substantive comments" under a 150-day limitations period (FS-001).
   - Tribal consultation risks being compressed into AI-summarized comment processes, against Tribal objections (FS-040).
   - Consulting pyramids flatten, and mid-career scarcity drives a wage premium for experienced reviewers.
3. **Third order**
   - New roles: FS-RS-01, FS-RS-17.
   - New competencies: FS-C01, FS-C03, FS-C13.
   - Professional societies and credentials (CAREP, FS-027) define AI practice standards.
   - If failures occur, a legitimacy swing toward SC2. If not, consolidation toward SC1 or SC3 depending on capacity.

**Taxonomy implication.** In L2, split tasks that bundle "produce" with "specify/review" (e.g., *draft an alternatives analysis* vs *specify, review and defend an AI-assisted alternatives analysis*). Exposure assessments can then tell which half is changing, and CLD can be computed at the pathway level.

---

## 6. Wind-tunnelling three workforce strategies

| Strategy | SC1 Assured Augmentation | SC2 Human Premium | SC3 Platform Stewardship | SC4 Patchwork Retreat | Verdict |
|---|---|---|---|---|---|
| **ST-S Substitution-first**: use AI to cut headcount, entry roles first | Partial: short-term throughput, then a judgment deficit by ~2033 | **Fails**: AI is pulled back and there are no juniors to fall back on | Works for budgets, **fails on accountability** (hollow state; lock-in) | **Fails badly**: neither AI nor people | Fragile; avoid |
| **ST-A Augmentation-first**: use AI to raise productivity and keep headcount | **Works** | Partial: AI value is small but people are kept | Partial: headcount unaffordable; still needs a public assurance core | Partial–fails: too few people left to augment | Good where capacity exists |
| **ST-M Augmentation-for-formation**: AI frees senior time for mentorship; a protected learning substrate; cross-actor rotations; ground truth as infrastructure | **Works** (slower initial throughput) | **Works** | Partial: preserves the intelligent-customer core and field-craft ladder at small scale | Partial: refugia rotations keep ladders alive | **Most robust; recommended** |

ST-M is v1's Scenario A intervention ("AI-mediated apprenticeships") generalized into a strategy that holds everywhere. [J; FS-051]

---

## 7. Three Horizons and causal layers (for facilitation)

### Three Horizons (applied to how the taxonomy and workforce system work) [J]

- **H1 (current system, declining fit):**
  - Static competency lists revised every few years
  - Classification by occupational series
  - Incident-only NWCG qualifications
  - Annual surveys
  - Entry through low-paid seasonal and internship ladders
- **H3 (emerging future, already visible in pockets):**
  - A living skills commons updated from signals
  - Portable skills records across seven sector actors
  - Governed human–AI teaming
  - Ground truth treated as shared infrastructure
  - Tribal nations as co-governors
- **H2+ (innovations that bridge toward H3):**
  - CEQ data standard (FS-007)
  - FireSat early-adopter program (FS-011)
  - OpenLMP demand signals
  - CAREP, but only if it is anchored to durable competencies (FS-027)
- **H2− (innovations H1 captures):**
  - Tool-fluency credentials that substitute for durable competence
  - Expert-task AI-training markets (FS-038) that extract practitioner know-how to build substitutes without returning a career ladder
  - Vendor platforms that make states dependent on one methodology

### Causal layered analysis [J]

1. **Litany:** "The agencies were gutted" and "AI will fix permitting".
2. **Systemic causes:**
   - Appropriations decoupled from staffing.
   - Classification by series makes hybrid roles hard to hire (FS-053).
   - Procurement rewards throughput.
   - Litigation risk drives document length.
3. **Worldview:** Efficiency and speed (SPEED Act: NEPA "purely procedural"; FS-001), against stewardship, precaution and relationship (99% of 220,000+ Roadless letters opposed rescission; FS-040).
4. **Myth/metaphor:** "Government as a vending machine for permits", against "stewardship as apprenticeship and kinship with place".

**Use in sessions.** SC3 feels like progress under the efficiency worldview and like loss under the stewardship worldview. Naming this layer stops scenario workshops from collapsing into arguments about whose preferred future is "realistic".

---

## 8. Backcasting and moves for the next 1–3 years

### 8.1 Vision for 2035 (from the charter)

A mobile environmental workforce whose field, data and statecraft blends are visible and portable across federal, state, local, Tribal, NGO, private and academic employers. AI is governed and assured. Entry ladders are intact. The EMST is the shared language and updates annually from signals.

### 8.2 Milestones, working backward [J]

| Year | Milestone that must be true |
|---|---|
| 2035 | Mid-career cohort (hired 2026–2030) can independently judge AI-assisted analyses; mobility across actors is routine |
| 2032 | Skills-based records are accepted across federal and multiple state systems; AI-assurance competencies appear in position descriptions and class specs; CLD-flagged pathways have redesigned formation tasks |
| 2030 | Entry cohorts in core environmental series restored to ≥2024 levels, **or** refugia rotations operating at scale; third sentinel cycle complete; first scenario refresh |
| 2028 | Decision window (v1): no-regret moves running in pilot agencies; tacit-knowledge capture done for the highest-risk sites and functions; AI validation in agency training curricula |
| 2027 | EMST v2.0 released with lifecycle states and watch layer; first annual Signals Review; NGO pilot kit in use; first federal and state pilots adopt no-regret moves |

### 8.3 No-regret moves for federal and state workforce strategy (late 2026 to 2029)

These hold in all four scenarios. Each is **[J]** with the evidence that motivates it.

| ID | Move | Federal | State | Why it is robust | Evidence |
|---|---|---|---|---|---|
| NR-1 | **Protect a minimum entry cohort and the learning substrate.** Ring-fence entry positions (whatever entry authorities are current; FH to confirm), state trainee classes, registered apprenticeships and corps contracts. Redesign entry work so juniors still produce, field-check and defend analyses with AI (FS-C13) | ✓ | ✓ | Needed for scale (SC1), fallback (SC2), the intelligent-customer core (SC3) and refugia (SC4) | FS-026, FS-046, FS-056 |
| NR-2 | **Run a tacit-knowledge capture and succession sprint** targeted at retirement-eligible experts in high-tacit, CLD-flagged and place-bound functions (structured elicitation, paired fieldwork, recorded field walks; FS-C12). Indigenous knowledge only on its holders' terms (TN) | ✓ | ✓ | Knowledge is leaving now in every scenario | FS-003, FS-029 |
| NR-3 | **Make AI validation and assurance a cross-cutting requirement** for anyone who consumes AI output (FS-C01), with a small model-risk function per agency (FS-C02) | ✓ | ✓ | Scales AI (SC1), limits harm (SC2), oversees vendors (SC3), triages failures (SC4) | FS-031, FS-012, FS-008 |
| NR-4 | **Treat ground truth as infrastructure.** Maintain reference plots, labelled datasets and calibrated field-assessor pools (FS-C04, FS-C08) | ✓ | ✓ | Every AI, EO and dMRV system depends on it; it keeps a field-craft ladder alive | FS-012, FS-047, FS-023 |
| NR-5 | **Build skills-based mobility channels now.** Translate federal experience into state, Tribal and NGO terms through EMST role crosswalks; use details, IPAs and interstate agreements | ✓ | ✓ | The 2025–26 displacement is a natural experiment in the theory of change; mobility also lets refugia work | FS-018, FS-017 |
| NR-6 | **Strengthen intelligent-customer capacity:** technology and data procurement with public data rights, model auditability and exit clauses (FS-C10); product ownership for permitting systems (FS-C09) | ✓ | ✓ | Essential in SC3, useful everywhere as data moves outside government | FS-011, FS-037, FS-007 |
| NR-7 | **Invest in intergovernmental agreement craft** (FS-C14) and fund partner capacity alongside any devolution | ✓ | ✓ | Devolution and Tribal assertion are predetermined; the capacity to administer agreements is thin | FS-039, FS-020, FS-040 |
| NR-8 | **Stand up horizon scanning and a sentinel network**, linked to taxonomy releases and agency workforce plans (see `horizon_scanning_protocol.md`) | ✓ | ✓ | Cheap; tells agencies which scenario is arriving | FS-052, FS-051 |

### 8.4 Scenario-contingent moves (hold until the trigger fires)

| ID | Move | Scenario | Trigger (signpost) | Risk if done too early |
|---|---|---|---|---|
| CM-1 | Scale AI-augmented review teams; create parenthetical titles and PD language for AI-assisted review lead (FS-RS-01) and product owner (FS-RS-07) | SC1 | Two or more appellate decisions upholding AI-assisted records **and** environmental-series headcount stable for 2 quarters | Committing to AI throughput before legitimacy is settled |
| CM-2 | Recruit and train BVLOS program leads (FS-RS-08) | SC1/SC3 | FAA Part 108 final rule published (FS-022) | Training for a rule that changes shape |
| CM-3 | Fund fire-intelligence analyst cohorts and data integration (FS-RS-05) | SC1/SC3 | Agency early-adopter ingestion of FireSat-class data with known access terms (FS-011) | Lock-in to a data product with unknown licensing |
| CM-4 | Retention premiums and retire-rehire programs for senior reviewers; human-produced analysis requirements | SC2 | First remands for AI-related record defects; agencies withdraw AI use cases | Over-paying for scarcity that AI later relieves |
| CM-5 | Platform-oversight package: model risk officers, data-rights negotiators, vendor-independent validation teams; public data commons agreements | SC3 | Contract obligations for analysis rise while FTE falls for 4 quarters; subscription-only intelligence data | Accelerating outsourcing it is meant to govern |
| CM-6 | Refugia strategy: fund state, Tribal (on Tribal terms) and extension hosts for rotational apprenticeships; emergency re-employment of annuitants; minimum viable sentinel network | SC4 | Entry hiring near zero for 4 quarters **and** RIF moratorium fails **or** state environmental budgets cut | Signals abandonment of federal capacity |
| CM-7 | Digital-twin stewardship training (FS-RS-09) | SC1 | An operational twin used in a regulatory or incident decision at a named agency | Training for research-stage tools |

**Decision point (named for the CA):** whether EMST v2 publishes these moves as part of the federal/state pilot package. I recommend yes: NR-1 to NR-8 as guidance, and CM-1 to CM-7 as watch-and-trigger notes. AS and FH should confirm that adopters can act on them.

### 8.5 Signpost dashboard (feeds L5 and the horizon-scanning protocol)

| Signpost | Source | Cadence | Points toward |
|---|---|---|---|
| Headcount and entry-grade hiring share in environmental series (0401, 0408, 0460, 0486, 0028, 0819, 1315, 1340 and others; FH to finalize) | OPM workforce data (data.opm.gov; FS-003 uses it) | Quarterly | Axis 1 |
| Staffing-floor, RIF-moratorium and reprogramming language | CRS appropriations reports; Congress.gov (FS-019, FS-048) | Per bill | Axis 1 |
| Conservation internship, AmeriCorps and permanent postings vs 2024 | Conservation Job Board data (FS-026) | Semi-annual | Axis 1 |
| Court decisions on AI-assisted environmental records | Federal dockets, CRS legal sidebars | Monthly | Axis 2 |
| High-impact AI uses in permitting, enforcement and monitoring; withdrawals | Agency AI use case inventories (FS-031) | Annual plus ad hoc | Axis 2 |
| AI-in-environmental-review procurements and cancellations | SAM.gov, state procurement portals | Quarterly | Axis 2; SC3 |
| Contract obligations for environmental analysis vs FTE | USAspending, agency budget justifications | Annual | SC3 |
| FireSat/EO data access terms and agency ingestion | EFA, agency announcements (FS-011) | Quarterly | SC1/SC3 |
| Part 108 final rule | Federal Register (FS-022) | Event | Sensing timing |
| Fire season acres vs 10-year average, and fire staffing | NIFC IMSR (FS-034); agency fire staffing | Weekly in season / annual | Predetermined pressure; SC4 |
| Discontinued federal environmental datasets | Agency notices; NGO trackers (FS-037) | Quarterly | SC3/SC4 |
| Tribal co-stewardship agreements signed or stalled | GAO, agency reports, Tribal organizations (via TN; FS-020) | Annual | Axis 1 |

---

## 9. Stress-testing the taxonomy against the scenarios

### 9.1 Procedure (proposed for every major release)

1. **Role cards.** For each scenario, list the 15–25 functions the federal/state environmental workforce must perform in 2033 (from §4 and `role_signals.csv`).
2. **Coverage test.** For each function, check whether the release has L3 role profiles and L1/L2 content that cover it. Uncovered functions needed in ≥2 scenarios are **scenario-critical gaps** and go to the candidate pool.
3. **Sensitivity tagging.** For each competency or task, record demand direction (up / flat / reshape / external / down) and reproduction risk (L/M/H) per scenario, as attributed L5 assessments.
4. **Robustness classes.**
   - **Robust:** non-declining in ≥3 scenarios and high reproduction risk in ≤1.
   - **Fragile:** non-declining in ≤2 and high risk in ≥2.
   - **Contingent:** otherwise.

   A competency in demand somewhere but fragile in supply in ≥2 scenarios gets a **protect** flag, so that declining public demand is never read as permission to let a safety- or trust-critical capability lapse.
5. **Architecture wind-tunnel.** Ask whether each architecture decision (spine, families, levels, crosswalks) still works if SC3 or SC4 arrives. For example, does a federal-series crosswalk still serve users if most delivery roles are state, NGO or private?

### 9.2 Illustrative run on v1 (heuristic, [J])

`scenario_stress_test.py` applies transparent rules to the v1 tags:

- craft primary
- modal automation type
- CLD flag
- Core profession families: public-agency-concentrated F1, F2, F8, F12 vs private-demand F7, F14, F15, following FS-051

Robustness is judged through the **federal/state workforce lens** (the first audience): "external" (work moves to vendors or partners) counts as loss of public capacity.

**Results across the 222 v1 competencies:**

- 74 robust, 109 contingent, 39 fragile
- 59 carry the protect flag

**Where fragility concentrates:**

- Field operations (13 of the 39 fragile are in D4, including prescribed burning 4.2.3, equipment operation 4.5.2–4.5.5 and water-quality surveys 4.1.3)
- Public-family field science (D1 forestry and wildlife: 1.3.x, 1.4.x)
- CLD-flagged entry work in communication and policy (5.1.1, 5.4.x, 6.1.1, 6.1.2, 6.4.1, 6.4.4)

**Where robustness concentrates:**

- Relational and intergovernmental statecraft (5.2.x, 6.5.x)
- AI-governance items (7.1.4, 7.2.1, 7.2.3, 2.6.5)
- Much of D2. This partly reflects v1's assignment of D2 competencies to F7, a private-demand family.

**Caveats.**

- Field-craft fragility in SC3/SC4 is partly **by construction**: a rule assigns high reproduction risk to FC under thin capacity. It rests on the v1 reproduction-regime argument (FS-051) and on the 2025 entry-pathway data (FS-026), not on independent measurement.
- The run inherits v1's single-analyst tags (FS-055).
- Its value is to show the mechanism and generate a ranked hypothesis list for Delphi and SME testing, not to classify.

**Scenario-critical gaps (functions needed in ≥2 scenarios with no adequate v1 competency) [J]:**

- AI/model risk management (FS-C02)
- AI provenance and record defensibility (FS-C03)
- Ground-truth stewardship (FS-C04)
- Technology and data procurement with data rights (FS-C10)
- Tacit-knowledge transfer (FS-C12)
- AI-augmented apprenticeship design (FS-C13)
- Intergovernmental agreement lifecycle (FS-C14)
- Assessor calibration (FS-C08)
- Continuous fire-intelligence fusion (FS-C05)

All are in `candidate_competencies.csv`.

---

## 10. Limits of this scenario set

- **Geography.** U.S.-centric, with EU and California disclosure as the main international links. Tribal futures are discussed only through published Tribal perspectives (FS-040) and must be revisited with TN's protocol and real Tribal participation. This set does not speak for Tribal nations.
- **Search constraints.** The shared web-search budget ran out during this phase. The evidence on carbon-market scale (FS-025, paywalled), eDNA programs and state climate-policy budgets is thinner than I would like.
- **Unverified items.** The SC2 storyline depends on court outcomes for AI-assisted records. I found **no** such ruling as of October 2026, so SC2's trigger events are [S].
- **Refresh.** These scenarios should be refreshed in 2029, or earlier if a wildcard fires.
