#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate Lattice capability profile runtime contracts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from capability_utils import agent_ids, knowledge_ids, load_json, mcp_ids, skill_ids


CONTRACT = "lat.capability-profile.runtime.v1"
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")

PROFILE_OWNERSHIP = {
    "model_routing",
    "skills",
    "tools",
    "knowledge",
    "permissions",
    "token_budget",
    "cache_policy",
    "telemetry",
}
AGENT_RESPONSIBILITIES = {"assess_state", "select_next_action", "stop", "escalate"}
AGENT_FORBIDDEN_OWNERSHIP = {
    "model_routing",
    "tool_permissions",
    "cache_policy",
    "delivery_verdict",
}
REQUIRED_LANES = {"economy", "coding", "flagship", "human"}
REQUIRED_ESCALATION_TRIGGERS = {
    "ambiguity",
    "high_blast_radius",
    "irreversibility",
    "low_observability",
    "conflicting_evidence",
    "security_or_compliance",
}
REQUIRED_CACHE_KEY_FIELDS = {
    "profile_id",
    "profile_version",
    "model_lane",
    "toolset_hash",
    "schema_version",
}
REQUIRED_CACHE_INVALIDATORS = {
    "profile_version_change",
    "toolset_change",
    "schema_change",
    "policy_change",
}
REQUIRED_HANDOFF_FIELDS = {
    "decision_required",
    "verified_facts",
    "conflicts",
    "unknowns",
    "evidence_refs",
    "reason_for_escalation",
}
REQUIRED_HUMAN_INTENTS = {
    "controllability",
    "competence",
    "cognitive_clarity",
    "safe_dissent",
    "collective_efficacy",
}
REQUIRED_HUMAN_AVOIDS = {
    "choice_overload",
    "approval_fatigue",
    "surveillance",
    "replacement_framing",
    "zero_error_promises",
}


def _as_set(value: Any) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {str(item) for item in value}


def _required(record: dict[str, Any], field: str, errors: list[str]) -> Any:
    if field not in record:
        errors.append(f"missing required field: {field}")
        return None
    return record[field]


def validate_profile(path: Path, root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    record = load_json(path)

    for field in [
        "contract",
        "profile_id",
        "profile_version",
        "status",
        "task_type",
        "agent_bindings",
        "profile_ownership",
        "skills",
        "mcp",
        "knowledge",
        "permissions",
        "model_routing",
        "verification",
        "handoff",
        "cache",
        "token_budget",
        "human_factors",
        "telemetry",
        "validation",
    ]:
        _required(record, field, errors)

    if record.get("contract") != CONTRACT:
        errors.append(f"contract must be {CONTRACT}")
    if not SEMVER_RE.match(str(record.get("profile_version", ""))):
        errors.append("profile_version must be semantic versioning")

    ownership = _as_set(record.get("profile_ownership"))
    missing_ownership = PROFILE_OWNERSHIP - ownership
    if missing_ownership:
        errors.append(
            "profile_ownership is missing: " + ", ".join(sorted(missing_ownership))
        )

    known_agents = agent_ids(root)
    bindings = record.get("agent_bindings", [])
    if not isinstance(bindings, list) or not bindings:
        errors.append("agent_bindings must be a non-empty list")
    for index, binding in enumerate(bindings if isinstance(bindings, list) else []):
        label = f"agent_bindings[{index}]"
        if not isinstance(binding, dict):
            errors.append(f"{label} must be an object")
            continue
        agent_id = str(binding.get("agent_id", ""))
        if agent_id not in known_agents:
            errors.append(f"{label} references unknown agent: {agent_id}")
        responsibilities = _as_set(binding.get("responsibilities"))
        missing_responsibilities = AGENT_RESPONSIBILITIES - responsibilities
        if missing_responsibilities:
            errors.append(
                f"{label}.responsibilities missing: "
                + ", ".join(sorted(missing_responsibilities))
            )
        forbidden_overlap = responsibilities & PROFILE_OWNERSHIP
        if forbidden_overlap:
            errors.append(
                f"{label} assigns profile-owned responsibilities to an agent: "
                + ", ".join(sorted(forbidden_overlap))
            )
        cannot_own = _as_set(binding.get("cannot_own"))
        missing_forbidden = AGENT_FORBIDDEN_OWNERSHIP - cannot_own
        if missing_forbidden:
            errors.append(
                f"{label}.cannot_own missing: "
                + ", ".join(sorted(missing_forbidden))
            )

    known_skills = skill_ids(root)
    for index, item in enumerate(record.get("skills", []) if isinstance(record.get("skills"), list) else []):
        if not isinstance(item, dict):
            errors.append(f"skills[{index}] must be an object")
            continue
        skill_id = str(item.get("skill_id", ""))
        if skill_id not in known_skills:
            errors.append(f"skills[{index}] references unknown skill: {skill_id}")

    known_mcp = mcp_ids(root)
    for index, item in enumerate(record.get("mcp", []) if isinstance(record.get("mcp"), list) else []):
        if not isinstance(item, dict):
            errors.append(f"mcp[{index}] must be an object")
            continue
        mcp_id = str(item.get("mcp_id", ""))
        if mcp_id not in known_mcp:
            errors.append(f"mcp[{index}] references unknown MCP: {mcp_id}")
        toolsets = item.get("toolsets", [])
        if not isinstance(toolsets, list) or not toolsets:
            errors.append(f"mcp[{index}].toolsets must be non-empty")
        if any(str(toolset).strip() == "*" for toolset in toolsets if isinstance(toolsets, list)):
            errors.append(f"mcp[{index}] must not expose wildcard toolsets")
        approval = item.get("approval", {})
        if not isinstance(approval, dict):
            errors.append(f"mcp[{index}].approval must be an object")
        else:
            if approval.get("write") not in {"prompt", "deny"}:
                errors.append(f"mcp[{index}].approval.write must be prompt or deny")
            if approval.get("destructive") != "deny":
                errors.append(f"mcp[{index}].approval.destructive must be deny")

    known_knowledge = knowledge_ids(root)
    for index, item in enumerate(record.get("knowledge", []) if isinstance(record.get("knowledge"), list) else []):
        if not isinstance(item, dict):
            errors.append(f"knowledge[{index}] must be an object")
            continue
        pack_id = str(item.get("pack_id", ""))
        if pack_id not in known_knowledge:
            errors.append(f"knowledge[{index}] references unknown pack: {pack_id}")

    permissions = record.get("permissions", {})
    if not isinstance(permissions, dict):
        errors.append("permissions must be an object")
    else:
        for field in ["repository_write", "merge", "deploy", "secret_access"]:
            if permissions.get(field) is not False:
                errors.append(f"permissions.{field} must default to false in public profiles")
        if permissions.get("repository_read") is not True:
            warnings.append("permissions.repository_read is not enabled")

    routing = record.get("model_routing", {})
    if not isinstance(routing, dict):
        errors.append("model_routing must be an object")
        routing = {}
    if routing.get("policy") != "lowest_authority_sufficient":
        errors.append("model_routing.policy must be lowest_authority_sufficient")
    lanes = routing.get("lanes", [])
    lane_ids: set[str] = set()
    if not isinstance(lanes, list):
        errors.append("model_routing.lanes must be a list")
        lanes = []
    for index, lane in enumerate(lanes):
        label = f"model_routing.lanes[{index}]"
        if not isinstance(lane, dict):
            errors.append(f"{label} must be an object")
            continue
        lane_id = str(lane.get("lane_id", ""))
        if not lane_id:
            errors.append(f"{label}.lane_id is required")
        elif lane_id in lane_ids:
            errors.append(f"duplicate model lane: {lane_id}")
        lane_ids.add(lane_id)
        model_class = str(lane.get("model_class", ""))
        authority = str(lane.get("max_authority", ""))
        expected_authority = {
            "economy": "candidate",
            "coding": "candidate_change",
            "flagship": "judged",
            "human": "human_decision",
        }.get(model_class)
        if expected_authority and authority != expected_authority:
            errors.append(
                f"{label}.max_authority must be {expected_authority} for {model_class}"
            )
        forbidden = _as_set(lane.get("forbidden"))
        if model_class == "economy":
            required = {"approve_delivery", "resolve_p0_conflict", "expand_scope"}
            if not required.issubset(forbidden):
                errors.append(f"{label} does not sufficiently restrict economy models")
        if model_class == "flagship":
            required = {"self_confirm_delivery", "override_machine_failure"}
            if not required.issubset(forbidden):
                errors.append(f"{label} does not sufficiently restrict flagship models")
    missing_lanes = REQUIRED_LANES - lane_ids
    if missing_lanes:
        errors.append("model_routing is missing lanes: " + ", ".join(sorted(missing_lanes)))

    escalation = _as_set(routing.get("escalation_triggers"))
    missing_escalation = REQUIRED_ESCALATION_TRIGGERS - escalation
    if missing_escalation:
        errors.append(
            "model_routing.escalation_triggers missing: "
            + ", ".join(sorted(missing_escalation))
        )

    verification = record.get("verification", {})
    if not isinstance(verification, dict):
        errors.append("verification must be an object")
    else:
        if verification.get("independent_review") is not True:
            errors.append("verification.independent_review must be true")
        if verification.get("delivery_verdict") not in {
            "evidence_gate",
            "evidence_and_human_gate",
        }:
            errors.append("verification.delivery_verdict cannot be model-only")
        if verification.get("model_consensus_is_not_proof") is not True:
            errors.append("verification must state that model consensus is not proof")
        deterministic = verification.get("deterministic", [])
        if not isinstance(deterministic, list) or not deterministic:
            errors.append("verification.deterministic must be non-empty")

    handoff = record.get("handoff", {})
    if not isinstance(handoff, dict):
        errors.append("handoff must be an object")
    else:
        missing_handoff = REQUIRED_HANDOFF_FIELDS - _as_set(handoff.get("required_fields"))
        if missing_handoff:
            errors.append(
                "handoff.required_fields missing: "
                + ", ".join(sorted(missing_handoff))
            )
        if handoff.get("full_reasoning_transcript_authoritative") is not False:
            errors.append("full reasoning transcripts must not be authoritative handoffs")

    cache = record.get("cache", {})
    if not isinstance(cache, dict):
        errors.append("cache must be an object")
    else:
        if cache.get("scope") != "model_and_profile_version":
            errors.append("cache.scope must be model_and_profile_version")
        if cache.get("cross_model_reuse") is not False:
            errors.append("cache.cross_model_reuse must be false")
        missing_cache_fields = REQUIRED_CACHE_KEY_FIELDS - _as_set(cache.get("include_in_key"))
        if missing_cache_fields:
            errors.append(
                "cache.include_in_key missing: "
                + ", ".join(sorted(missing_cache_fields))
            )
        missing_invalidators = REQUIRED_CACHE_INVALIDATORS - _as_set(cache.get("invalidate_on"))
        if missing_invalidators:
            errors.append(
                "cache.invalidate_on missing: "
                + ", ".join(sorted(missing_invalidators))
            )
        if int(cache.get("write_when_expected_reuses_at_least", 0) or 0) < 2:
            errors.append("cache writes require at least two expected uses")
        for field in ["stable_prefix", "dynamic_suffix"]:
            if not isinstance(cache.get(field), list) or not cache.get(field):
                errors.append(f"cache.{field} must be non-empty")

    human = record.get("human_factors", {})
    if not isinstance(human, dict):
        errors.append("human_factors must be an object")
    else:
        if human.get("evidence_status") != "hypothesis":
            errors.append("human_factors outcomes must remain hypotheses until observed")
        missing_intents = REQUIRED_HUMAN_INTENTS - _as_set(human.get("design_intents"))
        if missing_intents:
            errors.append(
                "human_factors.design_intents missing: "
                + ", ".join(sorted(missing_intents))
            )
        missing_avoids = REQUIRED_HUMAN_AVOIDS - _as_set(human.get("avoid"))
        if missing_avoids:
            errors.append(
                "human_factors.avoid missing: " + ", ".join(sorted(missing_avoids))
            )
        if human.get("telemetry_use") != "system_improvement_only":
            errors.append("human_factors telemetry must be for system improvement only")

    telemetry = record.get("telemetry", {})
    if not isinstance(telemetry, dict):
        errors.append("telemetry must be an object")
    else:
        for field in [
            "record_profile_hash",
            "record_model_lane",
            "record_toolset_hash",
            "record_cached_tokens",
            "record_quality_outcome",
        ]:
            if telemetry.get(field) is not True:
                errors.append(f"telemetry.{field} must be true")
        if telemetry.get("personnel_ranking") is not False:
            errors.append("telemetry.personnel_ranking must be false")

    validation = record.get("validation", [])
    if not isinstance(validation, list) or not validation:
        errors.append("validation must be a non-empty list")
    else:
        for command in validation:
            for token in str(command).split():
                if token.endswith(".py") and not (root / token).exists():
                    errors.append(f"validation references missing script: {token}")

    return errors, warnings


def find_profiles(root: Path) -> list[Path]:
    return sorted((root / "examples" / "capability-profiles").glob("*.json"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", nargs="?", help="Profile path. Defaults to committed examples.")
    parser.add_argument("--root", default=".", help="Lattice repository root.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    paths = [Path(args.profile)] if args.profile else find_profiles(root)
    if not paths:
        print("Errors:", file=sys.stderr)
        print("- no capability profile examples found", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    all_warnings: list[str] = []
    for path in paths:
        path = path if path.is_absolute() else root / path
        try:
            errors, warnings = validate_profile(path, root)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors, warnings = [str(exc)], []
        try:
            rel = path.relative_to(root)
        except ValueError:
            rel = path
        all_errors.extend(f"{rel}: {message}" for message in errors)
        all_warnings.extend(f"{rel}: {message}" for message in warnings)

    if all_warnings:
        print("Warnings:")
        for warning in all_warnings:
            print(f"- {warning}")
    if all_errors:
        print("Errors:", file=sys.stderr)
        for error in all_errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"validated {len(paths)} capability profile(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
