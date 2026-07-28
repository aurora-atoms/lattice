#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate downstream schemas and committed public instances with Draft 2020-12."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from jsonschema.exceptions import SchemaError
except ImportError as exc:  # pragma: no cover - exercised by the CLI environment
    raise SystemExit(
        "jsonschema is required; run with `uv run --with jsonschema` "
        "or install the pinned CI dependency"
    ) from exc


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def validate_instance(
    schema: dict[str, Any],
    instance: dict[str, Any],
    label: str,
) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{label}: {'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))
    ]


def validate_all(root: Path) -> tuple[list[str], int]:
    schema_paths = {
        "consumer": root
        / "schemas/downstream/downstream-consumer-manifest.v1.schema.json",
        "extension": root
        / "schemas/downstream/private-capability-extension.v1.schema.json",
        "asset_pack": root
        / "schemas/evidence/delivery-evidence-asset-pack.v1.schema.json",
        "claim": root / "schemas/evidence/evidence-claim.v1.schema.json",
        "report": root
        / "schemas/evidence/delivery-asset-pack-validation-report.v1.schema.json",
        "manager": root
        / "schemas/manager/manager-delivery-brief.v1.schema.json",
        "eval_case": root
        / "feature-delivery-harness-mvp/schemas/evals/eval-case.v1.schema.json",
        "summary": root
        / "feature-delivery-harness-mvp/schemas/evals/conformance-summary.v1.schema.json",
    }
    schemas = {name: load_json(path) for name, path in schema_paths.items()}
    errors: list[str] = []
    for name, schema in schemas.items():
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            errors.append(f"schema {name}: {exc}")

    example = root / "examples/synthetic-private-consumer"
    golden = example / "golden/manager-ready-delivery-asset-pack"
    instances: list[tuple[str, str, Path]] = [
        ("consumer", "synthetic consumer", example / "downstream-consumer-manifest.json"),
        (
            "extension",
            "synthetic private extension",
            example / "private-capability-extension.json",
        ),
        ("asset_pack", "golden asset pack", golden / "asset-pack.manifest.json"),
        ("report", "golden validation report", golden / "validation-report.json"),
    ]
    validated = 0
    for schema_name, label, path in instances:
        errors.extend(validate_instance(schemas[schema_name], load_json(path), label))
        validated += 1

    manager = load_json(golden / "manager-brief.json")
    manager_schema = copy.deepcopy(schemas["manager"])
    manager_schema["properties"]["claims"]["items"] = schemas["claim"]
    errors.extend(validate_instance(manager_schema, manager, "golden manager brief"))
    validated += 1
    for index, claim in enumerate(manager.get("claims", [])):
        if isinstance(claim, dict):
            errors.extend(
                validate_instance(schemas["claim"], claim, f"golden claim[{index}]")
            )
            validated += 1

    eval_root = root / "feature-delivery-harness-mvp/evals"
    for path in sorted(eval_root.glob("*/case.json")):
        errors.extend(
            validate_instance(
                schemas["eval_case"], load_json(path), f"eval case {path.parent.name}"
            )
        )
        validated += 1

    summary_path = (
        root
        / "artifacts/capability-runs/lattice-governor/"
        "2026-07-28-synthetic-private-consumer-pr4/conformance-summary.json"
    )
    summary = load_json(summary_path)
    errors.extend(
        validate_instance(
            schemas["summary"], summary, "committed conformance summary"
        )
    )
    results = summary.get("results", [])
    if isinstance(results, list):
        result_ids = [
            str(item.get("case_id"))
            for item in results
            if isinstance(item, dict)
        ]
        if len(set(result_ids)) != len(result_ids):
            errors.append("committed conformance summary: duplicate case_id")
        if summary.get("total") != len(results):
            errors.append("committed conformance summary: total does not match results")
        passed = sum(
            isinstance(item, dict) and item.get("status") == "pass"
            for item in results
        )
        failed = sum(
            isinstance(item, dict) and item.get("status") == "fail"
            for item in results
        )
        if summary.get("passed") != passed or summary.get("failed") != failed:
            errors.append(
                "committed conformance summary: pass/fail counts do not match results"
            )
        expected_case_ids = {path.parent.name for path in eval_root.glob("*/case.json")}
        if set(result_ids) != expected_case_ids:
            errors.append(
                "committed conformance summary: case IDs do not match eval inventory"
            )
    validated += 1
    return errors, validated


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    try:
        errors, count = validate_all(Path(args.root).resolve())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors, count = [str(exc)], 0
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"validated {count} downstream schema instance(s) with Draft 2020-12")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
