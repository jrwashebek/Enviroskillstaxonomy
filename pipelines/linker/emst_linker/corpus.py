"""Build EMST v2 competency documents from data/v2 records (core and modules).

A competency document joins prefLabel, altLabel, statement, definition, the statements of the tasks that support
it, its indicator statements and (while it still exists) the v1Seed title/description, with the repetition weights
in config.FIELD_REPEAT. Held Tribal content (ADR-0007 §D) and superseded/withdrawn records are excluded: held
records never enter an index, so they can never be linked or counted.
"""
from __future__ import annotations

import hashlib
from collections import defaultdict
from pathlib import Path

import yaml

from . import config as C


def _load(p: Path):
    with open(p, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _en(v):
    if isinstance(v, dict):
        e = v.get("en")
        if isinstance(e, list):
            return " ".join(map(str, e))
        return e or ""
    return v or ""


def held_keys(data_v2: Path = C.DATA_V2):
    p = data_v2 / "governance" / "tribal_hold.yaml"
    if not p.exists():
        return set()
    return set((_load(p) or {}).get("heldSeedKeys", []))


def is_held(rec, held):
    return bool(rec.get("indigenousDataFlag")) or rec.get("approvalStatus") == "pending-tribal-review" \
        or rec.get("id") in held or rec.get("sensitivity") == "restricted-governed"


def load(data_v2: Path = C.DATA_V2):
    """Return (competencies: list[dict], tasks_by_comp: dict[id, list[(task_id, text)]], release_hash)."""
    held = held_keys(data_v2)
    comps, tasks_by, inds_by = {}, defaultdict(list), defaultdict(list)
    files = sorted(list(data_v2.glob("core/*/*.yaml")) + list(data_v2.glob("modules/*/*/*.yaml")))
    h = hashlib.sha256()
    for p in files:
        try:
            r = _load(p)
        except Exception:  # noqa: BLE001 - other lanes may be mid-write; skip unreadable files
            continue
        if not isinstance(r, dict):
            continue
        t = r.get("type")
        if t not in ("Competency", "Task", "Indicator"):
            continue
        if r.get("status") in C.EXCLUDED_STATUSES or is_held(r, held):
            continue
        h.update(p.read_bytes())
        if t == "Competency":
            comps[r["id"]] = r
        elif t == "Task":
            for s in r.get("supports") or []:
                if isinstance(s, dict) and s.get("competency"):
                    tasks_by[s["competency"]].append((r["id"], _en(r.get("statement")) or _en(r.get("prefLabel"))))
        elif t == "Indicator" and r.get("competency"):
            inds_by[r["competency"]].append(_en(r.get("statement")))
    out = []
    for cid, r in sorted(comps.items()):
        if cid in held:
            continue
        seed = r.get("v1Seed") or {}
        parts = {
            "prefLabel": _en(r.get("prefLabel")),
            "altLabel": _en(r.get("altLabel")),
            "statement": _en(r.get("statement")),
            "definition": _en(r.get("definition")),
            "tasks": " ".join(t for _, t in tasks_by.get(cid, [])),
            "indicators": " ".join(inds_by.get(cid, [])[:12]),
            "v1Seed": " ".join(str(seed.get(k, "")) for k in ("title", "description") if isinstance(seed, dict)),
        }
        doc = " ".join(" ".join([parts[k]] * C.FIELD_REPEAT[k]) for k in C.FIELD_REPEAT if parts.get(k))
        short = ". ".join(x for x in (parts["prefLabel"], parts["statement"] or parts["definition"]) if x)
        out.append({"id": cid, "module": r.get("module"), "label": parts["prefLabel"], "doc": doc,
                    "short": short or parts["prefLabel"], "competencyType": r.get("competencyType"),
                    "validationStatus": r.get("validationStatus")})
    return out, dict(tasks_by), h.hexdigest()
