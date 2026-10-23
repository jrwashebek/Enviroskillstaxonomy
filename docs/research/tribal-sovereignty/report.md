# Tribal Nations Workforce & Sovereignty: Phase 2 Report (TN)

**Role:** Tribal Nations Workforce & Sovereignty Advisor (TN). **This is a simulated voice.** An AI agent wrote this report from published sources. It does not speak for any Tribal nation, inter-Tribal organization or Indigenous community. It drafts protocols and flags what needs real consultation.
**Date:** 2026-10-23
**Labels:** [E] evidence (source IDs in `sources.csv`), [J] expert judgment, [S] speculation.

**Files in this folder:**

| File | Contents |
|---|---|
| `report.md` | This report |
| `tribal_engagement_protocol.md` | Draft protocol (AI-drafted; requires Tribal review) |
| `indigenous_data_governance_policy.md` | Draft policy (AI-drafted; requires Tribal review) |
| `v1_assessment.csv` | 37 verdicts on v1 elements |
| `candidate_competencies.csv` | 13 candidates |
| `role_signals.csv` | 16 signals |
| `ecosystem.csv` | 30 entities |
| `sources.csv` | 61 sources, 7 of them not accessed and flagged |
| `scripts/` | Generators for every CSV; `lmp_tribal_counts.py`, which reproduces the OpenLMP counts and writes counts only, no component text; `validate_csvs.py`, which checks schemas and confirms that every cited ID resolves |

---

## 0. Evidence limits (read first)

- **Web search budget.** The team-wide web-search budget ran out after my tenth search. After that I could fetch only URLs that had already appeared in search results.
- **Blocked sources.** These primary sources were blocked or never reachable:
  - the CARE Principles text (TN-060);
  - Local Contexts (TN-061);
  - the U.S. Indigenous Data Sovereignty Network (TN-062);
  - FNIGC's OCAP materials (TN-063);
  - the 2022 OSTP/CEQ Indigenous Knowledge Guidance (TN-064);
  - the ACHP 2024 Indigenous Knowledge policy statement (TN-065);
  - the IFMAT IV executive summary file (TN-066).

  Where I use these frameworks, I rely on prior knowledge and label the claim [J]. All seven must be re-read before the draft policy is adopted.
- **Unread organizations.** I did not read the primary materials of NAFWS, CRITFC, GLIFWC, NWIFC, ITEP, NTAA, IAC, AIHEC, NCAI or any Alaska Native organization. As a result, Task 1 coverage of Tribal fisheries, Tribal colleges and Alaska is thin, and I say so in the relevant rows (e.g., TN-S16).
- **Tribally authored sources I did read:**
  - IFMAT IV, commissioned for the Intertribal Timber Council (TN-004);
  - Yakama Nation/ITC testimony (TN-006);
  - NATHPO's analysis of the Section 106 draft rule (TN-036);
  - an Indigenous legal scholar's post (TN-038);
  - Interior's summary of what more than 80 Tribes said about the fire reorganization (TN-009);
  - Tribal leaders quoted in journalism (TN-028, TN-031, TN-033).

  This is fewer Tribally authored sources than the mission calls for. It is a limit of this run, not a judgment that such sources are scarce.
- **Corpus counts.** The OpenLMP counts are mine and reproducible (TN-044). The comparison of planning-rule eras comes from LM's outputs (TN-045).

---

## 1. Where I say no (the veto) and why

I hold a design veto over knowledge or data that is not the project's to include. I use it for five things. [J, resting on TN-018, TN-017, TN-054, TN-014 and the CARE "authority to control" principle, TN-060]

1. **EMST must not define, describe, rank or credential Indigenous knowledge.**
   - **What this means.** No competency, proficiency level, indicator, task statement or exposure score may describe the content of a nation's knowledge (ecological, fire, harvest, place, ceremonial). None may grade anyone's "expertise in TEK."
   - **Why.** Interior's own policy says Indigenous knowledge must be "generally considered authoritative by the Indigenous Peoples who possess it" and that agencies should rely on Indigenous Peoples to interpret it [E: TN-018 §7.5, §7.6.A(5)]. A non-Tribal taxonomy that sets levels for it claims an authority it does not have.
   - **What it removes from v1.** This retires 5.3.2's ladder ("Deep understanding of TEK systems"; "Recognized expert in TEK integration"). It also retires v1's recommendation to credential Indigenous fire stewardship (TN-051).
2. **EMST must not hold confidential Tribal information.**
   - **What this covers.** Site locations, consultation content and material shared in confidence. The rule holds even under access controls.
   - **Why.** Interior warns staff not to overstate what FOIA lets it protect [E: TN-018 §7.6.A(1)(b)]. EMST is meant to be open, forkable and hosted by agencies. Not holding the material is the only protection that works. [J]
3. **EMST must not publish characterizations of named Tribes without consent.** This covers rankings, "capacity," "readiness" and maturity scores, and Tribe-level change indicators. Describing a sovereign government's performance is that government's business. [J]
4. **EMST must not ingest Tribal employers' documents or postings by default.** This includes using them in LLM pipelines. Analysis is a secondary use by a non-Tribal party, and any such use needs a Tribal decision (policy §6). [J]
5. **EMST must not create a "Tribal Natural Resource Management" profession family.**
   - **Why.** Tribal foresters are foresters. Tribal water-quality staff are water-quality staff. What differs is authority, law and accountability.
   - **Where that difference belongs.** It is a sector-actor and jurisdiction distinction, not a separate profession (P-TN-01). A family defined by identity or jurisdiction would also invite the "diversity-program" framing that has exposed Tribal programs to cuts in 2025–26 [E: TN-029, TN-032].

**What I do not veto.** Competencies that describe what **non-Tribal** professionals must know and do when they work with Tribal nations are the project's to write and are needed. Examples are government-to-government consultation, treaty rights, agreements, Indigenous data governance and protecting confidential information. They still pass a Tribal review gate before release (P-TN-03).

---

## 2. Tribal nations as sovereign governments and employers: the workforce picture

### 2.1 Scale and structure

- **Tribes.** There are 574 federally recognized Tribes. [E: TN-028]
- **Environmental programs.**
  - EPA's General Assistance Program (GAP), the main federal source of Tribal environmental program staffing, expects about 520 awards in FY2026, each at least $75,000. [E: TN-001]
  - EPA Region 9 alone serves 148 Tribal Nations. [E: TN-003]
  - GAP funds "core" capacities: administrative, financial management, information management, environmental baseline needs assessment, public education, legal, and technical/analytical. Applicants must submit a staffing plan with full-time equivalents (FTEs) per work component. [E: TN-001]
  - In one region the same notice covers GAP, Clean Water Act §106 monitoring, Clean Air Act §103/105 air programs (including drafting a Tribal air ordinance), CERCLA §128(a) Tribal response programs, drinking water (PFAS priority) and §319 nonpoint source. [E: TN-002] A Tribal environmental office is a multi-media regulatory and technical shop, usually with a small staff. [J]
- **Forestry.**
  - Trust forests cover 19.3 million acres. [E: TN-004]
  - Staffing has moved from the BIA to Tribal governments under self-determination. In 1991 there were 1,479 BIA and 775 Tribal forestry employees. In 2019 there were 436 BIA and 1,394 Tribal. Total staffing was lower. [E: TN-004]
  - Tribal governments are now the main employers of trust-forest professionals (TN-S01).
- **Fire.**
  - Tribes can run fire protection through direct service, Public Law 93-638 contracts, or self-governance compacts. [E: TN-013]
  - Compact parties set the qualification, fitness and safety standards. These "will not be less than NWCG and IFPM standards when mobilized off their Tribal lands". On their own lands, Tribes set standards by agreement. [E: TN-013]
  - The FY2027 request for the new U.S. Wildland Fire Service (USWFS) funds 640 Tribal wildland fire FTEs. [E: TN-011]

**Taxonomy implication.** Tribal governments are **standard-setters**, not only employers. Any EMST statement about qualifications on Tribal lands must defer to Tribal standards. [J, resting on TN-013]

### 2.2 Workforce pressures (what is documented)

| Pressure | Evidence |
|---|---|
| Flat base funding that no longer covers the salaries it was designed for; "neither the BIA nor tribes have adequate funds to pay for staffing" | [E: TN-004, finding C1] |
| Difficulty hiring permanent staff because funding is uncertain; staff shortages; lack of staff housing | [E: TN-004 C2] |
| Indian/Tribal preference raised the number of Native foresters, but some positions go unfilled and some hires come from other disciplines and need NASP preparation | [E: TN-004 C4] |
| Training is mostly technical and compliance-focused | [E: TN-004 C5] |
| Staff are fully committed to ongoing operations, with no capacity for new initiatives | [E: TN-004 H10] |
| "Not enough trained fire management qualified personnel in Indian Country" | [E: TN-004 K10] |
| Trust forests funded at about one third per acre of comparable federal forests; harvests at about 50% of allowable levels | [E: TN-005, TN-006] |
| BIA Yakama Agency failed to fill "many dozens of vacant forestry positions for more than a decade"; one timber sale in a year on about 650,000 forested acres | [E: TN-006] |
| Federal reimbursement backlogs to Tribal fire programs (Santa Ynez Band of Chumash about $8.6M since 2019; Karuk about $3M) | [E: TN-009] |
| "Project-by-project funding is not sustainable for long-term stewardship" | [E: TN-009] |
| 2025 grant terminations and holds hit Tribal science and monitoring positions (Northwestern Band of the Shoshone Nation; Alaska monitoring); a Native student internship program was paused | [E: TN-031] |

### 2.3 Policy shifts in 2025–26 (verified status)

- **EO 14112** (Tribal funding and self-determination, Dec 2023) was rescinded on March 14, 2025 by EO 14236. [E: TN-026] Existing programs continue; new initiatives under it stop. [E: TN-027] Members of Congress protested and asked whether any Tribe had been consulted. [E: TN-029]
- **EO 13175 and the consultation memoranda** "appear to remain in effect," per CRS (Sept 23, 2026). They are unenforceable in court. DOI did not adopt free, prior and informed consent (FPIC) as its consultation standard. OMB M-25-36 (Oct 2025) says deregulatory actions presumptively do not trigger consultation. [E: TN-014]
- **The U.S. Wildland Fire Service.**
  - SO 3443 (Sept 10, 2025) created it. It launched on Jan 12, 2026, and personnel began moving on Feb 8. BIA fire is included. [E: TN-007, TN-010, TN-012]
  - The order directs standardized fire position descriptions and a joint AD hiring program within 180 days. [E: TN-007]
  - Interior says ISDEAA agreements will be honored. It proposes an Office of Tribal Trust. [E: TN-008]
  - Congress has not endorsed the consolidation. [E: TN-010]
- **Section 106 (NHPA).**
  - On July 24, 2026 the ACHP voted 16–5 to advance a rewrite of 36 CFR 800. It is pending OIRA review and was unpublished as of mid-August. [E: TN-041, TN-038, TN-040]
  - NATHPO's analysis: the draft deletes language recognizing Tribes' special expertise, along with references to government-to-government relations, sovereignty and treaty rights. It reduces the role of Tribal Historic Preservation Officers (THPOs). It excludes "noncompact, unimproved natural features." [E: TN-036]
  - Proponents expect fewer delays and a final rule in 2027. [E: TN-042]
- **Co-management.** About 400 co-stewardship agreements existed by December 2024. [E: TN-034] A July 2026 proclamation cut Bears Ears National Monument by 91% and eliminated the Bears Ears Commission. [E: TN-033] I could not verify whether S.O. 3403 and bureau co-stewardship policies remain in force. [S]
- **Indigenous Knowledge policy.**
  - Interior's 301 DM 7 (Dec 2023) and its Handbook (Jan 17, 2025) were in place at the change of administration. [E: TN-018, TN-019]
  - The 2022 government-wide guidance now sits on an archive site, and its live URL was reported removed. [E: TN-021, TN-022]
  - I found no rescission of 301 DM 7. Its 2026 status is **unverified**.
- **Anti-DEI orders.** Agencies issued case-by-case exemptions for Tribal programs on sovereignty grounds. Coverage is uneven. [E: TN-032]

### 2.4 What Tribal employers say they need (published sources only)

These are summaries of published Tribal statements, not my own voice.

**From the 2025 USWFS consultation report** (more than 240 Tribal leaders and staff from more than 80 Tribes; 23 letters) [E: TN-009]. Tribes asked for:
- reorganization "with Tribes, not for Tribes";
- Tribal liaison positions with real decision authority;
- local fire staff and dispatch autonomy preserved;
- Indian preference applied across roles serving Tribal lands, as a political classification;
- year-round positions combining suppression, fuels and recovery work;
- partnerships with Tribal colleges, scholarships and loan forgiveness;
- stable, recurring, compactable fuels funding;
- faster reimbursement;
- inclusion in budget formulation;
- cultural burning protocols and fewer barriers to Tribally led burning;
- Traditional Ecological Knowledge treated as "a core part of fire management, not just stakeholder input," with Tribes recognized as co-managers and knowledge holders.

**From IFMAT IV** [E: TN-004]:
- staffing budgets in funding agreements, at pay equivalent to the federal GS grade;
- base funding that covers staff before project funding grows;
- a "boot camp" for foresters without forestry degrees;
- shared "strike teams" of experts;
- more access to NASP.

**From the Yakama Nation/ITC testimony** [E: TN-006]: "a great need for stronger educational and training programs provided by the federal government."

**Reading these together [J]:**
1. Much of what Tribal employers ask of the wider workforce system concerns **federal-side competence and conduct**: authority, payment, consultation quality, preference law, training access. EMST can serve that need directly with competencies for non-Tribal staff (TN-C02, TN-C04, TN-C08, TN-C09).
2. Tribes ask that their knowledge be treated as core to fire management **on their terms, as co-managers**. That is a request about *who governs*. It is not a request for a non-Tribal taxonomy to codify the knowledge.

### 2.5 What land management plans already demand of the workforce

Counts are from my own run of `scripts/lmp_tribal_counts.py` over the 58,544 OpenLMP components. [E: TN-044]

- **Volume.**
  - 814 components in 84 plans are tagged with Tribal coordination.
  - 102 components in 39 plans mention treaty or reserved rights.
  - 31 components in 24 plans combine confidentiality with cultural or Tribal subjects.
  - 129 carry Section 106 touchpoints.
- **Examples.**
  - The Northwest Forest Plan Aquatic Conservation Strategy (1994) sets a legal test before treaty uses may be restricted.
  - Nez Perce-Clearwater (2025) provides access for treaty-reserved rights (FW-DC-TT-09) and limits personal-use collection where it conflicts with Tribal first-foods uses (FW-GDL-TT-02).
  - Mt. Baker-Snoqualmie (1990) maintains site-location confidentiality under NHPA §304.
  - Ashley (2024) monitors "number of times input or traditional ecological knowledge has been received" (MON-TRIBE-01).
- **Trend.** Plans written under the 2012 planning rule carry about 27 Tribal touchpoints per 1,000 components, compared with about 10 under the 1982 rule. State plans carry about 4. [E: TN-045]
- **Caveat.** Federal (USFS) plans dominate this corpus. 817 of the 842 Tribal-mentioning components I first counted are USFS. [E: TN-044]

**Implications [J]:**
1. Treaty-rights analysis, consultation and confidentiality are **written requirements** in federal plans, yet v1 never names treaty rights outside a sector note. This is evidence for TN-C01, TN-C03 and TN-C11.
2. The Ashley indicator shows that agencies have started counting receipt of Indigenous knowledge as a performance metric. That creates pressure on staff to obtain it. It is a reason for TN-C10 (engage only on the holders' terms) and for the L2 review gate.

---

## 3. Indigenous data governance: implications for a workforce taxonomy

### 3.1 The frameworks

**CARE Principles** (Collective benefit, Authority to control, Responsibility, Ethics) [J; TN-060, not re-read]. CARE complements FAIR: FAIR describes how data are engineered, while CARE asks whose data they are and on what terms. Applied to EMST, the "authority to control" principle means Tribal-related content is governed by a Tribal body with binding authority (P-TN-03), not by project editors.

**Local Contexts TK/BC Labels and Notices** [J; TN-061, not re-read]. As I understand the system:
- **Labels** are applied by communities to express their own protocols.
- **Notices** can be applied by institutions to flag that Indigenous rights or interests may attach.

For EMST:
- The project uses Notices.
- Only Tribes apply Labels.
- Label and Notice identifiers travel in record metadata (policy §7).

**OCAP®** (FNIGC, Canada) [J; TN-063, not re-read].
- It is a useful comparator because it is operationalized with training and certification.
- OCAP is specific to First Nations in Canada and is a registered trademark. EMST should not claim OCAP compliance or apply OCAP to U.S. Tribes.
- It would become relevant only if EMST were used with First Nations.

**Federal policy.**

*Interior's 301 DM 7* is the most specific federal text I read. [E: TN-018] It provides that:
- IK is distinct from local or individual knowledge;
- bureaus must obtain FPIC before receiving and including IK;
- staff explain the purpose, scope, potential reuse, and the Paperwork Reduction Act, FOIA and Information Quality Act implications when seeking consent;
- the agency discloses publicly when it relies on IK;
- agencies rely on Indigenous Peoples to interpret their IK;
- holders are compensated, but IK is inalienable and compensation does not transfer ownership;
- staff are trained before engaging.

*NPS DO 71C* (Nov 2024, amended Mar 2025) provides that [E: TN-017]:
- the NPS "will not collect or record culturally sensitive information without permission of the Tribal representatives";
- managers warn Tribes about FOIA in advance;
- the NPS will "review positions, identify required competencies" for consultation, including co-stewardship and Indigenous knowledge.

*DOI's 2022 consultation policy* requires training before staff participate in consultation. [E: TN-016]

These provisions are federal competency requirements already in force or recently in force. EMST can carry them as evidence for competencies (TN-S15).

**Tribal research codes and IRBs.** Many Tribes regulate research involving their citizens, employees, lands or knowledge. [J; specific codes not read this session, see TN-E28] Any EMST Delphi, survey or interview that includes Tribal employees is research under such codes and may need Tribal approval. That approval is in addition to any university IRB.

### 3.2 What the taxonomy may hold and what it must not

| May hold (with the review gate) | Must not hold |
|---|---|
| Competencies for anyone working with Tribal nations: consultation, treaty rights, trust responsibility, agreements, Tribal jurisdiction, data governance, confidentiality, payment practice, THPO coordination (TN-C01 to TN-C12) | Indigenous knowledge content of any kind, even if public elsewhere |
| Public law, policy and plan requirements about Tribes, dated | Sensitive-place locations or descriptions; consultation content; confidential appendices |
| Aggregate demand signals from federal and state documents | Tribe-level rankings, capacity or readiness scores, and Tribe-identified change indicators without consent |
| Function-level Tribal-employer role variants, **only if** Tribal professionals validate them and the Tribal Advisory Council (TAC) approves (TN-C13) | Person-level data on Tribal employees; citizenship or preference status |
| Tribally contributed content under agreement, with the contributor's license, labels and withdrawal right | Exposure scores on named Tribal programs; LLM-inferred Tribal skills; Tribal documents not offered by the Tribe |

### 3.3 Consent, attribution and Tribally defined competencies

- **Consent.** Consent is per contribution, written and purpose-specific. It is renewed when purpose, license or host changes. A hand-off to a federal host would bring FOIA into play. (Protocol §7.)
- **Attribution.** Attribution follows the contributor and may be none. An individual's view is never presented as a Tribe's position. (Policy §10.)
- **Tribally defined competencies.** If Tribes choose to define competencies for their own workforce, for example Tribal data stewards or cultural fire practitioners, those competencies live in a **Tribally stewarded module**.
  - The module has its own namespace and license.
  - It is governed by its steward.
  - The core does not edit it.
  - The core may reference it only as the steward permits.

  This is the federated "module" in the CA's Option C. It applies with stronger authority than any subsector module, because the steward is a sovereign or its designee. [J]

---

## 4. Assessment of v1

The full verdicts (37 rows) are in `v1_assessment.csv`. Main findings follow.

**4.1 Structural invisibility.** v1 has five sector-application fields. "Public Agencies" absorbs Tribal governments, so Tribal nations never appear as employers or as regulators whose law binds others. [E: TN-046] The one explicit Tribal line in v1 describes Tribal Nations' work in Domain 1 as "Traditional Ecological Knowledge integration, co-management science, cultural resource protection" [E: TN-047 line 216]. That reduces governments that run multi-media environmental, forestry, fire and fisheries programs to suppliers of knowledge. **Verdict: change** (sector actor with subtypes; P-TN-01).

**4.2 Competency-izing Indigenous knowledge (the core problem).**

- **5.3.2 "Indigenous knowledge integration."**
  - The title, the "integration" frame and the ladder ("Understands TEK concepts" → "Deep understanding of TEK systems" → "Recognized expert in TEK integration") turn other peoples' knowledge into a skill tier for non-Indigenous practitioners.
  - The indicator "Recognizes complementarity of TEK and Western science" asks the practitioner to assert a relationship that is the nation's to define.
  - The consulting note "TEK documentation (with consent)" presents recording Indigenous knowledge as a service line.
  - **Verdict: retire.** Replace with TN-C10 (engage with Indigenous knowledge only on its holders' terms) and TN-C07 (data governance). Keep the compensation-and-credit indicator, strengthened. [E: TN-018, TN-017]
- **Domain 5 career progression.** It runs "single culture → cross-cultural → Indigenous knowledge integration" [E: TN-047 line 9698], which places Indigenous knowledge at the top of a non-Indigenous professional's ladder. **Retire.**
- **Domain 1 Cross-Cutting Competency 4 "Integration of Knowledge Systems."** It groups TEK with farmers' and practitioners' knowledge and aims at "genuine synthesis" [E: TN-049]. 301 DM 7 expressly distinguishes IK from local knowledge [E: TN-018 §7.5]. **Change:** keep practitioner and local knowledge in Field Craft's lane, and handle IK through TN-C10.
- **6.5.1 indicators.** "Incorporates traditional ecological knowledge appropriately" and "Integrates traditional knowledge with western science" put an IK-acquisition expectation inside a consultation competency. **Retire** these indicators.
- **3.5.5 indicators.** "Integrates AI insights with traditional ecological knowledge" and "Develops frameworks for integrating AI with Indigenous knowledge" treat IK as an AI input. **Retire.** Replace with a prohibition on ingestion without authorization.

**4.3 AI and confidentiality blind spots in the exposure instrument.**

- 6.5.1 T3 ("Document and incorporate tribal input") is coded A with "AI assists documentation drafting". [E: TN-052]
- 5.3.3 T2 ("Document and map cultural features") is coded Ac (compressive augmentation). [E: TN-046]
- Both treat AI processing of potentially confidential Tribal material as a productivity default.
- The reasoning for H on 6.5.1 T1 and T2 is sound: the accountability-relationship mechanism means government-to-government engagement cannot be delegated. **Carry.**
- **Proposal P-TN-09:** a standing rule that makes exposure on governed-data tasks conditional on Tribal authorization.

**4.4 Cultural resources.** 5.3.3 T1, "Conduct field surveys to identify historic or sacred sites," assigns the identification of sacred sites to the surveyor. Non-Tribal surveyors can identify *potential* resources. Significance is for Tribes to determine. That is reflected in current Section 106 language on Tribal special expertise, which the July 2026 draft would delete. [E: TN-036] **Change** (TN-C11).

**4.5 What v1 gets right.**

- **6.5.1** correctly frames consultation as government-to-government and treats Tribal nations as sovereign. **Carry the intent, rewrite the content.** Its levels are tenure bands ("Expert in tribal relations"). Its expert indicator "Advances tribal capacity" is paternalistic; the federal side controls barriers, not Tribal capacity [E: TN-009, TN-029].
- **7.1.1 Indigenous data sovereignty** is the strongest v1 element in my lane. Its foundational indicator, "data sovereignty is a rights issue, not a data management protocol," is right. **Keep, as a competency for non-Tribal professionals**, with these fixes:
  - Name the separate legal sources: Tribal law; federal policy (301 DM 7 requires FPIC for IK); and UNDRIP. DOI did not adopt FPIC for consultation generally [E: TN-014].
  - Add the FOIA-candor and AI-ingestion indicators.
  - Reword "Advises tribal governments on data governance code development" to "at a Tribe's request, supports…".
  - **Hold publication** until the TAC reviews it (concurring with the CA's needs-evidence verdict, TN-053).
- **7.1.2** correctly lists Tribal governments among parties with standing to authorize interventions. **Carry.**
- **D2 Cross-Cutting Competency 4** (data governance protocols agreed with Tribal governments before collection) is sound. **Carry** and add the AI indicators.

**4.6 The L2 lens (Cultural Rights & Self-Determination).**

- **Strength.** Separating rights from distribution (L2 vs L1) is the right analytical move. **Carry the lens.**
- **Problem 1: conflation.** It runs "Indigenous peoples' and local communities' collective rights" together. In the U.S., federally recognized Tribes hold a political, governmental status that local communities do not [E: TN-029]. Merging them blurs the trust and treaty basis of obligations.
- **Problem 2: FPIC.** It grounds the lens in FPIC as if FPIC were the operative U.S. standard. Practitioners need to know which obligation applies: Tribal law; federal law and policy (consultation; FPIC only where policy adopts it, as 301 DM 7 does for IK); or international standards. [E: TN-014, TN-018]
- **Problem 3: missing triggers.** It has no triggers for AI ingestion, records disclosure or workforce data about Tribal programs.
- **Population.** Only 4 of 222 competencies are tagged. 7.1.4 (AI governance) is tagged L2 = A (absent). That is wrong: AI-adoption decisions reach Tribal data. **Change** (P-TN-07).

**4.7 The fire recommendation.** v1's fire report recommends to "institutionalize TEK and Indigenous fire stewardship as professional competencies" and to "co-design credentialed competencies (with Tribes)" [E: TN-051]. Its diagnosis is right: Indigenous fire stewardship is under-recognized in workforce investment. Its remedy puts a non-Tribal credentialing system over Tribal knowledge. Tribes already set their own on-reservation standards through compacts [E: TN-013] and asked for fewer barriers, not outside credentials [E: TN-009]. **Change** (TN-C06; P-TN-12).

**4.8 Container.** Skill area 5.3, "Cultural Competency," places Tribal relations beside DEI (5.3.4). Tribal status is political, not demographic [E: TN-029]. In 2025–26 that placement has had practical consequences: Tribal programs were protected from anti-DEI cuts only agency by agency [E: TN-032]. **Change** (P-TN-08).

**4.9 Missing content.** v1 lacks:
- treaty-reserved rights;
- trust responsibility;
- ISDEAA self-determination and self-governance;
- treatment-as-a-state and Tribal law;
- THPO coordination;
- payment practice toward Tribes;
- Indian preference;
- Alaska Native contexts (ANCSA corporations sit under separate DOI policy [E: TN-016]);
- Native Hawaiian contexts;
- Tribal enactment notes on fire, forestry, fisheries, wildlife and water-quality competencies.

**Add** (TN-C01, C04, C05, C08, C09, C11; P-TN-13, P-TN-17).

---

## 5. Candidate competencies (summary)

Detail is in `candidate_competencies.csv`. Every candidate describes the **conduct** of the professional, never the content of Indigenous knowledge. Every one requires TAC review before publication.

| ID | Title (short) | Craft | Change type | Label |
|---|---|---|---|---|
| TN-C01 | Apply the trust responsibility and treaty-reserved rights to decisions | SC (FC) | stable | E |
| TN-C02 | Conduct government-to-government consultation as a pre-decisional process | SC | transforming | E |
| TN-C03 | Protect confidential Tribal information across records, disclosure law and AI tools | SC (DC) | emerging | E |
| TN-C04 | Structure and administer agreements for shared or Tribally led stewardship (638 contracts and compacts, co-stewardship, Tribal Forest Protection Act, Good Neighbor Authority, data agreements) | SC | transforming | E |
| TN-C05 | Operate within Tribal jurisdiction and Tribal law as a non-Tribal party | SC | stable | J |
| TN-C06 | Support Tribally led cultural and prescribed fire without directing Tribal knowledge | FC (SC) | emerging | E |
| TN-C07 | Govern data about Tribal lands, resources and peoples under Tribal authority (CARE with FAIR) | DC (SC) | transforming | E |
| TN-C08 | Administer funding to Tribal governments in ways that respect self-governance | SC | transforming | E |
| TN-C09 | Apply Indian preference and Tribal employment rights lawfully | SC | stable | E |
| TN-C10 | Engage with Indigenous knowledge only on its holders' terms | SC | transforming | E |
| TN-C11 | Coordinate cultural resource work with THPOs under Tribal direction | SC (FC) | transforming | E |
| TN-C12 | Sustain government-to-government obligations when procedures change | SC | emerging | E |
| TN-C13 | Establish and sustain core environmental program capacity for a Tribal government | SC (DC) | stable | E (framework); requires Tribal validation |

**Notes on the set:**
- **TN-C13 is the only candidate written *for* Tribal employees.** It describes public-administration functions from EPA's public GAP framework, not knowledge. It is in scope, but it must not ship unless Tribal environmental professionals validate it, for example through RTOCs or ITEP, and agree it reflects their work.
- **Craft blend.** Statecraft dominates this lane, as expected: these are relationship, authority and accountability competencies. TN-C03 and TN-C07 bring in Data Craft, and TN-C06 brings in Field Craft. [J]

---

## 6. Role signals (summary)

Full rows are in `role_signals.csv`, and all are subject to the policy §6 review gate. The strongest signals:

- **Tribal governments became the main employers of trust-forest professionals** (TN-S01). BIA agency forestry capacity is declining (TN-S02).
- **Tribal fire roles are being re-housed in USWFS**, with position descriptions to be standardized (TN-S03). This creates new Tribal-liaison and Office of Tribal Trust roles (TN-S04). Tribes are pushing for year-round combined positions (TN-S05).
- **Section 106 practice is transforming** under the pending Part 800 rewrite. Federal specialists would shift toward agency-prepared reports, and THPOs would face more advocacy work (TN-S12).
- **Federal planners' Tribal coordination load is rising** across planning-rule eras (TN-S11).
- **Formal competency requirements for federal staff who consult or receive IK** now appear in policy: DOI training prerequisites and NPS DO 71C position competencies (TN-S15).
- **Entry paths at risk.** Grant-funded Tribal science positions and Native student pipelines are vulnerable (TN-S08, TN-S09).
- **Speculative signal.** Co-stewardship coordinator roles on the federal side are declining (TN-S13, [S]).
- **Evidence gap.** Tribal fisheries and wildlife are not assessed (TN-S16, [S]).

---

## 7. Proposals

**P-TN-01 — Model Tribal nations as a sector actor and as a jurisdictional context, not as a profession family.**
- **Sector-actor vocabulary.** Add `tribal` with these subtypes:
  - federally recognized Tribe;
  - inter-Tribal organization or consortium;
  - Tribal college or university;
  - Tribal enterprise;
  - ANCSA corporation (distinct legal category);
  - Native Hawaiian organization (distinct status);
  - state-recognized Tribe (distinct status).
- **Jurisdictional-context facet.** Add a categorical facet (trust/Tribal lands; treaty-reserved rights areas; co-managed areas). Never use a geographic layer of Tribal places.
- **Role variants** carry the differences in authority and accountability. Examples: a Tribal forester answers to a Tribal council and to treaty obligations; Tribal programs implement Tribal law; compact parties set on-reservation standards.
- **Why:** TN-013, TN-004, TN-050. [J]

**P-TN-02 — Encode the exclusion rule (§1) in the schema and in CI.**
- **Schema fields:** `indigenous_data_flag`, `sensitivity`, `approval_status`, `ai_use_permitted` (policy §7).
- **CI checks:** fail release builds on unapproved Tribal-related records; fail on confidential records anywhere in the repository; fail on coordinates co-occurring with cultural-site vocabulary (policy §15).
- **Owner:** DE. [J]

**P-TN-03 — Create a Tribal review gate with binding authority, and amend the charter.**
- **Scope.** No release may contain Tribal-related content without approval from a Tribal Advisory Council constituted under the draft protocol. Tribal-related content means any L2-tagged item, the successors of 5.3, 6.5.1 and 7.1.1, TN-C01 to C13, and Tribal role variants.
- **Charter amendment.** The CA's dispute-resolution authority does not override the TAC on Tribal-related content. The default is withholding. [J]
- **Interim rule.** Until a TAC exists, **nothing Tribal-related is published**. This applies to v1 7.1.1 and to this report's CSVs.

**P-TN-04 — Retire 5.3.2 and replace it.** Retire 5.3.2, its ladder, and the D5 "cultural sophistication" progression. Replace them with TN-C10 and TN-C07. [E: TN-018]

**P-TN-05 — Rebuild the Tribal content of 6.5 Intergovernmental Relations.**
- Build it from TN-C01, C02, C04, C05, C08, C11 and C12.
- Remove the TEK-integration and "advances tribal capacity" indicators from 6.5.1.
- Treat these as **core Statecraft competencies for all sector actors**, not as enactment notes. [E: TN-014, TN-016, TN-017, TN-044]

**P-TN-06 — Revise 7.1.1 into TN-C07 and hold it for Tribal review.** Keep the rights framing. Add the legal-source precision and the FOIA and AI indicators. Separate it from any future competencies for Tribal data stewards, which belong in a Tribally stewarded module. [E: TN-018; J]

**P-TN-07 — Fix and gate the L2 lens.**
- **Definition.** Separate Tribal sovereignty from local communities. Name three obligation sources (Tribal law; federal law and policy; international standards). Add triggers for AI ingestion, records disclosure and Tribal workforce data.
- **Mandatory multi-rater L2 review set:** 4.2.3, 4.3.1–4.3.5, 1.4.5, 1.4.2, 1.3.5, 1.2.4, 2.6.1, 2.6.2, 5.3.3, 6.2.x and 7.1.4.
- **7.1.4.** Correct its L2 tag from A to at least I.
- **Gate.** L2 definitions and tags are published only through the gate. [E: TN-048, TN-014, TN-018]

**P-TN-08 — Split skill area 5.3.** Move Tribal government-to-government content into Statecraft and intergovernmental. Keep cross-cultural communication, reframed as observable cultural humility, separate from DEI and EJ. [E: TN-029, TN-032]

**P-TN-09 — Add exposure standing rule R13, "governed data."**
- **Tag.** A task that handles confidential Tribal information or IK carries `governed_data: tribal`.
- **Rule.** Its automation type may be A or Ac only conditionally, "where the Tribe authorizes AI use"; otherwise it is H.
- **Re-code under this rule:** 6.5.1 T3, 5.3.2 T3, 5.3.3 T2.
- **Owner:** LM and DC. [E: TN-052; J]

**P-TN-10 — Adopt the data rules for Tribal workforce data and change signals** (policy §6):
- quarantine Tribal-employer postings by default;
- flag signals with `tribal_programs`;
- hold flagged signals until the TAC reviews them;
- produce no Tribe-identified indicators without consent;
- never train models on Tribal documents.

Owners: IA and LM. [J]

**P-TN-11 — Separate licensing and namespaces.** CC0 covers project-authored content. Tribal-contributed content goes in its own namespace and carries the license the contributor chooses. It is excluded from the bulk CC0 release unless the contributor opts in. Owners: DE and AS. [E: TN-054; J]

**P-TN-12 — Replace v1's recommendation to credential Indigenous fire stewardship.** Use TN-C06 (partner conduct) instead. Reference Tribally defined qualifications only where a Tribe publishes them and asks EMST to reference them. Owner: FC (fire). [E: TN-013, TN-009]

**P-TN-13 — Add Tribal-actor enactment notes to fire, forestry, fisheries, wildlife and water-quality competencies.** The notes describe the authority context: compacts, treaty rights, Tribal law, Tribal water-quality standards. They never describe knowledge content. [E: TN-044, TN-013]

**P-TN-14 — Draft Tribal-employer role variants only from public program documents, mark them pending, and release them only on validation.**
- **Candidates:** Tribal environmental director (multi-media generalist); Tribal forester; Tribal fire management officer; THPO.
- **Sources:** public program documents only (GAP, NIFC, IFMAT).
- **Status:** each is marked "pending Tribal validation."
- **Release:** only after opt-in validation (protocol §14, phase 4). [E: TN-001, TN-013, TN-004]

**P-TN-15 — Replace the "Consultation" reform flag with dated driver events in L5.** The events:

| Date | Event |
|---|---|
| 2025-03-14 | EO 14112 rescinded |
| 2025-09-10 | SO 3443 |
| 2025-10 | OMB M-25-36 |
| 2026-01-12 | USWFS launch |
| 2026-07 | Bears Ears Commission eliminated |
| 2026-07-24 | Part 800 NPRM vote |

Re-check status against CRS at each release. [E: TN-026, TN-007, TN-014, TN-033, TN-041]

**P-TN-16 — Route Tribal participants through Tribal research approval.** IO's Delphi and CM's panels must ask each Tribe whether its research code applies, and obtain approval before including Tribal employees. Budget time for this. [J]

**P-TN-17 — Run separate tracks for Alaska Native and Native Hawaiian contexts.** Give them their own subtypes, enactment notes and reviewers. [E: TN-016; J]

**P-TN-18 — Ingest public federal Tribal-relations competency requirements and plan demand signals.**
- **Requirements:** NPS DO 71C position competencies and DOI training prerequisites, ingested as role-requirement evidence.
- **Demand signals:** OpenLMP Tribal touchpoints, ingested for TN-C01, C02, C03 and C11. Exclude Tribal plans and confidential appendices, as OpenLMP already does.

[E: TN-017, TN-016, TN-044, TN-054]

---

## 8. Answers to CA architecture questions (§6, TN)

### Q1. How should Tribal nations enter the model: as a sovereign-government and employer sector actor, as a jurisdictional context, or both? What must not be included? (DP-7)

**Both, plus a third thing the hypothesis misses.** [J, resting on TN-013, TN-014, TN-004]

1. **As a sector actor** (sovereign government and employer). Subtypes are listed in P-TN-01. Role profiles get Tribal-actor *variants* where authority and accountability differ. For example:
   - a Tribal environmental director answers to a Tribal council;
   - the program implements Tribal law and may assume federal programs;
   - qualifications on Tribal lands may be set by compact.

   This fits the CA's "variants share a function, differ in tasks, authority, crosswalks and frictions" model. One addition: **Tribal law and compact standards must be representable as an authority that can override EMST's default qualification statements** on Tribal lands.
2. **As a jurisdictional context.** This is a categorical facet: trust or Tribal lands; treaty-reserved rights areas; co-managed areas. Competencies and tasks can be tagged "performed differently here." It must never become a geographic layer of Tribal places.
3. **As the counterpart in other actors' Statecraft.** This is the piece the CA hypothesis misses. The CA writes that "sector actor is context, not content," with enactment notes where the actor changes the performance. That works for Tribal *employers*. It does not work for the obligations every other actor owes Tribal nations: consultation, treaty rights, agreements, confidentiality. Those are **core content**, as Statecraft competencies in L1 that apply across federal, state, local, private and NGO actors (TN-C01 to C12). They are not enactment notes. If they are reduced to notes, the trust and treaty obligations disappear from HR and training views.

**What must not be included:** §1 and policy §4. In summary:
- Indigenous knowledge content;
- confidential Tribal information and sensitive-place data;
- Tribe-level characterizations without consent;
- person-level Tribal data;
- Tribal documents and postings by default;
- LLM-inferred Tribal skills;
- an identity- or jurisdiction-defined profession family.

### Q2. What review and consent protocol must apply before content like 7.1.1 or any L2 material is published?

See `tribal_engagement_protocol.md`, which is AI-drafted and requires Tribal revision. In short [J]:

1. **Interim rule.** Nothing Tribal-related is published until a Tribal Advisory Council exists. This covers 7.1.1, its successor TN-C07, every L2 definition and tag, TN-C01 to C13, the Tribal role variants, and this report's signal and candidate files.
2. **The TAC.** Members are nominated by Tribal governments and inter-Tribal organizations. It has **binding** authority over inclusion, wording and release of Tribal-related content. A charter amendment sets aside the CA's override for this category. Disagreement means the content is withheld.
3. **Review package.** Each item goes to the TAC labeled AI-drafted where it is. Sources and evidence labels are attached. Review windows are 90–120 days for decisions that need Tribal government action and 30–45 days for professional review. Extensions are granted on request.
4. **Recording.** A written decision is recorded with the content's `approval_status`. The TAC can withdraw approval.
5. **Internal tagging versus publication.** Analysts may apply L2 tags internally (multi-rater, per the CA's audit) because tagging is analysis, not taking Indigenous content. **Publishing** the tags and definitions goes through the gate.
6. **Consent for contributed material.** Any material contributed by Tribes or Tribal professionals also needs free, prior and informed consent per contribution. It carries labels, the contributor's license and a withdrawal right (policy §7, §9, §12).

### Q3. What data-governance rules apply to change signals that touch Tribal programs?

See policy §6. In short [J]:
- **Source.** Public, non-confidential sources only, dated and attributed.
- **Flag and gate.** Signals carry `tribal_programs: true` and are held from release until the TAC reviews them.
- **Naming.** No named Tribe unless the source is that Tribe's own public statement and the TAC approves the use.
- **Tribal postings.** Tribal-employer postings are quarantined from the NLP pipeline by default. If the TAC releases them: derived signals only; no full text stored; no training on them; aggregates suppressed below a TAC-set threshold; a per-Tribe opt-out that is always honored.
- **Exposure.** Exposure assessments on governed-data tasks are conditional on Tribal authorization (P-TN-09).
- **Tribal interpretation.** Where Tribes or inter-Tribal organizations have published their own interpretation of a change, the signal links to it and gives it priority.

**Trade-off.** The Tribal workforce will be under-measured. v1 already notes it is invisible in federal series data [E: TN-050]. The right response is analyses that Tribes control and commission, not quiet ingestion.

---

## 9. Disagreements and trade-offs

1. **With v1's fire report (TN-051): credential Indigenous fire stewardship, or not?**
   - *Trade-off:* making Indigenous fire stewardship visible, which drives workforce investment, versus putting a non-Tribal credential over Tribal knowledge.
   - *My position:* make the **partner's** obligations visible and assessable (TN-C06), and reference Tribal qualifications only on Tribal terms. Where Tribes want their practitioners recognized in interagency systems, that is a Tribe-to-agency negotiation. It is not EMST's to pre-empt.
2. **With the CA's "sector actor is context, not content" hypothesis (TN-053).** I agree for Tribal employers and disagree for the obligations other actors owe Tribal nations. Those are core Statecraft content (Q1). The cost is a larger core. The benefit is that HR and training views actually show trust and treaty obligations.
3. **With the charter's dispute-resolution rule.** The CA resolves disputes. For Tribal-related content I propose that the TAC's decision is binding and that the default is withholding.
   - *Trade-off:* design coherence and speed versus legitimacy.
   - Without this carve-out, the "can say no" clause in the charter has no mechanism once TN is a simulated agent and real Tribes are not at the table.
4. **With the CC0 default from the OpenLMP pattern (DE, AS; TN-054).** Open by default is right for project-authored content and wrong for Tribal-contributed content. Namespace and license separation (P-TN-11) costs schema complexity.
5. **With the completeness goals of LM and IA.** Quarantining Tribal postings creates a measurement gap. I accept the gap. Completeness is not worth a sovereignty breach, and the gap is itself a finding.
6. **With IO's and CM's timelines.** Tribal research approvals and council cycles will slow any Delphi that includes Tribal professionals. Run the federal and state Delphi on schedule and the Tribal track on Tribal time. Do not shorten the Tribal track.
7. **With the charter's Field Craft reference.** The charter says "Indigenous and local knowledge where its holders choose to share it, on their terms." I agree with "on their terms." I disagree with grouping Indigenous knowledge with local knowledge, which 301 DM 7 distinguishes [E: TN-018]. I also disagree that knowledge shared with a project should become competency content; even shared knowledge stays with its holders.
8. **The cost of exclusion.** Leaving Indigenous knowledge out of EMST could be read as treating it as less important than the expertise EMST does encode.
   - *Mitigation:* the taxonomy should state on its face that Indigenous knowledge is a distinct body of environmental expertise, held and governed by Indigenous nations, **out of scope by design**. It should point to Tribally controlled resources where Tribes provide them. [J]
9. **With v1's exposure coding (LM, DC).** v1 coded documentation of Tribal input as AI-augmentable without condition (TN-052). P-TN-09 reduces measured AI exposure for some D5 and D6 tasks. That is intended.

---

## 10. Issues outside my area that affect the vision

- **FH (federal human capital).**
  - BIA forestry vacancies and USWFS position-description standardization within 180 days will shape the Tribal-adjacent federal workforce [E: TN-006, TN-007].
  - Indian preference is a political classification Tribes asked to have applied [E: TN-009]. FH should own TN-C09's placement.
- **SC (statecraft).** The Part 800 rewrite and OMB M-25-36 move procedural floors. Competencies should separate obligations from procedures (TN-C12) [E: TN-014, TN-036].
- **CP (compliance and product).**
  - If an agency hosts EMST, FOIA reaches its records. The product must not hold material it cannot protect [E: TN-018].
  - Anti-DEI review exposure is real for any Tribal content placed in DEI-adjacent containers [E: TN-032].
- **AS (adoption and stewardship).** Tribal engagement needs a funded compensation line before first contact. Tribal program funding volatility in 2025–26 also means unpaid review would be extractive [E: TN-031; J].
- **LM.** The Tribal workforce is structurally invisible in federal series and posting data [E: TN-050]. Any "sector-wide" workforce statistic EMST publishes should carry that caveat.
- **LC.** Tribal colleges and universities are both a pipeline and a partner. Tribes asked for TCU partnerships [E: TN-009]. Salish Kootenai College's forestry BS (2003) was the first at a TCU [E: TN-004]. Curriculum alignment with TCUs should be TCU-led.
- **Process.** The shared web-search budget ran out early in this run. If the CA wants Task 1 completed for fisheries, TCUs and Alaska, a follow-up run with search budget is needed.

---

## 11. Open questions for the Chief Taxonomy Architect

1. Will you take P-TN-03 (a binding TAC and a charter carve-out) to the project lead? If not, what mechanism gives the charter's "can say no" clause effect once real Tribes are involved?
2. Do you accept that obligations owed to Tribal nations are **core Statecraft content** for all actors (Q1, point 3), rather than enactment notes?
3. Should EMST include Tribal-employer role variants at all before a TAC exists, even as internal drafts? My recommendation: internal drafts only, marked pending, never released.
4. Will DE implement namespace and license separation (P-TN-11) in the v2 schema from day one? Retrofitting it is much harder.
5. Can AS budget compensation for Tribal reviewers in the pilot phase? If not, I recommend no Tribal outreach in the pilot. Ship federal and state content with the Tribal gate closed.
6. Do you accept P-TN-09 (the governed-data exposure rule) as a change to the exposure instrument?

---

## 12. What requires real consultation before any release

None of the following may be released on the strength of this AI-drafted work:

1. The Tribal engagement protocol and the Indigenous data governance policy, both in full.
2. The existence, composition and authority of the TAC.
3. The successor to 7.1.1 (TN-C07) and every L2 definition and tag.
4. TN-C01 to TN-C12: their wording, indicators and whether they belong.
5. TN-C13 and any Tribal-employer role variant.
6. Every row of `role_signals.csv`, because each touches Tribal programs.
7. Whether Tribal employer postings may ever be analyzed.
8. Labeling choices (Local Contexts Notices) and licensing for Tribal-contributed content.
9. Alaska Native and Native Hawaiian tracks, which need their own reviewers.
10. Any Delphi, survey or interview involving Tribal employees, which needs Tribal research approval where it applies.

Re-read the seven blocked sources (TN-060 to TN-066) before any of this goes to Tribal reviewers, so reviewers are not handed second-hand paraphrase.
