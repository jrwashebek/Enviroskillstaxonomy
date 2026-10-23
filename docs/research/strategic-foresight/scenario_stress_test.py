"""Heuristic scenario stress test of v1 EMST competencies (Strategic Foresight, FS).

Purpose: demonstrate the stress-test method proposed in report.md section 6 by
assigning each v1 competency a demand direction and a workforce-reproduction risk
under each of the four FS scenarios, using transparent rules over existing v1 tags.

Evidence label: [J] heuristic. Outputs are a starting hypothesis for Delphi / SME
validation, NOT validated classifications. Rules restate v1 single-analyst tags
(craft, modal automation type, CLD flag, profession-family Core assignments), so
any error in v1 tags propagates.

Scenarios (see scenarios.md):
  SC1 Assured Augmentation  = capacity rebuilt/coordinated  x AI trusted & assured
  SC2 Human Premium         = capacity rebuilt/coordinated  x AI brittle & contested
  SC3 Platform Stewardship  = capacity thin/fragmented      x AI trusted & assured
  SC4 Patchwork Retreat     = capacity thin/fragmented      x AI brittle & contested

Demand codes: up | flat | down | reshape (headcount compresses, tasks shift to review)
              | external (work moves to vendors/platforms/partners outside public agencies)
Reproduction risk codes: L | M | H  (risk that the ladder producing the competency breaks)

Inputs : /home/claude/emst/data/v1_baseline/{competencies,craft_stage_reform,exposure_summary,family_assignments}.csv
Output : scenario_stress_test_v1.csv (same folder as this script)
Run    : python3 -I scenario_stress_test.py
"""
import csv, os, collections

BASE = "/home/claude/emst/data/v1_baseline"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "scenario_stress_test_v1.csv")

def load(name):
    with open(os.path.join(BASE, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

comps = {r["code"]: r for r in load("competencies.csv")}
craft = {r["code"]: r for r in load("craft_stage_reform.csv")}
expo = {r["code"]: r for r in load("exposure_summary.csv")}
fam = collections.defaultdict(set)
for r in load("family_assignments.csv"):
    if r["assignment"] == "Core":
        fam[r["code"]].add(r["family_code"])

PUBLIC_FAM = {"F1", "F2", "F8", "F12"}   # v1 Structural Conditions: public-agency-concentrated families
PRIVATE_FAM = {"F7", "F14", "F15"}       # v1: strong private-sector demand
AI_GOV = {"7.1.4", "7.2.1", "7.2.3", "2.6.5"}            # AI governance / validation
PROCURE = {"3.3.4", "3.1.4", "3.5.1"}                    # procurement, agreements, digital transformation leadership
BROKER_PREFIX = ("6.5.", "5.2.")                          # intergovernmental coordination & collaboration
FIRE_SAFETY_PREFIX = ("4.3.", "4.4.")                     # fire and field safety/emergency

def norm_bool(v):
    return str(v).strip().lower() in ("true", "yes", "1")

rows = []
for code, c in sorted(comps.items(), key=lambda kv: [int(x) for x in kv[0].split(".")]):
    cr = craft.get(code, {}).get("craft_primary", "")
    ex = expo.get(code, {})
    auto = ex.get("modal_auto_type", "")
    cld = norm_bool(ex.get("cld_flag", ""))
    fams = fam.get(code, set())
    public = bool(fams & PUBLIC_FAM)
    private = bool(fams & PRIVATE_FAM)
    rules = []
    d = {}
    rr = {}

    # ---- SC1 Assured Augmentation ----
    if code in AI_GOV:
        d["SC1"] = "up"; rules.append("R1a")
    elif auto in ("Ac", "V", "S"):
        d["SC1"] = "reshape"; rules.append("R1b")
    elif auto == "A":
        d["SC1"] = "up"; rules.append("R1c")
    elif auto == "H" and cr == "FC":
        d["SC1"] = "up"; rules.append("R1d")   # field verification becomes bottleneck
    else:
        d["SC1"] = "flat"; rules.append("R1e")
    rr["SC1"] = "M" if cld else "L"

    # ---- SC2 Human Premium ----
    if code in AI_GOV:
        d["SC2"] = "up"; rules.append("R2a")     # brittle AI raises validation demand
    elif auto == "H":
        d["SC2"] = "up"; rules.append("R2b")
    else:
        d["SC2"] = "flat"; rules.append("R2c")   # AI constrained; humans keep tasks
    rr["SC2"] = "L"

    # ---- SC3 Platform Stewardship ----
    if code in AI_GOV or code in PROCURE:
        d["SC3"] = "up"; rules.append("R3a")
    elif auto in ("Ac", "V", "S"):
        d["SC3"] = "external"; rules.append("R3b")
    elif private and not public:
        d["SC3"] = "up"; rules.append("R3c")
    elif public:
        d["SC3"] = "down"; rules.append("R3d")
    elif cr == "DC":
        d["SC3"] = "external"; rules.append("R3e")
    else:
        d["SC3"] = "flat"; rules.append("R3f")
    if cld or cr == "FC":
        rr["SC3"] = "H"; rules.append("R3r1")
    else:
        rr["SC3"] = "M"

    # ---- SC4 Patchwork Retreat ----
    if code.startswith(FIRE_SAFETY_PREFIX):
        d["SC4"] = "up"; rules.append("R4a")     # climate demand persists, capacity does not
    elif code.startswith(BROKER_PREFIX) or code in AI_GOV:
        d["SC4"] = "up"; rules.append("R4b")     # brokering across a patchwork; triaging bad AI
    elif public:
        d["SC4"] = "down"; rules.append("R4c")
    elif private and not public:
        d["SC4"] = "flat"; rules.append("R4d")
    else:
        d["SC4"] = "down"; rules.append("R4e")
    if cr == "FC" or cld:
        rr["SC4"] = "H"; rules.append("R4r1")
    else:
        rr["SC4"] = "M"

    nondecl = sum(1 for s in d.values() if s in ("up", "flat", "reshape"))
    highrisk = sum(1 for s in rr.values() if s == "H")
    if nondecl >= 3 and highrisk <= 1:
        klass = "robust"
    elif nondecl <= 2 and highrisk >= 2:
        klass = "fragile"
    else:
        klass = "contingent"
    # protected-capability flag: in demand somewhere but supply fragile in >=2 scenarios
    protect = "true" if (highrisk >= 2 and any(s == "up" for s in d.values())) else "false"

    rows.append({
        "v1_code": code, "title": c["title"], "craft_primary": cr, "modal_auto_type": auto,
        "cld_flag": str(cld).lower(), "core_families": "|".join(sorted(fams)),
        "SC1_demand": d["SC1"], "SC1_repro_risk": rr["SC1"],
        "SC2_demand": d["SC2"], "SC2_repro_risk": rr["SC2"],
        "SC3_demand": d["SC3"], "SC3_repro_risk": rr["SC3"],
        "SC4_demand": d["SC4"], "SC4_repro_risk": rr["SC4"],
        "robustness_class": klass, "protect_flag": protect,
        "rules_fired": "|".join(rules), "evidence_label": "J",
    })

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

cnt = collections.Counter(r["robustness_class"] for r in rows)
by_craft = collections.Counter((r["craft_primary"], r["robustness_class"]) for r in rows)
print("competencies:", len(rows))
print("robustness:", dict(cnt))
print("protect_flag true:", sum(r["protect_flag"] == "true" for r in rows))
for k in sorted(by_craft):
    print(k, by_craft[k])
for s in ("SC1", "SC2", "SC3", "SC4"):
    print(s, dict(collections.Counter(r[s + "_demand"] for r in rows)), dict(collections.Counter(r[s + "_repro_risk"] for r in rows)))
