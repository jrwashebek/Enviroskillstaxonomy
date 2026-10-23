#!/usr/bin/env python3
"""Prototype of the computed venue applicability view (ADR-0016 section 3-4; SPEC section 11.6) — WP-05 (A5 SC).

venueApplicability and federalApplicability are COMPUTED fields (schema/lint/computed_fields.yaml): they are never
stored in source records. This script computes them from source records only:

  competency  <-  Enactment(enactmentKind = actor, competency, actorType, characteristicInstruments[])
  instrument  ->  current status = statusAfter of its latest DriverEvent on or before --as-of

Rule (draft, for CA/DE to port into scripts/build_release.py as a vocab/rules/ file; see CR-SC-001):
  for each competency and each sector actor family that has an actor enactment:
    active   = {in-force, in-force-litigated, interim-in-force, issued}
    inactive = {enjoined, stayed, vacated, rescinded, repealed}
    pending  = everything else in vocab/driver_mechanisms.yaml#instrument_statuses, or no event yet
    required-basis   if any linked instrument is active
    no-current-basis if at least one instrument is linked and every linked instrument is inactive
    permitted        otherwise (no instrument linked, or only pending ones): the work is lawful and optional
  federalApplicability = the value for the federal family, with asOf.
Q4 default (PROJECT_LEAD_DECISIONS): federal default views show this value with a note; nothing is excluded.

Known limit (CR-SC-001 item 3): characteristicInstruments does not say whether an instrument REQUIRES, ENABLES or
CONSTRAINS the work, so "required-basis" over-reads enabling instruments. The output flags basisLinked so views can
show "basis not yet linked" instead of a confident value.

Usage: python3 docs/build/WP-05/ci/venue_applicability.py [--data-root DIR] [--as-of YYYY-MM-DD] [--out DIR]
Licence: Apache-2.0.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402

ACTIVE = {"in-force", "in-force-litigated", "interim-in-force", "issued"}
INACTIVE = {"enjoined", "stayed", "vacated", "rescinded", "repealed"}
FAMILIES = ["federal", "state", "local", "tribal", "ngo", "private", "academic"]


def actor_family(actor: str, vocab_root: Path = ROOT / "vocab") -> str | None:
    d = L.load_yaml(vocab_root / "sector_actors.yaml")
    for t in d["terms"]:
        if actor == t["notation"] or actor in [s["notation"] for s in t.get("subtypes", [])]:
            return t["notation"]
    return None


def load(data_root: Path):
    comps, enas, events = {}, [], {}
    names = {}
    for loc, rec in L.iter_records(data_root):
        if not isinstance(rec, dict):
            continue
        typ = rec.get("type")
        if typ == "Competency" and rec.get("status") not in ("superseded", "withdrawn"):
            comps[rec["id"]] = rec
        elif typ == "Enactment" and rec.get("enactmentKind") == "actor":
            enas.append(rec)
        elif typ == "Instrument":
            names[rec["id"]] = (rec.get("prefLabel") or {}).get("en", rec["id"])
        elif typ == "DriverEvent":
            events.setdefault(rec["instrument"], []).append(rec)
    return comps, enas, events, names


def instrument_status(iid, events, as_of):
    evs = sorted((e for e in events.get(iid, []) if e["eventDate"] <= as_of), key=lambda e: e["eventDate"])
    return evs[-1]["statusAfter"] if evs else "no-event"


def compute(data_root: Path, as_of: str):
    comps, enas, events, names = load(data_root)
    by_comp = {}
    for e in enas:
        if e.get("indigenousDataFlag"):
            continue                    # held content never enters a computed view (ADR-0007 section D)
        fam = actor_family(e["actorType"])
        if fam is None or fam == "tribal":
            continue
        by_comp.setdefault(e["competency"], {}).setdefault(fam, []).append(e)
    rows = []
    for cid, fams in sorted(by_comp.items()):
        if cid not in comps:
            continue
        for fam in FAMILIES:
            if fam not in fams:
                continue
            inst = sorted({i for e in fams[fam] for i in (e.get("characteristicInstruments") or [])})
            statuses = {i: instrument_status(i, events, as_of) for i in inst}
            if any(s in ACTIVE for s in statuses.values()):
                value = "required-basis"
            elif inst and all(s in INACTIVE for s in statuses.values()):
                value = "no-current-basis"
            else:
                value = "permitted"
            rows.append({"competency": cid, "label": comps[cid]["prefLabel"]["en"], "sectorActor": fam,
                         "venueApplicability": value, "asOf": as_of, "basisLinked": bool(inst),
                         "enactments": "|".join(sorted(e["id"] for e in fams[fam])),
                         "instruments": "|".join(f"{i}={statuses[i]}" for i in inst)})
    return rows


def federal_view(rows):
    return {r["competency"]: {"federalApplicability": r["venueApplicability"], "asOf": r["asOf"],
                              "basisLinked": r["basisLinked"],
                              "note": "Computed from linked instruments; shown with no exclusion (Q4 default)."}
            for r in rows if r["sectorActor"] == "federal"}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", type=Path, default=L.DATA_V2)
    ap.add_argument("--as-of", default="2026-10-23")
    ap.add_argument("--out", type=Path, default=ROOT / "docs" / "build" / "WP-05" / "generated")
    a = ap.parse_args(argv)
    rows = compute(a.data_root, a.as_of)
    a.out.mkdir(parents=True, exist_ok=True)
    cols = ["competency", "label", "sectorActor", "venueApplicability", "asOf", "basisLinked", "enactments", "instruments"]
    with (a.out / "venue_applicability.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    (a.out / "federal_applicability.json").write_text(json.dumps(federal_view(rows), indent=1), encoding="utf-8")
    print(f"{len(rows)} competency-actor rows written to {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
