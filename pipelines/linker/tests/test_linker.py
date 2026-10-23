"""Synthetic tests for emst_linker (no network, no real postings). Run: python -m pytest -q pipelines/linker/tests"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from emst_linker import quality, safety  # noqa: E402
from emst_linker.index import HybridIndex  # noqa: E402


def test_pii_stripped():
    t, n = safety.strip_pii("Contact: A. Person\nCall 555-123-4567 or mail someone@example.org about sampling.")
    assert "555-123-4567" not in t and "someone@example.org" not in t and n >= 2


def test_tribal_quarantine():
    assert safety.quarantine("Coordinate consultation with Tribal governments on effects")
    assert safety.quarantine("Any text", source_employer_type="tribal")
    assert not safety.quarantine("Inspect wastewater treatment facilities for permit compliance")


def test_verify_span():
    assert safety.verify_span("permit limits", "operate plants to permit limits")
    assert not safety.verify_span("invented span", "operate plants to permit limits")


def test_index_ranks_relevant_first():
    docs = ["inspect facilities for permit compliance and document violations",
            "plan prescribed burns and fuels treatments with smoke management",
            "operate drinking water treatment processes"]
    idx = HybridIndex(docs, ["a", "b", "c"], semantic="none")
    order, S, raw = idx.rank(["prescribed fire burn plan"], k=3)
    assert idx.ids[order[0][0]] == "b"


def test_aggregate_refuses_without_gold():
    with pytest.raises(quality.UncorrectedCountError):
        quality.aggregate(["a", "b"], None, None)


def test_aggregate_corrects_with_confusion():
    confusion = {"a": {"a": 8, "b": 2}, "b": {"b": 9, "none": 1}}
    q = {"goldSet": "synthetic", "precisionAt1": 0.85, "ci95": [0.7, 0.95]}
    out = quality.aggregate(["a"] * 50 + ["b"] * 50, confusion, q, n_boot=200)
    sh = out["correctedShares"]
    assert abs(sh["a"]["share"] - 0.4) < 0.05 and abs(sh["b"]["share"] - 0.55) < 0.05
    assert out["linkerQuality"] == q


def test_evaluate_metrics():
    gold = [{"item_id": "1", "acceptable": {"a"}}, {"item_id": "2", "acceptable": {"c"}}, {"item_id": "3", "acceptable": set(), "noise": True}]
    ranked = {"1": ["a", "b"], "2": ["b", "c"], "3": []}
    m = quality.evaluate(ranked, gold, n_boot=200)
    assert m["p1"]["mean"] == 0.5 and m["hit5"]["mean"] == 1.0 and m["noise_abstention_recall"]["mean"] == 1.0
