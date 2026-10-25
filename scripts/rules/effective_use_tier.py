"""effective-use-tier@1.1.0 (vocab/rules/effective-use-tier@1.1.0.yaml; ADR-0015, ADR-0024, ADR-0029 §4.5, ADR-0032).

Effective tier = the minimum of the declared ceiling and the caps:
  lifecycle     1.1.0: NOT a cap (lifecycle describes the work, validationStatus the record; ADR-0032, review M7).
                withdrawn/lapsed/merged records still have no tier (the record is not current); `caps.lifecycle` is
                reported as null for every other state
  evidence      validationStatus ladder; a Competency at select also needs ≥ 1 linked critical task in a role variant
                at ≥ job-analysis-confirmed
  levelRule     Competency: highest tier whose IO tier_requirements hold at EVERY published level (none → describe);
                Indicator: its useClass, no higher than its competency's levelRule cap
  indicatorLint Indicator with an unwaived lint flag → develop
  pathway       Pathway → exploratory until the M-03 gate
Reliability is not a record cap: display-gate@1.0.0 decides per value (the tier never rises because a tag is shown).
Fail closed: a missing input yields the lower tier.
"""
from __future__ import annotations

TYPES = ("Competency", "Task", "Indicator", "RoleProfile", "RoleVariant", "KnowledgeStatement", "Enactment", "Pathway")
TIER_ORDER = ["exploratory", "describe", "develop", "select"]
LIFECYCLE_CAP = {"watch": "exploratory", "proposed": "exploratory", "emerging": "develop", "established": "select",
                 "declining": "select", "withdrawn": None, "lapsed": None, "merged": None}    # 1.0.0, kept for reference
NOT_CURRENT = {"withdrawn", "lapsed", "merged"}                                          # 1.1.0: no tier
NO_TIER = object()
EVIDENCE_CAP = {"seed-v1": "exploratory", "draft": "describe", "reviewed": "describe", "panel-retained": "develop",
                "job-analysis-confirmed": "select", "criterion-supported": "select"}
VALIDATION_ORDER = ["seed-v1", "draft", "reviewed", "panel-retained", "job-analysis-confirmed", "criterion-supported"]
PR_KEYS = {"PR-1": "existence", "PR-2": "distinctness", "PR-3": "assessability", "PR-4": "consensus"}
CAP_ORDER = ["declaredCeiling", "lifecycle", "evidence", "levelRule", "indicatorLint", "pathway"]
# every record field this rule reads (tests assert that v1 prior evidence is never an input)
INPUT_FIELDS = {
    "*": ["type", "useTier", "lifecycleState", "validationStatus"],
    "Competency": ["levels.level", "levels.indicators", "levels.publicationRuleChecks"],
    "Indicator": ["competency", "level", "useClass", "obs4"],
    "Task": ["supports.competency"],
    "RoleProfile": ["taskBundle.task", "taskBundle.critical"],
    "RoleVariant": ["variantOf", "validationStatus", "taskAdds", "taskDrops", "taskOverrides"],
}


def _min(tiers):
    return min(tiers, key=TIER_ORDER.index)


def _result(check):
    if isinstance(check, dict):
        return check.get("result") or "pending"
    return check or "pending"


def _at_least(status, floor):
    return status in VALIDATION_ORDER and VALIDATION_ORDER.index(status) >= VALIDATION_ORDER.index(floor)


def critical_tasks_in_confirmed_variants(released: dict) -> set:
    """Tasks marked critical in a released role variant at validationStatus ≥ job-analysis-confirmed."""
    out = set()
    for rid, v in released.items():
        if v.get("type") != "RoleVariant" or not _at_least(v.get("validationStatus"), "job-analysis-confirmed"):
            continue
        prof = released.get(v.get("variantOf")) or {}
        bundle = {b["task"]: dict(b) for b in prof.get("taskBundle") or [] if isinstance(b, dict) and b.get("task")}
        for t in v.get("taskDrops") or []:
            bundle.pop(t, None)
        for b in (v.get("taskAdds") or []) + (v.get("taskOverrides") or []):
            if isinstance(b, dict) and b.get("task"):
                bundle[b["task"]] = {**bundle.get(b["task"], {}), **b}
        out.update(t for t, b in bundle.items() if b.get("critical") is True)
    return out


def level_rule_cap(comp: dict, released: dict, tier_requirements: dict) -> str:
    levels = [lv for lv in comp.get("levels") or [] if isinstance(lv, dict)]
    if not levels:
        return "describe"
    for tier in reversed(TIER_ORDER[1:]):                       # select, develop, describe
        req = tier_requirements.get(tier) or {}
        ok = True
        for lv in levels:
            checks = lv.get("publicationRuleChecks") or {}
            for pr, key in PR_KEYS.items():
                if _result(checks.get(key)) not in (req.get(pr) or []):
                    ok = False
            floor = req.get("indicator_obs4_min")
            inds = [released.get(i) for i in lv.get("indicators") or []]
            if floor is not None and (not inds or any(not isinstance(i, dict) or not isinstance(i.get("obs4"), int)
                                                      or i["obs4"] < floor for i in inds)):
                ok = False
            if not ok:
                break
        if ok:
            return tier
    return "exploratory"


def compute(released: dict, tier_requirements: dict, lint: dict | None, stamp: dict) -> list[dict]:
    """lint: {record_id: [open hits]} from IO's linter, or None when unavailable (then every Indicator caps at develop)."""
    critical = critical_tasks_in_confirmed_variants(released)
    comp_has_critical = set()
    for rid, t in released.items():
        if t.get("type") == "Task" and rid in critical:
            comp_has_critical.update(s.get("competency") for s in t.get("supports") or [] if isinstance(s, dict))
    comp_cap = {rid: level_rule_cap(r, released, tier_requirements) for rid, r in released.items() if r.get("type") == "Competency"}
    rows = []
    for rid, r in sorted(released.items()):
        typ = r.get("type")
        if typ not in TYPES:
            continue
        declared = r.get("useTier") or "exploratory"
        caps = {}
        lc = r.get("lifecycleState")
        caps["lifecycle"] = None                       # 1.1.0: lifecycle never caps the tier (ADR-0032)
        no_tier = lc in NOT_CURRENT
        ev = EVIDENCE_CAP.get(r.get("validationStatus"), "exploratory")
        if typ == "Competency" and ev == "select" and rid not in comp_has_critical:
            ev = "develop"
        caps["evidence"] = ev
        if typ == "Competency":
            caps["levelRule"] = comp_cap[rid]
        elif typ == "Indicator":
            own = r.get("useClass") if r.get("useClass") in TIER_ORDER else "exploratory"
            caps["levelRule"] = _min([own, comp_cap.get(r.get("competency"), "exploratory")])
            caps["indicatorLint"] = "develop" if (lint is None or lint.get(rid)) else "select"
        if typ == "Pathway":
            caps["pathway"] = "exploratory"
        if no_tier:
            eff, binding = None, "notCurrent"
        else:
            values = {"declaredCeiling": declared, **{k: v for k, v in caps.items() if v is not None}}
            eff = _min(values.values())
            binding = next(k for k in CAP_ORDER if values.get(k) == eff)
        rows.append({"id": rid, "type": typ, "effectiveUseTier": eff, "declaredCeiling": declared,
                     "caps": caps, "bindingCap": binding, **stamp})
    return rows
