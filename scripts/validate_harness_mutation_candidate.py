#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate a governed Harness Mutation Candidate against its source Case 0 outcome.

The JSON Schema owns structure. This validator owns cross-file lineage, failure-point
classification, one-delta targeting, blind-evaluation readiness, protected metrics,
and the human promotion firewall.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

CONTRACT = "lat.harness_mutation_candidate.v1"
MISSION = "lat.goal.verified-decision-yield.v1"

FAILURE_TO_MECHANISM = {
    "context_selection_gap": {"context_selection_change"},
    "low_value_attention_request": {"attention_gate_change"},
    "routing_or_tool_selection_error": {"routing_change", "tool_surface_change"},
    "no_new_evidence_loop": {"stop_rule_change"},
    "verification_gap": {"verifier_change"},
    "knowledge_freshness_gap": {"knowledge_freshness_change"},
    "recurring_skill_rule_gap": {"skill_or_rule_candidate"},
    "evaluator_too_permissive": {"eval_change"},
}

REQUIRED_PROTECTED = {
    "critical_false_ready",
    "authority_drift",
    "private_to_public_leakage",
}
REQUIRED_CASE_CLASSES = {"representative", "hard", "reserved"}
REQUIRED_DECISIONS = {"reject", "revise", "continue_shadow", "scoped_canary"}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def _refs(value: Any) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {str(item) for item in value}


def _evidence_ids(pack: dict[str, Any]) -> set[str]:
    return {
        str(item.get("id"))
        for item in pack.get("evidence_refs", [])
        if isinstance(item, dict) and item.get("id")
    }


def _parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def validate_candidate(
    candidate: dict[str, Any],
    outcome: dict[str, Any],
    pack: dict[str, Any],
) -> list[str]:
    errors: list[str] = []

    if candidate.get("contract") != CONTRACT:
        errors.append(f"contract must be {CONTRACT}")
    if candidate.get("mission_anchor_ref") != MISSION:
        errors.append(f"mission_anchor_ref must be {MISSION}")
    if candidate.get("status") != "session_local_candidate":
        errors.append("Harness mutation must begin as session_local_candidate")

    case_ids = {
        str(candidate.get("source_case_id", "")),
        str(outcome.get("case_id", "")),
        str(pack.get("case_id", "")),
    }
    if "" in case_ids or len(case_ids) != 1:
        errors.append("candidate, Outcome Receipt, and Portable Case Pack must share one case id")

    if outcome.get("mission_anchor_ref") != MISSION or pack.get("mission_anchor_ref") != MISSION:
        errors.append("source Outcome Receipt and Portable Case Pack must preserve the mission anchor")

    evidence_ids = _evidence_ids(pack)
    candidate_refs = _refs(candidate.get("evidence_refs"))
    failure = candidate.get("failure_point")
    failure_refs = _refs(failure.get("evidence_refs")) if isinstance(failure, dict) else set()
    unknown_refs = (candidate_refs | failure_refs) - evidence_ids
    if unknown_refs:
        errors.append("candidate references unknown Case Pack evidence: " + ", ".join(sorted(unknown_refs)))

    source_failure = outcome.get("earliest_failure_point")
    if not isinstance(source_failure, dict) or not isinstance(failure, dict):
        errors.append("candidate requires a structured earliest failure point from Outcome Receipt")
    else:
        for field in ("stage", "statement"):
            if failure.get(field) != source_failure.get(field):
                errors.append(f"candidate failure_point.{field} must match Outcome Receipt earliest failure")
        if _refs(failure.get("evidence_refs")) != _refs(source_failure.get("evidence_refs")):
            errors.append("candidate failure_point evidence must match Outcome Receipt earliest failure")

    source_candidate = outcome.get("failure_point_candidate")
    if not isinstance(source_candidate, dict) or source_candidate.get("eligible_for_harness_candidate") is not True:
        errors.append("source Outcome Receipt does not make the failure point eligible for a Harness candidate")
    elif source_candidate.get("promotion_authority") != "none_from_outcome_receipt":
        errors.append("source Outcome Receipt must not grant promotion authority")

    mutation = candidate.get("mutation")
    if not isinstance(mutation, dict):
        errors.append("mutation must be an object")
    else:
        category = failure.get("category") if isinstance(failure, dict) else None
        mechanism = mutation.get("mechanism")
        allowed = FAILURE_TO_MECHANISM.get(str(category), set())
        if mechanism not in allowed:
            errors.append(
                f"failure category {category!r} cannot target mechanism {mechanism!r}; allowed: {sorted(allowed)}"
            )
        incumbent = mutation.get("incumbent")
        challenger = mutation.get("challenger")
        if isinstance(incumbent, dict) and isinstance(challenger, dict):
            if incumbent.get("variant_id") == challenger.get("variant_id"):
                errors.append("incumbent and challenger must be distinct variants")

    created = _parse_time(candidate.get("created_at"))
    expires = _parse_time(candidate.get("expires_at"))
    if created is None or expires is None:
        errors.append("created_at and expires_at must be parseable date-times")
    elif expires <= created:
        errors.append("expires_at must be later than created_at")

    plan = candidate.get("evaluation_plan")
    if not isinstance(plan, dict):
        errors.append("evaluation_plan must be an object")
    else:
        if plan.get("target_frozen") is not True:
            errors.append("evaluation target must be frozen before blind comparison")
        blindness = plan.get("blindness")
        if not isinstance(blindness, dict):
            errors.append("evaluation_plan.blindness must be an object")
        else:
            if blindness.get("variant_labels_blinded_to_evaluator") is not True:
                errors.append("incumbent/challenger labels must be blinded to evaluator")
            if blindness.get("candidate_author_can_view_reserved_outcome") is not False:
                errors.append("candidate author must not be able to view reserved outcome")

        allocations = plan.get("case_allocations")
        if not isinstance(allocations, list):
            errors.append("case_allocations must be a list")
            allocations = []
        case_ids_seen: set[str] = set()
        classes: set[str] = set()
        has_external_reserved = False
        for index, allocation in enumerate(allocations):
            if not isinstance(allocation, dict):
                errors.append(f"case_allocations[{index}] must be an object")
                continue
            case_id = str(allocation.get("case_id", ""))
            if case_id in case_ids_seen:
                errors.append(f"duplicate evaluation case_id: {case_id}")
            case_ids_seen.add(case_id)
            case_class = str(allocation.get("class", ""))
            classes.add(case_class)
            if case_class == "reserved":
                if allocation.get("oracle_visibility") != "evaluator_only":
                    errors.append("reserved case oracle must be evaluator_only")
                if allocation.get("availability") != "external_required":
                    errors.append("public candidate must keep the reserved case external to the proposer")
                if not str(allocation.get("oracle_ref", "")).startswith("withheld://"):
                    errors.append("reserved case oracle_ref must remain withheld from the candidate author")
                has_external_reserved = True

        missing_classes = REQUIRED_CASE_CLASSES - classes
        if missing_classes:
            errors.append("evaluation plan missing required case classes: " + ", ".join(sorted(missing_classes)))

        protected = _refs(plan.get("protected_metrics"))
        missing_metrics = REQUIRED_PROTECTED - protected
        if missing_metrics:
            errors.append("evaluation plan missing protected metrics: " + ", ".join(sorted(missing_metrics)))

        decisions = _refs(plan.get("decision_options"))
        if decisions != REQUIRED_DECISIONS:
            errors.append("decision_options must be exactly reject, revise, continue_shadow, scoped_canary")

        if has_external_reserved and plan.get("status") != "blocked_pending_reserved_oracle":
            errors.append("candidate with external reserved oracle must remain blocked_pending_reserved_oracle")

    ownership = candidate.get("ownership")
    if not isinstance(ownership, dict) or not str(ownership.get("owner", "")).strip():
        errors.append("candidate requires an accountable human owner")
    elif ownership.get("human_approval_required") is not True:
        errors.append("candidate cannot cross the promotion firewall without human approval")

    promotion = candidate.get("promotion_boundary")
    if not isinstance(promotion, dict):
        errors.append("promotion_boundary must be an object")
    else:
        if promotion.get("automatic_promotion_allowed") is not False:
            errors.append("automatic Harness promotion is forbidden")
        if promotion.get("team_available_allowed") is not False:
            errors.append("a session-local candidate cannot grant team_available")
        if promotion.get("human_owner_required") is not True:
            errors.append("human owner is required for any later promotion decision")
        if promotion.get("reserved_non_regression_required") is not True:
            errors.append("reserved non-regression is required before later promotion")
        if promotion.get("live_case_required_before_team_available") is not True:
            errors.append("a real live case is required before any later team_available decision")

    rollback = candidate.get("rollback")
    if not isinstance(rollback, dict):
        errors.append("candidate requires rollback trigger, action, and revalidation")
    else:
        for field in ("trigger", "action", "revalidation"):
            if not str(rollback.get(field, "")).strip():
                errors.append(f"rollback.{field} is required")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", help="Harness Mutation Candidate JSON path")
    parser.add_argument("outcome", help="Source Outcome Receipt JSON path")
    parser.add_argument("pack", help="Source Portable Case Pack JSON path")
    args = parser.parse_args()

    try:
        candidate = load_json(Path(args.candidate))
        outcome = load_json(Path(args.outcome))
        pack = load_json(Path(args.pack))
        errors = validate_candidate(candidate, outcome, pack)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"validated Harness Mutation Candidate: {args.candidate}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
