#!/usr/bin/env python3
"""Replay Pre-Silver/Silver guidance with public synthetic evidence.

This deterministic conformance replay exercises modeling decisions only. It
does not emulate DataHub, Databricks, Unity Catalog, or a production modeling
runtime, and it does not create or approve a Silver table.
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


@dataclass(frozen=True)
class ModelingQuestionContract:
    candidate_grain: str
    candidate_key: str
    join: str
    temporal_question: str
    dedup_question: str
    schema_scope_question: str


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
            f"candidate proposes grain={questions.candidate_grain} key={questions.candidate_key}",
        ]
        inferences = [
            "DataHub relationship, profile, and historical-query signals are orientation hypotheses only"
        ]
        counterevidence: list[str] = []
        unknowns: list[str] = []
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
            "candidate_only": True,
        }

        if not evidence.get("live_evidence_authorized", True):
            unknowns.extend(
                [
                    "candidate key stability is not established by authorized live evidence",
                    "join cardinality and temporal scope remain unverified",
                ]
            )
            candidate["status"] = "unknown"
            return _result(
                actions + ["stop_for_missing_evidence"],
                facts,
                inferences,
                counterevidence,
                unknowns,
                source_roles,
                candidate,
                "INSUFFICIENT_EVIDENCE",
            )

        duplicate_keys = evidence.get("duplicate_key_count", 0)
        if duplicate_keys:
            counterevidence.append(
                f"targeted live evidence found {duplicate_keys} duplicate candidate-key values"
            )
            candidate["candidate_key"] = None
            candidate["status"] = "partial"
            unknowns.append("a durable identifier or composite key remains unresolved")
            return _result(
                actions + ["reject_profiled_uniqueness"],
                facts,
                inferences,
                counterevidence,
                unknowns,
                source_roles,
                candidate,
                "PARTIAL_KEY_REJECTED",
            )

        fanout_ratio = evidence.get("join_fanout_ratio", 1.0)
        if fanout_ratio > 1.0:
            counterevidence.append(
                f"targeted join multiplied rows by {fanout_ratio:g} at the required grain"
            )
            candidate["status"] = "blocked"
            return _result(
                actions + ["reject_join_fanout"],
                facts,
                inferences,
                counterevidence,
                unknowns,
                source_roles,
                candidate,
                "BLOCKED_JOIN_FANOUT",
            )

        if not evidence.get("temporal_semantics"):
            available = ", ".join(evidence.get("available_time_fields", []))
            counterevidence.append(
                f"multiple timestamps are available without authority-backed semantics: {available}"
            )
            unknowns.append("event, ingest, update, and effective-time roles are unresolved")
            candidate["status"] = "blocked"
            return _result(
                actions + ["block_temporal_ambiguity"],
                facts,
                inferences,
                counterevidence,
                unknowns,
                source_roles,
                candidate,
                "BLOCKED_TEMPORAL_SEMANTICS",
            )

        authority_conflicts = evidence.get("authority_conflicts", [])
        if authority_conflicts:
            counterevidence.extend(authority_conflicts)
            unknowns.append("accountable domain authority has not resolved the semantic conflict")
            candidate["status"] = "blocked"
            return _result(
                actions + ["route_authority_conflict_to_human"],
                facts,
                inferences,
                counterevidence,
                unknowns,
                source_roles,
                candidate,
                "BLOCKED_AUTHORITY_CONFLICT",
            )

        duplicate_events = evidence.get("duplicate_event_count", 0)
        late_events = evidence.get("late_event_count", 0)
        if (duplicate_events or late_events) and not evidence.get("deduplication_semantics"):
            counterevidence.append(
                f"observed duplicate_events={duplicate_events} late_events={late_events} without a reconciliation rule"
            )
            unknowns.append("retry, replay, late-arrival, and deduplication behavior is unresolved")
            candidate["status"] = "partial"
            return _result(
                actions + ["require_dedup_and_late_arrival_decision"],
                facts,
                inferences,
                counterevidence,
                unknowns,
                source_roles,
                candidate,
                "PARTIAL_DEDUP_REQUIRED",
            )

        schema_versions = evidence.get("schema_versions", ["v1"])
        if len(schema_versions) > 1 and not evidence.get("schema_scope"):
            counterevidence.append(
                "current profile does not establish behavior across schema versions "
                + ", ".join(schema_versions)
            )
            unknowns.append("candidate version or time scope is not bounded")
            candidate["status"] = "partial"
            return _result(
                actions + ["require_schema_version_scope"],
                facts,
                inferences,
                counterevidence,
                unknowns,
                source_roles,
                candidate,
                "PARTIAL_VERSION_SCOPED",
            )

        actions.append("check_gold_consumer_fit")
        if evidence.get("gold_fit") is not True:
            counterevidence.append(
                "candidate cannot satisfy the Gold consumer's required grain or history"
            )
            candidate["gold_fit"] = "failed"
            candidate["status"] = "blocked"
            return _result(
                actions + ["reject_gold_mismatch"],
                facts,
                inferences,
                counterevidence,
                unknowns,
                source_roles,
                candidate,
                "REJECTED_GOLD_MISMATCH",
            )

        facts.extend(
            [
                "targeted live evidence did not disprove the candidate key within the bounded scope",
                "measured join cardinality preserved the required grain",
                "temporal, deduplication, and schema scope are explicit",
            ]
        )
        candidate["gold_fit"] = "candidate_fit"
        candidate["status"] = "candidate"
        unknowns.append("durability outside the tested version and time scope remains unproven")
        return _result(
            actions + ["request_accountable_human_review"],
            facts,
            inferences,
            counterevidence,
            unknowns,
            source_roles,
            candidate,
            "CANDIDATE_FOR_HUMAN_REVIEW",
        )


def _result(
    actions: list[str],
    facts: list[str],
    inferences: list[str],
    counterevidence: list[str],
    unknowns: list[str],
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
        "available_time_fields": [
            "event_time",
            "ingest_time",
            "update_time",
            "effective_from",
        ],
        "temporal_semantics": "event_time drives the event; ingest_time measures arrival",
        "authority_conflicts": [],
        "duplicate_event_count": 0,
        "late_event_count": 0,
        "deduplication_semantics": "deduplicate by event_id within schema version",
        "schema_versions": ["v2"],
        "schema_scope": "v2 events observed in the bounded synthetic window",
        "gold_fit": True,
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
    }
    passes = {
        name: result["STATUS"] == expected_statuses[name]
        and result["PRODUCTION_APPROVED"] is False
        for name, result in scenarios.items()
    }
    return {
        "simulation_status": "synthetic_reference",
        "downstream_adoption_status": "not_observed",
        "runtime_components": {
            "requirements": "synthetic Gold Consumer Contract",
            "context": "synthetic DataHub-shaped metadata and source-role signals",
            "live_source": "in-memory bounded evidence flags and measurements",
            "decision": "deterministic Silver-model guidance investigator",
        },
        "limitations": [
            "no real DataHub, Databricks, Unity Catalog, or database was started",
            "no table, ETL, pipeline, architecture decision, or production approval was created",
            "deterministic conformance does not prove behavior across external coding-agent models",
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
