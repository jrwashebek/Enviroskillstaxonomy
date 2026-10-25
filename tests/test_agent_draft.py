"""rc.1 fix pass M1 (DATA_FIX_BRIEF §1): display-gated agent drafts sit only in `agentDraft` in the bundle and appear in
no CSV or HCM export; the generated schema accepts exactly that shape."""
from __future__ import annotations

import copy
import csv
import io
import json

import jsonschema
import pytest

from conftest import FIXTURES, L, overlay_tree

import agent_draft
import build_release

TASK = "emst:core/TSK-EF34GHP"
CMP = "emst:core/CMP-AB12CDN"


def _role(**kw):
    r = L.load_yaml(FIXTURES / "records" / "valid" / "RoleProfile.yaml")
    r["taskBundle"][0]["task"] = TASK
    r["competencyTargets"][0].update(competency=CMP, importance=4, distinguishing=True, criticalForSelection=False)
    r.update(kw)
    return r


def _schema():
    return json.loads(L.SCHEMA_OUT.read_text(encoding="utf-8"))


def test_every_moved_field_is_gated_in_display_gates():
    gates = agent_draft.load_gates()
    ja = set(gates["role_profile_values"]["job_analysis_values"]["fields"])
    dims = {d["id"] for d in gates["dimensions"]}
    hosts = agent_draft.hosts(gates)
    for h in hosts:
        if h["type"] == "RoleProfile":
            assert {f"RoleProfile.{h['prop']}.{f}" for f in h["fields"]} <= ja
    for ids in list(agent_draft.TASK_FIELDS.values()) + list(agent_draft.INDICATOR_FIELDS.values()):
        assert set(ids) <= dims, ids
    covered = {f"RoleProfile.{h['prop']}.{f}" for h in hosts if h["type"] == "RoleProfile" for f in h["fields"]}
    assert covered == ja                                   # every job-analysis value has a host


def test_envelope_moves_unrendered_values_and_fold_restores_them():
    role = _role()
    env = agent_draft.Envelope()
    out = env.apply(role)
    item, target = out["taskBundle"][0], out["competencyTargets"][0]
    assert not {"importance", "timeShare", "critical", "neededAtEntry"} & set(item)
    assert item["agentDraft"] == {"importance": 5, "timeShare": 0.4, "critical": True, "neededAtEntry": True,
                                  "raterType": "analyst", "validationStatus": "draft",
                                  "displayGate": "Assessment pending (job analysis)."}
    assert item["task"] == TASK and "formationTask" not in item["agentDraft"]       # editorial values stay in place
    assert target["agentDraft"]["importance"] == 4 and "importance" not in target
    assert target["targetLevels"] == {"entry": "L1"}
    assert agent_draft.fold(out) == role and role["taskBundle"][0]["importance"] == 5   # source untouched
    task = L.load_yaml(FIXTURES / "trees" / "base" / "data" / "v2" / "core" / "tasks" / "TSK-EF34GHP.yaml")
    task["reproductionRegime"] = {"mentorshipDependence": "H", "credentialGate": "none"}
    t = env.apply(task)
    assert t["agentDraft"]["workFunction"] == "WF-ASSESS" and "workFunction" not in t
    assert t["agentDraft"]["reproductionRegime"] == {"mentorshipDependence": "H"}
    assert t["reproductionRegime"] == {"credentialGate": "none"}                    # not gated: stays
    assert agent_draft.fold(t) == task


def test_a_value_the_gate_renders_stays_in_place():
    role = _role(id="seed:fx-rol")
    env = agent_draft.Envelope({("seed:fx-rol", "RoleProfile.taskBundle.timeShare"): ("editorial", "status_reviewed")})
    item = env.apply(role)["taskBundle"][0]
    assert item["timeShare"] == 0.4 and "timeShare" not in item["agentDraft"] and item["agentDraft"]["importance"] == 5


def test_generated_schema_accepts_the_bundle_shape_only():
    v = jsonschema.Draft202012Validator(_schema())
    role = _role()
    assert not list(v.iter_errors(role))                                           # source form
    bundle_form = agent_draft.Envelope().apply(role)
    assert not list(v.iter_errors(bundle_form))                                    # bundle form
    bare = copy.deepcopy(bundle_form)
    del bare["taskBundle"][0]["agentDraft"]
    assert list(v.iter_errors(bare))                                               # neither in place nor in agentDraft
    bad = copy.deepcopy(bundle_form)
    bad["taskBundle"][0]["agentDraft"]["rank"] = 1
    assert list(v.iter_errors(bad))                                                # closed envelope
    nolabel = copy.deepcopy(bundle_form)
    del nolabel["taskBundle"][0]["agentDraft"]["displayGate"]
    assert list(v.iter_errors(nolabel))
    cf = L.load_yaml(L.LINT_DIR / "computed_fields.yaml")
    assert "agentDraft" in cf["fields"]                                            # never in a source record


def test_bundle_and_exports_carry_no_gated_value(tmp_path):
    data = overlay_tree(tmp_path / "src")
    (data / "core" / "roles").mkdir(parents=True, exist_ok=True)
    L.write_yaml(data / "core" / "roles" / "seed-fx-rol.yaml", _role())
    b = build_release.Builder(data, profile="preview", version="2.0.0-dev", build_commit="test")
    files = b.build(tmp_path / "out")
    graph = {r.get("id"): r for r in json.loads(files["emst.bundle.jsonld"])["@graph"]}
    item = graph["seed:fx-rol"]["taskBundle"][0]
    assert item["agentDraft"]["timeShare"] == 0.4 and "timeShare" not in item
    assert graph[TASK]["agentDraft"]["fieldDependency"] == "on-site-required" and "fieldDependency" not in graph[TASK]
    manifest = graph["https://w3id.org/emst/release/2.0.0-dev"]
    assert "agentDraft" in manifest["notice"] and "IDs are candidate" in manifest["notice"]
    tasks = list(csv.DictReader(io.StringIO(files["csv/tasks.csv"].decode())))
    assert not {"work_function", "field_dependency", "formation_dependency"} & set(tasks[0])
    assert tasks[0]["field_dependency_status"].startswith("Assessment pending")
    assert "on-site-required" not in files["csv/tasks.csv"].decode() and "WF-ASSESS" not in files["csv/tasks.csv"].decode()
    inds = list(csv.DictReader(io.StringIO(files["csv/indicators.csv"].decode())))
    assert "use_class" not in inds[0] and inds[0]["use_class_declared"] and all(r["obs4"] == "" for r in inds)
    assert all(r["effective_use_tier"] for r in inds)
    assert "agentDraft" in files["RELEASE_NOTES.md"].decode() and b.agent_draft_moved > 0


@pytest.mark.parametrize("field", ["importance", "timeShare", "critical", "neededAtEntry"])
def test_hcm_and_csv_headers_never_name_a_job_analysis_value(field):
    snake = "".join("_" + c.lower() if c.isupper() else c for c in field)
    for cols in build_release.Builder.TABLES.values():
        assert snake not in cols and field not in cols
