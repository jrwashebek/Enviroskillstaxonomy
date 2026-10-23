#!/usr/bin/env python3
"""EMST v2 display-gate reference evaluator (WP-11). Applies validation/display_gates.yaml.

The build (DE, WP-01) computes one agreement result per dimension and codebook version from stored atomic
ratings (validation/reliability.py) and calls `decide()` for every rated value it would put in a view; the
explorer (CP, WP-12) renders only values whose decision says `render: True`, and otherwise prints the label.

    from display_gate import load_gates, decide
    d = decide(value, result, gates, view_tier="describe", current_text_sha256=task_hash)

`value`  : {dimension, codebookVersion, raterTypes[], nHumanRaters, humanConsensus (bool), textSha256,
            stratum {key: value}, held (bool), llmGatePassed (bool), decisionPath}
`result` : agreement result as in display_gates.yaml#agreement_result_schema, or None.
Returns  : {render: bool, marker: production|tentative|hidden|drawer-only|not-rendered, label: str|None, reason: str}

Fail closed: anything missing or malformed yields render False.
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import yaml

HERE = Path(__file__).resolve().parent
DEFAULT_GATES = HERE / "display_gates.yaml"
ORDER = {"hidden": 0, "tentative": 1, "production": 2}


def load_gates(path: Path = DEFAULT_GATES) -> dict:
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _num(x: Any) -> float | None:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(v) else v


def marker_for_lower_bound(lb: float | None, gates: dict) -> str:
    th = gates["thresholds"]
    if lb is None:
        return "hidden"
    if lb >= th["production_min_lower_bound"]:
        return "production"
    if lb >= th["tentative_min_lower_bound"]:
        return "tentative"
    return "hidden"


def admissible(result: dict | None, gates: dict) -> tuple[bool, str]:
    """Is an agreement result admissible evidence for the gate? Returns (ok, reason)."""
    if not result:
        return False, "assessment_pending"
    adm = gates["admissibility"]
    req = gates["agreement_result_schema"]["required"]
    missing = [k for k in req if result.get(k) in (None, "")]
    if missing:
        return False, "insufficient_study"
    counted = set(result.get("raterTypesCounted") or [])
    if not counted or counted - set(adm["rater_types_counted"]) or counted & set(adm["rater_types_never_counted"]):
        return False, "insufficient_study"
    if (_num(result.get("nUnits")) or 0) < adm["min_units"]:
        return False, "insufficient_study"
    if (_num(result.get("nDistinctRaters")) or 0) < adm["min_distinct_raters"]:
        return False, "insufficient_study"
    if (_num(result.get("bootstrapResamples")) or 0) < gates["thresholds"]["ci"]["resamples_min"]:
        return False, "insufficient_study"
    if adm.get("blind_coding_attested") and result.get("blindCodingAttested") is not True:
        return False, "insufficient_study"
    if adm.get("preregistration_id_required") and not str(result.get("preregistrationId") or "").strip():
        return False, "insufficient_study"
    return True, ""


def dimension_marker(result: dict | None, gates: dict, stratum: dict | None = None) -> tuple[str, str]:
    ok, reason = admissible(result, gates)
    if not ok:
        return "hidden", reason
    overall = marker_for_lower_bound(_num(result.get("ciLower")), gates)
    if overall == "hidden":
        return "hidden", "below_gate"
    note = ""
    if stratum:
        min_n = gates["strata"]["separate_estimate_min_units"]
        for key, val in stratum.items():
            match = [s for s in (result.get("strata") or []) if s.get("key") == key and s.get("value") == val]
            if match and (_num(match[0].get("nUnits")) or 0) >= min_n:
                sm = marker_for_lower_bound(_num(match[0].get("ciLower")), gates)
                if sm == "hidden":
                    return "hidden", "below_gate"
                if ORDER[sm] < ORDER[overall]:
                    overall = sm
            else:
                note = "stratum_not_estimated"
    return overall, note


def decide(value: dict, result: dict | None, gates: dict, view_tier: str = "describe",
           current_text_sha256: str | None = None) -> dict:
    def out(render, marker, label, reason=""):
        return {"render": render, "marker": marker, "label": label, "reason": reason or (label or "")}

    if value.get("held"):
        return out(False, "not-rendered", None, "held content (ADR-0007)")
    rater_types = set(value.get("raterTypes") or [])
    human = set(gates["admissibility"]["rater_types_counted"])
    if rater_types == {"v1-analyst"}:
        return out(False, "drawer-only", "v1_prior", "v1 prior evidence only")
    if rater_types == {"external-index"}:
        return out(False, "hidden", "external_context", "external context is rendered by the external-context component, never as a tag")
    if not (rater_types & human):
        return out(False, "hidden", "assessment_pending", "no human rater behind this value")
    if "llm" in rater_types and not value.get("llmGatePassed"):
        return out(False, "hidden", "assessment_pending", "LLM-first value without a passed LLM-coder gate")
    if current_text_sha256 is None or value.get("textSha256") != current_text_sha256:
        return out(False, "hidden", "stale")
    if not result or value.get("dimension") != result.get("dimension"):
        return out(False, "hidden", "assessment_pending")
    if value.get("codebookVersion") != result.get("codebookVersion"):
        return out(False, "hidden", "assessment_pending", "codebook version mismatch")
    marker, note = dimension_marker(result, gates, value.get("stratum"))
    if marker == "hidden":
        return out(False, "hidden", note or "below_gate")
    cat_rule = gates.get("categories") or {}
    if cat_rule and value.get("category") is not None:
        for pc in result.get("perCategory") or []:
            if str(pc.get("category")) == str(value.get("category")) and (_num(pc.get("nUnits")) or 0) >= cat_rule["min_units"]:
                a = _num(pc.get("alpha"))
                if a is None or a < cat_rule["cap_below_point_alpha"]:
                    marker = "tentative" if marker == "production" else marker
    n_h = int(_num(value.get("nHumanRaters")) or 0)
    if not value.get("humanConsensus"):
        return out(False, "hidden", "no_consensus")
    if marker == "production" and n_h < 3:
        marker = "tentative"          # production values need a >= 3-rater human consensus
    if marker == "tentative" and n_h < 2:
        return out(False, "hidden", "no_consensus")
    if marker not in gates["use_tier_admission"].get(view_tier, []):
        return out(False, "hidden", "below_gate", f"{marker} not admitted in a {view_tier} view")
    label = "tentative" if marker == "tentative" else (note or None)
    return out(True, marker, label, note)


def rollup(markers: list[str], weights: list[float], gates: dict, min_mass: float = 0.80) -> dict:
    """Role or competency roll-up: renders when renderable task values carry >= min_mass of the weight."""
    total = sum(weights)
    if total <= 0 or len(markers) != len(weights):
        return {"render": False, "marker": "hidden", "label": "insufficient_coverage"}
    mass = sum(w for m, w in zip(markers, weights) if m in ("production", "tentative")) / total
    if mass < min_mass:
        return {"render": False, "marker": "hidden", "label": "insufficient_coverage", "coverage": mass}
    shown = [m for m in markers if m in ("production", "tentative")]
    marker = min(shown, key=lambda m: ORDER[m])
    return {"render": True, "marker": marker, "label": "tentative" if marker == "tentative" else None,
            "coverage": mass, "k": len(shown), "n": len(markers)}
