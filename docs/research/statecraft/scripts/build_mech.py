import csv
OUT="/home/claude/emst/docs/research/statecraft/driver_mechanisms.csv"
H=["mechanism_id","mechanism","definition","replaces_v1_flag","example_instrument_ids","direction_observed_2025_26","notes"]
R=[
["DM-01","review-scope","What effects, alternatives and resources an impact review must cover","(none; new)","PI-NEPA-07|PI-NEPA-04|PI-NEPA-09","narrowing","Seven County; DOI dropped direct/indirect/cumulative categories"],
["DM-02","review-timeline","Deadlines, page limits, paid acceleration, comment and objection windows","NEPA-timeline","PI-NEPA-01|PI-NEPA-08|PI-FOR-02","compressing","Generalizes beyond NEPA to state shot clocks and objection rules"],
["DM-03","screening-exemption","Categorical exclusions, exemptions, CE adoption across agencies, statutory exclusions","CatEx-scope","PI-NEPA-05|PI-NEPA-09|PI-FOR-01|PI-SEPA-01","expanding","Includes CEQA-type exemptions"],
["DM-04","participation-requirement","Required versus discretionary public involvement, comment periods, cooperating-agency participation","(none; new)","PI-NEPA-04|PI-NEPA-09","shrinking (required); discretion rising","Engagement moves from compliance step to judgment (SC-C06)"],
["DM-05","multi-agency-coordination","Lead, cooperating and participating roles; one-document approach; joint schedules and dashboards","one-federal-decision","PI-NEPA-01|PI-NEPA-10|PI-NEPA-04","codified in statute; agency discretion over cooperators","Replaces an executive-order label with the durable mechanism"],
["DM-06","esa-consultation","Section 7 consultation, incidental take, 4(d) and critical habitat rules","consultation-reform (part)","PI-ESA-01|PI-ESA-02|PI-ESA-03","narrowing; litigated","Split from consultation-reform"],
["DM-07","historic-preservation-review","NHPA section 106 review and program alternatives","consultation-reform (part)","PI-TRIBE-02","not verified this session","Becomes the critical path when NEPA accelerates"],
["DM-08","judicial-review","Deference, standing, limitations periods, remedies (vacatur vs remand)","(none; new)","PI-NEPA-07|PI-NEPA-09|PI-CWA-02","deference up; remedies narrowing (pending)","Drives record-integrity and litigation-risk competencies"],
["DM-09","jurisdiction-scope","Which waters, lands, species or sources fall under federal authority","(none; new)","PI-CWA-01","narrowing (proposed)","Pushes work to state, Tribal and local law"],
["DM-10","substantive-standard","Protective standards, definitions and findings that set what is prohibited or required","(none; new)","PI-ESA-01|PI-CAA-01|PI-CAA-02","rescinding (federal)","Litigated; states and air districts respond"],
["DM-11","authority-delegation","State or Tribal primacy, assumption and delegated programs and their oversight","(none; new)","PI-CWA-02","fragile","Florida 404 reverted to Corps in 2026"],
["DM-12","agreement-authority","Shared implementation agreements: GNA, recreation GNA, co-stewardship, TFPA, 638, shared stewardship MOUs","(none; new)","PI-GNA-01|PI-GNA-02|PI-GNA-03|PI-TRIBE-01","expanding (GNA); uncertain (co-stewardship)","Sovereign-consultation is a relationship tag, not a reform mechanism (TN)"],
["DM-13","disclosure-requirement","Mandatory reporting and disclosure by regulated entities","(none; new)","PI-DISC-01|PI-DISC-02|PI-DISC-03|PI-CAA-02","federal receding; CA starting; EU narrowed","Private-sector statecraft driver"],
["DM-14","digital-process","Electronic permitting, data standards, workflow automation, AI governance in review","digital-permitting","PI-TECH-01|PI-TECH-02|PI-TECH-03|PI-TECH-04|PI-AI-01","expanding","Most persistent v1 flag"],
["DM-15","fiscal-mechanism","Fees, cost recovery, revenue retention, appropriations conditions","(none; new)","PI-NEPA-08|PI-GNA-01","expanding (fees, retention)","Links to SC-C10"],
["DM-16","workforce-capacity","Hiring rules, staffing levels and classification changes that change capacity to perform","(none; new)","","not assessed by SC","FH/SL lane; include so capacity shocks are not mistaken for skill change"],
["DM-00","(retired) S2-S3-boundary","Workflow-model property, not a driver","S2-S3-boundary","","n/a","Retire as a flag; keep as a workflow note"],
]
with open(OUT,"w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(H)
    for r in R:
        assert len(r)==len(H); w.writerow(r)
print(len(R))
