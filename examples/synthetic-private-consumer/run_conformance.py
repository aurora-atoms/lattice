#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate and validate the synthetic downstream Manager-Ready Delivery Asset Pack."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

GENERATED_AT = "2026-07-28T00:15:00Z"
PACK_ID = "SYNTHETIC-PACK-001"
CASE_ID = "synthetic_fdc_dangling_ref_001"
ASSET_ID = "dangling-evidence-ref-guard"
REQUIRED_NEGATIVE_CASES = {
    "dangling-evidence-ref",
    "synthetic-maturity-violation",
    "team-wide-overclaim",
    "unreviewed-promotion",
    "unsupported-private-extension",
}


def add_script_path(lattice_root: Path) -> None:
    scripts = lattice_root / "scripts"
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))


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


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def validate_asset_source(example_root: Path, review: dict[str, Any] | None = None) -> list[str]:
    asset_root = example_root / "inputs" / "reusable-assets" / ASSET_ID
    asset = load_json(asset_root / "asset-manifest.json")
    proposal = load_json(asset_root / "change-proposal.json")
    review = review or load_json(asset_root / "review.json")
    usage = load_jsonl(asset_root / "usage-observations.jsonl")
    errors: list[str] = []
    for label, record in (
        ("asset", asset),
        ("proposal", proposal),
        ("review", review),
    ):
        if record.get("simulation_status") != "synthetic_reference":
            errors.append(f"{label}: simulation_status must be synthetic_reference")
        if record.get("downstream_adoption_status") != "not_observed":
            errors.append(f"{label}: downstream adoption must remain not_observed")
    if asset.get("activation_mode") != "never_by_default":
        errors.append("asset: synthetic activation must remain never_by_default")
    if review.get("review_mode") != "synthetic_conformance":
        errors.append("review: review_mode must be synthetic_conformance")
    if review.get("decision") != "format_validated":
        errors.append("review: synthetic decision can validate format only")
    if review.get("human_review_claim") is not False:
        errors.append("review: synthetic fixture cannot claim real human review")
    if review.get("activation_approved") is not False:
        errors.append("review: synthetic review cannot approve activation")
    if usage:
        errors.append("usage observations must be empty while adoption is not_observed")
    return errors


def render_dossier() -> str:
    return """# Reusable Asset Dossier

Simulation status: `synthetic_reference`

Downstream adoption status: `not_observed`

## Asset

- ID: `dangling-evidence-ref-guard`
- Version: `1.0.0`
- Type: `validator-rule`
- Activation: `never_by_default`
- Owner: synthetic-case-owner

## Origin

- Feature Delivery Case: `synthetic_fdc_dangling_ref_001`
- Contribution: `CONTRIB-PR-REVIEW-001`
- Source: `synthetic://pr-review/comment-001`

## Observable Change

Before: a mutated manager claim could reference a missing evidence record.

After: the local validator deterministically rejects the missing reference.

## Synthetic Challenge

The simulated reviewer challenged wording that implied passing conformance established real usefulness. The wording was narrowed to contract behavior only.

## Limitations

- All evidence and review records are synthetic.
- There is no real usage observation.
- Use, reuse, team adoption, manager acceptance, ROI, and business value remain unproven.

## Next Use

Run the guard against one bounded private asset pack, keep evidence local, and obtain accountable human review before any activation decision.
"""


def build_pack(
    example_root: Path, output_root: Path, *, allow_replace: bool = False
) -> None:
    inputs = example_root / "inputs"
    if output_root.exists():
        if output_root == output_root.parent or len(output_root.parts) < 3:
            raise ValueError(f"refusing unsafe output replacement: {output_root}")
        if not allow_replace:
            raise ValueError(
                f"output already exists: {output_root}; rerun with --force to replace it"
            )
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True)
    for name in (
        "feature-delivery-case.json",
        "evidence-ledger.jsonl",
        "contribution-ledger.jsonl",
        "manager-brief.json",
    ):
        copy_file(inputs / name, output_root / name)
    shutil.copytree(
        inputs / "reusable-assets",
        output_root / "reusable-assets",
    )
    (output_root / "reusable-asset-dossier.md").write_text(
        render_dossier(), encoding="utf-8"
    )
    brief = load_json(inputs / "manager-brief.json")
    from validate_manager_claims import render_manager_brief_markdown

    (output_root / "manager-brief.md").write_text(
        render_manager_brief_markdown(brief), encoding="utf-8"
    )
    manifest = {
        "contract": "lat.delivery-evidence-asset-pack.v1",
        "contract_version": "1.0.0",
        "pack_id": PACK_ID,
        "pack_version": "1.0.0",
        "simulation_status": "synthetic_reference",
        "downstream_adoption_status": "not_observed",
        "feature_delivery_case_id": CASE_ID,
        "accountable_owner": "synthetic-case-owner",
        "lattice_pin": {
            "ref": "v0.0.0-synthetic",
            "commit_sha": "0000000000000000000000000000000000000000",
        },
        "public_capabilities": [
            "skill:feature-delivery-case@1.0.0",
            "skill:lattice-governor@1.2.0",
        ],
        "evidence_origin": "synthetic",
        "artifacts": {
            "feature_delivery_case": "feature-delivery-case.json",
            "evidence_ledger": "evidence-ledger.jsonl",
            "contribution_ledger": "contribution-ledger.jsonl",
            "reusable_asset_dossier": "reusable-asset-dossier.md",
            "manager_brief": "manager-brief.json",
            "manager_brief_rendered": "manager-brief.md",
            "validation_report": "validation-report.json",
        },
        "reusable_assets": [
            {
                "asset_id": ASSET_ID,
                "asset_version": "1.0.0",
                "manifest_path": f"reusable-assets/{ASSET_ID}/asset-manifest.json",
                "change_proposal_path": f"reusable-assets/{ASSET_ID}/change-proposal.json",
                "review_path": f"reusable-assets/{ASSET_ID}/review.json",
                "usage_observations_path": f"reusable-assets/{ASSET_ID}/usage-observations.jsonl",
            }
        ],
        "generated_at": GENERATED_AT,
    }
    write_json(output_root / "asset-pack.manifest.json", manifest)


def apply_mutation(value: Any, pointer: str, replacement: Any) -> None:
    parts = [part.replace("~1", "/").replace("~0", "~") for part in pointer.split("/")[1:]]
    if not parts:
        raise ValueError("mutation_path cannot target the document root")
    target = value
    for part in parts[:-1]:
        target = target[int(part)] if isinstance(target, list) else target[part]
    final = parts[-1]
    if isinstance(target, list):
        target[int(final)] = replacement
    else:
        target[final] = replacement


def run_negative_cases(
    example_root: Path,
    lattice_root: Path,
    evidence: list[dict[str, Any]],
) -> tuple[list[str], list[str]]:
    from downstream_contracts import canonical_capabilities, validate_extension
    from validate_manager_claims import validate_manager_brief

    failures: list[str] = []
    passed: list[str] = []
    capabilities = canonical_capabilities(lattice_root)
    paths = sorted((example_root / "negative-cases").glob("*.json"))
    discovered_ids: set[str] = set()
    for path in paths:
        case = load_json(path)
        required = {
            "contract",
            "case_id",
            "target",
            "mutation_path",
            "mutation_value",
            "expected_error",
        }
        if set(case) != required or case["contract"] != "lat.synthetic-negative-case.v1":
            failures.append(f"{path.name}: invalid negative-case contract")
            continue
        case_id = str(case["case_id"])
        if case_id in discovered_ids:
            failures.append(f"{path.name}: duplicate negative case ID {case_id}")
            continue
        discovered_ids.add(case_id)
        target_name = case["target"]
        if target_name == "manager_brief":
            value = load_json(example_root / "inputs" / "manager-brief.json")
            apply_mutation(value, case["mutation_path"], case["mutation_value"])
            errors = validate_manager_brief(value, evidence)
        elif target_name == "private_extension":
            value = load_json(example_root / "private-capability-extension.json")
            apply_mutation(value, case["mutation_path"], case["mutation_value"])
            errors = validate_extension(value, capabilities)
        elif target_name == "asset_review":
            value = load_json(
                example_root
                / "inputs"
                / "reusable-assets"
                / ASSET_ID
                / "review.json"
            )
            apply_mutation(value, case["mutation_path"], case["mutation_value"])
            errors = validate_asset_source(example_root, review=value)
        else:
            failures.append(f"{path.name}: unsupported negative target {target_name}")
            continue
        expected = str(case["expected_error"])
        if not errors:
            failures.append(f"{path.name}: invalid mutation was accepted")
        elif not any(expected in error for error in errors):
            failures.append(
                f"{path.name}: expected error {expected!r}; got {'; '.join(errors)}"
            )
        else:
            passed.append(str(case["case_id"]))
    missing_cases = sorted(REQUIRED_NEGATIVE_CASES - discovered_ids)
    if missing_cases:
        failures.append(
            "missing required negative cases: " + ", ".join(missing_cases)
        )
    return failures, passed


def tree_differences(expected: Path, actual: Path) -> list[str]:
    expected_files = {
        path.relative_to(expected).as_posix(): path
        for path in expected.rglob("*")
        if path.is_file()
    }
    actual_files = {
        path.relative_to(actual).as_posix(): path
        for path in actual.rglob("*")
        if path.is_file()
    }
    differences = [
        f"golden missing generated file: {path}"
        for path in sorted(set(actual_files) - set(expected_files))
    ]
    differences.extend(
        f"generated output missing golden file: {path}"
        for path in sorted(set(expected_files) - set(actual_files))
    )
    for relative in sorted(set(expected_files) & set(actual_files)):
        if expected_files[relative].read_bytes() != actual_files[relative].read_bytes():
            differences.append(f"golden mismatch: {relative}")
    return differences


def validate_all(
    example_root: Path,
    lattice_root: Path,
    output_root: Path,
    *,
    allow_replace: bool = False,
) -> tuple[list[str], list[str]]:
    add_script_path(lattice_root)
    from validate_delivery_asset_pack import validate_asset_pack
    from validate_downstream_consumer import validate_consumer

    errors: list[str] = []
    checks: list[str] = []
    consumer = load_json(example_root / "downstream-consumer-manifest.json")
    consumer_errors = validate_consumer(
        consumer,
        lattice_root,
        example_root,
        validate_extension_files=True,
        verify_checkout_pin=True,
    )
    if consumer_errors:
        errors.extend(f"consumer: {item}" for item in consumer_errors)
    else:
        checks.append("downstream_consumer")
    feature_result = subprocess.run(
        [
            sys.executable,
            str(
                lattice_root
                / "skills"
                / "feature-delivery-case"
                / "scripts"
                / "validate_feature_delivery_case.py"
            ),
            str(example_root / "inputs" / "feature-delivery-case.json"),
            "--now",
            "2026-07-28T00:00:00Z",
        ],
        cwd=lattice_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if feature_result.returncode:
        errors.append("feature_delivery_case: " + feature_result.stderr.strip())
    else:
        checks.append("feature_delivery_case")
    source_errors = validate_asset_source(example_root)
    if source_errors:
        errors.extend(f"reusable_asset: {item}" for item in source_errors)
    else:
        checks.extend(["asset_candidate", "synthetic_review"])
    build_pack(example_root, output_root, allow_replace=allow_replace)
    evidence = load_jsonl(output_root / "evidence-ledger.jsonl")
    pack_errors, manifest = validate_asset_pack(
        output_root, lattice_root, allow_missing_validation_report=True
    )
    if pack_errors:
        errors.extend(f"asset_pack: {item}" for item in pack_errors)
    else:
        checks.extend(["evidence_ledger", "manager_claims", "delivery_asset_pack"])
    negative_errors, negative_passed = run_negative_cases(
        example_root, lattice_root, evidence
    )
    errors.extend(f"negative_case: {item}" for item in negative_errors)
    checks.extend(f"negative:{item}" for item in negative_passed)
    report = {
        "contract": "lat.delivery-asset-pack-validation-report.v1",
        "schema_version": "1.0.0",
        "status": "pass" if not errors else "fail",
        "pack_id": manifest.get("pack_id") if manifest else PACK_ID,
        "checks": checks,
        "negative_cases": negative_passed,
        "errors": errors,
        "generated_at": GENERATED_AT,
        "simulation_status": "synthetic_reference",
        "downstream_adoption_status": "not_observed",
        "privacy_note": "Synthetic local conformance only; no private evidence was read or uploaded.",
    }
    write_json(output_root / "validation-report.json", report)
    final_errors, _ = validate_asset_pack(output_root, lattice_root)
    if final_errors:
        errors.extend(f"final_asset_pack: {item}" for item in final_errors)
        report["status"] = "fail"
        report["errors"] = errors
        write_json(output_root / "validation-report.json", report)
    return errors, checks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--lattice-root")
    parser.add_argument("--out")
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing explicit or default generated output directory.",
    )
    args = parser.parse_args()
    example_root = Path(args.root).resolve()
    lattice_root = (
        Path(args.lattice_root).resolve()
        if args.lattice_root
        else Path(__file__).resolve().parents[2]
    )
    golden = example_root / "golden" / "manager-ready-delivery-asset-pack"
    temp: tempfile.TemporaryDirectory[str] | None = None
    if args.check:
        temp = tempfile.TemporaryDirectory(prefix="lat-synthetic-consumer-")
        output_root = Path(temp.name) / "manager-ready-delivery-asset-pack"
    else:
        output_root = (
            Path(args.out).resolve()
            if args.out
            else example_root / "generated" / "manager-ready-delivery-asset-pack"
        )
    try:
        errors, checks = validate_all(
            example_root,
            lattice_root,
            output_root,
            allow_replace=args.force,
        )
        if args.check:
            if not golden.is_dir():
                errors.append("golden asset pack is missing")
            else:
                errors.extend(tree_differences(golden, output_root))
        if errors:
            for error in errors:
                print(f"error: {error}", file=sys.stderr)
            return 1
        print(
            f"validated synthetic downstream consumer with {len(checks)} checks; "
            "adoption remains not_observed"
        )
        if args.check:
            print("golden Manager-Ready Delivery Asset Pack matches")
        else:
            print(f"generated Manager-Ready Delivery Asset Pack at {output_root}")
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    finally:
        if temp is not None:
            temp.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
