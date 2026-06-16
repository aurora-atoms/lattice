#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Build a bounded FDH context_pack record from validated JSONL input."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from fdh_lib import read_jsonl, stable_json, validate_records


def estimate_tokens(text: str) -> int:
    return max(1, (len(text) + 3) // 4) if text else 0


def record_summary(record: dict[str, Any]) -> str:
    payload = record.get("payload", {})
    for field in ("title", "objective", "validation_summary", "recommendation", "purpose"):
        value = payload.get(field)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return str(record.get("type", "record"))


def declared_external_refs(records: list[dict[str, Any]]) -> set[str]:
    refs: set[str] = set()
    for record in records:
        constraints = record.get("constraints", {})
        if isinstance(constraints, dict):
            for ref in constraints.get("declared_external_refs", []):
                refs.add(str(ref))
    return refs


def build_context_pack(records: list[dict[str, Any]], purpose: str, token_budget: int) -> dict[str, Any]:
    features = [record for record in records if record.get("type") == "feature_delivery_case"]
    case_id = str(features[0]["scope"]["feature_delivery_case_id"]) if features else "unknown"
    included_refs = sorted(str(record["id"]) for record in records)
    source_refs = sorted(declared_external_refs(records))
    projected_items = [
        {
            "id": str(record["id"]),
            "type": str(record["type"]),
            "summary": record_summary(record),
        }
        for record in records
    ]
    token_estimate = sum(estimate_tokens(item["summary"]) for item in projected_items)
    return {
        "type": "context_pack",
        "id": f"context_pack_{case_id}",
        "schema": "lat.context_pack.v1",
        "source": "build_context_pack",
        "target": "task-packet-builder",
        "scope": {"project_id": "lattice", "feature_delivery_case_id": case_id, "module_id": "scopekeeper"},
        "payload": {
            "feature_delivery_case_id": case_id,
            "purpose": purpose,
            "source_refs": source_refs,
            "included_refs": included_refs,
            "excluded_refs": [],
            "projected_items": projected_items,
            "token_budget": token_budget,
            "token_estimate": token_estimate,
            "raw_source_policy": "projected_only",
        },
        "constraints": {"raw_context": "forbidden"},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", help="Input JSONL file.")
    parser.add_argument("--purpose", default="bounded feature delivery context", help="Context pack purpose.")
    parser.add_argument("--token-budget", type=int, default=24000, help="Context token budget.")
    parser.add_argument("--out", help="Optional context_pack JSONL output path.")
    args = parser.parse_args()

    records, read_failures = read_jsonl(Path(args.jsonl))
    failures = read_failures + validate_records(records)
    if failures:
        for item in failures:
            print(item, file=sys.stderr)
        return 1
    context_pack = build_context_pack(records, args.purpose, args.token_budget)
    output = stable_json(context_pack) + "\n"
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(output, encoding="utf-8", newline="\n")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
