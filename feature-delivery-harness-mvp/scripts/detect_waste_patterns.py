#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Emit deterministic FDH waste pattern records from validated JSONL input."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from fdh_lib import list_value, read_jsonl, records_by_type, stable_json


def token_cost(value: int | None, source_ref: str) -> dict[str, Any]:
    return {"value": value, "unit": "tokens", "status": "estimated" if value is not None else "unknown", "source_ref": source_ref}


def waste_record(case_id: str, pattern: str, severity: str, evidence_refs: list[str], recommendation: str, impact: int | None = None) -> dict[str, Any]:
    return {
        "type": "yield.waste_pattern",
        "id": f"waste_{case_id}_{pattern}",
        "schema": "lat.yield.waste_pattern.v1",
        "source": "detect_waste_patterns",
        "target": "token-economics-dossier-generator",
        "scope": {"project_id": "lattice", "feature_delivery_case_id": case_id, "module_id": "deliveryyield"},
        "payload": {
            "feature_delivery_case_id": case_id,
            "pattern": pattern,
            "severity": severity,
            "detection_method": "deterministic_fixture_rules",
            "thresholds": {"context_token_budget": 24000, "repeat_threshold": 2, "repair_attempt_threshold": 2},
            "evidence_refs": sorted(evidence_refs),
            "estimated_token_impact": token_cost(impact, ",".join(sorted(evidence_refs)) or "unknown"),
            "recommendation": recommendation,
        },
        "constraints": {},
    }


def detect(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    features = records_by_type(records, "feature_delivery_case")
    case_id = "unknown"
    if features:
        case_id = str(features[0]["payload"].get("title", "fdc_001")).lower().replace(" ", "_")
        case_id = str(features[0]["scope"].get("feature_delivery_case_id", case_id))
    emitted: list[dict[str, Any]] = []
    failures = [code for record in records_by_type(records, "validation.result") for code in list_value(record.get("payload", {}).get("failure_codes"))]
    all_payloads = [record.get("payload", {}) for record in records]
    max_context = max([int(payload.get("context_token_count", 0) or 0) for payload in all_payloads] + [0])
    if max_context > 24000 or any(code in failures for code in ("RAW_CONTEXT_FORBIDDEN", "TOKEN_BUDGET_EXCEEDED", "SCOPE_TOO_LARGE")):
        emitted.append(waste_record(case_id, "oversized_context", "error", ["validation_context_budget"], "Project raw sources into a bounded context pack before model-visible use.", max_context - 24000 if max_context > 24000 else None))

    context_refs = [ref for payload in all_payloads for ref in list_value(payload.get("context_refs"))]
    repeated_refs = [ref for ref, count in Counter(context_refs).items() if count > 1]
    if repeated_refs:
        emitted.append(waste_record(case_id, "repeated_context_read", "warning", repeated_refs, "Reuse the existing bounded context pack instead of rereading the same source.", None))

    fingerprints = [fp for payload in all_payloads for fp in list_value(payload.get("analysis_fingerprints"))]
    duplicate_fps = [fp for fp, count in Counter(fingerprints).items() if count > 1]
    if duplicate_fps:
        emitted.append(waste_record(case_id, "duplicate_analysis", "warning", duplicate_fps, "Collapse duplicate analysis into one cited conclusion.", None))

    repair_attempts = max([int(payload.get("repair_attempts", 0) or 0) for payload in all_payloads] + [0])
    if repair_attempts >= 2 or "ACCEPTANCE_FAILED" in failures:
        emitted.append(waste_record(case_id, "failed_repair_loop", "error", ["validation_acceptance"], "Stop repair loops and return to task packet scope or acceptance criteria.", None))

    review_iterations = max([int(payload.get("review_iterations", 0) or 0) for payload in all_payloads] + [0])
    if review_iterations >= 2:
        emitted.append(waste_record(case_id, "review_loop_without_progress", "warning", ["review_iterations"], "Require a new evidence item or decision before another review pass.", None))
    return emitted


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", help="Input JSONL file.")
    parser.add_argument("--out", help="Optional JSONL output path.")
    args = parser.parse_args()

    records, failures = read_jsonl(Path(args.jsonl))
    if failures:
        for item in failures:
            print(item, file=sys.stderr)
        return 2
    output = [stable_json(record) for record in detect(records)]
    if args.out:
        Path(args.out).write_text("\n".join(output) + ("\n" if output else ""), encoding="utf-8", newline="\n")
    else:
        for line in output:
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
