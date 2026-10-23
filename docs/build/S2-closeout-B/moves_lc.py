#!/usr/bin/env python3
"""LC (A8) data moves for S2 close-out builder B (authoring aid; CI never runs it).

  python3 docs/build/S2-closeout-B/moves_lc.py pathways      # row 37: CR-LC-001 #1-#3
  python3 docs/build/S2-closeout-B/moves_lc.py credentials   # row 38: CR-LC-001 #5 and CR-DB-001 #7

pathways: moves the 11 staged pathways from docs/build/WP-07/staging/pathways/ into data/v2/core/pathways/:
  - each step's "all indicators at Lx" outcomes become sequence[].cloOutcomes {competency, level} (the generic CLO is
    the competency's levels[Lx].indicators; enactment variants are never part of it, CR-LC-001 #4), and the pathway's
    outcomes become Pathway.cloOutcomes (union of the steps); a step outcome that is not a full generic CLO stays in
    outcomes[] as a specific indicator;
  - formation provisions are typed from WP-07's audit copy docs/build/WP-07/formation_provisions.csv into
    sequence[].formationProvisions {task, responses[], quota?, releaseCriterion, mentorRequired};
  - the "CLOs: ..." and "Formation (...): ..." clauses are removed from step notes (now typed data);
  - emstRelease is set to the release the pathways are drafted for; the staged copies are removed (one source).
credentials: re-codes the policy-mandated register rows to employer-mandated (issuer and verification kept; legalBasis
  names the policy) and adds the module gate records the wave-1 briefs list that the register lacked; DB links the
  wildlife capture and immobilization tasks to the new gate records.
"""
import csv
import re
import sys
from collections import OrderedDict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import s2b_lib as S  # noqa: E402
L = S.L

STAGING = S.REPO / "docs" / "build" / "WP-07" / "staging" / "pathways"
PROVISIONS = S.REPO / "docs" / "build" / "WP-07" / "formation_provisions.csv"
OUT = S.DATA / "core" / "pathways"
GEN = HERE / "generated"
EMST_RELEASE = "2.0.0-rc.1"
CLO_RX = re.compile(r"\s*CLOs:\s*((seed:[A-Za-z0-9._/-]+?@L\d)(,\s*)?)+\.?")
CLO_ITEM = re.compile(r"(seed:[A-Za-z0-9._/-]+?)@(L\d)")
FORM_RX = re.compile(r"\s*Formation \([^)]*\):\s*seed:[A-Za-z0-9._/-]+:\s*[^.]*\.")


def _generic(cid, level, recs):
    p, c = recs(cid)
    for lv in (c or {}).get("levels") or []:
        if lv["level"] == level:
            return list(lv["indicators"])
    return None


_cache = {}


def _load(rid):
    if rid not in _cache:
        _cache[rid] = S.load(rid)
    return _cache[rid]


def _quota(text):
    text = text.strip()
    special = {"10 shadowed then 5 observed inspections": (15, "inspections: 10 shadowed, then 5 observed")}
    if text in special:
        c, u = special[text]
        return {"count": c, "unit": u}
    m = re.match(r"^(\d+)\s+(.*)$", text)
    if m:
        return {"count": int(m.group(1)), "unit": m.group(2)}
    m = re.search(r"\b(\d+)\b", text)
    if m:
        return {"count": int(m.group(1)), "unit": text}
    return None


def pathways():
    prov_rows = L.read_csv(PROVISIONS)
    by_step = {}
    for r in prov_rows:
        by_step.setdefault((r["pathway_id"], int(r["step"])), []).append(r)
    report = []
    OUT.mkdir(parents=True, exist_ok=True)
    for f in sorted(STAGING.glob("*.yaml")):
        pw = L.load_yaml(f)
        all_clos = OrderedDict()
        kept_specific, dropped_variants = [], []
        for st in pw.get("sequence") or []:
            outs = st.pop("outcomes", []) or []
            groups = OrderedDict()
            for o in outs:
                _, ind = _load(o)
                groups.setdefault((ind["competency"], ind["level"]), []).append(o)
            clos, specific = [], []
            note_clos = [(c, l) for c, l in CLO_ITEM.findall(CLO_RX.search((st.get("note") or {}).get("en", "")).group(0))] \
                if CLO_RX.search((st.get("note") or {}).get("en", "")) else []
            for (cid, lvl) in note_clos:          # WP-07 named the CLOs in the step note: they are authoritative
                clos.append({"competency": cid, "level": lvl})
                all_clos[(cid, lvl)] = True
            named = set(note_clos)
            for (cid, lvl), ids in groups.items():
                gen = _generic(cid, lvl, _load) or []
                if (cid, lvl) in named:
                    dropped_variants += [i for i in ids if i not in gen]
                elif set(gen) <= set(ids):
                    clos.append({"competency": cid, "level": lvl})
                    all_clos[(cid, lvl)] = True
                    dropped_variants += [i for i in ids if i not in gen]
                else:
                    specific += ids
            new = {}
            for k in ("step", "tasks"):
                if k in st:
                    new[k] = st[k]
            if specific:
                new["outcomes"] = specific
                kept_specific += specific
            if clos:
                new["cloOutcomes"] = clos
            provs = []
            for r in by_step.get((pw["id"], st["step"]), []):
                if r["task_id"] not in (st.get("tasks") or []):
                    raise SystemExit(f"{pw['id']} step {st['step']}: provision task {r['task_id']} not in step tasks")
                resp = [x for x in r["response"].split("+") if x]
                item = {"task": r["task_id"], "responses": resp}
                q = _quota(r["quota"])
                if q:
                    item["quota"] = q
                elif {"by-hand-quota", "supervised-repetitions"} & set(resp):
                    item["quota"] = {"count": 1, "unit": r["quota"]}
                item["releaseCriterion"] = r["release_criterion"]
                item["mentorRequired"] = r["mentor_required"].strip().lower() == "yes"
                provs.append(item)
            if provs:
                new["formationProvisions"] = provs
            for k in ("roleLevel",):
                if k in st:
                    new[k] = st[k]
            note = (st.get("note") or {}).get("en", "")
            note = FORM_RX.sub("", CLO_RX.sub("", note)).strip()
            if note:
                new["note"] = {"en": note}
            st.clear()
            st.update(new)
        # pathway-level outcomes -> cloOutcomes (union of steps)
        pw.pop("outcomes", None)
        rec = {}
        for k, v in pw.items():
            if k == "assessmentPlan":
                rec["emstRelease"] = EMST_RELEASE
                rec["cloOutcomes"] = [{"competency": c, "level": l} for (c, l) in all_clos]
            rec[k] = v
        if "cloOutcomes" not in rec:
            rec["cloOutcomes"] = [{"competency": c, "level": l} for (c, l) in all_clos]
            rec["emstRelease"] = EMST_RELEASE
        en = rec["editorialNote"]["en"]
        en = en.replace(" Staged outside data/v2 until the role records resolve (CR-LC-001).", "")
        tag = (" Moved into data/v2 in S2 (CR-LC-001 #1-#3): outcomes are named as CLOs {competency, level} (generic CLO = "
               "levels[].indicators; enactment anchors are reached through the enactment CLO, never listed here, CR-LC-001 #4); "
               "formation provisions are typed (formationProvisions), and docs/build/WP-07/formation_provisions.csv stays "
               "WP-07's audit copy; role references are planned targets until WP-08 writes the records.")
        if tag.strip() not in en:
            en = en + tag
        rec["editorialNote"] = {"en": en}
        ag = rec["provenance"].setdefault("agent", [])
        if S.AG["LC"] not in ag:
            ag.append(S.AG["LC"])
        dest = OUT / f.name
        L.write_yaml(dest, dict(rec))
        S.log(rec["id"], "Pathway", dest, "move-from-staging", "37")
        f.unlink()
        report.append({"pathway": rec["id"], "steps": len(rec["sequence"]), "clo_outcomes": len(rec["cloOutcomes"]),
                       "provisions": sum(len(s.get("formationProvisions") or []) for s in rec["sequence"]),
                       "specific_outcomes_kept": len([x for x in kept_specific]),
                       "enactment_variants_dropped": len(set(dropped_variants))})
    GEN.mkdir(exist_ok=True)
    (GEN / "pathway_moves.csv").write_text(L.csv_text(list(report[0].keys()), report), encoding="utf-8")
    try:
        STAGING.rmdir()
    except OSError:
        pass
    print(f"{len(report)} pathways moved; provisions {sum(r['provisions'] for r in report)}")


RECODE = {
    "seed:crd-wildland-fire-position-qualification": (
        "Interagency and agency policy for incident and prescribed-fire assignments (position qualification standards); not statute or regulation",
        [("NWCG is not a party to that alignment", "the alignment is between USWFS and USFS standards"),
         ("Gate type: required by agency and interagency policy for incident and prescribed-fire assignments, not by statute or regulation, so closureType is ''voluntary'' under the vocabulary''s definition (CR-LC-001 proposes an employer-or-policy-mandated value).",
          "Gate type: required by agency and interagency policy for incident and prescribed-fire assignments, not by statute or regulation: closureType employer-mandated (CR-LC-001 #5, ADR-0030)."),
         ("Gate type: required by agency and interagency policy for incident and prescribed-fire assignments, not by statute or regulation, so closureType is 'voluntary' under the vocabulary's definition (CR-LC-001 proposes an employer-or-policy-mandated value).",
          "Gate type: required by agency and interagency policy for incident and prescribed-fire assignments, not by statute or regulation: closureType employer-mandated (CR-LC-001 #5, ADR-0030).")]),
    "seed:crd-contracting-officers-representative": (
        "Federal acquisition workforce policy for designated contracting officer's representatives; not statute or regulation",
        [("(policy, not regulation; closureType per vocabulary definition)", "(policy, not regulation; closureType employer-mandated, CR-LC-001 #5)")]),
    "seed:crd-nims-ics-training": (
        "Agency and jurisdiction policy for incident assignments; adopting the national incident management framework is a condition of federal preparedness grants (verify current status)",
        []),
    "seed:crd-state-inspector-credential": (
        "State agency policy delegating inspection authority (per state; where a state sets the credential by regulation, that state's record is regulation-mandated-training)",
        [("closureType is the conservative default until each state''s basis is recorded.", "closureType employer-mandated (agency policy; CR-LC-001 #5) until each state's basis is recorded."),
         ("closureType is the conservative default until each state's basis is recorded.", "closureType employer-mandated (agency policy; CR-LC-001 #5) until each state's basis is recorded.")]),
}

NEW_GATES = [
    {"id": "seed:crd-scientific-collection-permit", "prefLabel": {"en": "Scientific collection permit for capturing, handling and marking wildlife and fish"},
     "credentialType": "licence", "issuer": "State fish and wildlife agencies; federal wildlife agencies for protected and migratory species",
     "issuingJurisdiction": "Each US state; United States (federal)",
     "legalBasis": "State wildlife codes and federal wildlife statutes restrict capture, possession and marking of wildlife to permit holders",
     "scopeOfPractice": {"en": "Capture, handling, marking, sampling and release of wild animals for research, survey and management under permit conditions"},
     "closureType": "legal-licensure", "renewal": "Annual or project-term permits (renewal cycle not verified)",
     "note": "Added by LC in S2 (CR-DB-001 #7): MOD-12 wildlife brief lists scientific collection permits as a gate. Usually issued to a project or principal investigator with named sub-permittees; animal-care protocol approval is an institutional approval, not a person credential, and is not a register record."},
    {"id": "seed:crd-controlled-substance-registration-wildlife-immobilization", "prefLabel": {"en": "Controlled-substance registration or authorization for chemical immobilization of wildlife"},
     "credentialType": "licence", "issuer": "Federal drug control authority registration, held by an agency or veterinarian, with agency authorization for named staff",
     "issuingJurisdiction": "United States (federal); state controlled-substance authorities where applicable",
     "legalBasis": "Federal and state controlled-substance law restricts possession and use of immobilization drugs to registrants and authorized users",
     "scopeOfPractice": {"en": "Possession, dosing and record-keeping of controlled immobilization drugs under a registrant's authority"},
     "closureType": "legal-licensure", "renewal": "Registration renewal by registrant (cycle not verified)",
     "note": "Added by LC in S2 (CR-DB-001 #7): MOD-12 wildlife brief lists controlled-drug authorization for immobilization as a gate. Staff usually act under an agency or veterinary registration, so the gate on a person is the authorization, recorded per agency."},
    {"id": "seed:crd-law-enforcement-commission-ranger", "prefLabel": {"en": "Law enforcement commission for protection rangers and conservation officers"},
     "credentialType": "position-qualification", "issuer": "The employing land-management or wildlife agency, after agency-required law enforcement training",
     "issuingJurisdiction": "Each employing agency (federal, state or local)",
     "legalBasis": "Agency law enforcement authority granted by statute and exercised only by commissioned officers under agency policy (per agency; verify)",
     "scopeOfPractice": {"en": "Exercise of law enforcement authority in parks, protected areas and wildlife management areas"},
     "closureType": "legal-licensure", "renewal": "Annual in-service training and qualification (cycle not verified)",
     "note": "Added by LC in S2 (CR-DB-001 #7): MOD-15 parks brief lists the commission as a role-variant gate, never a proficiency level. Closure type recorded as legal-licensure because only commissioned officers may exercise the authority; confirm per agency (WP-15)."},
]


def _cred(g):
    return {"id": g["id"], "type": "Credential", "prefLabel": g["prefLabel"], "credentialType": g["credentialType"],
            "issuer": g["issuer"], "issuingJurisdiction": g["issuingJurisdiction"], "legalBasis": g["legalBasis"],
            "scopeOfPractice": g["scopeOfPractice"], "closureType": g["closureType"], "renewal": g["renewal"],
            "issuerVerified": {"verified": False}, "layer": "L6", "module": "core", "status": "draft",
            "validationStatus": "draft", "license": "CC0-1.0", "sensitivity": "public",
            "editorialNote": {"en": g["note"] + " Issuer not verified: keep issuerVerified false until checked (ADR-0022 §3). A credential is a gate on tasks and role variants, never a proficiency level (ADR-0003 T-8)."},
            "provenance": S.prov(["LC"], adr=["ADR-0022", "ADR-0003", "ADR-0030"])}


def credentials():
    rows = []
    for cid, (basis, repl) in RECODE.items():
        def fn(r, basis=basis, repl=repl):
            r["closureType"] = "employer-mandated"
            r["legalBasis"] = basis
            en = (r.get("editorialNote") or {}).get("en", "")
            for a, b in repl:
                en = en.replace(a, b)
            r["editorialNote"] = {"en": en}
        S.patch(cid, fn, "LC", "38", "Re-coded employer-mandated in S2 (CR-LC-001 #5); issuer and verification status unchanged; legalBasis names the policy.")
        rows.append({"credential": cid, "action": "recode employer-mandated"})
    for g in NEW_GATES:
        p = S.DATA / "registers" / "credentials" / (L.id_to_stem(g["id"]) + ".yaml")
        if p.exists() and not S._owned(L.load_yaml(p)):
            raise SystemExit(f"{g['id']} exists and is not mine")
        L.write_yaml(p, _cred(g))
        S.log(g["id"], "Credential", p, "new", "38")
        rows.append({"credential": g["id"], "action": "new module gate record"})

    # DB links the wildlife capture and immobilization tasks to the new gates (credentialGates)
    def gate(*pairs):
        def fn(r):
            gl = r.setdefault("credentialGates", [])
            have = {x["credential"] for x in gl}
            for c, k in pairs:
                if c not in have:
                    gl.append({"credential": c, "kind": k})
        return fn
    S.patch("seed:FC-C15-T1", gate(("seed:crd-scientific-collection-permit", "required")), "DB", "38",
            "S2 (CR-DB-001 #7): credential gate to the new scientific collection permit record.")
    S.patch("seed:FC-C15-T3", gate(("seed:crd-scientific-collection-permit", "required")), "DB", "38",
            "S2 (CR-DB-001 #7): credential gate to the new scientific collection permit record.")
    S.patch("seed:FC-C15-T2", gate(("seed:crd-controlled-substance-registration-wildlife-immobilization", "required")), "DB", "38",
            "S2 (CR-DB-001 #7): credential gate to the new controlled-substance authorization record.")
    S.patch("seed:DB-C56-T2", gate(("seed:crd-scientific-collection-permit", "preferred")), "DB", "38", None)
    rows += [{"credential": "seed:crd-scientific-collection-permit", "action": "gate on FC-C15-T1, FC-C15-T3 (required), DB-C56-T2 (preferred)"},
             {"credential": "seed:crd-controlled-substance-registration-wildlife-immobilization", "action": "gate on FC-C15-T2 (required)"},
             {"credential": "seed:crd-law-enforcement-commission-ranger", "action": "role-variant gate; WP-08 links it (no task gate)"}]
    GEN.mkdir(exist_ok=True)
    (GEN / "credential_moves.csv").write_text(L.csv_text(["credential", "action"], rows), encoding="utf-8")
    print(f"{len(RECODE)} re-coded, {len(NEW_GATES)} new gate records")


if __name__ == "__main__":
    {"pathways": pathways, "credentials": credentials}[sys.argv[1]]()
