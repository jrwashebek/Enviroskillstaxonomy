#!/usr/bin/env python3
"""WP-06 record generator (authoring aid for A6 DB; not part of the build pipeline).

Reads the authoring sources in docs/build/WP-06/src/*.yaml and writes one record per file under
data/v2/modules/<namespace>/{competencies,tasks,indicators,enactments}/ following docs/standard/AUTHORING_GUIDE.md.
v1 seed records named in a source are edited in place (their id, notation, v1 facets and v1Seed are kept); a v1
seed task whose successor lives in another area is moved there. Re-running is idempotent. Every record written is
listed in docs/build/WP-06/manifest.csv so that counts are generated, never typed.

Usage: python3 docs/build/WP-06/build_wp06.py [src/<ns>.yaml ...]
"""
from __future__ import annotations

import copy
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import emstlib as L  # noqa: E402

DATA = REPO / "data" / "v2"
AGENT = "emstagent:db-agent@wp-06"
TOOL = "claude-opus-5-5"
PROMPT = "wp06-module-authoring@1"
GEN_AT = "2026-10-23T14:30:00Z"
REVIEW_BY = "2027-10-23"
ADR = ["ADR-0018", "ADR-0003", "ADR-0004"]
JV_RX = re.compile(r"\bapplicable\b[^.;]{0,60}\b(requirements|rules|law|laws|regulations|standards)\b|\bjurisdiction'?s requirements\b", re.I)
MANIFEST = HERE / "manifest.csv"


def seed(k: str) -> str:
    return k if k.startswith("seed:") else "seed:" + k


def index_existing():
    idx = {}
    for p in DATA.rglob("*.yaml"):
        idx[p.stem] = p
    return idx


def prov(df=None, sources=None, ev="J", extra_agent=None):
    p = {"method": "llm-assisted", "agent": [AGENT] + ([extra_agent] if extra_agent else []), "generatedAt": GEN_AT}
    if df:
        p["derivedFrom"] = df
    if sources:
        p["sources"] = sources
    p.update({"evidenceLabel": ev, "reviewStatus": "unreviewed", "toolVersion": TOOL, "promptVersion": PROMPT, "adr": ADR})
    return p


def base_tail(rec, module, life, use_tier="describe"):
    rec["layer"] = rec.get("layer")
    rec["module"] = module
    rec["status"] = "draft"
    rec["lifecycleState"] = life
    if life in ("watch", "proposed", "emerging"):
        rec["reviewBy"] = REVIEW_BY
    rec["useTier"] = use_tier
    rec["validationStatus"] = "draft"
    rec["license"] = "CC0-1.0"
    rec["sensitivity"] = "public"
    return rec


class Builder:
    def __init__(self):
        self.idx = index_existing()
        self.manifest = {}
        self.written = set()
        if MANIFEST.exists():
            for r in L.read_csv(MANIFEST):
                self.manifest[r["id"]] = r

    # ------------------------------------------------------------------ helpers
    def path_for(self, rid, module, kind):
        return DATA / "modules" / module / kind / (L.id_to_stem(rid) + ".yaml")

    def existing(self, rid):
        return self.idx.get(L.id_to_stem(rid))

    def write(self, rid, rec, module, kind, origin):
        dest = self.path_for(rid, module, kind)
        old = self.existing(rid)
        L.write_yaml(dest, rec)
        if old and old.resolve() != dest.resolve() and old.exists():
            old.unlink()
            origin = origin + "+moved"
        self.idx[dest.stem] = dest
        self.written.add(rid)
        self.manifest[rid] = {"id": rid, "type": rec["type"], "module": module, "path": str(dest.relative_to(REPO)),
                              "origin": origin}

    # ------------------------------------------------------------------ tasks
    def task(self, t, module, comp_id, comp_sub, comp_life):
        rid = seed(t["id"])
        text = t["text"].strip()
        old_p = self.existing(rid)
        old = L.load_yaml(old_p) if old_p else None
        supports = [{"competency": seed(t.get("comp", comp_id)), "strength": t.get("str", "primary")}]
        for extra in t.get("also", []):
            supports.append({"competency": seed(extra), "strength": "contributing"})
        rec = {"id": rid, "type": "Task", "prefLabel": {"en": text}, "statement": {"en": text},
               "textSha256": L.text_sha256(text), "supports": supports, "workFunction": t["wf"]}
        if t.get("modes"):
            rec["modes"] = t["modes"]
        if t.get("rel"):
            rec["relationshipTypes"] = t["rel"]
        if t.get("prof"):
            rec["workflowProfiles"] = t["prof"]
        rec["fieldDependency"] = t.get("fd", "remote-capable")
        rec["formationDependency"] = str(t.get("form", "no"))
        if t.get("rr") or t.get("cg"):
            rr = dict(t.get("rr") or {})
            if t.get("cg"):
                rr["credentialGate"] = t["cg"]
            rec["reproductionRegime"] = rr
        if t.get("cgs"):
            rec["credentialGates"] = [{"credential": seed(g["credential"]), "kind": g.get("kind", "required")} for g in t["cgs"]]
        if t.get("so"):
            rec["signOffAuthority"] = {"kind": t["so"]}
        if t.get("acc"):
            rec["accountabilityConstraint"] = {"required": True, "basis": {"en": t["acc"]}}
        rec["homeModule"] = module
        rec["subsectors"] = t.get("sub", comp_sub)
        rec["layer"] = "L2"
        base_tail(rec, module, t.get("life", comp_life))
        df = []
        origin = "new"
        if old and old.get("validationStatus") == "seed-v1" or (old and old.get("notation")):
            # rewrite of a migrated v1 task: keep its legacy facets and lineage
            origin = "v1-rewrite"
            for k in ("notation", "v1Tier", "v1Domain", "v1SkillArea"):
                if k in old:
                    rec[k] = old[k]
            for d in (old.get("provenance") or {}).get("derivedFrom") or []:
                d = dict(d)
                if d.get("relation") == "carried":
                    d["relation"] = "rewritten"
                df.append(d)
            rec["editorialNote"] = {"en": "v1 task order (T1 foundational … T3 advanced) is kept as v1Tier for provenance only (ADR-0003 G-2). WP-06 rewrote the statement to v2 task rules and re-pointed it to its module successor."}
        for k in t.get("v1", []) if isinstance(t.get("v1"), list) else ([t["v1"]] if t.get("v1") else []):
            if not any(d.get("v1Key") == k for d in df):
                df.append({"v1Key": k, "relation": "reference-only", "note": "v1 task text used as reference when writing this task"})
        if t.get("note"):
            rec["editorialNote"] = {"en": ((rec.get("editorialNote") or {}).get("en", "") + " " + t["note"]).strip()}
        rec["provenance"] = prov(df or None, t.get("src"))
        self.write(rid, rec, module, "tasks", origin)
        return rid

    # ------------------------------------------------------------------ indicators
    def indicators(self, c, comp_id, module, task_ids, span_min):
        levels = []
        slug = comp_id[len("seed:"):].lower().replace("v1-", "")
        for lvl, items in (c.get("ind") or {}).items():
            ids = []
            for n, it in enumerate(items):
                rid = f"seed:ind-{slug}-{lvl.lower()}-{chr(97 + n)}"
                text = it["t"].strip()
                obs4 = it.get("o", 3)
                rec = {"id": rid, "type": "Indicator", "prefLabel": {"en": it.get("label", text if len(text) <= 90 else text[:87].rsplit(" ", 1)[0] + "…")},
                       "competency": comp_id, "level": lvl, "statement": {"en": text},
                       "augmentationMode": it.get("m", "unaided"), "assessmentMethods": it.get("a", ["work-sample"]),
                       "useClass": it.get("u", "develop"), "obs4": obs4}
                if obs4 == 2:
                    rec["evidencePlan"] = {"en": it.get("ep", "Confirm observability through structured observation by two assessors on a sample of work products before use in development plans.")}
                rec["jurisdictionVariable"] = bool(JV_RX.search(text)) if "jv" not in it else it["jv"]
                st = []
                for s in it.get("st", []):
                    st.append(task_ids.get(s, seed(s)))
                st = list(dict.fromkeys(st))
                if st:
                    rec["servedTasks"] = st
                if lvl != span_min and it.get("att", c.get("att")):
                    rec["distinguishingAttribute"] = it.get("att", c.get("att"))
                if it.get("sc"):
                    rec["safetyOrLegalCritical"] = True
                rec["layer"] = "L1"
                base_tail(rec, module, c.get("life", "established"), use_tier="develop")
                df = [{"v1Key": k, "relation": "rewritten", "note": "v1 indicator rewritten to v2 indicator rules"} for k in it.get("v1", [])]
                rec["provenance"] = prov(df or None)
                self.write(rid, rec, module, "indicators", "new")
                ids.append(rid)
            levels.append({"level": lvl, "indicators": ids})
        return levels

    # ------------------------------------------------------------------ competencies
    def competency(self, c, module_default):
        module = c.get("module", module_default)
        rid = seed(c["id"])
        old_p = self.existing(rid)
        old = L.load_yaml(old_p) if old_p else None
        sub = c["sub"]
        life = c.get("life", "established")
        # tasks first (indicators reference them)
        task_ids = {}
        for t in c.get("tasks", []):
            tid = self.task(t, t.get("module", module), rid, sub, life)
            task_ids[t["id"]] = tid
            own = t["id"].startswith(c["id"] + "-") or (c["id"].startswith("v1-") and t["id"].startswith("db-" + c["id"][3:] + "-"))
            if own:
                task_ids[t["id"].split("-")[-1]] = tid
        rec = {"id": rid, "type": "Competency", "prefLabel": {"en": c["label"].strip()}}
        if c.get("alt"):
            rec["altLabel"] = {"en": c["alt"]}
        rec["definition"] = {"en": c["def"].strip()}
        rec["statement"] = {"en": c["stmt"].strip()}
        if old:
            for k in ("notation",):
                if k in old:
                    rec[k] = old[k]
        rec["competencyType"] = c.get("ctype", "practice")
        rec["levelSpan"] = {"min": c["span"][0], "max": c["span"][1]}
        levels = self.indicators(c, rid, module, task_ids, c["span"][0])
        if levels:
            rec["levels"] = levels
        rec["homeModule"] = module
        rec["subsectors"] = sub
        rec["reusability"] = c.get("reuse", "subsector-specific")
        rec["layer"] = "L1"
        base_tail(rec, module, life)
        df = []
        origin = "new"
        disp_note = ""
        if old and old.get("validationStatus") in ("seed-v1",) or (old and old.get("v1Seed")):
            origin = "v1-rewrite"
            for k in ("v1Domain", "v1SkillArea"):
                if k in old:
                    rec[k] = old[k]
            disp_note = (old.get("editorialNote") or {}).get("en", "").split(" WP-06:")[0]
            for d in (old.get("provenance") or {}).get("derivedFrom") or []:
                d = dict(d)
                if d.get("relation") == "carried":
                    d["relation"] = "rewritten"
                    d["note"] = "v1 title and description rewritten to v2 rules by WP-06"
                df.append(d)
        for d in c.get("df", []):
            if not any(x.get("v1Key") == d["v1Key"] and x.get("relation") == d["relation"] for x in df):
                df.append(d)
        note = (disp_note + " WP-06: " if disp_note else "WP-06: ") + c["note"].strip()
        rec["editorialNote"] = {"en": note}
        rec["provenance"] = prov(df or None, c.get("src"), c.get("ev", "J"))
        if old and "v1Seed" in old:
            rec["v1Seed"] = old["v1Seed"]
        self.write(rid, rec, module, "competencies", origin)
        return rid

    # ------------------------------------------------------------------ enactments
    def enactment(self, e, module):
        comp = seed(e["comp"])
        rid = seed(e["id"])
        task_ids = []
        for t in e.get("tasks", []):
            t = dict(t)
            t.setdefault("comp", comp)
            task_ids.append(self.task(t, module, comp, e["sub"], e.get("life", "established")))
        rec = {"id": rid, "type": "Enactment", "prefLabel": {"en": e["label"].strip()}, "competency": comp,
               "enactmentKind": "module"}
        if e.get("ap"):
            rec["authorityPosition"] = e["ap"]
        rec["enactedInModule"] = module
        if e.get("instr"):
            rec["characteristicInstruments"] = e["instr"]
        if task_ids:
            rec["additionalTasks"] = task_ids
        rec["note"] = {"en": e["note"].strip()}
        rec["layer"] = "L1"
        base_tail(rec, module, e.get("life", "established"))
        rec["editorialNote"] = {"en": "WP-06 module enactment of a core competency (ADR-0018 home-module rule; ADR-0003 G-4). Subsectors: " + ", ".join(e["sub"]) + ". " + e.get("basis", "Basis: DB Phase 2 subsector analysis [J].")}
        rec["provenance"] = prov(None, e.get("src"))
        self.write(rid, rec, module, "enactments", "new")
        return rid

    # ------------------------------------------------------------------ driver
    def run(self, src_files, full=False):
        for f in src_files:
            src = L.load_yaml(f)
            module = src["module"]
            for c in src.get("competencies", []):
                self.competency(c, module)
            for t in src.get("tasks", []):          # stand-alone tasks (e.g. supporting a competency homed elsewhere)
                self.task(t, t.get("module", module), seed(t["comp"]), t["sub"], t.get("life", "established"))
            for e in src.get("enactments", []):
                self.enactment(e, e.get("module", module))
        if full:   # a full run drops records this WP authored earlier that no source defines any more
            for rid, row in list(self.manifest.items()):
                if rid not in self.written and row["origin"].startswith("new"):
                    p = REPO / row["path"]
                    if p.exists():
                        p.unlink()
                    del self.manifest[rid]
        rows = sorted(self.manifest.values(), key=lambda r: (r["module"], r["type"], r["id"]))
        MANIFEST.write_text(L.csv_text(["id", "type", "module", "path", "origin"], rows), encoding="utf-8")


def main(argv):
    files = [Path(a) for a in argv] or sorted((HERE / "src").glob("*.yaml"))
    Builder().run(files, full=not argv)
    print(f"wrote records from {len(files)} source file(s); manifest: {MANIFEST.relative_to(REPO)}")


if __name__ == "__main__":
    main(sys.argv[1:])
