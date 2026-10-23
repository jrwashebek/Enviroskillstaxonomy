"""WP-03 group 6: FC craft enactment of the TX-A validation floor (DC-CAND-13; ADR-0025 §2).

The competency record seed:DC-CAND-13 is authored by WP-04 (DC). WP-03 authors only the FC Enactment, the tasks it
adds (Enactment.additionalTasks) and its indicator variants (Enactment.indicatorVariants). The indicators reference
the competency so that they sit on its levels, but they are listed only on the Enactment, never in the competency's
levels[] (DC declares those). Levels L1-L3 only, inside any span WP-04 is expected to set (TX-A floor: L1 on every
role profile).
"""
from wp03lib import T, I, L, W_prov, build_task_raw, build_indicator_raw, task_path, ind_path, CORE

COMP = "seed:DC-CAND-13"
ENA = "seed:ena-dc-cand-13-fc"
LIFE = "emerging"
RB = "2028-10-23"
SPEC = {"id": COMP, "life": LIFE, "review_by": RB, "use_tier": "develop"}

TASKS = [
    T("seed:fc-txa-plausibility", "Check AI-generated species, habitat or condition outputs for ecological plausibility against place, season, range and site history before using them",
      "WF-MONITOR", "remote-capable", "yes", "M seas eco none M", "R", alias="plaus"),
    T("seed:fc-txa-field-check", "Verify an AI-generated field product, such as a condition map or drafted inspection note, against observations made at the site before it is relied on",
      "WF-MONITOR", "on-site-required", "yes", "M seas eco none M", "R", alias="field", also=["seed:FC-C02"]),
    T("seed:fc-txa-escalate", "Escalate an AI-generated output that conflicts with field evidence, recording the conflicting observation for the analyst and the decision-maker",
      "WF-MONITOR", "remote-capable", "yes", "L none gen none L", "A", alias="esc"),
]

LEVELS = {
    "L1": [I("Flags an AI-generated identification, map or note that conflicts with what the person observed on site, recording the observation before the output is used.", "a", "seeded-error-work-sample record-audit", t="esc field"),
           I("Checks an AI-drafted field form or hazard analysis against actual site conditions, correcting entries that do not match before signing it.", "a", "seeded-error-work-sample", t="field")],
    "L2": [I("Rejects AI-suggested species or habitat outputs that are implausible for the place, season or known range, stating the ecological reason.", "a", "seeded-error-work-sample", att="ATT-KNO", t="plaus"),
           I("Decides when an AI-generated field product needs an on-site check before use, documenting the decision basis and the check result.", "a", "record-audit", att="ATT-GUI", t="field"),
           I("Records the field evidence behind each accepted, corrected or rejected AI output in a form the analyst can use for model correction.", "a", "record-audit", att="ATT-SCO", t="esc")],
    "L3": [I("Designs field ground-truth checks for an AI product used by a program, setting where, how often and by whom field verification is done.", "a", "portfolio-review", att="ATT-AUG", t="field"),
           I("Reviews colleagues' AI-assisted field products for ecological plausibility, returning each with the field evidence for any correction.", "a", "record-audit", att="ATT-FOR", t="plaus"),
           I("Explains to decision-makers the field conditions under which an AI product's outputs should not be trusted, citing ground-truth results.", "u", "structured-interview-bars", att="ATT-SCO", t="plaus field")],
}


def build():
    out = []
    alias = {}
    for t in TASKS:
        alias[t["alias"]] = t["id"]
    for t in TASKS:
        rec = build_task_raw(t, SPEC)
        rec["editorialNote"]["en"] = ("Task of the FC craft enactment " + ENA + " of " + COMP + " (TX-A validation floor). "
                                      + rec["editorialNote"]["en"])
        out.append(("Task", rec, task_path(t["id"])))
    ind_ids = []
    for lv in ["L1", "L2", "L3"]:
        for n, i in enumerate(LEVELS[lv]):
            rec = build_indicator_raw(SPEC, lv, "abcde"[n], i, alias, prefix="ind-fcena-dc-cand-13")
            out.append(("Indicator", rec, ind_path(rec["id"])))
            ind_ids.append(rec["id"])
    ena = {
        "id": ENA, "type": "Enactment",
        "prefLabel": {"en": "Field-craft enactment of AI-output validation: ecological plausibility and field ground truth"},
        "competency": COMP, "enactmentKind": "craft", "craft": "FC",
        "additionalTasks": [t["id"] for t in TASKS],
        "indicatorVariants": ind_ids,
        "note": {"en": ("FC enactment of the TX-A floor competency on validating AI-generated work products before professional use "
                        "(ADR-0025 §2). The field-craft contribution is ecological plausibility and field ground truth: practitioners "
                        "test AI outputs (species identifications, habitat and condition maps, detections, drafted field forms and hazard "
                        "analyses) against what they observe on site and against place, season, range and site history; decide when a "
                        "field check is needed; and reject or escalate outputs that conflict with field evidence. Validation at volume "
                        "(sampling design, error estimation) is the DC enactment; legal sufficiency and provenance in the record is the "
                        "SC enactment. Field ground-truth programmes are FC-C02; adjudication of automated detections at volume is FC-C03.")},
        "layer": "L1", "module": "core", "status": "draft", "lifecycleState": LIFE, "reviewBy": RB,
        "useTier": "develop", "validationStatus": "draft", "license": "CC0-1.0", "sensitivity": "public",
        "editorialNote": {"en": "WP-03 (FC) draft for WP-04 (DC), the owner of seed:DC-CAND-13. Indicator variants are listed here only, not in the competency's levels[]."},
        "provenance": W_prov(),
    }
    out.append(("Enactment", ena, CORE / "enactments" / "seed-ena-dc-cand-13-fc.yaml"))
    return out


EXTRA = [build]
