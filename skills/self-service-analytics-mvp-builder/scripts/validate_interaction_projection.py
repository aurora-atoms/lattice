#!/usr/bin/env python3
"""Validate the interaction-scoped analytics contract and fail-closed gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "interaction-analytics-projection.v1.schema.json"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected an object")
    return value


def schema_errors(instance: dict[str, Any]) -> list[str]:
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [error.message for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))]


def semantic_errors(instance: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    intent = instance["analytical_intent"]
    reuse = instance["reuse_decision"]
    projection = instance["projection_candidate"]
    status = instance["status"]
    semantic = instance["semantic_continuity"]
    filters = instance["filter_continuity"]
    security = instance["security_scope"]
    grain = instance["grain_cardinality_validation"]
    compute = instance["compute_budget"]
    plan = instance["compute_plan"]
    result = instance["result_validation"]
    promotion = instance["promotion_boundary"]

    if instance["production_approved"] is not False:
        errors.append("production_approved must remain false")
    if promotion["production_approved"] is not False or promotion["gold_promotion_approved"] is not False:
        errors.append("promotion boundary cannot approve production or Gold promotion")

    if reuse == "reuse_existing":
        if projection is not None:
            errors.append("reuse_existing cannot contain a projection_candidate")
        if status != "reuse_existing":
            errors.append("reuse_existing requires status=reuse_existing")
        if plan["mode"] != "reuse":
            errors.append("reuse_existing requires compute_plan.mode=reuse")

    if reuse == "gap_requires_projection" and projection is None:
        errors.append("gap_requires_projection requires projection_candidate")

    if intent["status"] in {"ambiguous", "unknown"}:
        if projection is not None:
            errors.append("ambiguous or unknown intent cannot become an executable projection")
        if status != "ambiguous":
            errors.append("ambiguous or unknown intent requires status=ambiguous")
        if reuse not in {"minimum_clarification", "unknown"}:
            errors.append("ambiguous or unknown intent requires minimum_clarification or unknown")

    if projection is not None:
        parent = instance["parent_semantic_contract"]
        parent_ref = projection["parent_metric_ref"]
        if parent_ref["metric_id"] != parent["metric_id"]:
            errors.append("projection parent metric_id must match parent semantic contract")
        if parent_ref["metric_version"] != parent["metric_version"]:
            errors.append("projection parent metric_version must match parent semantic contract")
        if projection["production_approved"] is not False:
            errors.append("projection production_approved must remain false")
        if projection["security_scope"] != security["authority_ceiling"]:
            errors.append("projection security scope must remain within the declared authority ceiling")

    if semantic["status"] == "passed":
        for field in ("parent_metric_preserved", "metric_version_preserved", "calculation_rule_preserved", "time_semantics_preserved"):
            if semantic[field] is not True:
                errors.append(f"semantic continuity status=passed requires {field}=true")

    if filters["status"] == "passed" and (not filters["material_filters_inherited"] or not filters["scope_not_widened"]):
        errors.append("filter continuity status=passed requires inherited filters and no widening")
    if security["expansion_detected"] and status not in {"blocked", "partial"}:
        errors.append("security scope cannot expand from the interaction")

    ready_statuses = {"display_ready", "reusable_candidate"}
    if status in ready_statuses:
        if semantic["status"] != "passed":
            errors.append("display-ready status requires passed semantic continuity")
        if filters["status"] != "passed":
            errors.append("display-ready status requires passed filter continuity")
        if security["row_level_status"] in {"unknown", "denied"}:
            errors.append("display-ready status requires authorized security scope")
        if grain["status"] != "passed" or grain["fanout_detected"]:
            errors.append("display-ready status requires passed grain/cardinality validation")
        if compute["status"] != "interactive_ready" or plan["mode"] not in {"interactive", "reuse"}:
            errors.append("display-ready status requires an interactive or reuse compute plan")
        if result["status"] != "display_ready":
            errors.append("display-ready status requires result_validation.status=display_ready")

    if status == "projection_candidate":
        if projection is None:
            errors.append("projection_candidate status requires a projection")
        if semantic["status"] != "passed" or filters["status"] != "passed" or grain["status"] != "passed":
            errors.append("projection_candidate status requires passed semantic, filter, and grain gates")
        if security["expansion_detected"] or security["row_level_status"] in {"unknown", "denied"}:
            errors.append("projection_candidate status cannot expand or leave security unresolved")
        if compute["status"] != "interactive_ready":
            errors.append("projection_candidate status requires an interactive-ready compute budget")

    if compute["status"] != "interactive_ready" and status in ready_statuses | {"projection_candidate"}:
        errors.append("interactive-ready status cannot be claimed after a compute-budget failure or async requirement")
    if result["status"] == "failed" and status in ready_statuses | {"projection_candidate"}:
        errors.append("result validation failure prevents display-ready or projection-candidate status")

    gate_statuses = [semantic["status"], filters["status"], grain["status"], compute["status"], result["status"]]
    if "unknown" in gate_statuses and not any(item["blocking"] for item in instance["unknowns"]):
        errors.append("unknown gate status requires a visible blocking unknown")

    if status == "reusable_candidate":
        if promotion["status"] != "reusable_candidate" or not promotion["human_review_required"]:
            errors.append("reusable_candidate requires an explicit human review boundary")

    return errors


def validate_instance(instance: dict[str, Any]) -> list[str]:
    errors = schema_errors(instance)
    if errors:
        return errors
    return semantic_errors(instance)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("instance", type=Path)
    args = parser.parse_args()
    instance = load_json(args.instance)
    errors = validate_instance(instance)
    if errors:
        for error in errors:
            print(error)
        return 1
    print(f"validated {instance['case_id']} against lat.interaction_analytics_projection.v1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
