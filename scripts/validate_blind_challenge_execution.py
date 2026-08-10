#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate Blind Challenge Execution against a frozen Harness Mutation Candidate.

The JSON Schema owns structure. This validator owns cross-file lineage, frozen-plan
parity, reserved-oracle blindness, complete case allocation coverage, protected-metric
gates, post-evaluation variant reveal, the observed-evidence gate, and the promotion
firewall.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import validate_blind_challenge_observed_evidence as OBSERVED
import validate_reserved_evaluation_handoff_v2 as HANDOFF_V2

CONTRACT = "lat.blind_challenge_execution.v1"
MISSION = "lat.goal.verified-decision-yield.v1"
REQUIRED_DECISIONS = {"reject", "revise", "continue_shadow", "scoped_canary"}
CRITICAL_PROTECTED = {
    "critical_false_ready",
    "authority_drift",
    "private_to_public_leakage",
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def _parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _target_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    plan = candidate.get("evaluation_plan", {})
    mutation = candidate.get("mutation", {})
    return {
        "candidate_id": candidate.get("candidate_id"),
        "candidate_version": candidate.get("version"),
        "failure_point": candidate.get("failure_point"),
        "mechanism": mutation.get("mechanism") if isinstance(mutation, dict) else None,
        "primary_delta": mutation.get("primary_delta") if isinstance(mutation, dict) else None,
        "hypothesis": mutation.get("hypothesis") if isinstance(mutation, dict) else None,
        "primary_metric": plan.get("primary_metric") if isinstance(plan, dict) else None,
        "protected_metrics": plan.get("protected_metrics") if isinstance(plan, dict) else None,
        "non_regression_constraints": plan.get("non_regression_constraints") if isinstance(plan, dict) else None,
    }


def expected_target_hash(candidate: dict[str, Any]) -> str:
    return _canonical_hash(_target_payload(candidate))


def expected_case_allocations_hash(candidate: dict[str, Any]) -> str:
    plan = candidate.get("evaluation_plan", {})
    allocations = plan.get("case_allocations", []) if isinstance(plan, dict) else []
    return _canonical_hash(allocations)


def _allocation_map(candidate: dict[str, Any]) -> dict[str, dict[str, Any]]:
    plan = candidate.get("evaluation_plan", {})
    allocations = plan.get("case_allocations", []) if isinstance(plan, dict) else []
    return {
        str(item.get("case_id")): item
        for item in allocations
        if isinstance(item, dict) and item.get("case_id")
    }


def _candidate_variants(candidate: dict[str, Any]) -> set[str]:
    mutation = candidate.get("mutation", {})
    if not isinstance(mutation, dict):
        return set()
    variants: set[str] = set()
    for name in ("incumbent", "challenger"):
        value = mutation.get(name)
        if isinstance(value, dict) and value.get("variant_id"):
            variants.add(str(value.get("variant_id")))
    return variants


def _challenger_id(candidate: dict[str, Any]) -> str:
    mutation = candidate.get("mutation", {})
    challenger = mutation.get("challenger", {}) if isinstance(mutation, dict) else {}
    return str(challenger.get("variant_id", "")) if isinstance(challenger, dict) else ""


def _result_map(execution: dict[str, Any]) -> dict[str, dict[str, Any]]:
    results = execution.get("case_results", [])
    return {
        str(item.get("case_id")): item
        for item in results
        if isinstance(item, dict) and item.get("case_id")
    }


def validate_execution(
    execution: dict[str, Any],
    candidate: dict[str, Any],
    *,
    handoff_records: list[dict[str, Any]] | None = None,
    blocked_execution: dict[str, Any] | None = None,
    handoff_schema: dict[str, Any] | None = None,
    trust_store: dict[str, Any] | None = None,
    consumed_nonces: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []

    if execution.get("contract") != CONTRACT:
        errors.append(f"contract must be {CONTRACT}")
    if execution.get("mission_anchor_ref") != MISSION:
        errors.append(f"mission_anchor_ref must be {MISSION}")
    if candidate.get("mission_anchor_ref") != MISSION:
        errors.append("candidate must preserve the Verified Decision Yield mission anchor")

    if execution.get("candidate_id") != candidate.get("candidate_id"):
        errors.append("execution candidate_id must match Harness Mutation Candidate")
    if execution.get("candidate_version") != candidate.get("version"):
        errors.append("execution candidate_version must match Harness Mutation Candidate")

    plan = candidate.get("evaluation_plan")
    frozen = execution.get("frozen_plan")
    if not isinstance(plan, dict) or not isinstance(frozen, dict):
        errors.append("candidate evaluation_plan and execution frozen_plan are required")
        return errors

    for field in ("evaluator_version", "primary_metric"):
        if frozen.get(field) != plan.get(field):
            errors.append(f"frozen_plan.{field} must match candidate evaluation plan")

    if list(frozen.get("protected_metrics", [])) != list(plan.get("protected_metrics", [])):
        errors.append("frozen_plan.protected_metrics must match candidate evaluation plan exactly")
    if set(frozen.get("decision_options", [])) != REQUIRED_DECISIONS:
        errors.append("frozen_plan.decision_options must be exactly reject, revise, continue_shadow, scoped_canary")
    if set(plan.get("decision_options", [])) != REQUIRED_DECISIONS:
        errors.append("candidate decision_options must remain the four governed verdicts")

    if frozen.get("target_hash") != expected_target_hash(candidate):
        errors.append("frozen_plan.target_hash does not match the canonical candidate target")
    if frozen.get("case_allocations_hash") != expected_case_allocations_hash(candidate):
        errors.append("frozen_plan.case_allocations_hash does not match candidate case allocations")

    blindness = execution.get("blindness")
    if not isinstance(blindness, dict):
        errors.append("blindness block is required")
    else:
        if blindness.get("variant_labels_blinded_to_evaluator") is not True:
            errors.append("variant labels must remain blinded during evaluation")
        if blindness.get("candidate_author_can_view_reserved_outcome") is not False:
            errors.append("candidate author cannot view reserved outcome during evaluation")
        if blindness.get("reserved_oracle_visibility") != "evaluator_only":
            errors.append("reserved oracle visibility must be evaluator_only")
        if blindness.get("oracle_content_included") is not False:
            errors.append("Blind Challenge receipt must not embed reserved oracle content")
        if blindness.get("mapping_revealed_after_evaluation") is not True:
            errors.append("variant mapping may be revealed only after evaluation")

    allocations = _allocation_map(candidate)
    reserved_allocations = [item for item in allocations.values() if item.get("class") == "reserved"]
    if len(reserved_allocations) != 1:
        errors.append("candidate must define exactly one reserved case for Blind Challenge v1")
        reserved_case_id = ""
    else:
        reserved_case_id = str(reserved_allocations[0].get("case_id", ""))
        reserved = reserved_allocations[0]
        if reserved.get("availability") != "external_required":
            errors.append("reserved case must remain externally supplied")
        if reserved.get("oracle_visibility") != "evaluator_only":
            errors.append("reserved case oracle must remain evaluator_only")

    oracle = execution.get("reserved_oracle")
    if not isinstance(oracle, dict):
        errors.append("reserved_oracle block is required")
    else:
        if reserved_case_id and oracle.get("case_id") != reserved_case_id:
            errors.append("reserved_oracle.case_id must match candidate reserved allocation")
        if oracle.get("oracle_visibility") != "evaluator_only":
            errors.append("reserved oracle must remain evaluator_only")
        if oracle.get("oracle_content_included") is not False:
            errors.append("reserved oracle contents must not be copied into the execution receipt")

    results = execution.get("case_results")
    if not isinstance(results, list):
        errors.append("case_results must be a list")
        results = []

    result_ids: set[str] = set()
    for index, result in enumerate(results):
        if not isinstance(result, dict):
            errors.append(f"case_results[{index}] must be an object")
            continue
        case_id = str(result.get("case_id", ""))
        if case_id in result_ids:
            errors.append(f"duplicate case result: {case_id}")
        result_ids.add(case_id)
        allocation = allocations.get(case_id)
        if allocation is None:
            errors.append(f"case result not present in frozen candidate allocation: {case_id}")
            continue
        if result.get("class") != allocation.get("class"):
            errors.append(f"case result class must match allocation for {case_id}")

        variant_outcomes = result.get("variant_outcomes", [])
        if not isinstance(variant_outcomes, list):
            errors.append(f"case result {case_id} variant_outcomes must be a list")
            variant_outcomes = []
        labels = [item.get("label") for item in variant_outcomes if isinstance(item, dict)]
        if sorted(labels) != ["A", "B"]:
            errors.append(f"case result {case_id} must contain exactly anonymous variants A and B")

        metrics = result.get("protected_metrics", [])
        if not isinstance(metrics, list):
            errors.append(f"case result {case_id} protected_metrics must be a list")
            metrics = []
        metric_names = [str(item.get("metric")) for item in metrics if isinstance(item, dict)]
        if set(metric_names) != set(plan.get("protected_metrics", [])):
            errors.append(f"case result {case_id} must evaluate every protected metric exactly once")
        if len(metric_names) != len(set(metric_names)):
            errors.append(f"case result {case_id} contains duplicate protected metrics")

    status = execution.get("status")
    decision = execution.get("decision")
    mapping = execution.get("variant_mapping")
    created = _parse_time(execution.get("created_at"))
    completed = _parse_time(execution.get("completed_at")) if execution.get("completed_at") else None

    if status == "blocked_pending_reserved_oracle":
        if decision is not None:
            errors.append("blocked execution cannot emit a governed verdict")
        if mapping is not None:
            errors.append("blocked execution cannot reveal variant mapping")
        if isinstance(oracle, dict) and oracle.get("status") != "unavailable":
            errors.append("blocked execution requires reserved oracle status unavailable")
        if reserved_case_id and reserved_case_id in result_ids:
            errors.append("blocked execution cannot claim a reserved-case result")
        allowed_non_reserved = {case_id for case_id, item in allocations.items() if item.get("class") != "reserved"}
        if not result_ids.issubset(allowed_non_reserved):
            errors.append("blocked execution may contain only frozen non-reserved preflight results")

    elif status == "evaluated":
        if created is None or completed is None:
            errors.append("evaluated execution requires parseable created_at and completed_at")
        elif completed < created:
            errors.append("completed_at cannot be before created_at")

        if isinstance(oracle, dict):
            if oracle.get("status") != "available":
                errors.append("evaluated execution requires reserved oracle attestation")
            for field in ("attestation_ref", "attestation_hash", "evaluated_by", "evaluated_at"):
                if not str(oracle.get(field, "")).strip():
                    errors.append(f"evaluated reserved oracle requires {field}")

        if set(result_ids) != set(allocations):
            missing = set(allocations) - result_ids
            extra = result_ids - set(allocations)
            if missing:
                errors.append("evaluated execution missing case results: " + ", ".join(sorted(missing)))
            if extra:
                errors.append("evaluated execution has extra case results: " + ", ".join(sorted(extra)))

        if not isinstance(mapping, dict):
            errors.append("evaluated execution requires post-evaluation variant mapping")
            challenger_label = ""
        else:
            mapped_variants = {str(mapping.get("A", "")), str(mapping.get("B", ""))}
            if mapped_variants != _candidate_variants(candidate):
                errors.append("variant_mapping must map A/B exactly to incumbent and challenger variants")
            reveal_time = _parse_time(mapping.get("revealed_at"))
            if completed is None or reveal_time is None or reveal_time < completed:
                errors.append("variant_mapping.revealed_at must be at or after completed_at")
            challenger = _challenger_id(candidate)
            challenger_label = "A" if mapping.get("A") == challenger else "B" if mapping.get("B") == challenger else ""

        if not isinstance(decision, dict):
            errors.append("evaluated execution requires exactly one governed verdict")
            verdict = ""
        else:
            verdict = str(decision.get("verdict", ""))
            if verdict not in REQUIRED_DECISIONS:
                errors.append("decision verdict must be reject, revise, continue_shadow, or scoped_canary")
            if decision.get("human_approval_required") is not True:
                errors.append("Blind Challenge verdict cannot bypass human approval")
            if decision.get("team_available_allowed") is not False:
                errors.append("Blind Challenge verdict cannot grant team_available")

        any_critical_failure = False
        any_not_evaluated = False
        for result in results:
            if not isinstance(result, dict):
                continue
            for metric in result.get("protected_metrics", []):
                if not isinstance(metric, dict):
                    continue
                name = str(metric.get("metric", ""))
                metric_status = metric.get("status")
                if metric_status == "not_evaluated":
                    any_not_evaluated = True
                if name in CRITICAL_PROTECTED and metric_status == "fail":
                    any_critical_failure = True

        if any_critical_failure and verdict not in {"reject", "revise"}:
            errors.append("critical protected-metric failure permits only reject or revise")
        if any_not_evaluated and verdict == "scoped_canary":
            errors.append("scoped_canary requires all protected metrics to be evaluated")

        if verdict == "scoped_canary":
            scope = decision.get("scoped_canary_scope") if isinstance(decision, dict) else None
            if not isinstance(scope, list) or not scope:
                errors.append("scoped_canary requires an explicit bounded scope")
            reserved_result = _result_map(execution).get(reserved_case_id)
            if not isinstance(reserved_result, dict):
                errors.append("scoped_canary requires a reserved-case result")
            elif not challenger_label:
                errors.append("scoped_canary requires a valid challenger label after mapping reveal")
            else:
                outcome_by_label = {
                    str(item.get("label")): item
                    for item in reserved_result.get("variant_outcomes", [])
                    if isinstance(item, dict)
                }
                challenger_outcome = outcome_by_label.get(challenger_label, {})
                if challenger_outcome.get("target_result") != "pass":
                    errors.append("scoped_canary requires challenger to pass the reserved target")
                if reserved_result.get("comparison") == "inconclusive":
                    errors.append("scoped_canary cannot follow an inconclusive reserved comparison")

    else:
        errors.append("status must be blocked_pending_reserved_oracle or evaluated")

    promotion = execution.get("promotion_boundary")
    if not isinstance(promotion, dict):
        errors.append("promotion_boundary is required")
    else:
        if promotion.get("automatic_promotion_allowed") is not False:
            errors.append("automatic promotion is forbidden")
        if promotion.get("team_available_allowed") is not False:
            errors.append("Blind Challenge cannot grant team_available")
        if promotion.get("human_owner_required") is not True:
            errors.append("human owner remains required")
        if promotion.get("scoped_canary_requires_human_approval") is not True:
            errors.append("scoped canary requires human approval")

    errors.extend(
        OBSERVED.validate_observed_evidence(
            execution,
            candidate,
            handoff_records=handoff_records,
            blocked_execution=blocked_execution,
            handoff_schema=handoff_schema,
            trust_store=trust_store,
            consumed_nonces=consumed_nonces,
        )
    )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("execution", help="Blind Challenge Execution JSON path")
    parser.add_argument("candidate", help="Harness Mutation Candidate JSON path")
    parser.add_argument(
        "--reserved-handoff-v2",
        help="Authenticated Reserved Evaluation Handoff v2 JSONL; required for downstream_observed/scoped_canary",
    )
    parser.add_argument(
        "--blocked-execution",
        help="Blocked source Blind Challenge Execution used to create the reserved request",
    )
    parser.add_argument(
        "--handoff-schema-v2",
        help="Reserved Evaluation Handoff v2 JSON Schema path",
    )
    parser.add_argument(
        "--trust-store",
        help="Trusted evaluator public-key store",
    )
    parser.add_argument(
        "--consumed-nonces",
        help="Consumed request nonce ledger",
    )
    args = parser.parse_args()

    try:
        execution = load_json(Path(args.execution))
        candidate = load_json(Path(args.candidate))
        handoff_records = (
            HANDOFF_V2.load_jsonl(Path(args.reserved_handoff_v2))
            if args.reserved_handoff_v2
            else None
        )
        blocked_execution = (
            load_json(Path(args.blocked_execution)) if args.blocked_execution else None
        )
        handoff_schema = (
            load_json(Path(args.handoff_schema_v2)) if args.handoff_schema_v2 else None
        )
        trust_store = (
            load_json(Path(args.trust_store)) if args.trust_store else None
        )
        consumed_nonces = (
            HANDOFF_V2.load_consumed_nonces(Path(args.consumed_nonces))
            if args.consumed_nonces
            else None
        )
        errors = validate_execution(
            execution,
            candidate,
            handoff_records=handoff_records,
            blocked_execution=blocked_execution,
            handoff_schema=handoff_schema,
            trust_store=trust_store,
            consumed_nonces=consumed_nonces,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"validated Blind Challenge Execution: {args.execution}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
