#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate Lattice workspace manifests and template references."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from capability_utils import (
    REQUIRED_WORKSPACE_FIELDS,
    agent_ids,
    check_required,
    is_relative_repo_path,
    knowledge_ids,
    load_json,
    load_jsonl,
    mcp_ids,
    skill_ids,
)


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
    if isinstance(repo_scope, dict):
        folders = repo_scope.get("folders", [])
        if not isinstance(folders, list):
            errors.append("repo_scope.folders must be a list when present")
        for folder in folders if isinstance(folders, list) else []:
            folder_value = str(folder)
            if not is_relative_repo_path(folder_value) and folder_value != ".":
                errors.append(f"repo_scope folder must be relative: {folder_value}")

    instructions = record.get("instructions", [])
    if not isinstance(instructions, list):
        errors.append("instructions must be a list")
    for item in instructions if isinstance(instructions, list) else []:
        if not isinstance(item, dict):
            errors.append("instructions entries must be objects")
            continue
        instruction_path = str(item.get("path", ""))
        if not is_relative_repo_path(instruction_path):
            errors.append(f"instruction path must be relative: {instruction_path}")
            continue
        if not (root / instruction_path).exists():
            if item.get("required") is True:
                errors.append(f"required instruction path missing: {instruction_path}")
            else:
                warnings.append(f"optional instruction path missing: {instruction_path}")

    excludes = record.get("excludes", [])
    if not isinstance(excludes, list):
        errors.append("excludes must be a list")
    for excluded in excludes if isinstance(excludes, list) else []:
        excluded_value = str(excluded)
        if not is_relative_repo_path(excluded_value) and excluded_value != ".git":
            errors.append(f"exclude path must be relative: {excluded_value}")

    validation = record.get("validation", [])
    if not isinstance(validation, list):
        errors.append("validation must be a list")
    for command in validation if isinstance(validation, list) else []:
        command_text = str(command)
        for token in command_text.split():
            if token.endswith(".py") and not (root / token).exists():
                errors.append(f"validation command references missing script: {token}")

    return errors, warnings


def validate_workspace_index(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()
    index_path = root / "registry" / "workspace_templates.index.jsonl"
    for row_number, row in enumerate(load_jsonl(index_path), start=1):
        row_label = f"registry/workspace_templates.index.jsonl:{row_number}"
        workspace_id = str(row.get("workspace_id", ""))
        if not workspace_id:
            errors.append(f"{row_label}: missing workspace_id")
            continue
        if workspace_id in seen:
            errors.append(f"{row_label}: duplicate workspace_id: {workspace_id}")
        seen.add(workspace_id)
        manifest_path_value = str(row.get("path", ""))
        if not is_relative_repo_path(manifest_path_value):
            errors.append(f"{row_label}: path must be a relative repo path")
            continue
        manifest_path = root / manifest_path_value
        if not manifest_path.exists():
            errors.append(f"{row_label}: workspace template path missing: {manifest_path_value}")
            continue
        manifest = load_json(manifest_path)
        if manifest.get("id") != workspace_id:
            errors.append(f"{row_label}: workspace_id does not match manifest id")
        for field in ["agents", "skills"]:
            if field in row and manifest.get(field) != row.get(field):
                warnings.append(f"{row_label}: {field} differs from manifest")
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
    errors, warnings = validate_workspace_index(root)
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
    print(f"validated {len(paths)} workspace manifest(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
