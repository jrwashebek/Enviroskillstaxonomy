#!/usr/bin/env python3
"""CA integration review of Sprint S1 (ADR-0030 §3). Read-only over data/v2 and the disposition CSVs.

Writes, next to this file:
  s1_core_size.csv      one row per core competency in the rc.1 projection (authored, unauthored seed, planned, held)
  s1_core_size.json     counts generated from s1_core_size.csv (never typed), before and after the ADR-0030 merges
  s1_duplicate_scan.csv competency pairs whose titles or statements are similar (TF-IDF cosine), with lanes
  s1_tribal_hold.json   Tribal-hold leak check over releasable (non-held) records

Usage: python3 docs/decisions/integration/s1_integration_review.py
This is a CA review tool. CI and the release build never run it (ADR-0029 rule 4); the normative core count is
`counts@1.0.0#coreCompetencies` in the release build.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import emstlib as L  # noqa: E402

DEAD = {"superseded", "withdrawn", "deprecated"}
LANE = {"wp-03": "FC/WP-03", "wp-04": "DC/WP-04", "wp-05": "SC/WP-05", "wp-06": "DB/WP-06", "wp-07": "LC/WP-07"}

# ADR-0030 §3.1 merges (absorbed -> survivor). Applied by authors in S2 (WP-08 brief) or WP-16; listed here so the
# projection after merges is generated, not typed.
MERGES = {
    "seed:v1-5.6.1": "seed:v1-5.6.4",   # behaviour-change theory KA -> knowledge statements of behaviour-change programmes
    "seed:v1-5.5.4": "seed:v1-5.1.1",   # public relations -> communicating technical information (public-information tasks)
    "seed:v1-5.4.3": "seed:v1-3.3.1",   # volunteer programme management -> supervision (volunteer workforce context)
    "seed:v1-3.1.5": "seed:v1-3.2.5",   # performance monitoring and evaluation -> adaptive management cycle
    "seed:v1-3.3.5": "seed:SC-C02",     # records management -> defensible administrative record (retention, disclosure)
}


def lane_of(rec) -> str:
    agents = (rec.get("provenance") or {}).get("agent") or []
    for a in agents:
        for k, v in LANE.items():
            if k in a:
                return v
    return "v1-seed (unauthored)" if rec.get("validationStatus") == "seed-v1" else "other"


def label(rec) -> str:
    p = rec.get("prefLabel") or {}
    return p.get("en", "") if isinstance(p, dict) else str(p)


def text(rec, key) -> str:
    v = rec.get(key) or {}
    return v.get("en", "") if isinstance(v, dict) else str(v or "")


def main() -> int:
    recs = {}
    for loc, rec in L.iter_records():
        if isinstance(rec, dict) and rec.get("id"):
            recs[rec["id"]] = (loc, rec)
    hold = L.load_yaml(REPO / "data/v2/governance/tribal_hold.yaml")
    held_keys = set(hold.get("heldSeedKeys") or [])

    # ---- 1. core size -------------------------------------------------------------------------------------
    rows = []
    for rid, (loc, rec) in sorted(recs.items()):
        if rec.get("type") != "Competency" or rec.get("module") != "core" or rec.get("status") in DEAD:
            continue
        state = "unauthored-v1-seed" if rec.get("validationStatus") == "seed-v1" else "authored"
        rows.append({"key": rid, "prefLabel": label(rec), "competencyType": rec.get("competencyType") or "unset",
                     "transversalCluster": rec.get("transversalCluster") or "", "state": state,
                     "held": str(rid in held_keys).lower(), "lane": lane_of(rec), "source": loc.path.name})
    have = {r["key"] for r in rows}
    for r in L.read_csv(REPO / "docs/decisions/candidate_disposition.csv"):
        k = "seed:" + r["cand_id"]
        if r["decision"] == "core-v2.0" and k not in recs:
            rows.append({"key": k, "prefLabel": r["proposed_title"], "competencyType": "practice",
                         "transversalCluster": "", "state": "planned-unauthored", "held": str(k in held_keys).lower(),
                         "lane": "", "source": "candidate_disposition.csv"})
            have.add(k)
    for r in L.read_csv(REPO / "data/v2/migration/v1_targets.csv"):
        k = r.get("target_key")
        if r.get("area") == "core" and r.get("target_kind") in ("v1-seed", "split-new", "candidate") and k \
                and k not in recs and k not in have:
            rows.append({"key": k, "prefLabel": r.get("target_raw", ""), "competencyType": "practice",
                         "transversalCluster": "", "state": "planned-unauthored",
                         "held": str(k in held_keys or r.get("held") == "true").lower(), "lane": "",
                         "source": "v1_targets.csv"})
            have.add(k)
    for r in rows:
        r["mergedInto_ADR0030"] = MERGES.get(r["key"], "")
    hdr = ["key", "prefLabel", "competencyType", "transversalCluster", "state", "held", "lane", "mergedInto_ADR0030",
           "source"]
    (HERE / "s1_core_size.csv").write_text(L.csv_text(hdr, rows), encoding="utf-8")

    def tally(rs):
        return {"total": len(rs),
                "nonHeld": sum(r["held"] == "false" for r in rs),
                "held": sum(r["held"] == "true" for r in rs),
                "byState": dict(sorted(Counter(r["state"] for r in rs).items())),
                "byKind": dict(sorted(Counter(r["competencyType"] for r in rs).items())),
                "byLane": dict(sorted(Counter(r["lane"] or "planned" for r in rs).items()))}
    after = [r for r in rows if not r["mergedInto_ADR0030"]]
    size = {"rule": "ADR-0003 G-9: core 120-180 (practice + knowledge areas + transversal), held items included",
            "liveRecordsNow": tally([r for r in rows if r["state"] != "planned-unauthored"]),
            "projectionRc1": tally(rows),
            "projectionAfterADR0030Merges": tally(after),
            "mergesListed": len(MERGES),
            "range": [120, 180]}
    (HERE / "s1_core_size.json").write_text(json.dumps(size, indent=1) + "\n", encoding="utf-8")

    # ---- 2. duplicate scan ------------------------------------------------------------------------------
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    comps = [(rid, loc, rec) for rid, (loc, rec) in sorted(recs.items())
             if rec.get("type") == "Competency" and rec.get("status") not in DEAD and rid not in held_keys]

    def stem(tok: str) -> str:
        for suf in ("ations", "ation", "ments", "ment", "ings", "ing", "ies", "es", "s", "ed"):
            if len(tok) > len(suf) + 3 and tok.endswith(suf):
                return tok[: -len(suf)]
        return tok

    def norm(s: str) -> str:
        return " ".join(stem(t) for t in re.findall(r"[a-z]+", s.lower()))
    titles = [norm(label(r)) for _, _, r in comps]
    bodies = [norm(label(r) + ". " + text(r, "statement") + " " + text(r, "definition")) for _, _, r in comps]
    tv = TfidfVectorizer(stop_words="english", sublinear_tf=True).fit(bodies)
    st = cosine_similarity(tv.transform(titles))
    sb = cosine_similarity(tv.transform(bodies))
    pairs = []
    for i in range(len(comps)):
        for j in range(i + 1, len(comps)):
            if st[i, j] >= 0.35 or sb[i, j] >= 0.30:
                a, b = comps[i], comps[j]
                pairs.append({"a": a[0], "a_title": titles[i], "a_module": a[2].get("module"), "a_lane": lane_of(a[2]),
                              "b": b[0], "b_title": titles[j], "b_module": b[2].get("module"), "b_lane": lane_of(b[2]),
                              "title_cos": f"{st[i, j]:.2f}", "text_cos": f"{sb[i, j]:.2f}",
                              "cross_lane": str(lane_of(a[2]) != lane_of(b[2])).lower()})
    pairs.sort(key=lambda p: (-float(p["text_cos"]), -float(p["title_cos"])))
    (HERE / "s1_duplicate_scan.csv").write_text(
        L.csv_text(list(pairs[0].keys()) if pairs else ["a"], pairs), encoding="utf-8")

    # ---- 3. Tribal hold ---------------------------------------------------------------------------------
    trig = re.compile(r"\b(tribal|tribe|tribes|indigenous|native american|alaska native|native hawaiian|treaty|"
                      r"sovereign|thpo|government-to-government|ancsa|traditional ecological knowledge|tek)\b", re.I)
    held_records, releasable_hits = [], []
    for rid, (loc, rec) in sorted(recs.items()):
        flagged = (rid in held_keys or rec.get("approvalStatus") == "pending-tribal-review"
                   or rec.get("indigenousDataFlag") is True or rec.get("sectorActor") == "tribal"
                   or rec.get("actorType") == "tribal")
        if flagged:
            held_records.append(rid)
            continue
        if rec.get("status") in DEAD:
            continue
        for path, s in L.iter_strings(rec):
            if path and path[0] in ("editorialNote", "provenance", "v1Seed", "v1Values", "id", "derivedFrom"):
                continue
            m = trig.search(s)
            if m:
                releasable_hits.append({"record": rid, "file": str(loc.path.relative_to(REPO)),
                                        "field": ".".join(str(p) for p in path), "term": m.group(0),
                                        "context": s[max(0, m.start() - 60): m.end() + 60]})
    out = {"heldRecordsPresent": len(held_records), "releasableRecordsWithTriggerTerms": len(releasable_hits),
           "hits": releasable_hits}
    (HERE / "s1_tribal_hold.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"core": size["projectionRc1"], "afterMerges": size["projectionAfterADR0030Merges"],
                      "duplicatePairs": len(pairs), "tribal": {k: v for k, v in out.items() if k != "hits"}}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
