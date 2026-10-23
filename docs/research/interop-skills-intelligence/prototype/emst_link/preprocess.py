"""Query-side preprocessing designed from dev-set failures (see report §Prototype). Scored on the held-out set.

1. Plan acronym glossary: land-management plans lean on acronyms that never appear in v1 competency text.
   Expansions are appended (not substituted) so the original token still counts.
2. Proper-name masking: agency and place names ("Wyoming Game and Fish Department", "Garden Creek",
   "Bull Run") produced false lexical anchors (fish -> fisheries, creek -> aquatic). Masked to a neutral token.
"""
import re

ACRONYMS = {
    "BMP": "best management practices water quality protection", "BMPS": "best management practices water quality protection",
    "SMZ": "streamside management zone riparian buffer water quality", "RMZ": "riparian management zone",
    "RMA": "riparian management area", "RMAS": "riparian management areas", "RHCA": "riparian habitat conservation area",
    "AUM": "animal unit month livestock grazing forage", "AUMS": "animal unit months livestock grazing forage",
    "ASQ": "allowable sale quantity timber harvest volume", "LTSY": "long-term sustained yield timber",
    "MMBF": "million board feet timber volume", "MBF": "thousand board feet timber volume", "CCF": "hundred cubic feet timber volume",
    "NRV": "natural range of variation", "LWD": "large woody debris stream habitat", "PFC": "proper functioning condition riparian",
    "TES": "threatened endangered sensitive species", "SCC": "species of conservation concern", "MIS": "management indicator species",
    "RNA": "research natural area", "IRA": "inventoried roadless area", "IRAS": "inventoried roadless areas",
    "WSR": "wild and scenic river", "VQO": "visual quality objective scenery", "SIO": "scenic integrity objective scenery",
    "ROS": "recreation opportunity spectrum", "WUI": "wildland urban interface wildfire", "LOP": "limited operating period wildlife disturbance",
    "OHV": "off-highway vehicle motorized recreation", "ORV": "off-road vehicle motorized recreation",
    "NHPA": "national historic preservation act cultural heritage resources", "TMDL": "total maximum daily load water quality",
    "BASI": "best available scientific information", "HUC": "hydrologic unit watershed", "GNA": "good neighbor authority agreement",
    "ESA": "endangered species act consultation", "NEPA": "national environmental policy act environmental review",
    "EIS": "environmental impact statement", "CWA": "clean water act water quality", "MER": "monitoring evaluation report",
}
# case-sensitive (plan acronyms are printed in capitals), optional plural "s"
ACR_RE = re.compile(r"\b(" + "|".join(sorted(ACRONYMS, key=len, reverse=True)) + r")s?\b")

PLACE = re.compile(r"\b(?:[A-Z][a-z]+\s){1,3}(?:Creek|River|Lake|Basin|Peak|Mountains?|Canyon|Run|Ridge|Pass|Gulch|Fork|Division|Ranger District|National Forests?|Wilderness)\b")
AGENCY = re.compile(r"\b(?:[A-Z][a-z]+\s){0,3}(?:Game and Fish|Fish and Game|Fish,? Wildlife(?: and Parks)?|Fish and Wildlife|Parks and Wildlife|Natural Heritage Program)(?:\s(?:Department|Commission|Service|Program))?\b"
                    r"|\b(?:Department|Dept\.?) of [A-Z][a-z]+(?: (?:and|of) [A-Z][a-z]+)*\b"
                    r"|\b(?:Federal Highway Administration|Northwest Power Planning Council)\b")


def expand_acronyms(text):
    extra = sorted({ACRONYMS[m.group(1)] for m in ACR_RE.finditer(text) if m.group(1) in ACRONYMS})
    return text + (" " + " ".join(extra) if extra else "")


def mask_names(text):
    text = AGENCY.sub(" partner-agency ", text)
    return PLACE.sub(" place-name ", text)


def prep(text):
    return expand_acronyms(mask_names(text))
