"""Shared helpers for the rc.1 data and method fix scripts (D-DATA lane; ADR-0032).

Format-preserving, idempotent record edits, modelled on docs/build/WP-16/wp16lib.py:
  * YAML records round-trip through scripts/emstlib.dump_yaml, so an unchanged record is byte-identical;
  * each edited JSONL line is written in the JSON style its original line used, so untouched lines stay byte-identical;
  * every function returns what it changed, and a second run changes nothing.
Licence: Apache-2.0.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402

AGENT = "emstagent:d-data-rc1-fix@claude-opus-5-5"
TODAY = "2026-10-25"
LOG: list[str] = []


def _styles():
    return [L.jsonl_line,
            lambda o: json.dumps(o, ensure_ascii=False, sort_keys=True),
            lambda o: json.dumps(o, ensure_ascii=False),
            lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"), sort_keys=True),
            lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))]


def style_of(line: str):
    obj = json.loads(line)
    for f in _styles():
        if f(obj) == line:
            return f
    raise ValueError(f"no known JSON style reproduces line: {line[:120]}")


def edit_jsonl(path: Path, fn) -> int:
    """fn(record) -> record | None (None = unchanged). Returns the number of changed lines."""
    path = Path(path)
    lines = path.read_text(encoding="utf-8").splitlines()
    out, n = [], 0
    for line in lines:
        if not line.strip():
            out.append(line)
            continue
        rec = json.loads(line)
        new = fn(json.loads(line))
        if new is not None and new != rec:
            out.append(style_of(line)(new))
            n += 1
        else:
            out.append(line)
    if n:
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
        LOG.append(f"{path.relative_to(ROOT)}: {n} line(s)")
    return n


def edit_yaml(path: Path, fn) -> bool:
    path = Path(path)
    before = path.read_text(encoding="utf-8")
    new = fn(L.load_yaml(path))
    if new is None:
        return False
    text = L.dump_yaml(new)
    if text != before:
        path.write_text(text, encoding="utf-8")
        LOG.append(str(path.relative_to(ROOT)))
        return True
    return False


def records(types=None):
    """[(Loc, record)] for every parseable record (optionally of the given types)."""
    out = []
    for loc, rec in L.iter_records(L.DATA_V2):
        if isinstance(rec, dict) and (types is None or rec.get("type") in types):
            out.append((loc, rec))
    return out


def yaml_path(rid: str) -> Path:
    stem = L.id_to_stem(rid) + ".yaml"
    hits = sorted(L.DATA_V2.rglob(stem))
    if len(hits) != 1:
        raise SystemExit(f"{rid}: expected one file {stem}, found {len(hits)}")
    return hits[0]


def insert_after(rec: dict, after: str, key: str, value) -> dict:
    """Return a copy of rec with key inserted after `after` (or at the end), keeping field order stable."""
    out = {}
    placed = False
    for k, v in rec.items():
        if k == key:
            continue
        out[k] = v
        if k == after:
            out[key] = value
            placed = True
    if not placed:
        out[key] = value
    return out


def write_report(name: str, text: str) -> Path:
    p = Path(__file__).resolve().parent / "generated" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists() or p.read_text(encoding="utf-8") != text:
        p.write_text(text, encoding="utf-8")
    return p


def summary(title: str):
    print(f"{title}: {len(LOG)} file(s) changed")
    for line in LOG:
        print("  " + line)
    LOG.clear()
