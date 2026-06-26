#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate Lattice workspace manifests and template references."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from capability_utils import REQUIRED_WORKSPACE_FIELDS, agent_ids, check_required, knowledge_ids, load_json, mcp_ids, skill_ids


SUPPORTED_VSCODE_SETTINGS = {
    "chat.agentSkillsLocations",
    "chat.instructionsFilesLocations",
    "git.scanRepositories",
    "git.autoRepositoryDetection",
    "git.openRepositoryInParentFolders",
    "search.exclude",
    "files.watcherExclude",
}


def validate_manifest(path: Path, root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    record = load_json(path)

    for field in check_required(record, REQUIRED_WORKSPACE_FIELDS):
        errors.append(f"missing required field: {field}")

    known_agents = agent_ids(root)
    known_skills = skill_ids(root)
    known_mcp = mcp_ids(root)
    known_knowledge = knowledge_ids(root)

    for agent_id in record.get("agents", []) if isinstance(record.get("agents", []), list) else []:
        if str(agent_id) not in known_agents:
            errors.append(f"unknown agent reference: {agent_id}")
    for skill_id in record.get("skills", []) if isinstance(record.get("skills", []), list) else []:
        if str(skill_id) not in known_skills:
            errors.append(f"unknown skill reference: {skill_id}")
    for mcp_id in record.get("mcp", []) if isinstance(record.get("mcp", []), list) else []:
        if str(mcp_id) not in known_mcp:
            errors.append(f"unknown MCP reference: {mcp_id}")
    for pack_id in record.get("knowledge", []) if isinstance(record.get("knowledge", []), list) else []:
        if str(pack_id) not in known_knowledge:
            errors.append(f"unknown knowledge pack reference: {pack_id}")

    source_control = record.get("source_control", {})
    if isinstance(source_control, dict):
        for key in source_control:
            if key not in SUPPORTED_VSCODE_SETTINGS:
                warnings.append(f"source_control setting is not in supported VS Code allowlist: {key}")
    else:
        errors.append("source_control must be an object")

    repo_scope = record.get("repo_scope", {})
    if isinstance(repo_scope, dict) and repo_scope.get("private_context_allowed") is True:
        warnings.append("workspace allows private context; keep public templates generic")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="?", help="Workspace manifest path. Defaults to all templates.")
    parser.add_argument("--root", default=".", help="Lattice repo root.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    paths = [Path(args.manifest)] if args.manifest else sorted((root / "workspaces" / "templates").glob("*.json"))
    all_errors: list[str] = []
    all_warnings: list[str] = []
    for path in paths:
        path = path if path.is_absolute() else root / path
        errors, warnings = validate_manifest(path, root)
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
    print(f"validated {len(paths)} workspace manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
