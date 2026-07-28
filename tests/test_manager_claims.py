from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_manager_claims.py"
SPEC = importlib.util.spec_from_file_location("validate_manager_claims", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def evidence(evidence_id: str = "ev-1", evidence_type: str = "validation") -> dict:
    return {
        "evidence_id": evidence_id,
        "evidence_type": evidence_type,
        "source_ref": "private://bounded/source",
        "relation": "supports",
        "observed_at": "2026-07-28T00:00:00Z",
        "source_authority": "private repository owner",
        "evidence_origin": "real_restricted",
        "feature_delivery_case_id": "FDC-1",
        "summary": "Bounded evidence summary.",
        "integrity_sha256": None,
    }


def claim(
    claim_id: str,
    kind: str,
    *,
    classification: str = "OBSERVED",
    refs: list[str] | None = None,
) -> dict:
    return {
        "claim_id": claim_id,
        "classification": classification,
        "claim_kind": kind,
        "statement": f"Bounded {kind} statement.",
        "presentation": "unknown" if classification == "UNKNOWN" else "qualified",
        "evidence_refs": ["ev-1"] if refs is None else refs,
        "evidence_origin": "real_restricted",
        "scope": "FDC-1",
        "method": "Compared cited states." if classification == "DERIVED" else None,
        "judgment_owner": "reviewer" if classification == "JUDGED" else None,
        "unknown_reason": "Evidence is unavailable." if classification == "UNKNOWN" else None,
        "limitations": [],
        "approval_authority": None,
    }


def brief() -> dict:
    return {
        "contract": "lat.manager-delivery-brief.v1",
        "contract_version": "1.0.0",
        "brief_id": "brief-1",
        "asset_pack_id": "pack-1",
        "simulation_status": "real_downstream",
        "downstream_adoption_status": "task_scoped",
        "evidence_origin": "real_restricted",
        "scope": "FDC-1",
        "version": "1.0.0",
        "claims": [
            claim("c-current", "current_delivery"),
            claim("c-asset", "reusable_asset"),
            claim("c-before", "before_state"),
            claim("c-after", "after_state", classification="DERIVED"),
            claim("c-next", "next_use", classification="JUDGED"),
        ],
        "human_challenge": {
            "challenge_present": True,
            "challenger_role": "reviewer",
            "challenge_summary": "Scope was too broad.",
            "resulting_change_or_open_issue": "Narrowed task scope.",
            "review_ref": "ev-1",
        },
        "known_limitations": ["One bounded case only."],
        "unresolved_unknowns": ["No later use observed."],
        "next_use_entry": "Revalidate on the next bounded case.",
        "manager_decision": "Review task-scoped continuation.",
        "human_review_ref": "ev-1",
        "governance_approval_ref": None,
    }


class ManagerClaimTests(unittest.TestCase):
    def test_valid_bounded_brief(self) -> None:
        self.assertEqual([], MODULE.validate_manager_brief(brief(), [evidence()]))

    def test_observed_without_evidence_fails(self) -> None:
        value = brief()
        value["claims"][0]["evidence_refs"] = []
        errors = MODULE.validate_manager_brief(value, [evidence()])
        self.assertTrue(any("OBSERVED requires evidence_refs" in item for item in errors))

    def test_dangling_evidence_ref_fails(self) -> None:
        value = brief()
        value["claims"][0]["evidence_refs"] = ["missing"]
        errors = MODULE.validate_manager_brief(value, [evidence()])
        self.assertTrue(any("dangling evidence refs" in item for item in errors))

    def test_observed_requires_supporting_relation(self) -> None:
        record = evidence()
        record["relation"] = "inconclusive"
        errors = MODULE.validate_manager_brief(brief(), [record])
        self.assertTrue(any("OBSERVED requires supporting evidence" in item for item in errors))

    def test_claim_and_evidence_origin_must_match_brief(self) -> None:
        record = evidence()
        record["evidence_origin"] = "real_sanitized"
        errors = MODULE.validate_manager_brief(brief(), [record])
        self.assertTrue(any("cited evidence origin differs" in item for item in errors))

    def test_unknown_presented_as_fact_fails(self) -> None:
        value = brief()
        value["claims"][0] = claim(
            "c-current", "current_delivery", classification="UNKNOWN", refs=[]
        )
        value["claims"][0]["presentation"] = "fact"
        errors = MODULE.validate_manager_brief(value, [evidence()])
        self.assertTrue(any("UNKNOWN cannot be presented as fact" in item for item in errors))

    def test_one_use_cannot_be_reuse(self) -> None:
        value = brief()
        value["downstream_adoption_status"] = "used_once"
        value["claims"].append(claim("c-reuse", "reuse"))
        errors = MODULE.validate_manager_brief(value, [evidence("ev-1", "usage_observation")])
        self.assertTrue(any("reuse cannot be claimed" in item for item in errors))

    def test_unknown_reuse_is_preserved_without_overclaim(self) -> None:
        value = brief()
        value["claims"].append(
            claim("c-reuse", "reuse", classification="UNKNOWN", refs=[])
        )
        errors = MODULE.validate_manager_brief(value, [evidence()])
        self.assertEqual([], errors)

    def test_one_case_cannot_be_team_wide(self) -> None:
        value = brief()
        value["claims"].append(claim("c-team", "team_adoption"))
        errors = MODULE.validate_manager_brief(value, [evidence()])
        self.assertTrue(any("team-wide language requires team_available" in item for item in errors))

    def test_hidden_limitations_fail(self) -> None:
        value = brief()
        value["known_limitations"] = []
        errors = MODULE.validate_manager_brief(value, [evidence()])
        self.assertTrue(any("known_limitations" in item for item in errors))

    def test_deliveryyield_cannot_approve(self) -> None:
        value = brief()
        value["claims"][0]["approval_authority"] = "DeliveryYield"
        errors = MODULE.validate_manager_brief(value, [evidence()])
        self.assertTrue(any("DeliveryYield" in item for item in errors))

    def test_synthetic_cannot_claim_used_once(self) -> None:
        value = brief()
        value["simulation_status"] = "synthetic_reference"
        value["evidence_origin"] = "synthetic"
        value["downstream_adoption_status"] = "used_once"
        value["human_review_ref"] = None
        for item in value["claims"]:
            item["evidence_origin"] = "synthetic"
        synthetic = evidence()
        synthetic["evidence_origin"] = "synthetic"
        errors = MODULE.validate_manager_brief(value, [synthetic])
        self.assertTrue(any("must remain not_observed" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
