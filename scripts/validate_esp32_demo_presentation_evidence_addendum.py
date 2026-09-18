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
    raise SystemExit("jsonschema is required; install requirements-validation.txt") from exc

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ADDENDUM = ROOT / "examples" / "esp32-demo-source-free-rebuild" / "presentation-evidence-addendum.v1.json"
CORE_CONTRACT_PATH = ROOT / "examples" / "esp32-demo-source-free-rebuild" / "rebuild-contract.v1.json"
SCHEMA_PATH = ROOT / "schemas" / "downstream" / "esp32-demo-presentation-evidence-addendum.v1.schema.json"

EXPECTED_SEQUENCE = [
    "multi-point-takeoff",
    "asmr-stroke-drawing",
    "in-stroke-silence",
    "same-drone-recovery",
    "landing-vs-airborne-disconnect",
    "duplicate-signal-and-identity-conflict",
    "geo-coast-patrol",
    "phoenix-formation",
    "distributed-landing",
]

EXPECTED_CHECKPOINTS = [
    "takeoff-established",
    "asmr-stroke-mid-drawing",
    "active-stroke-interrupted-one-drone-silent",
    "same-drone-recovered-stroke-resumed",
    "landed-vs-airborne-disconnected",
    "duplicate-signal-window",
    "shared-remote-id-conflict",
    "coast-patrol-in-motion",
    "phoenix-formed",
    "distributed-landing-complete",
]

EXPECTED_PROOF_CHECKPOINTS = [
    "active-stroke-interrupted-one-drone-silent",
    "landed-vs-airborne-disconnected",
    "duplicate-signal-window",
    "shared-remote-id-conflict",
]

EXPECTED_ALLOWED_ACTIONS = {
    "capture_left_panel_screenshot",
    "capture_right_panel_screenshot",
    "record_checkpoint_id_and_capture_times",
    "compose_captured_images_side_by_side_without_semantic_mutation",
}

EXPECTED_FORBIDDEN_ACTIONS = {
    "read_product_dom_as_semantic_evidence",
    "inspect_product_api_payloads",
    "inspect_product_websocket_or_network_payloads",
    "derive_automated_product_pass_fail",
    "mutate_product_state_to_make_a_checkpoint_pass",
    "mutate_simulator_truth_to_match_product_output",
    "alter_product_native_alerts_or_highlights_in_composition",
}

EXPECTED_DOWNSTREAM_RECORD_FIELDS = {
    "run_id",
    "mission_checkpoint",
    "stimulus_event_id",
    "left_screenshot_ref",
    "right_screenshot_ref",
    "capture_pairing_metadata",
    "same_stimulus_delivery_attestation",
    "visual_observation",
    "log_evidence_ref",
    "log_confirmation",
}

EXPECTED_FORBIDDEN_CLAIMS = {
    "visual_comparison_is_generally_superior_to_log_analysis",
    "visual_comparison_is_faster_than_log_analysis",
    "screenshots_alone_prove_product_detection_quality",
    "contract_validation_proves_runtime_product_behavior",
}

EXPECTED_PROOF_SEGMENT = [
    "asmr-stroke-drawing",
    "in-stroke-silence",
    "same-drone-recovery",
    "landing-vs-airborne-disconnect",
    "duplicate-signal-and-identity-conflict",
]
EXPECTED_SHOWCASE_OUTRO = ["geo-coast-patrol", "phoenix-formation", "distributed-landing"]

EXPECTED_STAGE_BEHAVIORS: dict[str, set[str]] = {
    "multi-point-takeoff": {
        "mission_roster_is_created_once_here",
        "drones_may_start_from_different_positions",
        "accepted_telemetry_shows_takeoff_progression_before_cruise_motion",
        "no_controller_reference_position_is_rendered_as_actual",
    },
    "asmr-stroke-drawing": {
        "starts_from_multi_point_takeoff_final_accepted_positions",
        "controller_precomputes_ordered_strokes_and_3d_waypoints",
        "drones_follow_time_ordered_continuous_3d_waypoints",
        "shape_is_revealed_by_strokes_not_instant_final_formation",
        "horizontal_xy_projection_remains_recognizable_without_using_z",
        "visual_trail_is_derived_only_from_accepted_telemetry_history",
        "visual_trail_does_not_invent_missing_motion",
        "accepted_telemetry_is_the_only_displayed_actual_state",
    },
    "in-stroke-silence": {
        "starts_from_asmr_stroke_drawing_current_positions",
        "fault_occurs_during_an_active_stroke",
        "only_one_existing_drone_is_silenced",
        "peers_continue_the_same_drawing_task_and_remain_fresh",
        "silent_drone_last_known_position_is_preserved",
        "visual_trail_does_not_bridge_unobserved_motion_as_observed",
        "mission_config_and_runtime_roster_are_not_reset",
    },
    "same-drone-recovery": {
        "recovery_reuses_same_runtime_drone_id",
        "recovery_reuses_same_config_and_board_boot_identity",
        "recovered_drone_resumes_from_continuous_mission_state",
        "remaining_stroke_continues_without_respawning_the_swarm",
        "missing_interval_is_not_rewritten_as_observed_telemetry",
    },
    "landing-vs-airborne-disconnect": {
        "one_existing_drone_descends_and_lands_before_telemetry_ceases",
        "one_different_existing_drone_ceases_while_last_known_state_is_airborne",
        "both_drones_remain_members_of_the_same_mission_roster",
        "landed_and_disconnected_drones_leave_the_active_flying_subset",
        "simulated_source_state_does_not_relabel_disconnect_as_landing",
    },
    "duplicate-signal-and-identity-conflict": {
        "duplicate_observations_reuse_one_existing_runtime_drone_without_creating_a_truth_entity",
        "two_or_three_existing_active_drones_may_claim_the_same_remote_id",
        "distinct_runtime_drone_ids_and_trajectories_are_preserved",
        "identity_stress_does_not_change_the_mission_truth_roster",
        "product_ui_response_is_recorded_only_by_screenshot",
    },
    "geo-coast-patrol": {
        "starts_from_previous_stage_last_accepted_positions",
        "existing_doubtful_sound_precomputed_path_is_reused",
        "remaining_active_members_join_the_patrol_continuously",
        "runtime_gis_lookup_is_not_added",
        "accepted_telemetry_remains_the_actual_state_source",
    },
    "phoenix-formation": {
        "starts_from_geo_coast_patrol_current_positions",
        "uses_remaining_active_members_only",
        "formation_transition_is_continuous_in_3d",
        "phoenix_horizontal_xy_projection_preserves_recognizable_silhouette",
        "phoenix_is_in_the_main_mission_but_is_not_product_validation_proof",
    },
    "distributed-landing": {
        "starts_from_phoenix_current_positions",
        "no_new_drone_is_spawned_for_landing",
        "remaining_active_drones_may_land_at_different_points",
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
    expect("authority.core_contract_remains_authoritative_for_truth_telemetry_and_session_semantics", authority.get("core_contract_remains_authoritative_for_truth_telemetry_and_session_semantics"), True)
    expect("authority.this_addendum_controls_demo_sequence_and_visual_evidence_capture_only", authority.get("this_addendum_controls_demo_sequence_and_visual_evidence_capture_only"), True)
    expect("authority.real_runtime_evidence_is_downstream_only", authority.get("real_runtime_evidence_is_downstream_only"), True)

    evidence = addendum.get("playwright_evidence", {})
    expect("playwright.mode", evidence.get("mode"), "screenshot_only")
    expect("playwright.comparison_layout", evidence.get("comparison_layout"), "left_simulated_source_state_right_real_product")
    expect("playwright.pairing_key", evidence.get("pairing_key"), "mission_checkpoint")
    for key in (
        "source_and_product_are_separate_browser_pages",
        "separate_panel_captures_required",
        "side_by_side_composition_required",
        "composition_is_presentation_only",
        "capture_time_skew_must_be_recorded",
        "checkpoint_id_and_capture_times_must_be_recorded",
    ):
        expect(f"playwright.{key}", evidence.get(key), True)
    expect("playwright.same_capture_frame_required", evidence.get("same_capture_frame_required"), False)
    expect("playwright.allowed_actions", set(evidence.get("allowed_actions", [])), EXPECTED_ALLOWED_ACTIONS)
    expect("playwright.forbidden_actions", set(evidence.get("forbidden_actions", [])), EXPECTED_FORBIDDEN_ACTIONS)
    expect("playwright.automated_image_diff_is_product_verdict", evidence.get("automated_image_diff_is_product_verdict"), False)
    expect("playwright.screenshots_are_evidence_not_ground_truth", evidence.get("screenshots_are_evidence_not_ground_truth"), True)
    expect("playwright.runtime_screenshots_committed_to_public_repo", evidence.get("runtime_screenshots_committed_to_public_repo"), False)

    left = evidence.get("left_panel", {})
    right = evidence.get("right_panel", {})
    expect("playwright.left_panel.label", left.get("label"), "Simulated Source State")
    expect("playwright.left_panel.source", left.get("source"), "browser_render_of_accepted_esp32_telemetry_only")
    expect("playwright.right_panel.label", right.get("label"), "Real Product")
    expect("playwright.right_panel.source", right.get("source"), "real_product_ui")

    comparison = addendum.get("comparison_evidence", {})
    expect("comparison_evidence.scope", comparison.get("scope"), "single_demo_run_not_general_human_factors_research")
    expect("comparison_evidence.proof_checkpoints", comparison.get("proof_checkpoints"), EXPECTED_PROOF_CHECKPOINTS)
    expect("comparison_evidence.observation_order", comparison.get("observation_order"), "visual_observation_then_independent_log_confirmation")
    expect("comparison_evidence.visual_observation_must_be_frozen_before_log_confirmation", comparison.get("visual_observation_must_be_frozen_before_log_confirmation"), True)
    expect("comparison_evidence.log_confirmation_is_not_a_speed_competitor", comparison.get("log_confirmation_is_not_a_speed_competitor"), True)
    expect("comparison_evidence.visual_vs_log_speed_claim_allowed", comparison.get("visual_vs_log_speed_claim_allowed"), False)
    expect("comparison_evidence.test_added_fault_annotation_before_visual_observation_is_frozen", comparison.get("test_added_fault_annotation_before_visual_observation_is_frozen"), False)
    expect("comparison_evidence.product_native_alerts_and_highlights_must_be_preserved", comparison.get("product_native_alerts_and_highlights_must_be_preserved"), True)
    expect("comparison_evidence.post_observation_test_annotation_allowed", comparison.get("post_observation_test_annotation_allowed"), True)
    expect("comparison_evidence.required_downstream_record_fields", set(comparison.get("required_downstream_record_fields", [])), EXPECTED_DOWNSTREAM_RECORD_FIELDS)
    expect("comparison_evidence.downstream_record_storage", comparison.get("downstream_record_storage"), "private_downstream_only")
    expect("comparison_evidence.same_stimulus_delivery_attestation_required", comparison.get("same_stimulus_delivery_attestation_required"), True)
    expect("comparison_evidence.permitted_claim", comparison.get("permitted_claim"), "visual_divergence_identified_and_independently_confirmed_by_logs_in_same_run")
    expect("comparison_evidence.forbidden_claims", set(comparison.get("forbidden_claims", [])), EXPECTED_FORBIDDEN_CLAIMS)

    main_demo = addendum.get("main_demo", {})
    expect("main_demo.theme", main_demo.get("theme"), "single_swarm_continuous_mission")
    expect("main_demo.sequence", main_demo.get("sequence"), EXPECTED_SEQUENCE)
    expect("main_demo.first_new_scenario_gate", main_demo.get("first_new_scenario_gate"), "single-target-silence-recovery")
    expect("main_demo.first_new_scenario_gate_stages", main_demo.get("first_new_scenario_gate_stages"), ["in-stroke-silence", "same-drone-recovery"])
    expect("main_demo.later_new_stages_activate_only_after_first_gate_passes", main_demo.get("later_new_stages_activate_only_after_first_gate_passes"), True)

    drawing = main_demo.get("drawing_mode", {})
    expect("drawing.name", drawing.get("name"), "ASMR-like Stroke Drawing")
    expect("drawing.contract_id", drawing.get("contract_id"), "asmr_stroke_drawing")
    expect("drawing.stroke_source", drawing.get("stroke_source"), "accepted_esp32_telemetry_history_only")
    for key in (
        "precomputed_stroke_plan_owned_by_controller",
        "continuous_3d_waypoints_required",
        "instant_final_formation_snap_forbidden",
        "telemetry_derived_visual_trail_allowed",
        "visual_trail_must_not_invent_missing_motion",
        "fault_may_interrupt_an_active_stroke",
        "recovery_continues_same_mission_stroke",
    ):
        expect(f"drawing.{key}", drawing.get(key), True)

    projection = main_demo.get("horizontal_projection", {})
    expect("horizontal_projection.projection_plane", projection.get("projection_plane"), "xy")
    expect("horizontal_projection.purpose", projection.get("purpose"), "planar_product_comparison")
    for key in (
        "applies_to_all_3d_formations",
        "top_down_projection_must_be_recognizable",
        "xy_silhouette_is_primary_shape_signature",
        "z_axis_may_add_depth_but_must_not_define_shape_identity_alone",
        "z_only_separation_must_not_be_required_for_recognition",
        "projected_self_overlap_must_not_destroy_key_shape_features",
        "projection_must_remain_comparable_when_altitude_is_ignored",
    ):
        expect(f"horizontal_projection.{key}", projection.get(key), True)

    continuity = main_demo.get("mission_continuity", {})
    for key in (
        "single_mission",
        "single_run",
        "mission_roster_created_once_at_start",
        "inactive_members_remain_part_of_mission_roster",
        "later_stages_use_remaining_active_members",
        "phoenix_uses_remaining_active_members",
        "distributed_landing_closes_remaining_active_members",
    ):
        expect(f"mission_continuity.{key}", continuity.get(key), True)
    expect("mission_continuity.stage_transition_start_state", continuity.get("stage_transition_start_state"), "previous_stage_last_accepted_telemetry")
    for key in (
        "new_start_between_stages",
        "config_reset_between_stages",
        "runtime_identity_rotation_between_stages",
        "respawn_or_reseed_between_stages",
        "truth_entity_roster_changes_for_observation_tests",
    ):
        expect(f"mission_continuity.{key}", continuity.get(key), False)

    phoenix = main_demo.get("phoenix", {})
    expect("main_demo.phoenix.retained", phoenix.get("retained"), True)
    expect("main_demo.phoenix.supported_formation", phoenix.get("supported_formation"), "phoenix")
    expect("main_demo.phoenix.in_main_sequence", phoenix.get("in_main_sequence"), True)
    expect("main_demo.phoenix.role", phoenix.get("role"), "mission_climax_showcase")
    expect("main_demo.phoenix.follows_stage", phoenix.get("follows_stage"), "geo-coast-patrol")
    expect("main_demo.phoenix.precedes_stage", phoenix.get("precedes_stage"), "distributed-landing")
    expect("main_demo.phoenix.uses_remaining_active_members", phoenix.get("uses_remaining_active_members"), True)
    expect("main_demo.phoenix.may_be_run_separately", phoenix.get("may_be_run_separately"), True)
    expect("main_demo.phoenix.may_be_used_as_validation_proof", phoenix.get("may_be_used_as_validation_proof"), False)

    segments = main_demo.get("presentation_segments", {})
    expect("presentation_segments.proof", segments.get("proof"), EXPECTED_PROOF_SEGMENT)
    expect("presentation_segments.showcase_outro", segments.get("showcase_outro"), EXPECTED_SHOWCASE_OUTRO)
    expect("presentation_segments.showcase_outro_must_not_be_reported_as_product_validation", segments.get("showcase_outro_must_not_be_reported_as_product_validation"), True)

    stages = addendum.get("stage_contracts", [])
    if not isinstance(stages, list):
        errors.append("stage_contracts must be a list")
    else:
        stage_map = {str(stage.get("id")): stage for stage in stages if isinstance(stage, dict) and stage.get("id") is not None}
        expect("stage_contract IDs", list(stage_map), EXPECTED_SEQUENCE)
        for stage_id, expected_behaviors in EXPECTED_STAGE_BEHAVIORS.items():
            stage = stage_map.get(stage_id, {})
            expect(f"stage_contracts[{stage_id}].required_behavior", set(stage.get("required_behavior", [])), expected_behaviors)

    identity = addendum.get("identity_test_semantics", {})
    expect("identity.runtime_drone_id_is_truth_entity_identity", identity.get("runtime_drone_id_is_truth_entity_identity"), True)
    expect("identity.claimed_remote_id_is_test_stimulus_identity", identity.get("claimed_remote_id_is_test_stimulus_identity"), True)
    expect("identity.duplicate_observation_case", identity.get("duplicate_observation_case"), "many_observations_one_existing_truth_entity")
    expect("identity.shared_remote_id_case", identity.get("shared_remote_id_case"), "multiple_existing_truth_entities_one_claimed_remote_id")
    expect("identity.remote_id_alone_must_not_define_truth_entity_count", identity.get("remote_id_alone_must_not_define_truth_entity_count"), True)
    expect("identity.identity_stress_must_not_change_mission_roster", identity.get("identity_stress_must_not_change_mission_roster"), True)
    expect("identity.real_product_identity_policy_is_not_assumed", identity.get("real_product_identity_policy_is_not_assumed"), True)

    expect("evidence_checkpoints", addendum.get("evidence_checkpoints"), EXPECTED_CHECKPOINTS)

    boundary = addendum.get("evidence_boundary", {})
    expect("evidence_boundary.left_side_is_not_physical_reality", boundary.get("left_side_is_not_physical_reality"), True)
    expect("evidence_boundary.left_side_name", boundary.get("left_side_name"), "Simulated Source State")
    expect("evidence_boundary.right_side_is_product_observation_not_ground_truth", boundary.get("right_side_is_product_observation_not_ground_truth"), True)
    expect("evidence_boundary.playwright_itself_makes_no_detection_quality_claim", boundary.get("playwright_itself_makes_no_detection_quality_claim"), True)
    expect("evidence_boundary.no_real_product_detection_quality_claim_from_public_contract", boundary.get("no_real_product_detection_quality_claim_from_public_contract"), True)
    expect("evidence_boundary.contract_valid_does_not_mean_demo_runtime_captured", boundary.get("contract_valid_does_not_mean_demo_runtime_captured"), True)
    expect("evidence_boundary.demo_runtime_captured_does_not_mean_human_reviewed", boundary.get("demo_runtime_captured_does_not_mean_human_reviewed"), True)
    expect("evidence_boundary.human_reviewed_does_not_automatically_mean_product_issue_confirmed", boundary.get("human_reviewed_does_not_automatically_mean_product_issue_confirmed"), True)

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
