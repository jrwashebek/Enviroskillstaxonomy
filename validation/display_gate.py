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
Returns  : {render: bool, marker: production|tentative|editorial|pending|hidden|drawer-only|not-rendered, label: str|None, reason: str}

display-gate@1.1.0 adds role-profile bundle values (CR-CP-001 B4): pass {field: 'RoleProfile.<path>', validationStatus,
reviewers[]} and a `context` (role | pathway | gap-check | federal-series-profile | state-class-view | catalogue | select);
decide() routes them to decide_role_value(). Editorial design values render marker 'editorial' with an editorial label;
job-analysis values render 'pending' until a pid: reviewer and validationStatus >= reviewed (FSP/SCV % time and
importance only from job-analysis-confirmed). Labels resolve in display_gates.yaml#role_profile_values.role_labels.

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


def _role_fields(gates: dict) -> tuple[set, set]:
    rp = gates.get("role_profile_values") or {}
    return (set((rp.get("editorial_design_values") or {}).get("fields") or []),
            set((rp.get("job_analysis_values") or {}).get("fields") or []))


def _human_reviewed(value: dict, rp: dict) -> bool:
    prefix = rp.get("human_reviewer_prefix", "pid:")
    revs = value.get("reviewers") or []
    if isinstance(revs, str):
        revs = [revs]
    revs = list(revs) + ([value["reviewedBy"]] if value.get("reviewedBy") else [])
    return any(isinstance(r, str) and r.startswith(prefix) for r in revs)


def _status_at_least(value: dict, minimum: str, rp: dict) -> bool:
    order = rp["status_order"]
    st = value.get("validationStatus")
    return st in order and order.index(st) >= order.index(minimum)


def decide_role_value(value: dict, gates: dict, view_tier: str = "describe", context: str = "role") -> dict:
    """display-gate@1.1.0 for RoleProfile bundle values (CR-CP-001 B4).

    value: {field (e.g. 'RoleProfile.taskBundle.timeShare'), validationStatus, reviewers[] or reviewedBy, held}
    context: role | pathway | gap-check | federal-series-profile | state-class-view | catalogue | select
    Returns the same shape as decide(); marker 'editorial' when rendered (human review, not alpha), 'pending'
    for job-analysis values awaiting review, 'hidden' otherwise. Fail closed on anything unknown.
    """
    def out(render, marker, label, reason=""):
        return {"render": render, "marker": marker, "label": label, "reason": reason or (label or "")}

    rp = gates.get("role_profile_values")
    if not rp:
        return out(False, "hidden", None, "gates file has no role_profile_values (fail closed)")
    if value.get("held"):
        return out(False, "not-rendered", None, "held content (ADR-0007)")
    if context not in rp["contexts"] or view_tier not in gates["use_tier_admission"]:
        return out(False, "hidden", None, f"unknown context {context!r} or view tier {view_tier!r} (fail closed)")
    editorial, job = _role_fields(gates)
    field = value.get("field")
    reviewed = _human_reviewed(value, rp) and _status_at_least(value, "reviewed", rp)
    is_select = context == "select" or view_tier == "select"
    if field in editorial:
        ed = rp["editorial_design_values"]
        if is_select or context in ed.get("never_in_contexts", []):
            return out(False, "hidden", None, "editorial design values never render in a select context")
        branch = ed["reviewed"] if reviewed else ed["unreviewed"]
        if view_tier not in branch["view_tiers"]:
            return out(False, "hidden", branch["label"], f"{branch['label']} not admitted in a {view_tier} view")
        return out(True, ed["marker"], branch["label"])
    if field in job:
        ja = rp["job_analysis_values"]
        if not reviewed:
            return out(False, "pending", ja["pending_label"], "agent-drafted or unreviewed job-analysis value")
        hr = ja["hr_classification_min_status"]
        if context in rp["hr_classification_contexts"] and field in hr["fields"] and not _status_at_least(value, hr["min_status"], rp):
            return out(False, "pending", hr["pending_label"], f"{field} renders in HR classification views only from {hr['min_status']}")
        if is_select and not _status_at_least(value, ja["select_min_status"], rp):
            return out(False, "hidden", ja["pending_label"], f"select contexts need {ja['select_min_status']}")
        return out(True, ja["marker"], ja["status_labels"].get(value.get("validationStatus"), "status_reviewed"))
    return out(False, "hidden", None, f"unknown role-profile field {field!r} (fail closed)")


def decide(value: dict, result: dict | None, gates: dict, view_tier: str = "describe",
           current_text_sha256: str | None = None, context: str = "role") -> dict:
    def out(render, marker, label, reason=""):
        return {"render": render, "marker": marker, "label": label, "reason": reason or (label or "")}

    editorial, job = _role_fields(gates)
    if value.get("field") in editorial | job or str(value.get("field") or "").startswith("RoleProfile."):
        return decide_role_value(value, gates, view_tier, context)
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
