#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Ingest one authenticated Reserved Evaluation Handoff v2 attestation.

This is a deterministic boundary adapter, not a verdict engine. It validates the
blocked Blind Challenge source, verifies the v2 request/attestation through the
existing cryptographic trust boundary, and emits only a public-safe reserved-result
projection plus readiness metadata. It never reveals A/B mapping, emits a governed
verdict, or grants promotion authority.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

import validate_blind_challenge_execution as BLIND
import validate_reserved_evaluation_handoff_v2 as HANDOFF

CONTRACT = "lat.reserved_evaluation_ingest_result.v1"
MISSION = "lat.goal.verified-decision-yield.v1"
DEFAULT_SCHEMA = (
    Path(__file__).resolve().parents[1]
    / "schemas"
    / "capability"
    / "reserved-evaluation-ingest-result.v1.schema.json"
)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def canonical_ingest_digest(result: dict[str, Any]) -> str:
    material = copy.deepcopy(result)
    material.pop("ingest_canonical_digest", None)
    payload = json.dumps(
        material,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def schema_errors(result: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors: list[str] = []
    for error in sorted(
        validator.iter_errors(result),
        key=lambda item: (
            tuple(str(part) for part in item.absolute_path),
            item.message,
        ),
    ):
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"{location}: {error.message}")
    return errors


def _allocation_ids(candidate: dict[str, Any]) -> set[str]:
    plan = candidate.get("evaluation_plan", {})
    allocations = plan.get("case_allocations", []) if isinstance(plan, dict) else []
    return {
        str(item.get("case_id"))
        for item in allocations
        if isinstance(item, dict) and item.get("case_id")
    }


def _source_case_ids(execution: dict[str, Any]) -> tuple[set[str], list[str]]:
    errors: list[str] = []
    seen: set[str] = set()
    results = execution.get("case_results", [])
    if not isinstance(results, list):
        return set(), ["blocked execution case_results must be a list"]
    for index, result in enumerate(results):
        if not isinstance(result, dict):
            errors.append(f"blocked execution case_results[{index}] must be an object")
            continue
        case_id = str(result.get("case_id", ""))
        if not case_id:
            errors.append(f"blocked execution case_results[{index}] requires case_id")
        elif case_id in seen:
            errors.append(f"blocked execution contains duplicate case result: {case_id}")
        seen.add(case_id)
    return seen, errors


def _safe_refs(value: Any) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            if key == "evidence_refs" and isinstance(nested, list):
                refs.update(str(item) for item in nested)
            else:
                refs.update(_safe_refs(nested))
    elif isinstance(value, list):
        for nested in value:
            refs.update(_safe_refs(nested))
    return refs


def _expected_projection(
    candidate: dict[str, Any],
    blocked_execution: dict[str, Any],
    reserved_case_result: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    allocation_ids = _allocation_ids(candidate)
    if not allocation_ids:
        errors.append("candidate evaluation plan must define case allocations")

    source_ids, source_errors = _source_case_ids(blocked_execution)
    errors.extend(source_errors)
    reserved_case_id = str(reserved_case_result.get("case_id", ""))
    if reserved_case_id in source_ids:
        errors.append("blocked execution must not already contain the reserved case result")
    merged = source_ids | ({reserved_case_id} if reserved_case_id else set())
    extra = merged - allocation_ids
    if extra:
        errors.append("ingested case ids are outside the frozen allocation: " + ", ".join(sorted(extra)))
    missing = allocation_ids - merged
    settled = bool(allocation_ids) and not missing and not extra
    return {
        "source_status": "blocked_pending_reserved_oracle",
        "reserved_oracle_status": "available",
        "merged_case_ids": sorted(merged),
        "missing_case_ids": sorted(missing),
        "all_allocations_settled": settled,
        "ready_for_governed_adjudication": settled,
    }, errors


def build_ingest_result(
    records: list[dict[str, Any]],
    candidate: dict[str, Any],
    blocked_execution: dict[str, Any],
    handoff_schema: dict[str, Any],
    trust_store: dict[str, Any],
    consumed_nonces: set[str],
    result_schema: dict[str, Any],
) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []

    source_errors = BLIND.validate_execution(blocked_execution, candidate)
    if source_errors:
        errors.extend(f"blocked execution: {error}" for error in source_errors)

    handoff_errors = HANDOFF.validate_handoff(
        records,
        candidate,
        blocked_execution,
        handoff_schema,
        trust_store=trust_store,
        consumed_nonces=consumed_nonces,
    )
    if handoff_errors:
        errors.extend(f"reserved handoff: {error}" for error in handoff_errors)

    if len(records) != 2:
        errors.append("ingestion requires exactly one authenticated request and one attestation")
    if errors:
        return None, errors

    request = records[0]
    attestation = records[1]
    request_payload = request.get("payload")
    attestation_payload = attestation.get("payload")
    if not isinstance(request_payload, dict) or not isinstance(attestation_payload, dict):
        return None, ["request and attestation payloads must be objects"]

    reserved_case_result = attestation_payload.get("reserved_case_result")
    identity = attestation_payload.get("evaluator_identity")
    if not isinstance(reserved_case_result, dict) or not isinstance(identity, dict):
        return None, ["attestation must contain reserved_case_result and evaluator_identity"]

    projection, projection_errors = _expected_projection(
        candidate,
        blocked_execution,
        reserved_case_result,
    )
    errors.extend(projection_errors)

    safe_refs = _safe_refs(reserved_case_result)
    attestation_ref = str(attestation_payload.get("attestation_ref", ""))
    if attestation_ref:
        safe_refs.add(attestation_ref)
    unsafe = sorted(
        ref
        for ref in safe_refs
        if not ref.startswith(HANDOFF.SAFE_EVIDENCE_PREFIXES)
    )
    if unsafe:
        errors.append("ingested reserved result contains unsafe evidence refs: " + ", ".join(unsafe))

    result: dict[str, Any] = {
        "$schema": "../../schemas/capability/reserved-evaluation-ingest-result.v1.schema.json",
        "contract": CONTRACT,
        "source_execution_id": blocked_execution.get("execution_id"),
        "candidate_id": candidate.get("candidate_id"),
        "candidate_version": candidate.get("version"),
        "mission_anchor_ref": MISSION,
        "simulation_status": blocked_execution.get("simulation_status"),
        "downstream_adoption_status": blocked_execution.get("downstream_adoption_status"),
        "data_classification": blocked_execution.get("data_classification"),
        "request": {
            "request_nonce": request_payload.get("request_nonce"),
            "variant_bundle_ref": request_payload.get("variant_bundle_ref"),
            "variant_bundle_digest": request_payload.get("variant_bundle_digest"),
        },
        "attestation": {
            "attestation_ref": attestation_ref,
            "attestation_canonical_digest": attestation_payload.get("attestation_canonical_digest"),
            "evaluator_id": identity.get("evaluator_id"),
            "key_id": identity.get("key_id"),
            "evaluated_at": attestation_payload.get("evaluated_at"),
            "signature_verified": True,
            "trust_verified": True,
        },
        "reserved_case_result": copy.deepcopy(reserved_case_result),
        "projection": projection,
        "human_gate": {
            "governed_verdict_included": False,
            "variant_mapping_included": False,
            "governed_verdict_allowed": False,
            "automatic_promotion_allowed": False,
            "team_available_allowed": False,
            "human_decision_required": True,
        },
        "safe_evidence_refs": sorted(safe_refs),
    }
    result["ingest_canonical_digest"] = canonical_ingest_digest(result)

    errors.extend(schema_errors(result, result_schema))
    errors.extend(
        validate_ingest_result(
            result,
            records,
            candidate,
            blocked_execution,
        )
    )
    if errors:
        return None, errors
    return result, []


def validate_ingest_result(
    result: dict[str, Any],
    records: list[dict[str, Any]],
    candidate: dict[str, Any],
    blocked_execution: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    if result.get("contract") != CONTRACT:
        errors.append(f"contract must be {CONTRACT}")
    if result.get("mission_anchor_ref") != MISSION:
        errors.append(f"mission_anchor_ref must be {MISSION}")
    if result.get("source_execution_id") != blocked_execution.get("execution_id"):
        errors.append("source_execution_id must match blocked Blind Challenge execution")
    if result.get("candidate_id") != candidate.get("candidate_id"):
        errors.append("candidate_id must match Harness Mutation Candidate")
    if result.get("candidate_version") != candidate.get("version"):
        errors.append("candidate_version must match Harness Mutation Candidate")
    for field in ("simulation_status", "downstream_adoption_status", "data_classification"):
        if result.get(field) != blocked_execution.get(field):
            errors.append(f"{field} must be inherited from blocked execution")

    if len(records) != 2:
        return errors + ["ingest result validation requires request + attestation records"]
    request_payload = records[0].get("payload", {})
    attestation_payload = records[1].get("payload", {})
    if not isinstance(request_payload, dict) or not isinstance(attestation_payload, dict):
        return errors + ["request and attestation payloads must be objects"]

    expected_request = {
        "request_nonce": request_payload.get("request_nonce"),
        "variant_bundle_ref": request_payload.get("variant_bundle_ref"),
        "variant_bundle_digest": request_payload.get("variant_bundle_digest"),
    }
    if result.get("request") != expected_request:
        errors.append("request projection must exactly match authenticated request")

    identity = attestation_payload.get("evaluator_identity", {})
    expected_attestation = {
        "attestation_ref": attestation_payload.get("attestation_ref"),
        "attestation_canonical_digest": attestation_payload.get("attestation_canonical_digest"),
        "evaluator_id": identity.get("evaluator_id") if isinstance(identity, dict) else None,
        "key_id": identity.get("key_id") if isinstance(identity, dict) else None,
        "evaluated_at": attestation_payload.get("evaluated_at"),
        "signature_verified": True,
        "trust_verified": True,
    }
    if result.get("attestation") != expected_attestation:
        errors.append("attestation projection must exactly match authenticated attestation")

    reserved_case_result = attestation_payload.get("reserved_case_result")
    if result.get("reserved_case_result") != reserved_case_result:
        errors.append("reserved_case_result must exactly match authenticated attestation")

    if isinstance(reserved_case_result, dict):
        expected_projection, projection_errors = _expected_projection(
            candidate,
            blocked_execution,
            reserved_case_result,
        )
        errors.extend(projection_errors)
        if result.get("projection") != expected_projection:
            errors.append("projection does not match frozen allocation settlement state")

        expected_refs = _safe_refs(reserved_case_result)
        attestation_ref = str(attestation_payload.get("attestation_ref", ""))
        if attestation_ref:
            expected_refs.add(attestation_ref)
        if result.get("safe_evidence_refs") != sorted(expected_refs):
            errors.append("safe_evidence_refs must be the exact public-safe attestation projection")

    expected_gate = {
        "governed_verdict_included": False,
        "variant_mapping_included": False,
        "governed_verdict_allowed": False,
        "automatic_promotion_allowed": False,
        "team_available_allowed": False,
        "human_decision_required": True,
    }
    if result.get("human_gate") != expected_gate:
        errors.append("ingestion result must stop before mapping, verdict, canary, or promotion authority")

    expected_digest = canonical_ingest_digest(result)
    if result.get("ingest_canonical_digest") != expected_digest:
        errors.append("ingest_canonical_digest does not match canonical ingest result")
    return errors


def consume_nonce(path: Path, nonce: str) -> None:
    existing = HANDOFF.load_consumed_nonces(path)
    if nonce in existing:
        raise ValueError("request nonce is already consumed")
    original = path.read_text(encoding="utf-8")
    prefix = original if not original or original.endswith("\n") else original + "\n"
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(prefix + nonce + "\n", encoding="utf-8")
    temp.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("handoff", help="Completed Reserved Evaluation Handoff v2 JSONL")
    parser.add_argument("candidate", help="Harness Mutation Candidate JSON")
    parser.add_argument("blocked_execution", help="Blocked Blind Challenge Execution JSON")
    parser.add_argument("--handoff-schema", required=True, help="Reserved Evaluation Handoff v2 schema")
    parser.add_argument("--trust-store", required=True, help="Trusted evaluator public-key store")
    parser.add_argument("--consumed-nonces", required=True, help="Consumed request nonce ledger")
    parser.add_argument(
        "--result-schema",
        default=str(DEFAULT_SCHEMA),
        help="Reserved Evaluation Ingest Result schema",
    )
    parser.add_argument("--output", help="Write deterministic ingest result JSON to this path")
    parser.add_argument(
        "--commit-nonce",
        action="store_true",
        help="After successful ingestion, atomically append the request nonce to the consumed ledger",
    )
    args = parser.parse_args()

    try:
        records = HANDOFF.load_jsonl(Path(args.handoff))
        candidate = load_json(Path(args.candidate))
        blocked_execution = load_json(Path(args.blocked_execution))
        handoff_schema = load_json(Path(args.handoff_schema))
        trust_store = load_json(Path(args.trust_store))
        consumed_path = Path(args.consumed_nonces)
        consumed_nonces = HANDOFF.load_consumed_nonces(consumed_path)
        result_schema = load_json(Path(args.result_schema))
        result, errors = build_ingest_result(
            records,
            candidate,
            blocked_execution,
            handoff_schema,
            trust_store,
            consumed_nonces,
            result_schema,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result, errors = None, [str(exc)]

    if errors or result is None:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = Path(args.output)
        output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)

    if args.commit_nonce:
        try:
            consume_nonce(Path(args.consumed_nonces), str(result["request"]["request_nonce"]))
        except (OSError, ValueError) as exc:
            print(f"error: ingest result created but nonce consumption failed: {exc}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
