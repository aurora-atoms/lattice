#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate the ESP32 demo screenshot-only presentation/evidence addendum."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "jsonschema is required; install requirements-validation.txt"
    ) from exc

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ADDENDUM = (
    ROOT
    / "examples"
    / "esp32-demo-source-free-rebuild"
    / "presentation-evidence-addendum.v1.json"
)
CORE_CONTRACT_PATH = (
    ROOT
    / "examples"
    / "esp32-demo-source-free-rebuild"
    / "rebuild-contract.v1.json"
)
SCHEMA_PATH = (
    ROOT
    / "schemas"
    / "downstream"
    / "esp32-demo-presentation-evidence-addendum.v1.schema.json"
)

EXPECTED_SEQUENCE = [
    "multi-point-takeoff",
    "perfect-progressive-drawing",
    "single-target-silence-recovery",
    "landing-vs-airborne-disconnect",
    "duplicate-observation-dedup",
    "shared-remote-id-identity-conflict",
    "geo-visible-patrol",
    "distributed-landing",
]

EXPECTED_CHECKPOINTS = [
    "takeoff-established",
    "perfect-drawing-mid-stroke",
    "single-target-silent-peers-fresh",
    "same-target-recovered",
    "landed-target-vs-airborne-disconnected-target",
    "duplicate-observation-window",
    "shared-remote-id-two-targets",
    "shared-remote-id-three-targets",
    "geo-patrol-in-motion",
    "distributed-landing-complete",
]

EXPECTED_ALLOWED_ACTIONS = {
    "capture_left_panel_screenshot",
    "capture_right_panel_screenshot",
    "capture_combined_side_by_side_screenshot",
    "record_checkpoint_id_and_capture_time",
}

EXPECTED_FORBIDDEN_ACTIONS = {
    "read_product_dom_as_semantic_evidence",
    "inspect_product_api_payloads",
    "inspect_product_websocket_or_network_payloads",
    "derive_automated_product_pass_fail",
    "mutate_product_state_to_make_a_checkpoint_pass",
    "mutate_simulator_truth_to_match_product_output",
}

EXPECTED_STAGE_BEHAVIORS: dict[str, set[str]] = {
    "multi-point-takeoff": {
        "drones_may_start_from_different_positions",
        "accepted_telemetry_shows_takeoff_progression_before_cruise_motion",
        "no_controller_reference_position_is_rendered_as_actual",
    },
    "perfect-progressive-drawing": {
        "formation_does_not_pop_directly_into_final_state",
        "drones_progress_through_continuous_3d_waypoints",
        "accepted_telemetry_is_the_only_displayed_actual_state",
    },
    "single-target-silence-recovery": {
        "only_one_drone_is_silenced",
        "peers_remain_fresh",
        "last_known_position_is_preserved_while_silent",
        "recovery_reuses_same_runtime_drone_id",
    },
    "landing-vs-airborne-disconnect": {
        "landing_target_descends_before_telemetry_ceases",
        "disconnect_target_ceases_while_last_known_state_is_airborne",
        "simulated_source_state_does_not_relabel_disconnect_as_landing",
    },
    "duplicate-observation-dedup": {
        "one_runtime_drone_remains_one_simulated_truth_entity",
        "duplicate_observations_may_be_emitted_for_the_same_claimed_identity",
        "product_ui_response_is_recorded_only_by_screenshot",
    },
    "shared-remote-id-identity-conflict": {
        "truth_entity_count_can_progress_one_to_two_to_three",
        "distinct_runtime_drone_ids_are_preserved",
        "claimed_remote_id_may_be_shared",
        "shared_remote_id_must_not_collapse_simulated_truth_entities",
        "product_ui_response_is_recorded_only_by_screenshot",
    },
    "geo-visible-patrol": {
        "existing_doubtful_sound_precomputed_path_is_reused",
        "runtime_gis_lookup_is_not_added",
        "accepted_telemetry_remains_the_actual_state_source",
    },
    "distributed-landing": {
        "drones_may_land_at_different_points",
        "descent_is_visible_before_each_target_becomes_non_live",
        "last_known_landed_state_is_preserved_according_to_core_lifecycle_rules",
    },
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def schema_errors(addendum: dict[str, Any]) -> list[str]:
    schema = load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    return [
        f"schema: {'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(addendum), key=lambda item: list(item.path))
    ]


def semantic_errors(addendum: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    def expect(label: str, actual: Any, expected: Any) -> None:
        if actual != expected:
            errors.append(f"{label}: expected {expected!r}, got {actual!r}")

    purpose = addendum.get("purpose", {})
    expect("purpose.presentation_only", purpose.get("presentation_only"), True)
    expect("purpose.truth_invariant_unchanged", purpose.get("truth_invariant_unchanged"), True)
    expect("purpose.core_baseline_acceptance_unchanged", purpose.get("core_baseline_acceptance_unchanged"), True)

    authority = addendum.get("authority", {})
    expect(
        "authority.core_contract_remains_authoritative_for_truth_telemetry_and_session_semantics",
        authority.get("core_contract_remains_authoritative_for_truth_telemetry_and_session_semantics"),
        True,
    )
    expect(
        "authority.this_addendum_controls_demo_sequence_and_visual_evidence_capture_only",
        authority.get("this_addendum_controls_demo_sequence_and_visual_evidence_capture_only"),
        True,
    )
    expect("authority.real_runtime_evidence_is_downstream_only", authority.get("real_runtime_evidence_is_downstream_only"), True)

    evidence = addendum.get("playwright_evidence", {})
    expect("playwright.mode", evidence.get("mode"), "screenshot_only")
    expect(
        "playwright.comparison_layout",
        evidence.get("comparison_layout"),
        "left_simulated_source_state_right_real_product",
    )
    expect("playwright.pairing_key", evidence.get("pairing_key"), "scenario_checkpoint")
    expect("playwright.allowed_actions", set(evidence.get("allowed_actions", [])), EXPECTED_ALLOWED_ACTIONS)
    expect("playwright.forbidden_actions", set(evidence.get("forbidden_actions", [])), EXPECTED_FORBIDDEN_ACTIONS)
    expect("playwright.automated_image_diff_is_product_verdict", evidence.get("automated_image_diff_is_product_verdict"), False)
    expect("playwright.screenshots_are_evidence_not_ground_truth", evidence.get("screenshots_are_evidence_not_ground_truth"), True)
    expect("playwright.runtime_screenshots_committed_to_public_repo", evidence.get("runtime_screenshots_committed_to_public_repo"), False)

    left = evidence.get("left_panel", {})
    right = evidence.get("right_panel", {})
    expect("playwright.left_panel.label", left.get("label"), "Simulated Source State")
    expect(
        "playwright.left_panel.source",
        left.get("source"),
        "browser_render_of_accepted_esp32_telemetry_only",
    )
    expect("playwright.right_panel.label", right.get("label"), "Real Product")
    expect("playwright.right_panel.source", right.get("source"), "real_product_ui")

    main_demo = addendum.get("main_demo", {})
    expect("main_demo.sequence", main_demo.get("sequence"), EXPECTED_SEQUENCE)
    expect("main_demo.first_new_scenario_gate", main_demo.get("first_new_scenario_gate"), "single-target-silence-recovery")
    expect(
        "main_demo.later_new_stages_activate_only_after_first_gate_passes",
        main_demo.get("later_new_stages_activate_only_after_first_gate_passes"),
        True,
    )
    phoenix = main_demo.get("phoenix", {})
    expect("main_demo.phoenix.retained", phoenix.get("retained"), True)
    expect("main_demo.phoenix.supported_formation", phoenix.get("supported_formation"), "phoenix")
    expect("main_demo.phoenix.in_main_sequence", phoenix.get("in_main_sequence"), False)
    expect("main_demo.phoenix.role", phoenix.get("role"), "standalone_showcase")
    expect("main_demo.phoenix.may_be_run_separately", phoenix.get("may_be_run_separately"), True)
    expect("main_demo.phoenix.may_be_used_as_validation_proof", phoenix.get("may_be_used_as_validation_proof"), False)
    if "phoenix" in main_demo.get("sequence", []):
        errors.append("main_demo.sequence: Phoenix must remain outside the main demo sequence")

    stages = addendum.get("stage_contracts", [])
    if not isinstance(stages, list):
        errors.append("stage_contracts must be a list")
    else:
        stage_map = {
            str(stage.get("id")): stage
            for stage in stages
            if isinstance(stage, dict) and stage.get("id") is not None
        }
        expect("stage_contract IDs", list(stage_map), EXPECTED_SEQUENCE)
        for stage_id, expected_behaviors in EXPECTED_STAGE_BEHAVIORS.items():
            stage = stage_map.get(stage_id, {})
            expect(
                f"stage_contracts[{stage_id}].required_behavior",
                set(stage.get("required_behavior", [])),
                expected_behaviors,
            )

    identity = addendum.get("identity_test_semantics", {})
    expect("identity.runtime_drone_id_is_truth_entity_identity", identity.get("runtime_drone_id_is_truth_entity_identity"), True)
    expect("identity.claimed_remote_id_is_test_stimulus_identity", identity.get("claimed_remote_id_is_test_stimulus_identity"), True)
    expect("identity.duplicate_observation_case", identity.get("duplicate_observation_case"), "many_observations_one_truth_entity")
    expect("identity.shared_remote_id_case", identity.get("shared_remote_id_case"), "multiple_truth_entities_one_claimed_remote_id")
    expect("identity.remote_id_alone_must_not_define_truth_entity_count", identity.get("remote_id_alone_must_not_define_truth_entity_count"), True)
    expect("identity.real_product_identity_policy_is_not_assumed", identity.get("real_product_identity_policy_is_not_assumed"), True)

    expect("evidence_checkpoints", addendum.get("evidence_checkpoints"), EXPECTED_CHECKPOINTS)

    boundary = addendum.get("evidence_boundary", {})
    expect("evidence_boundary.left_side_is_not_physical_reality", boundary.get("left_side_is_not_physical_reality"), True)
    expect("evidence_boundary.left_side_name", boundary.get("left_side_name"), "Simulated Source State")
    expect("evidence_boundary.right_side_is_product_observation_not_ground_truth", boundary.get("right_side_is_product_observation_not_ground_truth"), True)
    expect("evidence_boundary.playwright_itself_makes_no_detection_quality_claim", boundary.get("playwright_itself_makes_no_detection_quality_claim"), True)
    expect("evidence_boundary.no_real_product_detection_quality_claim_from_public_contract", boundary.get("no_real_product_detection_quality_claim_from_public_contract"), True)

    core = load_json(CORE_CONTRACT_PATH)
    formations = core.get("formation_contract", {}).get("supported", [])
    if "phoenix" not in formations:
        errors.append("core contract no longer retains Phoenix as a supported formation")
    next_required = core.get("scenario_contract", {}).get("next_required", {})
    expect("core.next_required.case_id", next_required.get("case_id"), "single-target-silence-recovery")
    expect("core.next_required.status", next_required.get("status"), "DEFERRED")

    return errors


def validate_addendum(path: Path) -> list[str]:
    addendum = load_json(path)
    return schema_errors(addendum) + semantic_errors(addendum)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("addendum", nargs="?", default=str(DEFAULT_ADDENDUM))
    args = parser.parse_args()
    path = Path(args.addendum)
    errors = validate_addendum(path)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"validated {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
