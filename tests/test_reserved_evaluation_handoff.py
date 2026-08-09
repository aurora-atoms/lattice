from __future__ import annotations

import copy
import importlib.util
import json
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


HANDOFF = load_module(
    "validate_reserved_evaluation_handoff",
    SCRIPTS / "validate_reserved_evaluation_handoff.py",
)
PREPARE = load_module(
    "prepare_reserved_evaluation_request",
    SCRIPTS / "prepare_reserved_evaluation_request.py",
)

CASE_DIR = ROOT / "examples" / "evidence-wayfinding" / "case-0-schema-parity"
SCHEMA_PATH = ROOT / "schemas" / "capability" / "reserved-evaluation-handoff-record.v1.schema.json"
CANDIDATE_PATH = CASE_DIR / "harness-mutation-candidate.json"
EXECUTION_PATH = CASE_DIR / "blind-challenge-execution.blocked.json"
REQUEST_PATH = CASE_DIR / "reserved-evaluation-handoff.request.jsonl"
COMPLETE_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "evidence-wayfinding"
    / "reserved-evaluation"
    / "handoff.synthetic-complete.jsonl"
)


class ReservedEvaluationHandoffTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = HANDOFF.load_json(SCHEMA_PATH)
        self.candidate = HANDOFF.load_json(CANDIDATE_PATH)
        self.execution = HANDOFF.load_json(EXECUTION_PATH)
        self.request_records = HANDOFF.load_jsonl(REQUEST_PATH)
        self.complete_records = HANDOFF.load_jsonl(COMPLETE_PATH)

    def validate(self, records=None, candidate=None, execution=None):
        return HANDOFF.validate_handoff(
            copy.deepcopy(records if records is not None else self.complete_records),
            copy.deepcopy(candidate if candidate is not None else self.candidate),
            copy.deepcopy(execution if execution is not None else self.execution),
            copy.deepcopy(self.schema),
        )

    def test_public_case0_request_is_valid_and_stays_request_only(self) -> None:
        self.assertEqual(1, len(self.request_records))
        self.assertEqual("eval.reserved_request", self.request_records[0]["type"])
        self.assertEqual([], self.validate(records=self.request_records))

    def test_synthetic_request_and_attestation_are_valid(self) -> None:
        self.assertEqual(2, len(self.complete_records))
        self.assertEqual([], self.validate())

    def test_request_builder_matches_committed_case0_projection(self) -> None:
        expected = self.request_records[0]
        built = PREPARE.build_request(
            self.candidate,
            self.execution,
            request_id=expected["id"],
            issued_at=expected["payload"]["issued_at"],
            variant_bundle_ref=expected["payload"]["variant_bundle_ref"],
        )
        self.assertEqual(expected, built)

    def test_attestation_cannot_arrive_before_request(self) -> None:
        records = [self.complete_records[1], self.complete_records[0]]
        errors = self.validate(records=records)
        self.assertTrue(any("first handoff record" in error for error in errors))

    def test_scope_must_match_frozen_execution(self) -> None:
        records = copy.deepcopy(self.complete_records)
        records[1]["scope"]["target_hash"] = "sha256:" + "2" * 64
        errors = self.validate(records=records)
        self.assertTrue(any("attestation scope must exactly match" in error for error in errors))

    def test_attestation_cannot_expose_variant_mapping(self) -> None:
        records = copy.deepcopy(self.complete_records)
        records[1]["payload"]["variant_mapping"] = {
            "A": "incumbent.syntax-plus-semantic",
            "B": "challenger.schema-instance-parity-gate",
        }
        errors = self.validate(records=records)
        self.assertTrue(any("Additional properties are not allowed" in error for error in errors))

    def test_attestation_cannot_include_raw_oracle_content(self) -> None:
        records = copy.deepcopy(self.complete_records)
        records[1]["payload"]["oracle_content"] = "private expected answer"
        errors = self.validate(records=records)
        self.assertTrue(any("Additional properties are not allowed" in error for error in errors))

    def test_attestation_cannot_emit_governed_verdict(self) -> None:
        records = copy.deepcopy(self.complete_records)
        records[1]["payload"]["decision"] = {"verdict": "scoped_canary"}
        errors = self.validate(records=records)
        self.assertTrue(any("Additional properties are not allowed" in error for error in errors))

    def test_attestation_must_evaluate_every_frozen_protected_metric(self) -> None:
        records = copy.deepcopy(self.complete_records)
        records[1]["payload"]["reserved_case_result"]["protected_metrics"].pop()
        errors = self.validate(records=records)
        self.assertTrue(any("protected metrics must match" in error for error in errors))

    def test_attestation_must_keep_anonymous_a_b_outcomes(self) -> None:
        records = copy.deepcopy(self.complete_records)
        records[1]["payload"]["reserved_case_result"]["variant_outcomes"][1]["label"] = "A"
        errors = self.validate(records=records)
        self.assertTrue(any("exactly anonymous variant outcomes A and B" in error for error in errors))

    def test_attestation_rejects_unsafe_evidence_reference(self) -> None:
        records = copy.deepcopy(self.complete_records)
        records[1]["payload"]["reserved_case_result"]["evidence_refs"] = [
            "file:///private/oracle.txt"
        ]
        errors = self.validate(records=records)
        self.assertTrue(any("safe projections" in error for error in errors))

    def test_handoff_cannot_start_from_already_evaluated_execution(self) -> None:
        execution = copy.deepcopy(self.execution)
        execution["status"] = "evaluated"
        errors = self.validate(execution=execution)
        self.assertTrue(any("blocked_pending_reserved_oracle" in error for error in errors))

    def test_request_builder_rejects_noncontrolled_variant_bundle(self) -> None:
        with self.assertRaisesRegex(ValueError, "controlled://"):
            PREPARE.build_request(
                self.candidate,
                self.execution,
                request_id="bad-request",
                issued_at="2026-08-09T03:49:00Z",
                variant_bundle_ref="repo://visible-bundle",
            )


if __name__ == "__main__":
    unittest.main()
