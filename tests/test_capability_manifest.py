from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_capability_manifest.py"
SPEC = importlib.util.spec_from_file_location("validate_capability_manifest", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def entry() -> dict:
    return {
        "capability_id": "skill:demo@1.0.0",
        "record_type": "skill",
        "family_name": "demo",
        "version": "1.0.0",
        "capability_role": "atomic_capability",
        "public_package_status": "contract_validated",
        "path": "skills/demo/SKILL.md",
        "description": "Validate a demo capability request into a bounded demo result.",
        "changes": "a demo request into a bounded result",
        "primary_user": "demo agent",
        "secondary_audience": ["reviewer"],
        "trigger": "a demo capability request arrives",
        "minimum_inputs": ["demo request"],
        "outputs": ["demo result"],
        "evidence_contract": {
            "required_sections": ["facts"],
            "policy": "cite facts",
        },
        "success_signals": ["demo result validates"],
        "stop_conditions": ["goal_reached"],
        "authority_boundary": "no approval authority",
        "compatibility": {
            "semantic_versioning": True,
            "legacy_status_field": "experimental",
            "migration": "use public package status",
        },
        "deprecated_by": None,
        "projection": {
            "source_registry": "registry/skills.index.jsonl",
            "context_catalog": "registry/skill-context.catalog.json",
            "legacy_record": {"status": "experimental"},
        },
    }


class CapabilityManifestTests(unittest.TestCase):
    def prepare(self, root: Path) -> None:
        (root / "skills" / "demo").mkdir(parents=True)
        (root / "skills" / "demo" / "SKILL.md").write_text(
            "---\nname: demo\ndescription: Validate a demo capability request into a bounded demo result.\n---\n",
            encoding="utf-8",
        )
        (root / "registry").mkdir()
        (root / "registry" / "skills.index.jsonl").write_text("", encoding="utf-8")

    def test_valid_entry(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.prepare(root)
            self.assertEqual([], MODULE.validate_entry(entry(), root, "demo"))

    def test_identity_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.prepare(root)
            value = entry()
            value["version"] = "1.1.0"
            errors = MODULE.validate_entry(value, root, "demo")
            self.assertTrue(any("capability_id must equal" in item for item in errors))

    def test_missing_path_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.prepare(root)
            value = entry()
            value["path"] = "skills/missing/SKILL.md"
            errors = MODULE.validate_entry(value, root, "demo")
            self.assertTrue(any("path does not exist" in item for item in errors))

    def test_description_trigger_conflict_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.prepare(root)
            value = entry()
            value["trigger"] = "unrelated satellite telemetry arrives"
            errors = MODULE.validate_entry(value, root, "demo")
            self.assertTrue(any("no shared semantic term" in item for item in errors))

    def test_public_manifest_rejects_adoption_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.prepare(root)
            value = entry()
            value["projection"]["legacy_record"][
                "downstream_adoption_status"
            ] = "used_once"
            errors = MODULE.validate_entry(value, root, "demo")
            self.assertTrue(any("must not contain downstream adoption" in item for item in errors))

    def test_missing_role_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.prepare(root)
            value = entry()
            del value["capability_role"]
            errors = MODULE.validate_entry(value, root, "demo")
            self.assertTrue(any("missing fields" in item for item in errors))

    def test_empty_outputs_fail_structural_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.prepare(root)
            value = entry()
            value["outputs"] = []
            errors = MODULE.validate_entry(value, root, "demo")
            self.assertTrue(any("outputs must be a non-empty" in item for item in errors))

    def test_malformed_evidence_contract_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.prepare(root)
            value = entry()
            value["evidence_contract"] = {"required_sections": [], "policy": ""}
            errors = MODULE.validate_entry(value, root, "demo")
            self.assertTrue(any("required_sections" in item for item in errors))
            self.assertTrue(any("evidence_contract.policy" in item for item in errors))

    def test_deprecated_capability_in_active_route_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "registry").mkdir()
            (root / "registry" / "capability-routing.index.jsonl").write_text(
                json.dumps({"route_id": "demo", "skill_id": "demo"}) + "\n",
                encoding="utf-8",
            )
            value = entry()
            value["public_package_status"] = "deprecated"
            value["deprecated_by"] = "skill:replacement@1.0.0"
            errors = MODULE.deprecated_reference_errors(root, [value])
            self.assertTrue(any("references deprecated capability" in item for item in errors))

    def test_projection_drift_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / "registry", root / "registry")
            manifest = MODULE.load_json(root / "registry" / "capability-manifest.json")
            policy_path = root / "registry" / "capability-context-policy.json"
            policy = MODULE.load_json(policy_path)
            policy["skill_versions"]["lattice-governor"] = "9.9.9"
            policy_path.write_text(json.dumps(policy), encoding="utf-8")
            errors = MODULE.projection_errors(root, manifest)
            self.assertTrue(any("capability-context-policy.json" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
