"""WP-03 (Field Craft) record generator library.

Authored content lives in docs/build/WP-03/src/g*_*.py as compact specs (C, T, I below). build_wp03.py turns them
into schema-valid YAML records under data/v2/core/, editing v1 seeds in place (keeping id, notation, legacy facets
and lineage) and creating new records for candidates and split targets. Licence: Apache-2.0 (code).
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402

AGENT = "emstagent:fc-agent@wp-03"
TOOL = "claude-opus-5-5"
PROMPT = "wp03-authoring@1"
GEN = "2026-10-23T14:00:00Z"
CORE = L.DATA_V2 / "core"

MODES = {"u": "unaided", "a": "assisted", "s": "supervisory"}
CYCLE = {"none": "none", "seas": "seasonal", "rare": "multi-year-or-rare-event"}
PLACE = {"gen": "general", "eco": "ecosystem-type", "site": "site-specific", "sys": "system-specific"}
CRED = {"none": "none", "int": "internal-qualification", "ext": "external-certificate", "lic": "licence"}
SPLIT_NOTE = {
    "P": "G-2 split role: execution to protocol (production).",
    "A": "G-2 split role: adaptation or decision in place.",
    "R": "G-2 split role: specification, review or defence of a product.",
    "D": "G-2 split role: design or planning of the work.",
    "F": "G-2 split role: formation of others in the practice.",
}


class T(dict):
    """Task spec. rr = 'mentorship cycle place credentialGate currencyDecay' using the short codes above."""

    def __init__(self, tid, statement, wf, fd, fo, rr, split="P", alias=None, also=(), contrib_only=False,
                 cred=(), modes=(), rel=(), note="", evidence="J", sources=(), repoint_only=False, supports=None):
        super().__init__(id=tid, s=statement, wf=wf, fd=fd, fo=fo, rr=rr, split=split, alias=alias, also=list(also),
                         cred=list(cred), modes=list(modes), rel=list(rel), note=note, evidence=evidence,
                         sources=list(sources), repoint_only=repoint_only, supports=supports,
                         contrib_only=contrib_only)


class I(dict):
    """Indicator spec. m: u|a|s; am: space-separated assessment methods; o: obs4; att: distinguishing attribute."""

    def __init__(self, s, m, am, o=3, att=None, t="", jv=False, crit=False, ev=(), plan=None, d=()):
        super().__init__(s=s, m=m, am=am.split(), o=o, att=att, t=t.split(), jv=jv, crit=crit, ev=list(ev),
                         plan=plan, d=list(d))


class C(dict):
    def __init__(self, cid, label, definition, statement, span, levels, tasks, life="established", review_by=None,
                 use_tier="develop", note="", derived=(), sources=(), evidence="J", alt=(), ctype="practice",
                 tx=None, protect_hint=None):
        lo, hi = span.split("-")
        super().__init__(id=cid, label=label, definition=definition, statement=statement, span=(lo, hi),
                         levels=levels, tasks=tasks, life=life, review_by=review_by, use_tier=use_tier, note=note,
                         derived=list(derived), sources=list(sources), evidence=evidence, alt=list(alt),
                         ctype=ctype, tx=tx, protect_hint=protect_hint)


# ----------------------------------------------------------------------------------------------------------------
def prov(evidence="J", sources=(), derived=None, adr=None):
    p = {"method": "llm-assisted", "agent": [AGENT], "generatedAt": GEN}
    if derived:
        p["derivedFrom"] = derived
    if sources:
        p["sources"] = list(sources)
    p["evidenceLabel"] = evidence
    p["reviewStatus"] = "unreviewed"
    p["toolVersion"] = TOOL
    p["promptVersion"] = PROMPT
    p["adr"] = adr or ["ADR-0003", "ADR-0004", "ADR-0005", "WP-03"]
    return p


def stem_of(rid):
    return L.id_to_stem(rid)


def comp_path(cid):
    return CORE / "competencies" / f"{stem_of(cid)}.yaml"


def task_path(tid):
    return CORE / "tasks" / f"{stem_of(tid)}.yaml"


def ind_path(iid):
    return CORE / "indicators" / f"{stem_of(iid)}.yaml"


def load(p):
    return L.load_yaml(p) if p.exists() else None


def rewrite_derived(old, relation="rewritten"):
    out = []
    for d in old or []:
        d = dict(d)
        if d.get("relation") == "carried":
            d["relation"] = relation
        out.append(d)
    return out


def short_label(s, n=12):
    words = s.rstrip(".").split()
    cut = []
    for w in words:
        cut.append(w)
        if w.endswith(",") or w.endswith(";"):
            cut[-1] = w[:-1]
            break
        if len(cut) >= n:
            break
    return " ".join(cut)


def ind_id(cid, level, letter):
    base = cid[len("seed:"):].lower()
    return f"seed:ind-{base}-{level.lower()}-{letter}"


LEVELS = ["L1", "L2", "L3", "L4", "L5"]


def build_task(t, comp, existing):
    """Return the Task record for spec t (supports comp primary unless overridden)."""
    tid = t["id"]
    supports = t["supports"]
    if supports is None:
        supports = [{"competency": comp["id"], "strength": "contributing" if t["contrib_only"] else "primary"}]
        for a in t["also"]:
            supports.append({"competency": a, "strength": "contributing"})
    mentor, cyc, place, cred, decay = t["rr"].split()
    st = t["s"].strip()
    rec = {"id": tid, "type": "Task", "prefLabel": {"en": st}, "statement": {"en": st},
           "textSha256": L.text_sha256(st), "supports": supports, "workFunction": t["wf"]}
    if t["modes"]:
        rec["modes"] = t["modes"]
    if t["rel"]:
        rec["relationshipTypes"] = t["rel"]
    rec["fieldDependency"] = t["fd"]
    rec["formationDependency"] = t["fo"]
    rec["reproductionRegime"] = {"mentorshipDependence": mentor, "cycleDependence": CYCLE[cyc],
                                 "placeBoundness": PLACE[place], "credentialGate": CRED[cred],
                                 "currencyDecay": decay}
    if t["cred"]:
        rec["credentialGates"] = [{"credential": c, "kind": k} for c, k in t["cred"]]
    if existing and existing.get("notation"):
        rec["notation"] = existing["notation"]
    rec.update({"homeModule": "core", "layer": "L2", "module": "core", "status": "draft",
                "lifecycleState": comp["life"] if comp["life"] in ("established", "emerging") else "established"})
    if rec["lifecycleState"] in ("watch", "proposed", "emerging"):
        rec["reviewBy"] = comp["review_by"]
    rec.update({"useTier": "develop" if comp["use_tier"] == "develop" else "describe", "validationStatus": "draft"})
    if existing:
        for k in ("v1Tier", "v1Domain", "v1SkillArea"):
            if k in existing:
                rec[k] = existing[k]
    note = SPLIT_NOTE[t["split"]]
    if t["note"]:
        note += " " + t["note"]
    if t["rr"].split()[3] != "none":
        note += " Credential gate level is the author's draft pending the WP-07 Credential register (T-8)."
    if existing:
        note += " Rewritten by WP-03 from the v1 seed task; v1 task order is kept as v1Tier for provenance only (ADR-0003 G-2)."
    rec["editorialNote"] = {"en": note}
    rec["license"] = "CC0-1.0"
    rec["sensitivity"] = "public"
    derived = rewrite_derived((existing or {}).get("provenance", {}).get("derivedFrom")) if existing else None
    rec["provenance"] = prov(t["evidence"], t["sources"], derived)
    return rec


def repoint_task(existing, supports, note):
    if existing is None:
        return None
    rec = copy.deepcopy(existing)
    rec["supports"] = supports
    old = (rec.get("editorialNote") or {}).get("en", "")
    rec["editorialNote"] = {"en": (note + " " + old).strip()}
    return rec


def build_indicator(comp, level, letter, i, alias_map, prefix=None):
    iid = ind_id(comp["id"], level, letter) if prefix is None else f"seed:{prefix}-{level.lower()}-{letter}"
    served = []
    for a in i["t"]:
        served.append(alias_map.get(a, a))
    rec = {"id": iid, "type": "Indicator", "prefLabel": {"en": short_label(i["s"])}, "competency": comp["id"],
           "level": level, "statement": {"en": i["s"]}, "augmentationMode": MODES[i["m"]],
           "assessmentMethods": i["am"], "useClass": "develop", "obs4": i["o"]}
    if i["ev"]:
        rec["evidenceTypes"] = i["ev"]
    if i["o"] == 2:
        rec["evidencePlan"] = {"en": i["plan"] or "Double-code OBS-4 with two human coders and collect assessor work samples before develop use (WP-11)."}
    rec["jurisdictionVariable"] = bool(i["jv"])
    if served:
        rec["servedTasks"] = served
    if i["att"]:
        rec["distinguishingAttribute"] = i["att"]
    if i["crit"]:
        rec["safetyOrLegalCritical"] = True
    rec.update({"layer": "L1", "module": "core", "status": "draft",
                "lifecycleState": comp["life"]})
    if comp["life"] in ("watch", "proposed", "emerging"):
        rec["reviewBy"] = comp["review_by"]
    rec.update({"useTier": "develop", "validationStatus": "draft", "license": "CC0-1.0", "sensitivity": "public"})
    derived = [{"v1Key": k, "relation": "rewritten"} for k in i["d"]] or None
    rec["provenance"] = prov("J", (), derived)
    return rec


def build_competency(c, existing, indicator_ids):
    rec = {"id": c["id"], "type": "Competency", "prefLabel": {"en": c["label"]}}
    if c["alt"]:
        rec["altLabel"] = {"en": c["alt"]}
    rec["definition"] = {"en": c["definition"]}
    rec["statement"] = {"en": c["statement"]}
    rec["competencyType"] = c["ctype"]
    if c["tx"]:
        rec["transversalCluster"] = c["tx"]
    rec["levelSpan"] = {"min": c["span"][0], "max": c["span"][1]}
    rec["levels"] = [{"level": lv, "indicators": indicator_ids[lv]} for lv in LEVELS if lv in indicator_ids]
    rec["homeModule"] = "core"
    if existing and existing.get("notation"):
        rec["notation"] = existing["notation"]
    rec.update({"layer": "L1", "module": "core", "status": "draft", "lifecycleState": c["life"]})
    if c["life"] in ("watch", "proposed", "emerging"):
        rec["reviewBy"] = c["review_by"]
    rec.update({"useTier": c["use_tier"], "validationStatus": "draft"})
    if existing:
        for k in ("v1Domain", "v1SkillArea"):
            if k in existing:
                rec[k] = existing[k]
    note = "WP-03 (FC) draft. " + c["note"]
    if existing and existing.get("editorialNote"):
        note += " " + existing["editorialNote"]["en"]
    rec["editorialNote"] = {"en": note.strip()}
    rec["license"] = "CC0-1.0"
    rec["sensitivity"] = "public"
    derived = rewrite_derived(existing["provenance"].get("derivedFrom")) if existing else []
    have = {(d["v1Key"], d["relation"]) for d in derived}
    for key, rel in c["derived"]:
        if (key, rel) not in have:
            derived.append({"v1Key": key, "relation": rel})
    rec["provenance"] = prov(c["evidence"], c["sources"], derived or None,
                             ["ADR-0003", "ADR-0004", "ADR-0005", "ADR-0011", "WP-03"] if derived else None)
    return rec


# aliases used by g6_enactments
W_prov = prov


def build_task_raw(t, spec):
    return build_task(t, spec, None)


def build_indicator_raw(spec, level, letter, i, alias_map, prefix):
    return build_indicator(spec, level, letter, i, alias_map, prefix=prefix)
