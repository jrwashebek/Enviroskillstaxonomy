#!/usr/bin/env python3
"""The `agentDraft` envelope of the JSON-LD release bundle (rc.1 fix pass, finding M1; DATA_FIX_BRIEF §1).

Source records store agent-drafted values in place (for example `RoleProfile.taskBundle[].timeShare`). The release
bundle must not present them as job-analysis output, so the build moves every value that `validation/display_gates.yaml`
gates, and that the gate does not render, into a sub-object named `agentDraft` on the same host, together with the
rater type, the record's `validationStatus` and the display-gate label:

    {"task": "emst:air/TSK-…", "formationTask": false, "roleLevels": [...],
     "agentDraft": {"importance": 5, "timeShare": 0.055, "critical": true, "neededAtEntry": true,
                    "raterType": "llm", "validationStatus": "draft", "displayGate": "Assessment pending (job analysis)."}}

Hosts and fields (each one is gated in validation/display_gates.yaml; tests/test_agent_draft.py checks that):
  RoleProfile.taskBundle[]          role_profile_values.job_analysis_values.fields (RoleProfile.taskBundle.*)
  RoleProfile.competencyTargets[]   role_profile_values.job_analysis_values.fields (RoleProfile.competencyTargets.*)
  Task                              the task-level copies of gated rating dimensions (TASK_FIELDS below)
  Indicator                         obs4 and the agents' self-code obs4Draft (dimension indicator.obs4)

L5 rating records (CraftRating, ExposureAssessment, FunctionRating, RelevanceRating) are not hosts: the whole record
is the rating, and its own raterType, validationStatus and evidence label describe every value in it.

`scripts/build_schema.py` generates the matching schema (one AgentDraft<Host> $def per host, an `agentDraft` property
on each host, and "value in place, or agentDraft" wherever a host requires a moved field). `agentDraft` is a computed
field: it never appears in a source record (schema/lint/computed_fields.yaml). In JSON-LD it is an `@json` literal,
so an RDF consumer never reads an agent draft as an asserted EMST property.
Licence: Apache-2.0.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emstlib as L  # noqa: E402

GATES_FILE = L.ROOT / "validation" / "display_gates.yaml"
FIELD = "agentDraft"

# Task-level copies of rating dimensions gated in display_gates.yaml#dimensions (field -> dimension ids).
TASK_FIELDS = {
    "workFunction": ["task.workFunction"],
    "fieldDependency": ["task.fieldDependency"],
    "formationDependency": ["task.formationDependency"],
    "modes": ["task.mode.engage", "task.mode.resolve"],
    "relationshipTypes": ["task.mode.engage.relationshipType"],
    "reproductionRegime.mentorshipDependence": ["task.reproductionRegime.mentorshipDependence"],
    "reproductionRegime.cycleDependence": ["task.reproductionRegime.cycleDependence"],
    "reproductionRegime.placeBoundness": ["task.reproductionRegime.placeBoundness"],
    "reproductionRegime.currencyDecay": ["task.reproductionRegime.currencyDecay"],
}
INDICATOR_FIELDS = {"obs4": ["indicator.obs4"], "obs4Draft": ["indicator.obs4"]}   # obs4Draft: the agents' self-code (m8)
# rater type of a value from the host record's provenance method (same mapping as scripts/rules/gated_values.py)
PROVENANCE_RATER = {"llm-assisted": "llm", "v1-migration": "v1-analyst", "lexical-linker": "llm"}
RENDERED = {"production", "tentative", "editorial"}


def load_gates(path: Path = GATES_FILE) -> dict:
    return L.load_yaml(path) if Path(path).exists() else {}


def hosts(gates: dict | None = None) -> list[dict]:
    """[{type, prop, defName, fields: [dotted field], gateField: {field: display-gate field id}, label}] per host."""
    gates = load_gates() if gates is None else gates
    rp = (gates.get("role_profile_values") or {})
    ja = rp.get("job_analysis_values") or {}
    labels = {**(gates.get("labels") or {}), **(rp.get("role_labels") or {})}
    ja_label = labels.get(ja.get("pending_label") or "assessment_pending_job_analysis", "Assessment pending (job analysis).")
    pending = labels.get("assessment_pending", "Assessment pending: no multi-rater v2 assessment of this value yet.")
    by_prop: dict[str, list[str]] = {}
    for f in ja.get("fields") or []:
        t, prop, field = f.split(".", 2)
        if t == "RoleProfile":
            by_prop.setdefault(prop, []).append(field)
    out = []
    for prop, def_name in (("taskBundle", "AgentDraftTaskBundleItem"), ("competencyTargets", "AgentDraftCompetencyTarget")):
        if by_prop.get(prop):
            out.append({"type": "RoleProfile", "prop": prop, "defName": def_name, "fields": by_prop[prop],
                        "gateField": {f: f"RoleProfile.{prop}.{f}" for f in by_prop[prop]}, "label": ja_label})
    out.append({"type": "Task", "prop": None, "defName": "AgentDraftTask", "fields": list(TASK_FIELDS),
                "gateField": {"workFunction": "Task.workFunction"}, "label": pending})
    out.append({"type": "Indicator", "prop": None, "defName": "AgentDraftIndicator", "fields": list(INDICATOR_FIELDS),
                "gateField": {}, "label": pending})
    return out


def label_texts(gates: dict | None = None) -> dict:
    gates = load_gates() if gates is None else gates
    return {**(gates.get("labels") or {}), **((gates.get("role_profile_values") or {}).get("role_labels") or {})}


def rater_type(rec: dict) -> str:
    return PROVENANCE_RATER.get((rec.get("provenance") or {}).get("method"), "analyst")


def _take(obj: dict, dotted: str):
    """Remove obj[a][b] for dotted 'a.b' (or obj[a]); return (found, value). Empty parents are removed."""
    parts = dotted.split(".")
    if len(parts) == 1:
        if parts[0] in obj and obj[parts[0]] is not None:
            return True, obj.pop(parts[0])
        return False, None
    parent = obj.get(parts[0])
    if not isinstance(parent, dict) or parts[1] not in parent or parent[parts[1]] is None:
        return False, None
    v = parent.pop(parts[1])
    if not parent:
        obj.pop(parts[0])
    return True, v


def _put(obj: dict, dotted: str, v) -> None:
    parts = dotted.split(".")
    if len(parts) == 1:
        obj[parts[0]] = v
    else:
        obj.setdefault(parts[0], {})[parts[1]] = v


class Envelope:
    """Moves gated, unrendered values into `agentDraft`. `decisions` maps (recordId, gate field) -> (decision, label key)
    from views/display_gate.json (role context for role-profile values); a value with no decision is not rendered
    (fail closed)."""

    def __init__(self, decisions: dict | None = None, gates: dict | None = None):
        self.gates = load_gates() if gates is None else gates
        self.hosts = {(h["type"], h["prop"]): h for h in hosts(self.gates)}
        self.labels = label_texts(self.gates)
        self.decisions = decisions or {}
        self.moved = 0                     # values moved, for the release notes

    @classmethod
    def from_display_gate(cls, view: dict, gates: dict | None = None):
        dec = {}
        for r in (view or {}).get("rows") or []:
            ctx = r.get("context")
            if ctx not in (None, "role"):
                continue
            dec[(r.get("recordId"), r.get("field"))] = (r.get("decision"), r.get("label"))
        return cls(dec, gates)

    def _envelope(self, rec: dict, target: dict, host: dict) -> dict:
        rid = rec.get("id")
        draft = {}
        label = host["label"]
        for f in host["fields"]:
            gf = host["gateField"].get(f)
            decision, lab = self.decisions.get((rid, gf), (None, None)) if gf else (None, None)
            if decision in RENDERED:
                continue                                    # the gate shows it: the value stays in place
            found, v = _take(target, f)
            if found:
                _put(draft, f, v)
                self.moved += 1
                if lab and lab in self.labels:
                    label = self.labels[lab]
        if not draft:
            return target
        target[FIELD] = {**draft, "raterType": rater_type(rec), "validationStatus": rec.get("validationStatus"),
                         "displayGate": label}
        return target

    def apply(self, rec: dict) -> dict:
        t = rec.get("type")
        if not any(k[0] == t for k in self.hosts):
            return rec
        out = copy.deepcopy(rec)
        top = self.hosts.get((t, None))
        if top:
            self._envelope(out, out, top)
        for (ht, prop), host in self.hosts.items():
            if ht != t or prop is None:
                continue
            items = out.get(prop)
            if isinstance(items, list):
                out[prop] = [self._envelope(out, it, host) if isinstance(it, dict) else it for it in items]
        return out


def fold(rec: dict) -> dict:
    """Inverse of Envelope.apply: put agentDraft values back in place (used by tests and round-trip checks)."""
    out = copy.deepcopy(rec)

    def back(obj):
        d = obj.pop(FIELD, None)
        if not isinstance(d, dict):
            return
        for k, v in d.items():
            if k in ("raterType", "validationStatus", "displayGate"):
                continue
            if isinstance(v, dict) and k == "reproductionRegime":
                obj.setdefault(k, {}).update(v)
            else:
                obj[k] = v
    back(out)
    for v in out.values():
        if isinstance(v, list):
            for it in v:
                if isinstance(it, dict):
                    back(it)
    return out


# ---------------------------------------------------------------------------------------------------------- schema
def _resolve(defs: dict, node: dict) -> dict:
    while isinstance(node, dict) and "$ref" in node and node["$ref"].startswith("#/$defs/"):
        node = defs[node["$ref"].split("/")[-1]]
    return node


def _props_node(defs: dict, start: dict, names: set) -> dict | None:
    """The schema node whose `properties` declares the host's fields (start, or an allOf/$ref it uses)."""
    todo, seen = [start], []
    while todo:
        n = _resolve(defs, todo.pop(0))
        if not isinstance(n, dict) or any(n is s for s in seen):
            continue
        seen.append(n)
        if names & set((n.get("properties") or {})):
            return n
        todo += [x for x in n.get("allOf") or [] if isinstance(x, dict)]
    return None


def _relax_required(node, names: set, local_defs: dict, depth=0):
    """Wherever `required` lists a moved field (in this node, its allOf branches, if/then/else, or a $ref used only
    here), replace the moved names by 'all of them in place, or agentDraft'."""
    if depth > 6 or not isinstance(node, dict):
        return
    req = node.get("required")
    if isinstance(req, list) and names & set(req):
        moved = [r for r in req if r in names]
        node["required"] = [r for r in req if r not in names]
        if not node["required"]:
            node.pop("required")
        node.setdefault("allOf", []).append({"anyOf": [{"required": moved}, {"required": [FIELD]}]})
    for key in ("then", "else"):
        _relax_required(node.get(key), names, local_defs, depth + 1)
    for sub in list(node.get("allOf") or []):
        _relax_required(sub, names, local_defs, depth + 1)


def _field_schema(defs: dict, props: dict, dotted: str):
    parts = dotted.split(".")
    s = props.get(parts[0])
    if len(parts) == 1:
        return s
    s = _resolve(defs, s or {})
    return ((s or {}).get("properties") or {}).get(parts[1])


def add_to_schema(defs: dict, gates: dict | None = None) -> list[str]:
    """Add AgentDraft<Host> defs and `agentDraft` host properties to `defs` in place. Returns the def names added.
    Hosts or fields that the source schema does not declare are skipped (the generator follows `src`)."""
    added = []
    for h in hosts(gates):
        tdef = defs.get(h["type"])
        if not tdef:
            continue
        start = tdef
        if h["prop"]:
            p = (tdef.get("properties") or {}).get(h["prop"])
            if not isinstance(p, dict) or not isinstance(p.get("items"), dict):
                continue
            start = p["items"]
        top = {f.split(".")[0] for f in h["fields"]}
        pn = _props_node(defs, start, top)
        if pn is None:
            continue
        props = pn["properties"]
        draft_props, nested = {}, {}
        for f in h["fields"]:
            fs = _field_schema(defs, props, f)
            if fs is None:
                continue
            if "." in f:
                nested.setdefault(f.split(".")[0], {})[f.split(".")[1]] = copy.deepcopy(fs)
            else:
                draft_props[f] = copy.deepcopy(fs)
        for parent, sub in nested.items():
            draft_props[parent] = {"type": "object", "additionalProperties": False, "minProperties": 1, "properties": sub}
        if not draft_props:
            continue
        defs[h["defName"]] = {
            "type": "object", "additionalProperties": False,
            "description": (f"Agent-drafted values of a {h['type']}{'.' + h['prop'] + '[]' if h['prop'] else ''} that the display "
                            "gate does not render, moved here in the release bundle (rc.1 fix pass M1; scripts/agent_draft.py). "
                            "Never present in a source record."),
            "required": ["raterType", "validationStatus", "displayGate"], "minProperties": 4,
            "properties": {**draft_props, "raterType": {"$ref": "#/$defs/v_raterType"},
                           "validationStatus": {"$ref": "#/$defs/v_validationStatus"},
                           "displayGate": {"type": "string", "minLength": 1}},
            "$comment": "GENERATED by scripts/build_schema.py from validation/display_gates.yaml (scripts/agent_draft.py)"}
        props[FIELD] = {"$ref": f"#/$defs/{h['defName']}"}
        _relax_required(start if h["prop"] else tdef, top, defs)
        if pn is not start and pn is not tdef:
            _relax_required(pn, top, defs)
        added.append(h["defName"])
    return added
