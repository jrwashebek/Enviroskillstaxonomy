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
    recs = [r for r in graph if r.get("type") not in ("Mapping", "Release", "CompetencyLevelOutcome")]   # CLO IRIs are derived
    # since WP-16 (ADR-0031 §6) the release carries promoted records only: minted IDs at a release status, nothing held,
    # nothing withheld for an unverified claims-register row
    assert recs and all(L.is_emst_id(r["id"]) and r.get("status") in build_release.RELEASE_STATUSES for r in recs)
    assert not [r for r in recs if r["id"] in b.withheld]
    assert b.excluded.get("draft (not in a release)", 0) > 0
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
    from rules import registry
    active = registry.active_rules()
    assert {r["ruleId"] for r in eut["rows"]} == {"effective-use-tier"}
    assert eut["header"]["ruleVersion"] == str(active["effective-use-tier"]["version"])


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
    from rules import registry
    ci = registry.active_rules()["change-indicator"]["version"]
    assert "third-party index-derived licence" in notes and f"| change-indicator | {ci} |" in notes


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


# ---------------------------------------------------------------- rc.1 fix pass (docs/review/DATA_FIX_BRIEF.md)
def test_b1_language_maps_only_where_the_schema_types_text(tmp_path):
    data = overlay_tree(tmp_path / "src")
    p = next((data / "core" / "competencies").glob("CMP-*.yaml"))
    rec = L.load_yaml(p)
    rec["provenance"]["derivedFrom"] = [{"v1Key": "v1:1.1.1", "relation": "rewritten", "note": "plain nested note"}]
    rec["changeNote"] = [{"release": "2.0.0", "note": "a Text-typed note"}]
    L.write_yaml(p, rec)
    b, files = build(data, tmp_path / "out", version="2.0.0-rc.0")
    node = next(r for r in json.loads(files["emst.bundle.jsonld"])["@graph"] if r.get("id") == rec["id"])
    assert node["provenance"]["derivedFrom"][0]["note"] == "plain nested note"          # schema: string
    assert node["changeNote"][0]["note"] == {"en": "a Text-typed note"}                 # schema: Text
    paths = build_release.schema_text_paths(b.schema())
    assert ("changeNote", "[]", "note") in paths["Competency"] and ("provenance", "derivedFrom", "[]", "note") not in paths["Competency"]


def test_b1_self_check_validates_every_bundle_node(tmp_path):
    data = overlay_tree(tmp_path / "src")
    b, files = build(data, tmp_path / "out", version="2.0.0-rc.0")
    doc = json.loads(files["emst.bundle.jsonld"])
    assert b.schema_check(doc) == []
    doc["@graph"][1]["useTier"] = "not-a-tier"
    doc["@graph"].append({"type": "Mapping", "subject_id": "a", "predicate_id": "skos:closeMatch", "object_id": "b",
                          "mapping_justification": "semapv:LLMBasedMatching", "confidence": "0.6"})
    doc["@graph"][0]["unexpected"] = 1                                                  # the Release manifest
    problems = b.schema_check(doc)
    assert problems[0].startswith("schema: 3 bundle nodes fail")
    assert any("Mapping" in p and "0.6" in p for p in problems) and any("Release" in p for p in problems)


def test_b1_redaction_never_empties_a_required_field(tmp_path):
    data = overlay_tree(tmp_path / "src")
    tool = _valid("Tool", id="seed:fx-tool-orphan", servesCompetencies=["seed:fx-never-authored"])
    tool.pop("servesTasks", None)
    (data / "tools").mkdir(exist_ok=True)
    (data / "tools" / "tools.jsonl").write_text(L.jsonl_line(tool) + "\n")
    b, files = build(data, tmp_path / "out", profile="preview", version="2.0.0-dev")
    assert b.held_back == ["seed:fx-tool-orphan"] and b.excluded[build_release.EXCLUDE_REDACTION] == 1
    assert b"seed:fx-tool-orphan" not in files["emst.bundle.jsonld"]
    assert "held back" in files["RELEASE_NOTES.md"].decode()


def test_m4_withheld_basis_makes_the_venue_value_indeterminate(tmp_path):
    data = overlay_tree(tmp_path / "src")
    b = build_release.Builder(data, profile="preview", version="2.0.0-dev", build_commit="test")
    b.included = set(b.records)
    ena = _valid("Enactment", id="seed:fx-ena-v", characteristicInstruments=[
        {"instrument": "seed:fx-ins-not-released", "role": "requires"}, {"instrument": "seed:fx-ins-2", "role": "removed-requirement"}])
    b.clean(ena)
    assert b.basis_withheld == {"seed:fx-ena-v"}
    b.clean(_valid("Enactment", id="seed:fx-ena-w", characteristicInstruments=[{"instrument": "seed:fx-ins-2", "role": "removed-requirement"}]))
    assert b.basis_withheld == {"seed:fx-ena-v"}                                        # removed-requirement never decides
    view = {"header": {}, "rows": [{"competency": "c", "sectorActor": "federal", "venueApplicability": "permitted", "enactments": ["seed:fx-ena-v"]},
                                   {"competency": "d", "sectorActor": "state", "venueApplicability": "permitted", "enactments": ["x"]}],
            "federal": {"c": {"federalApplicability": "permitted", "note": "n"}}}
    out = b.venue_overlay(view)
    assert out["rows"][0]["venueApplicability"] == build_release.VENUE_WITHHELD and out["rows"][0]["basisWithheld"]
    assert out["rows"][1]["venueApplicability"] == "permitted"
    assert out["federal"]["c"]["federalApplicability"] == build_release.VENUE_WITHHELD and "1 rows" in out["header"]["basisWithheldOverlay"]


def test_m14_trigger_scan_covers_every_file_and_field(tmp_path):
    data = overlay_tree(tmp_path / "src")
    b = build_release.Builder(data, profile="preview", version="2.0.0-dev", build_commit="test")
    bundle = {"@graph": [{"id": "r", "type": "Release", "indigenousKnowledgeStatement": build_release.INDIGENOUS_STATEMENT},
                         {"type": "Mapping", "subject_id": "EMSTv1:9.9.9", "comment": "successor withheld for Tribal review"},
                         {"id": "emst:core/TSK-X", "type": "Task", "provenance": {"note": "drafted with treaty rights in view"}}]}
    files = {
        "emst.bundle.jsonld": json.dumps(bundle).encode(),
        "emst.skos.ttl": (f'<{L.IRI_BASE}vocab/sector_actors/x> skos:definition "Tribal government"@en .\n'
                          f'<{L.IRI_BASE}core/CMP-X> skos:scopeNote "Consult Tribal nations"@en .\n').encode(),
        "sssom/x/1.sssom.yml": b"comment: Tribal role variants are not mapped\n",
        "sssom/x/1.sssom.tsv": b"subject_id\tother\na\theld_variants=tribal\n",
        "csv/mappings.csv": b"a,b,c\n",
        "views/v.json": json.dumps({"rows": [{"recordId": "x", "Tribal programmes": 1}]}).encode(),
        "views/counts.json": json.dumps({"excluded": {build_release.EXCLUDE_HELD: 3}}).encode(),
        "RELEASE_NOTES.md": "\n".join([f"- {build_release.HOLD_COUNT_LINE}: 3.", build_release.HOLD_POLICY_LINE,
                                       f"- {build_release.INDIGENOUS_STATEMENT}"]).encode(),
    }
    hits = b.trigger_scan(files)
    where = sorted(h.split(" in ", 1)[1].split(" ")[0] for h in hits)
    assert where == ["emst.bundle.jsonld", "emst.bundle.jsonld", "emst.skos.ttl", "sssom/x/1.sssom.tsv",
                     "sssom/x/1.sssom.yml", "views/v.json"], hits
    assert any("line 2" in h for h in hits if "skos" in h) and any("provenance/note" in h for h in hits)


def test_m14_x1_rows_carry_no_hold_marker(tmp_path):
    data = overlay_tree(tmp_path / "src")
    tsk = L.load_yaml(next((data / "core" / "tasks").glob("TSK-*.yaml")))
    d = data / "crosswalks" / "emst-v1"
    d.mkdir(parents=True)
    hdr = "subject_id\tpredicate_id\tobject_id\tmapping_justification\tother\tcomment\n"
    (d / "x.sssom.tsv").write_text(hdr
        + "EMSTv1:9.1.1\temst:replacedBy\tseed:TN-C02\tsemapv:LLMBasedMatching\t\tdecision=hold-for-tribal-review; target=TN-C02 (held)\n"
        + f"EMSTv1:9.1.2\temst:splitInto\t{tsk['id']}\tsemapv:LLMBasedMatching\t\tdecision=split; target=X|TN-C02 (held: Tribal)\n"
        + "EMSTv1:9.1.2\temst:splitInto\tseed:TN-C02\tsemapv:LLMBasedMatching\t\tdecision=split; target=X|TN-C02 (held: Tribal)\n")
    x3 = data / "crosswalks" / "soc"
    x3.mkdir(parents=True)
    (x3 / "2018.sssom.tsv").write_text("subject_id\tpredicate_id\tobject_id\tmapping_justification\tother\n"
                                       f"{tsk['id']}\tskos:relatedMatch\tSOC:19-1031\tsemapv:LLMBasedMatching\trater_type=llm;held_variants=tribal\n")
    b, files = build(data, tmp_path / "out", profile="preview", version="2.0.0-dev")
    rows = b._mapping_rows(b.released)["emst-v1/x"]
    x1 = {r["subject_id"]: r["comment"] for r in rows}
    assert x1["EMSTv1:9.1.1"] == build_release.X1_NOT_RELEASED
    held_row = next(r for r in rows if r["subject_id"] == "EMSTv1:9.1.1")
    assert held_row["object_id"] == "sssom:NoTermFound" and held_row["predicate_id"] == "emst:successorNotReleased"   # M9, m5
    assert x1["EMSTv1:9.1.2"] == "decision=split; ADR-0011; one or more successors not in this release"
    blob = b"".join(files.values()).decode("utf-8", "replace")
    assert "held_variants" not in blob and "TN-C02" not in blob
    assert "Tribal Advisory Council review" not in blob


def test_m1_build_stamp_must_identify_its_inputs(monkeypatch):
    head = "a" * 40
    monkeypatch.setattr(build_release, "git_state", lambda root: (head, True))
    chk = build_release.check_build_commit
    assert "refusing" in chk(head + "+uncommitted", "release") and "refusing" in chk("uncommitted", "release")
    assert "differ from HEAD" in chk(head, "release")                                   # claims a clean tree it is not
    assert "HEAD is" in chk("b" * 40, "release")
    assert chk(head + build_release.PENDING_COMMIT_SUFFIX, "release") is None
    assert chk(head + "+uncommitted", "preview") is None
    monkeypatch.setattr(build_release, "git_state", lambda root: (head, False))
    assert chk(head, "release") is None
    with pytest.raises(SystemExit, match="refusing"):
        build_release.Builder(FIXTURES / "trees" / "base" / "data" / "v2", profile="release", version="2.0.0-rc.0",
                              build_commit=head + "+uncommitted")


def test_m1_release_date_ignores_source_date_epoch(tmp_path, monkeypatch):
    data = overlay_tree(tmp_path / "src")
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1893456000")                                # 2030-01-01
    rel = build_release.Builder(data, profile="release", version="2.0.0-rc.0", build_commit="test")
    pre = build_release.Builder(data, profile="preview", version="2.0.0-dev", build_commit="test")
    assert rel.date == "2026-10-23" and pre.date == "2030-01-01"


def test_m2_datapackage_created_is_a_datetime(tmp_path):
    import re
    data = overlay_tree(tmp_path / "src")
    _, files = build(data, tmp_path / "out", version="2.0.0-rc.0")
    pkg = json.loads(files["csv/datapackage.json"])
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T00:00:00Z", pkg["created"])


def test_notes_state_status_ids_omissions_and_rater_breakdown(tmp_path):
    data = overlay_tree(tmp_path / "src")
    tsk = L.load_yaml(next((data / "core" / "tasks").glob("TSK-*.yaml")))
    d = data / "assessments" / "fx"
    d.mkdir(parents=True)
    rows = [_valid("CraftRating", id=f"seed:fx-cr-{i}", task=tsk["id"], taskTextSha256=tsk["textSha256"], raterType="llm",
                   raterId="emstagent:fx-rater@1", passIndex=i + 1, sessionId=f"fx-session-{i + 1}", validationStatus="draft",
                   provenance=dict(_valid("CraftRating")["provenance"], method="llm-assisted", toolVersion="fx-model",
                                   promptVersion="fx-prompt@1"))
            for i in range(3)]
    (d / "b.jsonl").write_text("".join(L.jsonl_line(r) + "\n" for r in rows))
    b, files = build(data, tmp_path / "out", profile="preview", version="2.0.0-dev")
    notes = files["RELEASE_NOTES.md"].decode()
    assert "Publication status: not cleared for external publication; items 6 and 7 fail" in notes          # m15
    assert "IDs are candidate; they become stable from 2.0.0" in notes                                        # m11
    assert "## Not in this release (SPEC §12.5, §17.2)" in notes and "CTDL-ASN" in notes and "CASE 1.1" in notes   # m3
    assert "| CraftRating | llm | 3 | 1 | 1 |" in notes                                                        # m12
    assert "IDs are candidate" in files["csv/hcm_skills_library.csv"].decode()
    assert b.publication["line"] == "not cleared for external publication; items 6 and 7 fail"


def test_m8_stale_ratings_are_marked_in_the_bundle(tmp_path):
    data = overlay_tree(tmp_path / "src")
    tsk = L.load_yaml(next((data / "core" / "tasks").glob("TSK-*.yaml")))
    d = data / "assessments" / "fx"
    d.mkdir(parents=True)
    fresh = _valid("CraftRating", id="seed:fx-fresh", task=tsk["id"], taskTextSha256=tsk["textSha256"], validationStatus="draft")
    stale = _valid("CraftRating", id="seed:fx-stale", task=tsk["id"], taskTextSha256="0" * 64, validationStatus="draft")
    (d / "b.jsonl").write_text(L.jsonl_line(fresh) + "\n" + L.jsonl_line(stale) + "\n")
    b, files = build(data, tmp_path / "out", profile="preview", version="2.0.0-dev")
    graph = {r.get("id"): r for r in json.loads(files["emst.bundle.jsonld"])["@graph"]}
    assert graph["seed:fx-stale"]["stale"] is True and "stale" not in graph["seed:fx-fresh"]
    view = json.loads(files["views/assessment_staleness.json"])
    rows = view if isinstance(view, list) else view.get("rows", [])
    assert {r["assessment"] for r in rows if r.get("stale")} == {"seed:fx-stale"}
    assert "stale" in L.load_yaml(L.LINT_DIR / "computed_fields.yaml")["fields"]


def test_m9_unreleased_successor_is_never_a_positive_no_term_found(tmp_path):
    data = overlay_tree(tmp_path / "src")
    d = data / "crosswalks" / "emst-v1"
    d.mkdir(parents=True)
    (d / "emst-v1_to_v2.sssom.tsv").write_text("subject_id\tpredicate_id\tobject_id\tmapping_justification\tcomment\n"
                                   "EMSTv1:9.2.1\temst:replacedBy\tseed:fx-unauthored\tsemapv:LLMBasedMatching\tdecision=carry; ADR-0011\n"
                                   "EMSTv1:9.2.2\temst:retiredWithoutReplacement\tsssom:NoTermFound\tsemapv:LLMBasedMatching\tdecision=retire\n")
    x = data / "crosswalks" / "esco"
    x.mkdir(parents=True)
    (x / "1.sssom.tsv").write_text("subject_id\tpredicate_id\tobject_id\tmapping_justification\n"
                                   "seed:fx-unauthored\tskos:closeMatch\tESCO:1\tsemapv:LLMBasedMatching\n"
                                   "EMSTv1:1.1.1\tskos:closeMatch\tseed:fx-unauthored\tsemapv:LLMBasedMatching\n")
    b, files = build(data, tmp_path / "out", profile="preview", version="2.0.0-dev")
    sets = b._mapping_rows(b.released)
    rows = {r["subject_id"]: r for r in sets["emst-v1/emst-v1_to_v2"]}
    assert rows["EMSTv1:9.2.1"]["predicate_id"] == "emst:successorNotReleased" and rows["EMSTv1:9.2.1"]["object_id"] == "sssom:NoTermFound"
    assert rows["EMSTv1:9.2.2"]["predicate_id"] == "emst:retiredWithoutReplacement"
    assert sets["esco/1"] == []                                   # mappings to or from unreleased content are not released
    v1 = {k["v1"]: k for k in json.loads(files["delta_v1.json"])["v1Keys"]}
    assert v1["EMSTv1:9.2.1"]["decision"] == "carry" and v1["EMSTv1:9.2.1"]["successorsNotInRelease"] == 1
