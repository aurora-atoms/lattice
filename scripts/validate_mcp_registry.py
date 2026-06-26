#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate MCP registry records for tool allowlists and approval policy."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from capability_utils import load_jsonl


RISKY_TOOL_WORDS = ["write", "deploy", "secret", "shell", "delete", "destructive"]


def validate_record(record: dict[str, object]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    mcp_id = str(record.get("mcp_id", "<missing>"))
    for field in ["mcp_id", "name", "status", "runtime_targets", "toolsets", "approval", "risk_level"]:
        if field not in record:
            errors.append(f"{mcp_id}: missing required field: {field}")

    toolsets = record.get("toolsets", [])
    if not isinstance(toolsets, list) or not toolsets:
        errors.append(f"{mcp_id}: toolsets must be a non-empty list")

    approval = record.get("approval", {})
    if not isinstance(approval, dict):
        errors.append(f"{mcp_id}: approval must be an object")
        approval = {}
    for key in ["read", "write", "destructive"]:
        if key not in approval:
            errors.append(f"{mcp_id}: approval.{key} is required")
    if approval.get("destructive") != "deny":
        errors.append(f"{mcp_id}: destructive approval must be deny")

    joined_toolsets = " ".join(str(item).lower() for item in toolsets if isinstance(toolsets, list))
    if any(word in joined_toolsets for word in RISKY_TOOL_WORDS):
        if approval.get("write") != "prompt" or approval.get("destructive") != "deny":
            errors.append(f"{mcp_id}: risky toolsets require write=prompt and destructive=deny")
    if record.get("risk_level") == "high":
        warnings.append(f"{mcp_id}: high-risk MCP record requires manual review before install")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Lattice repo root.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    records = load_jsonl(root / "registry" / "mcp_servers.index.jsonl")
    all_errors: list[str] = []
    all_warnings: list[str] = []
    for record in records:
        errors, warnings = validate_record(record)
        all_errors.extend(errors)
        all_warnings.extend(warnings)

    if all_warnings:
        print("Warnings:")
        for warning in all_warnings:
            print(f"- {warning}")
    if all_errors:
        print("Errors:", file=sys.stderr)
        for error in all_errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"validated {len(records)} MCP record(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
