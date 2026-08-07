from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
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
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

PROFILE = ROOT / "examples" / "capability-profiles" / "pr-review-runtime-profile.v1.json"


class CapabilityProfileRuntimeTests(unittest.TestCase):
    def load_profile(self) -> dict[str, object]:
        return json.loads(PROFILE.read_text(encoding="utf-8"))

    def validate_mutation(self, mutate) -> list[str]:
        record = self.load_profile()
        mutate(record)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "profile.json"
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            errors, _ = MODULE.validate_profile(path, ROOT)
        return errors

    def test_committed_profile_is_valid(self) -> None:
        errors, warnings = MODULE.validate_profile(PROFILE, ROOT)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_agent_cannot_own_profile_runtime_controls(self) -> None:
        def mutate(record: dict[str, object]) -> None:
            bindings = record["agent_bindings"]
            assert isinstance(bindings, list)
            binding = bindings[0]
            assert isinstance(binding, dict)
            responsibilities = binding["responsibilities"]
            assert isinstance(responsibilities, list)
            responsibilities.append("model_routing")

        errors = self.validate_mutation(mutate)
        self.assertTrue(
            any("profile-owned responsibilities" in error for error in errors), errors
        )

    def test_economy_model_cannot_gain_judgment_authority(self) -> None:
        def mutate(record: dict[str, object]) -> None:
            routing = record["model_routing"]
            assert isinstance(routing, dict)
            lanes = routing["lanes"]
            assert isinstance(lanes, list)
            economy = lanes[0]
            assert isinstance(economy, dict)
            economy["max_authority"] = "judged"

        errors = self.validate_mutation(mutate)
        self.assertTrue(
            any("must be candidate for economy" in error for error in errors), errors
        )

    def test_model_consensus_cannot_replace_evidence(self) -> None:
        def mutate(record: dict[str, object]) -> None:
            verification = record["verification"]
            assert isinstance(verification, dict)
            verification["model_consensus_is_not_proof"] = False

        errors = self.validate_mutation(mutate)
        self.assertTrue(
            any("model consensus is not proof" in error for error in errors), errors
        )

    def test_cache_cannot_be_shared_across_models(self) -> None:
        def mutate(record: dict[str, object]) -> None:
            cache = record["cache"]
            assert isinstance(cache, dict)
            cache["cross_model_reuse"] = True

        errors = self.validate_mutation(mutate)
        self.assertTrue(
            any("cross_model_reuse must be false" in error for error in errors), errors
        )

    def test_human_outcomes_must_remain_hypotheses(self) -> None:
        def mutate(record: dict[str, object]) -> None:
            human = record["human_factors"]
            assert isinstance(human, dict)
            human["evidence_status"] = "proven"

        errors = self.validate_mutation(mutate)
        self.assertTrue(
            any("must remain hypotheses" in error for error in errors), errors
        )

    def test_public_profile_denies_high_impact_writes(self) -> None:
        def mutate(record: dict[str, object]) -> None:
            permissions = record["permissions"]
            assert isinstance(permissions, dict)
            permissions["merge"] = True

        errors = self.validate_mutation(mutate)
        self.assertTrue(any("permissions.merge" in error for error in errors), errors)

    def test_handoff_cannot_treat_full_reasoning_as_authoritative(self) -> None:
        def mutate(record: dict[str, object]) -> None:
            handoff = record["handoff"]
            assert isinstance(handoff, dict)
            handoff["full_reasoning_transcript_authoritative"] = True

        errors = self.validate_mutation(mutate)
        self.assertTrue(
            any("must not be authoritative handoffs" in error for error in errors), errors
        )


if __name__ == "__main__":
    unittest.main()
