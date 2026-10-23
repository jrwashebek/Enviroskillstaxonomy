"""WP-10 external-index ExposureAssessment records at an aggregated, defensible grain.

Grain: the index's native OCCUPATION unit (O*NET-SOC / SOC), never a single EMST-task match (XR-06). Role targets are
reached through the X3 role-variant -> SOC crosswalk (WP-09; until it exists, mvp_role_set.csv soc_2018 is the
provisional path, recorded in crosswalkPath). The join to roles is computed, not stored (SPEC 14; LM 6.3).

Ingested: Eloundou et al. (capability family; human and GPT-4 labels) and Microsoft 'Working with AI' applicability
(observed-use family; Bing Copilot usage). NOT ingested here, with reasons recorded in CHANGE_SIGNALS.md:
AEI usage/labor_market_impacts (occupation file not retrieved; Hugging Face not reachable), BLS AI exposure categories
(XLSX not retrievable; and a composite of the same families), AIOE/LM-AIOE/Webb/ILO (context only per ADR-0008 s4).
Task-level external joins wait for X2 (two-coder EMST task -> O*NET 31.0 task crosswalk).
"""
import csv
import os
import re

from wp10_common import ROOT, base, provenance, write_jsonl

SCORES = "docs/research/labor-market-ai-impact/env_occupation_exposure_scores.csv"
ROLES = "docs/decisions/mvp_role_set.csv"
LICENSE = "LicenseRef-EMST-third-party-index-derived"


def role_map():
    """SOC (6-digit) and O*NET-SOC detail -> [(role_key, provisional match type)] from mvp_role_set.csv."""
    m = {}
    for r in csv.DictReader(open(os.path.join(ROOT, ROLES), newline="", encoding="utf-8")):
        field = r["soc_2018"]
        no_exact = "no exact SOC" in field
        parts = [p.strip() for p in field.split("|") if p.strip()]
        codes = []
        for p in parts:
            c6 = re.match(r"(\d{2}-\d{4})", p)
            det = re.search(r"O\*NET (\d{2}-\d{4}\.\d{2})", p)
            if c6:
                codes.append((c6.group(1), det.group(1) if det else None))
        mt = "close" if (len(codes) == 1 and not no_exact) else "broad"
        for c6, det in codes:
            m.setdefault(c6, []).append((r["role_key"], mt if not det else "broad"))
            if det:
                m.setdefault(det, []).append((r["role_key"], "close" if not no_exact else "broad"))
    return m


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def build():
    rm = role_map()
    rows = list(csv.DictReader(open(os.path.join(ROOT, SCORES), newline="", encoding="utf-8")))
    elo, ms = [], []
    for r in rows:
        code = r["soc_code"].strip()
        is_detail = "." in code
        onet = code if is_detail else code + ".00"
        title = r["title"].replace(" (O*NET-SOC detail)", "")
        targets = rm.get(code, [])
        tpath = ("; ".join("%s [%s]" % (k, mt) for k, mt in targets) if targets else "no MVP role lists this code")
        # ---------------- Eloundou (capability)
        hb, hp = fnum(r["eloundou_human_rating_beta"]), fnum(r["eloundou_human_rating_beta_pct"])
        gb, gp = fnum(r["eloundou_dv_rating_beta"]), fnum(r["eloundou_dv_rating_beta_pct"])
        if hb is not None:
            rec = base("seed:asm/external/eloundou-2024/%s" % code, "ExposureAssessment",
                       "Eloundou et al. LLM exposure, occupation aggregate: %s (%s)" % (title, onet),
                       editorial_note=("Occupation aggregate from published occupation scores; never attached to a single EMST task "
                                       "(XR-06). Theoretical capability, not use or outcome. Ratings date from 2023."))
            rec["license"] = LICENSE
            dist = None
            if fnum(r["share_E0_human"]) is not None:
                dist = {"E0": fnum(r["share_E0_human"]), "E1": fnum(r["share_E1_human"]), "E2": fnum(r["share_E2_human"])}
            rec.update({
                "targetType": "occupation",
                "targetId": "onet-soc:" + onet,
                "instrument": "eloundou-gpts-are-gpts",
                "codebookVersion": "E0/E1/E2 exposure rubric (Science 2024 replication data)",
                "raterType": "external-index",
                "raterId": "external:eloundou-et-al-2024",
                "assessedAt": "2024",
                "method": ("Occupation beta = share of the occupation's O*NET 27.x tasks labelled E1 plus half the share labelled E2, "
                           "as published in occ_level.csv; percentile over all occupations computed by LM Phase 2 "
                           "(scripts/env_occupation_exposure.py)."),
                "confidence": "medium",
                "technicalExposure": ([{"vector": "llm-cognitive", "levelDistribution": dist, "basis": "human labels; share of O*NET tasks"}]
                                      if dist else [{"vector": "llm-cognitive", "levelDistribution": None, "basis": "task shares not published for detail code"}]),
                "externalSource": {
                    "index": "Eloundou, Manning, Mishkin, Rock - GPTs are GPTs",
                    "release": "Science 2024 replication data (GitHub snapshot read 2026-10-23); O*NET 27.x tasks",
                    "unit": "O*NET-SOC occupation",
                    "matchedOnetTasks": [],
                    "aggregation": "occupation-level beta and its percentile; no EMST task match involved",
                    "dispersion": {"nTasks": fnum(r["n_tasks"]), "shareE0": fnum(r["share_E0_human"]),
                                   "sharePhysicalTasks": fnum(r["share_physical_tasks"])},
                    "values": {"betaHuman": hb, "betaHumanPercentile": hp, "betaGpt4": gb, "betaGpt4Percentile": gp},
                },
                "crosswalkPath": "native %s; role targets via X3 (pending), provisional per mvp_role_set.csv soc_2018: %s" % (onet, tpath),
                "crosswalkMinMatchType": "exact",
                "evidenceLabel": "E",
                "sources": ["LM-008", "LM-048"],
                "provenance": provenance(["LM-008", "LM-048"], "E", method="import", note_adr="ADR-0008"),
            })
            elo.append(rec)
        # ---------------- Microsoft (observed use)
        ma = fnum(r["ms_ai_applicability"])
        if ma is not None and not is_detail:
            rec = base("seed:asm/external/ms-working-with-ai-v6/%s" % code, "ExposureAssessment",
                       "Microsoft 'Working with AI' applicability, occupation aggregate: %s (%s)" % (title, code),
                       editorial_note=("Observed-use measure from one platform (Bing Copilot conversations) mapped O*NET task -> DWA -> IWA -> SOC; "
                                       "applicability is not automation and not employment impact. Cite the v6 title."))
            rec["license"] = LICENSE
            rec.update({
                "targetType": "occupation",
                "targetId": "soc:" + code,
                "instrument": "ms-working-with-ai-applicability",
                "codebookVersion": "AI applicability score (results files v1.1)",
                "raterType": "external-index",
                "raterId": "external:tomlinson-et-al-2025",
                "assessedAt": "2025-12-22",
                "method": "Published SOC-level AI applicability score and non-physical-task variant; percentiles over 785 SOCs computed by LM Phase 2.",
                "confidence": "medium",
                "externalSource": {
                    "index": "Tomlinson, Jaffe, Wang, Counts, Suri - Working with AI: Measuring the Applicability of Generative AI to Occupations",
                    "release": "arXiv:2507.07935 v6 (2025-12-22); results files v1.1",
                    "unit": "SOC occupation (via IWA)",
                    "matchedOnetTasks": [],
                    "aggregation": "occupation-level applicability; no EMST task match involved",
                    "dispersion": {"sharePhysicalTasks": fnum(r["share_physical_tasks"]), "coverageUser": fnum(r["ms_coverage_user"])},
                    "values": {"aiApplicability": ma, "aiApplicabilityPercentile": fnum(r["ms_ai_applicability_pct"]),
                               "nonphysicalApplicability": fnum(r["ms_nonphysical_applicability"]),
                               "nonphysicalApplicabilityPercentile": fnum(r["ms_nonphysical_pct"])},
                },
                "crosswalkPath": "native SOC %s; role targets via X3 (pending), provisional per mvp_role_set.csv soc_2018: %s" % (code, tpath),
                "crosswalkMinMatchType": "exact",
                "evidenceLabel": "E",
                "sources": ["LM-009", "LM-136"],
                "provenance": provenance(["LM-009", "LM-136"], "E", method="import", note_adr="ADR-0008"),
            })
            ms.append(rec)
    write_jsonl("data/v2/assessments/external/eloundou-2024/occupation-aggregates.jsonl", elo)
    write_jsonl("data/v2/assessments/external/ms-working-with-ai-v6/occupation-aggregates.jsonl", ms)
    return {"ExposureAssessment_external": len(elo) + len(ms),
            "ExposureAssessment_external_eloundou": len(elo), "ExposureAssessment_external_ms": len(ms)}
