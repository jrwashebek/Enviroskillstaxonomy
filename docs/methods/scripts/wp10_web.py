"""WP-10 signals from sources read on the web this session (2026-10-23): BLS Employment Projections 2025-35.

Values are transcribed from BLS Table 1.2 (LM-145; rows for SOC 11-, 13-, 15-, 17- and 19-10xx were readable) and
from OOH pages (LM-146..LM-150) for occupations whose Table 1.2 rows the fetch tool could not reach. Each value is a
published BLS figure; nothing is estimated. Not taken this session (fetch permission not granted): USAJOBS and
state-board baseline snapshots (LM-152, LM-153), OPM FWD series pulls, BLS AI exposure XLSX (LM-151).
"""
from wp10_common import base, provenance, AS_OF, WATCH_REVIEW_BY, TOOL_VERSION, PROMPT_VERSION

ALL_OCC_PCT = 3.5  # total employment +3.5% 2025-35 (LM-132)

# soc, title, emp2025 (k), emp2035 (k), change (k), pct, openings (k/yr or None), source
BLS = [
    ("11-9121", "Natural sciences managers", 112.2, 121.5, 9.2, 8.2, None, "LM-145"),
    ("13-1041", "Compliance officers", 436.4, 453.1, 16.7, 3.8, None, "LM-145"),
    ("13-1199", "Business operations specialists, all other", 1157.6, 1202.3, 44.7, 3.9, None, "LM-145"),
    ("13-2099", "Financial specialists, all other", 137.8, 143.4, 5.6, 4.1, None, "LM-145"),
    ("11-9161", "Emergency management directors", 14.0, 14.5, 0.5, 3.9, None, "LM-145"),
    ("11-3021", "Computer and information systems managers", 685.8, 793.9, 108.1, 15.8, None, "LM-145"),
    ("13-2011", "Accountants and auditors", 1595.2, 1674.6, 79.4, 5.0, None, "LM-145"),
    ("13-1151", "Training and development specialists", 472.5, 523.7, 51.1, 10.8, None, "LM-145"),
    ("11-3131", "Training and development managers", 50.2, 53.5, 3.2, 6.4, None, "LM-145"),
    ("15-2051", "Data scientists", 275.6, 371.0, 95.4, 34.6, 24.8, "LM-145"),
    ("15-1299", "Computer occupations, all other", 471.2, 495.3, 24.2, 5.1, 27.0, "LM-145"),
    ("17-1021", "Cartographers and photogrammetrists", 14.7, 15.7, 1.1, 7.4, 0.9, "LM-145"),
    ("17-1022", "Surveyors", 52.0, 55.0, 3.0, 5.8, 3.1, "LM-145"),
    ("17-2081", "Environmental engineers", 39.1, 41.6, 2.4, 6.3, 2.3, "LM-145"),
    ("17-3025", "Environmental engineering technologists and technicians", 12.5, 12.9, 0.4, 3.1, 1.1, "LM-145"),
    ("19-1013", "Soil and plant scientists", 19.9, 21.3, 1.3, 6.7, 1.4, "LM-145"),
    ("19-1023", "Zoologists and wildlife biologists", 19.5, 20.2, 0.7, 3.6, 1.4, "LM-145"),
    ("19-1029", "Biological scientists, all other", 59.6, 62.4, 2.8, 4.7, 4.3, "LM-145"),
    ("19-1031", "Conservation scientists", 27.7, 29.2, 1.5, 5.3, 2.1, "LM-145"),
    ("19-1032", "Foresters", 13.2, 13.5, 0.3, 2.2, 0.9, "LM-145"),
    ("19-2041", "Environmental scientists and specialists, including health", 93.4, 99.2, 5.7, 6.0, 7.3, "LM-146"),
    ("51-8031", "Water and wastewater treatment plant and system operators", 131.0, 123.5, -7.5, -6.0, 10.0, "LM-147"),
    ("19-4042", "Environmental science and protection technicians, including health", 36.4, 38.9, 2.5, 7.0, 5.3, "LM-148"),
    ("45-4011", "Forest and conservation workers", 14.7, 14.5, -0.2, -2.0, 2.2, "LM-149"),
    ("33-2011", "Firefighters", 355.3, 368.4, 13.1, 4.0, 26.8, "LM-150"),
]
PENDING = ["19-2043", "19-2042", "19-2021", "19-2099", "19-3051", "19-4071", "19-4044", "19-4021", "19-5011", "19-5012",
           "33-1021", "33-2022", "33-3031", "47-4041", "25-1053", "25-1043", "37-3011"]


def bls_signals():
    """One record per (SOC, MVP role listing the SOC): the occupation-level projection attached to its role
    crosswalk target (provisional path until X3)."""
    from wp10_external import role_map
    from wp10_common import extras
    rm = role_map()
    out, unattached = [], []
    for soc, title, e25, e35, chg, pct, opn, src in BLS:
        targets = rm.get(soc, [])
        if not targets:
            unattached.append(soc)
            continue
        direction = "grow" if pct > 1.0 else ("decline" if pct < -1.0 else "stable")
        rel = "faster than" if pct > ALL_OCC_PCT + 1.0 else ("slower than" if pct < ALL_OCC_PCT - 1.0 else "about as fast as")
        for role_key, mt in targets:
            r = base("seed:sig/bls-ep-2025-35/%s/%s" % (soc, role_key), "ChangeSignal",
                     "BLS projected employment change 2025-35 for %s (%s), attached to %s" % (title, soc, role_key),
                     editorial_note=("Projection, not observation; %s the all-occupation average (+3.5%%). Numeric change %s thousand%s. "
                                     "Projection drivers are not attributed per occupation in the sources read; BLS cites AI as a driver for some "
                                     "industries and for office and administrative support (V4-07). Supersedes LM Phase 2's 2022-32 figures."
                                     % (rel, chg, ("; about %s thousand openings a year" % opn) if opn is not None else "")),
                     notation=extras(family="projection", indep="bls-ep-2025-35", impact=2,
                                     baseline="value=3.5; unit=percent; all occupations 2025-35"))
            r.update({
                "targetType": "RoleProfile",
                "targetId": "mvp-role:" + role_key,
                "measure": {"name": "projected_employment_change_percent_2025_35", "value": pct, "unit": "percent", "ci95": None, "n": None,
                            "denominator": "employment 2025 = %s thousand (2035 projected %s thousand)" % (e25, e35)},
                "observedPeriod": {"start": "2025", "end": "2035", "note": "projection period"},
                "geography": "US",
                "source": src,
                "sourceRelease": "BLS Employment Projections 2025-35 (released 2026-08-27)",
                "corpus": {"version": "National Employment Matrix 2025-35", "sha256": None, "license": "public-domain-us-government"},
                "method": "Published BLS figure transcribed from %s (see docs/methods/sources.csv %s); no EMST computation." % (
                    "Table 1.2" if src == "LM-145" else "the OOH page", src),
                "toolVersion": TOOL_VERSION,
                "promptVersion": PROMPT_VERSION,
                "crosswalkPath": ["native SOC %s (BLS National Employment Matrix code)" % soc,
                                  "X3 role -> SOC (pending WP-09); provisional: docs/decisions/mvp_role_set.csv soc_2018 lists %s for %s" % (soc, role_key)],
                "crosswalkMinMatchType": "skos:closeMatch" if mt == "close" else "skos:broadMatch",
                "direction": direction,
                "directionConfidence": "med",
                "drivers": ["other"],
                "steepCategory": "economic",
                "novelty": 1,
                "reliability": "A",
                "corroboration": 1,
                "careFlag": False,
                "tribalPrograms": False,
                "personalData": False,
                "evidenceLabel": "S",
                "reviewStatus": "unreviewed",
                "reviewBy": WATCH_REVIEW_BY,
                "signalStatus": "watch",
                "provenance": provenance([src, "LM-132"], "E", method="import"),
            })
            out.append(r)
    return out


def build_groups():
    return {"data/v2/signals/2026/bls-ep-2025-35.jsonl": bls_signals()}
