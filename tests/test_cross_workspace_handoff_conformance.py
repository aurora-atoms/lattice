#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_cross_workspace_handoff.py"
FIXTURES = ROOT / "tests" / "fixtures" / "cross-workspace-handoff"
FEATURE_CASE = FIXTURES / "feature-requirement.synthetic.json"
FEATURE_RECEIPT = FIXTURES / "feature-requirement.receipt.json"
BUG_CASE = FIXTURES / "bug-investigation.synthetic.json"
BUG_RECEIPT = FIXTURES / "bug-investigation.receipt.json"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_cross_workspace_handoff", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


HANDOFF = load_module()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class CrossWorkspaceHandoffConformanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.feature_case = load_json(FEATURE_CASE)
        self.feature_receipt = load_json(FEATURE_RECEIPT)
        self.bug_case = load_json(BUG_CASE)
        self.bug_receipt = load_json(BUG_RECEIPT)

    def assertErrorContains(self, errors: list[str], text: str) -> None:
        self.assertTrue(any(text in error for error in errors), errors)

    def test_feature_requirement_handoff_preserves_candidate_context(self) -> None:
        self.assertEqual([], HANDOFF.validate_case(self.feature_case, ROOT))
        self.assertEqual([], HANDOFF.validate_receipt(self.feature_case, self.feature_receipt, ROOT))
        self.assertEqual(
            HANDOFF.canonical_json(HANDOFF.build_receipt(self.feature_case)),
            HANDOFF.canonical_json(self.feature_receipt),
        )
        self.assertEqual("candidate", self.feature_receipt["authority_ceiling"])
        self.assertEqual("verification_required", self.feature_receipt["readiness"])
        self.assertEqual(["FR-UNK-001"], self.feature_receipt["unknown_ids"])
        self.assertEqual("unresolved", self.feature_receipt["conflicts"][0]["status"])
        self.assertEqual("receiving_workspace", self.feature_receipt["capability_discovery"]["owner"])
        self.assertFalse(self.feature_receipt["capability_discovery"]["shared_mechanism_required"])

    def test_bug_handoff_keeps_root_cause_unverified_and_not_ready_for_fix(self) -> None:
        self.assertEqual([], HANDOFF.validate_case(self.bug_case, ROOT))
        self.assertEqual([], HANDOFF.validate_receipt(self.bug_case, self.bug_receipt, ROOT))
        by_id = {item["claim_id"]: item for item in self.bug_receipt["incoming_claims"]}
        self.assertEqual("derived", by_id["BUG-ROOT-HYP-001"]["incoming_status"])
        self.assertEqual("candidate_only", by_id["BUG-ROOT-HYP-001"]["confirmation_state"])
        self.assertEqual("verification_required", self.bug_receipt["readiness"])
        self.assertIn("BUG-ALT-001", self.bug_receipt["claims_requiring_repo_verification"])
        self.assertIn("BUG-ROOT-HYP-001", self.bug_receipt["claims_requiring_repo_verification"])

    def test_unknown_removed_fails(self) -> None:
        receipt = copy.deepcopy(self.feature_receipt)
        receipt["unknown_ids"] = []
        self.assertErrorContains(HANDOFF.validate_receipt(self.feature_case, receipt, ROOT), "UNKNOWN ids")

    def test_unresolved_conflict_silently_resolved_fails(self) -> None:
        receipt = copy.deepcopy(self.feature_receipt)
        receipt["conflicts"][0]["status"] = "resolved"
        errors = HANDOFF.validate_receipt(self.feature_case, receipt, ROOT)
        self.assertErrorContains(errors, "unresolved CONFLICT")

    def test_strongest_counterevidence_removed_fails(self) -> None:
        receipt = copy.deepcopy(self.feature_receipt)
        receipt["strongest_counterevidence"] = []
        errors = HANDOFF.validate_receipt(self.feature_case, receipt, ROOT)
        self.assertErrorContains(errors, "strongest counterevidence")

    def test_candidate_authority_promoted_to_confirmed_fails(self) -> None:
        receipt = copy.deepcopy(self.feature_receipt)
        receipt["authority_ceiling"] = "confirmed"
        self.assertErrorContains(HANDOFF.validate_receipt(self.feature_case, receipt, ROOT), "authority cannot increase")

    def test_candidate_promoted_to_work_ready_fails(self) -> None:
        receipt = copy.deepcopy(self.feature_receipt)
        receipt["readiness"] = "work_ready"
        self.assertErrorContains(HANDOFF.validate_receipt(self.feature_case, receipt, ROOT), "work_ready")

    def test_google_hypothesis_promoted_to_root_cause_verified_fails(self) -> None:
        receipt = copy.deepcopy(self.bug_receipt)
        root_claim = next(
            item for item in receipt["incoming_claims"] if item["claim_id"] == "BUG-ROOT-HYP-001"
        )
        root_claim["incoming_status"] = "root_cause_verified"
        errors = HANDOFF.validate_receipt(self.bug_case, receipt, ROOT)
        self.assertErrorContains(errors, "root_cause_verified")

    def test_required_coding_verification_removed_fails(self) -> None:
        receipt = copy.deepcopy(self.bug_receipt)
        receipt["required_coding_verification"] = []
        errors = HANDOFF.validate_receipt(self.bug_case, receipt, ROOT)
        self.assertErrorContains(errors, "required coding verification")

    def test_private_locator_copied_into_public_projection_fails(self) -> None:
        receipt = copy.deepcopy(self.feature_receipt)
        receipt["private_locator"] = "https://drive.google.com/drive/folders/private-example"
        errors = HANDOFF.validate_receipt(self.feature_case, receipt, ROOT)
        self.assertErrorContains(errors, "private locator")

    def test_target_or_case_ref_changed_fails(self) -> None:
        receipt = copy.deepcopy(self.feature_receipt)
        receipt["target"] = "Implement a different feature"
        self.assertErrorContains(HANDOFF.validate_receipt(self.feature_case, receipt, ROOT), "target must not change")

        receipt = copy.deepcopy(self.feature_receipt)
        receipt["case_ref"] = "synthetic/different-case"
        self.assertErrorContains(HANDOFF.validate_receipt(self.feature_case, receipt, ROOT), "case_ref must not change")

    def test_evidence_ref_lost_or_replaced_by_untraceable_prose_fails(self) -> None:
        receipt = copy.deepcopy(self.feature_receipt)
        receipt["evidence_ref_ids"] = ["the summary looked convincing"]
        errors = HANDOFF.validate_receipt(self.feature_case, receipt, ROOT)
        self.assertErrorContains(errors, "evidence_ref ids")

    def test_complete_search_claim_without_coverage_evidence_fails(self) -> None:
        receipt = copy.deepcopy(self.feature_receipt)
        receipt["source_scope"]["coverage_claim"] = "all_relevant_sources_searched"
        receipt["source_scope"]["evidence_ref_ids"] = []
        errors = HANDOFF.validate_receipt(self.feature_case, receipt, ROOT)
        self.assertErrorContains(errors, "cannot claim all relevant sources were searched")

    def test_workspace_specific_skill_required_by_canonical_handoff_fails(self) -> None:
        case = copy.deepcopy(self.feature_case)
        case["handoff_policy"]["required_skill"] = "skill:vendor-specific-feature@1.0.0"
        errors = HANDOFF.validate_case(case, ROOT)
        self.assertErrorContains(errors, "workspace-specific Skill")

    def test_synthetic_fixture_claims_real_downstream_adoption_fails(self) -> None:
        receipt = copy.deepcopy(self.feature_receipt)
        receipt["downstream_adoption_status"] = "used_once"
        errors = HANDOFF.validate_receipt(self.feature_case, receipt, ROOT)
        self.assertErrorContains(errors, "cannot claim real downstream adoption")

    def test_model_confidence_used_as_evidence_confirmation_fails(self) -> None:
        receipt = copy.deepcopy(self.feature_receipt)
        receipt["evidence_confirmation_basis"] = "model_confidence"
        errors = HANDOFF.validate_receipt(self.feature_case, receipt, ROOT)
        self.assertErrorContains(errors, "model confidence")

    def test_reference_consumer_cli_checks_committed_receipts(self) -> None:
        for case_path, receipt_path in (
            (FEATURE_CASE, FEATURE_RECEIPT),
            (BUG_CASE, BUG_RECEIPT),
        ):
            with self.subTest(case=case_path.name):
                completed = subprocess.run(
                    [sys.executable, str(SCRIPT), str(case_path), "--receipt", str(receipt_path)],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(0, completed.returncode, completed.stderr)
                self.assertIn("cross-workspace handoff conformance: valid", completed.stdout)


if __name__ == "__main__":
    unittest.main()
