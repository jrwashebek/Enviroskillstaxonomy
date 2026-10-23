#!/usr/bin/env python3
"""Generate WP-03 reports from the records (never typed): disposition coverage, WP-08 task-bundle handoff, counts.

Outputs (docs/build/WP-03/):
  disposition_coverage.csv     every FC-lane row of candidate_disposition.csv and v1_disposition.csv -> record or merge
  handoff_wp08_task_bundles.csv suggested P1 task bundles (COR-1, COR-2, R09) with formation-task and entry suggestions
  counts.json                   counts quoted in the worklog and final reply
Licence: Apache-2.0.
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402

DEC = ROOT / "docs/decisions"
LV = ["L1", "L2", "L3", "L4", "L5"]

FC_CANDS_CORE = "FC-C01 FC-C02 FC-C03 FC-C11 FC-C12 FC-C14 FC-C16 FC-C18 FC-C20 FC-C21 FC-C22 FC-C23 FC-C24 FC-C26 FC-C28 FC-C31 FS-C04 DB-C03".split()
V1_LANE = "1.1.2 1.1.5 1.2.1 1.2.4 1.2.5 1.4.2 1.4.3 1.4.4 1.6.2 1.7.1 1.3.1 1.3.2 1.3.4 1.8.3 4.1.1 4.1.2 4.1.3 4.1.4 4.1.5 4.2.1 4.2.2 4.2.3 4.2.4 4.2.5 4.3.1 4.3.2 4.3.3 4.3.4 4.3.5 4.4.1 4.4.2 4.4.3 4.4.4 4.4.5 4.5.1 4.5.2 4.5.3 4.5.4 4.5.5 4.6.1 4.6.2 4.6.3 4.6.4 4.6.5 4.7.1 4.7.2 4.7.3 4.7.4 4.7.5".split()

# Role -> core competencies the role draws on (FC judgment [J]; WP-08 decides the bundle)
ROLE_COMPS = {
    "R01-conservation-corps-member": ["seed:v1-4.2.1", "seed:v1-4.2.2", "seed:v1-4.2.4", "seed:v1-4.2.5", "seed:v1-4.5.1", "seed:v1-4.5.2", "seed:v1-4.4.1-A", "seed:v1-4.4.2", "seed:v1-4.4.5", "seed:v1-4.5.3-A", "seed:FC-C18", "seed:FC-C11", "seed:FC-C23"],
    "R02-field-resource-technician": ["seed:v1-4.1.1", "seed:v1-4.1.2", "seed:v1-4.1.3", "seed:v1-4.1.4", "seed:v1-1.4.3", "seed:FC-C23", "seed:FC-C24", "seed:FC-C16", "seed:FC-C18", "seed:FC-C11", "seed:FC-C12", "seed:FC-C14", "seed:FC-C01", "seed:FC-C02", "seed:v1-1.1.2", "seed:FC-C22", "seed:FC-C20", "seed:v1-4.4.1-A", "seed:v1-4.4.2", "seed:v1-4.5.3-A"],
    "R03-monitoring-data-technician": ["seed:FC-C01", "seed:FC-C24", "seed:FC-C23", "seed:FC-C16", "seed:v1-4.1.3", "seed:FC-C31", "seed:FC-C12", "seed:FC-C02", "seed:FC-C14", "seed:FS-C04", "seed:v1-4.4.1-A", "seed:v1-4.4.4-A"],
    "R04-geospatial-remote-sensing-analyst": ["seed:FC-C02", "seed:FS-C04", "seed:FC-C14"],
    "R05-ground-truth-validation-steward": ["seed:FC-C02", "seed:FS-C04", "seed:FC-C31", "seed:FC-C03", "seed:v1-1.4.3", "seed:v1-4.1.1", "seed:FC-C23", "seed:FC-C14", "seed:DC-CAND-13"],
    "R06-wildland-fire-operations": ["seed:v1-4.4.1-A", "seed:v1-4.5.1", "seed:v1-4.5.2", "seed:FC-C18", "seed:v1-4.4.2", "seed:v1-4.4.5", "seed:v1-4.5.3-A", "seed:FC-C14", "seed:FC-C20", "seed:v1-4.5.5", "seed:FC-C26"],
    "R07-fuels-prescribed-fire-specialist": ["seed:FC-C14", "seed:v1-4.4.1-A", "seed:FC-C20", "seed:v1-4.1.1", "seed:FC-C22", "seed:FC-C02", "seed:FC-C28", "seed:v1-4.5.2", "seed:FC-C21"],
    "R08-fire-intelligence-analyst": ["seed:FC-C02", "seed:DC-CAND-13"],
    "R09-restoration-project-lead": ["seed:v1-4.2.1", "seed:v1-4.2.2", "seed:v1-4.2.4", "seed:FC-C21", "seed:FC-C22", "seed:FC-C28", "seed:FC-C20", "seed:v1-1.1.2", "seed:v1-1.1.5", "seed:v1-1.7.1", "seed:v1-4.1.4", "seed:FC-C11", "seed:v1-4.4.1-A"],
}


def main():
    man = list(csv.DictReader(open(HERE / "manifest.csv", encoding="utf-8")))
    recs = {r["id"]: L.load_yaml(ROOT / r["path"]) for r in man}
    comps = {k: v for k, v in recs.items() if v["type"] == "Competency"}
    tasks = {k: v for k, v in recs.items() if v["type"] == "Task" and any("fc-agent" in a for a in v["provenance"]["agent"])}
    inds = {k: v for k, v in recs.items() if v["type"] == "Indicator"}
    # tasks per competency (any lane), from all task files on disk
    all_tasks = {}
    for p in sorted((L.DATA_V2 / "core" / "tasks").glob("*.yaml")):
        t = L.load_yaml(p)
        all_tasks[t["id"]] = t
    by_comp = defaultdict(list)
    for tid, t in all_tasks.items():
        if t.get("status") in ("superseded", "withdrawn"):
            continue
        for s in t.get("supports", []):
            by_comp[s["competency"]].append(tid)
    # ---------------------------------------------------------------- disposition coverage
    rows = []
    for r in csv.DictReader(open(DEC / "candidate_disposition.csv", encoding="utf-8")):
        cid, tgt = r["cand_id"], r["target"]
        mine = cid in FC_CANDS_CORE or cid.startswith("FC-") or any(x.strip() in ("FC-C02", "FC-C14", "FC-C31", "v1:4.2.2", "v1:4.4.1", "v1:4.2.1", "v1:1.4.3", "v1:4.4.4") for x in tgt.split("|")) and r["decision"] == "merge-into"
        if not mine:
            continue
        key = f"seed:{cid}"
        if r["decision"] == "core-v2.0":
            status = "authored (WP-03)" if key in comps else "not authored"
            where = key
        elif r["decision"] == "merge-into":
            t = tgt.strip()
            tkey = "seed:" + (t.replace("v1:", "v1-") if t.startswith("v1:") else t)
            if t == "v1:4.4.1":
                tkey = "seed:v1-4.4.1-A"
            if t == "v1:4.4.4":
                tkey = "seed:v1-4.4.4-A"
            status = ("merged into WP-03 record" if tkey in comps else "merge: target in another lane (see CR/handoff)")
            where = tkey
        else:
            status = f"{r['decision']} -> {tgt} (WP-06 lane; field enactment handoff in worklog)"
            where = tgt
        rows.append({"row": cid, "table": "candidate_disposition", "decision": r["decision"], "target": tgt, "wp03_record_or_merge": where, "status": status})
    for r in csv.DictReader(open(DEC / "v1_disposition.csv", encoding="utf-8")):
        code = r["v1_code"]
        if code not in V1_LANE:
            continue
        key = f"seed:v1-{code}"
        dec = r["decision"]
        if dec in ("carry", "rewrite"):
            where, status = key, ("authored (WP-03)" if key in comps else "not authored by WP-03")
        elif dec == "split":
            succ = [k for k in comps if k.startswith(key + "-")] + ([k for k in comps if k == "seed:v1-4.1.4"] if code == "1.2.1" else [])
            where = "|".join(succ) or "-"
            status = "split: FC successor authored; other parts in their lanes" if succ else "split: successors in other lanes"
        elif dec == "merge":
            where = r["target"]
            tk = "seed:" + (where.replace("v1:", "v1-") if where.startswith("v1:") else where)
            status = "merged into WP-03 record" if tk in comps else "merged into another lane's record"
        elif dec in ("move-to-tools",):
            rem = [k for k in comps if k in ("seed:FC-C16", "seed:FC-C23", "seed:FC-C14")]
            where = r["target"]
            status = "durable remainder merged into WP-03 record; tool to L4 (WP-04)"
        else:
            where, status = r["target"], f"{dec} (WP-06 lane)"
        rows.append({"row": code, "table": "v1_disposition", "decision": dec, "target": r["target"], "wp03_record_or_merge": where, "status": status})
    with open(HERE / "disposition_coverage.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["row", "table", "decision", "target", "wp03_record_or_merge", "status"])
        w.writeheader()
        w.writerows(rows)
    # ---------------------------------------------------------------- WP-08 task bundles
    roles = {r["role_key"]: r for r in csv.DictReader(open(DEC / "mvp_role_set.csv", encoding="utf-8"))}
    lowest = {}
    served_low = defaultdict(set)
    for cid, c in comps.items():
        lv = [l["level"] for l in c.get("levels", [])]
        lowest[cid] = min(lv, key=LV.index) if lv else None
    for iid, i in inds.items():
        if lowest.get(i["competency"]) == i["level"]:
            for t in i.get("servedTasks", []):
                served_low[i["competency"]].add(t)
    # FC enactment of DC-CAND-13: its tasks
    ena_tasks = [t for t in tasks if t.startswith("seed:fc-txa-")]
    out = []
    for rk, clist in ROLE_COMPS.items():
        role = roles[rk]
        levels = role["levels"].split("|")
        entry = "entry" in levels
        for cid in clist:
            tids = ena_tasks if cid == "seed:DC-CAND-13" else sorted(set(by_comp.get(cid, [])) & set(tasks))
            for tid in tids:
                t = tasks[tid]
                rr = t.get("reproductionRegime", {})
                at_low = tid in served_low.get(cid, set()) or cid == "seed:DC-CAND-13"
                formation = entry and t["formationDependency"] in ("yes", "partial") and rr.get("mentorshipDependence") in ("M", "H") and at_low
                out.append({"role_key": rk, "corridor": role["corridor"], "role_levels": role["levels"], "competency": cid,
                            "task": tid, "statement": t["statement"]["en"],
                            "suggest_roleLevels": ("entry|journey" if at_low and entry else ("journey|senior" if at_low else "senior|lead")),
                            "suggest_neededAtEntry": str(bool(entry and at_low)).lower(),
                            "suggest_formationTask": str(bool(formation)).lower(),
                            "fieldDependency": t["fieldDependency"], "formationDependency": t["formationDependency"],
                            "mentorshipDependence": rr.get("mentorshipDependence", ""),
                            "basis": "WP-03 [S] suggestion: formation = entry role AND formationDependency yes/partial AND mentorship M/H AND task served at the competency's lowest published level; WP-08 and IO decide (never LLM sole coder of neededAtEntry/critical, protocol_llm_coder_gate.md §2)"})
    with open(HERE / "handoff_wp08_task_bundles.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    # ---------------------------------------------------------------- counts
    tcount = Counter()
    for cid in comps:
        tcount[cid] = len(set(by_comp.get(cid, [])))
    split_roles = Counter()
    for t in tasks.values():
        note = t.get("editorialNote", {}).get("en", "")
        for k, v in (("execution to protocol", "P"), ("adaptation or decision in place", "A"), ("specification, review or defence", "R"), ("design or planning", "D"), ("formation of others", "F")):
            if k in note:
                split_roles[v] += 1
    counts = {
        "competencies_authored": len(comps),
        "competencies_by_source": dict(Counter("v1-seed" if k.startswith("seed:v1-") and not k.endswith(("-A",)) else ("split-target" if k.endswith("-A") else "candidate") for k in comps)),
        "tasks_authored_by_wp03": len(tasks),
        "tasks_by_g2_split_role": dict(split_roles),
        "tasks_with_credential_gates": sum(1 for t in tasks.values() if t.get("credentialGates")),
        "tasks_formationDependency": dict(Counter(t["formationDependency"] for t in tasks.values())),
        "tasks_fieldDependency": dict(Counter(t["fieldDependency"] for t in tasks.values())),
        "indicators_authored": len(inds),
        "indicators_by_mode": dict(Counter(i["augmentationMode"] for i in inds.values())),
        "enactments_authored": sum(1 for v in recs.values() if v["type"] == "Enactment"),
        "min_tasks_per_competency": min(tcount.values()),
        "competencies_with_fewer_than_3_tasks": [k for k, v in tcount.items() if v < 3],
        "craft_rating_records": sum(1 for _ in open(ROOT / "data/v2/assessments/emst-craft@0.1/wp03-fc-pass1.jsonl")) * 3,
        "wp08_handoff_rows": len(out),
        "wp08_formation_task_suggestions": sum(1 for o in out if o["suggest_formationTask"] == "true"),
        "wp08_formation_by_entry_role": dict(Counter(o["role_key"] for o in out if o["suggest_formationTask"] == "true")),
        "disposition_rows_covered": len(rows),
        "disposition_rows_not_authored": [r["row"] for r in rows if r["status"].startswith("not authored")],
    }
    with open(HERE / "competency_index.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["competency", "prefLabel", "levelSpan", "published_levels", "lifecycleState", "tasks_supporting", "wp03_indicators"])
        for cid in sorted(comps):
            c = comps[cid]
            n_ind = sum(len(l["indicators"]) for l in c.get("levels", []))
            w.writerow([cid, c["prefLabel"]["en"], f"{c['levelSpan']['min']}-{c['levelSpan']['max']}",
                        "|".join(l["level"] for l in c.get("levels", [])), c["lifecycleState"], tcount[cid], n_ind])
    (HERE / "counts.json").write_text(json.dumps(counts, indent=1), encoding="utf-8")
    print(json.dumps(counts, indent=1))


if __name__ == "__main__":
    main()
