#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate compact routing rules against the Skill registry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

VALID_POLICIES = {"auto", "recommend", "manual"}


def load(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{number}: expected object")
            value["_line"] = number
            rows.append(value)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []
    try:
        skills = {row["skill_id"]: row for row in load(root / "registry" / "skills.index.jsonl")}
        rules = load(root / "registry" / "capability-routing.index.jsonl")
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"Errors:\n- {exc}", file=sys.stderr)
        return 1

    seen: set[str] = set()
    required = {"route_id", "skill_id", "priority", "terms", "stages", "policy", "min_score", "min_margin", "requires_confirmation"}
    for rule in rules:
        label = f"registry/capability-routing.index.jsonl:{rule['_line']}"
        missing = sorted(required - set(rule))
        if missing:
            errors.append(f"{label}: missing fields: {', '.join(missing)}")
        route_id = str(rule.get("route_id", ""))
        if route_id in seen:
            errors.append(f"{label}: duplicate route_id: {route_id}")
        seen.add(route_id)
        skill_id = str(rule.get("skill_id", ""))
        if skill_id not in skills:
            errors.append(f"{label}: unknown skill_id: {skill_id}")
        if rule.get("policy") not in VALID_POLICIES:
            errors.append(f"{label}: invalid policy")
        if not isinstance(rule.get("terms"), list) or not rule.get("terms"):
            errors.append(f"{label}: terms must be a non-empty list")
        for field in ("priority", "min_score", "min_margin"):
            if not isinstance(rule.get(field), int) or int(rule.get(field, -1)) < 0:
                errors.append(f"{label}: {field} must be a nonnegative integer")
        if not isinstance(rule.get("requires_confirmation"), bool):
            errors.append(f"{label}: requires_confirmation must be boolean")
        record = skills.get(skill_id, {})
        effects = str(record.get("side_effects", "none")).casefold().strip()
        network = bool(record.get("uses_network", False))
        if rule.get("policy") == "auto" and (effects not in {"", "none", "read-only", "readonly"} or network):
            errors.append(f"{label}: side-effectful or network Skill cannot use auto policy")

    if errors:
        print("Errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"validated {len(rules)} capability routing rule(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
