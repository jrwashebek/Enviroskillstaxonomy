import csv
OUT='/home/claude/emst/docs/research/federal-human-capital/opm_series_register.csv'
NV='not verified this session (J)'
G0='0000 Miscellaneous'; G1='0100 Social Science, Psychology & Welfare'; G3='0300 General Administrative, Clerical & Office Services'
G4='0400 Natural Resources Management & Biological Sciences'; G6='0600 Medical, Hospital, Dental & Public Health'
G8='0800 Engineering & Architecture'; G11='1100 Business & Industry'; G13='1300 Physical Sciences'; G15='1500 Mathematical Sciences'; G21='2100 Transportation'; G22='2200 Information Technology'
PROF4='Professional & Scientific Positions group std + series IOR'
ADM='Administrative & Management Positions group std (specialized experience)'
TECH='Technical & Medical Support Positions group std (education may substitute)'
ENG='Professional Engineering Positions basic requirements (ABET degree or alternatives)'
JFS4='0400 professional job family standard (v1 claims 2005; '+NV+')'
JFS13='1300 professional physical sciences job family standard ('+NV+')'
JFS8='0800 professional engineering job family standard ('+NV+')'
S='FH-041|FH-042'
rows=[
# series,title,group,class_std_date,qual_std,positive_ed,agencies,headcount,families,notes,sources
("0018","Safety and Occupational Health Management",G0,NV,ADM+' / series IOR (verify)','verify','USFS|NPS|BLM|USACE|EPA|DOD','medium-large (J)','none (v1 4.4.x unaffiliated)','Field safety programs, job hazard analysis; v1 SA 4.4 competencies are zero-core in families yet universal in federal field series.',S),
("0020","Community Planning",G0,NV,PROF4,'Y (degree or combination; verify)','USACE|FEMA|HUD|DOD|NPS','small-medium (J)','F9','Land-use and comprehensive planning; federal land-management planners are more often 0401/0028/0023 than 0020.',S),
("0021","Community Planning Technician",G0,NV,TECH,'N','HUD|DOD','very small (E: on OPM consolidation list)','F9','OPM Phase One proposes realignment to 0303.','FH-014'),
("0023","Outdoor Recreation Planning",G0,NV,PROF4,'Y? (verify)','USFS|NPS|BLM|USACE|BOR','very small (E: on OPM consolidation list)','F9|F11','OPM Phase One proposes realignment (Appendix A target read as 0186 via summarizer; verify - 0188 Recreation Specialist would be the logical home). Recreation planning work does not disappear; EMST must keep the function and re-point the series code.','FH-014'),
("0025","Park Ranger",G0,NV,'Series IOR (experience or education)','N','NPS (dominant)|USACE|BOR','medium; -34.1% Sep 2024-Jan 2026 (E)','F11','Interpretation, visitor protection, resource education; commissioned LE rangers have 6(c) coverage. Largest occupation-level decline among environmental series in PPS analysis.','FH-008|FH-041'),
("0028","Environmental Protection Specialist",G0,NV,ADM,'N','EPA (dominant)|USFS|BLM|USACE|DOD|DOE|FHWA|NOAA|BOEM','large (J)','F8|F13','Compliance, permitting, enforcement, NEPA coordination. No positive education requirement makes it the most accessible landing series for reskilled scientists and the most common home for NEPA coordinators outside 0401.','FH-041|FH-042'),
("0029","Environmental Protection Assistant",G0,NV,TECH,'N','EPA|DOD','very small (E: on OPM consolidation list)','F8','OPM Phase One proposes realignment to 0303 (generic clerical/assistance). Paraprofessional environmental entry path loses its named series.','FH-014'),
("0081","Fire Protection and Prevention",G0,NV,'Series IOR','N','DOD|VA|NPS (structural)','medium (J)','F12','Structural/installation fire; distinct from wildland 0456/0462. Include only for disambiguation.',S),
("0089","Emergency Management",G0,NV,ADM,'N','FEMA (dominant)|USACE|USFS','medium (J)','F12','Incident/disaster coordination; adjacency for fire and flood workforce mobility.',S),
("0090","Guide",G0,NV,TECH,'N','NPS|USACE','very small (E: on OPM consolidation list)','F11','OPM Phase One proposes realignment to 1001 (General Arts and Information).','FH-014'),
("0101","Social Science",G1,NV,PROF4,'Y (degree or 24 sem hrs; verify)','USFS|NPS|BLM|EPA|NOAA|USACE','medium (J)','F11|F13','Social impact analysis, collaboration research, human dimensions; absorbing 0184 and 0190 under OPM Phase One.','FH-014|FH-041'),
("0110","Economist",G1,NV,PROF4,'Y (economics coursework; verify)','EPA|USDA ERS|USFS|BOEM|USACE|NOAA','medium (J)','F15|F8','Regulatory impact analysis, nonmarket valuation, benefit-cost; v1 SA 6.3 maps here.',S),
("0132","Intelligence",G1,NV,ADM,'N','DOD (dominant); fire intelligence roles at NIFC/GACCs','very large overall; tiny environmental share (J)','F12|F7','Included because v1 fire-intelligence research shows Predictive Services/intelligence work spread across 0132/1340/1560/2210/0462/0401 - a series-ambiguity signal, not an environmental home.','FH-040'),
("0150","Geography",G1,NV,PROF4,'Y (verify)','USGS|USFS|NGA|Census|NOAA','small (J)','F7|F9','Historic home for GIS professionals alongside 1370 and 0401; corrects v1 claim that only 1370 recognizes GIS.','FH-036|FH-041'),
("0170","History",G1,NV,PROF4,'Y (verify)','NPS|USFS|USACE|BOR','small (J)','none','Cultural resources (historic preservation, NHPA Section 106); v1 has no cultural-resources family.',S),
("0190","General Anthropology",G1,NV,PROF4,'Y (verify)','NPS|BIA|USFS','very small (E: on OPM consolidation list)','none','OPM Phase One proposes realignment to 0101.','FH-014'),
("0193","Archeology",G1,NV,PROF4,'Y (degree incl. archeology; verify)','USFS|BLM|NPS|USACE|BOR|FHWA','small (J)','none','Section 106 compliance is a statutory gate on most land-management projects; v1 5.3.3 only partially covers it. Candidate competency FH-C08.',S),
("0301","Miscellaneous Administration and Program",G3,NV,ADM,'N','all','very large (J)','F8','Common default for environmental program/partnership coordinators and grants roles when no technical series fits; classification drift risk.',S),
("0340","Program Management",G3,NV,ADM,'N','all (senior program managers)','small (J)','F8','Retained from v1 analysis as adjacency for senior program leadership; SP/C transfers concentrate in GS-15+ program/policy managers.','FH-005|FH-028|FH-036'),
("0343","Management and Program Analysis",G3,NV,ADM,'N','all','very large (J)','F8','Policy/program analysts; v1 claim that environmental policy professionals sit here is partly true but incomplete (also 0028, 0101, 0110, 0401, attorneys 0905).','FH-036'),
("0401","General Natural Resources Management and Biological Sciences",G4,JFS4,PROF4,'Y (bio/ag/natural resources degree or combination; verify)','USFS|BLM|FWS|NPS|BOR|BIA|NRCS|USACE|EPA|NOAA|DOD','large (J)','F2|F3|F5|F8|F12','Catch-all and interdisciplinary home (natural resource specialist, NEPA planner, botanist, invasive species). Absorbing 0410, 0437, 0480, 0487 under OPM Phase One - becomes even broader, which raises the value of competency profiles inside the series.','FH-014|FH-041|FH-042'),
("0403","Microbiology",G4,JFS4,PROF4,'Y (verify)','EPA|USGS|ARS|FDA|CDC','medium (J)','F13|F5','Lab and environmental microbiology (water quality, eDNA labs).',S),
("0404","Biological Science Technician",G4,NV,TECH,'N','USFS|FWS|NPS|BLM|USGS|ARS|NOAA|APHIS','large (J)','F2|F3|F5','Principal non-degree field entry path for biological work; absorbing 0455 Range Technician under OPM Phase One.','FH-014|FH-041'),
("0408","Ecology",G4,JFS4,PROF4,'Y (verify)','USFS|BLM|FWS|NPS|USGS|USACE|EPA','small-medium (J)','F5|F3','Often classified interdisciplinary with 0401/0486/0430.',S),
("0410","Zoology",G4,JFS4,PROF4,'Y (verify)','USGS|Smithsonian','very small (E: on OPM consolidation list)','F2|F5','OPM Phase One proposes realignment to 0401.','FH-014'),
("0413","Physiology",G4,JFS4,PROF4,'Y (verify)','ARS|NOAA|VA','small (J)','F5','Adjacent; limited environmental share.',S),
("0414","Entomology",G4,JFS4,PROF4,'Y (verify)','USFS (forest health)|APHIS|ARS','small (J)','F1|F10','Forest health protection entomologists; v1 1.3.4 maps.',S),
("0430","Botany",G4,JFS4,PROF4,'Y (verify)','BLM|USFS|FWS|NPS','small (J)','F5|F3','Rare plants, seeds of success, native seed; often 0401/0430 interdisciplinary.',S),
("0434","Plant Pathology",G4,JFS4,PROF4,'Y (verify)','USFS|APHIS|ARS','small (J)','F1|F10','Forest pathology.',S),
("0435","Plant Physiology",G4,JFS4,PROF4,'Y (verify)','ARS','very small (J)','F10','Adjacent.',S),
("0437","Horticulture",G4,JFS4,PROF4,'Y (verify)','ARS|NPS|USDA','very small (E: on OPM consolidation list)','F10','OPM Phase One proposes realignment to 0401.','FH-014'),
("0440","Genetics",G4,JFS4,PROF4,'Y (verify)','ARS|USFS R&D|FWS (conservation genetics labs)','small (J)','F5|F2','v1 SA 1.6 maps.',S),
("0454","Rangeland Management",G4,JFS4,PROF4,'Y (range/plant/animal/soil coursework; verify)','BLM (dominant)|USFS|NRCS|BIA','medium-small (J)','F3|F10','Grazing permit administration, allotment monitoring, NEPA for permit renewals. v1 has no grazing/allotment competency (candidate FH-C04).',S),
("0455","Range Technician",G4,NV,TECH,'N','BLM|USFS','very small (E: on OPM consolidation list)','F3|F10','OPM Phase One proposes realignment to 0404.','FH-014'),
("0456","Wildland Fire Management",G4,'2022 series establishment (J; not re-verified)','Series IOR (wildland fire experience; NWCG/IFPM qualifications as applicable; verify)','N','USFS (dominant)|BLM|NPS|FWS|BIA|DOI wildland fire consolidation','large and growing (E: wildland fire mgmt up Sep 2024-Jan 2026; USFS 10,496 WFF on board May 2026)','F12','Primary home for wildland firefighters and fire program managers. DOI consolidating bureau fire programs in phases (E: FH-035); formal U.S. Wildland Fire Service details not verified this session. Pay reform status not verified this session.','FH-008|FH-035|FH-039'),
("0457","Soil Conservation",G4,JFS4,PROF4,'Y (verify)','NRCS (dominant)|BIA','large within NRCS (J)','F10|F4','Conservation planning with private landowners, Farm Bill program delivery (EQIP/CSP). v1 lacks a conservation-planning competency (candidate FH-C03).',S),
("0458","Soil Conservation Technician",G4,NV,TECH,'N','NRCS','medium (J)','F10','Field layout, practice checkout; technician entry path at NRCS.',S),
("0459","Irrigation System Operation",G4,NV,TECH,'N','BOR|BIA','very small (E: on OPM consolidation list)','F4|F10','OPM Phase One proposes realignment (Appendix A target read as 4701; verify).','FH-014'),
("0460","Forestry",G4,JFS4,PROF4,'Y (forestry degree or 24 sem hrs forestry; verify)','USFS (dominant)|BLM|BIA|NPS|DOD|FWS','medium (J)','F1','Silviculture, timber sale prep/administration, stewardship contracting, forest health, NEPA. Positive education requirement is the main barrier to reskilling into 0460.','FH-037|FH-041|FH-042'),
("0462","Forestry Technician",G4,NV,TECH,'N','USFS (dominant)|BLM|BIA|NPS','very large incl. seasonal (J)','F1|F12','Timber cruising/marking, recreation, trails, fuels, and (historically) most firefighters before 0456 conversion. The entry pipeline for both forestry and fire.','FH-041'),
("0470","Soil Science",G4,JFS4,PROF4,'Y (soils coursework; verify)','NRCS (soil survey)|USFS|BLM','small-medium (J)','F10|F4','Soil survey, ecological site descriptions; NRCS digital soil mapping is an early DC adopter.',S),
("0471","Agronomy",G4,JFS4,PROF4,'Y (verify)','NRCS|ARS','small (J)','F10','Nutrient management, conservation agronomy.',S),
("0480","General Fish and Wildlife Administration",G4,JFS4,PROF4,'Y? (verify)','FWS','very small (E: on OPM consolidation list)','F2','OPM Phase One proposes realignment to 0401.','FH-014'),
("0482","Fish Biology",G4,JFS4,PROF4,'Y (aquatic coursework; verify)','FWS|NOAA Fisheries|USACE|BOR|USGS|USFS','medium (J)','F2|F4','Fishery management, ESA Section 7, hatcheries, FERC/hydropower. Hatchery operations not in v1 (candidate FH-C10).',S),
("0485","Wildlife Refuge Management",G4,JFS4,PROF4,'Y (verify)','FWS','small (J)','F2|F5','Refuge managers; compatibility determinations; program management.',S),
("0486","Wildlife Biology",G4,JFS4,PROF4,'Y (wildlife coursework; verify)','FWS|USFS|BLM|NPS|USGS|APHIS-WS|DOD','medium (J)','F2|F5','ESA consultation, surveys, habitat; v1 6.1.x is too generic for Section 7 consultation (candidate FH-C01).',S),
("0487","Animal Science",G4,JFS4,PROF4,'Y (verify)','ARS|APHIS','very small (E: on OPM consolidation list)','F10','OPM Phase One proposes realignment to 0401.','FH-014'),
("0499","Biological Science Student Trainee",G4,NV,'Pathways (enrollment-based)','enrollment','all 0400 employers','declining (E: student trainee occupations decreased significantly)','F2|F5','Pathways intern path into 0400 professional series; contraction is an entry-path-at-risk signal.','FH-008'),
("0688","Sanitarian",'0600 Medical, Hospital, Dental & Public Health',NV,PROF4,'verify','IHS|DOD|NPS (public health)','very small (E: on OPM consolidation list)','F13','OPM Phase One proposes realignment to 0601.','FH-014'),
("0690","Industrial Hygiene",'0600 Medical, Hospital, Dental & Public Health',NV,PROF4,'Y (verify)','DOD|DOE|OSHA|EPA','small-medium (J)','F13','Exposure assessment; v1 6.7.4 maps.',S),
("0698","Environmental Health Technician",'0600 Medical, Hospital, Dental & Public Health',NV,TECH,'N','IHS|DOD','very small (E: on OPM consolidation list)','F13','OPM Phase One proposes realignment to 0640.','FH-014'),
("0802","Engineering Technician",G8,NV,TECH,'N','USACE|BOR|USFS|NRCS','large (J)','F4','Field engineering support (roads, dams, conservation practices).',S),
("0810","Civil Engineering",G8,JFS8,ENG,'Y (with alternatives)','USACE (civil works dominant)|BOR|USFS|NPS|FHWA|NRCS','very large (J)','F4|F3','Water resources infrastructure, levees, dams, roads. OPM issued an AI competency model for 0810 in 2024 (E: title) - precedent for AI overlays on non-IT series.','FH-043|FH-041'),
("0819","Environmental Engineering",G8,JFS8,ENG,'Y (with alternatives)','EPA|USACE|DOD|DOE|NPS|IHS','medium-large (J)','F4|F13','Treatment, remediation, permitting, air/water engineering. v1 lacks remediation and treatment-process competencies (candidate FH-C12; DB lane).',S),
("0893","Chemical Engineering",G8,JFS8,ENG,'Y (with alternatives)','EPA|DOE|DOD','small (J)','F13','Included per assignment; environmental share is regulatory (air/chemicals) - low priority.',S),
("1170","Realty",G11,NV,ADM,'N','BLM|USFS|USACE|BOR|NPS|FWS|BIA','medium (J)','F9|F8','Land acquisition, rights-of-way, special use authorizations; absorbs Land Law Examining (0965) work context. Not in v1 task list but central to permitting (S3).','FH-014'),
("1301","General Physical Science",G13,JFS13,PROF4,'Y (verify)','EPA|USGS|NOAA|DOE|USACE|DOD','medium-large (J)','F6|F4','Interdisciplinary physical science; absorbing 1321, 1372, 1380, 1384 under OPM Phase One.','FH-014|FH-041'),
("1306","Health Physics",G13,JFS13,PROF4,'Y (verify)','DOE|NRC|EPA|DOD','small (J)','F13','Radiation protection.',S),
("1311","Physical Science Technician",G13,NV,TECH,'N','USGS|NOAA|EPA|USACE','medium (J)','F4|F6','Absorbing 1374 Geodetic Technician.','FH-014'),
("1315","Hydrology",G13,JFS13,PROF4,'Y (hydrology/physical science coursework; verify)','USGS (dominant)|USACE|NOAA NWS|NRCS|USFS|BLM|BOR|NPS','medium (J)','F4','Streamflow, modeling, BAER, water rights support; strong DC trajectory (sensors, models, ML).',S),
("1316","Hydrologic Technician",G13,NV,TECH,'N','USGS (dominant)|USACE','medium (J)','F4','Streamgaging field entry path; automation of data processing compresses technician tasks (v1 2.6.4).',S),
("1320","Chemistry",G13,JFS13,PROF4,'Y (verify)','EPA|USGS|NOAA|DOD|FDA','medium (J)','F13|F4','Environmental labs.',S),
("1340","Meteorology",G13,JFS13,PROF4,'Y (meteorology coursework; verify)','NOAA NWS (dominant)|USFS/BLM Predictive Services|DOD','medium (J)','F6|F12','IMETs and Predictive Services meteorologists bridge fire and weather (FH-040).','FH-040|FH-041'),
("1341","Meteorological Technician",G13,NV,TECH,'N','NOAA|DOD','small (J)','F6','Adjacency.',S),
("1350","Geology",G13,JFS13,PROF4,'Y (verify)','USGS|BLM|USFS|BOEM|USACE|NPS','small-medium (J)','F4','Minerals, groundwater, hazards.',S),
("1360","Oceanography",G13,JFS13,PROF4,'Y (verify)','NOAA|USGS|DOD','small (J)','F6|F4','Coastal and ocean observing.',S),
("1370","Cartography",G13,NV,PROF4,'Y? (verify)','NGA|USGS|USFS|NOAA','small (J)','F7','GIS/mapping; v1 claim that only 1370 recognizes GIS is incorrect (0150, 0401 GIS specialists, 1560).','FH-036|FH-041'),
("1372","Geodesy",G13,NV,PROF4,'Y (verify)','NOAA NGS|NGA','very small (E: on OPM consolidation list)','F7','OPM Phase One proposes realignment to 1301.','FH-014'),
("1373","Land Surveying",G13,NV,PROF4,'Y or licensure alternative (verify)','BLM (cadastral)|USFS|USACE|NPS|BIA','small (J)','F7|F9','Cadastral survey underpins boundary, realty and permitting work; not in v1.',S),
("1380","Forest Products Technology",G13,NV,PROF4,'Y (verify)','USFS Forest Products Lab','very small (E: on OPM consolidation list)','F1','OPM Phase One proposes realignment to 1301.','FH-014'),
("1560","Data Science",G15,'2021 series establishment (J; not re-verified)','Series IOR (degree in data science/statistics/CS/related or combination; verify)','Y (or combination; verify)','USGS|NOAA|EPA|USFS|USDA|DOI','small, growing (J)','F7','Corrects v1 claim that no environmental data science pathway exists. Fire intelligence and environmental modeling roles increasingly classifiable here (FH-040).','FH-036|FH-040|FH-041'),
("2151","Dispatching",G21,NV,TECH,'N','USFS|BLM|NPS|BIA (interagency dispatch centers)','medium (J); dispatch-center cuts 25-27% in CO/NV (E, low quality)','F12','Fire dispatch; highly automatable data-entry tasks but error-sensitive (FH-039).','FH-019|FH-039'),
("2210","Information Technology Management",G22,'2026-04-13 competency-based position classification standard issued (E: title)','Competency-based qualification standard issued 2026-04-13 (E: title)','N','all (incl. environmental data systems)','very large (J)','F7','Pilot for OPM competency-based classification + qualification + FWCI general/technical competency framework; the template OPM will likely extend to other series. Read FH-044 content in Phase 3.','FH-011|FH-044|FH-001'),
]
with open(OUT,'w',newline='',encoding='utf-8') as f:
    w=csv.writer(f)
    w.writerow(['series','title','group','classification_standard_date','qualification_standard','positive_education_requirement','env_agencies_major_employers','headcount_signal','emst_v1_families','notes','source_ids'])
    for r in rows:
        assert len(r)==11, r[0]
        w.writerow(r)
print(len(rows))
