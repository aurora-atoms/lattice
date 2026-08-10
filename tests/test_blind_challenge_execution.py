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
EVALUATED = (
    ROOT
    / "tests"
    / "fixtures"
    / "evidence-wayfinding"
    / "blind-challenge"
    / "evaluated.synthetic-conformance.json"
)
SCHEMA = ROOT / "schemas" / "capability" / "blind-challenge-execution.v1.schema.json"
HANDOFF_V2 = (
    ROOT
    / "tests"
    / "fixtures"
    / "evidence-wayfinding"
    / "reserved-evaluation"
    / "handoff.synthetic-complete.v2.jsonl"
)
HANDOFF_SCHEMA_V2 = (
    ROOT / "schemas" / "capability" / "reserved-evaluation-handoff-record.v2.schema.json"
)
TRUST_STORE = (
    ROOT
    / "tests"
    / "fixtures"
    / "evidence-wayfinding"
    / "reserved-evaluation"
    / "trusted-evaluators.synthetic.json"
)
CONSUMED_NONCES = (
    ROOT
    / "tests"
    / "fixtures"
    / "evidence-wayfinding"
    / "reserved-evaluation"
    / "consumed-nonces.empty.txt"
)


class BlindChallengeExecutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.candidate = BLIND.load_json(CANDIDATE)
        self.blocked = BLIND.load_json(BLOCKED)
        self.evaluated = BLIND.load_json(EVALUATED)
        self.handoff_records = BLIND.HANDOFF_V2.load_jsonl(HANDOFF_V2)
        self.handoff_schema = BLIND.load_json(HANDOFF_SCHEMA_V2)
        self.trust_store = BLIND.load_json(TRUST_STORE)
        self.consumed_nonces = BLIND.HANDOFF_V2.load_consumed_nonces(CONSUMED_NONCES)

    def validate(self, execution, *, trusted: bool = False):
        kwargs = {}
        if trusted:
            kwargs = {
                "handoff_records": copy.deepcopy(self.handoff_records),
                "blocked_execution": copy.deepcopy(self.blocked),
                "handoff_schema": copy.deepcopy(self.handoff_schema),
                "trust_store": copy.deepcopy(self.trust_store),
                "consumed_nonces": set(self.consumed_nonces),
            }
        return BLIND.validate_execution(
            copy.deepcopy(execution),
            copy.deepcopy(self.candidate),
            **kwargs,
        )

    def attested_execution(self, *, downstream_observed: bool = False):
        execution = copy.deepcopy(self.evaluated)
        attestation = self.handoff_records[1]["payload"]
        execution["execution_id"] = self.blocked["execution_id"]
        execution["completed_at"] = attestation["evaluated_at"]
        execution["variant_mapping"]["revealed_at"] = "2026-08-09T04:21:00Z"
        execution["case_results"][-1] = copy.deepcopy(attestation["reserved_case_result"])
        execution["reserved_oracle"] = {
            "case_id": attestation["reserved_case_result"]["case_id"],
            "status": "available",
            "oracle_visibility": "evaluator_only",
            "oracle_content_included": False,
            "attestation_ref": attestation["attestation_ref"],
            "attestation_hash": attestation["attestation_canonical_digest"],
            "evaluated_by": attestation["evaluator_identity"]["evaluator_id"],
            "evaluated_at": attestation["evaluated_at"],
        }
        execution["evidence_refs"] = [attestation["attestation_ref"]]
        execution["decision"] = {
            "verdict": "scoped_canary",
            "rationale": "Synthetic conformance exercise for the verified-attestation gate.",
            "human_approval_required": True,
            "team_available_allowed": False,
            "scoped_canary_scope": ["public contract audit shadow path"],
        }

        if downstream_observed:
            execution["simulation_status"] = "downstream_observed"
            execution["downstream_adoption_status"] = "observed_once"
            for result in execution["case_results"]:
                case_slug = result["case_id"].replace(".", "-")
                if not result["evidence_refs"]:
                    result["evidence_refs"] = [f"artifact://synthetic/{case_slug}/result"]
                for variant in result["variant_outcomes"]:
                    if not variant["evidence_refs"]:
                        variant["evidence_refs"] = [
                            f"artifact://synthetic/{case_slug}/variant-{variant['label'].lower()}"
                        ]
                for metric in result["protected_metrics"]:
                    if not metric.get("evidence_refs"):
                        metric["evidence_refs"] = [
                            f"artifact://synthetic/{case_slug}/metric-{metric['metric']}"
                        ]
        return execution

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

    def test_scoped_canary_requires_verified_attestation_context(self) -> None:
        execution = self.attested_execution()
        errors = self.validate(execution)
        self.assertTrue(any("requires verified reserved attestation context" in error for error in errors))

    def test_scoped_canary_accepts_matching_verified_attestation(self) -> None:
        execution = self.attested_execution()
        self.assertEqual([], self.validate(execution, trusted=True))

    def test_scoped_canary_requires_reserved_challenger_pass_and_scope(self) -> None:
        execution = self.attested_execution()
        self.assertEqual([], self.validate(execution, trusted=True))

        execution["case_results"][-1]["variant_outcomes"][1]["target_result"] = "fail"
        errors = self.validate(execution, trusted=True)
        self.assertTrue(any("challenger to pass the reserved target" in error for error in errors))

    def test_downstream_observed_rejects_empty_evidence_even_with_trusted_attestation(self) -> None:
        execution = self.attested_execution()
        execution["simulation_status"] = "downstream_observed"
        execution["downstream_adoption_status"] = "observed_once"
        errors = self.validate(execution, trusted=True)
        self.assertTrue(any("requires non-empty evidence_refs" in error for error in errors))

    def test_downstream_observed_accepts_evidence_complete_verified_execution(self) -> None:
        execution = self.attested_execution(downstream_observed=True)
        self.assertEqual([], self.validate(execution, trusted=True))

    def test_downstream_observed_requires_uri_like_evidence(self) -> None:
        execution = self.attested_execution(downstream_observed=True)
        execution["case_results"][0]["evidence_refs"] = ["opaque-string-without-scheme"]
        errors = self.validate(execution, trusted=True)
        self.assertTrue(any("URI-like evidence references" in error for error in errors))

    def test_authenticated_attestation_must_match_reserved_result(self) -> None:
        execution = self.attested_execution()
        execution["case_results"][-1]["comparison"] = "tie"
        errors = self.validate(execution, trusted=True)
        self.assertTrue(any("exactly match authenticated attestation projection" in error for error in errors))

    def test_authenticated_attestation_metadata_must_match_reserved_oracle(self) -> None:
        execution = self.attested_execution()
        execution["reserved_oracle"]["evaluated_by"] = "arbitrary-evaluator"
        errors = self.validate(execution, trusted=True)
        self.assertTrue(any("evaluated_by must match authenticated attestation" in error for error in errors))

    def test_synthetic_reference_cannot_claim_downstream_adoption(self) -> None:
        execution = copy.deepcopy(self.evaluated)
        execution["downstream_adoption_status"] = "observed_once"
        errors = self.validate(execution)
        self.assertTrue(any("cannot claim downstream adoption" in error for error in errors))

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
