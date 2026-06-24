#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Author deterministic delivery.verdict records from bounded FDH evidence."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from fdh_lib import list_value, read_jsonl, records_by_type, stable_json, validate_records, write_text_lf


VERDICT_ORDER = ["usable", "requires_human_review", "insufficient_evidence", "not_user_usable", "blocked"]


def acceptance_id(item: Any) -> str | None:
    if isinstance(item, dict):
        value = item.get("id") or item.get("acceptance_id")
        return str(value) if value else None
    if isinstance(item, str) and item.strip():
        return item.strip()
    return None


def is_manual_command(command: dict[str, Any]) -> bool:
    purpose = str(command.get("purpose", "")).lower()
    return bool(command.get("manual_steps")) or "manual" in purpose or "user acceptance" in purpose


def command_results(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for record in records_by_type(records, "validation.result"):
        command_id = str(record.get("payload", {}).get("command_id", ""))
        if command_id:
            result[command_id] = record
    return result


def summarize_acceptance(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    features = records_by_type(records, "feature_delivery_case")
    feature_payload = features[0].get("payload", {}) if features else {}
    ids = [item_id for item in list_value(feature_payload.get("acceptance_criteria")) if (item_id := acceptance_id(item))]
    validation_status: dict[str, set[str]] = {item_id: set() for item_id in ids}
    delivery_status: dict[str, set[str]] = {item_id: set() for item_id in ids}
    for record in records_by_type(records, "validation.result"):
        status = str(record.get("payload", {}).get("status", "not_run"))
        for item_id in list_value(record.get("payload", {}).get("target_acceptance_ids")):
            validation_status.setdefault(str(item_id), set()).add(status)
    for record in records_by_type(records, "delivery.evidence"):
        for result in list_value(record.get("payload", {}).get("acceptance_results")):
            if isinstance(result, dict) and result.get("acceptance_id"):
                delivery_status.setdefault(str(result["acceptance_id"]), set()).add(str(result.get("status", "unknown")))
    return [
        {
            "acceptance_id": item_id,
            "validation_status": sorted(validation_status.get(item_id, set())),
            "delivery_status": sorted(delivery_status.get(item_id, set())),
        }
        for item_id in sorted(set(ids) | set(validation_status) | set(delivery_status))
    ]


def author_verdict(records: list[dict[str, Any]]) -> dict[str, Any]:
    features = records_by_type(records, "feature_delivery_case")
    if not features:
        raise ValueError("feature_delivery_case record is required")
    feature = features[0]
    case_id = str(feature["scope"]["feature_delivery_case_id"])
    tasks = records_by_type(records, "task.packet")
    validations = records_by_type(records, "validation.result")
    delivery = records_by_type(records, "delivery.evidence")
    command_by_id = command_results(records)
    conflict_codes: set[str] = set()
    limitations: set[str] = set()
    unresolved_risks = set(str(item) for item in list_value(feature.get("payload", {}).get("risks")))

    has_validation_pass = any(record.get("payload", {}).get("status") == "pass" for record in validations)
    has_acceptance_fail = False
    has_blocked_dependency = False

    for record in validations:
        payload = record.get("payload", {})
        failure_codes = set(str(item) for item in list_value(payload.get("failure_codes")))
        if payload.get("blocking") and ("BLOCKED_DEPENDENCY" in failure_codes or payload.get("status") == "not_run"):
            has_blocked_dependency = True
            conflict_codes.add("BLOCKED_DEPENDENCY")
            limitations.add(str(payload.get("remediation_hint") or "Blocking dependency prevents validation."))
        if payload.get("status") == "fail":
            has_acceptance_fail = True

    for record in delivery:
        payload = record.get("payload", {})
        limitations.update(str(item) for item in list_value(payload.get("limitations")))
        if payload.get("user_usable_status") == "blocked":
            has_blocked_dependency = True
            conflict_codes.add("BLOCKED_DEPENDENCY")
        if payload.get("user_usable_status") == "not_user_usable":
            has_acceptance_fail = True
        for result in list_value(payload.get("acceptance_results")):
            if isinstance(result, dict) and str(result.get("status")) == "fail":
                has_acceptance_fail = True

    if has_validation_pass and has_acceptance_fail:
        conflict_codes.add("TESTS_PASS_ACCEPTANCE_FAIL")
        limitations.add("Passing validation evidence does not override failed acceptance or usability evidence.")

    for task in tasks:
        for command in list_value(task.get("payload", {}).get("validation_commands")):
            if isinstance(command, dict) and is_manual_command(command):
                command_id = str(command.get("id", ""))
                result = command_by_id.get(command_id)
                if result is None or result.get("payload", {}).get("status") in {"not_run", "warn"}:
                    conflict_codes.add("MISSING_MANUAL_ACCEPTANCE")
                    limitations.add(f"Manual acceptance command {command_id or 'unknown'} has no passing validation.result.")

    if has_blocked_dependency:
        verdict = "blocked"
        reason = "A blocking dependency prevents delivery verification."
    elif has_acceptance_fail:
        verdict = "not_user_usable"
        reason = "Acceptance or user-usability evidence failed."
    elif "MISSING_MANUAL_ACCEPTANCE" in conflict_codes or not delivery:
        verdict = "insufficient_evidence"
        reason = "Required delivery evidence or manual acceptance evidence is missing."
    elif any(record.get("payload", {}).get("user_usable_status") == "requires_human_review" for record in delivery):
        verdict = "requires_human_review"
        reason = "Delivery evidence requires human review."
    elif delivery and all(record.get("payload", {}).get("user_usable_status") == "usable" for record in delivery):
        verdict = "usable"
        reason = "Delivery evidence supports the user-usable outcome."
    else:
        verdict = "insufficient_evidence"
        reason = "Delivery evidence is inconclusive."

    return {
        "type": "delivery.verdict",
        "id": f"verdict_{case_id}",
        "schema": "lat.delivery.verdict.v1",
        "source": "author_delivery_verdict",
        "target": "token-economics-dossier-generator",
        "scope": {"project_id": "lattice", "feature_delivery_case_id": case_id, "module_id": "verifier"},
        "payload": {
            "feature_delivery_case_id": case_id,
            "verdict": verdict,
            "verdict_reason": reason,
            "delivery_evidence_refs": sorted(str(record["id"]) for record in delivery),
            "validation_result_refs": sorted(str(record["id"]) for record in validations),
            "acceptance_summary": summarize_acceptance(records),
            "unresolved_risks": sorted(unresolved_risks),
            "limitations": sorted(limitations),
            "conflict_codes": sorted(conflict_codes),
        },
        "constraints": {"delivery_verdict_boundary": "does_not_approve_merge_release_or_deliveryyield"},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", help="Input JSONL file.")
    parser.add_argument("--out", help="Optional delivery.verdict JSONL output path.")
    args = parser.parse_args()

    records, read_failures = read_jsonl(Path(args.jsonl))
    failures = read_failures + validate_records(records)
    if failures:
        for item in failures:
            print(item, file=sys.stderr)
        return 1
    try:
        verdict = author_verdict(records)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    output = stable_json(verdict) + "\n"
    if args.out:
        write_text_lf(Path(args.out), output)
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
