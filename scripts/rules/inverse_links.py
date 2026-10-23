"""inverse-links@1.2.0 (vocab/rules/inverse-links@1.2.0.yaml; ADR-0021, ADR-0029 §4.3, ADR-0030).

Links are stored once, on the many side; these inverses exist only in bundles and views:
  Competency.tasks[]       from Task.supports            ({task, strength}, sorted by task)
  Task.tools[]             from Tool.servesTasks         (sorted IDs; L4 points to L2, never the reverse)
  Competency.enactments[]  from Enactment.competency     ({enactment, enactmentKind, module}, sorted)
  X.mirroredBy[]           from Competency.mirrors[]     ({competency, relation}, sorted; X a competency or enactment)
Only released records take part, so an inverse never lists a record the release gate excluded.
"""
from __future__ import annotations

from collections import defaultdict


def compute(released: dict) -> dict:
    tasks, tools, enactments, mirrored = defaultdict(list), defaultdict(set), defaultdict(list), defaultdict(list)
    for rid, r in released.items():
        typ = r.get("type")
        if typ == "Task":
            for s in r.get("supports") or []:
                if isinstance(s, dict) and s.get("competency") in released:
                    tasks[s["competency"]].append({"task": rid, "strength": s.get("strength")})
        elif typ == "Tool":
            for t in r.get("servesTasks") or []:
                if t in released and released[t].get("type") == "Task":
                    tools[t].add(rid)
        if typ == "Competency":
            for m in r.get("mirrors") or []:
                t = m.get("target") if isinstance(m, dict) else None
                if t in released and released[t].get("type") in ("Competency", "Enactment"):
                    mirrored[t].append({"competency": rid, "relation": m.get("relation")})
        if typ == "Enactment":
            c = r.get("competency")
            if c in released and released[c].get("type") == "Competency":
                enactments[c].append({"enactment": rid, "enactmentKind": r.get("enactmentKind"), "module": r.get("module")})
    return {
        "_enactment_ids": {rid for rid, r in released.items() if r.get("type") == "Enactment"},
        "competency_tasks": {c: sorted(v, key=lambda x: x["task"]) for c, v in tasks.items()},
        "task_tools": {t: sorted(v) for t, v in tools.items()},
        "competency_enactments": {c: sorted(v, key=lambda x: x["enactment"]) for c, v in enactments.items()},
        "mirrored_by": {t: sorted(v, key=lambda x: (x["competency"], str(x["relation"]))) for t, v in mirrored.items()},
    }


def bundle_fields(inv: dict) -> dict:
    """{record id: {field: value}} merged into bundle records (rule outputs.bundle_fields)."""
    out = defaultdict(dict)
    for t, ids in inv["task_tools"].items():
        out[t]["tools"] = ids
    for c, items in inv["competency_enactments"].items():
        out[c]["enactments"] = [{"id": e["enactment"], "enactmentKind": e["enactmentKind"], "module": e["module"]} for e in items]
    for t, items in inv.get("mirrored_by", {}).items():
        out[t]["mirroredBy"] = [{"id": m["competency"], "relation": m["relation"]} for m in items]
    return out


def view_rows(inv: dict, stamp: dict) -> list[dict]:
    rows = []
    mirrored = inv.get("mirrored_by", {})
    enactment_ids = inv.get("_enactment_ids", set())
    for c in sorted(set(inv["competency_tasks"]) | set(inv["competency_enactments"]) | (set(mirrored) - enactment_ids)):
        rows.append({"competency": c, "tasks": inv["competency_tasks"].get(c, []),
                     "enactments": inv["competency_enactments"].get(c, []), "mirroredBy": mirrored.get(c, []), **stamp})
    for e in sorted(set(mirrored) & enactment_ids):
        rows.append({"enactment": e, "mirroredBy": mirrored[e], **stamp})
    for t in sorted(inv["task_tools"]):
        rows.append({"task": t, "tools": inv["task_tools"][t], **stamp})
    return rows
