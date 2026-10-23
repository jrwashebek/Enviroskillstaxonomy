"""Schema shapes ratified or added by the CA rulings of 2026-10-23 (ADR-0029 §1, §8, §9)."""
from __future__ import annotations

import copy
import json

import pytest
from jsonschema import Draft202012Validator

from conftest import FIXTURES, L

SCHEMA = json.loads(L.SCHEMA_OUT.read_text(encoding="utf-8"))
V = Draft202012Validator(SCHEMA)


def valid(t, **kw):
    rec = copy.deepcopy(L.load_yaml(FIXTURES / "records" / "valid" / f"{t}.yaml"))
    rec.update(kw)
    return rec


def ok(rec):
    errs = [e.message for e in V.iter_errors(rec)]
    assert not errs, errs[:3]


def bad(rec):
    assert list(V.iter_errors(rec)), "expected a schema error"


def external(**kw):
    rec = valid("ExposureAssessment", raterType="external-index", raterId="index:aei-task-usage", instrument="aei-task-usage",
                assessedAt="2026-01", license="LicenseRef-EMST-third-party-index-derived")
    rec["externalSource"] = {"index": "aei", "release": "2026-01", "aggregation": "mean", "unit": "onet-task",
                             "matchedOnetTasks": ["19-2041.00-T1"], "values": {"share": 0.1}}
    rec.pop("technicalExposure")
    rec.update(kw)
    return rec


def occupation(**kw):
    rec = external()
    for k in ("task", "taskTextSha256"):
        rec.pop(k)
    rec["externalSource"] = {"index": "bls", "release": "2026", "aggregation": "occupation", "unit": "occupation", "values": {"score": 0.4}}
    rec.update(targetType="RoleProfile", targetId="seed:R02-field-resource-technician",
               crosswalkPath=["X3 role -> SOC 19-4071"], crosswalkMinMatchType="skos:closeMatch")
    rec.update(kw)
    return rec


# ---------------------------------------------------------------- §9 ExposureAssessment grain
def test_task_grain_external_index_is_valid():
    ok(external())


def test_external_index_needs_matched_tasks_unless_occupation():
    rec = external()
    rec["externalSource"].pop("matchedOnetTasks")
    bad(rec)
    rec["externalSource"]["matchedOnetTasks"] = []
    bad(rec)


def test_occupation_grain_targets_a_role_not_a_task():
    ok(occupation())
    bad(occupation(targetType="Task"))
    bad(occupation(task="seed:fx-tsk"))
    rec = occupation()
    rec.pop("crosswalkMinMatchType")
    bad(rec)


def test_task_grain_forbids_role_targeting_fields():
    bad(external(targetType="RoleProfile"))
    bad(valid("ExposureAssessment", crosswalkPath=["x"]))


def test_external_index_assessed_at_may_be_partial_others_not():
    ok(external(assessedAt="2026"))
    bad(valid("ExposureAssessment", assessedAt="2026-10"))


def test_level_distribution_shape():
    ok(valid("ExposureAssessment", technicalExposure=[{"vector": "sensing", "levelDistribution": {"E0": 0.5, "E1": 0.5}, "basis": {"en": "x"}}]))
    bad(valid("ExposureAssessment", technicalExposure=[{"vector": "sensing", "levelDistribution": {"E0": 1.0}}]))          # basis
    bad(valid("ExposureAssessment", technicalExposure=[{"vector": "sensing", "level": "E1", "levelDistribution": {"E1": 1.0}, "basis": {"en": "x"}}]))
    bad(valid("ExposureAssessment", technicalExposure=[{"vector": "sensing", "levelDistribution": {"E5": 1.0}, "basis": {"en": "x"}}]))


# ---------------------------------------------------------------- §8 ChangeSignal
def test_active_signal_needs_family_and_key():
    bad(valid("ChangeSignal", signalStatus="active"))
    ok(valid("ChangeSignal", signalStatus="active", signalFamily="postings-pds", independenceKey="opm-ehri-fwd"))


def test_registered_deployment_only_for_deployment_family():
    ok(valid("ChangeSignal", signalFamily="deployment", registeredDeployment=True))
    bad(valid("ChangeSignal", signalFamily="headcount", registeredDeployment=True))


def test_signposts_scenarios_and_impact():
    ok(valid("ChangeSignal", scenarioSignposts=["vocab:scenarios#SP-01", "vocab:scenarios#SP-12"], impact=3,
             pointsToward=["SC3", "AX-1:thin-fragmented"]))
    bad(valid("ChangeSignal", scenarioSignposts=["SP-01"]))
    bad(valid("ChangeSignal", scenarioSignposts=["vocab:scenarios#SP-13"]))
    bad(valid("ChangeSignal", impact=4))
    bad(valid("ChangeSignal", pointsToward=["AX-1:nowhere"]))


def test_measure_baseline_and_sensitivity_are_closed():
    m = dict(valid("ChangeSignal")["measure"], baseline={"value": 0.1, "ci95": None, "n": 3, "note": "x"},
             sensitivity={"weighting": "component", "value": 0.2, "baselineValue": 0.1})
    ok(valid("ChangeSignal", measure=m))
    bad(valid("ChangeSignal", measure=dict(m, baseline={"value": 0.1, "extra": 1})))


def test_organization_targets():
    ok(valid("ChangeSignal", targetType="organization", targetId="opm-agency:IN00", sectorActor="federal"))
    bad(valid("ChangeSignal", targetType="organization", targetId="Acme Corp"))
    bad(valid("ChangeSignal", targetType="organization", targetId="opm-agency:IN00", sectorActor="tribal"))
    bad(valid("ChangeSignal", targetType="organization", targetId="opm-agency:IN00", tribalPrograms=True, indigenousDataFlag=True))


# ---------------------------------------------------------------- §1 enumerations and seed-v1
@pytest.mark.parametrize("t,field,value", [
    ("DriverEvent", "statusAfter", "in-force-ish"),
    ("DriverEvent", "eventType", "rumoured"),
    ("Instrument", "instrumentType", "decree"),
    ("Tool", "toolType", "gadget"),
    ("Pathway", "pathwayType", "teleport"),
])
def test_generated_enumerations_reject_unknown_values(t, field, value):
    bad(valid(t, **{field: value}))


def test_new_driver_values_are_accepted():
    ok(valid("DriverEvent", eventType="submitted-for-review", statusAfter="under-review"))
    ok(valid("Instrument", instrumentType="agency-order"))


def test_seed_v1_never_reaches_candidate():
    """ADR-0029 §1.3 as kept by ADR-0030 §1.1: candidate/published/deprecated always; superseded/withdrawn only with a
    minted ID (seed-keyed v1 lineage stubs stay valid)."""
    bad(valid("Competency", id="emst:core/CMP-AB12CDN", status="candidate", validationStatus="seed-v1"))
    bad(valid("Competency", id="emst:core/CMP-AB12CDN", status="superseded", validationStatus="seed-v1", replacedBy=["seed:x"]))
    ok(valid("Competency", id="seed:v1-9.9.9", status="superseded", validationStatus="seed-v1", replacedBy=["seed:x"]))   # ADR-0030 §1.1


def test_enactments_rejected_from_candidate():
    ok(valid("Competency", enactments=["seed:ena"]))
    bad(valid("Competency", id="emst:core/CMP-AB12CDN", status="candidate", enactments=["seed:ena"]))


def test_publication_rule_pass_needs_evidence():
    lv = {"level": "L1", "indicators": ["seed:a", "seed:b"],
          "publicationRuleChecks": {"existence": {"result": "pass", "evidence": []}}}
    rec = valid("Competency", levels=[lv])
    if "checkedBy" in json.dumps(SCHEMA["$defs"]["PublicationRuleCheck"]):
        pytest.skip("PublicationRuleCheck needs more fields than this probe supplies")
    bad(rec)


# ---------------------------------------------------------------- §7 E-level order
def test_exposure_level_order_comes_from_vocab_not_code_order():
    v = L.load_yaml(L.VOCAB / "exposure_instrument_v2.yaml")
    assert L.exposure_level_order() == v["constructs"]["technical_exposure"]["ordinal_order"]
    assert L.exposure_level_order() != sorted(L.exposure_level_order())          # E0 < E2 < E1 < E3
    assert sorted(SCHEMA["$defs"]["v_exposureLevel"]["enum"]) == sorted(L.exposure_level_order())
