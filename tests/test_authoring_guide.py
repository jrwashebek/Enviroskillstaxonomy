"""The minimal examples in docs/standard/AUTHORING_GUIDE.md stay valid against the generated schema."""
from __future__ import annotations

import json
import re

import pytest
from jsonschema import Draft202012Validator

from conftest import L

GUIDE = (L.ROOT / "docs" / "standard" / "AUTHORING_GUIDE.md").read_text(encoding="utf-8")
SCHEMA = json.loads(L.SCHEMA_OUT.read_text(encoding="utf-8"))
V = Draft202012Validator(SCHEMA)


def blocks(lang):
    return re.findall(r"```" + lang + r"\n(.*?)```", GUIDE, flags=re.S)


def fill(text):
    text = re.sub(r"textSha256: <[^>\n]*>", "textSha256: " + L.text_sha256("Brief a field crew on site hazards and escape routes before work begins"), text)
    text = text.replace("<hash of the exact statement you rated>", L.text_sha256("Brief a field crew on site hazards and escape routes before work begins"))
    return re.sub(r"<[^<>\n]*>", "placeholder", text)


YAML_EXAMPLES = [b for b in blocks("yaml") if b.lstrip().startswith("id:")]
JSON_EXAMPLES = blocks("json")


def test_guide_has_examples():
    assert len(YAML_EXAMPLES) >= 3 and JSON_EXAMPLES


@pytest.mark.parametrize("i", range(len(YAML_EXAMPLES)))
def test_yaml_example_validates(i):
    rec = L.load_yaml_text(fill(YAML_EXAMPLES[i]))
    assert [e.message for e in V.iter_errors(rec)] == []


@pytest.mark.parametrize("i", range(len(JSON_EXAMPLES)))
def test_json_example_validates(i):
    rec = json.loads(fill(JSON_EXAMPLES[i]))
    assert [e.message for e in V.iter_errors(rec)] == []
