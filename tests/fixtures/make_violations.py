"""Generator for tests/fixtures/violations/<case>/ overlays (applied on top of tests/fixtures/trees/base)."""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import emstlib as L  # noqa: E402

FX = L.ROOT / "tests" / "fixtures"
BASE = FX / "trees" / "base" / "data" / "v2"
VD = FX / "violations"
VALID = {p.stem: L.load_yaml(p) for p in (FX / "records" / "valid").glob("*.yaml")}
REG_HEADER = "id,type,namespace,minted_on,minted_by,status,superseded_by,first_release\n"
base_reg = (BASE / "ids" / "registry.csv").read_text(encoding="utf-8")
base_rows = base_reg.splitlines()[1:]
cmp_file = next((BASE / "core" / "competencies").glob("CMP-*.yaml"))
CMP = L.load_yaml(cmp_file)
TSK = L.load_yaml(next((BASE / "core" / "tasks").glob("TSK-*.yaml")))


def mid(ns, prefix, body):
    return f"emst:{ns}/{prefix}-{body}{L.luhn32_check(body)}"


def rec(t, **kw):
    r = copy.deepcopy(VALID[t])
    r.update(kw)
    return r


def task(rid, text, **kw):
    return rec("Task", id=rid, prefLabel={"en": text}, statement={"en": text}, textSha256=L.text_sha256(text), **kw)


HELD = {"indigenousDataFlag": True, "approvalStatus": "pending-tribal-review", "sensitivity": "restricted-governed"}
CASES = {}


def case(name, desc, expect, files, registry_base=False, check_x1=False, strict=False):
    CASES[name] = (desc, expect, files, registry_base, check_x1, strict)


case("registry-deleted-row", "a minted ID row was removed from the append-only registry",
     ["E-REGISTRY-APPEND-ONLY", "E-REGISTRY-MISSING"], {"ids/registry.csv": REG_HEADER + "\n".join(base_rows[1:]) + "\n"}, registry_base=True)
case("registry-edited-row", "an immutable registry column (minted_by) was edited",
     ["E-REGISTRY-APPEND-ONLY"], {"ids/registry.csv": REG_HEADER + "\n".join([base_rows[0].replace("emstagent:fixture@1", "pid:someone-else")] + base_rows[1:]) + "\n"}, registry_base=True)
case("registry-bad-transition", "registry status moved candidate -> superseded (not allowed)",
     ["E-REGISTRY-TRANSITION"], {"ids/registry.csv": REG_HEADER + "\n".join([base_rows[0].replace(",candidate,", ",superseded,")] + base_rows[1:]) + "\n"}, registry_base=True)
case("registry-bad-check-symbol", "a registry row whose check symbol is wrong",
     ["E-REGISTRY-FORMAT"], {"ids/registry.csv": base_reg + "emst:core/CMP-AB12CDZ,Competency,core,2026-10-23,emstagent:fixture@1,candidate,,\n"})
case("module-redefines-core", "a module file redefines the core competency's ID",
     ["E-MODULE-REDEFINES-CORE"], {f"modules/water/competencies/{cmp_file.name}": dict(CMP, module="water", homeModule="water", subsectors=["W01"])})
mod_core_id = mid("core", "CMP", "WW11WW")
case("module-mints-core-namespace", "a module record carries an ID minted in the core namespace",
     ["E-MODULE-REDEFINES-CORE"], {f"modules/water/competencies/{L.id_to_stem(mod_core_id)}.yaml":
                                    rec("Competency", id=mod_core_id, status="candidate", module="water", homeModule="water", subsectors=["W01"]),
                                    "ids/registry.csv": base_reg + f"{mod_core_id},Competency,core,2026-10-23,emstagent:fixture@1,candidate,,\n"})
case("tribal-held-key-unflagged", "a record using a held key (TN-C02) without the hold flags",
     ["E-TRIBAL-HOLD"], {"core/competencies/seed-TN-C02.yaml": rec("Competency", id="seed:TN-C02")})
leak_id = mid("core", "TSK", "TT22TT")
leak_text = "Conduct government-to-government consultation with Tribal nations before approving a permit"
case("tribal-leak-candidate", "a candidate task with Tribal-related text and no hold flags",
     ["E-TRIBAL-LEAK"], {f"core/tasks/{L.id_to_stem(leak_id)}.yaml": task(leak_id, leak_text, status="candidate", supports=[{"competency": CMP["id"], "strength": "primary"}]),
                         "ids/registry.csv": base_reg + f"{leak_id},Task,core,2026-10-23,emstagent:fixture@1,candidate,,\n"})
case("tribal-inherit", "an unflagged task supports a held competency",
     ["E-TRIBAL-INHERIT"], {"core/competencies/seed-fx-held.yaml": rec("Competency", id="seed:fx-held", **HELD),
                            "core/tasks/seed-fx-inherit.yaml": task("seed:fx-inherit", "Prepare a records request log for a programme office each quarter",
                                                                   supports=[{"competency": "seed:fx-held", "strength": "primary"}])})
case("tribal-coords-cultural", "coordinates next to cultural-site vocabulary",
     ["E-COORDS-CULTURAL"], {"core/competencies/seed-fx-coords.yaml": rec("Competency", id="seed:fx-coords",
                             scopeNote={"en": "Field notes: burial site observed at 45.12345, -110.54321 near the trail."})})
case("confidential-marker", "a file holding information shared in confidence",
     ["E-CONFIDENTIAL"], {"notes/meeting.md": "Synthetic fixture. Material shared in confidence by a participant.\n"})
case("personal-data-text", "an e-mail address in a record and a phone number in a CSV register",
     ["E-PERSONAL-DATA"], {"core/competencies/seed-fx-pd.yaml": rec("Competency", id="seed:fx-pd", scopeNote={"en": "Contact jane.doe@example.org for details."}),
                           "registers/contacts.csv": "org,phone\nSynthetic Org,555-123-4567\n"})
pd = rec("ExposureAssessment", id="seed:fx-pd-asm", raterType="v1-analyst", raterId="v1-analyst-01", confidence="low",
         v1Flags=[], v1Values={"auto_type": "A", "raterName": "A. Person"})
pd.pop("technicalExposure")
case("personal-data-field", "a person-level field inside a rating's v1Values",
     ["E-PERSONAL-DATA"], {"assessments/fixture/batch.jsonl": L.jsonl_line(dict(pd, task=TSK["id"], taskTextSha256=TSK["textSha256"])) + "\n"})
case("typing-lint", "an authored draft task naming an L4 product and an L5 instrument",
     ["E-LINT-TYPING"], {"core/tasks/seed-fx-typing.yaml": task("seed:fx-typing", "Prepare NEPA review maps in ArcGIS for the interdisciplinary team each week",
                                                               supports=[{"competency": CMP["id"], "strength": "primary"}])})
case("indicator-lint", "an authored indicator using a banned internal-state verb (B1)",
     ["E-LINT-INDICATOR"], {"core/indicators/seed-fx-lint.yaml": rec("Indicator", id="seed:fx-lint", competency=CMP["id"],
                            statement={"en": "Understands sampling theory and holding times."})})
comp = rec("Competency", id="seed:fx-computed")
comp["stabilityTier"] = "Stable"
cf = dict(pd, id="seed:fx-cf-asm", task=TSK["id"], taskTextSha256=TSK["textSha256"])
cf["v1Values"] = {"auto_type": "A", "reform_flag_count": 2}
case("computed-field", "stored summaries: stabilityTier on a competency, reform_flag_count inside v1Values",
     ["E-COMPUTED-FIELD"], {"core/competencies/seed-fx-computed.yaml": comp,
                            "assessments/fixture/batch.jsonl": L.jsonl_line(cf) + "\n"})
case("dependency-direction", "a core task depends on a module competency",
     ["E-DEPENDENCY-DIRECTION"], {"core/tasks/seed-fx-dep.yaml": task("seed:fx-dep", "Record treatment process readings on the shift log at each scheduled interval",
                                                                    supports=[{"competency": "seed:fx-water-cmp", "strength": "primary"}])})
bad_hash = task("seed:fx-hash", "Calibrate a field meter against two standards before each sampling day",
                supports=[{"competency": CMP["id"], "strength": "primary"}])
bad_hash["textSha256"] = "0" * 64
case("text-hash", "a task whose textSha256 does not match its statement", ["E-TEXT-HASH"], {"core/tasks/seed-fx-hash.yaml": bad_hash})
llm = rec("CraftRating", id="seed:fx-llm", raterType="llm", raterId="emstagent:fx-rater@1", evidenceLabel="J",
          task=TSK["id"], taskTextSha256=TSK["textSha256"])
llm["provenance"] = dict(llm["provenance"], method="llm-assisted", toolVersion="model-x", promptVersion="p@1", evidenceLabel="J")
llmc = rec("Competency", id="seed:fx-llmc", validationStatus="panel-retained")
llmc["provenance"] = dict(llmc["provenance"], method="llm-assisted", toolVersion="model-x", promptVersion="p@1")
case("llm-draft", "agent output presented as reviewed: an llm rating labelled J and an llm competency claiming panel retention",
     ["E-LLM-DRAFT"], {"assessments/fixture/llm.jsonl": L.jsonl_line(llm) + "\n", "core/competencies/seed-fx-llmc.yaml": llmc})
case("dangling-ref", "a task supports a competency that does not exist",
     ["E-REF-DANGLING"], {"core/tasks/seed-fx-dangle.yaml": task("seed:fx-dangle", "Check sample labels against the field form before shipping the cooler",
                                                                supports=[{"competency": "seed:does-not-exist", "strength": "primary"}])})
lic = rec("Competency", id="seed:fx-lic")
lic["provenance"] = dict(lic["provenance"], method="v1-migration",
                         derivedFrom=[{"v1Key": "v1:4.1.1", "relation": "carried", "workbookSha256": "6085795e0ec06c001fa29244ff8eb64e9a677ad6c5d297319dc570b459ce9080"}])
case("license-v1", "v1 text carried into a record licensed CC0 while the dedication is pending", ["E-LICENSE-V1"],
     {"core/competencies/seed-fx-lic.yaml": lic})
pth = rec("Pathway", id="seed:fx-recommended", recommended=True)
case("pathway-recommended", "a pathway labelled recommended before the M-03 gate", ["E-PATHWAY-RECOMMENDED"],
     {"core/pathways/seed-fx-recommended.yaml": pth})
x1_head = "subject_id\tpredicate_id\tobject_id\tmapping_justification\tauthor_id\tmapping_date\tmapping_tool\tcomment\n"
x1_meta = L.dump_yaml({"mapping_set_id": "https://w3id.org/emst/crosswalks/emst-v1/emst-v1_to_v2", "mapping_set_version": "0.0.1",
                       "license": "https://creativecommons.org/publicdomain/zero/1.0/", "curie_map": {"EMSTv1": "https://w3id.org/emst/v1/"}})
case("x1-incomplete", "X1 lacks almost every v1 key and records a decision that contradicts v1_disposition.csv",
     ["E-X1-INCOMPLETE", "E-X1-DECISION"],
     {"crosswalks/emst-v1/emst-v1_to_v2.sssom.tsv": x1_head + "EMSTv1:1.1.1\temst:retiredWithoutReplacement\tsssom:NoTermFound\tsemapv:ManualMappingCuration\temstagent:fixture\t2026-10-23\tfixture\tdecision=retire; fixture\n",
      "crosswalks/emst-v1/emst-v1_to_v2.sssom.yml": x1_meta}, check_x1=True)
case("sssom-third-party-text", "a CC0 crosswalk to O*NET that copies upstream labels and lacks nothing else",
     ["E-SSSOM-THIRD-PARTY-TEXT"],
     {"crosswalks/onet/31.0.sssom.tsv": "subject_id\tpredicate_id\tobject_id\tobject_label\tmapping_justification\n" + f"{TSK['id']}\tskos:closeMatch\tONET:19-2041.00-T1\tCollect samples (upstream text)\tsemapv:ManualMappingCuration\n",
      "crosswalks/onet/31.0.sssom.yml": L.dump_yaml({"mapping_set_id": "https://w3id.org/emst/crosswalks/onet/31.0", "mapping_set_version": "0.0.1",
                                                     "license": "CC0-1.0", "curie_map": {"ONET": "https://w3id.org/emst/ext/onet/"}})})
case("sssom-format", "a mapping set without its metadata file and with a predicate outside the vocabulary",
     ["E-SSSOM-FORMAT", "E-SSSOM-VALUE"],
     {"crosswalks/esco/1.2.1.sssom.tsv": "subject_id\tpredicate_id\tobject_id\tmapping_justification\n" + f"{CMP['id']}\towl:sameAs\tESCO:abc\tsemapv:ManualMappingCuration\n"})

# ---- ADR-0029 rulings (2026-10-23)
seedc_id = mid("core", "CMP", "SC33SC")
case("seed-candidate", "v1 seed content promoted to candidate without rewriting (ADR-0029 §1.3)", ["E-SEED-CANDIDATE"],
     {f"core/competencies/{L.id_to_stem(seedc_id)}.yaml": rec("Competency", id=seedc_id, status="candidate", validationStatus="seed-v1"),
      "ids/registry.csv": base_reg + f"{seedc_id},Competency,core,2026-10-23,emstagent:fixture@1,candidate,,\n"})
nota_id = mid("core", "TSK", "NN44NN")
case("notation-interim", "a candidate task still carrying an interim EMST-* notation scheme (ADR-0029 §8.2)", ["E-NOTATION-INTERIM"],
     {f"core/tasks/{L.id_to_stem(nota_id)}.yaml": task(nota_id, "Record calibration results for each field meter in the shared log weekly",
                                                       status="candidate", supports=[{"competency": CMP["id"], "strength": "primary"}],
                                                       notation=[{"scheme": "EMST-impact", "value": "2"}]),
      "ids/registry.csv": base_reg + f"{nota_id},Task,core,2026-10-23,emstagent:fixture@1,candidate,,\n"})
sig = rec("ChangeSignal", id="seed:fx-sig-active", targetId=TSK["id"], signalStatus="active", signalFamily="postings-pds",
          independenceKey="not-a-listed-key")
case("independence-key-unlisted", "an active signal whose independence key is not in vocab/change_types.yaml", ["E-INDEPENDENCE-KEY-UNLISTED"],
     {"signals/fixture/batch.jsonl": L.jsonl_line(sig) + "\n"})
org = rec("ChangeSignal", id="seed:fx-sig-org", targetType="organization", targetId="opm-agency:IN00", tribalPrograms=True,
          indigenousDataFlag=True, approvalStatus="pending-tribal-review", sensitivity="restricted-governed")
case("org-target-tribal", "an organization-target signal about Tribal programmes (ADR-0007 V3)", ["E-ORG-TARGET-TRIBAL"],
     {"signals/fixture/org.jsonl": L.jsonl_line(org) + "\n"})
ld = rec("ExposureAssessment", id="seed:fx-asm-dist", task=TSK["id"], taskTextSha256=TSK["textSha256"],
         technicalExposure=[{"vector": VALID["ExposureAssessment"]["technicalExposure"][0]["vector"],
                             "levelDistribution": {"E0": 0.5, "E1": 0.2, "E2": 0.1}, "basis": "synthetic"}])
case("level-distribution", "an exposure level distribution that sums to 0.8 (ADR-0029 §9.2)", ["E-LEVEL-DISTRIBUTION"],
     {"assessments/fixture/dist.jsonl": L.jsonl_line(ld) + "\n"})
ev = rec("DriverEvent", id="seed:fx-evt-review", eventType="submitted-for-review", statusAfter="in-force")
case("review-event-status", "a submitted-for-review event that claims the instrument is in force", ["E-REVIEW-EVENT-STATUS"],
     {"events/fixture.jsonl": L.jsonl_line(ev) + "\n"})
pr2_id = mid("core", "IND", "PR22PR")
pr2 = L.load_yaml(next((BASE / "core" / "indicators").glob("IND-*.yaml")))
pr2.update(id=pr2_id, level="L2")
pr2.pop("distinguishingAttribute", None)
case("pr2-attribute", "a candidate indicator above the lowest indicated level without a distinguishing attribute", ["E-PR2-ATTRIBUTE"],
     {f"core/indicators/{L.id_to_stem(pr2_id)}.yaml": pr2,
      "ids/registry.csv": base_reg + f"{pr2_id},Indicator,core,2026-10-23,emstagent:fixture@1,candidate,,\n"})
case("waiver-signer", "a lint waiver signed by a software agent (ADR-0029 §5.5)", ["E-WAIVER-SIGNER"],
     {"governance/lint_waivers.csv": "record_id,rule_id,text_sha256,waiver_class,reviewer,second_reviewer,decided_on,rationale\n"
                                     f"{CMP['id']},B09,{'a' * 64},accepted-warning,emstagent:fixture@1,,2026-10-23,synthetic\n"})
sel_head = "record_id\tsubject_id\tpredicate_id\tobject_id\tmapping_justification\tauthor_id\tother\n"
case("sssom-selection-llm", "a selection-use crosswalk row still justified by LLM-based matching (CR-IA-002)", ["E-SSSOM-SELECTION-1_1"],
     {"crosswalks/opm-fixture/2026.sssom.tsv": sel_head + f"x:1\t{TSK['id']}\tskos:closeMatch\tOPMseries:0401\tsemapv:LLMBasedMatching\temstagent:fx@1\tuse=selection;review_status=candidate\n",
      "crosswalks/opm-fixture/2026.sssom.yml": L.dump_yaml({"mapping_set_id": "https://w3id.org/emst/crosswalks/opm-fixture/2026", "mapping_set_version": "0.0.1",
                                                           "license": "https://creativecommons.org/publicdomain/zero/1.0/", "curie_map": {"OPMseries": "https://w3id.org/emst/ext/opm/"}})})


def main():
    import shutil
    if VD.exists():
        shutil.rmtree(VD)
    for name, (desc, expect, files, registry_base, check_x1, strict) in CASES.items():
        d = VD / name
        for rel, content in files.items():
            p = d / "data" / "v2" / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content if isinstance(content, str) else L.dump_yaml(content), encoding="utf-8")
        (d / "expect.yaml").write_text(L.dump_yaml({"description": "Synthetic seeded violation: " + desc, "expect": expect,
                                                     "registryBase": registry_base, "checkX1": check_x1, "strict": strict}), encoding="utf-8")
    print(len(CASES), "violation cases")


if __name__ == "__main__":
    main()
