#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Shared dependency-light Feature Delivery Harness validation helpers."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
WHITELIST_PATH = BASE_DIR / "schemas" / "record_type_whitelist.json"
SCHEMA_RECORD_FILES = {
    "feature_delivery_case": "feature_delivery_case.v1.schema.json",
    "task.packet": "task.packet.v1.schema.json",
    "delivery.evidence": "delivery.evidence.v1.schema.json",
    "delivery.verdict": "delivery.verdict.v1.schema.json",
    "validation.result": "validation.result.v1.schema.json",
    "yield.stage_breakdown": "yield.stage_breakdown.v1.schema.json",
    "yield.waste_pattern": "yield.waste_pattern.v1.schema.json",
    "yield.optimization_signal": "yield.optimization_signal.v1.schema.json",
    "yield.dossier": "yield.dossier.v1.schema.json",
    "context_pack": "context_pack.v1.schema.json",
    "promotion.candidate": "promotion.candidate.v1.schema.json",
    "promotion.review": "promotion.review.v1.schema.json",
}
ENVELOPE_FIELDS = {"type", "id", "schema", "source", "target", "scope", "payload", "constraints"}
SCOPE_FIELDS = {"project_id", "feature_delivery_case_id", "module_id"}
TOKEN_STATUSES = {"unknown", "estimated", "provider_reported", "known"}
RAW_KEYS = {"raw", "dump", "full_log", "trace", "html", "unbounded_context"}
RAW_TEXT_RE = re.compile(r"(?i)(raw transcript|^assistant:|^user:|otel\.(trace|span)|span_id|trace_id|timestamp=.*level=)", re.MULTILINE)

PAYLOAD_FIELDS: dict[str, set[str]] = {
    "feature_delivery_case": {
        "title",
        "user_usable_outcome",
        "status",
        "scope_summary",
        "in_scope",
        "non_goals",
        "acceptance_criteria",
        "risks",
        "evidence_refs",
        "unresolved_questions",
        "context_token_count",
    },
    "task.packet": {
        "feature_delivery_case_id",
        "objective",
        "allowed_changes",
        "forbidden_changes",
        "target_files",
        "target_areas",
        "acceptance_ids",
        "validation_commands",
        "evidence_requirements",
        "risk_controls",
        "rollback_notes",
        "context_token_count",
        "context_refs",
        "repair_attempts",
        "review_iterations",
        "analysis_fingerprints",
    },
    "delivery.evidence": {
        "feature_delivery_case_id",
        "task_id",
        "evidence_kind",
        "evidence_refs",
        "acceptance_results",
        "validation_summary",
        "user_usable_status",
        "limitations",
    },
    "delivery.verdict": {
        "feature_delivery_case_id",
        "verdict",
        "verdict_reason",
        "delivery_evidence_refs",
        "validation_result_refs",
        "acceptance_summary",
        "unresolved_risks",
        "limitations",
        "conflict_codes",
    },
    "validation.result": {
        "command_id",
        "status",
        "severity",
        "failure_codes",
        "target_acceptance_ids",
        "observed_output_ref",
        "blocking",
        "remediation_hint",
    },
    "yield.stage_breakdown": {
        "feature_delivery_case_id",
        "stage",
        "tokens",
        "cost",
        "source_refs",
        "status",
    },
    "yield.waste_pattern": {
        "feature_delivery_case_id",
        "pattern",
        "severity",
        "detection_method",
        "thresholds",
        "evidence_refs",
        "estimated_token_impact",
        "recommendation",
    },
    "yield.optimization_signal": {
        "feature_delivery_case_id",
        "signal_type",
        "recommendation",
        "expected_effect",
        "evidence_refs",
        "promotion_status",
    },
    "yield.dossier": {
        "feature_delivery_case_id",
        "delivery_status_ref",
        "total_tokens",
        "total_cost",
        "stage_breakdown_refs",
        "waste_pattern_refs",
        "optimization_signal_refs",
        "limitations",
        "claim_ledger",
    },
    "context_pack": {
        "feature_delivery_case_id",
        "purpose",
        "source_refs",
        "included_refs",
        "excluded_refs",
        "projected_items",
        "token_budget",
        "token_estimate",
        "raw_source_policy",
    },
    "promotion.candidate": {
        "feature_delivery_case_id",
        "candidate_kind",
        "candidate_ref",
        "source_refs",
        "scope",
        "evidence_refs",
        "ip_status",
        "promotion_status",
    },
    "promotion.review": {
        "feature_delivery_case_id",
        "candidate_id",
        "reviewer",
        "decision",
        "evidence_refs",
        "validation_refs",
        "resulting_artifact_type",
        "review_notes",
    },
}

REQUIRED_PAYLOAD_FIELDS: dict[str, set[str]] = {
    key: fields - {"context_token_count", "context_refs", "repair_attempts", "review_iterations", "analysis_fingerprints"}
    for key, fields in PAYLOAD_FIELDS.items()
}

ENUMS: dict[tuple[str, str], set[str]] = {
    ("feature_delivery_case", "status"): {"draft", "ready", "in_progress", "delivered", "failed", "blocked"},
    ("delivery.evidence", "user_usable_status"): {
        "usable",
        "not_user_usable",
        "requires_human_review",
        "insufficient_evidence",
        "blocked",
    },
    ("delivery.verdict", "verdict"): {
        "usable",
        "not_user_usable",
        "requires_human_review",
        "insufficient_evidence",
        "blocked",
    },
    ("validation.result", "status"): {"pass", "fail", "warn", "not_run"},
    ("validation.result", "severity"): {"info", "warning", "error", "critical"},
    ("yield.stage_breakdown", "status"): TOKEN_STATUSES,
    ("yield.waste_pattern", "pattern"): {
        "repeated_context_read",
        "oversized_context",
        "duplicate_analysis",
        "failed_repair_loop",
        "review_loop_without_progress",
    },
    ("yield.waste_pattern", "severity"): {"info", "warning", "error", "critical"},
    ("yield.optimization_signal", "promotion_status"): {"candidate", "review_required", "promoted", "rejected"},
    ("promotion.candidate", "candidate_kind"): {"asset", "automation", "skill", "learning", "rule", "contextpack"},
    ("promotion.candidate", "ip_status"): {"synthetic", "open", "sanitized", "review_required"},
    ("promotion.candidate", "promotion_status"): {"candidate", "review_required", "promoted"},
    ("promotion.review", "decision"): {"approved", "rejected", "needs_changes"},
}


def load_whitelist() -> dict[str, str]:
    return json.loads(WHITELIST_PATH.read_text(encoding="utf-8"))


def load_record_schema(record_type: str) -> dict[str, Any]:
    filename = SCHEMA_RECORD_FILES[record_type]
    return json.loads((BASE_DIR / "schemas" / "records" / filename).read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    records: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            failures.append(failure("INVALID_JSON", f"line {line_no}: {exc.msg}", line_no))
            continue
        if not isinstance(record, dict):
            failures.append(failure("NON_OBJECT_RECORD", f"line {line_no}: record must be an object", line_no))
            continue
        record["_line_no"] = line_no
        records.append(record)
    return records, failures


def failure(code: str, message: str, line_no: int | None = None, record_id: str | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"code": code, "message": message}
    if line_no is not None:
        result["line"] = line_no
    if record_id:
        result["id"] = record_id
    return result


def validate_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    whitelist = load_whitelist()
    failures: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for record in records:
        line_no = int(record.get("_line_no", 0)) or None
        record_id = str(record.get("id", ""))
        public_record = {key: value for key, value in record.items() if key != "_line_no"}
        extra_top = set(public_record) - ENVELOPE_FIELDS
        if extra_top:
            failures.append(failure("UNKNOWN_TOP_LEVEL_FIELD", f"unknown top-level fields: {', '.join(sorted(extra_top))}", line_no, record_id))
        missing_top = ENVELOPE_FIELDS - set(public_record)
        if missing_top:
            failures.append(failure("MISSING_ENVELOPE_FIELD", f"missing envelope fields: {', '.join(sorted(missing_top))}", line_no, record_id))
            continue
        if record_id in seen_ids:
            failures.append(failure("DUPLICATE_ID", f"duplicate id: {record_id}", line_no, record_id))
        seen_ids.add(record_id)
        record_type = str(record.get("type", ""))
        expected_schema = whitelist.get(record_type)
        if expected_schema is None:
            failures.append(failure("UNKNOWN_RECORD_TYPE", f"unknown record type: {record_type}", line_no, record_id))
            continue
        if record.get("schema") != expected_schema:
            failures.append(failure("SCHEMA_TYPE_MISMATCH", f"{record_type} must use schema {expected_schema}", line_no, record_id))
        failures.extend(validate_scope(record.get("scope"), line_no, record_id))
        payload = record.get("payload")
        if not isinstance(payload, dict):
            failures.append(failure("MISSING_PAYLOAD_FIELD", "payload must be an object", line_no, record_id))
            continue
        allowed = PAYLOAD_FIELDS[record_type]
        extra_payload = set(payload) - allowed
        if extra_payload:
            failures.append(failure("UNKNOWN_PAYLOAD_FIELD", f"unknown payload fields: {', '.join(sorted(extra_payload))}", line_no, record_id))
        missing_payload = REQUIRED_PAYLOAD_FIELDS[record_type] - set(payload)
        if missing_payload:
            failures.append(failure("MISSING_PAYLOAD_FIELD", f"missing payload fields: {', '.join(sorted(missing_payload))}", line_no, record_id))
        for (enum_type, field), values in ENUMS.items():
            if enum_type == record_type and field in payload and payload[field] not in values:
                failures.append(failure("INVALID_ENUM", f"{field} must be one of {', '.join(sorted(values))}", line_no, record_id))
        failures.extend(validate_json_schema_value(payload, load_record_schema(record_type), "payload", line_no, record_id))
        failures.extend(validate_token_cost_values(record_type, payload, line_no, record_id))
        if contains_raw_context(public_record):
            failures.append(failure("RAW_CONTEXT_FORBIDDEN", "record contains raw context marker or blocked raw payload field", line_no, record_id))
    return failures


def json_type_name(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def matches_json_type(value: Any, expected_type: str) -> bool:
    if expected_type == "null":
        return value is None
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "object":
        return isinstance(value, dict)
    return True


def type_matches(value: Any, expected: Any) -> bool:
    if isinstance(expected, str):
        return matches_json_type(value, expected)
    if isinstance(expected, list):
        return any(isinstance(item, str) and matches_json_type(value, item) for item in expected)
    return True


def validate_json_schema_value(
    value: Any,
    schema: dict[str, Any],
    path: str,
    line_no: int | None,
    record_id: str,
) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    expected_type = schema.get("type")
    if expected_type is not None and not type_matches(value, expected_type):
        expected = ", ".join(expected_type) if isinstance(expected_type, list) else str(expected_type)
        failures.append(failure("INVALID_SCHEMA_VALUE", f"{path} must be {expected}, got {json_type_name(value)}", line_no, record_id))
        return failures
    if "const" in schema and value != schema["const"]:
        failures.append(failure("INVALID_SCHEMA_VALUE", f"{path} must equal {schema['const']!r}", line_no, record_id))
    if "enum" in schema and value not in schema["enum"]:
        failures.append(failure("INVALID_SCHEMA_VALUE", f"{path} must be one of {', '.join(str(item) for item in schema['enum'])}", line_no, record_id))
    if "minimum" in schema and isinstance(value, (int, float)) and not isinstance(value, bool) and value < schema["minimum"]:
        failures.append(failure("INVALID_SCHEMA_VALUE", f"{path} must be at least {schema['minimum']}", line_no, record_id))
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            required = schema.get("required", [])
            if isinstance(required, list):
                missing = sorted(str(item) for item in required if item not in value)
                if missing:
                    failures.append(failure("INVALID_SCHEMA_VALUE", f"{path} missing required fields: {', '.join(missing)}", line_no, record_id))
            if schema.get("additionalProperties") is False:
                extra = sorted(set(value) - set(properties))
                if extra:
                    failures.append(failure("INVALID_SCHEMA_VALUE", f"{path} has unknown fields: {', '.join(extra)}", line_no, record_id))
            for key, subschema in properties.items():
                if key in value and isinstance(subschema, dict):
                    failures.extend(validate_json_schema_value(value[key], subschema, f"{path}.{key}", line_no, record_id))
    if isinstance(value, list) and isinstance(schema.get("items"), dict):
        item_schema = schema["items"]
        for index, item in enumerate(value):
            failures.extend(validate_json_schema_value(item, item_schema, f"{path}[{index}]", line_no, record_id))
    return failures


def validate_scope(scope: Any, line_no: int | None, record_id: str) -> list[dict[str, Any]]:
    if not isinstance(scope, dict):
        return [failure("MISSING_ENVELOPE_FIELD", "scope must be an object", line_no, record_id)]
    failures: list[dict[str, Any]] = []
    extra_scope = set(scope) - SCOPE_FIELDS
    missing_scope = SCOPE_FIELDS - set(scope)
    if extra_scope:
        failures.append(failure("UNKNOWN_TOP_LEVEL_FIELD", f"unknown scope fields: {', '.join(sorted(extra_scope))}", line_no, record_id))
    if missing_scope:
        failures.append(failure("MISSING_ENVELOPE_FIELD", f"missing scope fields: {', '.join(sorted(missing_scope))}", line_no, record_id))
    if scope.get("project_id") != "lattice":
        failures.append(failure("INVALID_ENUM", "scope.project_id must be lattice", line_no, record_id))
    return failures


def validate_token_cost_values(record_type: str, payload: dict[str, Any], line_no: int | None, record_id: str) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    if record_type == "yield.stage_breakdown":
        for key in ("tokens", "cost"):
            failures.extend(validate_token_cost(payload.get(key), key, line_no, record_id))
    if record_type == "yield.waste_pattern":
        failures.extend(validate_token_cost(payload.get("estimated_token_impact"), "estimated_token_impact", line_no, record_id))
    if record_type == "yield.dossier":
        for key in ("total_tokens", "total_cost"):
            failures.extend(validate_token_cost(payload.get(key), key, line_no, record_id))
    return failures


def validate_token_cost(value: Any, field: str, line_no: int | None, record_id: str) -> list[dict[str, Any]]:
    if not isinstance(value, dict):
        return [failure("INVALID_TOKEN_COST_STATUS", f"{field} must be an object with status", line_no, record_id)]
    if value.get("status") not in TOKEN_STATUSES:
        return [failure("INVALID_TOKEN_COST_STATUS", f"{field}.status must be unknown, estimated, provider_reported, or known", line_no, record_id)]
    for required in ("value", "unit", "source_ref"):
        if required not in value:
            return [failure("INVALID_TOKEN_COST_STATUS", f"{field} missing {required}", line_no, record_id)]
    return []


def contains_raw_context(value: Any) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).lower() in RAW_KEYS:
                return True
            if contains_raw_context(item):
                return True
    elif isinstance(value, list):
        return any(contains_raw_context(item) for item in value)
    elif isinstance(value, str):
        return bool(RAW_TEXT_RE.search(value))
    return False


def validation_result_record(code: str, message: str, case_id: str = "unknown", source: str = "fdh-validator") -> dict[str, Any]:
    return {
        "type": "validation.result",
        "id": f"validation_{code.lower()}",
        "schema": "lat.validation.result.v1",
        "source": source,
        "target": "feature-delivery-harness-mvp",
        "scope": {
            "project_id": "lattice",
            "feature_delivery_case_id": case_id,
            "module_id": "deliveryyield",
        },
        "payload": {
            "command_id": source,
            "status": "fail",
            "severity": "error",
            "failure_codes": [code],
            "target_acceptance_ids": [],
            "observed_output_ref": message,
            "blocking": True,
            "remediation_hint": message,
        },
        "constraints": {},
    }


def stable_json(record: dict[str, Any]) -> str:
    return json.dumps(record, sort_keys=True, separators=(",", ":"))


def records_by_type(records: list[dict[str, Any]], record_type: str) -> list[dict[str, Any]]:
    return [record for record in records if record.get("type") == record_type]


def list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []
