"""Format-preserving record edits for WP-16 one-off data steps (CA/DE integration; ADR-0031).

YAML records round-trip byte-identically through scripts/emstlib.dump_yaml. JSONL files in the WP-10 lane use
json.dumps defaults (", " / ": ", sorted keys) while DE batches use emstlib.jsonl_line; each edited line is written in
the style its original line used, so untouched lines and files stay byte-identical. Every write is idempotent.
Licence: Apache-2.0.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402

AGENT = "emstagent:ca-de-wp16@claude-opus-5-5"
LOG: list[str] = []


def _styles():
    return [L.jsonl_line,
            lambda o: json.dumps(o, ensure_ascii=False, sort_keys=True),
            lambda o: json.dumps(o, ensure_ascii=False),
            lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"), sort_keys=True)]


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


def append_jsonl(path: Path, rec: dict, like: Path | None = None) -> bool:
    """Append rec unless a line with the same id exists. Style follows the file's first line (or `like`)."""
    path = Path(path)
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    for line in text.splitlines():
        if line.strip() and json.loads(line).get("id") == rec["id"]:
            return False
    src = text.splitlines()[0] if text.strip() else Path(like).read_text(encoding="utf-8").splitlines()[0]
    line = style_of(src)(rec)
    path.write_text(text + ("" if text.endswith("\n") or not text else "\n") + line + "\n", encoding="utf-8")
    LOG.append(f"{path.relative_to(ROOT)}: appended {rec['id']}")
    return True


def edit_yaml(path: Path, fn) -> bool:
    path = Path(path)
    rec = L.load_yaml(path)
    before = L.dump_yaml(rec)
    new = fn(L.load_yaml(path))
    if new is None:
        return False
    text = L.dump_yaml(new)
    if text != before:
        path.write_text(text, encoding="utf-8")
        LOG.append(f"{path.relative_to(ROOT)}")
        return True
    return False


def replace_in_strings(obj, old: str, new: str):
    if isinstance(obj, str):
        return obj.replace(old, new)
    if isinstance(obj, list):
        return [replace_in_strings(x, old, new) for x in obj]
    if isinstance(obj, dict):
        return {k: replace_in_strings(v, old, new) for k, v in obj.items()}
    return obj


def find_yaml(rid: str) -> Path:
    stem = L.id_to_stem(rid) + ".yaml"
    hits = sorted(L.DATA_V2.rglob(stem))
    if len(hits) != 1:
        raise SystemExit(f"{rid}: expected one file {stem}, found {len(hits)}")
    return hits[0]
