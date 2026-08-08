#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate Lattice Portable Case Pack v1 structural and evidence-reference invariants."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

CONTRACT = "lat.portable_case_pack.v1"
MISSION = "lat.goal.verified-decision-yield.v1"
CLAIM_BUCKETS = {"observed", "derived", "judged", "unknown"}
CLASSIFICATIONS = {"public", "private", "restricted"}
FORBIDDEN_KEYS = {"chain_of_thought", "reasoning_transcript", "full_reasoning"}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def collect_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.add(str(key).lower())
            keys.update(collect_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            keys.update(collect_keys(nested))
    return keys


def _refs(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def validate_pack(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if record.get("contract") != CONTRACT:
        errors.append(f"contract must be {CONTRACT}")
    if record.get("mission_anchor_ref") != MISSION:
        errors.append(f"mission_anchor_ref must be {MISSION}")
    if record.get("data_classification") not in CLASSIFICATIONS:
        errors.append("data_classification must be public, private, or restricted")

    forbidden = collect_keys(record) & FORBIDDEN_KEYS
    if forbidden:
        errors.append(
            "authoritative handoff contains forbidden reasoning transcript field(s): "
            + ", ".join(sorted(forbidden))
        )

    scope = record.get("scope")
    if not isinstance(scope, dict) or not isinstance(scope.get("in"), list) or not scope.get("in"):
        errors.append("scope.in must be a non-empty list")
    if not isinstance(scope, dict) or not isinstance(scope.get("out"), list):
        errors.append("scope.out must be a list")

    claims = record.get("claims")
    if not isinstance(claims, dict) or set(claims) != CLAIM_BUCKETS:
        errors.append("claims must contain exactly observed, derived, judged, and unknown")
        claims = {}

    evidence = record.get("evidence_refs")
    if not isinstance(evidence, list) or not evidence:
        errors.append("evidence_refs must be a non-empty list")
        evidence = []
    evidence_ids: set[str] = set()
    for index, item in enumerate(evidence):
        if not isinstance(item, dict):
            errors.append(f"evidence_refs[{index}] must be an object")
            continue
        evidence_id = str(item.get("id", ""))
        if not evidence_id:
            errors.append(f"evidence_refs[{index}].id is required")
        elif evidence_id in evidence_ids:
            errors.append(f"duplicate evidence id: {evidence_id}")
        evidence_ids.add(evidence_id)
        access = item.get("access")
        if access not in CLASSIFICATIONS:
            errors.append(f"evidence_refs[{index}].access is invalid")
        if record.get("data_classification") == "public" and access != "public":
            errors.append("public packs cannot reference private or restricted evidence")

    claim_ids: set[str] = set()
    for bucket_name, bucket in claims.items():
        if not isinstance(bucket, list):
            errors.append(f"claims.{bucket_name} must be a list")
            continue
        for index, claim in enumerate(bucket):
            label = f"claims.{bucket_name}[{index}]"
            if not isinstance(claim, dict):
                errors.append(f"{label} must be an object")
                continue
            claim_id = str(claim.get("claim_id", ""))
            if not claim_id:
                errors.append(f"{label}.claim_id is required")
            elif claim_id in claim_ids:
                errors.append(f"duplicate claim id: {claim_id}")
            claim_ids.add(claim_id)
            refs = _refs(claim.get("evidence_refs"))
            if bucket_name == "observed" and not refs:
                errors.append(f"{label} observed claims require evidence_refs")
            for ref in refs:
                if ref not in evidence_ids:
                    errors.append(f"{label} references unknown evidence: {ref}")

    conflicts = record.get("conflicts", [])
    if not isinstance(conflicts, list):
        errors.append("conflicts must be a list")
        conflicts = []
    for index, conflict in enumerate(conflicts):
        if not isinstance(conflict, dict):
            errors.append(f"conflicts[{index}] must be an object")
            continue
        for ref in _refs(conflict.get("claim_refs")):
            if ref not in claim_ids:
                errors.append(f"conflicts[{index}] references unknown claim: {ref}")
        for ref in _refs(conflict.get("evidence_refs")):
            if ref not in evidence_ids:
                errors.append(f"conflicts[{index}] references unknown evidence: {ref}")

    for field in ("strongest_counterevidence", "rejected_directions"):
        value = record.get(field, [])
        if not isinstance(value, list):
            errors.append(f"{field} must be a list")
            continue
        for index, item in enumerate(value):
            if not isinstance(item, dict):
                errors.append(f"{field}[{index}] must be an object")
                continue
            for ref in _refs(item.get("evidence_refs")):
                if ref not in evidence_ids:
                    errors.append(f"{field}[{index}] references unknown evidence: {ref}")

    for field in ("decision_requested", "next_tool_task", "falsification"):
        if not isinstance(record.get(field), str) or not str(record[field]).strip():
            errors.append(f"{field} must be a non-empty string")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack", help="Portable Case Pack JSON path")
    args = parser.parse_args()
    path = Path(args.pack)
    try:
        record = load_json(path)
        errors = validate_pack(record)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"validated portable case pack: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
