#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate a Manager-Ready Delivery Asset Pack locally."""

from __future__ import annotations

import argparse
import json
import subprocess
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
    FLOATING_REFS,
    SEMVER_RE,
    SHA_RE,
    TAG_RE,
    canonical_capabilities,
    exact_fields,
    load_json,
    load_jsonl,
    nonempty_string,
    safe_relative_path,
    string_array,
)
from validate_manager_claims import (
    validate_manager_brief,
    validate_rendered_manager_brief,
)

REPORT_CHECKS = [
    "artifact_presence",
    "cross_file_identity",
    "evidence_references",
    "manager_claims",
    "rendered_brief_parity",
    "authority_boundaries",
]


def validate_validation_report(
    report: dict[str, Any], manifest: dict[str, Any]
) -> list[str]:
    required = {
        "contract",
        "schema_version",
        "status",
        "pack_id",
        "checks",
        "errors",
        "generated_at",
        "simulation_status",
        "downstream_adoption_status",
        "privacy_note",
    }
    errors = exact_fields(
        report, required, "validation report", optional={"negative_cases"}
    )
    if errors:
        return errors
    if report["contract"] != "lat.delivery-asset-pack-validation-report.v1":
        errors.append("validation report: invalid contract")
    if report["schema_version"] != "1.0.0":
        errors.append("validation report: unsupported schema_version")
    if report["status"] not in {"pass", "fail"}:
        errors.append("validation report: invalid status")
    if report["pack_id"] != manifest["pack_id"]:
        errors.append("validation report: pack ID does not match manifest")
    if report["simulation_status"] != manifest["simulation_status"]:
        errors.append("validation report: simulation status does not match manifest")
    if (
        report["downstream_adoption_status"]
        != manifest["downstream_adoption_status"]
    ):
        errors.append("validation report: adoption status does not match manifest")
    if not string_array(report["checks"], minimum=1):
        errors.append("validation report: checks must be a non-empty string array")
    elif len(set(report["checks"])) != len(report["checks"]):
        errors.append("validation report: checks must not contain duplicates")
    if not isinstance(report["errors"], list) or any(
        not nonempty_string(item) for item in report["errors"]
    ):
        errors.append("validation report: errors must be a string array")
    if report["status"] == "pass" and report["errors"]:
        errors.append("validation report: pass status cannot contain errors")
    if report["status"] == "fail" and not report["errors"]:
        errors.append("validation report: fail status requires errors")
    if not nonempty_string(report["generated_at"]) or not nonempty_string(
        report["privacy_note"]
    ):
        errors.append(
            "validation report: generated_at and privacy_note must be non-empty"
        )
    if "negative_cases" in report and not string_array(report["negative_cases"]):
        errors.append("validation report: negative_cases must be a string array")
    return errors


def validate_asset_pack(
    pack_root: Path,
    lattice_root: Path,
    *,
    allow_missing_validation_report: bool = False,
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
    if not SEMVER_RE.fullmatch(str(manifest["pack_version"])):
        errors.append("asset pack manifest: pack_version must be semantic version")
    pin = manifest["lattice_pin"]
    errors.extend(exact_fields(pin, {"ref", "commit_sha"}, "lattice_pin"))
    if isinstance(pin, dict):
        ref = str(pin.get("ref", ""))
        sha = str(pin.get("commit_sha", ""))
        if not SHA_RE.fullmatch(sha):
            errors.append("lattice_pin: commit_sha must be a full lowercase SHA")
        if (
            ref.lower() in FLOATING_REFS
            or ref.startswith("refs/heads/")
            or not (SHA_RE.fullmatch(ref) or TAG_RE.fullmatch(ref))
        ):
            errors.append("lattice_pin: ref must be an immutable tag or full commit SHA")
        if SHA_RE.fullmatch(ref) and ref != sha:
            errors.append("lattice_pin: SHA ref and commit_sha must match")
        synthetic_sentinel = (
            manifest["simulation_status"] == "synthetic_reference"
            and ref == "v0.0.0-synthetic"
            and sha == "0" * 40
        )
        if not synthetic_sentinel and SHA_RE.fullmatch(sha):
            try:
                checkout_sha = subprocess.run(
                    ["git", "-C", str(lattice_root), "rev-parse", "HEAD"],
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip()
            except (OSError, subprocess.CalledProcessError):
                errors.append(
                    "lattice_pin: pinned checkout commit could not be verified locally"
                )
            else:
                if checkout_sha != sha:
                    errors.append(
                        "lattice_pin: commit_sha does not match the local Lattice checkout"
                    )
            if TAG_RE.fullmatch(ref):
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
                    errors.append(f"lattice_pin: immutable tag does not exist locally: {ref}")
                else:
                    if tag_sha != sha:
                        errors.append(
                            "lattice_pin: tag and commit_sha resolve to different commits"
                        )
    capabilities = canonical_capabilities(lattice_root)
    selected = manifest["public_capabilities"]
    if not isinstance(selected, list) or not selected:
        errors.append("asset pack manifest: public_capabilities must be non-empty")
        selected = []
    elif len(set(map(str, selected))) != len(selected):
        errors.append("asset pack manifest: public_capabilities must not contain duplicates")
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
    elif simulation == "real_downstream" and origin == "synthetic":
        errors.append(
            "asset pack manifest: real downstream pack cannot use synthetic evidence"
        )
    elif simulation != "real_downstream":
        errors.append("asset pack manifest: invalid simulation_status")
    artifacts_required = {
        "feature_delivery_case",
        "evidence_ledger",
        "contribution_ledger",
        "reusable_asset_dossier",
        "manager_brief",
        "manager_brief_rendered",
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
            missing_report_allowed = (
                name == "validation_report" and allow_missing_validation_report
            )
            if not missing_report_allowed and not resolved[name].is_file():
                errors.append(f"asset pack artifacts: missing {relative}")
    evidence_records: list[dict[str, Any]] = []
    contribution_ids: set[str] = set()
    if resolved.get("evidence_ledger", Path()).is_file():
        evidence_records = load_jsonl(resolved["evidence_ledger"])
        for index, record in enumerate(evidence_records):
            if record.get("feature_delivery_case_id") != manifest[
                "feature_delivery_case_id"
            ]:
                errors.append(f"evidence[{index}]: feature delivery case mismatch")
            if record.get("evidence_origin") != origin:
                errors.append(f"evidence[{index}]: evidence origin differs from pack")
    if resolved.get("contribution_ledger", Path()).is_file():
        contributions = load_jsonl(resolved["contribution_ledger"])
        if not contributions:
            errors.append("asset pack: contribution ledger must not be empty")
        for index, record in enumerate(contributions):
            contribution_id = str(record.get("contribution_id", ""))
            if not nonempty_string(contribution_id):
                errors.append(f"contribution[{index}]: contribution_id must be non-empty")
            elif contribution_id in contribution_ids:
                errors.append(
                    f"contribution[{index}]: duplicate contribution_id {contribution_id}"
                )
            contribution_ids.add(contribution_id)
            if record.get("feature_delivery_case_id") != manifest["feature_delivery_case_id"]:
                errors.append(f"contribution[{index}]: feature delivery case mismatch")
            if record.get("simulation_status") != simulation:
                errors.append(f"contribution[{index}]: simulation status differs from pack")
    if resolved.get("feature_delivery_case", Path()).is_file():
        case = load_json(resolved["feature_delivery_case"])
        if case.get("case_id") != manifest["feature_delivery_case_id"]:
            errors.append("asset pack: feature-delivery-case ID does not match manifest")
    if resolved.get("manager_brief", Path()).is_file():
        brief = load_json(resolved["manager_brief"])
        if brief.get("asset_pack_id") != manifest["pack_id"]:
            errors.append("asset pack: manager brief pack ID does not match manifest")
        if brief.get("scope") != manifest["feature_delivery_case_id"]:
            errors.append("asset pack: manager brief scope does not match manifest")
        if brief.get("version") != manifest["pack_version"]:
            errors.append("asset pack: manager brief version does not match manifest")
        if brief.get("simulation_status") != simulation:
            errors.append("asset pack: manager brief simulation status does not match manifest")
        if brief.get("downstream_adoption_status") != adoption:
            errors.append("asset pack: manager brief adoption status does not match manifest")
        if brief.get("evidence_origin") != origin:
            errors.append("asset pack: manager brief evidence origin does not match manifest")
        errors.extend(validate_manager_brief(brief, evidence_records))
        rendered = resolved.get("manager_brief_rendered")
        if rendered is not None:
            errors.extend(validate_rendered_manager_brief(brief, rendered))
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
        asset_version = str(asset["asset_version"])
        if asset_id in asset_ids:
            errors.append(f"{label}: duplicate asset_id {asset_id}")
        asset_ids.add(asset_id)
        if not nonempty_string(asset_id) or not SEMVER_RE.fullmatch(asset_version):
            errors.append(f"{label}: asset_id and semantic asset_version are required")
        asset_paths: dict[str, Path] = {}
        for field in asset_fields - {"asset_id", "asset_version"}:
            relative = asset[field]
            if not safe_relative_path(relative):
                errors.append(f"{label}: {field} must be a safe relative path")
            elif not (pack_root / relative).is_file():
                errors.append(f"{label}: missing {relative}")
            else:
                asset_paths[field] = pack_root / relative
        manifest_file = asset_paths.get("manifest_path")
        if manifest_file:
            asset_manifest = load_json(manifest_file)
            expected_values = {
                "asset_id": asset_id,
                "asset_version": asset_version,
                "feature_delivery_case_id": manifest["feature_delivery_case_id"],
                "simulation_status": simulation,
                "downstream_adoption_status": adoption,
            }
            for field, expected in expected_values.items():
                if asset_manifest.get(field) != expected:
                    errors.append(f"{label}: asset manifest {field} mismatch")
            contribution_refs = asset_manifest.get(
                "created_from_contribution_refs", []
            )
            if not isinstance(contribution_refs, list):
                errors.append(
                    f"{label}: asset manifest contribution refs must be an array"
                )
            else:
                dangling_contributions = sorted(
                    set(map(str, contribution_refs)) - contribution_ids
                )
                if dangling_contributions:
                    errors.append(
                        f"{label}: asset manifest dangling contribution refs: "
                        + ", ".join(dangling_contributions)
                    )
            if (
                simulation == "synthetic_reference"
                and asset_manifest.get("activation_mode") != "never_by_default"
            ):
                errors.append(
                    f"{label}: synthetic asset activation must remain never_by_default"
                )
        linked_records: dict[str, dict[str, Any]] = {}
        for path_field, record_label in (
            ("change_proposal_path", "change proposal"),
            ("review_path", "review"),
        ):
            record_path = asset_paths.get(path_field)
            if not record_path:
                continue
            record = load_json(record_path)
            linked_records[record_label] = record
            for field, expected in (
                ("asset_id", asset_id),
                ("simulation_status", simulation),
                ("downstream_adoption_status", adoption),
            ):
                if record.get(field) != expected:
                    errors.append(f"{label}: {record_label} {field} mismatch")
            refs = record.get("evidence_refs", [])
            if not isinstance(refs, list):
                errors.append(f"{label}: {record_label} evidence_refs must be an array")
            else:
                evidence_ids = {
                    str(item.get("evidence_id")) for item in evidence_records
                }
                dangling = sorted(set(map(str, refs)) - evidence_ids)
                if dangling:
                    errors.append(
                        f"{label}: {record_label} dangling evidence refs: "
                        + ", ".join(dangling)
                    )
            if simulation == "synthetic_reference" and record_label == "review":
                if record.get("review_mode") != "synthetic_conformance":
                    errors.append(
                        f"{label}: synthetic review mode must be synthetic_conformance"
                    )
                if record.get("decision") != "format_validated":
                    errors.append(
                        f"{label}: synthetic review can validate format only"
                    )
                if record.get("human_review_claim") is not False:
                    errors.append(
                        f"{label}: synthetic review cannot claim real human review"
                    )
                if record.get("activation_approved") is not False:
                    errors.append(
                        f"{label}: synthetic review cannot approve activation"
                    )
        proposal = linked_records.get("change proposal")
        review = linked_records.get("review")
        if proposal and review and review.get("proposal_id") != proposal.get(
            "proposal_id"
        ):
            errors.append(f"{label}: review proposal_id mismatch")
        usage_path = asset_paths.get("usage_observations_path")
        if usage_path:
            usage = load_jsonl(usage_path)
            if simulation == "synthetic_reference" and usage:
                errors.append(f"{label}: synthetic asset cannot contain usage observations")
            minimum_usage = (
                2
                if adoption in {"reused", "team_available"}
                else 1
                if adoption == "used_once"
                else 0
            )
            if len(usage) < minimum_usage:
                errors.append(
                    f"{label}: adoption status {adoption} requires at least "
                    f"{minimum_usage} usage observation(s)"
                )
    report_path = resolved.get("validation_report")
    if report_path and report_path.is_file():
        report = load_json(report_path)
        errors.extend(validate_validation_report(report, manifest))
    return errors, manifest


def validation_report(
    errors: list[str], manifest: dict[str, Any] | None
) -> dict[str, Any]:
    return {
        "contract": "lat.delivery-asset-pack-validation-report.v1",
        "schema_version": "1.0.0",
        "status": "pass" if not errors else "fail",
        "pack_id": manifest.get("pack_id") if manifest else None,
        "checks": REPORT_CHECKS,
        "errors": errors,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "simulation_status": manifest.get("simulation_status") if manifest else None,
        "downstream_adoption_status": (
            manifest.get("downstream_adoption_status") if manifest else None
        ),
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
            pack_root,
            Path(args.lattice_root).resolve(),
            allow_missing_validation_report=True,
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
    if not errors and report_path:
        final_errors, _ = validate_asset_pack(
            pack_root, Path(args.lattice_root).resolve()
        )
        if final_errors:
            errors.extend(final_errors)
            report = validation_report(errors, manifest)
            report_path.write_text(
                json.dumps(report, indent=2) + "\n", encoding="utf-8"
            )
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
