from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_esp32_demo_presentation_evidence_addendum.py"
SPEC = importlib.util.spec_from_file_location(
    "validate_esp32_demo_presentation_evidence_addendum", SCRIPT
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

ADDENDUM_PATH = (
    ROOT
    / "examples"
    / "esp32-demo-source-free-rebuild"
    / "presentation-evidence-addendum.v1.json"
)


class Esp32DemoPresentationEvidenceAddendumTests(unittest.TestCase):
    def load_addendum(self) -> dict:
        return json.loads(ADDENDUM_PATH.read_text(encoding="utf-8"))

    def validate_mutation(self, value: dict) -> list[str]:
        return MODULE.schema_errors(value) + MODULE.semantic_errors(value)

    def test_committed_addendum_validates(self) -> None:
        self.assertEqual([], MODULE.validate_addendum(ADDENDUM_PATH))

    def test_playwright_cannot_be_promoted_to_dom_semantic_verifier(self) -> None:
        value = self.load_addendum()
        value["playwright_evidence"]["forbidden_actions"].remove(
            "read_product_dom_as_semantic_evidence"
        )
        value["playwright_evidence"]["allowed_actions"].append(
            "read_product_dom_as_semantic_evidence"
        )
        errors = self.validate_mutation(value)
        self.assertTrue(any("playwright" in error for error in errors))

    def test_playwright_cannot_inspect_product_network_payloads(self) -> None:
        value = self.load_addendum()
        value["playwright_evidence"]["forbidden_actions"].remove(
            "inspect_product_websocket_or_network_payloads"
        )
        errors = self.validate_mutation(value)
        self.assertTrue(any("forbidden_actions" in error for error in errors))

    def test_playwright_cannot_issue_automated_product_verdict(self) -> None:
        value = self.load_addendum()
        value["playwright_evidence"]["automated_image_diff_is_product_verdict"] = True
        self.assertTrue(self.validate_mutation(value))

    def test_public_repo_cannot_claim_runtime_screenshot_evidence(self) -> None:
        value = self.load_addendum()
        value["playwright_evidence"]["runtime_screenshots_committed_to_public_repo"] = True
        self.assertTrue(self.validate_mutation(value))

    def test_left_panel_cannot_use_controller_targets_as_truth(self) -> None:
        value = self.load_addendum()
        value["playwright_evidence"]["left_panel"]["source"] = "controller_targets"
        errors = self.validate_mutation(value)
        self.assertTrue(any("left_panel.source" in error for error in errors))

    def test_drawing_mode_must_remain_asmr_stroke_drawing(self) -> None:
        value = self.load_addendum()
        value["main_demo"]["drawing_mode"]["contract_id"] = "instant_formation"
        errors = self.validate_mutation(value)
        self.assertTrue(any("drawing.contract_id" in error for error in errors))

    def test_stroke_trail_cannot_invent_missing_motion(self) -> None:
        value = self.load_addendum()
        value["main_demo"]["drawing_mode"]["visual_trail_must_not_invent_missing_motion"] = False
        errors = self.validate_mutation(value)
        self.assertTrue(any("visual_trail_must_not_invent_missing_motion" in error for error in errors))

    def test_3d_formation_must_remain_recognizable_in_xy_projection(self) -> None:
        value = self.load_addendum()
        value["main_demo"]["horizontal_projection"]["top_down_projection_must_be_recognizable"] = False
        errors = self.validate_mutation(value)
        self.assertTrue(any("horizontal_projection.top_down_projection_must_be_recognizable" in error for error in errors))

    def test_shape_identity_cannot_depend_on_z_only(self) -> None:
        value = self.load_addendum()
        value["main_demo"]["horizontal_projection"]["z_only_separation_must_not_be_required_for_recognition"] = False
        errors = self.validate_mutation(value)
        self.assertTrue(any("z_only_separation_must_not_be_required_for_recognition" in error for error in errors))

    def test_mission_cannot_reset_between_stages(self) -> None:
        value = self.load_addendum()
        value["main_demo"]["mission_continuity"]["config_reset_between_stages"] = True
        errors = self.validate_mutation(value)
        self.assertTrue(any("config_reset_between_stages" in error for error in errors))

    def test_mission_cannot_respawn_swarm_between_stages(self) -> None:
        value = self.load_addendum()
        value["main_demo"]["mission_continuity"]["respawn_or_reseed_between_stages"] = True
        errors = self.validate_mutation(value)
        self.assertTrue(any("respawn_or_reseed_between_stages" in error for error in errors))

    def test_phoenix_must_be_mission_climax(self) -> None:
        value = self.load_addendum()
        value["main_demo"]["phoenix"]["in_main_sequence"] = False
        value["main_demo"]["phoenix"]["role"] = "standalone_showcase"
        errors = self.validate_mutation(value)
        self.assertTrue(any("phoenix" in error.lower() for error in errors))

    def test_phoenix_cannot_become_validation_proof(self) -> None:
        value = self.load_addendum()
        value["main_demo"]["phoenix"]["may_be_used_as_validation_proof"] = True
        self.assertTrue(self.validate_mutation(value))

    def test_silence_recovery_remains_first_new_scenario_gate(self) -> None:
        value = self.load_addendum()
        value["main_demo"]["first_new_scenario_gate"] = "identity-conflict"
        errors = self.validate_mutation(value)
        self.assertTrue(any("first_new_scenario_gate" in error for error in errors))

    def test_shared_remote_id_cannot_collapse_simulated_truth(self) -> None:
        value = self.load_addendum()
        value["identity_test_semantics"]["remote_id_alone_must_not_define_truth_entity_count"] = False
        self.assertTrue(self.validate_mutation(value))

    def test_identity_stress_cannot_change_mission_roster(self) -> None:
        value = self.load_addendum()
        value["identity_test_semantics"]["identity_stress_must_not_change_mission_roster"] = False
        self.assertTrue(self.validate_mutation(value))

    def test_duplicate_observation_and_shared_id_cases_stay_distinct(self) -> None:
        value = self.load_addendum()
        value["identity_test_semantics"]["shared_remote_id_case"] = (
            "many_observations_one_existing_truth_entity"
        )
        errors = self.validate_mutation(value)
        self.assertTrue(any("shared_remote_id_case" in error for error in errors))

    def test_checkpoint_inventory_is_frozen(self) -> None:
        value = self.load_addendum()
        value["evidence_checkpoints"].append("unreviewed-surprise-checkpoint")
        errors = self.validate_mutation(value)
        self.assertTrue(any("evidence_checkpoints" in error for error in errors))

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
