#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate a downstream consumer and its declared private extensions locally."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from downstream_contracts import (
    CAPABILITY_ID_RE,
    FLOATING_REFS,
    SHA_RE,
    canonical_capabilities,
    exact_fields,
    load_json,
    nonempty_string,
    safe_relative_path,
    string_array,
    validate_extension,
)


def validate_consumer(
    manifest: dict[str, Any],
    lattice_root: Path,
    consumer_root: Path,
    *,
    validate_extension_files: bool = True,
    verify_checkout_pin: bool = False,
) -> list[str]:
    required = {
        "contract",
        "contract_version",
        "consumer_id",
        "consumer_repository",
        "simulation_status",
        "lattice_source",
        "contract_versions",
        "capability_profiles",
        "public_capabilities",
        "private_extensions",
        "evidence_storage",
        "manager_projection",
        "validation_commands",
        "compatibility_policy",
    }
    errors = exact_fields(manifest, required, "consumer manifest")
    if errors:
        return errors
    if manifest["contract"] != "lat.downstream-consumer-manifest.v1":
        errors.append("consumer manifest: invalid contract")
    if manifest["contract_version"] != "1.0.0":
        errors.append("consumer manifest: unsupported contract_version")
    if str(manifest["consumer_id"]).lower() in {"lat", "lattice"}:
        errors.append("consumer manifest: consumer_id cannot use the public project identity")
    errors.extend(
        exact_fields(
            manifest["consumer_repository"],
            {"repository_id", "visibility"},
            "consumer_repository",
        )
    )
    if isinstance(manifest["consumer_repository"], dict):
        if not nonempty_string(manifest["consumer_repository"].get("repository_id")):
            errors.append("consumer_repository: repository_id must be non-empty")
        if manifest["consumer_repository"].get("visibility") != "private":
            errors.append("consumer_repository: visibility must be private")
    if manifest["simulation_status"] not in {
        "synthetic_reference",
        "real_downstream",
    }:
        errors.append("consumer manifest: invalid simulation_status")
    source = manifest["lattice_source"]
    errors.extend(
        exact_fields(source, {"repository", "ref", "commit_sha"}, "lattice_source")
    )
    if isinstance(source, dict):
        ref = str(source.get("ref", ""))
        sha = str(source.get("commit_sha", ""))
        if ref.lower() in FLOATING_REFS or ref.startswith("refs/heads/"):
            errors.append("lattice_source: ref must be an immutable tag or full commit SHA")
        if not SHA_RE.fullmatch(sha):
            errors.append("lattice_source: commit_sha must be a full lowercase SHA")
        if SHA_RE.fullmatch(ref) and ref != sha:
            errors.append("lattice_source: SHA ref and commit_sha must match")
        if not nonempty_string(source.get("repository")):
            errors.append("lattice_source: repository must be non-empty")
        if (
            verify_checkout_pin
            and manifest["simulation_status"] == "real_downstream"
            and SHA_RE.fullmatch(sha)
        ):
            try:
                checkout_sha = subprocess.run(
                    ["git", "-C", str(lattice_root), "rev-parse", "HEAD"],
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip()
            except (OSError, subprocess.CalledProcessError):
                errors.append(
                    "lattice_source: pinned checkout commit could not be verified locally"
                )
            else:
                if checkout_sha != sha:
                    errors.append(
                        "lattice_source: commit_sha does not match the local Lattice checkout"
                    )
            if not SHA_RE.fullmatch(ref):
                try:
                    tag_sha = subprocess.run(
                        [
                            "git",
                            "-C",
                            str(lattice_root),
                            "rev-parse",
                            f"refs/tags/{ref}^{{commit}}",
                        ],
                        check=True,
                        capture_output=True,
                        text=True,
                    ).stdout.strip()
                except (OSError, subprocess.CalledProcessError):
                    errors.append(
                        f"lattice_source: immutable tag does not exist locally: {ref}"
                    )
                else:
                    if tag_sha != sha:
                        errors.append(
                            "lattice_source: tag and commit_sha resolve to different commits"
                        )
    versions = manifest["contract_versions"]
    required_contract_versions = {
        "lat.canonical-capability-manifest.v1": "1.0.0",
        "lat.downstream-adoption-lifecycle.v1": "1.0.0",
        "lat.downstream-consumer-manifest.v1": "1.0.0",
        "lat.delivery-evidence-asset-pack.v1": "1.0.0",
        "lat.evidence-claim.v1": "1.0.0",
        "lat.manager-delivery-brief.v1": "1.0.0",
    }
    if manifest["private_extensions"]:
        required_contract_versions["lat.private-capability-extension.v1"] = "1.0.0"
    if not isinstance(versions, dict) or not versions:
        errors.append("contract_versions must be a non-empty object")
    elif any(
        not nonempty_string(name) or not isinstance(version, str)
        for name, version in versions.items()
    ):
        errors.append("contract_versions must map contract names to versions")
    else:
        for contract, supported_version in required_contract_versions.items():
            if versions.get(contract) != supported_version:
                errors.append(
                    f"contract_versions: {contract} must be pinned to {supported_version}"
                )
    capabilities = canonical_capabilities(lattice_root)
    selected: set[str] = set()
    profile_ids: set[str] = set()
    for field, require_profile in (
        ("capability_profiles", True),
        ("public_capabilities", False),
    ):
        records = manifest[field]
        if not isinstance(records, list) or (field == "public_capabilities" and not records):
            errors.append(f"{field} must be a {'non-empty ' if field == 'public_capabilities' else ''}array")
            continue
        for index, record in enumerate(records):
            label = f"{field}[{index}]"
            item_errors = exact_fields(record, {"capability_id", "purpose"}, label)
            errors.extend(item_errors)
            if item_errors:
                continue
            capability_id = str(record["capability_id"])
            if "*" in capability_id or not CAPABILITY_ID_RE.fullmatch(capability_id):
                errors.append(f"{label}: capability_id must be one exact version")
                continue
            if capability_id in selected:
                errors.append(f"{label}: duplicate capability selection {capability_id}")
            selected.add(capability_id)
            capability = capabilities.get(capability_id)
            if capability is None:
                errors.append(f"{label}: capability version does not exist: {capability_id}")
                continue
            if capability["public_package_status"] in {"draft", "deprecated"}:
                errors.append(f"{label}: capability is not dependency-ready: {capability_id}")
            if require_profile and capability["capability_role"] != "capability_profile":
                errors.append(f"{label}: selected capability is not a capability_profile")
            if require_profile:
                profile_ids.add(capability_id)
            if not nonempty_string(record["purpose"]):
                errors.append(f"{label}: purpose must be non-empty")
    if len(selected) > 20:
        errors.append("consumer manifest: broad capability loading exceeds the bounded maximum of 20")
    extension_refs = manifest["private_extensions"]
    if not isinstance(extension_refs, list):
        errors.append("private_extensions must be an array")
        extension_refs = []
    for index, reference in enumerate(extension_refs):
        label = f"private_extensions[{index}]"
        item_errors = exact_fields(reference, {"extension_id", "manifest_path"}, label)
        errors.extend(item_errors)
        if item_errors:
            continue
        if not safe_relative_path(reference["manifest_path"]):
            errors.append(f"{label}: manifest_path must be a safe relative path")
            continue
        if not validate_extension_files:
            continue
        path = consumer_root / reference["manifest_path"]
        if not path.is_file():
            errors.append(f"{label}: extension manifest does not exist: {reference['manifest_path']}")
            continue
        extension = load_json(path)
        if extension.get("extension_id") != reference["extension_id"]:
            errors.append(f"{label}: extension_id does not match the extension manifest")
        errors.extend(
            f"{label}: {error}"
            for error in validate_extension(
                extension, capabilities, selected_capabilities=selected
            )
        )
    evidence = manifest["evidence_storage"]
    errors.extend(
        exact_fields(
            evidence,
            {"root", "classification", "public_upload_prohibited"},
            "evidence_storage",
        )
    )
    if isinstance(evidence, dict):
        if not safe_relative_path(evidence.get("root")):
            errors.append("evidence_storage: root must be a safe relative path")
        if evidence.get("classification") not in {
            "synthetic",
            "real_sanitized",
            "real_restricted",
        }:
            errors.append("evidence_storage: invalid classification")
        if evidence.get("public_upload_prohibited") is not True:
            errors.append("evidence_storage: public upload must be prohibited")
    projection = manifest["manager_projection"]
    errors.extend(
        exact_fields(
            projection,
            {"asset_pack_root", "brief_path", "human_review_required"},
            "manager_projection",
        )
    )
    if isinstance(projection, dict):
        for field in ("asset_pack_root", "brief_path"):
            if not safe_relative_path(projection.get(field)):
                errors.append(f"manager_projection: {field} must be a safe relative path")
        if projection.get("human_review_required") is not True:
            errors.append("manager_projection: human review must be required")
    if not string_array(manifest["validation_commands"], minimum=3):
        errors.append("validation_commands must contain at least three local commands")
    policy = manifest["compatibility_policy"]
    errors.extend(
        exact_fields(
            policy,
            {
                "missing_capability",
                "deprecated_capability",
                "major_version_change",
                "authority_change",
            },
            "compatibility_policy",
        )
    )
    if isinstance(policy, dict):
        if policy.get("missing_capability") != "fail":
            errors.append("compatibility_policy: missing_capability must fail")
        if policy.get("major_version_change") != "human_review":
            errors.append("compatibility_policy: major version changes require human review")
        if policy.get("authority_change") != "human_review":
            errors.append("compatibility_policy: authority changes require human review")
        if policy.get("deprecated_capability") not in {"fail", "human_review"}:
            errors.append("compatibility_policy: invalid deprecated capability policy")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest")
    parser.add_argument("--lattice-root", default=".")
    parser.add_argument("--consumer-root")
    parser.add_argument("--skip-extension-files", action="store_true")
    args = parser.parse_args()
    manifest_path = Path(args.manifest).resolve()
    lattice_root = Path(args.lattice_root).resolve()
    consumer_root = (
        Path(args.consumer_root).resolve()
        if args.consumer_root
        else manifest_path.parent
    )
    try:
        manifest = load_json(manifest_path)
        errors = validate_consumer(
            manifest,
            lattice_root,
            consumer_root,
            validate_extension_files=not args.skip_extension_files,
            verify_checkout_pin=True,
        )
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(
        f"validated downstream consumer {manifest['consumer_id']} locally; no evidence upload performed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
