#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate manager claims against a local evidence ledger."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from downstream_contracts import (
    ADOPTION_STATUSES,
    EVIDENCE_ORIGINS,
    exact_fields,
    load_json,
    load_jsonl,
    nonempty_string,
    string_array,
    validate_claim,
)

REQUIRED_CLAIM_KINDS = {
    "current_delivery",
    "reusable_asset",
    "before_state",
    "after_state",
    "next_use",
}
REVIEWED_STATUSES = {"task_scoped", "used_once", "reused", "team_available"}


def evidence_errors(records: list[dict[str, Any]]) -> tuple[list[str], set[str]]:
    required = {
        "evidence_id",
        "evidence_type",
        "source_ref",
        "relation",
        "observed_at",
        "source_authority",
        "evidence_origin",
        "feature_delivery_case_id",
        "summary",
        "integrity_sha256",
    }
    errors: list[str] = []
    evidence_ids: set[str] = set()
    for index, record in enumerate(records):
        label = f"evidence[{index}]"
        item_errors = exact_fields(record, required, label)
        errors.extend(item_errors)
        if item_errors:
            continue
        evidence_id = str(record["evidence_id"])
        if not nonempty_string(evidence_id):
            errors.append(f"{label}: evidence_id must be non-empty")
        elif evidence_id in evidence_ids:
            errors.append(f"{label}: duplicate evidence_id {evidence_id}")
        evidence_ids.add(evidence_id)
        for field in (
            "evidence_type",
            "source_ref",
            "observed_at",
            "source_authority",
            "feature_delivery_case_id",
            "summary",
        ):
            if not nonempty_string(record[field]):
                errors.append(f"{label}: {field} must be non-empty")
        if record["relation"] not in {"supports", "contradicts", "inconclusive"}:
            errors.append(f"{label}: invalid relation")
        if record["evidence_origin"] not in EVIDENCE_ORIGINS:
            errors.append(f"{label}: invalid evidence_origin")
        integrity = record["integrity_sha256"]
        if integrity is not None and (
            not isinstance(integrity, str)
            or len(integrity) != 64
            or any(char not in "0123456789abcdef" for char in integrity)
        ):
            errors.append(f"{label}: integrity_sha256 must be null or a lowercase SHA-256")
    return errors, evidence_ids


def validate_manager_brief(
    brief: dict[str, Any], evidence_records: list[dict[str, Any]]
) -> list[str]:
    required = {
        "contract",
        "contract_version",
        "brief_id",
        "asset_pack_id",
        "simulation_status",
        "downstream_adoption_status",
        "evidence_origin",
        "scope",
        "version",
        "claims",
        "human_challenge",
        "known_limitations",
        "unresolved_unknowns",
        "next_use_entry",
        "manager_decision",
        "human_review_ref",
        "governance_approval_ref",
    }
    errors = exact_fields(brief, required, "manager brief")
    if errors:
        return errors
    if brief["contract"] != "lat.manager-delivery-brief.v1":
        errors.append("manager brief: invalid contract")
    if brief["contract_version"] != "1.0.0":
        errors.append("manager brief: unsupported contract_version")
    evidence_validation, evidence_ids = evidence_errors(evidence_records)
    errors.extend(evidence_validation)
    evidence_by_id = {
        str(record.get("evidence_id")): record
        for record in evidence_records
        if nonempty_string(record.get("evidence_id"))
    }
    claims = brief["claims"]
    claim_ids: set[str] = set()
    claim_kinds: set[str] = set()
    if not isinstance(claims, list):
        errors.append("manager brief: claims must be an array")
        claims = []
    for claim in claims:
        if not isinstance(claim, dict):
            errors.append("manager brief: every claim must be an object")
            continue
        claim_id = str(claim.get("claim_id", ""))
        if claim_id in claim_ids:
            errors.append(f"manager brief: duplicate claim_id {claim_id}")
        claim_ids.add(claim_id)
        claim_kinds.add(str(claim.get("claim_kind", "")))
        errors.extend(validate_claim(claim, evidence_ids))
        if claim.get("evidence_origin") != brief["evidence_origin"]:
            errors.append(f"claim {claim_id}: evidence_origin differs from the brief")
        if claim.get("claim_kind") in REQUIRED_CLAIM_KINDS and claim.get("scope") != brief["scope"]:
            errors.append(f"claim {claim_id}: scope differs from the brief")
        refs = [str(ref) for ref in claim.get("evidence_refs", [])]
        resolved = [evidence_by_id[ref] for ref in refs if ref in evidence_by_id]
        if any(record.get("evidence_origin") != brief["evidence_origin"] for record in resolved):
            errors.append(f"claim {claim_id}: cited evidence origin differs from the brief")
        if (
            claim.get("classification") == "OBSERVED"
            and resolved
            and not any(record.get("relation") == "supports" for record in resolved)
        ):
            errors.append(f"claim {claim_id}: OBSERVED requires supporting evidence")
    missing_kinds = sorted(REQUIRED_CLAIM_KINDS - claim_kinds)
    if missing_kinds:
        errors.append(
            f"manager brief: missing required claim kinds: {', '.join(missing_kinds)}"
        )
    simulation = brief["simulation_status"]
    adoption = brief["downstream_adoption_status"]
    if simulation not in {"synthetic_reference", "real_downstream"}:
        errors.append("manager brief: invalid simulation_status")
    if adoption not in ADOPTION_STATUSES:
        errors.append("manager brief: invalid downstream_adoption_status")
    if brief["evidence_origin"] not in EVIDENCE_ORIGINS:
        errors.append("manager brief: invalid evidence_origin")
    if simulation == "synthetic_reference":
        if adoption != "not_observed":
            errors.append("manager brief: synthetic evidence must remain not_observed")
        if brief["evidence_origin"] != "synthetic":
            errors.append("manager brief: synthetic evidence must declare synthetic origin")
        if brief["human_review_ref"] is not None:
            errors.append("manager brief: synthetic review cannot claim real human approval")
        if brief["governance_approval_ref"] is not None:
            errors.append("manager brief: synthetic review cannot claim governance approval")
    if simulation == "real_downstream" and adoption in REVIEWED_STATUSES:
        if not nonempty_string(brief["human_review_ref"]):
            errors.append(f"manager brief: {adoption} requires human_review_ref")
    if adoption == "team_available" and not nonempty_string(
        brief["governance_approval_ref"]
    ):
        errors.append("manager brief: team_available requires governance_approval_ref")
    usage_evidence = {
        record["evidence_id"]
        for record in evidence_records
        if record.get("evidence_type") == "usage_observation"
    }
    for claim in claims:
        if not isinstance(claim, dict):
            continue
        kind = claim.get("claim_kind")
        classification = claim.get("classification")
        refs = set(map(str, claim.get("evidence_refs", [])))
        label = f"claim {claim.get('claim_id', '<missing>')}"
        if kind == "reuse" and classification != "UNKNOWN":
            if adoption not in {"reused", "team_available"}:
                errors.append(f"{label}: reuse cannot be claimed at adoption status {adoption}")
            if len(refs & usage_evidence) < 2:
                errors.append(f"{label}: reuse requires two separately evidenced uses")
        if kind == "team_adoption" and classification != "UNKNOWN":
            if adoption != "team_available":
                errors.append(f"{label}: team-wide language requires team_available")
            if not nonempty_string(brief["governance_approval_ref"]):
                errors.append(f"{label}: team-wide language requires governance approval")
        if (
            kind == "manager_acceptance"
            and classification != "UNKNOWN"
            and simulation == "synthetic_reference"
        ):
            errors.append(f"{label}: synthetic evidence cannot claim manager acceptance")
        if kind == "roi" and classification != "UNKNOWN":
            if brief["evidence_origin"] == "synthetic":
                errors.append(f"{label}: synthetic evidence cannot claim ROI")
            if claim.get("classification") not in {"OBSERVED", "DERIVED"}:
                errors.append(f"{label}: ROI must be OBSERVED or DERIVED")
            if not nonempty_string(claim.get("method")):
                errors.append(f"{label}: ROI requires a declared method")
    if not string_array(brief["known_limitations"], minimum=1):
        errors.append("manager brief: known_limitations must be visible and non-empty")
    if not string_array(brief["unresolved_unknowns"]):
        errors.append("manager brief: unresolved_unknowns must be a string array")
    if not nonempty_string(brief["next_use_entry"]):
        errors.append("manager brief: next_use_entry must be non-empty")
    challenge = brief["human_challenge"]
    errors.extend(
        exact_fields(
            challenge,
            {
                "challenge_present",
                "challenger_role",
                "challenge_summary",
                "resulting_change_or_open_issue",
                "review_ref",
            },
            "human_challenge",
        )
    )
    if isinstance(challenge, dict) and challenge.get("challenge_present") is True:
        for field in (
            "challenger_role",
            "challenge_summary",
            "resulting_change_or_open_issue",
            "review_ref",
        ):
            if not nonempty_string(challenge.get(field)):
                errors.append(f"human_challenge: {field} is required when present")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief")
    parser.add_argument("--evidence-ledger", required=True)
    args = parser.parse_args()
    try:
        brief = load_json(Path(args.brief))
        evidence = load_jsonl(Path(args.evidence_ledger))
        errors = validate_manager_brief(brief, evidence)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(
        f"validated {len(brief['claims'])} manager claim(s) against {len(evidence)} evidence record(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
