from __future__ import annotations

import unittest

from scripts.validate_skill_change_contract import validate_direction_fit


class DirectionFitValidationTests(unittest.TestCase):
    def test_accepts_current_product_delivery(self) -> None:
        text = """
## Direction Fit

primary_value_path: current_product_delivery
direction_verdict: proceed
evidence_refs: feature_delivery_case/example-123
existing_capability_gap: Existing capabilities do not validate this user-facing outcome.
user_outcome: A named user can complete the target workflow with observable acceptance evidence.
"""
        self.assertEqual(validate_direction_fit(text), [])

    def test_accepts_strategic_asset(self) -> None:
        text = """
## Direction Fit

primary_value_path: strategic_asset
direction_verdict: proceed
evidence_refs: experiment/example-benchmark-1
existing_capability_gap: Existing validators cannot reproduce the target environment.
proprietary_input: Company-specific operating constraints represented by synthetic public fixtures.
verifiable_artifact: A repeatable benchmark and validation harness.
second_use: Product design review and regression qualification.
maintenance_owner: capability-governance-owner
"""
        self.assertEqual(validate_direction_fit(text), [])

    def test_accepts_team_reuse_with_second_use_evidence(self) -> None:
        text = """
## Direction Fit

primary_value_path: team_reuse
direction_verdict: proceed
evidence_refs: delivery-case/one, delivery-case/two
existing_capability_gap: Existing guidance requires the original author's private context.
second_use_evidence: Two independent delivery cases requested the same bounded capability.
adoption_owner: team-capability-owner
"""
        self.assertEqual(validate_direction_fit(text), [])

    def test_rejects_missing_direction_section(self) -> None:
        errors = validate_direction_fit("# Skill\n")
        self.assertTrue(any("Direction Fit" in error for error in errors))

    def test_rejects_non_proceed_new_skill(self) -> None:
        text = """
## Direction Fit

primary_value_path: current_product_delivery
direction_verdict: retain_candidate
evidence_refs: idea/example
existing_capability_gap: The gap is not yet validated.
user_outcome: A possible future outcome.
"""
        errors = validate_direction_fit(text)
        self.assertTrue(any("requires direction_verdict 'proceed'" in error for error in errors))

    def test_rejects_placeholder_fields(self) -> None:
        text = """
## Direction Fit

primary_value_path: strategic_asset
direction_verdict: proceed
evidence_refs: <evidence>
existing_capability_gap: <gap>
proprietary_input: <input>
verifiable_artifact: <artifact>
second_use: <second use>
maintenance_owner: <owner>
"""
        errors = validate_direction_fit(text)
        self.assertGreaterEqual(len(errors), 6)
        self.assertTrue(all("placeholder" in error for error in errors))


if __name__ == "__main__":
    unittest.main()