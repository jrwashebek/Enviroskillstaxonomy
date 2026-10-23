"""Generated WP-04 counts (S1 brief: counts by script, not typed). Run from the repo root."""
import glob, json, sys
from collections import Counter, defaultdict
sys.path.insert(0, "scripts")
import emstlib as L  # noqa: E402
AG = "emstagent:A4-DC@wp-04"
c = Counter(); comp_types = Counter(); lifec = Counter(); seeds_rewritten = 0
tasks_by_comp = defaultdict(int); mine_comps = []
for p in glob.glob("data/v2/core/**/*.yaml", recursive=True):
    d = L.load_yaml(p)
    if not isinstance(d, dict) or AG not in (d.get("provenance") or {}).get("agent", []):
        continue
    c[d["type"] + ("" if d.get("status") != "superseded" else " (superseded)")] += 1
    if d["type"] == "Competency":
        mine_comps.append(d["id"]); comp_types[d.get("competencyType") + (("/" + d["transversalCluster"]) if d.get("transversalCluster") else "")] += 1
        lifec[d.get("lifecycleState")] += 1
        seeds_rewritten += d["id"].startswith("seed:v1-")
for p in glob.glob("data/v2/core/tasks/*.yaml"):
    d = L.load_yaml(p)
    if d.get("status") in ("superseded", "withdrawn"):
        continue
    for s in d.get("supports", []):
        if s["strength"] == "primary":
            tasks_by_comp[s["competency"]] += 1
tools = [json.loads(l) for l in open("data/v2/tools/tools.jsonl")]
steward = Counter(t["editorialNote"]["en"].split(" (")[0].replace("Steward: ", "").split(" ")[0] for t in tools)
x12 = [l.split("\t") for l in open("data/v2/crosswalks/dol-ai-literacy/ten-07-25.sssom.tsv").read().splitlines()[1:]]
ratings = sum(1 for p in glob.glob("data/v2/assessments/emst-craft@0.1/wp04-dc-pass*.jsonl") for _ in open(p))
out = {"records_by_type": dict(c), "competencies_by_type": dict(comp_types), "competency_lifecycle": dict(lifec),
       "v1_seed_competencies_rewritten_in_place": seeds_rewritten, "new_candidate_competencies": len(mine_comps) - seeds_rewritten,
       "competencies_with_lt3_primary_tasks": sorted(k for k in mine_comps if tasks_by_comp[k] < 3),
       "tools": len(tools), "tools_by_lifecycle": dict(Counter(t["lifecycleState"] for t in tools)), "tools_by_steward": dict(steward),
       "tools_by_type": dict(Counter(t["toolType"] for t in tools)),
       "x12_rows": len(x12), "x12_notermfound": sum(1 for r in x12 if r[5] == "sssom:NoTermFound"),
       "x12_dol_objects": len({r[5] for r in x12 if r[5] != "sssom:NoTermFound"}), "craft_ratings": ratings}
print(json.dumps(out, indent=1))
json.dump(out, open("docs/build/WP-04/counts.json", "w"), indent=1)
