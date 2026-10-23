#!/usr/bin/env python3
"""S2 close-out A (A5 SC; LM supplies registry IDs): typed instrument-link roles on the SC-lane actor enactments.

Work orders (docs/decisions/integration/s2_work_orders.csv):
  * "38 SC actor enactments" — CR-SC-001 #2 and #5: set link roles; add base `requires` links (SL-C02 federal);
    move 'Delegated constraints:' text from authorityBasis into Enactment.delegatedConstraints.
  * "seed:ena-db-c52-federal; seed:ena-db-c52-state" — CR-SC-001 #2: link the EJ instruments LM registered, with roles
    per docs/methods/generated/wp05_instrument_resolution.csv (A9 LM with A5 SC; SC part done here, IDs from LM).

Roles (vocab/driver_mechanisms.yaml#instrument_link_roles) are set per link, never per instrument. Only `requires`
decides venue applicability (vocab/rules/venue-applicability@1.0.0.yaml). Additions are the base instruments WP-05
asked LM to register (docs/build/WP-05/instruments_to_register.csv) and LM registered (registry IDs only; most have no
dated events yet, so they give basisLinked = true, basisVerified = false until SC's quarterly refresh).

Edits only the enactments named in ROLES (all SC-authored, WP-05). DB's 11 module enactments are DB's work order.
Usage: python3 docs/build/S2-closeout-A/moves_instrument_roles.py [--dry-run]
Licence: Apache-2.0 (code). Records stay CC0-1.0.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402

AGENT = "emstagent:a5-sc@s2-closeout-a"
ENA = L.DATA_V2 / "core" / "enactments"
R, EN, C, X = "requires", "enables", "constrains", "removed-requirement"
EX_STATE = "Example state only; other states' statutes are not yet registered."
NO_EVENT = "Registered without dated events; basis linked, status not yet verified."

# enactment -> list of (instrument key, role, note or None). Existing links must all appear; extra rows are added.
ROLES: dict[str, list[tuple[str, str, str | None]]] = {
    "ena-db-c50-federal": [("nhpa-s106-regs", R, None)],
    "ena-db-c52-federal": [
        ("eo-12898", R, "Revoked 2025-01-21 by EO 14173; linked so the federal value computes from its status."),
        ("eo-14096", R, "Revoked 2025-01-20 by EO 14148."),
        ("eo-14008", R, "Justice40 provisions; revoked 2025-01-20 by EO 14148."),
        ("eo-14173", X, "Revoking order for EO 12898; never a basis."),
        ("eo-14148", X, "Revoking order for EO 14096 and EO 14008; never a basis.")],
    "ena-db-c52-state": [("nj-ej-law", R, None), ("ny-ecl-70-0118", R, None)],
    "ena-fh-c01-action-agency": [
        ("esa-s7-regs-current", R, NO_EVENT),
        ("esa-harm-rescission", C, "Narrows the regulatory definition of harm used in effects analysis."),
        ("esa-4d-4b2-rules", C, None),
        ("esa-s4-s7-regs-2025", C, "Proposed amendments to the consultation regulations.")],
    "ena-fh-c01-consulting-agency": [
        ("esa-s7-regs-current", R, NO_EVENT),
        ("esa-harm-rescission", C, None),
        ("esa-s4-s7-regs-2025", C, "Proposed amendments to the consultation regulations.")],
    "ena-fh-c01-state": [("state-esa-ca", R, EX_STATE)],
    "ena-sc-c01-agency": [("florida-404-assumption", EN, "One state's assumed programme (vacated 2026-03-27); an "
                                                         "example of a state authority in the pathway, not a basis.")],
    "ena-sc-c01-regulated-party": [("nepa-s112-fee", EN, "Sponsor opt-in."), ("fast-41", EN, "Covered-project status is an option for sponsors.")],
    "ena-sc-c02-federal": [
        ("apa-judicial-review", R, "Whole-record review. " + NO_EVENT),
        ("seven-county", C, "Deference standard that shapes how a reviewing court reads the record."),
        ("ceq-permitting-data-standard", C, "Sets record and data formats for permitting systems."),
        ("permitting-tech-action-plan", EN, None),
        ("omb-m-25-21", C, "Conditions on agency AI use that the record must document."),
        ("speed-act", C, "Pending legislation on limitations periods and standing.")],
    "ena-sc-c02-state": [("ceqa-2025-reforms", C, EX_STATE)],
    "ena-sc-c03-federal": [
        ("nepa-fra-2023", R, None), ("doi-nepa-procedures", R, None), ("usda-nepa-procedures", R, None),
        ("dot-nepa-procedures", R, None), ("epa-nepa-procedures", R, "Proposed; decides nothing until in force."),
        ("nepa-s112-fee", EN, "Sponsor-paid acceleration.")],
    "ena-sc-c03-state": [
        ("ceqa-2025-reforms", C, "New statutory exemptions narrow what must be reviewed (example state)."),
        ("state-sepa-ca", R, EX_STATE), ("state-sepa-wa", R, EX_STATE), ("state-sepa-mn", R, EX_STATE),
        ("state-sepa-ny", R, EX_STATE)],
    "ena-sc-c04-federal": [("nepa-fra-2023", R, "Section 107(f) sponsor preparation under agency supervision."),
                           ("doi-nepa-procedures", R, None), ("nepa-s112-fee", EN, None)],
    "ena-sc-c04-state": [("state-sepa-ca", R, EX_STATE), ("state-sepa-wa", R, EX_STATE),
                         ("state-sepa-mn", R, EX_STATE), ("state-sepa-ny", R, EX_STATE)],
    "ena-sc-c06-federal": [
        ("doi-nepa-procedures", R, "Comment solicitation for impact statements."),
        ("usda-nepa-procedures", R, None),
        ("ceq-nepa-regs-removal", X, "Removed the government-wide public-involvement provisions; never a basis."),
        ("usfs-objection-rule", R, None)],
    "ena-sc-c08-county": [("good-neighbor-authority", EN, None)],
    "ena-sc-c08-federal": [("good-neighbor-authority", EN, None), ("long-term-gna-act", EN, "Pending legislation."),
                           ("fix-our-forests-act", EN, "Pending legislation."),
                           ("stewardship-contracting", EN, NO_EVENT)],
    "ena-sc-c08-state": [("co-hb26-1205", EN, EX_STATE), ("good-neighbor-authority", EN, None)],
    "ena-sc-c09-federal": [
        ("nepa-fra-2023", R, "Section 107 lead, cooperating and participating agency rules."),
        ("fast-41", R, "Coordination plans for covered projects."),
        ("ceq-permitting-data-standard", C, None), ("doi-nepa-procedures", R, None),
        ("speed-act", C, "Pending legislation.")],
    "ena-sc-c09-state-local": [("speed-act", C, "Pending legislation.")],
    "ena-sc-c10-agreement-revenue": [("good-neighbor-authority", EN, "Revenue retention by partners.")],
    "ena-sc-c10-federal": [
        ("appropriations-law", R, "Purpose, time and amount. " + NO_EVENT),
        ("fy2026-interior-approps", EN, "Funds the programme year and carries conditions."),
        ("obbba-ira-rescissions", C, "Rescinded unobligated balances; limits what can be obligated."),
        ("nepa-s112-fee", EN, "Fee revenue.")],
    "ena-sc-c11-federal": [
        ("ceq-nepa-regs-removal", C, "Object of the durability analysis, not a basis."),
        ("doi-nepa-procedures", C, None), ("esa-harm-rescission", C, None),
        ("ghg-endangerment-rescission", C, "Object of the durability analysis, not a basis."),
        ("wotus-definition", C, None),
        ("cra-and-deregulation-orders", C, "Disapproval and review mechanisms that bear on durability. " + NO_EVENT)],
    "ena-sc-c11-private": [("ca-sb-253", C, None), ("ca-sb-261", C, None), ("sec-climate-disclosure", C, None),
                           ("eu-omnibus-i", C, None)],
    "ena-sc-c11-state": [("florida-404-assumption", C, None), ("wotus-definition", C, None)],
    "ena-sc-c12-federal": [
        ("ceq-nepa-regs-removal", C, "A tracked change; not a basis."),
        ("ceq-nepa-guidance-2025", R, "Directed agencies to revise their procedures, the translation this enactment performs."),
        ("doi-nepa-procedures", C, None), ("usda-nepa-procedures", C, None),
        ("esa-harm-rescission", C, None), ("ghg-endangerment-rescission", C, "A tracked change; not a basis.")],
    "ena-sc-c12-private": [("ca-sb-253", C, None), ("ca-sb-261", C, None), ("eu-omnibus-i", C, None)],
    "ena-sc-c14-federal-overseer": [("state-program-approval-regs", R, NO_EVENT),
                                    ("categorical-program-grants", EN, "Grant conditions carry work-plan and reporting terms. " + NO_EVENT)],
    "ena-sc-c14-state-delegated": [
        ("florida-404-assumption", EN, "One state's assumption (vacated 2026-03-27); an example, not the basis."),
        ("wotus-definition", C, None),
        ("state-program-approval-regs", R, NO_EVENT),
        ("categorical-program-grants", EN, NO_EVENT)],
    "ena-sc-c15-private": [
        ("ca-sb-253", R, None), ("ca-sb-261", R, "Enjoined 2025-11-18."), ("eu-omnibus-i", C, "Narrowed the EU reporting scope."),
        ("sec-climate-disclosure", R, "Stayed."),
        ("ghgrp-reconsideration", X, "Proposed removal of federal reporting obligations; never a basis.")],
    "ena-sc-c17-advocate": [("speed-act", C, "Pending legislation on standing and limitations.")],
    "ena-sc-c17-federal": [("apa-judicial-review", R, NO_EVENT), ("seven-county", C, None), ("speed-act", C, "Pending legislation."),
                           ("usfs-objection-rule", C, "Pre-decisional objection sets exhaustion and timing.")],
    "ena-sc-c17-state": [("ceqa-2025-reforms", C, EX_STATE)],
    "ena-sc-c18-federal": [("schedule-policy-career", C, "Changes the status of policy-influencing positions.")],
    "ena-sl-c02-federal-regulator": [
        ("wotus-definition", C, "Jurisdictional definition; limits scope, never a basis."),
        ("ghg-endangerment-rescission", X, "Rescission; never a basis (ADR-0030 §1, SL-C02 defect)."),
        ("cwa-402-npdes", R, NO_EVENT), ("caa-title-v", R, NO_EVENT), ("caa-nsr-psd", R, NO_EVENT),
        ("rcra-permits", R, "Where the federal regulator issues the permit. " + NO_EVENT),
        ("cwa-404", R, "Outside assumed states. " + NO_EVENT)],
    "ena-sl-c02-federal-resource-manager": [("usfs-objection-rule", C, None),
                                            ("federal-land-use-authorizations", R, NO_EVENT)],
    "ena-sl-c02-state-regulator": [
        ("florida-404-assumption", EN, "One state's assumption (vacated 2026-03-27); an example, not the basis."),
        ("wotus-definition", C, None),
        ("cwa-402-npdes", R, "State programme authorization. " + NO_EVENT), ("caa-title-v", R, NO_EVENT),
        ("caa-nsr-psd", R, NO_EVENT), ("rcra-permits", R, "State authorization. " + NO_EVENT)],
    "ena-sl-c03-federal": [("federal-inspection-authorities", R, NO_EVENT)],
    "ena-sl-c04-federal": [("epa-penalty-policies", C, "Penalty calculation policies. " + NO_EVENT)],
    "ena-sl-c08-consultant": [("nepa-s112-fee", EN, None)],
    "ena-sl-c08-federal": [
        ("nepa-fra-2023", R, None),
        ("ceq-nepa-regs-removal", X, "Removed the government-wide regulations; never a basis (CR-SC-001 #2)."),
        ("ceq-nepa-guidance-2025", C, None), ("doi-nepa-procedures", R, None), ("usda-nepa-procedures", R, None),
        ("dot-nepa-procedures", R, None), ("epa-nepa-procedures", R, "Proposed; decides nothing until in force."),
        ("nepa-s112-fee", EN, None), ("seven-county", C, None), ("usfs-objection-rule", C, None),
        ("ceq-permitting-data-standard", C, None)],
    "ena-sl-c08-state": [
        ("ceqa-2025-reforms", C, EX_STATE),
        ("state-sepa-ca", R, EX_STATE), ("state-sepa-wa", R, EX_STATE), ("state-sepa-mn", R, EX_STATE),
        ("state-sepa-ny", R, EX_STATE),
        ("nepa-assignment-23usc327", EN, "State transportation agencies may carry federal review by assignment. " + NO_EVENT)],
    "ena-sl-c10-state": [("caa-507-sbeap", R, NO_EVENT)],
    "ena-sl-c12-federal-overseer": [("fy2026-interior-approps", EN, "Capitalization grant funding.")],
    "ena-sl-c12-state-funder": [("fy2026-interior-approps", EN, "Capitalization grant funding.")],
    "ena-sl-c16-state": [("state-licensing-acts-wi", C, "Limits use of a licensed title in classified positions. " + EX_STATE)],
    "ena-db-c25-state": [("npdes-ereporting-rule", EN, "Electronic monitoring reports make data-driven targeting possible. " + NO_EVENT)],
    "ena-db-c26-private": [("report-certification-rules", R, NO_EVENT)],
    "ena-db-c26-public-utility": [("report-certification-rules", R, NO_EVENT)],
    "ena-db-c26-federal-facility": [("report-certification-rules", R, NO_EVENT)],
    "ena-ps-c18-federal": [("federal-ethics-rules", R, NO_EVENT)],
    "ena-v1-3-1-4-federal": [("federal-acquisition-assistance", R, NO_EVENT)],
    "ena-v1-6-3-4-federal-rulemaking": [("eo-12866-circular-a4", R, NO_EVENT)],
    "ena-v1-6-4-5-federal": [("anti-lobbying-1913", C, NO_EVENT)],
    "ena-v1-7-1-3-federal": [("eo-14303", R, "Directs the update of agency scientific-integrity policies.")],
    "ena-v1-6-2-3-federal": [
        ("usfs-objection-rule", C, None), ("usda-nepa-procedures", R, "Review of plan revisions and amendments."),
        ("doi-nepa-procedures", R, None),
        ("roadless-rule-rescission", X, "Proposed rescission of a planning-area prohibition; never a basis.")],
}

DELEGATED = ("ena-sc-c14-state-delegated", "ena-sl-c02-state-regulator")
SEP = "Delegated constraints:"
NOTE = ("S2 close-out A (A5 SC; CR-SC-001 #2, #5): instrument link roles set; only requires links decide venue "
        "applicability.")
DB52_FED_NOTE = ("ADR-0016: applicability is computed, not asserted. The revoked orders are linked as requires and the "
                 "revoking orders as removed-requirement, so the federal value computes no-current-basis from their "
                 "status; statute-based duties keep the work possible, and the Q4 default shows the value with a note "
                 "and no exclusion.")


def registry():
    ids = set()
    for line in (L.DATA_V2 / "instruments" / "instruments.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            ids.add(json.loads(line)["id"])
    return ids


def apply(dry: bool) -> list[dict]:
    reg = registry()
    report = []
    for key, rows in ROLES.items():
        rid = "seed:" + key
        path = ENA / (L.id_to_stem(rid) + ".yaml")
        rec = L.load_yaml(path)
        if rec.get("provenance", {}).get("agent", [""])[0] != "emstagent:a5-sc@wp-05":
            raise SystemExit(f"{rid}: not an SC-authored enactment; refusing to edit")
        want = {"seed:ins/" + k: (role, note) for k, role, note in rows}
        for ins in want:
            if ins not in reg:
                raise SystemExit(f"{rid}: {ins} not in the instrument registry")
        existing = [x["instrument"] if isinstance(x, dict) else x for x in rec.get("characteristicInstruments", [])]
        missing = [i for i in existing if i not in want]
        if missing:
            raise SystemExit(f"{rid}: existing links without a role decision: {missing}")
        links = []
        for ins in existing + [i for i in want if i not in existing]:
            role, note = want[ins]
            item = {"instrument": ins, "role": role}
            if note:
                item["note"] = {"en": note}
            links.append(item)
            report.append({"enactment": rid, "instrument": ins, "role": role,
                           "action": "role-set" if ins in existing else "added"})
        new = {}
        for k, v in rec.items():
            if k == "note" and "characteristicInstruments" not in rec:
                new["characteristicInstruments"] = links
            if k == "characteristicInstruments":
                new[k] = links
                continue
            new[k] = v
            if k == "authorityBasis" and key in DELEGATED:
                text = v["en"]
                if SEP in text:
                    head, tail = text.split(SEP, 1)
                    new["authorityBasis"] = {"en": head.strip()}
                    new["delegatedConstraints"] = {"en": tail.strip()[0].upper() + tail.strip()[1:]}
                    report.append({"enactment": rid, "instrument": "", "role": "",
                                   "action": "delegatedConstraints-moved"})
        if "characteristicInstruments" not in new:
            new["characteristicInstruments"] = links
        if key == "ena-db-c52-federal":
            new["note"] = {"en": DB52_FED_NOTE}
        ed = (new.get("editorialNote") or {}).get("en", "")
        if NOTE not in ed:
            new["editorialNote"] = {"en": (ed + " " + NOTE).strip()}
        prov = new["provenance"]
        if AGENT not in prov["agent"]:
            prov["agent"] = list(prov["agent"]) + [AGENT]
        # keep key order sensible: editorialNote before provenance
        if "editorialNote" in new and list(new).index("editorialNote") > list(new).index("provenance"):
            p = new.pop("provenance")
            new["provenance"] = p
        if not dry:
            L.write_yaml(path, new)
    return report


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    rep = apply(a.dry_run)
    out = HERE / "generated" / "instrument_link_roles.csv"
    out.parent.mkdir(exist_ok=True)
    if not a.dry_run:
        out.write_text(L.csv_text(["enactment", "instrument", "role", "action"], rep), encoding="utf-8")
    from collections import Counter
    print(json.dumps({"enactments": len(ROLES), "actions": Counter(r["action"] for r in rep),
                      "roles": Counter(r["role"] for r in rep if r["role"])}, indent=1, default=dict))


if __name__ == "__main__":
    main()
