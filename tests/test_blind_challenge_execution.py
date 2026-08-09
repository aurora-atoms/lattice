from __future__ import annotations

import copy
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


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BLIND = load_module(
    "validate_blind_challenge_execution",
    SCRIPTS / "validate_blind_challenge_execution.py",
)
SCHEMA_VALIDATOR = load_module(
    "validate_json_schema_instance_blind",
    SCRIPTS / "validate_json_schema_instance.py",
)

CASE_DIR = ROOT / "examples" / "evidence-wayfinding" / "case-0-schema-parity"
CANDIDATE = CASE_DIR / "harness-mutation-candidate.json"
BLOCKED = CASE_DIR / "blind-challenge-execution.blocked.json"
EVALUATED = ROOT / "tests" / "fixtures" / "evidence-wayfinding" / "blind-challenge" / "evaluated.synthetic-conformance.json"
SCHEMA = ROOT / "schemas" / "capability" / "blind-challenge-execution.v1.schema.json"


class BlindChallengeExecutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.candidate = BLIND.load_json(CANDIDATE)
        self.blocked = BLIND.load_json(BLOCKED)
        self.evaluated = BLIND.load_json(EVALUATED)

    def validate(self, execution):
        return BLIND.validate_execution(copy.deepcopy(execution), copy.deepcopy(self.candidate))

    def test_blocked_public_preflight_is_structurally_valid(self) -> None:
        self.assertEqual([], SCHEMA_VALIDATOR.validate_instance(SCHEMA, BLOCKED))

    def test_synthetic_evaluated_fixture_is_structurally_valid(self) -> None:
        self.assertEqual([], SCHEMA_VALIDATOR.validate_instance(SCHEMA, EVALUATED))

    def test_blocked_public_preflight_is_semantically_valid(self) -> None:
        self.assertEqual([], self.validate(self.blocked))

    def test_synthetic_evaluated_fixture_is_semantically_valid(self) -> None:
        self.assertEqual([], self.validate(self.evaluated))

    def test_frozen_target_hash_detects_candidate_target_drift(self) -> None:
        execution = copy.deepcopy(self.blocked)
        execution["frozen_plan"]["target_hash"] = "sha256:" + "1" * 64
        errors = self.validate(execution)
        self.assertTrue(any("target_hash" in error for error in errors))

    def test_frozen_allocation_hash_detects_case_bank_drift(self) -> None:
        execution = copy.deepcopy(self.blocked)
        execution["frozen_plan"]["case_allocations_hash"] = "sha256:" + "2" * 64
        errors = self.validate(execution)
        self.assertTrue(any("case_allocations_hash" in error for error in errors))

    def test_blocked_execution_cannot_emit_verdict_or_mapping(self) -> None:
        execution = copy.deepcopy(self.blocked)
        execution["decision"] = {
            "verdict": "continue_shadow",
            "rationale": "not allowed while reserved oracle is unavailable",
            "human_approval_required": True,
            "team_available_allowed": False,
        }
        execution["variant_mapping"] = {
            "A": "incumbent.syntax-plus-semantic",
            "B": "challenger.schema-instance-parity-gate",
            "revealed_at": "2026-08-09T03:51:00Z",
        }
        errors = self.validate(execution)
        self.assertTrue(any("blocked execution cannot emit" in error for error in errors))
        self.assertTrue(any("blocked execution cannot reveal" in error for error in errors))

    def test_evaluated_execution_requires_every_frozen_case(self) -> None:
        execution = copy.deepcopy(self.evaluated)
        execution["case_results"].pop()
        errors = self.validate(execution)
        self.assertTrue(any("missing case results" in error for error in errors))

    def test_evaluated_execution_requires_reserved_attestation(self) -> None:
        execution = copy.deepcopy(self.evaluated)
        execution["reserved_oracle"]["status"] = "unavailable"
        execution["reserved_oracle"].pop("attestation_ref")
        errors = self.validate(execution)
        self.assertTrue(any("requires reserved oracle attestation" in error for error in errors))
        self.assertTrue(any("requires attestation_ref" in error for error in errors))

    def test_variant_mapping_must_match_candidate_and_be_revealed_after_eval(self) -> None:
        execution = copy.deepcopy(self.evaluated)
        execution["variant_mapping"]["A"] = "unknown.variant"
        execution["variant_mapping"]["revealed_at"] = "2026-08-09T03:49:00Z"
        errors = self.validate(execution)
        self.assertTrue(any("map A/B exactly" in error for error in errors))
        self.assertTrue(any("revealed_at" in error for error in errors))

    def test_critical_protected_failure_cannot_continue_or_canary(self) -> None:
        execution = copy.deepcopy(self.evaluated)
        execution["case_results"][0]["protected_metrics"][0]["status"] = "fail"
        execution["decision"]["verdict"] = "continue_shadow"
        errors = self.validate(execution)
        self.assertTrue(any("critical protected-metric failure" in error for error in errors))

    def test_scoped_canary_requires_reserved_challenger_pass_and_scope(self) -> None:
        execution = copy.deepcopy(self.evaluated)
        execution["decision"] = {
            "verdict": "scoped_canary",
            "rationale": "synthetic gate exercise only",
            "human_approval_required": True,
            "team_available_allowed": False,
            "scoped_canary_scope": ["public contract audit shadow path"],
        }
        self.assertEqual([], self.validate(execution))

        execution["case_results"][-1]["variant_outcomes"][1]["target_result"] = "fail"
        errors = self.validate(execution)
        self.assertTrue(any("challenger to pass the reserved target" in error for error in errors))

    def test_blind_challenge_cannot_grant_team_available(self) -> None:
        execution = copy.deepcopy(self.evaluated)
        execution["promotion_boundary"]["team_available_allowed"] = True
        execution["decision"]["team_available_allowed"] = True
        errors = self.validate(execution)
        self.assertTrue(any("cannot grant team_available" in error for error in errors))

    def test_reserved_oracle_content_is_never_embedded(self) -> None:
        execution = copy.deepcopy(self.evaluated)
        execution["blindness"]["oracle_content_included"] = True
        execution["reserved_oracle"]["oracle_content_included"] = True
        errors = self.validate(execution)
        self.assertTrue(any("must not embed reserved oracle content" in error for error in errors))
        self.assertTrue(any("must not be copied" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
