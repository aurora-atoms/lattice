#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate compatibility registry projections from the canonical manifest."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

MANIFEST_PATH = "registry/capability-manifest.json"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def json_text(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def jsonl_text(records: list[dict[str, Any]]) -> str:
    return "".join(
        json.dumps(record, separators=(",", ":"), ensure_ascii=False) + "\n"
        for record in records
    )


def context_entry(capability: dict[str, Any], *, agent: bool) -> dict[str, Any]:
    entry = {
        "name": capability["family_name"],
        "changes": capability["changes"],
        "primary_user": capability["primary_user"],
        "secondary_audience": capability["secondary_audience"],
        "trigger": capability["trigger"],
        "minimum": capability["minimum_inputs"],
        "outputs": capability["outputs"],
        "runtime_targets": capability["projection"]["legacy_record"].get(
            "runtime_targets", []
        ),
    }
    if agent:
        entry = {
            "name": capability["family_name"],
            "path": capability["path"],
            **{key: value for key, value in entry.items() if key != "name"},
        }
    return entry


def legacy_projection(capability: dict[str, Any]) -> dict[str, Any]:
    record = dict(capability["projection"]["legacy_record"])
    record.update(
        {
            "version": capability["version"],
            "capability_role": capability["capability_role"],
            "public_package_status": capability["public_package_status"],
            "description": capability["description"],
            "trigger": capability["trigger"],
        }
    )
    return record


def capability_index_record(capability: dict[str, Any]) -> dict[str, Any]:
    legacy = capability["projection"]["legacy_record"]
    record_type = capability["record_type"]
    if record_type == "skill":
        source_id = capability["family_name"]
        path = legacy["path"]
        tags = [capability["capability_role"], legacy.get("domain", "skill")]
        install_scopes = ["project"]
        risk_level = legacy.get("risk_tier", "medium")
        data_classification = "public"
    elif record_type == "agent":
        source_id = legacy["id"]
        path = legacy["path"]
        tags = list(legacy.get("tags", [])) + [capability["capability_role"]]
        install_scopes = list(legacy.get("install_scopes", ["project"]))
        risk_level = legacy.get("risk_level", "medium")
        data_classification = "public"
    elif record_type == "mcp":
        source_id = legacy["mcp_id"]
        path = capability["projection"]["source_registry"]
        tags = ["mcp", capability["capability_role"]]
        install_scopes = ["project"]
        risk_level = legacy.get("risk_level", "medium")
        data_classification = "public"
    elif record_type == "knowledge_pack":
        source_id = legacy["pack_id"]
        path = capability["projection"]["source_registry"]
        tags = ["knowledge", capability["capability_role"]]
        install_scopes = ["project"]
        risk_level = "low"
        data_classification = legacy.get("data_classification", "public")
    else:
        source_id = legacy["workspace_id"]
        path = legacy["path"]
        tags = ["workspace", capability["capability_role"]]
        install_scopes = list(legacy.get("install_scopes", ["project"]))
        risk_level = "medium"
        data_classification = "public"
    return {
        "capability_id": capability["capability_id"],
        "record_type": record_type,
        "source_index": capability["projection"]["source_registry"],
        "source_id": source_id,
        "path": path,
        "version": capability["version"],
        "capability_role": capability["capability_role"],
        "public_package_status": capability["public_package_status"],
        "description": capability["description"],
        "trigger": capability["trigger"],
        "tags": sorted(set(tags)),
        "runtime_targets": list(legacy.get("runtime_targets", [])),
        "install_scopes": install_scopes,
        "risk_level": risk_level,
        "data_classification": data_classification,
    }


def build_projections(root: Path, manifest: dict[str, Any]) -> dict[str, str]:
    capabilities = list(manifest["capabilities"])
    projections: dict[str, str] = {}

    policy_path = root / "registry" / "capability-context-policy.json"
    policy = load_json(policy_path)
    policy["contract_version"] = "1.2.0"
    policy["skill_versions"] = {
        item["family_name"]: item["version"]
        for item in capabilities
        if item["record_type"] == "skill"
    }
    policy["agent_versions"] = {
        item["family_name"]: item["version"]
        for item in capabilities
        if item["record_type"] == "agent"
    }
    projections["registry/capability-context-policy.json"] = json_text(policy)

    context_paths = {
        str(item["projection"].get("context_catalog"))
        for item in capabilities
        if item["record_type"] in {"skill", "agent"}
    }
    for relative in sorted(context_paths):
        path = root / relative
        catalog = load_json(path)
        if "contract_version" in catalog:
            catalog["contract_version"] = "1.2.0"
        if relative == "registry/agent-context.catalog.json":
            catalog["agents"] = [
                context_entry(item, agent=True)
                for item in capabilities
                if item["record_type"] == "agent"
            ]
        else:
            catalog["skills"] = [
                context_entry(item, agent=False)
                for item in capabilities
                if item["record_type"] == "skill"
                and item["projection"].get("context_catalog") == relative
            ]
        projections[relative] = json_text(catalog)

    registry_types = {
        "skill": "registry/skills.index.jsonl",
        "agent": "registry/agents.index.jsonl",
        "mcp": "registry/mcp_servers.index.jsonl",
        "knowledge_pack": "registry/knowledge_packs.index.jsonl",
        "workspace_template": "registry/workspace_templates.index.jsonl",
    }
    for record_type, relative in registry_types.items():
        records = [
            legacy_projection(item)
            for item in capabilities
            if item["record_type"] == record_type
        ]
        projections[relative] = jsonl_text(records)

    projections["registry/capabilities.index.jsonl"] = jsonl_text(
        [capability_index_record(item) for item in capabilities]
    )
    return projections


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    try:
        manifest = load_json(root / MANIFEST_PATH)
        projections = build_projections(root, manifest)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    drift: list[str] = []
    for relative, expected in sorted(projections.items()):
        path = root / relative
        actual = path.read_text(encoding="utf-8") if path.exists() else ""
        if args.check:
            if actual != expected:
                drift.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8")

    if drift:
        for relative in drift:
            print(f"projection drift: {relative}", file=sys.stderr)
        print(
            "run scripts/generate_capability_registry_projections.py to regenerate",
            file=sys.stderr,
        )
        return 1
    if args.check:
        print(f"validated {len(projections)} deterministic registry projection(s)")
    else:
        print(f"generated {len(projections)} registry projection(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
