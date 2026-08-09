#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate cross-file invariants for a public Evidence Wayfinding replay case.

Portable Case Pack, Attention Admission, and Outcome Receipt each retain their
own structural/semantic validators. This validator only composes those contracts
and checks the remaining case-spine projection lineage.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from validate_attention_admission import validate_admission
from validate_outcome_receipt import validate_outcome

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


def collect_evidence_refs(value: Any) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            if key == "evidence_refs":
                refs.update(as_string_set(nested))
            else:
                refs.update(collect_evidence_refs(nested))
    elif isinstance(value, list):
        for nested in value:
            refs.update(collect_evidence_refs(nested))
    return refs


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

    for name in ["decision_card", "verification_receipt"]:
        unknown = collect_evidence_refs(records[name]) - evidence_ids
        if unknown:
            errors.append(
                f"{REQUIRED_FILES[name]} references unknown evidence: "
                + ", ".join(sorted(unknown))
            )

    errors.extend(validate_admission(admission, pack, contract))
    if admission.get("status") != "READY":
        errors.append("Case 0 replay requires READY admission")

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

    errors.extend(validate_outcome(outcome, pack))
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
