#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check FDH runtime payload fields match published record schemas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from fdh_lib import BASE_DIR, PAYLOAD_FIELDS, REQUIRED_PAYLOAD_FIELDS


SCHEMA_FILES = {
    "feature_delivery_case": "feature_delivery_case.v1.schema.json",
    "task.packet": "task.packet.v1.schema.json",
    "delivery.evidence": "delivery.evidence.v1.schema.json",
    "delivery.verdict": "delivery.verdict.v1.schema.json",
    "validation.result": "validation.result.v1.schema.json",
    "yield.stage_breakdown": "yield.stage_breakdown.v1.schema.json",
    "yield.waste_pattern": "yield.waste_pattern.v1.schema.json",
    "yield.optimization_signal": "yield.optimization_signal.v1.schema.json",
    "yield.dossier": "yield.dossier.v1.schema.json",
    "context_pack": "context_pack.v1.schema.json",
    "promotion.candidate": "promotion.candidate.v1.schema.json",
    "promotion.review": "promotion.review.v1.schema.json",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    failures: list[str] = []
    schema_dir = BASE_DIR / "schemas" / "records"
    for record_type, filename in SCHEMA_FILES.items():
        schema = json.loads((schema_dir / filename).read_text(encoding="utf-8"))
        properties = set(schema.get("properties", {}))
        required = set(schema.get("required", []))
        runtime_fields = PAYLOAD_FIELDS[record_type]
        runtime_required = REQUIRED_PAYLOAD_FIELDS[record_type]
        if properties != runtime_fields:
            failures.append(
                f"{record_type}: properties drift schema_only={sorted(properties - runtime_fields)} runtime_only={sorted(runtime_fields - properties)}"
            )
        if required != runtime_required:
            failures.append(
                f"{record_type}: required drift schema_only={sorted(required - runtime_required)} runtime_only={sorted(runtime_required - required)}"
            )
        if schema.get("additionalProperties") is not False:
            failures.append(f"{record_type}: additionalProperties must be false")
    if failures:
        for failure in failures:
            print(failure)
        return 1
    print(f"validated {len(SCHEMA_FILES)} schema/runtime contract(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
