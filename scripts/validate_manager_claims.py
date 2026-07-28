#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate manager claims against a local evidence ledger."""

from __future__ import annotations

import argparse
import json
import re
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
SENSITIVE_CLAIM_PATTERNS = {
    "reuse": (
        r"\bproven reusable\b",
        r"\bhas been reused\b",
        r"\breuse (?:is|was) established\b",
    ),
    "team_adoption": (
        r"\bteam (?:adopted|has adopted|uses|is using)\b",
        r"\bteam-wide adoption\b",
    ),
    "manager_acceptance": (
        r"\bmanagers? (?:accepted|approved|endorsed)\b",
    ),
    "roi": (
        (
            r"\b(?:roi|return on investment|success rate) "
            r"(?:is|was|improved|increased|decreased|equals)\b"
        ),
        r"\b[0-9]+(?:\.[0-9]+)?%\s+(?:roi|success rate)\b",
    ),
}
FORBIDDEN_VALUE_INFERENCE_PATTERNS = (
    r"\bgreen ci proves\b",
    r"\bdeliveryyield approved\b",
    r"\b(?:skill|pr|token|tool-call) counts? prove\b",
)


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


def _markdown_items(values: list[str]) -> str:
    return "\n".join(f"- {value}" for value in values) if values else "- None recorded."


def _render_claim(claim: dict[str, Any]) -> str:
    refs = claim.get("evidence_refs", [])
    ref_text = ", ".join(f"`{ref}`" for ref in refs) if refs else "None"
    details = [
        f"{claim.get('classification')}: {claim.get('statement')}",
        f"Evidence: {ref_text}.",
    ]
    if claim.get("method"):
        details.append(f"Method: {claim['method']}")
    if claim.get("judgment_owner"):
        details.append(f"Judgment owner: {claim['judgment_owner']}.")
    if claim.get("unknown_reason"):
        details.append(f"Unknown reason: {claim['unknown_reason']}")
    return " ".join(details)


def render_manager_brief_markdown(brief: dict[str, Any]) -> str:
    """Render the canonical human-readable projection of a structured brief."""
    claims = [
        claim for claim in brief.get("claims", []) if isinstance(claim, dict)
    ]
    claims_by_kind: dict[str, list[dict[str, Any]]] = {}
    for claim in claims:
        claims_by_kind.setdefault(str(claim.get("claim_kind")), []).append(claim)

    def first_claim(kind: str) -> str:
        values = claims_by_kind.get(kind, [])
        return _render_claim(values[0]) if values else "Required claim is missing."

    primary_kinds = {
        "current_delivery",
        "reusable_asset",
        "before_state",
        "after_state",
        "next_use",
    }
    additional_claims = [
        claim for claim in claims if claim.get("claim_kind") not in primary_kinds
    ]
    claim_limitations = [
        f"`{claim.get('claim_id')}`: {limitation}"
        for claim in claims
        for limitation in claim.get("limitations", [])
        if isinstance(limitation, str)
    ]
    challenge = brief.get("human_challenge", {})
    if not isinstance(challenge, dict):
        challenge = {}
    lines = [
        "# Manager Delivery Brief",
        "",
        (
            "> Synthetic reference only. This is not a real manager deliverable and "
            "does not establish private adoption or business value."
            if brief.get("simulation_status") == "synthetic_reference"
            else "> Private downstream brief. Evidence access and approval remain local."
        ),
        "",
        "## Current Delivery",
        "",
        first_claim("current_delivery"),
        "",
        "## Reusable Asset Left Behind",
        "",
        first_claim("reusable_asset"),
        "",
        "## Observable State Change",
        "",
        f"- Before — {first_claim('before_state')}",
        f"- After — {first_claim('after_state')}",
        "",
        "## Human Challenge",
        "",
        f"- Present: `{str(challenge.get('challenge_present')).lower()}`",
        f"- Challenger role: {challenge.get('challenger_role') or 'Not recorded.'}",
        f"- Summary: {challenge.get('challenge_summary') or 'Not recorded.'}",
        (
            "- Resulting change or open issue: "
            f"{challenge.get('resulting_change_or_open_issue') or 'Not recorded.'}"
        ),
        f"- Review ref: {challenge.get('review_ref') or 'Not recorded.'}",
        "",
        "## Evidence Boundary",
        "",
        f"- Scope: `{brief.get('scope')}`",
        f"- Brief version: `{brief.get('version')}`",
        f"- Simulation status: `{brief.get('simulation_status')}`",
        f"- Adoption status: `{brief.get('downstream_adoption_status')}`",
        f"- Evidence origin: `{brief.get('evidence_origin')}`",
        f"- Asset pack: `{brief.get('asset_pack_id')}`",
        "",
        "## Other Material Claims",
        "",
    ]
    lines.extend(
        f"- `{claim.get('claim_kind')}` / `{claim.get('claim_id')}` — "
        f"{_render_claim(claim)}"
        for claim in additional_claims
    )
    if not additional_claims:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Known Limitations",
            "",
            _markdown_items(brief.get("known_limitations", [])),
            "",
            "Claim-specific limitations:",
            "",
            _markdown_items(claim_limitations),
            "",
            "## Unresolved Unknowns",
            "",
            _markdown_items(brief.get("unresolved_unknowns", [])),
            "",
            "## Next Use",
            "",
            first_claim("next_use"),
            "",
            str(brief.get("next_use_entry") or "Not recorded."),
            "",
            "## Manager Decision",
            "",
            str(brief.get("manager_decision") or "No manager decision requested."),
            "",
            "## Authority References",
            "",
            f"- Human review: {brief.get('human_review_ref') or 'Not recorded.'}",
            (
                "- Governance approval: "
                f"{brief.get('governance_approval_ref') or 'Not recorded.'}"
            ),
            "",
        ]
    )
    return "\n".join(lines)


def validate_rendered_manager_brief(
    brief: dict[str, Any], rendered_path: Path
) -> list[str]:
    if not rendered_path.is_file():
        return [f"manager brief render: missing {rendered_path.name}"]
    actual = rendered_path.read_text(encoding="utf-8")
    expected = render_manager_brief_markdown(brief)
    if actual != expected:
        return [
            "manager brief render: Markdown differs from the canonical structured projection"
        ]
    return []


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
        if claim.get("scope") != brief["scope"]:
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
    elif simulation == "real_downstream" and brief["evidence_origin"] == "synthetic":
        errors.append(
            "manager brief: real downstream brief cannot use synthetic evidence origin"
        )
    if (
        simulation == "real_downstream"
        and adoption in REVIEWED_STATUSES
        and not nonempty_string(brief["human_review_ref"])
    ):
        errors.append(f"manager brief: {adoption} requires human_review_ref")
    if adoption == "team_available" and not nonempty_string(
        brief["governance_approval_ref"]
    ):
        errors.append("manager brief: team_available requires governance_approval_ref")
    for field in ("human_review_ref", "governance_approval_ref"):
        reference = brief[field]
        if reference is not None and str(reference) not in evidence_ids:
            errors.append(f"manager brief: {field} is not present in the evidence ledger")
    governance_authority = str(brief["governance_approval_ref"] or "").lower()
    if "deliveryyield" in governance_authority or "delivery_yield" in governance_authority:
        errors.append("manager brief: DeliveryYield cannot grant governance approval")
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
        statement = str(claim.get("statement", ""))
        refs = set(map(str, claim.get("evidence_refs", [])))
        label = f"claim {claim.get('claim_id', '<missing>')}"
        for expected_kind, patterns in SENSITIVE_CLAIM_PATTERNS.items():
            if not any(re.search(pattern, statement, flags=re.IGNORECASE) for pattern in patterns):
                continue
            if classification == "UNKNOWN":
                errors.append(
                    f"{label}: UNKNOWN statement contains affirmative {expected_kind} wording"
                )
            elif kind != expected_kind:
                errors.append(
                    f"{label}: {expected_kind} wording must use claim_kind {expected_kind}"
                )
        if any(
            re.search(pattern, statement, flags=re.IGNORECASE)
            for pattern in FORBIDDEN_VALUE_INFERENCE_PATTERNS
        ):
            errors.append(
                f"{label}: statement assigns value or approval authority to a forbidden proxy"
            )
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
    decision = str(brief["manager_decision"] or "")
    team_decision = re.search(
        r"\b(?:approve|authorize|adopt|roll out)\b.{0,30}\b(?:team-wide|team)\b",
        decision,
        flags=re.IGNORECASE,
    )
    negated_team_decision = re.search(
        r"\b(?:do not|not to|never)\s+(?:approve|authorize|adopt|roll out)\b"
        r".{0,30}\b(?:team-wide|team)\b",
        decision,
        flags=re.IGNORECASE,
    )
    if team_decision and not negated_team_decision:
        if adoption != "team_available" or not nonempty_string(
            brief["governance_approval_ref"]
        ):
            errors.append(
                "manager brief: team-level manager decision requires team_available "
                "and governance approval"
            )
    if re.search(r"\bdeliveryyield\b.{0,20}\bapprov", decision, flags=re.IGNORECASE):
        errors.append("manager brief: DeliveryYield cannot approve a manager decision")
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
        review_ref = challenge.get("review_ref")
        if nonempty_string(review_ref) and str(review_ref) not in evidence_ids:
            errors.append(
                "human_challenge: review_ref is not present in the evidence ledger"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief")
    parser.add_argument("--evidence-ledger", required=True)
    parser.add_argument(
        "--rendered-brief",
        help="Optional canonical Markdown projection to validate against the JSON brief.",
    )
    args = parser.parse_args()
    try:
        brief = load_json(Path(args.brief))
        evidence = load_jsonl(Path(args.evidence_ledger))
        errors = validate_manager_brief(brief, evidence)
        if args.rendered_brief:
            errors.extend(
                validate_rendered_manager_brief(brief, Path(args.rendered_brief))
            )
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
