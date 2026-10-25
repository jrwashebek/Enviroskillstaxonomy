#!/usr/bin/env python3
"""rc.1 fix pass, change signals (D-DATA; ADR-0032; DATA_FIX_BRIEF §7). Idempotent: a second run changes nothing.

  m9  `reliability` -> `sourceGrade` (an Admiralty grade of the source, not a statistical reliability).
  M5  `upstreamSource` (one ID per upstream dataset, whatever document `source` cites), `processingChain` (the
      judgment-bearing steps: coder, crosswalk, classifier) and `observationId` (one observation attached to several
      targets shares one ID); `measure.nullReason` says why a Required ci95 or n is null.
  M6  `indeterminate` where the stored data do not establish a direction: OpenLMP signals whose difference interval
      (generated/openlmp_differences.csv, from openlmp_difference.py) or plans-only sensitivity interval includes 0;
      SIG-84J3FBK (value 2,000 against a baseline of 0 from a congressional letter); projection signals whose absolute
      and all-occupation-relative readings disagree. Projection signals attached more broadly than closeMatch are
      capped at confidence low. OpenLMP denominators name what was averaged (documents of three kinds).
      Within one observation, records that share a direction share the lowest stated confidence.
Every record whose direction or confidence changes gets a changeNote for 2.0.0-rc.1.
Run: python3 -I docs/build/rc1-fix/fix_signals.py   Licence: Apache-2.0.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rc1lib as R  # noqa: E402

L = R.L
SIG = L.DATA_V2 / "signals"
GEN = Path(__file__).resolve().parent / "generated"
RELEASE = "2.0.0-rc.1"
CONF_ORDER = ["low", "med", "high"]
GOOD = {"skos:exactMatch", "skos:closeMatch"}

# one upstream dataset, several citing documents (sources.csv / key facts): DC-001, LM-027 and LM-138 are the 2025 OMB
# AI use-case inventory; LM-128 (PPS), LM-129 (Inside Climate News) and FS-029 (GAO) all read OPM workforce data (FH-050)
UPSTREAM = {"DC-001": "LM-138", "LM-027": "LM-138", "LM-128": "FH-050", "LM-129": "FH-050", "FS-029": "FH-050"}
A9 = "coder:emstagent:A9-LM@claude-opus-5-5"
FH_S2A = "coder:emstagent:fh-agent@s2-closeout-a"
X3_SOC = "crosswalk:emst-x3-soc-2018@0.1.0-draft"
X4_OPM = "crosswalk:emst-x4-opm-series-2026-10-23@0.1.0-draft"
OMB_KW = "classifier:wp10-omb-keyword-families@0.2.0"
LMP_KW = "classifier:wp10-openlmp-keyword-families@0.2.0"
# readings of one observation encoded twice with different measure names or denominators (inspected 2026-10-25)
ALIASES = {"emst:core/SIG-33E283Q": "emst:core/SIG-RNE5HKD",       # paid internship postings -43.8% (LM-130)
           "emst:core/SIG-5YMQNBG": "emst:core/SIG-8S0JB1K"}       # three operational FireSat satellites (FS-011)
NULL_REASON = {
    "bls-ep-2025-35": ("projection: BLS publishes no interval for occupational projections",
                       "projection for the whole occupation, not a sample estimate"),
    "ombegov-ai-inventory": ("count of registered use cases in the complete inventory, not a sample",
                             "complete inventory count; no sampling"),
    "opm-ehri-fwd": ("administrative headcount from OPM workforce data, not a sample", "administrative count; no sampling"),
    "gao-opm": ("administrative headcount reported by GAO from OPM data, not a sample", "administrative count; no sampling"),
    "conservation-job-board": ("change in one board's postings; the source gives no interval",
                               "posting counts are not reported by the source"),
    "federal-register-pipeline": ("status of one instrument; no interval applies", "one instrument; not a sample"),
    "crs-appropriations": ("ratio of enacted to requested appropriations; no interval applies", "one appropriations act; not a sample"),
    "nifc-imsr": ("situation-report total for the season to date; no interval published", "complete season count; not a sample"),
    "pnnl-openai-draftnepabench": ("count from one benchmark release; no interval applies", "benchmark size, not a sample of practice"),
    "pnnl-permitai": ("count of available services; no interval applies", "one provider's catalogue; not a sample"),
}
SINGLE_DOC = ("single document or announcement; no interval applies", "single document; not a sample")


def subject_of(r):
    """What was counted, when the value alone does not identify the observation."""
    cp = (r.get("crosswalkPath") or [""])[0]
    m = re.search(r"native SOC (\d{2}-\d{4})", cp)
    if m:
        return "soc:" + m.group(1)
    m = re.search(r"keyword (?:function )?family '([^']+)'", cp)
    if m:
        return "family:" + m.group(1)
    m = re.search(r"coordination tag '([^']+)'", cp)
    if m:
        return "tag:" + m.group(1)
    return ""


def upstream(r):
    return UPSTREAM.get(r["source"], r["source"])


def obs_key(r):
    """Fields this script never edits (the OpenLMP denominator is edited, so those records key on the measure name)."""
    m = r["measure"]
    what = m.get("name") if r.get("independenceKey") == "openlmp-usfs-western-plans" else m.get("denominator")
    return (upstream(r), m.get("value"), what, (r.get("observedPeriod") or {}).get("end"), subject_of(r))


def chain(r, fname):
    steps = []
    agents = (r.get("provenance") or {}).get("agent") or []
    if fname == "s2a-change-view-atoms.jsonl":
        steps += [FH_S2A, A9]                         # attached by FH from a sector-level signal A9-LM coded
    elif any(a.startswith("emstagent:A9-LM") for a in agents):
        steps.append(A9)
    else:
        steps += [f"coder:{a}" for a in agents if not a.startswith("emstagent:wp10-builder")]
    cp = " ".join(r.get("crosswalkPath") or [])
    if "native SOC" in cp and r.get("targetType") in ("RoleProfile", "RoleVariant"):
        steps.append(X3_SOC)
    if re.search(r"OPM series \d{4}|GS-\d{4}", cp) and r.get("targetType") in ("RoleProfile", "RoleVariant"):
        steps.append(X4_OPM)
    if "OMB use case text -> keyword function family" in cp:
        steps.append(OMB_KW)
    if re.search(r"keyword family '[^']+' in plan component text", cp):
        steps.append(LMP_KW)
    return list(dict.fromkeys(steps))


def load_differences():
    p = GEN / "openlmp_differences.csv"
    if not p.exists():
        raise SystemExit("run docs/build/rc1-fix/openlmp_difference.py first")
    return {r["signal_id"]: r for r in L.read_csv(p)}


def includes_zero(lo, hi):
    return float(lo) <= 0 <= float(hi)


def note(r, text):
    notes = list(r.get("changeNote") or [])
    entry = {"release": RELEASE, "note": text}
    if entry not in notes:
        notes.append(entry)
    r["changeNote"] = notes


def main():
    diffs = load_differences()
    files = sorted(SIG.rglob("*.jsonl"))
    allrecs = [(p, json.loads(line)) for p in files for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
    # observation groups (aliases folded into their target's group)
    key_of = {r["id"]: obs_key(r) for _, r in allrecs}
    for a, b in ALIASES.items():
        if a in key_of and b in key_of:
            key_of[a] = key_of[b]
    groups = defaultdict(list)
    for _, r in allrecs:
        groups[key_of[r["id"]]].append(r["id"])
    obs_id = {}
    for k, ids in groups.items():
        rep = min(ids)
        canon = json.dumps({"upstreamSource": k[0], "value": k[1], "denominator": k[2], "end": k[3], "subject": k[4]},
                           sort_keys=True, ensure_ascii=False)
        oid = "obs-" + hashlib.sha256(canon.encode("utf-8")).hexdigest()[:12]
        for i in ids:
            obs_id[i] = oid
        _ = rep
    # direction decisions first (so the group confidence uses the final directions)
    decided = {}
    for p, r in allrecs:
        m = r["measure"]
        d, c, why = r["direction"], r["directionConfidence"], []
        if r["id"] in diffs:
            x = diffs[r["id"]]
            if includes_zero(x["difference_ci_low"], x["difference_ci_high"]):
                d, why = "indeterminate", why + ["the interval of the 2012-rule minus 1982-rule difference includes 0"]
            elif includes_zero(x["plans_only_ci_low"], x["plans_only_ci_high"]):
                d, why = "indeterminate", why + ["the plans-only sensitivity interval of the difference includes 0"]
        if r["id"] == "emst:core/SIG-84J3FBK":
            d, why = "indeterminate", why + ["the stored value (2,000 hires committed for 2026 against 0 in 2025) points up, "
                                             "not down, and rests on a congressional letter with no USDA primary release"]
        if r.get("signalFamily") == "projection":
            base = (m.get("baseline") or {}).get("value")
            v = m.get("value")
            if isinstance(base, (int, float)) and isinstance(v, (int, float)):
                rel = "grow" if v > base else ("decline" if v < 0 else None)
                if rel is None:
                    d, why = "indeterminate", why + [f"projected change {v} is positive but below the all-occupation baseline {base}"]
                elif rel != d:
                    d, why = "indeterminate", why + [f"absolute and baseline-relative readings disagree ({v} vs {base})"]
            if r.get("crosswalkMinMatchType") not in GOOD and c != "low":
                c, why = "low", why + [f"attached through {r.get('crosswalkMinMatchType')}, broader than skos:closeMatch"]
        if d == "indeterminate" and c != "low":
            c = "low"
        decided[r["id"]] = (d, c, why)
    # within one observation, records with the same direction share the lowest confidence
    by_obs = defaultdict(list)
    for _, r in allrecs:
        by_obs[(obs_id[r["id"]], decided[r["id"]][0])].append(r["id"])
    for ids in by_obs.values():
        low = min((decided[i][1] for i in ids), key=CONF_ORDER.index)
        for i in ids:
            d, c, why = decided[i]
            if c != low:
                decided[i] = (d, low, why + ["the same observation is stated with lower confidence on another target"])

    changed_dir = []

    def fix(r, fname):
        out = {}
        for k, v in r.items():
            out["sourceGrade" if k == "reliability" else k] = v
        if "upstreamSource" not in out:
            out = R.insert_after(out, "source", "upstreamSource", upstream(r))
        if not out.get("processingChain"):
            out = R.insert_after(out, "crosswalkMinMatchType", "processingChain", chain(r, fname))
        out = R.insert_after(out, "measure", "observationId", obs_id[r["id"]]) if out.get("observationId") != obs_id[r["id"]] else out
        m = dict(out["measure"])
        reasons = NULL_REASON.get(out.get("independenceKey"), SINGLE_DOC)
        nr = dict(m.get("nullReason") or {})
        if m.get("ci95") is None and "ci95" not in nr:
            nr["ci95"] = reasons[0]
        if m.get("n") is None and "n" not in nr:
            nr["n"] = reasons[1]
        if nr:
            m["nullReason"] = nr
        if r["id"] in diffs:
            x = diffs[r["id"]]
            m["denominator"] = "documents (plans, monitoring reports, monitoring plans), each weighted equally"
            m["difference"] = {
                "value": float(x["difference"]), "ci95": [float(x["difference_ci_low"]), float(x["difference_ci_high"])],
                "method": ("2012-rule minus 1982-rule; paired resample means of the team stream (random.Random(20261023), "
                           "10,000 document resamples per era); percentile interval with linear interpolation "
                           "(docs/build/rc1-fix/openlmp_difference.py)"),
                "sensitivity": {"variant": "plans only (monitoring reports and stand-alone monitoring plans excluded)",
                                "value": float(x["plans_only_difference"]),
                                "ci95": [float(x["plans_only_ci_low"]), float(x["plans_only_ci_high"])],
                                "n": int(x["plans_only_n_2012"]), "baselineN": int(x["plans_only_n_1982"])}}
        out["measure"] = m
        d, c, why = decided[r["id"]]
        if (d, c) != (r["direction"], r["directionConfidence"]):
            out["direction"], out["directionConfidence"] = d, c
            note(out, f"direction {r['direction']} -> {d}, confidence {r['directionConfidence']} -> {c}: " + "; ".join(why)
                 + " (ADR-0032; data-method review M6)")
            changed_dir.append((r["id"], r["direction"], d, r["directionConfidence"], c, "; ".join(why)))
        return out

    for p in files:
        R.edit_jsonl(p, lambda r, fname=p.name: fix(r, fname))
    rows = [{"signal_id": i, "direction_before": a, "direction_after": b, "confidence_before": c, "confidence_after": d,
             "reason": w} for i, a, b, c, d, w in sorted(changed_dir)]
    if rows:
        R.write_report("signal_direction_changes.csv", L.csv_text(list(rows[0]), rows))
    n_obs = len(set(obs_id.values()))
    released = [r for _, r in allrecs if r.get("status") != "draft"]
    print(f"signals {len(allrecs)} ({len(released)} released); distinct observations {n_obs} "
          f"({len({obs_id[r['id']] for r in released})} among released); direction/confidence changes this run {len(rows)}")
    R.summary("fix_signals")


if __name__ == "__main__":
    main()
