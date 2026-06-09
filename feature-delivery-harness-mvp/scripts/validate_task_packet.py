#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate bounded task packets inside FDH JSONL files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from fdh_lib import list_value, read_jsonl, records_by_type, stable_json, validate_records, validation_result_record


UNBOUNDED_RE = re.compile(r"(?i)\b(entire repo|whole repo|whole system|all files|everything|full rewrite|all modules)\b")
UNSAFE_COMMAND_RE = re.compile(r"(?i)\b(git\s+push|git\s+reset|remove-item|rm\s+-rf|del\s+/s|deploy|release|publish|prod|production|secret|credential)\b")


def fail(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


def text_is_vague(value: Any) -> bool:
    if not isinstance(value, str):
        return True
    cleaned = value.strip()
    return len(cleaned) < 12 or cleaned.lower() in {"tbd", "todo", "fix it", "make it better", "unknown"}


def validate_task_packet(records: list[dict[str, Any]]) -> list[dict[str, str]]:
    failures: list[dict[str, str]] = []
    features = records_by_type(records, "feature_delivery_case")
    tasks = records_by_type(records, "task.packet")
    if not features:
        failures.append(fail("VAGUE_OUTCOME", "feature_delivery_case record is required"))
    if not tasks:
        failures.append(fail("MISSING_VALIDATION_COMMANDS", "task.packet record is required"))
        return failures

    feature_payload = features[0].get("payload", {}) if features else {}
    task_payload = tasks[0].get("payload", {})
    if text_is_vague(feature_payload.get("user_usable_outcome")):
        failures.append(fail("VAGUE_OUTCOME", "feature_delivery_case.user_usable_outcome is missing or vague"))
    if not list_value(feature_payload.get("acceptance_criteria")):
        failures.append(fail("MISSING_ACCEPTANCE_CRITERIA", "feature_delivery_case.acceptance_criteria is required"))
    if not list_value(feature_payload.get("non_goals")):
        failures.append(fail("MISSING_NON_GOALS", "feature_delivery_case.non_goals is required"))
    if not list_value(task_payload.get("allowed_changes")):
        failures.append(fail("MISSING_ALLOWED_CHANGES", "task.packet.allowed_changes is required"))
    if not list_value(task_payload.get("forbidden_changes")):
        failures.append(fail("MISSING_FORBIDDEN_CHANGES", "task.packet.forbidden_changes is required"))
    if not list_value(task_payload.get("evidence_requirements")):
        failures.append(fail("MISSING_EVIDENCE_REQUIREMENTS", "task.packet.evidence_requirements is required"))

    target_files = list_value(task_payload.get("target_files"))
    target_areas = list_value(task_payload.get("target_areas"))
    scope_text = " ".join(str(item) for item in target_files + target_areas + [feature_payload.get("scope_summary", ""), task_payload.get("objective", "")])
    if not target_files and not target_areas:
        failures.append(fail("UNBOUNDED_SCOPE", "task.packet requires target_files or target_areas"))
    if UNBOUNDED_RE.search(scope_text):
        failures.append(fail("UNBOUNDED_SCOPE", "task.packet scope is too broad"))
    if len(target_files) > 12 or len(target_areas) > 6 or int(feature_payload.get("context_token_count", 0) or 0) > 24000 or int(task_payload.get("context_token_count", 0) or 0) > 24000:
        failures.append(fail("SCOPE_TOO_LARGE", "task.packet exceeds MVP scope or context budget"))

    validation_commands = list_value(task_payload.get("validation_commands"))
    if not validation_commands:
        failures.append(fail("MISSING_VALIDATION_COMMANDS", "task.packet.validation_commands is required"))
    has_automated = False
    has_usability = False
    for command in validation_commands:
        if not isinstance(command, dict):
            failures.append(fail("MISSING_VALIDATION_COMMANDS", "validation command must be an object"))
            continue
        for field in ("id", "purpose", "cwd", "timeout", "expected_outcome", "target_acceptance_ids"):
            if field not in command:
                failures.append(fail("MISSING_VALIDATION_COMMANDS", f"validation command missing {field}"))
        if command.get("command"):
            has_automated = True
            if UNSAFE_COMMAND_RE.search(str(command.get("command"))) and not command.get("explicitly_whitelisted"):
                failures.append(fail("UNSAFE_COMMAND", f"unsafe validation command: {command.get('id', 'unknown')}"))
        if command.get("manual_steps") or re.search(r"(?i)(acceptance|usable|user)", str(command.get("purpose", ""))):
            has_usability = True
    if validation_commands and not has_automated:
        failures.append(fail("MISSING_VALIDATION_COMMANDS", "code task requires at least one automated validation command"))
    if validation_commands and not has_usability:
        failures.append(fail("MISSING_USER_USABILITY_VALIDATION", "task requires acceptance or user-usability validation"))
    return dedupe(failures)


def dedupe(failures: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    result: list[dict[str, str]] = []
    for item in failures:
        key = (item["code"], item["message"])
        if key not in seen:
            result.append(item)
            seen.add(key)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", help="Input JSONL file.")
    parser.add_argument("--emit-validation-result", action="store_true", help="Print validation.result JSONL for failures.")
    args = parser.parse_args()

    path = Path(args.jsonl)
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2
    records, read_failures = read_jsonl(path)
    structural_failures = read_failures + validate_records(records)
    failures = [{"code": str(item["code"]), "message": str(item["message"])} for item in structural_failures]
    failures.extend(validate_task_packet(records))
    failures = dedupe(failures)
    if failures:
        if args.emit_validation_result:
            for item in failures:
                print(stable_json(validation_result_record(item["code"], item["message"], source="validate_task_packet")))
        else:
            for item in failures:
                print(json.dumps(item, sort_keys=True), file=sys.stderr)
        return 1
    print("validated task packet")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
