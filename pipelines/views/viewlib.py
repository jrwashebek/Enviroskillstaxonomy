"""Shared loaders for the WP-08 generated HR views (Federal Series Profile, State Class View, job families, role-change
inputs, mirror links). Read-only over data/v2; writes only under docs/build/WP-08/generated/.

These generators are WP-08 authoring-lane code (ADR-0029 rule 4). They are deterministic so DE can port them into
scripts/ with registered rule files at integration (CR-FH-001). Licence: Apache-2.0.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402

OUT = ROOT / "docs" / "build" / "WP-08" / "generated"
AS_OF = "2026-10-23"
DISCLAIMER = "Not a classification basis / not a job analysis / not for RIF or rating decisions."
EVIDENCE_NOTICE = ("All task importance, time share, critical, needed-at-entry and target-level values are agent drafts "
                   "(raterType llm, validationStatus draft, evidence S). They are not job-analysis results and no human "
                   "has reviewed them. Credential gates and sign-off are shown only as drafts until an E-labelled source "
                   "is attached.")
LEVEL_KEYS = ["entry", "journey", "senior", "lead", "strategic"]


def stamp(rule, version, generator):
    return {"ruleId": rule, "ruleVersion": version, "ruleStatus": "proposed (CR-FH-001; not yet in vocab/rules/)",
            "generator": generator, "asOf": AS_OF}


def held(rec):
    return bool(isinstance(rec, dict) and (rec.get("indigenousDataFlag") or rec.get("approvalStatus") == "pending-tribal-review"
                                           or rec.get("tribalPrograms") is True or rec.get("careFlag") is True))


class Data:
    def __init__(self):
        self.recs = {}
        self.by_type = defaultdict(list)
        self.v1asm = defaultdict(list)
        self.external = defaultdict(list)
        self.signals = []
        for loc, rec in L.iter_records():
            if not isinstance(rec, dict) or "id" not in rec:
                continue
            t = rec.get("type")
            if t == "ExposureAssessment":
                if rec.get("raterType") == "v1-analyst" and rec.get("task"):
                    self.v1asm[rec["task"]].append(rec["id"])
                elif rec.get("raterType") == "external-index":
                    self.external[str(rec.get("targetId", ""))].append(rec)
                elif rec.get("task"):
                    self.v1asm.setdefault("__v2__" + rec["task"], []).append(rec["id"])
                continue
            if t in ("CraftRating", "FunctionRating", "RelevanceRating", "Indicator", "Tool"):
                continue
            if t == "ChangeSignal":
                self.signals.append(rec)
            self.recs[rec["id"]] = rec
            self.by_type[t].append(rec["id"])
        self.series = {r["seriesCode"]: r for r in (self.recs[i] for i in self.by_type["SeriesRecord"])}
        self.ks_by_comp = defaultdict(list)
        for i in self.by_type["KnowledgeStatement"]:
            k = self.recs[i]
            if held(k):
                continue
            sup = k.get("supports") or []
            for c in (sup if isinstance(sup, list) else [sup]):
                c = c.get("competency") if isinstance(c, dict) else c
                self.ks_by_comp[c].append(k)
        self.variants_of = defaultdict(list)
        for i in self.by_type["RoleVariant"]:
            self.variants_of[self.recs[i]["variantOf"]].append(self.recs[i])

    def get(self, rid):
        return self.recs.get(rid)

    def roles(self):
        return [self.recs[i] for i in sorted(self.by_type["RoleProfile"])]

    def tier(self, role):
        for n in role.get("notation") or []:
            if n.get("scheme") == "MVPtier":
                return n["value"]
        return "?"

    def label(self, rid):
        r = self.recs.get(rid) or {}
        return (r.get("prefLabel") or {}).get("en", rid)

    def statement(self, tid):
        r = self.recs.get(tid) or {}
        return (r.get("statement") or {}).get("en", "")


def read_set(path):
    with open(path, encoding="utf-8", newline="") as fh:
        lines = [ln for ln in fh if not ln.startswith("#")]
    return list(csv.DictReader(lines, delimiter="\t", quoting=csv.QUOTE_NONE))


def parse_other(s):
    out = {}
    for part in (s or "").split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def effective_bundle(role, variant):
    drops = set((variant or {}).get("taskDrops") or [])
    items = [dict(i) for i in role.get("taskBundle") or [] if i["task"] not in drops]
    for a in (variant or {}).get("taskAdds") or []:
        items.append(dict(a, added=True))
    return items


def at_levels(items, levels):
    sel = [dict(i) for i in items if set(i.get("roleLevels") or LEVEL_KEYS) & set(levels)]
    tot = sum(i.get("timeShare", 0) for i in sel) or 1
    for i in sel:
        i["shareWithin"] = round(i.get("timeShare", 0) / tot, 3)
    return sel


def primary_target(data, tid, target_ids):
    t = data.get(tid) or {}
    sup = t.get("supports") or []
    for s in sup:
        if s["competency"] in target_ids and s.get("strength") == "primary":
            return s["competency"]
    for s in sup:
        if s["competency"] in target_ids:
            return s["competency"]
    return sup[0]["competency"] if sup else None


def duties(data, role, items):
    targets = {t["competency"]: t for t in role.get("competencyTargets") or []}
    groups = defaultdict(list)
    for i in items:
        groups[primary_target(data, i["task"], targets)].append(i)
    out = []
    for cid, its in groups.items():
        pct = round(100 * sum(i["shareWithin"] for i in its))
        out.append({"competency": cid, "duty": data.label(cid), "pctTime": pct,
                    "tasks": [{"task": i["task"], "statement": data.statement(i["task"]), "importance": i.get("importance"),
                               "critical": i.get("critical", False), "neededAtEntry": i.get("neededAtEntry", False),
                               "formationTask": i.get("formationTask", False), "variantAdded": i.get("added", False),
                               "pctTime": round(100 * i["shareWithin"], 1)}
                              for i in sorted(its, key=lambda x: -x["shareWithin"])]})
    out.sort(key=lambda d: -d["pctTime"])
    return out


def parse_band(band):
    """'GS-5 to GS-7 [entry]; GS-9 to GS-11 [journey]' -> [('GS-5 to GS-7', ['entry']), ...]"""
    out = []
    for part in (band or "").split(";"):
        part = part.strip()
        if not part:
            continue
        if "[" in part and part.endswith("]"):
            b, lv = part[:-1].split("[", 1)
            out.append((b.strip(), [x.strip() for x in lv.split("|")]))
        else:
            out.append((part, []))
    return out


def targets_at(data, role, levels):
    out = []
    for t in role.get("competencyTargets") or []:
        tl = {k: v for k, v in t["targetLevels"].items() if k in levels}
        if not tl:
            continue
        c = data.get(t["competency"]) or {}
        out.append({"competency": t["competency"], "label": data.label(t["competency"]), "targetLevels": tl,
                    "importance": t.get("importance"), "distinguishing": t.get("distinguishing", False),
                    "competencyType": c.get("competencyType"), "transversalCluster": c.get("transversalCluster")})
    out.sort(key=lambda x: (-(x["importance"] or 0), x["competency"]))
    return out


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
