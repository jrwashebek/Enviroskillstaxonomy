"""Data-driven builder for a competency with its tasks and indicators."""
from lib import Bundle, competency, df, rewrite_seed_competency, rewrite_seed_task, task, write


def build(spec):
    cid = spec["id"]
    seed = spec.get("seed", False)
    tmap = {}
    tasks = []
    for t in spec["tasks"]:
        key, tid = t["key"], t["id"]
        tmap[key] = tid
        sup = t.get("supports") or [cid]
        kw = dict(t.get("kw", {}))
        if spec.get("lifecycle") in ("emerging", "proposed") and "lifecycle" not in kw:
            kw["lifecycle"] = spec["lifecycle"]
        if t.get("rewrite"):
            tasks.append(rewrite_seed_task(tid, t["s"], sup, t["wf"], t["field"], t["form"], **kw))
        else:
            tasks.append(task(tid, t["s"], sup, t["wf"], t["field"], t["form"], **kw))
    b = Bundle(cid, spec["prefix"])
    for row in spec["inds"]:
        lv, st, mode, methods, tkeys = row[:5]
        kw = dict(row[5]) if len(row) > 5 else {}
        if spec.get("lifecycle") in ("emerging", "proposed"):
            kw.setdefault("lifecycle", spec["lifecycle"])
        b.ind(lv, st, mode, methods, [tmap[k] for k in tkeys], **kw)
    b.write_indicators()
    common = dict(cluster=spec.get("cluster"), lifecycle=spec.get("lifecycle", "established"), evidence=spec.get("evidence", "J"),
                  sources=spec.get("sources"), alt=spec.get("alt"), note=spec.get("note"),
                  reusability=spec.get("reusability", "cross-subsector"), enactments=spec.get("enactments"),
                  scope=spec.get("scope"))
    if seed:
        rec = rewrite_seed_competency(cid, spec["title"], spec["definition"], spec["statement"], spec.get("type", "practice"),
                                      spec["span"], b.levels(), extra_derived=spec.get("derived"), **common)
    else:
        rec = competency(cid, spec["title"], spec["definition"], spec["statement"], spec.get("type", "practice"), spec["span"],
                         b.levels(), derived=spec.get("derived"), notation=[{"scheme": "EMST-candidate", "value": cid.split(":")[1]}],
                         **common)
    write(rec)
    for t in tasks:
        write(t)
    return rec, tasks, b.inds


def T(key, tid, s, wf, field, form, supports=None, rewrite=False, **kw):
    return {"key": key, "id": tid, "s": s, "wf": wf, "field": field, "form": form, "supports": supports, "rewrite": rewrite, "kw": kw}
