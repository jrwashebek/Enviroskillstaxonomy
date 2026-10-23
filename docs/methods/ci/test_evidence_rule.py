"""CI test for the ADR-0028 s2 two-family evidence rule (WP-10, owner A9 LM). DE: move into tests/ when porting.

1. Every synthetic case in evidence_rule_cases.yaml yields its expected decision and reason code.
2. Regression on the real seed: no agent-seeded ChangeSignal under data/v2/signals/ moves any indicator (all are
   unreviewed agent output, so ER-5 must hold them at watch), and every seeded signal declares a family that the
   rule recognises.
"""
import copy
import json
import pathlib
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import evidence_rule as ER  # noqa: E402


def _cases():
    doc = yaml.safe_load((HERE / "evidence_rule_cases.yaml").read_text(encoding="utf-8"))
    assert doc.get("synthetic") is True
    return doc


def _fill(defaults, partial):
    rec = copy.deepcopy(defaults)
    rec.update(copy.deepcopy(partial))
    if rec.get("type") == "ExposureAssessment":
        for k in ("direction", "drivers", "signalStatus"):
            rec.pop(k, None)
    return rec


def test_synthetic_cases():
    doc = _cases()
    failures = []
    for case in doc["cases"]:
        ind = case.get("indicator", doc["indicator"])
        recs = [_fill(doc["defaults"], s) for s in case["signals"]]
        res = ER.evaluate(ind, recs)
        if res["decision"] != case["expect"]:
            failures.append((case["id"], "decision", res))
        elif case.get("reason") and case["reason"] not in res["reasons"]:
            failures.append((case["id"], "reason", res))
    assert not failures, failures


def _seeded_signals():
    out = []
    for p in sorted((ROOT / "data" / "v2" / "signals").rglob("*.jsonl")):
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
    return out


def test_seed_never_moves_an_indicator():
    recs = _seeded_signals()
    if not recs:
        return
    res = ER.evaluate_corpus(recs, kinds=("role-change", "skill-change"))
    moved = [k for k, v in res.items() if v["decision"] == "moves"]
    assert not moved, moved[:5]


def test_seed_families_and_flags():
    recs = _seeded_signals()
    bad = []
    for r in recs:
        fam = ER.family(r)
        if fam not in ER.COUNTING_FAMILIES | ER.NEVER_COUNT:
            bad.append((r["id"], "family", fam))
        if r.get("personalData") is not False:
            bad.append((r["id"], "personalData"))
        if not r.get("drivers"):
            bad.append((r["id"], "drivers"))
        if r.get("reliability") not in ("A", "B", "C", "D"):
            bad.append((r["id"], "reliability"))
        if not r.get("sourceRelease"):
            bad.append((r["id"], "sourceRelease"))
        if r.get("tribalPrograms") and not (r.get("indigenousDataFlag") and r.get("sensitivity") == "restricted-governed"):
            bad.append((r["id"], "tribal-quarantine"))
    assert not bad, bad[:10]
