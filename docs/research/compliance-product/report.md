# CP Report: Compliance-Minimizing Architecture and Product Direction for EMST v2

**Role:** Security, Privacy & Government Compliance Lead + Product & UX Lead (CP) · **Date:** 2026-10-23 · **Phase:** 2

**Evidence labels** follow TEAM_BRIEF §3:
- **[E]** cites a source I read (IDs resolve to `sources.csv`).
- **[J]** marks my judgment, with its basis stated.
- **[S]** marks speculation.

**How the files fit together.** This report holds the compliance findings, the recommended architecture, the answers to CA's questions and the required closing sections. Detail lives in the companion files:

| File | Contents |
|---|---|
| `compliance_matrix.csv` | 39 requirements: federal, state/local, open data, personnel data, AI |
| `product_strategy.md` | Vision, users and JTBD, principles, positioning, roadmap, product risks. It also contains the full proposal text (P-CP-01…20), which is summarized in §12 here. |
| `mvp_spec.md` | Scope, architecture detail, IA, screens, data needs, accessibility, data visualization and uncertainty standard, technology appraisal, analytics, metrics, release plan |
| `user_research_plan.md` | Methods, recruitment, tasks, measures, cadence, and the route from findings to taxonomy change |
| `v1_assessment.csv`, `ecosystem.csv`, `sources.csv` | Structured outputs |
| `scripts/` | Generators for the CSVs, so they can be reproduced |

---

## 0. Summary

1. **Adoption stalls at procurement when EMST holds data about people or agencies.** The heavy regimes all turn on two triggers:
   - a service that collects or maintains *Federal information on behalf of an agency* (FedRAMP, FISMA ATO) [E: CP-015, CP-016];
   - records about individuals that are retrieved by an identifier (Privacy Act SORN, PIA, state public-employee data law) [J: CP-040, CP-077].

   The regimes that apply whatever the architecture (accessibility, supply-chain transparency, licensing) are cheap if they are designed in now. My recommendation is therefore architectural:
   - an **open data core**;
   - a **static, local-first public explorer** that never receives personal or agency data;
   - optional **run-it-yourself kits** that agencies operate inside systems they have already authorized;
   - **no hosted personnel-data service**. [J]

2. **Several requirements changed in 2025–26:**
   - **ADA Title II:** web deadlines moved to **April 26, 2027** (population 50,000 or more) and **April 26, 2028** (smaller entities and special districts). The standard is still WCAG 2.1 AA [E: CP-012].
   - **Secure software:** **OMB M-26-05** (January 23, 2026) rescinded M-22-18 and M-23-16 [E: CP-014].
   - **FedRAMP:** the **Consolidated Rules for 2026** replace "authorization" with "certification", add Classes A–D, and add a Program path that needs no agency sponsor [E: CP-016, CP-018].
   - **LLM procurement:** **M-26-04** adds transparency terms to LLM procurement [E: CP-021].
   - **AI in hiring:** **OPM's memo of August 27, 2026** treats AI-drafted PDs as generally *not* high-impact when officials review, revise and adopt them. AI-assisted steps remain subject to 5 CFR 300.103 [E: CP-022].

3. **Accessibility.** Section 508 still incorporates WCAG 2.0 AA. WCAG 2.2 is the current standard (ISO/IEC 40500:2025); there will be no 2.3, and WCAG 3 is years away [E: CP-025, CP-026]. Targeting **WCAG 2.2 AA** satisfies 508, Title II and HHS §504 (first deadline May 11, 2026) [E: CP-013; J].

4. **Product.** The first user is a **training or program lead in an NGO pilot organization**. The MVP, the **Role Change & Development Planner**, has three views:
   - role change;
   - a local-first gap check;
   - a pathway across sector actors.

   It covers 12–15 function × level role profiles on three corridors that end in state and federal roles. The pilot therefore tests what state and federal training officers will use next. [J]

5. **Uncertainty is shown, never smoothed.** Every v1 exposure value is a single analyst's judgment, made with LLM assistance. For 75 of 222 competencies the exposure data are reconstructed or retrospective, and 33 are flagged "contested" [E: CP-007]. The MVP shows tier, agreement and date on every judgment and never turns single-rater data into headline percentages. v1's Flourish story did exactly that [E: CP-004, CP-003].

6. **Limitation.** The shared web-search budget ran out after 9 of my searches. New URLs that had not come back from a search were blocked for this background agent; this included the primary M-25-21 PDF and designsystem.digital.gov. I compensated in two ways:
   - I read primary text from official open repositories: FedRAMP's 2026 documentation source, W3C WAI, USWDS, Digital.gov, 18F and OpenSSF.
   - I checked current versions in package registries.

   Requirements I could not re-verify are labeled [J] and marked `unverified` in `sources.csv`. They are mainly:
   - the current status of state AI-employment laws;
   - GovRAMP details;
   - the status of M-23-22;
   - SORN specifics;
   - comparable tools' current features.

   SL, FH and a follow-up session should verify these before the federal and state phase.

---

## 1. Method and source choices

I read the charter, the brief, and CA's audit and hypotheses first [E: CP-001–CP-003]. I then read the v1 platform artifacts and conversation records [E: CP-004–CP-009] and CM's early transferability outputs [E: CP-010].

Source priorities, in order:
1. **Regulatory text and the agencies' own documentation repositories.**
   - FedRAMP/2026-markdown, commit of 2026-10-14. The legacy repository marks itself "historical reference only" and points here [E: CP-016, CP-020].
   - w3c/wai-website, 2026-10-22 [E: CP-025].
   - uswds/uswds-site, 2026-10-19 [E: CP-026, CP-027].
2. **Law-firm summaries**, only where the primary text was blocked: CP-013, CP-014, CP-018 and CP-023, labeled Medium.
3. **One vendor page**, for 20x pipeline dates only, rated Low (CP-019).

The Digital.gov and 18F guidance on PRA and ATO is useful but partly dated. One Digital.gov page carries a review flag from 2025, and 18F's guide has not been maintained since its 2025 reorganization. I use these sources only for statutory points that are stable [E: CP-029–CP-033].

I did not conduct user research. The personas are clearly labeled CP drafts and are to be merged with CM's.

---

## 2. What changed in 2025–26 (verified)

| Requirement | Status as of October 2026 | Evidence |
|---|---|---|
| FedRAMP scope | Cloud services that "create, collect, process, store, or maintain Federal information on behalf of a Federal agency". Excluded: "widely available services that provide commercially available information to agencies, but do not collect Federal information"; negligible-risk ancillary services. The agency decides. | [E: CP-016 (verbatim M-24-15 §III); CP-015] |
| FedRAMP CR26 / 20x | Launched June 24, 2026. Effective for new 20x certifications from July 4, 2026; mandatory January 1, 2027. New Rev5 certifications end June 11, 2027. Class A is presumed adequate for "processing public information". Program path available. | [E: CP-016, CP-018; CP-019 Low] |
| Secure software | M-26-05 rescinds M-22-18 and M-23-16. Policies are now agency-specific and risk-based. The CISA form is optional. An SBOM can be required on request. SSDF is a reference. Inventories are mandatory. | [E: CP-014] |
| AI use and acquisition | M-25-21: employment access is a presumed high-impact area with 7 minimum practices due within 365 days. M-25-22: data rights, anti-lock-in, and no training on non-public agency data without consent. M-26-04: LLM solicitations require an acceptable-use policy, model, system or data cards, and a feedback mechanism; the memo sunsets after 2 years. | [E: CP-023, CP-024, CP-021] |
| AI in federal hiring | OPM memo of August 27, 2026: PD drafting is generally not high-impact with real review. 5 CFR 300.103 still applies. Applicant data may be processed only in authorized tools. Use must be auditable. | [E: CP-022] |
| Section 508 / WCAG | 508 = WCAG 2.0 AA. WCAG 2.2 = ISO/IEC 40500:2025. EN 301 549 (2026) uses 2.2. No 2.3 is planned. The WCAG 3 Working Draft dates from September 2026. | [E: CP-026, CP-025] |
| ADA Title II | Interim final rule of April 20, 2026 sets April 26, 2027 and April 26, 2028; WCAG 2.1 AA. The rule covers content provided through vendors. Comments were due June 22, 2026. | [E: CP-012, CP-013] |
| HHS §504 web rule | First compliance date May 11, 2026; not extended as of April 2026. | [E: CP-013] |
| PRA and research | Identical questions to 10 or more persons need clearance. Federal employees acting in their role are exempt. Direct observation is generally not "information". | [E: CP-029, CP-033] |

**Retire from team references:**
- M-22-18 and M-23-16;
- the terms "FedRAMP Authorized" and "Ready";
- any plan that assumes Title II compliance by April 24, 2026;
- the FedRAMP legacy documentation site [E: CP-014, CP-016, CP-020, CP-012].

---

## 3. When is an ATO, FedRAMP, SORN or PIA needed?

| Adoption pattern | FedRAMP | Agency ATO | SORN / PIA |
|---|---|---|---|
| Staff read the public site or download a release | No: an information provider that collects no Federal information [E: CP-015, CP-016] | No new ATO [J] | No |
| An agency loads release files into its HCM or LMS | No | A change within that system's existing ATO, plus inventory under M-26-05 [E: CP-014; J] | Covered by the existing SORN [J] |
| An agency rehosts the static site on .gov | No | Covered by the hosting platform's ATO [J] | PTA only (no PII). Federal website rules apply [J: CP-052, CP-053] |
| An agency runs a Tier 2 kit in its own environment | Only via components it already uses | Within its authorized environment | PTA; PIA if PII is processed; SORN check; AI inventory and impact assessment [E: CP-024; J] |
| An NGO hosts a SaaS holding agency staff profiles | **Yes** | **Yes** | **Yes**, at every agency, plus GovRAMP for states [E: CP-016; J: CP-048] |

**Design consequence.** The public explorer must never collect Federal information:
- no uploads;
- no accounts;
- no server-side processing of input;
- no query logs.

FedRAMP treats public AI chatbots that handle only public information as out of scope when users are told not to enter sensitive data [E: CP-015, CP-017]. Even so, an "Ask EMST" assistant would collect and log queries, so I keep it out of the MVP [J].

---

## 4. Recommended architecture: four tiers (P-CP-01)

```
TIER 0  OPEN CORE (no personal data, ever)                  owner: DE, IA
  GitHub repo = single source of truth: CSV/JSON/JSON-LD (SKOS), schemas, validators
  Signed, versioned releases + DOI + SBOM + provenance attestation + delta file
  License: CC0 data/vocabularies, Apache-2.0 code; third-party license register
                 |  build in CI from a tagged release
                 v
TIER 1  PUBLIC EXPLORER (static, local-first)               owner: CP
  Pre-rendered HTML; no server, accounts, cookies, third-party requests or analytics
  Gap check runs in the browser; answers stay on device; save/load as a file
  USWDS 3 tokens/components; WCAG 2.2 AA; Pagefind client-side search
  Rehostable unchanged on .gov (DAP via one include)
                 |  download kits; import release files
                 v
TIER 2  RUN-IT-YOURSELF KITS (adopter-operated)             owner: IA (+CP docs)
  Skills-library import files for HCM/LMS; team gap workbook (min cell 5);
  PD drafting kit; later a skills-inference pipeline with person confirmation.
  Each kit: PTA/PIA starter, SORN data-element inventory, AI system card,
  impact-assessment inputs, ACR for any UI, SBOM

TIER 3  HOSTED PERSONNEL-DATA SERVICE                       NOT ON ROADMAP
  FedRAMP (Class B/C) + agency ATOs + SORNs + PIAs + GovRAMP + M-25-21 review
  + state AI-employment laws. If ever needed: partner with a certified platform.
```

**Standing rules** (P-CP-02; proposed as an architectural invariant):
1. The EMST steward holds no personal data.
2. Person-level computation happens locally.
3. No user input goes into URLs [J: CR-13].
4. No third-party requests are made at runtime. The Google Fonts call in the OpenLMP dashboard is the pattern to avoid [E: CP-011].
5. Every judgment carries its provenance (tier, rater type, date, method) [E: CP-003].
6. EMST is for development use only: it never ranks, scores or screens people [J: CR-19].

**Why not "just collect an email"?** In an NGO pilot, server-side profiles add little value for users. They would cost a privacy notice, breach duties and possible state privacy exposure for an NGO steward [J: CP-078]. Above all, they would put up a permanent barrier for federal and state staff, who would need an agency determination before entering their own data. Local-first delivers most of the value at almost none of the compliance cost [J].

---

## 5. Personnel data and AI inference

**Why this data is sensitive:**
- Skills profiles are PII. Once an agency stores them they are Privacy Act records [J: CP-040].
- In a state agency they may be disclosable under public-records law unless classified private [J: CP-077].
- Shared with a non-federal party, they become CUI [J: CP-076].

**Inferring skills from a person's documents adds further obligations:**
- Presumed high-impact status under M-25-21 if the output drives employment decisions [E: CP-023].
- OPM's rule that applicant data be processed only in authorized tools [E: CP-022].
- State AI-employment duties [J: CP-043–CP-047].
- Proxy risk. Tool vintages can stand in for age, and gaps in physical field tasks can stand in for disability [J].

**Constraints PC-1 to PC-8** (detail in `mvp_spec.md` §2.5):

| # | Constraint |
|---|---|
| PC-1 | EMST never receives person-level data. The team accepts no agency personnel data, including for pilots. |
| PC-2 | Person-level computation runs on the device (Tier 1) or in the adopter's authorized system (Tier 2). |
| PC-3 | Team views are aggregates with a minimum cell size of 5. |
| PC-4 | Profiles and signals describe work, not workers. PII is stripped when signals are ingested. |
| PC-5 | Skills inference from documents about an individual is deferred. If built, it is Tier 2 only, with person confirmation, visible evidence spans, no default storage and published error rates. |
| PC-6 | AI-assisted builders produce drafts that a human adopts. Exports record that AI assisted and which release was used. |
| PC-7 | Outputs are labeled "not a selection instrument". |
| PC-8 | Tribal-governed content follows TN's protocol and CARE. |

---

## 6. Accessibility plan (P-CP-05)

**Target:** WCAG 2.2 AA for the site, exports and kit UIs. This is a superset of 508's 2.0 AA and of the 2.1 AA required by Title II and §504 [E: CP-025, CP-026, CP-012, CP-013].

**New 2.2 criteria that matter here** [E: CP-025; J]:

| Criterion | What it means for EMST |
|---|---|
| 2.5.7 Dragging movements | Pathway and team views need alternatives to dragging |
| 2.5.8 Target size | Rating controls must be at least 24 px |
| 2.4.11 Focus not obscured | Sticky header must not hide focused elements |
| 3.3.7 Redundant entry | The chosen role carries through all views |
| 3.2.6 Consistent help | Help appears in a consistent place |

**Charts** follow USWDS guidance [E: CP-027]:
- the message stated in text;
- a table behind every chart;
- no hover-only information;
- no color-only encoding.

**Procurement:** an ACR (VPAT, 508 and WCAG editions) per major release, plus an accessibility statement [E: CP-026].

**Testing:**
- automated checks in CI;
- manual keyboard and screen-reader passes before release;
- at least 2 assistive-technology users in each research round.

Automated checks verify presence, not meaning [E: CP-027].

---

## 7. Security packet (P-CP-03, P-CP-04)

M-26-05 replaced the single federal attestation with agency-by-agency risk policies [E: CP-014]. Answer agency questionnaires once, publicly, in a packet that ships with each release:

1. An applicability statement covering FedRAMP and ATO, with a data-flow diagram [E: CP-016].
2. An SBOM and release checksums [E: CP-014].
3. An SSDF practice mapping and a voluntarily completed CISA form [E: CP-014].
4. OpenSSF Scorecard results, targeting 7 or higher. Pin Actions by commit SHA (OpenLMP pins by tag), use least-privilege tokens, protect branches, run Dependabot, and sign releases with provenance [E: CP-034, CP-011; J: CP-060].
5. SECURITY.md, a vulnerability-disclosure policy, and security.txt [J: CP-059].
6. A Content-Security-Policy set through a meta tag, because GitHub Pages cannot set response headers. Moving to a host that can is a DE decision, and that host becomes a third party [J: CP-080].

Cost: about 3–5 person-days to set up and about 1 hour per release to maintain [J].

---

## 8. State and local readiness (P-CP-18)

| Area | Position |
|---|---|
| Security | Tiers 0–1 hold no state data, so GovRAMP, TX-RAMP and AZRAMP should not apply. This is [J]; confirm with one pilot-state CISO [J: CP-048, CP-049]. |
| Accessibility | Title II reaches content a state entity provides "through vendors". When a state embeds EMST, EMST's conformance becomes the state's legal exposure, which makes the ACR an adoption asset [E: CP-013; J]. |
| Employee data | Tier 2 kits assume stored individual ratings may be exposed to public-records requests, and default to aggregates [J: CP-077]. |
| AI laws | Colorado (delayed to June 30, 2026), Illinois HB 3773 (January 1, 2026), California CRD ADS regulations (October 1, 2025), Texas TRAIGA (January 1, 2026) and NYC LL 144. None were re-verified for October 2026 [J: CP-043–CP-047]. The development-use boundary is the durable mitigation. |
| Deliverable | A one-page brief per pilot state for the CIO, CISO and ADA coordinator. SL completes the state-law table. |

---

## 9. Licensing and provenance (P-CP-08)

**The v1 conflict.** The v1 setup guide selected CC0 in GitHub while stating CC BY 4.0 in the README [E: CP-005]. Two licences on one dataset invite counsel to say no.

**Recommended licences:**
- **Data and vocabularies:** CC0. This matches OpenLMP [E: CP-011] and lets agencies and HCM vendors embed EMST without attribution chains.
- **Documentation:** CC0 or CC BY 4.0.
- **Code:** Apache-2.0.

**Third-party material:**
- Exclude O*NET text (CC BY 4.0), ESCO and licensed posting data from the CC0 dedication, and list them in a register.
- Crosswalks store external IDs, not copied text [J].
- Federal works are public domain under 17 U.S.C. 105 [J: CP-055]. State documents need a rights field, as OpenLMP records [E: CP-011].

**Citation.** Every page and export shows the release ID and DOI (CR-11, CR-39).

DE and AS decide the licences. I flag this as a blocker for procurement.

---

## 10. Product direction in brief

- **First user (U1):** a training or program lead at an NGO pilot organization. Examples: a corps, land trust, watershed or restoration nonprofit. U1 plans development for field and program staff and wants to show them routes into state and federal careers.
- **Secondary users:** supervisors (U3) and early-career staff (U2) [J].
- **Why U1 comes first.** U1's job contains the state training officer's job, with different role variants. U1 can act tomorrow without a compliance review, and one pilot organization exercises all three pilot personas [J].
- **Not a taxonomy browser.** Users enter by role and see 10–20 relevant competencies, with depth one click down. This follows CA principle 6 [E: CP-003].
- **Positioning.** O*NET and CareerOneStop describe national occupations for job seekers [J: CP-061, CP-062]. Vendor skills clouds infer skills from personnel data inside one employer [J: CP-066]. EMST is the **open, domain-specific reference layer** that shows how environmental roles change and how people move among sector actors. It is built to be imported into the systems adopters already run: **be the content, not the platform** [J].

---

## 11. Answers to CA architecture questions (architecture_hypotheses.md §6 "CP", and DP-6)

The full data-field tables are in `mvp_spec.md` §5–6. The answers, in brief:

### Q1. Which three views does the first user need, and what does each require of the data model?

From the product side I support CA's hybrid lean: a task-and-role spine with competency packaging. All three views are role-anchored and computed from tasks, so a competency hub without a task layer could produce none of them [J].

**View 1: "How is this role changing?"** This is v1's forester prototype, generated from data [E: CP-006]. It requires:

| Requirement | Notes |
|---|---|
| L3 role profiles with sector-actor variants | Plus alternative titles and a plain summary of 60 words or fewer |
| Role–task links with **time share** | Drives "how much of the job"; the prototype used duty percentages |
| L2 tasks | With work function and craft |
| **Several attributed L5 exposure assessments per task** | Rater type, date, method and codebook version, confidence, contested flag, so the view can show tier and agreement |
| L5 change signals | With **an interval or n** and a coverage note |
| Emerging items | With lifecycle status |
| A descriptive "stays human" rationale | Descriptive, not normative; CA's D7 critique [E: CP-003] |
| Computed role summaries | Generated at build time |

**View 2: "Where are the gaps?"** (individual; team from shared files). It requires:

| Requirement | Notes |
|---|---|
| Role–competency links | Target level per role level, criticality, and **served_task_ids**, so a gap can be tied to a changing task |
| L1 levels with 3–5 **observable, anchored indicators** per level | IO decides the scale (DP-4). v1's generic statements cannot be self-rated [E: CP-003 §4.3] |
| Optional learning hooks | Owned by LC |
| **No person entity in the model** | Ratings exist only as a versioned client-side file: `{release_id, role_variant_id, level, ratings[], schema_version}` |

**View 3: "Where can this role lead?"** It requires:

| Requirement | Notes |
|---|---|
| Computed pathway edges between role variants | CM decides the similarity basis (CM Q1). Includes an asymmetric gap list; CM's family-level `dest_core_absent_in_origin` is the prototype [E: CP-010] |
| A **computed vs observed** flag | Observed only as aggregates with a minimum count of 5 |
| First-class friction attributes | Dated and sourced |
| **Dated crosswalks** on destinations | OPM consolidates series through September 2027 [E: CP-003] |

**Cross-cutting rule:** every number on screen traces to stored, attributed records in a tagged release and is computed at build time, never hand-typed [J; E: CP-003].

### Q2. What privacy constraints apply if role profiles or signals ever touch person-level data?

PC-1 to PC-8 (§5) apply. Architecturally:

1. The EMST schema has **no person entity**. Person-level structures exist only as client-side file formats or as Tier 2 kit schemas that adopters instantiate in their own authorized systems.
2. Signals from PDs, postings and plans are **de-identified at ingestion**. Only derived signals and source hashes are stored.
3. **Observed career transitions** come only from consented research cohorts or from aggregates that agencies compute internally, stored as aggregate edges with a minimum count of 5.
4. If person-level processing ever runs on EMST infrastructure, every regime in §3's last row applies. That is the reason to keep it off.

[J; CR-01, CR-08, CR-10, CR-28, CR-34, CR-35]

### DP-6 (CA open question 4): role-profile grain and first set

- **Grain:** function × level of responsibility (entry, journey, lead), with sector-actor variants. Not OPM series × grade: series are being consolidated and are federal-only, and grade is a pay construct that state classes do not match. Each variant carries dated crosswalks to series, state class and SOC [J; E: CP-003].
- **Size:** 12–15 profiles, about 30–40 variants. That covers three corridors end to end, and each profile can be validated in a 60-minute practitioner session [J].
- **Candidate corridors** (AS confirms against the cohort; FH and SL confirm the destinations):
  1. Field → data: field technician → monitoring or data technician → GIS / remote-sensing analyst.
  2. Field → statecraft: crew or restoration project lead → environmental review / permitting specialist → program manager.
  3. Corps → career: corps member → seasonal technician (state or federal) → permanent technician or specialist. Add fire or water quality if the cohort's employers need them.

  The corridors deliberately cross all three crafts [J; E: CP-009 for v1's pilot framing].

---

## 12. v1 assessment highlights (full list in `v1_assessment.csv`)

| v1 element | Verdict | Why |
|---|---|---|
| Airtable as source of truth | **Retire** | Conflicts with GitHub as source of truth. The free plan blocked scripting, CSV imports broke, and there is a single editor [E: CP-005, CP-009, CP-003] |
| GitBook as public interface | **Retire** (product) | Third-party SaaS and scripts; little control over accessibility conformance or computed views; navigation starts from domains [E: CP-005, CP-009] |
| Flourish story | **Retire** as product channel; one-off use only | Claims run ahead of evidence: "validated against OPM and O*NET", "38% Human-Essential", "68% in transition". CLD counts are stale (49 vs 62). The palette depends on color [E: CP-004, CP-007, CP-003] |
| Forester PD prototype | **Carry** as the flagship, generated from data | Right job and narrative. It needs provenance, uncertainty and accessibility; it has 0 ARIA attributes [E: CP-006] |
| v1 personas | **Change** | Good use contexts, but untested and tilted toward funders and analysts [E: CP-008] |
| Licence selection | **Change** | CC0 vs CC BY contradiction [E: CP-005] |
| "Pre-Delphi" disclosure | **Carry** and generalize into evidence tiers | [E: CP-005] |

---

## Proposals

Full text, including "why" for each, is in `product_strategy.md` §Proposals.

| ID | Proposal |
|---|---|
| P-CP-01 | Four-tier, compliance-minimizing architecture (§4) |
| P-CP-02 | Invariant: the EMST steward holds no personal data, plus the six standing rules |
| P-CP-03 | Agency security packet with every release |
| P-CP-04 | Supply-chain baseline in CI from the first commit (Scorecard ≥ 7; SHA-pinned Actions; signed releases; SBOM) |
| P-CP-05 | WCAG 2.2 AA target; ACR per major release; accessible exports; assistive-technology testing |
| P-CP-06 | Development-use boundary; the "human adopts the draft" pattern for AI-assisted builders (OPM, August 2026) |
| P-CP-07 | Tier 2 kits ship with PTA/PIA starters, SORN data-element inventory, aggregate defaults and AI system card |
| P-CP-08 | Licensing: CC0 data, Apache-2.0 code, third-party register, CARE flag; resolve the v1 conflict |
| P-CP-09 | Claims hygiene: evidence tier and denominator on every public number; retire Flourish headlines |
| P-CP-10 | Retire Airtable as source of truth; no GitBook or Flourish in the product |
| P-CP-11 | Eleventy 3 (or Astro), USWDS 3, Pagefind, build-time SVG + tables, vanilla-JS islands; GitHub Pages; rehostable on .gov |
| P-CP-12 | MVP = Role Change & Development Planner: three views, 12–15 roles, three corridors |
| P-CP-13 | Uncertainty display standard (`mvp_spec.md` §7) |
| P-CP-14 | Analytics without PII: no script in the MVP; DAP-ready |
| P-CP-15 | Research feeds the taxonomy. Triage rule: 3+ participants in 2+ organizations → change request to CA |
| P-CP-16 | PRA-aware, consent-based research; no raw research data in the repo |
| P-CP-17 | Release ID and DOI stamped on every page and export; versioned client-side file formats |
| P-CP-18 | State readiness brief per pilot state |
| P-CP-19 | Strip PII at demand-signal ingestion (IA, LM) |
| P-CP-20 | Defer skills inference from individuals' documents; Tier 2 only, with controls |

---

## Disagreements and trade-offs

Full text is in `product_strategy.md`. In brief:

1. **With the v1 platform plan: polish vs control.** v1's author preferred Flourish's look [E: CP-009]. I trade visual flash for reproducibility, accessibility, privacy and federal familiarity, and will meet the aesthetic bar through deliberate design [J].
2. **With CM (anticipated): telemetry vs privacy.** I propose no telemetry; consented cohorts and agency-computed aggregates instead. Causal evidence will be slower to build [J].
3. **With IA (anticipated): inference vs self-rating.** I defer inference. Self- and supervisor rating against anchored indicators is slower and subject to bias, but it is transparent. IO judges whether it is adequate [J].
4. **With AS (anticipated): shared workspace vs file sharing.** File sharing adds friction but means no hosted personnel data [J].
5. **With CA and LM: showing v1 exposure values.** Show them at task level, labeled "v1 single analyst, unvalidated", with contested markers and a "challenge this" route. Never aggregate them. Hide them if comprehension testing fails [J].
6. **With FH and LC: the PD builder.** The MVP ships a PD skeleton export; the full builder comes in 1.1 [J].
7. **With subject-matter experts' appetite for depth.** The UI shows role-relevant subsets; the full model is downloadable [J].
8. **Licensing: CC0 vs CC BY.** CC0 reduces friction for adopters; CC BY gives partners attribution. I lean CC0 for data [J].

---

## Issues outside my area that affect the vision

- **Stewardship (AS):** someone must own the domain, the GitHub org, the DOI account and the annual ACR in year five. The Australian Skills Classification precedent applies [E: CP-003].
- **Observable proficiency (IO):** the gap check is only as good as its indicators [E: CP-003].
- **Tribal content (TN):** the protocol behind the "not ours to show" flag (PC-8) must come from TN.
- **OPM series consolidation (FH):** destination crosswalks will churn through September 2027. EMST could also feed OPM's later skills-based framework phase [E: CP-003].
- **Demand-signal licensing (LM, IA):** licensed postings can be published only as permitted aggregates [J].
- **Federal staff on GitHub (AS, DE):** agencies need approved terms of service before staff can contribute. Offer email or comment-period routes as well [J].
- **Hosting headers (DE):** GitHub Pages cannot set CSP or HSTS [J].
- **Unverified state AI-law status (SL):** verify before the federal and state phase [J: CP-043–CP-047].

---

## Open questions for the Chief Taxonomy Architect

1. **Proposed DP-11:** adopt "no personal data held by EMST" and the four-tier architecture as binding on all roles, including IA's skills-intelligence work?
2. **DP-6:** accept function × level with sector-actor variants, and 12–15 profiles on three corridors, for the MVP?
3. **DP-8 display policy:** may v1 analyst exposure values appear in the MVP with an "unvalidated" tier?
4. **Licence:** CC0 for data (with DE and AS), decided before the first public release?
5. **Scope:** PD builder in 1.1 rather than the MVP?
6. **Accessibility ownership:** who signs and maintains the ACR after the pilot? It is a release gate.
