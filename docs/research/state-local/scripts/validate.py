#!/usr/bin/env python3
"""Validate SL CSV outputs: headers match TEAM_BRIEF schemas, rows have full width,
every source_id resolves to sources.csv, every v1 code exists in data/v1_baseline/competencies.csv,
controlled vocabularies are respected. Deterministic, no network. Run: python3 -I scripts/validate.py"""
import csv, os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
def rows(n): 
    with open(os.path.join(HERE, n), encoding="utf-8") as f: return list(csv.DictReader(f))
def hdr(n):
    with open(os.path.join(HERE, n), encoding="utf-8") as f: return next(csv.reader(f))
SCHEMA = {
 "sources.csv": "source_id,title,author_or_publisher,date_published,url,source_type,accessed,used_for,quality,status,why_chosen",
 "candidate_competencies.csv": "cand_id,proposed_title,description,craft_primary,craft_secondary,subsector,sector_actors,change_type,driver,evidence_label,source_ids,related_v1_codes,rationale,proposed_by",
 "role_signals.csv": "signal_id,role_title,sector_actor,subsector,signal_type,description,driver,horizon,evidence_label,source_ids,related_v1_codes,proposed_by",
 "v1_assessment.csv": "element,v1_location,verdict,rationale,evidence_label,source_ids,proposed_by",
 "ecosystem.csv": "entity_id,name,entity_type,owner_or_host,sector_focus,what_it_illuminates,latest_release_or_status,how_emst_connects,integration_detail,url,evidence_label,source_ids,proposed_by",
 "state_classification_sample.csv": "state,agency,class_title,class_code,series_or_family,min_qualifications,degree_required,pay_band_signal,url,emst_v1_codes,notes,source_ids",
 "state_policy_levers.csv": "lever_id,lever,level,example_states,how_it_works,relevance_to_emst,evidence_label,source_ids",
 "mobility_map.csv": "item_id,item_type,name,direction,mechanism,scale_or_evidence,emst_implication,evidence_label,source_ids",
 "minimal_common_fields.csv": "field,definition,type_or_format,requirement,controlled_vocab_or_example,why_needed,observed_in_sample,source_ids",
}
VOC = {
 ("sources.csv","source_type"): {"peer-reviewed","government","standard","dataset","index","industry-report","job-posting","grey-literature","news","practitioner","legal"},
 ("candidate_competencies.csv","craft_primary"): {"FC","DC","SC"},
 ("candidate_competencies.csv","change_type"): {"new","emerging","transforming","stable","declining"},
 ("role_signals.csv","signal_type"): {"new-role","transforming-role","declining-role","merging-roles","splitting-role","skill-shift","entry-path-at-risk"},
 ("role_signals.csv","horizon"): {"now","1-3y","3-5y","5-10y","10y+"},
 ("v1_assessment.csv","verdict"): {"carry","change","retire","add","needs-evidence"},
 ("ecosystem.csv","entity_type"): {"index","dataset","research-program","paper","working-group","coalition","organization","fund","standard","tool","platform","policy","credential"},
 ("state_classification_sample.csv","degree_required"): {"required","substitutable","not-required","agency-set","per-recruitment","not-stated"},
 ("state_policy_levers.csv","level"): {"state","local","multi","state|local"},
 ("minimal_common_fields.csv","requirement"): {"MUST","SHOULD","MAY"},
}
PIPE = {("candidate_competencies.csv","sector_actors"): {"federal","state","local","tribal","ngo","private","academic"},
        ("candidate_competencies.csv","driver"): {"AI","automation-robotics","sensing-tech","policy-reform","climate","market","demographic","fiscal","other"},
        ("role_signals.csv","driver"): {"AI","automation-robotics","sensing-tech","policy-reform","climate","market","demographic","fiscal","other"},
        ("ecosystem.csv","how_emst_connects"): {"ingest","crosswalk","benchmark","partner","funder","adopter","validator","distribution","watch"}}
err = []
srcids = {r["source_id"] for r in rows("sources.csv")}
codes = {r["code"] for r in csv.DictReader(open(os.path.join(ROOT,"data","v1_baseline","competencies.csv"), encoding="utf-8"))}
for n, h in SCHEMA.items():
    if hdr(n) != h.split(","): err.append(f"{n}: header mismatch")
    for i, r in enumerate(rows(n), 2):
        if None in r or any(v is None for v in r.values()): err.append(f"{n}:{i} wrong width")
        for s in (r.get("source_ids") or "").split("|"):
            if s and s not in srcids: err.append(f"{n}:{i} unresolved source {s}")
        for col in ("related_v1_codes","emst_v1_codes"):
            for c in (r.get(col) or "").split("|"):
                if c and c not in codes: err.append(f"{n}:{i} bad v1 code {c}")
        if "evidence_label" in r and r["evidence_label"] not in {"E","J","S"}: err.append(f"{n}:{i} bad evidence_label")
        if r.get("evidence_label") == "E" and n != "sources.csv" and not r.get("source_ids"): err.append(f"{n}:{i} E without source")
        for (fn,col),allowed in VOC.items():
            if fn==n and r[col] not in allowed: err.append(f"{n}:{i} {col}={r[col]!r}")
        for (fn,col),allowed in PIPE.items():
            if fn==n:
                for v in r[col].split("|"):
                    if v not in allowed: err.append(f"{n}:{i} {col} has {v!r}")
        if n=="sources.csv":
            q=r["quality"].split(";")[0]
            if q not in {"High","Medium","Low"}: err.append(f"{n}:{i} quality {q}")
            st=r["status"]
            if not (st in {"current","outdated","poor-fit","unverified"} or st.startswith("superseded-by:")): err.append(f"{n}:{i} status {st}")
print("\n".join(err) if err else "OK: all SL CSVs valid")
sys.exit(1 if err else 0)
