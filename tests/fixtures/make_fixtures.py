"""Generator for tests/fixtures (synthetic records; run once, output committed as static files)."""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import emstlib as L  # noqa: E402

FX = L.ROOT / "tests" / "fixtures"
TS = "2026-10-23T00:00:00Z"
PROV = {"method": "human-authoring", "agent": ["emstagent:fixture@1"], "generatedAt": TS, "evidenceLabel": "S",
        "reviewStatus": "unreviewed"}
NOTE = {"en": "Synthetic test fixture; not EMST content."}


def mid(ns, prefix, body):
    return f"emst:{ns}/{prefix}-{body}{L.luhn32_check(body)}"


def base(rid, typ, layer, label, **kw):
    r = {"id": rid, "type": typ, "prefLabel": {"en": label}, "layer": layer, "module": "core", "status": "draft",
         "license": "CC0-1.0", "sensitivity": "public"}
    r.update(kw)
    r["editorialNote"] = NOTE
    r["provenance"] = copy.deepcopy(PROV)
    return r


def l13(**kw):
    d = {"lifecycleState": "established", "useTier": "describe", "validationStatus": "draft"}
    d.update(kw)
    return d


def rating(**kw):
    # validationStatus is required on every rating (rc.1 fix pass, ADR-0032; review M2)
    d = {"validationStatus": "draft", "raterType": "analyst", "raterId": "pid:fx-rater-01", "assessedAt": "2026-10-23", "method": "fixture",
         "confidence": "med", "instrument": "emst-craft@0.1", "codebookVersion": "fixture", "evidenceLabel": "S", "sources": []}
    d.update(kw)
    return d


TASK_TEXT = "Collect water samples from a stream reach following the sampling plan and chain-of-custody procedure"
VALID = {
    "VocabularyTerm": base("seed:fx-voc", "VocabularyTerm", "L0", "Assess and sense", inScheme="work_functions",
                           notation=[{"scheme": "work_functions", "value": "WF-ASSESS"}], definition={"en": "Inventory and observe conditions."}),
    "Competency": base("seed:fx-cmp", "Competency", "L1", "Collect defensible environmental samples",
                       definition={"en": "Synthetic competency for tests."}, statement={"en": "Collect environmental samples so that results are defensible."},
                       competencyType="practice", levelSpan={"min": "L1", "max": "L3"}, levelSpanBasis="declared", homeModule="core", **l13()),
    "Indicator": base("seed:fx-ind", "Indicator", "L1", "Records chain of custody", competency="seed:fx-cmp", level="L1",
                      statement={"en": "Records chain-of-custody entries for each sample under a qualified sampler's direction so that every transfer is traceable."},
                      augmentationMode="unaided", assessmentMethods=["record-audit"], useClass="develop", obs4=None,
                      obs4Draft={"value": 3, "raterType": "llm", "raterId": "emstagent:fixture@1", "codedOn": "2026-10-23"},
                      jurisdictionVariable=False, **l13(useTier="develop")),
    "Enactment": base("seed:fx-ena", "Enactment", "L1", "State regulator enactment", competency="seed:fx-cmp", enactmentKind="actor",
                      actorType="state", authorityBasis={"en": "State delegated programme authority."}, principal={"en": "The public."},
                      accountabilityVenue={"en": "State administrative review."}, note={"en": "Synthetic enactment."}, **l13()),
    "Task": base("seed:fx-tsk", "Task", "L2", TASK_TEXT, statement={"en": TASK_TEXT}, textSha256=L.text_sha256(TASK_TEXT),
                 supports=[{"competency": "seed:fx-cmp", "strength": "primary"}], workFunction="WF-ASSESS",
                 fieldDependency="on-site-required", formationDependency="yes", homeModule="core", **l13()),
    "KnowledgeStatement": base("seed:fx-knw", "KnowledgeStatement", "L2", "Holding times", statement={"en": "Holding times limit how long a sample remains valid."},
                               lowestLevel="L1", supports=["seed:fx-cmp"], **l13()),
    "RoleProfile": base("seed:fx-rol", "RoleProfile", "L3", "Field monitoring technician", definition={"en": "Synthetic role."},
                        functionStatement={"en": "Collects field samples and observations to protocol."}, primaryWorkFunction="WF-ASSESS",
                        roleLevels=[{"key": "entry", "levelBand": ["L1", "L2"]}],
                        taskBundle=[{"task": "seed:fx-tsk", "importance": 5, "timeShare": 0.4, "critical": True, "neededAtEntry": True}],
                        competencyTargets=[{"competency": "seed:fx-cmp", "targetLevels": {"entry": "L1"}}], homeModule="core", **l13()),
    "RoleVariant": base("seed:fx-var", "RoleVariant", "L3", "Field monitoring technician (state)", definition={"en": "Synthetic variant."},
                        variantOf="seed:fx-rol", sectorActor="state", authorityPosition="regulator",
                        disclaimers=["Not a classification basis.", "Not a job analysis.", "Not for RIF or rating decisions."], **l13()),
    "JobFamily": base("seed:fx-fam", "JobFamily", "L3", "Monitoring", definition={"en": "Synthetic family."}, memberRule="family-by-function@1.0", **l13()),
    "Pathway": base("seed:fx-pth", "Pathway", "L3", "Entry pathway", definition={"en": "Synthetic pathway."}, fromVariant="seed:fx-var",
                    toVariant="seed:fx-var", pathwayType="new-hire", recommended=False, **l13(useTier="exploratory")),
    "Tool": base("seed:fx-tl", "Tool", "L4", "Field data capture app (category)", toolType="software-category", vendorNeutral=True,
                 servesTasks=["seed:fx-tsk"], lifecycleState="established"),
    "ExposureAssessment": base("seed:fx-asm-exp", "ExposureAssessment", "L5", "Exposure rating of seed:fx-tsk", task="seed:fx-tsk",
                               taskTextSha256=L.text_sha256(TASK_TEXT), technicalExposure=[{"vector": "sensing", "level": "E1"}],
                               deploymentMode="assisted", **rating(instrument="emst-exposure@2.0", codebookVersion="2.0")),
    "CraftRating": base("seed:fx-asm-crf", "CraftRating", "L5", "Craft rating of seed:fx-tsk", task="seed:fx-tsk",
                        taskTextSha256=L.text_sha256(TASK_TEXT), scale="ordinal-0-2", values={"FC": 2, "DC": 1, "SC": 0}, **rating()),
    "FunctionRating": base("seed:fx-asm-fun", "FunctionRating", "L5", "Function rating of seed:fx-tsk", task="seed:fx-tsk",
                           taskTextSha256=L.text_sha256(TASK_TEXT), workFunction="WF-ASSESS", **rating(instrument="emst-function@0.1")),
    "RelevanceRating": base("seed:fx-asm-rel", "RelevanceRating", "L5", "Relevance of seed:fx-cmp to seed:fx-rol", subject="seed:fx-cmp",
                            subjectTextSha256=L.competency_text_sha256("Collect defensible environmental samples", "Collect environmental samples so that results are defensible."),
                            object="seed:fx-rol", objectScheme="role-profile", relevance={"importance": 4}, **rating(instrument="emst-relevance@0.1")),
    "ChangeSignal": base("seed:fx-sig", "ChangeSignal", "L5", "Synthetic posting-demand signal", targetType="Task", targetId="seed:fx-tsk",
                         measure={"name": "posting share", "value": 0.1, "unit": "share", "ci95": [0.05, 0.15], "n": 100,
                                  "denominator": "synthetic postings"},
                         observedPeriod={"start": "2026-01-01", "end": "2026-06-30"}, geography="US", source="DE-022", sourceRelease="fixture",
                         corpus={"version": "fixture", "sha256": "0" * 64, "license": "CC0-1.0"}, method="fixture", toolVersion="fixture",
                         crosswalkPath=["fixture"], crosswalkMinMatchType="skos:closeMatch", direction="grow", directionConfidence="low",
                         drivers=["other"], steepCategory="economic", novelty="new", sourceGrade="D", corroboration=0, careFlag=False,
                         tribalPrograms=False, personalData=False, evidenceLabel="S", reviewStatus="unreviewed", reviewBy="2027-10-23",
                         signalStatus="watch", independenceKey="conservation-job-board", upstreamSource="DE-022",
                         processingChain=["coder:pid:fx-coder-01"], observationId="obs-000000000001"),
    "WatchItem": base("seed:fx-wat", "WatchItem", "L5", "Synthetic watch item", signals=["seed:fx-sig"], highPriority=True,
                      hypothesizedEntity={"type": "Competency", "label": {"en": "Hypothetical"}, "functionStatement": {"en": "Hypothetical function."}},
                      reviewBy="2027-10-23", outcome="open"),
    "Instrument": base("seed:fx-ins", "Instrument", "L5", "Synthetic statute", citation="Synthetic Act of 2026", instrumentType="statute",
                       jurisdiction="US-federal", mechanisms=["DM-02"]),
    "DriverEvent": base("seed:fx-evt", "DriverEvent", "L5", "Synthetic enactment event", instrument="seed:fx-ins", eventType="enacted",
                        eventDate="2026-01-01", jurisdiction="US-federal", direction="reshapes", statusAfter="in-force", sources=["DE-022"],
                        evidenceLabel="S", recordedBy="emstagent:fixture@1", reviewBy="2027-10-23"),
    "FrictionRecord": base("seed:fx-frc", "FrictionRecord", "L5", "Synthetic friction", fromActor="federal", toActor="state",
                           frictionType="pay-system-and-direction", direction="from-to", severity="minor", basis="practice",
                           asOf="2026-10-23", evidenceLabel="S", sources=[]),
    "Credential": base("seed:fx-crd", "Credential", "L6", "Synthetic certificate", credentialType="certificate", issuer="Synthetic Issuer",
                       closureType="voluntary", issuerVerified={"verified": False}),
    "SeriesRecord": base("seed:fx-srs", "SeriesRecord", "L6", "Synthetic series", seriesCode="0000", seriesStatus="active"),
    "StateClassRecord": base("seed:fx-scr", "StateClassRecord", "L6", "Synthetic class", jurisdictionId="00", employerType="state-agency",
                             agency="Synthetic Agency", classCode="X1", classTitle="Synthetic Analyst 1", seriesId="Synthetic Analyst 1-3",
                             levelIndex=1, supervisoryStatus="non-supervisory", specEffectiveDate="2026-07-01",
                             workDescriptionText="Synthetic description.", mqText="Synthetic.", mqLocation="spec", degreeRule="substitutable",
                             licensesRequired=[], payBasis="annual", payMinMax=[1, 2], payEffectiveDate="2026-07-01",
                             emstMapping={"roleVariant": "seed:fx-var", "matchType": "close", "confidence": 0.5}),
    "Mapping": {"type": "Mapping", "subject_id": "seed:fx-tsk", "predicate_id": "skos:closeMatch", "object_id": "ONET:00-0000.00-T1",
                "mapping_justification": "semapv:ManualMappingCuration", "confidence": 0.5},
    "LearningResource": base("seed:fx-lrn", "LearningResource", "learning", "Synthetic course", resourceType="course", provider="Synthetic College",
                             teaches=[{"target": "seed:fx-ind", "ireLevel": "I"}]),
    "Bundle": base("seed:fx-bnd", "Bundle", "learning", "Synthetic bundle", workFunction="WF-ASSESS", emstRelease="2.0.0-rc.1"),
    "Source": base("seed:fx-src", "Source", "provenance", "Synthetic source", sourceId="DE-022", publisher="Synthetic", rights="CC0-1.0",
                   quality="Low; synthetic", sourceStatus="current"),
    "ChangeRecord": base("seed:fx-chg", "ChangeRecord", "provenance", "Synthetic change", changeType="C", affectedIds=["seed:fx-tsk"],
                         semverImpact="patch", decisionRef="ADR-0022"),
}
# one seeded violation per type
INVALID_MUT = {
    "VocabularyTerm": ("missing inScheme", lambda r: r.pop("inScheme")),
    "Competency": ("stored computed summary (craftBlend)", lambda r: r.__setitem__("craftBlend", {"FC": 0.5})),
    "Indicator": ("select use class below OBS-4 = 3", lambda r: (r.__setitem__("useClass", "select"), r.__setitem__("obs4", 2))),
    "Enactment": ("actor enactment without authorityBasis", lambda r: r.pop("authorityBasis")),
    "Task": ("compound unknown field and bad work function", lambda r: r.__setitem__("workFunction", "WF-NOTAFUNCTION")),
    "KnowledgeStatement": ("statement missing", lambda r: r.pop("statement")),
    "RoleProfile": ("emerging role without counterSignal/reviewBy", lambda r: r.__setitem__("lifecycleState", "emerging")),
    "RoleVariant": ("state variant without the three disclaimers", lambda r: r.__setitem__("disclaimers", ["Not a classification basis."])),
    "JobFamily": ("stored membership (members is computed)", lambda r: r.__setitem__("members", ["seed:fx-rol"])),
    "Pathway": ("bad pathway type", lambda r: r.__setitem__("pathwayType", "recommended-route")),
    "Tool": ("serves nothing (L4 must point at L1/L2)", lambda r: r.pop("servesTasks")),
    "ExposureAssessment": ("system-executes without deployment evidence", lambda r: r.__setitem__("deploymentMode", "system-executes")),
    "CraftRating": ("ordinal value outside 0/1/2", lambda r: r["values"].__setitem__("FC", 3)),
    "FunctionRating": ("missing taskTextSha256", lambda r: r.pop("taskTextSha256")),
    "RelevanceRating": ("v2 relevance to a v1 legacy scheme", lambda r: r.__setitem__("objectScheme", "v1-family")),
    "ChangeSignal": ("personalData true", lambda r: r.__setitem__("personalData", True)),
    "WatchItem": ("single signal without highPriority", lambda r: r.pop("highPriority")),
    "Instrument": ("no mechanisms", lambda r: r.__setitem__("mechanisms", [])),
    "DriverEvent": ("unknown event type", lambda r: r.__setitem__("eventType", "rumoured")),
    "FrictionRecord": ("Tribal actor without the hold flags", lambda r: r.__setitem__("toActor", "tribal")),
    "Credential": ("verified without a date", lambda r: r.__setitem__("issuerVerified", {"verified": True})),
    "SeriesRecord": ("bad series status", lambda r: r.__setitem__("seriesStatus", "realigned")),
    "StateClassRecord": ("missing MUST field mqText", lambda r: r.pop("mqText")),
    "Mapping": ("predicate not in vocab", lambda r: r.__setitem__("predicate_id", "owl:sameAs")),
    "LearningResource": ("teaches nothing", lambda r: r.__setitem__("teaches", [])),
    "Bundle": ("stored computed clos", lambda r: r.__setitem__("clos", ["seed:fx-ind"])),
    "Source": ("bad quality label", lambda r: r.__setitem__("quality", "Great")),
    "ChangeRecord": ("substantive change without two evidence items", lambda r: r.__setitem__("changeType", "S")),
}


def main():
    vd, idir = FX / "records" / "valid", FX / "records" / "invalid"
    vd.mkdir(parents=True, exist_ok=True)
    idir.mkdir(parents=True, exist_ok=True)
    for t, rec in VALID.items():
        (vd / f"{t}.yaml").write_text("# Synthetic valid fixture (WP-01). Not EMST content.\n" + L.dump_yaml(rec), encoding="utf-8")
        bad = copy.deepcopy(rec)
        why, fn = INVALID_MUT[t]
        fn(bad)
        (idir / f"{t}.yaml").write_text(f"# Synthetic INVALID fixture (WP-01). Seeded violation: {why}\n" + L.dump_yaml(bad), encoding="utf-8")
    # ------------------------------------------------------------------ base tree (valid) + violation overlays
    tree = FX / "trees" / "base" / "data" / "v2"
    cmp_id = mid("core", "CMP", "AB12CD")
    tsk_id = mid("core", "TSK", "EF34GH")
    ind_ids = [mid("core", "IND", "JK56MN"), mid("core", "IND", "PQ78RS")]
    comp = copy.deepcopy(VALID["Competency"])
    comp.update(id=cmp_id, status="candidate", levels=[{"level": "L1", "indicators": ind_ids}])
    task = copy.deepcopy(VALID["Task"])
    task.update(id=tsk_id, status="candidate", supports=[{"competency": cmp_id, "strength": "primary"}])
    inds = []
    for i, iid in enumerate(ind_ids):
        x = copy.deepcopy(VALID["Indicator"])
        x.update(id=iid, status="candidate", competency=cmp_id, servedTasks=[tsk_id])
        if i:
            x["statement"] = {"en": "Labels each sample container with the site code and time under a qualified sampler's direction so that no label is missing."}
        inds.append(x)
    files = {f"core/competencies/{L.id_to_stem(cmp_id)}.yaml": comp, f"core/tasks/{L.id_to_stem(tsk_id)}.yaml": task}
    for x in inds:
        files[f"core/indicators/{L.id_to_stem(x['id'])}.yaml"] = x
    modc = copy.deepcopy(VALID["Competency"])
    modc.update(id="seed:fx-water-cmp", module="water", homeModule="water", subsectors=["W01"], prefLabel={"en": "Operate a treatment process to permit limits"})
    modt = copy.deepcopy(VALID["Task"])
    modt.update(id="seed:fx-water-tsk", module="water", homeModule="water", subsectors=["W01"],
                supports=[{"competency": "seed:fx-water-cmp", "strength": "primary"}, {"competency": cmp_id, "strength": "contributing"}])
    files["modules/water/competencies/seed-fx-water-cmp.yaml"] = modc
    files["modules/water/tasks/seed-fx-water-tsk.yaml"] = modt
    for rel, rec in files.items():
        p = tree / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(L.dump_yaml(rec), encoding="utf-8")
    reg = tree / "ids" / "registry.csv"
    reg.parent.mkdir(parents=True, exist_ok=True)
    rows = [(cmp_id, "Competency"), (tsk_id, "Task"), (ind_ids[0], "Indicator"), (ind_ids[1], "Indicator")]
    reg.write_text("id,type,namespace,minted_on,minted_by,status,superseded_by,first_release\n" +
                   "".join(f"{i},{t},core,2026-10-23,emstagent:fixture@1,candidate,,\n" for i, t in rows), encoding="utf-8")
    gov = tree / "governance"
    gov.mkdir(parents=True, exist_ok=True)
    (gov / "tribal_hold.yaml").write_text((L.DATA_V2 / "governance" / "tribal_hold.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    # The fixture tree keeps the ADR-0013 FALLBACK state (v1 dedication pending) so the licence gate stays tested;
    # the repository itself records the project lead's CC0 dedication (PROJECT_LEAD_DECISIONS.md Q2).
    (gov / "licensing.yaml").write_text(
        "# Synthetic fixture: exercises the ADR-0013 fallback (v1 dedication pending). Not the repository state.\n"
        "v1Dedication: pending\nv1DedicationRecord: null\n", encoding="utf-8")
    print("fixtures written")


if __name__ == "__main__":
    main()
