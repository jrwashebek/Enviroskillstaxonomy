"""The DE draft v2 record schema accepts well-formed migrated records and rejects each class of v1 drift.

Run: python -m pytest -q tests/test_proposed_schema.py
Schema: docs/research/data-engineering/proposed/emst-record.schema.json (DRAFT; see report.md section 6).
Each negative case reproduces a defect found in the v1 audit (docs/audit/data-audit.md).
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path

import pytest

jsonschema = pytest.importorskip("jsonschema")

ROOT = Path(__file__).resolve().parents[1]
PROP = ROOT / "docs" / "research" / "data-engineering" / "proposed"
SCHEMA = json.loads((PROP / "emst-record.schema.json").read_text())
EXAMPLES = json.loads((PROP / "examples.json").read_text())
V = jsonschema.Draft202012Validator(SCHEMA)


def errors(rec):
    return list(V.iter_errors(rec))


def by_type(t):
    return copy.deepcopy(next(r for r in EXAMPLES if r["type"] == t))


def test_schema_is_valid_2020_12():
    jsonschema.Draft202012Validator.check_schema(SCHEMA)


@pytest.mark.parametrize("rec", EXAMPLES, ids=lambda r: r["type"])
def test_examples_validate(rec):
    assert errors(rec) == []


def test_task_hash_is_real_and_cited_by_assessment():
    t, a = by_type("task"), by_type("exposure_assessment")
    norm = re.sub(r"\s+", " ", t["statement"].strip())
    assert hashlib.sha256(norm.encode()).hexdigest() == t["text_sha256"] == a["task_text_sha256"]


def test_derived_from_points_at_the_baseline_workbook():
    info = json.loads((ROOT / "data" / "v1_baseline" / "BUILD_INFO.json").read_text())
    sha = info["inputs"][0]["sha256"]
    for r in EXAMPLES:
        for d in r["derived_from"]:
            assert d["v1_workbook_sha256"] == sha


# --- negative cases: each is a v1 failure mode -------------------------------------------------------
def test_rejects_yes_no_boolean():                       # audit section 4: 160 Yes/No cells
    a = by_type("exposure_assessment")
    a["values"]["s_trajectory"] = "No"
    assert errors(a)


def test_rejects_undocumented_cld_severity():           # 'Highest' / 'Ungraded'
    a = by_type("exposure_assessment")
    a["values"]["cld_severity"] = "Highest"
    assert errors(a)


def test_rejects_stored_modal_or_count_fields():        # section 1.6 / C03: derived values must be computed
    c = by_type("competency")
    c["modal_automation_type"] = "Ac"
    assert errors(c)
    c = by_type("competency")
    c["supporting_family_count"] = 10
    assert errors(c)


def test_rejects_h_with_ai_vector():                    # C11: 4.4.2 T2, 4.6.1 T2, 4.7.2 T3
    a = by_type("exposure_assessment")
    a["values"].update(automation_type="H", vector="AI", horizon="2")
    assert errors(a)


def test_rejects_migration_without_derived_from():      # provenance must survive migration
    t = by_type("task")
    del t["derived_from"]
    assert errors(t)


def test_rejects_evidence_label_without_source():       # team brief section 3
    t = by_type("task")
    t["provenance"]["source_ids"] = []
    assert errors(t)


def test_rejects_free_text_provenance_method():         # 'D6 exposure file, reconciled March 2026'
    t = by_type("task")
    t["provenance"]["method"] = "D6 exposure file, reconciled March 2026"
    assert errors(t)


def test_rejects_assessment_without_task_text_hash():   # section 7: D1/D3 classified different text
    a = by_type("exposure_assessment")
    del a["task_text_sha256"]
    assert errors(a)


def test_rejects_superseded_without_successor():
    c = by_type("competency")
    c["status"] = "superseded"
    assert errors(c)


def test_rejects_v1_code_as_id():                       # D.SA.N codes are aliases, never IDs
    c = by_type("competency")
    c["id"] = "1.1.1"
    assert errors(c)
