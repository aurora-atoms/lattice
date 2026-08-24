#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate a safety-critical review record and its fail-closed gate semantics."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas/capability/safety-critical-review.v1.schema.json"
DECISION_ORDER = {"pass_candidate": 0, "conditional": 1, "block": 2}
HIGH_SEVERITY = {"S0", "S1"}
PRIVATE_PATTERNS = (
    re.compile(r"(?i)/(?:Users|home)/"),
    re.compile(r"[A-Za-z]:\\(?:Users|workspace|repo)\\", re.IGNORECASE),
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def _all_strings(value: Any) -> list[str]:
    strings: list[str] = []
    if isinstance(value, str):
        strings.append(value)
    elif isinstance(value, dict):
        for nested in value.values():
            strings.extend(_all_strings(nested))
    elif isinstance(value, list):
        for nested in value:
            strings.extend(_all_strings(nested))
    return strings


def schema_errors(record: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(record), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"schema:{location}: {error.message}")
    return errors


def _duplicates(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def _derived_checks(
    record: dict[str, Any], chain: dict[str, Any], requirement: dict[str, Any]
) -> dict[str, bool]:
    enforcement = chain.get("enforcement_points", [])
    runtime = chain.get("runtime_evidence", [])
    tests = chain.get("adversarial_tests", [])
    classification = chain.get("failure_classification", {})
    obligations = record.get("assurance_boundary", {}).get(
        "applicable_external_obligations", []
    )
    unknowns = record.get("evidence", {}).get("unknowns", [])

    high_severity_closed = (
        classification.get("severity") not in HIGH_SEVERITY
        or classification.get("finding_status") == "verified_closed"
    )
    closure_evidenced = (
        classification.get("finding_status") != "verified_closed"
        or classification.get("evidence_status") == "OBSERVED"
    )
    runtime_types = {
        str(item.get("evidence_type")) for item in runtime if isinstance(item, dict)
    }
    technical_enforcement = any(
        item.get("kind") in {"architecture", "code", "interface", "configuration"}
        for item in enforcement
    )
    runtime_is_action_grade = bool(
        runtime_types
        & {
            "enforcement_decision",
            "state_transition",
            "authorization_decision",
            "physical_postcondition",
            "outcome_attribution",
            "reconciliation",
        }
    )

    return {
        "requirement_approved": requirement.get("normalized_requirement", {}).get("status")
        == "approved",
        "invariant_explicit": chain.get("invariant", {}).get("applicability")
        == "applicable",
        "enforcement_verified": bool(enforcement)
        and technical_enforcement
        and all(item.get("verification_status") == "verified" for item in enforcement),
        "runtime_evidence_observed": bool(runtime)
        and runtime_is_action_grade
        and all(item.get("observation_status") == "observed" for item in runtime),
        "adversarial_test_passed": any(
            item.get("level") in {"L3", "L4"} and item.get("result") == "passed"
            for item in tests
        ),
        "no_open_s0_s1": high_severity_closed and closure_evidenced,
        "unknowns_nonblocking": not any(item.get("blocking") is True for item in unknowns),
        "external_obligations_mapped": bool(obligations)
        and all(item.get("applicability") != "pending" for item in obligations),
        "test_execution_safe": bool(tests)
        and record.get("assurance_boundary", {}).get(
            "contract_grants_live_harmful_testing_authority"
        )
        is False
        and all(str(item.get("execution_safety", "")).strip() for item in tests),
    }


def _expected_decision(
    checks: dict[str, bool], chain: dict[str, Any]
) -> tuple[str, list[str]]:
    failures = sorted(key for key, passed in checks.items() if not passed)
    classification = chain.get("failure_classification", {})
    severity = classification.get("severity")
    finding_status = classification.get("finding_status")
    controls = chain.get("release_gate", {}).get("conditional_controls", [])

    if failures:
        return "block", failures
    if severity == "S2" and finding_status != "verified_closed":
        if controls:
            return "conditional", []
        return "block", ["open_s2_missing_conditional_control"]
    return "pass_candidate", []


def semantic_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if record.get("simulation_status") == "synthetic_reference":
        if any(pattern.search(text) for text in _all_strings(record) for pattern in PRIVATE_PATTERNS):
            errors.append("public synthetic review contains a private locator, path, or email")
        if record.get("downstream_adoption_status") != "not_observed":
            errors.append("synthetic review cannot claim downstream adoption")

    requirements = [
        item for item in record.get("requirements", []) if isinstance(item, dict)
    ]
    chains = [item for item in record.get("review_chains", []) if isinstance(item, dict)]
    requirements_by_id = {
        str(item.get("requirement_id")): item for item in requirements if item.get("requirement_id")
    }

    duplicate_requirements = _duplicates(
        [str(item.get("requirement_id")) for item in requirements]
    )
    if duplicate_requirements:
        errors.append("duplicate requirement_id(s): " + ", ".join(duplicate_requirements))
    duplicate_chains = _duplicates([str(item.get("chain_id")) for item in chains])
    if duplicate_chains:
        errors.append("duplicate chain_id(s): " + ", ".join(duplicate_chains))

    nested_ids: list[str] = []
    chain_decisions: dict[str, str] = {}
    for chain in chains:
        chain_id = str(chain.get("chain_id", "<missing>"))
        requirement_id = str(chain.get("requirement_id", ""))
        requirement = requirements_by_id.get(requirement_id)
        if requirement is None:
            errors.append(f"{chain_id}: unknown requirement_id: {requirement_id}")
            continue

        evaluation = requirement.get("evaluation", {})
        normalized = requirement.get("normalized_requirement", {})
        if evaluation.get("verdict") in {"reject", "unknown"} and normalized.get("status") == "approved":
            errors.append(
                f"{chain_id}: rejected or unknown requirement evaluation cannot produce an approved requirement"
            )
        if evaluation.get("verdict") == "accept" and evaluation.get("defects"):
            errors.append(f"{chain_id}: accepted requirement cannot retain listed defects")
        if evaluation.get("verdict") == "amend" and not evaluation.get("defects"):
            errors.append(f"{chain_id}: amended requirement must name at least one defect")

        invariant = chain.get("invariant", {})
        nested_ids.append(str(invariant.get("invariant_id", "")))
        for collection, key in (
            (chain.get("enforcement_points", []), "point_id"),
            (chain.get("runtime_evidence", []), "evidence_id"),
            (chain.get("adversarial_tests", []), "test_id"),
        ):
            nested_ids.extend(
                str(item.get(key, "")) for item in collection if isinstance(item, dict)
            )

        checks = _derived_checks(record, chain, requirement)
        declared_checks = chain.get("release_gate", {}).get("mandatory_checks", {})
        for check, expected in checks.items():
            if declared_checks.get(check) is not expected:
                errors.append(
                    f"{chain_id}: mandatory_checks.{check} must be {str(expected).lower()} from review evidence"
                )

        expected_decision, reasons = _expected_decision(checks, chain)
        declared_decision = chain.get("release_gate", {}).get("recommended_decision")
        chain_decisions[chain_id] = expected_decision
        if declared_decision != expected_decision:
            errors.append(
                f"{chain_id}: recommended_decision must be {expected_decision}, not {declared_decision}"
            )
        declared_reasons = chain.get("release_gate", {}).get("blocking_reasons", [])
        if expected_decision == "block" and not declared_reasons:
            errors.append(f"{chain_id}: blocked chain must state blocking_reasons")
        if expected_decision != "block" and declared_reasons:
            errors.append(f"{chain_id}: non-blocked chain cannot retain blocking_reasons")
        if reasons and not set(reasons).issubset(set(map(str, declared_reasons))):
            errors.append(
                f"{chain_id}: blocking_reasons must include derived reason(s): {', '.join(reasons)}"
            )
        controls = chain.get("release_gate", {}).get("conditional_controls", [])
        if expected_decision == "conditional" and not controls:
            errors.append(f"{chain_id}: conditional decision requires a bounded control")
        if expected_decision == "pass_candidate" and controls:
            errors.append(f"{chain_id}: pass_candidate cannot retain conditional controls")

    duplicate_nested = _duplicates([value for value in nested_ids if value])
    if duplicate_nested:
        errors.append("duplicate invariant/enforcement/evidence/test id(s): " + ", ".join(duplicate_nested))

    if chains and chain_decisions:
        expected_global = max(chain_decisions.values(), key=lambda item: DECISION_ORDER[item])
        declared_global = record.get("review_verdict", {}).get("recommendation")
        if declared_global != expected_global:
            errors.append(
                f"review_verdict.recommendation must be {expected_global}, not {declared_global}"
            )
        expected_blocking = sorted(
            chain_id for chain_id, decision in chain_decisions.items() if decision == "block"
        )
        declared_blocking = sorted(
            map(str, record.get("review_verdict", {}).get("blocking_chain_ids", []))
        )
        if declared_blocking != expected_blocking:
            errors.append("review_verdict.blocking_chain_ids must match blocked review chains")

    return errors


def validate_record(record: dict[str, Any], schema: dict[str, Any] | None = None) -> list[str]:
    active_schema = schema or load_json(SCHEMA_PATH)
    errors = schema_errors(record, active_schema)
    if errors:
        return errors
    return semantic_errors(record)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review", help="Safety-critical review JSON file")
    parser.add_argument("--schema", default=str(SCHEMA_PATH))
    args = parser.parse_args()

    try:
        record = load_json(Path(args.review))
        schema = load_json(Path(args.schema))
        errors = validate_record(record, schema)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print("safety-critical review: valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
