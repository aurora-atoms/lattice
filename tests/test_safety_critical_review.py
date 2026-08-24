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
SCRIPT = ROOT / "scripts" / "validate_safety_critical_review.py"
FIXTURE = (
    ROOT
    / "examples"
    / "safety-critical-review"
    / "synthetic-target-binding.review.v1.json"
)


def load_module():
    spec = importlib.util.spec_from_file_location("validate_safety_critical_review", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REVIEW = load_module()


class SafetyCriticalReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def assertErrorContains(self, errors: list[str], text: str) -> None:
        self.assertTrue(any(text in error for error in errors), errors)

    def test_synthetic_fixture_is_valid(self) -> None:
        self.assertEqual([], REVIEW.validate_record(self.record))

    def test_open_s0_cannot_pass(self) -> None:
        record = copy.deepcopy(self.record)
        chain = record["review_chains"][0]
        chain["failure_classification"]["finding_status"] = "open"
        self.assertErrorContains(
            REVIEW.validate_record(record), "mandatory_checks.no_open_s0_s1 must be false"
        )

    def test_open_s0_is_valid_only_when_record_blocks(self) -> None:
        record = copy.deepcopy(self.record)
        chain = record["review_chains"][0]
        chain["failure_classification"]["finding_status"] = "open"
        chain["release_gate"]["mandatory_checks"]["no_open_s0_s1"] = False
        chain["release_gate"]["recommended_decision"] = "block"
        chain["release_gate"]["blocking_reasons"] = ["no_open_s0_s1"]
        record["review_verdict"]["recommendation"] = "block"
        record["review_verdict"]["blocking_chain_ids"] = ["CHAIN-SYN-001"]
        self.assertEqual([], REVIEW.validate_record(record))

    def test_accepted_s0_exception_still_blocks(self) -> None:
        record = copy.deepcopy(self.record)
        chain = record["review_chains"][0]
        chain["failure_classification"]["finding_status"] = "accepted_exception"
        self.assertErrorContains(
            REVIEW.validate_record(record), "mandatory_checks.no_open_s0_s1 must be false"
        )

    def test_missing_runtime_evidence_fails_schema(self) -> None:
        record = copy.deepcopy(self.record)
        record["review_chains"][0]["runtime_evidence"] = []
        self.assertErrorContains(REVIEW.validate_record(record), "schema:review_chains.0.runtime_evidence")

    def test_planned_runtime_evidence_cannot_pass(self) -> None:
        record = copy.deepcopy(self.record)
        record["review_chains"][0]["runtime_evidence"][0]["observation_status"] = "planned"
        self.assertErrorContains(
            REVIEW.validate_record(record), "mandatory_checks.runtime_evidence_observed must be false"
        )

    def test_l2_only_test_cannot_satisfy_load_bearing_gate(self) -> None:
        record = copy.deepcopy(self.record)
        record["review_chains"][0]["adversarial_tests"][0]["level"] = "L2"
        self.assertErrorContains(
            REVIEW.validate_record(record), "mandatory_checks.adversarial_test_passed must be false"
        )

    def test_unapproved_normalized_requirement_cannot_pass(self) -> None:
        record = copy.deepcopy(self.record)
        record["requirements"][0]["normalized_requirement"]["status"] = "candidate"
        self.assertErrorContains(
            REVIEW.validate_record(record), "mandatory_checks.requirement_approved must be false"
        )

    def test_open_s2_requires_conditional_control(self) -> None:
        record = copy.deepcopy(self.record)
        chain = record["review_chains"][0]
        chain["failure_classification"].update(
            {"severity": "S2", "finding_status": "open", "evidence_status": "OBSERVED"}
        )
        chain["release_gate"]["mandatory_checks"]["no_open_s0_s1"] = True
        chain["release_gate"]["recommended_decision"] = "conditional"
        record["review_verdict"]["recommendation"] = "conditional"
        self.assertErrorContains(
            REVIEW.validate_record(record), "recommended_decision must be block"
        )

    def test_open_s2_with_bounded_control_is_valid_conditional(self) -> None:
        record = copy.deepcopy(self.record)
        chain = record["review_chains"][0]
        chain["failure_classification"].update(
            {"severity": "S2", "finding_status": "open", "evidence_status": "OBSERVED"}
        )
        chain["release_gate"]["recommended_decision"] = "conditional"
        chain["release_gate"]["conditional_controls"] = [
            {
                "control": "Restrict the synthetic scenario to one node until the retest passes.",
                "owner_role": "synthetic safety owner",
                "expires_at": "2026-09-01T00:00:00Z",
                "retest_ref": "synthetic://retest-plan/target-binding-002",
                "observability": "The simulator rejects any second-node activation."
            }
        ]
        record["review_verdict"]["recommendation"] = "conditional"
        self.assertEqual([], REVIEW.validate_record(record))

    def test_blocking_unknown_cannot_pass(self) -> None:
        record = copy.deepcopy(self.record)
        record["evidence"]["unknowns"] = [
            {
                "unknown_id": "UNK-001",
                "statement": "The deployed clock-skew bound is unknown.",
                "blocking": True,
                "owner_role": "synthetic platform owner"
            }
        ]
        self.assertErrorContains(
            REVIEW.validate_record(record), "mandatory_checks.unknowns_nonblocking must be false"
        )

    def test_public_fixture_cannot_claim_real_adoption(self) -> None:
        record = copy.deepcopy(self.record)
        record["downstream_adoption_status"] = "used_once"
        self.assertErrorContains(REVIEW.validate_record(record), "schema:downstream_adoption_status")

    def test_public_fixture_rejects_private_locator(self) -> None:
        record = copy.deepcopy(self.record)
        record["requirements"][0]["source_ref"] = "file:/Users/example/private-requirement.md"
        self.assertErrorContains(REVIEW.validate_record(record), "private locator")

    def test_cli_validates_fixture(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURE)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("safety-critical review: valid", completed.stdout)


if __name__ == "__main__":
    unittest.main()
