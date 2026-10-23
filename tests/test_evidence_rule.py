"""change-indicator@1.0.0 evidence rule (ADR-0028 §2; ADR-0029 §8.3-8.4). Moved from docs/methods/ci/ (LM, WP-10).

1. Every synthetic case in tests/fixtures/evidence_rule_cases.yaml yields its expected decision and reason code.
2. Regression on the real seed: no agent-seeded ChangeSignal under data/v2/signals/ moves any indicator, even if its
   watch signals were counted, and every seeded signal declares a family the vocabulary recognises.
3. The port reads its families, providers and instrument map from the vocabulary and rule file, not constants.
"""
import copy
import json
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402
from rules import change_indicator as ER  # noqa: E402

CASES = ROOT / "tests" / "fixtures" / "evidence_rule_cases.yaml"


def _doc():
    doc = yaml.safe_load(CASES.read_text(encoding="utf-8"))
    assert doc.get("synthetic") is True
    return doc


def _fill(defaults, partial):
    rec = copy.deepcopy(defaults)
    rec.update(copy.deepcopy(partial))
    if rec.get("type") == "ExposureAssessment":
        for k in ("direction", "drivers", "signalStatus"):
            rec.pop(k, None)
    return rec


@pytest.mark.parametrize("case", _doc()["cases"], ids=lambda c: c["id"])
def test_synthetic_case(case):
    doc = _doc()
    ind = case.get("indicator", doc["indicator"])
    res = ER.evaluate(ind, [_fill(doc["defaults"], s) for s in case["signals"]])
    assert res["decision"] == case["expect"], res
    if case.get("reason"):
        assert case["reason"] in res["reasons"], res


def test_reason_codes_are_declared_or_documented():
    rule = L.load_yaml(ROOT / "vocab" / "rules" / "change-indicator@1.0.0.yaml")
    declared = set(rule["reason_codes"]) | {"ER-0-NOT-ACTIVE", "ER-0-ORGANIZATION-TARGET"}   # DE additions, CR-DE-004
    for case in _doc()["cases"]:
        if case.get("reason"):
            assert case["reason"] in declared, case["id"]


def _seeded():
    out = []
    for p in sorted((L.DATA_V2 / "signals").rglob("*.jsonl")):
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
    return out


def test_seed_never_moves_an_indicator():
    recs = _seeded()
    if not recs:
        pytest.skip("no seeded signals")
    for include_watch in (False, True):
        res = ER.evaluate_corpus(recs, kinds=("role-change", "skill-change"), include_watch=include_watch)
        moved = [k for k, v in res.items() if v["decision"] == "moves"]
        assert not moved, moved[:5]


def test_seed_families_and_flags():
    cfg = ER.default_config()
    bad = []
    for r in _seeded():
        fam = ER.family(r, cfg)
        if fam not in cfg.families:
            bad.append((r["id"], "family", fam))
        if r.get("personalData") is not False:
            bad.append((r["id"], "personalData"))
        if not r.get("drivers"):
            bad.append((r["id"], "drivers"))
        if not r.get("sourceRelease"):
            bad.append((r["id"], "sourceRelease"))
        if r.get("tribalPrograms") and not (r.get("indigenousDataFlag") and r.get("sensitivity") == "restricted-governed"):
            bad.append((r["id"], "tribal-quarantine"))
    assert not bad, bad[:10]


def test_config_comes_from_vocabulary():
    cfg = ER.load_config()
    ct = L.load_yaml(ROOT / "vocab" / "change_types.yaml")
    assert cfg.families == {v["notation"] for v in ct["signal_families"]["values"]}
    assert cfg.counts_toward["policy"] == {"role-change"}
    assert cfg.counts_toward["projection"] == set()
    assert cfg.providers["bls-ai-exposure-observed"] >= {"anthropic", "microsoft"}
    rule = L.load_yaml(ROOT / "vocab" / "rules" / "change-indicator@1.0.0.yaml")
    assert set(cfg.instruments) == set(rule["external_index_instruments"])


def test_view_rows_are_stamped():
    rows = ER.view_rows(_seeded(), stamp={"ruleId": "change-indicator", "ruleVersion": "1.0.0", "buildCommit": "x"})
    for r in rows:
        assert r["ruleId"] == "change-indicator" and r["decision"] in ("moves", "watch", "invalid")
        assert r["kind"] in ("role-change", "skill-change")
