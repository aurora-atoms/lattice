from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT=Path(__file__).resolve().parents[1]/"scripts/validate_capability_context.py"
spec=importlib.util.spec_from_file_location("capability_context_validator",SCRIPT)
validator=importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(validator)


def catalog(kind: str, entry: dict) -> dict:
    return {
        "contract":"lat.capability-context.v1",
        "contract_version":"1.0.0",
        "default_version":"1.0.0",
        "breaking_change_policy":"semantic_versioning",
        "optional_context_discovery":"Discover the smallest related capability or source for the named gap.",
        "skills" if kind=="skill" else "agents":[entry],
    }


def entry(name: str="demo") -> dict:
    return {
        "name":name,
        "changes":"an unclear request into a bounded result",
        "primary_user":"delivery agent",
        "secondary_audience":["reviewer"],
        "trigger":"a bounded result is requested",
        "minimum":["task request"],
        "outputs":["bounded result"],
        "runtime_targets":["codex"],
    }


class CapabilityContextTests(unittest.TestCase):
    def test_valid_skill_catalog(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/"skills/demo").mkdir(parents=True)
            (root/"skills/demo/SKILL.md").write_text("# Demo",encoding="utf-8")
            path=root/"skills.json"
            path.write_text(json.dumps(catalog("skill",entry())),encoding="utf-8")
            errors,records=validator.validate_catalog(path,root,"skill")
            self.assertEqual([],errors)
            self.assertEqual(1,len(records))

    def test_missing_trigger_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/"skills/demo").mkdir(parents=True)
            (root/"skills/demo/SKILL.md").write_text("# Demo",encoding="utf-8")
            value=entry(); value["trigger"]=""
            path=root/"skills.json"
            path.write_text(json.dumps(catalog("skill",value)),encoding="utf-8")
            errors,_=validator.validate_catalog(path,root,"skill")
            self.assertTrue(any("trigger must be non-empty" in item for item in errors))

    def test_missing_optional_discovery_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/"skills/demo").mkdir(parents=True)
            (root/"skills/demo/SKILL.md").write_text("# Demo",encoding="utf-8")
            value=catalog("skill",entry()); value["optional_context_discovery"]=""
            path=root/"skills.json"
            path.write_text(json.dumps(value),encoding="utf-8")
            errors,_=validator.validate_catalog(path,root,"skill")
            self.assertTrue(any("optional_context_discovery is required" in item for item in errors))

    def test_bad_version_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/"skills/demo").mkdir(parents=True)
            (root/"skills/demo/SKILL.md").write_text("# Demo",encoding="utf-8")
            value=catalog("skill",entry()); value["default_version"]="one"
            path=root/"skills.json"
            path.write_text(json.dumps(value),encoding="utf-8")
            errors,_=validator.validate_catalog(path,root,"skill")
            self.assertTrue(any("default_version must be semantic version" in item for item in errors))

if __name__=="__main__":
    unittest.main()
