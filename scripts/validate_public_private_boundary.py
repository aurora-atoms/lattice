#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate public fixture privacy and public/private lifecycle separation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ADOPTION_ORDER = [
    "not_observed",
    "imported",
    "task_scoped",
    "used_once",
    "reused",
    "team_available",
]
ADOPTION_STATUSES = set(ADOPTION_ORDER) | {"deprecated"}
PRIVATE_PATTERNS = {
    "absolute user path": re.compile(r"(?i)(?:/users/|/home/|[a-z]:\\\\users\\\\)"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "secret assignment": re.compile(
        r"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*[\"']?[^\\s\"']+"
    ),
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_no}: expected JSON object")
        records.append(value)
    return records


def validate_adoption_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    status = record.get("downstream_adoption_status")
    simulation = record.get("simulation_status")
    evidence = record.get("evidence_refs")
    human_review = record.get("human_review_ref")
    governance = record.get("governance_approval_ref")
    if status not in ADOPTION_STATUSES:
        errors.append("invalid downstream_adoption_status")
        return errors
    if simulation not in {"synthetic_reference", "real_downstream"}:
        errors.append("invalid simulation_status")
    if not isinstance(evidence, list):
        errors.append("evidence_refs must be an array")
        evidence = []
    if simulation == "synthetic_reference":
        if status != "not_observed":
            errors.append("synthetic reference must remain not_observed")
        if human_review is not None or governance is not None:
            errors.append("synthetic reference cannot claim real human or governance approval")
        return errors
    if status in {"task_scoped", "used_once", "reused", "team_available"} and not human_review:
        errors.append(f"{status} requires accountable human review")
    if status in {"used_once", "reused", "team_available"} and not evidence:
        errors.append(f"{status} requires real evidence")
    if status in {"reused", "team_available"} and len(set(map(str, evidence))) < 2:
        errors.append(f"{status} requires separately addressable later-use evidence")
    if status == "team_available" and not governance:
        errors.append("team_available requires separate governance approval")
    return errors


def validate_transition(previous: str, current: str) -> list[str]:
    if previous not in ADOPTION_STATUSES or current not in ADOPTION_STATUSES:
        return ["invalid adoption transition status"]
    if current == "deprecated":
        return []
    if previous == "deprecated":
        return ["deprecated adoption cannot transition to an active state"]
    expected_index = ADOPTION_ORDER.index(previous) + 1
    if expected_index >= len(ADOPTION_ORDER) or ADOPTION_ORDER[expected_index] != current:
        return [f"adoption transition cannot skip from {previous} to {current}"]
    return []


def fixture_errors(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    for label, pattern in PRIVATE_PATTERNS.items():
        if pattern.search(text):
            errors.append(f"{path}: possible {label}")
    if path.suffix == ".jsonl":
        records = load_jsonl(path)
    elif path.suffix == ".json":
        value = json.loads(text)
        records = value if isinstance(value, list) else [value]
    else:
        return errors
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            continue
        constraints = record.get("constraints", {})
        if not isinstance(constraints, dict) or constraints.get("ip_boundary") != "synthetic":
            continue
        label = f"{path}:{index + 1}"
        lifecycle = {
            "simulation_status": constraints.get("simulation_status"),
            "downstream_adoption_status": constraints.get(
                "downstream_adoption_status"
            ),
            "evidence_refs": [],
            "human_review_ref": None,
            "governance_approval_ref": None,
        }
        for error in validate_adoption_record(lifecycle):
            errors.append(f"{label}: {error}")
        payload = record.get("payload", {})
        if isinstance(payload, dict):
            status = payload.get("downstream_adoption_status")
            if status is not None and status != "not_observed":
                errors.append(f"{label}: synthetic payload adoption must remain not_observed")
            if record.get("type") == "reusable_asset.candidate":
                if payload.get("public_package_status") not in {
                    "draft",
                    "contract_validated",
                    "conformance_validated",
                }:
                    errors.append(f"{label}: invalid synthetic public_package_status")
                if payload.get("activation_mode") != "never_by_default":
                    errors.append(f"{label}: synthetic candidate must remain never_by_default")
            if (
                record.get("type") == "reusable_asset.review"
                and "deliveryyield" in json.dumps(record).lower()
                and payload.get("decision") == "approved"
            ):
                errors.append(f"{label}: DeliveryYield cannot approve asset promotion")
    return errors


def validate_root(root: Path) -> list[str]:
    errors: list[str] = []
    manifest = load_json(root / "registry" / "capability-manifest.json")
    if "downstream_adoption_status" in json.dumps(manifest):
        errors.append("canonical public manifest contains private downstream adoption state")
    fixture_roots = [
        root / "feature-delivery-harness-mvp" / "evals",
        root / "examples",
    ]
    for fixture_root in fixture_roots:
        if not fixture_root.exists():
            continue
        for path in sorted(fixture_root.rglob("*")):
            if path.is_file() and path.suffix in {".json", ".jsonl"}:
                errors.extend(fixture_errors(path))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    try:
        errors = validate_root(root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print("validated public/private fixture and lifecycle boundaries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
