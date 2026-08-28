#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


RECORD_TYPE = "lat.domain_context_pack.v1"
REF_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*://\S+$")
MODELING_REQUIRED_DIMENSIONS = {
    "entity_boundary",
    "grain",
    "key",
    "source_authority",
    "temporal_semantics",
    "deduplication",
    "schema_scope",
    "gold_fit",
}


def parse_time(value: str) -> datetime:
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    return datetime.fromisoformat(normalized)


def add_unique_error(values: list[Any], label: str, errors: list[str]) -> None:
    normalized = [str(value) for value in values]
    if len(normalized) != len(set(normalized)):
        errors.append(f"{label} values must be unique")


def _validate_modeling_decision(
    pack: dict[str, Any],
    source_by_id: dict[str, dict[str, Any]],
    selected_source_ids: set[str],
    unknown_ids: list[Any],
    blocking_unknown: bool,
    blocking_conflict: bool,
    answer_status: Any,
    errors: list[str],
) -> None:
    task = pack.get("task", {})
    task_origin = task.get("origin") if isinstance(task, dict) else None
    modeling = pack.get("modeling_decision")

    if task_origin != "modeling_decision":
        if modeling is not None:
            errors.append("modeling_decision is only valid when task.origin=modeling_decision")
        return

    if not isinstance(modeling, dict):
        errors.append("task.origin=modeling_decision requires modeling_decision")
        return

    questions = modeling.get("modeling_questions", [])
    question_ids = [
        question.get("question_id")
        for question in questions
        if isinstance(question, dict)
    ]
    add_unique_error(question_ids, "modeling_questions.question_id", errors)

    dimensions = {
        str(question.get("dimension"))
        for question in questions
        if isinstance(question, dict) and question.get("dimension")
    }
    missing_dimensions = MODELING_REQUIRED_DIMENSIONS - dimensions
    if missing_dimensions:
        errors.append(
            "modeling_decision must preserve core modeling questions: "
            + ", ".join(sorted(missing_dimensions))
        )

    blocking_open_question = any(
        isinstance(question, dict)
        and question.get("blocking") is True
        and question.get("status") in {"open", "blocked"}
        for question in questions
    )

    source_roles = modeling.get("source_roles", [])
    for index, source_role in enumerate(source_roles):
        if not isinstance(source_role, dict):
            continue
        source_id = str(source_role.get("source_id", ""))
        if source_id not in source_by_id:
            errors.append(
                f"modeling_decision.source_roles[{index}] references unknown source_id: {source_id}"
            )
        elif source_id not in selected_source_ids:
            errors.append(
                f"modeling_decision.source_roles[{index}] source must have selection_status=selected"
            )
        role = source_role.get("role")
        status = source_role.get("status")
        if role == "authoritative" and status not in {"observed", "verified"}:
            errors.append(
                f"modeling_decision.source_roles[{index}] authoritative role cannot be merely inferred or unknown"
            )
        if role == "unknown_authority" and status == "verified":
            errors.append(
                f"modeling_decision.source_roles[{index}] unknown_authority cannot be verified"
            )
        refs = source_role.get("evidence_refs", [])
        for ref in refs if isinstance(refs, list) else []:
            if not isinstance(ref, str) or not REF_RE.fullmatch(ref):
                errors.append(
                    f"modeling_decision.source_roles[{index}] evidence_ref must be addressable"
                )

    candidate = modeling.get("candidate")
    if not isinstance(candidate, dict):
        errors.append("modeling_decision requires a candidate result, including unknown or blocked")
        return

    candidate_status = candidate.get("status")
    candidate_unknown_refs = set(str(value) for value in candidate.get("unknown_refs", []))
    known_unknown_ids = set(str(value) for value in unknown_ids)
    dangling_unknown_refs = candidate_unknown_refs - known_unknown_ids
    if dangling_unknown_refs:
        errors.append(
            "modeling candidate unknown_refs must reference declared unknowns: "
            + ", ".join(sorted(dangling_unknown_refs))
        )

    refs = candidate.get("evidence_refs", [])
    for ref in refs if isinstance(refs, list) else []:
        if not isinstance(ref, str) or not REF_RE.fullmatch(ref):
            errors.append("modeling candidate evidence_refs must be addressable")

    relationships = candidate.get("relationships", [])
    if isinstance(relationships, list) and relationships and "join_cardinality" not in dimensions:
        errors.append(
            "modeling candidate with relationships requires a join_cardinality modeling question"
        )

    status_to_answerability = {
        "candidate": {"answerable"},
        "partial": {"partial"},
        "unknown": {"partial", "abstain"},
        "blocked": {"blocked"},
    }
    allowed_answerability = status_to_answerability.get(candidate_status)
    if allowed_answerability is not None and answer_status not in allowed_answerability:
        errors.append(
            f"modeling candidate status {candidate_status} is inconsistent with answerability.status={answer_status}"
        )

    if candidate_status == "candidate":
        if blocking_open_question:
            errors.append("modeling candidate cannot be candidate while a blocking modeling question remains open")
        if blocking_unknown:
            errors.append("modeling candidate cannot be candidate while a blocking unknown remains")
        if blocking_conflict:
            errors.append("modeling candidate cannot be candidate while a blocking conflict remains unresolved")
        if candidate.get("gold_fit") != "candidate_fit":
            errors.append("modeling candidate status=candidate requires gold_fit=candidate_fit")
        keys = candidate.get("candidate_keys", [])
        if not isinstance(keys, list) or not keys:
            errors.append("modeling candidate status=candidate requires at least one candidate key")

    if candidate.get("gold_fit") == "failed" and candidate_status != "blocked":
        errors.append("gold_fit=failed requires modeling candidate status=blocked")


def semantic_errors(pack: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if pack.get("record_type") != RECORD_TYPE:
        errors.append(f"record_type must be {RECORD_TYPE}")
        return errors

    try:
        as_of = parse_time(str(pack["as_of_at"]))
    except (KeyError, TypeError, ValueError):
        errors.append("as_of_at must be a valid RFC 3339 date-time")
        return errors

    sources = pack.get("sources", [])
    items = pack.get("context_items", [])
    unknowns = pack.get("unknowns", [])
    conflicts = pack.get("conflicts", [])
    activation_plan = pack.get("activation_plan", [])

    source_ids = [source.get("source_id") for source in sources if isinstance(source, dict)]
    item_ids = [item.get("item_id") for item in items if isinstance(item, dict)]
    unknown_ids = [item.get("unknown_id") for item in unknowns if isinstance(item, dict)]
    conflict_ids = [item.get("conflict_id") for item in conflicts if isinstance(item, dict)]
    add_unique_error(source_ids, "source_id", errors)
    add_unique_error(item_ids, "item_id", errors)
    add_unique_error(unknown_ids, "unknown_id", errors)
    add_unique_error(conflict_ids, "conflict_id", errors)

    source_by_id = {
        str(source.get("source_id")): source
        for source in sources
        if isinstance(source, dict) and source.get("source_id")
    }
    item_by_id = {
        str(item.get("item_id")): item
        for item in items
        if isinstance(item, dict) and item.get("item_id")
    }

    selected_source_ids: set[str] = set()
    conditional_source_ids: set[str] = set()
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            continue
        source_id = str(source.get("source_id", ""))
        selection = source.get("selection_status")
        access = source.get("access_status")
        freshness = source.get("freshness_status")
        authority_for = source.get("authority_for")

        try:
            observed_at = parse_time(str(source.get("observed_at", "")))
            if observed_at > as_of:
                errors.append(f"sources[{index}] observed_at cannot be later than as_of_at")
        except ValueError:
            errors.append(f"sources[{index}].observed_at must be a valid RFC 3339 date-time")

        expires_at = source.get("expires_at")
        if expires_at is not None:
            try:
                expiry = parse_time(str(expires_at))
                if selection == "selected" and expiry < as_of:
                    errors.append(f"sources[{index}] selected source is expired at as_of_at")
            except ValueError:
                errors.append(f"sources[{index}].expires_at must be null or a valid RFC 3339 date-time")

        if selection == "selected":
            selected_source_ids.add(source_id)
            if access != "authorized":
                errors.append(f"sources[{index}] selected source must be authorized")
            if freshness != "current":
                errors.append(f"sources[{index}] selected source must be current")
            if not isinstance(authority_for, list) or not authority_for:
                errors.append(f"sources[{index}] selected source must declare authority_for")
        elif selection == "conditional":
            conditional_source_ids.add(source_id)

    activation_by_target: dict[str, list[str]] = {}
    sequences: list[int] = []
    for entry in activation_plan:
        if not isinstance(entry, dict):
            continue
        target = str(entry.get("target_ref", ""))
        action = str(entry.get("action", ""))
        activation_by_target.setdefault(target, []).append(action)
        if isinstance(entry.get("sequence"), int):
            sequences.append(int(entry["sequence"]))
    add_unique_error(sequences, "activation_plan.sequence", errors)

    allowed_conditional_actions = {
        "load_on_condition",
        "request_permission",
        "request_refresh",
        "human_review",
    }
    for source_id in sorted(conditional_source_ids):
        actions = set(activation_by_target.get(source_id, []))
        if not actions.intersection(allowed_conditional_actions):
            errors.append(
                f"conditional source {source_id} requires an activation action: "
                "load_on_condition, request_permission, request_refresh, or human_review"
            )

    selected_tokens = 0
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        source_id = str(item.get("source_id", ""))
        if source_id not in source_by_id:
            errors.append(f"context_items[{index}] references unknown source_id: {source_id}")
            continue
        if source_id not in selected_source_ids:
            errors.append(f"context_items[{index}] source must have selection_status=selected")
        source = source_by_id[source_id]
        information_class = item.get("information_class")
        authority_for = source.get("authority_for", [])
        if information_class not in authority_for:
            errors.append(
                f"context_items[{index}] information_class is outside source authority_for"
            )
        token_estimate = item.get("token_estimate")
        if isinstance(token_estimate, int):
            selected_tokens += token_estimate
        for ref in item.get("evidence_refs", []) if isinstance(item.get("evidence_refs"), list) else []:
            if not isinstance(ref, str) or not REF_RE.fullmatch(ref):
                errors.append(f"context_items[{index}] evidence_ref must be an addressable URI-like reference")

    budget = pack.get("context_budget", {})
    if isinstance(budget, dict):
        declared_selected = budget.get("selected_tokens")
        max_tokens = budget.get("max_tokens")
        if declared_selected != selected_tokens:
            errors.append(
                f"context_budget.selected_tokens must equal context item token sum ({selected_tokens})"
            )
        if isinstance(max_tokens, int) and selected_tokens > max_tokens:
            errors.append("selected context tokens exceed context_budget.max_tokens")

    known_item_ids = set(item_by_id)
    known_source_ids = set(source_by_id)
    blocking_conflict = False
    for index, conflict in enumerate(conflicts):
        if not isinstance(conflict, dict):
            continue
        for item_ref in conflict.get("item_refs", []) if isinstance(conflict.get("item_refs"), list) else []:
            if item_ref not in known_item_ids:
                errors.append(f"conflicts[{index}] references unknown item_ref: {item_ref}")
        for source_ref in conflict.get("source_refs", []) if isinstance(conflict.get("source_refs"), list) else []:
            if source_ref not in known_source_ids:
                errors.append(f"conflicts[{index}] references unknown source_ref: {source_ref}")
        if conflict.get("blocking") is True and conflict.get("status") == "unresolved":
            blocking_conflict = True

    blocking_unknown = any(
        isinstance(item, dict) and item.get("blocking") is True for item in unknowns
    )

    evidence_summary = pack.get("evidence_summary", {})
    if isinstance(evidence_summary, dict):
        unknown_ref_set = set(str(value) for value in evidence_summary.get("unknown_refs", []))
        missing_unknown_refs = set(str(value) for value in unknown_ids) - unknown_ref_set
        if missing_unknown_refs:
            errors.append(
                "evidence_summary.unknown_refs must preserve every unknown_id: "
                + ", ".join(sorted(missing_unknown_refs))
            )
        for ref in evidence_summary.get("citations", []) if isinstance(evidence_summary.get("citations"), list) else []:
            if not isinstance(ref, str) or not REF_RE.fullmatch(ref):
                errors.append("evidence_summary citations must be addressable URI-like references")

    answerability = pack.get("answerability", {})
    answer_status = answerability.get("status") if isinstance(answerability, dict) else None
    authorization = pack.get("authorization", {})
    auth_decision = authorization.get("decision") if isinstance(authorization, dict) else None

    if auth_decision == "deny":
        if selected_source_ids or items:
            errors.append("authorization decision deny cannot include selected sources or context_items")
        if answer_status != "blocked":
            errors.append("authorization decision deny requires answerability.status=blocked")

    if answer_status == "answerable":
        if not items:
            errors.append("answerability=answerable requires at least one context item")
        if blocking_unknown:
            errors.append("answerability=answerable is invalid while a blocking unknown remains")
        if blocking_conflict:
            errors.append("answerability=answerable is invalid while a blocking conflict remains unresolved")
        citations = evidence_summary.get("citations", []) if isinstance(evidence_summary, dict) else []
        if not citations:
            errors.append("answerability=answerable requires at least one evidence citation")

    _validate_modeling_decision(
        pack,
        source_by_id,
        selected_source_ids,
        unknown_ids,
        blocking_unknown,
        blocking_conflict,
        answer_status,
        errors,
    )

    if pack.get("simulation_status") == "synthetic_reference" and pack.get("downstream_adoption_status") != "not_observed":
        errors.append("synthetic_reference packs must keep downstream_adoption_status=not_observed")

    return errors


def validate_pack(pack: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(pack), key=lambda item: list(item.absolute_path)):
        location = ".".join(str(part) for part in error.absolute_path) or "$"
        errors.append(f"schema {location}: {error.message}")
    errors.extend(semantic_errors(pack))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Domain Context Pack contract and semantics.")
    parser.add_argument("pack", help="Path to domain-context-pack.v1 JSON")
    parser.add_argument(
        "--schema",
        default=str(Path(__file__).resolve().parents[1] / "schemas" / "domain-context-pack.v1.schema.json"),
        help="Path to JSON Schema",
    )
    args = parser.parse_args()

    pack_path = Path(args.pack)
    schema_path = Path(args.schema)
    try:
        pack = json.loads(pack_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not isinstance(pack, dict) or not isinstance(schema, dict):
        print("error: pack and schema roots must be JSON objects", file=sys.stderr)
        return 1

    errors = validate_pack(pack, schema)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"validated Domain Context Pack: {pack_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
