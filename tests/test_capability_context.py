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
        "contract_version":"1.1.0",
        "default_version":"1.0.0",
        "breaking_change_policy":"semantic_versioning",
        "optional_context_discovery":"Discover the smallest related capability or source for the named gap.",
        "run_result_contract":{"schema":"run-result.schema.json","record_type":"lat.capability.run_result.v1","writeback_pattern":"artifacts/capability-runs/<capability-name>/<run-id>/run-result.json","visible_artifact_required":True,"inline_fallback":"Return structured result inline when write permission is unavailable."},
        "evidence_contract":{"required_sections":["facts","inference_summary","citations","uncertainty","unknowns","assumptions"],"policy":"Separate facts and inference."},
        "success_contract":{"required":True,"result_enum":["met","not_met","not_evaluated"],"policy":"Evaluate success from evidence."},
        "stop_contract":{"default_retry_budget":1,"stage_gate_by_default":True,"continue_to_final_goal_only_when_explicitly_requested":True,"reasons":["goal_reached","stage_gate_reached","retry_budget_exhausted","missing_permission","missing_required_input","source_unavailable","insufficient_evidence","high_risk_boundary","human_decision_required","explicit_user_stop","failed_validation"],"policy":"Stop at the next reviewable stage or evidence boundary."},
        "skills" if kind=="skill" else "agents":[entry],
    }


def entry(name: str="demo") -> dict:
    return {"name":name,"changes":"an unclear request into a bounded result","primary_user":"delivery agent","secondary_audience":["reviewer"],"trigger":"a bounded result is requested","minimum":["task request"],"outputs":["bounded result"],"runtime_targets":["codex"]}


def prepare(root: Path) -> None:
    (root/"skills/demo").mkdir(parents=True)
    (root/"skills/demo/SKILL.md").write_text("# Demo",encoding="utf-8")
    (root/"run-result.schema.json").write_text("{}",encoding="utf-8")


class CapabilityContextTests(unittest.TestCase):
    def test_valid_skill_catalog(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); prepare(root)
            path=root/"skills.json"; path.write_text(json.dumps(catalog("skill",entry())),encoding="utf-8")
            errors,records=validator.validate_catalog(path,root,"skill")
            self.assertEqual([],errors); self.assertEqual(1,len(records))

    def test_missing_trigger_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); prepare(root)
            value=entry(); value["trigger"]=""
            path=root/"skills.json"; path.write_text(json.dumps(catalog("skill",value)),encoding="utf-8")
            errors,_=validator.validate_catalog(path,root,"skill")
            self.assertTrue(any("trigger must be non-empty" in item for item in errors))

    def test_missing_run_contract_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); prepare(root)
            value=catalog("skill",entry()); del value["run_result_contract"]
            path=root/"skills.json"; path.write_text(json.dumps(value),encoding="utf-8")
            errors,_=validator.validate_catalog(path,root,"skill")
            self.assertTrue(any("run_result_contract is required" in item for item in errors))

    def test_incomplete_evidence_contract_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); prepare(root)
            value=catalog("skill",entry()); value["evidence_contract"]["required_sections"]=["facts"]
            path=root/"skills.json"; path.write_text(json.dumps(value),encoding="utf-8")
            errors,_=validator.validate_catalog(path,root,"skill")
            self.assertTrue(any("evidence required_sections" in item for item in errors))

    def test_unbounded_retry_policy_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); prepare(root)
            value=catalog("skill",entry()); value["stop_contract"]["default_retry_budget"]=-1
            path=root/"skills.json"; path.write_text(json.dumps(value),encoding="utf-8")
            errors,_=validator.validate_catalog(path,root,"skill")
            self.assertTrue(any("default_retry_budget" in item for item in errors))


if __name__=="__main__":
    unittest.main()
