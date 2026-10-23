# Federal Human Capital & Classification Advisor (FH): Phase 2 Report

**Role code:** FH · **Date:** 2026-10-23 · **Folder:** `docs/research/federal-human-capital/`
**I push on:** Could a federal HR specialist use EMST tomorrow?
**Labels:** [E] evidence; source IDs resolve to `sources.csv`. [J] FH professional judgment; I say what it rests on. [S] speculation; I say what would settle it.

---

## 0. Summary

**Could an HR specialist use EMST tomorrow?** Not yet. They could within one pilot cycle if v2 adds a thin federal layer. That layer needs:
1. a versioned OPM series register;
2. series × grade-band role profiles;
3. proficiency levels defined by responsibility, not years;
4. behavioral anchors usable as SME-QA benchmarks;
5. duty-statement and Factor 1 language.

v1 has none of these. Its Intermediate-level indicators are good raw material. Its Advanced and Expert anchors are not usable for hiring.

**Federal HR has moved toward what EMST could supply.**
- **The law.** The Chance to Compete Act requires position-specific, job-analysis-based technical assessments [E: FH-023]. Since 30 Sep 2025, self-assessments may not rank candidates [E: FH-002].
- **Practice lags.** In FY2025, 91% of delegated-examining announcements relied only on self-report questionnaires. Only 15% of agencies employ I-O psychologists [E: FH-017].
- **OPM is building series-level competency models** through the Federal Workforce Competency Initiative (FWCI) [E: FH-017, FH-044]. It issued its first competency-based classification and qualification standards (2210) on 13 Apr 2026 [E: FH-011].
- **OPM is consolidating 115 low-use series**, several of them environmental, with new standards through Sep 2027 [E: FH-014].

**Where EMST fits.** USA Hire covers general competencies [E: FH-026]. The gap is technical competency content for environmental series, written so agency SMEs can turn it into job analyses and benchmarks quickly [J].

**The workforce EMST would serve has contracted sharply.**
- About 317,000 federal departures in 2025 [E: FH-030].
- USFS and NPS each lost more than a quarter of their employees between Sep 2024 and Jan 2026 [E: FH-008].
- Park rangers fell 34.1% [E: FH-008].
- Student-trainee occupations shrank, and the under-30 share fell to 7.9% [E: FH-008].
- Every vacancy needs Strategic Hiring Committee approval under EO 14356 [E: FH-029].

In this setting, competency evidence matters most in three places: justifying hires, protecting critical skills, and rebuilding entry pipelines.

---

## 1. Method, scope and limits

**What I did**
- Read the charter, the brief, the v1 database (via `data/v1_baseline/`), the v1 OPM cross-domain workbook, and the v1 forester PD (`legacy/v1/docs/forester_pd_transformation.html`).
- Ran 13 targeted searches.
- Read 35 sources in depth. Primary: OPM reports to Congress, CHCO memos, Federal Register rules, EO text and the U.S. Code. Secondary: CRS and GAO summaries, Partnership for Public Service analysis, and trade press.
- Built a series register (73 series), a crosswalk of 13 priority series against v1 competencies (193 rows), five HR workflows, the CSV deliverables, and generator scripts (`scripts/`).

**Hard limits this session**
1. **Search and fetch access.** The shared web-search budget ran out after 13 searches. After that, the permission layer blocked most fetches of unsurfaced URLs. Blocked:
   - Federal Workforce Data (FH-050)
   - DOI wildland fire pages (FH-051)
   - the FWCI and 2210 competency-standard memos (FH-044)
   - staffing-plan guidance and the final RIF regulations (FH-045)
   - the AI-workforce memo (FH-048)
   - all OPM classification and qualification standard pages (FH-041, FH-042)
2. **What that means for the deliverables.**
   - **Register dates and positive-education flags are mostly [J] "not verified this session".** The exceptions are 2210 and the OPM consolidation list, which are [E]. The [J] entries rest on professional familiarity, not documents re-read today.
   - **The whole crosswalk is [J].** No live USAJOBS announcements or PDs were sampled. The `basis` column records what each judgment rests on. A validation protocol is in P-FH-11.
   - **Unverified:** U.S. Wildland Fire Service status; the USDA/USFS reorganization; wildland firefighter pay reform; agency-level 2025 losses at EPA, NOAA, USGS, BOR, BIA, NRCS and USACE.
3. **Why these sources.** OPM reports to Congress (FH-001, FH-017), its memo index (FH-011) and Federal Register rules (FH-013, FH-021) are the authoritative record. PPS (FH-008) is the best independent read of OPM's new workforce data. I used trade press only where no primary source was reachable, and graded it Medium or Low.

---

## 2. Federal HR landscape, October 2026

### 2.1 Hiring: the Merit Hiring Plan and the Chance to Compete Act

**The Merit Hiring Plan (MHP, 29 May 2025) is the operative framework** [E: FH-012, FH-003]. It requires:
- at least one technical or alternative assessment in every competitive hiring process;
- self-assessments only for minimum qualifications and eligibility, from 30 Sep 2025 [E: FH-002, FH-017];
- "rule of many" category ranking (final rule 8 Sep 2025) with agency cut scores;
- essay questions at GS-5 and above;
- agency talent teams.

**Recent changes** [E: FH-003, FH-032, FH-049 (titles only)]:
- OPM issued supplemental guidance in Feb 2026.
- *AFGE v. Kupor* stayed essay Question 3 on 11 Sep 2026. OPM replaced it and added a Question 5 tied to agency priorities, due by 2 Nov 2026.
- Further memos covered candidate ranking (Jan 2026), time-to-hire (Sep 2026) and strategic recruitment (Oct 2026).

**The Chance to Compete Act (P.L. 118-188) amended 5 U.S.C. 3304** [E: FH-023]. A *technical assessment* must:
- be "a position-specific tool";
- let applicants demonstrate "job-related skills, abilities, knowledge, and competencies";
- be "based upon a job analysis";
- not "solely or principally rely on" automated self-assessment.

The Act defines a subject-matter expert as someone with "an understanding of the duties of, and knowledge, skills, and abilities required for, the position." Technical assessments are preferred for three years, then required, with waivers available.

**Implementation status** [E]:
- FY2025: 91.23% of delegated-examining announcements used only self-report questionnaires, and they produced 92.5% of selections [FH-017].
- FY2026 Q2: 34.3% used technical or off-the-shelf assessments [FH-001].
- Targets: 75% of positions in FY2026 and 100% in FY2027 per the Agency Priority Goals [FH-016], but FY2028 per the Jul 2026 plan [FH-001].
- Talent teams operate at 154 agencies with 1,000+ members. SME-QA has 53 master trainers [FH-017].

**USA Hire** [E]:
- Standard batteries measure general competencies by series and grade (GS-3 to GS-11): reading, reasoning, judgment, mathematical reasoning and interaction [FH-026].
- Coverage grew from 138 to 412 series in Mar 2026 [FH-001].
- The Oct 2025 materials named no environmental series [FH-026].
- **Implication [J]:** for 0400, 0800 and 1300 environmental series, USA Hire can carry the general hurdle. The technical hurdle falls to agencies, and most lack the staff to build it.

**Cross-agency hiring** [E: FH-013]. An interim rule effective 15 Oct 2026:
- extends shared certificates to Schedule D and Schedule Policy/Career;
- authorizes OPM-led pooled hiring for common occupations;
- bars re-rating on shared excepted-service certificates.

**Implication [J]:** a common technical benchmark for 0401, 0028 or 0462 could be reused across USFS, BLM, FWS and NPS. That is an adoption hook.

**AI in hiring** [E: FH-015]. OPM's 27 Aug 2026 memo treats AI drafting of announcements, PDs, job analyses, qualifications, crediting plans and interview questions as generally not high-impact when "the process of drafting content itself does not affect an individual's access to employment." AI-assisted steps "remain subject to job analysis and validation requirements under 5 CFR 300.103," and humans must independently review and adopt the output.

**Implication [J]:** an LLM pipeline that drafts job analyses from EMST is permitted if it is documented and the SMEs own the output.

### 2.2 Classification and qualification modernization

**Phase One consolidation memo (24 Apr 2026)** [E: FH-014]:
- 115 series covering about 4,926 employees are proposed for realignment.
- Agency feedback was due 11 May 2026.
- New standards are scheduled from Apr 2026 to Sep 2027.

Environmental and adjacent series on the list, with proposed destinations:

| Series | Proposed destination |
|---|---|
| 0023 Outdoor Recreation Planning | 01xx (target to verify) |
| 0029 Environmental Protection Assistant | 0303 |
| 0190 General Anthropology | 0101 |
| 0410 Zoology, 0437 Horticulture, 0480 Fish & Wildlife Administration, 0487 Animal Science | 0401 |
| 0455 Range Technician | 0404 |
| 0459 Irrigation System Operation | trades family |
| 0688 Sanitarian | 0601 |
| 0698 Environmental Health Technician | 0640 |
| 0090 Guide | 1001 |
| 0965 Land Law Examining | 0901 |
| 1372 Geodesy, 1380 Forest Products Technology | 1301 |
| 1374 Geodetic Technician | 1311 |
| 5042 Tree Trimming | 5001 |
| 5729 Drill Rig Operating | 5701 |

The memo says consolidation "will not automatically change an employee's grade, pay, tenure, or career ladder placement" and "does not diminish the recognition of specialized work," citing wildlife biology and geospatial analysis. Later phases will "redesign the classification framework" and address "skills-based workforce frameworks." I could not confirm finalization after May 2026, so treat the list as **proposed**.

**Competency-based standards** [E: FH-011, FH-044 (titles verified, content blocked); FH-017]:
- On 13 Apr 2026 OPM issued, for 2210: a competency-based classification standard, a competency-based qualification standard, job aids, and FWCI "General and Technical Competencies and Competency Frameworks."
- An FWCI survey followed on 27 Apr.
- The Dec 2025 Chance to Compete report says FWCI general models were updated for 200+ series and technical models built for 2210. Qualification and classification updates target 300+ series by the end of FY2026 and 600+ by FY2027.
- **This is the most design-relevant development [J].** OPM is building the series-level competency layer EMST would have proposed. EMST should feed it or crosswalk to it, not compete.

**AI competencies** [E: FH-043, titles only]. In Apr 2024 OPM issued an AI competency model, skills-based hiring guidance for AI work, and an AI competency model for Civil Engineering (0810). That is a precedent for an AI overlay on a non-IT series. EMST's 2.6 and 7.2 competencies could become the 0400/1300 analogue [J].

**MOSAIC** is absent from both 2025–26 Chance to Compete reports [E: FH-001, FH-017]. FWCI appears to be its successor [J].

### 2.3 Hiring controls and workforce reductions

**Hiring controls** [E: FH-012, FH-029, FH-006, FH-045]:
- The freeze of 20 Jan 2025 was extended to 15 Oct 2025.
- EO 14356 (15 Oct 2025) replaced it. A Strategic Hiring Committee, including the deputy head and chief of staff, approves every vacancy.
- Annual staffing plans target "highest-need areas," with quarterly updates from Q2 FY2026.
- Exceptions cover immigration, national security and public safety. There is no end date.
- Until a plan is approved, the EO 14210 ratio of one hire per four departures applies.
- OPM issued staffing-plan guidance on 30 Jul 2026 (title only).
- Firefighters are not named in the exceptions. I could not verify whether wildland fire hiring is treated as public safety.

**Scale of losses** [E]:
- About 317,000 departures in 2025 [FH-030]: deferred resignation (DRP) about 144k; early retirement or buyout about 21k; attrition about 129k; involuntary about 24k (RIF 17k, probationary 7k).
- Hires were about 68k by the end of August [FH-030].
- The workforce fell from 2,313,216 (Sep 2024) to 2,035,344 (Jan 2026) [FH-008].
- GAO-26-108719 reports 134,122 separations in Jan–Jun 2025, including 16,414 USDA DRP [FH-009, secondary].

**Environmental agencies**
- **USFS** lost more than a quarter of its employees from Sep 2024 to Jan 2026 [E: FH-008]. A USDA OIG figure cited in May 2026 gives 16% for 2025 [E: FH-035]. The bases differ, so cite both with dates.
  - By May 2025, about 5,000 voluntary departures had taken place: a quarter of the non-fire workforce, including about 1,600 staff holding fire certifications [E: FH-018, FH-025].
  - In Feb 2025, at least 3,400 probationary employees were fired, including trail crews, wilderness rangers, biologists and NEPA coordinators [E: FH-024].
  - USFS told the Senate it will need state and community partners [E: FH-018].
- **NPS** lost more than a quarter of its employees; park rangers fell 34.1% [E: FH-008].
- **DOI** had about 2,300 probationary firings in Feb 2025 [E: FH-024].
- **Six western states:** a consultancy study reports 5,874 job losses across seven land agencies, and 25–27% cuts at dispatch centers in CO and NV [E, low quality: FH-019].
- **Wildland fire management grew** [E: FH-008]. USFS had 10,496 firefighters in May 2026 against a goal of 11,300. DOI reported 6,600 and is "consolidating wildland fire management programs in deliberate phases" [E: FH-035].
- **Not verified:** losses at EPA, NOAA, USGS, BOR, BIA, NRCS and USACE. That is a gap in what I could check, not a finding of no effect.

**Entry pipeline** [E: FH-008]
- Student-trainee occupations "decreased significantly," which PPS calls "a contraction in entry-level opportunities."
- The under-30 share fell from 8.9% to 7.9%. The share aged 50+ rose from 35.7% to about 40%.
- This is the strongest external support for v1's career-ladder concern. The driver here is fiscal and policy, not AI [J].

**Other rules** [E: FH-045, FH-011, titles only]:
- final RIF regulations (2 Sep 2026);
- performance-appraisal rules (24 Jul 2026);
- a standardized rating distribution for FY2026;
- probationary guidance (Apr and Aug 2025).

**Legislation.** The proposed Public Lands Workforce Stability Act would bar RIFs at DOI and USFS until 2030 without appropriations-committee approval [E: FH-020].

### 2.4 Schedule Policy/Career

- The final rule was published 6 Feb 2026 and took effect 9 Mar 2026 [E: FH-021, FH-004]. Policy-influencing positions are excepted from chapter 75 and chapter 43 procedures. Incumbents remain career, and competitive-service positions are still filled by merit procedures.
- The 3 Jun 2026 EO (EO 14410 per FH-022) moved about 8,000 employees in about 4,800 positions across 54 agencies; 97% are GS-15 or above. USDA moved 81 positions [E: FH-005, FH-028].
- EPA reclassified 98 legal staff [E: FH-007].
- Suits by PEER, AFGE, NTEU and GAP are pending [E: FH-028].
- **Implication [J]:** senior statecraft roles now serve at will, which raises the stakes of v1 7.1.3 and the L5 lens. EMST must never be used to identify positions for Schedule Policy/Career.

### 2.5 Reorganization and wildland fire

**Verified:** DOI is consolidating fire programs in phases, and the 0456 occupation is growing [E: FH-035, FH-008].

**Not verified this session:**
- how the U.S. Wildland Fire Service was established and how it is staffed;
- the 2025–26 USDA reorganization;
- the current fire pay regime.

I recall that a U.S. Wildland Fire Service consolidating DOI bureau fire programs was announced in late 2025, and that USDA planned headquarters relocation to regional hubs and the phase-out of USFS regional offices [S: confirm with DOI and USDA primary documents]. **Design implication either way [J]:** roles are moving between departments, so profiles must be function-defined, with department, bureau and series as changeable attributes.

### 2.6 Data and HR systems

- Federal Workforce Data (data.opm.gov) replaced FedScope in Jan 2026, with monthly updates [E: FH-010, FH-033]. It was not accessible to me (FH-050).
- OPM is consolidating core HR systems: "Federal HR 2.0," a Core HCM MVP in FY2026, and an HR Shared Service Center [E: FH-016, FH-047].
- EMST records should be loadable as reference data (IA lane) [J].

### 2.7 Training and development

- OPM launched governmentwide supervisory training (Dec 2025) and new SES/GS-15/GS-14 development programs (Nov 2025) [E: FH-046, titles].
- A Tribal treaties and consultation training dates from Dec 2024 [E: FH-046].
- EMST supervisory and leadership competencies (3.3.1, 3.5.x) should point to these, not duplicate them [J].

---

## 3. What this means for EMST design

1. **Competency with proficiency is the federal currency, and tasks are the evidence for it** [E: FH-023, FH-002, FH-017, FH-026].
2. **The federal unit of use is series × grade band**, not profession family [J].
3. **EMST's distinct federal value is technical competency content for environmental series, written to SME-QA standard.** It should not duplicate the general competencies OPM already measures [J].
4. **OPM is a moving target until at least Sep 2027** [E: FH-014, FH-017]. Crosswalks must be versioned and profiles function-defined [J].
5. **Contraction makes three uses urgent:** justifying hires, planning critical skills and knowledge transfer, and rebuilding entry pipelines [J; E: FH-008, FH-029].
6. **Guardrails are product features.** EMST must never decide or justify classification, RIF retention, Schedule Policy/Career designation or performance ratings [J].

---

## 4. Series register (`opm_series_register.csv`)

**Scope:** 73 series. That is the assignment list, refined, plus 27 additions: 0018, 0021, 0081, 0089, 0090, 0301, 0340, 0404, 0410, 0455, 0458, 0480, 0485, 0487, 0499, 0688, 0690, 0698, 0802, 0810, 1170, 1311, 1316, 1341, 1372, 1380, 2151.

**Observations**
- **Consolidation.** Twelve environmental or adjacent series are on OPM's Phase One list [E: FH-014]. EMST must store realignment status and successor series as data.
- **0401 is getting broader** as it absorbs 0410, 0437, 0480 and 0487 [E: FH-014]. The broader the series, the more a within-series profile is worth [J].
- **0028 has no positive-education requirement** and spans compliance, permitting, enforcement and NEPA. That makes it the most accessible landing series for reskilled staff [J; verify].
- **Positive-education barriers.** 0460, 1315, 1560 and most professional 0400/1300 series carry positive-education requirements. These are hard barriers [J; verify].
- **Two v1 claims are wrong [J]:**
  - "No environmental data science series": 1560 Data Science exists.
  - "Only 1370 recognizes GIS": 0150, 0401 and 1560 also cover GIS work.
- **Series ambiguity.** Fire intelligence work spreads across 0132, 1340, 1560, 2210, 0462 and 0401 [E, secondary: FH-040]. That ambiguity argues for function-defined profiles.

---

## 5. Competency-to-series crosswalk (`opm_series_to_emst_crosswalk.csv`)

### 5.1 Method

**Series covered (13):** 0401, 0408, 0454, 0456, 0460, 0462, 0482, 0486, 0028, 0819, 1315, 0025, 0457.

Each series has 7–9 **core** and 5–8 **supporting** competencies, for 193 rows in total.
- **Core:** a regular and recurring requirement in most positions at full performance; it would appear in a Factor 1 statement or a grade-controlling duty.
- **Supporting:** required in a substantial subset of positions, or at particular grades.

**Evidence label:** every row is J (see §1).

### 5.2 Findings

| Series | Core / supporting | Core that is also family-Core in v1 | Craft mix of core (v1 tags) | Entry (P) tasks | Entry tasks tagged Ac/S/V |
|---|---|---|---|---|---|
| 0028 Environmental Protection Specialist | 8 / 8 | 7 of 8 | SC 8 | 7 | **6 (86%)** |
| 0819 Environmental Engineering | 8 / 7 | 3 of 8 | SC 5, DC 2, FC 1 | 4 | 2 (50%) |
| 1315 Hydrology | 8 / 7 | **2 of 8** | **DC 7**, FC 1 | 10 | 5 (50%) |
| 0401 General Natural Resources | 8 / 7 | 5 of 8 | SC 4, DC 2, FC 2 | 8 | 3 (38%) |
| 0025 Park Ranger | 9 / 6 | 3 of 9 | SC 5, FC 4 | 13 | 5 (38%) |
| 0408 Ecology | 7 / 7 | 6 of 7 | DC 4, FC 2, SC 1 | 6 | 2 (33%) |
| 0460 Forestry | 8 / 8 | 5 of 8 | FC 3, DC 3, SC 2 | 7 | 2 (29%) |
| 0482 Fish Biology | 8 / 7 | 6 of 8 | FC 4, DC 3, SC 1 | 11 | 3 (27%) |
| 0454 Rangeland Management | 7 / 5 | **2 of 7** | SC 4, DC 2, FC 1 | 8 | 2 (25%) |
| 0462 Forestry Technician | 7 / 8 | **2 of 7** | FC 5, DC 2 | 15 | 3 (20%) |
| 0486 Wildlife Biology | 9 / 7 | 7 of 9 | FC 5, DC 2, SC 2 | 11 | 2 (18%) |
| 0456 Wildland Fire Management | 8 / 7 | 5 of 8 | FC 7, SC 1 | 8 | 1 (12%) |
| 0457 Soil Conservation | 9 / 5 | 7 of 9 | FC 6, SC 2, DC 1 | 8 | 0 (0%) |

*Computed from the crosswalk joined to the v1 family, craft and task tags in `data/v1_baseline`. Those tags were assigned by a single analyst [J, FH-038], so this is a derived signal.*

**What the table shows**
- **Statecraft is under-weighted in v1 families [J].**
  - F1 Forestry Core omits 3.1.4 (contract administration) and 6.1.4 (NEPA), both regular duties in federal forestry.
  - 0454 Rangeland is dominated by permit administration, NEPA, enforcement and conflict work; only 2 of its 7 core competencies are family-Core.
  - Families are therefore a poor proxy for federal roles (P-FH-01).
- **Hydrology is datacraft-heavy:** 7 of 8 core competencies are DC, while F4 is fieldcraft-heavy [J]. The role is converging with 1560.
- **Entry-level exposure is series-specific [J, derived].**
  - 0028 entry tasks (drafting, compliance checks, permit processing) are almost all coded Ac/S/V, the drafting OPM's AI memo normalizes [E: FH-015].
  - 0456 and 0457 entry work is mostly human-essential field work.
  - So pipeline risk differs: for 0028 it is fewer entry drafting tasks; for 0462 and 0499 it is fewer entry positions [E: FH-008].
- **No v1 home** (candidates FH-C01–C04 and C08–C12):
  - ESA Section 7 consultation
  - timber-sale and stewardship contracts
  - conservation planning
  - grazing permits
  - Section 106 review
  - collateral-duty incident roles
  - hatcheries
  - compliance inspection
  - remediation

### 5.3 v1 OPM cross-domain workbook and forester PD

Verdicts are recorded in `v1_assessment.csv` (16 rows).

**OPM cross-domain workbook**
- **Carry:** the finding that fieldcraft is recognized in the 0400 series and 0025.
- **Retire:**
  - "no environmental data science series";
  - the "0401 Fire" row, since 0456 now exists;
  - "292 competencies".
- **Correct:** the datacraft finding. The method is flawed [J]. Classification standards are deliberately tool-agnostic, so datacraft recognition shows up instead in:
  - PDs, postings and selective factors;
  - OPM guidance;
  - 1560, the 2024 AI models and the 2026 2210 standard [E: FH-043, FH-044].
- **Needs evidence:** the quoted "OPM language" is uncited.

**Forester PD**
- **Carry:**
  - the insight that PDs under-describe professional judgment;
  - the four new competencies, now FH-C05 and FH-C06, with mappings to 1.7.2 and 7.2.1;
  - the career-ladder concern.
- **Correct:**
  - **Format.** A Factor Evaluation System PD has major duties with percentage of time, plus Factors 1–9. KSA lists belong in announcements, not PDs.
  - **Whose entry is at risk.** Much cruising is done by 0462 technicians and seasonals, so the path at risk is 0462/0499 into 0460 [E: FH-008].
  - **Strike-throughs.** Reword rather than delete.
- **Retire:** functional positions as the PD's structure.
- **Needs evidence:**
  - The duty-time shifts (25% to about 12%) are speculation.
  - The PD omits a classification consequence: when grade-controlling duties shrink, the grade or series can change [J]. Any redesigned PD must be labelled "subject to classification review."

---

## 6. What v1 lacks for federal use

### 6.1 Gaps, in priority order

1. Series codes and a versioned register.
2. Series × grade-band role profiles.
3. Responsibility-based levels.
   - v1 uses tenure bands. Federal qualifications rest on specialized experience at the next lower grade, and OPM says tenure is a weak proxy [E: FH-001].
   - 189 of 222 Advanced knowledge statements begin "Expert in…". 192 of 222 Expert statements begin "Shapes/Advances/Leads…" [E: computed, FH-038].
4. Assessable anchors.
   - 454 of 1,183 Expert indicators (38.4%) are reputational [E: computed, FH-038].
   - Intermediate indicators are good: only 1 of 1,228 is reputational.
5. Duty-statement and Factor 1 language.
6. Needed-at-entry and distinguishing flags, and task importance and frequency fields.
7. General vs technical typing, mapped to OPM names and USA Hire.
8. Positive-education and credential flags (NWCG, FAC-COR, SAF CF, TWS CWB, AFS).
9. A corrected family→SOC crosswalk (§9, Q3).
10. Content that cannot be a federal requirement in 2026 [E: FH-011 for DEI; J for EJ]: 5.3.4 DEI and possibly 6.7.2 EJ. These need sector-actor applicability flags (CA decides).

### 6.2 Proficiency scale proposal (DP-4, with IO)

Grade bands are **indicative only, never a classification criterion**. The level names reflect my recollection of OPM proficiency scales [J]; check them against FWCI content (FH-044).

| Level | Definition | v1 | Professional (two-grade interval) | Technician (one-grade interval) |
|---|---|---|---|---|
| 1 Awareness | Recognizes the competency's purpose and when to involve others; workforce-wide literacy | — | any | any |
| 2 Developmental | Performs defined tasks under close guidance | Foundational | GS-5–7 | GS-3–5 |
| 3 Full performance | Independent across the full range of standard work; adapts methods; reviewed for soundness | Intermediate | GS-9–11 | GS-6–7 |
| 4 Advanced | Handles novel or contested problems; designs methods; leads others | Advanced | GS-12–13 | GS-8–9 |
| 5 Expert | Sets direction or standards for a program, region or agency; resolves the hardest cases | Expert | GS-14–15 | rare |

---

## 7. Federal role profile (the L3 grain FH needs)

**Proposed fields [J]**
- `role_id`
- `function`
- `title`
- `sector_actor = federal`
- `series_current`
- `series_former[]` (with effective dates)
- `interdisciplinary_series[]`
- `grade_band`
- `supervisory_status`
- `competency_targets[]`, each with `level`, `importance`, `needed_at_entry`, `distinguishing` and `time_to_proficiency`
- `task_bundle[]` (with time share)
- `grade_controlling_tasks[]`
- `usahire_general_competencies[]`
- `positive_education_requirement` (with qualification-standard version)
- `credentials_required[]`
- `exposure_summary` (computed)
- `entry_pipeline_series[]`
- `adjacent_series[]` (with barriers listed separately)
- `crosswalks`
- `provenance`
- `disclaimer`

**First role set:** the 13 crosswalked series at two grade bands each, giving 26 profiles.

---

## 8. Proposals

- **P-FH-01 — Federal entry point.** Make series × grade-band role profiles the federal entry point. The assessed unit is a competency at a proficiency level, and tasks are the job-analysis evidence. Families remain as views.
- **P-FH-02 — Versioned series register.** Keep a versioned OPM series register as an L6 crosswalk, with `status`, `effective_date` and `successor_series`.
  - Record each OPM issuance as a dated L5 event.
  - DE and IA ingest Federal Workforce Data headcounts monthly.
- **P-FH-03 — Align with FWCI, don't compete.**
  - Now: crosswalk general competencies to OPM names and USA Hire.
  - As OPM publishes them: crosswalk the 0400/1300/0800/0000 technical frameworks.
  - AS to explore offering EMST content and SME networks to OPM.
- **P-FH-04 — Proficiency scale.** Replace tenure bands with the five-level scale in §6.2. Rewrite Advanced and Expert anchors as observable outcomes. Ban reputational indicators except in research-grade variants.
- **P-FH-05 — Federal fields.** Add REQ-FH-01 to REQ-FH-20 (see `hr_use_cases.md`). Priority: duty templates, Factor 1 statements, needed-at-entry and distinguishing flags, and positive-education flags.
- **P-FH-06 — "EMST Job Analysis Starter Kit" for the 13 series.**
  - Contents: task inventory, rating sheet, SME-QA benchmark drafts by grade band, structured-interview bank, and one work-sample prompt per series.
  - Pilot with one talent team on 3–5 vacancies. IO designs the validation; FH runs the process.
  - Measure SME hours and time-to-hire against the 80-day target [E: FH-016].
- **P-FH-07 — SOC and series crosswalks.** Correct the family→SOC crosswalk and add family→series (§9, Q3).
- **P-FH-08 — Candidate competencies.** Add the 15 candidates.
  - Federal MVP priority: FH-C01, C02, C03, C04, C09, C13, C14.
  - Wording owners: SC (C01, C08, C11), DB (C12), DC (C05, C15), LC/FC (C06).
- **P-FH-09 — Retire or correct v1 claims** per §5.3. Rebuild the forester PD in FES format, reviewed by a classifier, before showing it to SAF or any agency again.
- **P-FH-10 — Guardrails as product features.**
  - Export disclaimers: "not a classification basis / not a job analysis / not for RIF or rating decisions".
  - Aggregate data by default.
  - No support for Schedule Policy/Career designation.
  - CP handles privacy and Section 508.
- **P-FH-11 — Validate the crosswalk before any external claim.**
  - Per series, sample at least 5 USAJOBS announcements from at least 3 agencies (2023–2026), via the USAJOBS historical API (IA).
  - Add duties from OPM classification appeal decisions and agency standard PDs.
  - IA extracts duties to EMST tasks. Two SMEs per series confirm each row, and IO computes agreement.
  - Only then move rows from J to E.
- **P-FH-12 — Entry-pipeline indicator.** Track entry pipelines as a standing federal indicator: computed entry-task exposure plus Federal Workforce Data counts of under-30 staff, student trainees (0499, 0099) and Pathways conversions. Feed the result to CLD.
- **P-FH-13 — Federal MVP series order.**
  - First: 0401, 0028, 0460, 0462, 0456, 0486, 0482, 1315, 0454, 0457, 0819, 0408, 0025.
  - Next: 0404, 1560, 0193, 0810, 1316, 0470.

---

## 9. Answers to CA architecture questions (§6, FH)

**Q1. What grain does skills-based hiring need? (DP-6)**

All three grains are needed, each for a different job:

| Grain | Job | Basis |
|---|---|---|
| Role (series × grade band) | **Use** | Hiring actions, qualification standards and USA Hire are all organized by series and grade [E: FH-026, FH-001] |
| Competency with proficiency | **Assessment** | The statute names "skills, abilities, knowledge, and competencies" [E: FH-023]; OPM centres "critical competencies identified through job analysis" [E: FH-002]; FWCI works per series [E: FH-017] |
| Task | **Evidence** | Job analysis under 5 CFR 300.103 links tasks to competencies [E: FH-002] |

This supports CA's hybrid: the Option B task spine, Option A packaging, and L3 as the federal door [J].

**Usable tomorrow [J]:** a profile of 6–10 critical competencies with anchors at the target level, plus 15–40 draft tasks, exported as a job-analysis rating sheet and an SME-QA benchmark draft.

**Q2. Which OPM artifacts to crosswalk, and how to track the consolidation?**

**Must crosswalk** [E for existence: FH-014, FH-017, FH-026, FH-044; J for priority]:
1. Series, with version and status.
2. Qualification standards: basic and positive-education requirements only, not agency selective factors.
3. FWCI general and technical models.
4. USA Hire coverage and the competencies it measures, by series and grade.
5. New competency-based classification and qualification standards.

**Should crosswalk [J]:** ECQs and OPM leadership programs; NWCG position qualifications; FAC-COR; the OPM AI competency model.

**Tracking change [J]:**
- Key every record to `(series_code, series_version_date)`.
- Set `status` to one of active, proposed-realignment, realigned-to:XXXX or cancelled, and record `successor_series`.
- Keep old codes as aliases; never overwrite.
- Record each OPM issuance as a dated L5 event, and re-check quarterly until Sep 2027 [E: FH-014].
- Anchor profiles to **function**, so a realignment such as 0455→0404 changes one attribute and the profile survives.
- Treat Phase One as "proposed" until finalization is confirmed.

**Q3. Verify the v1 family→SOC mappings.**

I could not reach BLS or O*NET either (CA-046). The table below rests on my working knowledge of the 2018 SOC [J]. IA should confirm it against the SOC 2018 structure file and O*NET-SOC 2019.

| Family | v1 | Assessment | Proposed |
|---|---|---|---|
| F12 Fire | 33-1021 labelled "Fire Inspectors" | Title wrong: 33-1021 is First-Line Supervisors of Firefighting and Prevention Workers | Primary 33-2011 Firefighters; secondary 33-2022 Forest Fire Inspectors and Prevention Specialists and 33-1021; federal 0456/0462 |
| F13 Env Health & Justice | 29-9021 | Not environmental: it is Health Information Technologists and Medical Registrars | 19-2041 Environmental Scientists and Specialists, Including Health; 19-5011; 19-4042 |
| F11 Env Education | 25-2031 / 25-4031 | 25-4031 is Library Technicians (wrong); 25-2031 fits school-based roles only | 25-9031 Instructional Coordinators; 19-1031 (O*NET places park naturalists there); federal 0025/1701 |
| F10 Sustainable Agriculture | 19-1012 labelled "Farm & Home Mgmt Educators" | Code–title mismatch: 19-1012 is Food Scientists and Technologists; Farm and Home Management Educators is 25-9021 | 19-1013 Soil and Plant Scientists; 25-9021; 19-4012; federal 0457/0470/0471 |
| all | 19-2041 absent | The largest environmental SOC is missing | Add to F8, F13 and parts of F3/F5; it is the natural match for 0028 |
| F8 Env Policy | 23-1011 / 11-9199 | Fragmented | Add 19-2041, 13-1041 Compliance Officers, 19-3011 Economists |
| F1, F2, F4, F9 | 19-1032, 19-1023, 19-2043, 19-3051 | Plausible | Carry; add 19-4071 Forest and Conservation Technicians to F1 (the 0462 counterpart) |

**Q4. What proficiency scale will OPM-aligned users accept? (DP-4)**

The five-level responsibility scale in §6.2 [J]; check its names against FWCI (FH-044).
- **They will reject** tenure bands and reputational anchors [J; E: FH-001].
- **They need:**
  - an indicative grade-band map, labelled "not a classification criterion";
  - levels that track independence and complexity, which parallels FES Factors 2, 4 and 5.
- **Structure:** a generic scale plus competency-specific anchors at the levels where each competency is actually practiced (CA Option A). This is what SME-QA benchmarks need.

---

## 10. Disagreements and trade-offs

1. **Families vs series profiles (with v1, partly CA).**
   - *Trade-off:* identity views legible to students vs profiles HR can act on.
   - *Recommendation:* keep both, with series profiles as the federal door.
2. **Competency vs task as what users touch (likely with IO).**
   - *Position:* tasks validate better, but every federal hiring artifact is competency-shaped [E: FH-023, FH-017, FH-026].
   - *Recommendation:* task spine with competency packaging.
3. **Precision vs portability in statecraft (with SC).**
   - *Trade-off:* hiring benchmarks need Section 7, Section 106 and NEPA specificity; portability needs statute-neutral wording.
   - *Recommendation:* statute-neutral titles, with federal-specific **tasks and anchors** in the federal variant.
4. **FES language vs learner language (with LC).**
   - *Recommendation:* store two renderings per competency.
5. **Tool-neutral duties vs tool-specific postings (with DC).**
   - *Recommendation:* L4 supplies tool examples; competencies stay durable.
6. **DEI and EJ content (with CA, SL, TN).**
   - *Trade-off:* these cannot be federal requirements in 2026 [E: FH-011; J], but deleting them misrepresents state, NGO and Tribal practice. Federal adoptability vs sector completeness.
   - *Recommendation:* applicability flags, and keep them out of federal default profiles. CA decides.
7. **Biggest trade-off: coupling to OPM.**
   - *Tight coupling* is the fastest route to adoption and could make EMST the environmental technical layer OPM lacks. But it ties EMST to a system being redesigned through 2027, to political churn, and to the risk that OPM's own technical models supersede it.
   - *Loose coupling* keeps EMST portable, which is the theory of change, but leaves it as "one more framework."
   - *Recommendation:* function-first profiles, versioned crosswalks, and an explicit offer to *feed* FWCI (P-FH-03).

---

## 11. Issues outside my area that affect the vision

- **CP:**
  - Competency ratings retrieved by employee name are likely a Privacy Act system of records. That needs a SORN, or aggregate-only design.
  - Exports must meet Section 508.
- **AS and CA:** Essay questions, Schedule Policy/Career and the DEI rescission are all contested or litigated [E: FH-032, FH-028]. EMST must stay nonpartisan, supply no essay content, and give no help with political designations.
- **AS (labor relations):**
  - Changes to PDs, RIFs and appraisals trigger bargaining obligations [E: FH-014, FH-045].
  - Consult AFGE, NFFE, NTEU and PEER on non-punitive use before pilots.
- **TN and SL:**
  - Tribal programs run under self-determination contracts or compacts employ many people outside title 5.
  - FH-C08, and Section 7 wording that touches Tribal consultation, need TN review.
- **SL and CM:** separated federal staff are moving to states and localities, so state class crosswalks are needed.
- **FC, SC, LM and DE to confirm:**
  - the U.S. Wildland Fire Service and the USDA reorganization;
  - NEPA procedure changes since 2025, which make v1 6.1.4 indicators outdated;
  - 2025 losses at EPA, NOAA, USGS, BOR, BIA, NRCS and USACE.
- **AS (claims):** The Flourish guide's "validated against OPM … classification systems" claim (per the CA audit) must not be repeated. This crosswalk is the first competency-level OPM crosswalk, and it is judgment-grade.

---

## 12. Open questions for the Chief Taxonomy Architect

1. Should series × grade-band role profiles be the federal MVP grain, with families demoted to views? (DP-6)
2. Adopt the five-level responsibility scale with indicative grade bands, or keep four levels with a mapping? (DP-4, with IO)
3. Should AS open a channel to FWCI, accepting the risk of co-option? Or stay an independent crosswalk?
4. How should DEI and EJ competencies be represented: applicability flags (my proposal), variants, or removal? (DP-7)
5. May the register carry "proposed-realignment" status until OPM confirms Phase One? (DP-10)
6. Who owns Phase 3 verification (P-FH-11), with enough web budget to read the OPM standards, FWCI and Federal Workforce Data? I recommend FH with IA.

---

## 13. Files in this folder

| File | Contents |
|---|---|
| `report.md` | This report |
| `hr_use_cases.md` | Five federal HR workflows with guardrails, and requirements REQ-FH-01–20 |
| `opm_series_register.csv` | 73 OPM series |
| `opm_series_to_emst_crosswalk.csv` | 193 rows, 13 series |
| `v1_assessment.csv` | 38 verdicts |
| `candidate_competencies.csv` | FH-C01–C15 |
| `role_signals.csv` | FH-R01–R15 |
| `ecosystem.csv` | 29 entities |
| `sources.csv` | 51 sources (FH-001–051), 8 unverified or blocked |
| `scripts/` | Python generators for the CSVs (`sources.py`, `register.py`, `xwalk.py`, `v1a.py`, `cand.py`, `eco.py`) |
