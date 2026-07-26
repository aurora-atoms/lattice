#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate a bounded Experience-to-Asset record set and generate a Reusable Asset Dossier."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_TYPES = {
    "experience.contribution",
    "reusable_asset.candidate",
    "reusable_asset.change_proposal",
    "reusable_asset.review",
    "reusable_asset.usage_observation",
}
ASSET_TYPES = {
    "skill", "workflow", "context_pack", "prompt_pattern", "rule", "instruction",
    "script", "schema", "eval_case", "failure_pattern", "reference",
    "architecture_decision", "capability_profile", "manager_dossier",
}
ACTIVATION_MODES = {"never_by_default", "task_scoped", "profile_selected", "team_available"}
MATURITY = {"idea", "draft", "runnable", "qualified_for_scope", "used_once", "reused", "team_available", "deprecated"}
OPERATIONS = {"create", "update", "split", "merge", "reclassify", "deprecate"}
OUTCOMES = {
    "completed_as_requested", "partially_completed", "usable_with_revision", "artifact_created",
    "accepted_by_reviewer", "merged", "not_evaluated", "outcome_unclear", "blocked", "abandoned",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_no}: invalid JSON: {exc.msg}") from exc
        if not isinstance(record, dict):
            raise ValueError(f"line {line_no}: record must be an object")
        records.append(record)
    return records


def require(payload: dict[str, Any], fields: set[str], record_id: str) -> list[str]:
    missing = sorted(field for field in fields if field not in payload)
    return [f"{record_id}: missing payload fields: {', '.join(missing)}"] if missing else []


def validate(records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    ids: set[str] = set()
    by_type: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        record_id = str(record.get("id", ""))
        record_type = str(record.get("type", ""))
        if not record_id or not record_type or not isinstance(record.get("payload"), dict):
            errors.append("each record requires type, id, and object payload")
            continue
        if record_id in ids:
            errors.append(f"duplicate id: {record_id}")
        ids.add(record_id)
        by_type.setdefault(record_type, []).append(record)
    missing_types = sorted(REQUIRED_TYPES - set(by_type))
    if missing_types:
        errors.append("missing record types: " + ", ".join(missing_types))
    if errors:
        return errors

    contribution = by_type["experience.contribution"][0]
    candidate = by_type["reusable_asset.candidate"][0]
    proposal = by_type["reusable_asset.change_proposal"][0]
    review = by_type["reusable_asset.review"][0]
    usage = by_type["reusable_asset.usage_observation"][0]
    cp = contribution["payload"]
    ap = candidate["payload"]
    pp = proposal["payload"]
    rp = review["payload"]
    up = usage["payload"]

    errors += require(cp, {"feature_delivery_case_id", "source_ref", "contributor", "contribution_kind", "original_text", "evidence_class", "captured_at"}, contribution["id"])
    errors += require(ap, {"feature_delivery_case_id", "asset_id", "name", "version", "asset_type", "created_from_contribution_refs", "problem_addressed", "summary", "current_scope", "out_of_scope", "artifact_location", "activation_mode", "current_status", "known_limitations", "open_questions", "owner", "evidence_refs"}, candidate["id"])
    errors += require(pp, {"candidate_id", "operation", "contribution_refs", "proposed_changes", "evidence_refs", "status"}, proposal["id"])
    errors += require(rp, {"candidate_id", "proposal_id", "reviewer", "decision", "review_notes", "evidence_refs", "validation_refs", "reviewed_at"}, review["id"])
    errors += require(up, {"asset_id", "version", "feature_delivery_case_id", "used_for", "user_role", "outcome_status", "evidence_refs", "observed_at"}, usage["id"])

    if ap.get("asset_type") not in ASSET_TYPES:
        errors.append(f"{candidate['id']}: invalid asset_type")
    if ap.get("activation_mode") not in ACTIVATION_MODES:
        errors.append(f"{candidate['id']}: invalid activation_mode")
    if ap.get("current_status") not in MATURITY:
        errors.append(f"{candidate['id']}: invalid current_status")
    if pp.get("operation") not in OPERATIONS:
        errors.append(f"{proposal['id']}: invalid operation")
    if rp.get("decision") not in {"approved", "rejected", "needs_changes"}:
        errors.append(f"{review['id']}: invalid decision")
    if up.get("outcome_status") not in OUTCOMES:
        errors.append(f"{usage['id']}: invalid outcome_status")
    if contribution["id"] not in ap.get("created_from_contribution_refs", []):
        errors.append("candidate must preserve the originating contribution reference")
    if candidate["id"] != pp.get("candidate_id") or candidate["id"] != rp.get("candidate_id"):
        errors.append("proposal and review must reference the candidate record id")
    if proposal["id"] != rp.get("proposal_id"):
        errors.append("review must reference the change proposal record id")
    if ap.get("asset_id") != up.get("asset_id") or ap.get("version") != up.get("version"):
        errors.append("usage observation must reference the candidate asset id and version")
    if ap.get("feature_delivery_case_id") != cp.get("feature_delivery_case_id") or ap.get("feature_delivery_case_id") != up.get("feature_delivery_case_id"):
        errors.append("all vertical-slice records must share one Feature Delivery Case")
    if rp.get("decision") != "approved" and ap.get("activation_mode") != "never_by_default":
        errors.append("unapproved assets must remain never_by_default")
    if rp.get("decision") != "approved" and ap.get("current_status") in {"qualified_for_scope", "used_once", "reused", "team_available"}:
        errors.append("unapproved assets cannot claim qualified or used maturity")
    if ap.get("activation_mode") == "team_available" and rp.get("decision") != "approved":
        errors.append("team_available activation requires approved human review")
    return errors


def render_dossier(records: list[dict[str, Any]]) -> str:
    by_type = {record["type"]: record for record in records}
    contribution = by_type["experience.contribution"]
    candidate = by_type["reusable_asset.candidate"]
    review = by_type["reusable_asset.review"]
    usage = by_type["reusable_asset.usage_observation"]
    cp, ap, rp, up = contribution["payload"], candidate["payload"], review["payload"], usage["payload"]
    limitations = "\n".join(f"- {item}" for item in ap["known_limitations"]) or "- None recorded"
    questions = "\n".join(f"- {item}" for item in ap["open_questions"]) or "- None recorded"
    return f"""# Reusable Asset Dossier v0.1

## Asset
- Asset ID: `{ap['asset_id']}`
- Name: {ap['name']}
- Version: `{ap['version']}`
- Type: `{ap['asset_type']}`
- Status: `{ap['current_status']}`
- Activation: `{ap['activation_mode']}`
- Owner: {ap['owner']}

## Origin
- Feature Delivery Case: `{ap['feature_delivery_case_id']}`
- Contribution: `{contribution['id']}`
- Source: `{cp['source_ref']}`
- Contribution kind: `{cp['contribution_kind']}`

## Problem Addressed
{ap['problem_addressed']}

## Summary
{ap['summary']}

## Scope
- Current scope: {ap['current_scope']}
- Out of scope: {ap['out_of_scope']}
- Artifact: `{ap['artifact_location']}`

## Human Review
- Decision: `{rp['decision']}`
- Reviewer: {rp['reviewer']}
- Notes: {rp['review_notes']}

## Observed Usage
- Used for: {up['used_for']}
- User role: `{up['user_role']}`
- Outcome: `{up['outcome_status']}`
- Evidence: {', '.join(f'`{item}`' for item in up['evidence_refs'])}

## Known Limitations
{limitations}

## Open Questions
{questions}

## Next Iteration
{ap.get('next_iteration', 'Not specified')}

This dossier reports a scoped, evidence-linked asset state. It does not prove organization-wide ROI or authorize automatic promotion.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", help="Experience-to-Asset JSONL input")
    parser.add_argument("--out", required=True, help="Markdown dossier output")
    parser.add_argument("--expected", help="Optional golden Markdown file")
    args = parser.parse_args()
    try:
        records = load_jsonl(Path(args.jsonl))
        errors = validate(records)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    dossier = render_dossier(records)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(dossier, encoding="utf-8", newline="\n")
    if args.expected:
        expected = Path(args.expected).read_text(encoding="utf-8")
        if dossier.strip() != expected.strip():
            print("generated dossier differs from expected golden", file=sys.stderr)
            return 1
    print(f"validated reusable asset loop and wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
