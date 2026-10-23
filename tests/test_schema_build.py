"""WP-01: the schema is generated from vocab/, is valid 2020-12, and accepts/rejects one fixture per entity type."""
from __future__ import annotations

import json

import pytest
from jsonschema import Draft202012Validator

from conftest import FIXTURES, L

import build_schema

SCHEMA = json.loads(L.SCHEMA_OUT.read_text(encoding="utf-8"))
V = Draft202012Validator(SCHEMA)
ENTITY_TYPES = SCHEMA["$defs"]["v_entityType"]["enum"]

# the seeded violation each invalid fixture carries, and a fragment of the error it must raise
EXPECTED = {
    "VocabularyTerm": "'inScheme' is a required property",
    "Competency": "craftBlend",
    "Indicator": "obs4",
    "Enactment": "'authorityBasis' is a required property",
    "Task": "WF-NOTAFUNCTION",
    "KnowledgeStatement": "'statement' is a required property",
    "RoleProfile": "is a required property",
    "RoleVariant": "does not contain items matching",
    "JobFamily": "members",
    "Pathway": "recommended-route",
    "Tool": "",
    "ExposureAssessment": "'deploymentEvidence' is a required property",
    "CraftRating": "3 is not one of",
    "FunctionRating": "'taskTextSha256' is a required property",
    "RelevanceRating": "v1-family",
    "ChangeSignal": "False was expected",
    "WatchItem": "'highPriority' is a required property",
    "Instrument": "should be non-empty",
    "DriverEvent": "rumoured",
    "FrictionRecord": "'indigenousDataFlag' is a required property",
    "Credential": "'date' is a required property",
    "SeriesRecord": "realigned",
    "StateClassRecord": "'mqText' is a required property",
    "Mapping": "owl:sameAs",
    "LearningResource": "should be non-empty",
    "Bundle": "clos",
    "Source": "Great",
    "ChangeRecord": "'evidence' is a required property",
}


def test_all_19_vocab_files_load_and_generate_enums():
    files = sorted(p.name for p in L.VOCAB.glob("*.yaml"))
    assert len(files) == 19
    enums = build_schema.generate_enums()
    sources = {e["source"].split("#")[0].split(" ")[0] for e in enums.values()}
    assert sources == set(files)
    for name, e in enums.items():
        assert e["enum"], name
        assert SCHEMA["$defs"][name]["enum"] == e["enum"], f"{name} stale in emst.schema.json"


def test_schema_and_context_are_current():
    assert build_schema.main(["--check"]) == 0


def test_schema_is_valid_2020_12():
    Draft202012Validator.check_schema(SCHEMA)
    assert SCHEMA["$schema"] == "https://json-schema.org/draft/2020-12/schema"


def test_yaml_12_booleans_keep_vocabulary_codes():
    assert SCHEMA["$defs"]["v_formationDependency"]["enum"] == ["yes", "partial", "no"]
    assert L.load_yaml_text("x: [yes, no, on, off]")["x"] == ["yes", "no", "on", "off"]


def test_id_pattern_generated_from_vocab():
    assert SCHEMA["$defs"]["EmstId"]["pattern"] == L.load_yaml(L.VOCAB / "identifiers.yaml")["form"]["regex"]


def test_every_entity_type_has_a_def_and_both_fixtures():
    assert len(ENTITY_TYPES) == 28
    for t in ENTITY_TYPES:
        assert t in SCHEMA["$defs"], t
        assert (FIXTURES / "records" / "valid" / f"{t}.yaml").exists(), t
        assert (FIXTURES / "records" / "invalid" / f"{t}.yaml").exists(), t
    assert set(EXPECTED) == set(ENTITY_TYPES)


@pytest.mark.parametrize("etype", ENTITY_TYPES)
def test_valid_fixture_passes(etype):
    rec = L.load_yaml(FIXTURES / "records" / "valid" / f"{etype}.yaml")
    errs = [e.message for e in V.iter_errors(rec)]
    assert errs == []


@pytest.mark.parametrize("etype", ENTITY_TYPES)
def test_invalid_fixture_fails_for_its_seeded_reason(etype):
    rec = L.load_yaml(FIXTURES / "records" / "invalid" / f"{etype}.yaml")
    errs = list(V.iter_errors(rec))
    assert errs, f"{etype} invalid fixture unexpectedly validates"
    text = " | ".join(e.message for e in errs) + " | " + " | ".join(str(list(e.absolute_path)) for e in errs)
    assert EXPECTED[etype] in text


def test_unknown_field_rejected_closed_objects():
    rec = L.load_yaml(FIXTURES / "records" / "valid" / "Task.yaml")
    rec["exposureSummary"] = {"modal": "A"}
    assert any("exposureSummary" in e.message for e in V.iter_errors(rec))


def test_seed_v1_relaxation_and_full_requirements():
    rec = L.load_yaml(FIXTURES / "records" / "valid" / "Competency.yaml")
    for f in ("competencyType", "levelSpan", "definition", "lifecycleState"):
        rec.pop(f)
    assert list(V.iter_errors(rec)), "authored competency must carry the full field set"
    rec["validationStatus"] = "seed-v1"
    assert [e.message for e in V.iter_errors(rec)] == []


def test_context_has_a_term_for_every_property():
    ctx = json.loads(L.CONTEXT_OUT.read_text(encoding="utf-8"))["@context"]
    for t in ENTITY_TYPES:
        if t == "Mapping":
            continue
        props = {}
        for part in [SCHEMA["$defs"][t]] + [SCHEMA["$defs"]["RecordBase"]]:
            props.update(part.get("properties", {}))
        for p in props:
            if p not in ("id", "type"):
                assert p in ctx, f"{t}.{p} has no JSON-LD term"
