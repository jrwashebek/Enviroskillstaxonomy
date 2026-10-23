#!/usr/bin/env python3
"""Data-quality audit of the normalized v1 baseline.

    python scripts/audit_v1.py          # reads data/v1_baseline/, writes data/v1_baseline/qa/

Every number in docs/audit/data-audit.md comes from qa/metrics.json or a qa/*.csv written here.
Heuristics (genericity, task structure, tool mentions, near-duplicates) are documented inline and in the
audit; they are screening tools for human review, not verdicts.
Requires scikit-learn (TF-IDF) in addition to the standard library.
"""
from __future__ import annotations

import csv
import io
import json
import re
import statistics
from collections import Counter, OrderedDict, defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "v1_baseline"
QA = BASE / "qa"
DIMS = ["auto_type", "tacit_density", "career_ladder", "vector", "horizon"]


def load(name, sub=""):
    p = BASE / sub / f"{name}.csv"
    with p.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(name, rows, cols):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, lineterminator="\n", extrasaction="ignore")
    w.writeheader()
    for r in rows:
        w.writerow({c: ("" if r.get(c) is None else ("|".join(map(str, r[c])) if isinstance(r.get(c), (list, tuple))
                                                      else r[c])) for c in cols})
    (QA / f"{name}.csv").write_text(buf.getvalue(), encoding="utf-8")


def pct(a, b):
    return round(100.0 * a / b, 1) if b else None


def code_key(c):
    return tuple(int(x) for x in c.split("."))


# ----------------------------------------------------------------------------- genericity heuristic
# Lead-phrase classes for proficiency statements (Knowledge / Application) and indicators.
# Rule: classify on the first one-to-three words, lower-cased. Order matters (first match wins).
STATUS_INFLUENCE = [r"shapes\b", r"transforms\b", r"leads transformative", r"advances\b", r"influences\b",
                    r"is recognized", r"recognized (as|authority|leader)", r"thought leader", r"provides (strategic |expert )?"
                    r"(leadership|vision|direction)", r"sets (the )?(direction|agenda|vision)", r"pioneers\b",
                    r"champions\b", r"drives (field|sector|innovation)", r"defines (the )?field"]
COGNITIVE_STATE = [r"understands\b", r"knows\b", r"is aware", r"aware of", r"familiar", r"appreciates\b",
                   r"has (basic |working |deep )?(knowledge|understanding|awareness)", r"comprehends\b",
                   r"expert in\b", r"deep (understanding|knowledge|expertise)", r"broad knowledge",
                   r"knowledgeable", r"grasps\b", r"recognizes (the )?(importance|value|need|role)"]
VAGUE_ACTION = [r"applies\b", r"supports\b", r"assists\b", r"participates\b", r"contributes\b", r"helps\b",
                r"engages\b", r"works (with|on|in)\b", r"is able to", r"demonstrates\b", r"manages\b", r"leads\b",
                r"oversees\b", r"directs\b", r"provides\b", r"handles\b", r"follows\b", r"uses\b"]


def classify_statement(text):
    t = (text or "").strip().lower()
    if not t:
        return "blank"
    for cls, pats in (("status_influence", STATUS_INFLUENCE), ("cognitive_state", COGNITIVE_STATE),
                      ("vague_action", VAGUE_ACTION)):
        for p in pats:
            if re.match(p, t):
                return cls
    return "observable_action"


NON_OBSERVABLE = {"status_influence", "cognitive_state"}


def template_of(text, title):
    """Replace the competency's own title words with <X> to expose cross-competency templates."""
    words = {w for w in re.findall(r"[a-z]+", (title or "").lower()) if len(w) > 3}
    toks = re.findall(r"[A-Za-z]+|[^A-Za-z\s]", (text or "").lower())
    out = []
    for tk in toks:
        out.append("<x>" if tk in words or tk.rstrip("s") in words else tk)
    s = " ".join(out)
    return re.sub(r"(<x> ?)+", "<x> ", s).strip()


# ----------------------------------------------------------------------------- task-statement heuristic
PURPOSE = re.compile(r"\b(to|for|in order to|so that|that|ensuring|ensure|based on|using|with|under|across|within|"
                     r"against|according to|in accordance with|by)\b", re.I)
OUTCOME_ONLY = re.compile(r"\b(to|for|in order to|so that|ensuring|ensure|that)\b", re.I)
TOOL_TERMS = re.compile(r"\b(ArcGIS|QGIS|ArcPro|ENVI|eCognition|Google Earth Engine|GEE|R\b|Python|SQL|MATLAB|SAS|SPSS|Excel|"
                        r"Tableau|Power BI|InVEST|ARIES|FVS|IMPLAN|HEC-RAS|SWAT|MS Project|Microsoft Project|Asana|"
                        r"Smartsheet|Gantt|Survey123|Fulcrum|Collector|Field Maps|iNaturalist|eBird|PlantNet|LiDAR|"
                        r"Blender|Unity|Unreal|3ds Max|CityEngine|Zoom|Teams|Slack|SharePoint|ChatGPT|LLM|TensorFlow|"
                        r"PyTorch|Wildlife Insights|MaxEnt|Program MARK|Distance|BEHAVE|FARSITE|FlamMap|WFDSS|IFTDSS)\b")


def task_structure(text, verbs):
    toks = (text or "").split()
    if not toks:
        return dict(verb_first=False, has_object=False, has_purpose=False, has_outcome=False, n_words=0)
    first = toks[0].strip(",;:").lower()
    after = " ".join(toks[1:])
    return dict(verb_first=first in verbs, first_word=first, has_object=len(toks) >= 3,
                has_purpose=bool(PURPOSE.search(after)), has_outcome=bool(OUTCOME_ONLY.search(after)),
                n_words=len(toks), n_verbs_conjoined=len(re.findall(r"\b(and|or)\b", " ".join(toks[:4]).lower())))


# Imperative verbs seen in first position (curated from the 666 tasks; non-verbs excluded by review).
TASK_VERBS = set("""
adapt address administer advise advocate align allocate analyze anticipate apply appraise apply arrange assess assist
audit balance brief build calculate calibrate capture categorize certify champion classify clean coach co-design
collaborate collect combine communicate compare compile complete comply conduct configure connect construct consult
contribute convene coordinate correlate create cultivate curate debrief decide define deliver demonstrate deploy design
detect determine develop diagnose digitize direct document download draft educate employ enforce engage enhance ensure
establish estimate evaluate examine execute explain export facilitate forecast foster gather generate guide help
identify implement improve incorporate inform input inspect install integrate interpret inventory investigate issue
launch lead leverage liaise link log maintain manage map measure mediate mentor merge migrate mitigate model monitor
motivate navigate negotiate observe obtain operate optimize organize oversee participate partner perform pilot plan
predict prepare present prioritize process procure produce program promote propose protect provide publish quantify
recommend reconcile record recruit reduce refine report represent research resolve respond restore review run
safeguard sample schedule screen secure select serve set share simulate site solicit source speak standardize
streamline structure study submit summarize supervise support survey sustain synthesize tailor teach test track train
transfer translate troubleshoot update use utilize validate verify visualize weigh work write
accept access attend break broker cite customize describe drive equip escalate follow greet harmonize include
justify listen mop plant prune remove respect scout seek service sync tag transport upload
""".split())


def main():
    QA.mkdir(parents=True, exist_ok=True)
    comp = load("competencies")
    tasks = load("tasks")
    prof = load("proficiency")
    inds = load("indicators")
    csr = load("craft_stage_reform")
    fam = load("family_assignments")
    lens = load("ethical_lenses")
    exs = load("exposure_summary")
    srcs = load("exposure_sources")
    sect = load("sector_applications")
    signals = load("workforce_signals")
    xwalk = load("labor_market_crosswalk")
    M = OrderedDict()
    cm = {c["key"]: c for c in comp}
    dom = {c["key"]: c["domain_num"] for c in comp}
    title = {c["key"]: (c["suggested_title"] or c["title"]) for c in comp}
    T = defaultdict(list)
    for t in tasks:
        T[t["competency_key"]].append(t)
    csr_by = {r["key"]: r for r in csr}
    ex_by = {r["key"]: r for r in exs}

    # ------------------------------------------------------------------ A. completeness
    comp_rows = []
    for name, rows in (("competencies", comp), ("tasks", tasks), ("proficiency", prof), ("indicators", inds),
                       ("craft_stage_reform", csr), ("exposure_summary", exs), ("sector_applications", sect),
                       ("labor_market_crosswalk", xwalk)):
        for col in rows[0].keys():
            n = len(rows)
            nb = sum(1 for r in rows if r[col] not in ("",))
            comp_rows.append(dict(table=name, column=col, n=n, nonblank=nb, pct_nonblank=pct(nb, n)))
    write("completeness", comp_rows, ["table", "column", "n", "nonblank", "pct_nonblank"])
    # analytical-layer completeness per competency
    lens_comp = Counter(r["competency_key"] for r in lens)
    M["completeness"] = dict(
        competencies=len(comp), description_blank=sum(1 for c in comp if not c["description"]),
        proficiency_levels_without_knowledge=sum(1 for p in prof if not p["knowledge"]),
        proficiency_levels_without_application=sum(1 for p in prof if not p["application"]),
        craft_secondary_blank=sum(1 for r in csr if not r["craft_secondary"]),
        stage_secondary_1_blank=sum(1 for r in csr if not r["stage_secondary_1"]),
        stage_primary_2_filled=sum(1 for r in csr if r["stage_primary_2"]),
        stage_secondary_2_filled=sum(1 for r in csr if r["stage_secondary_2"]),
        lens_cells_filled=len(lens), lens_cells_total=len(comp) * 5,
        lens_competencies_filled=len(lens_comp), cld_severity_filled=sum(1 for e in exs if e["cld_severity"]),
        tasks_with_all_5_dims=sum(1 for t in tasks if all(t[d] for d in DIMS)),
    )

    # ------------------------------------------------------------------ B. consistency checks
    checks = []

    def check(cid, desc, n, viol, examples=(), note=""):
        checks.append(dict(check_id=cid, description=desc, n_checked=n, n_violations=len(viol),
                           examples=list(viol)[:8] if not examples else list(examples)[:8], note=note))
        return viol

    core = Counter(r["competency_key"] for r in fam if r["assignment"] == "Core")
    sup = Counter(r["competency_key"] for r in fam if r["assignment"] == "Supporting")
    check("C01", "Reform Flag Count equals the number of TRUE reform flags", len(csr),
          [r["code"] for r in csr if int(r["reform_flag_count"]) != sum(
              r[c] == "true" for c in r if c.startswith("reform_") and c != "reform_flag_count")])
    check("C02", "Core Family Count equals Core assignments", len(csr),
          [r["code"] for r in csr if int(r["core_family_count"]) != core[r["key"]]])
    check("C03", "Supporting Family Count equals Supporting assignments", len(csr),
          [f"{r['code']} (stored {r['supporting_family_count']}, actual {sup[r['key']]})" for r in csr
           if int(r["supporting_family_count"]) != sup[r["key"]]])
    check("C04", "Zero Core flag equals (Core count == 0)", len(csr),
          [r["code"] for r in csr if (r["zero_core"] == "true") != (core[r["key"]] == 0)])

    # stability tier rule (Data Dictionary, revised Feb 2026)
    tier_v = []
    for r in csr:
        k = r["key"]
        acs = any(t["auto_type"] in ("Ac", "S") for t in T[k])
        flags = int(r["reform_flag_count"]) > 0
        tier = r["stability_tier"]
        if tier == "Stable" and (flags or acs):
            tier_v.append(f"{r['code']} Stable but reform={int(r['reform_flag_count'])} AcS={acs}")
        if tier == "Transition" and not (flags or acs):
            tier_v.append(f"{r['code']} Transition without reform flag or Ac/S task")
    check("C05", "Stability Tier follows the documented rule (Stable = no reform flag and no Ac/S task; "
                 "Transition = 1+ reform flag or 1+ Ac/S task; Emergent exempt)", len(csr), tier_v)

    # modal recompute
    modal_rows = []
    modal_viol = defaultdict(list)
    contested_viol = []
    for k in sorted(T, key=lambda x: code_key(x.split(":")[1])):
        e = ex_by[k]
        any_contested = False
        for d in DIMS:
            vals = [t[d] for t in sorted(T[k], key=lambda x: x["task_n"])]
            c = Counter(vals).most_common()
            mode = c[0][0] if c[0][1] >= 2 else None
            stored = e[f"modal_{d}"]
            ok = (stored == mode) if mode else (stored in vals)
            if mode is None and d == "auto_type":
                any_contested = True
            if not ok:
                modal_viol[d].append(f"{e['code']} {vals}->{stored}")
            modal_rows.append(dict(key=k, code=e["code"], dimension=d, t1=vals[0], t2=vals[1], t3=vals[2],
                                   recomputed_mode=mode or "(no majority)", stored_modal=stored, consistent=ok,
                                   exposure_provenance=e["exposure_provenance"]))
        if (e["modal_contested"] == "true") != any_contested:
            contested_viol.append(f"{e['code']} stored={e['modal_contested']} auto_types="
                                  f"{[t['auto_type'] for t in T[k]]}")
    write("modal_consistency", modal_rows, ["key", "code", "dimension", "t1", "t2", "t3", "recomputed_mode",
                                            "stored_modal", "consistent", "exposure_provenance"])
    for d in DIMS:
        check(f"C06-{d}", f"Stored modal {d} equals the majority of T1-T3 (or one of them when no majority)",
              len(exs), modal_viol[d])
    check("C07", "Modal Contested is TRUE exactly when T1-T3 automation types have no majority", len(exs),
          contested_viol, note="v1 never defines 'Modal Contested'; this tests the most literal reading")
    import itertools
    au = [r for r in modal_rows if r["dimension"] == "auto_type"]
    best = (0, None)
    for order in itertools.permutations(["A", "Ac", "H", "V", "S"]):
        rank = {x: i for i, x in enumerate(order)}
        ok = sum(min((r["t1"], r["t2"], r["t3"]), key=lambda v: rank[v]) == r["stored_modal"] for r in au)
        best = max(best, (ok, order))
    modal_by_domain = {d: dict(consistent=sum(1 for r in au if r["code"][0] == d and r["consistent"]),
                               n=sum(1 for r in au if r["code"][0] == d)) for d in sorted({r["code"][0] for r in au})}
    minority_promoted = Counter(f"{'/'.join(sorted((r['t1'], r['t2'], r['t3'])))}->{r['stored_modal']}"
                                for r in au if not r["consistent"])
    inc_by_prov = Counter(r["exposure_provenance"] for r in modal_rows if r["consistent"] is False)
    M["modal"] = dict(cells=len(modal_rows), inconsistent=sum(1 for r in modal_rows if r["consistent"] is False),
                      inconsistent_by_provenance=dict(inc_by_prov),
                      competencies_with_any_inconsistency=len({r["key"] for r in modal_rows if not r["consistent"]}),
                      contested_mismatch=len(contested_viol),
                      auto_type_majority_consistent=sum(1 for r in au if r["consistent"]),
                      auto_type_best_priority_rule=dict(order=best[1], explains=best[0], of=len(au)),
                      auto_type_consistent_by_domain=modal_by_domain,
                      auto_type_minority_promoted=dict(minority_promoted))

    cld_v, cldm_v, sev_v, sev_v2 = [], [], [], []
    for e in exs:
        k = e["key"]
        rule = any(t["career_ladder"] == "P" and t["auto_type"] in ("Ac", "S", "V") for t in T[k])
        if (e["cld_flag"] == "true") != rule:
            cld_v.append(f"{e['code']} stored={e['cld_flag']} rule={rule} [{e['exposure_provenance']}]")
        if e["modal_cld_flag"] != e["cld_flag"]:
            cldm_v.append(e["code"])
        if e["cld_flag"] == "true" and not e["cld_severity"]:
            sev_v.append(e["code"])
        if e["cld_flag"] == "false" and e["cld_severity"]:
            sev_v2.append(f"{e['code']} severity={e['cld_severity']}")
    check("C08", "CLD Flag is TRUE exactly when some task is P-position and Ac/S/V (Data Dictionary rule)",
          len(exs), cld_v)
    check("C09", "CLD Flag (modal) equals CLD Flag", len(exs), cldm_v)
    check("C10a", "CLD Severity is filled when CLD Flag is TRUE", sum(e["cld_flag"] == "true" for e in exs), sev_v)
    check("C10b", "CLD Severity is blank when CLD Flag is FALSE", sum(e["cld_flag"] == "false" for e in exs), sev_v2)
    hv = [f"{t['key']} {t['auto_type']}/{t['vector']}/{t['horizon']}" for t in tasks
          if (t["auto_type"] == "H") != (t["vector"] == "none") or (t["auto_type"] == "H") != (t["horizon"] == "N")]
    check("C11", "Human-essential (H) tasks, and only they, have vector none and horizon N", len(tasks), hv)
    st = [e["code"] for e in exs if e["s_trajectory_flag"] == "true" and not any(t["auto_type"] == "Ac"
                                                                                  for t in T[e["key"]])]
    check("C12", "S-Trajectory flag TRUE only where the competency has an Ac task", len(exs), st)
    check("C13", "Dual Primary Exception: Data Dictionary documents 5 (1.5.5, 1.6.3, 2.1.1, 2.7.3, 4.3.2); "
                 "database has TRUE for", 5, [c for c in ("1.5.5", "1.6.3", "2.1.1", "2.7.3", "4.3.2")
                                              if csr_by[f"v1:{c}"]["dual_primary_exception"] != "true"],
          note="Stage Primary 2 is also blank for all 222 rows, so the second primary stage is lost")

    # ------------------------------------------------------------------ C. stale dashboards and documents
    sig = defaultdict(dict)
    for s in signals:
        sig[(s["block"], s["row_label"])][s["column"]] = s["value"]
    craft_now = Counter(r["craft_primary"] for r in csr)
    tier_now = Counter(r["stability_tier"] for r in csr)
    stage_now = Counter(r["stage_primary_1"] for r in csr)
    stale = []
    for c in ("SC", "DC", "FC"):
        stale.append(dict(metric=f"craft primary {c}", dashboard=sig[("PROFESSIONAL CRAFT DISTRIBUTION", c)].get("Count"),
                          baseline=craft_now[c]))
    for s_ in ("S1", "S2", "S3", "S4", "S5", "S6"):
        stale.append(dict(metric=f"stage primary {s_}",
                          dashboard=sig[("WORKFLOW STAGE PRIMARY DISTRIBUTION", s_)].get("Primary Tag Count"),
                          baseline=stage_now[s_]))
    for tr in ("Stable", "Transition", "Emergent"):
        stale.append(dict(metric=f"tier {tr}", dashboard=sig[("COMPETENCY STABILITY TIERS", tr)].get("Count"),
                          baseline=tier_now[tr]))
    famname = {r["family_code"]: r["family_name"] for r in xwalk}
    core_by_fam = Counter(r["family_code"] for r in fam if r["assignment"] == "Core")
    for fc, fn in famname.items():
        stale.append(dict(metric=f"core count {fc} {fn}",
                          dashboard=sig[("PROFESSION FAMILY CORE COVERAGE", fn)].get("Core Competency Count"),
                          baseline=core_by_fam[fc]))
    for s in stale:
        s["differs"] = str(s["dashboard"]) != str(s["baseline"])
    write("workforce_signals_vs_baseline", stale, ["metric", "dashboard", "baseline", "differs"])
    M["workforce_signals"] = dict(metrics=len(stale), differing=sum(s["differs"] for s in stale))

    # automation-type distribution vs CL-007 (change log) and Task 14 synthesis
    d16 = [t for t in tasks if dom[t["competency_key"]] != "7"]
    M["exposure_distribution"] = dict(
        all_666=dict(Counter(t["auto_type"] for t in tasks)),
        d1_d6_645=dict(Counter(t["auto_type"] for t in d16)),
        changelog_cl007_636=dict(A=368, H=136, Ac=92, V=31, S=9),
        by_domain={d: dict(Counter(t["auto_type"] for t in tasks if dom[t["competency_key"]] == d))
                   for d in sorted(set(dom.values()))},
    )
    flagged = sum(1 for r in csr if int(r["reform_flag_count"]) > 0)
    M["reform"] = dict(competencies_flagged=flagged, pct=pct(flagged, len(csr)),
                       flag_instances=sum(int(r["reform_flag_count"]) for r in csr),
                       by_code={c: sum(r[c] == "true" for r in csr) for c in csr[0] if c.startswith("reform_")
                                and c != "reform_flag_count"},
                       data_dictionary_claim="122 (57%) of 215; 174 instances")

    # ------------------------------------------------------------------ D. exposure provenance & record alignment
    prov = []
    by_src = defaultdict(list)
    for s in srcs:
        by_src[s["source"]].append(s)
    for src, rows in sorted(by_src.items()):
        sims = [float(r["task_text_similarity"]) for r in rows if r["task_text_similarity"]]
        prov.append(dict(
            source=src, source_file=rows[0]["source_file"], n_task_rows=len(rows),
            n_with_rationale=sum(1 for r in rows if r["rationale"]),
            matches_baseline=sum(r["matches_baseline"] == "true" for r in rows),
            auto_type_matches_baseline=None,
            text_exact=sum(1 for v in sims if v == 1.0), text_sim_lt_0_8=sum(1 for v in sims if v < 0.8),
            text_sim_median=round(statistics.median(sims), 3) if sims else None,
            source_inferred_marked=sum(r["source_inferred"] == "true" for r in rows),
            confidence=dict(Counter(r["confidence"] for r in rows if r["confidence"]))))
    tk = {t["key"]: t for t in tasks}
    for p in prov:
        rows = by_src[p["source"]]
        p["auto_type_matches_baseline"] = sum(1 for r in rows if tk.get(r["task_key"]) and
                                              r["auto_type"] == tk[r["task_key"]]["auto_type"])
    write("exposure_source_alignment", prov, ["source", "source_file", "n_task_rows", "n_with_rationale",
                                              "matches_baseline", "auto_type_matches_baseline", "text_exact",
                                              "text_sim_lt_0_8", "text_sim_median", "source_inferred_marked",
                                              "confidence"])
    rationale_tasks = {s["task_key"] for s in srcs if s["rationale"]}
    M["exposure_provenance"] = dict(
        tasks_by_provenance=dict(Counter(t["exposure_provenance"] for t in tasks)),
        tasks_with_any_rationale=len(rationale_tasks),
        tasks_with_rationale_by_domain={d: sum(1 for t in tasks if dom[t["competency_key"]] == d
                                               and t["key"] in rationale_tasks) for d in sorted(set(dom.values()))},
        sources=prov)

    # ------------------------------------------------------------------ E. genericity of proficiency statements
    gen_rows = []
    gcount = Counter()
    for p in prof:
        for field in ("knowledge", "application"):
            cls = classify_statement(p[field])
            gen_rows.append(dict(key=p["key"], code=p["code"], domain=dom[p["competency_key"]], level=p["level"],
                                 field=field, text=p[field], class_=cls,
                                 template=template_of(p[field], title[p["competency_key"]]) if p[field] else None))
            gcount[(p["level"], field, cls)] += 1
    for i in inds:
        if i["qa_flag"]:
            continue
        cls = classify_statement(i["text"])
        gen_rows.append(dict(key=i["key"], code=i["code"], domain=dom[i["competency_key"]], level=i["level"],
                             field="indicator", text=i["text"], class_=cls,
                             template=template_of(i["text"], title[i["competency_key"]])))
    # cross-competency templates (same template string in >= 5 different competencies)
    tmpl_comps = defaultdict(set)
    for r in gen_rows:
        if r["template"]:
            tmpl_comps[(r["field"], r["level"], r["template"])].add(r["code"])
    for r in gen_rows:
        n = len(tmpl_comps.get((r["field"], r["level"], r["template"]), ()))
        r["template_competency_count"] = n
        r["templated"] = n >= 5
    for r in gen_rows:
        r["class"] = r.pop("class_")
    write("proficiency_genericity", gen_rows, ["key", "code", "domain", "level", "field", "class", "templated",
                                               "template_competency_count", "template", "text"])
    LV = ["foundational", "intermediate", "advanced", "expert"]

    def tab(field):
        out = OrderedDict()
        for lv in LV:
            rows = [r for r in gen_rows if r["field"] == field and r["level"] == lv and r["class"] != "blank"]
            out[lv] = OrderedDict(n=len(rows), **{c: sum(r["class"] == c for r in rows) for c in
                                                  ("observable_action", "vague_action", "cognitive_state",
                                                   "status_influence")},
                                  non_observable_pct=pct(sum(r["class"] in NON_OBSERVABLE for r in rows), len(rows)),
                                  templated_pct=pct(sum(r["templated"] for r in rows), len(rows)))
        return out
    lead = OrderedDict()
    for f in ("knowledge", "application", "indicator"):
        for lv in LV:
            rows = [r for r in gen_rows if r["field"] == f and r["level"] == lv and r["text"]]
            c = Counter((r["text"].split() or [""])[0].lower().strip(",;:") for r in rows)
            top = c.most_common(3)
            lead[f"{f}:{lv}"] = dict(n=len(rows), top=[(w, n, pct(n, len(rows))) for w, n in top])
    by_dom = OrderedDict()
    for d in sorted(set(dom.values())):
        rows = [r for r in gen_rows if r["domain"] == d and r["field"] in ("knowledge", "application")
                and r["class"] != "blank"]
        irows = [r for r in gen_rows if r["domain"] == d and r["field"] == "indicator"]
        by_dom[d] = dict(ka_n=len(rows), ka_non_observable_pct=pct(sum(r["class"] in NON_OBSERVABLE for r in rows), len(rows)),
                         ka_templated_pct=pct(sum(r["templated"] for r in rows), len(rows)),
                         ind_n=len(irows),
                         ind_non_observable_pct=pct(sum(r["class"] in NON_OBSERVABLE for r in irows), len(irows)))
    top_templates = sorted(((f, lv, t, len(c)) for (f, lv, t), c in tmpl_comps.items() if len(c) >= 5),
                           key=lambda x: -x[3])[:25]
    ka = [r for r in gen_rows if r["field"] in ("knowledge", "application") and r["class"] != "blank"]
    M["genericity"] = dict(lead_words=lead, knowledge=tab("knowledge"), application=tab("application"), indicator=tab("indicator"),
                           by_domain=by_dom,
                           ka_total=len(ka), ka_non_observable=sum(r["class"] in NON_OBSERVABLE for r in ka),
                           ka_templated=sum(r["templated"] for r in ka),
                           expert_ka_status_influence=sum(1 for r in ka if r["level"] == "expert"
                                                          and r["class"] == "status_influence"),
                           expert_ka_n=sum(1 for r in ka if r["level"] == "expert"),
                           top_templates=[dict(field=f, level=lv, template=t, competencies=n)
                                          for f, lv, t, n in top_templates])

    # ------------------------------------------------------------------ F. indicators
    src_prof = load("proficiency", "source_text") if (BASE / "source_text" / "proficiency.csv").exists() else []
    ind_lv = OrderedDict()
    for lv in LV:
        pr = [p for p in prof if p["level"] == lv]
        sp = [p for p in src_prof if p["level"] == lv]
        ind_lv[lv] = dict(db_valid_total=sum(int(p["n_indicators_valid"]) for p in pr),
                          db_mean=round(statistics.mean(int(p["n_indicators_valid"]) for p in pr), 2),
                          db_levels_at_cap_6=sum(1 for p in pr if int(p["n_indicators"]) == 6),
                          source_total=sum(int(p["n_indicators_source"]) for p in sp) if sp else None,
                          source_mean=round(statistics.mean(int(p["n_indicators_source"]) for p in sp), 2) if sp else None,
                          source_max=max(int(p["n_indicators_source"]) for p in sp) if sp else None,
                          truncated_levels=sum(1 for p in sp if int(p["n_indicators_source"]) > int(p["n_indicators_db"]))
                          if sp else None)
    # exact duplicate indicator texts across competencies
    dup = defaultdict(set)
    for i in inds:
        if not i["qa_flag"]:
            dup[i["text"].strip().lower()].add(i["code"])
    dups = sorted(((t, sorted(c, key=code_key)) for t, c in dup.items() if len(c) > 1), key=lambda x: -len(x[1]))
    write("duplicate_indicators", [dict(text=t, n_competencies=len(c), codes=c) for t, c in dups],
          ["text", "n_competencies", "codes"])
    M["indicators"] = dict(by_level=ind_lv, exact_duplicate_texts=len(dups),
                           indicator_rows_in_duplicates=sum(len(c) for _, c in dups),
                           d5_misparsed=sum(1 for i in inds if i["qa_flag"]))

    # ------------------------------------------------------------------ G. task statements
    trows = []
    for t in tasks:
        s = task_structure(t["text"], TASK_VERBS)
        tools = sorted(set(m.group(0) for m in TOOL_TERMS.finditer(t["text"] or "")))
        trows.append(dict(key=t["key"], code=t["code"], domain=dom[t["competency_key"]], text=t["text"], **s,
                          tool_mentions=tools, compound_verb=bool(re.match(r"^\w+(,? (and|or) \w+|/\w+)\b",
                                                                           t["text"] or "")
                                                                  and (t["text"] or "").split()[0].lower()
                                                                  in TASK_VERBS)))
    write("task_quality", trows, ["key", "code", "domain", "first_word", "verb_first", "has_object", "has_purpose",
                                  "has_outcome", "compound_verb", "n_words", "tool_mentions", "text"])
    fw = Counter(r["first_word"] for r in trows)
    M["tasks"] = dict(n=len(trows), verb_first=sum(r["verb_first"] for r in trows),
                      not_verb_first=[r["key"] + " " + r["text"] for r in trows if not r["verb_first"]][:20],
                      has_purpose_or_condition=sum(r["has_purpose"] for r in trows),
                      has_outcome_clause=sum(r["has_outcome"] for r in trows),
                      vo_only=sum(1 for r in trows if r["verb_first"] and not r["has_purpose"]),
                      compound_verb=sum(r["compound_verb"] for r in trows),
                      words_median=statistics.median(r["n_words"] for r in trows),
                      words_min=min(r["n_words"] for r in trows), words_max=max(r["n_words"] for r in trows),
                      with_tool_mentions=sum(1 for r in trows if r["tool_mentions"]),
                      top_first_words=fw.most_common(15),
                      distinct_first_words=len(fw))
    ind_tools = sum(1 for i in inds if not i["qa_flag"] and TOOL_TERMS.search(i["text"]))
    M["tools"] = dict(tasks_with_tool_mentions=M["tasks"]["with_tool_mentions"], indicators_with_tool_mentions=ind_tools,
                      tool_counts=Counter(tool for r in trows for tool in r["tool_mentions"]).most_common(20))

    # ------------------------------------------------------------------ H. near-duplicates (TF-IDF cosine)
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    def neardups(items, threshold, ngram=(1, 2)):
        keys = [k for k, _ in items]
        texts = [x for _, x in items]
        v = TfidfVectorizer(stop_words="english", ngram_range=ngram, sublinear_tf=True, min_df=1)
        X = v.fit_transform(texts)
        S = cosine_similarity(X)
        pairs = []
        for i, j in combinations(range(len(keys)), 2):
            if S[i, j] >= threshold:
                pairs.append((keys[i], keys[j], round(float(S[i, j]), 3)))
        dist = sorted((float(S[i, j]) for i, j in combinations(range(len(keys)), 2)), reverse=True)
        return sorted(pairs, key=lambda x: -x[2]), dist

    citems = [(c["key"], f"{c['suggested_title'] or c['title']}. {c['suggested_description'] or c['description'] or ''}")
              for c in comp]
    cpairs, cdist = neardups(citems, 0.35)
    titems = [(t["key"], t["text"]) for t in tasks]
    tpairs, tdist = neardups(titems, 0.5)
    # richer per-competency document: title + description + tasks + valid proficiency text + indicators
    rich = defaultdict(list)
    for c in comp:
        rich[c["key"]].append(f"{c['suggested_title'] or c['title']}. {c['suggested_description'] or c['description'] or ''}")
    for t in tasks:
        rich[t["competency_key"]].append(t["text"])
    for i in inds:
        if not i["qa_flag"]:
            rich[i["competency_key"]].append(i["text"])
    ritems = [(k, " ".join(v)) for k, v in rich.items()]
    rpairs, rdist = neardups(ritems, 0.25)
    write("near_duplicate_competencies_rich", [dict(a=a, b=b, cosine=s_, same_skill_area=a.rsplit(".", 1)[0] ==
                                                    b.rsplit(".", 1)[0], title_a=title[a], title_b=title[b])
                                               for a, b, s_ in rpairs],
          ["a", "b", "cosine", "same_skill_area", "title_a", "title_b"])
    ctext = dict(citems)
    write("near_duplicate_competencies", [dict(a=a, b=b, cosine=s, same_skill_area=a.rsplit(".", 1)[0] == b.rsplit(".", 1)[0],
                                               text_a=ctext[a], text_b=ctext[b]) for a, b, s in cpairs],
          ["a", "b", "cosine", "same_skill_area", "text_a", "text_b"])
    ttext = dict(titems)
    write("near_duplicate_tasks", [dict(a=a, b=b, cosine=s, same_competency=a.rsplit(":", 1)[0] == b.rsplit(":", 1)[0],
                                        text_a=ttext[a], text_b=ttext[b]) for a, b, s in tpairs],
          ["a", "b", "cosine", "same_competency", "text_a", "text_b"])

    def q(dist, p):
        return round(dist[int(len(dist) * p)], 3)
    M["near_duplicates"] = dict(
        competency_pairs=len(cdist), competency_pairs_ge_0_35=len(cpairs),
        competency_pairs_ge_0_5=sum(1 for p in cpairs if p[2] >= 0.5),
        competency_top1pct=q(cdist, 0.01), competency_top01pct=q(cdist, 0.001), competency_max=round(cdist[0], 3),
        task_pairs=len(tdist), task_pairs_ge_0_5=len(tpairs), task_pairs_ge_0_7=sum(1 for p in tpairs if p[2] >= 0.7),
        task_top01pct=q(tdist, 0.001), task_max=round(tdist[0], 3),
        top_competency_pairs=cpairs[:15], top_task_pairs=tpairs[:15],
        rich_pairs_ge_0_25=len(rpairs), rich_pairs_ge_0_30=sum(1 for p in rpairs if p[2] >= 0.3),
        rich_top1pct=q(rdist, 0.01), rich_top01pct=q(rdist, 0.001), rich_max=round(rdist[0], 3),
        rich_cross_skill_area_ge_0_25=sum(1 for a, b, _ in rpairs if a.rsplit(".", 1)[0] != b.rsplit(".", 1)[0]),
        rich_cross_domain_ge_0_25=sum(1 for a, b, _ in rpairs if a.split(":")[1][0] != b.split(":")[1][0]),
        top_rich_pairs=[(a, title[a], b, title[b], s_) for a, b, s_ in rpairs[:25]])

    # ------------------------------------------------------------------ I. distributions
    M["distributions"] = dict(
        craft_primary=dict(Counter(r["craft_primary"] for r in csr)),
        craft_secondary=dict(Counter(r["craft_secondary"] or "(none)" for r in csr)),
        craft_primary_by_domain={d: dict(Counter(r["craft_primary"] for r in csr if dom[r["key"]] == d))
                                 for d in sorted(set(dom.values()))},
        stage_primary=dict(Counter(r["stage_primary_1"] for r in csr)),
        stage_secondary=dict(Counter(r["stage_secondary_1"] or "(none)" for r in csr)),
        stability_tier=dict(Counter(r["stability_tier"] for r in csr)),
        families_core=dict(Counter(r["family_code"] for r in fam if r["assignment"] == "Core")),
        families_supporting=dict(Counter(r["family_code"] for r in fam if r["assignment"] == "Supporting")),
        core_count_per_competency=dict(Counter(int(r["core_family_count"]) for r in csr)),
        zero_core=sum(r["zero_core"] == "true" for r in csr),
        foundational_prep=sum(r["foundational_professional_prep"] == "true" for r in csr),
        tacit=dict(Counter(t["tacit_density"] for t in tasks)),
        career=dict(Counter(t["career_ladder"] for t in tasks)),
        vector=dict(Counter(t["vector"] for t in tasks)),
        horizon=dict(Counter(t["horizon"] for t in tasks)),
        cld_flag=sum(e["cld_flag"] == "true" for e in exs),
        cld_severity=dict(Counter(e["cld_severity"] or "(blank)" for e in exs)),
        s_trajectory=sum(e["s_trajectory_flag"] == "true" for e in exs),
        tasks_by_position_and_type={f"T{n}": dict(Counter(t["auto_type"] for t in tasks if t["task_n"] == str(n)))
                                    for n in (1, 2, 3)},
        career_by_task_position={f"T{n}": dict(Counter(t["career_ladder"] for t in tasks if t["task_n"] == str(n)))
                                 for n in (1, 2, 3)},
    )

    # ------------------------------------------------------------------ J. source-text extras
    if (BASE / "source_text" / "skill_areas.csv").exists():
        stasks = load("tasks", "source_text")
        sinds = load("indicators", "source_text")
        M["source_text"] = dict(
            tasks_verbatim=sum(r["exact_match"] == "true" for r in stasks), tasks=len(stasks),
            indicators_source=len(sinds), indicators_in_db=sum(r["in_db_same_position"] == "true" for r in sinds),
            indicators_missing_from_db=sum(r["in_db_same_position"] != "true" for r in sinds),
            proficiency_levels=len(src_prof),
            ka_recoverable_d5=sum(1 for p in src_prof if p["code"].startswith("5.") and p["source_knowledge"]),
        )
    M["checks"] = checks
    write("consistency_checks", checks, ["check_id", "description", "n_checked", "n_violations", "examples", "note"])
    (QA / "metrics.json").write_text(json.dumps(M, indent=1, default=str) + "\n", encoding="utf-8")
    for c in checks:
        print(f"{c['check_id']:14s} {c['n_violations']:4d}/{c['n_checked']:<4d} {c['description'][:80]}")


if __name__ == "__main__":
    main()
