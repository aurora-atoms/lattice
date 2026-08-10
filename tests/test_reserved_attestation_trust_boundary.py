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


TRUST = load_module(
    "validate_reserved_evaluation_handoff_v2",
    SCRIPTS / "validate_reserved_evaluation_handoff_v2.py",
)
PREPARE = load_module(
    "prepare_reserved_evaluation_request_v2",
    SCRIPTS / "prepare_reserved_evaluation_request_v2.py",
)

CASE_DIR = ROOT / "examples" / "evidence-wayfinding" / "case-0-schema-parity"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "evidence-wayfinding" / "reserved-evaluation"
SCHEMA_PATH = ROOT / "schemas" / "capability" / "reserved-evaluation-handoff-record.v2.schema.json"
CANDIDATE_PATH = CASE_DIR / "harness-mutation-candidate.json"
EXECUTION_PATH = CASE_DIR / "blind-challenge-execution.blocked.json"
REQUEST_PATH = CASE_DIR / "reserved-evaluation-handoff.request.v2.synthetic.jsonl"
COMPLETE_PATH = FIXTURE_DIR / "handoff.synthetic-complete.v2.jsonl"
TRUST_STORE_PATH = FIXTURE_DIR / "trusted-evaluators.synthetic.json"
BUNDLE_PATH = FIXTURE_DIR / "variant-bundle.synthetic.json"


class ReservedAttestationTrustBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = TRUST.load_json(SCHEMA_PATH)
        self.candidate = TRUST.load_json(CANDIDATE_PATH)
        self.execution = TRUST.load_json(EXECUTION_PATH)
        self.request_records = TRUST.load_jsonl(REQUEST_PATH)
        self.complete_records = TRUST.load_jsonl(COMPLETE_PATH)
        self.trust_store = TRUST.load_json(TRUST_STORE_PATH)

    def validate(
        self,
        records=None,
        *,
        trust_store=True,
        consumed_nonces=None,
    ):
        return TRUST.validate_handoff(
            copy.deepcopy(records if records is not None else self.complete_records),
            copy.deepcopy(self.candidate),
            copy.deepcopy(self.execution),
            copy.deepcopy(self.schema),
            trust_store=(copy.deepcopy(self.trust_store) if trust_store else None),
            consumed_nonces=(set() if consumed_nonces is None else set(consumed_nonces)),
        )

    def test_public_case0_v2_request_is_valid_without_private_trust_material(self) -> None:
        self.assertEqual(1, len(self.request_records))
        self.assertEqual("eval.reserved_request", self.request_records[0]["type"])
        errors = TRUST.validate_handoff(
            copy.deepcopy(self.request_records),
            copy.deepcopy(self.candidate),
            copy.deepcopy(self.execution),
            copy.deepcopy(self.schema),
        )
        self.assertEqual([], errors)

    def test_signed_synthetic_attestation_is_valid(self) -> None:
        self.assertEqual([], self.validate())

    def test_request_builder_binds_exact_bundle_digest(self) -> None:
        digest = PREPARE.sha256_file(BUNDLE_PATH)
        self.assertEqual(
            "sha256:36eec5c55ce6bb65e9837ecacc55894ef4f030214e7e42de53b2ae8ea0eb1a87",
            digest,
        )
        request = self.complete_records[0]
        built = PREPARE.build_request(
            self.candidate,
            self.execution,
            request_id=request["id"],
            issued_at=request["payload"]["issued_at"],
            expires_at=request["payload"]["expires_at"],
            request_nonce=request["payload"]["request_nonce"],
            variant_bundle_ref=request["payload"]["variant_bundle_ref"],
            variant_bundle_digest=digest,
        )
        self.assertEqual(request, built)

    def test_attestation_requires_trusted_evaluator_store(self) -> None:
        errors = self.validate(trust_store=False)
        self.assertTrue(any("trusted evaluator key store" in error for error in errors))

    def test_arbitrary_evaluator_identity_is_rejected(self) -> None:
        records = copy.deepcopy(self.complete_records)
        records[1]["payload"]["evaluator_identity"]["evaluator_id"] = "arbitrary-evaluator"
        errors = self.validate(records)
        self.assertTrue(any("not uniquely trusted" in error for error in errors))

    def test_inactive_evaluator_key_is_rejected(self) -> None:
        trust_store = copy.deepcopy(self.trust_store)
        trust_store["evaluators"][0]["status"] = "revoked"
        errors = TRUST.validate_handoff(
            copy.deepcopy(self.complete_records),
            copy.deepcopy(self.candidate),
            copy.deepcopy(self.execution),
            copy.deepcopy(self.schema),
            trust_store=trust_store,
            consumed_nonces=set(),
        )
        self.assertTrue(any("must be active" in error for error in errors))

    def test_bundle_digest_must_match_frozen_request(self) -> None:
        records = copy.deepcopy(self.complete_records)
        records[0]["payload"]["variant_bundle_digest"] = "sha256:" + "2" * 64
        errors = self.validate(records)
        self.assertTrue(any("variant_bundle_digest must match" in error for error in errors))

    def test_attestation_content_mutation_breaks_digest_and_signature(self) -> None:
        records = copy.deepcopy(self.complete_records)
        records[1]["payload"]["reserved_case_result"]["comparison"] = "tie"
        errors = self.validate(records)
        self.assertTrue(any("canonical_digest does not match" in error for error in errors))
        self.assertTrue(any("signature verification failed" in error for error in errors))

    def test_arbitrary_attestation_digest_is_rejected(self) -> None:
        records = copy.deepcopy(self.complete_records)
        records[1]["payload"]["attestation_canonical_digest"] = "sha256:" + "3" * 64
        errors = self.validate(records)
        self.assertTrue(any("canonical_digest does not match" in error for error in errors))

    def test_arbitrary_signature_is_rejected(self) -> None:
        records = copy.deepcopy(self.complete_records)
        records[1]["payload"]["signature"] = "A" * 86 + "=="
        errors = self.validate(records)
        self.assertTrue(any("signature verification failed" in error for error in errors))

    def test_request_nonce_must_match_attestation(self) -> None:
        records = copy.deepcopy(self.complete_records)
        records[0]["payload"]["request_nonce"] = "req_case0_other_20260809_001"
        errors = self.validate(records)
        self.assertTrue(any("request_nonce must match" in error for error in errors))

    def test_consumed_nonce_replay_is_rejected(self) -> None:
        nonce = self.complete_records[0]["payload"]["request_nonce"]
        errors = self.validate(consumed_nonces={nonce})
        self.assertTrue(any("replay rejected" in error for error in errors))

    def test_attestation_after_request_expiry_is_rejected(self) -> None:
        records = copy.deepcopy(self.complete_records)
        records[0]["payload"]["expires_at"] = "2026-08-09T04:15:00Z"
        errors = self.validate(records)
        self.assertTrue(any("cannot exceed request expires_at" in error for error in errors))

    def test_request_builder_rejects_noncontrolled_bundle(self) -> None:
        with self.assertRaisesRegex(ValueError, "controlled://"):
            PREPARE.build_request(
                self.candidate,
                self.execution,
                request_id="bad-request",
                issued_at="2026-08-09T04:10:00Z",
                expires_at="2026-08-10T04:10:00Z",
                request_nonce="req_case0_synth_20260809_001",
                variant_bundle_ref="repo://visible-bundle",
                variant_bundle_digest="sha256:" + "0" * 64,
            )

    def test_request_builder_rejects_short_or_unsafe_nonce(self) -> None:
        with self.assertRaisesRegex(ValueError, "request_nonce"):
            PREPARE.build_request(
                self.candidate,
                self.execution,
                request_id="bad-nonce",
                issued_at="2026-08-09T04:10:00Z",
                expires_at="2026-08-10T04:10:00Z",
                request_nonce="short nonce",
                variant_bundle_ref="controlled://blind-bundle/synthetic",
                variant_bundle_digest="sha256:" + "0" * 64,
            )


if __name__ == "__main__":
    unittest.main()
