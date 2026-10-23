"""Small helpers so the S2 close-out A content files stay readable. Licence: Apache-2.0."""

WS = ["work-sample"]
RA = ["record-audit"]
SEW = ["seeded-error-work-sample"]
BARS = ["structured-interview-bars"]
SIM = ["simulation-role-play"]
PORT = ["portfolio-review"]
KT = ["knowledge-test"]
C360 = ["counterpart-360"]
TBO = ["task-book-observation"]
R, EN, C, X = "requires", "enables", "constrains", "removed-requirement"


def T(id, text, wf, field="remote-capable", formation="partial", **kw):
    d = {"id": id, "text": text, "wf": wf, "field": field, "formation": formation}
    d.update(kw)
    return d


def I(text, methods, attr=None, obs4=3, mode="unaided", tasks=None, **kw):
    d = {"text": text, "methods": methods, "attr": attr, "obs4": obs4, "mode": mode, "tasks": tasks or []}
    d.update(kw)
    return d


def E(id, label, actor, basis, principal, venue, note, position=None, links=None, **kw):
    d = {"id": id, "label": label, "actor": actor, "basis": basis, "principal": principal, "venue": venue,
         "note": note, "position": position, "links": links or []}
    d.update(kw)
    return d
