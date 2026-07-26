#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validate(packet: dict) -> list[str]:
    errors: list[str] = []
    if packet.get("record_type") != "lat.decision_question.v1":
        errors.append("record_type must be lat.decision_question.v1")

    options = packet.get("options")
    if not isinstance(options, list) or not 2 <= len(options) <= 4:
        errors.append("options must contain two to four entries")
        options = []

    ids: list[str] = []
    for index, option in enumerate(options):
        label = f"options[{index}]"
        if not isinstance(option, dict):
            errors.append(f"{label} must be an object")
            continue
        option_id = option.get("option_id")
        if not isinstance(option_id, str) or option_id not in {"A", "B", "C", "D"}:
            errors.append(f"{label}.option_id must be A, B, C, or D")
        else:
            ids.append(option_id)
        for field in ("action", "why_viable", "reversibility", "execution_after_selection", "validation_after_selection"):
            if not isinstance(option.get(field), str) or not option[field].strip():
                errors.append(f"{label}.{field} must be non-empty")
        for field in ("evidence_refs", "benefits", "tradeoffs", "risks"):
            value = option.get(field)
            if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
                errors.append(f"{label}.{field} must be a non-empty string list")

    if len(ids) != len(set(ids)):
        errors.append("option_id values must be unique")

    question = packet.get("primary_question")
    if not isinstance(question, str) or not question.strip():
        errors.append("primary_question must be non-empty")
    elif question.count("?") > 1:
        errors.append("primary_question must contain one primary question")

    response = packet.get("minimum_response")
    if not isinstance(response, str) or not response.strip():
        errors.append("minimum_response must be non-empty")
    else:
        missing = [option_id for option_id in ids if option_id not in response]
        if missing:
            errors.append("minimum_response must expose every selectable option id: " + ", ".join(missing))

    follow_ups = packet.get("follow_ups")
    if not isinstance(follow_ups, list) or len(follow_ups) > 2:
        errors.append("follow_ups must be a list with at most two entries")

    recipient = packet.get("recipient")
    if not isinstance(recipient, dict) or not recipient.get("role") or not recipient.get("authority_reason"):
        errors.append("recipient role and authority_reason are required")

    if not packet.get("execution_unlocked"):
        errors.append("execution_unlocked is required")
    if not packet.get("fallback_behavior"):
        errors.append("fallback_behavior is required")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate decision-question packet semantics.")
    parser.add_argument("packet")
    args = parser.parse_args()
    path = Path(args.packet)
    try:
        packet = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not isinstance(packet, dict):
        print("error: packet root must be an object", file=sys.stderr)
        return 1
    errors = validate(packet)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"validated decision question packet: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
