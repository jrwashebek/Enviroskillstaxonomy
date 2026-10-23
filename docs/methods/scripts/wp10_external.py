"""WP-10 external-index ExposureAssessment records at an aggregated, defensible grain.

Grain: the index's native OCCUPATION value (O*NET-SOC / SOC), attached to each MVP role that lists the code (the
provisional role -> SOC path until WP-09 delivers X3), never to a single EMST-task match (XR-06). Occupation grain is
allowed by CR-LM-002 (ADR-0029 s9); the release gate excludes LicenseRef-EMST-third-party-index-derived records.

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
STAGE = "data/v2/assessments/external/"  # CR-LM-002 accepted (ADR-0029 s9); was docs/methods/staging/ before the ruling


def role_entries():
    """[(role_key, soc6, onet_detail_or_None, single_uncaveated)] from mvp_role_set.csv soc_2018."""
    out = []
    for r in csv.DictReader(open(os.path.join(ROOT, ROLES), newline="", encoding="utf-8")):
        field = r["soc_2018"]
        no_exact = "no exact SOC" in field
        parts = []
        for p in [p.strip() for p in field.split("|") if p.strip()]:
            c6 = re.match(r"(\d{2}-\d{4})", p)
            det = re.search(r"O\*NET (\d{2}-\d{4}\.\d{2})", p)
            if c6:
                parts.append((c6.group(1), det.group(1) if det else None))
        single = len(parts) == 1 and not no_exact
        for c6, det in parts:
            out.append((r["role_key"], c6, det, single))
    return out


def role_map(available=None):
    """code -> [(role_key, match)] for attaching occupation values to MVP roles.
    Six-digit sources (available=None: BLS, Microsoft): every role whose listed code has that SOC prefix; close only
    for single, uncaveated, 6-digit listings, else broad (the SOC is broader than the role).
    Detail-capable sources (available = set of codes with values: Eloundou): a role listing an O*NET detail code
    attaches at the detail code when a value exists, otherwise at its parent SOC (broad)."""
    m = {}
    for role_key, c6, det, single in role_entries():
        if available is not None and det and det in available:
            m.setdefault(det, []).append((role_key, "close" if single else "broad"))
            continue
        m.setdefault(c6, []).append((role_key, "close" if (single and not det) else "broad"))
    return m


PRED = {"close": "skos:closeMatch", "broad": "skos:broadMatch"}


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _common(rec, code, onet, role_key, mt):
    rec["license"] = LICENSE
    rec["targetType"] = "RoleProfile"
    rec["targetId"] = "mvp-role:" + role_key
    rec["crosswalkPath"] = ["native %s (index unit)" % onet,
                            "X3 role -> SOC (pending WP-09); provisional: docs/decisions/mvp_role_set.csv soc_2018 lists %s for %s" % (code, role_key)]
    rec["crosswalkMinMatchType"] = PRED[mt]


def build():
    rows = list(csv.DictReader(open(os.path.join(ROOT, SCORES), newline="", encoding="utf-8")))
    rm_elo = role_map(available={r["soc_code"].strip() for r in rows if fnum(r["eloundou_human_rating_beta"]) is not None})
    rm_six = role_map()
    elo, ms, unattached = [], [], []
    for r in rows:
        code = r["soc_code"].strip()
        is_detail = "." in code
        onet = code if is_detail else code + ".00"
        title = r["title"].replace(" (O*NET-SOC detail)", "")
        targets_elo = rm_elo.get(code, [])
        targets_six = rm_six.get(code, []) if not is_detail else []
        if not targets_elo and not targets_six:
            unattached.append(code)
            continue
        hb, hp = fnum(r["eloundou_human_rating_beta"]), fnum(r["eloundou_human_rating_beta_pct"])
        gb, gp = fnum(r["eloundou_dv_rating_beta"]), fnum(r["eloundou_dv_rating_beta_pct"])
        dist = None
        if fnum(r["share_E0_human"]) is not None:
            dist = {"E0": fnum(r["share_E0_human"]), "E1": fnum(r["share_E1_human"]), "E2": fnum(r["share_E2_human"])}
        ma = fnum(r["ms_ai_applicability"])
        for role_key, mt in targets_elo:
            if hb is not None:
                rec = base("seed:asm/external/eloundou-2024/%s/%s" % (code, role_key), "ExposureAssessment",
                           "Eloundou et al. LLM exposure (occupation aggregate %s %s) attached to %s" % (onet, title, role_key),
                           editorial_note=("Occupation aggregate from published occupation scores, attached to a role through the role-SOC "
                                           "crosswalk; never attached to a single EMST task (XR-06). Theoretical capability, not use or outcome. "
                                           "Ratings date from 2023. STAGED pending CR-LM-002 (schema requires task-grain ExposureAssessment)."))
                _common(rec, code, onet, role_key, mt)
                rec.update({
                    "instrument": "eloundou-gpts-are-gpts",
                    "codebookVersion": "E0/E1/E2 exposure rubric (Science 2024 replication data)",
                    "raterType": "external-index",
                    "raterId": "index:eloundou-et-al-2024",
                    "assessedAt": "2024",
                    "method": ("Occupation beta = share of the occupation's O*NET 27.x tasks labelled E1 plus half the share labelled E2, "
                               "as published in occ_level.csv; percentile over all occupations computed by LM Phase 2 "
                               "(docs/research/labor-market-ai-impact/scripts/env_occupation_exposure.py)."),
                    "confidence": "med",
                    "externalSource": {
                        "index": "Eloundou, Manning, Mishkin, Rock - GPTs are GPTs",
                        "release": "Science 2024 replication data (GitHub snapshot read 2026-10-23); O*NET 27.x tasks",
                        "unit": "occupation",
                        "matchedOnetTasks": [],
                        "aggregation": "occupation-level beta and percentile for O*NET-SOC %s; no EMST task match involved" % onet,
                        "dispersion": {"nTasks": fnum(r["n_tasks"]), "shareE0": fnum(r["share_E0_human"]),
                                       "sharePhysicalTasks": fnum(r["share_physical_tasks"])},
                        "values": {"betaHuman": hb, "betaHumanPercentile": hp, "betaGpt4": gb, "betaGpt4Percentile": gp},
                    },
                    "evidenceLabel": "E",
                    "sources": ["LM-008"],
                    "provenance": provenance(["LM-008"], "E", method="import", adr="ADR-0008"),
                })
                if dist:
                    rec["technicalExposure"] = [{"vector": "llm-cognitive", "levelDistribution": dist,
                                                 "basis": "human labels; share of the occupation's O*NET tasks"}]
                elo.append(rec)
        for role_key, mt in targets_six:
            if ma is not None:
                rec = base("seed:asm/external/ms-working-with-ai-v6/%s/%s" % (code, role_key), "ExposureAssessment",
                           "Microsoft 'Working with AI' applicability (occupation aggregate %s %s) attached to %s" % (code, title, role_key),
                           editorial_note=("Observed-use measure from one platform (Bing Copilot conversations) mapped O*NET task -> DWA -> IWA -> SOC; "
                                           "applicability is not automation and not employment impact. Cite the v6 title. Occupation grain per CR-LM-002 (ADR-0029 s9)."))
                _common(rec, code, code, role_key, mt)
                rec.update({
                    "instrument": "ms-working-with-ai-applicability",
                    "codebookVersion": "AI applicability score (results files v1.1)",
                    "raterType": "external-index",
                    "raterId": "index:ms-working-with-ai-v6",
                    "assessedAt": "2025-12-22",
                    "method": "Published SOC-level AI applicability score and non-physical-task variant; percentiles over 785 SOCs computed by LM Phase 2.",
                    "confidence": "med",
                    "externalSource": {
                        "index": "Tomlinson, Jaffe, Wang, Counts, Suri - Working with AI: Measuring the Applicability of Generative AI to Occupations",
                        "release": "arXiv:2507.07935 v6 (2025-12-22); results files v1.1",
                        "unit": "occupation",
                        "matchedOnetTasks": [],
                        "aggregation": "occupation-level applicability for SOC %s (via O*NET task -> DWA -> IWA); no EMST task match involved" % code,
                        "dispersion": {"sharePhysicalTasks": fnum(r["share_physical_tasks"]), "coverageUser": fnum(r["ms_coverage_user"])},
                        "values": {"aiApplicability": ma, "aiApplicabilityPercentile": fnum(r["ms_ai_applicability_pct"]),
                                   "nonphysicalApplicability": fnum(r["ms_nonphysical_applicability"]),
                                   "nonphysicalApplicabilityPercentile": fnum(r["ms_nonphysical_pct"])},
                    },
                    "evidenceLabel": "E",
                    "sources": ["LM-009", "V4-02"],
                    "provenance": provenance(["LM-009", "V4-02"], "E", method="import", adr="ADR-0008"),
                })
                ms.append(rec)
    write_jsonl(STAGE + "eloundou-2024/occupation-aggregates-by-role.jsonl", elo)
    write_jsonl(STAGE + "ms-working-with-ai-v6/occupation-aggregates-by-role.jsonl", ms)
    with open(os.path.join(ROOT, "docs/methods/generated/unattached_occupations.txt"), "w", encoding="utf-8") as f:
        f.write("# In-scope occupations with index values but no MVP role listing the code (generated)\n")
        for c in sorted(set(unattached)):
            f.write(c + "\n")
    return {"ExposureAssessment_external": len(elo) + len(ms),
            "ExposureAssessment_external_eloundou": len(elo), "ExposureAssessment_external_ms": len(ms),
            "occupations_unattached_no_mvp_role": len(set(unattached))}
