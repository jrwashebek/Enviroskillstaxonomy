#!/usr/bin/env python3
"""WP-16 Step 1 data edits (CA rulings in ADR-0031). Idempotent: a second run changes nothing.

Sections (ADR-0031 section in brackets):
  A  wrong forms in data/v2 (CR-FIX-A-003 #1, #3; brief Step 1.4; CR-FIX-C-001 #5)            [§4.3, §6]
  B  OpenLMP interval method: plan-level percentile bootstrap from Fix-A's seeded build (#2)  [§4.3]
  C  superseded provenance (#5)                                                               [§4.3]
  D  two DriverEvents (#4)                                                                     [§4.3]
  E  internal codes in record text, scenario wording, headcount bound (CR-FIX-C-001 #2, #3, #7; N13) [§4.7, §8]
  F  Good Neighbor Authority label (N12)                                                       [§8]
  G  instruments registered from verified records (S2 close-out A list)                       [§5.2]
  H  role competency targets from the S2 work orders' needed_by (R13, R26 and the rest)        [§5.3]
Run: python3 -I docs/build/WP-16/step1_data.py
Licence: Apache-2.0.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wp16lib as W  # noqa: E402

L = W.L
ROOT = W.ROOT
D = L.DATA_V2
SIG = D / "signals" / "2026"
FIG = ROOT / "docs" / "package" / "report" / "figures"      # read-only input (Fix-A's seeded bootstrap)


# ------------------------------------------------------------------------------------------------ A wrong forms
def section_a():
    def sl_c02(r):
        return W.replace_in_strings(r, "derives limits, conditions and monitoring requirements from the technical record",
                                    "derives limits, conditions and monitoring terms from the technical record")
    W.edit_yaml(W.find_yaml("seed:SL-C02"), sl_c02)

    def ind(r):
        return W.replace_in_strings(r, "Derives limits and monitoring requirements for a routine facility",
                                    "Derives limits and monitoring terms for a routine facility")
    W.edit_yaml(W.find_yaml("seed:sl-c02-l2-b"), ind)

    def task(r):
        r = W.replace_in_strings(r, "stating the validation, review and monitoring requirements the tier carries.",
                                 "stating the validation, review and monitoring the tier requires.")
        r["textSha256"] = L.text_sha256(r["statement"]["en"])
        return r
    W.edit_yaml(W.find_yaml("seed:dc-19-propose-tier"), task)

    omb_old = ("Counts of individually reported use cases in nine environmental bureaus (USGS, NOAA, USDA NRE incl. USFS, EPA, "
               "USDA FPAC incl. NRCS, FWS, BOR, BLM, NPS)")
    omb_new = ("Counts of individually reported use cases in eleven environmental units of the 2025 inventory (nine agencies "
               "and bureaus and two USDA mission areas: USGS, NOAA, USDA NRE incl. USFS, EPA, USDA FPAC incl. NRCS, FWS, BOR, "
               "BLM, BSEE, NPS, BIA)")
    W.edit_jsonl(SIG / "omb-ai-inventory-2025.jsonl", lambda r: W.replace_in_strings(r, omb_old, omb_new))


# ------------------------------------------------------------------------------------------------ B OpenLMP intervals
def _fig_rows(name):
    with open(FIG / name, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


BOOT = "plan-level percentile bootstrap over documents, 10,000 resamples, seed 20261023"


def section_b():
    f05 = {r["variant"]: r for r in _fig_rows("f05_plan_monitoring_share_by_rule.csv")}
    f06 = {r["signal_id"]: r for r in _fig_rows("f06_plan_content_rates_by_rule.csv") if r.get("signal_id")}
    head, plans = f05["all"], f05["plans_only"]

    def fix(r):
        m = r.get("measure") or {}
        rid = r["id"]
        if rid == "seed:sig/openlmp/monitoring-share-2012-vs-1982":
            row = head
            r["prefLabel"] = {"en": "Components typed as monitoring as a share of plan components: 2012-rule vs 1982-rule "
                                    "land management plans (western national forests)"}
            r["directionConfidence"] = "low"
            r["editorialNote"] = {"en": (
                "Headline (all documents, plan-equal): bootstrap intervals do not overlap. Not robust to document type: "
                f"{int(head['rule_2012_n_documents']) - int(plans['rule_2012_n_documents'])} of the "
                f"{head['rule_2012_n_documents']} 2012-rule documents are monitoring evaluation reports or stand-alone "
                f"monitoring plans; among plan documents only the shares are {float(plans['rule_2012_plan_equal']):.1%} "
                f"({plans['rule_2012_n_documents']} plans) vs {float(plans['rule_1982_plan_equal']):.1%} "
                f"({plans['rule_1982_n_documents']} plans) and the intervals overlap (claims register PLAN-01; "
                "docs/package/report/figures/f05_plan_monitoring_share_by_rule.csv). Components typed as monitoring "
                "measure what plans name, not funded workload.")}
            r["method"] = (
                "Cross-era comparison of plan components (not a time series of the same plans). Headline weights each document "
                f"equally (share computed within document, then averaged); ci95 = {BOOT} (Fix-A, report figure F05); "
                "component-weighted value kept as the ADR-0028 sensitivity check. Sensitivity by document type: among plan "
                f"documents only (excluding monitoring evaluation reports and stand-alone monitoring plans) the 2012-rule share is "
                f"{plans['rule_2012_plan_equal']} (ci95 {plans['rule_2012_ci95_low']}-{plans['rule_2012_ci95_high']}, n "
                f"{plans['rule_2012_n_documents']}) vs {plans['rule_1982_plan_equal']} (ci95 {plans['rule_1982_ci95_low']}-"
                f"{plans['rule_1982_ci95_high']}, n {plans['rule_1982_n_documents']}); the intervals overlap, so the direction "
                "is not robust to document type. Scope: western national forests (about 95% of components are USFS plans).")
        elif rid in f06:
            row = f06[rid]
            overlap = row.get("plan_equal_cis_overlap") == "yes"
            po = row.get("plans_only_cis_overlap") == "yes"
            r["editorialNote"] = {"en": (
                f"Plan-equal bootstrap intervals {'overlap' if overlap else 'do not overlap'} across all documents; among plan "
                f"documents only they {'overlap' if po else 'do not overlap'} (report figure F06).")}
            meth = r.get("method", "")
            meth = meth.replace("ci95 = mean +/- 1.96 SE across plans", f"ci95 = {BOOT} (Fix-A, report figure F06)")
            r["method"] = meth
            if overlap and r.get("directionConfidence") != "low":
                r["directionConfidence"] = "low"
        else:
            return None
        m["ci95"] = [float(row["rule_2012_ci95_low"]), float(row["rule_2012_ci95_high"])]
        b = m.get("baseline") or {}
        b["ci95"] = [float(row["rule_1982_ci95_low"]), float(row["rule_1982_ci95_high"])]
        m["baseline"] = b
        r["measure"] = m
        return r
    W.edit_jsonl(SIG / "openlmp.jsonl", fix)


# ------------------------------------------------------------------------------------------------ C provenance
def section_c():
    def bls(r):
        p = r.get("provenance") or {}
        if p.get("sources") == ["V4-07"]:
            p["sources"] = ["LM-132"]
            r["provenance"] = p
            return r
        return None
    W.edit_jsonl(SIG / "bls-ep-2025-35.jsonl", bls)

    def colorado(r):
        changed = False
        for holder in (r, r.get("provenance") or {}):
            if holder.get("sources") == ["CP-043", "IO-034"]:
                holder["sources"] = ["LM-117", "LM-155"]
                changed = True
        return r if changed else None
    W.edit_jsonl(D / "events" / "2026.jsonl", colorado)
    W.edit_jsonl(D / "instruments" / "instruments.jsonl", colorado)


# ------------------------------------------------------------------------------------------------ D events
def _event(instrument, etype, date, label, direction, status_after, sources, evidence, review_by):
    slug = instrument.split("/", 1)[1]
    return {"direction": direction, "eventDate": date, "eventType": etype, "evidenceLabel": evidence,
            "id": f"seed:evt/{slug}/{etype}/{date}", "instrument": instrument, "jurisdiction": "US" if "nj-" not in slug else "US-NJ",
            "layer": "L5", "license": "CC0-1.0", "module": "core", "prefLabel": {"en": label},
            "provenance": {"adr": "ADR-0031", "agent": [W.AGENT], "evidenceLabel": evidence, "generatedAt": "2026-10-23T23:30:00Z",
                           "method": "llm-assisted", "promptVersion": "WP16_BRIEF@2026-10-23",
                           "reviewStatus": "unreviewed", "sources": sources, "toolVersion": "docs/build/WP-16/step1_data.py"},
            "recordedBy": W.AGENT, "reviewBy": review_by, "sensitivity": "public", "sources": sources, "status": "draft",
            "statusAfter": status_after, "type": "DriverEvent"}


def section_d():
    W.append_jsonl(D / "events" / "2025.jsonl", _event(
        "seed:ins/americorps-grant-terminations", "decided", "2025-07-01",
        "AmeriCorps FY2025 grant terminations: grantees terminated on 2025-04-25, including programmes in states outside the "
        "litigation, told they were eligible for reinstatement (July 2025; day not recorded; uptake undocumented)",
        "expands", "enjoined", ["FIXA-01"], "J", "2026-12-15"))
    W.append_jsonl(D / "events" / "2026.jsonl", _event(
        "seed:ins/nj-ej-law", "decided", "2026-07-01",
        "New Jersey Environmental Justice Law and implementing rules: New Jersey Supreme Court granted certification; the "
        "rules remain in effect while the appeal is pending (July 2026; day not recorded)",
        "reshapes", "in-force-litigated", ["FIXA-03"], "J", "2026-12-15"))


# ------------------------------------------------------------------------------------------------ E codes, wording
def _fs_titles():
    out = {}
    with open(ROOT / "docs/research/strategic-foresight/sources.csv", encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            out[r["source_id"]] = f"{r['title']} ({r['author_or_publisher']}, {r['date_published']})"
    return out


def _role_titles():
    with open(ROOT / "docs/decisions/mvp_role_set.csv", encoding="utf-8", newline="") as fh:
        return {r["role_key"]: r["title"] for r in csv.DictReader(fh)}


SIGNPOST_CTX = {"AX-1": "public stewardship capacity", "AX-2": "AI reliability and legitimacy",
                "SC1/SC3": "Assured Augmentation and Platform Stewardship scenarios",
                "SC3/SC4": "Platform Stewardship and Patchwork Retreat scenarios"}
X11_OLD = " Seeded from PS translation row; requires PS and CM confirmation."
X11_NEW = " Seeded from a private-sector translation row; requires review by EMST's private-sector and career-mobility agents."


def section_e():
    fs, roles = _fs_titles(), _role_titles()
    rx_att = re.compile(r", attached to (R\d{2}-[a-z0-9-]+)$")
    rx_sp = re.compile(r"^Signpost SP-\d{2} \(([^)]+)\): ")

    def sig(r):
        changed = False
        lab = (r.get("prefLabel") or {}).get("en", "")
        m = rx_att.search(lab)
        if m and m.group(1) in roles:
            lab = lab[: m.start()] + f" (role: {roles[m.group(1)]})"
            changed = True
        m = rx_sp.match(lab)
        if m:
            ctx = SIGNPOST_CTX.get(m.group(1), m.group(1))
            lab = f"Scenario signpost ({ctx}): " + lab[m.end():]
            changed = True
        if changed:
            r["prefLabel"] = {"en": lab}
        if str(r.get("sourceRelease", "")).startswith("docs/research/strategic-foresight/weak_signals.csv") and r.get("source") in fs:
            r["sourceRelease"] = fs[r["source"]]
            changed = True
        if r.get("id", "").startswith("seed:sig/headcount/") and (r.get("measure") or {}).get("value") == -0.25:
            m2 = r["measure"]
            m2["name"] = "headcount_change_share_bound"
            m2["unit"] = "share, as a bound: the loss is more than a quarter (PPS gives no exact figure)"
            changed = True
        return r if changed else None
    for f in sorted(SIG.glob("*.jsonl")):
        W.edit_jsonl(f, sig)

    for tsv in sorted((D / "crosswalks" / "emst-public-private").glob("*.sssom.tsv")):
        t = tsv.read_text(encoding="utf-8")
        if X11_OLD in t:
            tsv.write_text(t.replace(X11_OLD, X11_NEW), encoding="utf-8")
            W.LOG.append(f"{tsv.relative_to(ROOT)}: X11 comments")
    gen = ROOT / "pipelines" / "crosswalks" / "x8_x11_private.py"
    t = gen.read_text(encoding="utf-8")
    if X11_OLD in t:
        gen.write_text(t.replace(X11_OLD, X11_NEW), encoding="utf-8")
        W.LOG.append(f"{gen.relative_to(ROOT)}: X11 comment text")

    sc = ROOT / "vocab" / "scenarios.yaml"
    t = sc.read_text(encoding="utf-8")
    new = (t.replace("agencies become intelligent customers;", "agencies become informed buyers;")
            .replace('move: "Build intelligent-customer capacity (procurement, data rights, model audit)."',
                     'move: "Build informed-buyer capacity (procurement, data rights, model audit)."')
            .replace('effect: "Moves AX-2 quickly"', 'effect: "Moves the AI reliability and legitimacy axis quickly"'))
    if new != t:
        sc.write_text(new, encoding="utf-8")
        W.LOG.append("vocab/scenarios.yaml: SC3 summary, NR-6, W2")


# ------------------------------------------------------------------------------------------------ F GNA label
def section_f():
    def gna(r):
        if r.get("id") == "seed:ins/good-neighbor-authority":
            r["prefLabel"] = {"en": "Good Neighbor Authority"}
            r["citation"] = "16 U.S.C. 2113a"
            return r
        if r.get("instrument") == "seed:ins/good-neighbor-authority" and "EXPLORE" in (r.get("prefLabel") or {}).get("en", "") + str(r.get("editorialNote")):
            lab = (r.get("prefLabel") or {}).get("en", "")
            new = lab.replace("Good Neighbor Authority incl. EXPLORE Act amendments", "Good Neighbor Authority")
            if new != lab:
                r["prefLabel"] = {"en": new}
                return r
        return None
    W.edit_jsonl(D / "instruments" / "instruments.jsonl", gna)
    for f in sorted((D / "events").glob("*.jsonl")):
        W.edit_jsonl(f, gna)


# ------------------------------------------------------------------------------------------------ G instruments
def _instrument(iid, label, citation, itype, juris, mechs, sources, evidence="E"):
    return {"citation": citation, "id": iid, "instrumentType": itype, "jurisdiction": juris, "layer": "L5", "license": "CC0-1.0",
            "mechanisms": mechs, "module": "core", "prefLabel": {"en": label},
            "provenance": {"adr": "ADR-0031", "agent": [W.AGENT], "evidenceLabel": evidence, "generatedAt": "2026-10-23T23:30:00Z",
                           "method": "llm-assisted", "promptVersion": "WP16_BRIEF@2026-10-23", "reviewStatus": "unreviewed",
                           "sources": sources, "toolVersion": "docs/build/WP-16/step1_data.py"},
            "sensitivity": "public", "status": "draft", "type": "Instrument"}


def _add_link(rid, iid, role):
    def fn(r):
        links = r.get("characteristicInstruments") or []
        if any(isinstance(x, dict) and x.get("instrument") == iid for x in links):
            return None
        r["characteristicInstruments"] = links + [{"instrument": iid, "role": role}]
        return r
    W.edit_yaml(W.find_yaml(rid), fn)


def section_g():
    inst = D / "instruments" / "instruments.jsonl"
    W.append_jsonl(inst, _instrument(
        "seed:ins/ada-title-ii", "ADA Title II and the DOJ rule on accessible web content and mobile apps of state and local governments",
        "42 U.S.C. 12131 et seq.; 28 CFR part 35 subpart H; compliance dates amended by 91 FR 20902 (2026-04-20)",
        "regulation", "US", ["DM-10", "DM-14"], ["V2-11", "CP-012"]))
    W.append_jsonl(D / "events" / "2026.jsonl", _event(
        "seed:ins/ada-title-ii", "interim", "2026-04-20",
        "ADA Title II web and mobile accessibility rule: interim final rule extends compliance dates to 2027-04-26 "
        "(population 50,000+) and 2028-04-26 (smaller entities and special districts); standard stays WCAG 2.1 AA",
        "reshapes", "in-force", ["V2-11", "CP-012"], "E", "2027-01-31"))
    W.append_jsonl(inst, _instrument(
        "seed:ins/chance-to-compete-act", "Chance to Compete Act of 2024 (technical assessments in federal competitive hiring)",
        "Chance to Compete Act of 2024, amending 5 U.S.C. 3304", "statute", "US", ["DM-16"], ["FH-001", "FH-017"]))
    _add_link("seed:ena-v1-5-3-4-a-local", "seed:ins/ada-title-ii", "requires")
    _add_link("seed:ena-fh-c13-federal", "seed:ins/chance-to-compete-act", "requires")


# ------------------------------------------------------------------------------------------------ H role targets
LEVELS = ["L1", "L2", "L3", "L4", "L5"]
SENIOR = {"senior", "lead", "strategic"}


def _needed_by():
    """{competency seed key: [(role_key_prefix, levels or None)]} from the core-residue work orders, plus the R26
    SL-C03 target that the S2 close-out B hand-off and the WP-16 brief name (SL-C07's inspection tasks now support
    SL-C03 through seed:ena-sl-c03-envhealth)."""
    out = {"seed:SL-C03": [("R26", None)]}
    with open(ROOT / "docs/decisions/integration/s2_work_orders.csv", encoding="utf-8", newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if r["kind"] == "core-residue"]
    for r in rows:
        nb = r["needed_by"]
        items = []
        if "senior levels of every P1 role" in nb:
            items += [(f"R{n:02d}", SENIOR) for n in range(1, 14)]
        for part in re.split(r";", nb):
            only = {"strategic"} if "strategic level" in part else None
            for a, b in re.findall(r"\bR(\d{2})(?:-R(\d{2}))?\b", part):
                for n in range(int(a), int(b or a) + 1):
                    items.append((f"R{n:02d}", only))
        if items:
            out[r["target"]] = items
    return out


def section_h():
    roles = {}
    for loc, rec in L.iter_records(D):
        if isinstance(rec, dict) and rec.get("type") == "RoleProfile" and loc.line is None:
            roles[rec["id"].split(":", 1)[1][:3]] = (loc.path, rec)
    comps = {}
    for loc, rec in L.iter_records(D):
        if isinstance(rec, dict) and rec.get("type") == "Competency":
            comps[rec["id"]] = rec
    added = []
    for comp, items in sorted(_needed_by().items()):
        c = comps.get(comp)
        if not c or c.get("validationStatus") == "seed-v1" or c.get("status") != "draft":
            continue
        lo, hi = LEVELS.index(c["levelSpan"]["min"]), LEVELS.index(c["levelSpan"]["max"])
        for rkey, only in items:
            if rkey not in roles:
                continue
            path, role = roles[rkey]
            if any(t.get("competency") == comp for t in role.get("competencyTargets") or []):
                continue
            tl = {}
            for rl in role.get("roleLevels") or []:
                if only and rl["key"] not in only:
                    continue
                band_lo, band_hi = (LEVELS.index(x) for x in rl["levelBand"])
                if band_hi < lo:
                    continue
                tl[rl["key"]] = LEVELS[min(max(band_lo, lo), hi)]
            if not tl:
                continue

            def fn(r, comp=comp, tl=tl):
                if any(t.get("competency") == comp for t in r.get("competencyTargets") or []):
                    return None
                r["competencyTargets"] = list(r.get("competencyTargets") or []) + [{"competency": comp, "targetLevels": tl}]
                ag = r["provenance"].setdefault("agent", [])
                if W.AGENT not in ag:
                    ag.append(W.AGENT)
                return r
            if W.edit_yaml(path, fn):
                added.append((role["id"], comp, tl))
                roles[rkey] = (path, L.load_yaml(path))
    out = ROOT / "docs/build/WP-16/generated/role_target_additions.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    prev = out.read_text(encoding="utf-8") if out.exists() else ""
    rows = [r for r in csv.DictReader(prev.splitlines())] if prev else []
    have = {(r["role"], r["competency"]) for r in rows}
    for rid, comp, tl in added:
        if (rid, comp) not in have:
            rows.append({"role": rid, "competency": comp, "targetLevels": ";".join(f"{k}={v}" for k, v in tl.items()),
                         "rule": "level = role level band minimum, clamped to the competency levelSpan; levels below the span skipped",
                         "basis": "docs/decisions/integration/s2_work_orders.csv needed_by; ADR-0031 §5.3"})
    out.write_text(L.csv_text(["role", "competency", "targetLevels", "rule", "basis"], rows), encoding="utf-8")


# ------------------------------------------------------------------------------------------------ I edge reviewBy
def section_i():
    """From candidate on, a J- or S-labelled instrument-sensitivity edge needs reviewBy (E-EDGE-REVIEWBY; ADR-0030).
    The 29 judgment edges without one get 2027-01-31, the date SC used for its reviewed task edges, so each is
    re-checked before 2.0.0 (ADR-0031 §6)."""
    for loc, rec in L.iter_records(D):
        if not isinstance(rec, dict) or loc.line is not None:
            continue
        if any(isinstance(e, dict) and e.get("evidenceLabel") in ("J", "S") and not e.get("reviewBy")
               for e in rec.get("instrumentSensitivity") or []):
            def fn(r):
                for e in r.get("instrumentSensitivity") or []:
                    if isinstance(e, dict) and e.get("evidenceLabel") in ("J", "S") and not e.get("reviewBy"):
                        e["reviewBy"] = "2027-01-31"
                return r
            W.edit_yaml(loc.path, fn)


if __name__ == "__main__":
    for s in (section_a, section_b, section_c, section_d, section_e, section_f, section_g, section_h, section_i):
        s()
    print("\n".join(W.LOG) or "no changes")
