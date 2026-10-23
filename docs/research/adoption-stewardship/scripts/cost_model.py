"""EMST v2 stewardship 5-year cost model (2027-2031).

Produces ../cost_model.csv with Lean, Planning and Full scenarios per line item and year,
plus a Maintenance Floor scenario (the minimum that keeps the open core alive).
All figures are USD thousands, [J] estimates by AS (see sustainability_model.md for assumptions).
Run: python3 -I cost_model.py
"""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "cost_model.csv")
YEARS = ["2027", "2028", "2029", "2030", "2031"]

# Staffing: FTE (lean, full) per year
FTE = {
    "Managing editor / program director": [(1, 1)] * 5,
    "Data steward / engineer": [(1, 1)] * 5,
    "Community & partnerships manager": [(1, 1)] * 5,
    "Pilot & adoption coordinator": [(1, 1), (1, 1), (0.5, 0.5), (0, 0), (0, 0)],
    "Validation scientist (I-O)": [(0.5, 0.75), (0.5, 0.75), (0.5, 0.5), (0.5, 0.5), (0.5, 0.5)],
    "Skills-intelligence / NLP engineer": [(0.5, 1), (0.5, 1), (0.5, 0.75), (0.5, 0.75), (0.5, 0.75)],
    "Tribal liaison (reports to Tribal Council)": [(0.5, 0.5)] * 5,
    "Communications / UX (part-time)": [(0.25, 0.5)] * 5,
}
LOADED = {"lean": 130, "planning": 155, "full": 185}  # $k per FTE (salary + fringe)

# Non-personnel lines: (lean, full) per year; pass-through lines carry no indirect
NONP = {
    "Infrastructure (hosting, CI, API, backups)": [(8, 30)] * 5,
    "Security, privacy and Section 508 reviews": [(25, 60), (10, 25), (10, 25), (10, 25), (10, 25)],
    "Delphi / validation cycles": [(60, 140), (40, 100), (20, 50), (60, 140), (20, 50)],
    "Sentinel network annual update": [(0, 0), (20, 50), (20, 50), (20, 50), (20, 50)],
    "Data licenses (job postings, PD corpora)": [(0, 75)] * 5,
    "LLM / compute for skills extraction": [(5, 30)] * 5,
    "Convenings, advisory council, travel": [(30, 90)] * 5,
    "Tribal Council support (honoraria, travel, consultation)": [(40, 120)] * 5,
    "External evaluation": [(30, 80), (30, 80), (0, 0), (40, 100), (0, 0)],
    "Legal (license, trademark, MOUs, DUAs, host agreement)": [(15, 50), (5, 15), (5, 15), (5, 15), (5, 15)],
    "Communications and design": [(10, 40)] * 5,
}
PASS = {"NGO pilot stipends (pass-through)": [(96, 240), (40, 120), (0, 0), (0, 0), (0, 0)]}
INDIRECT = {"lean": 0.15, "planning": 0.20, "full": 0.30}

# Maintenance floor: 3.0 FTE; annual minor release; no new validation; Tribal Council kept
FLOOR_FTE = 3.0
FLOOR_NONP = 20 + 30 + 40 + 25 + 5 + 10  # infra, convenings, Tribal, sentinel, legal, compute


def pick(lo, hi, scen):
    return lo if scen == "lean" else hi if scen == "full" else (lo + hi) / 2


rows = []
totals = {s: [0.0] * 5 for s in ("lean", "planning", "full", "floor")}
for scen in ("lean", "planning", "full"):
    for y in range(5):
        fte = sum(pick(*v[y], scen) for v in FTE.values())
        pers = fte * LOADED[scen]
        rows.append([scen, YEARS[y], "Personnel", f"{fte:.2f} FTE", round(pers)])
        nonp = 0
        for k, v in NONP.items():
            c = pick(*v[y], scen)
            nonp += c
            rows.append([scen, YEARS[y], k, "", round(c)])
        ind = (pers + nonp) * INDIRECT[scen]
        rows.append([scen, YEARS[y], f"Indirect ({int(INDIRECT[scen]*100)}%, excl. pass-through)", "", round(ind)])
        pas = sum(pick(*v[y], scen) for v in PASS.values())
        rows.append([scen, YEARS[y], "NGO pilot stipends (pass-through)", "", round(pas)])
        tot = pers + nonp + ind + pas
        totals[scen][y] = tot
        rows.append([scen, YEARS[y], "TOTAL", f"{fte:.2f} FTE", round(tot)])
for y in range(5):
    tot = (FLOOR_FTE * LOADED["lean"] + FLOOR_NONP) * (1 + INDIRECT["planning"])
    totals["floor"][y] = tot
    rows.append(["floor", YEARS[y], "TOTAL", f"{FLOOR_FTE:.2f} FTE", round(tot)])

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["scenario", "year", "line_item", "fte", "usd_thousands"])
    w.writerows(rows)

for s, v in totals.items():
    print(s, [round(x) for x in v], "5-yr:", round(sum(v)))
