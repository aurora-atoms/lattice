from __future__ import annotations

import importlib.util
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills" / "feature-delivery-case" / "scripts" / "validate_feature_delivery_case.py"
SPEC = importlib.util.spec_from_file_location("validate_feature_delivery_case", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
validate_case = MODULE.validate_case


def valid_case() -> dict:
    return {
        "case_profile": "lifecycle_v1",
        "case_id": "fdc_test_001",
        "revision": 2,
        "title": "Add bounded readiness validation",
        "lifecycle_status": "in_progress",
        "accountable_owner": "feature owner",
        "purpose": {
            "why": "Prevent unsupported readiness claims.",
            "beneficiaries": ["delivery team"],
            "expected_change": "Readiness is evidence-linked and deterministic.",
            "success_signals": ["invalid ready claims fail validation"],
        },
        "boundary": {
            "feature_boundary": "Feature Delivery Case lifecycle validation only.",
            "in_scope": ["readiness validation"],
            "out_of_scope": ["production deployment"],
            "affected_surfaces": ["case validator"],
            "impact_areas": ["delivery governance"],
            "compatibility_constraints": ["keep v1 JSONL projection"],
            "non_goals": ["approve merge"],
        },
        "acceptance_criteria": [
            {"id": "AC1", "statement": "Ready requires current evidence.", "evidence_requirements": ["test evidence"]}
        ],
        "context_coverage": [
            {"category": category, "status": "not_applicable", "search_scope": "test fixture", "source_refs": [], "findings": []}
            for category in sorted(MODULE.COVERAGE_CATEGORIES)
        ],
        "decision_log": [
            {
                "id": "D1",
                "status": "active",
                "choice": "Use deterministic readiness enum.",
                "decided_at": "2026-07-25T00:00:00Z",
                "decision_owner": "feature owner",
                "rationale": "Avoid vague readiness language.",
                "alternatives": ["free-form prose"],
                "applicability_conditions": ["lifecycle_v1"],
                "evidence_refs": ["E1"],
                "review_condition": {"review_at": None, "event_triggers": ["readiness enum changes"]},
                "supersedes": [],
            }
        ],
        "assumption_log": [
            {
                "id": "A1",
                "status": "active",
                "statement": "Evidence remains valid through the review window.",
                "basis": "bounded test fixture",
                "owner": "feature owner",
                "confidence": "high",
                "validity_conditions": ["validator unchanged"],
                "expires_at": "2027-01-01T00:00:00Z",
                "review_condition": {"review_at": None, "event_triggers": ["validator changes"]},
                "impact_if_false": "Readiness must be reassessed.",
                "evidence_refs": ["E1"],
            }
        ],
        "dependencies": [
            {
                "id": "DEP1",
                "kind": "technical",
                "name": "Python runtime",
                "state": "satisfied",
                "blocking": True,
                "owner": "maintainer",
                "required_participants": [],
                "evidence_refs": ["E1"],
                "review_triggers": ["runtime changes"],
            }
        ],
        "evidence_ledger": [
            {
                "id": "E1",
                "kind": "test",
                "source_ref": "tests/test_feature_delivery_case.py",
                "relation": "supports",
                "supports_refs": ["AC1", "D1", "A1"],
                "result": "pass",
                "observed_at": "2026-07-25T00:00:00Z",
                "expires_at": "2027-01-01T00:00:00Z",
                "confidence": "high",
                "source_authority": "CI",
            }
        ],
        "risk_ledger": [
            {
                "id": "R1",
                "kind": "direct",
                "statement": "Schema and validator can drift.",
                "component_refs": [],
                "owner": "maintainer",
                "exposure": "medium",
                "controls": ["CI tests"],
                "evidence_refs": ["E1"],
                "review_triggers": ["schema changes"],
                "status": "controlled",
            }
        ],
        "unresolved_items": [],
        "artifacts": [
            {
                "id": "ART1",
                "kind": "readiness_card",
                "uri": "reports/readiness-card.md",
                "case_revision": 2,
                "owner": "feature owner",
                "evidence_refs": ["E1"],
                "generated_at": "2026-07-25T00:00:00Z",
                "expires_at": "2027-01-01T00:00:00Z",
                "review_triggers": ["evidence changes"],
                "authority_note": "Assessment only; accountable owners retain approval authority.",
            }
        ],
        "readiness": {
            "target": "review",
            "result": "ready",
            "criteria": [{"id": "RG1", "status": "pass", "evidence_refs": ["E1"]}],
            "blocking_item_refs": [],
            "evidence_refs": ["E1"],
            "assessed_at": "2026-07-25T00:00:00Z",
            "expires_at": "2027-01-01T00:00:00Z",
            "review_triggers": ["scope or evidence changes"],
            "authority_note": "Assessment only; accountable owners retain approval authority.",
        },
    }


class FeatureDeliveryCaseValidationTests(unittest.TestCase):
    NOW = datetime(2026, 7, 25, tzinfo=timezone.utc)

    def test_valid_ready_case_passes(self) -> None:
        self.assertEqual([], validate_case(valid_case(), self.NOW))

    def test_ready_case_rejects_expired_active_assumption(self) -> None:
        case = valid_case()
        case["assumption_log"][0]["expires_at"] = "2026-07-24T00:00:00Z"
        errors = validate_case(case, self.NOW)
        self.assertTrue(any("active but expired" in item for item in errors))
        self.assertTrue(any("ready result conflicts" in item for item in errors))

    def test_ready_case_rejects_blocking_dependency(self) -> None:
        case = valid_case()
        case["dependencies"][0]["state"] = "pending"
        errors = validate_case(case, self.NOW)
        self.assertTrue(any("blocking dependencies" in item for item in errors))

    def test_pending_context_is_rejected(self) -> None:
        case = valid_case()
        case["context_coverage"][0]["status"] = "pending"
        errors = validate_case(case, self.NOW)
        self.assertTrue(any("remains pending" in item for item in errors))

    def test_compound_risk_requires_multiple_components(self) -> None:
        case = valid_case()
        case["risk_ledger"][0]["kind"] = "compound"
        case["risk_ledger"][0]["component_refs"] = ["DEP1"]
        errors = validate_case(case, self.NOW)
        self.assertTrue(any("at least two components" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
