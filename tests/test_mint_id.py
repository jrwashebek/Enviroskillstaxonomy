"""WP-01: the single ID writer (ADR-0010 §2): CSPRNG bodies, Luhn mod-32 check symbol, append-only registry."""
from __future__ import annotations

import csv
import re

import pytest

from conftest import FIXTURES, L, overlay_tree

import mint_id
import validate_v2


def test_10000_minted_ids_match_pattern_pass_check_and_never_collide(tmp_path):
    reg = tmp_path / "registry.csv"
    ids = mint_id.mint("Competency", "core", "emstagent:test@1", count=10_000, registry=reg, today="2026-10-23")
    rx = re.compile(L.load_yaml(L.VOCAB / "identifiers.yaml")["form"]["regex"])
    assert len(ids) == 10_000 and len(set(ids)) == 10_000
    for i in ids:
        assert rx.match(i), i
        assert L.luhn32_valid(i.rsplit("-", 1)[1]), i
    assert mint_id.verify(reg) == []
    rows = list(csv.DictReader(reg.open()))
    assert [r["id"] for r in rows] == ids
    assert {r["status"] for r in rows} == {"candidate"}


def test_check_symbol_catches_substitutions_and_transpositions():
    body = "T6N5VE"
    code = body + L.luhn32_check(body)
    assert L.luhn32_valid(code)
    for i in range(7):
        for ch in L.CROCKFORD:
            if ch != code[i]:
                assert not L.luhn32_valid(code[:i] + ch + code[i + 1:]), (i, ch)
    for i in range(6):
        if code[i] != code[i + 1]:
            swapped = code[:i] + code[i + 1] + code[i] + code[i + 2:]
            assert not L.luhn32_valid(swapped), i


def test_ia_example_id_validates_cross_implementation():
    assert L.is_emst_id("emst:core/CMP-T6N5VE4")   # IA data_model_v2.md example (v1 2.1.1)


def test_collision_is_redrawn(monkeypatch, tmp_path):
    reg = tmp_path / "r.csv"
    first = mint_id.mint("Task", "core", "emstagent:test@1", registry=reg)[0]
    _, _, code = L.id_parts(first)
    body_n = sum(L.CROCKFORD.index(c) << (5 * i) for i, c in enumerate(reversed(code[:6])))
    draws = iter([body_n, body_n, 12345])
    monkeypatch.setattr(mint_id.secrets, "randbits", lambda bits: next(draws))
    second = mint_id.mint("Task", "core", "emstagent:test@1", registry=reg)[0]
    assert second != first and mint_id.verify(reg) == []


@pytest.mark.parametrize("etype,ns,by,msg", [
    ("WatchItem", "core", "emstagent:x@1", "no TYPE prefix"),
    ("Competency", "nowhere", "emstagent:x@1", "not registered"),
    ("Competency", "core", "Jane Doe", "pseudonymous"),
])
def test_mint_refuses(tmp_path, etype, ns, by, msg):
    with pytest.raises(mint_id.MintError, match=msg):
        mint_id.mint(etype, ns, by, registry=tmp_path / "r.csv")


def test_lock_prevents_a_second_writer(tmp_path):
    reg = tmp_path / "r.csv"
    with mint_id.registry_lock(reg):
        with pytest.raises(mint_id.MintError, match="locked"):
            mint_id.mint("Competency", "core", "emstagent:x@1", registry=reg)


def test_promote_mints_renames_and_rewrites_references(tmp_path):
    data = overlay_tree(tmp_path)
    draft = L.load_yaml(FIXTURES / "records" / "valid" / "Competency.yaml")
    draft["id"] = "seed:fx-promote"
    L.write_yaml(data / "core" / "competencies" / "seed-fx-promote.yaml", draft)
    task = L.load_yaml(FIXTURES / "records" / "valid" / "Task.yaml")
    task["id"] = "seed:fx-promote-task"
    task["supports"] = [{"competency": "seed:fx-promote", "strength": "primary"}]
    L.write_yaml(data / "core" / "tasks" / "seed-fx-promote-task.yaml", task)
    new_id, path = mint_id.promote("seed:fx-promote", "emstagent:test@1", data_root=data, today="2026-10-24")
    assert path.name == L.id_to_stem(new_id) + ".yaml" and not (data / "core" / "competencies" / "seed-fx-promote.yaml").exists()
    rec = L.load_yaml(path)
    assert rec["id"] == new_id and rec["status"] == "candidate"
    t = L.load_yaml(data / "core" / "tasks" / "seed-fx-promote-task.yaml")
    assert t["supports"][0]["competency"] == new_id
    assert "seed:fx-promote," in (data / "ids" / "seed_map.csv").read_text()
    rep = validate_v2.Validator(data, use_git_base=False, check_x1=False,
                                registry_base=FIXTURES / "trees" / "base" / "data" / "v2" / "ids" / "registry.csv").run()
    assert [i.code for i in rep.errors] == []


def test_promote_refuses_held_and_unauthored_seeds(tmp_path):
    data = overlay_tree(tmp_path)
    held = L.load_yaml(FIXTURES / "records" / "valid" / "Competency.yaml")
    held.update(id="seed:fx-held", indigenousDataFlag=True, approvalStatus="pending-tribal-review", sensitivity="restricted-governed")
    L.write_yaml(data / "core" / "competencies" / "seed-fx-held.yaml", held)
    with pytest.raises(mint_id.MintError, match="Tribal"):
        mint_id.promote("seed:fx-held", "emstagent:test@1", data_root=data)
    seed = L.load_yaml(FIXTURES / "records" / "valid" / "Competency.yaml")
    seed.update(id="seed:fx-seed", validationStatus="seed-v1")
    L.write_yaml(data / "core" / "competencies" / "seed-fx-seed.yaml", seed)
    with pytest.raises(mint_id.MintError, match="seed"):
        mint_id.promote("seed:fx-seed", "emstagent:test@1", data_root=data)


def test_transitions_follow_the_lifecycle(tmp_path):
    reg = tmp_path / "r.csv"
    a, b = mint_id.mint("Competency", "core", "emstagent:x@1", count=2, registry=reg)
    with pytest.raises(mint_id.MintError):
        mint_id.transition(a, "superseded", "emstagent:x@1", registry=reg, superseded_by=b)   # candidate -> superseded
    mint_id.transition(a, "published", "emstagent:x@1", registry=reg, release="2.0.0-rc.1")
    mint_id.transition(a, "superseded", "emstagent:x@1", registry=reg, superseded_by=b)
    rows = {r["id"]: r for r in csv.DictReader(reg.open())}
    assert rows[a]["status"] == "superseded" and rows[a]["superseded_by"] == b and rows[a]["first_release"] == "2.0.0-rc.1"
    with pytest.raises(mint_id.MintError):
        mint_id.transition(a, "published", "emstagent:x@1", registry=reg)
