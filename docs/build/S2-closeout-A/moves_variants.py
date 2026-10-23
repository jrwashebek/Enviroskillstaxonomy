#!/usr/bin/env python3
"""S2 close-out A (A7 FH): RoleVariant data moves.

1. Work order "RoleVariant.indicativeGradeOrBand" (CR-FH-001 #6; ADR-0030 §1.9): write
   `indicativeGradeOrBand.byRoleLevel` from WP-08's micro-format ("GS-9 to GS-11 [journey]; GS-12 to GS-13 [senior]")
   and drop the micro-format `band`. Values are unchanged FH judgment (WP-08 prompt @1), label unchanged.
2. Same pass, WP-08 instruction (ADR-0030 §6: "author RoleVariant.instruments[] typed {instrument, role}"): set the
   role on each variant instrument link that DE converted without a role (CR-SC-001 #2 conversion). Roles follow the
   matching SC enactments (moves_instrument_roles.py) and the variant's authority position.

Only WP-08 (FH) variant records are edited. build_wp08.py is not re-run (it would overwrite S2 edits).
Usage: python3 docs/build/S2-closeout-A/moves_variants.py [--dry-run]
Licence: Apache-2.0 (code). Records stay CC0-1.0.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402

AGENT = "emstagent:fh-agent@s2-closeout-a"
R, EN, C, X = "requires", "enables", "constrains", "removed-requirement"
LEVELS = ["entry", "journey", "senior", "lead", "strategic"]

ROLES = {
    "seed:R01-conservation-corps-member/ngo": {"americorps-grant-terminations": (C, "Terminations, injunction and FY2026 settlement bound programme funding.")},
    "seed:R09-restoration-project-lead/federal": {"stewardship-contracting": (EN, None), "good-neighbor-authority": (EN, None)},
    "seed:R09-restoration-project-lead/state": {"good-neighbor-authority": (EN, None)},
    "seed:R10-environmental-review-specialist/federal": {
        "nepa-fra-2023": (R, None), "ceq-nepa-regs-removal": (X, "Removed the government-wide regulations; never a basis."),
        "seven-county": (C, None), "doi-nepa-procedures": (R, None), "usda-nepa-procedures": (R, None),
        "epa-nepa-procedures": (R, "Proposed; decides nothing until in force."), "dot-nepa-procedures": (R, None),
        "fast-41": (C, "Coordination and timetables for covered projects.")},
    "seed:R10-environmental-review-specialist/local": {"state-sepa-ca": (R, "Example state."), "state-sepa-wa": (R, "Example state.")},
    "seed:R10-environmental-review-specialist/state": {
        "state-sepa-ca": (R, "Example state."), "state-sepa-mn": (R, "Example state."), "state-sepa-ny": (R, "Example state."),
        "state-sepa-wa": (R, "Example state."), "ceqa-2025-reforms": (C, None),
        "nepa-assignment-23usc327": (EN, "Federal review by assignment to state transportation agencies.")},
    "seed:R11-environmental-permit-writer/federal": {
        "cwa-402-npdes": (R, None), "cwa-404": (R, "Outside assumed states."), "caa-title-v": (R, None),
        "caa-nsr-psd": (R, None), "rcra-permits": (R, "Where the federal regulator issues the permit."),
        "state-program-approval-regs": (R, "Federal review of state-issued permits in delegated programmes.")},
    "seed:R11-environmental-permit-writer/local": {"caa-title-v": (R, "Delegated air districts."), "caa-nsr-psd": (R, "Delegated air districts.")},
    "seed:R11-environmental-permit-writer/state": {
        "cwa-402-npdes": (R, None), "caa-title-v": (R, None), "caa-nsr-psd": (R, None), "rcra-permits": (R, None),
        "cwa-404": (EN, "State assumption is optional."),
        "florida-404-assumption": (EN, "One state's assumption (vacated 2026-03-27); an example, not the basis.")},
    "seed:R12-environmental-compliance-inspector/federal": {"federal-inspection-authorities": (R, None), "epa-penalty-policies": (C, None)},
    "seed:R12-environmental-compliance-inspector/state": {"epa-penalty-policies": (C, "Delegated programmes follow federal response policies.")},
    "seed:R13-resource-program-manager/federal": {
        "appropriations-law": (R, None), "fy2026-interior-approps": (EN, None),
        "obbba-ira-rescissions": (C, "Rescinded unobligated balances."), "good-neighbor-authority": (EN, None)},
    "seed:R13-resource-program-manager/state": {"categorical-program-grants": (EN, None)},
    "seed:R22-environmental-engineer/state": {"state-licensing-acts-wi": (C, "Example state.")},
    "seed:R23-enforcement-case-manager/federal": {"epa-penalty-policies": (C, None)},
    "seed:R23-enforcement-case-manager/state": {"epa-penalty-policies": (C, None)},
    "seed:R33-permitting-technology-product-owner/federal": {
        "permitting-tech-pm-2025": (R, None), "ceq-permitting-data-standard": (R, None), "permitting-tech-action-plan": (EN, None)},
    "seed:R36-ghg-nature-data-controller/private": {
        "ca-sb-253": (R, None), "ca-sb-261": (R, "Enjoined 2025-11-18."), "eu-omnibus-i": (C, "Narrowed the EU reporting scope."),
        "ghgrp-reconsideration": (X, "Proposed removal of federal reporting obligations; never a basis.")},
    "seed:R37-facility-environmental-compliance-specialist/federal": {"report-certification-rules": (R, None), "rcra-permits": (R, None)},
    "seed:R37-facility-environmental-compliance-specialist/local": {
        "report-certification-rules": (R, None), "cwa-402-npdes": (R, None), "npdes-ereporting-rule": (R, None)},
    "seed:R37-facility-environmental-compliance-specialist/private": {
        "report-certification-rules": (R, None), "cwa-402-npdes": (R, None), "caa-title-v": (R, None),
        "rcra-permits": (R, None), "npdes-ereporting-rule": (R, None)},
    "seed:R28-air-quality-specialist/federal": {"caa-title-v": (R, None), "caa-nsr-psd": (R, None)},
    "seed:R28-air-quality-specialist/local": {"caa-title-v": (R, None)},
    "seed:R28-air-quality-specialist/state": {"caa-title-v": (R, None), "caa-nsr-psd": (R, None)},
    "seed:R06-wildland-fire-operations/federal": {"uswfs-so-3448": (EN, "Establishes the organization; not a basis for the work."),
                                                  "wildland-fire-quals-alignment": (R, None)},
    "seed:R07-fuels-prescribed-fire-specialist/federal": {"wildland-fire-quals-alignment": (R, None), "fix-our-forests-act": (EN, "Pending legislation.")},
    "seed:R08-fire-intelligence-analyst/federal": {"uswfs-so-3448": (EN, "Establishes the organization; not a basis for the work.")},
    "seed:R14-forester/federal": {"stewardship-contracting": (EN, None), "good-neighbor-authority": (EN, None)},
    "seed:R18-rangeland-management-specialist/federal": {"federal-land-use-authorizations": (R, None)},
    "seed:R34-stewardship-agreement-manager/federal": {"good-neighbor-authority": (EN, None), "stewardship-contracting": (EN, None)},
    "seed:R34-stewardship-agreement-manager/state": {"good-neighbor-authority": (EN, None), "co-hb26-1205": (EN, "Example state.")},
    "seed:R24-drinking-water-program-analyst/federal": {"state-program-approval-regs": (R, "Primacy approval and oversight.")},
    "seed:R24-drinking-water-program-analyst/state": {"state-program-approval-regs": (R, "Primacy conditions.")},
}
OLD_NOTE = "the bracketed role levels say which band each level is read against"
NEW_NOTE = "indicativeGradeOrBand.byRoleLevel gives the band each role level is read against"


def parse(band: str) -> dict:
    out = {}
    for part in band.split(";"):
        part = part.strip()
        if not part:
            continue
        if not (part.endswith("]") and "[" in part):
            raise ValueError(f"unparseable band part {part!r}")
        b, lv = part[:-1].split("[", 1)
        for x in lv.split("|"):
            x = x.strip()
            if x not in LEVELS or x in out:
                raise ValueError(f"bad level {x!r} in {band!r}")
            out[x] = b.strip()
    return {k: out[k] for k in LEVELS if k in out}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    stats = Counter()
    rows = []
    paths = sorted(L.DATA_V2.glob("core/variants/*.yaml")) + sorted(L.DATA_V2.glob("modules/*/variants/*.yaml"))
    seen = set()
    for path in paths:
        rec = L.load_yaml(path)
        rid = rec["id"]
        changed = False
        if rec["provenance"]["agent"][0] != "emstagent:fh-agent@wp-08":
            continue
        igb = rec.get("indicativeGradeOrBand")
        if igb and igb.get("band") and not igb.get("byRoleLevel"):
            levels = {r["key"] for r in []}
            by = parse(igb["band"])
            new_igb = {k: v for k, v in igb.items() if k != "band"}
            new_igb = {"scheme": igb["scheme"], "byRoleLevel": by, "label": igb["label"]}
            rec["indicativeGradeOrBand"] = new_igb
            stats["byRoleLevel written"] += 1
            changed = True
        if rec.get("instruments"):
            want = ROLES.get(rid)
            if want is None:
                raise SystemExit(f"{rid}: instrument links without a role decision")
            seen.add(rid)
            links = []
            for x in rec["instruments"]:
                ins = x["instrument"] if isinstance(x, dict) else x
                key = ins.split("/", 1)[1]
                if key not in want:
                    raise SystemExit(f"{rid}: no role for {ins}")
                role, note = want[key]
                item = {"instrument": ins, "role": role}
                if note:
                    item["note"] = {"en": note}
                if isinstance(x, dict) and x.get("role") and x["role"] != role:
                    raise SystemExit(f"{rid}: {ins} already typed {x['role']}")
                links.append(item)
                rows.append({"variant": rid, "instrument": ins, "role": role})
                stats["links typed"] += 1
            rec["instruments"] = links
            changed = True
        ed = (rec.get("editorialNote") or {}).get("en", "")
        if OLD_NOTE in ed:
            rec["editorialNote"] = {"en": ed.replace(OLD_NOTE, NEW_NOTE)}
            changed = True
        if changed:
            if AGENT not in rec["provenance"]["agent"]:
                rec["provenance"]["agent"] = list(rec["provenance"]["agent"]) + [AGENT]
            stats["variants edited"] += 1
            if not a.dry_run:
                L.write_yaml(path, rec)
    missing = set(ROLES) - seen
    if missing:
        raise SystemExit(f"role table names variants with no links: {sorted(missing)}")
    if not a.dry_run:
        (HERE / "generated").mkdir(exist_ok=True)
        (HERE / "generated" / "variant_link_roles.csv").write_text(
            L.csv_text(["variant", "instrument", "role"], rows), encoding="utf-8")
    print(json.dumps({**stats, "roles": Counter(r["role"] for r in rows)}, indent=1))


if __name__ == "__main__":
    main()
