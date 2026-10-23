"""Validate TN CSV outputs against the team-brief schemas (section 5) and check that every source_id cited resolves."""
import csv, sys, os, re
D = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = {
 "sources.csv": "source_id,title,author_or_publisher,date_published,url,source_type,accessed,used_for,quality,status,why_chosen",
 "candidate_competencies.csv": "cand_id,proposed_title,description,craft_primary,craft_secondary,subsector,sector_actors,change_type,driver,evidence_label,source_ids,related_v1_codes,rationale,proposed_by",
 "role_signals.csv": "signal_id,role_title,sector_actor,subsector,signal_type,description,driver,horizon,evidence_label,source_ids,related_v1_codes,proposed_by",
 "v1_assessment.csv": "element,v1_location,verdict,rationale,evidence_label,source_ids,proposed_by",
 "ecosystem.csv": "entity_id,name,entity_type,owner_or_host,sector_focus,what_it_illuminates,latest_release_or_status,how_emst_connects,integration_detail,url,evidence_label,source_ids,proposed_by",
}
errs = []
data = {}
for fn, hdr in S.items():
    with open(os.path.join(D, fn), newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if rows[0] != hdr.split(","):
        errs.append(f"{fn}: header mismatch")
    for i, r in enumerate(rows[1:], 2):
        if len(r) != len(rows[0]):
            errs.append(f"{fn}:{i}: {len(r)} fields")
    data[fn] = [dict(zip(rows[0], r)) for r in rows[1:]]
ids = {r["source_id"] for r in data["sources.csv"]}
st = ("peer-reviewed","government","standard","dataset","index","industry-report","job-posting","grey-literature","news","practitioner","legal")
for r in data["sources.csv"]:
    if r["source_type"] not in st: errs.append(f"sources: bad type {r['source_id']}")
    if not re.match(r"^(High|Medium|Low|Medium-High|Low-Medium)(;|$)", r["quality"]): errs.append(f"sources: quality {r['source_id']}")
    if not (r["status"] in ("current","outdated","poor-fit","unverified") or r["status"].startswith("superseded-by:")): errs.append(f"sources: status {r['source_id']}")
for fn in ("candidate_competencies.csv","role_signals.csv","v1_assessment.csv","ecosystem.csv"):
    for r in data[fn]:
        for s in filter(None, r["source_ids"].split("|")):
            if s not in ids: errs.append(f"{fn}: unresolved {s}")
        if r["evidence_label"] not in ("E","J","S"): errs.append(f"{fn}: label")
        if r["proposed_by"] != "TN": errs.append(f"{fn}: proposed_by")
# report.md citations resolve
rp = os.path.join(D, "report.md")
if os.path.exists(rp):
    for s in set(re.findall(r"TN-\d{3}", open(rp, encoding="utf-8").read())):
        if s not in ids: errs.append(f"report.md: unresolved {s}")
for fn in ("tribal_engagement_protocol.md","indigenous_data_governance_policy.md"):
    p = os.path.join(D, fn)
    if os.path.exists(p):
        for s in set(re.findall(r"TN-\d{3}", open(p, encoding="utf-8").read())):
            if s not in ids: errs.append(f"{fn}: unresolved {s}")
print("\n".join(errs) if errs else "OK: all TN CSVs valid; all citations resolve")
print({k: len(v) for k, v in data.items()})
sys.exit(1 if errs else 0)
