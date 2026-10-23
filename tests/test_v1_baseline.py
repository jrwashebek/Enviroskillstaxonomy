"""Tests for the normalized v1 baseline (data/v1_baseline/), produced by scripts/extract_v1.py.

Run: python -m pytest -q tests/test_v1_baseline.py

What is pinned here:
- shape: row counts, one-to-many cardinalities (3 tasks, 4 levels, 5 sector notes per competency);
- identity: key uniqueness and key format;
- vocabulary: every coded value is in the documented v1 vocabulary or in the explicit
  `observed_undocumented` list (so a new undocumented value fails the build);
- referential integrity between tables;
- provenance: BUILD_INFO input hashes match the files on disk; the build is deterministic;
- known v1 defects, pinned at their audited counts so a silent change in the extract is caught
  (see docs/audit/data-audit.md).
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "v1_baseline"
LEGACY_DATA = ROOT / "legacy" / "v1" / "data"


def load(name):
    with (BASE / f"{name}.csv").open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


@pytest.fixture(scope="module")
def t():
    names = ["structure", "competencies", "tasks", "proficiency", "indicators", "craft_stage_reform",
             "family_assignments", "ethical_lenses", "exposure_summary", "exposure_sources", "sector_applications",
             "labor_market_crosswalk", "workforce_signals", "data_dictionary", "vocabularies", "normalization_log"]
    return {n: load(n) for n in names}


@pytest.fixture(scope="module")
def vocab(t):
    v = defaultdict(dict)
    for r in t["vocabularies"]:
        v[r["vocabulary"]][r["code"]] = r["status"]
    return v


# ----------------------------------------------------------------------------- shape
EXPECTED_ROWS = {
    "competencies": 222, "tasks": 666, "proficiency": 888, "craft_stage_reform": 222, "exposure_summary": 222,
    "sector_applications": 1110, "structure": 7 + 45, "labor_market_crosswalk": 15, "family_assignments": 1002,
    "ethical_lenses": 20, "indicators": 4852,
}


@pytest.mark.parametrize("name,n", sorted(EXPECTED_ROWS.items()))
def test_row_counts(t, name, n):
    assert len(t[name]) == n


def test_structure_counts(t):
    lv = Counter(r["level"] for r in t["structure"])
    assert lv == {"domain": 7, "skill_area": 45}
    per_domain = Counter(r["domain_num"] for r in t["competencies"])
    assert per_domain == {"1": 40, "2": 35, "3": 35, "4": 35, "5": 30, "6": 40, "7": 7}
    assert all(r["summary_sheet_consistent"] == "true" for r in t["structure"] if r["level"] == "skill_area")


def test_cardinalities(t):
    for table, n in (("tasks", 3), ("proficiency", 4), ("sector_applications", 5)):
        c = Counter(r["competency_key"] for r in t[table])
        assert set(c.values()) == {n}, table
        assert len(c) == 222


def test_indicator_counts_per_level(t):
    n = Counter(r["proficiency_key"] for r in t["indicators"])
    assert max(n.values()) == 6                      # v1 import cap (source text has up to 12)
    assert min(n.values()) == 3
    for p in t["proficiency"]:
        assert int(p["n_indicators"]) == n[p["key"]]


# ----------------------------------------------------------------------------- identity
KEY_PATTERNS = {
    "competencies": r"^v1:[1-7]\.\d{1,2}\.\d{1,2}$",
    "tasks": r"^v1:[1-7]\.\d{1,2}\.\d{1,2}:T[123]$",
    "proficiency": r"^v1:[1-7]\.\d{1,2}\.\d{1,2}:(foundational|intermediate|advanced|expert)$",
    "indicators": r"^v1:[1-7]\.\d{1,2}\.\d{1,2}:(foundational|intermediate|advanced|expert):I[1-6]$",
    "family_assignments": r"^v1:[1-7]\.\d{1,2}\.\d{1,2}:F([1-9]|1[0-5])$",
    "ethical_lenses": r"^v1:[1-7]\.\d{1,2}\.\d{1,2}:L[1-5]$",
    "sector_applications": r"^v1:[1-7]\.\d{1,2}\.\d{1,2}:sector:[a-z_]+$",
    "structure": r"^v1:[1-7](\.\d{1,2})?$",
    "craft_stage_reform": r"^v1:[1-7]\.\d{1,2}\.\d{1,2}$",
    "exposure_summary": r"^v1:[1-7]\.\d{1,2}\.\d{1,2}$",
}


@pytest.mark.parametrize("name", sorted(KEY_PATTERNS))
def test_keys_unique_and_well_formed(t, name):
    keys = [r["key"] for r in t[name]]
    assert len(keys) == len(set(keys)), f"duplicate keys in {name}"
    bad = [k for k in keys if not re.match(KEY_PATTERNS[name], k)]
    assert not bad, bad[:5]


@pytest.mark.parametrize("name", ["exposure_sources", "labor_market_crosswalk", "workforce_signals",
                                  "data_dictionary"])
def test_other_keys_unique(t, name):
    keys = [r["key"] for r in t[name]]
    assert len(keys) == len(set(keys))


def test_codes_match_keys(t):
    for name in ("competencies", "tasks", "proficiency", "indicators", "craft_stage_reform", "exposure_summary"):
        for r in t[name]:
            assert r["key"].split(":")[1] == r["code"]


# ----------------------------------------------------------------------------- vocabulary
def _check(vocab, voc, values, allow_blank=False):
    allowed = set(vocab[voc])
    bad = [v for v in values if not (allow_blank and v == "") and v not in allowed]
    assert not bad, f"{voc}: {Counter(bad).most_common(5)}"


def test_vocab_crafts_stages_tiers(t, vocab):
    csr = t["craft_stage_reform"]
    _check(vocab, "craft", [r["craft_primary"] for r in csr])
    _check(vocab, "craft", [r["craft_secondary"] for r in csr], allow_blank=True)
    for col in ("stage_primary_1", "stage_primary_2", "stage_secondary_1", "stage_secondary_2"):
        _check(vocab, "stage", [r[col] for r in csr], allow_blank=(col != "stage_primary_1"))
    _check(vocab, "stability_tier", [r["stability_tier"] for r in csr])
    for r in csr:
        for col in [c for c in r if c.startswith("reform_") and c != "reform_flag_count"] + \
                   ["dual_primary_exception", "foundational_professional_prep", "zero_core"]:
            assert r[col] in ("true", "false"), (r["key"], col, r[col])


def test_vocab_families_lenses(t, vocab):
    _check(vocab, "family_assignment", [r["assignment"] for r in t["family_assignments"]])
    _check(vocab, "family", [r["family_code"] for r in t["family_assignments"]])
    _check(vocab, "lens_value", [r["value"] for r in t["ethical_lenses"]])
    _check(vocab, "lens", [r["lens_code"] for r in t["ethical_lenses"]])


def test_vocab_task_exposure(t, vocab):
    for col in ("auto_type", "tacit_density", "career_ladder", "vector", "horizon"):
        _check(vocab, col, [r[col] for r in t["tasks"]])
    _check(vocab, "exposure_provenance", [r["exposure_provenance"] for r in t["tasks"]])


def test_vocab_exposure_summary(t, vocab):
    ex = t["exposure_summary"]
    _check(vocab, "cld_severity", [r["cld_severity"] for r in ex], allow_blank=True)
    for col, voc in (("modal_auto_type", "auto_type"), ("modal_tacit_density", "tacit_density"),
                     ("modal_career_ladder", "career_ladder"), ("modal_vector", "vector"),
                     ("modal_horizon", "horizon")):
        _check(vocab, voc, [r[col] for r in ex])
    for col in ("cld_flag", "s_trajectory_flag", "modal_cld_flag", "modal_contested"):
        assert {r[col] for r in ex} <= {"true", "false"}


def test_undocumented_values_are_exactly_the_audited_ones(t, vocab):
    sev = Counter(r["cld_severity"] for r in t["exposure_summary"] if vocab["cld_severity"].get(r["cld_severity"])
                  == "observed_undocumented")
    assert sev == {"Highest": 4, "Ungraded": 4}
    prov = Counter(r["exposure_provenance"] for r in t["exposure_summary"])
    assert prov == {"session_direct": 147, "reconstructed_d2": 35, "d6_exposure_file_reconciled_2026_03": 30,
                    "pre_task_15a_d6_ac_retrospective": 10}


def test_vocab_other(t, vocab):
    _check(vocab, "mapping_quality", [r["mapping_quality"] for r in t["labor_market_crosswalk"]])
    _check(vocab, "sector", [r["sector"] for r in t["sector_applications"]])
    _check(vocab, "proficiency_level", [r["level"] for r in t["proficiency"]])


# ----------------------------------------------------------------------------- referential integrity
def test_referential_integrity(t):
    comp = {r["key"] for r in t["competencies"]}
    struct = {r["key"] for r in t["structure"]}
    prof = {r["key"] for r in t["proficiency"]}
    tasks = {r["key"] for r in t["tasks"]}
    for r in t["competencies"]:
        assert r["domain_key"] in struct and r["skill_area_key"] in struct
        assert r["skill_area_key"].startswith(r["domain_key"] + ".")
    for name in ("tasks", "proficiency", "indicators", "family_assignments", "ethical_lenses", "sector_applications"):
        assert {r["competency_key"] for r in t[name]} <= comp, name
    assert {r["key"] for r in t["craft_stage_reform"]} == comp
    assert {r["key"] for r in t["exposure_summary"]} == comp
    assert {r["proficiency_key"] for r in t["indicators"]} <= prof
    assert {r["task_key"] for r in t["exposure_sources"]} <= tasks
    fams = {r["family_code"] for r in t["labor_market_crosswalk"]}
    assert {r["family_code"] for r in t["family_assignments"]} <= fams
    listed = {c for r in t["structure"] for c in r["competency_codes"].split("|")}
    assert listed == {r["code"] for r in t["competencies"]}


def test_family_counts_match_assignments(t):
    core = Counter(r["competency_key"] for r in t["family_assignments"] if r["assignment"] == "Core")
    sup = Counter(r["competency_key"] for r in t["family_assignments"] if r["assignment"] == "Supporting")
    sup_mismatch = []
    for r in t["craft_stage_reform"]:
        assert int(r["core_family_count"]) == core[r["key"]], r["key"]
        assert (r["zero_core"] == "true") == (core[r["key"]] == 0), r["key"]
        if int(r["supporting_family_count"]) != sup[r["key"]]:
            sup_mismatch.append((r["code"], int(r["supporting_family_count"]) - sup[r["key"]]))
    # Known v1 defect: every Domain 7 row overstates its stored Supporting Family Count by 1-2.
    assert sorted(sup_mismatch) == [("7.1.1", 2), ("7.1.2", 2), ("7.1.3", 1), ("7.1.4", 1), ("7.2.1", 1),
                                    ("7.2.2", 1), ("7.2.3", 2)]


def test_reform_flag_count(t):
    for r in t["craft_stage_reform"]:
        n = sum(r[c] == "true" for c in r if c.startswith("reform_") and c != "reform_flag_count")
        assert int(r["reform_flag_count"]) == n, r["key"]


# ----------------------------------------------------------------------------- provenance & reproducibility
def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def test_build_info_hashes_match_inputs():
    info = json.loads((BASE / "BUILD_INFO.json").read_text())
    assert info["inputs"][0]["role"] == "baseline"
    assert info["inputs"][0]["file"].endswith("Core_V3_reconciled__copyB_aaf34c8c.xlsx")
    for inp in info["inputs"]:
        p = ROOT / inp["file"]
        assert p.exists(), inp["file"]
        assert _sha(p) == inp["sha256"], f"input changed since build: {inp['file']}"
    for out in info["outputs"]:
        assert _sha(BASE / out["file"]) == out["sha256"], f"output edited by hand: {out['file']}"
    assert info["checks"]["profession_family_view_mismatches_vs_dimension_tags"] == 0


def test_build_is_deterministic_and_current():
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "extract_v1.py"), "--check"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_json_matches_csv(t):
    j = json.loads((BASE / "v1_baseline.json").read_text())
    assert len(j["competencies"]) == 222
    assert sum(len(c["tasks"]) for c in j["competencies"]) == 666
    assert sum(len(p["indicators"]) for c in j["competencies"] for p in c["proficiency"]) == len(t["indicators"])
    c0 = j["competencies"][0]
    assert c0["key"] == "v1:1.1.1" and set(c0["sector_applications"]) == {
        "public_agencies", "private_sector", "ngos", "consulting", "academia"}


# ----------------------------------------------------------------------------- pinned v1 defects (audit)
def test_known_defects_pinned(t):
    flags = Counter(f for r in t["competencies"] for f in r["qa_flags"].split("|") if f)
    assert flags["title_contains_description"] == 19
    assert flags["proficiency_statements_missing"] == 30            # all of Domain 5
    assert Counter(r["qa_flag"] for r in t["indicators"] if r["qa_flag"]) == {
        "misparsed_knowledge_line": 120, "misparsed_application_line": 120, "misparsed_indicators_line": 120}
    assert all(r["code"].startswith("5.") for r in t["indicators"] if r["qa_flag"])
    lens_comps = {r["code"] for r in t["ethical_lenses"]}
    assert lens_comps == {"7.1.1", "7.1.2", "7.1.3", "7.1.4"}       # L1-L5 empty for the other 218
    csr = t["craft_stage_reform"]
    assert sum(r["dual_primary_exception"] == "true" for r in csr) == 0   # Data Dictionary documents 5
    assert all(r["stage_primary_2"] == "" for r in csr)


def test_titles_never_blank_and_suggested_split_only_when_flagged(t):
    for r in t["competencies"]:
        assert r["title"]
        assert bool(r["suggested_title"]) == ("title_contains_description" in r["qa_flags"])
        if r["suggested_title"]:
            assert r["title"].startswith(r["suggested_title"]) and r["title"].endswith(r["suggested_description"])


def test_no_import_residue_left_in_text(t):
    pat = re.compile(r"(\bDOMAIN \d:|\bSKILL AREAS\b|DOMAIN-LEVEL|\s[*#]$)")
    for name, cols in (("competencies", ["title", "description"]), ("tasks", ["text"]),
                       ("sector_applications", ["text"]), ("proficiency", ["knowledge", "application"])):
        for r in t[name]:
            for c in cols:
                assert not pat.search(r[c] or ""), (name, r["key"], c)


# ----------------------------------------------------------------------------- source-text cross-check
SRC = BASE / "source_text"


@pytest.mark.skipif(not (SRC / "tasks.csv").exists(), reason="source text not exported yet")
def test_source_text_crosscheck():
    tasks = list(csv.DictReader((SRC / "tasks.csv").open()))
    assert len(tasks) == 645 and all(r["exact_match"] == "true" for r in tasks)   # D1-D6 task text verbatim
    prof = list(csv.DictReader((SRC / "proficiency.csv").open()))
    assert len(prof) == 860
    mism = [r for r in prof if r["knowledge_match"] != "true" or r["application_match"] != "true"]
    assert {r["code"][0] for r in mism} == {"5"} and len(mism) == 120
    sect = list(csv.DictReader((SRC / "sector_applications.csv").open()))
    assert len(sect) == 1075 and all(r["exact_match"] == "true" for r in sect)
    inds = list(csv.DictReader((SRC / "indicators.csv").open()))
    assert len(inds) == 6484
    assert sum(r["in_db_same_position"] == "true" for r in inds) == 4380


# ----------------------------------------------------------------------------- exposure working records
def test_every_task_has_a_working_record(t):
    rec = defaultdict(set)
    for r in t["exposure_sources"]:
        rec[r["task_key"]].add(r["source"])
    assert {k for k in rec} == {r["key"] for r in t["tasks"]}           # all 666 tasks covered
    assert Counter(r["source"] for r in t["exposure_sources"]) == {
        "d1_record": 120, "d2_record": 105, "d3_record": 105, "d4_record": 105, "d5_record": 90, "d5": 90,
        "d6": 120, "pre15a": 30, "d7_record": 21}


def test_exposure_record_alignment_pinned(t):
    by = defaultdict(list)
    for r in t["exposure_sources"]:
        by[r["source"]].append(r)
    agree = {s: sum(r["matches_baseline"] == "true" for r in rows) for s, rows in by.items()}
    assert agree == {"d1_record": 120, "d2_record": 37, "d3_record": 105, "d4_record": 105, "d5_record": 89,
                     "d5": 90, "d6": 102, "pre15a": 24, "d7_record": 21}
    assert sum(r["source_inferred"] == "true" for r in by["d3_record"]) == 98
    # Domain 6 in the baseline = D6 exposure file for SA 6.1, 6.2, 6.4-6.7 exactly
    for r in by["d6"]:
        if not r["task_key"].startswith(("v1:6.3.", "v1:6.8.")):
            assert r["matches_baseline"] == "true", r["task_key"]
    # Pre-Task 15A: all 12 A->Ac reclassifications are present in the baseline
    re12 = [r for r in by["pre15a"] if r["prev_auto_type"] == "A" and r["auto_type"] == "Ac"]
    tk = {x["key"]: x for x in t["tasks"]}
    assert len(re12) == 12 and all(tk[r["task_key"]]["auto_type"] == "Ac" for r in re12)
