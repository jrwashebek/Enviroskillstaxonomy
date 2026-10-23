#!/usr/bin/env python3
"""Build the EMST Ecosystem Atlas (WP-13).

Merges docs/research/_merged/ecosystem.csv (626 rows from 18 roles) with the Phase 2b
verification results (docs/research/_verification/) into docs/adoption/ecosystem_atlas.csv.

- Deduplicates entities that several roles recorded (manual cluster map below; every
  other row is a singleton). Provenance of contributing rows and roles is kept.
- Carries the best-verified status and URL across a cluster and attaches key-fact checks.
- Applies the verification corrections (names, URLs, status text) and the corrected-facts
  list in ADR-0027 s3.
- Flags Tribal-related rows and holds them (ADR-0007 s D; tribal_gate_procedures.md).
- Records no commitments: the commitment register is the only source of committed status.

Run from the repository root:  python3 -I docs/adoption/scripts/build_ecosystem_atlas.py
Licence: Apache-2.0. Output licence: CC0-1.0.
"""
import csv, re, sys
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
R = ROOT / 'docs/research'
OUT = ROOT / 'docs/adoption/ecosystem_atlas.csv'
RUN_DATE = '2026-10-23'          # date of the Phase 2b verification pass and of this build
REVIEW_FAST = '2027-01-23'       # +3 months: policies, indices, datasets, platforms, tools, funds; weakly verified rows
REVIEW_SLOW = '2027-04-23'       # +6 months: before the April MINOR

def read(p):
    with open(p, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

eco = read(R / '_merged/ecosystem.csv')
results = {r['item_id']: r for r in read(R / '_verification/ALL_queue_results.csv')}
facts = {r['fact_id']: r for r in read(R / '_verification/ALL_key_facts.csv')}
queued = {r['item_id'] for r in read(R / '_verification/queue.csv') if r['item_type'] == 'ecosystem'}
queued |= {r['item_id'] for r in read(R / '_verification/queue_v4.csv') if r['item_type'] == 'ecosystem'}
sources = {r['source_id']: r for r in read(R / '_merged/sources.csv')}
byid = {r['entity_id']: r for r in eco}

ROLE_CODE = {'adoption-stewardship': 'AS', 'chief-architect': 'CA', 'compliance-product': 'CP',
             'data-craft': 'DC', 'data-engineering': 'DE', 'domain-bench': 'DB', 'federal-human-capital': 'FH',
             'field-craft': 'FC', 'interop-skills-intelligence': 'IA', 'io-validation': 'IO',
             'labor-market-ai-impact': 'LM', 'learning-curriculum': 'LC', 'mobility-workforce-voice': 'CM',
             'private-sector': 'PS', 'state-local': 'SL', 'statecraft': 'SC', 'strategic-foresight': 'FS',
             'tribal-sovereignty': 'TN'}

# ---------------------------------------------------------------- clusters (same entity, several roles)
CLUSTERS = {
 'onet-db': ['AS-E001', 'CA-ECO-001', 'IA-ECO-001', 'IO-E19', 'ECO-LM-26', 'DB-ECO-048'],
 'onet-online': ['CP-ECO-20', 'IA-ECO-002'],
 'case': ['AS-E053', 'IA-ECO-008'],
 'soc2028': ['AS-E003', 'LC-E-08'],
 'wioa-aswa': ['AS-E015', 'SL-E13'],
 'awma': ['AS-E082', 'DB-ECO-013'],
 'aihec': ['AS-E101', 'TN-E23'],
 'awwa': ['AS-E080', 'DB-ECO-001'],
 'americorps': ['AS-E017', 'EC-CM-10'],
 'aei': ['ECO-LM-01', 'AS-E135'],
 'abc-wpi': ['DB-ECO-003', 'SL-E29'],
 'acwa': ['AS-E029', 'SL-E24', 'DB-ECO-005'],
 'afwa': ['AS-E027', 'SL-E22'],
 'astswmo': ['AS-E031', 'SL-E26', 'DB-ECO-015'],
 'asdwa': ['AS-E028', 'SL-E23', 'DB-ECO-004'],
 'asfpm': ['AS-E087', 'DB-ECO-024'],
 'asc': ['AS-E064', 'CA-ECO-006'],
 'birdnet': ['DC-ECO-23', 'FC-E25'],
 'bls-ep': ['ECO-LM-16', 'PS-ECO-003'],
 'bgi': ['AS-E045', 'ECO-LM-20', 'EC-CM-06', 'IO-E16'],
 'ca-sb253': ['PS-ECO-008', 'SC-E12', 'FS-ECO-22'],
 'care': ['AS-E057', 'TN-E01', 'DC-ECO-25', 'CP-ECO-37'],
 'ceq-standard': ['AS-E022', 'SC-E02', 'DC-ECO-11', 'FS-ECO-03', 'LC-E-18', 'SC-E01'],
 'ctc': ['AS-E005', 'EC-CM-20', 'IO-E06', 'FH-E25'],
 'chco': ['AS-E008', 'FH-E09'],
 'cieem': ['AS-E066', 'FC-E23'],
 'corps-network': ['AS-E108', 'EC-CM-09', 'LC-E-24'],
 'crs': ['FH-E13', 'SC-E06', 'FS-ECO-14'],
 'credential-engine': ['AS-E046', 'LC-E-10', 'IA-ECO-005', 'DE-ECO-06'],
 'eco-canada': ['AS-E062', 'DB-ECO-046', 'PS-ECO-029'],
 'ecos': ['AS-E025', 'SL-E20', 'DB-ECO-045'],
 'ehac': ['LC-E-04', 'DB-ECO-022'],
 'epa-bf': ['AS-E013', 'DB-ECO-018'],
 'epa-iwiwd': ['DB-ECO-009', 'LC-E-14'],
 'esco': ['AS-E060', 'CA-ECO-002', 'IA-ECO-003', 'CP-ECO-23', 'EC-CM-17', 'DB-ECO-049'],
 'eu-omnibus': ['PS-ECO-007', 'SC-E13'],
 'faa108': ['FC-E06', 'FS-ECO-21'],
 'ai-inventory': ['ECO-LM-27', 'DC-ECO-01', 'FS-ECO-20'],
 'unions': ['FH-E15', 'EC-CM-12'],
 'fwd': ['FH-E07', 'EC-CM-01', 'ECO-LM-28', 'FS-ECO-07'],
 'gao': ['AS-E020', 'FH-E12', 'FS-ECO-13'],
 'gee-alphaearth': ['DC-ECO-17', 'FS-ECO-19'],
 'ieee': ['AS-E055', 'IA-ECO-010'],
 'isep': ['AS-E065', 'PS-ECO-005'],
 'ihmm': ['AS-E092', 'DB-ECO-017'],
 'isa': ['FC-E18', 'PS-ECO-017'],
 'issb': ['PS-ECO-006', 'DB-ECO-030'],
 'issp': ['AS-E084', 'DB-ECO-032'],
 'itep': ['AS-E102', 'TN-E18', 'LC-E-25'],
 'itc': ['AS-E103', 'TN-E15'],
 'lightcast': ['AS-E051', 'EC-CM-04', 'IA-ECO-021', 'CP-ECO-24', 'CA-ECO-009', 'ECO-LM-15'],
 'linkedin': ['AS-E052', 'ECO-LM-14', 'PS-ECO-024'],
 'localcontexts': ['AS-E056', 'TN-E02', 'FC-E33'],
 'arset': ['AS-E142', 'LC-E-20'],
 'nasa-esdt': ['DC-ECO-29', 'FS-ECO-17'],
 'nacaa': ['AS-E030', 'SL-E25', 'DB-ECO-011'],
 'naco': ['AS-E037', 'SL-E15'],
 'abcep': ['AS-E077', 'PS-ECO-011'],
 'napa': ['AS-E019', 'FH-E14'],
 'nasf': ['AS-E026', 'SL-E21', 'SC-E10'],
 'naspe': ['AS-E032', 'SL-E18'],
 'naswa': ['AS-E033', 'SL-E19'],
 'nawb': ['AS-E036', 'SL-E14'],
 'nafws': ['AS-E104', 'TN-E17'],
 'neha': ['AS-E083', 'DB-ECO-019', 'SL-E27'],
 'nice': ['AS-E059', 'EC-CM-18', 'CA-ECO-003'],
 'nwcg': ['FH-E17', 'LC-E-15', 'IO-E08', 'FC-E01'],
 'fire-quals': ['AS-E010', 'EC-CM-21'],
 'oecd': ['AS-E144', 'ECO-LM-17'],
 'omb-ai': ['CP-ECO-04', 'DC-ECO-05', 'DC-ECO-06'],
 'ob3': ['AS-E058', 'IA-ECO-009'],
 'osmt': ['DE-ECO-05', 'CA-ECO-011', 'IA-ECO-006'],
 'openlmp': ['AS-E024', 'ECO-LM-30', 'SC-E19', 'DC-ECO-13', 'CP-ECO-26', 'FC-E32', 'CA-ECO-013',
             'DE-ECO-07', 'SL-E17', 'LC-E-29', 'IA-ECO-013', 'DB-ECO-050'],
 'opm-ai-cm': ['DC-ECO-07', 'FH-E22'],
 'opm-class': ['AS-E004', 'FH-E02', 'CA-ECO-012'],
 'merit': ['FH-E24', 'IO-E05', 'AS-E007'],
 'oaw': ['AS-E043', 'IO-E23', 'SL-E03'],
 'nga': ['AS-E034', 'EC-CM-07', 'SL-E01'],
 'pps': ['AS-E018', 'EC-CM-13', 'FH-E11', 'ECO-LM-31'],
 'pnnl': ['AS-E023', 'LC-E-19', 'DC-ECO-12', 'SC-E03', 'FS-ECO-04'],
 'saf': ['AS-E073', 'LC-E-01'],
 'sfia': ['AS-E061', 'CA-ECO-005', 'IO-E11'],
 'skillsfuture': ['AS-E063', 'CA-ECO-007', 'CP-ECO-22'],
 'smeqa': ['FH-E05', 'IO-E07'],
 'sssom': ['DE-ECO-01', 'IA-ECO-011'],
 'sdel': ['AS-E107', 'ECO-LM-08'],
 'trellis': ['ECO-LM-32', 'PS-ECO-002'],
 'uswfs': ['AS-E009', 'LC-E-16'],
 'usahire': ['FH-E04', 'AS-E006'],
 'usajobs': ['AS-E021', 'IA-ECO-022', 'ECO-LM-29'],
 'useer': ['ECO-LM-33', 'DB-ECO-038'],
 'vendor-skills': ['IA-ECO-024', 'CP-ECO-25'],
 'wef-foj': ['AS-E143', 'ECO-LM-13', 'FS-ECO-23'],
 'wef-water': ['AS-E081', 'DB-ECO-002'],
 'workforce-pell': ['AS-E016', 'LC-E-11'],
 'megadetector': ['DC-ECO-22', 'FC-E26'],
 'fed-training': ['LC-E-26', 'FH-E19'],
 'naaee': ['AS-E085', 'LC-E-05'],
 'abet': ['AS-E094', 'LC-E-02', 'LC-E-03'],
 'iap2': ['SC-E14', 'AS-E091'],
 'tni': ['DB-ECO-044', 'FC-E12'],
 'gcse': ['LC-E-06', 'AS-E099'],
 'esip': ['AS-E141', 'DC-ECO-31'],
}

# ---------------------------------------------------------------- key facts and source-item checks attached to entities
FACTS = {
 'onet-db': ['V3-01', 'V4-08'], 'AS-E002': ['V3-01'], 'soc2028': ['V3-02'], 'wioa-aswa': ['V3-03'],
 'workforce-pell': ['V3-03'], 'AS-E014': ['V3-04'], 'corps-network': ['V3-05'], 'credential-engine': ['V3-06', 'V4-10'],
 'saf': ['V3-07', 'V3-08'], 'AS-E074': ['V3-07', 'V3-08'], 'AS-E075': ['V3-07'], 'AS-E086': ['V3-07'],
 'AS-E079': ['V3-07', 'V3-08'], 'neha': ['V3-07', 'V3-08'], 'asfpm': ['V3-07', 'V3-08'], 'abcep': ['V3-07'],
 'eco-canada': ['V3-07'], 'issp': ['V3-07', 'V3-08'], 'isep': ['V3-07'], 'DB-ECO-031': ['V3-07'],
 'ihmm': ['V3-08'], 'isa': ['V3-08'], 'FC-E17': ['V3-08'], 'abc-wpi': ['V3-08'],
 'AS-E124': ['V3-10'], 'AS-E125': ['V3-10'], 'AS-E120': ['V3-10'], 'AS-E122': ['V3-10'], 'AS-E123': ['V3-10'],
 'AS-E126': ['V3-10'], 'AS-E096': ['V3-11'], 'epa-bf': ['V3-12'], 'nwcg': ['V3-13'], 'fire-quals': ['V3-13'],
 'opm-class': ['V1-10'], 'FH-E01': ['V1-11'], 'FH-E03': ['V1-11'], 'ctc': ['V1-17', 'V1-09'], 'merit': ['V1-09'],
 'FH-E26': ['V1-08'], 'fwd': ['V1-16'], 'uswfs': ['V1-06'], 'AS-E011': ['V1-07', 'V1-04'], 'americorps': ['V1-05'],
 'CP-ECO-05': ['V1-13'], 'FH-E27': ['V1-12'], 'pps': ['V1-01', 'V1-02'], 'FS-ECO-08': ['V1-14'],
 'ceq-standard': ['V2-08'], 'pnnl': ['V2-08'], 'omb-ai': ['V2-09'], 'CP-ECO-06': ['V2-09'], 'CP-ECO-01': ['V2-10'],
 'CP-ECO-08': ['V2-11'], 'CP-ECO-10': ['V2-12'], 'TN-E06': ['V2-13'], 'TN-E05': ['V2-13'], 'TN-E08': ['V2-13'],
 'TN-E07': ['V2-14'], 'ca-sb253': ['V2-15'], 'eu-omnibus': ['V2-15'], 'faa108': ['V2-17'], 'FC-E07': ['V2-17'],
 'SC-E07': ['V2-01'], 'aei': ['V4-01'], 'ECO-LM-03': ['V4-01'], 'ECO-LM-06': ['V4-02'], 'sdel': ['V4-03'],
 'ECO-LM-11': ['V4-04'], 'wef-foj': ['V4-05'], 'linkedin': ['V4-06'], 'bls-ep': ['V4-07'], 'esco': ['V4-09'],
 'case': ['V4-10'], 'osmt': ['V4-10'], 'ieee': ['V4-11'], 'ob3': ['V4-12'], 'sssom': ['V4-13'],
 'DC-ECO-03': ['V4-14'], 'opm-ai-cm': ['V4-14'], 'ai-inventory': ['V4-15'], 'DC-ECO-14': ['V4-16'],
 'DC-ECO-16': ['V4-16'], 'gee-alphaearth': ['V4-16'], 'ECO-LM-18': ['V4-17'],
}
SOURCE_CHECKS = {'IO-E01': ['IO-020', 'IO-022'], 'IO-E21': ['CP-043']}

# ---------------------------------------------------------------- corrections (verification findings and ADR-0027 s3)
NAME = {
 'onet-db': 'O*NET database and programme (National Center for O*NET Development)',
 'abc-wpi': 'Water Professionals International (formerly Association of Boards of Certification, ABC)',
 'issp': 'International Society of Sustainability Professionals (ISSP) credentials, now offered by GBCI',
 'isep': 'ISEP: Institute of Sustainability and Environmental Professionals (formerly IEMA)',
 'DB-ECO-031': 'ISEP (formerly IEMA) Sustainability / Environment Skills Map',
 'lightcast': 'Lightcast Skills Taxonomy (formerly Open Skills) and job-posting data',
 'DC-ECO-19': 'GEO-Bench / GEO-Bench-2',
 'AS-E096': 'Coalition of Natural Resource Societies (not found as an active body)',
 'fire-quals': 'Federal Wildland Fire Qualifications Supplement and IQCS 2026 Transition Plan (USWFS-USFS aligned standards)',
 'EC-CM-24': 'Five Functional Positions framework (EMST v1 project document)',
 'opm-class': 'OPM occupational series modernization and consolidation (Phase One list proposed)',
 'ieee': 'IEEE 1484.20.3-2022 Sharable Competency Definitions (and P1484.20.3a)',
 'aei': 'Anthropic Economic Index (reports and datasets)',
 'ceq-standard': 'CEQ Permitting Innovation Center and NEPA & Permitting Data and Technology Standard',
 'pnnl': 'PNNL PermitAI (NEPATEC 3.0, PermitTEC, DraftNEPABench and shared services)',
 'credential-engine': 'Credential Engine (CTDL, CTDL-ASN, Credential Registry)',
 'corps-network': 'The Corps Network',
 'americorps': 'AmeriCorps (national service funding for corps)',
 'AS-E123': 'Doris Duke Foundation (Environment; formerly Doris Duke Charitable Foundation)',
 'TN-E03': 'United States Indigenous Data Sovereignty Network (USIDSN)',
 'esco': 'ESCO (European Skills, Competences, Qualifications and Occupations), incl. green skills collection',
 'nga': 'National Governors Association Center for Best Practices (incl. Skills in the States)',
 'iap2': 'IAP2: International Association for Public Participation (and IAP2 USA)',
 'gcse': 'Global Council for Science and the Environment (incl. Council of Environmental Deans and Directors)',
 'nwcg': 'National Wildfire Coordinating Group (NWCG) qualification system (PMS 310-1, Position Task Books)',
}
STATUS = {
 'onet-db': 'O*NET 31.0 (Aug 2026); CSV, JSON and RDF downloads added Jul 2026; O*NET-SOC 2019 remains the taxonomy; no later database release announced as of Oct 2026; modernized Work Context slated for a future release',
 'AS-E002': 'Report "Indexing the Impact of AI within the O*NET System: A Review of Methods and Development of Recommendations" (Jun 2026)',
 'soc2028': 'First FRN Jun 12 2024 (comments closed Aug 12 2024); second FRN with initial recommendations TBD; final 2028 SOC planned for 2027',
 'wioa-aswa': 'H.R. 8210 introduced Apr 6 2026 and ordered reported 19-14 by House Education and Workforce Apr 21 2026; no floor vote or Senate action found; WIOA not reauthorized',
 'workforce-pell': 'Final rule May 18 2026; eligible short programmes (150-599 clock hours, 8 to under 15 weeks) from Jul 1 2026; governors, working with state workforce boards, identify in-demand occupations and approve programmes; ED then reviews',
 'AS-E014': '17 CESUs and 500+ partners (Apr 2024); work under CESU master agreements capped at 17.5% overhead',
 'corps-network': '140 member organizations engaging 22,000+ young people a year; Resource Assistants Program page does not show 2025-26 activity or scale (check before citing RAP as live)',
 'credential-engine': 'About 49 state partners (page last modified May 2024); CTDL actively maintained (credential-types update Jun 11 2025; qualifications frameworks Jul 9 2025); OSMT and RSD transitioned to Credential Engine Feb 2025',
 'abc-wpi': 'ABC is now Water Professionals International: maintains standardized operator exams and need-to-know criteria; water and wastewater operator certification is issued by state programmes, not by WPI',
 'issp': 'ISSP-SA and ISSP-CSP credentials offered by GBCI since Dec 2019; no current independent ISSP activity found; do not cite ISSP as an independent active issuer',
 'isep': 'IEMA rebranded as ISEP by Jul 2025; iema.net redirects to isepglobal.org; do not use IEMA as the current name',
 'DB-ECO-031': 'Refer to as the ISEP (formerly IEMA) skills map; any revision not checked',
 'AS-E096': 'NOT FOUND as an active body. Closest activity: ad hoc joint statement by AFS, SAF, SRM and TWS on federal workforce reductions (Feb 27 2025), naming no standing coalition and not addressing AI or skills frameworks. No active environment-sector-wide workforce/AI coalition exists; the four-society group is a partner prospect, not a coalition',
 'epa-bf': 'FY2026 selections published Jan 27 2026: about $12M to 25 communities (up to $500k per grant over up to five years); an FY2027 round appears underway (NOFO not read)',
 'nwcg': 'PMS 310-1 updated Jan 23 2026 (position names, CIM/IPTM requirements); NWCG is not a party to the Jan 2027 USWFS-USFS qualification alignment',
 'fire-quals': 'USWFS and USFS aligned federal qualification standards effective Jan 2027 (2026 IQCS Transition Plan, Jan 28 2026); existing qualifications carry over; NWCG not a party',
 'opm-class': 'PROPOSED: CHCO memo of Apr 24 2026 issued a Phase One list of 115 series proposed for realignment (e.g. 0410/0437/0480/0487 to 0401; 0455 to 0404); agency feedback due May 11 2026; no final-decision memo as of Oct 23 2026. Never describe series as realigned',
 'FH-E01': 'Apr 13 2026: FWCI general and technical competencies and competency frameworks issued with the 2210 standards; OPM targets 300+ series by end FY2026 and 600+ by end FY2027',
 'FH-E03': 'Competency-based classification and qualification standards for 2210 issued Apr 13 2026 under FWCI',
 'ctc': 'OPM Jul 2026 plan: Natural Resources Management is Tier 2 (with Transportation and Physical Sciences), addressed after Tier 1 matures, with no Tier 2 date; FY2028 is the governmentwide full-implementation target',
 'merit': 'Merit Hiring Plan May 29 2025: from Sep 30 2025 self-assessment questionnaires only for minimum qualifications, not rating and ranking (exceptions); FY2025 91.23% of DE announcements relied solely on self-report; FY2026 Q2 34.3% used technical or off-the-shelf assessments',
 'FH-E26': 'EO 14356 signed Oct 15 2025: Strategic Hiring Committees approve creating or filling each vacancy; annual staffing plans with quarterly updates from FY2026 Q2',
 'fwd': 'Federal Workforce Data (data.opm.gov) launched Jan 2026, replacing FedScope; monthly updates',
 'uswfs': 'Established by SO 3448 (Jan 12 2026) at DOI, unifying the fire programmes of BIA, BLM, NPS and FWS with the Office of Wildland Fire and Office of Aviation Services; 5,780 federal wildland fire personnel; supports ~900 Tribal wildland fire personnel',
 'AS-E011': 'Reorganization announced Mar 31-Apr 1 2026: HQ to Salt Lake City; all nine regional offices close (15 state directors); 57 of 77 research facilities close; relocations summer 2026 into 2027. No non-fire seasonal hiring in 2025; 2,000 seasonals committed for 2026',
 'americorps': '~$400M in grants terminated Apr 2025; cuts enjoined in 24 plaintiff states + DC (Jun 5 2025); Sep 11 2026 settlement covers FY2026 only; litigation stayed through Feb 1 2027',
 'CP-ECO-05': 'OPM memo Aug 27 2026: AI-assisted drafting of PDs and job-opportunity artifacts generally not high-impact when the responsible official independently reviews, revises and adopts the draft; rating, ranking and scoring presumed high-impact',
 'FH-E27': 'Final rule Feb 6 2026 (effective Mar 9 2026); EO 14410 (Jun 3 2026) placed ~8,000 employees in ~4,800 positions into Schedule Policy/Career',
 'pps': 'Federal civilian workforce 2,313,216 (Sep 2024) to 2,035,344 (Jan 2026), net about -278k (12%); PPS counts 386,826 separations Jan 2025-Jan 2026; the ~317k 2025 departures figure is OPM\'s own tally, not PPS',
 'FS-ECO-08': 'One job board: Conservation Job Board postings -29.4% YoY (Mar-Sep 2025); paid internships -43.8%; AmeriCorps positions -42%',
 'ceq-standard': 'Data standard v1.2 (Aug 18 2025); Permitting Technology Action Plan May 30 2025; CEQ-led Permitting Innovation Center with GSA TTS',
 'pnnl': 'PermitAI reusable modules (SearchNEPA, CommentNEPA, WriteNEPA, EngageNEPA) and NEPATEC 3.0; the "1-5 hours saved per EIS subsection" figure is not confirmed and must not be published',
 'omb-ai': 'M-25-21 and M-25-22 issued Apr 3 2025 (replacing M-24-10 and M-24-18); M-26-04 Unbiased AI Principles dated Dec 11 2025 (not Jan 2026)',
 'CP-ECO-06': 'M-26-05 dated Jan 23 2026; rescinds M-22-18 and M-23-16; CISA attestation form optional; agencies may require an SBOM on request',
 'CP-ECO-01': 'Consolidated Rules for 2026 replace "authorization" with "certification" (Classes A-D); optional early adoption Jul 4 2026; mandatory from Jan 1 2027',
 'CP-ECO-08': 'DOJ interim final rule Apr 20 2026: compliance by Apr 26 2027 (population 50,000+) and Apr 26 2028 (smaller entities and special districts); technical standard remains WCAG 2.1 AA',
 'CP-ECO-10': 'WCAG 2.2 approved as ISO/IEC 40500:2025 (Oct 21 2025); EMST release gate is WCAG 2.2 AA',
 'TN-E06': 'CRS R48093 (rev. Sep 23 2026): presidential consultation directives incl. EO 13175 appear to remain in effect; EO 14112 revoked by EO 14236 (Mar 2025); status of Joint Secretarial Order 3403 unconfirmed; publish neither as settled',
 'TN-E07': 'ACHP voted Jul 24 2026 to advance an NPRM rewriting 36 CFR 800; at OIRA review; not published as of Oct 9 2026',
 'ca-sb253': 'CARB SB 253/261 regulation approved by OAL Oct 12 2026; SB 253 first reports (Scope 1 and 2) due Nov 10 2026, Scope 3 from 2027; SB 261 enforcement enjoined pending Ninth Circuit appeal',
 'eu-omnibus': 'Omnibus I Directive published Feb 26 2026, in force Mar 18 2026; CSRD scope narrowed to undertakings with >1,000 employees and >EUR 450m turnover',
 'faa108': 'NPRM Aug 7 2025; final rule at OIRA since Jul 10 2026 and not published as of Oct 21 2026: a signpost, not a fact',
 'FC-E07': 'ASDA: from Dec 22 2025 covered foreign-adversary UAS may not be procured or operated with federal funds; FCC added all foreign-produced UAS and critical components to the Covered List Dec 22 2025 (previously authorized models still usable)',
 'aei': 'Six numbered reports: Feb 10 2025; Mar 27 2025; Sep 15 2025; Jan 15 2026; Mar 24 2026; Jun 26 2026; datasets on Hugging Face (CC BY). API automation-pattern shares describe API usage, never job automation',
 'ECO-LM-06': 'Tomlinson et al., arXiv:2507.07935 (v6 Dec 22 2025; 200k Bing Copilot conversations); NeurIPS 2026 poster',
 'sdel': 'Canaries update Aug 12 2026: employment of 22-25-year-olds in highly AI-exposed occupations ~19% below trend as of Jun 2026; no economy-wide displacement',
 'ECO-LM-11': 'ILO Working Paper 140 (May 20 2025): about 1 in 4 workers globally in occupations with some GenAI exposure; 3.3% in the highest gradient',
 'wef-foj': 'Future of Jobs Report 2025 (Jan 7 2025); no 2026 edition found; "Four Futures for Jobs in the New Economy: AI and Talent in 2030" is a separate white paper (~Jan 2026)',
 'linkedin': 'Latest release found: LinkedIn Global Green Stocktake 2025 (Dec 2025); no full Global Green Skills Report 2025 or 2026 edition found',
 'bls-ep': 'Employment Projections 2025-35 released Aug 27 2026, with new AI exposure categories; the 2024-34 projections are superseded',
 'esco': 'ESCO v1.2.1 (Dec 2025) is current; no v1.3 listed; v1.2.1 revised green skill-occupation relations; language count to be rechecked before publishing',
 'case': 'CASE 1.1 final release Feb 28 2024; publicly available from Apr 2 2025',
 'osmt': 'OSMT and Rich Skill Descriptors transitioned from WGU to Credential Engine (Feb 3 2025); OSMT remains open source',
 'ieee': 'IEEE Std 1484.20.3-2022 active (published Jul 27 2023); amendment P1484.20.3a PAR approved Jun 19 2025',
 'ob3': 'Open Badges 3.0 Final Release current (document v1.4.5, Jun 29 2026); W3C Verifiable Credentials Data Model 2.0 Recommendation May 15 2025',
 'sssom': 'SSSOM 1.0.0 latest stable (Aug 9 2024); 1.1.0 only as alpha pre-releases (a5 May 22 2026)',
 'DC-ECO-03': 'AI RMF 1.0 (Jan 26 2023) still the released version, under revision with no date; Generative AI Profile NIST-AI-600-1 (Jul 26 2024)',
 'opm-ai-cm': 'OPM Skills-Based Hiring Guidance and Competency Model for AI Work (Apr 29 2024): 43 general and 14 technical competencies',
 'ai-inventory': '2025 Federal Agency AI Use Case Inventory on GitHub (ombegov): 3,611 individually reported use cases, 445 high-impact; summary as of Apr 13 2026',
 'DC-ECO-14': 'Prithvi-EO-2.0 (IBM and NASA) models released Dec 4 2024 (300M and 600M parameters)',
 'DC-ECO-16': 'Clay Foundation Model: open source, Apache-2.0 code and weights; no versioned releases listed',
 'gee-alphaearth': 'AlphaEarth Foundations (Google DeepMind) announced Jul 30 2025; annual 10 m Satellite Embedding dataset in Earth Engine',
 'ECO-LM-18': 'AI Index Report 2026 published Apr 2026',
 'SC-E18': 'Five-ECQ framework effective Oct 1 2025; Political Savvy, Partnering and Influencing/Negotiating no longer appear; no statecraft content cites the ECQs as its warrant',
 'IO-E01': '29 CFR 1607 still codified, but a DOJ OLC opinion (Jun 9 2026) found its disparate-impact framework unconstitutional as applied; OPM interim final rule (Jul 31 2026) removed UGESP references incl. 5 CFR 300.103; OFCCP rescission of 41 CFR 60-3 effective Oct 26 2026. EMST never frames validation as "UGESP compliance"',
 'IO-E21': 'Colorado SB 24-205 never took effect as written: enforcement stayed Apr 27 2026; SB 26-189 (signed May 14 2026, effective Jan 1 2027; notice and disclosure, not impact assessments) repealed and replaced it; do not cite SB 24-205 as a live obligation',
 'TN-E03': 'Link removed: the former USIDSN domain now serves unrelated content and must never be linked; cite USIDSN only via a verified Native Nations Institute page (not yet identified)',
 'AS-E124': 'AI for Climate and Nature Grand Challenge Phase II awards Oct 23 2025 (15 teams, $30M); no next round announced; not a workforce-skills programme',
 'AS-E125': 'Google.org AI Collaborative: Wildfires launched Mar 17 2025 ($27M+, 15+ organizations); still granting Jul 2026; not a workforce-skills programme',
 'AS-E120': 'Wildfire Resilience Initiative, $110M over six years (Feb 2023); not a workforce-skills programme',
 'AS-E122': 'Environment Program active; new director named Feb 2026; not a workforce-skills programme',
 'AS-E123': 'Environment programme active (climate-smart forests, Indigenous-led conservation); not a workforce-skills programme',
 'AS-E126': 'AI in Science postdoctoral fellowships advertised for 2026 (indirect evidence); not a workforce-skills programme',
 'AS-E065': 'IEMA rebranded as ISEP by Jul 2025',
 'AS-E118': 'Incubation of EMST through Dec 2027 not confirmed (questions_for_project_lead.md Q3); no commitment recorded',
}
URL = {  # corrected URLs from verification findings
 'isep': 'https://www.isepglobal.org', 'DB-ECO-031': 'https://www.isepglobal.org', 'EC-CM-14': 'https://greentwopointzero.org/',
 'ieee': 'https://sagroups.ieee.org/1484-20-3', 'wef-foj': 'https://www.weforum.org/publications/the-future-of-jobs-report-2025/',
 'linkedin': 'https://economicgraph.linkedin.com', 'TN-E03': '', 'AS-E096': '',
 'fire-quals': 'https://iqcsweb.nwcg.gov/sites/default/files/documents/2026_Transition_Plan.pdf',
 'abc-wpi': '', 'issp': 'https://www.bdcnetwork.com/codes-and-standards/news/55162937/new-gbci-certification-recognizes-expertise-in-sustainability',
}

MODES = ['ingest', 'crosswalk', 'benchmark', 'partner', 'funder', 'adopter', 'validator', 'distribution', 'watch']
TRIBAL_RE = re.compile(r'Tribal|Tribe|Indigenous|Native American|Native Hawaiian|Alaska Native|Inter-?Tribal|Intertribal|'
                       r'AIHEC|\bITEP\b|NATHPO|THPO|\bBIA\b|OCAP|CARE Principles|Local Contexts|Mukurtu|First Nations|'
                       r'\bNARF\b|\bNCAI\b|Bears Ears|IFMAT', re.I)
NOT_TRIBAL = {'AS-E012'}  # DOI bureaus: federal department; 'BIA' appears only in a list of bureaus
RANK = {'verified': 1, 'corrected': 2, 'superseded': 3, 'source-read': 4, 'unreachable': 5, 'unverified': 6, 'not-found': 7}
FAST_TYPES = {'policy', 'index', 'dataset', 'platform', 'tool', 'fund'}
JOINS = [  # (join key, regex over name + what + integration detail)
 ('onet-task-id', r'O\*NET[^|]{0,80}(task|match)|task[- ]level[^.;|]{0,40}O\*NET|O\*NET task|\bDWA|task IDs?|task penetration|task-level (usage|exposure|shares?)'),
 ('onet-soc', r'O\*NET-SOC|O\*NET SOC|occupation code|O\*NET occupation'),
 ('soc', r'\bSOC\b'), ('esco-uri', r'ESCO'), ('isco-08', r'ISCO'), ('opm-series', r'OPM series|\bseries\b[^.;]{0,30}(0[0-9]{3}|OPM)|GS series|0401|0404|0028'),
 ('state-class', r'state class|class spec'), ('cip', r'\bCIP\b'), ('ctid', r'CTDL|CTID|Credential Registry'),
 ('naics', r'NAICS'), ('emst-id', r'EMST ID'), ('ceq-data-standard', r'CEQ[^.;]{0,40}standard|NEPA[^.;]{0,20}data standard'),
]

def http(u):
    u = (u or '').strip()
    if not u:
        return ''
    first = re.split(r'\s+\|\s+|\s+;\s+|\s+', u)[0]
    return first if first.startswith('http') else ''

def scrub(s):
    s = s or ''
    s = re.sub(r'usindigenousdata(\[\.\]|\.)org', '[former USIDSN domain removed]', s, flags=re.I)
    return s

def member_status(eid):
    r = byid[eid]
    if eid in results:
        res = results[eid]
        return res['verification_status'], RUN_DATE, http(res.get('checked_url')), res.get('source_date', ''), \
               f"{eid} ({res.get('theme','')}): {res['finding']}" + (f" [fix: {res['corrected_fields']}]" if res.get('corrected_fields') else '')
    if eid in queued:
        return 'unverified', '', '', '', ''
    if r['evidence_label'] == 'E':
        acc = ''
        for sid in re.split(r'[|;, ]+', r.get('source_ids') or ''):
            if sid in sources:
                a = sources[sid].get('accessed', '')
                if re.match(r'\d{4}-\d{2}-\d{2}', a):
                    acc = a[:10]
                    break
        return ('source-read', acc, '', '', '') if acc else ('unverified', '', '', '', '')
    return 'unverified', '', '', '', ''

def fact_status(fid):
    f = facts[fid]
    st = f['verification_status']
    st = {'refuted': 'corrected'}.get(st, st)
    return st, RUN_DATE, http(f.get('source_url')), f.get('source_date', ''), f"{fid}: {f['correct_statement'][:400]}"

cluster_of = {}
for c, ids in CLUSTERS.items():
    for i in ids:
        assert i in byid, f'unknown id {i} in cluster {c}'
        assert i not in cluster_of, f'{i} in two clusters'
        cluster_of[i] = c
groups = OrderedDict()
for r in eco:
    key = cluster_of.get(r['entity_id'], r['entity_id'])
    groups.setdefault(key, []).append(r['entity_id'])

out = []
for key, ids in groups.items():
    rows = [byid[i] for i in ids]
    sts = [(i,) + member_status(i) for i in ids]
    checks = list(sts)
    for fid in FACTS.get(key, []) + sum((FACTS.get(i, []) for i in ids if i != key), []):
        checks.append((fid,) + fact_status(fid))
    for i in ids:
        for sid in SOURCE_CHECKS.get(i, []):
            res = results[sid]
            checks.append((sid, res['verification_status'], RUN_DATE, http(res['checked_url']), res.get('source_date', ''),
                           f"{sid} ({res.get('theme','')}): {res['finding'][:400]}"))
    best = min(checks, key=lambda c: RANK.get(c[1], 9))
    status = best[1]
    if status == 'refuted':
        status = 'corrected'
    corrected = [c[0] for c in checks if c[1] in ('corrected', 'superseded', 'refuted')]
    # representative row: best member status, then has URL, then E label, then longest integration detail
    def rk(i):
        m = next(s for s in sts if s[0] == i)
        r = byid[i]
        return (RANK.get(m[1], 9), 0 if http(r['url']) else 1, 0 if r['evidence_label'] == 'E' else 1, -len(r['integration_detail'] or ''))
    rep = byid[min(ids, key=rk)]
    roles = sorted({ROLE_CODE.get(r['role_folder'], r['role_folder']) for r in rows})
    name = NAME.get(key, rep['name'])
    types = sorted({r['entity_type'] for r in rows})
    modes = []
    for r in rows:
        for m in re.split(r'[|;, ]+', r['how_emst_connects'] or ''):
            m = m.strip().lower()
            if m in MODES and m not in modes:
                modes.append(m)
    modes = sorted(modes, key=MODES.index)
    blob = ' '.join([name] + [r['what_it_illuminates'] or '' for r in rows] + [r['integration_detail'] or '' for r in rows])
    tribal = (any(r['role_folder'] == 'tribal-sovereignty' for r in rows) or bool(TRIBAL_RE.search(name))
              or bool(TRIBAL_RE.search(' '.join(r['name'] for r in rows)))) and key not in NOT_TRIBAL
    joins = [k for k, rx in JOINS if re.search(rx, blob)]
    # URL: corrected override, else best verified check URL that is the entity's own site, else representative URL
    url = URL.get(key, URL.get(rep['entity_id'], None))
    if url is None:
        url = http(rep['url']) or next((http(byid[i]['url']) for i in ids if http(byid[i]['url'])), '')
        if not url and rep['url'] and rep['url'].startswith(('local:', '/home')):
            url = rep['url']
    vurl = best[3] if best[3] else ''
    # integration detail: keep each role's distinct text
    details, seen = [], set()
    for r in rows:
        d = (r['integration_detail'] or '').strip()
        if d and d not in seen:
            seen.add(d)
            details.append(f"[{ROLE_CODE.get(r['role_folder'], '?')}] {d}")
    latest = STATUS.get(key, STATUS.get(rep['entity_id'], rep['latest_release_or_status']))
    note_parts = [c[5] for c in checks if c[5]]
    owner = 'TN' if tribal else ROLE_CODE.get(rep['role_folder'], 'AS')
    t0 = rep['entity_type']
    review = REVIEW_FAST if (t0 in FAST_TYPES or status in ('unverified', 'unreachable', 'not-found')) else REVIEW_SLOW
    if tribal:
        release = 'held-pending-tribal-review'
        modes_out = 'watch'
        connect_note = 'Phase 2 connection modes (' + ('|'.join(modes) or 'none') + ') suspended under the Tribal gate; no outreach'
    else:
        release = 'usable-with-citation' if status in ('verified', 'corrected', 'superseded') else \
                  ('verify-before-external-use' if status in ('source-read', 'unreachable', 'unverified') else 'do-not-cite-as-active')
        modes_out = '|'.join(modes) or 'watch'
        connect_note = ''
    out.append(OrderedDict([
        ('atlas_id', ''),
        ('name', scrub(name)),
        ('entity_type', t0),
        ('entity_type_alternates', '|'.join(t for t in types if t != t0)),
        ('owner_or_host', scrub(rep['owner_or_host'])),
        ('sector_focus', scrub(rep['sector_focus'])),
        ('what_it_illuminates', scrub(rep['what_it_illuminates'])),
        ('latest_release_or_status', scrub(latest)),
        ('how_emst_connects', modes_out),
        ('join_keys', '|'.join(joins) or 'none'),
        ('integration_detail', scrub(' || '.join(details))),
        ('url', scrub(url)),
        ('verification_status', status),
        ('verified_on', best[2] or ''),
        ('verification_source_date', scrub(best[4] or '')),
        ('verification_url', scrub(vurl)),
        ('verification_refs', '|'.join(c[0] for c in checks if c[0] in results or c[0] in facts)),
        ('corrections_applied', '|'.join(corrected)),
        ('verification_note', scrub(' || '.join(note_parts))[:1500]),
        ('evidence_label', 'E' if status in ('verified', 'corrected', 'superseded', 'source-read') else
                           ('S' if all(r['evidence_label'] == 'S' for r in rows) else 'J')),
        ('source_ids', '|'.join(OrderedDict.fromkeys(s for r in rows for s in re.split(r'[|;, ]+', r['source_ids'] or '') if s))),
        ('contributing_roles', '|'.join(roles)),
        ('contributing_entity_ids', '|'.join(ids)),
        ('n_contributing_rows', str(len(ids))),
        ('tribal_related', 'true' if tribal else 'false'),
        ('release_status', release),
        ('connection_note', connect_note),
        ('commitment_status', 'none recorded (commitment register empty on ' + RUN_DATE + ')'),
        ('atlas_owner_role', owner),
        ('review_by', review),
    ]))

# stable order: by entity type then name; assign local atlas IDs (not EMST IDs)
out.sort(key=lambda r: (r['entity_type'], r['name'].lower()))
for n, r in enumerate(out, 1):
    r['atlas_id'] = f'ATL-{n:04d}'
with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    w.writeheader()
    w.writerows(out)

from collections import Counter
print('input rows', len(eco), '-> atlas entities', len(out), '; merged clusters', sum(1 for g in groups.values() if len(g) > 1))
print('verification_status', dict(Counter(r['verification_status'] for r in out)))
print('release_status', dict(Counter(r['release_status'] for r in out)))
print('tribal_related', Counter(r['tribal_related'] for r in out)['true'])
print('join onet-task-id', sum('onet-task-id' in r['join_keys'] for r in out))
