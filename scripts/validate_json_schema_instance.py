#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate a JSON instance against a Draft 2020-12 JSON Schema.

Structural validity is owned by the schema. Domain-specific cross-field semantics
remain the responsibility of the caller's semantic validator.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from jsonschema.exceptions import SchemaError
except ImportError as exc:  # pragma: no cover - exercised by environment setup
    raise SystemExit(
        "jsonschema is required; install requirements-validation.txt before running this validator"
    ) from exc


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _json_path(parts: list[object]) -> str:
    path = "$"
    for part in parts:
        if isinstance(part, int):
            path += f"[{part}]"
        else:
            path += f".{part}"
    return path


def validate_instance(schema_path: Path, instance_path: Path) -> list[str]:
    """Return deterministic validation errors for one instance."""
    schema = load_json(schema_path)
    instance = load_json(instance_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: (
            tuple(str(part) for part in error.absolute_path),
            error.message,
        ),
    )
    return [f"{_json_path(list(error.absolute_path))}: {error.message}" for error in errors]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("schema", help="Draft 2020-12 JSON Schema path")
    parser.add_argument("instances", nargs="+", help="JSON instance path(s)")
    args = parser.parse_args()

    schema_path = Path(args.schema)
    all_errors: list[str] = []
    try:
        for raw_path in args.instances:
            instance_path = Path(raw_path)
            errors = validate_instance(schema_path, instance_path)
            all_errors.extend(f"{instance_path}: {message}" for message in errors)
    except (OSError, json.JSONDecodeError, SchemaError) as exc:
        all_errors.append(str(exc))

    if all_errors:
        for error in all_errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"validated {len(args.instances)} instance(s) against {schema_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
