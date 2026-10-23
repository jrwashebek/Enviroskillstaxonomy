"""change-indicator@1.0.0: the ADR-0028 §2 two-family evidence rule (vocab/rules/change-indicator@1.0.0.yaml).

Port of LM's reference implementation (docs/methods/ci/evidence_rule.py, 2026-10-23; ADR-0029 §8.3). Differences from
the reference, all required by the rulings:
  * families and `counts_toward` come from vocab/change_types.yaml#signal_families, providers from
    #independence_keys, and the external-index instrument map from the rule file's `external_index_instruments`,
    instead of constants;
  * only `signalStatus: active` signals count (ER-0-NOT-ACTIVE otherwise); watch signals are evaluated for the
    "what's coming" view only (`include_watch=True` gives the hypothetical decision shown there);
  * readings of signpost SP-12 are quarantined like careFlag (ER-0-QUARANTINED);
  * organization targets never match a role or skill indicator (ER-0-ORGANIZATION-TARGET).

A signal set moves an indicator {targetId, direction, driver, kind} only if ER-1..ER-5 all hold; otherwise `watch`.
Deterministic, no I/O beyond the vocabulary files read by load_config().
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import emstlib as L  # noqa: E402

RULE_ID = "change-indicator"
RULE_VERSION = "1.0.0"
GOOD_MATCH = {"skos:exactMatch", "skos:closeMatch"}
REVIEWED = {"reviewed", "validated", "gold"}
QUARANTINED_SIGNPOSTS = {"vocab:scenarios#SP-12", "SP-12"}


@dataclass
class Config:
    counts_toward: dict = field(default_factory=dict)      # family -> set(kinds)
    providers: dict = field(default_factory=dict)          # independence key -> set(providers)
    instruments: dict = field(default_factory=dict)        # external-index instrument -> (family, key)
    kinds: tuple = ("role-change", "skill-change")

    @property
    def families(self):
        return set(self.counts_toward)


def load_config(root: Path = L.ROOT) -> Config:
    ct = L.load_yaml(root / "vocab" / "change_types.yaml")
    counts = {v["notation"]: set(v.get("counts_toward") or []) for v in ct["signal_families"]["values"]}
    providers = {k["key"]: set(k.get("providers") or [k["key"]]) for k in ct["independence_keys"]["keys"]}
    kinds = tuple(v["notation"] for v in (ct.get("change_indicator_kinds") or {}).get("values", [])) or ("role-change", "skill-change")
    rule = L.load_yaml(root / "vocab" / "rules" / f"{RULE_ID}@{RULE_VERSION}.yaml")
    inst = {k: (v["family"], v["independenceKey"]) for k, v in (rule.get("external_index_instruments") or {}).items()}
    return Config(counts, providers, inst, kinds)


_DEFAULT: Config | None = None


def default_config() -> Config:
    global _DEFAULT
    if _DEFAULT is None:
        _DEFAULT = load_config()
    return _DEFAULT


# ------------------------------------------------------------------------------------------------ field access
def _nota(rec, scheme):
    """Interim encoding used by drafts written before ADR-0029: notation scheme EMST-<field>."""
    for n in rec.get("notation") or []:
        if isinstance(n, dict) and n.get("scheme") == scheme:
            return n.get("value")
    return None


def _nota_all(rec, scheme):
    return [n.get("value") for n in rec.get("notation") or [] if isinstance(n, dict) and n.get("scheme") == scheme]


def is_external(rec) -> bool:
    return rec.get("type") == "ExposureAssessment"


def family(rec, cfg: Config | None = None):
    cfg = cfg or default_config()
    if is_external(rec):
        return cfg.instruments.get(rec.get("instrument"), ("capability", rec.get("instrument")))[0]
    return rec.get("signalFamily") or _nota(rec, "EMST-signalFamily")


def independence_key(rec, cfg: Config | None = None):
    cfg = cfg or default_config()
    if is_external(rec):
        return cfg.instruments.get(rec.get("instrument"), (None, rec.get("instrument") or rec.get("raterId")))[1]
    return rec.get("independenceKey") or _nota(rec, "EMST-independenceKey") or rec.get("source")


def providers(rec, cfg: Config | None = None):
    cfg = cfg or default_config()
    k = independence_key(rec, cfg)
    return cfg.providers.get(k, {k})


def registered(rec, cfg: Config | None = None):
    v = rec.get("registeredDeployment")
    if v is None:
        v = _nota(rec, "EMST-registeredDeployment") == "true"
    return bool(v) and family(rec, cfg) == "deployment"


def signposts(rec):
    return set(rec.get("scenarioSignposts") or []) | set(_nota_all(rec, "EMST-signpost"))


def quarantined(rec) -> bool:
    return bool(rec.get("careFlag") or rec.get("tribalPrograms") or rec.get("indigenousDataFlag")
                or signposts(rec) & QUARANTINED_SIGNPOSTS)


def _period(rec):
    p = rec.get("observedPeriod") or {}
    return (str(p.get("start")), str(p.get("end")))


def _measure(rec):
    return (rec.get("measure") or {}).get("name") or rec.get("instrument")


def _reviewed(rec):
    rs = rec.get("reviewStatus") or (rec.get("provenance") or {}).get("reviewStatus")
    reviewer = rec.get("reviewer") or ((rec.get("provenance") or {}).get("reviewers") or [None])[0]
    return rs in REVIEWED and isinstance(reviewer, str) and reviewer.startswith(("pid:", "panel:"))


def _match_ok(rec):
    return rec.get("crosswalkMinMatchType") in GOOD_MATCH


# ------------------------------------------------------------------------------------------------ the rule
def evaluate(indicator: dict, records: list, cfg: Config | None = None, include_watch: bool = False) -> dict:
    """indicator: {targetId, direction, driver, kind}. Returns {"decision", "reasons", "counted"}.

    include_watch=True also counts watch signals: the hypothetical shown in the "what's coming" view only."""
    cfg = cfg or default_config()
    kind = indicator.get("kind", "role-change")
    reasons, eligible = [], []
    for r in records:
        if r.get("type") == "ChangeSignal" and r.get("personalData") is not False:
            return {"decision": "invalid", "reasons": ["ER-0-PERSONAL-DATA"], "counted": []}
        if r.get("targetId") != indicator["targetId"]:
            continue
        if r.get("type") == "ChangeSignal" and r.get("targetType") == "organization":
            reasons.append("ER-0-ORGANIZATION-TARGET")
            continue
        if quarantined(r):
            reasons.append("ER-0-QUARANTINED")
            continue
        if r.get("raterType") == "v1-analyst":
            reasons.append("ER-0-V1-PRIOR-EVIDENCE")
            continue
        if is_external(r) and r.get("raterType") not in (None, "external-index"):
            continue                     # only external-index assessments are change evidence
        if r.get("type") == "ChangeSignal":
            st = r.get("signalStatus")
            if st == "retired":
                continue
            if st != "active" and not (include_watch and st == "watch"):
                reasons.append("ER-0-NOT-ACTIVE")
                continue
            if r.get("direction") != indicator["direction"]:
                reasons.append("ER-0-DIRECTION")
                continue
        fam = family(r, cfg)
        if fam not in cfg.families or not cfg.counts_toward.get(fam):
            reasons.append("ER-1-NONCOUNTING-FAMILY")
            continue
        if kind not in cfg.counts_toward[fam]:
            reasons.append("ER-1-POLICY-NOT-FOR-SKILL-CHANGE" if fam == "policy" else "ER-1-NONCOUNTING-FAMILY")
            continue
        eligible.append(r)

    # ER-4 driver attribution, before pairing, so a fiscal shock cannot pair with an AI capability signal
    drv = indicator.get("driver")
    with_driver = []
    for r in eligible:
        tags = {"AI"} if is_external(r) else set(r.get("drivers") or [])
        if not tags or (drv and drv not in tags):
            reasons.append("ER-4-DRIVER")
            continue
        with_driver.append(r)

    matched = []                                                   # ER-3
    for r in with_driver:
        if not _match_ok(r):
            reasons.append("ER-3-MATCH-TYPE")
            continue
        matched.append(r)

    reviewed = []                                                  # ER-5
    for r in matched:
        if not _reviewed(r):
            reasons.append("ER-5-NO-NAMED-REVIEW")
            continue
        reviewed.append(r)

    fams: dict = {}                                                # ER-1
    for r in reviewed:
        fams.setdefault(family(r, cfg), []).append(r)
    keys = sorted(fams)
    pair = None
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            for ra in fams[a]:
                for rb in fams[b]:
                    if not (providers(ra, cfg) & providers(rb, cfg)):
                        pair = (ra, rb)
                        break
                if pair:
                    break
            if pair:
                break
        if pair:
            break
    if not pair:
        reasons.append("ER-1-ONE-FAMILY" if len(keys) < 2 else "ER-1-SAME-VENDOR")
        return {"decision": "watch", "reasons": sorted(set(reasons)), "counted": []}

    by_measure: dict = {}                                          # ER-2
    for r in reviewed:
        by_measure.setdefault((family(r, cfg), _measure(r)), set()).add(_period(r))
    persistent = any(len(ps) >= 2 for ps in by_measure.values()) or any(registered(r, cfg) for r in reviewed)
    if not persistent:
        reasons.append("ER-2-NO-PERSISTENCE")
        return {"decision": "watch", "reasons": sorted(set(reasons)), "counted": []}
    return {"decision": "moves", "reasons": [], "counted": sorted(r["id"] for r in reviewed)}


def combos(records):
    """Every (targetId, direction, driver) present among non-organization ChangeSignals."""
    out = set()
    for r in records:
        if r.get("type") != "ChangeSignal" or r.get("targetType") == "organization":
            continue
        for dv in r.get("drivers") or []:
            out.add((r.get("targetId"), r.get("direction"), dv))
    return sorted(out, key=lambda t: tuple(str(x) for x in t))


def evaluate_corpus(records, kinds=("role-change",), cfg: Config | None = None, include_watch: bool = False):
    """Evaluate every combination present in a corpus (regression: no agent-seeded signal moves an indicator)."""
    cfg = cfg or default_config()
    out = {}
    for (t, d, dv) in combos(records):
        for k in kinds:
            out[(t, d, dv, k)] = evaluate({"targetId": t, "direction": d, "driver": dv, "kind": k}, records, cfg, include_watch)
    return out


def view_rows(records, cfg: Config | None = None, stamp: dict | None = None) -> list[dict]:
    """Rows of views/change_indicators.json (rule file `outputs.fields`), plus the watch-inclusive hypothetical."""
    cfg = cfg or default_config()
    stamp = stamp or {}
    rows = []
    for (t, d, dv) in combos(records):
        for k in cfg.kinds:
            ind = {"targetId": t, "direction": d, "driver": dv, "kind": k}
            res = evaluate(ind, records, cfg)
            hyp = evaluate(ind, records, cfg, include_watch=True)
            watch = sorted(r["id"] for r in records if r.get("type") == "ChangeSignal" and r.get("targetId") == t
                           and r.get("direction") == d and dv in (r.get("drivers") or []) and r.get("signalStatus") == "watch")
            rows.append({"targetId": t, "kind": k, "direction": d, "driver": dv, "decision": res["decision"],
                         "reasons": res["reasons"], "counted": res["counted"], "watchSignals": watch,
                         "ifWatchCounted": hyp["decision"], **stamp})
    return rows
