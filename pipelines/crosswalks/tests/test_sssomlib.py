"""Tests for the WP-09 SSSOM writer/checker. Run: python -m pytest -q pipelines/crosswalks/tests"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sssomlib as S  # noqa: E402


def row(**kw):
    base = dict(record_id="r1", subject_id="seed:R14-forester", predicate_id="skos:closeMatch",
                object_id="SOC2018:19-1032", mapping_justification="semapv:LLMBasedMatching",
                author_id=S.AUTHOR, mapping_date="2026-10-23", comment="c",
                other="weakest_match_type=skos:closeMatch;review_status=candidate;evidence=J")
    base.update(kw)
    return base


def check(rows):
    p, j = S.vocab_terms()
    return S.check_rows(rows, p, j)


def test_valid_row_passes():
    assert check([row()]) == []


def test_object_label_forbidden():
    assert any("forbidden column object_label" in e for e in check([row(object_label="Foresters")]))


def test_no_term_needs_reason():
    errs = check([row(object_id=S.NO_TERM, other="weakest_match_type=sssom:NoTermFound;review_status=candidate;evidence=J")])
    assert any("no-term reason" in e for e in errs)


def test_other_requires_weakest():
    assert any("weakest_match_type" in e for e in check([row(other="review_status=candidate;evidence=J")]))


def test_duplicate_record_ids():
    assert any("repeated" in e for e in check([row(), row()]))


def test_weakest_and_chain():
    assert S.weakest("skos:closeMatch", "skos:broadMatch") == "skos:broadMatch"
    assert S.weakest("skos:broadMatch", "skos:narrowMatch") == "skos:relatedMatch"
    assert S.chain("skos:closeMatch", "skos:broadMatch") == "skos:broadMatch"
    assert S.chain("skos:broadMatch", "skos:narrowMatch") == "skos:relatedMatch"
    assert S.chain("skos:closeMatch", "skos:exactMatch") == "skos:closeMatch"
