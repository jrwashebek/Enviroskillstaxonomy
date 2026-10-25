"""Computed-view rule files in vocab/rules/ and the lanes around them (ADR-0029 §4.2, §10)."""
from __future__ import annotations

import importlib
import json
import re

import pytest
import yaml

from conftest import L, overlay_tree

from rules import registry

FILES = sorted((L.VOCAB / "rules").glob("*.yaml"))
DOCS = {p.name: L.load_yaml(p) for p in FILES}
KEYS = {f"{d['ruleId']}@{d['version']}" for d in DOCS.values()}


def test_rule_files_exist():
    assert len(FILES) >= 8


@pytest.mark.parametrize("path", FILES, ids=lambda p: p.name)
def test_rule_file_parses_with_both_loaders_and_is_named_by_id_and_version(path):
    a = yaml.safe_load(path.read_text(encoding="utf-8"))
    b = L.load_yaml(path)
    assert a == b
    assert path.name == f"{b['ruleId']}@{b['version']}.yaml"
    assert b.get("status") in ("active", "interim", "superseded", "draft")


@pytest.mark.parametrize("path", FILES, ids=lambda p: p.name)
def test_lineage_targets_exist(path):
    d = DOCS[path.name]
    for k in ("supersededBy", "replaces"):
        for target in ([d[k]] if isinstance(d.get(k), str) else d.get(k) or []):
            assert target in KEYS, f"{path.name}: {k} {target} has no rule file"


@pytest.mark.parametrize("path", FILES, ids=lambda p: p.name)
def test_implementation_path_exists_and_symbol_resolves(path):
    impl = str(DOCS[path.name]["implementation"]).split()[0]
    rel, _, symbol = impl.partition("#")
    assert (L.ROOT / rel).exists(), f"{path.name}: implementation {rel} missing"
    if rel.startswith("scripts/") and rel.endswith(".py") and symbol:
        mod = importlib.import_module(rel[len("scripts/"):-3].replace("/", "."))
        obj = mod
        for part in symbol.split("."):
            obj = getattr(obj, part)


def test_one_active_or_interim_version_per_rule():
    active = registry.active_rules()
    assert set(active) == {d["ruleId"] for d in DOCS.values()}
    assert active["effective-use-tier"]["version"] == "1.1.0"      # ADR-0032: lifecycle no longer caps the tier
    assert active["change-indicator"]["version"] == "1.1.0"        # ADR-0032: ER-1 independence on three axes
    assert active["inverse-links"]["version"] == "1.2.0"          # ADR-0030: mirrored_by landed with its test


def _stamps(node, out):
    if isinstance(node, dict):
        if "ruleId" in node and "ruleVersion" in node:
            out.add((node["ruleId"], str(node["ruleVersion"])))
        for v in node.values():
            _stamps(v, out)
    elif isinstance(node, list):
        for v in node:
            _stamps(v, out)
    return out


def test_every_stamp_in_a_built_view_has_a_rule_file(tmp_path):
    import build_release
    data = overlay_tree(tmp_path / "src")
    b = build_release.Builder(data, version="2.0.0-rc.0", build_commit="test")
    files = b.build(tmp_path / "out")
    stamps = set()
    for name, blob in files.items():
        if name.startswith("views/"):
            _stamps(json.loads(blob), stamps)
    assert stamps, "no stamped view rows"
    for rule_id, version in stamps:
        assert f"{rule_id}@{version}" in KEYS, (rule_id, version)
        assert DOCS[f"{rule_id}@{version}.yaml"]["status"] in ("active", "interim")
    assert {r for r, _ in b.stamped} >= {"counts", "inverse-links", "effective-use-tier", "assessment-staleness",
                                         "change-indicator", "display-gate"}
    assert b.stamped >= stamps
    for rule_id, version in b.stamped:
        assert f"{rule_id}@{version}" in KEYS


def test_ci_and_scripts_never_invoke_methods_scripts():
    """CR-LM-003: docs/methods/scripts/ belongs to LM; CI and the build never run it."""
    rx = re.compile(r"docs/methods/scripts/")
    hits = []
    for p in sorted((L.ROOT / ".github" / "workflows").glob("*.yml")) + sorted((L.ROOT / "scripts").rglob("*.py")):
        if rx.search(p.read_text(encoding="utf-8")):
            hits.append(str(p.relative_to(L.ROOT)))
    assert not hits, hits
