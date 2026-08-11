#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from render_google_workspace_senior_attention_adapters import (  # noqa: E402
    PROJECTION_MANIFEST_REL,
    build_outputs,
    check_outputs,
    source_hash,
)
from validate_google_workspace_adapter import validate_adapter  # noqa: E402

MANIFEST = ROOT / "runtime-adapters" / "google-workspace" / "senior-attention" / "adapter-source.v1.json"
SCHEMA = ROOT / "schemas" / "runtime-adapters" / "google-workspace-adapter-manifest.v1.schema.json"
PROJECTION_SCHEMA = ROOT / "schemas" / "runtime-adapters" / "google-workspace-projection-manifest.v1.schema.json"


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
        self.assertEqual("1.1.1", self.manifest["adapter_version"])

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
        self.assertTrue(self._validate_mutation(payload))

        payload = copy.deepcopy(self.manifest)
        payload["product_assumptions"]["uniform_workspace_surface_assumed"] = True
        self.assertTrue(self._validate_mutation(payload))

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

    def test_gw2_projections_match_canonical_source(self) -> None:
        self.assertEqual([], check_outputs(ROOT, self.manifest))
        outputs = build_outputs(self.manifest)
        self.assertEqual(10, len(outputs))
        for rel in outputs:
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_projection_manifest_binds_source_and_render_hashes(self) -> None:
        projection = load_json(ROOT / PROJECTION_MANIFEST_REL)
        schema = load_json(PROJECTION_SCHEMA)
        structural = sorted(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(projection),
            key=lambda error: list(error.path),
        )
        self.assertEqual([], [error.message for error in structural])
        self.assertEqual(source_hash(self.manifest), projection["adapter_source_hash"])
        self.assertEqual("candidate", projection["authority_ceiling"])
        self.assertEqual("bounded_not_complete", projection["coverage_claim"])
        self.assertEqual(9, len(projection["files"]))
        self.assertEqual(9, len({item["path"] for item in projection["files"]}))
        self.assertEqual({"gem", "workspace_studio", "notebook"}, {item["target"] for item in projection["files"]})

    def test_runtime_projection_authority_and_source_invariants(self) -> None:
        base = ROOT / "runtime-adapters" / "google-workspace" / "senior-attention"
        gem = (base / "gem" / "gem-instructions.template.md").read_text(encoding="utf-8")
        studio = (base / "workspace-studio" / "skill-instructions.template.md").read_text(encoding="utf-8")
        studio_flow = (base / "workspace-studio" / "manual-shadow-flow.template.yaml").read_text(encoding="utf-8")
        notebook = (base / "notebook" / "notebook-custom-chat.template.md").read_text(encoding="utf-8")
        for text in (gem, studio, notebook):
            self.assertIn("candidate", text.lower())
            self.assertIn("UNKNOWN", text)
            self.assertIn("counterevidence", text.lower())
            self.assertIn("complete enterprise search", text.lower())
            self.assertIn("receiving coding workspace owns capability discovery", text.lower())
            self.assertIn("independently verify", text.lower())
        self.assertIn("automatic_actions: false", studio_flow)
        self.assertIn("authority_ceiling: candidate", studio_flow)
        self.assertIn("coverage_claim: bounded_not_complete", studio_flow)
        self.assertIn("draft_candidate_and_required_verification", studio_flow)

    def test_renderer_cli_check_succeeds(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPTS / "render_google_workspace_senior_attention_adapters.py"), "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("deterministic projection", completed.stdout)

    def test_renderer_detects_projection_drift(self) -> None:
        outputs = build_outputs(self.manifest)
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            for rel, text in outputs.items():
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
            target = root / "runtime-adapters/google-workspace/senior-attention/gem/starter-prompts.md"
            target.write_text(target.read_text(encoding="utf-8") + "drift\n", encoding="utf-8")
            errors = check_outputs(root, self.manifest)
            self.assertTrue(any("generated projection drift" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
