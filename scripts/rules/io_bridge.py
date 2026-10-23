"""Load IO's validation modules (validation/*.py) by path, so scripts/ and tests share one import route.

The modules use dataclasses, which resolve their module through sys.modules, so each is registered before exec.
Every loader returns None when the file is absent (forks without validation/ still build, with the fallbacks).
"""
from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATION = ROOT / "validation"


def load(name: str, root: Path = ROOT):
    key = f"emst_io_{name}"
    if key in sys.modules:
        return sys.modules[key]
    p = Path(root) / "validation" / f"{name}.py"
    if not p.exists():
        return None
    spec = importlib.util.spec_from_file_location(key, p)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[key] = mod
    spec.loader.exec_module(mod)
    return mod


def file_sha256(rel: str, root: Path = ROOT) -> str | None:
    p = Path(root) / rel
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None


def lint(records: dict, waivers: list[dict], tool_names: list[str] | None = None, mode: str = "release"):
    """Run IO's indicator linter once over released Indicator/Competency/Task/KnowledgeStatement records.
    Returns (open, waived): open = {record_id: [hits]} without waived and info hits, or None when the linter is
    unavailable; waived = the hits a valid waiver covered (release notes count them by rule)."""
    mod = load("lint_indicators")
    if mod is None:
        return None, []
    linter = mod.Linter(mod.load_rules(), mode, waivers, tool_names or [], [])
    recs = [mod.Record(r, rid) for rid, r in records.items() if r.get("type") in ("Indicator", "Competency", "Task", "KnowledgeStatement")]
    open_: dict[str, list] = {}
    waived = []
    for h in linter.lint_set(recs):
        if h.status == "waived":
            waived.append(h)
        elif h.severity != "info":
            open_.setdefault(h.record_id, []).append(h)
    return open_, waived
