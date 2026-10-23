#!/usr/bin/env python3
"""Build the EMST credential register seed (L6; data/v2/registers/credentials/) from DB's Phase 2 register
(docs/research/domain-bench/credentials_register.csv), corrected by the V3 verification pass and LC's own checks.

Rules (ADR-0022 §3; ADR-0003 T-8):
- A credential is a gate, never proficiency. Each row records issuer, credential type, gate (closure) type and an
  issuer-verified flag with date and sources. Only rows whose issuer was confirmed by V3-07/V3-08 or an LC source read
  this session are `verified: true`; every other row stays `verified: false` until checked (P-DB-07, P-DB-16).
- Corrections applied: LEED AP / Green Associate and ISSP-SA/CSP are issued by GBCI; IEMA is now ISEP; water and
  wastewater operator certificates are issued by state programmes, with exams often from Water Professionals
  International (formerly ABC) (V3-07, V3-08, LC-101; ADR-0027 corrected facts).
- Tribal-related rows are not authored here (ADR-0007 §D): DB-CR-005 is left for TN inside the hold.
- Organizational accreditations (DB-CR-089 laboratory accreditation) are not person credentials and are left out.

Usage: python3 docs/build/WP-07/scripts/build_wp07_credentials.py
"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "scripts"))
import emstlib as L  # noqa: E402

SRC = REPO / "docs" / "research" / "domain-bench" / "credentials_register.csv"
OUT = REPO / "data" / "v2" / "registers" / "credentials"
AGENT = "emstagent:lc-agent@wp-07"
GEN = "2026-10-23T14:15:00Z"
CHECKED = "2026-10-23"

SKIP = {"DB-CR-005": "Tribal-related; held for TN (ADR-0007 §D)", "DB-CR-089": "organizational accreditation, not a person credential"}

# V3-08 confirmed these issuers (identity and active programme); V3-07 confirmed the ABCEP CEP listing.
V308 = {"DB-CR-043", "DB-CR-022", "DB-CR-067", "DB-CR-009", "DB-CR-018", "DB-CR-073", "DB-CR-071", "DB-CR-080", "DB-CR-050", "DB-CR-040"}
V307 = {"DB-CR-041"}

MANDATED_TRAINING = {"DB-CR-024", "DB-CR-025", "DB-CR-026", "DB-CR-033", "DB-CR-053"}
# closureType follows vocab/authority_positions.yaml#closure_types as defined: "regulation-mandated-training" only where a
# regulation requires the credential for the act; employer or interagency-policy requirements are "voluntary" by that
# definition (CR-LC-001 asks the CA for an employer-or-policy-mandated value).
REG_MANDATED_QUAL = {"DB-CR-012", "DB-CR-019", "DB-CR-032", "DB-CR-078", "DB-CR-085"}

OVERRIDE = {
    "DB-CR-001": dict(key="seed:crd-drinking-water-treatment-operator",
                      issuer="State drinking water operator certification programme (exams often from Water Professionals International, formerly ABC)",
                      issuingJurisdiction="Each US state's certification programme", credentialType="licence", closureType="legal-licensure",
                      legalBasis="State law under federal operator certification guidelines for public water systems",
                      verified=(True, ["V3-08", "LC-101"]),
                      note="Grade follows plant classification; the operator in responsible charge must hold the grade. WPI supplies standardized exams many states use; the state issues the certificate."),
    "DB-CR-002": dict(key="seed:crd-water-distribution-operator",
                      issuer="State drinking water operator certification programme (exams often from Water Professionals International, formerly ABC)",
                      issuingJurisdiction="Each US state's certification programme", credentialType="licence", closureType="legal-licensure",
                      legalBasis="State law under federal operator certification guidelines for public water systems", verified=(True, ["V3-08", "LC-101"])),
    "DB-CR-003": dict(key="seed:crd-wastewater-treatment-operator",
                      issuer="State wastewater operator certification programme (exams often from Water Professionals International, formerly ABC)",
                      issuingJurisdiction="Each US state's certification programme", credentialType="licence", closureType="legal-licensure",
                      verified=(True, ["V3-08", "LC-101"])),
    "DB-CR-004": dict(key="seed:crd-wastewater-collection-operator",
                      issuer="State wastewater operator certification programme (exams often from Water Professionals International, formerly ABC)",
                      issuingJurisdiction="Each US state's certification programme", credentialType="licence", closureType="legal-licensure",
                      verified=(True, ["V3-08", "LC-101"])),
    "DB-CR-007": dict(key="seed:crd-professional-engineer", issuer="State engineering licensing boards (examinations by NCEES)",
                      issuingJurisdiction="Each US state and territory", credentialType="licence", closureType="legal-licensure"),
    "DB-CR-024": dict(key="seed:crd-hazwoper", derivedFrom=[
                          {"v1Key": "v1:4.4.4", "relation": "split-from", "note": "Credential part of v1 4.4.4 (training-level indicators foundational I1, intermediate I1 and I9, advanced I1); planned key in data/v2/migration/v1_targets.csv"}], issuer="Employer or training provider (training required by the federal occupational safety standard for hazardous waste operations and emergency response)",
                      credentialType="mandated-training-record", closureType="regulation-mandated-training", verified=(False, ["LC-106", "LC-039"]),
                      note="A training record, not an independent certification; v1 4.4.4 rows mixed site-worker training hours with emergency-response levels (LC Phase 2)."),
    "DB-CR-057": dict(key="seed:crd-leed-ap", name="LEED AP (with specialty) and LEED Green Associate",
                      issuer="Green Business Certification Inc. (GBCI); the LEED rating system is owned by USGBC",
                      verified=(True, ["V3-08"]),
                      note="Corrected issuer (V3-08): GBCI has administered the LEED AP credential since 2008. Standard-bound credential: the LEED rating system itself belongs in the L4 tools and standards layer."),
    "DB-CR-060": dict(key="seed:crd-issp-csp", name="ISSP Sustainability Associate (ISSP-SA) and ISSP Certified Sustainability Professional (ISSP-CSP)",
                      issuer="Green Business Certification Inc. (GBCI); credentials originally developed by ISSP",
                      verified=(True, ["V3-07", "V3-08"]),
                      note="Corrected issuer (V3-07, V3-08): GBCI has offered ISSP-SA and ISSP-CSP since December 2019; no current independent ISSP activity was found. Do not cite ISSP as an active independent issuer."),
    "DB-CR-064": dict(key="seed:crd-isep-membership", name="ISEP membership grades (Graduate, Associate, Practitioner, Full, Fellow)",
                      issuer="Institute of Sustainability and Environmental Professionals (ISEP; formerly IEMA)", issuingJurisdiction="United Kingdom (international membership)",
                      verified=(True, ["V3-07", "LC-102"]),
                      note="IEMA rebranded as ISEP by July 2025 (V3-07); never use IEMA as the current name. Post-nominals reported as GradISEP, AISEP, PISEP and FISEP (LC-102; a secondary source naming six of seven grades); the Full grade's post-nominal and the competency basis of each grade were not confirmed on an ISEP page. Chartered Environmentalist is recorded separately."),
    "DB-CR-081": dict(key="seed:crd-wildland-fire-position-qualification", name="Wildland fire position qualifications under the interagency standard (e.g., firefighter, burn boss, incident commander types)",
                      issuer="The employing agency's certifying official, under the interagency wildland fire position qualification standard",
                      credentialType="position-qualification", closureType="voluntary",
                      verified=(True, ["V3-13", "LC-103", "LC-104"]),
                      note="Each qualification is certified by the employing agency after task-book evaluation, not issued by the standards body (LC-104). The standard is revised annually and was updated in January 2026, changing some position names; USWFS-USFS aligned federal qualification standards take effect January 2027 (NWCG is not a party to that alignment) (V3-13, LC-103). Gate type: required by agency and interagency policy for incident and prescribed-fire assignments, not by statute or regulation, so closureType is 'voluntary' under the vocabulary's definition (CR-LC-001 proposes an employer-or-policy-mandated value). Holding a qualification is a gate, not a proficiency level (ADR-0004 §8)."),
    "DB-CR-091": dict(key="seed:crd-remote-pilot-certificate", issuer="Federal Aviation Administration", issuingJurisdiction="United States",
                      credentialType="licence", closureType="legal-licensure", verified=(False, ["LC-105", "LC-040"])),
    "DB-CR-043": dict(key="seed:crd-rehs-rs"),
    "DB-CR-071": dict(key="seed:crd-saf-certified-forester"),
    "DB-CR-073": dict(key="seed:crd-certified-wildlife-biologist"),
    "DB-CR-018": dict(key="seed:crd-professional-wetland-scientist"),
    "DB-CR-067": dict(key="seed:crd-certified-floodplain-manager"),
    "DB-CR-080": dict(key="seed:crd-cerp"),
    "DB-CR-090": dict(key="seed:crd-gisp"),
    "DB-CR-082": dict(key="seed:crd-state-prescribed-burn-manager"),
    "DB-CR-036": dict(key="seed:crd-pesticide-applicator"),
    "DB-CR-068": dict(key="seed:crd-nims-ics-training"),
    "DB-CR-092": dict(key="seed:crd-wilderness-first-aid"),
}

EXTRA = [
    dict(key="seed:crd-chartered-environmentalist", name="Chartered Environmentalist (CEnv)",
         issuer="Society for the Environment, through licensed professional bodies (ISEP among them)", issuingJurisdiction="United Kingdom",
         credentialType="certification", closureType="voluntary", subsectors="M01|P06|X01", verified=(False, []),
         note="Split from DB-CR-064. Licensing arrangement between ISEP and the Society for the Environment not checked this session."),
    dict(key="seed:crd-contracting-officers-representative", name="Federal contracting officer's representative certification (FAC-COR)",
         issuer="Federal acquisition workforce certification programme administered through the employing agency", issuingJurisdiction="United States (federal)",
         credentialType="certification", closureType="voluntary", subsectors="", verified=(False, []),
         note="Required by federal acquisition policy for designated representatives (policy, not regulation; closureType per vocabulary definition). Gate for the federal technical-representative enactment of PS-C01 (seed:lc-ena-txf-scope-federal-technical-rep). Current programme name, levels and issuer not verified this session (WP-15 check)."),
    dict(key="seed:crd-state-inspector-credential", name="State environmental inspector credential (programme-issued delegation to inspect)",
         issuer="The state programme that delegates inspection authority (varies by state and programme)", issuingJurisdiction="Each US state programme",
         credentialType="position-qualification", closureType="voluntary", subsectors="", verified=(False, []),
         note="Legal basis varies by state; closureType is the conservative default until each state's basis is recorded. Generic placeholder for state-issued inspector credentials used by the regulatory-inspector enactment of IO-C01; each state's programme name, basis and renewal must be recorded per state (SL lane, X5)."),
]

TYPE_MAP = {"license": "licence", "certification": "certification", "certificate": "certificate", "qualification": "position-qualification"}


def slug(name):
    s = re.sub(r"\(.*?\)", "", name)
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:48].rstrip("-")


def record(row, o):
    name = o.get("name") or row["name"]
    ctype = o.get("credentialType") or ("mandated-training-record" if row["credential_id"] in MANDATED_TRAINING else TYPE_MAP[row["type"]])
    if o.get("closureType"):
        closure = o["closureType"]
    elif ctype == "licence":
        closure = "legal-licensure"
    elif ctype == "mandated-training-record" or row["credential_id"] in REG_MANDATED_QUAL:
        closure = "regulation-mandated-training"
    else:
        closure = "voluntary"
    cid = row["credential_id"]
    verified, vsrc = o.get("verified", (cid in V308 or cid in V307, ["V3-08"] if cid in V308 else (["V3-07"] if cid in V307 else [])))
    key = o.get("key") or "seed:crd-" + slug(name)
    rec = {"id": key, "type": "Credential", "prefLabel": {"en": name}}
    rec["notation"] = [{"scheme": "DB-credentials-register", "value": cid}]
    rec["credentialType"] = ctype
    rec["issuer"] = o.get("issuer") or row["issuer"]
    if o.get("issuingJurisdiction"):
        rec["issuingJurisdiction"] = o["issuingJurisdiction"]
    legal = o.get("legalBasis") or row.get("required_by")
    if legal:
        rec["legalBasis"] = legal
    if row.get("competency_areas"):
        rec["scopeOfPractice"] = {"en": row["competency_areas"]}
    rec["closureType"] = closure
    if row.get("renewal"):
        rec["renewal"] = row["renewal"] + " (renewal cycle not verified)"
    iv = {"verified": bool(verified)}
    if verified:
        iv["date"] = CHECKED
    if vsrc:
        iv["sources"] = vsrc
    rec["issuerVerified"] = iv
    rec.update({"layer": "L6", "module": "core", "status": "draft", "validationStatus": "draft", "license": "CC0-1.0", "sensitivity": "public"})
    notes = [f"Seeded from DB Phase 2 register row {cid} (subsectors {row['subsector'] or 'n/a'})."]
    if o.get("note"):
        notes.append(o["note"])
    notes.append("Issuer verified by V3/LC sources." if verified else "Issuer not verified: keep issuerVerified false until checked (ADR-0022 §3).")
    notes.append("A credential is a gate on tasks and role variants, never a proficiency level (ADR-0003 T-8).")
    rec["editorialNote"] = {"en": " ".join(notes)}
    srcs = sorted(set([s for s in row["source_ids"].split("|") if s] + list(vsrc)))
    rec["provenance"] = {"method": "llm-assisted", "agent": [AGENT], "generatedAt": GEN, "toolVersion": "claude-opus-5-5",
                         "promptVersion": "wp07-credentials@1"}
    if o.get("derivedFrom"):
        rec["provenance"]["derivedFrom"] = o["derivedFrom"]
    if srcs:
        rec["provenance"]["sources"] = srcs
    rec["provenance"].update({"evidenceLabel": "E" if srcs else "J", "reviewStatus": "unreviewed",
                              "adr": ["ADR-0022", "ADR-0003", "ADR-0027"] + (["ADR-0011"] if o.get("derivedFrom") else [])})
    return rec


def main():
    rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
    out = []
    for row in rows:
        if row["credential_id"] in SKIP:
            continue
        out.append(record(row, OVERRIDE.get(row["credential_id"], {})))
    for e in EXTRA:
        row = {"credential_id": "none", "name": e["name"], "issuer": e["issuer"], "subsector": e["subsectors"], "type": "",
               "required_by": "", "renewal": "", "competency_areas": "", "source_ids": ""}
        rec = record(row, dict(e, credentialType=e["credentialType"]))
        rec.pop("notation")
        rec["editorialNote"]["en"] = rec["editorialNote"]["en"].replace("Seeded from DB Phase 2 register row none (subsectors n/a). ", "Added by LC (WP-07). ")
        out.append(rec)
    keys = [r["id"] for r in out]
    dup = {k for k in keys if keys.count(k) > 1}
    if dup:
        raise SystemExit(f"duplicate keys: {dup}")
    for rec in out:
        L.write_yaml(OUT / f"{L.id_to_stem(rec['id'])}.yaml", rec)
    nv = sum(1 for r in out if r["issuerVerified"]["verified"])
    print(f"wrote {len(out)} credential records ({nv} issuer-verified, {len(out) - nv} unverified); skipped {sorted(SKIP)}")


if __name__ == "__main__":
    main()
