#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Prepare a public-safe reserved-evaluation request JSONL record.

The script projects only frozen candidate/execution metadata. It does not receive
or emit the reserved oracle, raw private evidence, or incumbent/challenger mapping.
A controlled coordinator must provide an opaque blinded variant bundle reference.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

MISSION = "lat.goal.verified-decision-yield.v1"
SCHEMA_ID = "lat.reserved_evaluation_handoff.v1"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def reserved_allocation(candidate: dict[str, Any]) -> dict[str, Any]:
    plan = candidate.get("evaluation_plan")
    allocations = plan.get("case_allocations", []) if isinstance(plan, dict) else []
    reserved = [
        item
        for item in allocations
        if isinstance(item, dict) and item.get("class") == "reserved"
    ]
    if len(reserved) != 1:
        raise ValueError("candidate must define exactly one reserved allocation")
    return reserved[0]


def build_request(
    candidate: dict[str, Any],
    execution: dict[str, Any],
    *,
    request_id: str,
    issued_at: str,
    variant_bundle_ref: str,
) -> dict[str, Any]:
    if candidate.get("mission_anchor_ref") != MISSION:
        raise ValueError("candidate does not preserve the Verified Decision Yield mission anchor")
    if execution.get("mission_anchor_ref") != MISSION:
        raise ValueError("execution does not preserve the Verified Decision Yield mission anchor")
    if execution.get("status") != "blocked_pending_reserved_oracle":
        raise ValueError("request may only be prepared from blocked_pending_reserved_oracle")
    if execution.get("candidate_id") != candidate.get("candidate_id"):
        raise ValueError("execution candidate_id does not match candidate")
    if execution.get("candidate_version") != candidate.get("version"):
        raise ValueError("execution candidate_version does not match candidate")
    if not variant_bundle_ref.startswith("controlled://"):
        raise ValueError("variant_bundle_ref must use controlled:// and remain opaque")

    plan = candidate.get("evaluation_plan")
    frozen = execution.get("frozen_plan")
    oracle = execution.get("reserved_oracle")
    if not isinstance(plan, dict) or not isinstance(frozen, dict):
        raise ValueError("candidate evaluation_plan and execution frozen_plan are required")
    if not isinstance(oracle, dict) or oracle.get("status") != "unavailable":
        raise ValueError("source execution must still have an unavailable reserved oracle")
    if execution.get("decision") is not None or execution.get("variant_mapping") is not None:
        raise ValueError("source execution must not contain verdict or variant mapping")

    reserved = reserved_allocation(candidate)
    if reserved.get("availability") != "external_required":
        raise ValueError("reserved allocation must remain external_required")
    if reserved.get("oracle_visibility") != "evaluator_only":
        raise ValueError("reserved allocation must remain evaluator_only")

    return {
        "type": "eval.reserved_request",
        "id": request_id,
        "schema": SCHEMA_ID,
        "source": {
            "boundary": "public_repository",
            "role": "reserved_evaluation_coordinator",
        },
        "target": {
            "boundary": "controlled_private_evaluator",
            "role": "reserved_oracle_evaluator",
        },
        "scope": {
            "candidate_id": candidate.get("candidate_id"),
            "candidate_version": candidate.get("version"),
            "execution_id": execution.get("execution_id"),
            "reserved_case_id": reserved.get("case_id"),
            "mission_anchor_ref": MISSION,
            "target_hash": frozen.get("target_hash"),
            "case_allocations_hash": frozen.get("case_allocations_hash"),
        },
        "payload": {
            "status": "awaiting_external_evaluator",
            "issued_at": issued_at,
            "evaluator_version": plan.get("evaluator_version"),
            "primary_metric": plan.get("primary_metric"),
            "protected_metrics": list(plan.get("protected_metrics", [])),
            "variant_bundle_ref": variant_bundle_ref,
            "variant_labels": ["A", "B"],
            "requested_outputs": [
                "anonymous_variant_outcomes",
                "comparison",
                "protected_metrics",
                "attestation_digest",
            ],
        },
        "constraints": {
            "oracle_visibility": "evaluator_only",
            "oracle_content_allowed": False,
            "raw_private_evidence_allowed": False,
            "variant_mapping_allowed": False,
            "governed_verdict_allowed": False,
            "automatic_promotion_allowed": False,
            "team_available_allowed": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", help="Harness Mutation Candidate JSON path")
    parser.add_argument("execution", help="Blocked Blind Challenge Execution JSON path")
    parser.add_argument("--request-id", required=True)
    parser.add_argument("--issued-at", required=True, help="Frozen request date-time")
    parser.add_argument(
        "--variant-bundle-ref",
        required=True,
        help="Opaque controlled:// reference to blinded A/B execution bundle",
    )
    parser.add_argument("--output", help="Write JSONL record to this path; stdout if omitted")
    args = parser.parse_args()

    try:
        record = build_request(
            load_json(Path(args.candidate)),
            load_json(Path(args.execution)),
            request_id=args.request_id,
            issued_at=args.issued_at,
            variant_bundle_ref=args.variant_bundle_ref,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    line = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
    if args.output:
        Path(args.output).write_text(line, encoding="utf-8")
    else:
        sys.stdout.write(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
