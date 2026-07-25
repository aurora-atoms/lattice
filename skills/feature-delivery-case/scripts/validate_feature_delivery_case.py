#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate lifecycle semantics for a Feature Delivery Case JSON entity."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

COVERAGE_CATEGORIES = {
    "business_rules",
    "system_constraints",
    "similar_cases",
    "negative_knowledge",
    "source_facts",
}
READINESS_RESULTS = {
    "ready",
    "not_ready",
    "blocked",
    "insufficient_evidence",
    "human_decision_required",
}
UNSATISFIED_DEPENDENCY_STATES = {"unknown", "identified", "pending", "failed", "blocked"}
INVALID_ACTIVE_ASSUMPTION_STATES = {"expired", "invalidated", "unsupported"}


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def has_review_condition(record: dict[str, Any]) -> bool:
    review = record.get("review_condition")
    if not isinstance(review, dict):
        return False
    return bool(review.get("review_at") or review.get("event_triggers"))


def validate_case(case: dict[str, Any], now: datetime | None = None) -> list[str]:
    now = now or datetime.now(timezone.utc)
    errors: list[str] = []

    required_top = {
        "case_profile",
        "case_id",
        "revision",
        "title",
        "lifecycle_status",
        "accountable_owner",
        "purpose",
        "boundary",
        "acceptance_criteria",
        "context_coverage",
        "decision_log",
        "assumption_log",
        "dependencies",
        "evidence_ledger",
        "risk_ledger",
        "unresolved_items",
        "artifacts",
        "readiness",
    }
    missing = sorted(required_top - set(case))
    if missing:
        errors.append("missing top-level fields: " + ", ".join(missing))
        return errors

    if case.get("case_profile") != "lifecycle_v1":
        errors.append("case_profile must be lifecycle_v1")
    if not isinstance(case.get("revision"), int) or case["revision"] < 1:
        errors.append("revision must be an integer greater than zero")

    purpose = case.get("purpose")
    if not isinstance(purpose, dict):
        errors.append("purpose must be an object")
    else:
        for key in ("why", "beneficiaries", "expected_change", "success_signals"):
            if not purpose.get(key):
                errors.append(f"purpose.{key} is required")

    boundary = case.get("boundary")
    if not isinstance(boundary, dict):
        errors.append("boundary must be an object")
    else:
        for key in ("feature_boundary", "in_scope", "out_of_scope", "affected_surfaces", "impact_areas", "compatibility_constraints", "non_goals"):
            if key not in boundary:
                errors.append(f"boundary.{key} is required")

    coverage = case.get("context_coverage")
    if not isinstance(coverage, list):
        errors.append("context_coverage must be an array")
    else:
        categories = [item.get("category") for item in coverage if isinstance(item, dict)]
        missing_categories = sorted(COVERAGE_CATEGORIES - set(categories))
        duplicate_categories = sorted({item for item in categories if categories.count(item) > 1})
        if missing_categories:
            errors.append("missing context coverage categories: " + ", ".join(missing_categories))
        if duplicate_categories:
            errors.append("duplicate context coverage categories: " + ", ".join(duplicate_categories))
        for index, item in enumerate(coverage):
            if not isinstance(item, dict):
                errors.append(f"context_coverage[{index}] must be an object")
                continue
            if item.get("status") == "pending":
                errors.append(f"context_coverage[{index}] remains pending")
            if item.get("status") == "found" and not item.get("source_refs"):
                errors.append(f"context_coverage[{index}] found status requires source_refs")

    for index, decision in enumerate(case.get("decision_log", [])):
        if not isinstance(decision, dict):
            errors.append(f"decision_log[{index}] must be an object")
            continue
        if decision.get("status") in {"active", "pending"} and not has_review_condition(decision):
            errors.append(f"decision {decision.get('id', index)} lacks a review condition")
        if not decision.get("rationale"):
            errors.append(f"decision {decision.get('id', index)} lacks rationale")

    expired_assumption_ids: set[str] = set()
    for index, assumption in enumerate(case.get("assumption_log", [])):
        if not isinstance(assumption, dict):
            errors.append(f"assumption_log[{index}] must be an object")
            continue
        assumption_id = str(assumption.get("id", index))
        status = assumption.get("status")
        expires_at = parse_time(assumption.get("expires_at"))
        if status == "active" and not has_review_condition(assumption):
            errors.append(f"assumption {assumption_id} lacks a review condition")
        if status == "active" and expires_at is not None and expires_at <= now:
            errors.append(f"assumption {assumption_id} is active but expired")
            expired_assumption_ids.add(assumption_id)
        if status in INVALID_ACTIVE_ASSUMPTION_STATES:
            expired_assumption_ids.add(assumption_id)
        if not assumption.get("impact_if_false"):
            errors.append(f"assumption {assumption_id} lacks impact_if_false")

    blocking_dependency_ids: set[str] = set()
    for index, dependency in enumerate(case.get("dependencies", [])):
        if not isinstance(dependency, dict):
            errors.append(f"dependencies[{index}] must be an object")
            continue
        dependency_id = str(dependency.get("id", index))
        if dependency.get("blocking") and dependency.get("state") in UNSATISFIED_DEPENDENCY_STATES:
            blocking_dependency_ids.add(dependency_id)
        if dependency.get("kind") in {"shadow", "stakeholder", "decision"} and not dependency.get("owner"):
            errors.append(f"dependency {dependency_id} requires an owner")

    evidence_ids: set[str] = set()
    for index, evidence in enumerate(case.get("evidence_ledger", [])):
        if not isinstance(evidence, dict):
            errors.append(f"evidence_ledger[{index}] must be an object")
            continue
        evidence_id = str(evidence.get("id", index))
        evidence_ids.add(evidence_id)
        if not evidence.get("source_ref"):
            errors.append(f"evidence {evidence_id} lacks source_ref")
        if not evidence.get("supports_refs"):
            errors.append(f"evidence {evidence_id} does not link to a claim, criterion, decision, or risk")

    for index, risk in enumerate(case.get("risk_ledger", [])):
        if not isinstance(risk, dict):
            errors.append(f"risk_ledger[{index}] must be an object")
            continue
        risk_id = str(risk.get("id", index))
        if risk.get("kind") == "compound" and len(risk.get("component_refs", [])) < 2:
            errors.append(f"compound risk {risk_id} must link at least two components")
        if risk.get("status") in {"open", "controlled", "accepted"} and not risk.get("review_triggers"):
            errors.append(f"risk {risk_id} lacks review triggers")

    blocking_unresolved_ids: set[str] = set()
    unresolved_expired_assumption_refs: set[str] = set()
    for index, item in enumerate(case.get("unresolved_items", [])):
        if not isinstance(item, dict):
            errors.append(f"unresolved_items[{index}] must be an object")
            continue
        item_id = str(item.get("id", index))
        if item.get("blocking") and item.get("status") == "open":
            blocking_unresolved_ids.add(item_id)
        if item.get("kind") == "expired_assumption" and item.get("status") == "open":
            unresolved_expired_assumption_refs.add(item_id)
        if item.get("status") == "open" and not item.get("owner"):
            errors.append(f"unresolved item {item_id} lacks an owner")

    artifact_ids: set[str] = set()
    for index, artifact in enumerate(case.get("artifacts", [])):
        if not isinstance(artifact, dict):
            errors.append(f"artifacts[{index}] must be an object")
            continue
        artifact_id = str(artifact.get("id", index))
        artifact_ids.add(artifact_id)
        if artifact.get("case_revision") != case.get("revision"):
            errors.append(f"artifact {artifact_id} does not match case revision")
        if not artifact.get("authority_note"):
            errors.append(f"artifact {artifact_id} lacks authority_note")

    readiness = case.get("readiness")
    if not isinstance(readiness, dict):
        errors.append("readiness must be an object")
        return errors

    result = readiness.get("result")
    if result not in READINESS_RESULTS:
        errors.append("readiness.result is invalid")
    expires_at = parse_time(readiness.get("expires_at"))
    if result == "ready" and expires_at is None and not readiness.get("review_triggers"):
        errors.append("ready result requires expires_at or review_triggers")
    if result == "ready" and expires_at is not None and expires_at <= now:
        errors.append("ready result is expired")
    if result == "ready" and blocking_dependency_ids:
        errors.append("ready result conflicts with blocking dependencies: " + ", ".join(sorted(blocking_dependency_ids)))
    if result == "ready" and blocking_unresolved_ids:
        errors.append("ready result conflicts with blocking unresolved items: " + ", ".join(sorted(blocking_unresolved_ids)))
    if result == "ready" and expired_assumption_ids:
        errors.append("ready result conflicts with expired or invalid assumptions: " + ", ".join(sorted(expired_assumption_ids)))
    if result == "ready" and not evidence_ids:
        errors.append("ready result requires evidence")
    if result == "ready" and not artifact_ids:
        errors.append("ready result requires a shareable artifact")
    if result == "ready":
        failing = [item.get("id", "unknown") for item in readiness.get("criteria", []) if isinstance(item, dict) and item.get("status") != "pass"]
        if failing:
            errors.append("ready result has non-passing criteria: " + ", ".join(map(str, failing)))
    if not readiness.get("authority_note"):
        errors.append("readiness.authority_note is required")
    if "approve" in str(readiness.get("authority_note", "")).lower():
        errors.append("readiness.authority_note must not claim approval authority")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_json", help="Feature Delivery Case lifecycle JSON file")
    parser.add_argument("--now", help="Optional ISO-8601 validation time for deterministic tests")
    args = parser.parse_args()

    path = Path(args.case_json)
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2
    try:
        case = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON: {exc}", file=sys.stderr)
        return 2
    if not isinstance(case, dict):
        print("error: case must be a JSON object", file=sys.stderr)
        return 2

    now = parse_time(args.now) if args.now else None
    if args.now and now is None:
        print("error: --now must be ISO-8601", file=sys.stderr)
        return 2

    errors = validate_case(case, now)
    if errors:
        for error in errors:
            print(json.dumps({"code": "INVALID_FEATURE_DELIVERY_CASE", "message": error}, sort_keys=True), file=sys.stderr)
        return 1
    print("validated feature delivery case lifecycle_v1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
