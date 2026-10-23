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
    assert {r["type"] for r in graph} == {"Release", "Competency", "Task", "Indicator"}
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
    assert {r["ruleId"] for r in json.loads(files["views/effective_use_tier.json"])} == {"effective-use-tier"}


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
