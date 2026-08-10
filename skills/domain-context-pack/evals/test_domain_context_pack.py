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

    def test_valid_synthetic_fixture_passes(self) -> None:
        self.assertEqual([], self.validate(copy.deepcopy(self.base)))

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


if __name__ == "__main__":
    unittest.main()
