#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from route_capabilities import route  # noqa: E402
from validate_capability_profile import validate_profile  # noqa: E402

PROFILE = ROOT / "workspaces" / "templates" / "senior-attention-runtime-profile.v1.json"
WORKFLOW = ROOT / "docs" / "senior-attention.md"
FIXTURE = ROOT / "tests" / "fixtures" / "senior-attention-entry" / "routing-cases.v1.json"
MANIFEST = ROOT / "registry" / "capability-manifest.json"
WORKSPACE_INDEX = ROOT / "registry" / "workspace_templates.index.jsonl"
CAPABILITY_INDEX = ROOT / "registry" / "capabilities.index.jsonl"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class SeniorAttentionEntrypointTests(unittest.TestCase):
    def test_profile_is_structurally_and_semantically_valid(self) -> None:
        profile = load_json(PROFILE)
        schema = load_json(ROOT / "schemas" / "capability" / "capability-profile-runtime.v1.schema.json")
        structural = sorted(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(profile),
            key=lambda error: list(error.path),
        )
        self.assertEqual([], [error.message for error in structural])

        errors, _warnings = validate_profile(PROFILE, ROOT)
        self.assertEqual([], errors)
        self.assertEqual("senior-attention-runtime", profile["profile_id"])
        self.assertEqual("1.0.0", profile["profile_version"])
        self.assertEqual("contract_validated", profile["status"])

    def test_profile_uses_progressive_activation_and_public_read_only_permissions(self) -> None:
        profile = load_json(PROFILE)
        skills = {item["skill_id"]: item for item in profile["skills"]}
        required = {
            "feature-understanding-loop",
            "context-mastery",
            "domain-context-pack",
            "delivery-rescue",
            "risk-ahead",
            "decision-question-builder",
            "unasked-questions-generator",
            "contradiction-adjudication",
            "delivery-artifact-builder",
            "management-translation",
            "senior-attention-queue",
            "feature-outcome-review",
        }
        self.assertTrue(required.issubset(skills))
        self.assertEqual("on_demand", skills["delivery-capability-conductor"]["activation"])
        self.assertFalse(any(item["activation"] == "implicit" for item in profile["skills"]))
        self.assertEqual("explicit", skills["decision-question-builder"]["activation"])
        self.assertTrue(profile["permissions"]["repository_read"])
        for field in ("repository_write", "merge", "deploy", "secret_access"):
            self.assertFalse(profile["permissions"][field])
        self.assertEqual(0, profile["token_budget"]["max_always_loaded_knowledge"])

    def test_workflow_is_one_canonical_entry_not_a_second_fact_system(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        for heading in (
            "Feature Requirement / Work Ready",
            "Risk Preflight",
            "Bug / Delivery Rescue",
            "Decision Support",
            "Management Translation",
        ):
            self.assertIn(heading, text)
        for state in (
            "INTAKE",
            "CONTEXT_READY",
            "INVESTIGATING",
            "DECISION_READY",
            "WORK_READY",
            "SETTLED",
            "BLOCKED",
            "ESCALATED",
        ):
            self.assertIn(state, text)
        self.assertIn("feature_delivery_case", text)
        self.assertIn("Public / Private Boundary", text)
        self.assertIn("Decision Strip, Decision Card, and Evidence Map are projections", text)
        self.assertIn("scripts/route_capabilities.py` only as a compatibility or evaluation fallback", text)

    def test_workflow_and_profile_are_registered_in_canonical_manifest(self) -> None:
        manifest = load_json(MANIFEST)
        by_id = {item["capability_id"]: item for item in manifest["capabilities"]}
        workflow = by_id["workspace:senior-attention-workflow@1.0.0"]
        profile = by_id["workspace:senior-attention-runtime@1.0.0"]

        self.assertEqual("reference_workflow", workflow["capability_role"])
        self.assertEqual("docs/senior-attention.md", workflow["path"])
        self.assertEqual("contract_validated", workflow["public_package_status"])
        self.assertEqual("capability_profile", profile["capability_role"])
        self.assertEqual(
            "workspaces/templates/senior-attention-runtime-profile.v1.json",
            profile["path"],
        )
        self.assertEqual("contract_validated", profile["public_package_status"])

        workspace_rows = {row["workspace_id"]: row for row in load_jsonl(WORKSPACE_INDEX)}
        self.assertIn("senior-attention-workflow@1.0.0", workspace_rows)
        self.assertIn("senior-attention-runtime@1.0.0", workspace_rows)

        capability_rows = {row["capability_id"]: row for row in load_jsonl(CAPABILITY_INDEX)}
        self.assertEqual(
            "reference_workflow",
            capability_rows["workspace:senior-attention-workflow@1.0.0"]["capability_role"],
        )
        self.assertEqual(
            "capability_profile",
            capability_rows["workspace:senior-attention-runtime@1.0.0"]["capability_role"],
        )

    def test_five_positive_fallback_probes_are_discoverable(self) -> None:
        fixture = load_json(FIXTURE)
        self.assertEqual("synthetic_reference", fixture["simulation_status"])
        self.assertEqual("not_observed", fixture["downstream_adoption_status"])
        for case in fixture["positive"]:
            with self.subTest(family=case["family"]):
                result = route(ROOT, case["request"], "", "assist")
                self.assertNotEqual("no_match", result["status"])
                self.assertTrue(result["selected"])
                self.assertEqual(case["expected_skill"], result["selected"][0]["skill_id"])

    def test_negative_probes_do_not_force_senior_attention(self) -> None:
        fixture = load_json(FIXTURE)
        for case in fixture["negative"]:
            with self.subTest(request=case["request"]):
                result = route(ROOT, case["request"], "", "assist")
                self.assertEqual("no_match", result["status"])
                self.assertEqual([], result["selected"])

    def test_no_senior_attention_mega_skill_or_agent_is_created(self) -> None:
        self.assertFalse((ROOT / "skills" / "senior-attention").exists())
        self.assertFalse((ROOT / "agents" / "senior-attention").exists())


if __name__ == "__main__":
    unittest.main()
