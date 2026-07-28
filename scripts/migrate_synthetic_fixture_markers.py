#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Add explicit synthetic/adoption markers to public JSONL conformance fixtures."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def normalize(path: Path, *, check: bool) -> bool:
    changed = False
    output: list[str] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_no}: expected JSON object")
        constraints = value.get("constraints")
        if isinstance(constraints, dict) and constraints.get("ip_boundary") == "synthetic":
            if constraints.get("simulation_status") != "synthetic_reference":
                constraints["simulation_status"] = "synthetic_reference"
                changed = True
            if constraints.get("downstream_adoption_status") != "not_observed":
                constraints["downstream_adoption_status"] = "not_observed"
                changed = True
        output.append(json.dumps(value, separators=(",", ":"), ensure_ascii=False))
    if changed and not check:
        path.write_text("\n".join(output) + "\n", encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    changed: list[Path] = []
    try:
        for path in sorted(
            (root / "feature-delivery-harness-mvp" / "evals").glob("*/input.jsonl")
        ):
            if normalize(path, check=args.check):
                changed.append(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if args.check and changed:
        for path in changed:
            print(f"synthetic marker drift: {path.relative_to(root)}", file=sys.stderr)
        return 1
    action = "validated" if args.check else "normalized"
    print(f"{action} synthetic markers across {len(changed)} changed fixture(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
