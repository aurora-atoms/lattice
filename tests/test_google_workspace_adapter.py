#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_google_workspace_adapter import validate_adapter  # noqa: E402

MANIFEST = ROOT / "runtime-adapters" / "google-workspace" / "senior-attention" / "adapter-source.v1.json"
SCHEMA = ROOT / "schemas" / "runtime-adapters" / "google-workspace-adapter-manifest.v1.schema.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class GoogleWorkspaceAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = load_json(MANIFEST)
        self.schema = load_json(SCHEMA)

    def _validate_mutation(self, payload: dict) -> list[str]:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "adapter.json"
            path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            return validate_adapter(path, ROOT, SCHEMA)

    def test_manifest_is_structurally_and_semantically_valid(self) -> None:
        structural = sorted(
            Draft202012Validator(self.schema, format_checker=FormatChecker()).iter_errors(self.manifest),
            key=lambda error: list(error.path),
        )
        self.assertEqual([], [error.message for error in structural])
        self.assertEqual([], validate_adapter(MANIFEST, ROOT, SCHEMA))

    def test_contract_is_one_source_for_three_candidate_only_targets(self) -> None:
        self.assertEqual("lat.google_workspace_senior_attention_adapter.v1", self.manifest["contract"])
        self.assertEqual("google-workspace-senior-attention", self.manifest["adapter_id"])
        targets = {item["target"]: item for item in self.manifest["targets"]}
        self.assertEqual({"gem", "workspace_studio", "notebook"}, set(targets))
        for item in targets.values():
            self.assertEqual("unknown", item["availability"])
            self.assertEqual("candidate", item["authority_ceiling"])
        self.assertFalse(self.manifest["authority"]["public_writeback_allowed"])
        self.assertFalse(self.manifest["authority"]["automatic_action_default"])

    def test_five_task_families_match_canonical_senior_attention_entry(self) -> None:
        self.assertEqual(
            {"feature_requirement", "risk", "bug", "decision", "management"},
            set(self.manifest["task_families"]),
        )
        self.assertEqual("docs/senior-attention.md", self.manifest["canonical_refs"]["senior_attention_workflow"])
        self.assertEqual(
            "workspaces/templates/senior-attention-runtime-profile.v1.json",
            self.manifest["canonical_refs"]["capability_profile"],
        )

    def test_public_contract_cannot_claim_account_specific_runtime_availability(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["targets"][0]["availability"] = "verified"
        errors = self._validate_mutation(payload)
        self.assertTrue(any("public canonical availability" in error for error in errors), errors)

    def test_authority_ceiling_cannot_expand(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["targets"][1]["authority_ceiling"] = "approved"
        errors = self._validate_mutation(payload)
        self.assertTrue(any("schema:" in error for error in errors), errors)

    def test_complete_search_and_uniform_surface_assumptions_fail_closed(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["product_assumptions"]["complete_enterprise_search_assumed"] = True
        errors = self._validate_mutation(payload)
        self.assertTrue(errors)

        payload = copy.deepcopy(self.manifest)
        payload["product_assumptions"]["uniform_workspace_surface_assumed"] = True
        errors = self._validate_mutation(payload)
        self.assertTrue(errors)

    def test_private_google_locator_is_rejected_from_public_source(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["direction_fit"]["unknowns"].append("private source https://drive.google.com/drive/folders/example")
        errors = self._validate_mutation(payload)
        self.assertTrue(any("private/account-specific locator" in error for error in errors), errors)

    def test_handoff_cannot_drop_counterevidence_or_unknowns(self) -> None:
        payload = copy.deepcopy(self.manifest)
        payload["handoff"]["required_sections"].remove("strongest_counterevidence")
        errors = self._validate_mutation(payload)
        self.assertTrue(any("handoff required_sections" in error for error in errors), errors)

        payload = copy.deepcopy(self.manifest)
        payload["handoff"]["required_sections"].remove("unknowns")
        errors = self._validate_mutation(payload)
        self.assertTrue(any("handoff required_sections" in error for error in errors), errors)

    def test_no_google_specific_task_skill_agent_or_module_is_created(self) -> None:
        self.assertFalse((ROOT / "skills" / "google-workspace-senior-attention").exists())
        self.assertFalse((ROOT / "agents" / "google-workspace-senior-attention").exists())
        self.assertFalse((ROOT / "modules" / "google-workspace-senior-attention").exists())

    def test_gw1_stops_before_runtime_specific_projection_templates(self) -> None:
        base = ROOT / "runtime-adapters" / "google-workspace" / "senior-attention"
        self.assertFalse((base / "gem").exists())
        self.assertFalse((base / "workspace-studio").exists())
        self.assertFalse((base / "notebook").exists())
        self.assertEqual(
            "generated_in_later_adapter_stage",
            self.manifest["progressive_disclosure"]["runtime_specific_projection"],
        )


if __name__ == "__main__":
    unittest.main()
