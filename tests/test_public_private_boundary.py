from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_public_private_boundary.py"
SPEC = importlib.util.spec_from_file_location("validate_public_private_boundary", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def adoption(
    status: str,
    *,
    simulation: str = "real_downstream",
    evidence: list[str] | None = None,
    human_review: str | None = "review-1",
    governance: str | None = None,
) -> dict:
    return {
        "public_capability_id": "skill:demo@1.0.0",
        "simulation_status": simulation,
        "downstream_adoption_status": status,
        "evidence_refs": evidence or [],
        "human_review_ref": human_review,
        "governance_approval_ref": governance,
    }


class PublicPrivateBoundaryTests(unittest.TestCase):
    def test_synthetic_used_once_fails(self) -> None:
        value = adoption(
            "used_once",
            simulation="synthetic_reference",
            evidence=["synthetic"],
            human_review=None,
        )
        errors = MODULE.validate_adoption_record(value)
        self.assertTrue(any("must remain not_observed" in item for item in errors))

    def test_real_used_once_requires_evidence(self) -> None:
        errors = MODULE.validate_adoption_record(adoption("used_once"))
        self.assertTrue(any("requires real evidence" in item for item in errors))

    def test_reused_requires_later_use_evidence(self) -> None:
        errors = MODULE.validate_adoption_record(
            adoption("reused", evidence=["one-use"])
        )
        self.assertTrue(any("later-use evidence" in item for item in errors))

    def test_team_available_requires_governance_approval(self) -> None:
        errors = MODULE.validate_adoption_record(
            adoption("team_available", evidence=["use-1", "use-2"])
        )
        self.assertTrue(any("separate governance approval" in item for item in errors))

    def test_transition_cannot_skip(self) -> None:
        errors = MODULE.validate_transition("imported", "used_once")
        self.assertTrue(any("cannot skip" in item for item in errors))

    def test_valid_next_transition(self) -> None:
        self.assertEqual([], MODULE.validate_transition("used_once", "reused"))

    def test_public_fixture_rejects_private_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "fixture.jsonl"
            path.write_text(
                json.dumps(
                    {
                        "type": "example",
                        "id": "private-path",
                        "payload": {"path": "/Users/example/private/repo"},
                        "constraints": {
                            "ip_boundary": "synthetic",
                            "simulation_status": "synthetic_reference",
                            "downstream_adoption_status": "not_observed",
                        },
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            errors = MODULE.fixture_errors(path)
            self.assertTrue(any("absolute user path" in item for item in errors))

    def test_deliveryyield_cannot_approve_promotion(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "fixture.jsonl"
            path.write_text(
                json.dumps(
                    {
                        "type": "reusable_asset.review",
                        "id": "deliveryyield-review",
                        "source": "DeliveryYield",
                        "payload": {"decision": "approved"},
                        "constraints": {
                            "ip_boundary": "synthetic",
                            "simulation_status": "synthetic_reference",
                            "downstream_adoption_status": "not_observed",
                        },
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            errors = MODULE.fixture_errors(path)
            self.assertTrue(any("DeliveryYield cannot approve" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
