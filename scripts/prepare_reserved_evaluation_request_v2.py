#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Prepare a v2 reserved-evaluation request bound to one blinded bundle digest.

The coordinator supplies the request nonce and either a precomputed SHA-256 digest
or a local blinded-bundle path. This script never receives the reserved oracle,
raw private evidence, incumbent/challenger mapping, or a governed verdict.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

MISSION = "lat.goal.verified-decision-yield.v1"
SCHEMA_ID = "lat.reserved_evaluation_handoff.v2"
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
NONCE_RE = re.compile(r"^[A-Za-z0-9_-]{22,128}$")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def parse_time(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"invalid date-time: {value}") from exc


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


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
    expires_at: str,
    request_nonce: str,
    variant_bundle_ref: str,
    variant_bundle_digest: str,
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
    if not SHA256_RE.fullmatch(variant_bundle_digest):
        raise ValueError("variant_bundle_digest must be sha256:<64 lowercase hex>")
    if not NONCE_RE.fullmatch(request_nonce):
        raise ValueError("request_nonce must be 22-128 URL-safe characters")

    issued = parse_time(issued_at)
    expires = parse_time(expires_at)
    if expires <= issued:
        raise ValueError("expires_at must be after issued_at")

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
            "expires_at": expires_at,
            "request_nonce": request_nonce,
            "evaluator_version": plan.get("evaluator_version"),
            "primary_metric": plan.get("primary_metric"),
            "protected_metrics": list(plan.get("protected_metrics", [])),
            "variant_bundle_ref": variant_bundle_ref,
            "variant_bundle_digest": variant_bundle_digest,
            "variant_labels": ["A", "B"],
            "requested_outputs": [
                "anonymous_variant_outcomes",
                "comparison",
                "protected_metrics",
                "attestation_digest",
                "attestation_signature",
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
    parser.add_argument("--expires-at", required=True, help="Request expiry date-time")
    parser.add_argument("--request-nonce", required=True, help="Unique 22-128 character nonce")
    parser.add_argument(
        "--variant-bundle-ref",
        required=True,
        help="Opaque controlled:// reference to blinded A/B execution bundle",
    )
    digest_group = parser.add_mutually_exclusive_group(required=True)
    digest_group.add_argument(
        "--variant-bundle-digest",
        help="Precomputed sha256:<64 lowercase hex> for the exact blinded bundle bytes",
    )
    digest_group.add_argument(
        "--variant-bundle-path",
        help="Local blinded-bundle file whose exact bytes are SHA-256 hashed",
    )
    parser.add_argument("--output", help="Write JSONL record to this path; stdout if omitted")
    args = parser.parse_args()

    try:
        bundle_digest = (
            args.variant_bundle_digest
            if args.variant_bundle_digest
            else sha256_file(Path(args.variant_bundle_path))
        )
        record = build_request(
            load_json(Path(args.candidate)),
            load_json(Path(args.execution)),
            request_id=args.request_id,
            issued_at=args.issued_at,
            expires_at=args.expires_at,
            request_nonce=args.request_nonce,
            variant_bundle_ref=args.variant_bundle_ref,
            variant_bundle_digest=bundle_digest,
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
