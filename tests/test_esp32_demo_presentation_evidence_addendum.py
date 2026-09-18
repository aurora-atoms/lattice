from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_esp32_demo_presentation_evidence_addendum.py"
SPEC = importlib.util.spec_from_file_location("validate_esp32_demo_presentation_evidence_addendum", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

ADDENDUM_PATH = ROOT / "examples" / "esp32-demo-source-free-rebuild" / "presentation-evidence-addendum.v1.json"


class Esp32DemoPresentationEvidenceAddendumTests(unittest.TestCase):
    def load_addendum(self) -> dict:
        return json.loads(ADDENDUM_PATH.read_text(encoding="utf-8"))

    def validate_mutation(self, value: dict) -> list[str]:
        return MODULE.schema_errors(value) + MODULE.semantic_errors(value)

    def test_committed_addendum_validates(self) -> None:
        self.assertEqual([], MODULE.validate_addendum(ADDENDUM_PATH))

    def test_product_and_source_remain_separate_browser_pages(self) -> None:
        value = self.load_addendum()
        value["playwright_evidence"]["source_and_product_are_separate_browser_pages"] = False
        self.assertTrue(self.validate_mutation(value))

    def test_same_capture_frame_must_not_be_required(self) -> None:
        value = self.load_addendum()
        value["playwright_evidence"]["same_capture_frame_required"] = True
        errors = self.validate_mutation(value)
        self.assertTrue(any("same_capture_frame_required" in error for error in errors))

    def test_separate_panel_captures_are_required(self) -> None:
        value = self.load_addendum()
        value["playwright_evidence"]["separate_panel_captures_required"] = False
        self.assertTrue(self.validate_mutation(value))

    def test_capture_time_skew_must_be_recorded(self) -> None:
        value = self.load_addendum()
        value["playwright_evidence"]["capture_time_skew_must_be_recorded"] = False
        self.assertTrue(self.validate_mutation(value))

    def test_composition_cannot_alter_product_native_alerts(self) -> None:
        value = self.load_addendum()
        value["playwright_evidence"]["forbidden_actions"].remove(
            "alter_product_native_alerts_or_highlights_in_composition"
        )
        errors = self.validate_mutation(value)
        self.assertTrue(any("forbidden_actions" in error for error in errors))

    def test_playwright_cannot_be_promoted_to_dom_semantic_verifier(self) -> None:
        value = self.load_addendum()
        value["playwright_evidence"]["forbidden_actions"].remove("read_product_dom_as_semantic_evidence")
        errors = self.validate_mutation(value)
        self.assertTrue(any("forbidden_actions" in error for error in errors))

    def test_visual_observation_is_frozen_before_log_confirmation(self) -> None:
        value = self.load_addendum()
        value["comparison_evidence"]["visual_observation_must_be_frozen_before_log_confirmation"] = False
        self.assertTrue(self.validate_mutation(value))

    def test_log_confirmation_is_not_a_speed_competitor(self) -> None:
        value = self.load_addendum()
        value["comparison_evidence"]["log_confirmation_is_not_a_speed_competitor"] = False
        self.assertTrue(self.validate_mutation(value))

    def test_visual_vs_log_speed_claim_is_forbidden(self) -> None:
        value = self.load_addendum()
        value["comparison_evidence"]["visual_vs_log_speed_claim_allowed"] = True
        self.assertTrue(self.validate_mutation(value))

    def test_only_test_added_pre_highlighting_is_forbidden(self) -> None:
        value = self.load_addendum()
        value["comparison_evidence"]["test_added_fault_annotation_before_visual_observation_is_frozen"] = True
        self.assertTrue(self.validate_mutation(value))

    def test_product_native_alerts_must_be_preserved(self) -> None:
        value = self.load_addendum()
        value["comparison_evidence"]["product_native_alerts_and_highlights_must_be_preserved"] = False
        self.assertTrue(self.validate_mutation(value))

    def test_duplicate_signal_is_a_proof_checkpoint(self) -> None:
        value = self.load_addendum()
        value["comparison_evidence"]["proof_checkpoints"].remove("duplicate-signal-window")
        errors = self.validate_mutation(value)
        self.assertTrue(any("proof_checkpoints" in error for error in errors))

    def test_downstream_record_is_minimal_but_attests_same_stimulus(self) -> None:
        value = self.load_addendum()
        value["comparison_evidence"]["required_downstream_record_fields"].remove("same_stimulus_delivery_attestation")
        self.assertTrue(self.validate_mutation(value))

    def test_contract_cannot_claim_visual_speed_superiority(self) -> None:
        value = self.load_addendum()
        value["comparison_evidence"]["forbidden_claims"].remove("visual_comparison_is_faster_than_log_analysis")
        self.assertTrue(self.validate_mutation(value))

    def test_left_panel_cannot_use_controller_targets_as_truth(self) -> None:
        value = self.load_addendum()
        value["playwright_evidence"]["left_panel"]["source"] = "controller_targets"
        self.assertTrue(self.validate_mutation(value))

    def test_stroke_trail_cannot_invent_missing_motion(self) -> None:
        value = self.load_addendum()
        value["main_demo"]["drawing_mode"]["visual_trail_must_not_invent_missing_motion"] = False
        self.assertTrue(self.validate_mutation(value))

    def test_3d_formation_must_remain_recognizable_in_xy_projection(self) -> None:
        value = self.load_addendum()
        value["main_demo"]["horizontal_projection"]["top_down_projection_must_be_recognizable"] = False
        self.assertTrue(self.validate_mutation(value))

    def test_mission_cannot_reset_between_stages(self) -> None:
        value = self.load_addendum()
        value["main_demo"]["mission_continuity"]["config_reset_between_stages"] = True
        self.assertTrue(self.validate_mutation(value))

    def test_phoenix_cannot_become_validation_proof(self) -> None:
        value = self.load_addendum()
        value["main_demo"]["phoenix"]["may_be_used_as_validation_proof"] = True
        self.assertTrue(self.validate_mutation(value))

    def test_identity_stress_cannot_change_mission_roster(self) -> None:
        value = self.load_addendum()
        value["identity_test_semantics"]["identity_stress_must_not_change_mission_roster"] = False
        self.assertTrue(self.validate_mutation(value))

    def test_checkpoint_inventory_is_frozen(self) -> None:
        value = self.load_addendum()
        value["evidence_checkpoints"].append("unreviewed-surprise-checkpoint")
        self.assertTrue(self.validate_mutation(value))

    def test_unknown_top_level_field_is_rejected(self) -> None:
        value = self.load_addendum()
        value["private_product_url"] = "not-allowed"
        errors = self.validate_mutation(value)
        self.assertTrue(any("Additional properties" in error for error in errors))

    def test_cli_accepts_explicit_addendum_path(self) -> None:
        value = self.load_addendum()
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "addendum.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            self.assertEqual([], MODULE.validate_addendum(path))


if __name__ == "__main__":
    unittest.main()
