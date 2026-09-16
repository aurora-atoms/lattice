from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_esp32_demo_rebuild_contract.py"
SPEC = importlib.util.spec_from_file_location("validate_esp32_demo_rebuild_contract", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

CONTRACT_PATH = (
    ROOT
    / "examples"
    / "esp32-demo-source-free-rebuild"
    / "rebuild-contract.v1.json"
)


class Esp32DemoRebuildContractTests(unittest.TestCase):
    def load_contract(self) -> dict:
        return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    def validate_mutation(self, value: dict) -> list[str]:
        return MODULE.schema_errors(value) + MODULE.semantic_errors(value)

    def test_committed_contract_validates(self) -> None:
        self.assertEqual([], MODULE.validate_contract(CONTRACT_PATH))

    def test_source_code_inclusion_is_rejected(self) -> None:
        value = self.load_contract()
        value["public_boundary"]["source_code_included"] = True
        errors = self.validate_mutation(value)
        self.assertTrue(errors)

    def test_legal_clean_room_claim_is_rejected(self) -> None:
        value = self.load_contract()
        value["public_boundary"]["legal_clean_room_claim"] = True
        errors = self.validate_mutation(value)
        self.assertTrue(errors)

    def test_controller_target_cannot_become_actual_source(self) -> None:
        value = self.load_contract()
        value["mission"]["actual_state_source"] = "controller_target"
        value["mission"]["controller_targets_are_intent_only"] = False
        errors = self.validate_mutation(value)
        self.assertTrue(any("actual_state_source" in error for error in errors))

    def test_esp32_cannot_take_over_formation_planning(self) -> None:
        value = self.load_contract()
        roles = {item["id"]: item for item in value["system_roles"]}
        roles["esp32"]["owns"].append("formation_geometry")
        roles["esp32"]["must_not"].remove("plan_formations")
        errors = self.validate_mutation(value)
        self.assertTrue(any("system_roles[esp32]" in error for error in errors))

    def test_browser_cannot_render_controller_targets_as_actual(self) -> None:
        value = self.load_contract()
        roles = {item["id"]: item for item in value["system_roles"]}
        roles["browser_ui"]["must_not"] = ["invent_missing_motion"]
        errors = self.validate_mutation(value)
        self.assertTrue(any("system_roles[browser_ui].must_not" in error for error in errors))

    def test_geo_lock_cannot_ignore_partial_coverage(self) -> None:
        value = self.load_contract()
        value["geo_contract"]["camera_acquisition"][
            "requires_selected_operator_and_all_controlled_drones"
        ] = False
        errors = self.validate_mutation(value)
        self.assertTrue(
            any("requires_selected_operator_and_all_controlled_drones" in error for error in errors)
        )

    def test_geo_refresh_must_reacquire_near_current_path_segment(self) -> None:
        value = self.load_contract()
        value["geo_contract"]["camera_acquisition"][
            "refresh_or_reselection_reacquires_near_current_path_segment"
        ] = False
        errors = self.validate_mutation(value)
        self.assertTrue(any("refresh_or_reselection" in error for error in errors))

    def test_silence_recovery_cannot_be_promoted_without_explicit_contract_change(self) -> None:
        value = self.load_contract()
        value["scenario_contract"]["next_required"]["status"] = "IMPLEMENTED_SOFTWARE"
        value["scenario_contract"]["next_required"]["required_for_baseline"] = True
        errors = self.validate_mutation(value)
        self.assertTrue(errors)

    def test_new_scenario_cannot_be_silently_added_to_baseline(self) -> None:
        value = self.load_contract()
        value["scenario_contract"]["baseline_required"].append("new-surprise-scenario")
        errors = self.validate_mutation(value)
        self.assertTrue(any("scenario.baseline_required" in error for error in errors))

    def test_acceptance_inventory_is_frozen(self) -> None:
        value = self.load_contract()
        value["acceptance_matrix"].append(
            {
                "id": "R12_NEW_SCENARIO",
                "required_for_baseline": True,
                "pass": "A new scenario appears without an explicit contract version change and review.",
            }
        )
        errors = self.validate_mutation(value)
        self.assertTrue(any("acceptance_matrix IDs" in error for error in errors))

    def test_implementation_freedom_cannot_remove_source_independence(self) -> None:
        value = self.load_contract()
        value["implementation_freedom"]["may_change"].remove("directory_layout")
        errors = self.validate_mutation(value)
        self.assertTrue(any("implementation_freedom.may_change" in error for error in errors))

    def test_unknown_top_level_field_is_rejected_by_schema(self) -> None:
        value = self.load_contract()
        value["private_source_repo"] = "not-allowed"
        errors = self.validate_mutation(value)
        self.assertTrue(any("Additional properties" in error for error in errors))

    def test_cli_accepts_explicit_contract_path(self) -> None:
        value = self.load_contract()
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "contract.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            self.assertEqual([], MODULE.validate_contract(path))


if __name__ == "__main__":
    unittest.main()
