#!/usr/bin/env python3
"""Generate the S2 close-out B completion table and counts (never typed by hand).

Reads docs/decisions/integration/s2_work_orders.csv (rows assigned to builder B by author code), manifest.csv (every
record this builder wrote, patched or moved, with its work-order row) and the craft-rating batches; writes
counts.json and replaces the block between the COMPLETION markers in WORKLOG.md.

  python3 docs/build/S2-closeout-B/report_s2b.py
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import emstlib as L  # noqa: E402

ORDERS = REPO / "docs" / "decisions" / "integration" / "s2_work_orders.csv"
AUTHORS = {"A6 DB", "A3 FC (as WP-08 contributor)", "A4 DC", "A8 LC", "A8 LC with IO", "A9 LM with FS"}

# Outcome per row: (status, what was done). Status is one of done | done (verified) | partial.
OUTCOME = {
    "2": ("done", "core competency authored L1-L4; module enactments hazards, forest, envhealth"),
    "3": ("done", "core competency authored L1-L4; six v1 3.3.2/3.3.3 task seeds rewritten"),
    "9": ("done", "core competency authored (emerging, reviewBy 2027-10-23) L2-L4; DC review pending"),
    "10": ("done", "core competency authored L3-L5"),
    "17": ("done", "seed rewritten in place L1-L4; 6.7.3 merged; held research-code enactments not authored"),
    "18": ("done", "seed rewritten in place L1-L4 with IO review code; 3.5.2 and 5.4.3 tasks rewritten"),
    "19": ("done", "seed rewritten in place L1-L4; 5.1.2/5.1.5/5.5.4/5.1.4 tasks rewritten"),
    "20": ("done", "seed rewritten in place L1-L4; 5.4.5 tasks made distinct"),
    "21": ("done", "seed rewritten in place L1-L4; 5.4.2 tasks rewritten"),
    "22": ("done", "seed rewritten in place L1-L4; 5.6.1 as knowledge statements; 5.6.1-T2 superseded"),
    "25": ("done", "task + 3 indicators added to SL-C03; contributing links; SC review pending"),
    "26": ("done", "2 tasks + L2 halt indicator; contributing links to v1-4.4.4-A, FC-C24; FC review pending"),
    "27": ("done", "station-condition and community-sensor tasks (contributing FC-C21); FC review pending"),
    "28": ("done", "laboratory data review task and L2 indicator in v1 2.2.3; DC review pending"),
    "29": ("done", "module candidate authored (wildlife, L1-L3); FC review pending; disposition row at WP-16 (CA)"),
    "30": ("done", "SL-C07 refocused on plan review/site evaluation; seed:ena-sl-c03-envhealth with 4 tasks and 7 indicator variants"),
    "31": ("done", "subsectors moved into Enactment.subsectors on every module enactment"),
    "33": ("done", "roles set on all 17 links of the 11 DB module enactments"),
    "34": ("done (verified)", "links already set by builder A (SC) per LM's resolution table; checked, not re-edited"),
    "37": ("done", "11 pathways moved (8 core, 3 forest); typed formationProvisions and cloOutcomes; staging removed"),
    "38": ("done", "4 rows re-coded employer-mandated; 3 missing module gate records added and linked"),
    "39": ("done", "names with a clean case-sensitive dry run moved to productExamples; the rest kept with reasons"),
    "40": ("done", "DB review of DB-C06 and DB-C21 recorded; two small changes applied as DC (PS-C07/PS-C09 are builder A's)"),
    "41": ("done (verified)", "0 mvp-role placeholders; 2 sector-specific signals re-keyed to federal variants"),
}


def _csv(name):
    p = HERE / "generated" / name
    return L.read_csv(p) if p.exists() else []


GEN_NOTE = {
    "31": lambda: f" ({sum(1 for r in _csv('enactment_subsectors.csv') if r['action'] == 'moved')} moved, "
                  f"{sum(1 for r in _csv('enactment_subsectors.csv') if r['action'] == 'already-set')} already set; generated/enactment_subsectors.csv)",
    "33": lambda: f" ({len(_csv('db_module_link_roles.csv'))} links; generated/db_module_link_roles.csv)",
    "37": lambda: f" ({sum(int(r['provisions']) for r in _csv('pathway_moves.csv'))} provisions, "
                  f"{sum(int(r['clo_outcomes']) for r in _csv('pathway_moves.csv'))} pathway-level CLOs; generated/pathway_moves.csv)",
    "38": lambda: f" (generated/credential_moves.csv, {len(_csv('credential_moves.csv'))} rows)",
    "39": lambda: f" ({sum(1 for r in _csv('product_name_dryrun.csv') if r['decision'] == 'move')} moved, "
                  f"{sum(1 for r in _csv('product_name_dryrun.csv') if r['decision'] != 'move')} kept; generated/product_name_dryrun.csv)",
}


def mine(row_no, r):
    a = r["author"]
    return (a in AUTHORS or a == "A9 LM" or a.startswith("A6 DB (") or (a == "A9 LM with A5 SC" and r["kind"] == "data-move"))


def main():
    orders = L.read_csv(ORDERS)
    man = L.read_csv(HERE / "manifest.csv")
    by_row = defaultdict(Counter)
    for m in man:
        by_row[m["row"]][(m["type"], m["action"])] += 1
    lines = ["| Row | Kind | Target | Author code | Status | Records touched (type: action = n) | What was done |",
             "|---|---|---|---|---|---|---|"]
    assigned, done = 0, 0
    for i, r in enumerate(orders, start=2):
        if not mine(i, r):
            continue
        assigned += 1
        st, what = OUTCOME.get(str(i), ("not done", ""))
        what += GEN_NOTE.get(str(i), lambda: "")()
        done += st.startswith("done")
        touched = "; ".join(f"{t}: {a} = {n}" for (t, a), n in sorted(by_row.get(str(i), {}).items())) or "-"
        tgt = r["target"] if len(r["target"]) < 60 else r["target"][:57] + "..."
        lines.append(f"| {i} | {r['kind']} | `{tgt}` | {r['author']} | {st} | {touched} | {what} |")
    ratings = Counter()
    for n in (1, 2, 3):
        p = REPO / "data" / "v2" / "assessments" / "emst-craft@0.1" / f"s2b-pass{n}.jsonl"
        if p.exists():
            ratings[f"pass{n}"] = sum(1 for x in p.read_text(encoding="utf-8").splitlines() if x.strip())
    by_type = Counter((m["type"], m["action"]) for m in man)
    counts = {"rows_assigned": assigned, "rows_done": done,
              "records_by_type_action": {f"{t}:{a}": n for (t, a), n in sorted(by_type.items())},
              "records_total": len(man), "craft_ratings": dict(ratings)}
    (HERE / "counts.json").write_text(json.dumps(counts, indent=1) + "\n", encoding="utf-8")
    block = ["<!-- COMPLETION:BEGIN (generated by report_s2b.py; do not edit) -->",
             f"Rows assigned to builder B: **{assigned}**; done: **{done}**. Records written, patched or moved: {len(man)}; "
             f"craft ratings: {', '.join(f'{k} {v}' for k, v in sorted(ratings.items())) or 'none'}.", ""] + lines + \
            ["<!-- COMPLETION:END -->"]
    wl = HERE / "WORKLOG.md"
    text = wl.read_text(encoding="utf-8")
    if "<!-- COMPLETION:BEGIN" in text:
        pre = text.split("<!-- COMPLETION:BEGIN")[0]
        post = text.split("<!-- COMPLETION:END -->")[1]
        text = pre + "\n".join(block) + post
    else:
        text = text.rstrip() + "\n\n## Completion against the work orders\n\n" + "\n".join(block) + "\n"
    wl.write_text(text, encoding="utf-8")
    print(json.dumps(counts, indent=1))


if __name__ == "__main__":
    main()
