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
EVIDENCE_NOTICE = ("Task importance, time share, critical and needed-at-entry values are agent drafts (raterType llm, "
                   "validationStatus draft, evidence S): assessment pending (job analysis). They are not job-analysis "
                   "results and no human has reviewed them. Target levels are editorial design drafts. A credential gate "
                   "is shown only when its issuer is verified with a cited source; the other gates are counted, not "
                   "shown, until the issuer is verified (CR-CP-001 C7).")


def gate_view(d, gates):
    """Credential gates for display (CR-CP-001 C7; SPEC §10.5 rule 8): only gates whose Credential has
    issuerVerified.verified = true with sources are listed; the rest are counted."""
    shown, hidden = [], 0
    for g in gates or []:
        iv = ((d.get(g["credential"]) or {}).get("issuerVerified") or {})
        if iv.get("verified") is True and iv.get("sources"):
            shown.append({"credential": g["credential"], "label": d.label(g["credential"]), "kind": g["kind"],
                          "issuerVerifiedSources": iv["sources"]})
        else:
            hidden += 1
    return {"shown": shown, "notShownUntilIssuerVerified": hidden}


def gate_text(gv):
    parts = [f"{g['label']} ({g['kind']})" for g in gv["shown"]]
    if gv["notShownUntilIssuerVerified"]:
        parts.append(f"{gv['notShownUntilIssuerVerified']} not shown until the issuer is verified")
    return "; ".join(parts)
LEVEL_KEYS = ["entry", "journey", "senior", "lead", "strategic"]


def stamp(rule, version, generator):
    """View stamp. The status is read from the registered rule file (vocab/rules/), so a page is never stale about it."""
    status = "not registered"
    f = ROOT / "vocab" / "rules" / f"{rule}@{version}.yaml"
    if f.exists():
        status = f"registered rule, status {L.load_yaml(f).get('status', 'unknown')}"
    return {"ruleId": rule, "ruleVersion": version, "ruleStatus": status, "generator": generator, "asOf": AS_OF}


# ---------------------------------------------------------------- display gate (display-gate@1.1.0; CR-FIX-B-001)
def _gate_engine():
    import importlib.util
    spec = importlib.util.spec_from_file_location("emst_display_gate_views", ROOT / "validation" / "display_gate.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, mod.load_gates()


GATE, GATES = _gate_engine()
TIME_NOTICE = GATES["role_profile_values"]["role_labels"]["fsp_time_share_notice"]
PENDING_JA = GATES["role_profile_values"]["role_labels"]["assessment_pending_job_analysis"]


def role_value(role, field, context):
    """IO's decision for one role-profile bundle field in a view context (validation/display_gate.py#decide_role_value).
    The role record carries the validationStatus and reviewers that govern every bundle value on it."""
    v = {"field": f"RoleProfile.{field}", "validationStatus": role.get("validationStatus"),
         "reviewers": list((role.get("provenance") or {}).get("reviewers") or []), "held": held(role)}
    return GATE.decide_role_value(v, GATES, "describe", context)


def shows(role, field, context):
    return bool(role_value(role, field, context).get("render"))


def held(rec):
    return bool(isinstance(rec, dict) and (rec.get("indigenousDataFlag") or rec.get("approvalStatus") == "pending-tribal-review"
                                           or rec.get("tribalPrograms") is True or rec.get("careFlag") is True))


class Data:
    def __init__(self):
        self.seed_map = L.load_seed_map()
        self.seed_rev = {v: k for k, v in self.seed_map.items()}
        self.mvp_keys = {r["role_key"][:3]: r["role_key"] for r in L.read_csv(ROOT / "docs" / "decisions" / "mvp_role_set.csv")}
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
        """A record by ID; a seed key promoted at WP-16 resolves to its minted record (data/v2/ids/seed_map.csv)."""
        return self.recs.get(rid) or self.recs.get(self.seed_map.get(rid, ""))

    def canon(self, rid):
        """The current ID for a reference: the minted ID when a seed key was promoted, else the reference itself."""
        return self.seed_map.get(rid, rid)

    def seed_of(self, rid):
        return self.seed_rev.get(rid, rid)

    def role_key(self, role):
        """The MVP role key (e.g. R13-resource-program-manager) from the role's MVProleSet notation; stable across
        minting, so generated file names and the report figures that read them do not change."""
        for n in role.get("notation") or []:
            if isinstance(n, dict) and n.get("scheme") == "MVProleSet":
                return self.mvp_keys.get(str(n.get("value")), str(n.get("value")))
        s = self.seed_of(role["id"])
        return s.split(":", 1)[1] if s.startswith("seed:") else L.id_to_stem(s)

    def variant_for(self, role_id, actor):
        """The role's variant for a sector actor, found by variantOf and sectorActor, never by seed-key suffix."""
        hits = sorted((v for v in self.variants_of.get(role_id, []) if v.get("sectorActor") == actor and not held(v)),
                      key=lambda v: (self.seed_of(v["id"]).count("/"), v["id"]))
        return hits[0] if hits else None

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


def duties(data, role, items, context="federal-series-profile"):
    """Major duties grouped by the competency each task primarily supports, in role-record order (display-gate@1.1.0
    `rollups`: job-analysis values never order a view). % time, importance, critical and needed-at-entry are given only
    where the gate renders them in this context; otherwise they are None and the view prints the gate's label."""
    targets = {t["competency"]: t for t in role.get("competencyTargets") or []}
    groups = {}
    for i in items:
        groups.setdefault(primary_target(data, i["task"], targets), []).append(i)
    pct_ok = shows(role, "taskBundle.timeShare", context)
    imp_ok = shows(role, "taskBundle.importance", context)
    crit_ok = shows(role, "taskBundle.critical", context)
    entry_ok = shows(role, "taskBundle.neededAtEntry", context)
    form_ok = shows(role, "taskBundle.formationTask", context)
    out = []
    for cid, its in groups.items():
        out.append({"competency": cid, "duty": data.label(cid),
                    "pctTime": round(100 * sum(i["shareWithin"] for i in its)) if pct_ok else None,
                    "tasks": [{"task": i["task"], "statement": data.statement(i["task"]),
                               "importance": i.get("importance") if imp_ok else None,
                               "critical": i.get("critical", False) if crit_ok else None,
                               "neededAtEntry": i.get("neededAtEntry", False) if entry_ok else None,
                               "formationTask": i.get("formationTask", False) if form_ok else None,
                               "variantAdded": i.get("added", False),
                               "pctTime": round(100 * i["shareWithin"], 1) if pct_ok else None}
                              for i in its]})
    return out


def link_ids(links):
    """Instrument IDs from typed links {instrument, role, note?} (CR-SC-001 #2; ADR-0030) or legacy plain strings."""
    return [x["instrument"] if isinstance(x, dict) else x for x in links or []]


def link_items(d, links):
    """[{id, label, role}] for a typed link list; role None when the link is untyped."""
    return [{"id": i, "label": d.label(i), "role": (x.get("role") if isinstance(x, dict) else None)}
            for x, i in zip(links or [], link_ids(links))]


LEVEL_ORDER = ["entry", "journey", "senior", "lead", "strategic"]


def band_pairs(igb):
    """Bands per role level: from indicativeGradeOrBand.byRoleLevel (CR-FH-001 #6; ADR-0030) when present, otherwise
    from the retired micro-format in `band`. Returns [(band, [roleLevel, ...]), ...]; adjacent levels sharing a band
    are grouped."""
    igb = igb or {}
    by = igb.get("byRoleLevel")
    if by:
        out = []
        for lv in sorted(by, key=lambda k: LEVEL_ORDER.index(k) if k in LEVEL_ORDER else 99):
            if out and out[-1][0] == by[lv]:
                out[-1][1].append(lv)
            else:
                out.append((by[lv], [lv]))
        return out
    return parse_band(igb.get("band"))


def band_text(igb):
    """Human-readable band string for views (same form as the retired micro-format)."""
    igb = igb or {}
    if igb.get("byRoleLevel"):
        return "; ".join(f"{b} [{'|'.join(lv)}]" for b, lv in band_pairs(igb))
    return igb.get("band", "not recorded")


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
    return out              # role-record order: importance is a gated job-analysis value and never orders a view


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
