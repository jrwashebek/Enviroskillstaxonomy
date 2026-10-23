"""Write WP-04 craft ratings: three llm passes over WP-04 task statements (shuffled, statements only).

Honest limit: one model instance authored the tasks and coded all three passes, so the passes are run-to-run
consistency checks, not independent raters and not inter-rater reliability; agreement is computed by CI.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent / "rating"  # rating inputs live in docs/build/WP-04/rating
OUT = Path("/home/claude/emst/data/v2/assessments/emst-craft@0.1")
BATCHES = [("", 0), ("b", 1), ("c", 2)]
SEEDS_C = {1: 121, 2: 242, 3: 363}  # batch-c orders were drawn with these seeds
CONF = {1: "low", 2: "low", 3: "med", 4: "high", 5: "high"}
SEEDS = {1: 101, 2: 202, 3: 303}
total = 0
for p in (1, 2, 3):
  recs = []
  for suf, _ in BATCHES:
    rows = json.load(open(HERE / f"rate_tasks{'_' + suf if suf else ''}.json"))
    order = json.load(open(HERE / f"order{p}{suf}.json"))
    codes = [list(map(int, ln.split())) for ln in open(HERE / f"pass{p}{suf}.txt") if ln.strip()]
    assert len(codes) == len(order) == len(rows)
    seed = SEEDS[p] if not suf else (SEEDS_C[p] if suf == "c" else SEEDS[p] + 10 * p)
    for k, fc, dc, sc, conf in codes:
        tid, stmt, sha = rows[order[k]]
        slug = tid.split(":", 1)[1].replace("/", "--")
        rid = f"emstagent:dc-craft-rater-{p}@wp04"
        recs.append({
            "id": f"seed:asm/wp04-dc-pass{p}/{slug}", "type": "CraftRating",
            "prefLabel": {"en": f"WP-04 craft pass {p} rating of {tid}"},
            "layer": "L5", "module": "core", "status": "draft", "license": "CC0-1.0", "sensitivity": "public",
            "task": tid, "taskTextSha256": sha, "scale": "ordinal-0-2", "values": {"FC": fc, "DC": dc, "SC": sc},
            "raterType": "llm", "raterId": rid, "assessedAt": "2026-10-23",
            "method": (f"emst-craft-codebook@1.0.0-draft decision procedure; statements only, shuffled (seed {seed}), coded blind "
                       "to competency, domain and prior labels; same model instance that authored the tasks, so not blind to "
                       "authorship; run-to-run consistency pass, not inter-rater reliability"),
            "confidence": CONF[conf], "instrument": "emst-craft@0.1", "codebookVersion": "emst-craft-codebook@1.0.0-draft",
            "evidenceLabel": "S", "sources": [],
            "provenance": {"method": "llm-assisted", "agent": [rid], "generatedAt": "2026-10-23T16:00:00Z",
                           "toolVersion": "claude-opus-5-5", "promptVersion": "wp04-craft-pass@1", "evidenceLabel": "S",
                           "reviewStatus": "unreviewed"}})
  if True:
    recs.sort(key=lambda r: r["id"])
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"wp04-dc-pass{p}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in recs), encoding="utf-8")
    total += len(recs)
print("craft ratings written:", total)
