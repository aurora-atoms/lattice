#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate canonical Lattice agent records and instruction sources."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from capability_utils import (
    PRIVATE_TERMS,
    REQUIRED_AGENT_FIELDS,
    SCENARIO_TERMS,
    agent_ids,
    check_required,
    contains_any,
    is_relative_repo_path,
    knowledge_ids,
    load_json,
    mcp_ids,
    skill_ids,
    stable_text_issues,
)


def find_agent_records(root: Path) -> list[Path]:
    agents_root = root / "agents"
    if not agents_root.exists():
        return []
    return sorted(agents_root.rglob("agent.json"))


def validate_record(path: Path, root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    record = load_json(path)

    for field in check_required(record, REQUIRED_AGENT_FIELDS):
        errors.append(f"missing required field: {field}")

    agent_id = str(record.get("id", ""))
    name = str(record.get("name", ""))
    if agent_id and not agent_id.startswith(f"{name}@"):
        errors.append("id must start with name@")
    if name and contains_any(name, SCENARIO_TERMS):
        errors.append("agent name appears scenario-specific")
    if str(record.get("role", "")) != name:
        warnings.append("role should match the generic agent name")

    instruction = record.get("instruction_source", {})
    if isinstance(instruction, dict):
        instruction_path = str(instruction.get("path", ""))
        if not is_relative_repo_path(instruction_path):
            errors.append("instruction_source.path must be a relative repo path")
        source_path = root / instruction_path
        if not source_path.exists():
            errors.append(f"instruction source missing: {instruction_path}")
        else:
            text = source_path.read_text(encoding="utf-8")
            for issue in stable_text_issues(text):
                errors.append(f"{instruction_path}: {issue}")
            private_terms = contains_any(text, PRIVATE_TERMS)
            if private_terms:
                errors.append(f"{instruction_path}: private/downstream context term found: {', '.join(private_terms)}")
            scenario_terms = contains_any(text, SCENARIO_TERMS)
            if scenario_terms:
                errors.append(f"{instruction_path}: scenario-specific term found: {', '.join(scenario_terms)}")
        if instruction.get("hash_required") is not True:
            errors.append("instruction_source.hash_required must be true")
    else:
        errors.append("instruction_source must be an object")

    cache = record.get("cache", {})
    if isinstance(cache, dict):
        for key in ["deterministic_order", "no_timestamps", "no_random_ids", "no_absolute_local_paths", "agent_hash_required"]:
            if cache.get(key) is not True:
                errors.append(f"cache.{key} must be true")
    else:
        errors.append("cache must be an object")

    install = record.get("install", {})
    scopes = install.get("scopes", []) if isinstance(install, dict) else []
    if "global" in scopes:
        warnings.append("global install scope is present; ensure installs remain narrow")

    known_skills = skill_ids(root)
    known_mcp = mcp_ids(root)
    known_knowledge = knowledge_ids(root)
    for item in record.get("skills", []) if isinstance(record.get("skills", []), list) else []:
        skill_id = str(item.get("skill_id", "")) if isinstance(item, dict) else str(item)
        if skill_id and skill_id not in known_skills:
            errors.append(f"unknown skill_id reference: {skill_id}")
    for item in record.get("mcp", []) if isinstance(record.get("mcp", []), list) else []:
        mcp_id = str(item.get("mcp_id", "")) if isinstance(item, dict) else str(item)
        if mcp_id and mcp_id not in known_mcp:
            errors.append(f"unknown mcp_id reference: {mcp_id}")
        toolsets = item.get("toolsets", []) if isinstance(item, dict) else []
        if not toolsets:
            errors.append(f"mcp reference lacks toolsets: {mcp_id}")
    for item in record.get("knowledge", []) if isinstance(record.get("knowledge", []), list) else []:
        pack_id = str(item.get("pack_id", "")) if isinstance(item, dict) else str(item)
        if pack_id and pack_id not in known_knowledge:
            errors.append(f"unknown knowledge pack reference: {pack_id}")

    indexed_agents = agent_ids(root)
    if agent_id and indexed_agents and agent_id not in indexed_agents:
        warnings.append("agent record is not present in registry/agents.index.jsonl")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Lattice repo root.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    records = find_agent_records(root)
    all_errors: list[str] = []
    all_warnings: list[str] = []
    for path in records:
        errors, warnings = validate_record(path, root)
        rel = path.relative_to(root)
        all_errors.extend(f"{rel}: {message}" for message in errors)
        all_warnings.extend(f"{rel}: {message}" for message in warnings)

    if all_warnings:
        print("Warnings:")
        for warning in all_warnings:
            print(f"- {warning}")
    if all_errors:
        print("Errors:", file=sys.stderr)
        for error in all_errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"validated {len(records)} agent record(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
