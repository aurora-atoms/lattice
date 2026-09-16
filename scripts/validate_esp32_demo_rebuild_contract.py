#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate the public source-free ESP32 demo rebuild contract."""

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
DEFAULT_CONTRACT = (
    ROOT
    / "examples"
    / "esp32-demo-source-free-rebuild"
    / "rebuild-contract.v1.json"
)
SCHEMA_PATH = ROOT / "schemas/downstream/esp32-demo-rebuild-contract.v1.schema.json"

EXPECTED_ROLES: dict[str, tuple[set[str], set[str]]] = {
    "pc_controller": (
        {
            "scenario_selection",
            "operator_to_drone_relationships",
            "formation_geometry",
            "geo_path_progression",
            "target_positions",
            "config_lifecycle",
            "runtime_identity_rotation",
        },
        {
            "claim_command_as_execution",
            "substitute_targets_for_actual_telemetry",
        },
    ),
    "esp32": (
        {
            "configured_virtual_entity_runtime_state",
            "local_target_execution_and_interpolation",
            "per_entity_telemetry_sequence",
            "current_position_telemetry",
            "board_boot_identity",
        },
        {
            "plan_formations",
            "calculate_operator_drone_ownership",
            "discover_runtime_gis_paths",
            "perform_product_side_tracking_or_scoring",
        },
    ),
    "browser_ui": (
        {
            "render_accepted_telemetry",
            "fresh_stale_last_known_source_loss_presentation",
            "geo_observation_camera",
            "human_readable_identity_and_emission_labels",
        },
        {
            "invent_missing_motion",
            "render_reference_geometry_or_controller_targets_as_actual",
        },
    ),
    "external_product_side": (
        {
            "real_detector_collector_product_behavior",
            "product_side_comparison_if_later_authorized",
        },
        {"be_assumed_implemented_by_this_demo"},
    ),
}

EXPECTED_BASELINE_CASES = [
    "primary-circle-triangle",
    "geo-visible-patrol",
    "controller-restart-board-stays-up",
]

EXPECTED_ACCEPTANCE_IDS = [
    "R01_START_FRESH",
    "R02_CIRCLE",
    "R03_TRIANGLE",
    "R04_STOP_LAST_KNOWN",
    "R05_RESTART_ROTATES_SESSION",
    "R06_CONTROLLER_RESTART_BOARD_STAYS_UP",
    "R07_GEO_TRANSITION",
    "R08_GEO_REACQUIRE",
    "R09_GEO_PARTIAL_TELEMETRY",
    "R10_GEO_VISIBLE_MOTION",
    "R11_SINGLE_TARGET_SILENCE_RECOVERY",
]

EXPECTED_TELEMETRY_FIELDS = [
    "entity_type",
    "board_id",
    "operator_id",
    "emission_mode",
    "x",
    "y",
    "z",
    "seq",
    "frame_id",
    "config_id",
    "boot_id",
    "ts_ms",
]

EXPECTED_FORMATIONS = [
    "circle",
    "triangle",
    "smiley",
    "phoenix",
    "right-square-pyramid",
]

EXPECTED_IMPLEMENTATION_FREEDOM = {
    "programming_language",
    "web_framework",
    "server_framework",
    "class_and_function_names",
    "directory_layout",
    "internal_module_boundaries",
    "internal_algorithms_that_do_not_change_observable_behavior",
    "wire_encoding_as_long_as_both_rebuilt_endpoints_share_the_same_semantics",
}

EXPECTED_PRESERVED = {
    "truth_invariant",
    "role_boundaries",
    "entity_and_identity_semantics",
    "emission_vs_transport_separation",
    "protocol_semantics",
    "telemetry_freshness_and_lifecycle",
    "geo_camera_acceptance_semantics",
    "baseline_acceptance_matrix",
    "deferred_next_scenario_status",
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def schema_errors(contract: dict[str, Any]) -> list[str]:
    schema = load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    return [
        f"schema: {'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(contract), key=lambda item: list(item.path))
    ]


def semantic_errors(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    def expect(label: str, actual: Any, expected: Any) -> None:
        if actual != expected:
            errors.append(f"{label}: expected {expected!r}, got {actual!r}")

    purpose = contract.get("purpose", {})
    expect(
        "purpose.compatibility_target",
        purpose.get("compatibility_target"),
        "observable_behavior_and_acceptance",
    )
    expect("purpose.source_compatibility_required", purpose.get("source_compatibility_required"), False)
    expect("purpose.framework_compatibility_required", purpose.get("framework_compatibility_required"), False)
    expect("purpose.wire_encoding_compatibility_required", purpose.get("wire_encoding_compatibility_required"), False)
    expect("purpose.protocol_semantics_required", purpose.get("protocol_semantics_required"), True)

    boundary = contract.get("public_boundary", {})
    for key in (
        "source_code_included",
        "private_repository_coordinates_included",
        "private_runtime_evidence_included",
        "company_internal_material_included",
        "legal_clean_room_claim",
    ):
        expect(f"public_boundary.{key}", boundary.get(key), False)

    mission = contract.get("mission", {})
    expect("mission.product_side_external", mission.get("product_side_external"), True)
    expect("mission.actual_state_source", mission.get("actual_state_source"), "accepted_esp32_telemetry")
    expect("mission.controller_targets_are_intent_only", mission.get("controller_targets_are_intent_only"), True)
    expect("mission.command_sent_is_not_execution_evidence", mission.get("command_sent_is_not_execution_evidence"), True)
    invariant = str(mission.get("truth_invariant", ""))
    required_invariant_terms = [
        "PC Controller defines scenario and control intent",
        "ESP32 executes virtual Operator/Drone state",
        "ESP32 emits current-state telemetry",
        "Browser renders accepted ESP32 telemetry only",
    ]
    for term in required_invariant_terms:
        if term not in invariant:
            errors.append(f"mission.truth_invariant missing load-bearing term: {term}")

    roles = contract.get("system_roles", [])
    if not isinstance(roles, list):
        errors.append("system_roles must be a list")
    else:
        role_map = {
            str(role.get("id")): role
            for role in roles
            if isinstance(role, dict) and role.get("id") is not None
        }
        expect("system_roles IDs", set(role_map), set(EXPECTED_ROLES))
        for role_id, (owns, must_not) in EXPECTED_ROLES.items():
            role = role_map.get(role_id, {})
            expect(f"system_roles[{role_id}].owns", set(role.get("owns", [])), owns)
            expect(f"system_roles[{role_id}].must_not", set(role.get("must_not", [])), must_not)

    entity = contract.get("entity_model", {})
    expect("entity_model.entity_types", entity.get("entity_types"), ["operator", "drone"])
    topology = entity.get("topology", {})
    expect("topology.operator_controls_min_drones", topology.get("operator_controls_min_drones"), 1)
    expect("topology.operator_and_controlled_drones_same_board", topology.get("operator_and_controlled_drones_same_board"), True)
    expect("topology.max_drones_per_board", topology.get("max_drones_per_board"), 16)
    expect("topology.primary", topology.get("primary"), {"operator_count": 1, "drone_count_min": 6, "drone_count_max": 8})
    expect("topology.fallback", topology.get("fallback"), {"operator_count": 2, "drone_count": 16, "drones_per_operator": [8, 8]})

    identity = contract.get("identity_contract", {})
    expect("identity.max_visible_chars", identity.get("max_visible_chars"), 20)
    expect("identity.stable_within_run", identity.get("stable_within_run"), True)
    expect("identity.rotate_each_start", identity.get("rotate_each_start"), True)
    expect("identity.shared_association_component", identity.get("shared_association_component"), "animal_group_name_only")

    emission = contract.get("emission_contract", {})
    expect("emission.modes", emission.get("modes"), ["WF", "BT", "WB"])
    expect("emission.telemetry_transport", emission.get("telemetry_transport"), "UDP/WiFi")
    expect("emission.telemetry_transport_is_not_emission_mode", emission.get("telemetry_transport_is_not_emission_mode"), True)
    expect("emission.product_facing_rf_emitter_required", emission.get("product_facing_rf_emitter_required"), False)

    protocol = contract.get("protocol_contract", {})
    expect("protocol.semantic_version", protocol.get("semantic_version"), 5)
    expect("protocol.wire_encoding_free", protocol.get("wire_encoding_free"), True)
    expect("protocol.command_port", protocol.get("command_port"), 4210)
    expect("protocol.telemetry_port", protocol.get("telemetry_port"), 4211)
    expect(
        "protocol.commands",
        protocol.get("commands"),
        {
            "CONFIGURE": ["config_id", "board_id", "operators", "drones"],
            "UPDATE": ["config_id", "frame_id", "board_id", "entity_targets"],
            "STOP": ["config_id", "board_id"],
        },
    )
    expect("protocol.telemetry_required_fields", protocol.get("telemetry_required_fields"), EXPECTED_TELEMETRY_FIELDS)
    expect("protocol.drone_additional_field", protocol.get("drone_additional_field"), "drone_id")
    expect("protocol.duplicate_configure", protocol.get("duplicate_configure"), "idempotent")
    expect("protocol.partial_updates_allowed", protocol.get("partial_updates_allowed"), True)
    expect("protocol.update_ordering", protocol.get("update_ordering"), "per_entity")
    expect("protocol.config_id_allocation", protocol.get("config_id_allocation"), "persisted_monotonic_generation_with_wall_clock_floor")
    expect("protocol.controller_restart_without_board_reboot", protocol.get("controller_restart_without_board_reboot"), True)

    lifecycle = contract.get("telemetry_lifecycle", {})
    expect("telemetry.output_interval_ms", lifecycle.get("output_interval_ms"), 100)
    expect("telemetry.stale_after_ms", lifecycle.get("stale_after_ms"), 1500)
    expect("telemetry.freshness_scope", lifecycle.get("freshness_scope"), "per_entity")
    expect("telemetry.source_disconnect_is_separate_state", lifecycle.get("source_disconnect_is_separate_state"), True)
    expect("telemetry.stopped_samples_are_last_known", lifecycle.get("stopped_samples_are_last_known"), True)
    expect("telemetry.old_session_packets_rejected", lifecycle.get("old_session_packets_rejected"), True)
    expect("telemetry.boot_change_requires_reinitialize", lifecycle.get("boot_change_requires_reinitialize"), True)
    expect("telemetry.reject_non_finite_coordinates", lifecycle.get("reject_non_finite_coordinates"), True)
    expect("telemetry.reject_emission_mode_mismatch", lifecycle.get("reject_emission_mode_mismatch"), True)

    formation = contract.get("formation_contract", {})
    expect("formation.supported", formation.get("supported"), EXPECTED_FORMATIONS)
    expect("formation.all_are_3d", formation.get("all_are_3d"), True)
    expect("formation.state_is_per_operator", formation.get("state_is_per_operator"), True)

    geo = contract.get("geo_contract", {})
    expect("geo.scene_id", geo.get("scene_id"), "doubtful-sound-patea")
    expect("geo.simulation_only", geo.get("simulation_only"), True)
    expect("geo.runtime_gis_lookup", geo.get("runtime_gis_lookup"), False)
    expect("geo.precomputed_anchor_count", geo.get("precomputed_anchor_count"), 11)
    expect("geo.default_spacing_m", geo.get("default_spacing_m"), 12.0)
    expect("geo.speed_mps", geo.get("speed_mps"), 20.0)
    expect("geo.default_target_cadence_ms", geo.get("default_target_cadence_ms"), 250)
    expect("geo.observation_zoom", geo.get("observation_zoom"), 60)
    expect("geo.reference_path_is_not_actual", geo.get("reference_path_is_not_actual"), True)
    acquisition = geo.get("camera_acquisition", {})
    for key in (
        "pre_geo_cached_telemetry_must_not_lock",
        "requires_geo_frame_or_later",
        "requires_selected_operator_and_all_controlled_drones",
        "requires_candidate_projection_visible",
        "refresh_or_reselection_reacquires_near_current_path_segment",
        "reference_path_only_gates_lock_readiness",
    ):
        expect(f"geo.camera_acquisition.{key}", acquisition.get(key), True)
    observation = geo.get("observation", {})
    expect("geo.observation.camera_fixed_after_lock", observation.get("camera_fixed_after_lock"), True)
    expect("geo.observation.window_seconds", observation.get("window_seconds"), 1)
    expect("geo.observation.minimum_marker_diameters_moved", observation.get("minimum_marker_diameters_moved"), 1.5)

    display = contract.get("display_contract", {})
    expect("display.telemetry_only", display.get("telemetry_only"), True)
    expect("display.controller_targets_must_not_be_rendered_as_actual", display.get("controller_targets_must_not_be_rendered_as_actual"), True)
    expect("display.stale_distinct_from_fresh", display.get("stale_distinct_from_fresh"), True)
    expect("display.source_disconnect_distinct", display.get("source_disconnect_distinct"), True)

    scenario = contract.get("scenario_contract", {})
    expect("scenario.baseline_required", scenario.get("baseline_required"), EXPECTED_BASELINE_CASES)
    next_required = scenario.get("next_required", {})
    expect("scenario.next_required.case_id", next_required.get("case_id"), "single-target-silence-recovery")
    expect("scenario.next_required.priority", next_required.get("priority"), "MUST")
    expect("scenario.next_required.status", next_required.get("status"), "DEFERRED")
    expect("scenario.next_required.required_for_baseline", next_required.get("required_for_baseline"), False)
    expect("scenario.scenario_expansion", scenario.get("scenario_expansion"), "blocked_until_next_required_is_implemented_and_validated")

    acceptance = contract.get("acceptance_matrix", [])
    if not isinstance(acceptance, list):
        errors.append("acceptance_matrix must be a list")
    else:
        ids = [str(case.get("id")) for case in acceptance if isinstance(case, dict)]
        expect("acceptance_matrix IDs", ids, EXPECTED_ACCEPTANCE_IDS)
        for case in acceptance:
            if not isinstance(case, dict):
                continue
            case_id = case.get("id")
            if case_id == "R11_SINGLE_TARGET_SILENCE_RECOVERY":
                expect("R11.required_for_baseline", case.get("required_for_baseline"), False)
                expect("R11.status", case.get("status"), "DEFERRED")
            else:
                expect(f"{case_id}.required_for_baseline", case.get("required_for_baseline"), True)
                if "status" in case:
                    errors.append(f"{case_id}: baseline case must not carry deferred status")

    freedom = contract.get("implementation_freedom", {})
    expect("implementation_freedom.may_change", set(freedom.get("may_change", [])), EXPECTED_IMPLEMENTATION_FREEDOM)
    expect("implementation_freedom.must_preserve", set(freedom.get("must_preserve", [])), EXPECTED_PRESERVED)

    readiness = contract.get("readiness", {})
    expect("readiness.software_rebuild_may_claim", readiness.get("software_rebuild_may_claim"), "SOFTWARE_PARITY_CANDIDATE")
    expect("readiness.software_green_does_not_claim", readiness.get("software_green_does_not_claim"), "PHYSICAL_READY")
    expect("readiness.hardware_and_intended_screen_evidence_required_separately", readiness.get("hardware_and_intended_screen_evidence_required_separately"), True)

    return errors


def validate_contract(path: Path) -> list[str]:
    contract = load_json(path)
    return schema_errors(contract) + semantic_errors(contract)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", nargs="?", default=str(DEFAULT_CONTRACT))
    args = parser.parse_args()
    path = Path(args.contract).resolve()
    try:
        errors = validate_contract(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"validated source-free ESP32 demo rebuild contract: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
