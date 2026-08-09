#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate Attention Admission v1 against its Case Contract and Portable Case Pack.

The JSON Schema owns structure. This validator owns cross-file semantics and the
non-negotiable admission rule: READY requires every mandatory invariant to pass.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

CONTRACT = "lat.attention_admission_receipt.v1"
MISSION = "lat.goal.verified-decision-yield.v1"
CHECKS = (
    "M1_target",
    "M2_evidence",
    "M3_counterevidence",
    "M4_risk_authority",
    "M5_delivery",
)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def _refs(value: Any) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {str(item) for item in value}


def _collect_evidence_refs(value: Any) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            if key == "evidence_refs":
                refs.update(_refs(nested))
            else:
                refs.update(_collect_evidence_refs(nested))
    elif isinstance(value, list):
        for nested in value:
            refs.update(_collect_evidence_refs(nested))
    return refs


def _pack_evidence_ids(pack: dict[str, Any]) -> set[str]:
    return {
        str(item.get("id"))
        for item in pack.get("evidence_refs", [])
        if isinstance(item, dict) and item.get("id")
    }


def _case_target_ready(case_contract: dict[str, Any]) -> bool:
    authority = case_contract.get("authority")
    scope = case_contract.get("scope")
    return all(
        [
            isinstance(case_contract.get("decision_requested"), str)
            and bool(case_contract["decision_requested"].strip()),
            isinstance(authority, dict)
            and isinstance(authority.get("final_decision_owner"), str)
            and bool(authority["final_decision_owner"].strip()),
            isinstance(scope, dict)
            and isinstance(scope.get("in"), list)
            and bool(scope["in"])
            and isinstance(scope.get("out"), list),
            isinstance(case_contract.get("evidence_cutoff"), str)
            and bool(case_contract["evidence_cutoff"].strip()),
            isinstance(case_contract.get("acceptance"), list)
            and bool(case_contract["acceptance"]),
            isinstance(case_contract.get("acceptance_observer"), str)
            and bool(case_contract["acceptance_observer"].strip()),
        ]
    )


def _pack_evidence_ready(pack: dict[str, Any]) -> bool:
    evidence_ids = _pack_evidence_ids(pack)
    claims = pack.get("claims")
    if not evidence_ids or not isinstance(claims, dict):
        return False
    for bucket_name in ("observed", "derived", "judged"):
        bucket = claims.get(bucket_name)
        if not isinstance(bucket, list):
            return False
        for claim in bucket:
            if not isinstance(claim, dict):
                return False
            refs = _refs(claim.get("evidence_refs"))
            if not refs or not refs.issubset(evidence_ids):
                return False
    return True


def _counterevidence_ready(pack: dict[str, Any]) -> bool:
    counterevidence = pack.get("strongest_counterevidence")
    if isinstance(counterevidence, list) and bool(counterevidence):
        return True
    source_gaps = pack.get("source_gaps")
    return isinstance(source_gaps, list) and bool(source_gaps)


def _risk_authority_status(
    case_contract: dict[str, Any], receipt: dict[str, Any]
) -> str:
    authority = case_contract.get("authority")
    if not isinstance(authority, dict) or not str(
        authority.get("final_decision_owner", "")
    ).strip():
        return "fail"
    reversibility = receipt.get("reversibility")
    if not isinstance(reversibility, dict):
        return "fail"
    if reversibility.get("level") == "unknown":
        return "escalate"
    return "pass"


def _delivery_ready(pack: dict[str, Any], receipt: dict[str, Any]) -> bool:
    required_output = pack.get("required_output")
    delivery = receipt.get("delivery_contract")
    if not isinstance(required_output, dict) or not isinstance(delivery, dict):
        return False
    pack_contract = str(required_output.get("contract", "")).strip()
    return all(
        [
            bool(pack_contract),
            delivery.get("required_output_contract") == pack_contract,
            bool(str(delivery.get("verifier", "")).strip()),
            bool(str(delivery.get("expected_state_change", "")).strip()),
        ]
    )


def validate_admission(
    receipt: dict[str, Any],
    pack: dict[str, Any],
    case_contract: dict[str, Any],
) -> list[str]:
    errors: list[str] = []

    if receipt.get("contract") != CONTRACT:
        errors.append(f"contract must be {CONTRACT}")
    if receipt.get("mission_anchor_ref") != MISSION:
        errors.append(f"mission_anchor_ref must be {MISSION}")

    case_ids = {
        str(receipt.get("case_id", "")),
        str(pack.get("case_id", "")),
        str(case_contract.get("case_id", "")),
    }
    if "" in case_ids or len(case_ids) != 1:
        errors.append("receipt, Portable Case Pack, and Case Contract must share one case_id")

    if pack.get("mission_anchor_ref") != MISSION:
        errors.append("Portable Case Pack mission anchor does not match admission mission")
    if case_contract.get("mission_anchor_ref") != MISSION:
        errors.append("Case Contract mission anchor does not match admission mission")

    evidence_ids = _pack_evidence_ids(pack)
    unknown_refs = _collect_evidence_refs(receipt) - evidence_ids
    if unknown_refs:
        errors.append(
            "attention admission references unknown Portable Case Pack evidence: "
            + ", ".join(sorted(unknown_refs))
        )

    checks = receipt.get("mandatory_checks")
    if not isinstance(checks, dict):
        errors.append("mandatory_checks must be an object")
        return errors

    expected = {
        "M1_target": "pass" if _case_target_ready(case_contract) else "fail",
        "M2_evidence": "pass" if _pack_evidence_ready(pack) else "fail",
        "M3_counterevidence": "pass" if _counterevidence_ready(pack) else "fail",
        "M4_risk_authority": _risk_authority_status(case_contract, receipt),
        "M5_delivery": "pass" if _delivery_ready(pack, receipt) else "fail",
    }

    for check_id in CHECKS:
        check = checks.get(check_id)
        if not isinstance(check, dict):
            errors.append(f"missing mandatory admission check: {check_id}")
            continue
        actual = check.get("status")
        if actual != expected[check_id]:
            errors.append(
                f"{check_id} status must be {expected[check_id]} from source contracts, got {actual}"
            )

    if "escalate" in expected.values():
        expected_status = "ESCALATE"
    elif "fail" in expected.values():
        expected_status = "BLOCKED"
    else:
        expected_status = "READY"

    if receipt.get("status") != expected_status:
        errors.append(
            f"admission status must be {expected_status}; mandatory checks cannot be waived"
        )

    missing_actions = receipt.get("missing_actions")
    if not isinstance(missing_actions, list):
        errors.append("missing_actions must be a list")
        missing_actions = []
    action_ids = {
        str(item.get("check_id"))
        for item in missing_actions
        if isinstance(item, dict) and item.get("check_id")
    }
    non_pass = {check_id for check_id, status in expected.items() if status != "pass"}
    if expected_status == "READY" and missing_actions:
        errors.append("READY admission must not contain missing_actions")
    if expected_status != "READY" and not non_pass.issubset(action_ids):
        missing = non_pass - action_ids
        errors.append(
            "non-READY admission requires one bounded action for every failed/escalated check: "
            + ", ".join(sorted(missing))
        )

    if receipt.get("status") == "READY" and receipt.get("reversibility", {}).get("level") == "unknown":
        errors.append("READY admission cannot hide unknown reversibility")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", help="Attention Admission Receipt JSON path")
    parser.add_argument("pack", help="Portable Case Pack JSON path")
    parser.add_argument("case_contract", help="Case Contract JSON path")
    args = parser.parse_args()

    try:
        receipt = load_json(Path(args.receipt))
        pack = load_json(Path(args.pack))
        case_contract = load_json(Path(args.case_contract))
        errors = validate_admission(receipt, pack, case_contract)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"validated attention admission receipt: {args.receipt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
