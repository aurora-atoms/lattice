#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Observed-evidence gate for Blind Challenge Execution.

This gate is intentionally narrow. The Blind Challenge validator still owns its
existing candidate/evaluation semantics. This module adds two fail-closed rules
identified by the post-Case-0A audit:

1. a `downstream_observed` execution must carry non-empty, URI-like evidence at
   every result layer; and
2. any `scoped_canary` decision, plus every downstream-observed execution, must
   be bound to a successfully authenticated Reserved Evaluation Handoff v2
   attestation.

The v2 handoff validator remains the cryptographic authority. This module only
composes that verified attestation with the Blind Challenge receipt and checks
that the reserved result and attestation metadata are the same facts.
"""

from __future__ import annotations

import re
from typing import Any

import validate_reserved_evaluation_handoff_v2 as HANDOFF_V2

EVIDENCE_REF = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*://\S+$")


def _refs(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _require_refs(errors: list[str], value: Any, path: str) -> None:
    refs = _refs(value)
    if not refs:
        errors.append(f"{path} requires non-empty evidence_refs for downstream_observed")
        return
    invalid = [ref for ref in refs if not EVIDENCE_REF.match(ref)]
    if invalid:
        errors.append(
            f"{path} evidence_refs must be URI-like evidence references: "
            + ", ".join(invalid)
        )


def _reserved_result(execution: dict[str, Any]) -> dict[str, Any] | None:
    for result in execution.get("case_results", []):
        if isinstance(result, dict) and result.get("class") == "reserved":
            return result
    return None


def _attestation(records: list[dict[str, Any]] | None) -> dict[str, Any] | None:
    if not isinstance(records, list) or len(records) != 2:
        return None
    record = records[1]
    if not isinstance(record, dict) or record.get("type") != HANDOFF_V2.ATTESTATION_TYPE:
        return None
    return record


def _validate_downstream_evidence(execution: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if execution.get("simulation_status") != "downstream_observed":
        return errors

    if execution.get("status") != "evaluated":
        errors.append("downstream_observed Blind Challenge must be status=evaluated")
    if execution.get("downstream_adoption_status") not in {"observed_once", "reused"}:
        errors.append(
            "downstream_observed Blind Challenge requires downstream_adoption_status "
            "observed_once or reused"
        )

    _require_refs(errors, execution.get("evidence_refs"), "execution")

    results = execution.get("case_results", [])
    if not isinstance(results, list):
        return errors
    for result_index, result in enumerate(results):
        if not isinstance(result, dict):
            continue
        case_id = str(result.get("case_id", result_index))
        path = f"case_results[{case_id}]"
        _require_refs(errors, result.get("evidence_refs"), path)

        variants = result.get("variant_outcomes", [])
        if isinstance(variants, list):
            for variant_index, variant in enumerate(variants):
                if not isinstance(variant, dict):
                    continue
                label = str(variant.get("label", variant_index))
                _require_refs(
                    errors,
                    variant.get("evidence_refs"),
                    f"{path}.variant_outcomes[{label}]",
                )

        metrics = result.get("protected_metrics", [])
        if isinstance(metrics, list):
            for metric_index, metric in enumerate(metrics):
                if not isinstance(metric, dict):
                    continue
                name = str(metric.get("metric", metric_index))
                _require_refs(
                    errors,
                    metric.get("evidence_refs"),
                    f"{path}.protected_metrics[{name}]",
                )

    return errors


def _validate_attestation_binding(
    execution: dict[str, Any],
    candidate: dict[str, Any],
    *,
    handoff_records: list[dict[str, Any]] | None,
    blocked_execution: dict[str, Any] | None,
    handoff_schema: dict[str, Any] | None,
    trust_store: dict[str, Any] | None,
    consumed_nonces: set[str] | None,
) -> list[str]:
    errors: list[str] = []
    decision = execution.get("decision")
    verdict = str(decision.get("verdict", "")) if isinstance(decision, dict) else ""
    needs_verified_attestation = (
        execution.get("simulation_status") == "downstream_observed"
        or verdict == "scoped_canary"
    )
    if not needs_verified_attestation:
        return errors

    missing: list[str] = []
    if handoff_records is None:
        missing.append("reserved handoff v2 records")
    if blocked_execution is None:
        missing.append("blocked source execution")
    if handoff_schema is None:
        missing.append("reserved handoff v2 schema")
    if trust_store is None:
        missing.append("trusted evaluator key store")
    if consumed_nonces is None:
        missing.append("consumed nonce ledger")
    if missing:
        errors.append(
            "downstream_observed/scoped_canary requires verified reserved attestation context: "
            + ", ".join(missing)
        )
        return errors

    assert handoff_records is not None
    assert blocked_execution is not None
    assert handoff_schema is not None
    assert trust_store is not None
    assert consumed_nonces is not None

    trust_errors = HANDOFF_V2.validate_handoff(
        handoff_records,
        candidate,
        blocked_execution,
        handoff_schema,
        trust_store=trust_store,
        consumed_nonces=consumed_nonces,
    )
    if trust_errors:
        errors.extend(f"trusted reserved attestation: {error}" for error in trust_errors)
        return errors

    if execution.get("execution_id") != blocked_execution.get("execution_id"):
        errors.append(
            "evaluated Blind Challenge execution_id must preserve blocked execution lineage"
        )

    attestation = _attestation(handoff_records)
    if attestation is None:
        errors.append("verified reserved attestation stream must contain request + attestation")
        return errors
    payload = attestation.get("payload")
    if not isinstance(payload, dict):
        errors.append("verified reserved attestation payload is required")
        return errors

    attested_result = payload.get("reserved_case_result")
    execution_result = _reserved_result(execution)
    if not isinstance(attested_result, dict) or not isinstance(execution_result, dict):
        errors.append("verified reserved attestation and execution both require reserved result")
    elif execution_result != attested_result:
        errors.append(
            "Blind Challenge reserved result must exactly match authenticated attestation projection"
        )

    oracle = execution.get("reserved_oracle")
    if not isinstance(oracle, dict):
        errors.append("evaluated Blind Challenge requires reserved_oracle metadata")
        return errors

    identity = payload.get("evaluator_identity")
    evaluator_id = (
        str(identity.get("evaluator_id", "")) if isinstance(identity, dict) else ""
    )
    expected = {
        "attestation_ref": payload.get("attestation_ref"),
        "attestation_hash": payload.get("attestation_canonical_digest"),
        "evaluated_by": evaluator_id,
        "evaluated_at": payload.get("evaluated_at"),
    }
    for field, value in expected.items():
        if oracle.get(field) != value:
            errors.append(
                f"reserved_oracle.{field} must match authenticated attestation"
            )

    attestation_ref = str(payload.get("attestation_ref", ""))
    if attestation_ref and attestation_ref not in _refs(execution.get("evidence_refs")):
        errors.append(
            "downstream_observed/scoped_canary execution evidence_refs must include "
            "authenticated attestation_ref"
        )

    return errors


def validate_observed_evidence(
    execution: dict[str, Any],
    candidate: dict[str, Any],
    *,
    handoff_records: list[dict[str, Any]] | None = None,
    blocked_execution: dict[str, Any] | None = None,
    handoff_schema: dict[str, Any] | None = None,
    trust_store: dict[str, Any] | None = None,
    consumed_nonces: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []

    simulation_status = execution.get("simulation_status")
    adoption_status = execution.get("downstream_adoption_status")
    if simulation_status == "synthetic_reference" and adoption_status != "not_observed":
        errors.append(
            "synthetic_reference Blind Challenge cannot claim downstream adoption"
        )

    errors.extend(_validate_downstream_evidence(execution))
    errors.extend(
        _validate_attestation_binding(
            execution,
            candidate,
            handoff_records=handoff_records,
            blocked_execution=blocked_execution,
            handoff_schema=handoff_schema,
            trust_store=trust_store,
            consumed_nonces=consumed_nonces,
        )
    )
    return errors
