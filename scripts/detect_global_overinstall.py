#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Detect capability records that would expose broad tools or context globally."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from capability_utils import load_json, load_jsonl


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Lattice repo root.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    for record_path in sorted((root / "agents").rglob("agent.json")):
        record = load_json(record_path)
        scopes = record.get("install", {}).get("scopes", []) if isinstance(record.get("install"), dict) else []
        if "global" in scopes:
            capability_count = len(record.get("skills", [])) + len(record.get("mcp", [])) + len(record.get("knowledge", []))
            if capability_count > 3:
                errors.append(f"{record_path.relative_to(root)}: global scope exposes too many capabilities")
            else:
                warnings.append(f"{record_path.relative_to(root)}: global scope requires explicit install review")

    for record in load_jsonl(root / "registry" / "capabilities.index.jsonl"):
        scopes = record.get("install_scopes", [])
        if isinstance(scopes, list) and "global" in scopes:
            errors.append(f"{record.get('capability_id')}: global install scope is not allowed in public seed index")

    if all(path.exists() for path in [root / "registry" / "skills.index.jsonl", root / "registry" / "capabilities.index.jsonl"]):
        skill_count = len(load_jsonl(root / "registry" / "skills.index.jsonl"))
        global_count = sum(
            1
            for record in load_jsonl(root / "registry" / "capabilities.index.jsonl")
            if isinstance(record.get("install_scopes"), list) and "global" in record.get("install_scopes", [])
        )
        if skill_count and global_count >= skill_count:
            errors.append("capability index appears to expose all skills globally")

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    if errors:
        print("Errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("global overinstall check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
