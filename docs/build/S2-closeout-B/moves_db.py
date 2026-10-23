#!/usr/bin/env python3
"""DB (A6) data moves for S2 close-out builder B (authoring aid; CI never runs it).

  python3 docs/build/S2-closeout-B/moves_db.py subsectors   # row 31: CR-DB-001 #2
  python3 docs/build/S2-closeout-B/moves_db.py roles        # row 33: CR-SC-001 #2

subsectors: every live module Enactment (enactmentKind = module) whose subsectors are stated in editorialNote as
  "Subsectors: A, B." gets `subsectors: [A, B]` (after enactedInModule) and the sentence is removed from the note
  (one fact, one place). Records that already carry `subsectors` are left as they are.
roles: the 11 DB module enactments with instrument links get a role on every link, aligned with the roles SC set on
  the same instruments in actor enactments (builder A, docs/build/S2-closeout-A/generated/instrument_link_roles.csv).
Outputs a generated table in generated/ for each move. Text of records is otherwise unchanged.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import s2b_lib as S  # noqa: E402
L = S.L

GEN = HERE / "generated"
SUB_RX = re.compile(r"\s*Subsectors:\s*([A-Z]\d{2}(?:\s*,\s*[A-Z]\d{2})*)\.\s*")

ROLES = {
    "seed:ena-ps-c09-air": {"seed:ins/ghgrp-reconsideration": ("removed-requirement", "Proposed reconsideration would end most reporting obligations; never a basis.")},
    "seed:ena-6.2.3-forest": {"seed:ins/usfs-objection-rule": ("constrains", None), "seed:ins/usda-nepa-procedures": ("requires", None)},
    "seed:ena-db-c50-forest": {"seed:ins/nhpa-s106-regs": ("requires", None)},
    "seed:ena-db-c50-hazards": {"seed:ins/nhpa-s106-regs": ("requires", None)},
    "seed:ena-db-c50-parks": {"seed:ins/nhpa-s106-regs": ("requires", None)},
    "seed:ena-fc-c14-forest": {"seed:ins/faa-part-108": ("enables", "Proposed beyond-visual-line-of-sight rule; would enable, not require, the work.")},
    "seed:ena-sc-c08-forest": {"seed:ins/good-neighbor-authority": ("enables", None), "seed:ins/co-hb26-1205": ("enables", None),
                               "seed:ins/long-term-gna-act": ("enables", None)},
    "seed:ena-sl-c08-forest": {"seed:ins/usda-nepa-procedures": ("requires", None), "seed:ins/usfs-objection-rule": ("constrains", None),
                               "seed:ins/seven-county": ("constrains", None)},
    "seed:ena-sc-c14-waterq": {"seed:ins/florida-404-assumption": ("enables", None)},
    "seed:ena-sl-c02-waterq": {"seed:ins/wotus-definition": ("constrains", None)},
    "seed:ena-fh-c01-wildlife": {"seed:ins/esa-s4-s7-regs-2025": ("constrains", "Proposed amendments to the consultation regulations."),
                                 "seed:ins/esa-harm-rescission": ("constrains", None)},
}


def _module_enactments():
    for p in sorted((S.DATA / "modules").rglob("enactments/*.yaml")):
        rec = L.load_yaml(p)
        if rec.get("type") == "Enactment" and rec.get("enactmentKind") == "module" and rec.get("status") not in ("superseded", "withdrawn"):
            yield p, rec


def _insert_after(rec, after_key, key, value):
    out = {}
    for k, v in rec.items():
        if k == key:
            continue
        out[k] = v
        if k == after_key:
            out[key] = value
    if key not in out:
        out[key] = value
    return out


def subsectors():
    rows = []
    for p, rec in _module_enactments():
        note = (rec.get("editorialNote") or {}).get("en", "")
        m = SUB_RX.search(note)
        if rec.get("subsectors"):
            rows.append({"enactment": rec["id"], "subsectors": "|".join(rec["subsectors"]), "action": "already-set"})
            continue
        if not m:
            rows.append({"enactment": rec["id"], "subsectors": "", "action": "no-note-value"})
            continue
        subs = [s.strip() for s in m.group(1).split(",")]
        new_note = (note[:m.start()] + " " + note[m.end():]).strip()
        rec = _insert_after(rec, "enactedInModule", "subsectors", subs)
        rec["editorialNote"] = {"en": new_note + " Subsectors moved to the subsectors field (CR-DB-001 #2, S2)."}
        ag = rec["provenance"].setdefault("agent", [])
        if S.AG["DB"] not in ag:
            ag.append(S.AG["DB"])
        L.write_yaml(p, rec)
        S.log(rec["id"], "Enactment", p, "move-subsectors", "31")
        rows.append({"enactment": rec["id"], "subsectors": "|".join(subs), "action": "moved"})
    GEN.mkdir(exist_ok=True)
    (GEN / "enactment_subsectors.csv").write_text(L.csv_text(["enactment", "subsectors", "action"], rows), encoding="utf-8")
    print({a: sum(1 for r in rows if r["action"] == a) for a in {r["action"] for r in rows}})


def roles():
    rows = []
    for eid, want in ROLES.items():
        p, rec = S.load(eid)
        links = rec.get("characteristicInstruments") or []
        have = {(x["instrument"] if isinstance(x, dict) else x) for x in links}
        missing = set(want) - have
        extra = have - set(want)
        if missing or extra:
            raise SystemExit(f"{eid}: link set differs (missing {missing}, extra {extra})")
        new = []
        for x in links:
            iid = x["instrument"] if isinstance(x, dict) else x
            role, note = want[iid]
            item = {"instrument": iid, "role": role}
            if note:
                item["note"] = {"en": note}
            elif isinstance(x, dict) and x.get("note"):
                item["note"] = x["note"]
            new.append(item)
            rows.append({"enactment": eid, "instrument": iid, "role": role, "action": "role-set"})
        rec["characteristicInstruments"] = new
        en = (rec.get("editorialNote") or {}).get("en", "")
        tag = "Instrument link roles set (CR-SC-001 #2, S2; aligned with SC's actor-enactment roles); only requires links decide venue applicability."
        if tag not in en:
            rec["editorialNote"] = {"en": (en + " " if en else "") + tag}
        ag = rec["provenance"].setdefault("agent", [])
        if S.AG["DB"] not in ag:
            ag.append(S.AG["DB"])
        L.write_yaml(p, rec)
        S.log(eid, "Enactment", p, "set-link-roles", "33")
    GEN.mkdir(exist_ok=True)
    (GEN / "db_module_link_roles.csv").write_text(L.csv_text(["enactment", "instrument", "role", "action"], rows), encoding="utf-8")
    print(f"{len(ROLES)} enactments, {len(rows)} links typed")


if __name__ == "__main__":
    {"subsectors": subsectors, "roles": roles}[sys.argv[1]]()
