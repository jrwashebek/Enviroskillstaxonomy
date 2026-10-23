"""Validate AS CSVs against TEAM_BRIEF schemas 5.1, 5.3, 5.4, 5.5. Run: python3 -I validate_csvs.py"""
import csv, os, re, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
err = []
def load(n):
    with open(os.path.join(D, n), encoding="utf-8") as f:
        return list(csv.DictReader(f)), open(os.path.join(D, n), encoding="utf-8").readline().strip()

src, h = load("sources.csv")
assert h == "source_id,title,author_or_publisher,date_published,url,source_type,accessed,used_for,quality,status,why_chosen", h
ids = set()
ST = {"peer-reviewed","government","standard","dataset","index","industry-report","job-posting","grey-literature","news","practitioner","legal"}
for r in src:
    if not re.fullmatch(r"AS-\d{3}", r["source_id"]): err.append(("src id", r["source_id"]))
    if r["source_id"] in ids: err.append(("dup src", r["source_id"]))
    ids.add(r["source_id"])
    if r["source_type"] not in ST: err.append(("src type", r["source_id"], r["source_type"]))
    if not re.match(r"(High|Medium|Low|Medium-High|Low-Medium)(;| )", r["quality"]): err.append(("quality", r["source_id"], r["quality"]))
    if not (r["status"] in {"current","outdated","poor-fit","unverified"} or r["status"].startswith("superseded-by:")): err.append(("status", r["source_id"], r["status"]))

def check_ids(field, rid, allow_other=False):
    for s in [x for x in field.split("|") if x]:
        if s.startswith("AS-") and s not in ids: err.append(("unresolved", rid, s))
        if not s.startswith("AS-") and not allow_other: err.append(("foreign id", rid, s))

eco, h = load("ecosystem.csv")
assert h == "entity_id,name,entity_type,owner_or_host,sector_focus,what_it_illuminates,latest_release_or_status,how_emst_connects,integration_detail,url,evidence_label,source_ids,proposed_by", h
ET = {"index","dataset","research-program","paper","working-group","coalition","organization","fund","standard","tool","platform","policy","credential"}
HC = {"ingest","crosswalk","benchmark","partner","funder","adopter","validator","distribution","watch"}
seen = set()
for r in eco:
    if r["entity_type"] not in ET: err.append(("etype", r["entity_id"], r["entity_type"]))
    for c in r["how_emst_connects"].split("|"):
        if c not in HC: err.append(("connects", r["entity_id"], c))
    if r["evidence_label"] not in {"E","J","S"}: err.append(("label", r["entity_id"]))
    if r["evidence_label"] == "E" and not r["source_ids"]: err.append(("E without source", r["entity_id"]))
    check_ids(r["source_ids"], r["entity_id"])
    if r["name"].lower() in seen: err.append(("dup name", r["name"]))
    seen.add(r["name"].lower())
    if not r["integration_detail"].strip(): err.append(("no integration", r["entity_id"]))

va, h = load("v1_assessment.csv")
assert h == "element,v1_location,verdict,rationale,evidence_label,source_ids,proposed_by", h
for r in va:
    if r["verdict"] not in {"carry","change","retire","add","needs-evidence"}: err.append(("verdict", r["element"]))
    if r["evidence_label"] not in {"E","J","S"}: err.append(("va label", r["element"]))
    check_ids(r["source_ids"], r["element"][:30])

rs, h = load("role_signals.csv")
assert h == "signal_id,role_title,sector_actor,subsector,signal_type,description,driver,horizon,evidence_label,source_ids,related_v1_codes,proposed_by", h
SA = {"federal","state","local","tribal","ngo","private","academic"}
DR = {"AI","automation-robotics","sensing-tech","policy-reform","climate","market","demographic","fiscal","other"}
for r in rs:
    for a in r["sector_actor"].split("|"):
        if a not in SA: err.append(("actor", r["signal_id"], a))
    if r["signal_type"] not in {"new-role","transforming-role","declining-role","merging-roles","splitting-role","skill-shift","entry-path-at-risk"}: err.append(("stype", r["signal_id"]))
    for d in r["driver"].split("|"):
        if d not in DR: err.append(("driver", r["signal_id"], d))
    if r["horizon"] not in {"now","1-3y","3-5y","5-10y","10y+"}: err.append(("horizon", r["signal_id"]))
    check_ids(r["source_ids"], r["signal_id"])

# v1 codes resolve
v1 = {r["code"] for r in csv.DictReader(open("/home/claude/emst/data/v1_baseline/competencies.csv", encoding="utf-8"))}
for r in rs:
    for c in [x for x in r["related_v1_codes"].split("|") if x]:
        if c not in v1: err.append(("v1 code", r["signal_id"], c))

# Source IDs cited in markdown resolve
for md in ["adoption_roadmap.md","ngo_pilot_design.md","governance_charter_draft.md","sustainability_model.md","report.md"]:
    p = os.path.join(D, md)
    if os.path.exists(p):
        for m in set(re.findall(r"AS-\d{3}\b", open(p, encoding="utf-8").read())):
            if m not in ids: err.append(("md unresolved", md, m))

used = set()
for r in eco + va + rs:
    used |= set(x for x in r["source_ids"].split("|") if x)
for md in ["adoption_roadmap.md","ngo_pilot_design.md","governance_charter_draft.md","sustainability_model.md","report.md"]:
    p = os.path.join(D, md)
    if os.path.exists(p): used |= set(re.findall(r"AS-\d{3}\b", open(p, encoding="utf-8").read()))
print("sources:", len(src), "| ecosystem:", len(eco), "| v1_assessment:", len(va), "| role_signals:", len(rs))
print("unused sources:", sorted(ids - used))
print("ERRORS:", len(err))
for e in err: print(" ", e)
sys.exit(1 if err else 0)
