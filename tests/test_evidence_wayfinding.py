from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

SPEC = importlib.util.spec_from_file_location(
    "validate_capability_profile",
    SCRIPTS / "validate_capability_profile.py",
)
assert SPEC and SPEC.loader
PROFILE_VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROFILE_VALIDATOR)

PROFILE = (
    ROOT
    / "examples"
    / "capability-profiles"
    / "senior-decision-wayfinding-runtime-profile.v1.json"
)
PACK = (
    ROOT
    / "examples"
    / "evidence-wayfinding"
    / "portable-case-pack.synthetic.v1.json"
)
SCHEMA = ROOT / "schemas" / "capability" / "portable-case-pack.v1.schema.json"
WORKFLOW = ROOT / "docs" / "evidence-wayfinding.md"
FRONTIER_SKILL = ROOT / "skills" / "frontier-practice-scout" / "SKILL.md"


class EvidenceWayfindingTests(unittest.TestCase):
    def load_pack(self) -> dict[str, object]:
        return json.loads(PACK.read_text(encoding="utf-8"))

    def test_runtime_profile_satisfies_capability_profile_boundary(self) -> None:
        errors, warnings = PROFILE_VALIDATOR.validate_profile(PROFILE, ROOT)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_public_profile_is_read_only_and_does_not_promote_frontier_skill(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        permissions = profile["permissions"]
        self.assertTrue(permissions["repository_read"])
        for key in ["repository_write", "merge", "deploy", "secret_access"]:
            self.assertFalse(permissions[key], key)
        skill_ids = {item["skill_id"] for item in profile["skills"]}
        self.assertNotIn("frontier-practice-scout", skill_ids)
        self.assertFalse(FRONTIER_SKILL.exists())

    def test_portable_case_pack_has_closed_contract_shape(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        pack = self.load_pack()
        self.assertEqual("lat.portable_case_pack.v1", pack["contract"])
        self.assertEqual("lat.goal.verified-decision-yield.v1", pack["mission_anchor_ref"])
        self.assertEqual("public", pack["data_classification"])
        self.assertFalse(schema["additionalProperties"])
        for field in schema["required"]:
            self.assertIn(field, pack)
        self.assertEqual(
            {"observed", "derived", "judged", "unknown"},
            set(pack["claims"]),
        )

    def test_every_claim_reference_resolves_to_pack_evidence(self) -> None:
        pack = self.load_pack()
        evidence_ids = {item["id"] for item in pack["evidence_refs"]}
        for bucket in pack["claims"].values():
            for claim in bucket:
                for ref in claim["evidence_refs"]:
                    self.assertIn(ref, evidence_ids)
        for counter in pack["strongest_counterevidence"]:
            for ref in counter["evidence_refs"]:
                self.assertIn(ref, evidence_ids)
        for direction in pack["rejected_directions"]:
            for ref in direction["evidence_refs"]:
                self.assertIn(ref, evidence_ids)

    def test_authoritative_pack_does_not_contain_reasoning_transcript(self) -> None:
        text = PACK.read_text(encoding="utf-8").lower()
        self.assertNotIn('"chain_of_thought"', text)
        self.assertNotIn('"reasoning_transcript"', text)
        self.assertNotIn('"full_reasoning"', text)

    def test_workflow_preserves_governed_evolution_and_stop_rules(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        required_phrases = [
            "## Mission Anchor",
            "## Ordered Workflow",
            "## Frontier Practice Scout Decision",
            "## Portable Case Pack",
            "## Governed Evolution",
            "two consecutive rounds with no new evidence",
            "not a new Lattice module",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
