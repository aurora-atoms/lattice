#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate public adversarial-innovation handoff records and anti-premature-novelty semantics."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas/capability/adversarial-innovation-handoff.v1.schema.json"
PRIVATE_PATTERNS = (
    re.compile(r"(?i)/(?:Users|home)/"),
    re.compile(r"[A-Za-z]:\\(?:Users|workspace|repo)\\", re.IGNORECASE),
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
)
LEGAL_ASSERTION_PATTERNS = (
    re.compile(r"\b(?:is|are)\s+patentable\b", re.IGNORECASE),
    re.compile(r"\b(?:is|are)\s+novel\b", re.IGNORECASE),
    re.compile(r"\bno\s+prior\s+art\b", re.IGNORECASE),
    re.compile(r"\bFTO\s+clear\b", re.IGNORECASE),
    re.compile(r"\bnon[- ]infringing\b", re.IGNORECASE),
)
REJECT_STATUSES = {
    "reject_existing_control",
    "reject_prior_art",
    "reject_not_reproducible",
    "reject_not_commercial",
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def _all_strings(value: Any) -> list[str]:
    strings: list[str] = []
    if isinstance(value, str):
        strings.append(value)
    elif isinstance(value, dict):
        for nested in value.values():
            strings.extend(_all_strings(nested))
    elif isinstance(value, list):
        for nested in value:
            strings.extend(_all_strings(nested))
    return strings


def _duplicates(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def schema_errors(record: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(record), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"schema:{location}: {error.message}")
    return errors


def semantic_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    strings = _all_strings(record)
    if any(pattern.search(text) for text in strings for pattern in PRIVATE_PATTERNS):
        errors.append("public innovation handoff contains a private locator, path, or email")
    if any(pattern.search(text) for text in strings for pattern in LEGAL_ASSERTION_PATTERNS):
        errors.append("innovation handoff contains an unsupported patentability/novelty/FTO assertion")

    source_review = record.get("source_review", {})
    allowed_chain_ids = set(map(str, source_review.get("source_chain_ids", [])))
    candidates = [item for item in record.get("mechanism_candidates", []) if isinstance(item, dict)]

    duplicate_candidates = _duplicates([str(item.get("candidate_id")) for item in candidates])
    if duplicate_candidates:
        errors.append("duplicate candidate_id(s): " + ", ".join(duplicate_candidates))

    falsifier_ids: list[str] = []
    for candidate in candidates:
        candidate_id = str(candidate.get("candidate_id", "<missing>"))
        candidate_chain_ids = set(map(str, candidate.get("source_chain_ids", [])))
        unknown_chain_ids = sorted(candidate_chain_ids - allowed_chain_ids)
        if unknown_chain_ids:
            errors.append(
                f"{candidate_id}: source_chain_ids not present in source_review: {', '.join(unknown_chain_ids)}"
            )

        hard_case = candidate.get("hard_case", {})
        counter = candidate.get("counter_control", {})
        prior_art = candidate.get("prior_art_challenge", {})
        falsifiers = [item for item in candidate.get("falsifiers", []) if isinstance(item, dict)]
        falsifier_ids.extend(str(item.get("falsifier_id", "")) for item in falsifiers)
        status = candidate.get("status")
        decision = candidate.get("decision")

        reproduced = hard_case.get("reproducibility") in {"deterministic", "intermittent"}
        unresolved_falsifier = any(item.get("status") != "survived" for item in falsifiers)
        prior_art_completed = prior_art.get("status") == "completed"
        prior_art_clear_bounded = (
            prior_art_completed
            and prior_art.get("conclusion") == "no_equivalent_found_in_bounded_search"
        )
        prior_art_defeats = (
            prior_art_completed
            and prior_art.get("conclusion") == "equivalent_or_broader_mechanism_found"
        )

        if counter.get("defeats_candidate") is True:
            if status != "reject_existing_control" or decision != "reject":
                errors.append(
                    f"{candidate_id}: a defeating existing control requires reject_existing_control + reject"
                )

        if prior_art_defeats and (status != "reject_prior_art" or decision != "reject"):
            errors.append(
                f"{candidate_id}: equivalent/broader prior art requires reject_prior_art + reject"
            )

        if status in REJECT_STATUSES and decision != "reject":
            errors.append(f"{candidate_id}: reject status requires decision=reject")

        if status == "prior_art_pending":
            if decision != "needs_more_evidence":
                errors.append(f"{candidate_id}: prior_art_pending requires needs_more_evidence")
            if prior_art.get("status") not in {"not_started", "pending", "blocked"}:
                errors.append(f"{candidate_id}: prior_art_pending cannot declare prior-art completion")

        if status == "retain_candidate" or decision == "retain_for_research":
            if status != "retain_candidate" or decision != "retain_for_research":
                errors.append(
                    f"{candidate_id}: retain_candidate and retain_for_research must be declared together"
                )
            if not reproduced:
                errors.append(f"{candidate_id}: retained candidate requires a reproduced hard case")
            if counter.get("defeats_candidate") is True:
                errors.append(f"{candidate_id}: retained candidate cannot have a defeating existing control")
            if unresolved_falsifier:
                errors.append(f"{candidate_id}: retained candidate requires all falsifiers to survive")
            if not prior_art_clear_bounded:
                errors.append(
                    f"{candidate_id}: retained candidate requires completed bounded prior-art challenge with no equivalent found"
                )

        if not reproduced and status not in {"candidate", "insufficient_evidence", "reject_not_reproducible"}:
            errors.append(
                f"{candidate_id}: unreproduced hard case cannot advance beyond candidate/insufficient/reject"
            )

    duplicate_falsifiers = _duplicates([value for value in falsifier_ids if value])
    if duplicate_falsifiers:
        errors.append("duplicate falsifier_id(s): " + ", ".join(duplicate_falsifiers))

    return errors


def validate_record(record: dict[str, Any], schema: dict[str, Any] | None = None) -> list[str]:
    active_schema = schema or load_json(SCHEMA_PATH)
    errors = schema_errors(record, active_schema)
    if errors:
        return errors
    return semantic_errors(record)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("handoff", help="Adversarial innovation handoff JSON file")
    parser.add_argument("--schema", default=str(SCHEMA_PATH))
    args = parser.parse_args()

    try:
        record = load_json(Path(args.handoff))
        schema = load_json(Path(args.schema))
        errors = validate_record(record, schema)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print("adversarial innovation handoff: valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
