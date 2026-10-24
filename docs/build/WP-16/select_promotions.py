#!/usr/bin/env python3
"""Select the draft records that rc.1 publishes, for promotion to `candidate` (ADR-0031 §6). Read-only over data/v2.

A record is promoted when every condition holds:
  1. status draft, seed key, validationStatus not seed-v1 (unauthored v1 seeds are never released; ADR-0030 §4);
  2. not held (Tribal hold: flags, held keys, held v1 lineage, or a dependent link to held content; ADR-0007 §D);
  3. not excluded by another release-gate rule (third-party index licence, quarantined signal, placeholder target,
     organization measure with n < 5, withheld for an unverified claims-register row);
  4. in core, the registers, a wave-1 module, or one of the early drafts the dispositions name in a wave-2 module
     (FH-C03 and role R19 in worklands; IA-CC-05 in extract) (gate item 4; ADR-0018);
  5. its dependent links (task, competency, subject, targetId, variantOf, supports, instrument) resolve to records
     that are themselves promoted (fixed point), so the release is referentially closed on what a record depends on.
Writes generated/promote_keys.txt (one key per line) and generated/promotion_summary.csv.
Licence: Apache-2.0.
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import wp16lib as W  # noqa: E402

L = W.L
sys.path.insert(0, str(L.ROOT / "scripts"))
import build_release as BR  # noqa: E402

WAVE1 = {"water", "waterq", "air", "waste", "envhealth", "hazards", "forest", "wildlife", "parks"}
EARLY = {"worklands", "extract"}
DEP_FIELDS = ("task", "competency", "subject", "targetId", "variantOf", "instrument")


def dependent_refs(rec):
    out = [rec.get(f) for f in DEP_FIELDS]
    sup = rec.get("supports")
    sup = sup if isinstance(sup, list) else ([sup] if sup else [])
    sup_refs = [s.get("competency") if isinstance(s, dict) else s for s in sup]
    return [x for x in out if isinstance(x, str) and L.is_record_ref(x)], [x for x in sup_refs if isinstance(x, str) and L.is_record_ref(x)]


def main():
    b = BR.Builder(L.DATA_V2, "preview", "2.0.0-dev")
    reason = {}
    cand = set()
    for rid, rec in b.records.items():
        if rec.get("type") == "VocabularyTerm":
            continue
        if not L.is_seed(rid):
            reason[rid] = "already minted"
            continue
        if rec.get("status") != "draft":
            reason[rid] = f"status {rec.get('status')}"
            continue
        if rec.get("validationStatus") == "seed-v1":
            reason[rid] = "unauthored v1 seed"
            continue
        if b.is_held(rid, rec) or b.depends_on_held(rec):
            reason[rid] = "held"
            continue
        if rec.get("license") == BR.THIRD_PARTY_LICENSE:
            reason[rid] = "third-party index licence"
            continue
        if rid in b.withheld or (rec.get("type") == "DriverEvent" and rec.get("instrument") in b.withheld):
            reason[rid] = "withheld (unverified register row)"
            continue
        if b.quarantined(rec) or str(rec.get("targetId", "")).startswith("mvp-role:") or (
                rec.get("type") == "ChangeSignal" and rec.get("targetType") == "organization"
                and isinstance((rec.get("measure") or {}).get("n"), int) and rec["measure"]["n"] < 5):
            reason[rid] = "release-gate exclusion (signal)"
            continue
        ns = rec.get("module") or "core"
        if ns != "core" and ns not in WAVE1 and ns not in EARLY:
            reason[rid] = f"wave-2/3 module {ns}"
            continue
        cand.add(rid)
    # early drafts in wave-2 namespaces must be exactly the FH-C03 / R19 / IA-CC-05 families
    early = sorted(r for r in cand if (b.records[r].get("module") in EARLY))
    fam = ("FH-C03", "fh-c03", "R19-soil-conservationist", "IA-CC-05", "ia-cc-05")
    stray = [r for r in early if not any(f in r for f in fam)]
    if stray:
        raise SystemExit(f"unexpected wave-2 drafts: {stray[:10]}")
    # fixed point on dependent links
    changed = True
    while changed:
        changed = False
        for rid in sorted(cand):
            rec = b.records[rid]
            deps, sups = dependent_refs(rec)
            bad = [d for d in deps if d not in cand and not L.is_emst_id(d)]
            if bad or (sups and not any(s in cand or L.is_emst_id(s) for s in sups)):
                cand.discard(rid)
                reason[rid] = f"depends on a record not promoted ({(bad or sups)[0]})"
                changed = True
    for rid in cand:
        reason[rid] = "promote"
    out = HERE / "generated"
    out.mkdir(exist_ok=True)
    (out / "promote_keys.txt").write_text("".join(k + "\n" for k in sorted(cand)), encoding="utf-8")
    summary = Counter((b.records[r].get("type"), (b.records[r].get("module") or "core"),
                       v if not v.startswith("depends on") else "depends on a record not promoted") for r, v in reason.items())
    rows = [{"type": t, "module": m, "outcome": o, "records": n} for (t, m, o), n in sorted(summary.items(), key=lambda x: tuple(map(str, x[0])))]
    (out / "promotion_summary.csv").write_text(L.csv_text(["type", "module", "outcome", "records"], rows), encoding="utf-8")
    dep = sorted((r, v) for r, v in reason.items() if v.startswith("depends on"))
    (out / "promotion_dependency_drops.csv").write_text(L.csv_text(["id", "reason"], [{"id": r, "reason": v} for r, v in dep]), encoding="utf-8")
    print(f"promote {len(cand)}; not promoted {len(reason) - len(cand)}")
    print(Counter(v if not v.startswith("depends") else "depends on a record not promoted" for v in reason.values()))


if __name__ == "__main__":
    main()
