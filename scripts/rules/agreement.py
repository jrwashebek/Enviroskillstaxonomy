"""Agreement-result emitter for the display gate (ADR-0029 §6.1; validation/display_gates.yaml#agreement_result_schema).

One result per (dimension, codebook version) and study, computed from stored atomic HUMAN ratings with IO's
validation/reliability.py, written to dist/<release>/views/agreement/<studyId>.json. Studies are declared in
data/v2/governance/agreement_studies.yaml (none exist before the S2 reliability studies); without a declaration
nothing is emitted, and every gated value stays 'Assessment pending'. Agent, external-index and v1-analyst ratings
are never counted (display_gates.yaml#admissibility).

Study declaration (one list item per study):
  {studyId, dimension, codebookVersion, metric: nominal|ordinal|interval|ratio, preregistrationId, studyDate,
   blindCodingAttested, valueField: dotted path to the rated value in each rating record, categories: [...] (nominal)}
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import emstlib as L  # noqa: E402
from rules import io_bridge  # noqa: E402

STUDIES_REL = Path("governance") / "agreement_studies.yaml"


def dimension(rec: dict) -> str:
    """The gated dimension a rating belongs to: <type>:<instrument without version>."""
    inst = str(rec.get("instrument") or "unknown").split("@", 1)[0]
    return f"{rec.get('type')}:{inst}"


def unit(rec: dict) -> str | None:
    return rec.get("task") or rec.get("competency") or rec.get("subject") or rec.get("targetId")


def _get(rec, dotted):
    cur = rec
    for part in dotted.split("."):
        if isinstance(cur, list):
            cur = cur[int(part)] if part.isdigit() and int(part) < len(cur) else None
        elif isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return None
    return cur


def human_types(gates: dict) -> set:
    return set(gates["admissibility"]["rater_types_counted"])


def matrix(ratings: list[dict], value_field: str, gates: dict, categories: list | None = None):
    """units x raters matrix (NaN = missing) from human ratings only, plus the unit and rater orders and rater types."""
    humans = human_types(gates)
    keep = [r for r in ratings if r.get("raterType") in humans]
    units = sorted({unit(r) for r in keep if unit(r)})
    raters = sorted({r.get("raterId") for r in keep if r.get("raterId")})
    ui, ri = {u: i for i, u in enumerate(units)}, {r: j for j, r in enumerate(raters)}
    m = [[math.nan] * len(raters) for _ in units]
    for r in keep:
        v = _get(r, value_field)
        if v is None or unit(r) not in ui or r.get("raterId") not in ri:
            continue
        if categories is not None:
            if v not in categories:
                continue
            v = categories.index(v)
        try:
            m[ui[unit(r)]][ri[r["raterId"]]] = float(v)
        except (TypeError, ValueError):
            continue
    return m, units, raters, sorted({r.get("raterType") for r in keep})


def load_studies(data_root: Path) -> list[dict]:
    p = Path(data_root) / STUDIES_REL
    if not p.exists():
        return []
    d = L.load_yaml(p) or {}
    return list(d.get("studies") or [])


def emit(ratings: list[dict], studies: list[dict], stamp: dict, B: int = 10000) -> dict[str, dict]:
    """{studyId: agreement result}. Each result carries every agreement_result_schema field, stamped display-gate."""
    rel = io_bridge.load("reliability")
    gate_mod = io_bridge.load("display_gate")
    if rel is None or gate_mod is None:
        return {}
    gates = gate_mod.load_gates()
    required = gates["agreement_result_schema"]["required"]
    out = {}
    for st in sorted(studies, key=lambda s: s["studyId"]):
        rs = [r for r in ratings if dimension(r) == st["dimension"] and r.get("codebookVersion") == st["codebookVersion"]]
        m, units, raters, types = matrix(rs, st["valueField"], gates, st.get("categories"))
        if not units or len(raters) < 2:
            continue
        res = rel.agreement_result(st["dimension"], st["codebookVersion"], st.get("metric", "nominal"), m, types,
                                   st["preregistrationId"], st["studyId"], str(st["studyDate"]), stamp["buildCommit"],
                                   bool(st.get("blindCodingAttested")), B=B, seed=int(st.get("seed", 20261023)))
        res.update({"ruleId": stamp["ruleId"], "ruleVersion": stamp["ruleVersion"], "buildCommit": stamp["buildCommit"]})
        missing = [k for k in required if k not in res]
        if missing:
            raise ValueError(f"agreement result {st['studyId']} lacks {missing}")
        out[st["studyId"]] = res
    return out
