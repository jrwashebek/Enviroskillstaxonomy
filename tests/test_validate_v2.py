"""WP-01: cross-record rules fail on seeded violations (tests/fixtures/violations/*) and pass on the base tree."""
from __future__ import annotations

import pytest

from conftest import FIXTURES, L, overlay_tree

import validate_v2

CASES = sorted(p.name for p in (FIXTURES / "violations").iterdir() if p.is_dir())
BASE_REG = FIXTURES / "trees" / "base" / "data" / "v2" / "ids" / "registry.csv"


def run(data, **kw):
    kw.setdefault("use_git_base", False)
    kw.setdefault("check_x1", False)
    return validate_v2.Validator(data, **kw).run()


def test_base_tree_is_clean(tmp_path):
    rep = run(overlay_tree(tmp_path), registry_base=BASE_REG)
    assert [(i.code, i.where, i.message) for i in rep.issues] == []


def test_violation_suite_covers_every_required_check():
    required = {"registry-deleted-row", "registry-edited-row", "module-redefines-core", "module-mints-core-namespace",
                "tribal-held-key-unflagged", "tribal-leak-candidate", "tribal-inherit", "tribal-coords-cultural",
                "confidential-marker", "personal-data-text", "personal-data-field", "typing-lint", "indicator-lint",
                "computed-field", "x1-incomplete"}
    assert required <= set(CASES)


@pytest.mark.parametrize("case", CASES)
def test_seeded_violation_is_caught(tmp_path, case):
    d = FIXTURES / "violations" / case
    exp = L.load_yaml(d / "expect.yaml")
    data = overlay_tree(tmp_path, d)
    rep = run(data, registry_base=BASE_REG if exp["registryBase"] else None, check_x1=exp["checkX1"], strict=exp["strict"])
    codes = set(rep.codes())
    for code in exp["expect"]:
        assert code in codes, f"{case}: expected {code}, got {sorted(codes)}"
    assert rep.errors, f"{case} must fail CI"


def test_registry_status_transition_is_allowed(tmp_path):
    data = overlay_tree(tmp_path)
    reg = data / "ids" / "registry.csv"
    lines = reg.read_text().splitlines()
    parts = lines[1].split(",")
    parts[5], parts[7] = "published", "2.0.0-rc.1"
    lines[1] = ",".join(parts)
    reg.write_text("\n".join(lines) + "\n")
    cmp = next((data / "core" / "competencies").glob("CMP-*.yaml"))
    rec = L.load_yaml(cmp)
    rec.update(status="published", versionIntroduced="2.0.0-rc.1", lastChangedIn="2.0.0-rc.1")
    L.write_yaml(cmp, rec)
    rep = run(data, registry_base=BASE_REG)
    assert [i.code for i in rep.errors] == []


def test_draft_tribal_text_warns_and_strict_mode_errors(tmp_path):
    data = overlay_tree(tmp_path)
    rec = L.load_yaml(FIXTURES / "records" / "valid" / "Competency.yaml")
    rec.update(id="seed:fx-draft-leak", scopeNote={"en": "Includes consultation with Tribal governments."})
    L.write_yaml(data / "core" / "competencies" / "seed-fx-draft-leak.yaml", rec)
    assert "W-TRIBAL-LEAK" in run(data).codes()
    assert "E-TRIBAL-LEAK" in run(data, strict=True).codes()


def test_lint_on_seed_records_is_a_warning(tmp_path):
    data = overlay_tree(tmp_path)
    text = "Use ArcGIS to map plots for the annual field season report"
    rec = L.load_yaml(FIXTURES / "records" / "valid" / "Task.yaml")
    rec.update(id="seed:fx-seed-lint", prefLabel={"en": text}, statement={"en": text}, textSha256=L.text_sha256(text),
               validationStatus="seed-v1")
    L.write_yaml(data / "core" / "tasks" / "seed-fx-seed-lint.yaml", rec)
    codes = run(data).codes()
    assert "W-LINT-TYPING" in codes and "E-LINT-TYPING" not in codes
