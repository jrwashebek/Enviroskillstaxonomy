#!/usr/bin/env python3
"""S2 close-out A (A5 SC): migrate docs/build/WP-05/mirror_links.csv into Competency.mirrors[] (CR-SC-001 #3).

Mirrors are stored once, on the authority or overseer side (ADR-0030 §2 rule 3); `mirroredBy` is computed by
inverse-links@1.2.0. `relation` (vocab/authority_positions.yaml#mirror_relations) names the target's position relative
to the authority. A target may be a Competency or an Enactment.

Not migrated (and why), written to generated/mirror_migration.csv:
  * within-competency mirrors (FH-C01, DB-C50, SC-C14, SC-C07, SC-C17, SL-C02 variants): already expressed by actor
    enactments with different authorityPosition; a mirror to one's own enactment is E-MIRROR-SELF.
  * SC-C04 -> PS-C18 'related': not a mirror relation (the shared task seed:sc-screen-preparer-conflicts carries it).
  * SC-C15 -> PS-C07: the verifier is the overseer side, so the link belongs on PS-C07, a DC-authored record
    (ADR-0030 §3.2). Handed to DC; not edited here.

Usage: python3 docs/build/S2-closeout-A/moves_mirrors.py [--dry-run]
Licence: Apache-2.0 (code). Records stay CC0-1.0.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402

AGENT = "emstagent:a5-sc@s2-closeout-a"
COMP = L.DATA_V2 / "core" / "competencies"

# (authority-side competency, target, relation, csv row it migrates)
MIRRORS = [
    ("seed:SL-C02", "seed:ena-sc-c01-regulated-party", "applicant-mirror", "SL-C02,SC-C01"),
    ("seed:SL-C02", "seed:DB-C26", "regulated-party-mirror", "SL-C02,DB-C26"),
    ("seed:SL-C03", "seed:DB-C26", "regulated-party-mirror", "SL-C03,DB-C26"),
    ("seed:SL-C04", "seed:DB-C26", "regulated-party-mirror", "SL-C04,DB-C26"),
    ("seed:SL-C10", "seed:DB-C26", "regulated-party-mirror", "SL-C10,DB-C26"),
    ("seed:DB-C25", "seed:DB-C26", "regulated-party-mirror", "DB-C25,DB-C26"),
    ("seed:SC-C04", "seed:ena-sl-c08-consultant", "preparer-mirror", "SC-C04,SL-C08"),
]
NOT_MIGRATED = [
    ("SC-C04,PS-C18", "related, not a mirror relation; carried by the shared task seed:sc-screen-preparer-conflicts"),
    ("FH-C01,FH-C01", "within-competency: actor enactments with different authorityPosition; E-MIRROR-SELF if stored"),
    ("DB-C50,DB-C50", "within-competency: actor enactments; E-MIRROR-SELF if stored"),
    ("SC-C14,SC-C14", "within-competency: actor enactments; E-MIRROR-SELF if stored"),
    ("SC-C07,SC-C07", "within-competency: actor enactments; E-MIRROR-SELF if stored"),
    ("SC-C17,SC-C17", "within-competency: actor enactments; E-MIRROR-SELF if stored"),
    ("SL-C02,SL-C02", "within-competency variants: actor enactments; E-MIRROR-SELF if stored"),
    ("SC-C15,PS-C07", "overseer side is PS-C07 (DC-authored, ADR-0030 §3.2): handed to DC as "
                      "PS-C07.mirrors[{target: seed:SC-C15, relation: regulated-party-mirror}]"),
]
NOTE = "S2 close-out A (A5 SC; CR-SC-001 #3): mirror links migrated from docs/build/WP-05/mirror_links.csv."


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    by = {}
    for src, tgt, rel, _ in MIRRORS:
        by.setdefault(src, []).append({"target": tgt, "relation": rel})
    for src, items in by.items():
        path = COMP / (L.id_to_stem(src) + ".yaml")
        rec = L.load_yaml(path)
        if rec["provenance"]["agent"][0] != "emstagent:a5-sc@wp-05":
            raise SystemExit(f"{src}: not SC-authored")
        new = {}
        for k, v in rec.items():
            if k == "mirrors":
                continue
            new[k] = v
            if k == "instrumentSensitivity":
                new["mirrors"] = items
        if "mirrors" not in new:
            new["mirrors"] = items
        ed = (new.get("editorialNote") or {}).get("en", "")
        if NOTE not in ed:
            new["editorialNote"] = {"en": (ed + " " + NOTE).strip()}
        if AGENT not in new["provenance"]["agent"]:
            new["provenance"]["agent"] = list(new["provenance"]["agent"]) + [AGENT]
        if not a.dry_run:
            L.write_yaml(path, new)
        print(src, items)
    rows = [{"csv_pair": p, "stored_on": s, "target": t, "relation": r, "status": "migrated"} for s, t, r, p in MIRRORS]
    rows += [{"csv_pair": p, "stored_on": "", "target": "", "relation": "", "status": "not migrated: " + why}
             for p, why in NOT_MIGRATED]
    if not a.dry_run:
        (HERE / "generated").mkdir(exist_ok=True)
        (HERE / "generated" / "mirror_migration.csv").write_text(
            L.csv_text(["csv_pair", "stored_on", "target", "relation", "status"], rows), encoding="utf-8")


if __name__ == "__main__":
    main()
