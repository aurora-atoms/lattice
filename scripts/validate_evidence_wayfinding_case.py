#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate cross-file invariants for a public Evidence Wayfinding replay case.

This validator intentionally does not replace the Portable Case Pack JSON Schema
or semantic validator. It validates the case spine: identity, admission,
Decision Card projection, verification evidence, and observed outcome lineage.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_FILES = {
    "case_contract": "case-contract.json",
    "portable_case_pack": "portable-case-pack.json",
    "admission_receipt": "admission-receipt.json",
    "decision_card": "decision-card.json",
    "verification_receipt": "verification-receipt.json",
    "outcome_receipt": "outcome-receipt.json",
}

PUBLIC_MARKERS = {
    "simulation_status": "synthetic_reference",
    "downstream_adoption_status": "not_observed",
    "data_classification": "public",
}

MANDATORY_ADMISSION_CHECKS = {
    "bounded_decision",
    "evidence",
    "counterevidence",
    "authority",
    "delivery_state_change",
}

FORBIDDEN_KEYS = {
    "chain_of_thought",
    "reasoning_transcript",
    "full_reasoning",
    "full_reasoning_transcript",
}


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


def as_string_set(value: Any) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {str(item) for item in value}


def validate_case(case_dir: Path) -> list[str]:
    errors: list[str] = []
    records: dict[str, dict[str, Any]] = {}

    for name, filename in REQUIRED_FILES.items():
        path = case_dir / filename
        if not path.exists():
            errors.append(f"missing required case file: {filename}")
            continue
        try:
            records[name] = load_json(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(str(exc))

    if errors:
        return errors

    case_ids = {str(record.get("case_id", "")) for record in records.values()}
    if "" in case_ids or len(case_ids) != 1:
        errors.append("all case files must carry the same non-empty case_id")

    for name, record in records.items():
        forbidden = collect_keys(record) & FORBIDDEN_KEYS
        if forbidden:
            errors.append(
                f"{REQUIRED_FILES[name]} contains forbidden reasoning field(s): "
                + ", ".join(sorted(forbidden))
            )
        if name == "portable_case_pack":
            if record.get("data_classification") != "public":
                errors.append("portable-case-pack.json must be public in the public replay fixture")
            continue
        for field, expected in PUBLIC_MARKERS.items():
            if record.get(field) != expected:
                errors.append(f"{REQUIRED_FILES[name]}.{field} must be {expected}")

    contract = records["case_contract"]
    pack = records["portable_case_pack"]
    admission = records["admission_receipt"]
    card = records["decision_card"]
    verification = records["verification_receipt"]
    outcome = records["outcome_receipt"]

    if contract.get("mission_anchor_ref") != "lat.goal.verified-decision-yield.v1":
        errors.append("case-contract.json must use the Verified Decision Yield mission anchor")
    if contract.get("value_path") != "current_product_delivery":
        errors.append("Case 0 must remain bound to current_product_delivery")

    decision = str(contract.get("decision_requested", ""))
    if not decision:
        errors.append("case-contract.json decision_requested is required")
    for filename, value in [
        ("portable-case-pack.json", pack.get("decision_requested")),
        ("decision-card.json", card.get("decision_requested")),
    ]:
        if value != decision:
            errors.append(f"{filename} decision_requested must match case-contract.json")

    evidence = pack.get("evidence_refs", [])
    if not isinstance(evidence, list):
        evidence = []
    evidence_ids = {
        str(item.get("id"))
        for item in evidence
        if isinstance(item, dict) and item.get("id")
    }
    if not evidence_ids:
        errors.append("portable-case-pack.json must expose evidence ids")

    for name in ["admission_receipt", "decision_card", "verification_receipt", "outcome_receipt"]:
        record = records[name]
        refs = as_string_set(record.get("evidence_refs"))
        unknown = refs - evidence_ids
        if unknown:
            errors.append(
                f"{REQUIRED_FILES[name]} references unknown evidence: "
                + ", ".join(sorted(unknown))
            )

    if admission.get("status") != "READY":
        errors.append("Case 0 admission status must be READY")
    checks = admission.get("mandatory_checks", [])
    if not isinstance(checks, list):
        checks = []
        errors.append("admission-receipt.json mandatory_checks must be a list")
    seen_checks: set[str] = set()
    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            errors.append(f"admission-receipt.json mandatory_checks[{index}] must be an object")
            continue
        check_id = str(check.get("id", ""))
        if check_id in seen_checks:
            errors.append(f"duplicate admission check: {check_id}")
        seen_checks.add(check_id)
        if check.get("status") != "pass":
            errors.append(f"READY admission cannot contain non-pass check: {check_id}")
        unknown = as_string_set(check.get("evidence_refs")) - evidence_ids
        if unknown:
            errors.append(
                f"admission check {check_id} references unknown evidence: "
                + ", ".join(sorted(unknown))
            )
    missing_checks = MANDATORY_ADMISSION_CHECKS - seen_checks
    if missing_checks:
        errors.append(
            "admission-receipt.json missing mandatory checks: "
            + ", ".join(sorted(missing_checks))
        )

    if card.get("projection_of") != "portable-case-pack.json":
        errors.append("decision-card.json must remain a projection of portable-case-pack.json")
    options = card.get("options", [])
    if not isinstance(options, list) or not 2 <= len(options) <= 4:
        errors.append("decision-card.json must contain two to four options")
        options = []
    option_ids = {
        str(option.get("option_id"))
        for option in options
        if isinstance(option, dict) and option.get("option_id")
    }
    recommendation = card.get("recommendation", {})
    recommended_option = (
        str(recommendation.get("option_id", ""))
        if isinstance(recommendation, dict)
        else ""
    )
    if recommended_option not in option_ids:
        errors.append("decision-card.json recommendation must name a defined option")
    if not str(card.get("strongest_counterevidence", "")).strip():
        errors.append("decision-card.json strongest_counterevidence is required")
    unknowns = card.get("unknowns")
    if not isinstance(unknowns, list) or not unknowns:
        errors.append("decision-card.json must preserve at least one bounded unknown")

    if verification.get("verdict") != "pass_for_case_target":
        errors.append("verification-receipt.json verdict must be pass_for_case_target")
    verification_checks = verification.get("checks", [])
    if not isinstance(verification_checks, list) or not verification_checks:
        errors.append("verification-receipt.json checks must be non-empty")
    else:
        for index, check in enumerate(verification_checks):
            if not isinstance(check, dict) or check.get("status") != "pass":
                errors.append(
                    f"verification-receipt.json checks[{index}] must record a passing check"
                )

    decision_record = outcome.get("decision", {})
    selected_option = (
        str(decision_record.get("selected_option", ""))
        if isinstance(decision_record, dict)
        else ""
    )
    if selected_option not in option_ids:
        errors.append("outcome-receipt.json selected_option must name a Decision Card option")
    if outcome.get("delivery_state_changed") is not True:
        errors.append("Case 0 outcome must record an observed delivery state change")
    if outcome.get("state_before") == outcome.get("state_after"):
        errors.append("outcome-receipt.json state_before and state_after must differ")
    if not str(outcome.get("earliest_failure_point", "")).strip():
        errors.append("outcome-receipt.json earliest_failure_point is required")

    candidate = outcome.get("failure_point_candidate", {})
    if isinstance(candidate, dict) and candidate.get("promotion_authority") != "none_from_this_case":
        errors.append("Case 0 must not grant promotion authority from a single replay case")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_dir", help="Evidence Wayfinding case directory")
    args = parser.parse_args()
    case_dir = Path(args.case_dir)
    try:
        errors = validate_case(case_dir)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"validated Evidence Wayfinding case spine: {case_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
