from __future__ import annotations

import copy
import importlib.util
import sys
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


ADMISSION = load_module(
    "validate_attention_admission",
    SCRIPTS / "validate_attention_admission.py",
)
OUTCOME = load_module(
    "validate_outcome_receipt",
    SCRIPTS / "validate_outcome_receipt.py",
)
CASE_DIR = ROOT / "examples" / "evidence-wayfinding" / "case-0-schema-parity"


class AttentionAdmissionContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.receipt = ADMISSION.load_json(CASE_DIR / "admission-receipt.json")
        self.pack = ADMISSION.load_json(CASE_DIR / "portable-case-pack.json")
        self.contract = ADMISSION.load_json(CASE_DIR / "case-contract.json")

    def validate(self, receipt=None, pack=None, contract=None):
        return ADMISSION.validate_admission(
            copy.deepcopy(receipt if receipt is not None else self.receipt),
            copy.deepcopy(pack if pack is not None else self.pack),
            copy.deepcopy(contract if contract is not None else self.contract),
        )

    def test_case0_ready_admission_is_valid(self) -> None:
        self.assertEqual([], self.validate())

    def test_derived_claim_without_evidence_blocks_admission(self) -> None:
        pack = copy.deepcopy(self.pack)
        pack["claims"]["derived"][0]["evidence_refs"] = []
        errors = self.validate(pack=pack)
        self.assertTrue(any("M2_evidence status must be fail" in error for error in errors))
        self.assertTrue(any("admission status must be BLOCKED" in error for error in errors))

    def test_blocked_state_is_valid_when_source_contract_fails(self) -> None:
        pack = copy.deepcopy(self.pack)
        pack["claims"]["derived"][0]["evidence_refs"] = []
        receipt = copy.deepcopy(self.receipt)
        receipt["mandatory_checks"]["M2_evidence"]["status"] = "fail"
        receipt["mandatory_checks"]["M2_evidence"]["reason"] = (
            "A non-UNKNOWN derived claim has no evidence reference."
        )
        receipt["status"] = "BLOCKED"
        receipt["missing_actions"] = [
            {
                "check_id": "M2_evidence",
                "action": "Attach evidence or downgrade the claim before requesting Senior attention.",
            }
        ]
        self.assertEqual([], self.validate(receipt=receipt, pack=pack))

    def test_unknown_reversibility_escalates_instead_of_ready(self) -> None:
        receipt = copy.deepcopy(self.receipt)
        receipt["reversibility"]["level"] = "unknown"
        receipt["mandatory_checks"]["M4_risk_authority"]["status"] = "escalate"
        receipt["mandatory_checks"]["M4_risk_authority"]["reason"] = (
            "Reversibility is unknown and requires accountable human review."
        )
        receipt["status"] = "ESCALATE"
        receipt["missing_actions"] = [
            {
                "check_id": "M4_risk_authority",
                "action": "Resolve reversibility and risk authority before continuing.",
                "owner": "repository_maintainer",
            }
        ]
        self.assertEqual([], self.validate(receipt=receipt))

    def test_four_of_five_cannot_be_treated_as_ready(self) -> None:
        pack = copy.deepcopy(self.pack)
        pack["claims"]["derived"][0]["evidence_refs"] = []
        receipt = copy.deepcopy(self.receipt)
        receipt["mandatory_checks"]["M2_evidence"]["status"] = "fail"
        receipt["missing_actions"] = [
            {
                "check_id": "M2_evidence",
                "action": "Supply evidence or downgrade the claim.",
            }
        ]
        errors = self.validate(receipt=receipt, pack=pack)
        self.assertTrue(any("admission status must be BLOCKED" in error for error in errors))

    def test_ready_requires_acceptance_observer(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract.pop("acceptance_observer")
        errors = self.validate(contract=contract)
        self.assertTrue(any("M1_target status must be fail" in error for error in errors))


class OutcomeReceiptContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.receipt = OUTCOME.load_json(CASE_DIR / "outcome-receipt.json")
        self.pack = OUTCOME.load_json(CASE_DIR / "portable-case-pack.json")

    def validate(self, receipt=None, pack=None):
        return OUTCOME.validate_outcome(
            copy.deepcopy(receipt if receipt is not None else self.receipt),
            copy.deepcopy(pack if pack is not None else self.pack),
        )

    def test_case0_outcome_is_valid(self) -> None:
        self.assertEqual([], self.validate())

    def test_every_case_pack_claim_requires_an_outcome(self) -> None:
        receipt = copy.deepcopy(self.receipt)
        receipt["claim_outcomes"].pop()
        errors = self.validate(receipt=receipt)
        self.assertTrue(any("missing claim outcomes" in error for error in errors))

    def test_non_unknown_outcome_requires_evidence(self) -> None:
        receipt = copy.deepcopy(self.receipt)
        receipt["claim_outcomes"][0]["evidence_refs"] = []
        errors = self.validate(receipt=receipt)
        self.assertTrue(any("non-UNKNOWN status requires evidence_refs" in error for error in errors))

    def test_status_history_must_end_at_current_status(self) -> None:
        receipt = copy.deepcopy(self.receipt)
        receipt["claim_outcomes"][0]["status"] = "INVALIDATED"
        errors = self.validate(receipt=receipt)
        self.assertTrue(any("status must equal the last status_history.to" in error for error in errors))

    def test_status_history_version_is_explicit(self) -> None:
        receipt = copy.deepcopy(self.receipt)
        receipt["claim_outcomes"][0]["version"] = 2
        errors = self.validate(receipt=receipt)
        self.assertTrue(any("version must equal status_history length" in error for error in errors))

    def test_claim_cutoff_cannot_be_after_observed_outcome(self) -> None:
        receipt = copy.deepcopy(self.receipt)
        receipt["claim_outcomes"][0]["cutoff"] = "2026-08-10T00:00:00Z"
        errors = self.validate(receipt=receipt)
        self.assertTrue(any("cutoff cannot be after observed_at" in error for error in errors))

    def test_remaining_unknown_must_still_be_unknown_or_hypothesis(self) -> None:
        receipt = copy.deepcopy(self.receipt)
        receipt["claim_outcomes"][-1]["status"] = "CONFIRMED"
        receipt["claim_outcomes"][-1]["evidence_refs"] = ["EV-003"]
        receipt["claim_outcomes"][-1]["status_history"][0]["to"] = "CONFIRMED"
        receipt["claim_outcomes"][-1]["status_history"][0]["evidence_refs"] = ["EV-003"]
        errors = self.validate(receipt=receipt)
        self.assertTrue(any("claim must remain UNKNOWN or HYPOTHESIS" in error for error in errors))

    def test_outcome_cannot_promote_harness_candidate(self) -> None:
        receipt = copy.deepcopy(self.receipt)
        receipt["failure_point_candidate"]["promotion_authority"] = "team_available"
        errors = self.validate(receipt=receipt)
        self.assertTrue(any("cannot grant Harness promotion authority" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
