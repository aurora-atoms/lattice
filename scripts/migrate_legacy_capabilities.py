#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Create the one-time canonical capability manifest from legacy registries."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROLES = [
    "atomic_capability",
    "selector",
    "reference_workflow",
    "capability_profile",
    "projection",
    "validator",
    "template",
    "governance_contract",
]

ROLE_OVERRIDES = {
    "lattice-governor": "governance_contract",
    "delivery-capability-conductor": "selector",
    "context-mastery": "selector",
    "knowledge-integrity": "selector",
    "risk-ahead": "selector",
    "delivery-artifact-builder": "selector",
    "delivery-learning": "selector",
    "human-judgment-amplifier": "selector",
    "management-translation": "selector",
    "delivery-capability-strategy": "selector",
    "feature-understanding-loop": "selector",
    "knowledge-profile-evaluator": "validator",
    "capability-harness-engineer": "validator",
    "token-economics-dossier-generator": "projection",
    "pr-to-release-summary": "projection",
    "executive-feature-brief": "projection",
    "risk-escalation-packet": "projection",
    "audience-adapted-management-update": "projection",
    "delivery-capability-conductor-agent": "selector",
    "context-mastery-agent": "selector",
    "knowledge-integrity-agent": "selector",
    "risk-sentinel-agent": "selector",
    "delivery-artifact-agent": "selector",
    "delivery-learning-agent": "selector",
    "human-judgment-agent": "selector",
    "management-translation-agent": "selector",
    "delivery-capability-strategy-agent": "selector",
    "capability-harness-engineer-agent": "validator",
}

EVIDENCE_CONTRACT = {
    "required_sections": [
        "facts",
        "inference_summary",
        "citations",
        "uncertainty",
        "unknowns",
        "assumptions",
    ],
    "policy": "Separate source-supported facts from inference and preserve uncertainty, unknowns, and assumptions.",
}

STOP_CONDITIONS = [
    "goal_reached",
    "stage_gate_reached",
    "missing_permission",
    "missing_required_input",
    "source_unavailable",
    "insufficient_evidence",
    "high_risk_boundary",
    "human_decision_required",
    "failed_validation",
]

AUTHORITY_BOUNDARY = (
    "Provides public capability behavior or artifacts only; grants no private business conclusion, "
    "adoption, asset-promotion, manager-wording, merge, release, deployment, or production authority."
)
CANONICAL_PROJECTION_FIELDS = {
    "version",
    "capability_role",
    "public_package_status",
    "description",
    "trigger",
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_no}: expected JSON object")
        records.append(value)
    return records


def native_skill_description(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^description:\s*(.+)$", text)
    if not match:
        raise ValueError(f"{path}: missing frontmatter description")
    value = match.group(1).strip()
    if value.startswith(("'", '"')) and value.endswith(value[0]):
        value = value[1:-1]
    return value


def split_versioned_id(value: str) -> tuple[str, str]:
    family, separator, version = value.rpartition("@")
    if not separator or not family or not version:
        raise ValueError(f"invalid versioned id: {value}")
    return family, version


def strip_generated_fields(
    record: dict[str, Any], *, keep_description: bool = False
) -> dict[str, Any]:
    generated = set(CANONICAL_PROJECTION_FIELDS)
    if keep_description:
        generated.remove("description")
    return {
        key: value
        for key, value in record.items()
        if key not in generated
    }


def context_entries(root: Path) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    entries: dict[str, dict[str, Any]] = {}
    sources: dict[str, str] = {}
    paths = [root / "registry" / "skill-context.catalog.json"]
    paths.extend(sorted((root / "registry" / "skill-context.extensions").glob("*.json")))
    for path in paths:
        value = load_json(path)
        for entry in value.get("skills", []):
            name = str(entry["name"])
            entries[name] = entry
            sources[name] = path.relative_to(root).as_posix()
    return entries, sources


def normalized_skill_legacy(
    root: Path,
    name: str,
    context: dict[str, Any],
    existing: dict[str, Any] | None,
) -> dict[str, Any]:
    package = root / "skills" / name
    record = strip_generated_fields(dict(existing or {}))
    record.update(
        {
            "skill_id": name,
            "path": f"skills/{name}",
            "status": str(record.get("status", "experimental")),
            "owner": str(record.get("owner", "aurora-atoms")),
            "domain": str(record.get("domain", name)),
            "runtime_targets": list(context["runtime_targets"]),
            "risk_tier": str(record.get("risk_tier", "medium")),
            "auto_invocation": bool(record.get("auto_invocation", False)),
            "side_effects": str(record.get("side_effects", "repo_write")),
            "uses_scripts": bool(record.get("uses_scripts", (package / "scripts").exists())),
            "uses_network": bool(record.get("uses_network", False)),
            "contains_private_context": False,
            "public_export_allowed": True,
            "depends_on": list(record.get("depends_on", [])),
            "last_validated_at": str(record.get("last_validated_at", "pending")),
            "trigger_eval": str(
                record.get(
                    "trigger_eval",
                    "present" if (package / "evals" / "trigger_queries.json").exists() else "missing",
                )
            ),
            "output_eval": str(
                record.get(
                    "output_eval",
                    "present" if (package / "evals" / "output_cases.json").exists() else "missing",
                )
            ),
            "release_channel": str(record.get("release_channel", "experimental")),
            "notes": str(record.get("notes", context["changes"])),
        }
    )
    return record


def base_capability(
    *,
    prefix: str,
    record_type: str,
    family: str,
    version: str,
    role: str,
    status: str,
    path: str,
    description: str,
    changes: str,
    primary_user: str,
    secondary_audience: list[str],
    trigger: str,
    minimum_inputs: list[str],
    outputs: list[str],
    source_registry: str,
    legacy_record: dict[str, Any],
    context_catalog: str | None = None,
) -> dict[str, Any]:
    projection: dict[str, Any] = {
        "source_registry": source_registry,
        "legacy_record": legacy_record,
    }
    if context_catalog:
        projection["context_catalog"] = context_catalog
    return {
        "capability_id": f"{prefix}:{family}@{version}",
        "record_type": record_type,
        "family_name": family,
        "version": version,
        "capability_role": role,
        "public_package_status": status,
        "path": path,
        "description": description,
        "changes": changes,
        "primary_user": primary_user,
        "secondary_audience": secondary_audience,
        "trigger": trigger,
        "minimum_inputs": minimum_inputs,
        "outputs": outputs,
        "evidence_contract": EVIDENCE_CONTRACT,
        "success_signals": [
            "declared outputs are visible and validated",
            "evidence and authority boundaries remain satisfied",
        ],
        "stop_conditions": STOP_CONDITIONS,
        "authority_boundary": AUTHORITY_BOUNDARY,
        "compatibility": {
            "semantic_versioning": True,
            "legacy_status_field": str(legacy_record.get("status", "experimental")),
            "migration": "Legacy status remains a compatibility field; use public_package_status for public dependency readiness.",
        },
        "deprecated_by": None,
        "projection": projection,
    }


def build_manifest(root: Path) -> dict[str, Any]:
    policy = load_json(root / "registry" / "capability-context-policy.json")
    skill_context, context_sources = context_entries(root)
    agent_context_value = load_json(root / "registry" / "agent-context.catalog.json")
    agent_context = {str(item["name"]): item for item in agent_context_value["agents"]}
    skill_index = {
        str(item["skill_id"]): item
        for item in load_jsonl(root / "registry" / "skills.index.jsonl")
    }
    agent_index = {
        str(item["name"]): item
        for item in load_jsonl(root / "registry" / "agents.index.jsonl")
    }
    capabilities: list[dict[str, Any]] = []

    for name, version in sorted(policy["skill_versions"].items()):
        context = skill_context[name]
        legacy = normalized_skill_legacy(root, name, context, skill_index.get(name))
        capabilities.append(
            base_capability(
                prefix="skill",
                record_type="skill",
                family=name,
                version=str(version),
                role=ROLE_OVERRIDES.get(name, "atomic_capability"),
                status="contract_validated",
                path=f"skills/{name}/SKILL.md",
                description=native_skill_description(root / "skills" / name / "SKILL.md"),
                changes=str(context["changes"]),
                primary_user=str(context["primary_user"]),
                secondary_audience=list(context["secondary_audience"]),
                trigger=str(context["trigger"]),
                minimum_inputs=list(context["minimum"]),
                outputs=list(context["outputs"]),
                source_registry="registry/skills.index.jsonl",
                legacy_record=legacy,
                context_catalog=context_sources[name],
            )
        )

    for name, version in sorted(policy["agent_versions"].items()):
        context = agent_context[name]
        legacy = strip_generated_fields(dict(agent_index[name]))
        agent_record = load_json(root / str(legacy["path"]))
        capabilities.append(
            base_capability(
                prefix="agent",
                record_type="agent",
                family=name,
                version=str(version),
                role=ROLE_OVERRIDES.get(name, "atomic_capability"),
                status="contract_validated",
                path=str(legacy["instruction_path"]),
                description=str(agent_record["description"]),
                changes=str(context["changes"]),
                primary_user=str(context["primary_user"]),
                secondary_audience=list(context["secondary_audience"]),
                trigger=str(context["trigger"]),
                minimum_inputs=list(context["minimum"]),
                outputs=list(context["outputs"]),
                source_registry="registry/agents.index.jsonl",
                legacy_record=legacy,
                context_catalog="registry/agent-context.catalog.json",
            )
        )

    for record in load_jsonl(root / "registry" / "mcp_servers.index.jsonl"):
        family, version = split_versioned_id(str(record["mcp_id"]))
        capabilities.append(
            base_capability(
                prefix="mcp",
                record_type="mcp",
                family=family,
                version=version,
                role="governance_contract",
                status="draft",
                path="registry/mcp_servers.index.jsonl",
                description=str(record.get("notes") or f"Public MCP contract for {record['name']}."),
                changes="approved public tool exposure into a bounded runtime interface",
                primary_user="downstream runtime integrator",
                secondary_audience=["security reviewers", "capability maintainers"],
                trigger=f"{record['name']} tool access is explicitly required",
                minimum_inputs=["task scope", "approved toolset", "approval policy"],
                outputs=["bounded MCP tool contract"],
                source_registry="registry/mcp_servers.index.jsonl",
                legacy_record=strip_generated_fields(dict(record)),
            )
        )

    for record in load_jsonl(root / "registry" / "knowledge_packs.index.jsonl"):
        family, version = split_versioned_id(str(record["pack_id"]))
        capabilities.append(
            base_capability(
                prefix="knowledge",
                record_type="knowledge_pack",
                family=family,
                version=version,
                role="projection",
                status="draft",
                path="registry/knowledge_packs.index.jsonl",
                description=str(record["description"]),
                changes="public sources into a bounded knowledge projection",
                primary_user="downstream context assembler",
                secondary_audience=["knowledge owners", "security reviewers"],
                trigger=f"{record['name']} context is required for a bounded task",
                minimum_inputs=["task scope", "authorized source list"],
                outputs=["bounded public knowledge pack"],
                source_registry="registry/knowledge_packs.index.jsonl",
                legacy_record=strip_generated_fields(
                    dict(record), keep_description=True
                ),
            )
        )

    for record in load_jsonl(root / "registry" / "workspace_templates.index.jsonl"):
        family, version = split_versioned_id(str(record["workspace_id"]))
        capabilities.append(
            base_capability(
                prefix="workspace",
                record_type="workspace_template",
                family=family,
                version=version,
                role="capability_profile",
                status="contract_validated",
                path=str(record["path"]),
                description=f"Public workspace profile for {record['task_type']} tasks.",
                changes="a bounded task type into a least-privilege workspace capability profile",
                primary_user="downstream workspace maintainer",
                secondary_audience=["developers", "security reviewers"],
                trigger=f"a {record['task_type']} workspace profile is requested",
                minimum_inputs=["task type", "repository scope", "runtime target"],
                outputs=["bounded workspace capability profile"],
                source_registry="registry/workspace_templates.index.jsonl",
                legacy_record=strip_generated_fields(dict(record)),
            )
        )

    return {
        "contract": "lat.canonical-capability-manifest.v1",
        "contract_version": "1.0.0",
        "public_package_status_contract": "schemas/capability/public-package-lifecycle.v1.schema.json",
        "capability_roles": ROLES,
        "capabilities": sorted(capabilities, key=lambda item: item["capability_id"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument(
        "--out",
        default="registry/capability-manifest.json",
        help="Manifest path relative to root.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing manifest. Intended only for the reviewed one-time migration.",
    )
    args = parser.parse_args()
    root = Path(args.root).resolve()
    out = root / args.out
    if out.exists() and not args.force:
        print(f"{out}: already exists; refuse legacy overwrite without --force", file=sys.stderr)
        return 2
    try:
        manifest = build_manifest(root)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"wrote {len(manifest['capabilities'])} canonical capabilities to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
