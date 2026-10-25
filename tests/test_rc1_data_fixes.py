"""rc.1 data and method fix pass (ADR-0032; docs/review/data_method_review.md): one test per finding that would have
caught it, on synthetic trees for the validator rules and on the live data for the invariants the fix established.

Findings: M2-M10, m5-m10, m13, m14 (data parts). Validator rules exercised: E-INDEPENDENCE-KEY-UNLISTED at every
status, E-LIFECYCLE-BASIS (threshold re-applied to the evidence), E-SSSOM-NOTERM-POSITIVE, E-LLM-RATER and friends.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import re
from collections import defaultdict

import pytest
from jsonschema import Draft202012Validator

from conftest import FIXTURES, L, overlay_tree

import validate_v2
from rules import change_indicator as CI
from rules import federal_series_profile as FSP
from rules import lifecycle_basis as LB
from rules import state_class_view as SCV

SCHEMA = json.loads(L.SCHEMA_OUT.read_text(encoding="utf-8"))
SV = Draft202012Validator(SCHEMA)
CAVEAT = validate_v2.LLM_PASS_CAVEAT


def run(data, **kw):
    kw.setdefault("use_git_base", False)
    kw.setdefault("check_x1", False)
    return validate_v2.Validator(data, **kw).run()


def valid(t, **kw):
    rec = L.load_yaml(FIXTURES / "records" / "valid" / f"{t}.yaml")
    rec.update(kw)
    return rec


def codes_for(rep, rid):
    return {i.code for i in rep.issues if i.rid == rid}


def schema_errors(rec):
    return [e.message for e in SV.iter_errors(rec)]


@pytest.fixture(scope="module")
def live():
    """Every parseable live record, once per module."""
    return [r for _, r in L.iter_records(L.DATA_V2) if isinstance(r, dict)]


@pytest.fixture(scope="module")
def live_by_id(live):
    return {r["id"]: r for r in live if isinstance(r.get("id"), str)}


def _sets():
    out = {}
    for tsv in sorted((L.DATA_V2 / "crosswalks").rglob("*.sssom.tsv")):
        lines = [ln for ln in tsv.read_text(encoding="utf-8").splitlines() if ln and not ln.startswith("#")]
        out[tsv] = list(csv.DictReader(lines, delimiter="\t"))
    return out


def _other(row):
    return dict(p.split("=", 1) for p in (row.get("other") or "").split(";") if "=" in p)


# ================================================================== M2: v1 tags are LLM-assisted, never J
def test_m2_every_v1_rating_is_labelled_llm_assisted(live):
    v1 = [r for r in live if r.get("type") in L.RATING_TYPES and r.get("raterType") == "v1-analyst"]
    assert len(v1) > 2000
    for r in v1:
        p = r["provenance"]
        assert r["evidenceLabel"] == "S" and p["evidenceLabel"] == "S", r["id"]
        assert p["method"] == "llm-assisted" and p["toolVersion"] == "unknown (v1 sessions)", r["id"]
        assert p["promptVersion"] == "legacy/v1 working records", r["id"]


def test_m2_every_rating_carries_validation_status(live):
    ratings = [r for r in live if r.get("type") in L.RATING_TYPES]
    assert ratings and all(r.get("validationStatus") == "draft" for r in ratings)


def test_m2_schema_rejects_a_j_labelled_v1_tag_and_a_rating_without_validation_status():
    r = valid("RelevanceRating", raterType="v1-analyst", raterId="v1-analyst-01", confidence="low", objectScheme="v1-family",
              object="EMSTv1:family/F1", v1Values={"family_code": "F1"}, evidenceLabel="J")
    r.pop("subjectTextSha256", None)
    assert any("'S' was expected" in m for m in schema_errors(r))
    r2 = valid("CraftRating")
    r2.pop("validationStatus")
    assert any("'validationStatus' is a required property" in m for m in schema_errors(r2))


# ================================================================== M3: X1 is agent-made, not manual curation
def test_m3_x1_uses_llm_based_matching_with_its_decision_source():
    rows = _sets()[L.X1_TSV]
    assert rows and {r["mapping_justification"] for r in rows} == {"semapv:LLMBasedMatching"}
    assert all("decision_source=docs/decisions/v1_disposition.csv" in r["other"] for r in rows)


def test_m3_validator_rejects_manual_curation_by_an_agent(tmp_path):
    data = overlay_tree(tmp_path)
    tid = next((data / "core" / "tasks").glob("TSK-*.yaml")).stem
    d = data / "crosswalks" / "fx-set"
    d.mkdir(parents=True)
    (d / "1.sssom.tsv").write_text("record_id\tsubject_id\tpredicate_id\tobject_id\tmapping_justification\tauthor_id\tother\n"
                                   f"a\temst:core/{tid}\tskos:closeMatch\tX:1\tsemapv:ManualMappingCuration\temstagent:fx@1\treview_status=candidate\n")
    (d / "1.sssom.yml").write_text(L.dump_yaml({"mapping_set_id": "x", "mapping_set_version": "0", "license": "CC0",
                                                "curie_map": {"X": "https://example.org/x/"}}))
    assert "E-SSSOM-MANUAL-AGENT" in run(data).codes()


# ================================================================== M4: passes of one model are one rater
def _llm_rating(rid, pass_index, rater="emstagent:llm-rater@model-x/fx-craft@1", method=f"fixture; {CAVEAT}"):
    return valid("CraftRating", id=rid, raterType="llm", raterId=rater, passIndex=pass_index, sessionId=f"fx-pass{pass_index}",
                 method=method, provenance={"method": "llm-assisted", "agent": [rater], "generatedAt": "2026-10-23T00:00:00Z",
                                             "toolVersion": "model-x", "promptVersion": "fx-craft@1", "evidenceLabel": "S",
                                             "reviewStatus": "unreviewed"})


def test_m4_live_llm_passes_share_one_rater_per_model_and_prompt_family(live):
    fams = defaultdict(set)
    for r in live:
        if r.get("type") in L.RATING_TYPES and r.get("raterType") == "llm":
            p = r["provenance"]
            m = validate_v2.LLM_RATER_RE.match(r["raterId"])
            assert m and m.group(1) == p["toolVersion"], r["id"]
            assert CAVEAT in r["method"] and r["passIndex"] in (1, 2, 3) and r["sessionId"], r["id"]
            fams[(r["instrument"], p["toolVersion"], m.group(2))].add(r["raterId"])
    assert fams and all(len(v) == 1 for v in fams.values())


def test_m4_validator_rejects_per_pass_raters_missing_caveat_and_duplicate_passes(tmp_path):
    data = overlay_tree(tmp_path)
    recs = [_llm_rating("seed:fx-p1", 1, rater="emstagent:fx-rater-1@wp99"),           # old per-pass rater id
            _llm_rating("seed:fx-p2", 2, method="blind coding"),                      # no caveat
            _llm_rating("seed:fx-p3", 3), _llm_rating("seed:fx-p3b", 3)]              # pass 3 twice
    p = data / "assessments" / "emst-craft@0.1" / "fx.jsonl"
    p.parent.mkdir(parents=True)
    p.write_text("".join(L.jsonl_line(r) + "\n" for r in recs))
    rep = run(data)
    assert "E-LLM-RATER" in codes_for(rep, "seed:fx-p1")
    assert "E-LLM-PASS-METHOD" in codes_for(rep, "seed:fx-p2")
    assert "E-LLM-PASS-DUPLICATE" in codes_for(rep, "seed:fx-p3b")


def test_m4_schema_requires_pass_and_session_on_llm_ratings():
    r = _llm_rating("seed:fx-p", 1)
    assert not schema_errors(r)
    r.pop("passIndex")
    assert any("'passIndex' is a required property" in m for m in schema_errors(r))


# ================================================================== M5: independence key, upstream, chain, observations
def test_m5_independence_key_is_the_vocabulary_enumeration():
    keys = [k["key"] for k in L.load_yaml(L.VOCAB / "change_types.yaml")["independence_keys"]["keys"]]
    assert SCHEMA["$defs"]["v_independenceKey"]["enum"] == keys
    prop = SCHEMA["$defs"]["ChangeSignal"]["properties"]["independenceKey"]
    assert prop.get("$ref") == "#/$defs/v_independenceKey"


@pytest.mark.parametrize("status", ["watch", "active", "retired"])
def test_m5_unlisted_key_is_rejected_at_every_status(tmp_path, status):
    data = overlay_tree(tmp_path)
    sig = valid("ChangeSignal", id="seed:fx-unlisted", signalStatus=status, independenceKey="not-a-listed-key",
                signalFamily="postings-pds")
    p = data / "signals" / "fixture" / "u.jsonl"
    p.parent.mkdir(parents=True)
    p.write_text(L.jsonl_line(sig) + "\n")
    assert "E-INDEPENDENCE-KEY-UNLISTED" in codes_for(run(data), "seed:fx-unlisted")


def test_m5_every_live_signal_names_upstream_chain_and_observation(live):
    keys = {k["key"] for k in L.load_yaml(L.VOCAB / "change_types.yaml")["independence_keys"]["keys"]}
    sigs = [r for r in live if r.get("type") == "ChangeSignal"]
    assert sigs
    for s in sigs:
        assert s["independenceKey"] in keys and s["upstreamSource"] and s["processingChain"], s["id"]
        assert re.fullmatch(r"obs-[0-9a-f]{12}", s["observationId"]), s["id"]
        assert "reliability" not in s and s["sourceGrade"] in "ABCD", s["id"]          # m9


def test_m5_repeated_observations_share_one_id_and_the_counts_are_distinct(live):
    sigs = [r for r in live if r.get("type") == "ChangeSignal" and r.get("status") == "candidate"]
    by_obs = defaultdict(set)
    for s in sigs:
        by_obs[s["observationId"]].add((s["upstreamSource"], json.dumps(s["measure"]["value"])))
    assert all(len(v) == 1 for v in by_obs.values())
    epa = {s["observationId"] for s in sigs if s["measure"]["name"] == "headcount" and s["measure"]["value"] == 12849}
    assert len(epa) == 1                                    # the EPA staffing figure is one observation on three targets
    assert len(by_obs) < len(sigs)


def test_m5_pnnl_signals_are_not_independent(live_by_id):
    a, b = live_by_id["emst:core/SIG-NHFHG9M"], live_by_id["emst:core/SIG-RKPCJRG"]
    assert not CI.independent(a, b)
    assert CI.providers(a) & CI.providers(b) == {"pnnl"}


def test_m5_null_measure_fields_state_a_reason(tmp_path, live):
    for s in (r for r in live if r.get("type") == "ChangeSignal"):
        m = s["measure"]
        for f in ("ci95", "n"):
            assert m.get(f) is not None or (m.get("nullReason") or {}).get(f), (s["id"], f)
    data = overlay_tree(tmp_path)
    sig = valid("ChangeSignal", id="seed:fx-null")
    sig["measure"] = {k: v for k, v in sig["measure"].items() if k != "ci95"}
    p = data / "signals" / "fixture" / "n.jsonl"
    p.parent.mkdir(parents=True)
    p.write_text(L.jsonl_line(sig) + "\n")
    assert "E-MEASURE-NULL-REASON" in codes_for(run(data), "seed:fx-null")


def test_m5_inconsistent_observation_is_rejected(tmp_path):
    data = overlay_tree(tmp_path)
    a = valid("ChangeSignal", id="seed:fx-oa")
    b = valid("ChangeSignal", id="seed:fx-ob", measure=dict(a["measure"], value=0.2))
    p = data / "signals" / "fixture" / "o.jsonl"
    p.parent.mkdir(parents=True)
    p.write_text(L.jsonl_line(a) + "\n" + L.jsonl_line(b) + "\n")
    assert "E-OBSERVATION-INCONSISTENT" in run(data).codes()


# ================================================================== M6: directions follow from the data
def test_m6_indeterminate_where_the_difference_interval_includes_zero(live_by_id):
    for sid in ("SIG-6SMSZRG", "SIG-HGAGZE8", "SIG-SS0M0J6", "SIG-EDTT3Y9", "SIG-4G9Z4EK", "SIG-84J3FBK", "SIG-VFA30PA"):
        assert live_by_id[f"emst:core/{sid}"]["direction"] == "indeterminate", sid
    for r in live_by_id.values():
        diff = (r.get("measure") or {}).get("difference") if r.get("type") == "ChangeSignal" else None
        if diff:
            spans = [diff["ci95"]] + ([diff["sensitivity"]["ci95"]] if diff.get("sensitivity") else [])
            if any(lo <= 0 <= hi for lo, hi in spans):
                assert r["direction"] == "indeterminate", r["id"]


def test_m6_projection_confidence_is_capped_when_broader_than_close_match(live):
    for r in live:
        if r.get("type") == "ChangeSignal" and r.get("signalFamily") == "projection" \
                and r["crosswalkMinMatchType"] not in ("skos:exactMatch", "skos:closeMatch"):
            assert r["directionConfidence"] == "low", r["id"]


def test_m6_validator_catches_unsupported_directions(tmp_path):
    data = overlay_tree(tmp_path)
    tid = next((data / "core" / "tasks").glob("TSK-*.yaml")).stem
    a = valid("ChangeSignal", id="seed:fx-diff", targetId=f"emst:core/{tid}")
    a["measure"] = dict(a["measure"], difference={"value": 1.0, "ci95": [-0.1, 2.0], "method": "fixture"})
    b = valid("ChangeSignal", id="seed:fx-proj", targetId=f"emst:core/{tid}", signalFamily="projection",
              crosswalkMinMatchType="skos:broadMatch", directionConfidence="med", direction="grow")
    b["measure"] = dict(b["measure"], value=2.2, baseline={"value": 3.5})
    p = data / "signals" / "fixture" / "d.jsonl"
    p.parent.mkdir(parents=True)
    p.write_text(L.jsonl_line(a) + "\n" + L.jsonl_line(b) + "\n")
    rep = run(data)
    assert "E-DIRECTION-INDETERMINATE" in codes_for(rep, "seed:fx-diff")
    assert {"E-PROJECTION-CONFIDENCE", "E-PROJECTION-DIRECTION"} <= codes_for(rep, "seed:fx-proj")


# ================================================================== M7: lifecycle thresholds
def _sig(sid, key, family, actor, chain, upstream):
    return {"id": sid, "type": "ChangeSignal", "independenceKey": key, "signalFamily": family, "sectorActor": actor,
            "processingChain": chain, "upstreamSource": upstream, "source": upstream, "observationId": "obs-" + sid[-12:].rjust(12, "0")}


def test_m7_entry_test_counts_only_independent_signals():
    tests = LB.entry_tests()
    good = {"s:a": _sig("s:000000000001", "opm-ehri-fwd", "headcount", "federal", ["coder:pid:a"], "U-1"),
            "s:b": _sig("s:000000000002", "conservation-job-board", "postings-pds", "ngo", ["coder:pid:b"], "U-2"),
            "s:c": _sig("s:000000000003", "nifc-imsr", "workload", "federal", ["coder:pid:c"], "U-3")}
    recs = {s["id"]: s for s in good.values()}
    role = {"type": "Competency", "lifecycleBasis": {"evidence": sorted(recs)}}
    b = LB.evaluate(role, recs, "proposed", "2026-10-25", tests)
    assert b["counts"]["independentSignals"] == 3 and b["result"] == "met"
    for s in recs.values():                                   # one LLM coder for all three: one independent signal
        s["processingChain"] = ["coder:emstagent:llm@x"]
    b = LB.evaluate(role, recs, "proposed", "2026-10-25", tests)
    assert b["counts"]["independentSignals"] == 1 and b["result"] == "not-met"


def test_m7_no_live_record_is_proposed_or_emerging_without_a_met_test(live):
    for r in live:
        if r.get("type") in LB.L1_L4_TYPES and r.get("lifecycleState") in LB.TESTED_STATES \
                and r.get("status") in ("candidate", "published", "deprecated"):
            assert (r.get("lifecycleBasis") or {}).get("result") == "met", r["id"]


def test_m7_the_eight_roles_are_watch_with_their_test_stored(live_by_id):
    for rid in ("emst:core/ROL-ETRR81A", "emst:core/ROL-RTNR722", "emst:core/ROL-8V0NKZ4", "emst:core/ROL-AC7DRZ6",
                "emst:core/ROL-XVN70QT", "emst:forest/ROL-G90XCWY", "emst:core/ROL-7DTPX8B", "emst:forest/ROL-FSCZ00K"):
        r = live_by_id[rid]
        assert r["lifecycleState"] == "watch" and r["lifecycleBasis"]["result"] == "not-met", rid


def test_m7_validator_re_applies_the_threshold(tmp_path):
    data = overlay_tree(tmp_path)
    cmp = next((data / "core" / "competencies").glob("CMP-*.yaml"))
    rec = L.load_yaml(cmp)
    rec.update(lifecycleState="emerging", reviewBy="2027-10-25")
    L.write_yaml(cmp, rec)
    assert "E-LIFECYCLE-BASIS" in run(data).codes()               # no basis at all (the schema requires it too)
    rec["lifecycleBasis"] = {"testedFor": "emerging", "test": "vocab/lifecycle_states.yaml#emerging.entry_test",
                             "result": "met", "evidence": [], "counts": {k: 0 for k in ("signals", "distinctObservations",
                             "independentSignals", "signalFamilies", "sectorActors", "postingsOrPds", "actorTypes")},
                             "assessedOn": "2026-10-25", "assessedBy": "emstagent:fixture@1"}
    L.write_yaml(cmp, rec)
    msgs = [i.message for i in run(data).issues if i.code == "E-LIFECYCLE-BASIS"]
    assert any("entry test gives 'not-met'" in m for m in msgs)    # claims met; the evidence does not


def test_m7_vocabulary_no_longer_caps_tiers_or_equates_established_with_validated():
    states = {s["notation"]: s for s in L.load_yaml(L.VOCAB / "lifecycle_states.yaml")["lifecycle_states"]}
    assert all("max_use_tier" not in s for s in states.values())
    assert "validationStatus" in states["established"]["meaning"] and "Validated" not in states["established"]["meaning"]
    from rules import effective_use_tier as EUT
    rows = EUT.compute({"x": {"id": "x", "type": "Task", "useTier": "develop", "lifecycleState": "watch",
                              "validationStatus": "draft"}}, {}, None, {})
    assert rows[0]["caps"]["lifecycle"] is None and rows[0]["effectiveUseTier"] == "describe"


# ================================================================== M8: v1 codes only in v1Values; sample frame; ranks
def test_m8_v1_exposure_records_carry_no_v2_construct_field(live):
    v2_fields = {"deploymentMode", "sWatch", "tacitExperienceRequirement", "mappingRule", "technicalExposure", "deploymentStage"}
    v1 = [r for r in live if r.get("type") == "ExposureAssessment" and r.get("raterType") == "v1-analyst"]
    assert v1 and not [r["id"] for r in v1 if v2_fields & set(r)]


def test_m8_schema_rejects_a_mapped_v1_deployment_mode():
    r = valid("ExposureAssessment", raterType="v1-analyst", raterId="v1-analyst-01", confidence="low", evidenceLabel="S",
              v1Values={"auto_type": "A"}, v1Flags=[])
    r.pop("technicalExposure", None)
    r["provenance"].update(method="llm-assisted", toolVersion="unknown (v1 sessions)", promptVersion="legacy/v1 working records")
    assert schema_errors(r)                                                      # deploymentMode: assisted is present
    r.pop("deploymentMode")
    assert not schema_errors(r)


def test_m8_exposure_batch_states_its_sample_frame_and_levels_have_ranks(live):
    x = [r for r in live if r.get("instrument") == "emst-exposure@2.0" and r.get("raterType") == "llm"]
    assert x and all("selected on outcome" in r["sampleFrame"] for r in x)
    ex = L.load_yaml(L.VOCAB / "exposure_instrument_v2.yaml")["constructs"]["technical_exposure"]
    ranks = {lv["notation"]: lv["intensityRank"] for lv in ex["levels"]}
    assert sorted(ranks, key=ranks.get) == ex["ordinal_order"]


# ================================================================== M9: one NoTermFound convention; honest X2 status
def test_m9_no_no_term_found_row_asserts_a_positive_predicate():
    for tsv, rows in _sets().items():
        for r in rows:
            if r["object_id"] == "sssom:NoTermFound":
                ok = r["predicate_id"] in validate_v2.NO_OBJECT_PREDICATES or \
                    (r["predicate_id"] in validate_v2.SKOS_PREDICATES and r.get("predicate_modifier") == "Not")
                assert ok, (tsv.name, r.get("record_id") or r["subject_id"], r["predicate_id"])


def test_m9_validator_rejects_a_positive_no_term_found_row(tmp_path):
    data = overlay_tree(tmp_path)
    d = data / "crosswalks" / "fx-set"
    d.mkdir(parents=True)
    (d / "1.sssom.tsv").write_text("record_id\tsubject_id\tpredicate_id\tobject_id\tmapping_justification\tauthor_id\tother\n"
                                   "a\tseed:fx-tsk\tskos:closeMatch\tsssom:NoTermFound\tsemapv:LLMBasedMatching\temstagent:fx@1\treview_status=candidate\n")
    (d / "1.sssom.yml").write_text(L.dump_yaml({"mapping_set_id": "x", "mapping_set_version": "0", "license": "CC0",
                                                "curie_map": {"X": "https://example.org/x/"}}))
    assert "E-SSSOM-NOTERM-POSITIVE" in run(data).codes()


def test_m9_x2_agreement_is_labelled_llm_and_the_set_records_kappa():
    rows = _sets()[L.DATA_V2 / "crosswalks" / "onet-task" / "27.2.sssom.tsv"]
    statuses = {_other(r).get("review_status") for r in rows}
    assert "two-coder-agreed-target" not in statuses and "two-llm-coders-agreed-target" in statuses
    meta = L.load_yaml(L.DATA_V2 / "crosswalks" / "onet-task" / "27.2.sssom.yml")
    assert "kappa_match_type=0.465" in meta["other"] and "gate=fail" in meta["other"]
    real = [r for r in rows if r["object_id"] != "sssom:NoTermFound"]
    agreed = [r for r in real if _other(r).get("review_status") == "two-llm-coders-agreed-target"]
    good = [r for r in agreed if r["predicate_id"] in ("skos:exactMatch", "skos:closeMatch")]
    assert (len(rows), len(real), len(agreed), len(good)) == (316, 202, 153, 16)


# ================================================================== M10: HR views never show sub-closeMatch rows
def _hr_released():
    role = {"id": "emst:core/ROL-FX00001", "type": "RoleProfile", "notation": [{"scheme": "MVPtier", "value": "P1"}],
            "roleLevels": [{"key": "journey", "levelBand": ["L2", "L3"]}], "taskBundle": [], "competencyTargets": [],
            "homeModule": "core", "prefLabel": {"en": "Fixture role"}}
    v1 = {"id": "emst:core/VAR-FX00001", "type": "RoleVariant", "variantOf": role["id"], "sectorActor": "state", "prefLabel": {"en": "v1"}}
    v2 = {"id": "emst:core/VAR-FX00002", "type": "RoleVariant", "variantOf": role["id"], "sectorActor": "local", "prefLabel": {"en": "v2"}}
    scr = {"id": "emst:core/SCR-FX00001", "type": "StateClassRecord", "classCode": "1", "notation": [{"scheme": "class-TX", "value": "1"}],
           "emstMapping": [{"roleVariant": v1["id"], "roleLevel": "journey", "matchType": "skos:closeMatch", "confidence": 0.5},
                           {"roleVariant": v2["id"], "roleLevel": "journey", "matchType": "skos:exactMatch", "confidence": 0.6},
                           {"roleVariant": v1["id"], "roleLevel": "journey", "matchType": "skos:relatedMatch", "confidence": 0.2}]}
    return {r["id"]: r for r in (role, v1, v2, scr)}


def test_m10_state_class_view_lists_every_variant_and_drops_related_matches():
    out = SCV.compute(_hr_released(), {"ruleId": "state-class-view", "ruleVersion": "0.2.0", "buildCommit": "t"})
    doc = out["views/state_class_views/TX--1.json"]
    assert [b["variant"] for b in doc["variants"]] == ["emst:core/VAR-FX00001", "emst:core/VAR-FX00002"]
    assert all("agentConfidence (uncalibrated)" in b["match"] and "confidence" not in b["match"] for b in doc["variants"])
    assert out["views/state_class_views/index.json"]["excludedBelowCloseMatch"] == 1


def test_m10_federal_series_profile_drops_rows_below_close_match():
    rel = {"emst:core/ROL-FX00001": {"id": "emst:core/ROL-FX00001", "type": "RoleProfile", "notation": [{"scheme": "MVPtier", "value": "P1"}],
                                     "roleLevels": [], "taskBundle": [], "competencyTargets": [], "prefLabel": {"en": "r"}},
           "emst:core/VAR-FX00001": {"id": "emst:core/VAR-FX00001", "type": "RoleVariant", "variantOf": "emst:core/ROL-FX00001",
                                     "sectorActor": "federal", "prefLabel": {"en": "v"}},
           "emst:core/SER-FX00001": {"id": "emst:core/SER-FX00001", "type": "SeriesRecord", "seriesCode": "0401", "prefLabel": {"en": "s"}}}
    rows = {"opm-series/x": [{"subject_id": "emst:core/ROL-FX00001", "predicate_id": "skos:relatedMatch", "object_id": "OPMseries:0401",
                              "confidence": "0.2", "other": "review_status=candidate"}]}
    out = FSP.compute(rel, rows, {"ruleId": "federal-series-profile", "ruleVersion": "0.2.0", "buildCommit": "t"}, "2026-10-25")
    assert "views/federal_series_profiles/0401.json" not in out
    assert out["views/federal_series_profiles/index.json"]["excludedBelowCloseMatch"] == 1


# ================================================================== m5: successors name the v1 key they succeed
def test_m5_minor_every_x1_successor_names_its_v1_key(live_by_id):
    for r in _sets()[L.X1_TSV]:
        o = live_by_id.get(r["object_id"])
        if not o or o.get("type") in L.RATING_TYPES:
            continue
        key = r["subject_id"].replace("EMSTv1:", "v1:")
        df = [d.get("v1Key", "") for d in (o.get("provenance") or {}).get("derivedFrom") or []]
        assert any(x == key or x.startswith(key + ":") for x in df), (r["subject_id"], r["object_id"])


# ================================================================== m6: level spans
def test_m6_minor_l5_needs_an_anchor_and_the_basis_is_checked(tmp_path, live):
    for c in (r for r in live if r.get("type") == "Competency" and r.get("status") == "candidate"):
        assert c["levelSpanBasis"] in ("anchored", "declared"), c["id"]
    data = overlay_tree(tmp_path)
    cmp = next((data / "core" / "competencies").glob("CMP-*.yaml"))
    rec = L.load_yaml(cmp)
    rec.update(levelSpan={"min": "L1", "max": "L5"}, levelSpanBasis="anchored")
    L.write_yaml(cmp, rec)
    assert "E-LEVELSPAN-BASIS" in run(data).codes()


# ================================================================== m7: production without review
def test_m7_minor_production_review_lint(tmp_path):
    data = overlay_tree(tmp_path)
    comp = valid("Competency", id="seed:fx-prod", prefLabel={"en": "Produce program reports"})
    L.write_yaml(data / "core" / "competencies" / "seed-fx-prod.yaml", comp)
    text = "Prepare an annual program report summarizing outputs and outcomes for the governing board"
    task = valid("Task", id="seed:fx-prod-t", prefLabel={"en": text}, statement={"en": text}, textSha256=L.text_sha256(text),
                 supports=[{"competency": "seed:fx-prod", "strength": "primary"}])
    L.write_yaml(data / "core" / "tasks" / "seed-fx-prod-t.yaml", task)
    assert "W-LINT-PRODUCTION-REVIEW" in codes_for(run(data), "seed:fx-prod")
    text2 = "Verify an annual program report against the program records before it goes to the governing board"
    L.write_yaml(data / "core" / "tasks" / "seed-fx-prod-r.yaml",
                 valid("Task", id="seed:fx-prod-r", prefLabel={"en": text2}, statement={"en": text2}, textSha256=L.text_sha256(text2),
                       supports=[{"competency": "seed:fx-prod", "strength": "primary"}]))
    assert "W-LINT-PRODUCTION-REVIEW" not in codes_for(run(data), "seed:fx-prod")


def test_m7_minor_the_eight_sampled_competencies_have_a_review_task(live):
    sampled = {"CMP-94MWBXW", "CMP-G0WT56E", "CMP-7JXTB4F", "CMP-YS52BS8", "CMP-PYQADZP", "CMP-BR5Q9TJ", "CMP-H55Y4NM", "CMP-6S8JA64"}
    review = {"review", "verify", "audit"}
    covered = set()
    for t in (r for r in live if r.get("type") == "Task"):
        if t["statement"]["en"].split(" ", 1)[0].lower() in review:
            covered |= {s["competency"].split("/")[-1] for s in t.get("supports") or []}
    assert sampled <= covered


# ================================================================== m8: OBS-4 is human-coded or null
def test_m8_minor_no_self_coded_obs4(tmp_path, live):
    inds = [r for r in live if r.get("type") == "Indicator" and r.get("validationStatus") != "seed-v1"]
    assert inds and all(r["obs4"] is None and r["obs4Draft"]["raterType"] == "llm" for r in inds)
    data = overlay_tree(tmp_path)
    ind = next((data / "core" / "indicators").glob("IND-*.yaml"))
    rec = L.load_yaml(ind)
    rec["obs4"] = 3
    L.write_yaml(ind, rec)
    assert "E-OBS4-SELF-CODED" in run(data).codes()


# ================================================================== m9: source grade, not reliability
def test_m9_minor_role_change_view_says_source_grade():
    from rules import role_change
    sig = {"id": "s", "signalStatus": "watch", "sourceGrade": "B", "reliability": "B"}
    out = role_change._signal(sig)
    assert out["sourceGrade"] == "B" and "reliability" not in out


# ================================================================== m10: no claimed hash without a hash
def test_m10_minor_state_class_records_never_claim_a_missing_hash(tmp_path, live):
    for r in (x for x in live if x.get("type") == "StateClassRecord"):
        for k in ("workDescriptionText", "mqText"):
            v = r.get(k)
            assert not (isinstance(v, dict) and v.get("storage") == "hash-and-url" and not v.get("sha256")), r["id"]
    data = overlay_tree(tmp_path)
    scr = valid("StateClassRecord", workDescriptionText={"storage": "hash-and-url", "url": "https://example.org/x", "sha256": None})
    p = data / "registers" / "state_classes" / "seed-fx-scr.yaml"
    p.parent.mkdir(parents=True, exist_ok=True)
    L.write_yaml(p, scr)
    assert "E-SCR-HASH" in run(data).codes()


# ================================================================== m13: label on the difference, not on overlap
def test_m13_overlapping_intervals_can_hide_a_difference():
    p = L.ROOT / "docs" / "package" / "report" / "figures" / "build_figures.py"
    spec = importlib.util.spec_from_file_location("emst_build_figures", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    import random
    rng = random.Random(5)
    v82 = [rng.random() for _ in range(80)]
    v12 = [0.15 + rng.random() for _ in range(40)]
    i82, i12 = mod.resamples(len(v82), rng, 2000), mod.resamples(len(v12), rng, 2000)
    lo82, hi82 = mod.boot_ci(v82, i82)
    lo12, hi12 = mod.boot_ci(v12, i12)
    lo, hi = mod.diff_ci(v12, i12, v82, i82)
    assert max(lo82, lo12) <= min(hi82, hi12)        # the era intervals overlap ...
    assert lo > 0                                    # ... yet the interval of the difference excludes 0


# ================================================================== m14: the TN queue and held markers
def test_m14_routed_records_are_held_and_no_set_marks_held_variants(live_by_id):
    q = L.load_yaml(L.GOVERNANCE / "tn_review_queue.yaml")
    ids = {i["id"] for i in q["items"]}
    assert ids == {"emst:core/CMP-2VQTX8E", "emst:core/TSK-11X9525", "emst:core/TSK-5ZRM1W1"}
    for rid in ids | set(q["heldByInheritance"]["ids"]):
        r = live_by_id[rid]
        assert r["indigenousDataFlag"] is True and r["approvalStatus"] == "pending-tribal-review", rid
        assert r["sensitivity"] == "restricted-governed", rid
    for tsv, rows in _sets().items():
        assert not [r for r in rows if "held_variants" in _other(r)], tsv.name


def test_m14_validator_rejects_an_unheld_queue_item(tmp_path):
    data = overlay_tree(tmp_path)
    cid = "emst:core/" + next((data / "core" / "competencies").glob("CMP-*.yaml")).stem
    (data / "governance" / "tn_review_queue.yaml").write_text(L.dump_yaml(
        {"items": [{"id": cid, "approval_status": "pending-tribal-review"}]}))
    assert "E-TN-QUEUE" in run(data).codes()


def test_m8_stale_ids_marks_a_rating_whose_task_text_changed():
    from rules import assessment_staleness as ST
    task = {"id": "emst:core/TSK-0000000", "type": "Task", "textSha256": "a" * 64}
    fresh = {"id": "r1", "type": "CraftRating", "task": task["id"], "taskTextSha256": "a" * 64}
    stale = {"id": "r2", "type": "ExposureAssessment", "task": task["id"], "taskTextSha256": "b" * 64}
    assert ST.stale_ids({x["id"]: x for x in (task, fresh, stale)}) == {"r2"}
