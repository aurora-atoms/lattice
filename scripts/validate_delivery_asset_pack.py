#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate a Manager-Ready Delivery Asset Pack locally."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from downstream_contracts import (
    ADOPTION_STATUSES,
    CAPABILITY_ID_RE,
    EVIDENCE_ORIGINS,
    SHA_RE,
    canonical_capabilities,
    exact_fields,
    load_json,
    load_jsonl,
    nonempty_string,
    safe_relative_path,
    string_array,
)
from validate_manager_claims import validate_manager_brief


def validate_asset_pack(
    pack_root: Path, lattice_root: Path
) -> tuple[list[str], dict[str, Any] | None]:
    manifest_path = pack_root / "asset-pack.manifest.json"
    if not manifest_path.is_file():
        return ["asset pack: missing asset-pack.manifest.json"], None
    manifest = load_json(manifest_path)
    required = {
        "contract",
        "contract_version",
        "pack_id",
        "pack_version",
        "simulation_status",
        "downstream_adoption_status",
        "feature_delivery_case_id",
        "accountable_owner",
        "lattice_pin",
        "public_capabilities",
        "evidence_origin",
        "artifacts",
        "reusable_assets",
        "generated_at",
    }
    errors = exact_fields(manifest, required, "asset pack manifest")
    if errors:
        return errors, manifest
    if manifest["contract"] != "lat.delivery-evidence-asset-pack.v1":
        errors.append("asset pack manifest: invalid contract")
    if manifest["contract_version"] != "1.0.0":
        errors.append("asset pack manifest: unsupported contract_version")
    if not nonempty_string(manifest["pack_id"]) or not nonempty_string(
        manifest["accountable_owner"]
    ):
        errors.append("asset pack manifest: pack_id and accountable_owner must be non-empty")
    pin = manifest["lattice_pin"]
    errors.extend(exact_fields(pin, {"ref", "commit_sha"}, "lattice_pin"))
    if isinstance(pin, dict) and not SHA_RE.fullmatch(str(pin.get("commit_sha", ""))):
        errors.append("lattice_pin: commit_sha must be a full lowercase SHA")
    capabilities = canonical_capabilities(lattice_root)
    selected = manifest["public_capabilities"]
    if not isinstance(selected, list) or not selected:
        errors.append("asset pack manifest: public_capabilities must be non-empty")
        selected = []
    for capability_id in selected:
        if (
            not isinstance(capability_id, str)
            or not CAPABILITY_ID_RE.fullmatch(capability_id)
            or capability_id not in capabilities
        ):
            errors.append(f"asset pack manifest: unknown public capability {capability_id}")
    simulation = manifest["simulation_status"]
    adoption = manifest["downstream_adoption_status"]
    origin = manifest["evidence_origin"]
    if adoption not in ADOPTION_STATUSES:
        errors.append("asset pack manifest: invalid downstream_adoption_status")
    if origin not in EVIDENCE_ORIGINS:
        errors.append("asset pack manifest: invalid evidence_origin")
    if simulation == "synthetic_reference":
        if adoption != "not_observed":
            errors.append("asset pack manifest: synthetic pack must remain not_observed")
        if origin != "synthetic":
            errors.append("asset pack manifest: synthetic pack must use synthetic evidence")
    elif simulation != "real_downstream":
        errors.append("asset pack manifest: invalid simulation_status")
    artifacts_required = {
        "feature_delivery_case",
        "evidence_ledger",
        "contribution_ledger",
        "reusable_asset_dossier",
        "manager_brief",
        "validation_report",
    }
    artifacts = manifest["artifacts"]
    errors.extend(exact_fields(artifacts, artifacts_required, "asset pack artifacts"))
    resolved: dict[str, Path] = {}
    if isinstance(artifacts, dict):
        for name, relative in artifacts.items():
            if not safe_relative_path(relative):
                errors.append(f"asset pack artifacts: {name} must be a safe relative path")
                continue
            resolved[name] = pack_root / relative
            if name != "validation_report" and not resolved[name].is_file():
                errors.append(f"asset pack artifacts: missing {relative}")
    evidence_records: list[dict[str, Any]] = []
    if resolved.get("evidence_ledger", Path()).is_file():
        evidence_records = load_jsonl(resolved["evidence_ledger"])
    if resolved.get("contribution_ledger", Path()).is_file():
        contributions = load_jsonl(resolved["contribution_ledger"])
        if not contributions:
            errors.append("asset pack: contribution ledger must not be empty")
        for index, record in enumerate(contributions):
            if not nonempty_string(record.get("contribution_id")):
                errors.append(f"contribution[{index}]: contribution_id must be non-empty")
            if record.get("feature_delivery_case_id") != manifest["feature_delivery_case_id"]:
                errors.append(f"contribution[{index}]: feature delivery case mismatch")
    if resolved.get("feature_delivery_case", Path()).is_file():
        case = load_json(resolved["feature_delivery_case"])
        if case.get("case_id") != manifest["feature_delivery_case_id"]:
            errors.append("asset pack: feature-delivery-case ID does not match manifest")
    if resolved.get("manager_brief", Path()).is_file():
        brief = load_json(resolved["manager_brief"])
        if brief.get("asset_pack_id") != manifest["pack_id"]:
            errors.append("asset pack: manager brief pack ID does not match manifest")
        if brief.get("downstream_adoption_status") != adoption:
            errors.append("asset pack: manager brief adoption status does not match manifest")
        errors.extend(validate_manager_brief(brief, evidence_records))
    reusable_assets = manifest["reusable_assets"]
    if not isinstance(reusable_assets, list) or not reusable_assets:
        errors.append("asset pack manifest: reusable_assets must be a non-empty array")
        reusable_assets = []
    asset_ids: set[str] = set()
    asset_fields = {
        "asset_id",
        "asset_version",
        "manifest_path",
        "change_proposal_path",
        "review_path",
        "usage_observations_path",
    }
    for index, asset in enumerate(reusable_assets):
        label = f"reusable_assets[{index}]"
        item_errors = exact_fields(asset, asset_fields, label)
        errors.extend(item_errors)
        if item_errors:
            continue
        asset_id = str(asset["asset_id"])
        if asset_id in asset_ids:
            errors.append(f"{label}: duplicate asset_id {asset_id}")
        asset_ids.add(asset_id)
        for field in asset_fields - {"asset_id", "asset_version"}:
            relative = asset[field]
            if not safe_relative_path(relative):
                errors.append(f"{label}: {field} must be a safe relative path")
            elif not (pack_root / relative).is_file():
                errors.append(f"{label}: missing {relative}")
    return errors, manifest


def validation_report(
    errors: list[str], manifest: dict[str, Any] | None
) -> dict[str, Any]:
    return {
        "contract": "lat.delivery-asset-pack-validation-report.v1",
        "status": "pass" if not errors else "fail",
        "pack_id": manifest.get("pack_id") if manifest else None,
        "checks": {
            "artifact_presence": "pass" if not any("missing" in item for item in errors) else "fail",
            "evidence_references": "pass" if not any("evidence ref" in item for item in errors) else "fail",
            "manager_claims": "pass" if not any("claim " in item for item in errors) else "fail",
            "authority_boundaries": "pass"
            if not any("authority" in item.lower() for item in errors)
            else "fail",
        },
        "errors": errors,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "privacy_note": "Local validation only; no evidence content was uploaded.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack_root")
    parser.add_argument("--lattice-root", default=".")
    parser.add_argument("--report-out")
    args = parser.parse_args()
    pack_root = Path(args.pack_root).resolve()
    try:
        errors, manifest = validate_asset_pack(
            pack_root, Path(args.lattice_root).resolve()
        )
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        errors, manifest = [str(exc)], None
    report = validation_report(errors, manifest)
    report_path: Path | None = None
    if args.report_out:
        report_path = Path(args.report_out)
    elif manifest and isinstance(manifest.get("artifacts"), dict):
        relative = manifest["artifacts"].get("validation_report")
        if safe_relative_path(relative):
            report_path = pack_root / relative
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(
        f"validated delivery asset pack {manifest['pack_id']} locally; no evidence upload performed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
