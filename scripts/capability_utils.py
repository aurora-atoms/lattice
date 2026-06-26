#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Shared helpers for dependency-light capability-control-plane validators."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REQUIRED_AGENT_FIELDS = [
    "id",
    "name",
    "description",
    "owner",
    "status",
    "role",
    "scope",
    "risk_level",
    "data_classification",
    "instruction_source",
    "skills",
    "mcp",
    "knowledge",
    "token_budget",
    "cache",
    "install",
    "telemetry",
]

REQUIRED_WORKSPACE_FIELDS = [
    "id",
    "task_type",
    "repo_scope",
    "agents",
    "skills",
    "mcp",
    "knowledge",
    "instructions",
    "source_control",
    "excludes",
    "validation",
]

SCENARIO_TERMS = [
    "feature-a",
    "feature a",
    "ticket-",
    "ticket ",
    "customer-",
    "customer ",
    "repo-",
    "repo ",
    "migration-",
]

PRIVATE_TERMS = [
    "auralis",
    "aurora-context",
    "ptcg",
    "customer",
    "company-specific",
    "downstream repo",
]

ABSOLUTE_PATH_RE = re.compile(r"(?i)(?:[a-z]:\\|/home/|/users/|/var/|/tmp/)")
TIMESTAMP_RE = re.compile(r"\b20[0-9]{2}-[0-9]{2}-[0-9]{2}(?:[tT ][0-9]{2}:[0-9]{2})?\b")
UUID_RE = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError(f"{path}:{line_number}: expected JSON object")
            records.append(record)
    return records


def registry_ids(records: list[dict[str, Any]], key: str) -> set[str]:
    return {str(record[key]) for record in records if key in record}


def skill_ids(root: Path) -> set[str]:
    return registry_ids(load_jsonl(root / "registry" / "skills.index.jsonl"), "skill_id")


def agent_ids(root: Path) -> set[str]:
    return registry_ids(load_jsonl(root / "registry" / "agents.index.jsonl"), "id")


def mcp_ids(root: Path) -> set[str]:
    return registry_ids(load_jsonl(root / "registry" / "mcp_servers.index.jsonl"), "mcp_id")


def knowledge_ids(root: Path) -> set[str]:
    return registry_ids(load_jsonl(root / "registry" / "knowledge_packs.index.jsonl"), "pack_id")


def contains_any(text: str, terms: list[str]) -> list[str]:
    lowered = text.lower()
    return [term for term in terms if term in lowered]


def check_required(record: dict[str, Any], fields: list[str]) -> list[str]:
    return [field for field in fields if field not in record]


def is_relative_repo_path(value: str) -> bool:
    return bool(value) and not ABSOLUTE_PATH_RE.search(value) and not value.startswith("../")


def stable_text_issues(text: str) -> list[str]:
    issues: list[str] = []
    if ABSOLUTE_PATH_RE.search(text):
        issues.append("absolute local path found")
    if TIMESTAMP_RE.search(text):
        issues.append("timestamp-like value found")
    if UUID_RE.search(text):
        issues.append("random-id-like UUID found")
    return issues
