#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check FDH acceptance evidence, evidence refs, and manual promotion boundaries."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from fdh_lib import failure, list_value, read_jsonl, records_by_type, validate_records


def declared_external_refs(records: list[dict[str, Any]]) -> set[str]:
    refs: set[str] = set()
    for record in records:
        constraints = record.get("constraints", {})
        if isinstance(constraints, dict):
            for ref in constraints.get("declared_external_refs", []):
                refs.add(str(ref))
    return refs


def acceptance_id(item: Any) -> str | None:
    if isinstance(item, dict):
        value = item.get("id") or item.get("acceptance_id")
        return str(value) if value else None
    if isinstance(item, str) and item.strip():
        return item.strip()
    return None


def evidence_ref_values(record: dict[str, Any]) -> list[str]:
    payload = record.get("payload", {})
    values: list[str] = []
    for field in ("evidence_refs",):
        values.extend(str(item) for item in list_value(payload.get(field)))
    return values


def check_acceptance_coverage(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    feature_records = records_by_type(records, "feature_delivery_case")
    validation_records = records_by_type(records, "validation.result")
    delivery_records = records_by_type(records, "delivery.evidence")
    covered: set[str] = set()
    for record in validation_records:
        covered.update(str(item) for item in list_value(record.get("payload", {}).get("target_acceptance_ids")))
    for record in delivery_records:
        for result in list_value(record.get("payload", {}).get("acceptance_results")):
            if isinstance(result, dict) and result.get("acceptance_id"):
                covered.add(str(result["acceptance_id"]))
    for feature in feature_records:
        for item in list_value(feature.get("payload", {}).get("acceptance_criteria")):
            item_id = acceptance_id(item)
            if item_id and item_id not in covered:
                failures.append(
                    failure(
                        "MISSING_EVIDENCE_FOR_ACCEPTANCE",
                        f"acceptance criterion {item_id} has no validation.result or delivery.evidence coverage",
                        int(feature.get("_line_no", 0)) or None,
                        str(feature.get("id", "")),
                    )
                )
    return failures


def check_evidence_refs(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    known_refs = {str(record.get("id")) for record in records}
    known_refs.update(declared_external_refs(records))
    failures: list[dict[str, Any]] = []
    for record in records:
        for ref in evidence_ref_values(record):
            if ref not in known_refs:
                failures.append(
                    failure(
                        "DANGLING_EVIDENCE_REF",
                        f"evidence_ref {ref} does not resolve to a record id or declared external ref",
                        int(record.get("_line_no", 0)) or None,
                        str(record.get("id", "")),
                    )
                )
    return failures


def check_promotions(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    reviews = records_by_type(records, "promotion.review")
    approved_reviews = {
        str(record.get("payload", {}).get("candidate_id")): record
        for record in reviews
        if record.get("payload", {}).get("decision") == "approved"
    }
    for candidate in records_by_type(records, "promotion.candidate"):
        payload = candidate.get("payload", {})
        candidate_id = str(candidate.get("id", ""))
        if payload.get("promotion_status") == "promoted" and candidate_id not in approved_reviews:
            failures.append(
                failure(
                    "AUTO_PROMOTION_FORBIDDEN",
                    f"promotion candidate {candidate_id} is promoted without approved promotion.review",
                    int(candidate.get("_line_no", 0)) or None,
                    candidate_id,
                )
            )
        review = approved_reviews.get(candidate_id)
        if review:
            review_payload = review.get("payload", {})
            if not review_payload.get("reviewer") or not list_value(review_payload.get("evidence_refs")) or not list_value(review_payload.get("validation_refs")) or not review_payload.get("resulting_artifact_type"):
                failures.append(
                    failure(
                        "PROMOTION_REVIEW_INCOMPLETE",
                        f"promotion review for {candidate_id} lacks reviewer, evidence_refs, validation_refs, or resulting_artifact_type",
                        int(review.get("_line_no", 0)) or None,
                        str(review.get("id", "")),
                    )
                )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", help="Input JSONL file.")
    args = parser.parse_args()

    records, read_failures = read_jsonl(Path(args.jsonl))
    failures = read_failures + validate_records(records)
    if not failures:
        failures.extend(check_acceptance_coverage(records))
        failures.extend(check_evidence_refs(records))
        failures.extend(check_promotions(records))
    if failures:
        for item in failures:
            print(json.dumps(item, sort_keys=True), file=sys.stderr)
        return 1
    print("validated evidence completeness")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
