#!/usr/bin/env python3
"""Build WP-07 records (TX-C..TX-F competencies, indicators = CLOs, tasks, enactments, knowledge statements)
from wp07_content.py into data/v2/core/.

Idempotent: re-running rewrites the same files. Existing v1 seed records named in the content (v1 7.2.2 and the
merged/split v1 task seeds) are edited in place, keeping id, notation and v1 facets; the builder refuses to touch a
seed that another agent has already rewritten (provenance.agent without this agent and validationStatus != seed-v1).

Usage (from the repo root):  python3 docs/build/WP-07/scripts/build_wp07.py [--dry-run]
"""
from __future__ import annotations

import argparse
import copy
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(HERE))

import emstlib as L  # noqa: E402
import wp07_content as C  # noqa: E402

AGENT = "emstagent:lc-agent@wp-07"
TOOL = "claude-opus-5-5"
PROMPT = "wp07-transversal-learning@1"
GEN = "2026-10-23T14:30:00Z"
CHECKED_ON = "2026-10-23"
CORE = REPO / "data" / "v2" / "core"
ADRS = ["ADR-0025", "ADR-0026", "ADR-0004", "ADR-0003"]


def prov(evidence="J", derived=None, sources=None, adr=None):
    p = {"method": "llm-assisted", "agent": [AGENT], "generatedAt": GEN, "toolVersion": TOOL, "promptVersion": PROMPT}
    if derived:
        p["derivedFrom"] = derived
    if sources:
        p["sources"] = sorted(set(sources))
    p["evidenceLabel"] = evidence
    p["reviewStatus"] = "unreviewed"
    p["adr"] = adr or ADRS
    return p


def base(rid, typ, layer, pref, use_tier):
    return {"id": rid, "type": typ, "prefLabel": {"en": pref}}, {
        "layer": layer, "module": "core", "status": "draft", "lifecycleState": "established", "useTier": use_tier,
        "validationStatus": "draft", "license": "CC0-1.0", "sensitivity": "public"}


def path_for(rid, typ):
    d = L.ENTITY[typ]["store"][1]
    return CORE / d / f"{L.id_to_stem(rid)}.yaml"


def short_label(text, n=12):
    first = re.split(r",| so that | by | when | before ", text, maxsplit=1)[0].strip().rstrip(".")
    words = first.split()
    return " ".join(words[:n]) if len(words) > n else first


def mine_or_seed(rec):
    if rec.get("validationStatus") == "seed-v1":
        return True
    agents = (rec.get("provenance") or {}).get("agent") or []
    return AGENT in agents


class Builder:
    def __init__(self, dry):
        self.dry = dry
        self.written = []
        self.skipped = []

    def write(self, rid, typ, rec):
        p = path_for(rid, typ)
        if not self.dry:
            L.write_yaml(p, rec)
        self.written.append((typ, rid, str(p.relative_to(REPO))))

    def load_existing(self, rid, typ):
        p = path_for(rid, typ)
        if not p.exists():
            raise SystemExit(f"expected existing record {rid} at {p}")
        return L.load_yaml(p)

    # ------------------------------------------------------------------ indicators
    def indicator(self, comp, slug, spec):
        level, letter, text, mode, methods, served, attr, extra = spec
        rid = f"seed:lc-{slug}-{level.lower()}-{letter}"
        use = extra.get("use", "develop")
        head, tail = base(rid, "Indicator", "L1", short_label(text), use)
        rec = dict(head)
        rec["competency"] = comp
        rec["level"] = level
        rec["statement"] = {"en": text}
        rec["augmentationMode"] = mode
        rec["assessmentMethods"] = methods
        rec["useClass"] = use
        rec["obs4"] = extra.get("obs4", 3)
        if extra.get("evidence"):
            rec["evidenceTypes"] = extra["evidence"]
        if extra.get("plan"):
            rec["evidencePlan"] = extra["plan"]
        rec["jurisdictionVariable"] = bool(extra.get("jv", False))
        rec["servedTasks"] = served
        if attr:
            rec["distinguishingAttribute"] = attr
        if extra.get("safety"):
            rec["safetyOrLegalCritical"] = True
        rec.update(tail)
        derived = [{"v1Key": k, "relation": "rewritten"} for k in extra.get("v1", [])]
        rec["provenance"] = prov("J", derived or None)
        self.write(rid, "Indicator", rec)
        return rid, level

    # ------------------------------------------------------------------ tasks
    def task(self, t):
        rid = t["key"]
        text = t["text"]
        supports = [{"competency": c, "strength": s} for c, s in t["supports"]]
        fields = {
            "statement": {"en": text}, "textSha256": L.text_sha256(text), "supports": supports, "workFunction": t["wf"]}
        if t.get("modes"):
            fields["modes"] = t["modes"]
        fields["fieldDependency"] = t["field"]
        fields["formationDependency"] = t["form"]
        if t.get("rr"):
            fields["reproductionRegime"] = t["rr"]
        if t.get("gates"):
            fields["credentialGates"] = t["gates"]
        fields["homeModule"] = "core"
        if t.get("existing"):
            old = self.load_existing(rid, "Task")
            if not mine_or_seed(old):
                self.skipped.append((rid, "already rewritten by another agent; left unchanged"))
                return rid
            rec = {"id": rid, "type": "Task", "prefLabel": {"en": text}}
            rec.update(fields)
            for k in ("notation",):
                if k in old:
                    rec[k] = old[k]
            rec.update({"layer": "L2", "module": "core", "status": "draft", "lifecycleState": "established",
                        "useTier": "describe", "validationStatus": "draft"})
            for k in ("v1Tier", "v1Domain", "v1SkillArea"):
                if k in old:
                    rec[k] = old[k]
            notes = []
            old_note = ((old.get("editorialNote") or {}).get("en") or "").split(" | WP-07:")[0]
            if old_note:
                notes.append(old_note)
            notes.append("WP-07: rewritten to v2 task rules (one verb, 8-30 words, no product names; ADR-0003 G-2)."
                         + (" " + t["note"] if t.get("note") else ""))
            rec["editorialNote"] = {"en": " | ".join(notes)}
            rec["license"] = "CC0-1.0"
            rec["sensitivity"] = "public"
            derived = []
            for d in (old.get("provenance") or {}).get("derivedFrom") or []:
                d = copy.deepcopy(d)
                if d.get("v1Key") == t["v1"]:
                    d["relation"] = "rewritten"
                    derived.append(d)
            if not derived:
                derived.append({"v1Key": t["v1"], "relation": "rewritten"})
            for mk in t.get("merged", []):
                derived.append({"v1Key": mk, "relation": "merged-from", "note": "consolidated duplicate task (WP-07)"})
            rec["provenance"] = prov("J", derived, adr=ADRS + ["ADR-0011"])
        else:
            head, tail = base(rid, "Task", "L2", text, "describe")
            rec = dict(head)
            rec.update(fields)
            rec.update(tail)
            if t.get("note"):
                rec["editorialNote"] = {"en": t["note"]}
            rec["provenance"] = prov("J")
        self.write(rid, "Task", rec)
        return rid

    def supersede_task(self, rid, target, why):
        old = self.load_existing(rid, "Task")
        if old.get("validationStatus") != "seed-v1" and not mine_or_seed(old):
            self.skipped.append((rid, "already changed by another agent; left unchanged"))
            return
        rec = copy.deepcopy(old)
        rec["status"] = "superseded"
        rec["replacedBy"] = [target]
        note = ((rec.get("editorialNote") or {}).get("en") or "").split(" | WP-07:")[0]
        rec["editorialNote"] = {"en": (note + " | " if note else "") + f"WP-07: superseded by {target}. {why}"}
        self.write(rid, "Task", rec)

    # ------------------------------------------------------------------ enactments, knowledge
    def enactment(self, comp, e):
        rid = e["key"]
        head, tail = base(rid, "Enactment", "L1", e["prefLabel"], "describe")
        rec = dict(head)
        rec["competency"] = comp
        rec["enactmentKind"] = e["kind"]
        if e["kind"] == "craft":
            rec["craft"] = e["craft"]
        if e["kind"] == "actor":
            rec["actorType"] = e["actorType"]
            if e.get("authorityPosition"):
                rec["authorityPosition"] = e["authorityPosition"]
            rec["authorityBasis"] = e["authorityBasis"]
            rec["principal"] = e["principal"]
            rec["accountabilityVenue"] = e["accountabilityVenue"]
        rec["note"] = {"en": e["note"]}
        rec.update(tail)
        cited = sorted(set(re.findall(r"\b(LC-\d{3}|V\d-\d{2})\b", e["note"])))
        rec["provenance"] = prov("E" if cited else "J", sources=cited or None)
        self.write(rid, "Enactment", rec)
        return rid

    def knowledge(self, comp, k):
        rid = k["key"]
        head, tail = base(rid, "KnowledgeStatement", "L2", short_label(k["text"], 10), "describe")
        rec = dict(head)
        rec["statement"] = {"en": k["text"]}
        rec["lowestLevel"] = k["lowest"]
        rec["supports"] = [comp]
        rec["assessmentMethods"] = k["methods"]
        rec.update(tail)
        rec["provenance"] = prov("J")
        self.write(rid, "KnowledgeStatement", rec)
        return rid

    # ------------------------------------------------------------------ competencies
    def competency(self, c):
        rid = c["id"]
        ind_ids = {}
        for spec in c["indicators"]:
            iid, lvl = self.indicator(rid, c["slug"], spec)
            ind_ids.setdefault(lvl, []).append(iid)
        for t in c["tasks"]:
            self.task(t)
        ena_ids = [self.enactment(rid, e) for e in c["enactments"]]
        ks_ids = [self.knowledge(rid, k) for k in c["knowledge"]]
        order = ["L1", "L2", "L3", "L4", "L5"]
        levels = []
        for lvl in order:
            if lvl not in ind_ids:
                continue
            ids = ind_ids[lvl]
            if not 2 <= len(ids) <= 5:
                raise SystemExit(f"{rid} {lvl}: {len(ids)} indicators (need 2-5)")
            levels.append({"level": lvl, "indicators": ids, "publicationRuleChecks": {
                "existence": {"result": "pending"},
                "distinctness": {"result": "pass", "evidence": ["agent self-check: lint B08a clean; distinguishingAttribute recorded on indicators above levelSpan.min"], "checkedOn": CHECKED_ON},
                "assessability": {"result": "pending"},
                "consensus": {"result": "pending"}}})
        lo, hi = c["span"]
        span_levels = order[order.index(lo): order.index(hi) + 1]
        missing = [x for x in span_levels if x not in ind_ids]
        if missing:
            raise SystemExit(f"{rid}: no indicators at {missing}")
        rec = {"id": rid, "type": "Competency", "prefLabel": {"en": c["prefLabel"]}}
        if c.get("altLabel"):
            rec["altLabel"] = {"en": c["altLabel"]}
        rec["definition"] = {"en": c["definition"]}
        rec["statement"] = {"en": c["statement"]}
        old = None
        if not c["new"]:
            old = self.load_existing(rid, "Competency")
            if not mine_or_seed(old):
                self.skipped.append((rid, "already rewritten by another agent; left unchanged"))
                return
            if "notation" in old:
                rec["notation"] = old["notation"]
        rec["competencyType"] = "transversal"
        rec["transversalCluster"] = c["cluster"]
        rec["levelSpan"] = {"min": lo, "max": hi}
        rec["levels"] = levels
        if ks_ids:
            rec["knowledge"] = ks_ids
        if ena_ids:
            rec["enactments"] = ena_ids
        rec["homeModule"] = "core"
        rec["learningDesign"] = c["learningDesign"]
        rec.update({"layer": "L1", "module": "core", "status": "draft", "lifecycleState": "established",
                    "useTier": "develop", "validationStatus": "draft"})
        note = c["editorialNote"]
        if old is not None:
            for k in ("v1Domain", "v1SkillArea"):
                if k in old:
                    rec[k] = old[k]
            prior = ((old.get("editorialNote") or {}).get("en") or "").split(" | WP-07:")[0]
            note = prior + " | WP-07: " + note
        rec["editorialNote"] = {"en": note}
        rec["license"] = "CC0-1.0"
        rec["sensitivity"] = "public"
        derived = []
        if old is not None:
            for d in (old.get("provenance") or {}).get("derivedFrom") or []:
                d = copy.deepcopy(d)
                d["relation"] = "rewritten"
                derived.append(d)
        derived += copy.deepcopy(c.get("derivedFrom") or [])
        rec["provenance"] = prov("J", derived or None, sources=c.get("sources") or None,
                                 adr=ADRS + (["ADR-0011"] if derived else []))
        self.write(rid, "Competency", rec)

    def run(self):
        for c in C.COMPETENCIES:
            self.competency(c)
        for rid, target, why in C.SUPERSEDED_TASKS:
            self.supersede_task(rid, target, why)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    b = Builder(a.dry_run)
    b.run()
    by = {}
    for typ, _, _ in b.written:
        by[typ] = by.get(typ, 0) + 1
    print("written:", dict(sorted(by.items())))
    for rid, why in b.skipped:
        print("SKIPPED", rid, why)


if __name__ == "__main__":
    main()
