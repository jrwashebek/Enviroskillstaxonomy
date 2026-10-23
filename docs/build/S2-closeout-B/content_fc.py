"""FC (A3, as WP-08 contributor) content for S2 close-out builder B: CR-FC-001 field-performance content in SL-C03
(work-order row 25). SL-C03 and its tasks are SC-lane records (builder A): this module writes only the new field
task and indicators and makes minimal patches (levels[] entries, contributing links, provenance agent, note).
Content evidence label J (FC Phase 2 report §1.5, codebook E4; CR-FC-001).
"""
import s2b_lib as S

ROW = "25"
FC = ["FC"]
NOTE = ("S2 (CR-FC-001 ruling; FC as WP-08 contributor, SC review pending): field-performance anchors of merged candidate "
        "FC-C04 added: adaptation-in-place task seed:fc-sl-c03-extend-inspection (G-2), L2 beyond-checklist indicator, L1 "
        "field-measurement integrity indicator, L2 assisted imagery check (links FC-C02 ground-truthing); contributing links "
        "from the sampling task to FC-C24 and FC-C16 and from the site inspection task to v1-4.4.4-A. FC-C04 lineage is "
        "recorded here because derivedFrom takes v1 keys only.")

TASK = {"id": "seed:fc-sl-c03-extend-inspection", "wf": "WF-ENFORCE", "field": "on-site-required", "formation": "yes",
        "text": "Extend an inspection beyond the planned checklist when site conditions show an unpermitted activity, discharge or control failure, documenting each observation",
        "regime": {"mentorshipDependence": "H", "cycleDependence": "none", "placeBoundness": "general", "credentialGate": "internal-qualification", "currencyDecay": "M"},
        "note": "CR-FC-001: adaptation in place (G-2), alongside the checklist inspection task seed:v1-6.1.2-T1."}

INDS = [
    ("seed:fc-sl-c03-l1-measure", "L1", "unaided", ["record-audit", "task-book-observation"], None,
     "Measures field parameters during an inspection with meters calibrated that day, recording the calibration so that each measurement can be used as evidence.",
     ["seed:sc-collect-inspection-evidence", "seed:v1-6.1.2-T1"]),
    ("seed:fc-sl-c03-l2-beyond-checklist", "L2", "unaided", ["task-book-observation", "seeded-error-work-sample"], "ATT-CPX",
     "Recognizes evidence of an unpermitted discharge, control failure or unreported activity outside the checklist, documenting it with photographs, measurements and location.",
     ["seed:fc-sl-c03-extend-inspection"]),
    ("seed:fc-sl-c03-l2-imagery-check", "L2", "assisted", ["record-audit", "task-book-observation"], "ATT-AUG",
     "Checks drone or remote imagery used to target an inspection against conditions observed on site, recording where the imagery was wrong.",
     ["seed:v1-6.1.2-T1", "seed:sc-plan-inspection"]),
]

SPECS = []


def _write_new():
    spec = {"id": "seed:SL-C03", "roles": FC}
    S.build_task(TASK, spec, "core", ROW)
    for key, lvl, mode, methods, att, text, served in INDS:
        S.put(S.indicator("seed:SL-C03", key, lvl, text, mode, methods, "core", FC, served, att=att), "core", ROW)


def _levels(rec):
    want = {"L1": ["seed:fc-sl-c03-l1-measure"], "L2": ["seed:fc-sl-c03-l2-beyond-checklist", "seed:fc-sl-c03-l2-imagery-check"]}
    for lv in rec["levels"]:
        for k in want.get(lv["level"], []):
            if k not in lv["indicators"]:
                lv["indicators"].append(k)


def _contrib(*cids):
    def fn(rec):
        have = {s["competency"] for s in rec["supports"]}
        for c in cids:
            if c not in have:
                rec["supports"].append({"competency": c, "strength": "contributing"})
    return fn


def sl_c03_field_content():
    _write_new()
    S.patch("seed:SL-C03", _levels, "FC", ROW, NOTE)
    S.patch("seed:sc-collect-inspection-evidence", _contrib("seed:FC-C24", "seed:FC-C16"), "FC", ROW,
            "S2 (CR-FC-001 ruling): contributing links to FC-C24 (field custody and QC) and FC-C16 (trace-level sampling) added by FC.")
    S.patch("seed:v1-6.1.2-T1", _contrib("seed:v1-4.4.4-A"), "FC", ROW,
            "S2 (CR-FC-001 ruling): contributing link to v1-4.4.4-A (hazardous, industrial and energized sites) added by FC.")


PATCHES = [sl_c03_field_content]
