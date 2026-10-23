# Verification pass — brief (Phase 2b)

During Phase 2 the team's shared web-search budget ran out, so 340 of 1,084 sources and ~314 ecosystem entries were
recorded from prior knowledge and marked `unverified`. Before the Chief Architect finalizes decisions and before any
sector-facing material is published, the claims that matter most must be checked against current primary sources.
Today is **2026-10-23**.

## Inputs
- `docs/research/_verification/queue.csv` — every unverified source/ecosystem item, with a `theme` column (V1–V4).
- The **key facts** for your theme (below) — these will appear in the public package, so they come first.
- Role folders under `docs/research/<role>/` if you need context (read-only for you).

## Method
1. Verify the **key facts** for your theme first. For each: find the primary or most authoritative current source
   (agency, Federal Register, court, statute, standards body, the publisher itself), confirm or correct the claim.
2. Then work through queue items for your theme, prioritizing: government/legal/standard sources > items cited for
   numbers or dates > ecosystem entities named as top connections > everything else. One search can often settle
   several items. Aim for breadth; don't spend more than ~3 calls on any one item.
3. Use WebSearch (mode "standard"; "extended" only for stubborn, high-stakes items) and WebFetch. Never invent URLs,
   dates, or quotes. If you cannot reach or confirm something, say `unreachable` or `not-found` — that is useful.
4. Do **not** edit role folders. Write only your two output files.

## Outputs (CSV, UTF-8, header row)
`docs/research/_verification/<THEME>_key_facts.csv`
`fact_id,claim_as_stated,stated_by,verification_status,correct_statement,source_title,source_publisher,source_date,source_url,note`

`docs/research/_verification/<THEME>_queue_results.csv`
`item_id,role_folder,item_type,title,verification_status,checked_url,source_date,finding,corrected_fields`

`verification_status` ∈ verified | corrected | refuted | not-found | unreachable | superseded

Final reply (≤200 words): counts by status, the most consequential corrections, and anything the team must stop saying.

## Key facts by theme

### V1 — federal & public workforce, HR policy, reorganization
- V1-01 Federal civilian workforce fell from ~2.31M (Sep 2024) to ~2.04M (Jan 2026); ~317k departures in 2025 (PPS / OPM data).
- V1-02 USFS and NPS each lost >25% of employees Sep 2024–Jan 2026; park rangers −34.1%; under-30 share of federal workforce 7.9%.
- V1-03 EPA staff fell to ~12,849 (≈−24%); median service of departing EPA staff ~30.3 years.
- V1-04 USFS hired no non-fire seasonal employees in 2025 and committed to ~2,000 for 2026.
- V1-05 AmeriCorps cuts of ~$400M hit conservation corps; FY2026 AmeriCorps status (settlement/stay to Feb 1, 2027).
- V1-06 The U.S. Wildland Fire Service was established at DOI in January 2026, consolidating bureau fire programs (incl. BIA); ~5,780 federal + ~900 Tribal fire personnel.
- V1-07 USDA/USFS reorganization: HQ to Salt Lake City; nine regional offices closing; 57 of 77 research facilities closing; relocations through 2027.
- V1-08 EO 14356 (Oct 15, 2025) created agency Strategic Hiring Committees approving every vacancy, with annual staffing plans.
- V1-09 OPM Merit Hiring Plan (May 29, 2025); self-assessment questionnaires may not rank candidates after Sep 30, 2025; technical-assessment adoption rates (91% self-report-only in FY2025; 34.3% technical by FY2026 Q2).
- V1-10 OPM Phase One occupational series consolidation memo (Apr 24, 2026): 115 series; 0410/0437/0480/0487→0401; 0455→0404; 0029→0303; 0688→0601.
- V1-11 OPM issued competency-based classification and qualification standards for 2210 on Apr 13, 2026 under the Federal Workforce Competency Initiative (FWCI); targets of 300+ / 600+ series.
- V1-12 Schedule Policy/Career final rule (Feb 6, 2026; effective Mar 9, 2026) and a June 2026 EO moving ~8,000 employees.
- V1-13 OPM memo of Aug 27, 2026 on AI use in hiring (AI-drafted PDs generally not high-impact when humans adopt them).
- V1-14 Conservation job postings fell 29.4% YoY (Mar–Sep 2025); paid internships −43.8%; AmeriCorps postings −42%.
- V1-15 FY2026 Interior–Environment appropriations ≈ $42.56bn (−1.9% YoY), well above the President's request.
- V1-16 Federal Workforce Data (data.opm.gov) replaced FedScope (Jan 2026).
- V1-17 Natural Resources Management named a Tier 2 occupational group for Chance to Compete technical assessments, full implementation FY2028.

### V2 — environmental law & policy, Tribal policy, compliance/accessibility/security rules
- V2-01 CEQ's NEPA regulations were removed (interim final rule 2025; final removal effective Jan 8, 2026?) and agencies adopted their own procedures (DOI handbook; USDA 7 CFR 1b).
- V2-02 Seven County Infrastructure Coalition v. Eagle County (May 2025) — "substantial deference" to agency NEPA judgments.
- V2-03 SPEED Act passed the House (Dec 18, 2025); current Senate status; key provisions (150-day limitations period; standing tied to substantive comments).
- V2-04 NEPA §112 sponsor-funded expedited reviews (180-day EA / 1-year EIS) — status and use.
- V2-05 ESA "harm" definition rescission — final? effective date; litigation.
- V2-06 EPA GHG endangerment finding rescission — final? date; litigation.
- V2-07 WOTUS rule status (2025–26 proposal/final).
- V2-08 CEQ permitting technology: data standard version (v1.2.0?), Permitting Technology Action Plan, PermitAI/NEPATEC.
- V2-09 OMB M-25-21 and M-25-22 (Apr 2025) on federal AI use and acquisition; M-26-04 (LLM procurement) and M-26-05 (secure software, rescinding M-22-18/M-23-16), Jan 2026.
- V2-10 FedRAMP 20x and the "Consolidated Rules for 2026" (certification classes; dates).
- V2-11 DOJ ADA Title II web accessibility deadlines moved to Apr 26, 2027 / Apr 26, 2028 (interim final rule, Apr 2026); WCAG 2.1 AA.
- V2-12 WCAG 2.2 published as ISO/IEC 40500:2025.
- V2-13 EO 13175 still in effect; EO 14112 rescinded; status of Joint Secretarial Order 3403 and federal Indigenous Knowledge guidance; DOI 301 DM 7.
- V2-14 ACHP Section 106 regulations rewrite — status.
- V2-15 California SB 253/261 status and first reporting dates (SB 253 first reports due ~Nov 10, 2026?); EU CSRD Omnibus I thresholds (>1,000 employees, >€450m turnover).
- V2-16 CEQA reforms enacted 2025 (AB 130 / SB 131).
- V2-17 FAA Part 108 (BVLOS) rule status; American Security Drone Act / FCC Covered List effects on agency drones.

### V3 — organizations, credentials, programs, education standards (ecosystem atlas)
- V3-01 O*NET current database release (31.0?), RDF format availability, and an O*NET AI-impact methods report (June 2026?).
- V3-02 SOC 2028 revision status (Federal Register notices).
- V3-03 Workforce Pell live Jul 1, 2026 with state boards approving programs; WIOA reauthorization (A Stronger Workforce for America Act, H.R. 8210 2026?) status.
- V3-04 CESU Network: 17.5% indirect cost cap; number of partners.
- V3-05 The Corps Network: ~140 corps, 22,000+ participants/year; Resource Assistants Program with USFS.
- V3-06 Credential Engine Registry reach (states); CTDL current.
- V3-07 Professional societies active and current names: SAF, TWS, AFS, SER, NAEP, ESA, AWWA, WEF, A&WMA, NEHA, ISSP (status?), NAAEE, SRM, ASFPM, APA/AICP, ABCEP (CEP credential issuer), ECO Canada.
- V3-08 Credential issuers for: REHS/RS (NEHA), CHMM (IHMM), CFM (ASFPM), CPESC (EnviroCert), PWS (SWS PCP), CWB (TWS), SAF Certified Forester, CERP (SER), ISA Certified Arborist, QEP (IPEP), ISSP-CSP, LEED AP (USGBC), state water/wastewater operator certification (ABC).
- V3-09 NCES CIP 2020 and the CIP–SOC crosswalk (current version / any 2025–26 update).
- V3-10 Status of major funders' environmental-workforce/AI programs (Moore, Packard, Walton, Doris Duke, Bezos Earth Fund AI for Climate & Nature Grand Challenge, Google.org AI Collaborative: Wildfires, Schmidt Sciences).
- V3-11 Is there an existing environment-sector-wide coalition focused on workforce skills and AI (e.g., Coalition of Natural Resource Societies)? Confirm or state none found.
- V3-12 EPA Brownfields Job Training grants (2026 round; amounts).
- V3-13 NWCG and USWFS aligned wildland fire qualifications effective Jan 2027.

### V4 — AI & labor-market indices, data and interoperability standards (run after LM/IA finish)
- Assigned later.

### V4 — AI & labor-market indices, data and interoperability standards (queue: `queue_v4.csv`)
- V4-01 Anthropic Economic Index: list every public release through Oct 2026 (dates, titles), what the latest adds (task-level usage, automation vs augmentation, API/enterprise, geography), and the public dataset location/licence.
- V4-02 Microsoft "Working with AI" occupational applicability (Tomlinson et al., 2025): status/date; any 2026 update.
- V4-03 Brynjolfsson, Chandar & Chen "Canaries in the Coal Mine?" (2025) — finding on early-career employment in AI-exposed occupations; any 2026 follow-ups.
- V4-04 ILO generative-AI exposure index — latest refinement (2025) and headline.
- V4-05 WEF Future of Jobs 2025 (Jan 2025) — confirm; any 2026 edition.
- V4-06 LinkedIn Global Green Skills Report — latest edition/date.
- V4-07 BLS Employment Projections — current 10-year cycle (2024–34?) release date; BLS AI-impact case studies in the Monthly Labor Review.
- V4-08 O*NET 31.0 (Aug 2026?) and next update; O*NET-SOC 2019 still current.
- V4-09 ESCO current version (v1.2.1, Dec 2025?).
- V4-10 1EdTech CASE 1.1 final (Apr 2025?); Credential Engine stewardship of RSD/OSMT since Feb 2025; CTDL-ASN updates (Jan 2025).
- V4-11 IEEE 1484.20.3-2022 status and amendment PAR (2025).
- V4-12 W3C Verifiable Credentials 2.0 Recommendation (May 2025); Open Badges 3.0 current.
- V4-13 SSSOM 1.0 / 1.1 status.
- V4-14 NIST AI RMF 1.0 and Generative AI Profile (NIST AI 600-1) — any 2025–26 revisions; OPM AI competency model (2024).
- V4-15 OMB 2025 federal AI use-case inventory (published? where; counts for USDA, DOI, EPA, DOC/NOAA).
- V4-16 Earth-observation foundation models in operational use (e.g., Prithvi, Clay, AlphaEarth Foundations) — confirm names/dates.
- V4-17 Stanford AI Index 2026 published (date).
