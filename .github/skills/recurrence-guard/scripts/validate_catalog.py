#!/usr/bin/env python3
"""Dependency-free validation for Recurrence Guard catalogs and replay fixtures."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

STATUSES = {"candidate", "active", "retired"}
SEVERITIES = {"block", "warn"}
OUTCOMES = {"BLOCK", "WARN", "UNKNOWN", "NO_KNOWN_MATCH"}
REQUIRED_GUARD_FIELDS = {
    "id",
    "title",
    "status",
    "severity",
    "scope",
    "prohibited_change",
    "applicability",
    "evidence_refs",
    "exceptions",
    "rationale",
}
REQUIRED_REPLAY_FIELDS = {
    "id",
    "guard_id",
    "change_summary",
    "evidence_available",
    "exception_applies",
    "expected_outcome",
    "reason",
}


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc.msg}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number}: each JSONL row must be an object")
            value["_line"] = line_number
            rows.append(value)
    return rows


def require_nonempty_list(row: dict, field: str, label: str, errors: list[str]) -> None:
    value = row.get(field)
    if not isinstance(value, list) or not value:
        errors.append(f"{label}: {field} must be a non-empty list")


def validate_guards(path: Path, rows: list[dict], authoritative: bool) -> tuple[dict[str, dict], list[str]]:
    errors: list[str] = []
    by_id: dict[str, dict] = {}
    for row in rows:
        label = f"{path}:{row['_line']}"
        missing = sorted(REQUIRED_GUARD_FIELDS - set(row))
        if missing:
            errors.append(f"{label}: missing fields: {', '.join(missing)}")
            continue
        guard_id = str(row["id"])
        if guard_id in by_id:
            errors.append(f"{label}: duplicate guard id: {guard_id}")
        by_id[guard_id] = row
        if row["status"] not in STATUSES:
            errors.append(f"{label}: invalid status: {row['status']}")
        if row["severity"] not in SEVERITIES:
            errors.append(f"{label}: invalid severity: {row['severity']}")
        if row["status"] == "candidate" and row["severity"] == "block":
            errors.append(f"{label}: candidate guards cannot block")
        if not isinstance(row["scope"], dict) or not row["scope"]:
            errors.append(f"{label}: scope must be a non-empty object")
        require_nonempty_list(row, "evidence_refs", label, errors)
        if not isinstance(row["exceptions"], list):
            errors.append(f"{label}: exceptions must be a list")
        if row["status"] == "active" and row["severity"] == "block" and not row.get("prohibited_change"):
            errors.append(f"{label}: active blocking guards need a prohibited_change")
        if authoritative:
            for ref in row.get("evidence_refs", []):
                if str(ref).startswith("synthetic://"):
                    errors.append(f"{label}: authoritative catalogs cannot use synthetic evidence: {ref}")
    return by_id, errors


def validate_replays(path: Path, rows: list[dict], guards: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for row in rows:
        label = f"{path}:{row['_line']}"
        missing = sorted(REQUIRED_REPLAY_FIELDS - set(row))
        if missing:
            errors.append(f"{label}: missing fields: {', '.join(missing)}")
            continue
        replay_id = str(row["id"])
        if replay_id in seen:
            errors.append(f"{label}: duplicate replay id: {replay_id}")
        seen.add(replay_id)
        guard_id = str(row["guard_id"])
        guard = guards.get(guard_id)
        if guard is None:
            errors.append(f"{label}: unknown guard_id: {guard_id}")
            continue
        outcome = row["expected_outcome"]
        if outcome not in OUTCOMES:
            errors.append(f"{label}: invalid expected_outcome: {outcome}")
        if guard["status"] == "candidate" and outcome == "BLOCK":
            errors.append(f"{label}: candidate guard cannot have BLOCK as expected outcome")
        if row["exception_applies"] is True and outcome == "BLOCK":
            errors.append(f"{label}: an applicable exception cannot produce BLOCK")
        if row["evidence_available"] is False and outcome == "BLOCK":
            errors.append(f"{label}: missing evidence cannot produce BLOCK")
    if not any(row.get("expected_outcome") == "BLOCK" for row in rows):
        errors.append(f"{path}: replay set needs at least one positive BLOCK case")
    if not any(row.get("expected_outcome") == "NO_KNOWN_MATCH" for row in rows):
        errors.append(f"{path}: replay set needs at least one negative NO_KNOWN_MATCH case")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    base = Path(__file__).resolve().parent.parent
    parser.add_argument("--catalog", type=Path, default=base / "guards.example.jsonl")
    parser.add_argument("--evals", type=Path, default=base / "evals" / "replay-cases.jsonl")
    parser.add_argument(
        "--authoritative",
        action="store_true",
        help="Reject synthetic evidence; use this for a real repository guards.jsonl catalog.",
    )
    args = parser.parse_args()

    try:
        guard_rows = load_jsonl(args.catalog)
        replay_rows = load_jsonl(args.evals)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    guards, errors = validate_guards(args.catalog, guard_rows, args.authoritative)
    errors.extend(validate_replays(args.evals, replay_rows, guards))
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"validated {len(guard_rows)} guard(s) and {len(replay_rows)} replay case(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
