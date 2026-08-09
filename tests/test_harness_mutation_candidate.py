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


CANDIDATE_VALIDATOR = load_module(
    "validate_harness_mutation_candidate",
    SCRIPTS / "validate_harness_mutation_candidate.py",
)
SCHEMA_VALIDATOR = load_module(
    "validate_json_schema_instance",
    SCRIPTS / "validate_json_schema_instance.py",
)

CASE_DIR = ROOT / "examples" / "evidence-wayfinding" / "case-0-schema-parity"
CANDIDATE_PATH = CASE_DIR / "harness-mutation-candidate.json"
OUTCOME_PATH = CASE_DIR / "outcome-receipt.json"
PACK_PATH = CASE_DIR / "portable-case-pack.json"
SCHEMA_PATH = ROOT / "schemas" / "capability" / "harness-mutation-candidate.v1.schema.json"


class HarnessMutationCandidateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.candidate = CANDIDATE_VALIDATOR.load_json(CANDIDATE_PATH)
        self.outcome = CANDIDATE_VALIDATOR.load_json(OUTCOME_PATH)
        self.pack = CANDIDATE_VALIDATOR.load_json(PACK_PATH)

    def validate(self, candidate=None, outcome=None, pack=None):
        return CANDIDATE_VALIDATOR.validate_candidate(
            copy.deepcopy(candidate if candidate is not None else self.candidate),
            copy.deepcopy(outcome if outcome is not None else self.outcome),
            copy.deepcopy(pack if pack is not None else self.pack),
        )

    def structural_errors(self, candidate) -> list[str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "candidate.json"
            path.write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")
            return SCHEMA_VALIDATOR.validate_instance(SCHEMA_PATH, path)

    def test_case0_candidate_passes_schema_and_semantics(self) -> None:
        self.assertEqual([], SCHEMA_VALIDATOR.validate_instance(SCHEMA_PATH, CANDIDATE_PATH))
        self.assertEqual([], self.validate())

    def test_candidate_is_linked_to_outcome_earliest_failure(self) -> None:
        candidate = copy.deepcopy(self.candidate)
        candidate["failure_point"]["statement"] = "A different failure point."
        errors = self.validate(candidate=candidate)
        self.assertTrue(any("must match Outcome Receipt earliest failure" in error for error in errors))

    def test_failure_taxonomy_limits_mutation_target(self) -> None:
        candidate = copy.deepcopy(self.candidate)
        candidate["mutation"]["mechanism"] = "routing_change"
        errors = self.validate(candidate=candidate)
        self.assertTrue(any("cannot target mechanism" in error for error in errors))

    def test_one_primary_delta_is_structural(self) -> None:
        candidate = copy.deepcopy(self.candidate)
        candidate["mutation"]["secondary_delta"] = "Also change routing."
        errors = self.structural_errors(candidate)
        self.assertTrue(any("Additional properties are not allowed" in error for error in errors))

    def test_representative_hard_and_reserved_cases_are_required(self) -> None:
        candidate = copy.deepcopy(self.candidate)
        candidate["evaluation_plan"]["case_allocations"] = [
            case
            for case in candidate["evaluation_plan"]["case_allocations"]
            if case["class"] != "hard"
        ]
        errors = self.validate(candidate=candidate)
        self.assertTrue(any("missing required case classes" in error for error in errors))

    def test_reserved_oracle_is_withheld_from_candidate_author(self) -> None:
        candidate = copy.deepcopy(self.candidate)
        reserved = next(
            case
            for case in candidate["evaluation_plan"]["case_allocations"]
            if case["class"] == "reserved"
        )
        reserved["oracle_visibility"] = "visible_to_evaluator"
        reserved["availability"] = "public_fixture"
        reserved["oracle_ref"] = "repo://expected-result.json"
        errors = self.validate(candidate=candidate)
        self.assertTrue(any("reserved case oracle must be evaluator_only" in error for error in errors))
        self.assertTrue(any("keep the reserved case external" in error for error in errors))
        self.assertTrue(any("oracle_ref must remain withheld" in error for error in errors))

    def test_external_reserved_oracle_blocks_ready_for_blind_eval(self) -> None:
        candidate = copy.deepcopy(self.candidate)
        candidate["evaluation_plan"]["status"] = "ready_for_blind_eval"
        errors = self.validate(candidate=candidate)
        self.assertTrue(any("blocked_pending_reserved_oracle" in error for error in errors))

    def test_protected_metrics_cannot_drop_critical_false_ready(self) -> None:
        candidate = copy.deepcopy(self.candidate)
        candidate["evaluation_plan"]["protected_metrics"].remove("critical_false_ready")
        errors = self.validate(candidate=candidate)
        self.assertTrue(any("missing protected metrics" in error for error in errors))

    def test_candidate_cannot_grant_team_available_or_auto_promotion(self) -> None:
        candidate = copy.deepcopy(self.candidate)
        candidate["promotion_boundary"]["automatic_promotion_allowed"] = True
        candidate["promotion_boundary"]["team_available_allowed"] = True
        structural = self.structural_errors(candidate)
        self.assertTrue(structural)

    def test_candidate_requires_expiry_after_creation(self) -> None:
        candidate = copy.deepcopy(self.candidate)
        candidate["expires_at"] = candidate["created_at"]
        errors = self.validate(candidate=candidate)
        self.assertTrue(any("expires_at must be later" in error for error in errors))

    def test_public_case_references_exist_and_reserved_case_is_external(self) -> None:
        for case in self.candidate["evaluation_plan"]["case_allocations"]:
            ref = case["case_ref"]
            if case["availability"] == "public_fixture":
                self.assertTrue(ref.startswith("repo://"))
                path = ROOT / ref.removeprefix("repo://").split("#", 1)[0]
                self.assertTrue(path.exists(), ref)
            else:
                self.assertEqual("reserved", case["class"])
                self.assertTrue(ref.startswith("downstream://"))


if __name__ == "__main__":
    unittest.main()
