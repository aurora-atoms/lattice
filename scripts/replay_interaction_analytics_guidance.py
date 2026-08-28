#!/usr/bin/env python3
"""Deterministic public-safe replay for interaction-driven analytics guidance.

This replay checks the contract and cross-field gates with a synthetic dashboard.
It does not emulate a real BI runtime, DataHub, Databricks, or external-agent
behavior, and it does not prove downstream adoption.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "skills" / "self-service-analytics-mvp-builder" / "scripts"
sys.path.insert(0, str(VALIDATOR_PATH))
from validate_interaction_projection import validate_instance  # noqa: E402


REF = "synthetic://service-operations-dashboard"


def base_case(case_id: str) -> dict[str, Any]:
    return {
        "contract": "lat.interaction_analytics_projection.v1",
        "contract_version": "1.0.0",
        "case_id": case_id,
        "simulation_status": "synthetic_reference",
        "downstream_adoption_status": "not_observed",
        "interaction_snapshot": {
            "dashboard_id": "service-operations-dashboard",
            "dashboard_version": "v5",
            "visual_id": "failure-rate-by-region",
            "visual_type": "bar",
            "selected_mark": "region=Midwest",
            "metric_id": "failure_rate",
            "metric_version": "v3",
            "current_drill_level": "region",
            "filters": {"tenant": "synthetic-tenant", "environment": "prod", "time": "2026-08-01/2026-08-28"},
            "time_range": {"start": "2026-08-01", "end": "2026-08-28"},
            "security_scope_ref": "synthetic://auth/aggregate-only",
            "semantic_model_version": "v5",
            "interaction_timestamp": "2026-08-28T00:00:00Z",
        },
        "analytical_intent": {
            "status": "inferred",
            "intent_id": "breakdown_by_region",
            "evidence_refs": [REF],
            "options": ["breakdown", "trend", "contributors"],
        },
        "parent_semantic_contract": {
            "metric_id": "failure_rate",
            "metric_version": "v3",
            "business_definition": "failed completed requests divided by completed requests",
            "calculation_rule": "exclude cancelled requests from numerator and denominator",
            "population": "completed requests",
            "aggregation_semantics": "rate",
            "filter_scope": "tenant and environment inherited from parent visual",
            "time_semantics": "customer-local day",
            "unit": "ratio",
            "semantic_source_ref": "synthetic://semantic-model/v5/failure_rate",
        },
        "reuse_decision": "gap_requires_projection",
        "projection_candidate": {
            "projection_id": f"projection-{case_id}",
            "question": "Break down the selected failure-rate value by an authorized dimension.",
            "parent_metric_ref": {"metric_id": "failure_rate", "metric_version": "v3"},
            "output_grain": "tenant, environment, firmware_version, customer-local-day",
            "dimensions": ["firmware_version"],
            "filters": {"tenant": "synthetic-tenant", "environment": "prod", "time": "2026-08-01/2026-08-28"},
            "relationships": ["request -> firmware_version is one-to-one for the bounded slice"],
            "source_refs": ["synthetic://semantic-model/v5/failure_rate", "synthetic://data/requests"],
            "security_scope": "aggregate-only within synthetic-tenant",
            "freshness_requirement": "less than 15 minutes",
            "expected_cardinality": "one result per firmware_version and day",
            "compute_budget_ref": "synthetic://compute/interactive-2500ms",
            "evidence_refs": [REF],
            "assumptions": ["firmware_version is an authorized grouped dimension"],
            "unknown_refs": [],
            "production_approved": False,
        },
        "context_refs": [
            {"kind": "interaction", "ref": REF, "purpose": "selected visual and inherited state"},
            {"kind": "semantic", "ref": "synthetic://semantic-model/v5/failure_rate", "purpose": "parent metric contract"},
        ],
        "security_scope": {
            "tenant_scope": "synthetic-tenant",
            "role_class": "operations-manager",
            "row_level_status": "aggregate_only",
            "requested_detail_level": "grouped",
            "authority_ceiling": "aggregate-only within synthetic-tenant",
            "expansion_detected": False,
        },
        "semantic_continuity": {
            "status": "passed",
            "parent_metric_preserved": True,
            "metric_version_preserved": True,
            "calculation_rule_preserved": True,
            "time_semantics_preserved": True,
            "notes": "Child groups reuse the parent failure-rate definition.",
        },
        "filter_continuity": {
            "status": "passed",
            "material_filters_inherited": True,
            "scope_not_widened": True,
            "lost_filters": [],
            "evidence_refs": [REF],
        },
        "grain_cardinality_validation": {
            "status": "passed",
            "join_risk": "one_to_one",
            "fanout_detected": False,
            "evidence_refs": ["synthetic://data/profile/request-firmware"],
            "notes": "Bounded profile found no fanout in the selected slice.",
        },
        "compute_budget": {
            "status": "interactive_ready",
            "latency_budget_ms": 2500,
            "estimated_latency_ms": 420,
            "estimated_scan_scope": "selected 28-day tenant slice",
            "timeout_ms": 2000,
            "notes": "Partition-pruned grouped read stays within interactive budget.",
        },
        "compute_plan": {"mode": "interactive", "source_scope": "selected tenant/time slice", "bounded": True, "timeout_ms": 2000},
        "result_validation": {
            "status": "display_ready",
            "checks": [
                {"check_id": "parent_metric_reconciliation", "status": "passed", "evidence_refs": [REF]},
                {"check_id": "result_cardinality", "status": "passed", "evidence_refs": [REF]},
            ],
            "notes": "Result is validated for the selected grouped slice.",
        },
        "promotion_boundary": {
            "status": "interaction_only",
            "human_review_required": False,
            "production_approved": False,
            "gold_promotion_approved": False,
        },
        "status": "projection_candidate",
        "unknowns": [],
        "evidence_refs": [REF],
        "production_approved": False,
    }


def mutate_cases() -> dict[str, dict[str, Any]]:
    cases: dict[str, dict[str, Any]] = {}

    reuse = base_case("reuse_existing")
    reuse["reuse_decision"] = "reuse_existing"
    reuse["projection_candidate"] = None
    reuse["status"] = "reuse_existing"
    reuse["compute_plan"] = {"mode": "reuse", "source_scope": "certified region drill", "bounded": True, "timeout_ms": 1500}
    reuse["promotion_boundary"]["status"] = "interaction_only"
    cases["reuse_existing"] = reuse

    cases["valid_projection"] = base_case("valid_projection")

    semantic = base_case("semantic_drift")
    semantic["semantic_continuity"].update({"status": "failed", "calculation_rule_preserved": False, "notes": "Generated child query included cancelled requests."})
    semantic["result_validation"].update({"status": "failed", "notes": "Result not safe to display."})
    semantic["status"] = "blocked"
    cases["semantic_drift"] = semantic

    hidden = base_case("hidden_filter_loss")
    hidden["filter_continuity"].update({"status": "failed", "material_filters_inherited": False, "scope_not_widened": False, "lost_filters": ["environment=prod"]})
    hidden["result_validation"].update({"status": "failed", "notes": "Material environment filter was lost."})
    hidden["status"] = "blocked"
    cases["hidden_filter_loss"] = hidden

    security = base_case("security_expansion")
    security["security_scope"].update({"row_level_status": "denied", "requested_detail_level": "row", "expansion_detected": True})
    security["result_validation"].update({"status": "failed", "notes": "Requested detail exceeds authority ceiling."})
    security["status"] = "blocked"
    cases["security_expansion"] = security

    fanout = base_case("fanout")
    fanout["grain_cardinality_validation"].update({"status": "failed", "join_risk": "one_to_many", "fanout_detected": True, "notes": "Request joined to multiple event records."})
    fanout["result_validation"].update({"status": "failed", "notes": "Potential denominator duplication."})
    fanout["status"] = "blocked"
    cases["fanout"] = fanout

    non_additive = base_case("non_additive")
    non_additive["parent_semantic_contract"].update({"metric_id": "p95_processing_latency", "aggregation_semantics": "percentile", "calculation_rule": "95th percentile of request latency"})
    non_additive["interaction_snapshot"].update({"metric_id": "p95_processing_latency"})
    non_additive["projection_candidate"]["parent_metric_ref"].update({"metric_id": "p95_processing_latency"})
    non_additive["result_validation"].update({"status": "failed", "notes": "Child P95 values were averaged."})
    non_additive["status"] = "blocked"
    cases["non_additive"] = non_additive

    ambiguous = base_case("ambiguous_click")
    ambiguous["analytical_intent"] = {"status": "ambiguous", "intent_id": "needs_clarification", "evidence_refs": [REF], "options": ["breakdown", "trend", "contributors"]}
    ambiguous["reuse_decision"] = "minimum_clarification"
    ambiguous["projection_candidate"] = None
    ambiguous["compute_plan"] = {"mode": "not_executable", "source_scope": "not selected", "bounded": True, "timeout_ms": 0}
    ambiguous["result_validation"] = {"status": "not_executed", "checks": [], "notes": "Awaiting a bounded user choice."}
    ambiguous["status"] = "ambiguous"
    cases["ambiguous_click"] = ambiguous

    budget = base_case("compute_budget")
    budget["compute_budget"].update({"status": "async_required", "estimated_latency_ms": 12000, "estimated_scan_scope": "unbounded full history", "notes": "Interactive budget exceeded."})
    budget["compute_plan"] = {"mode": "async", "source_scope": "full history pending explicit async request", "bounded": False, "timeout_ms": 0}
    budget["result_validation"] = {"status": "not_executed", "checks": [], "notes": "No interactive result produced."}
    budget["status"] = "async_required"
    cases["compute_budget"] = budget

    stale = base_case("stale_version")
    stale["context_refs"].append({"kind": "governed_context", "ref": "synthetic://semantic-model/v4/failure_rate", "purpose": "stale context to challenge"})
    stale["semantic_continuity"].update({"status": "unknown", "metric_version_preserved": False, "notes": "Dashboard uses v5 while context describes v4."})
    stale["unknowns"] = [{"unknown_id": "semantic-version-conflict", "statement": "Current deployed semantic version and context version disagree.", "blocking": True}]
    stale["result_validation"].update({"status": "unknown", "notes": "Continuity cannot be established."})
    stale["status"] = "blocked"
    cases["stale_version"] = stale

    reconciliation = base_case("result_reconciliation")
    reconciliation["parent_semantic_contract"]["aggregation_semantics"] = "additive"
    reconciliation["result_validation"].update({"status": "failed", "notes": "Child groups do not reconcile to the parent."})
    reconciliation["status"] = "blocked"
    cases["result_reconciliation"] = reconciliation

    repeated = base_case("repeated_use")
    repeated["promotion_boundary"].update({"status": "reusable_candidate", "human_review_required": True})
    repeated["status"] = "reusable_candidate"
    cases["repeated_use"] = repeated

    compound = base_case("compound_failures")
    compound["semantic_continuity"].update({"status": "failed", "metric_version_preserved": False, "notes": "Semantic version conflict."})
    compound["filter_continuity"].update({"status": "failed", "material_filters_inherited": False, "scope_not_widened": False, "lost_filters": ["environment=prod"]})
    compound["grain_cardinality_validation"].update({"status": "failed", "join_risk": "many_to_many", "fanout_detected": True, "notes": "Many-to-many join creates fanout."})
    compound["compute_budget"].update({"status": "failed", "estimated_latency_ms": 30000, "estimated_scan_scope": "unbounded full history", "notes": "Compute budget violated."})
    compound["result_validation"].update({"status": "failed", "notes": "Result validation stopped after upstream failures."})
    compound["unknowns"] = [{"unknown_id": "schema-scope", "statement": "Relevant schema version is not bounded.", "blocking": True}]
    compound["status"] = "blocked"
    cases["compound_failures"] = compound

    return cases


def gate_results(case: dict[str, Any]) -> list[dict[str, str]]:
    mapping = {
        "semantic_continuity": case["semantic_continuity"]["status"],
        "filter_continuity": case["filter_continuity"]["status"],
        "security_scope": "failed" if case["security_scope"]["expansion_detected"] or case["security_scope"]["row_level_status"] == "denied" else "passed",
        "grain_cardinality": case["grain_cardinality_validation"]["status"],
        "compute_budget": "passed" if case["compute_budget"]["status"] == "interactive_ready" else case["compute_budget"]["status"],
        "result_validation": case["result_validation"]["status"],
    }
    return [{"gate": key, "result": value} for key, value in mapping.items()]


def run_replay() -> dict[str, Any]:
    expected = {
        "reuse_existing": "reuse_existing",
        "valid_projection": "projection_candidate",
        "semantic_drift": "blocked",
        "hidden_filter_loss": "blocked",
        "security_expansion": "blocked",
        "fanout": "blocked",
        "non_additive": "blocked",
        "ambiguous_click": "ambiguous",
        "compute_budget": "async_required",
        "stale_version": "blocked",
        "result_reconciliation": "blocked",
        "repeated_use": "reusable_candidate",
        "compound_failures": "blocked",
    }
    scenarios: dict[str, Any] = {}
    passes: list[str] = []
    failures: list[str] = []
    for name, case in mutate_cases().items():
        errors = validate_instance(case)
        observed = case["status"] if not errors else "contract_invalid"
        result = {
            "expected": expected[name],
            "observed": observed,
            "pass": not errors and observed == expected[name],
            "validation_errors": errors,
            "gate_results": gate_results(case),
            "production_approved": case["production_approved"],
        }
        scenarios[name] = result
        (passes if result["pass"] else failures).append(name)
    return {
        "replay_kind": "deterministic_guidance_conformance",
        "simulation_status": "synthetic_reference",
        "downstream_adoption_status": "not_observed",
        "agent_behavior_status": "not_evaluated",
        "all_passed": not failures,
        "passes": passes,
        "failures": failures,
        "scenarios": scenarios,
        "limitations": [
            "Synthetic contract replay does not prove Codex, Copilot, Claude, Gemini, or another external agent will follow the guidance.",
            "No real DataHub, semantic model, BI runtime, Databricks query, or downstream adoption was exercised.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print the complete replay as JSON")
    args = parser.parse_args()
    result = run_replay()
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        for name, value in result["scenarios"].items():
            print(f"{name}: {'PASS' if value['pass'] else 'FAIL'} expected={value['expected']} observed={value['observed']}")
        print(f"all_passed={result['all_passed']}")
        print(f"agent_behavior_status={result['agent_behavior_status']}")
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
