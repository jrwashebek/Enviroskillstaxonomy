"""WP-01: the release build is deterministic, applies the release gate and produces parseable exports."""
from __future__ import annotations

import json

import pytest

from conftest import FIXTURES, L, overlay_tree

import build_release


def build(data, out, **kw):
    kw.setdefault("build_commit", "test")
    b = build_release.Builder(data, **kw)
    return b, b.build(out)


def test_two_consecutive_builds_are_byte_identical(tmp_path):
    data = overlay_tree(tmp_path / "src")
    _, a = build(data, tmp_path / "a", version="2.0.0-rc.0")
    _, b = build(data, tmp_path / "b", version="2.0.0-rc.0")
    assert sorted(a) == sorted(b)
    for name in a:
        assert a[name] == b[name], name
    assert (tmp_path / "a" / "SHA256SUMS").read_bytes() == (tmp_path / "b" / "SHA256SUMS").read_bytes()


def test_repository_preview_build_is_deterministic(tmp_path):
    import shutil
    snap = tmp_path / "snap"            # other agents write data/v2 concurrently: build from one snapshot
    shutil.copytree(L.DATA_V2, snap)
    kw = dict(profile="preview", version="2.0.0-dev", include_pending_license=True)
    b1, a = build(snap, tmp_path / "a", **kw)
    _, b = build(snap, tmp_path / "b", **kw)
    assert a == b
    bundle = json.loads(a["emst.bundle.jsonld"])
    ids = {r.get("id") for r in bundle["@graph"]}
    for held in ("seed:v1-5.3.2", "seed:v1-6.5.1", "seed:v1-7.1.1", "seed:v1-5.3.2-T1"):
        assert held not in ids
    assert not any("v1Seed" in r for r in bundle["@graph"])
    assert b1.excluded["held (Tribal content hold, ADR-0007 §D)"] > 0


def test_release_profile_excludes_drafts_held_and_pending_licence(tmp_path):
    b, files = build(L.DATA_V2, tmp_path / "r", version="2.0.0-rc.0")
    graph = json.loads(files["emst.bundle.jsonld"])["@graph"]
    assert not [r for r in graph if r.get("type") not in ("Mapping", "Release")]   # nothing is a candidate yet
    assert "held (Tribal content hold, ADR-0007 §D)" in b.excluded
    # the project lead dedicated the v1 text to CC0 (Q2): no record is excluded for licence reasons
    assert "v1-derived text pending CC0 dedication (ADR-0013, Q2)" not in b.excluded
    x1 = [r for r in graph if r.get("type") == "Mapping" and r["mapping_set_id"].endswith("emst-v1_to_v2")]
    subjects = {r["subject_id"] for r in x1}
    assert len(subjects) == 222 + 666                                    # X1 stays complete in the release
    assert all(not str(r["object_id"]).startswith("seed:") for r in x1)   # unreleased successors -> NoTermFound
    notes = files["RELEASE_NOTES.md"].decode()
    assert "held (Tribal content hold" in notes and "TN-C" not in notes


def test_base_tree_release_contents_and_exports_parse(tmp_path):
    import rdflib
    data = overlay_tree(tmp_path / "src")
    b, files = build(data, tmp_path / "out", version="2.0.0-rc.0")
    graph = json.loads(files["emst.bundle.jsonld"])["@graph"]
    assert {r["type"] for r in graph} == {"Release", "Competency", "Task", "Indicator", "CompetencyLevelOutcome"}
    clo = [r for r in graph if r["type"] == "CompetencyLevelOutcome"]
    cmp = next(r for r in graph if r["type"] == "Competency")
    assert [c["id"] for c in clo] == [f"{cmp['id']}/levels/{lv['level']}" for lv in cmp["levels"]]
    assert clo[0]["indicators"] == cmp["levels"][0]["indicators"]
    g = rdflib.Graph()
    g.parse(data=files["emst.skos.ttl"].decode(), format="turtle")
    assert len(g) > 100
    doc = json.loads(files["emst.bundle.jsonld"])
    jg = rdflib.Graph()
    jg.parse(data=json.dumps(doc), format="json-ld")
    assert len(jg) > 20
    pkg = json.loads(files["csv/datapackage.json"])
    for res in pkg["resources"]:
        assert res["hash"] == "sha256:" + L.sha256_bytes(files["csv/" + res["path"]])
    lib = files["csv/hcm_skills_library.csv"].decode().splitlines()
    assert lib[0].startswith("skill_id,uri,case_uuid,ctid") and len(lib) == 2
    assert "not a selection instrument" in lib[1]
    eut = json.loads(files["views/effective_use_tier.json"])
    assert {r["ruleId"] for r in eut["rows"]} == {"effective-use-tier"} and eut["header"]["ruleVersion"] == "1.0.0"


def test_gate_refuses_tribal_text_in_released_record(tmp_path):
    data = overlay_tree(tmp_path / "src")
    cmp = next((data / "core" / "competencies").glob("CMP-*.yaml"))
    rec = L.load_yaml(cmp)
    rec["scopeNote"] = {"en": "Covers government-to-government consultation with Tribal nations."}
    L.write_yaml(cmp, rec)
    with pytest.raises(SystemExit, match="release gate"):
        build(data, tmp_path / "out", version="2.0.0-rc.0")


def test_build_refuses_when_validation_fails(tmp_path):
    data = overlay_tree(tmp_path / "src", FIXTURES / "violations" / "dangling-ref")
    assert build_release.main(["--data-root", str(data), "--out", str(tmp_path / "out"), "--version", "2.0.0-rc.0"]) == 1


def test_held_references_are_redacted_from_released_records(tmp_path):
    data = overlay_tree(tmp_path / "src")
    held = L.load_yaml(FIXTURES / "records" / "valid" / "Competency.yaml")
    held.update(id="seed:TN-C02", indigenousDataFlag=True, approvalStatus="pending-tribal-review", sensitivity="restricted-governed")
    L.write_yaml(data / "core" / "competencies" / "seed-TN-C02.yaml", held)
    cmp = next((data / "core" / "competencies").glob("CMP-*.yaml"))
    rec = L.load_yaml(cmp)
    rec["replaces"] = ["seed:TN-C02"]
    L.write_yaml(cmp, rec)
    _, files = build(data, tmp_path / "out", version="2.0.0-rc.0")
    assert b"TN-C02" not in b"".join(files.values())


# ---------------------------------------------------------------- ADR-0029 §4, §6, §8, §9 release gate and views
def _valid(t, **kw):
    rec = L.load_yaml(FIXTURES / "records" / "valid" / f"{t}.yaml")
    rec.update(kw)
    return rec


def test_gate_excludes_third_party_quarantined_placeholder_and_small_n(tmp_path):
    data = overlay_tree(tmp_path / "src")
    tsk = L.load_yaml(next((data / "core" / "tasks").glob("TSK-*.yaml")))
    recs = [
        _valid("ExposureAssessment", id="seed:fx-x-3p", task=tsk["id"], taskTextSha256=tsk["textSha256"],
               license="LicenseRef-EMST-third-party-index-derived"),
        _valid("ChangeSignal", id="seed:fx-x-care", targetId=tsk["id"], careFlag=True),
        _valid("ChangeSignal", id="seed:fx-x-sp12", targetId=tsk["id"], scenarioSignposts=["vocab:scenarios#SP-12"]),
        _valid("ChangeSignal", id="seed:fx-x-mvp", targetType="RoleProfile", targetId="mvp-role:R02-field-resource-technician"),
        _valid("ChangeSignal", id="seed:fx-x-org", targetType="organization", targetId="opm-agency:AG00",
               measure=dict(_valid("ChangeSignal")["measure"], n=2)),
        _valid("ChangeSignal", id="seed:fx-x-ok", targetId=tsk["id"]),
    ]
    for r in recs:
        d = data / ("assessments/fx" if r["type"] == "ExposureAssessment" else "signals/fx")
        d.mkdir(parents=True, exist_ok=True)
        with (d / "batch.jsonl").open("a") as fh:
            fh.write(L.jsonl_line(r) + "\n")
    b, files = build(data, tmp_path / "out", profile="preview", version="2.0.0-dev")
    ids = {r.get("id") for r in json.loads(files["emst.bundle.jsonld"])["@graph"]}
    assert "seed:fx-x-ok" in ids
    assert not ids & {"seed:fx-x-3p", "seed:fx-x-care", "seed:fx-x-sp12", "seed:fx-x-mvp", "seed:fx-x-org"}
    assert b.excluded[build_release.EXCLUDE_THIRD_PARTY] == 1
    blob = b"".join(files.values())
    assert b"LicenseRef-EMST-third-party-index-derived" not in blob
    notes = files["RELEASE_NOTES.md"].decode()
    assert "third-party index-derived licence" in notes and "| change-indicator | 1.0.0 |" in notes


def test_records_on_held_targets_inherit_the_hold(tmp_path):
    data = overlay_tree(tmp_path / "src")
    held = _valid("Task", id="seed:fx-held-task", indigenousDataFlag=True, approvalStatus="pending-tribal-review",
                  sensitivity="restricted-governed")
    L.write_yaml(data / "core" / "tasks" / "seed-fx-held-task.yaml", held)
    d = data / "assessments" / "fx"
    d.mkdir(parents=True)
    (d / "b.jsonl").write_text(L.jsonl_line(_valid("ExposureAssessment", id="seed:fx-on-held", task="seed:fx-held-task")) + "\n")
    b, files = build(data, tmp_path / "out", profile="preview", version="2.0.0-dev")
    assert b"seed:fx-on-held" not in b"".join(files.values()) and b"fx-held-task" not in b"".join(files.values())


def test_inverse_links_are_computed_into_bundle_and_view(tmp_path):
    data = overlay_tree(tmp_path / "src")
    cmp = L.load_yaml(next((data / "core" / "competencies").glob("CMP-*.yaml")))
    tsk = L.load_yaml(next((data / "core" / "tasks").glob("TSK-*.yaml")))
    L.write_yaml(data / "core" / "enactments" / "seed-fx-ena.yaml", _valid("Enactment", id="seed:fx-ena", competency=cmp["id"]))
    tool = _valid("Tool", id="seed:fx-tool", servesTasks=[tsk["id"]])
    tool.pop("servesCompetencies", None)
    (data / "tools").mkdir(exist_ok=True)
    (data / "tools" / "tools.jsonl").write_text(L.jsonl_line(tool) + "\n")
    _, files = build(data, tmp_path / "out", profile="preview", version="2.0.0-dev")
    graph = {r.get("id"): r for r in json.loads(files["emst.bundle.jsonld"])["@graph"]}
    assert graph[tsk["id"]]["tools"] == ["seed:fx-tool"]
    assert graph[cmp["id"]]["enactments"][0]["id"] == "seed:fx-ena"
    assert graph[cmp["id"]]["enactments"][0]["enactmentKind"] == _valid("Enactment")["enactmentKind"]
    view = json.loads(files["views/inverse_links.json"])
    row = next(r for r in view if r.get("competency") == cmp["id"])
    assert row["enactments"][0]["enactment"] == "seed:fx-ena" and row["ruleVersion"] == "1.2.0"
    assert next(r for r in view if r.get("task") == tsk["id"])["tools"] == ["seed:fx-tool"]


def test_views_pin_io_files_and_gate_values(tmp_path):
    data = overlay_tree(tmp_path / "src")
    _, files = build(data, tmp_path / "out", profile="preview", version="2.0.0-dev")
    eut = json.loads(files["views/effective_use_tier.json"])
    assert eut["header"]["tierRequirementsSha256"] == L.sha256_bytes((L.ROOT / "validation" / "indicator_lint_rules.yaml").read_bytes())
    for r in eut["rows"]:
        assert set(r["caps"]) <= {"lifecycle", "evidence", "levelRule", "indicatorLint", "pathway"} and r["bindingCap"]
    dg = json.loads(files["views/display_gate.json"])
    assert dg["header"]["gatesSha256"] == L.sha256_bytes((L.ROOT / "validation" / "display_gates.yaml").read_bytes())
    assert {r["decision"] for r in dg["rows"]} <= {"production", "tentative", "editorial", "pending", "hidden"}
    assert any(r["decision"] == "editorial" for r in dg["rows"])           # Competency.competencyType etc.
    assert json.loads(files["views/agreement/index.json"])["studies"] == []   # no study data before S2
    assert "rows" in json.loads(files["views/change_indicators.json"])


def test_strict_sssom_rendering(tmp_path):
    data = overlay_tree(tmp_path / "src")
    tsk = L.load_yaml(next((data / "core" / "tasks").glob("TSK-*.yaml")))
    d = data / "crosswalks" / "fx"
    d.mkdir(parents=True)
    (d / "1.sssom.tsv").write_text("record_id\tsubject_id\tpredicate_id\tobject_id\tmapping_justification\tother\n"
                                   f"a\t{tsk['id']}\tskos:closeMatch\tX:1\tsemapv:LLMBasedMatching\treview_status=candidate\n")
    (d / "1.sssom.yml").write_text(L.dump_yaml({"mapping_set_id": "https://w3id.org/emst/crosswalks/fx/1", "mapping_set_version": "0.0.1",
                                                "license": "https://creativecommons.org/publicdomain/zero/1.0/", "curie_map": {"X": "https://example.org/x/"}}))
    _, files = build(data, tmp_path / "out", profile="preview", version="2.0.0-dev")
    strict = files["sssom/strict-1.0/fx/1.sssom.tsv"].decode().splitlines()
    assert "semapv:UnspecifiedMatching" in strict[1] and "original_justification=semapv:LLMBasedMatching" in strict[1]
    assert "semapv:LLMBasedMatching\treview_status" in files["sssom/fx/1.sssom.tsv"].decode()


def test_agreement_emitter_against_synthetic_human_ratings():
    """ADR-0029 §6.1: built against IO's validation/tests conventions; synthetic ratings, no study data."""
    import random
    from rules import agreement, io_bridge
    gates = io_bridge.load("display_gate").load_gates()
    rng = random.Random(7)
    ratings = []
    for u in range(130):
        truth = rng.choice(["A", "B", "C"])
        for j, rater in enumerate(("pid:fx-r1", "pid:fx-r2", "pid:fx-r3")):
            v = truth if rng.random() > 0.03 else rng.choice(["A", "B", "C"])
            ratings.append({"type": "CraftRating", "instrument": "emst-craft@0.1", "codebookVersion": "craft-codebook@1.0.0",
                            "task": f"seed:fx-t{u:03d}", "raterType": "sme", "raterId": rater, "values": {"primary": v}})
        ratings.append({"type": "CraftRating", "instrument": "emst-craft@0.1", "codebookVersion": "craft-codebook@1.0.0",
                        "task": f"seed:fx-t{u:03d}", "raterType": "llm", "raterId": "emstagent:fx@1", "values": {"primary": "A"}})
    study = {"studyId": "REL-FX-01", "dimension": "CraftRating:emst-craft", "codebookVersion": "craft-codebook@1.0.0",
             "metric": "nominal", "preregistrationId": "osf-fixture", "studyDate": "2027-03-01", "blindCodingAttested": True,
             "valueField": "values.primary", "categories": ["A", "B", "C"]}
    stamp = {"ruleId": "display-gate", "ruleVersion": "1.0.0", "buildCommit": "test"}
    res = agreement.emit(ratings, [study], stamp, B=2000)["REL-FX-01"]
    for k in gates["agreement_result_schema"]["required"]:
        assert k in res, k
    assert res["raterTypesCounted"] == ["sme"] and res["nUnits"] == 130 and res["ruleVersion"] == "1.0.0"
    assert res["ciLower"] > 0.8
