#!/usr/bin/env python3
"""Replay code-to-live-evidence guidance with a public synthetic service.

This is a deterministic guidance-conformance replay. It does not emulate or
claim a real DataHub or Elasticsearch deployment and it does not prove model
behavior in every coding-agent runtime.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ExpectedEffect:
    event_action: str
    correlation_value: str
    code_field: str = "requestId"
    indexed_field: str = "request.id"
    environment: str = "test"
    destination: str = "logs-upload-test"


@dataclass
class EvidenceTrace:
    code_path_executed: bool = False
    trigger_satisfied: bool = False
    emitter_called: bool = False
    suppressed_by_config: bool = False
    transport_accepted: bool = False
    ingest_accepted: bool = False
    transformation_applied: bool = False
    observations: list[dict[str, Any]] = field(default_factory=list)


class SyntheticLiveStore:
    def __init__(self) -> None:
        self._documents: list[dict[str, Any]] = []

    def index(self, destination: str, document: dict[str, Any]) -> None:
        self._documents.append({"_destination": destination, **document})

    def query(self, destination: str, filters: dict[str, str]) -> list[dict[str, Any]]:
        return [
            document
            for document in self._documents
            if document.get("_destination") == destination
            and all(_read_dotted(document, field_name) == value for field_name, value in filters.items())
        ]


def _read_dotted(document: dict[str, Any], field_name: str) -> Any:
    current: Any = document
    for part in field_name.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


class SyntheticPipeline:
    def __init__(self, store: SyntheticLiveStore) -> None:
        self.store = store

    def publish(
        self,
        event: dict[str, Any],
        trace: EvidenceTrace,
        *,
        drop_at_ingest: bool,
        destination: str,
    ) -> None:
        trace.transport_accepted = True
        if drop_at_ingest:
            trace.observations.append({"stage": "ingest", "status": "dropped"})
            return

        trace.ingest_accepted = True
        transformed = {
            "event": {"action": event["event"]},
            "request": {"id": event["requestId"]},
            "object": {"id": event["objectId"]},
            "elapsedMs": event["elapsedMs"],
            "environment": event["environment"],
            "service": event["service"],
            "message": event["message"],
        }
        trace.transformation_applied = True
        trace.observations.append(
            {
                "stage": "transformation",
                "status": "observed",
                "mapping": "requestId -> request.id",
            }
        )
        self.store.index(destination, transformed)


class SyntheticUploadService:
    def __init__(self, pipeline: SyntheticPipeline) -> None:
        self.pipeline = pipeline

    def handle(
        self,
        *,
        request_id: str,
        object_id: str,
        complete_upload: bool,
        info_enabled: bool,
        environment: str,
        destination: str,
        drop_at_ingest: bool = False,
    ) -> EvidenceTrace:
        trace = EvidenceTrace(code_path_executed=True)
        trace.trigger_satisfied = complete_upload
        if not complete_upload:
            trace.observations.append({"stage": "trigger", "status": "not_satisfied"})
            return trace

        if not info_enabled:
            trace.suppressed_by_config = True
            trace.observations.append({"stage": "logger_config", "status": "suppressed"})
            return trace

        trace.emitter_called = True
        event = {
            "event": "upload_complete",
            "requestId": request_id,
            "objectId": object_id,
            "elapsedMs": 17,
            "environment": environment,
            "service": "synthetic-upload-service",
            "message": "Upload completed",
        }
        trace.observations.append({"stage": "emitter", "status": "observed", "event": event})
        self.pipeline.publish(
            event,
            trace,
            drop_at_ingest=drop_at_ingest,
            destination=destination,
        )
        return trace


class OperationalEvidenceInvestigator:
    """Applies the guidance order to bounded synthetic evidence."""

    def __init__(self, store: SyntheticLiveStore, context: dict[str, Any]) -> None:
        self.store = store
        self.context = context

    def investigate(
        self,
        effect: ExpectedEffect,
        trace: EvidenceTrace,
        *,
        initial_field: str | None = None,
        initial_destination: str | None = None,
    ) -> dict[str, Any]:
        actions = ["inspect_code", "build_expected_effect_contract"]
        facts: list[str] = []
        counterevidence: list[str] = []
        unknowns: list[str] = []

        if not trace.code_path_executed:
            unknowns.append("code-path execution was not observed")
            return _result(actions, facts, counterevidence, unknowns, "UNKNOWN")
        facts.append("bounded request entered the code path")

        if not trace.trigger_satisfied:
            facts.append("expected-effect trigger was not satisfied")
            return _result(actions, facts, counterevidence, unknowns, "TRIGGER_NOT_EXECUTED")

        if trace.suppressed_by_config:
            facts.append("runtime logger configuration suppressed the INFO effect")
            return _result(actions, facts, counterevidence, unknowns, "SUPPRESSED_BY_CONFIG")

        if not trace.emitter_called:
            unknowns.append("trigger was satisfied but emitter execution is not established")
            return _result(actions, facts, counterevidence, unknowns, "UNKNOWN_AT_EMITTER")

        facts.append("application emitter call was observed")
        if not trace.transport_accepted:
            unknowns.append("transport acceptance is not established")
            return _result(actions, facts, counterevidence, unknowns, "UNKNOWN_AT_TRANSPORT")
        facts.append("transport accepted the event")

        if not trace.ingest_accepted:
            facts.append("ingest recorded a drop before live storage")
            counterevidence.append("application emission did not produce stored live evidence")
            return _result(actions, facts, counterevidence, unknowns, "INGEST_DROP")

        actions.extend(["select_minimum_context", "query_live_source"])
        field_name = initial_field or effect.indexed_field
        destination = initial_destination or effect.destination
        query_filters = {
            field_name: effect.correlation_value,
            "event.action": effect.event_action,
            "environment": effect.environment,
        }
        matches = self.store.query(destination, query_filters)

        if not matches:
            counterevidence.append(
                f"initial query found no match in {destination} using {field_name}"
            )
            mapping = self.context["field_mapping"].get(effect.code_field)
            mapped_destination = self.context["deployment_destination"].get(effect.environment)
            if mapping and mapping != field_name:
                actions.append("correct_cross_boundary_field_mapping")
                field_name = mapping
            if mapped_destination and mapped_destination != destination:
                actions.append("correct_environment_destination_mapping")
                destination = mapped_destination
            if actions[-1].startswith("correct_") or (
                len(actions) > 1 and actions[-2].startswith("correct_")
            ):
                actions.append("retry_narrow_live_query")
                query_filters = {
                    field_name: effect.correlation_value,
                    "event.action": effect.event_action,
                    "environment": effect.environment,
                }
                matches = self.store.query(destination, query_filters)

        if matches:
            facts.append(
                f"live source matched event={effect.event_action} correlation={effect.correlation_value} environment={effect.environment} in {destination} using {field_name}"
            )
            return _result(actions, facts, counterevidence, unknowns, "VERIFIED")

        unknowns.append("event remains unlocated after bounded mapping correction")
        return _result(actions, facts, counterevidence, unknowns, "UNKNOWN_AFTER_QUERY")


def _result(
    actions: list[str],
    facts: list[str],
    counterevidence: list[str],
    unknowns: list[str],
    verdict: str,
) -> dict[str, Any]:
    return {
        "actions": actions,
        "FACT": facts,
        "INFERENCE": [],
        "COUNTEREVIDENCE": counterevidence,
        "UNKNOWN": unknowns,
        "VERDICT": verdict,
    }


def run_replay() -> dict[str, Any]:
    context = {
        "simulation_status": "synthetic_reference",
        "downstream_adoption_status": "not_observed",
        "field_mapping": {"requestId": "request.id"},
        "deployment_destination": {"test": "logs-upload-test"},
    }
    store = SyntheticLiveStore()
    service = SyntheticUploadService(SyntheticPipeline(store))
    investigator = OperationalEvidenceInvestigator(store, context)
    effect = ExpectedEffect(event_action="upload_complete", correlation_value="req-42")

    scenarios: dict[str, dict[str, Any]] = {}

    healthy = service.handle(
        request_id="req-42",
        object_id="obj-7",
        complete_upload=True,
        info_enabled=True,
        environment="test",
        destination="logs-upload-test",
    )
    scenarios["healthy"] = investigator.investigate(effect, healthy)

    trigger_not_executed = service.handle(
        request_id="req-trigger",
        object_id="obj-7",
        complete_upload=False,
        info_enabled=True,
        environment="test",
        destination="logs-upload-test",
    )
    scenarios["trigger_not_executed"] = investigator.investigate(
        ExpectedEffect(event_action="upload_complete", correlation_value="req-trigger"),
        trigger_not_executed,
    )

    suppressed = service.handle(
        request_id="req-suppressed",
        object_id="obj-7",
        complete_upload=True,
        info_enabled=False,
        environment="test",
        destination="logs-upload-test",
    )
    scenarios["logging_suppressed"] = investigator.investigate(
        ExpectedEffect(event_action="upload_complete", correlation_value="req-suppressed"),
        suppressed,
    )

    transformed = service.handle(
        request_id="req-transform",
        object_id="obj-7",
        complete_upload=True,
        info_enabled=True,
        environment="test",
        destination="logs-upload-test",
    )
    scenarios["transformation_mismatch"] = investigator.investigate(
        ExpectedEffect(event_action="upload_complete", correlation_value="req-transform"),
        transformed,
        initial_field="requestId",
    )

    wrong_environment = service.handle(
        request_id="req-env",
        object_id="obj-7",
        complete_upload=True,
        info_enabled=True,
        environment="test",
        destination="logs-upload-test",
    )
    scenarios["wrong_environment_destination"] = investigator.investigate(
        ExpectedEffect(event_action="upload_complete", correlation_value="req-env"),
        wrong_environment,
        initial_destination="logs-upload-prod",
    )

    dropped = service.handle(
        request_id="req-drop",
        object_id="obj-7",
        complete_upload=True,
        info_enabled=True,
        environment="test",
        destination="logs-upload-test",
        drop_at_ingest=True,
    )
    scenarios["ingest_drop"] = investigator.investigate(
        ExpectedEffect(event_action="upload_complete", correlation_value="req-drop"),
        dropped,
    )

    unlocated = service.handle(
        request_id="req-unlocated",
        object_id="obj-7",
        complete_upload=True,
        info_enabled=True,
        environment="test",
        destination="logs-upload-shadow",
    )
    scenarios["unlocated_after_bounded_query"] = investigator.investigate(
        ExpectedEffect(event_action="upload_complete", correlation_value="req-unlocated"),
        unlocated,
    )

    expected_verdicts = {
        "healthy": "VERIFIED",
        "trigger_not_executed": "TRIGGER_NOT_EXECUTED",
        "logging_suppressed": "SUPPRESSED_BY_CONFIG",
        "transformation_mismatch": "VERIFIED",
        "wrong_environment_destination": "VERIFIED",
        "ingest_drop": "INGEST_DROP",
        "unlocated_after_bounded_query": "UNKNOWN_AFTER_QUERY",
    }
    passes = {
        name: result["VERDICT"] == expected_verdicts[name]
        for name, result in scenarios.items()
    }
    return {
        "simulation_status": "synthetic_reference",
        "downstream_adoption_status": "not_observed",
        "runtime_components": {
            "code": "executed Python SyntheticUploadService",
            "context": "synthetic DataHub-shaped mapping fixture",
            "live_source": "in-memory Elasticsearch-like exact-match store",
        },
        "limitations": [
            "no real DataHub deployment was started",
            "no real Elasticsearch deployment was available",
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
