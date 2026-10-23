"""Reference implementation of the ADR-0028 s2 evidence rule (P-LM-07): what may move a computed change indicator.

Owner: A9 LM (WP-10). For DE to port into scripts/validate_v2.py / the build's indicator rule
(vocab/rules/<rule-id>@<version>.yaml). Pure Python, no dependencies, deterministic.

A signal set moves an indicator (target, direction, driver) only if ALL hold; otherwise the outcome is `watch`:
  ER-1  two INDEPENDENT signal families point the same way. Families: capability, observed-use, deployment,
        postings-pds, headcount, plan-requirements, worker-report (+ policy for role-change indicators only;
        projection and workload never count). Two indices built on the same data family count as one (they share a
        family). The two supporting signals must also have disjoint upstream data providers, so no indicator rests on
        a single vendor's data (ADR-0008 s4) - e.g. BLS 'observed' exposure is built on Anthropic and Microsoft data
        and is NOT independent of either.
  ER-2  persistence: two distinct consecutive observation periods of the same measure, or one period plus a
        registered deployment (a deployment-family signal flagged registeredDeployment).
  ER-3  every counted signal's crosswalk path has weakest match type exact or close (broad/related/narrow -> watch).
  ER-4  driver tag declared and consistent: each counted signal carries the indicator's driver (fiscal and policy
        shocks cannot masquerade as AI effects).
  ER-5  named human review: reviewStatus reviewed|validated|gold and a pid:/panel: reviewer (no software agent).
Excluded before counting (never evidence): personalData != false (record invalid), careFlag/tribalPrograms true
(quarantined until the Tribal Council clears it), v1-analyst assessments (prior evidence only, ADR-0008 s5),
signalStatus retired, other targets, other directions.

Interim field access: family, independence key and registered deployment are read from typed fields if present
(signalFamily, independenceKey, registeredDeployment - proposed in CR-LM-001) or from the interim notation schemes
EMST-signalFamily / EMST-independenceKey / EMST-registeredDeployment.
"""

COUNTING_FAMILIES = {"capability", "observed-use", "deployment", "postings-pds", "headcount", "plan-requirements",
                     "worker-report", "policy"}
NEVER_COUNT = {"projection", "workload"}
GOOD_MATCH = {"skos:exactMatch", "skos:closeMatch"}
REVIEWED = {"reviewed", "validated", "gold"}

# Upstream data providers behind each independence key. Unlisted keys are their own provider.
PROVIDERS = {
    "anthropic-economic-index": {"anthropic"},
    "anthropic-labor-market-impacts": {"anthropic"},
    "anthropic-robot-exposure": {"anthropic"},
    "ms-working-with-ai": {"microsoft"},
    "eloundou-gpts-are-gpts": {"openai-eloundou"},
    "bls-ai-exposure-theoretical": {"felten-raj-seamans", "openai-eloundou", "eisfeldt"},
    "bls-ai-exposure-observed": {"anthropic", "microsoft"},
    "pnnl-openai-draftnepabench": {"pnnl", "openai"},
    "ombegov-ai-inventory": {"omb-agency-self-report"},
    "opm-ehri-fwd": {"opm-ehri"},
    "gao-opm": {"opm-ehri"},
    "openlmp-usfs-western-plans": {"openlmp"},
}
# External-index assessments: instrument -> (family, independence key)
INSTRUMENTS = {
    "eloundou-gpts-are-gpts": ("capability", "eloundou-gpts-are-gpts"),
    "ms-working-with-ai-applicability": ("observed-use", "ms-working-with-ai"),
    "aei-task-usage": ("observed-use", "anthropic-economic-index"),
    "aei-labor-market-impacts": ("observed-use", "anthropic-labor-market-impacts"),
    "aei-robot-exposure": ("capability", "anthropic-robot-exposure"),
    "bls-ai-exposure-theoretical": ("capability", "bls-ai-exposure-theoretical"),
    "bls-ai-exposure-observed": ("observed-use", "bls-ai-exposure-observed"),
}


def _nota(rec, scheme):
    for n in rec.get("notation") or []:
        if n.get("scheme") == scheme:
            return n.get("value")
    return None


def family(rec):
    if rec.get("type") == "ExposureAssessment":
        return INSTRUMENTS.get(rec.get("instrument"), ("capability", rec.get("instrument")))[0]
    return rec.get("signalFamily") or _nota(rec, "EMST-signalFamily")


def independence_key(rec):
    if rec.get("type") == "ExposureAssessment":
        return INSTRUMENTS.get(rec.get("instrument"), (None, rec.get("instrument") or rec.get("raterId")))[1]
    return rec.get("independenceKey") or _nota(rec, "EMST-independenceKey") or rec.get("source")


def providers(rec):
    k = independence_key(rec)
    return PROVIDERS.get(k, {k})


def registered(rec):
    v = rec.get("registeredDeployment")
    if v is None:
        v = _nota(rec, "EMST-registeredDeployment") == "true"
    return bool(v) and family(rec) == "deployment"


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


def _direction(rec):
    if rec.get("type") == "ExposureAssessment":
        return rec.get("direction")  # external-index assessments carry no direction; they support only via ER-1 pairing
    return rec.get("direction")


def evaluate(indicator, records):
    """indicator: {targetId, direction, driver, kind: 'role-change'|'skill-change'}.
    Returns {"decision": "moves"|"watch"|"invalid", "reasons": [codes], "counted": [ids]}."""
    reasons, eligible = [], []
    for r in records:
        if r.get("personalData") is not False and r.get("type") == "ChangeSignal":
            return {"decision": "invalid", "reasons": ["ER-0-PERSONAL-DATA"], "counted": []}
        if r.get("careFlag") or r.get("tribalPrograms") or r.get("indigenousDataFlag"):
            reasons.append("ER-0-QUARANTINED")
            continue
        if r.get("raterType") == "v1-analyst":
            reasons.append("ER-0-V1-PRIOR-EVIDENCE")
            continue
        if r.get("signalStatus") == "retired":
            continue
        if r.get("targetId") != indicator["targetId"]:
            continue
        d = _direction(r)
        if r.get("type") == "ChangeSignal" and d != indicator["direction"]:
            reasons.append("ER-0-DIRECTION")
            continue
        fam = family(r)
        if fam in NEVER_COUNT or fam not in COUNTING_FAMILIES:
            reasons.append("ER-1-NONCOUNTING-FAMILY")
            continue
        if fam == "policy" and indicator.get("kind") == "skill-change":
            reasons.append("ER-1-POLICY-NOT-FOR-SKILL-CHANGE")
            continue
        eligible.append(r)

    # ER-4 driver attribution (applied before pairing so a fiscal shock cannot pair with an AI capability signal)
    drv = indicator.get("driver")
    with_driver = []
    for r in eligible:
        tags = set(r.get("drivers") or [])
        if r.get("type") == "ExposureAssessment":
            tags = {"AI"}  # external AI-exposure indices measure AI by construction
        if not tags or (drv and drv not in tags):
            reasons.append("ER-4-DRIVER")
            continue
        with_driver.append(r)

    # ER-3 match type
    matched = []
    for r in with_driver:
        if not _match_ok(r):
            reasons.append("ER-3-MATCH-TYPE")
            continue
        matched.append(r)

    # ER-5 named human review
    reviewed = []
    for r in matched:
        if not _reviewed(r):
            reasons.append("ER-5-NO-NAMED-REVIEW")
            continue
        reviewed.append(r)

    # ER-1 two independent families with disjoint providers
    pair = None
    fams = {}
    for r in reviewed:
        fams.setdefault(family(r), []).append(r)
    keys = sorted(fams)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            for ra in fams[a]:
                for rb in fams[b]:
                    if not (providers(ra) & providers(rb)):
                        pair = (ra, rb)
                        break
                if pair:
                    break
            if pair:
                break
        if pair:
            break
    if not pair:
        if len(keys) < 2:
            reasons.append("ER-1-ONE-FAMILY")
        else:
            reasons.append("ER-1-SAME-VENDOR")
        return {"decision": "watch", "reasons": sorted(set(reasons)), "counted": []}

    # ER-2 persistence: two distinct periods of the same measure among reviewed signals, or a registered deployment
    by_measure = {}
    for r in reviewed:
        by_measure.setdefault((family(r), _measure(r)), set()).add(_period(r))
    persistent = any(len(ps) >= 2 for ps in by_measure.values()) or any(registered(r) for r in reviewed)
    if not persistent:
        reasons.append("ER-2-NO-PERSISTENCE")
        return {"decision": "watch", "reasons": sorted(set(reasons)), "counted": []}
    return {"decision": "moves", "reasons": [], "counted": sorted(r["id"] for r in reviewed)}


def evaluate_corpus(records, kinds=("role-change",)):
    """Evaluate every (target, direction, driver) combination present in a corpus; used for the regression assertion
    that no agent-seeded signal moves an indicator."""
    combos = set()
    for r in records:
        if r.get("type") != "ChangeSignal":
            continue
        for dv in r.get("drivers") or []:
            combos.add((r.get("targetId"), r.get("direction"), dv))
    out = {}
    for (t, d, dv) in sorted(combos):
        for k in kinds:
            out[(t, d, dv, k)] = evaluate({"targetId": t, "direction": d, "driver": dv, "kind": k}, records)
    return out
