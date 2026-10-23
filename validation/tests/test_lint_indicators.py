"""Tests for validation/lint_indicators.py against validation/indicator_lint_rules.yaml (WP-11).

Run: python -m pytest -q validation/tests
The rule file's own examples are the primary oracle: every `fail` example must be flagged by its rule and every
`pass` example must not be. Fixtures in tests/fixtures are synthetic.
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
VAL = HERE.parent
ROOT = VAL.parent
sys.path.insert(0, str(VAL))

import lint_indicators as L  # noqa: E402

RULES = L.load_rules()
SPEC_ORDER = ["internal-state verbs", "level labels as content", "reputation, influence and status",
              "proxies (credentials, training completion, publications, tenure)", "outcome guarantees", "empty verbs",
              "compound performances", "adjective-only gradation",
              "vendor, product, model or technology-family names",
              "hard-coded jurisdiction rules (named statutes, regulations, programmes, orders)", "traits and attitudes",
              "non-job-related access requirements"]


def strip_tag(t: str) -> str:
    return t.split(": ", 1)[1] if t.startswith(("v1: ", "IO-exemplar: ")) else t


@pytest.fixture(scope="module")
def lin():
    return L.Linter(RULES)


def ids_for(lin, text, prefix, rtype="Indicator"):
    return [h.rule_id for h in lin.lint_text(text, rtype) if h.rule_id.startswith(prefix) and h.severity != "info"]


# ------------------------------------------------------------------------------------------- rule file integrity
def test_twelve_banned_constructions_in_spec_order():
    bc = RULES["banned_constructions"]
    assert [r["id"] for r in bc] == [f"B{n:02d}" for n in range(1, 13)]
    assert [r["name"] for r in bc] == SPEC_ORDER


def test_every_regex_compiles_and_has_severity():
    for r in RULES["banned_constructions"]:
        assert r["patterns"], r["id"]
        for p in r["patterns"]:
            assert p["severity"] in {"error", "warn", "info"}
            if "regex" in p:
                re.compile(p["regex"])
        assert r["examples"]["fail"], f"{r['id']} needs fail examples"
        assert r["examples"]["pass"], f"{r['id']} needs pass examples"


# ------------------------------------------------------------------------------------------- rule examples
CASES_FAIL = [(r["id"], strip_tag(t)) for r in RULES["banned_constructions"] for t in r["examples"]["fail"]]
CASES_PASS = [(r["id"], t) for r in RULES["banned_constructions"] for t in r["examples"]["pass"]]


@pytest.mark.parametrize("rule_id,text", CASES_FAIL)
def test_fail_examples_are_flagged(lin, rule_id, text):
    assert ids_for(lin, text, rule_id), f"{rule_id} missed: {text}"


@pytest.mark.parametrize("rule_id,text", CASES_PASS)
def test_pass_examples_are_not_flagged_by_their_rule(lin, rule_id, text):
    assert not ids_for(lin, text, rule_id), f"{rule_id} false positive: {text}"


def _ind(rid, comp, level, text, **kw):
    d = {"type": "Indicator", "id": rid, "competency": comp, "level": level, "statement": {"en": text},
         "augmentationMode": "unaided", "assessmentMethods": ["work sample"], "useClass": "develop", "obs4": 3,
         "jurisdictionVariable": False, "validationStatus": "draft"}
    d.update(kw)
    return L.Record(d, "test")


def test_b08_cross_level_examples(lin):
    b08 = next(r for r in RULES["banned_constructions"] if r["id"] == "B08")
    for ex in b08["examples"]["cross_level_fail"]:
        hits = lin.lint_set([_ind("a", "c", "L1", ex["lower"]), _ind("b", "c", "L2", ex["higher"])])
        assert any(h.rule_id == "B08a" and h.record_id == "b" for h in hits)
    for ex in b08["examples"]["cross_level_pass"]:
        hits = lin.lint_set([_ind("a", "c", "L1", ex["lower"]), _ind("b", "c", "L2", ex["higher"])])
        assert not any(h.rule_id == "B08a" for h in hits)


def test_typing_subset_applies_to_tasks_but_b01_does_not(lin):
    assert ids_for(lin, "Run HEC-RAS to model the floodplain for a restoration reach.", "B09", "Task")
    assert ids_for(lin, "Draft the Section 7 effects determination for a project.", "B10", "Task")
    assert not ids_for(lin, "Understand the floodplain.", "B01", "Task")


def test_tool_class_is_allowed_product_is_not(lin):
    assert not ids_for(lin, "Validates an AI-generated land-cover classification against field plots and records the error matrix.", "B09")
    assert ids_for(lin, "Validates a land-cover classification produced in Google Earth Engine against field plots.", "B09")


def test_external_lexicons_extend_b09_and_b10():
    lin = L.Linter(RULES, extra_products=["AquaTrackPro"], extra_instruments=["Example River Compact"])
    assert ids_for(lin, "Configures AquaTrackPro telemetry for a gauge network.", "B09")
    assert ids_for(lin, "Applies the Example River Compact allocation to a diversion request.", "B10")


# ------------------------------------------------------------------------------------------- publication rules
def test_good_indicator_has_no_failing_hits(lin):
    rec = _ind("g", "c", "L2", "Conducts a point-count survey independently on an assigned route, so that detections, distances and effort meet the protocol's data standard.")
    assert not [h for h in lin.lint_set([rec]) if h.fails]


@pytest.mark.parametrize("kw,text,rule", [
    ({}, "Records detections on a datasheet. Reports anomalies to the crew lead.", "PUB-01"),
    ({}, " ".join(["Records"] + ["word"] * 31) + ".", "PUB-02"),
    ({"augmentationMode": None}, "Records detections on a datasheet so that counts pass QA.", "PUB-03"),
    ({"useClass": "hire"}, "Records detections on a datasheet so that counts pass QA.", "PUB-03"),
    ({"obs4": 1}, "Records detections on a datasheet so that counts pass QA.", "PUB-04"),
    ({"useClass": "select", "obs4": 2}, "Records detections on a datasheet so that counts pass QA.", "PUB-04"),
    ({"assessmentMethods": [], "evidenceTypes": []}, "Records detections on a datasheet so that counts pass QA.", "PUB-03"),
    ({"jurisdictionVariable": False}, "Drafts permit limits that meet the applicable federal, state, Tribal or local requirements.", "PUB-07"),
])
def test_publication_rule_errors(lin, kw, text, rule):
    hits = lin.lint_set([_ind("x", "c", "L2", text, **kw)])
    assert any(h.rule_id == rule and h.severity == "error" for h in hits), [h.rule_id for h in hits]


def test_abbreviation_does_not_split_sentence(lin):
    hits = lin.lint_set([_ind("x", "c", "L1", "Calibrates field meters (e.g. pH and conductivity) before use, recording results against the QA criteria.")])
    assert not any(h.rule_id == "PUB-01" for h in hits)


def test_assisted_without_verification_warns(lin):
    hits = lin.lint_set([_ind("x", "c", "L2", "Drafts a site description from field notes for the planning file.", augmentationMode="assisted")])
    assert any(h.rule_id == "PUB-05" and h.severity == "warn" for h in hits)


def test_unaided_with_ai_output_warns(lin):
    hits = lin.lint_set([_ind("x", "c", "L2", "Reviews AI-generated species identifications against the reference collection.", augmentationMode="unaided")])
    assert any(h.rule_id == "PUB-08" for h in hits)


# ------------------------------------------------------------------------------------------- competency-level rules
def test_fixture_good_set_is_clean():
    recs = L.load_path(HERE / "fixtures" / "good_set.yaml")
    hits = L.Linter(RULES, "release").lint_set(recs)
    assert not [h for h in hits if h.fails], [(h.record_id, h.rule_id, h.match) for h in hits if h.fails]


def test_fixture_bad_set_seeded_violations():
    recs = L.load_path(HERE / "fixtures" / "bad_set.yaml")
    hits = L.Linter(RULES, "release").lint_set(recs)
    got = {(h.record_id, h.rule_id) for h in hits if h.fails}
    assert ("seed:fx-bad-1", "B01a") in got
    assert ("seed:fx-bad-1", "PUB-04") in got
    assert ("seed:fx-bad-2", "B10b") in got
    assert ("seed:fx-bad-2", "PUB-13") in got            # L4 outside span L1-L2
    assert ("seed:fixture-cmp-bad", "PUB-10") in got     # one indicator at L2
    assert ("seed:fixture-cmp-bad", "PUB-14") in got     # consensus/existence claimed without human evidence
    assert ("seed:fixture-tsk-bad", "B09a") in got       # product in task text (T-4)


def test_pub14_accepts_human_evidence(lin):
    comp = L.Record({"type": "Competency", "id": "c", "status": "draft", "levelSpan": {"min": "L1", "max": "L2"},
                     "levels": [{"level": "L1", "indicators": ["a", "b"], "publicationRuleChecks": {"consensus": "pass"}}]}, "t")
    a = _ind("a", "c", "L1", "Records detections on a datasheet so that counts pass QA.", validationStatus="panel-retained")
    b = _ind("b", "c", "L1", "Labels recorder media following the custody procedure so that files trace to a station.")
    assert not any(h.rule_id == "PUB-14" for h in lin.lint_set([comp, a, b]))


def test_pub12_warns_in_ci_and_fails_in_release_for_published():
    comp = {"type": "Competency", "id": "c", "status": "published", "levelSpan": {"min": "L1", "max": "L2"},
            "levels": [{"level": "L1", "indicators": ["a", "b"]}]}
    a = _ind("a", "c", "L1", "Records detections on a datasheet so that counts pass QA.", obs4=2)
    b = _ind("b", "c", "L1", "Labels recorder media following the custody procedure so that files trace to a station.", obs4=2)
    ci = L.Linter(RULES, "ci").lint_set([L.Record(comp, "t"), a, b])
    rel = L.Linter(RULES, "release").lint_set([L.Record(comp, "t"), a, b])
    assert any(h.rule_id == "PUB-12" and not h.fails for h in ci)
    assert any(h.rule_id == "PUB-12" and h.fails for h in rel)


# ------------------------------------------------------------------------------------------- waivers and modes
def _waiver(rid, rule, text, cls, r1="rev-0007", r2=""):
    return {"record_id": rid, "rule_id": rule, "text_sha256": L.text_sha256(text), "waiver_class": cls,
            "reviewer": r1, "second_reviewer": r2, "decided_on": "2026-10-23", "rationale": "test"}


def test_select_indicator_with_warning_fails_only_in_release():
    text = "Prepares a comprehensive stormwater inspection report that cites the evidence for each finding."
    recs = [_ind("s", "c", "L2", text, useClass="select")]
    assert not [h for h in L.Linter(RULES, "ci").lint_set(recs) if h.fails]
    assert [h for h in L.Linter(RULES, "release").lint_set(recs) if h.fails]


def test_warning_waiver_by_human_clears_release_failure():
    text = "Prepares a comprehensive stormwater inspection report that cites the evidence for each finding."
    recs = [_ind("s", "c", "L2", text, useClass="select")]
    w = [_waiver("s", "B08b", text, "accepted-warning")]
    assert not [h for h in L.Linter(RULES, "release", w).lint_set(recs) if h.fails]


def test_waiver_rules_for_errors_agents_and_edits():
    text = "Prepares a Phase I ESA report for a parcel that documents each recognized environmental condition."
    recs = [_ind("e", "c", "L2", text)]
    one = [_waiver("e", "B10b", text, "accepted-warning")]
    assert [h for h in L.Linter(RULES, "ci", one).lint_set(recs) if h.fails], "errors need false-positive + 2 reviewers"
    two = [_waiver("e", "B10b", text, "false-positive", "rev-0007", "rev-0011")]
    assert not [h for h in L.Linter(RULES, "ci", two).lint_set(recs) if h.rule_id == "B10b" and h.fails]
    agent = [_waiver("e", "B10b", text, "false-positive", "llm-run-3", "rev-0011")]
    assert [h for h in L.Linter(RULES, "ci", agent).lint_set(recs) if h.fails], "agents cannot sign waivers"
    edited = [_ind("e", "c", "L2", text + " ")]  # whitespace-only edit keeps the hash (normalized)
    assert not [h for h in L.Linter(RULES, "ci", two).lint_set(edited) if h.rule_id == "B10b" and h.fails]
    changed = [_ind("e", "c", "L2", text.replace("parcel", "property"))]
    assert [h for h in L.Linter(RULES, "ci", two).lint_set(changed) if h.fails], "text change voids the waiver"


# ------------------------------------------------------------------------------------------- CLI
def _cli(*args):
    return subprocess.run([sys.executable, str(VAL / "lint_indicators.py"), *args], capture_output=True, text=True)


def test_cli_exit_codes_and_json():
    assert _cli(str(HERE / "fixtures" / "good_set.yaml"), "--mode", "release").returncode == 0
    bad = _cli(str(HERE / "fixtures" / "bad_set.yaml"), "--json")
    assert bad.returncode == 1
    report = json.loads(bad.stdout)
    assert report["summary"]["failing"] > 0
    assert _cli(str(HERE / "fixtures" / "missing.yaml")).returncode == 2


def test_cli_reads_csv(tmp_path):
    p = tmp_path / "sheet.csv"
    with open(p, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["indicator_id", "competency", "level", "text", "augmentationMode", "assessmentMethods", "useClass", "obs4", "jurisdictionVariable", "validationStatus"])
        w.writerow(["seed:csv-1", "c", "L1", "Shapes understanding of ecosystem theory", "unaided", "interview", "develop", "0", "false", "draft"])
    r = _cli(str(p), "--json")
    assert r.returncode == 1 and "B03a" in r.stdout


# ------------------------------------------------------------------------------------------- regression on IO material
EXEMPLARS = ROOT / "docs" / "research" / "io-validation" / "exemplar_rewrites.csv"
V1_CODED = ROOT / "docs" / "research" / "io-validation" / "v1_observability_ratings.csv"


@pytest.mark.skipif(not EXEMPLARS.exists(), reason="IO Phase 2 exemplars not present")
def test_io_exemplars_only_known_compounds_error(lin):
    """Phase 2 IO exemplar rewrites are the positive reference set. Two are genuine compounds the lint found
    ('Selects and sequences…', 'Calibrates and verifies…'); they are to be split when migrated (WP-03/WP-04).
    If they are fixed upstream, update KNOWN."""
    KNOWN = {"Selects and sequences", "Calibrates and verifies"}
    errs = set()
    for row in csv.DictReader(open(EXEMPLARS, encoding="utf-8")):
        if any(h.severity == "error" for h in lin.lint_text(row["v2_indicator"])):
            errs.add(" ".join(row["v2_indicator"].split()[:3]))
    assert errs == KNOWN, errs


@pytest.mark.skipif(not V1_CODED.exists(), reason="v1 OBS-4 coded sample not present")
def test_screen_is_directional_on_v1_development_data(lin):
    """Development check only: the v1 OBS-4 codes are single-coder agent ratings (raterType llm-equivalent,
    evidence label S), so this is not a validation of the lint. It asserts the screen flags code-0/1 statements
    far more often than code-2/3 statements. Figures are computed here, never typed into documents."""
    flagged = {"low": [0, 0], "high": [0, 0]}
    for row in csv.DictReader(open(V1_CODED, encoding="utf-8")):
        k = "low" if row["score"] in ("0", "1") else "high"
        flagged[k][1] += 1
        flagged[k][0] += any(h.severity == "error" for h in lin.lint_text(row["text"]))
    low = flagged["low"][0] / flagged["low"][1]
    high = flagged["high"][0] / flagged["high"][1]
    assert low > 0.6 and high < 0.25 and low - high > 0.4, (low, high)
