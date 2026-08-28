#!/usr/bin/env python3
"""Deterministic conformance replay for Pre-Silver/Silver guidance.

This fixture exercises the documented decision gates with public synthetic
inputs. It does not run an external coding agent and therefore does not prove
agent behavior, DataHub integration, Databricks integration, or production
modeling correctness.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GoldConsumerContract:
    consumer: str
    entity_or_event: str
    required_grain: str
    required_history: str
    required_identifier: str
    freshness_expectation: str
    security_governance_boundary: str


@dataclass(frozen=True)
class ModelingQuestionContract:
    candidate_grain: str
    candidate_key: str
    join: str
    temporal_question: str
    dedup_question: str
    schema_scope_question: str


BLOCKING_STATUS = {
    "join_fanout": "BLOCKED_JOIN_FANOUT",
    "temporal_semantics": "BLOCKED_TEMPORAL_SEMANTICS",
    "authority_conflict": "BLOCKED_AUTHORITY_CONFLICT",
    "gold_fit": "REJECTED_GOLD_MISMATCH",
    "freshness": "BLOCKED_FRESHNESS_MISMATCH",
    "governance": "BLOCKED_GOVERNANCE_MISMATCH",
}

PARTIAL_STATUS = {
    "candidate_key": "PARTIAL_KEY_REJECTED",
    "deduplication": "PARTIAL_DEDUP_REQUIRED",
    "schema_scope": "PARTIAL_VERSION_SCOPED",
}


class SilverModelingInvestigator:
    """Applies the guidance order to bounded synthetic modeling evidence."""

    def investigate(
        self,
        consumer: GoldConsumerContract,
        questions: ModelingQuestionContract,
        evidence: dict[str, Any],
    ) -> dict[str, Any]:
        actions = [
            "define_gold_consumer_contract",
            "define_modeling_question_contract",
            "select_minimum_datahub_context",
            "inspect_targeted_live_evidence",
            "classify_field_level_source_roles",
            "reconcile_cross_source_evidence",
            "challenge_silver_candidate",
        ]
        facts = [
            f"Gold consumer requires grain={consumer.required_grain}",
            f"Gold consumer requires freshness={consumer.freshness_expectation}",
            f"Gold consumer governance boundary={consumer.security_governance_boundary}",
            f"candidate proposes grain={questions.candidate_grain} key={questions.candidate_key}",
        ]
        inferences = [
            "DataHub relationship, profile, and historical-query signals are orientation hypotheses only"
        ]
        counterevidence: list[str] = []
        unknowns: list[str] = []
        gate_results: list[dict[str, str]] = []
        source_roles = evidence.get(
            "source_roles",
            {
                "identity": "unknown authority",
                "event_time": "unknown authority",
                "enrichment": "supporting source",
            },
        )

        candidate: dict[str, Any] = {
            "entity_or_event": consumer.entity_or_event,
            "grain": questions.candidate_grain,
            "candidate_key": questions.candidate_key,
            "join": questions.join,
            "temporal_semantics": evidence.get("temporal_semantics"),
            "deduplication_semantics": evidence.get("deduplication_semantics"),
            "schema_scope": evidence.get("schema_scope"),
            "source_roles": source_roles,
            "gold_fit": "not_checked",
            "freshness_fit": "not_checked",
            "governance_fit": "not_checked",
            "candidate_only": True,
        }

        if not evidence.get("live_evidence_authorized", True):
            unknowns.extend(
                [
                    "candidate key stability is not established by authorized live evidence",
                    "join cardinality and temporal scope remain unverified",
                ]
            )
            gate_results.append(
                {"gate": "live_evidence", "result": "unknown", "detail": "authorized live evidence unavailable"}
            )
            candidate["status"] = "unknown"
            return _result(
                actions + ["stop_for_missing_evidence"],
                facts,
                inferences,
                counterevidence,
                unknowns,
                gate_results,
                source_roles,
                candidate,
                "INSUFFICIENT_EVIDENCE",
            )

        blocking_failures: list[str] = []
        partial_failures: list[str] = []

        duplicate_keys = evidence.get("duplicate_key_count", 0)
        if duplicate_keys:
            partial_failures.append("candidate_key")
            counterevidence.append(
                f"targeted live evidence found {duplicate_keys} duplicate candidate-key values"
            )
            gate_results.append(
                {"gate": "candidate_key", "result": "failed", "detail": "live duplicates defeated profiled uniqueness"}
            )
            candidate["candidate_key"] = None
            unknowns.append("a durable identifier or composite key remains unresolved")
        else:
            gate_results.append({"gate": "candidate_key", "result": "passed", "detail": "no duplicate key found in bounded scope"})

        fanout_ratio = evidence.get("join_fanout_ratio", 1.0)
        if fanout_ratio > 1.0:
            blocking_failures.append("join_fanout")
            counterevidence.append(
                f"targeted join multiplied rows by {fanout_ratio:g} at the required grain"
            )
            gate_results.append(
                {"gate": "join_fanout", "result": "failed", "detail": f"row multiplication={fanout_ratio:g}"}
            )
        else:
            gate_results.append({"gate": "join_fanout", "result": "passed", "detail": "required grain preserved"})

        if not evidence.get("temporal_semantics"):
            blocking_failures.append("temporal_semantics")
            available = ", ".join(evidence.get("available_time_fields", []))
            counterevidence.append(
                f"multiple timestamps are available without authority-backed semantics: {available}"
            )
            unknowns.append("event, ingest, update, and effective-time roles are unresolved")
            gate_results.append(
                {"gate": "temporal_semantics", "result": "failed", "detail": "available timestamps remain semantically ambiguous"}
            )
        else:
            gate_results.append({"gate": "temporal_semantics", "result": "passed", "detail": "business and ingest time roles are explicit"})

        authority_conflicts = evidence.get("authority_conflicts", [])
        if authority_conflicts:
            blocking_failures.append("authority_conflict")
            counterevidence.extend(authority_conflicts)
            unknowns.append("accountable domain authority has not resolved the semantic conflict")
            gate_results.append(
                {"gate": "authority_conflict", "result": "failed", "detail": "conflicting evidence classes require accountable resolution"}
            )
        else:
            gate_results.append({"gate": "authority_conflict", "result": "passed", "detail": "no unresolved authority conflict in bounded scope"})

        duplicate_events = evidence.get("duplicate_event_count", 0)
        late_events = evidence.get("late_event_count", 0)
        if (duplicate_events or late_events) and not evidence.get("deduplication_semantics"):
            partial_failures.append("deduplication")
            counterevidence.append(
                f"observed duplicate_events={duplicate_events} late_events={late_events} without a reconciliation rule"
            )
            unknowns.append("retry, replay, late-arrival, and deduplication behavior is unresolved")
            gate_results.append(
                {"gate": "deduplication", "result": "failed", "detail": "observed retries/late arrivals lack a reconciliation rule"}
            )
        else:
            gate_results.append({"gate": "deduplication", "result": "passed", "detail": "deduplication/late-arrival semantics are explicit or not triggered"})

        schema_versions = evidence.get("schema_versions", ["v1"])
        if len(schema_versions) > 1 and not evidence.get("schema_scope"):
            partial_failures.append("schema_scope")
            counterevidence.append(
                "current profile does not establish behavior across schema versions "
                + ", ".join(schema_versions)
            )
            unknowns.append("candidate version or time scope is not bounded")
            gate_results.append(
                {"gate": "schema_scope", "result": "failed", "detail": "multiple schema versions lack an explicit supported scope"}
            )
        else:
            gate_results.append({"gate": "schema_scope", "result": "passed", "detail": "candidate version/time scope is bounded"})

        freshness_met = evidence.get("freshness_met", True)
        candidate["freshness_fit"] = "candidate_fit" if freshness_met else "failed"
        if not freshness_met:
            blocking_failures.append("freshness")
            counterevidence.append("observed data freshness cannot satisfy the Gold consumer freshness expectation")
            gate_results.append(
                {"gate": "freshness", "result": "failed", "detail": "consumer freshness SLA is not met"}
            )
        else:
            gate_results.append({"gate": "freshness", "result": "passed", "detail": "bounded evidence meets the consumer freshness expectation"})

        governance_ok = evidence.get("security_scope_compatible", True)
        candidate["governance_fit"] = "candidate_fit" if governance_ok else "failed"
        if not governance_ok:
            blocking_failures.append("governance")
            counterevidence.append("candidate cannot preserve the Gold consumer security/governance boundary")
            gate_results.append(
                {"gate": "governance", "result": "failed", "detail": "candidate broadens or cannot enforce the required scope"}
            )
        else:
            gate_results.append({"gate": "governance", "result": "passed", "detail": "candidate preserves the declared governance boundary"})

        actions.append("check_gold_consumer_fit")
        gold_fit = evidence.get("gold_fit") is True
        candidate["gold_fit"] = "candidate_fit" if gold_fit else "failed"
        if not gold_fit:
            blocking_failures.append("gold_fit")
            counterevidence.append(
                "candidate cannot satisfy the Gold consumer's required grain or history"
            )
            gate_results.append(
                {"gate": "gold_fit", "result": "failed", "detail": "consumer grain/history cannot be reproduced"}
            )
        else:
            gate_results.append({"gate": "gold_fit", "result": "passed", "detail": "candidate supports the bounded consumer need"})

        if blocking_failures:
            candidate["status"] = "blocked"
            if len(blocking_failures) == 1 and not partial_failures:
                status = BLOCKING_STATUS[blocking_failures[0]]
            else:
                status = "BLOCKED_MULTIPLE_MODELING_CONSTRAINTS"
            actions.append("preserve_all_failed_gates_for_next_iteration")
        elif partial_failures:
            candidate["status"] = "partial"
            if len(partial_failures) == 1:
                status = PARTIAL_STATUS[partial_failures[0]]
            else:
                status = "PARTIAL_MULTIPLE_MODELING_CONSTRAINTS"
            actions.append("preserve_all_partial_gates_for_next_iteration")
        else:
            facts.extend(
                [
                    "targeted live evidence did not disprove the candidate key within the bounded scope",
                    "measured join cardinality preserved the required grain",
                    "temporal, deduplication, schema, freshness, and governance scope are explicit",
                ]
            )
            candidate["status"] = "candidate"
            unknowns.append("durability outside the tested version and time scope remains unproven")
            status = "CANDIDATE_FOR_HUMAN_REVIEW"
            actions.append("request_accountable_human_review")

        return _result(
            actions,
            facts,
            inferences,
            counterevidence,
            unknowns,
            gate_results,
            source_roles,
            candidate,
            status,
        )


def _result(
    actions: list[str],
    facts: list[str],
    inferences: list[str],
    counterevidence: list[str],
    unknowns: list[str],
    gate_results: list[dict[str, str]],
    source_roles: dict[str, str],
    candidate: dict[str, Any],
    status: str,
) -> dict[str, Any]:
    return {
        "actions": actions,
        "FACT": facts,
        "INFERENCE": inferences,
        "COUNTEREVIDENCE": counterevidence,
        "UNKNOWN": unknowns,
        "GATE_RESULTS": gate_results,
        "SOURCE_ROLES": source_roles,
        "SILVER_MODEL_CANDIDATE": candidate,
        "STATUS": status,
        "PRODUCTION_APPROVED": False,
    }


def run_replay() -> dict[str, Any]:
    investigator = SilverModelingInvestigator()
    consumer = GoldConsumerContract(
        consumer="synthetic monthly account reliability metric",
        entity_or_event="synthetic service event",
        required_grain="one row per synthetic service event",
        required_history="monthly event history",
        required_identifier="stable event identity",
        freshness_expectation="complete within 30 minutes",
        security_governance_boundary="synthetic tenant scope only",
    )
    questions = ModelingQuestionContract(
        candidate_grain="one row per synthetic service event",
        candidate_key="event_id",
        join="event.account_ref = account.account_ref",
        temporal_question="which timestamp represents business event time?",
        dedup_question="how are retry and replay duplicates reconciled?",
        schema_scope_question="which schema versions and time ranges are supported?",
    )
    base_evidence: dict[str, Any] = {
        "live_evidence_authorized": True,
        "duplicate_key_count": 0,
        "join_fanout_ratio": 1.0,
        "available_time_fields": ["event_time", "ingest_time", "update_time", "effective_from"],
        "temporal_semantics": "event_time drives the event; ingest_time measures arrival",
        "authority_conflicts": [],
        "duplicate_event_count": 0,
        "late_event_count": 0,
        "deduplication_semantics": "deduplicate by event_id within schema version",
        "schema_versions": ["v2"],
        "schema_scope": "v2 events observed in the bounded synthetic window",
        "gold_fit": True,
        "freshness_met": True,
        "security_scope_compatible": True,
        "source_roles": {
            "identity": "authoritative source: synthetic event source",
            "event_time": "authoritative source: synthetic event source",
            "account_attributes": "reference or enrichment source: synthetic account source",
        },
    }

    def scenario(**overrides: Any) -> dict[str, Any]:
        evidence = {**base_evidence, **overrides}
        return investigator.investigate(consumer, questions, evidence)

    scenarios = {
        "clean_candidate": scenario(),
        "false_uniqueness": scenario(duplicate_key_count=2),
        "join_fanout": scenario(join_fanout_ratio=2.0),
        "temporal_mismatch": scenario(temporal_semantics=None),
        "conflicting_authority": scenario(
            authority_conflicts=[
                "requirement defines status as business outcome while code and DataHub description use processing state"
            ]
        ),
        "late_duplicate_events": scenario(
            duplicate_event_count=3,
            late_event_count=1,
            deduplication_semantics=None,
        ),
        "schema_evolution": scenario(schema_versions=["v1", "v2"], schema_scope=None),
        "gold_consumer_mismatch": scenario(gold_fit=False),
        "insufficient_evidence": scenario(live_evidence_authorized=False),
        "freshness_mismatch": scenario(freshness_met=False),
        "governance_mismatch": scenario(security_scope_compatible=False),
        "compound_failures": scenario(
            duplicate_key_count=2,
            join_fanout_ratio=2.0,
            temporal_semantics=None,
            schema_versions=["v1", "v2"],
            schema_scope=None,
        ),
    }
    expected_statuses = {
        "clean_candidate": "CANDIDATE_FOR_HUMAN_REVIEW",
        "false_uniqueness": "PARTIAL_KEY_REJECTED",
        "join_fanout": "BLOCKED_JOIN_FANOUT",
        "temporal_mismatch": "BLOCKED_TEMPORAL_SEMANTICS",
        "conflicting_authority": "BLOCKED_AUTHORITY_CONFLICT",
        "late_duplicate_events": "PARTIAL_DEDUP_REQUIRED",
        "schema_evolution": "PARTIAL_VERSION_SCOPED",
        "gold_consumer_mismatch": "REJECTED_GOLD_MISMATCH",
        "insufficient_evidence": "INSUFFICIENT_EVIDENCE",
        "freshness_mismatch": "BLOCKED_FRESHNESS_MISMATCH",
        "governance_mismatch": "BLOCKED_GOVERNANCE_MISMATCH",
        "compound_failures": "BLOCKED_MULTIPLE_MODELING_CONSTRAINTS",
    }
    passes = {
        name: result["STATUS"] == expected_statuses[name]
        and result["PRODUCTION_APPROVED"] is False
        for name, result in scenarios.items()
    }
    return {
        "simulation_status": "synthetic_reference",
        "downstream_adoption_status": "not_observed",
        "replay_kind": "deterministic_guidance_conformance",
        "agent_behavior_status": "not_evaluated",
        "runtime_components": {
            "requirements": "synthetic Gold Consumer Contract",
            "context": "synthetic DataHub-shaped metadata and source-role signals",
            "live_source": "in-memory bounded evidence flags and measurements",
            "decision": "deterministic Silver-model guidance investigator",
        },
        "limitations": [
            "no real DataHub, Databricks, Unity Catalog, or database was started",
            "no external Codex, Copilot, Claude Code, Gemini CLI, or other isolated agent was executed",
            "this replay proves deterministic rule conformance, not agent behavioral compliance",
            "no table, ETL, pipeline, architecture decision, or production approval was created",
        ],
        "scenarios": scenarios,
        "passes": passes,
        "all_passed": all(passes.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    result = run_replay()
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
