#!/usr/bin/env python3
"""WP-08 builder: role specs (src/roles_*.py, src/variants.py, src/families.py) -> one YAML record per file.

Writes  data/v2/<area>/roles/seed-<role_key>.yaml          RoleProfile (37)
        data/v2/<area>/variants/seed-<role_key>--<actor>[--<slice>].yaml   RoleVariant
        data/v2/core/families/seed-fh-family-*.yaml        JobFamily (membership computed by pipelines/views/job_families.py)
        docs/build/WP-08/change_view_inputs.yaml           authored change-view atoms (P1)
        docs/build/WP-08/manifest.csv, counts.json         generated counts (never typed)
Idempotent: a full run removes WP-08 records that no spec defines any more. Authoring tool only (ADR-0029 rule 4).
Licence: Apache-2.0.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))
import wp08lib as W  # noqa: E402
from wp08lib import L  # noqa: E402

import roles_p1  # noqa: E402
import roles_p2  # noqa: E402
import roles_p3p4  # noqa: E402
import variants as VAR  # noqa: E402
import families as FAM  # noqa: E402

DATA = L.DATA_V2
PROBLEMS: list[str] = []


def problem(msg):
    PROBLEMS.append(msg)


def area_dir(area, kind):
    return DATA / ("core" if area == "core" else f"modules/{area}") / kind


def formation_index():
    """Formation-task proposals from WP-07 provisions (by corridor) and WP-03 suggestions (by role)."""
    by_role = {}
    for r in csv.DictReader(open(L.ROOT / "docs/build/WP-03/handoff_wp08_task_bundles.csv", encoding="utf-8")):
        if r["suggest_formationTask"] == "true":
            by_role.setdefault(r["role_key"][:3], set()).add(r["task"])
    prov = set()
    for r in csv.DictReader(open(L.ROOT / "docs/build/WP-07/formation_provisions.csv", encoding="utf-8")):
        prov.add(r["task_id"])
    return by_role, prov


def clamp(idx, cid, level, role_key, rl):
    allowed = idx.levels_of(cid)
    if level in allowed:
        return level
    if not allowed:
        problem(f"{role_key}: {cid} has no published levels; target {level} at {rl} dropped")
        return None
    order = W.LEVEL_ORDER
    best = min(allowed, key=lambda a: abs(order.index(a) - order.index(level)))
    problem(f"{role_key}: {cid} target {level} at {rl} clamped to {best} (published {allowed})")
    return best


def targets(idx, spec):
    out, seen = [], set()
    comps = list(spec.comps)
    present = {c.comp for c in comps}
    for f in W.TX_FLOOR:
        if f not in present:
            override = spec.tx_floor.get(f)
            comps.append(W.C(f, 3 if f in ("DC-CAND-13", "DC-CAND-02") else 2,
                             override or " ".join("L1" for _ in spec.levels)))
    for c in comps:
        cid = W.sk(c.comp)
        if cid in seen:
            problem(f"{spec.key}: duplicate target {cid}")
            continue
        seen.add(cid)
        if not idx.comp_usable(cid):
            problem(f"{spec.key}: target {cid} not usable (missing, superseded, held or seed-v1)")
            continue
        if spec.area == "core" and idx.area.get(cid) != "core":
            problem(f"{spec.key}: core role cannot target module competency {cid}")
            continue
        toks = c.targets.split()
        if len(toks) != len(spec.levels):
            raise SystemExit(f"{spec.key}: {cid} targets {c.targets!r} do not match levels {spec.levels}")
        tl = {}
        for rl, lv in zip(spec.levels, toks):
            if lv == "-":
                continue
            v = clamp(idx, cid, lv, spec.key, rl)
            if v:
                tl[rl] = v
        if not tl:
            continue
        item = {"competency": cid, "targetLevels": tl, "importance": c.imp, "distinguishing": c.dist,
                "criticalForSelection": False}
        out.append(item)
    return out


BASE_TASK = re.compile(r"^seed:(v1-|[A-Z]{2}-C\d+-T\d|[A-Z]{2}-CC-\d+-T\d|FS-C\d+-T\d|LC-C-\d+-T)")
CAP = {5: 4, 4: 3, 3: 2}


def auto_tasks(idx, spec, target_items):
    """P2-P4 starter-kit bundles: primary tasks of the targeted competencies (draft rule in the prompt file)."""
    chosen, seen = [], set()
    allowed = {"core"} | ({spec.area} if spec.area != "core" else set())
    skip = {W.sk(x) for x in spec.skip}
    ranked = sorted(spec.comps, key=lambda c: -c.imp)
    for c in ranked:
        if c.imp < 3:
            continue
        cid = W.sk(c.comp)
        cand = sorted(idx.by_comp.get(cid, []), key=lambda x: (x[0] != "primary", not BASE_TASK.match(x[1]), x[1]))
        n = 0
        for strength, tid in cand:
            if strength != "primary" or tid in seen or tid in skip:
                continue
            if idx.area.get(tid) not in allowed:
                continue
            seen.add(tid)
            chosen.append((c, tid, n))
            n += 1
            if n >= CAP[min(c.imp, 5)]:
                break
    if len(chosen) > 40:
        chosen = chosen[:40]
    items = []
    lowest = spec.levels[0]
    for c, tid, rank in chosen:
        text = idx.text(tid)
        lv = W.heuristic_levels(text, spec.levels)
        crit = c.imp >= 5 and rank < 2
        entry = (lowest in lv) and c.imp >= 4
        imp = c.imp if rank < 2 else max(2, c.imp - 1)
        items.append(W.T(tid.replace("seed:", ""), imp, float(imp), ("C" if crit else "") + ("E" if entry else ""),
                         "".join(k[0] if k != "strategic" else "x" for k in lv)))
    return items


def bundle(idx, spec, target_items, form_role, form_prov):
    tasks = spec.tasks if not spec.auto else auto_tasks(idx, spec, target_items)
    tot = sum(t.w for t in tasks)
    items, seen = [], set()
    target_ids = {t["competency"] for t in target_items}
    for t in tasks:
        tid = W.sk(t.task)
        if tid in seen:
            problem(f"{spec.key}: duplicate task {tid}")
            continue
        seen.add(tid)
        if not idx.task_usable(tid):
            problem(f"{spec.key}: task {tid} not usable (missing, superseded, held or seed-v1)")
            continue
        if spec.area == "core" and idx.area.get(tid) != "core":
            problem(f"{spec.key}: core role cannot bundle module task {tid}")
            continue
        sup = {s["competency"] for s in idx.tasks[tid].get("supports") or []}
        if not sup & target_ids:
            problem(f"{spec.key}: task {tid} supports none of the role's targets ({sorted(sup)})")
        lv = W.lv_from(t.lv, spec.levels) if not spec.auto else [W.ABBR[ch] for ch in t.lv]
        form = "F" in t.flags
        if spec.auto and (tid in form_prov or tid in form_role.get(spec.key[:3], set())) and spec.levels[0] in lv:
            form = True
        it = {"task": tid, "importance": t.imp, "timeShare": round(t.w / tot, 3), "critical": "C" in t.flags,
              "neededAtEntry": "E" in t.flags, "formationTask": form, "roleLevels": lv}
        items.append(it)
    # make time shares sum to exactly 1.000 (rounding residue on the largest share)
    if items:
        resid = round(1.0 - sum(i["timeShare"] for i in items), 3)
        if resid:
            big = max(items, key=lambda i: i["timeShare"])
            big["timeShare"] = round(big["timeShare"] + resid, 3)
    # coverage: every critical competency (importance >= 4) served by >= 1 bundled task
    served = set()
    for i in items:
        for s in idx.tasks[i["task"]].get("supports") or []:
            served.add(s["competency"])
    for tg in target_items:
        if tg["importance"] >= 4 and tg["competency"] not in served:
            problem(f"{spec.key}: critical target {tg['competency']} has no bundled task")
    return items


def role_record(idx, spec, form_role, form_prov):
    tg = targets(idx, spec)
    tb = bundle(idx, spec, tg, form_role, form_prov)
    ncrit = sum(1 for t in tg if t["importance"] >= 4)
    depth = {"P1": (15, 40, 6, 12), "P2": (15, 40, 6, 10)}.get(spec.tier)
    if depth:
        lo, hi, clo, chi = depth
        if not lo <= len(tb) <= hi:
            problem(f"{spec.key}: {len(tb)} tasks outside {lo}-{hi} for {spec.tier}")
        if not clo <= ncrit <= chi:
            problem(f"{spec.key}: {ncrit} critical competencies outside {clo}-{chi} for {spec.tier}")
    rid = W.sk(spec.key)
    note = (f"Tier {spec.tier} ({'full depth' if spec.tier == 'P1' else 'starter-kit depth' if spec.tier == 'P2' else 'what is coming' if spec.tier == 'P3' else 'draft'}). "
            f"{W.DRAFT_NOTICE} LLM-coder gate G0: the critical and needed-at-entry flags are pre-fills for human "
            "verification and never reach G2 (protocol_llm_coder_gate.md section 2). criticalForSelection is false "
            "everywhere: v2.0 is never used for selection. Time shares are relative shares across the whole role "
            "(all levels); views renormalize within a role level. Formation flags follow WP-07 provisions and WP-03 "
            "suggestions where FH agreed. Mirror and mobility links: entryFrom/progressesTo here; mirror pairs in X11.")
    if spec.auto:
        note += (" Starter-kit bundle selected by the WP-08 auto rule (primary tasks of the targeted competencies, "
                 "level and flag heuristics in the prompt file); FH did not review each task individually.")
    if spec.note:
        note += " " + spec.note
    rec = {
        "id": rid, "type": "RoleProfile", "prefLabel": {"en": spec.title},
        "definition": {"en": spec.definition}, "functionStatement": {"en": spec.function},
        "primaryWorkFunction": spec.wf,
        "roleLevels": [{"key": k, "levelBand": W.BANDS[k]} for k in spec.levels],
        "taskBundle": tb, "competencyTargets": tg, "homeModule": spec.area,
        "layer": "L3", "module": spec.area, "status": "draft", "lifecycleState": spec.life,
        "useTier": spec.use_tier, "validationStatus": "draft", "license": "CC0-1.0", "sensitivity": "public",
        "editorialNote": {"en": note},
        "notation": [{"scheme": "MVProleSet", "value": spec.key[:3]}],
    }
    if spec.alt:
        rec["altLabel"] = {"en": spec.alt}
    if spec.entry_from:
        rec["entryFrom"] = [W.sk(x) for x in spec.entry_from]
    if spec.progresses_to:
        rec["progressesTo"] = [W.sk(x) for x in spec.progresses_to]
    if spec.life in ("proposed", "emerging"):
        em = spec.emerging or {}
        rec["evidenceSignals"] = em["signals"]
        rec["feederRoles"] = em["feeders"]
        rec["horizon"] = em["horizon"]
        rec["scenarioSensitivity"] = em["scenarios"]
        rec["counterSignal"] = em["counter"]
        rec["reviewBy"] = em.get("reviewBy", W.REVIEW_BY_EMERGING)
    rec["provenance"] = W.prov(adr=["ADR-0006", "ADR-0017", "ADR-0024", "ADR-0025", "ADR-0029"])
    return rec, tb, tg


ACTOR_WORDS = {"federal": "federal", "state": "state", "local": "local government", "ngo": "nonprofit",
               "private": "private-sector", "academic": "academic", "tribal": "held"}
POS_WORDS = {
    "regulator": "acts as regulator, deciding on or enforcing obligations of others",
    "resource-manager": "acts as resource manager for lands, waters or programmes the employer holds",
    "regulated-party": "acts for a regulated party that holds permits or reporting obligations",
    "service-provider": "delivers the work for another party under contract or agreement",
    "independent-verifier": "provides independent verification or assurance",
    "funder": "administers grants, loans or financial assistance",
    "advocate": "influences decisions without holding authority",
    "advisor-researcher": "provides advice, research or technical assistance without decision authority",
}


def variant_record(idx, spec, v, role_tasks):
    vkey = f"{spec.key}/{v.actor}" + (f"/{v.slice}" if v.slice else "")
    vid = W.sk(vkey)
    label = v.label or f"{spec.title} ({v.actor}{', ' + v.slice.replace('-', ' ') if v.slice else ''})"
    base = {"id": vid, "type": "RoleVariant", "prefLabel": {"en": label}, "variantOf": W.sk(spec.key),
            "sectorActor": v.actor, "authorityPosition": v.pos, "layer": "L3", "module": spec.area,
            "status": "draft", "validationStatus": "draft", "license": "CC0-1.0"}
    if v.actor == "tribal":
        base.update({
            "definition": {"en": "Held placeholder for this sector-actor variant. No content is drafted; authoring, "
                                 "wording and release are reserved to review under ADR-0007 section D."},
            "lifecycleState": "proposed", "reviewBy": W.REVIEW_BY_EMERGING, "useTier": "exploratory",
            "sensitivity": "restricted-governed", "indigenousDataFlag": True,
            "approvalStatus": "pending-tribal-review", "aiUsePermitted": False,
            "editorialNote": {"en": "Held under ADR-0007 section D; excluded from every release artifact. No tasks, "
                                    "instruments, credentials or crosswalks are attached."},
            "provenance": W.prov(adr=["ADR-0007", "ADR-0006"])})
        return vid, base
    defin = f"{spec.title} in a {ACTOR_WORDS[v.actor]} setting: {POS_WORDS[v.pos]}."
    if v.note:
        defin += " " + v.note
    if len(defin.split()) > 60:
        problem(f"{vid}: definition over 60 words")
    base.update({"definition": {"en": defin}, "lifecycleState": spec.life, "useTier": spec.use_tier,
                 "sensitivity": "public"})
    if spec.life in ("proposed", "emerging"):
        base["reviewBy"] = (spec.emerging or {}).get("reviewBy", W.REVIEW_BY_EMERGING)
    for k, val in (("sectorActorSubtype", v.subtype), ("industry", v.industry), ("ownership", v.ownership),
                   ("deliveryModel", v.delivery)):
        if val:
            base[k] = val
    if v.adds:
        adds = []
        for t in v.adds:
            tid = W.sk(t.task)
            if not idx.task_usable(tid):
                problem(f"{vid}: taskAdds {tid} not usable")
                continue
            if spec.area == "core" and idx.area.get(tid) != "core":
                problem(f"{vid}: core variant cannot add module task {tid}")
                continue
            if tid in role_tasks:
                problem(f"{vid}: taskAdds {tid} already in the role bundle")
                continue
            adds.append({"task": tid, "importance": t.imp, "timeShare": round(t.w, 3),
                         "critical": "C" in t.flags, "neededAtEntry": "E" in t.flags,
                         "roleLevels": W.lv_from(t.lv, spec.levels)})
        if adds:
            base["taskAdds"] = adds
    if v.drops:
        drops = [W.sk(d) for d in v.drops]
        for d in drops:
            if d not in role_tasks:
                problem(f"{vid}: taskDrops {d} not in the role bundle")
        base["taskDrops"] = drops
    if v.instruments:
        base["instruments"] = [W.sk(f"ins/{i}") for i in v.instruments]
    if v.gates:
        base["credentialGates"] = [{"credential": W.sk(f"crd-{c}"), "kind": k} for c, k in v.gates]
    if v.signoff:
        kind, creds = v.signoff
        so = {"kind": kind}
        if creds:
            so["credentials"] = [W.sk(f"crd-{c}") for c in creds]
        base["signOffAuthority"] = so
    if v.juris:
        base["jurisdictionalContext"] = v.juris
    if v.band:
        base["indicativeGradeOrBand"] = {"scheme": v.scheme, "band": v.band, "label": "not a classification criterion"}
    if v.actor in ("federal", "state", "local"):
        base["disclaimers"] = [W.DISCLAIMER, W.DRAFT_NOTICE]
    note = ("Variant attributes sectorActor, sectorActorSubtype and authorityPosition are editorial (SPEC section 10 "
            "rule 6). Credential gates and sign-off authority are verified facts only once an E-labelled source is "
            "attached; until then views do not show them (SPEC section 10 rule 8).")
    if v.band:
        note += (" indicativeGradeOrBand is FH judgment from the FH Phase 2 proficiency proposal (report section 6.2), "
                 "never a classification criterion; the bracketed role levels say which band each level is read against.")
    base["editorialNote"] = {"en": note}
    base["provenance"] = W.prov(adr=["ADR-0006", "ADR-0007", "ADR-0017", "ADR-0022"])
    return vid, base


def main():
    idx = W.Index()
    form_role, form_prov = formation_index()
    mvp = W.mvp_roles()
    specs = roles_p1.ROLES + roles_p2.ROLES + roles_p3p4.ROLES
    keys = [s.key for s in specs]
    if sorted(keys) != sorted(mvp):
        raise SystemExit(f"role specs differ from mvp_role_set: missing {set(mvp) - set(keys)}, extra {set(keys) - set(mvp)}")
    written, manifest, change_atoms = set(), [], []
    counts = Counter()
    for spec in specs:
        m = mvp[spec.key]
        want_levels = m["levels"].split("|")
        if want_levels != spec.levels:
            problem(f"{spec.key}: levels {spec.levels} differ from mvp_role_set {want_levels}")
        rec, tb, tg = role_record(idx, spec, form_role, form_prov)
        path = area_dir(spec.area, "roles") / f"{L.id_to_stem(rec['id'])}.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        L.write_yaml(path, rec)
        written.add(path)
        manifest.append({"id": rec["id"], "type": "RoleProfile", "tier": spec.tier, "area": spec.area,
                         "tasks": len(tb), "targets": len(tg),
                         "critical_targets": sum(1 for t in tg if t["importance"] >= 4),
                         "lifecycle": spec.life, "path": str(path.relative_to(L.ROOT))})
        counts[f"roles_{spec.tier}"] += 1
        # variants
        vspecs = VAR.for_role(spec)
        actors_listed = [a.replace("(held)", "") for a in m["sector_actor_variants"].split("|")]
        have = {v.actor for v in vspecs if not v.slice}
        if set(actors_listed) != have:
            problem(f"{spec.key}: variant actors {sorted(have)} differ from mvp_role_set {sorted(actors_listed)}")
        role_tasks = {i["task"] for i in tb}
        for v in vspecs:
            vid, vrec = variant_record(idx, spec, v, role_tasks)
            vpath = area_dir(spec.area, "variants") / f"{L.id_to_stem(vid)}.yaml"
            vpath.parent.mkdir(parents=True, exist_ok=True)
            L.write_yaml(vpath, vrec)
            written.add(vpath)
            manifest.append({"id": vid, "type": "RoleVariant", "tier": spec.tier, "area": spec.area,
                             "tasks": len(vrec.get("taskAdds", [])), "targets": "", "critical_targets": "",
                             "lifecycle": vrec.get("lifecycleState"), "path": str(vpath.relative_to(L.ROOT))})
            counts["variants"] += 1
            counts[f"variants_{v.actor}"] += 1
            if v.actor == "tribal":
                counts["variants_held"] += 1
        for x in spec.change:
            tid = "role" if x.target == "role" else W.sk(x.target)
            if tid != "role" and tid not in role_tasks:
                problem(f"{spec.key}: change claim on {tid}, which is not in the bundle")
            change_atoms.append({"role": W.sk(spec.key), "target": tid, "kind": x.kind, "drivers": x.drivers,
                                 "note": x.note, "instruments": [W.sk(f"ins/{i}") for i in x.instruments],
                                 "signals": [W.sk(s) for s in x.signals]})
    for frec in FAM.records():
        fpath = DATA / "core" / "families" / f"{L.id_to_stem(frec['id'])}.yaml"
        fpath.parent.mkdir(parents=True, exist_ok=True)
        L.write_yaml(fpath, frec)
        written.add(fpath)
        manifest.append({"id": frec["id"], "type": "JobFamily", "tier": "", "area": "core", "tasks": "", "targets": "",
                         "critical_targets": "", "lifecycle": frec["lifecycleState"], "path": str(fpath.relative_to(L.ROOT))})
        counts["families"] += 1
    # remove stale WP-08 records
    for kind in ("roles", "variants", "families"):
        for p in DATA.glob(f"**/{kind}/*.yaml"):
            if p not in written:
                rec = L.load_yaml(p)
                if AGENT_MATCH(rec):
                    p.unlink()
                    counts["removed_stale"] += 1
    hdr = ["# WP-08 change-view inputs: authored atoms (agent drafts, raterType llm, validationStatus draft, evidence S).",
           "# Joined with signals, external context and v1 prior evidence by pipelines/views/change_view.py.",
           "# kind: vocab/change_types.yaml content_change_types (tasks) or role_signal_types (role). Licence: CC0-1.0."]
    (HERE / "change_view_inputs.yaml").write_text("\n".join(hdr) + "\n" + L.dump_yaml(
        {"generatedBy": "docs/build/WP-08/build_wp08.py", "raterType": "llm", "model": W.MODEL, "prompt": W.PROMPT,
         "validationStatus": "draft", "evidenceLabel": "S", "atoms": change_atoms}), encoding="utf-8")
    counts["change_atoms"] = len(change_atoms)
    with open(HERE / "manifest.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(manifest[0].keys()))
        w.writeheader()
        w.writerows(manifest)
    counts["problems"] = len(PROBLEMS)
    (HERE / "counts.json").write_text(json.dumps(dict(sorted(counts.items())), indent=1) + "\n", encoding="utf-8")
    (HERE / "build_problems.txt").write_text("\n".join(PROBLEMS) + ("\n" if PROBLEMS else ""), encoding="utf-8")
    print(json.dumps(dict(sorted(counts.items())), indent=1))
    for p in PROBLEMS:
        print("PROBLEM:", p)


def AGENT_MATCH(rec):
    return isinstance(rec, dict) and W.AGENT in ((rec.get("provenance") or {}).get("agent") or [])


if __name__ == "__main__":
    main()
