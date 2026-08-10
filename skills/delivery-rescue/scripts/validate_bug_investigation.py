#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "bug-investigation.v1.schema.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def path_text(parts: list[Any]) -> str:
    if not parts:
        return "$"
    result = "$"
    for part in parts:
        if isinstance(part, int):
            result += f"[{part}]"
        else:
            result += f".{part}"
    return result


def structural_errors(packet: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(packet), key=lambda item: list(item.absolute_path))
    return [f"{path_text(list(error.absolute_path))}: {error.message}" for error in errors]


def duplicate_ids(items: list[dict[str, Any]], field: str, label: str) -> list[str]:
    values = [item.get(field) for item in items if isinstance(item, dict)]
    duplicates = sorted({value for value in values if isinstance(value, str) and values.count(value) > 1})
    return [f"{label} contains duplicate {field}: {value}" for value in duplicates]


def has_test_outcome(
    tests: list[dict[str, Any]],
    hypothesis_id: str,
    outcomes: set[str],
) -> bool:
    return any(
        test.get("target_hypothesis_id") == hypothesis_id and test.get("outcome") in outcomes
        for test in tests
        if isinstance(test, dict)
    )


def validate_semantics(packet: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    observations = [item for item in packet.get("observations", []) if isinstance(item, dict)]
    hypotheses = [item for item in packet.get("hypotheses", []) if isinstance(item, dict)]
    tests = [item for item in packet.get("verification_tests", []) if isinstance(item, dict)]

    errors.extend(duplicate_ids(observations, "observation_id", "observations"))
    errors.extend(duplicate_ids(hypotheses, "hypothesis_id", "hypotheses"))
    errors.extend(duplicate_ids(tests, "test_id", "verification_tests"))

    observation_ids = {item.get("observation_id") for item in observations}
    hypothesis_by_id = {
        str(item.get("hypothesis_id")): item
        for item in hypotheses
        if isinstance(item.get("hypothesis_id"), str)
    }

    evidence_summary = packet.get("evidence_summary", {})
    if isinstance(evidence_summary, dict):
        for fact_id in evidence_summary.get("facts", []):
            if fact_id not in observation_ids:
                errors.append(f"evidence_summary.facts references unknown observation: {fact_id}")

    for test in tests:
        target = test.get("target_hypothesis_id")
        if target not in hypothesis_by_id:
            errors.append(f"verification test {test.get('test_id')} references unknown hypothesis: {target}")
        if test.get("outcome") != "not_run" and not test.get("evidence_refs"):
            errors.append(f"verification test {test.get('test_id')} with an observed outcome requires evidence_refs")

    for hypothesis_id, hypothesis in hypothesis_by_id.items():
        status = hypothesis.get("status")
        evidence_for = hypothesis.get("evidence_for", [])
        evidence_against = hypothesis.get("evidence_against", [])
        if status == "supported":
            if not evidence_for:
                errors.append(f"supported hypothesis {hypothesis_id} requires evidence_for")
            if not has_test_outcome(tests, hypothesis_id, {"supports"}):
                errors.append(f"supported hypothesis {hypothesis_id} requires a supporting verification test")
        if status == "falsified":
            if not evidence_against and not has_test_outcome(tests, hypothesis_id, {"falsifies"}):
                errors.append(f"falsified hypothesis {hypothesis_id} requires contrary evidence or a falsifying test")

    reproduction = packet.get("reproduction", {})
    if isinstance(reproduction, dict):
        status = reproduction.get("status")
        attempts = reproduction.get("attempts")
        last_attempt = reproduction.get("last_attempt_at")
        if status == "not_attempted":
            if attempts != 0:
                errors.append("reproduction.status=not_attempted requires attempts=0")
            if last_attempt is not None:
                errors.append("reproduction.status=not_attempted requires last_attempt_at=null")
        else:
            if not isinstance(attempts, int) or attempts < 1:
                errors.append(f"reproduction.status={status} requires at least one attempt")
            if last_attempt is None:
                errors.append(f"reproduction.status={status} requires last_attempt_at")
        if status == "reproduced":
            if not reproduction.get("steps"):
                errors.append("reproduction.status=reproduced requires reproduction steps")
            if not reproduction.get("evidence_refs"):
                errors.append("reproduction.status=reproduced requires reproduction evidence_refs")

    root_cause = packet.get("root_cause", {})
    root_status = root_cause.get("status") if isinstance(root_cause, dict) else None
    root_hypothesis_id = root_cause.get("hypothesis_id") if isinstance(root_cause, dict) else None
    strongest_alternative = (
        root_cause.get("strongest_alternative_hypothesis_id") if isinstance(root_cause, dict) else None
    )
    alternative_disposition = (
        root_cause.get("alternative_disposition") if isinstance(root_cause, dict) else None
    )

    if root_status == "unknown":
        if root_hypothesis_id is not None:
            errors.append("root_cause.status=unknown requires hypothesis_id=null")
    elif root_status in {"hypothesis_supported", "verified"}:
        if root_hypothesis_id not in hypothesis_by_id:
            errors.append("root_cause must reference an existing hypothesis")
        else:
            root_hypothesis = hypothesis_by_id[root_hypothesis_id]
            if root_status == "hypothesis_supported" and root_hypothesis.get("status") not in {
                "strengthened",
                "supported",
            }:
                errors.append("hypothesis_supported root cause requires a strengthened or supported hypothesis")
            if root_status == "verified":
                if root_hypothesis.get("status") != "supported":
                    errors.append("verified root cause requires hypothesis.status=supported")
                if reproduction.get("status") != "reproduced":
                    errors.append("verified root cause requires a reproduced failure")
                if not has_test_outcome(tests, root_hypothesis_id, {"supports"}):
                    errors.append("verified root cause requires a supporting falsification or controlled verification test")
                if not root_cause.get("evidence_refs"):
                    errors.append("verified root cause requires evidence_refs")

    if strongest_alternative is not None:
        if strongest_alternative not in hypothesis_by_id:
            errors.append("strongest alternative must reference an existing hypothesis")
        if strongest_alternative == root_hypothesis_id:
            errors.append("strongest alternative must differ from the selected root-cause hypothesis")
    if alternative_disposition == "not_applicable" and strongest_alternative is not None:
        errors.append("alternative_disposition=not_applicable requires no strongest alternative")
    if alternative_disposition in {"falsified", "weakened", "accepted_residual_risk", "unresolved"}:
        if strongest_alternative is None:
            errors.append(f"alternative_disposition={alternative_disposition} requires a strongest alternative")
    if strongest_alternative in hypothesis_by_id:
        alternative = hypothesis_by_id[strongest_alternative]
        if alternative_disposition == "falsified":
            if alternative.get("status") != "falsified" and not has_test_outcome(
                tests, strongest_alternative, {"falsifies"}
            ):
                errors.append("falsified alternative disposition requires a falsified alternative hypothesis")
        if alternative_disposition == "weakened":
            if alternative.get("status") not in {"weakened", "falsified"} and not has_test_outcome(
                tests, strongest_alternative, {"weakens", "falsifies"}
            ):
                errors.append("weakened alternative disposition requires weakening evidence")

    material_live = [
        item
        for item in hypotheses
        if item.get("material") is True and item.get("status") not in {"falsified"}
    ]
    if root_status in {"hypothesis_supported", "verified"} and len(material_live) > 1:
        if strongest_alternative is None:
            errors.append("multiple material live hypotheses require a strongest alternative")

    next_step = packet.get("minimum_next_step", {})
    next_kind = next_step.get("kind") if isinstance(next_step, dict) else None
    if reproduction.get("status") in {"not_attempted", "not_reproduced", "intermittent"} and next_kind == "repair":
        errors.append("repair cannot be the minimum next step before the failure is reproduced")
    if root_status == "unknown" and next_kind == "repair":
        errors.append("repair cannot be the minimum next step while root cause remains unknown")

    fix_readiness = packet.get("fix_readiness", {})
    fix_status = fix_readiness.get("status") if isinstance(fix_readiness, dict) else None
    blocking_unknowns = []
    if isinstance(evidence_summary, dict):
        blocking_unknowns = [
            item
            for item in evidence_summary.get("unknowns", [])
            if isinstance(item, dict) and item.get("blocking") is True
        ]

    if fix_status == "ready_for_bounded_fix":
        if reproduction.get("status") != "reproduced":
            errors.append("ready_for_bounded_fix requires a reproduced failure")
        if root_status not in {"hypothesis_supported", "verified"}:
            errors.append("ready_for_bounded_fix requires a supported or verified root-cause hypothesis")
        if blocking_unknowns:
            errors.append("ready_for_bounded_fix is not allowed while blocking unknowns remain")
        if alternative_disposition in {"accepted_residual_risk", "unresolved"}:
            errors.append("ready_for_bounded_fix is not allowed with unresolved or accepted residual alternative risk")
        if not fix_readiness.get("proposed_fix_scope"):
            errors.append("ready_for_bounded_fix requires a bounded proposed_fix_scope")
        if not str(fix_readiness.get("acceptance_observer", "")).strip():
            errors.append("ready_for_bounded_fix requires an acceptance_observer")
        if not fix_readiness.get("validation_commands"):
            errors.append("ready_for_bounded_fix requires validation_commands")
        if not fix_readiness.get("evidence_refs"):
            errors.append("ready_for_bounded_fix requires evidence_refs")
        if next_kind != "repair":
            errors.append("ready_for_bounded_fix requires minimum_next_step.kind=repair")

    simulation_status = packet.get("simulation_status")
    adoption_status = packet.get("downstream_adoption_status")
    if simulation_status == "synthetic_reference" and adoption_status != "not_observed":
        errors.append("synthetic_reference packets must keep downstream_adoption_status=not_observed")
    if adoption_status != "not_observed" and simulation_status != "downstream_observed":
        errors.append("observed adoption requires simulation_status=downstream_observed")

    return errors


def validate_packet(packet: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors = structural_errors(packet, schema)
    if errors:
        return errors
    return validate_semantics(packet)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a lat.bug_investigation.v1 packet.")
    parser.add_argument("packet")
    parser.add_argument("--schema", default=str(SCHEMA_PATH))
    args = parser.parse_args()

    try:
        packet = load_json(Path(args.packet))
        schema = load_json(Path(args.schema))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if not isinstance(packet, dict):
        print("error: packet root must be an object", file=sys.stderr)
        return 1
    if not isinstance(schema, dict):
        print("error: schema root must be an object", file=sys.stderr)
        return 1

    errors = validate_packet(packet, schema)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"validated bug investigation packet: {args.packet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
