#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

EXPECTED_TASK_FAMILIES = {
    "feature_requirement",
    "risk",
    "bug",
    "decision",
    "management",
}

EXPECTED_TARGET_ROLES = {
    "gem": "interactive_intake_and_scouting",
    "workspace_studio": "manual_or_shadow_workflow",
    "notebook": "source_grounded_synthesis",
}

EXPECTED_HANDOFF_SECTIONS = {
    "target",
    "source_scope",
    "claims",
    "unknowns",
    "conflicts",
    "strongest_counterevidence",
    "proposals",
    "authority",
    "privacy",
}

FORBIDDEN_PUBLIC_LOCATOR_PATTERNS = (
    re.compile(r"https?://(?:drive|docs|chat|mail|gmail)\\.google\\.com/", re.IGNORECASE),
    re.compile(r"(?:^|[\\s\"'])/[A-Za-z0-9_.-]+/(?:Users|home|workspace|repo)/"),
    re.compile(r"[A-Za-z]:\\\\(?:Users|workspace|repo)\\\\", re.IGNORECASE),
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"),
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _all_strings(value: Any) -> list[str]:
    result: list[str] = []
    if isinstance(value, str):
        result.append(value)
    elif isinstance(value, dict):
        for item in value.values():
            result.extend(_all_strings(item))
    elif isinstance(value, list):
        for item in value:
            result.extend(_all_strings(item))
    return result


def validate_adapter(manifest_path: Path, root: Path, schema_path: Path | None = None) -> list[str]:
    errors: list[str] = []
    manifest = load_json(manifest_path)
    schema_file = schema_path or root / "schemas" / "runtime-adapters" / "google-workspace-adapter-manifest.v1.schema.json"
    schema = load_json(schema_file)

    Draft202012Validator.check_schema(schema)
    structural = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(manifest),
        key=lambda error: list(error.path),
    )
    for error in structural:
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"schema:{location}: {error.message}")
    if structural:
        return errors

    task_families = set(manifest["task_families"])
    if task_families != EXPECTED_TASK_FAMILIES:
        errors.append(
            "semantic:task_families must contain exactly feature_requirement, risk, bug, decision, and management"
        )

    targets = manifest["targets"]
    by_target = {item["target"]: item for item in targets}
    if set(by_target) != set(EXPECTED_TARGET_ROLES) or len(by_target) != len(targets):
        errors.append("semantic:targets must contain exactly one gem, workspace_studio, and notebook entry")
    else:
        for target, expected_role in EXPECTED_TARGET_ROLES.items():
            item = by_target[target]
            if item["role"] != expected_role:
                errors.append(f"semantic:{target} role must be {expected_role}")
            if item["authority_ceiling"] != "candidate":
                errors.append(f"semantic:{target} authority ceiling must remain candidate")
            if item["availability"] != "unknown":
                errors.append(
                    f"semantic:{target} public canonical availability must remain unknown until downstream account observation"
                )

    if set(manifest["handoff"]["required_sections"]) != EXPECTED_HANDOFF_SECTIONS:
        errors.append("semantic:handoff required_sections must preserve target, sources, claims, unknowns, conflicts, counterevidence, proposals, authority, and privacy")

    authority = manifest["authority"]
    if authority != {
        "authority_ceiling": "candidate",
        "human_confirmation_required": True,
        "public_writeback_allowed": False,
        "authoritative_case_write_allowed": False,
        "delivery_verdict_allowed": False,
        "automatic_action_default": False,
    }:
        errors.append("semantic:authority firewall drifted from candidate-only, human-confirmed, non-writing behavior")

    privacy = manifest["privacy"]
    if privacy["private_content_in_public_repo"] != "forbidden":
        errors.append("semantic:private content must be forbidden in public Lattice")
    if privacy["real_company_data_in_public_fixtures"] is not False:
        errors.append("semantic:public fixtures cannot contain real company data")
    if privacy["private_results_location"] != "downstream_only":
        errors.append("semantic:real results must remain downstream-only")

    source_binding = manifest["source_binding"]
    if source_binding["private_workspace_sources"] != "downstream_only":
        errors.append("semantic:private Workspace sources must bind downstream only")
    if source_binding["account_availability_verification"] != "downstream_required":
        errors.append("semantic:runtime availability must be verified downstream")
    if source_binding["coverage_claim"] != "bounded_not_complete":
        errors.append("semantic:adapter must not claim complete enterprise source coverage")

    disclosure = manifest["progressive_disclosure"]
    if disclosure["load_all_skills"] is not False or disclosure["minimum_capability_selection"] is not True:
        errors.append("semantic:adapter must preserve smallest-sufficient progressive capability selection")
    if disclosure["runtime_specific_projection"] != "generated_in_later_adapter_stage":
        errors.append("semantic:GW-1 cannot smuggle Gem, Studio, or Notebook rendered configuration into the canonical contract")

    assumptions = manifest["product_assumptions"]
    for field in (
        "uniform_workspace_surface_assumed",
        "complete_enterprise_search_assumed",
        "notebook_dynamic_global_search_assumed",
        "experimental_features_required",
    ):
        if assumptions[field] is not False:
            errors.append(f"semantic:{field} must remain false in the public adapter contract")
    if assumptions["availability_state_source"] != "downstream_observation":
        errors.append("semantic:availability state must come from downstream observation")

    refs = manifest["canonical_refs"]
    for label, relative_path in refs.items():
        if not (root / relative_path).is_file():
            errors.append(f"semantic:canonical ref {label} does not exist: {relative_path}")

    for value in _all_strings(manifest):
        for pattern in FORBIDDEN_PUBLIC_LOCATOR_PATTERNS:
            if pattern.search(value):
                errors.append("semantic:public adapter source contains a private/account-specific locator or email-like value")
                break

    joined_non_goals = "\n".join(manifest["non_goals"]).lower()
    required_non_goal_signals = (
        "mega skill",
        "new agent",
        "active module",
        "private",
        "adoption",
        "automatic",
    )
    for signal in required_non_goal_signals:
        if signal not in joined_non_goals:
            errors.append(f"semantic:non_goals must explicitly preserve the {signal!r} boundary")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the canonical Google Workspace Senior Attention adapter contract.")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--schema", type=Path, default=None)
    args = parser.parse_args()

    errors = validate_adapter(args.manifest.resolve(), args.root.resolve(), args.schema.resolve() if args.schema else None)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("google-workspace-adapter: valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
