from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SKILL_ROOT = HERE.parent
FIXTURE = HERE / "fixtures" / "valid-domain-context-pack.synthetic.json"
SCHEMA = SKILL_ROOT / "schemas" / "domain-context-pack.v1.schema.json"
VALIDATOR_PATH = SKILL_ROOT / "scripts" / "validate_domain_context_pack.py"

spec = importlib.util.spec_from_file_location("domain_context_validator", VALIDATOR_PATH)
validator_module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator_module)


class DomainContextPackContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    def validate(self, value: dict) -> list[str]:
        return validator_module.validate_pack(value, self.schema)

    def assertInvalidContains(self, value: dict, fragment: str) -> None:
        errors = self.validate(value)
        self.assertTrue(errors, "expected validation failure")
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got: {errors}",
        )

    def make_modeling_pack(self) -> dict:
        value = copy.deepcopy(self.base)
        value["task"]["origin"] = "modeling_decision"
        value["task"]["objective"] = "Evaluate a synthetic Silver model candidate."
        value["task"]["expected_output"] = "Evidence-backed candidate for accountable human review."
        value["modeling_decision"] = {
            "gold_consumer": {
                "consumer": "synthetic reliability dashboard",
                "workflow_or_question": "Compute monthly completed events by account without double counting.",
                "entity_or_event": "service event",
                "required_grain": "one row per service event",
                "required_history": "monthly event history",
                "required_identifiers": ["event_id", "account_ref"],
                "dimensions_relationships": ["account_ref -> account"],
                "freshness_expectation": "data complete within 30 minutes",
                "correctness_expectation": "no duplicate event contribution",
                "security_governance_boundary": "synthetic tenant scope only",
                "unusable_conditions": ["fanout changes event counts", "tenant scope cannot be preserved"]
            },
            "modeling_questions": [
                {"question_id": "MQ-ENTITY", "dimension": "entity_boundary", "question": "What is one event?", "status": "supported", "blocking": true, "evidence_needed": "bounded requirement and event contract"},
                {"question_id": "MQ-GRAIN", "dimension": "grain", "question": "What is the required row grain?", "status": "supported", "blocking": true, "evidence_needed": "consumer contract and live counts"},
                {"question_id": "MQ-KEY", "dimension": "key", "question": "Is event_id stable and unique?", "status": "supported", "blocking": true, "evidence_needed": "targeted duplicate check"},
                {"question_id": "MQ-JOIN", "dimension": "join_cardinality", "question": "Does account enrichment preserve event grain?", "status": "supported", "blocking": true, "evidence_needed": "two-sided cardinality check"},
                {"question_id": "MQ-AUTH", "dimension": "source_authority", "question": "Which source owns identity and event time?", "status": "resolved", "blocking": true, "evidence_needed": "source ownership evidence"},
                {"question_id": "MQ-TIME", "dimension": "temporal_semantics", "question": "Which timestamp is business event time?", "status": "supported", "blocking": true, "evidence_needed": "requirement plus observed timestamps"},
                {"question_id": "MQ-DEDUP", "dimension": "deduplication", "question": "How are retries reconciled?", "status": "supported", "blocking": true, "evidence_needed": "duplicate/replay evidence"},
                {"question_id": "MQ-SCHEMA", "dimension": "schema_scope", "question": "Which versions are covered?", "status": "supported", "blocking": true, "evidence_needed": "version-bounded evidence"},
                {"question_id": "MQ-GOLD", "dimension": "gold_fit", "question": "Can the candidate satisfy the consumer?", "status": "supported", "blocking": true, "evidence_needed": "consumer-fit check"}
            ],
            "source_roles": [
                {
                    "scope": "event identity",
                    "source_id": "SRC-SCHEMA",
                    "role": "authoritative",
                    "status": "observed",
                    "evidence_refs": ["repo://synthetic/contracts/order-event-v3#idempotency-key"]
                },
                {
                    "scope": "consumer business rule",
                    "source_id": "SRC-REQ",
                    "role": "authoritative",
                    "status": "verified",
                    "evidence_refs": ["source://synthetic/checkout-requirement-v1#idempotency"]
                }
            ],
            "candidate": {
                "status": "candidate",
                "entity_or_event": "service event",
                "grain": "one row per service event",
                "candidate_keys": ["event_id"],
                "relationships": ["event.account_ref -> account.account_ref many-to-one"],
                "temporal_semantics": "event_time is business time; ingest_time measures arrival",
                "deduplication_semantics": "deduplicate retry copies by event_id within supported schema scope",
                "schema_scope": "synthetic v3 contract in the bounded test window",
                "gold_fit": "candidate_fit",
                "evidence_refs": [
                    "source://synthetic/checkout-requirement-v1#idempotency",
                    "repo://synthetic/contracts/order-event-v3#idempotency-key"
                ],
                "unknown_refs": [],
                "production_approved": false
            }
        }
        return value

    def test_valid_synthetic_fixture_passes(self) -> None:
        self.assertEqual([], self.validate(copy.deepcopy(self.base)))

    def test_valid_modeling_pack_passes(self) -> None:
        self.assertEqual([], self.validate(self.make_modeling_pack()))

    def test_synthetic_fixture_cannot_claim_downstream_use(self) -> None:
        value = copy.deepcopy(self.base)
        value["downstream_adoption_status"] = "used_once"
        self.assertInvalidContains(value, "not_observed")

    def test_selected_source_must_be_authorized(self) -> None:
        value = copy.deepcopy(self.base)
        value["sources"][0]["access_status"] = "denied"
        self.assertInvalidContains(value, "selected source must be authorized")

    def test_selected_source_must_be_current(self) -> None:
        value = copy.deepcopy(self.base)
        value["sources"][0]["freshness_status"] = "stale"
        self.assertInvalidContains(value, "selected source must be current")

    def test_selected_source_must_not_be_expired(self) -> None:
        value = copy.deepcopy(self.base)
        value["sources"][0]["expires_at"] = "2026-08-01T00:00:00Z"
        self.assertInvalidContains(value, "selected source is expired")

    def test_context_item_must_fit_source_authority(self) -> None:
        value = copy.deepcopy(self.base)
        value["context_items"][0]["information_class"] = "system_constraint"
        self.assertInvalidContains(value, "outside source authority_for")

    def test_context_item_cannot_use_conditional_source(self) -> None:
        value = copy.deepcopy(self.base)
        value["context_items"][0]["source_id"] = "SRC-OLD-ADR"
        value["context_items"][0]["information_class"] = "historical_decision"
        self.assertInvalidContains(value, "selection_status=selected")

    def test_declared_selected_tokens_must_equal_item_sum(self) -> None:
        value = copy.deepcopy(self.base)
        value["context_budget"]["selected_tokens"] = 199
        self.assertInvalidContains(value, "must equal context item token sum")

    def test_budget_overflow_fails(self) -> None:
        value = copy.deepcopy(self.base)
        value["context_budget"]["max_tokens"] = 150
        self.assertInvalidContains(value, "exceed context_budget.max_tokens")

    def test_blocking_unknown_prevents_answerable(self) -> None:
        value = copy.deepcopy(self.base)
        value["unknowns"][0]["blocking"] = True
        self.assertInvalidContains(value, "blocking unknown")

    def test_unresolved_blocking_conflict_prevents_answerable(self) -> None:
        value = copy.deepcopy(self.base)
        value["conflicts"] = [
            {
                "conflict_id": "C-001",
                "item_refs": ["CTX-001", "CTX-002"],
                "source_refs": ["SRC-REQ", "SRC-SCHEMA"],
                "summary": "Synthetic requirement and schema interpretations conflict.",
                "blocking": True,
                "status": "unresolved",
                "next_action": "Route to the accountable owner for adjudication."
            }
        ]
        self.assertInvalidContains(value, "blocking conflict")

    def test_unknowns_cannot_disappear_from_evidence_summary(self) -> None:
        value = copy.deepcopy(self.base)
        value["evidence_summary"]["unknown_refs"] = []
        self.assertInvalidContains(value, "must preserve every unknown_id")

    def test_conditional_source_requires_activation_action(self) -> None:
        value = copy.deepcopy(self.base)
        value["activation_plan"] = [
            entry for entry in value["activation_plan"] if entry["target_ref"] != "SRC-PRIVATE"
        ]
        self.assertInvalidContains(value, "conditional source SRC-PRIVATE requires an activation action")

    def test_evidence_refs_must_be_addressable(self) -> None:
        value = copy.deepcopy(self.base)
        value["context_items"][0]["evidence_refs"] = ["requirements.md#idempotency"]
        self.assertInvalidContains(value, "addressable")

    def test_authorization_deny_cannot_carry_selected_context(self) -> None:
        value = copy.deepcopy(self.base)
        value["authorization"]["decision"] = "deny"
        value["answerability"]["status"] = "blocked"
        self.assertInvalidContains(value, "deny cannot include selected sources")

    def test_answerable_requires_citations(self) -> None:
        value = copy.deepcopy(self.base)
        value["evidence_summary"]["citations"] = []
        self.assertInvalidContains(value, "requires at least one evidence citation")

    def test_unknown_top_level_field_fails_schema(self) -> None:
        value = copy.deepcopy(self.base)
        value["private_raw_dump"] = "must not be accepted"
        self.assertInvalidContains(value, "Additional properties are not allowed")

    def test_modeling_origin_requires_machine_contract(self) -> None:
        value = copy.deepcopy(self.base)
        value["task"]["origin"] = "modeling_decision"
        self.assertInvalidContains(value, "modeling_decision")

    def test_modeling_contract_requires_core_questions(self) -> None:
        value = self.make_modeling_pack()
        value["modeling_decision"]["modeling_questions"] = [
            question
            for question in value["modeling_decision"]["modeling_questions"]
            if question["dimension"] != "temporal_semantics"
        ]
        self.assertInvalidContains(value, "core modeling questions")

    def test_authoritative_source_role_cannot_be_inferred(self) -> None:
        value = self.make_modeling_pack()
        value["modeling_decision"]["source_roles"][0]["status"] = "inferred"
        self.assertInvalidContains(value, "authoritative role cannot be merely inferred")

    def test_candidate_cannot_hide_blocking_modeling_question(self) -> None:
        value = self.make_modeling_pack()
        value["modeling_decision"]["modeling_questions"][2]["status"] = "open"
        self.assertInvalidContains(value, "blocking modeling question")

    def test_candidate_status_must_match_answerability(self) -> None:
        value = self.make_modeling_pack()
        value["modeling_decision"]["candidate"]["status"] = "partial"
        self.assertInvalidContains(value, "inconsistent with answerability")

    def test_gold_fit_failure_requires_blocked_candidate(self) -> None:
        value = self.make_modeling_pack()
        value["modeling_decision"]["candidate"]["gold_fit"] = "failed"
        self.assertInvalidContains(value, "gold_fit=failed")

    def test_modeling_candidate_never_approves_production(self) -> None:
        value = self.make_modeling_pack()
        value["modeling_decision"]["candidate"]["production_approved"] = True
        self.assertInvalidContains(value, "False was expected")

    def test_modeling_candidate_unknown_refs_must_exist(self) -> None:
        value = self.make_modeling_pack()
        value["modeling_decision"]["candidate"]["unknown_refs"] = ["U-MISSING"]
        self.assertInvalidContains(value, "must reference declared unknowns")

    def test_relationship_requires_join_cardinality_question(self) -> None:
        value = self.make_modeling_pack()
        value["modeling_decision"]["modeling_questions"] = [
            question
            for question in value["modeling_decision"]["modeling_questions"]
            if question["dimension"] != "join_cardinality"
        ]
        self.assertInvalidContains(value, "join_cardinality")


if __name__ == "__main__":
    unittest.main()
