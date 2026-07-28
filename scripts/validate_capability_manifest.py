#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate canonical capability identity, lifecycle, paths, and projections."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from generate_capability_registry_projections import build_projections

ROLES = {
    "atomic_capability",
    "selector",
    "reference_workflow",
    "capability_profile",
    "projection",
    "validator",
    "template",
    "governance_contract",
}
PUBLIC_STATUSES = {
    "draft",
    "contract_validated",
    "conformance_validated",
    "released",
    "deprecated",
}
PREFIX = {
    "skill": "skill",
    "agent": "agent",
    "mcp": "mcp",
    "knowledge_pack": "knowledge",
    "workspace_template": "workspace",
}
REQUIRED_FIELDS = {
    "capability_id",
    "record_type",
    "family_name",
    "version",
    "capability_role",
    "public_package_status",
    "path",
    "description",
    "changes",
    "primary_user",
    "secondary_audience",
    "trigger",
    "minimum_inputs",
    "outputs",
    "evidence_contract",
    "success_signals",
    "stop_conditions",
    "authority_boundary",
    "compatibility",
    "deprecated_by",
    "projection",
}
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
FAMILY_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
WORD_RE = re.compile(r"[a-z0-9][a-z0-9_-]*")
STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "be",
    "do",
    "for",
    "from",
    "in",
    "into",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
    "use",
    "when",
    "with",
}
CONCEPT_GROUPS = (
    {"context", "understanding", "learning"},
    {"risk", "commitment", "exposure"},
    {"human", "expert", "expertise", "authority", "judgment"},
)


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


def terms(value: str) -> set[str]:
    normalized = value.lower().replace("-", " ").replace("_", " ")
    result = {word for word in WORD_RE.findall(normalized) if word not in STOPWORDS}
    for group in CONCEPT_GROUPS:
        if result & group:
            result.update(group)
    return result


def validate_entry(entry: Any, root: Path, label: str) -> list[str]:
    if not isinstance(entry, dict):
        return [f"{label}: capability must be an object"]
    errors: list[str] = []
    missing = sorted(REQUIRED_FIELDS - set(entry))
    if missing:
        errors.append(f"{label}: missing fields: {', '.join(missing)}")
        return errors
    extra = sorted(set(entry) - REQUIRED_FIELDS)
    if extra:
        errors.append(f"{label}: unknown fields: {', '.join(extra)}")
    record_type = str(entry["record_type"])
    family = str(entry["family_name"])
    version = str(entry["version"])
    expected_id = f"{PREFIX.get(record_type, 'invalid')}:{family}@{version}"
    if entry["capability_id"] != expected_id:
        errors.append(f"{label}: capability_id must equal {expected_id}")
    if not FAMILY_RE.fullmatch(family):
        errors.append(f"{label}: invalid family_name")
    if not SEMVER_RE.fullmatch(version):
        errors.append(f"{label}: invalid semantic version")
    if entry["capability_role"] not in ROLES:
        errors.append(f"{label}: invalid capability_role")
    status = entry["public_package_status"]
    if status not in PUBLIC_STATUSES:
        errors.append(f"{label}: invalid public_package_status")
    if status == "deprecated" and not entry["deprecated_by"]:
        errors.append(f"{label}: deprecated capability requires deprecated_by")
    if status != "deprecated" and entry["deprecated_by"] is not None:
        errors.append(f"{label}: active capability cannot declare deprecated_by")
    for field in (
        "description",
        "changes",
        "primary_user",
        "trigger",
        "authority_boundary",
    ):
        if not isinstance(entry[field], str) or not entry[field].strip():
            errors.append(f"{label}: {field} must be a non-empty string")
    for field in (
        "secondary_audience",
        "minimum_inputs",
        "outputs",
        "success_signals",
        "stop_conditions",
    ):
        value = entry[field]
        if (
            not isinstance(value, list)
            or not value
            or any(not isinstance(item, str) or not item.strip() for item in value)
        ):
            errors.append(f"{label}: {field} must be a non-empty string array")
    evidence_contract = entry["evidence_contract"]
    if not isinstance(evidence_contract, dict):
        errors.append(f"{label}: evidence_contract must be an object")
    else:
        if set(evidence_contract) != {"required_sections", "policy"}:
            errors.append(f"{label}: evidence_contract fields do not match the contract")
        required_sections = evidence_contract.get("required_sections")
        if (
            not isinstance(required_sections, list)
            or not required_sections
            or any(
                not isinstance(item, str) or not item.strip()
                for item in required_sections
            )
        ):
            errors.append(
                f"{label}: evidence_contract.required_sections must be a non-empty string array"
            )
        if not isinstance(evidence_contract.get("policy"), str) or not evidence_contract[
            "policy"
        ].strip():
            errors.append(f"{label}: evidence_contract.policy must be non-empty")
    compatibility = entry["compatibility"]
    if not isinstance(compatibility, dict):
        errors.append(f"{label}: compatibility must be an object")
    else:
        required_compatibility = {
            "semantic_versioning",
            "legacy_status_field",
            "migration",
        }
        if set(compatibility) != required_compatibility:
            errors.append(f"{label}: compatibility fields do not match the contract")
        if compatibility.get("semantic_versioning") is not True:
            errors.append(f"{label}: compatibility.semantic_versioning must be true")
        for field in ("legacy_status_field", "migration"):
            if not isinstance(compatibility.get(field), str) or not compatibility[
                field
            ].strip():
                errors.append(f"{label}: compatibility.{field} must be non-empty")
    path = root / str(entry["path"])
    if not path.exists():
        errors.append(f"{label}: path does not exist: {entry['path']}")
    description = str(entry["description"])
    trigger = str(entry["trigger"])
    if not description.strip() or not trigger.strip():
        errors.append(f"{label}: description and trigger must be non-empty")
    elif not (terms(description) & terms(trigger)):
        errors.append(f"{label}: description and trigger have no shared semantic term")
    projection = entry["projection"]
    if not isinstance(projection, dict):
        errors.append(f"{label}: projection must be an object")
    else:
        source = root / str(projection.get("source_registry", ""))
        if not source.exists():
            errors.append(f"{label}: source registry does not exist")
        legacy = projection.get("legacy_record")
        if not isinstance(legacy, dict):
            errors.append(f"{label}: projection.legacy_record must be an object")
        elif not str(legacy.get("status", "")).strip():
            errors.append(f"{label}: legacy status compatibility field is missing")
    if "downstream_adoption_status" in json.dumps(entry, ensure_ascii=False):
        errors.append(f"{label}: canonical public capability must not contain downstream adoption state")
    return errors


def native_description_errors(
    root: Path, capabilities: list[dict[str, Any]]
) -> list[str]:
    errors: list[str] = []
    for entry in capabilities:
        if entry["record_type"] == "skill":
            text = (root / entry["path"]).read_text(encoding="utf-8")
            match = re.search(r"(?m)^description:\s*(.+)$", text)
            value = match.group(1).strip() if match else ""
            if value.startswith(("'", '"')) and value.endswith(value[0]):
                value = value[1:-1]
            if value != entry["description"]:
                errors.append(f"{entry['capability_id']}: native Skill description drift")
        elif entry["record_type"] == "agent":
            legacy = entry["projection"]["legacy_record"]
            record = load_json(root / str(legacy["path"]))
            if record.get("description") != entry["description"]:
                errors.append(f"{entry['capability_id']}: native Agent description drift")
    return errors


def deprecated_reference_errors(
    root: Path, capabilities: list[dict[str, Any]]
) -> list[str]:
    deprecated = {
        str(entry["family_name"])
        for entry in capabilities
        if entry["public_package_status"] == "deprecated"
    }
    if not deprecated:
        return []
    errors: list[str] = []
    for route in load_jsonl(root / "registry" / "capability-routing.index.jsonl"):
        if route.get("skill_id") in deprecated:
            errors.append(
                f"active routing entry {route.get('route_id')} references deprecated capability {route.get('skill_id')}"
            )
    for entry in capabilities:
        if entry["capability_role"] != "capability_profile":
            continue
        skills = entry["projection"]["legacy_record"].get("skills", [])
        for name in skills:
            if str(name).split("@", 1)[0] in deprecated:
                errors.append(
                    f"active profile {entry['capability_id']} references deprecated capability {name}"
                )
    return errors


def projection_errors(root: Path, manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for relative, expected in build_projections(root, manifest).items():
        path = root / relative
        actual = path.read_text(encoding="utf-8") if path.exists() else ""
        if actual != expected:
            errors.append(f"projection drift: {relative}")
    return errors


def validate_manifest(root: Path, manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required_top_level = {
        "contract",
        "contract_version",
        "public_package_status_contract",
        "capability_roles",
        "capabilities",
    }
    if set(manifest) != required_top_level:
        missing = sorted(required_top_level - set(manifest))
        extra = sorted(set(manifest) - required_top_level)
        if missing:
            errors.append(f"manifest missing fields: {', '.join(missing)}")
        if extra:
            errors.append(f"manifest has unknown fields: {', '.join(extra)}")
    if manifest.get("contract") != "lat.canonical-capability-manifest.v1":
        errors.append("manifest contract must be lat.canonical-capability-manifest.v1")
    if manifest.get("contract_version") != "1.0.0":
        errors.append("manifest contract_version must be 1.0.0")
    if (
        manifest.get("public_package_status_contract")
        != "schemas/capability/public-package-lifecycle.v1.schema.json"
    ):
        errors.append("manifest public package lifecycle contract path is invalid")
    if set(manifest.get("capability_roles", [])) != ROLES:
        errors.append("manifest capability_roles do not match the canonical set")
    capabilities = manifest.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        return errors + ["manifest capabilities must be a non-empty array"]
    ids: set[str] = set()
    families: set[tuple[str, str]] = set()
    for index, entry in enumerate(capabilities):
        label = f"capabilities[{index}]"
        errors.extend(validate_entry(entry, root, label))
        if not isinstance(entry, dict):
            continue
        capability_id = str(entry.get("capability_id", ""))
        family_key = (str(entry.get("record_type", "")), str(entry.get("family_name", "")))
        if capability_id in ids:
            errors.append(f"{label}: duplicate capability_id {capability_id}")
        ids.add(capability_id)
        if family_key in families:
            errors.append(f"{label}: duplicate active family {family_key[0]}:{family_key[1]}")
        families.add(family_key)
    valid_entries = [entry for entry in capabilities if isinstance(entry, dict)]
    errors.extend(native_description_errors(root, valid_entries))
    errors.extend(deprecated_reference_errors(root, valid_entries))
    errors.extend(projection_errors(root, manifest))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    try:
        manifest = load_json(root / "registry" / "capability-manifest.json")
        errors = validate_manifest(root, manifest)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"validated {len(manifest['capabilities'])} canonical capability record(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
