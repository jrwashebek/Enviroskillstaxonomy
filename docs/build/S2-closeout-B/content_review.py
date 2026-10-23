"""DB (A6) content review of the DC-authored DB candidates DB-C06 and DB-C21 (work-order row 40; ADR-0030 §3.2).

Agent review, not a human review: reviewStatus stays unreviewed. DC (A4, the author of record's craft, same builder)
applies the two changes the review asks for. Findings are in WORKLOG.md (row 40).
"""
import s2b_lib as S

ROW = "40"

C06_NOTE = ("DB content review (S2 close-out B, agent review, not human): scope, boundaries (DB-C03 automated process "
            "control; DC-CAND-21 enterprise governance) and recurrence (water, air and waste module enactments) confirmed; no "
            "duplicate in any lane (ADR-0030 §3.2); DC remains author of record. Change: G-2 split added for automated anomaly "
            "and intrusion alerts (task seed:dc-db06-triage-alerts, L2 assisted indicator seed:db-c06-l2-c).")
C21_NOTE = ("DB content review (S2 close-out B, agent review, not human): scope, emerging lifecycle and reviewBy, recurrence "
            "(water, waste, air and envhealth module enactments) and the DB-C29 boundary (risk communication task contributes "
            "to DB-C29) confirmed; no duplicate in any lane (ADR-0030 §3.2); DC remains author of record. Change: the "
            "investigation-plan task now contributes to FC-C16 (trace-level sampling without contamination) and the data "
            "user's laboratory review lives in v1 2.2.3 (CR-DB-001 #3).")


def review():
    spec = {"id": "seed:DB-C06", "roles": ["DC"]}
    S.build_task({"id": "seed:dc-db06-triage-alerts", "wf": "WF-OPERATE", "field": "remote-capable", "formation": "yes",
                  "text": "Triage automated anomaly or intrusion alerts from control and monitoring networks against process data, closing or escalating each with the evidence recorded",
                  "regime": {"mentorshipDependence": "M", "cycleDependence": "none", "placeBoundness": "system-specific",
                             "credentialGate": "none", "currencyDecay": "H"},
                  "note": "G-2 split added at DB review: judging automated alerts, beside the production task seed:dc-db06-report-anomaly."},
                 spec, "core", ROW)
    S.put(S.indicator("seed:DB-C06", "seed:db-c06-l2-c", "L2",
                      "Checks an automated anomaly or intrusion alert against process data and field observation, closing or escalating it with the evidence recorded.",
                      "assisted", ["seed-error-work-sample".replace("seed-error", "seeded-error"), "record-audit"], "core", ["DC"],
                      ["seed:dc-db06-triage-alerts"], att="ATT-AUG"), "core", ROW)

    def add_l2(r):
        for lv in r["levels"]:
            if lv["level"] == "L2" and "seed:db-c06-l2-c" not in lv["indicators"]:
                lv["indicators"].append("seed:db-c06-l2-c")
    S.patch("seed:DB-C06", add_l2, "DB", ROW, C06_NOTE)
    S.patch("seed:DB-C06", lambda r: None, "DC", ROW, None)

    def contrib(r):
        if "seed:FC-C16" not in {s["competency"] for s in r["supports"]}:
            r["supports"].append({"competency": "seed:FC-C16", "strength": "contributing"})
    S.patch("seed:dc-db21-investigation-plan", contrib, "DC", ROW,
            "S2 (DB review): contributing link to FC-C16 (trace-level sampling without contamination).")
    S.patch("seed:DB-C21", lambda r: None, "DB", ROW, C21_NOTE)


SPECS = []
PATCHES = [review]
