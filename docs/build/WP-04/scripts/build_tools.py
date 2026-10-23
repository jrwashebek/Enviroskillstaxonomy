"""WP-04 L4 tools seed: data/v2/tools/tools.jsonl (DC entries + FC field instruments + PS reporting tools).

Policy (DC report §7.4; vocab/lifecycle_states.yaml#l4_state_mapping): watch -> established (DC 'active') -> declining
('legacy') -> withdrawn ('retired'). L4 points at L1/L2; L1/L2 never names an L4 product (T-4).
productExamples feed the typing lint case-insensitively (scripts/validate_v2.py), so names that are also ordinary words
(InVEST, Slack, Confluence, Zonation, Raven, Unity, Python, Clay, Watershed, Fulcrum, MAPLE, Zoom, SWAT, Excel, Asana)
are recorded in scopeNote, not productExamples (CR-DC-001).
"""
import csv
import glob
import json
import sys
from pathlib import Path

sys.path.insert(0, "/home/claude/emst/scripts")
import emstlib as L  # noqa: E402

from lib import AGENT, GEN_AT, MODEL, REPO, df  # noqa: E402

PROMPT = "wp04-dc-tools@1"
REVIEW_BY_WATCH = "2027-10-23"
OUT = REPO / "data" / "v2" / "tools" / "tools.jsonl"

TRIG = {
    "Q": "Quarterly light review: expected half-life of 2 years or less, or high replacement risk (DC L4 policy).",
    "A": "Annual full review of the L4 layer (DC L4 policy).",
    "vendor": "Out of cycle: vendor end-of-life, major-version, licence or ownership announcement.",
    "price": "Out of cycle: platform pricing or access-terms change (e.g. a provider-pays change).",
    "policy": "Out of cycle: a governing L5 instrument is issued, amended, rescinded or sunsets.",
    "inventory": "Out of cycle: retirement or new deployment recorded in a tracked AI use-case inventory.",
    "curriculum": "Out of cycle: a curriculum or lesson that teaches the tool is retired.",
    "security": "Out of cycle: a security, privacy or supply-chain advisory affects the tool.",
    "model": "Out of cycle: a new model generation or successor release.",
    "benchmark": "Out of cycle: the benchmark saturates or a successor benchmark is adopted.",
    "standard": "Out of cycle: the issuing body publishes a revision, withdrawal or successor standard.",
    "procurement": "Out of cycle: federal procurement restrictions on the platform class change (e.g. covered-equipment lists).",
}

# ------------------------------------------------------------------ reference resolution (existing records or planned keys)
EXIST = set()
for p in glob.glob(str(REPO / "data/v2/**/*.yaml"), recursive=True):
    try:
        d = L.load_yaml(Path(p))
        if isinstance(d, dict) and d.get("id") and d.get("status") not in ("superseded", "withdrawn"):
            EXIST.add((d["id"], d.get("type")))
    except Exception:  # noqa: BLE001
        pass
COMPS = {i for i, t in EXIST if t == "Competency"}
TASKS = {i for i, t in EXIST if t == "Task"}
PLANNED = {r["target_key"] for r in csv.DictReader(open(REPO / "data/v2/migration/v1_targets.csv"))}
DROPPED = []


def resolve(refs, pool, tool_id):
    ok = []
    for r in refs:
        if r in pool or (r in PLANNED and not r.startswith("seed:tool-")):
            ok.append(r)
        else:
            DROPPED.append((tool_id, r))
    return ok


ROWS = []


def tool(key, label, ttype, category, *, serves=(), tasks=(), products=(), other_names=None, vendor_neutral=None,
         maturity="established", half_life=None, risk="medium", lifecycle="established", steward="DC", trig=("A",),
         sources=(), derived=(), notation=None, note=None, definition=None, evidence=None):
    tid = f"seed:tool-{key}"
    sc = resolve(list(serves), COMPS, tid)
    st = resolve(list(tasks), TASKS, tid)
    assert sc or st, (tid, serves, tasks)
    trig = list(trig)
    if (half_life is not None and half_life <= 2) or risk == "high":
        if "Q" not in trig:
            trig.insert(0, "Q")
    if "A" not in trig:
        trig.append("A")
    rec = {"id": tid, "type": "Tool", "prefLabel": {"en": label}}
    if definition:
        rec["definition"] = {"en": definition}
    scope = []
    if other_names:
        scope.append("Further product names (kept out of productExamples because they are also ordinary words; CR-DC-001): " + ", ".join(other_names) + ".")
    if scope:
        rec["scopeNote"] = {"en": " ".join(scope)}
    ed = [f"Steward: {steward} (DC L4 policy §7.4: DC data and AI entries, FC field instruments, PS private-sector reporting tools)."]
    if note:
        ed.append(note)
    rec["editorialNote"] = {"en": " ".join(ed)}
    if notation:   # Phase 2 seed-list ID kept in the note (no EMST-* notation schemes; ADR-0029)
        rec["editorialNote"]["en"] += f" Phase 2 L4 seed-list ID {notation} (docs/research/data-craft/tools_layer_proposal.csv)."
    rec.update({"layer": "L4", "module": "core", "status": "draft", "lifecycleState": lifecycle, "validationStatus": "draft",
                "license": "CC0-1.0", "sensitivity": "public", "toolType": ttype, "category": category,
                "vendorNeutral": bool(vendor_neutral if vendor_neutral is not None else not products)})
    if products:
        assert all(len(p) >= 3 for p in products), products
        rec["productExamples"] = list(products)
    if sc:
        rec["servesCompetencies"] = sc
    if st:
        rec["servesTasks"] = st
    rec["maturity"] = maturity
    if half_life is not None:
        rec["expectedHalfLifeYears"] = half_life
    rec["replacementRisk"] = risk
    rec["reviewTriggers"] = [TRIG[t] for t in trig]
    if lifecycle in ("watch",):
        rec["reviewBy"] = REVIEW_BY_WATCH
    ev = evidence or ("E" if sources else "J")
    prov = {"method": "llm-assisted", "agent": [AGENT], "generatedAt": GEN_AT, "toolVersion": MODEL, "promptVersion": PROMPT,
            "evidenceLabel": ev, "reviewStatus": "unreviewed"}
    if derived:
        prov["derivedFrom"] = list(derived)
    if sources:
        prov["sources"] = sorted(set(sources))
    prov["adr"] = ["ADR-0003", "ADR-0015"]
    rec["provenance"] = prov
    ROWS.append(rec)
    return tid


MV = lambda k, what: df(k, "split-from", f"tool-fluency content moved to L4 ({what}); X1 emst:movedToTools")  # noqa: E731
REF = lambda k, what="named in v1 text": df(k, "reference-only", what)  # noqa: E731

# ================================================================== v1 move-to-tools targets (planned keys; all twelve)
tool("gis-platforms", "Desktop and web GIS platforms", "software-category", "GIS platforms",
     serves=["seed:v1-2.1.4", "seed:v1-2.1.5"], tasks=["seed:v1-2.1.1-T1", "seed:v1-2.1.1-T2", "seed:v1-2.1.1-T3"],
     half_life=5, risk="medium", trig=("vendor", "inventory", "curriculum"), sources=["DC-001"],
     derived=[MV("v1:2.1.1", "GIS operation"), REF("v1:2.7.5:foundational:I2")],
     note="Product records: seed:tool-arcgis-pro, seed:tool-qgis. AI assistants are being embedded in GIS platforms [E: DC-001]; skills tied to interface versions decay fast, spatial concepts do not.")
tool("field-data-apps", "Mobile field data-collection apps", "software-category", "Field data capture",
     serves=["seed:FC-C23", "seed:v1-2.2.3"], tasks=["seed:v1-2.3.4-T1", "seed:v1-2.3.4-T2", "seed:v1-2.3.4-T3"],
     products=["ODK", "KoBoToolbox"], other_names=["Fulcrum"], vendor_neutral=True, half_life=4, risk="medium", steward="FC",
     trig=("vendor", "security"), sources=["DC-042"],
     derived=[MV("v1:2.3.4", "mobile applications for field science"), REF("v1:2.3.3:intermediate:I2"), REF("v1:4.1.5:intermediate:I1")],
     note="Product records: seed:tool-survey123-field-maps, seed:tool-inaturalist. Connectivity, ruggedness and cloud-security approvals are the usual barriers (FC field_tech_change_matrix FT-08).")
tool("meeting-platforms", "Virtual meeting and team collaboration platforms", "software-category", "Collaboration platforms",
     serves=["seed:v1-5.2.2"], tasks=["seed:v1-2.5.1-T1", "seed:v1-2.5.1-T2", "seed:v1-2.5.1-T3"],
     products=["Microsoft Teams", "Webex", "Google Meet"], other_names=["Zoom", "Slack"], vendor_neutral=True, half_life=3, risk="medium",
     trig=("vendor", "security"), derived=[MV("v1:2.5.1", "virtual meeting facilitation"), REF("v1:3.5.2:intermediate:I5"), REF("v1:3.5.4:intermediate:I3")])
tool("project-management-software", "Project and task management software", "software-category", "Project management",
     serves=["seed:PS-C03"], tasks=["seed:v1-2.5.3-T2", "seed:v1-3.1.1-T2"],
     products=["Trello", "Smartsheet", "Microsoft Project"], other_names=["Asana"], vendor_neutral=True, half_life=4, risk="medium", steward="PS",
     trig=("vendor",), derived=[MV("v1:2.5.3", "project management software"), REF("v1:3.1.1:foundational:I4"), REF("v1:2.5.3:advanced:I2")])
tool("ar-tool-family", "Augmented-reality devices and field overlay applications", "software-category", "Immersive and AR",
     serves=["seed:v1-2.1.5"], tasks=["seed:v1-2.7.1-T1", "seed:v1-2.7.1-T2", "seed:v1-2.7.1-T3"],
     products=["HoloLens"], vendor_neutral=True, maturity="emerging", half_life=2, risk="high", lifecycle="watch",
     trig=("inventory", "vendor"), sources=["DC-001"], derived=[MV("v1:2.7.1", "augmented reality field applications"), REF("v1:2.7.1:advanced:I4")],
     note="Watch only: one AR use case (pre-deployment) among 438 USDA/DOI/EPA inventory entries [E: DC-001]; no environmental demand evidence (v1_disposition 2.7.1). Review +12 months.")
tool("vr-tool-family", "Virtual-reality headsets and simulation content tools", "software-category", "Immersive and AR",
     serves=["seed:v1-5.4.1"], tasks=["seed:v1-2.7.2-T1", "seed:v1-2.7.2-T2", "seed:v1-2.7.2-T3"],
     products=["Unreal Engine"], other_names=["Unity"], vendor_neutral=True, maturity="emerging", half_life=2, risk="high", lifecycle="watch",
     trig=("vendor", "curriculum"), sources=["DC-001"], derived=[MV("v1:2.7.2", "virtual reality environmental education"), REF("v1:2.7.2:intermediate:I1")],
     note="Watch only (v1_disposition 2.7.2); instructional design stays with v1 5.4.1.")
tool("immersive-platforms", "Immersive visualization and 3-D storytelling platforms", "software-category", "Immersive and AR",
     serves=["seed:v1-2.1.5"], tasks=["seed:v1-2.7.4-T1", "seed:v1-2.7.4-T2", "seed:v1-2.7.4-T3"],
     vendor_neutral=True, maturity="emerging", half_life=2, risk="high", lifecycle="watch", trig=("vendor",),
     derived=[MV("v1:2.7.4", "immersive visualization design"), REF("v1:2.7.4:intermediate:I2")],
     note="Watch only (v1_disposition 2.7.4); the durable part (visual communication) is v1 2.1.5.")
tool("method", "Environmental DNA laboratory assays and bioinformatic pipelines", "protocol", "Genetic survey methods",
     serves=["seed:FC-C16", "seed:v1-1.6.1"], vendor_neutral=True, maturity="growing", half_life=3, risk="medium", steward="FC",
     trig=("standard",), derived=[MV("v1:1.6.2", "eDNA methods: assays and pipelines are an L4 method")],
     note="Planned key from v1_disposition 1.6.2 ('L4 method (eDNA)'). Field sampling and contamination control are FC-C16; assay interpretation knowledge is v1 1.6.1. Standardization of methods and reporting is still in progress (FC FT-05).")
tool("financial-systems-and-dashboards", "Financial management systems and budget dashboards", "software-category", "Financial systems",
     serves=["seed:SC-C10", "seed:PS-C03"], vendor_neutral=True, half_life=4, risk="medium", steward="PS",
     trig=("vendor", "policy"), derived=[MV("v1:3.4.1", "digital financial systems and data-driven budgeting"), REF("v1:3.4.1:intermediate:I2")],
     note="Planned key from v1_disposition 3.4.1. Dashboard products are in seed:tool-dashboard-bi-software.")
tool("financial-automation-tools", "Financial automation and automated compliance-checking tools", "software-category", "Financial systems",
     serves=["seed:SC-C10", "seed:DB-C26"], vendor_neutral=True, maturity="growing", half_life=2, risk="high", steward="PS",
     trig=("vendor", "policy"), derived=[MV("v1:3.4.4", "automated financial operations and AI-enhanced compliance")],
     note="Planned key from v1_disposition 3.4.4 (robotic process automation, AI compliance checks). Durable controls stay in SC-C10 and DB-C26.")
tool("impact-measurement-platforms", "Real-time impact measurement and reporting platforms", "software-category", "Impact reporting",
     serves=["seed:v1-3.1.5"], vendor_neutral=True, maturity="emerging", half_life=2, risk="high", lifecycle="watch", steward="PS",
     trig=("vendor",), derived=[MV("v1:3.4.5", "real-time impact measurement and financial transparency")],
     note="Planned key from v1_disposition 3.4.5; the durable content is programme evaluation (v1 3.1.5).")
tool("precision-agriculture-systems", "Precision agriculture systems: auto-steer, variable-rate application and spray drones", "instrument-class", "Agricultural automation",
     serves=["seed:FC-C14", "seed:v1-4.6.1"], vendor_neutral=True, half_life=4, risk="medium", steward="FC",
     trig=("procurement", "vendor"), derived=[MV("v1:4.6.2", "precision agriculture technology use")],
     note="Planned key from v1_disposition 4.6.2. Durable content: supervising automated machinery (FC-C14) and validating prescriptions against field conditions (FC FT-17); spray-drone supply is exposed to covered-equipment actions (FC-008).")

# ================================================================== DC entries (Phase 2 tools_layer_proposal.csv)
tool("arcgis-pro", "ArcGIS Pro", "software-product", "GIS platforms", serves=["seed:v1-2.1.4", "seed:v1-2.1.5", "seed:DC-CAND-22"],
     products=["ArcGIS Pro", "ArcGIS Online"], half_life=5, risk="medium", trig=("vendor", "inventory"), sources=["DC-001"], notation="DC-TOOL-001")
tool("qgis", "QGIS", "software-product", "GIS platforms", serves=["seed:v1-2.1.4", "seed:v1-2.1.5"], products=["QGIS"], half_life=6, risk="low",
     trig=("vendor",), sources=["DC-001"], notation="DC-TOOL-002", note="Open-source, vendor-neutral training option for NGO and local users.")
tool("geospatial-libraries", "Open geospatial processing libraries", "software-category", "Geospatial libraries", serves=["seed:v1-2.1.4", "seed:DC-CAND-08"],
     products=["GDAL", "OGR", "PROJ"], vendor_neutral=True, half_life=10, risk="low", trig=("vendor",), notation="DC-TOOL-003")
tool("cloud-native-geospatial-formats", "Cloud-native geospatial formats and catalogue specifications", "technical-standard", "Data formats",
     serves=["seed:DC-CAND-06", "seed:DC-CAND-04", "seed:v1-2.1.2"], products=["Zarr", "GeoParquet", "STAC", "Cloud Optimized GeoTIFF"], vendor_neutral=True,
     maturity="growing", half_life=8, risk="low", trig=("standard",), sources=["DC-027"], notation="DC-TOOL-004")
tool("google-earth-engine", "Google Earth Engine", "platform", "Cloud Earth-observation platforms", serves=["seed:v1-2.1.2"],
     products=["Google Earth Engine", "Earth Engine"], half_life=4, risk="medium", trig=("price", "vendor"), sources=["DC-028"], notation="DC-TOOL-005",
     note="Platform terms change: the satellite-embedding storage bucket became provider-pays in July 2026 [E: DC-028]; competencies must not assume free access.")
tool("planetary-computer", "Microsoft Planetary Computer", "platform", "Cloud Earth-observation platforms", serves=["seed:v1-2.1.2"],
     products=["Planetary Computer"], half_life=3, risk="high", trig=("vendor", "price"), sources=["DC-027"], notation="DC-TOOL-006",
     note="Public issues repository last updated 2024-11; current hosted-service status not verified [E: DC-027]. Platform-concentration example; check status at next review.")
tool("hls", "Harmonized Landsat Sentinel-2 surface reflectance", "dataset-product", "Earth-observation data products", serves=["seed:v1-2.1.2"],
     products=["Harmonized Landsat Sentinel-2"], half_life=10, risk="low", trig=("standard",), sources=["DC-023"], notation="DC-TOOL-007",
     note="Depends on continuity of the Landsat and Sentinel missions.")
tool("nlcd", "National Land Cover Database", "dataset-product", "Earth-observation data products", serves=["seed:v1-2.1.2", "seed:DC-CAND-09"],
     products=["National Land Cover Database", "NLCD"], half_life=10, risk="low", trig=("standard",), sources=["DC-001", "DC-028"], notation="DC-TOOL-008",
     note="Deep-learning production [E: DC-001]; also a training target for satellite embeddings, so embedding-based updates of similar maps risk circular validation [E: DC-028].")
tool("prithvi-eo", "Prithvi-EO-2.0 Earth-observation foundation model", "model", "Earth-observation foundation models", serves=["seed:v1-2.1.2", "seed:v1-2.4.1"],
     tasks=["seed:dc-212-transfer-test"], products=["Prithvi-EO-2.0", "Prithvi"], maturity="growing", half_life=2, risk="high", trig=("model",),
     sources=["DC-023"], notation="DC-TOOL-009")
tool("olmoearth", "OlmoEarth models and platform", "model", "Earth-observation foundation models", serves=["seed:v1-2.1.2"], tasks=["seed:dc-212-transfer-test"],
     products=["OlmoEarth"], maturity="growing", half_life=1, risk="high", lifecycle="watch", trig=("model",), sources=["DC-025"], notation="DC-TOOL-010",
     note="Three model generations in about a year [E: DC-025]: direct evidence for a roughly one-year half-life of specific models.")
tool("clay-model", "Clay Earth-observation foundation model", "model", "Earth-observation foundation models", serves=["seed:v1-2.1.2"], tasks=["seed:dc-212-transfer-test"],
     products=["Clay foundation model"], other_names=["Clay"], maturity="growing", half_life=2, risk="high", lifecycle="watch", trig=("model",), sources=["DC-024"],
     notation="DC-TOOL-011")
tool("alphaearth-embeddings", "AlphaEarth Foundations satellite embedding dataset", "dataset-product", "Earth-observation embeddings",
     serves=["seed:v1-2.1.2", "seed:DC-CAND-09"], tasks=["seed:dc-212-circularity-check"], products=["AlphaEarth Foundations", "AlphaEarth", "Satellite Embedding V1"],
     maturity="growing", half_life=3, risk="medium", trig=("price", "model"), sources=["DC-028"], notation="DC-TOOL-012",
     note="Embedding bands are 'not independently interpretable' and were trained with national land-cover and crop targets [E: DC-028].")
tool("terratorch", "TerraTorch fine-tuning toolkit", "software-product", "Machine-learning libraries", serves=["seed:v1-2.1.2"], products=["TerraTorch"],
     maturity="growing", half_life=2, risk="high", lifecycle="watch", trig=("vendor",), sources=["DC-026", "DC-023"], notation="DC-TOOL-013")
tool("geo-bench", "GEO-Bench Earth-observation benchmark", "dataset-product", "Evaluation benchmarks", serves=["seed:DC-CAND-15", "seed:v1-2.1.2"],
     products=["GEO-Bench"], half_life=3, risk="medium", trig=("benchmark",), sources=["DC-060", "DC-023"], notation="DC-TOOL-014")
tool("survey123-field-maps", "Survey123 and ArcGIS Field Maps", "software-product", "Field data capture", serves=["seed:FC-C23"],
     tasks=["seed:v1-2.3.4-T1", "seed:v1-2.3.4-T2"], products=["Survey123", "ArcGIS Field Maps"], half_life=4, risk="medium", steward="FC",
     trig=("vendor", "security"), sources=["DC-042"], notation="DC-TOOL-015", derived=[REF("v1:2.3.4:T1")])
tool("inaturalist", "iNaturalist community-science platform", "platform", "Community science", serves=["seed:FC-C23", "seed:DC-CAND-03", "seed:DC-CAND-07", "seed:v1-5.4.4"],
     products=["iNaturalist"], half_life=6, risk="low", trig=("vendor",), sources=["DC-042", "DC-029"], notation="DC-TOOL-016", derived=[REF("v1:2.3.4:T1")],
     note="Community data quality and obscuring of sensitive locations are durable concerns (DC-CAND-07).")
tool("gnss-receivers", "GNSS receivers including real-time kinematic correction", "instrument-class", "Positioning instruments",
     serves=["seed:FC-C18", "seed:FC-C23"], vendor_neutral=True, half_life=5, risk="low", steward="FC", trig=("vendor",), sources=["DC-042"], notation="DC-TOOL-017",
     derived=[REF("v1:2.1.3")], note="Device operation is fluency; positional accuracy and datum concepts are durable knowledge (v1_disposition 2.1.3).")
tool("small-uas-platforms", "Small uncrewed aircraft systems for survey and imagery", "instrument-class", "Uncrewed aircraft",
     serves=["seed:FC-C14"], vendor_neutral=True, half_life=3, risk="medium", steward="FC", trig=("procurement", "policy", "vendor"),
     sources=["FC-001", "FC-002", "FC-008"], notation="DC-TOOL-018",
     derived=[REF("v1:2.3.2", "aircraft moved to L4; flight operations to FC-C14"), REF("v1:4.5.4", "aircraft moved to L4")],
     note="Federal procurement restrictions on covered aircraft and components drive churn [E: FC-001, FC-008]; airspace rules are L5 instruments; remote-pilot certification is a Credential.")
tool("photogrammetry-software", "Structure-from-motion photogrammetry software", "software-category", "Image processing",
     serves=["seed:v1-2.1.2", "seed:v1-2.1.4"], products=["Pix4D", "DroneDeploy", "Agisoft Metashape", "OpenDroneMap"], vendor_neutral=True,
     half_life=3, risk="medium", trig=("vendor", "security"), notation="DC-TOOL-018", derived=[REF("v1:2.3.2", "processing software moved to L4")])
tool("megadetector", "MegaDetector camera-trap animal detector", "model", "Camera-trap AI", serves=["seed:v1-2.4.1", "seed:DC-CAND-13", "seed:FC-C03"],
     products=["MegaDetector"], half_life=3, risk="medium", trig=("model",), sources=["DC-038"], notation="DC-TOOL-019",
     note="Detects animals, not species [E: DC-038].")
tool("speciesnet", "SpeciesNet camera-trap species classifier", "model", "Camera-trap AI", serves=["seed:v1-2.4.1", "seed:FC-C03"], products=["SpeciesNet"],
     maturity="growing", half_life=2, risk="high", trig=("model",), sources=["DC-039", "DC-038"], notation="DC-TOOL-020")
tool("birdnet", "BirdNET bioacoustic classifier", "model", "Bioacoustic AI", serves=["seed:v1-2.4.1", "seed:FC-C03", "seed:DC-CAND-15"],
     tasks=["seed:v1-2.6.2-T2"], products=["BirdNET-Analyzer", "BirdNET"], half_life=3, risk="medium", trig=("model",), sources=["DC-040"], notation="DC-TOOL-021",
     note="Per-model licences; built-in train and evaluate commands [E: DC-040].")
tool("bioacoustic-analysis-software", "Bioacoustic analysis and annotation software", "software-category", "Bioacoustic AI", serves=["seed:v1-2.4.1"],
     tasks=["seed:v1-2.6.2-T2", "seed:v1-2.6.2-T3"], products=["Kaleidoscope Pro", "Raven Pro"], other_names=["Raven", "Kaleidoscope"], vendor_neutral=True,
     half_life=5, risk="medium", trig=("vendor",), derived=[REF("v1:2.6.2:intermediate:I5")])
tool("viame", "VIAME image and video analytics toolkit for marine environments", "software-product", "Marine image AI", serves=["seed:v1-2.4.1", "seed:DC-CAND-13"],
     products=["VIAME"], half_life=4, risk="medium", trig=("vendor",), sources=["DC-001"], notation="DC-TOOL-022")
tool("r-ecosystem", "R language and package ecosystem", "software-category", "Programming ecosystems", serves=["seed:DC-CAND-08", "seed:v1-2.2.2"],
     products=["tidyverse", "RStudio"], other_names=["R", "sf", "terra"], vendor_neutral=True, half_life=8, risk="low", trig=("curriculum", "vendor"),
     sources=["DC-030", "DC-031"], notation="DC-TOOL-023", derived=[REF("v1:2.2.4:T2"), REF("v1:2.2.2:foundational:I5")],
     note="Curricula tied to package stacks churn even when the language persists (a geospatial lesson retired in 2026) [E: DC-031].")
tool("python-scientific-stack", "Python scientific and geospatial stack", "software-category", "Programming ecosystems", serves=["seed:DC-CAND-08"],
     products=["NumPy", "xarray", "rasterio", "GeoPandas", "SciPy"], other_names=["Python", "pandas"], vendor_neutral=True, half_life=8, risk="low",
     trig=("curriculum", "vendor"), sources=["DC-023", "DC-025"], notation="DC-TOOL-024", derived=[REF("v1:2.2.4:T2"), REF("v1:2.1.1:advanced:I2")])
tool("jupyter", "Jupyter notebooks", "software-product", "Reproducibility infrastructure", serves=["seed:DC-CAND-08"], products=["Jupyter", "JupyterLab"],
     half_life=6, risk="low", trig=("vendor",), sources=["DC-023", "DC-024"], notation="DC-TOOL-025")
tool("version-control", "Version control and hosted repositories", "software-category", "Reproducibility infrastructure",
     serves=["seed:DC-CAND-08", "seed:DC-CAND-05"], products=["GitHub", "GitLab"], other_names=["Git"], vendor_neutral=True, half_life=10, risk="low",
     trig=("vendor", "security"), sources=["DC-037"], notation="DC-TOOL-026")
tool("environment-managers", "Software environment managers and containers", "software-category", "Reproducibility infrastructure", serves=["seed:DC-CAND-08"],
     products=["Docker", "conda"], other_names=["mamba", "uv"], vendor_neutral=True, half_life=5, risk="medium", trig=("vendor",), sources=["DC-025", "DC-024"],
     notation="DC-TOOL-027")
tool("relational-databases", "Relational database systems and SQL", "software-category", "Databases", serves=["seed:v1-2.2.1", "seed:DC-CAND-04"],
     products=["PostgreSQL", "PostGIS", "SQLite"], vendor_neutral=True, half_life=15, risk="low", trig=("vendor", "security"), sources=["DC-042"],
     notation="DC-TOOL-028", derived=[REF("v1:2.2.1:intermediate:I2")], note="Longest half-life in the layer.")
tool("geospatial-metadata-standards", "Geospatial metadata standards", "technical-standard", "Metadata standards", serves=["seed:DC-CAND-06"],
     products=["ISO 19115", "FGDC CSDGM"], vendor_neutral=True, half_life=10, risk="low", trig=("standard",), sources=["DC-042", "DC-001"], notation="DC-TOOL-029",
     derived=[REF("v1:2.2.5")], note="Metadata authoring is increasingly machine-generated [E: DC-001]; reviewing it stays in DC-CAND-06.")
tool("genai-assistants", "General-purpose generative AI assistants", "software-category", "Generative AI assistants",
     serves=["seed:DC-CAND-02", "seed:DC-CAND-13", "seed:DC-CAND-16", "seed:v1-7.2.3"],
     products=["ChatGPT", "Microsoft Copilot", "Azure OpenAI", "Google Gemini", "Anthropic Claude"], vendor_neutral=True, maturity="growing", half_life=1,
     risk="high", trig=("model", "policy", "inventory", "security"), sources=["DC-001", "DC-008"], notation="DC-TOOL-030",
     derived=[REF("v1:3.5.1:foundational:I6")],
     note="Federal procurement of large language models is governed by L5 instruments (seed:ins/omb-m-26-04, seed:ins/omb-m-25-22). Never named in competency text.")
tool("ai-coding-assistants", "AI coding assistants and coding agents", "software-category", "Generative AI assistants", serves=["seed:DC-CAND-08"],
     tasks=["seed:dc-08-review-ai-code"], products=["GitHub Copilot", "Gemini Code Assist", "Amazon Q Developer", "Codex CLI", "Claude Code"], vendor_neutral=True,
     maturity="growing", half_life=1, risk="high", trig=("model", "security"), sources=["DC-001", "DC-032"], notation="DC-TOOL-031",
     note="Agent supervision is the L5 watch item seed:watch-DC-CAND-17, not an L1 competency (WP-04 acceptance).")
tool("retrieval-augmented-generation", "Retrieval-augmented generation frameworks over agency corpora", "software-category", "Generative AI assistants",
     serves=["seed:DC-CAND-18", "seed:DC-CAND-16"], products=["GraphRAG"], vendor_neutral=True, maturity="growing", half_life=1.5, risk="high",
     trig=("model", "inventory"), sources=["DC-001"], notation="DC-TOOL-032")
tool("comment-analysis-services", "Public-comment analysis services", "software-category", "Domain AI services", serves=["seed:DC-CAND-16", "seed:DC-CAND-13"],
     tasks=["seed:v1-6.4.4-T2", "seed:dc-13-check-comment-grouping"], products=["DocketScope", "CommentNEPA"], vendor_neutral=True, maturity="growing",
     half_life=2, risk="high", trig=("inventory", "policy"), sources=["DC-001", "DC-033"], notation="DC-TOOL-033",
     note="Deployed with analyst verification; one interior comment tool was retired between the 2024 and 2025 inventories [E: DC-001].")
tool("permitai-services", "PermitAI shared services and NEPATEC corpus", "platform", "Domain AI services", serves=["seed:DC-CAND-16", "seed:DC-CAND-15"],
     products=["PermitAI", "SearchNEPA", "WriteNEPA", "EngageNEPA", "NEPATEC"], maturity="emerging", half_life=2, risk="high", lifecycle="watch",
     trig=("inventory", "policy"), sources=["DC-033", "DC-032"], notation="DC-TOOL-034")
tool("forest-planning-genai-tools", "Forest-planning generative AI tools", "software-category", "Domain AI services", serves=["seed:DC-CAND-16"],
     vendor_neutral=True, maturity="emerging", half_life=2, risk="high", lifecycle="watch", trig=("inventory",), sources=["DC-001"], notation="DC-TOOL-035",
     note="Plan review and planning-support tools deployed June-July 2025 by one agency with two vendors [E: DC-001]; single-organization evidence, so watch.")
tool("draftnepabench", "DraftNEPABench and related NEPA drafting evaluation pipelines", "dataset-product", "Evaluation benchmarks", serves=["seed:DC-CAND-15"],
     tasks=["seed:dc-15-judge-check"], products=["DraftNEPABench"], other_names=["MAPLE"], maturity="emerging", half_life=2, risk="high", lifecycle="watch",
     trig=("benchmark",), sources=["DC-032"], notation="DC-TOOL-036",
     note="Subject-matter rubrics graded by LLM judges; the judges themselves need human validation [E: DC-032].")
tool("nist-dioptra", "NIST Dioptra AI test platform", "software-product", "AI test platforms", serves=["seed:DC-CAND-15", "seed:DC-CAND-19", "seed:DC-CAND-20"],
     products=["Dioptra"], maturity="growing", half_life=3, risk="medium", trig=("vendor",), sources=["DC-041"], notation="DC-TOOL-037")
tool("model-system-data-cards", "Model, system and data cards", "technical-standard", "AI documentation", serves=["seed:DC-CAND-05", "seed:DC-CAND-19", "seed:DC-CAND-20"],
     tasks=["seed:dc-20-read-documentation"], vendor_neutral=True, maturity="growing", half_life=5, risk="medium", trig=("policy", "standard"), sources=["DC-008"],
     notation="DC-TOOL-038", note="Required for procured large language models under an L5 instrument [E: DC-008]; formats will evolve, the reading skill will not.")
tool("emds", "Ecosystem Management Decision Support system", "software-product", "Decision-support systems", serves=["seed:DC-CAND-22"],
     products=["Ecosystem Management Decision Support", "EMDS"], half_life=5, risk="medium", trig=("vendor",), sources=["DC-001"], notation="DC-TOOL-039",
     note="In agency use since 1997 [E: DC-001]: long-lived decision-support systems show 'AI' labels applied retroactively to classical systems.")
tool("forest-vegetation-simulator", "Forest Vegetation Simulator", "model", "Process models", serves=["seed:v1-1.3.3", "seed:v1-2.4.2", "seed:DC-CAND-09"],
     products=["Forest Vegetation Simulator", "FVS"], half_life=10, risk="low", trig=("vendor",), sources=["DC-001"], notation="DC-TOOL-040",
     derived=[REF("v1:1.3.3:intermediate:I1")], note="Now wrapped by a retrieval help-desk pilot [E: DC-001].")
tool("ecosystem-service-models", "Ecosystem-service models", "software-category", "Process models", serves=["seed:v1-6.3.2", "seed:DC-CAND-09"],
     products=["ARIES"], other_names=["InVEST"], vendor_neutral=True, half_life=6, risk="medium", trig=("vendor",), sources=["DC-042"], notation="DC-TOOL-041",
     derived=[REF("v1:6.3.2:T2"), REF("v1:6.3.2:intermediate:I2")])
tool("ej-screening-tools", "Environmental-justice and cumulative-burden screening tools", "software-category", "Screening tools",
     serves=["seed:DB-C52", "seed:DC-CAND-09", "seed:DC-CAND-11"], products=["EJScreen", "CalEnviroScreen"], vendor_neutral=True, maturity="legacy", half_life=2,
     risk="high", lifecycle="declining", trig=("policy", "vendor"), sources=["DC-042"], notation="DC-TOOL-042",
     derived=[REF("v1:6.7.2:T1"), REF("v1:6.7.2:foundational:I2")],
     note="Federal tool availability is volatile (removal of the federal screening tool in early 2025 is expert recollection, to verify through WP-15); state tools persist. Function lives in DB-C52 (ADR-0016).")
tool("ai-forecast-emulators", "AI weather and climate emulators and AI forecast models", "model", "Forecast systems", serves=["seed:DC-CAND-12", "seed:v1-2.4.2"],
     products=["Ai2 Climate Emulator"], maturity="emerging", half_life=2, risk="high", lifecycle="watch", trig=("model", "inventory"), sources=["DC-001"],
     notation="DC-TOOL-043")
tool("earth-system-digital-twins", "Earth-system digital twin programmes", "platform", "Forecast systems", serves=["seed:DC-CAND-12"], products=["Destination Earth"],
     maturity="emerging", half_life=3, risk="high", lifecycle="watch", trig=("vendor", "policy"), notation="DC-TOOL-044",
     note="Programme status not verified this session (DC-054, DC-055 unverified).")
tool("distributed-ledger-tools", "Blockchain and distributed-ledger tooling for conservation finance", "software-category", "Ledgers",
     serves=["seed:v1-6.6.3"], products=["Ethereum"], other_names=["blockchain"], vendor_neutral=True, maturity="declining", half_life=1, risk="high",
     lifecycle="declining", trig=("inventory",), sources=["DC-001"], notation="DC-TOOL-046",
     derived=[REF("v1:3.4.3:foundational:I1", "v1 3.4.3 retired (NoTermFound); ledger tooling kept in L4 as declining")],
     note="Zero blockchain use cases among 438 USDA/DOI/EPA inventory entries [E: DC-001]; v1 3.4.3 retired.")
tool("nist-ai-rmf", "NIST AI Risk Management Framework and Generative AI Profile", "technical-standard", "AI governance standards",
     serves=["seed:DC-CAND-19", "seed:DC-CAND-21", "seed:DC-CAND-14"], products=["NIST AI RMF", "NIST-AI-600-1"], vendor_neutral=True, half_life=3,
     risk="medium", trig=("standard", "policy"), sources=["DC-004", "DC-005", "DC-010"], notation="DC-TOOL-049",
     note="A practitioner-chosen framework, so L4 (T-7). Revision under way; trustworthiness characteristics are durable vocabulary, version-specific playbook steps are not.")
tool("iso-iec-42001", "ISO/IEC 42001 AI management system standard", "technical-standard", "AI governance standards", serves=["seed:DC-CAND-21", "seed:DC-CAND-19"],
     products=["ISO/IEC 42001"], vendor_neutral=True, half_life=6, risk="low", trig=("standard",), notation="DC-TOOL-053", evidence="J",
     note="Certifiable private-sector analogue to the NIST framework (DC-053 not read; J).")

# ------------------------------------------------------------------ further tools named in v1 text (acceptance: every tool moved out of v1 text is in L4)
tool("knowledge-management-platforms", "Document and knowledge management platforms", "software-category", "Knowledge management",
     serves=["seed:DC-CAND-18"], tasks=["seed:v1-2.5.4-T1"], products=["SharePoint"], other_names=["Confluence"], vendor_neutral=True, half_life=5,
     risk="medium", trig=("vendor", "security"), derived=[REF("v1:2.5.4:intermediate:I3")])
tool("dashboard-bi-software", "Dashboard and business-intelligence software", "software-category", "Dashboards",
     serves=["seed:DC-CAND-22"], tasks=["seed:v1-2.4.3-T2"], products=["Tableau", "Power BI"], vendor_neutral=True, half_life=4, risk="medium",
     trig=("vendor",), derived=[REF("v1:3.4.1:intermediate:I2")])
tool("statistical-software", "Statistical analysis and spreadsheet software", "software-category", "Statistical software",
     serves=["seed:v1-2.2.2"], products=["SPSS", "Stata"], other_names=["Excel", "SAS"], vendor_neutral=True, half_life=8, risk="low",
     trig=("vendor", "curriculum"), derived=[REF("v1:2.2.2:foundational:I5")])
tool("ml-frameworks", "Machine-learning frameworks and detection model architectures", "software-category", "Machine-learning libraries",
     serves=["seed:v1-2.4.1"], products=["scikit-learn", "TensorFlow", "PyTorch", "YOLO"], vendor_neutral=True, half_life=3, risk="medium",
     trig=("vendor", "model"), derived=[REF("v1:2.4.1:intermediate:I6"), REF("v1:2.6.1:intermediate:I2")])
tool("agent-based-modelling", "Agent-based and system-dynamics modelling platforms", "software-category", "Simulation platforms",
     serves=["seed:v1-2.4.2"], products=["NetLogo"], vendor_neutral=True, half_life=6, risk="low", trig=("vendor",), derived=[REF("v1:2.4.2:intermediate:I5")])
tool("conservation-prioritization", "Systematic conservation-planning and prioritization software", "software-category", "Spatial prioritization",
     serves=["seed:v1-2.1.4"], products=["Marxan"], other_names=["Zonation"], vendor_neutral=True, half_life=6, risk="low", trig=("vendor",),
     derived=[REF("v1:2.1.4:advanced:I3")])
tool("fire-behaviour-models", "Fire behaviour models and fire decision-support systems", "software-category", "Fire modelling",
     serves=["seed:v1-2.4.2", "seed:DC-CAND-11", "seed:v1-4.3.4", "seed:FS-C05"], tasks=["seed:v1-2.4.2-T1", "seed:dc-11-incident-confidence-briefing"],
     products=["FARSITE", "FlamMap", "BehavePlus", "IFTDSS", "WFDSS"], vendor_neutral=True, half_life=5, risk="medium", steward="DC (with FC review)",
     trig=("vendor", "policy"), derived=[REF("v1:4.3.3:advanced:I2"), REF("v1:4.3.4:advanced:I4"), REF("v1:4.3.2:advanced:I4")],
     note="Used by fire behaviour and long-term analysts (P1 role R08); system consolidation follows interagency fire-governance decisions recorded in L5.")
tool("hydrologic-hydraulic-models", "Hydrologic, hydraulic and groundwater models", "software-category", "Process models",
     serves=["seed:v1-2.4.2", "seed:v1-1.2.3"], products=["HEC-HMS", "HEC-RAS", "MODFLOW"], other_names=["SWAT"], vendor_neutral=True, half_life=8,
     risk="low", steward="DC (PS screen)", trig=("vendor",), derived=[REF("v1:1.2.3:intermediate:I3")],
     note="Private postings screen on these names (ADR-0003 PS dissent): role variants link here through tools_commonly_required.")
tool("air-dispersion-models", "Air dispersion and photochemical models", "software-category", "Process models",
     serves=["seed:DB-C14"], products=["AERMOD", "CALPUFF"], vendor_neutral=True, half_life=8, risk="low", steward="PS", trig=("policy", "vendor"),
     note="Regulatory model preferences are set by L5 instruments; private postings screen on model names (ADR-0003 PS dissent).")
tool("cad-software", "Computer-aided design software for site and terrain models", "software-category", "Design software",
     serves=["seed:v1-2.1.4"], products=["AutoCAD", "Civil 3D"], vendor_neutral=True, half_life=6, risk="low", trig=("vendor",), derived=[REF("v1:2.7.5:T1")])
tool("climate-vulnerability-indices", "Species and habitat climate-vulnerability index tools", "software-category", "Vulnerability assessment",
     serves=["seed:v1-1.5.2"], products=["NatureServe Climate Change Vulnerability Index"], vendor_neutral=True, half_life=6, risk="low",
     trig=("standard",), derived=[REF("v1:1.5.2:intermediate:I1")])

# ================================================================== FC field instruments (steward FC)
tool("uas-ignition-systems", "UAS aerial ignition systems", "instrument-class", "Uncrewed aircraft", serves=["seed:FC-C14", "seed:v1-4.3.2"],
     vendor_neutral=True, half_life=3, risk="medium", steward="FC", trig=("procurement", "policy"), sources=["FC-002", "FC-010", "FC-001"],
     note="Scaled in prescribed fire (188,986 acres ignited by UAS in FY24) [E: FC-002]; one agency shifted some ignition back to helicopters under drone restrictions [E: FC-001].")
tool("lidar-systems", "Lidar systems: airborne, drone, terrestrial and mobile", "instrument-class", "Remote sensing instruments",
     serves=["seed:FC-C02", "seed:v1-2.1.2", "seed:v1-2.1.4", "seed:v1-1.3.2"], vendor_neutral=True, half_life=5, risk="medium", steward="FC",
     trig=("vendor",), sources=["FC-032"], derived=[REF("v1:2.1.2:advanced:I2"), REF("v1:2.7.4:T2")])
tool("edna-sampling-equipment", "Environmental DNA field sampling equipment and autosamplers", "instrument-class", "Genetic survey methods",
     serves=["seed:FC-C16"], vendor_neutral=True, maturity="growing", half_life=4, risk="medium", steward="FC", trig=("standard",), evidence="J",
     note="Contamination control, field blanks and replication are FC-C16; assays and pipelines are seed:tool-method.")
tool("acoustic-recorders", "Passive acoustic recorders", "instrument-class", "Biological survey instruments",
     serves=["seed:FC-C01", "seed:v1-2.4.1"], tasks=["seed:v1-2.6.2-T1"], vendor_neutral=True, half_life=4, risk="medium", steward="FC", trig=("vendor",), evidence="J")
tool("camera-traps", "Camera traps", "instrument-class", "Biological survey instruments", serves=["seed:FC-C01", "seed:FC-C03"],
     vendor_neutral=True, half_life=5, risk="low", steward="FC", trig=("vendor",), evidence="J",
     note="Images of people raise privacy handling duties (FC FT-07); AI triage products are separate entries.")
tool("in-situ-sensors-telemetry", "Continuous in-situ sensors, data loggers and telemetry", "instrument-class", "Environmental sensors",
     serves=["seed:FC-C01", "seed:DC-CAND-04"], tasks=["seed:v1-2.3.1-T1", "seed:v1-2.3.1-T2", "seed:v1-2.3.1-T3"], vendor_neutral=True, half_life=6, risk="low",
     steward="FC", trig=("vendor", "security"), derived=[REF("v1:2.3.1", "sensor hardware named in v1 2.3.1")], evidence="J",
     note="Maintenance budgets are often omitted from capital grants (FC FT-09).")
tool("low-cost-air-sensors", "Low-cost air sensors and community monitoring networks", "instrument-class", "Environmental sensors",
     serves=["seed:FC-C01", "seed:DB-C13"], vendor_neutral=True, maturity="growing", half_life=3, risk="medium", steward="FC", trig=("vendor", "policy"), evidence="J",
     note="Colocation with reference monitors and humidity correction are the durable checks (FC FT-10).")
tool("reference-air-monitors", "Reference-grade ambient air monitors", "instrument-class", "Environmental sensors", serves=["seed:DB-C13"],
     vendor_neutral=True, half_life=10, risk="low", steward="FC", trig=("policy",), evidence="J",
     note="Designation of reference and equivalent methods is set by L5 instruments.")
tool("water-quality-field-meters", "Water-quality field meters, multiparameter sondes and flow meters", "instrument-class", "Field measurement instruments",
     serves=["seed:v1-4.1.3", "seed:FC-C24"], vendor_neutral=True, half_life=8, risk="low", steward="FC", trig=("vendor",), evidence="J")
tool("burn-severity-products", "Satellite burn-severity and post-fire change products", "dataset-product", "Earth-observation data products",
     serves=["seed:FC-C02", "seed:v1-4.3.5", "seed:v1-2.1.2"], products=["MTBS", "RAVG"], half_life=8, risk="low", steward="FC", trig=("vendor", "policy"),
     sources=["FC-027"], note="Field verification before regulatory or treatment use stays FC (FC FT-11).")
tool("tree-planting-drones", "Tree-planting and seeding drones", "instrument-class", "Uncrewed aircraft", serves=["seed:FC-C14"],
     vendor_neutral=True, maturity="emerging", half_life=2, risk="high", lifecycle="watch", steward="FC", trig=("procurement",), evidence="S",
     note="Pilots and commercial offers; establishment evidence not verified (FC FT-12, label S).")
tool("machine-control-equipment", "Machine-controlled, teleoperated and assisted heavy equipment", "instrument-class", "Field machinery",
     serves=["seed:FC-C14", "seed:v1-4.2.1"], vendor_neutral=True, maturity="growing", half_life=5, risk="medium", steward="FC", trig=("vendor",), sources=["FC-027"])
tool("firefighting-robots", "Ground and aerial firefighting robots and autonomous suppression concepts", "instrument-class", "Field machinery",
     serves=["seed:v1-4.3.1"], vendor_neutral=True, maturity="concept", half_life=2, risk="high", lifecycle="watch", steward="FC", trig=("policy",),
     sources=["FC-012"], evidence="S", note="Horizon signal only; single-aircraft operating limits block swarms until rules change (FC FT-14, label S).")
tool("ai-field-id-apps", "AI field identification and field-assistant apps", "software-category", "Field AI assistants",
     serves=["seed:FC-C03", "seed:DC-CAND-02"], products=["Merlin Bird ID", "Pl@ntNet", "Seek by iNaturalist"], vendor_neutral=True, maturity="growing",
     half_life=2, risk="high", steward="FC", trig=("model", "vendor"), sources=["FC-053"],
     note="Risk that novices stop forming identification judgment (FC FT-16); verification stays with FC-C03 and DC-CAND-13.")
tool("vegetation-risk-analytics", "Utility vegetation and tree-risk analytics", "software-category", "Asset risk analytics",
     serves=["seed:FC-C26", "seed:FC-C02"], vendor_neutral=True, maturity="growing", half_life=3, risk="medium", steward="FC", trig=("vendor", "policy"),
     sources=["FC-064"], note="Field verification and documented overrides feed model correction (FC FT-18).")
tool("field-communication-devices", "Satellite messengers, satellite phones and field radios", "instrument-class", "Field communication",
     serves=["seed:v1-4.4.5"], vendor_neutral=True, half_life=5, risk="medium", steward="FC", trig=("vendor", "security"), evidence="J",
     derived=[REF("v1:2.3.5", "communication equipment named in v1 2.3.5 (merged into 4.4.5)")])
tool("forest-mensuration-instruments", "Forest mensuration instruments", "instrument-class", "Field measurement instruments",
     serves=["seed:v1-1.3.2"], vendor_neutral=True, half_life=15, risk="low", steward="FC", trig=("vendor",), evidence="J",
     note="Increment borers, clinometers, diameter tapes, prisms and laser rangefinders.")

# ================================================================== PS reporting tools and technical standards (steward PS)
tool("esg-ehs-reporting-software", "ESG and EHS data and reporting software", "software-category", "Sustainability reporting",
     serves=["seed:SC-C15", "seed:DB-C26"], products=["Workiva", "Diligent ESG", "Sphera", "Cority", "Enablon", "Intelex", "Persefoni"],
     other_names=["Watershed (carbon accounting software)"], vendor_neutral=True, maturity="growing", half_life=3, risk="medium", steward="PS",
     trig=("vendor", "policy"), sources=["PS-023", "PS-018"], derived=[REF("v1:3.6.2:foundational:I3")],
     note="Vendors market these tools as replacements for junior and consultant labour [E: PS-023, vendor view].")
tool("environmental-data-management-systems", "Environmental data management systems for site and monitoring data", "software-category", "Environmental data management",
     serves=["seed:v1-2.2.1", "seed:DC-CAND-06"], products=["EQuIS"], vendor_neutral=True, half_life=8, risk="low", steward="PS", trig=("vendor",),
     note="Private postings screen on these names (ADR-0003 PS dissent).")
tool("lca-software", "Life-cycle assessment software and inventory databases", "software-category", "Life-cycle assessment",
     serves=["seed:v1-3.7.3"], products=["SimaPro", "GaBi", "openLCA", "ecoinvent"], vendor_neutral=True, half_life=6, risk="low", steward="PS",
     trig=("vendor", "standard"), derived=[REF("v1:3.7.3:foundational:I3")])
tool("ghg-protocol", "GHG Protocol corporate, scope 3 and product standards", "technical-standard", "GHG accounting standards",
     serves=["seed:SC-C15"], products=["GHG Protocol"], vendor_neutral=True, half_life=5, risk="medium", steward="PS", trig=("standard", "policy"),
     note="ADR-0003 T-7 example of a practitioner-chosen technical standard (L4). Also serves PS-C07 and PS-C09 when authored.")
tool("iso-14064", "ISO 14064 greenhouse gas quantification and verification standards", "technical-standard", "GHG accounting standards",
     serves=["seed:SC-C15"], products=["ISO 14064"], vendor_neutral=True, half_life=6, risk="low", steward="PS", trig=("standard",),
     note="Also serves PS-C07 (independent GHG verification) when authored.")
tool("gri-standards", "GRI sustainability reporting standards", "reporting-framework", "Sustainability reporting frameworks",
     serves=["seed:SC-C15"], products=["GRI Standards"], vendor_neutral=True, half_life=5, risk="medium", steward="PS", trig=("standard",),
     derived=[REF("v1:3.6.2", "framework named in v1 3.6.2 title; moved to L4 per v1_disposition")])
tool("sasb-standards", "SASB industry-based disclosure standards", "reporting-framework", "Sustainability reporting frameworks",
     serves=["seed:SC-C15"], products=["SASB Standards"], vendor_neutral=True, half_life=4, risk="medium", steward="PS", trig=("standard",),
     derived=[REF("v1:3.6.2", "framework named in v1 3.6.2 title; moved to L4 per v1_disposition")])
tool("issb-standards", "ISSB sustainability disclosure standards", "reporting-framework", "Sustainability reporting frameworks",
     serves=["seed:SC-C15"], products=["IFRS S1", "IFRS S2", "ISSB"], vendor_neutral=True, maturity="growing", half_life=4, risk="medium", steward="PS",
     trig=("standard", "policy"), note="Jurisdictional adoption of these standards is recorded as L5 instruments where it has legal force.")
tool("tnfd-recommendations", "TNFD nature-related disclosure recommendations", "reporting-framework", "Sustainability reporting frameworks",
     serves=["seed:SC-C15"], products=["TNFD"], vendor_neutral=True, maturity="growing", half_life=3, risk="medium", steward="PS", trig=("standard",))
tool("cdp-disclosure", "CDP environmental disclosure system", "platform", "Sustainability reporting frameworks", serves=["seed:SC-C15"],
     products=["CDP"], half_life=4, risk="medium", steward="PS", trig=("vendor", "standard"))
tool("sustainability-assurance-standards", "Sustainability assurance standards", "technical-standard", "Assurance standards",
     serves=["seed:SC-C15"], products=["ISSA 5000", "ISAE 3410", "AA1000"], vendor_neutral=True, maturity="growing", half_life=5, risk="medium", steward="PS",
     trig=("standard",), note="Also serves PS-C07 (independent verification) when authored.")
tool("iso-14001", "ISO 14001 environmental management system standard", "technical-standard", "Management system standards",
     serves=["seed:DB-C26"], products=["ISO 14001"], vendor_neutral=True, half_life=8, risk="low", steward="PS", trig=("standard",))

# ------------------------------------------------------------------ write
OUT.parent.mkdir(parents=True, exist_ok=True)
ids = [r["id"] for r in ROWS]
assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
ROWS.sort(key=lambda r: r["id"])
OUT.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in ROWS), encoding="utf-8")
from collections import Counter  # noqa: E402
print("tools:", len(ROWS), dict(Counter(r["lifecycleState"] for r in ROWS)))
print("by steward:", dict(Counter(r["editorialNote"]["en"].split(" (")[0].replace("Steward: ", "") for r in ROWS)))
print("dropped refs:", DROPPED)
