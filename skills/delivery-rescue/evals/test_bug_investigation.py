from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_bug_investigation.py"
SCHEMA_PATH = ROOT / "schemas" / "bug-investigation.v1.schema.json"
FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "valid-bug-investigation.synthetic.json"

spec = importlib.util.spec_from_file_location("validate_bug_investigation", VALIDATOR_PATH)
validator_module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator_module)


class BugInvestigationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def errors_for(self, packet: dict) -> list[str]:
        return validator_module.validate_packet(packet, self.schema)

    def test_valid_synthetic_packet_passes(self) -> None:
        self.assertEqual([], self.errors_for(copy.deepcopy(self.fixture)))

    def test_unknown_top_level_field_fails_structural_contract(self) -> None:
        packet = copy.deepcopy(self.fixture)
        packet["unexpected"] = True
        errors = self.errors_for(packet)
        self.assertTrue(any("Additional properties are not allowed" in item for item in errors), errors)

    def test_reproduced_failure_requires_evidence(self) -> None:
        packet = copy.deepcopy(self.fixture)
        packet["reproduction"]["evidence_refs"] = []
        errors = self.errors_for(packet)
        self.assertTrue(any("reproduction.status=reproduced requires reproduction evidence_refs" in item for item in errors), errors)

    def test_verified_root_cause_requires_reproduced_failure(self) -> None:
        packet = copy.deepcopy(self.fixture)
        packet["reproduction"]["status"] = "not_reproduced"
        errors = self.errors_for(packet)
        self.assertTrue(any("verified root cause requires a reproduced failure" in item for item in errors), errors)

    def test_correlation_alone_cannot_verify_root_cause(self) -> None:
        packet = copy.deepcopy(self.fixture)
        packet["verification_tests"] = [packet["verification_tests"][1]]
        errors = self.errors_for(packet)
        self.assertTrue(any("supported hypothesis H-ORDER requires a supporting verification test" in item for item in errors), errors)
        self.assertTrue(any("verified root cause requires a supporting falsification or controlled verification test" in item for item in errors), errors)

    def test_supported_hypothesis_requires_supporting_test(self) -> None:
        packet = copy.deepcopy(self.fixture)
        packet["verification_tests"][0]["outcome"] = "weakens"
        errors = self.errors_for(packet)
        self.assertTrue(any("supported hypothesis H-ORDER requires a supporting verification test" in item for item in errors), errors)

    def test_falsified_hypothesis_requires_contrary_evidence(self) -> None:
        packet = copy.deepcopy(self.fixture)
        packet["hypotheses"][1]["evidence_against"] = []
        packet["verification_tests"][1]["outcome"] = "not_run"
        packet["verification_tests"][1]["evidence_refs"] = []
        errors = self.errors_for(packet)
        self.assertTrue(any("falsified hypothesis H-TIMING requires contrary evidence or a falsifying test" in item for item in errors), errors)

    def test_ready_fix_requires_supported_root_cause(self) -> None:
        packet = copy.deepcopy(self.fixture)
        packet["root_cause"]["status"] = "unknown"
        packet["root_cause"]["hypothesis_id"] = None
        packet["root_cause"]["strongest_alternative_hypothesis_id"] = None
        packet["root_cause"]["alternative_disposition"] = "not_applicable"
        packet["root_cause"]["evidence_refs"] = []
        errors = self.errors_for(packet)
        self.assertTrue(any("ready_for_bounded_fix requires a supported or verified root-cause hypothesis" in item for item in errors), errors)
        self.assertTrue(any("repair cannot be the minimum next step while root cause remains unknown" in item for item in errors), errors)

    def test_ready_fix_rejects_blocking_unknown(self) -> None:
        packet = copy.deepcopy(self.fixture)
        packet["evidence_summary"]["unknowns"][0]["blocking"] = True
        errors = self.errors_for(packet)
        self.assertTrue(any("ready_for_bounded_fix is not allowed while blocking unknowns remain" in item for item in errors), errors)

    def test_ready_fix_rejects_unresolved_alternative(self) -> None:
        packet = copy.deepcopy(self.fixture)
        packet["hypotheses"][1]["status"] = "plausible"
        packet["root_cause"]["alternative_disposition"] = "unresolved"
        errors = self.errors_for(packet)
        self.assertTrue(any("ready_for_bounded_fix is not allowed with unresolved or accepted residual alternative risk" in item for item in errors), errors)

    def test_intermitttent_failure_cannot_jump_to_repair(self) -> None:
        packet = copy.deepcopy(self.fixture)
        packet["reproduction"]["status"] = "intermittent"
        packet["root_cause"]["status"] = "hypothesis_supported"
        packet["minimum_next_step"]["kind"] = "repair"
        packet["fix_readiness"]["status"] = "not_ready"
        errors = self.errors_for(packet)
        self.assertTrue(any("repair cannot be the minimum next step before the failure is reproduced" in item for item in errors), errors)

    def test_verification_test_must_reference_existing_hypothesis(self) -> None:
        packet = copy.deepcopy(self.fixture)
        packet["verification_tests"][0]["target_hypothesis_id"] = "H-MISSING"
        errors = self.errors_for(packet)
        self.assertTrue(any("references unknown hypothesis" in item for item in errors), errors)

    def test_fact_ids_must_reference_observations(self) -> None:
        packet = copy.deepcopy(self.fixture)
        packet["evidence_summary"]["facts"].append("OBS-MISSING")
        errors = self.errors_for(packet)
        self.assertTrue(any("references unknown observation: OBS-MISSING" in item for item in errors), errors)

    def test_synthetic_fixture_cannot_claim_downstream_adoption(self) -> None:
        packet = copy.deepcopy(self.fixture)
        packet["downstream_adoption_status"] = "used_once"
        errors = self.errors_for(packet)
        self.assertTrue(any("synthetic_reference packets must keep downstream_adoption_status=not_observed" in item for item in errors), errors)

    def test_invalid_evidence_reference_fails_schema(self) -> None:
        packet = copy.deepcopy(self.fixture)
        packet["blocker"]["evidence_refs"] = ["plain-label"]
        errors = self.errors_for(packet)
        self.assertTrue(any("does not match" in item for item in errors), errors)

    def test_not_attempted_reproduction_has_zero_attempts(self) -> None:
        packet = copy.deepcopy(self.fixture)
        packet["reproduction"]["status"] = "not_attempted"
        packet["reproduction"]["attempts"] = 1
        packet["reproduction"]["last_attempt_at"] = None
        packet["root_cause"]["status"] = "unknown"
        packet["root_cause"]["hypothesis_id"] = None
        packet["root_cause"]["strongest_alternative_hypothesis_id"] = None
        packet["root_cause"]["alternative_disposition"] = "not_applicable"
        packet["root_cause"]["evidence_refs"] = []
        packet["minimum_next_step"]["kind"] = "reproduce"
        packet["fix_readiness"]["status"] = "not_ready"
        errors = self.errors_for(packet)
        self.assertTrue(any("reproduction.status=not_attempted requires attempts=0" in item for item in errors), errors)


if __name__ == "__main__":
    unittest.main()
