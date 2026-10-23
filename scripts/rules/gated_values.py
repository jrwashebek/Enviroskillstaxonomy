"""display-gate@1.0.0 view (vocab/rules/display-gate@1.0.0.yaml; ADR-0029 §6.2).

For every gated value a view might show, IO's validation/display_gate.py::decide() says whether it renders and with
which marker. Gated values are the task-level ratings (one value per unit, dimension and codebook version, pooled
over raters) and Task.workFunction; the rule's editorial fields render with the label 'editorial' and are not
alpha-gated. The bundle and CSVs keep every value with its validationStatus; only views are gated (CP reads gated
values from this view or through decide()).
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import emstlib as L  # noqa: E402
from rules import io_bridge  # noqa: E402
from rules.agreement import dimension, unit  # noqa: E402

VALUE_FIELDS = ("values", "workFunction", "modes", "authorityPosition", "technicalExposure", "relevance", "scale")
PROVENANCE_RATER = {"llm-assisted": "llm", "v1-migration": "v1-analyst", "lexical-linker": "llm"}


def _fingerprint(r: dict) -> str:
    return json.dumps({k: r.get(k) for k in VALUE_FIELDS if k in r}, sort_keys=True)


def _decision(d: dict) -> str:
    if d.get("render"):
        return d["marker"]
    return "pending" if d.get("label") == "assessment_pending" else "hidden"


def _current_hash(target: dict | None):
    if not target:
        return None
    if target.get("type") == "Task":
        return target.get("textSha256")
    if target.get("type") == "Competency":
        return L.competency_text_sha256((target.get("prefLabel") or {}).get("en", ""), (target.get("statement") or {}).get("en", ""))
    return None


def editorial_rows(released: dict, editorial_fields: list[str], stamp: dict) -> list[dict]:
    want = defaultdict(list)
    for f in editorial_fields:
        t, field = f.split(".", 1)
        want[t].append(field)
    rows = []
    for rid, r in sorted(released.items()):
        for field in want.get(r.get("type"), []):
            if r.get(field) not in (None, [], ""):
                rows.append({"recordId": rid, "field": f"{r['type']}.{field}", "decision": "editorial", "label": "editorial",
                             "reason": "editorial field (not alpha-gated)", "studyId": None, **stamp})
    return rows


def compute(released: dict, rule: dict, results: dict, stamp: dict, view_tier: str = "describe") -> dict:
    """Returns the view document {header, rows}. results: {studyId: agreement result} from rules.agreement.emit."""
    gm = io_bridge.load("display_gate")
    header = {**stamp, "gatesFile": "validation/display_gates.yaml", "gatesSha256": io_bridge.file_sha256("validation/display_gates.yaml"),
              "viewTier": view_tier, "agreementResults": sorted(results)}
    if gm is None:
        header["engine"] = "unavailable: every gated value is hidden (fail closed)"
    gates = gm.load_gates() if gm else None
    by_dim = {(r["dimension"], r["codebookVersion"]): r for r in results.values()}
    definition = rule.get("definition") or {}
    rows = editorial_rows(released, definition.get("editorial_fields") or rule.get("editorial_fields") or [], stamp)
    groups = defaultdict(list)
    for rid, r in released.items():
        if r.get("type") in L.RATING_TYPES and unit(r):
            groups[(unit(r), dimension(r), r.get("codebookVersion"))].append(r)
    humans = set(gates["admissibility"]["rater_types_counted"]) if gates else set()
    for (u, dim, cbv), rs in sorted(groups.items(), key=lambda kv: tuple(str(x) for x in kv[0])):
        types = sorted({r.get("raterType") for r in rs})
        human = [r for r in rs if r.get("raterType") in humans]
        prints = {_fingerprint(r) for r in human}
        target = released.get(u)
        hashes = {r.get("taskTextSha256") or r.get("competencyTextSha256") or r.get("subjectTextSha256") for r in rs}
        value = {"dimension": dim, "codebookVersion": cbv, "raterTypes": types,
                 "nHumanRaters": len({r.get("raterId") for r in human}), "humanConsensus": bool(human) and len(prints) == 1,
                 "textSha256": next(iter(hashes)) if len(hashes) == 1 else None, "held": False}
        result = by_dim.get((dim, cbv))
        d = gm.decide(value, result, gates, view_tier, _current_hash(target)) if gm else {"render": False, "label": "engine_unavailable", "reason": ""}
        rows.append({"recordId": u, "field": dim, "codebookVersion": cbv, "decision": _decision(d), "label": d.get("label"),
                     "reason": d.get("reason"), "studyId": (result or {}).get("studyId"), "nRatings": len(rs), **stamp})
    for rid, r in sorted(released.items()):
        if r.get("type") == "Task" and r.get("workFunction"):
            rt = PROVENANCE_RATER.get((r.get("provenance") or {}).get("method"), "analyst")
            value = {"dimension": "Task.workFunction", "codebookVersion": None, "raterTypes": [rt],
                     "nHumanRaters": 0 if rt != "analyst" else 1, "humanConsensus": False, "textSha256": r.get("textSha256"), "held": False}
            d = gm.decide(value, by_dim.get(("Task.workFunction", None)), gates, view_tier, r.get("textSha256")) if gm else {"render": False, "label": "engine_unavailable"}
            rows.append({"recordId": rid, "field": "Task.workFunction", "codebookVersion": None, "decision": _decision(d),
                         "label": d.get("label"), "reason": d.get("reason"), "studyId": None, "nRatings": 0, **stamp})
    return {"header": header, "rows": rows}
