#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Shared local-only validation helpers for downstream contracts."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
TAG_RE = re.compile(r"^v?[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")
CAPABILITY_ID_RE = re.compile(
    r"^(skill|agent|mcp|knowledge|workspace):"
    r"[a-z0-9][a-z0-9-]*@[0-9]+\.[0-9]+\.[0-9]+$"
)
EXTENSION_ID_RE = re.compile(
    r"^private:([a-z][a-z0-9-]*)/([a-z0-9][a-z0-9-]*)@"
    r"([0-9]+\.[0-9]+\.[0-9]+)$"
)
FLOATING_REFS = {"main", "master", "head", "develop", "development", "latest"}
ADOPTION_STATUSES = {
    "not_observed",
    "imported",
    "task_scoped",
    "used_once",
    "reused",
    "team_available",
    "deprecated",
}
EVIDENCE_ORIGINS = {"synthetic", "real_sanitized", "real_restricted"}
CLAIM_CLASSES = {"OBSERVED", "DERIVED", "JUDGED", "UNKNOWN"}
CLAIM_KINDS = {
    "current_delivery",
    "reusable_asset",
    "before_state",
    "after_state",
    "human_challenge",
    "limitation",
    "next_use",
    "reuse",
    "team_adoption",
    "manager_acceptance",
    "roi",
    "other",
}
UNKNOWN_STATEMENT_MARKERS = (
    "unknown",
    "not established",
    "not observed",
    "not available",
    "not proven",
    "unproven",
    "no evidence",
    "insufficient evidence",
    "cannot be established",
    "cannot be determined",
    "remains uncertain",
)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_number}: expected JSON object")
        records.append(value)
    return records


def exact_fields(
    value: Any, required: set[str], label: str, *, optional: set[str] | None = None
) -> list[str]:
    if not isinstance(value, dict):
        return [f"{label}: expected object"]
    optional = optional or set()
    errors: list[str] = []
    missing = sorted(required - set(value))
    extra = sorted(set(value) - required - optional)
    if missing:
        errors.append(f"{label}: missing fields: {', '.join(missing)}")
    if extra:
        errors.append(f"{label}: unknown fields: {', '.join(extra)}")
    return errors


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def string_array(value: Any, *, minimum: int = 0) -> bool:
    return (
        isinstance(value, list)
        and len(value) >= minimum
        and all(nonempty_string(item) for item in value)
    )


def safe_relative_path(value: Any) -> bool:
    if not nonempty_string(value):
        return False
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts


def canonical_capabilities(lattice_root: Path) -> dict[str, dict[str, Any]]:
    manifest = load_json(lattice_root / "registry" / "capability-manifest.json")
    return {
        str(record["capability_id"]): record
        for record in manifest.get("capabilities", [])
        if isinstance(record, dict) and "capability_id" in record
    }


def validate_extension(
    extension: dict[str, Any],
    capabilities: dict[str, dict[str, Any]],
    *,
    selected_capabilities: set[str] | None = None,
) -> list[str]:
    required = {
        "contract",
        "contract_version",
        "extension_id",
        "extension_version",
        "private_namespace",
        "simulation_status",
        "relationship",
        "public_capability_id",
        "scope",
        "required_permissions",
        "authority_boundary",
        "preserves_public_safety_boundaries",
        "compatibility",
        "governance_review_ref",
        "content_path",
    }
    errors = exact_fields(extension, required, "private extension")
    if errors:
        return errors
    if extension["contract"] != "lat.private-capability-extension.v1":
        errors.append("private extension: invalid contract")
    if extension["contract_version"] != "1.0.0":
        errors.append("private extension: unsupported contract_version")
    match = EXTENSION_ID_RE.fullmatch(str(extension["extension_id"]))
    namespace = str(extension["private_namespace"])
    version = str(extension["extension_version"])
    if not match:
        errors.append("private extension: extension_id must use private:<namespace>/<name>@<semver>")
    else:
        if match.group(1) != namespace:
            errors.append("private extension: extension_id namespace mismatch")
        if match.group(3) != version:
            errors.append("private extension: extension_id version mismatch")
    if namespace in {"lat", "lattice"}:
        errors.append("private extension: public lat or lattice namespace is prohibited")
    if not SEMVER_RE.fullmatch(version):
        errors.append("private extension: invalid extension_version")
    if extension["simulation_status"] not in {
        "synthetic_reference",
        "real_downstream",
    }:
        errors.append("private extension: invalid simulation_status")
    relationship = extension["relationship"]
    if relationship not in {"extends", "overrides", "composes"}:
        errors.append("private extension: invalid relationship")
    public_id = str(extension["public_capability_id"])
    if not CAPABILITY_ID_RE.fullmatch(public_id) or public_id not in capabilities:
        errors.append(f"private extension: public capability version does not exist: {public_id}")
    elif capabilities[public_id]["public_package_status"] in {"draft", "deprecated"}:
        errors.append(f"private extension: public capability is not dependency-ready: {public_id}")
    if selected_capabilities is not None and public_id not in selected_capabilities:
        errors.append("private extension: referenced public capability is not selected")
    if relationship == "overrides" and not nonempty_string(
        extension["governance_review_ref"]
    ):
        errors.append("private extension: overrides require governance_review_ref")
    if extension["preserves_public_safety_boundaries"] is not True:
        errors.append("private extension: public safety and authority boundaries must be preserved")
    if not nonempty_string(extension["authority_boundary"]):
        errors.append("private extension: authority_boundary must be non-empty")
    if not string_array(extension["required_permissions"]):
        errors.append("private extension: required_permissions must be a string array")
    if not safe_relative_path(extension["content_path"]):
        errors.append("private extension: content_path must be a safe relative path")
    errors.extend(
        exact_fields(
            extension["scope"],
            {"repositories", "task_types", "excluded_uses"},
            "private extension scope",
        )
    )
    if isinstance(extension["scope"], dict):
        if not string_array(extension["scope"].get("repositories"), minimum=1):
            errors.append("private extension: scope.repositories must be non-empty")
        if not string_array(extension["scope"].get("task_types"), minimum=1):
            errors.append("private extension: scope.task_types must be non-empty")
        if not string_array(extension["scope"].get("excluded_uses")):
            errors.append("private extension: scope.excluded_uses must be a string array")
    errors.extend(
        exact_fields(
            extension["compatibility"],
            {"public_version_range", "on_incompatible"},
            "private extension compatibility",
        )
    )
    if isinstance(extension["compatibility"], dict):
        if not nonempty_string(extension["compatibility"].get("public_version_range")):
            errors.append("private extension: public_version_range must be non-empty")
        if extension["compatibility"].get("on_incompatible") not in {
            "fail",
            "human_review",
        }:
            errors.append("private extension: invalid on_incompatible policy")
    forbidden = {
        "public_package_status",
        "release_channel",
        "public_conformance_status",
    }
    if forbidden & set(extension):
        errors.append("private extension: cannot impersonate a public package")
    return errors


def validate_claim(claim: dict[str, Any], evidence_ids: set[str]) -> list[str]:
    required = {
        "claim_id",
        "classification",
        "claim_kind",
        "statement",
        "presentation",
        "evidence_refs",
        "evidence_origin",
        "scope",
        "method",
        "judgment_owner",
        "unknown_reason",
        "limitations",
        "approval_authority",
    }
    label = f"claim {claim.get('claim_id', '<missing>')}"
    errors = exact_fields(claim, required, label)
    if errors:
        return errors
    classification = claim["classification"]
    refs = claim["evidence_refs"]
    if classification not in CLAIM_CLASSES:
        errors.append(f"{label}: invalid classification")
    if claim["claim_kind"] not in CLAIM_KINDS:
        errors.append(f"{label}: invalid claim_kind")
    if not nonempty_string(claim["statement"]) or not nonempty_string(claim["scope"]):
        errors.append(f"{label}: statement and scope must be non-empty")
    if not isinstance(refs, list) or any(not nonempty_string(ref) for ref in refs):
        errors.append(f"{label}: evidence_refs must be a string array")
        refs = []
    elif len(set(map(str, refs))) != len(refs):
        errors.append(f"{label}: evidence_refs must not contain duplicates")
    if classification in {"OBSERVED", "DERIVED", "JUDGED"} and not refs:
        errors.append(f"{label}: {classification} requires evidence_refs")
    dangling = sorted(set(map(str, refs)) - evidence_ids)
    if dangling:
        errors.append(f"{label}: dangling evidence refs: {', '.join(dangling)}")
    if classification == "DERIVED" and not nonempty_string(claim["method"]):
        errors.append(f"{label}: DERIVED requires a declared method")
    if classification == "JUDGED" and not nonempty_string(claim["judgment_owner"]):
        errors.append(f"{label}: JUDGED requires a judgment_owner")
    if classification == "UNKNOWN":
        if claim["presentation"] != "unknown":
            errors.append(f"{label}: UNKNOWN cannot be presented as fact")
        if not nonempty_string(claim["unknown_reason"]):
            errors.append(f"{label}: UNKNOWN requires unknown_reason")
        statement = str(claim["statement"]).lower()
        if not (
            statement.strip().startswith("no ")
            or any(marker in statement for marker in UNKNOWN_STATEMENT_MARKERS)
        ):
            errors.append(
                f"{label}: UNKNOWN statement must visibly communicate uncertainty"
            )
    if claim["presentation"] not in {"fact", "qualified", "unknown"}:
        errors.append(f"{label}: invalid presentation")
    if claim["evidence_origin"] not in EVIDENCE_ORIGINS:
        errors.append(f"{label}: invalid evidence_origin")
    if not string_array(claim["limitations"]):
        errors.append(f"{label}: limitations must be a string array")
    authority = str(claim["approval_authority"] or "").lower()
    if "deliveryyield" in authority or "delivery_yield" in authority:
        errors.append(f"{label}: DeliveryYield cannot be an approval authority")
    return errors
