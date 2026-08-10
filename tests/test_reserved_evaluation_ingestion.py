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


INGEST = load_module(
    "ingest_reserved_evaluation_attestation",
    SCRIPTS / "ingest_reserved_evaluation_attestation.py",
)
HANDOFF = load_module(
    "validate_reserved_evaluation_handoff_v2_for_ingest_test",
    SCRIPTS / "validate_reserved_evaluation_handoff_v2.py",
)

CASE_DIR = ROOT / "examples" / "evidence-wayfinding" / "case-0-schema-parity"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "evidence-wayfinding"
CANDIDATE_PATH = CASE_DIR / "harness-mutation-candidate.json"
BLOCKED_PATH = CASE_DIR / "blind-challenge-execution.blocked.json"
EVALUATED_PATH = FIXTURE_DIR / "blind-challenge" / "evaluated.synthetic-conformance.json"
HANDOFF_PATH = FIXTURE_DIR / "reserved-evaluation" / "handoff.synthetic-complete.v2.jsonl"
HANDOFF_SCHEMA_PATH = ROOT / "schemas" / "capability" / "reserved-evaluation-handoff-record.v2.schema.json"
RESULT_SCHEMA_PATH = ROOT / "schemas" / "capability" / "reserved-evaluation-ingest-result.v1.schema.json"
TRUST_STORE_PATH = FIXTURE_DIR / "reserved-evaluation" / "trusted-evaluators.synthetic.json"


class ReservedEvaluationIngestionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.candidate = INGEST.load_json(CANDIDATE_PATH)
        self.blocked = INGEST.load_json(BLOCKED_PATH)
        self.evaluated = INGEST.load_json(EVALUATED_PATH)
        self.records = HANDOFF.load_jsonl(HANDOFF_PATH)
        self.handoff_schema = INGEST.load_json(HANDOFF_SCHEMA_PATH)
        self.result_schema = INGEST.load_json(RESULT_SCHEMA_PATH)
        self.trust_store = INGEST.load_json(TRUST_STORE_PATH)

    def build(self, blocked=None, records=None, consumed=None):
        return INGEST.build_ingest_result(
            copy.deepcopy(records if records is not None else self.records),
            copy.deepcopy(self.candidate),
            copy.deepcopy(blocked if blocked is not None else self.blocked),
            copy.deepcopy(self.handoff_schema),
            copy.deepcopy(self.trust_store),
            set(consumed or set()),
            copy.deepcopy(self.result_schema),
        )

    def test_authenticated_attestation_without_preflight_results_stays_blocked(self) -> None:
        result, errors = self.build()
        self.assertEqual([], errors)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertFalse(result["projection"]["all_allocations_settled"])
        self.assertFalse(result["projection"]["ready_for_governed_adjudication"])
        self.assertEqual(
            [
                "counterexample.valid-minimal-pack",
                "hard.semantic-boundary-derived-evidence",
                "representative.missing-audience",
            ],
            result["projection"]["missing_case_ids"],
        )
        self.assertFalse(result["human_gate"]["governed_verdict_allowed"])
        self.assertFalse(result["human_gate"]["automatic_promotion_allowed"])
        self.assertTrue(result["human_gate"]["human_decision_required"])

    def test_ingest_is_ready_only_after_all_frozen_allocations_are_settled(self) -> None:
        blocked = copy.deepcopy(self.blocked)
        blocked["case_results"] = copy.deepcopy(self.evaluated["case_results"][:3])
        result, errors = self.build(blocked=blocked)
        self.assertEqual([], errors)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertTrue(result["projection"]["all_allocations_settled"])
        self.assertTrue(result["projection"]["ready_for_governed_adjudication"])
        self.assertEqual([], result["projection"]["missing_case_ids"])
        self.assertEqual(4, len(result["projection"]["merged_case_ids"]))

    def test_ingest_output_is_structurally_valid_and_deterministic(self) -> None:
        first, first_errors = self.build()
        second, second_errors = self.build()
        self.assertEqual([], first_errors)
        self.assertEqual([], second_errors)
        self.assertEqual(first, second)
        assert first is not None
        self.assertEqual([], INGEST.schema_errors(first, self.result_schema))
        self.assertEqual(
            first["ingest_canonical_digest"],
            INGEST.canonical_ingest_digest(first),
        )

    def test_signed_attestation_mutation_is_rejected_before_ingest(self) -> None:
        records = copy.deepcopy(self.records)
        records[1]["payload"]["reserved_case_result"]["comparison"] = "A_better"
        result, errors = self.build(records=records)
        self.assertIsNone(result)
        joined = "\n".join(errors).lower()
        self.assertTrue("signature" in joined or "canonical" in joined)

    def test_consumed_nonce_replay_is_rejected(self) -> None:
        nonce = str(self.records[0]["payload"]["request_nonce"])
        result, errors = self.build(consumed={nonce})
        self.assertIsNone(result)
        joined = "\n".join(errors).lower()
        self.assertIn("nonce", joined)
        self.assertTrue("consum" in joined or "replay" in joined)

    def test_ingest_result_cannot_smuggle_mapping_or_verdict_authority(self) -> None:
        result, errors = self.build()
        self.assertEqual([], errors)
        assert result is not None
        self.assertNotIn("variant_mapping", result)
        self.assertNotIn("decision", result)
        mutated = copy.deepcopy(result)
        mutated["human_gate"]["governed_verdict_allowed"] = True
        semantic_errors = INGEST.validate_ingest_result(
            mutated,
            self.records,
            self.candidate,
            self.blocked,
        )
        self.assertTrue(any("stop before mapping" in error for error in semantic_errors))
        self.assertNotEqual(
            mutated["ingest_canonical_digest"],
            INGEST.canonical_ingest_digest(mutated),
        )

    def test_nonce_consumption_is_persisted_and_duplicate_rejected(self) -> None:
        nonce = str(self.records[0]["payload"]["request_nonce"])
        with tempfile.TemporaryDirectory() as temp_dir:
            ledger = Path(temp_dir) / "consumed-nonces.txt"
            ledger.write_text("# test ledger\n", encoding="utf-8")
            INGEST.consume_nonce(ledger, nonce)
            self.assertIn(nonce, HANDOFF.load_consumed_nonces(ledger))
            with self.assertRaises(ValueError):
                INGEST.consume_nonce(ledger, nonce)


if __name__ == "__main__":
    unittest.main()
