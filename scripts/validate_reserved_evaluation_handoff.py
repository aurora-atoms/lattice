#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate controlled reserved-evaluation JSONL handoffs.

The JSON Schema owns record structure. This validator owns cross-record and
cross-contract lineage between a Harness Mutation Candidate, a blocked Blind
Challenge Execution, the public request, and an optional safe evaluator
attestation. Raw reserved-oracle content is never accepted by this protocol.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_ID = "lat.reserved_evaluation_handoff.v1"
MISSION = "lat.goal.verified-decision-yield.v1"
REQUEST_TYPE = "eval.reserved_request"
ATTESTATION_TYPE = "eval.reserved_attestation"
REQUIRED_OUTPUTS = {
    "anonymous_variant_outcomes",
    "comparison",
    "protected_metrics",
    "attestation_digest",
}
SAFE_EVIDENCE_PREFIXES = (
    "attestation://",
    "digest://",
    "redacted://",
)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_no}: expected JSON object")
        records.append(value)
    return records


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def schema_errors(record: dict[str, Any], schema: dict[str, Any], index: int) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors: list[str] = []
    for error in sorted(validator.iter_errors(record), key=lambda item: list(item.absolute_path)):
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"record[{index}] {location}: {error.message}")
    return errors


def reserved_allocation(candidate: dict[str, Any]) -> dict[str, Any] | None:
    plan = candidate.get("evaluation_plan")
    allocations = plan.get("case_allocations", []) if isinstance(plan, dict) else []
    reserved = [
        item
        for item in allocations
        if isinstance(item, dict) and item.get("class") == "reserved"
    ]
    return reserved[0] if len(reserved) == 1 else None


def collect_safe_evidence_refs(value: Any) -> list[str]:
    refs: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            if key == "evidence_refs" and isinstance(nested, list):
                refs.extend(str(item) for item in nested)
            else:
                refs.extend(collect_safe_evidence_refs(nested))
    elif isinstance(value, list):
        for nested in value:
            refs.extend(collect_safe_evidence_refs(nested))
    return refs


def expected_scope(
    candidate: dict[str, Any],
    execution: dict[str, Any],
    reserved: dict[str, Any],
) -> dict[str, Any]:
    frozen = execution.get("frozen_plan", {})
    return {
        "candidate_id": candidate.get("candidate_id"),
        "candidate_version": candidate.get("version"),
        "execution_id": execution.get("execution_id"),
        "reserved_case_id": reserved.get("case_id"),
        "mission_anchor_ref": MISSION,
        "target_hash": frozen.get("target_hash") if isinstance(frozen, dict) else None,
        "case_allocations_hash": (
            frozen.get("case_allocations_hash") if isinstance(frozen, dict) else None
        ),
    }


def validate_handoff(
    records: list[dict[str, Any]],
    candidate: dict[str, Any],
    execution: dict[str, Any],
    schema: dict[str, Any],
) -> list[str]:
    errors: list[str] = []

    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema exposes several schema exceptions
        return [f"invalid handoff schema: {exc}"]

    if not records:
        return ["handoff JSONL must contain one request record"]
    if len(records) > 2:
        errors.append("handoff JSONL may contain one request and at most one attestation")

    for index, record in enumerate(records):
        errors.extend(schema_errors(record, schema, index))

    ids = [str(record.get("id", "")) for record in records]
    if any(not item for item in ids):
        errors.append("every handoff record requires a non-empty id")
    if len(ids) != len(set(ids)):
        errors.append("handoff record ids must be unique")

    types = [record.get("type") for record in records]
    if types[0] != REQUEST_TYPE:
        errors.append("first handoff record must be eval.reserved_request")
    if types.count(REQUEST_TYPE) != 1:
        errors.append("handoff must contain exactly one eval.reserved_request")
    if types.count(ATTESTATION_TYPE) > 1:
        errors.append("handoff may contain at most one eval.reserved_attestation")
    if len(records) == 2 and types[1] != ATTESTATION_TYPE:
        errors.append("second handoff record, when present, must be eval.reserved_attestation")

    if candidate.get("mission_anchor_ref") != MISSION:
        errors.append("candidate must preserve the Verified Decision Yield mission anchor")
    if execution.get("mission_anchor_ref") != MISSION:
        errors.append("Blind Challenge Execution must preserve the mission anchor")
    if execution.get("candidate_id") != candidate.get("candidate_id"):
        errors.append("execution candidate_id must match candidate")
    if execution.get("candidate_version") != candidate.get("version"):
        errors.append("execution candidate_version must match candidate version")
    if execution.get("status") != "blocked_pending_reserved_oracle":
        errors.append("handoff may only start from a blocked_pending_reserved_oracle execution")
    if execution.get("decision") is not None:
        errors.append("blocked source execution cannot already contain a governed verdict")
    if execution.get("variant_mapping") is not None:
        errors.append("blocked source execution cannot already expose variant mapping")

    oracle = execution.get("reserved_oracle")
    if not isinstance(oracle, dict) or oracle.get("status") != "unavailable":
        errors.append("blocked source execution must record reserved oracle as unavailable")

    reserved = reserved_allocation(candidate)
    if reserved is None:
        errors.append("candidate must define exactly one reserved allocation")
        return errors
    if reserved.get("availability") != "external_required":
        errors.append("reserved allocation must remain external_required")
    if reserved.get("oracle_visibility") != "evaluator_only":
        errors.append("reserved allocation oracle must remain evaluator_only")

    scope = expected_scope(candidate, execution, reserved)
    plan = candidate.get("evaluation_plan")
    if not isinstance(plan, dict):
        errors.append("candidate evaluation_plan is required")
        return errors

    request = records[0]
    if request.get("schema") != SCHEMA_ID:
        errors.append(f"request schema must be {SCHEMA_ID}")
    if request.get("scope") != scope:
        errors.append("request scope must exactly match frozen candidate/execution lineage")
    payload = request.get("payload")
    if not isinstance(payload, dict):
        errors.append("request payload must be an object")
        return errors

    if payload.get("evaluator_version") != plan.get("evaluator_version"):
        errors.append("request evaluator_version must match candidate evaluation plan")
    if payload.get("primary_metric") != plan.get("primary_metric"):
        errors.append("request primary_metric must match candidate evaluation plan")
    if list(payload.get("protected_metrics", [])) != list(plan.get("protected_metrics", [])):
        errors.append("request protected_metrics must match candidate evaluation plan exactly")
    if set(payload.get("variant_labels", [])) != {"A", "B"}:
        errors.append("request variant_labels must be exactly A and B")
    if set(payload.get("requested_outputs", [])) != REQUIRED_OUTPUTS:
        errors.append("request requested_outputs must be the four safe attestation outputs")
    issued_at = parse_time(payload.get("issued_at"))
    if issued_at is None:
        errors.append("request issued_at must be a parseable date-time")

    if len(records) == 1:
        return errors

    attestation = records[1]
    if attestation.get("scope") != scope:
        errors.append("attestation scope must exactly match request scope")
    att_payload = attestation.get("payload")
    if not isinstance(att_payload, dict):
        errors.append("attestation payload must be an object")
        return errors

    if att_payload.get("evaluator_version") != payload.get("evaluator_version"):
        errors.append("attestation evaluator_version must match the frozen request")
    if att_payload.get("variant_bundle_ref") != payload.get("variant_bundle_ref"):
        errors.append("attestation variant_bundle_ref must match the frozen request")

    evaluated_at = parse_time(att_payload.get("evaluated_at"))
    if evaluated_at is None:
        errors.append("attestation evaluated_at must be a parseable date-time")
    elif issued_at is not None and evaluated_at < issued_at:
        errors.append("attestation evaluated_at cannot precede request issued_at")

    result = att_payload.get("reserved_case_result")
    if not isinstance(result, dict):
        errors.append("attestation requires reserved_case_result")
        return errors
    if result.get("case_id") != reserved.get("case_id"):
        errors.append("attestation reserved case id must match candidate reserved allocation")
    if result.get("class") != "reserved":
        errors.append("attestation result must remain class=reserved")

    outcomes = result.get("variant_outcomes", [])
    labels = [
        item.get("label")
        for item in outcomes
        if isinstance(item, dict)
    ] if isinstance(outcomes, list) else []
    if sorted(labels) != ["A", "B"]:
        errors.append("attestation must contain exactly anonymous variant outcomes A and B")

    metrics = result.get("protected_metrics", [])
    metric_names = [
        str(item.get("metric"))
        for item in metrics
        if isinstance(item, dict)
    ] if isinstance(metrics, list) else []
    if metric_names != list(plan.get("protected_metrics", [])):
        errors.append("attestation protected metrics must match the frozen plan exactly")
    if len(metric_names) != len(set(metric_names)):
        errors.append("attestation protected metrics cannot contain duplicates")

    for ref in collect_safe_evidence_refs(result):
        if not ref.startswith(SAFE_EVIDENCE_PREFIXES):
            errors.append(
                "attestation evidence refs must be safe projections using "
                "attestation://, digest://, or redacted://"
            )
            break

    if att_payload.get("oracle_content_included") is not False:
        errors.append("attestation must not include reserved oracle content")
    if att_payload.get("variant_mapping_included") is not False:
        errors.append("attestation must not expose incumbent/challenger mapping")
    if att_payload.get("governed_verdict_included") is not False:
        errors.append("attestation cannot emit the Blind Challenge governed verdict")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("handoff", help="JSONL handoff path")
    parser.add_argument("candidate", help="Harness Mutation Candidate JSON path")
    parser.add_argument("execution", help="Blocked Blind Challenge Execution JSON path")
    parser.add_argument(
        "--schema",
        required=True,
        help="Reserved Evaluation Handoff record JSON Schema path",
    )
    args = parser.parse_args()

    try:
        records = load_jsonl(Path(args.handoff))
        candidate = load_json(Path(args.candidate))
        execution = load_json(Path(args.execution))
        schema = load_json(Path(args.schema))
        errors = validate_handoff(records, candidate, execution, schema)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    mode = "request+attestation" if len(records) == 2 else "request-only"
    print(f"validated reserved evaluation handoff ({mode}): {args.handoff}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
