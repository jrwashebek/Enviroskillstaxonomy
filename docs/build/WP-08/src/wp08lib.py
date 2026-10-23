"""WP-08 authoring library: turns compact role specs into RoleProfile / RoleVariant / JobFamily records.

Authoring tool in WP-08's lane (ADR-0029 rule 4): never run by CI or the release build. Every value it writes is an
agent draft (raterType llm, validationStatus draft, evidence S). Licence: Apache-2.0.
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
import emstlib as L  # noqa: E402

AGENT = "emstagent:fh-agent@wp-08"
MODEL = "claude-opus-5-5"
PROMPT = "docs/build/WP-08/prompts/wp08-role-profile.md@1"
GENERATED_AT = "2026-10-23T17:00:00Z"
REVIEW_BY_EMERGING = "2027-10-23"
LEVEL_ORDER = ["A", "L1", "L2", "L3", "L4", "L5"]
ROLE_LEVELS = ["entry", "journey", "senior", "lead", "strategic"]
ABBR = {"e": "entry", "j": "journey", "s": "senior", "l": "lead", "x": "strategic"}
DISCLAIMER = "Not a classification basis / not a job analysis / not for RIF or rating decisions."
DRAFT_NOTICE = ("Agent draft (raterType llm, validationStatus draft, evidence S): task importance, time share, "
                "critical and needed-at-entry flags and target levels are not job-analysis results.")
TX_FLOOR = ["DC-CAND-01", "DC-CAND-02", "DC-CAND-13", "DC-CAND-05"]  # ADR-0025 floor, every role at least L1 (WP-04)


def role_level_bands():
    v = L.load_yaml(ROOT / "vocab" / "proficiency_levels.yaml")
    return {b["key"]: b["band"] for b in v["role_level_bands"]}


BANDS = role_level_bands()


def mvp_roles():
    return {r["role_key"]: r for r in csv.DictReader(open(ROOT / "docs/decisions/mvp_role_set.csv", encoding="utf-8"))}


class Index:
    """Live competencies and tasks with their area (core or module namespace)."""

    def __init__(self):
        self.comps, self.tasks, self.area = {}, {}, {}
        self.by_comp = defaultdict(list)
        for loc, rec in L.iter_records():
            if not isinstance(rec, dict):
                continue
            t = rec.get("type")
            if t not in ("Competency", "Task"):
                continue
            rid = rec["id"]
            self.area[rid] = rec.get("module")
            if t == "Competency":
                self.comps[rid] = rec
            else:
                self.tasks[rid] = rec
        for tid, t in self.tasks.items():
            if not self.task_usable(tid):
                continue
            for s in t.get("supports") or []:
                self.by_comp[s["competency"]].append((s.get("strength"), tid))

    @staticmethod
    def held(rec):
        return bool(rec.get("indigenousDataFlag"))

    def comp_usable(self, cid):
        c = self.comps.get(cid)
        return bool(c) and c.get("status") not in ("superseded", "withdrawn") and not self.held(c) \
            and c.get("validationStatus") == "draft"

    def task_usable(self, tid):
        t = self.tasks.get(tid)
        return bool(t) and t.get("status") not in ("superseded", "withdrawn") and not self.held(t) \
            and t.get("validationStatus") == "draft"

    def levels_of(self, cid):
        """Levels at which the competency publishes indicators (knowledge areas: their levelSpan)."""
        c = self.comps[cid]
        lv = [x.get("level") for x in c.get("levels") or [] if x.get("level")]
        if lv:
            return lv
        span = c.get("levelSpan") or {}
        if span.get("min") and span.get("max"):
            i, j = LEVEL_ORDER.index(span["min"]), LEVEL_ORDER.index(span["max"])
            return LEVEL_ORDER[i:j + 1]
        return []

    def primary_comp(self, tid, prefer=()):
        sup = self.tasks[tid].get("supports") or []
        for s in sup:
            if s["competency"] in prefer and s.get("strength") == "primary":
                return s["competency"]
        for s in sup:
            if s["competency"] in prefer:
                return s["competency"]
        return sup[0]["competency"] if sup else None

    def text(self, tid):
        return (self.tasks[tid].get("statement") or {}).get("en", "")


@dataclass
class C:
    comp: str
    imp: int
    targets: str            # one token per role level, '-' = not targeted; e.g. "L1 L2 L3"
    dist: bool = False


@dataclass
class T:
    task: str
    imp: int
    w: float = 1.0
    flags: str = ""         # C critical, E needed at entry, F formation task
    lv: str = ""            # role levels by letter (e j s l x); '' = all levels of the role


@dataclass
class X:
    target: str             # task key, or 'role'
    kind: str               # content_change_types for tasks; role_signal_types for 'role'
    drivers: list
    note: str
    instruments: list = field(default_factory=list)
    signals: list = field(default_factory=list)


@dataclass
class V:
    actor: str
    pos: str
    subtype: str | None = None
    industry: str | None = None
    ownership: str | None = None
    delivery: str | None = None
    slice: str | None = None
    label: str | None = None
    note: str = ""
    gates: list = field(default_factory=list)          # [(credential key without seed:, kind)]
    signoff: tuple | None = None                       # (kind, [credential keys])
    instruments: list = field(default_factory=list)    # instrument keys without seed:
    adds: list = field(default_factory=list)           # [T]
    drops: list = field(default_factory=list)          # [task keys]
    juris: list = field(default_factory=list)
    band: str | None = None                            # e.g. "GS-5 to GS-7 [entry]; GS-9 to GS-11 [journey]"
    scheme: str = "GS"


@dataclass
class Role:
    key: str
    tier: str
    area: str
    wf: str
    levels: list
    life: str
    title: str
    definition: str
    function: str
    comps: list
    tasks: list = field(default_factory=list)
    auto: bool = False
    per: int = 3
    variants: list = field(default_factory=list)
    change: list = field(default_factory=list)
    entry_from: list = field(default_factory=list)
    progresses_to: list = field(default_factory=list)
    use_tier: str = "describe"
    alt: list = field(default_factory=list)
    emerging: dict | None = None    # evidenceSignals, feederRoles, horizon, scenarioSensitivity, counterSignal
    note: str = ""
    tx_floor: dict = field(default_factory=dict)  # comp -> targets string override for the TX floor
    skip: list = field(default_factory=list)      # auto rule: task keys FH excluded after review


STRATEGIC_VERBS = ("Set ", "Establish ", "Charter ", "Govern ", "Run a model risk", "Report data and AI")
SENIOR_VERBS = ("Design ", "Plan ", "Lead ", "Train ", "Teach ", "Evaluate ", "Review another", "Decide whether",
                "Direct ", "Supervise ", "Negotiate ", "Recommend ", "Advise ", "Certify ", "Resolve ", "Testify ",
                "Defend ", "Audit a local", "Brief ", "Prepare a contingency", "Specify ", "Exercise responsible",
                "Mediate ", "Present ", "Represent ")
JOURNEY_VERBS = ("Write ", "Prepare ", "Prescribe ", "Develop ", "Fit ", "Forecast ", "Compare ", "Estimate ",
                 "Calculate ", "Determine ", "Issue ", "Draft ", "Assess ", "Review ", "Model ", "Simulate ", "Run a ",
                 "Analyze ", "Quantify ", "Select ", "Schedule ", "Derive ", "Delineate ", "Characterize ",
                 "Appraise ", "Translate ", "Inspect contract", "Adjust a ", "Conduct a vulnerability", "Rank ",
                 "Verify that", "Close out", "Integrate ", "Synthesize ", "Rate ", "Apply a data-limited")


def heuristic_levels(text, levels):
    """Draft rule for P2-P4 auto bundles (documented in the prompt file): which role levels perform a task."""
    if text.startswith(STRATEGIC_VERBS):
        return levels[-2:] if len(levels) > 1 else levels
    if text.startswith(SENIOR_VERBS):
        if "senior" in levels:
            return levels[levels.index("senior"):]
        return levels[1:] if len(levels) > 1 else levels
    if text.startswith(JOURNEY_VERBS) and levels[0] == "entry" and len(levels) > 1:
        return levels[1:]
    return list(levels)


def lv_from(s, levels):
    if not s:
        return list(levels)
    out = [ABBR[ch] for ch in s]
    bad = [x for x in out if x not in levels]
    if bad:
        raise ValueError(f"task levels {bad} not in role levels {levels}")
    return [x for x in levels if x in out]


def prov(evidence="S", sources=None, adr=None):
    p = {"method": "llm-assisted", "agent": [AGENT], "generatedAt": GENERATED_AT, "toolVersion": MODEL,
         "promptVersion": PROMPT, "evidenceLabel": evidence, "reviewStatus": "unreviewed",
         "adr": adr or ["ADR-0006", "ADR-0017", "ADR-0024"]}
    if sources:
        p["sources"] = sorted(sources)
    return p


def sk(k):
    return k if k.startswith("seed:") else f"seed:{k}"
