# EMST Governance and Contribution Charter (draft v0.1)

**Role:** AS · **Date:** 2026-10-23 · **Status:** draft for CA decision DP-9. Tribal provisions are **pending TN review** and, before adoption, real consultation with Tribal nations and inter-Tribal organizations. A simulated advisor cannot ratify them.
**Evidence labels:** [E: ID] · [J] · [S]. AS-, CA- and TN- IDs resolve in each role's `sources.csv`.

---

## Part A — What the precedents teach

| Precedent | Who governs | How change happens | Cadence and versioning | License | Lesson for EMST |
|---|---|---|---|---|---|
| **NICE Framework** (NIST) | NICE Program Office decides; SMEs and users consulted | Anyone may submit a change request with rationale, change type and effect on related content. Proposals become "candidates" for public comment. Comments are adjudicated as Noted / Accepted / Accepted with modification / Deferred / Rejected. Criteria: fit, essential, cross-sector, relation to existing content, authoring guide [E: AS-025] | MAJOR.MINOR.ADMIN. Major no more than once every 3 years with ≥1 year notice; minor no more than yearly; admin anytime. Withdrawn content stays available in old versions [E: AS-026]. v2.0.0 (Mar 2025) handed removed roles to DoD's DCWF [E: AS-027; CA-033] | U.S. government work [J] | The best template for change control and cadence. **Federation works when the partner (DCWF) has its own mandate and staff.** [J] |
| **ESCO** (European Commission) | DG EMPL manages and funds; Member States Working Group advises (2 experts per state; consensus, else simple majority; mandate to 2030) [E: AS-028] | Continuous: user forums, member-state notices, vacancy and CV big data, studies; QA and domain-expert validation before major updates [E: AS-029] | v1 (2017), v1.1 (2022), v1.2 (May 2024) [E: AS-028] | Free reuse [J] | Formal seats for public authorities give legitimacy. **Labor-market data is a standing input to change, not a one-off.** |
| **O*NET** (DOL) | Federal program run by a contractor center | Rolling data collection; emerging tasks via write-ins and NLP review [E: AS-003] | Quarterly database releases (30.1–31.0 in 2025–26) [E: AS-004] | CC BY 4.0 [J, not re-verified] | Quarterly data releases can coexist with a stable structure. Attribution licensing has not blocked wide vendor reuse. [J] |
| **Credential Engine / CTDL** | Nonprofit; state partners | Open schema development; state publishing partnerships [E: AS-033] | Continuous registry | CTDL is open [J] | Sustained by philanthropy plus state partnerships across 49 states [E: AS-033, AS-034]. A funder-diverse nonprofit standard can last. |
| **SFIA** | SFIA Foundation (not-for-profit) | Consultation-based major versions; SFIA 10 in consultation [E: AS-030]. Attendee proposals for a "stable core + plug-ins" [E: CA-034] | ~3-year majors [E: CA-034] | Free for individuals and single organizations; **paid partner and commercial licences** (GBP 250–4,000/yr) fund upkeep [E: AS-030] | Shows commercial-use revenue can sustain a framework. It conflicts with an open core, so EMST takes the revenue idea but applies it to services and conformance (Part C). |
| **ECO Canada NOS / EP** | Sector organization | Not described on the page [E: AS-031] | No version stated | Proprietary; certification fees (3,000+ EPs) [E: AS-032] | Closest environmental precedent. **The standard survives because a credential and services business rides on it.** [J] |
| **schema.org / W3C / IETF** | Small steering group plus open community groups; staged maturity; rough consensus [J, not re-verified] | Public issue trackers; staged drafts | Continuous with tagged releases | Open | Open participation with a small decision body; draft → candidate → release stages. |
| **TDWG (Darwin Core)** | Biodiversity standards community | Vocabulary Maintenance Specification: term changes, deprecation, public review [J, not re-verified] | Versioned term lists | CC BY | Environmental-domain proof that a volunteer community can run term-level change control for decades. |
| **Australian Skills Classification** | Single government agency | Structure: core competencies, specialist tasks, technology tools; trending and emerging flags [E: AS-060 via CA-036] | 3.0 (data to Dec 2023); **no longer actively maintained** [E: AS-060 via CA-036] | Government open data [J] | **Cautionary case.** A one-owner taxonomy ends when that owner's priorities change. Users without a governance stake cannot keep it alive. [J] |
| **OpenLMP** (sister repo) | Repo maintainers as editors until a host is agreed | `standard-change` issues with examples from ≥2 plans; decision with rationale; breaking changes need 30-day comment plus migration script; proposed advisory group incl. a Tribal representative; upstream alignment with CEQ [E: AS-046] | Semantic versioning; every record states its version [E: AS-046] | Code Apache-2.0; data CC0 [E: AS-046] | Same team, same repo patterns. EMST should align with it but needs heavier governance because it touches hiring. |

**Five lessons applied below** [J]:
1. Small decision body, open participation.
2. Formal seats for the public authorities and professions whose legitimacy EMST borrows.
3. Labor-market and practitioner signals as standing inputs.
4. A published, predictable cadence with long support windows. Stability is what adopters buy.
5. No single owner. Durability must not depend on one organization's priorities. This is the ASC lesson.

---

## Part B — Is federated core-plus-modules governance credible? (CA DP-9, Option C)

**Short answer: yes, in stages, and not as v2.0's starting state.** [J]

Evidence for:
- NICE's hand-off of removed work roles to DoD's DCWF shows a core and an extension can be governed separately when the extension's steward has its own mandate and staff. [E: AS-027; CA-033]
- ESCO's member-state seats show distributed legitimacy can be formalized. [E: AS-028]
- SFIA 10 workshop attendees asked for a core with plug-ins, though SFIA has not decided this. [E: CA-034]

Evidence against, or gaps:
- **No subsector body was found that has agreed, or is resourced, to steward an EMST module.** I could not contact or verify most candidates this session (ecosystem entries marked UNVERIFIED).
- The professional societies EMST would rely on have thin staff and compete for jurisdiction (forestry vs. wildlife vs. data science vs. planning). [E: AS-056]
- SAF recently renamed programs to protect its ability to accredit. [E: AS-042] Societies are under their own pressure and will not take on unfunded duties.

**Recommended phasing:**

| Phase | Module status | Who authors | Who signs off | Trigger to advance |
|---|---|---|---|---|
| **v2.0–v2.1 (2027–28)** | *Editorial sections*: namespaced IDs and shared schema, but governed by the core Editorial Board | Core team and DB experts, **commissioned and paid centrally** | Editorial Board, with a named **module advisory partner** (e.g., SAF for forestry) reviewing | Partner signs a Module Stewardship Agreement and completes two review cycles on time |
| **v2.2+ (2029–)** | *Stewarded modules* | Module steward's SME pool (with core editorial support) | Module steward, within core rules; core checks conformance | Annual conformance review |
| **Any time** | *Orphaned module* | Core resumes authorship | Editorial Board | Steward misses two cycles or withdraws (Art. 4.7) |

**Candidate module partners** (all [J]; status per `ecosystem.csv`; none yet committed):

| Module | Advisory partner, then steward candidate | Notes |
|---|---|---|
| Forestry | SAF [E: AS-040 active] | Strongest fit: accreditation plus CF |
| Wildlife and fisheries | TWS and AFS jointly | Joint stewardship reduces jurisdiction disputes |
| Fire | USWFS/USFS training with NWCG as **reviewer**, not steward | NWCG governs qualifications. EMST links to them and must not appear to compete [E: AS-011] |
| Restoration | SER | |
| Water and wastewater | AWWA and WEF with ASDWA/ACWA as state reviewers | DB to confirm the subsector list |
| Air | A&WMA with NACAA | |
| Environmental health | NEHA | |
| Planning and land use | APA (AICP) | |
| Geospatial and environmental data | UCGIS / GISCI / ESIP consortium | Data craft is transversal, so the module covers tools and specialist tasks only |
| Corporate sustainability / ESG | PS to identify (ISSP status unknown) | |
| *(no Tribal module)* | — | Following TN: Tribal employers are a sector actor with role variants, not a family or module. The **Tribal Council's authority runs across all modules** (Art. 3.5) |

What would change this view:
- If no partner signs a Module Stewardship Agreement by the end of 2028, Option C collapses into central authoring with modules as editorial sections only. CA anticipated this in §7. EMST then needs about one more editorial FTE (`sustainability_model.md`). [J]

---

## Part C — Draft charter

### Article 1. Purpose and scope
1.1 The Environmental Management Skills Taxonomy (EMST) is an open, vendor-neutral standard that describes environmental work: tasks, competencies, proficiency levels, role profiles, crafts and change signals. It helps people, skills and knowledge move between federal, state, local, Tribal, NGO, private and academic institutions.
1.2 This charter governs the EMST **core**, its **modules**, its **fast layers** (tools, signals) and its **crosswalks**, as defined by the architecture CA adopts (L0–L6 and modules).
1.3 The charter does not govern the standards EMST crosswalks to, such as O*NET, OPM standards, NWCG qualifications or society credentials. EMST proposes changes upstream to their owners and never forks them. This follows OpenLMP's CEQ rule. [E: AS-046]

### Article 2. Principles
- 2.1 **Open by default.** The core data, documentation and history are public (Article 8).
- 2.2 **Evidence-labeled.** Every substantive record carries E/J/S provenance and sources.
- 2.3 **Stability for adopters.** Published IDs are permanent. Changes follow Article 6.
- 2.4 **Function over institution.** Content describes work, not org charts.
- 2.5 **Sovereignty and consent.** Tribal nations' authority over their data and knowledge is respected under the CARE Principles. [E: AS-046] Indigenous knowledge is included only where its holders choose, on their terms.
- 2.6 **No single owner.** No organization, including the steward, may hold a majority of votes on any decision body.
- 2.7 **Worker protection.** EMST is not a tool for ranking or removing individuals. Uses in selection require validity evidence that meets the standard IO sets (Article 5.6).

### Article 3. Bodies

**3.1 Steward (host institution).** Operates the program and employs staff. Holds the EMST name and marks **in trust** for the Consortium (Art. 9). Signs agreements and manages funds. Has no editorial veto. Is bound by a five-year Host Agreement with succession terms (Art. 11).

**3.2 Editorial Board (7–9 voting members).**
- **Seats:**
  - the Managing Editor (chair; votes only to break ties);
  - three craft editors (field, data, statecraft);
  - a methods editor (job analysis and validation);
  - an interoperability editor;
  - a sector-balance editor (state, local, NGO or private);
  - the Tribal Council's liaison (voting);
  - one rotating module representative once modules are stewarded.
- **Terms:** two years, staggered; at most two consecutive terms.
- **Role:** decides substantive content changes and releases.
- **Composition rules:** no more than one member from the same organization; at least three sector actors represented.

**3.3 Technical Steering Committee (3–5).** Owns the schema, ID policy, release engineering, crosswalk method and the build. Includes the data steward, IA's successor role and one external maintainer from an adopter.

**3.4 Advisory Council (17–21 seats).**
- **Seats:** federal (2), state (2), local (1), Tribal (2, appointed by the Tribal Council), NGO (2), private employers (2), academia and accreditors (2), professional societies (2), workforce voice and employee organizations (2), labor-market data and research (1), plus funders as **non-voting observers**.
- **Role:** advises on priorities, reviews the annual plan, ratifies major releases (2/3 vote), appoints Editorial Board members from nominations, and selects a successor steward if needed.
- **Meetings:** at least twice a year.

**3.5 Tribal Council (5–7 members; pending TN design and real consultation).**
- **Membership:** appointed by Tribal nations and inter-Tribal organizations through a process they design. Members are never chosen by the steward.
- **Authority over Tribal-related content**, defined by the Council as at least: content about Tribal governments as employers, Tribal law and jurisdiction, consultation, Indigenous knowledge, cultural resources, and data from or about Tribal programs.
- **Consent.** Tribal-related content may not be published, changed or ingested without the Council's consent. The Council may require removal or restriction at any time. It may require Local Contexts Labels or Notices.
- **No override.** Its decisions cannot be overridden by the Editorial Board or the Advisory Council.
- **Support.** The steward funds its participation (honoraria, travel, a 0.5 FTE liaison who reports to the Council).
- **Interim rule.** Until the Council exists, no new Tribal-related content is published. v1 content in this category is held, not released. [J; consistent with TN v1 assessments, e.g., TN on 5.3.2 and 6.5.1]

**3.6 Module Stewards.** Organizations that hold a Module Stewardship Agreement (Art. 4.7).

**3.7 Validation Panels.** SME and Delphi panels convened under IO's protocols. Panels advise and their results are published. Content decisions remain with the Editorial Board.

**3.8 Sentinel Network.** 40–80 practitioners recruited through partner societies, corps and agencies. They report change signals in an annual cycle, and the steward pays honoraria. This carries forward v1's Task 22 concept [E: AS-049, AS-053] (see `v1_assessment.csv`).

**3.9 Community.** Anyone may open issues, comment, propose changes and contribute under Article 5.

### Article 4. Decision-making
- 4.1 **Lazy consensus** for administrative changes: a proposal with no objection in 7 days passes.
- 4.2 **Rough consensus** for content changes in the Editorial Board. If consensus fails, a 2/3 vote of members present (quorum 2/3). The chair records objections and how they were addressed.
- 4.3 **Major releases** need an Editorial Board 2/3 vote **and** Advisory Council ratification (2/3).
- 4.4 **Tribal-related decisions** need Tribal Council consent first (Art. 3.5).
- 4.5 **Disputes.** The Editorial Board decides. Appeals go to the Advisory Council's executive group, whose decision is final. During v2 construction (Phases 1–3), CA resolves disputes per the team charter.
- 4.6 **Transparency.** Decisions and rationale are published in the repo's decisions log within 14 days.
- 4.7 **Module Stewardship Agreement.** Terms:
  - (a) Use the core schema, namespaced IDs and core vocabularies.
  - (b) Run at least one review cycle per year on the core cadence.
  - (c) Meet the core evidence standard.
  - (d) Name an SME pool and a contact.
  - (e) Accept conformance checks.
  - (f) Termination: a steward that misses two cycles, or withdraws, returns the module to the core (**orphan clause**).
  - (g) No exclusivity: a module cannot be licensed differently from the core.

### Article 5. Contribution and change-request process
5.1 **Who.** Anyone. Federal employees' contributions are U.S. government works. [J] Contributors certify origin using the Developer Certificate of Origin (DCO). Inbound terms equal outbound terms; no copyright assignment.

5.2 **Change types:**
- E — errata;
- C — crosswalk update;
- S — substantive add or modify (task, competency, indicator, role variant);
- D — deprecate;
- X — structural (schema or vocabulary);
- T — Tribal-related (routed to the Tribal Council first).

5.3 **Required in a request.**
- Problem and proposed change.
- Affected IDs and related content. A new task must name its competencies and role profiles, following NICE practice. [E: AS-025]
- Evidence with E/J/S labels.
- **For S and X:** at least two independent sources, including at least one demand signal (posting, PD, plan requirement, staffing plan) or SME panel data.
- Effect on adopters (breaking or not).
- Proposed sector-actor variants.

5.4 **Stages and service levels:**

| Stage | What happens | Time limit |
|---|---|---|
| Proposal | Issue opened with template; auto-checks | — |
| Triage | Editor assigns type, owner, priority; may reject as out of scope with reasons | ≤30 days |
| Candidate | Drafted change published for comment | 30 days (minor) / 60 days (major or X) |
| Adjudication | Each comment marked Noted / Accepted / Accepted with modification / Deferred / Rejected [E: AS-025] | ≤30 days after comment closes |
| Decision | Editorial Board (or module steward within its module) | Next scheduled meeting |
| Release | Bundled into the next release per Art. 6 | — |

Fast track:
- E and C changes may go straight to the next patch release after editor review.
- T changes pause until the Tribal Council decides.

5.5 **Signals intake.** Sentinel reports, NLP drift reports (IA), O*NET and ESCO releases, OPM standard changes and policy events enter as **signal records** in L5. A signal triggers a change request only when it meets the evidence standard LM sets (CA question to LM). [J]

5.6 **Use-tier labels.** Each competency and role profile carries a validity tier set by IO: *exploratory*, *training-grade* or *selection-grade*. Selection-grade requires documented job-analysis evidence. Kits state the tier. [J]

### Article 6. Versioning and release cadence
6.1 **Release identifiers.** MAJOR.MINOR.PATCH for the whole release, following NICE MAJOR.MINOR.ADMIN. [E: AS-026] Modules carry their own MINOR.PATCH inside a core MAJOR.

6.2 **IDs.**
- Never reused.
- Deprecated IDs are kept as tombstones with `status`, `deprecated_in` and `replaced_by`.
- Each record states the release it was created and last changed in. DE and IA define the format.

6.3 **Cadence: what adopters can plan around** [J; precedents E: AS-026, AS-004]:

| Release | Contents | Cadence | Notice |
|---|---|---|---|
| PATCH | Errata, crosswalk refreshes (e.g., re-pinned to new O*NET releases), signal-layer updates | As needed; crosswalks at least quarterly (CM M-30) | Release notes |
| MINOR | Additive content, new role variants, deprecations with replacements | **Once a year, fixed month (proposed: April)**, after the annual sentinel cycle and before federal fiscal-year planning | Candidate published ≥60 days before |
| MAJOR | Breaking structural change | **No more than once every 3 years**, announced ≥12 months ahead | Migration guide and crosswalk old → new |

6.4 **Support window.** Each MAJOR is supported (errata, crosswalk refresh) for **≥24 months** after its successor ships. Adopters using EMST in assessments may pin a version until their next job-analysis refresh. [J]

6.5 **Every release includes:**
- a human-readable change notice ("does this affect me?");
- machine-readable diffs;
- a DOI;
- signed artifacts and provenance (DE, CP);
- an accessibility conformance report for the views (CP).

6.6 **Annual "State of Environmental Work"** report published with each MINOR. It is the main convening and communication product.

### Article 7. Conflicts of interest
- 7.1 All body members file an annual disclosure: employment, funding, consulting, vendor relationships, and roles in organizations whose standards EMST crosswalks.
- 7.2 Members recuse themselves from decisions where they or their organization would gain directly, e.g., a vendor mapping, a client's role profile, or a society's credential crosswalk.
- 7.3 **Funders** have no vote on any body. Funding agreements must include an editorial-independence clause.
- 7.4 **Vendors and consultancies** hold at most two Advisory Council seats and no Editorial Board seats.
- 7.5 **Fee-for-service firewall.** Staff delivering paid services may not serve as decision-makers on change requests arising from that engagement. Paid work never buys content changes. Any content change from paid work goes through Article 5 like any other request.
- 7.6 Violations go to the Advisory Council executive group. Remedies range from recusal to removal.

### Article 8. Licensing (recommendation with reasons)

| Option | For | Against | Verdict |
|---|---|---|---|
| **CC0 1.0** for everything | Maximum reuse. No attribution friction for agencies writing standards or for vendors embedding data. Matches CEQ standard and OpenLMP [E: AS-046, AS-047]. Federal works are effectively public domain anyway [J] | No enforceable attribution, so adopters drop version citations. Provenance, and with it legal defensibility, weakens ("which version did this PD use?"). Weaker funding case (visibility). Altered copies can circulate as "EMST" (trademark mitigates) | Best for **schema, identifiers, vocabularies and crosswalk tables** |
| **CC BY 4.0** for content | Requires attribution with version, which supports provenance, adoption measurement and funder visibility. Permits commercial use. O*NET's database is widely embedded under CC BY 4.0 [J, not re-verified]. v1 already announced CC BY 4.0 [E: AS-055] | Attribution stacking in large derived databases. Some legal reviews take longer | Best for **competency, task, indicator and role-profile text and the documentation** |
| **CC BY-SA 4.0** | Keeps derivatives open | Share-alike blocks embedding in proprietary HR systems and some government standards | Reject [J] |
| **Proprietary / SFIA-style commercial licence** | Direct revenue [E: AS-030] | Contradicts the open-standard mission; blocks vendor-neutral adoption | Reject for the core. Use revenue from services instead (sustainability model) |
| **Apache-2.0** for code | Permissive with an explicit patent grant; matches OpenLMP [E: AS-046] | — | **Adopt** |
| **MIT** for code | Simpler | No patent grant | Second choice |

**Recommendation** [J]:
1. Content (L1–L3 text, documentation): **CC BY 4.0**, with a recommended citation that includes the release ID and DOI.
2. Schema, IDs, controlled vocabularies (L0) and crosswalk link tables (L6): **CC0 1.0**, so agencies and vendors can embed them without legal friction.
3. Code: **Apache-2.0**.
4. **Tribal-related content** is excluded from the open licenses unless the Tribal Council authorizes otherwise, and is labeled as it directs.
5. **Third-party content** keeps its own terms (e.g., O*NET-derived fields keep O*NET's license; OPM text is public domain).
6. **Resolve v1's contradiction** before the first release. The v1 repository was created with the CC0 dropdown while its README states CC BY 4.0. [E: AS-048] CP flagged the same issue. [E: CP per product_strategy]

**Disagreement noted.** OpenLMP uses CC0 for all data. The case for CC0 everywhere is real: it gives the fastest federal embedding. The trade-off is weaker provenance and visibility in exchange for less friction. Splitting by layer gets most of both. CA decides.

### Article 9. Name, marks and conformance
- 9.1 "EMST" and its logo are held by the Steward **in trust** for the Consortium. If the Steward withdraws, they are assigned to the successor (Art. 11).
- 9.2 Anyone may say they "use" or "map to" EMST with a release ID.
- 9.3 "EMST-conformant" and "EMST-mapped" claims require a conformance check against published criteria. This is a value-added service; fees are listed publicly and waived for small NGOs, Tribes and public agencies under a size threshold.
- 9.4 Modified versions may not be called EMST.

### Article 10. Amendments
Amendments require a 2/3 vote of the Editorial Board **and** a 2/3 vote of the Advisory Council, after a 60-day public comment. Amendments to Article 3.5, or to any Tribal-related provision, also require the Tribal Council's consent.

### Article 11. Succession and continuity (the anti-ASC clause)
- 11.1 **Host Agreement:** five-year renewable term; ≥12 months' notice of withdrawal; obligation to transfer staff records, funds held for EMST, domain names, accounts and marks to a successor.
- 11.2 **Successor selection** by the Advisory Council, from a standing list of at least two pre-qualified alternates. The list is reviewed annually and includes a fiscal-sponsor or open-standards foundation option.
- 11.3 **Continuity by design:**
  - Public repo mirrored to at least two places, plus archival deposit (e.g., Zenodo DOI per release).
  - Reproducible build; documented runbooks.
  - Credentials held by at least two people at two organizations.
- 11.4 **Maintenance floor.** If funding falls below the planning budget, the Steward moves to the published floor (`sustainability_model.md`: about 3 FTE; annual MINOR; quarterly crosswalk patches; Tribal Council support kept) before cutting anything else. It notifies adopters 6 months ahead of any change to cadence.
- 11.5 **Five-year review** of the charter, the host and the funding mix, with a public report.
