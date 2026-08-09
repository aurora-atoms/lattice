#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate Outcome Receipt v1 against a Portable Case Pack.

The schema owns structure. This validator owns claim/evidence lineage, history
continuity, cutoff ordering, and the rule that one outcome cannot promote a
Harness candidate into team-wide authority.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CONTRACT = "lat.outcome_receipt.v1"
MISSION = "lat.goal.verified-decision-yield.v1"
STATUSES = {
    "UNKNOWN",
    "HYPOTHESIS",
    "EVIDENCED",
    "CONFIRMED",
    "CONFLICTED",
    "STALE",
    "INVALIDATED",
}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def _parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _refs(value: Any) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {str(item) for item in value}


def _collect_evidence_refs(value: Any) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            if key == "evidence_refs":
                refs.update(_refs(nested))
            else:
                refs.update(_collect_evidence_refs(nested))
    elif isinstance(value, list):
        for nested in value:
            refs.update(_collect_evidence_refs(nested))
    return refs


def _pack_evidence_ids(pack: dict[str, Any]) -> set[str]:
    return {
        str(item.get("id"))
        for item in pack.get("evidence_refs", [])
        if isinstance(item, dict) and item.get("id")
    }


def _pack_claim_ids(pack: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    claims = pack.get("claims")
    if not isinstance(claims, dict):
        return ids
    for bucket in claims.values():
        if not isinstance(bucket, list):
            continue
        for claim in bucket:
            if isinstance(claim, dict) and claim.get("claim_id"):
                ids.add(str(claim["claim_id"]))
    return ids


def validate_outcome(receipt: dict[str, Any], pack: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if receipt.get("contract") != CONTRACT:
        errors.append(f"contract must be {CONTRACT}")
    if receipt.get("mission_anchor_ref") != MISSION:
        errors.append(f"mission_anchor_ref must be {MISSION}")
    if pack.get("mission_anchor_ref") != MISSION:
        errors.append("Portable Case Pack mission anchor does not match outcome mission")
    if receipt.get("case_id") != pack.get("case_id"):
        errors.append("Outcome Receipt and Portable Case Pack must share one case_id")

    evidence_ids = _pack_evidence_ids(pack)
    unknown_refs = _collect_evidence_refs(receipt) - evidence_ids
    if unknown_refs:
        errors.append(
            "Outcome Receipt references unknown Portable Case Pack evidence: "
            + ", ".join(sorted(unknown_refs))
        )

    pack_claim_ids = _pack_claim_ids(pack)
    outcomes = receipt.get("claim_outcomes")
    if not isinstance(outcomes, list):
        errors.append("claim_outcomes must be a list")
        outcomes = []

    outcome_ids: list[str] = []
    observed_at = _parse_time(receipt.get("observed_at"))
    for index, outcome in enumerate(outcomes):
        label = f"claim_outcomes[{index}]"
        if not isinstance(outcome, dict):
            errors.append(f"{label} must be an object")
            continue
        claim_id = str(outcome.get("claim_id", ""))
        if not claim_id:
            errors.append(f"{label}.claim_id is required")
            continue
        outcome_ids.append(claim_id)
        if claim_id not in pack_claim_ids:
            errors.append(f"{label} references unknown claim: {claim_id}")

        status = outcome.get("status")
        if status not in STATUSES:
            errors.append(f"{label}.status is invalid")
        refs = _refs(outcome.get("evidence_refs"))
        if status != "UNKNOWN" and not refs:
            errors.append(f"{label} non-UNKNOWN status requires evidence_refs")

        history = outcome.get("status_history")
        if not isinstance(history, list) or not history:
            errors.append(f"{label}.status_history must be non-empty")
            continue
        version = outcome.get("version")
        if version != len(history):
            errors.append(f"{label}.version must equal status_history length")

        previous_to: str | None = None
        last_changed: datetime | None = None
        for history_index, event in enumerate(history):
            event_label = f"{label}.status_history[{history_index}]"
            if not isinstance(event, dict):
                errors.append(f"{event_label} must be an object")
                continue
            from_status = event.get("from")
            to_status = event.get("to")
            if from_status is not None and from_status not in STATUSES:
                errors.append(f"{event_label}.from is invalid")
            if to_status not in STATUSES:
                errors.append(f"{event_label}.to is invalid")
            if history_index == 0:
                if from_status is not None:
                    errors.append(f"{event_label}.from must be null for version 1 lineage")
            elif from_status != previous_to:
                errors.append(f"{event_label}.from must equal the previous to status")
            previous_to = str(to_status) if to_status is not None else None

            changed_at = _parse_time(event.get("changed_at"))
            if changed_at is None:
                errors.append(f"{event_label}.changed_at must be a date-time")
            else:
                if last_changed is not None and changed_at < last_changed:
                    errors.append(f"{event_label}.changed_at must be nondecreasing")
                if observed_at is not None and changed_at > observed_at:
                    errors.append(f"{event_label}.changed_at cannot be after observed_at")
                last_changed = changed_at

        if previous_to != status:
            errors.append(f"{label}.status must equal the last status_history.to")

        cutoff = _parse_time(outcome.get("cutoff"))
        if cutoff is None:
            errors.append(f"{label}.cutoff must be a date-time")
        elif observed_at is not None and cutoff > observed_at:
            errors.append(f"{label}.cutoff cannot be after observed_at")

    if len(outcome_ids) != len(set(outcome_ids)):
        errors.append("claim_outcomes contains duplicate claim_id values")
    if set(outcome_ids) != pack_claim_ids:
        missing = pack_claim_ids - set(outcome_ids)
        extra = set(outcome_ids) - pack_claim_ids
        if missing:
            errors.append("Outcome Receipt is missing claim outcomes: " + ", ".join(sorted(missing)))
        if extra:
            errors.append("Outcome Receipt contains extra claim outcomes: " + ", ".join(sorted(extra)))

    changed = receipt.get("delivery_state_changed")
    before = receipt.get("state_before")
    after = receipt.get("state_after")
    if changed is True and isinstance(before, dict) and isinstance(after, dict):
        if before.get("statement") == after.get("statement"):
            errors.append("delivery_state_changed=true requires different before/after statements")

    failure = receipt.get("earliest_failure_point")
    candidate = receipt.get("failure_point_candidate")
    if isinstance(candidate, dict):
        if candidate.get("promotion_authority") != "none_from_outcome_receipt":
            errors.append("Outcome Receipt cannot grant Harness promotion authority")
        if candidate.get("eligible_for_harness_candidate") is True:
            if not isinstance(failure, dict) or not str(failure.get("statement", "")).strip():
                errors.append("eligible Harness candidate requires an earliest_failure_point")
            elif not _refs(failure.get("evidence_refs")):
                errors.append("eligible Harness candidate requires evidence-backed earliest_failure_point")

    remaining = receipt.get("remaining_unknowns")
    if isinstance(remaining, list):
        status_by_claim = {
            str(item.get("claim_id")): item.get("status")
            for item in outcomes
            if isinstance(item, dict) and item.get("claim_id")
        }
        for index, item in enumerate(remaining):
            if not isinstance(item, dict):
                continue
            claim_id = item.get("claim_id")
            if claim_id is not None:
                claim_id = str(claim_id)
                if claim_id not in pack_claim_ids:
                    errors.append(f"remaining_unknowns[{index}] references unknown claim: {claim_id}")
                elif status_by_claim.get(claim_id) not in {"UNKNOWN", "HYPOTHESIS"}:
                    errors.append(
                        f"remaining_unknowns[{index}] claim must remain UNKNOWN or HYPOTHESIS"
                    )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", help="Outcome Receipt JSON path")
    parser.add_argument("pack", help="Portable Case Pack JSON path")
    args = parser.parse_args()

    try:
        receipt = load_json(Path(args.receipt))
        pack = load_json(Path(args.pack))
        errors = validate_outcome(receipt, pack)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"validated outcome receipt: {args.receipt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
