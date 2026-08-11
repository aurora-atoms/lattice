#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate and deterministically consume a workspace-neutral handoff fixture."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_portable_case_pack import validate_pack  # noqa: E402

DCP_SCHEMA = ROOT / "skills/domain-context-pack/schemas/domain-context-pack.v1.schema.json"
DCP_VALIDATOR = ROOT / "skills/domain-context-pack/scripts/validate_domain_context_pack.py"
PCP_SCHEMA = ROOT / "schemas/capability/portable-case-pack.v1.schema.json"
RECEIPT_SCHEMA = ROOT / "schemas/capability/workspace-handoff-verification-request.v1.schema.json"

FIXTURE_TYPE = "cross_workspace_handoff_conformance_case"
FIXTURE_KEYS = {
    "fixture_type",
    "fixture_id",
    "scenario",
    "simulation_status",
    "downstream_adoption_status",
    "handoff_policy",
    "domain_context_pack",
    "portable_case_pack",
    "required_coding_verification",
    "stop_conditions",
}
POLICY_KEYS = {
    "source_surface",
    "authority_ceiling",
    "coverage_claim",
    "human_handoff_required",
    "automatic_orchestration_allowed",
    "capability_discovery_owner",
    "shared_discovery_mechanism_required",
}
VERIFICATION_KINDS = {
    "repository",
    "runtime",
    "reproduction",
    "test",
    "configuration",
    "dependency",
    "repository_and_test",
    "reproduction_and_runtime",
}
FORBIDDEN_DISCOVERY_KEYS = {
    "required_skill",
    "required_skill_name",
    "required_skill_path",
    "receiver_skill",
    "discovery_projection",
}
PRIVATE_PATTERNS = (
    re.compile(r"https?://(?:drive|docs|chat|mail|gmail)\.google\.com/", re.IGNORECASE),
    re.compile(r"(?:^|[\s\"'])/(?:Users|home)/"),
    re.compile(r"[A-Za-z]:\\(?:Users|workspace|repo)\\", re.IGNORECASE),
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def _load_dcp_validator() -> Any:
    spec = importlib.util.spec_from_file_location("lat_domain_context_pack_validator", DCP_VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load Domain Context Pack validator: {DCP_VALIDATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _schema_errors(instance: Any, schema: dict[str, Any], label: str) -> list[str]:
    errors: list[str] = []
    for error in sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(instance),
        key=lambda item: list(item.path),
    ):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"{label} schema:{location}: {error.message}")
    return errors


def _all_strings(value: Any) -> list[str]:
    values: list[str] = []
    if isinstance(value, str):
        values.append(value)
    elif isinstance(value, dict):
        for nested in value.values():
            values.extend(_all_strings(nested))
    elif isinstance(value, list):
        for nested in value:
            values.extend(_all_strings(nested))
    return values


def _all_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.add(str(key).lower())
            keys.update(_all_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            keys.update(_all_keys(nested))
    return keys


def _contains_private_locator(value: Any) -> bool:
    return any(pattern.search(text) for text in _all_strings(value) for pattern in PRIVATE_PATTERNS)


def _claim_records(pack: dict[str, Any]) -> list[dict[str, Any]]:
    claims = pack.get("claims", {})
    result: list[dict[str, Any]] = []
    if not isinstance(claims, dict):
        return result
    for status in ("observed", "derived", "judged", "unknown"):
        for claim in claims.get(status, []) if isinstance(claims.get(status), list) else []:
            if isinstance(claim, dict):
                result.append({"status": status, **claim})
    return result


def _sorted_unique(values: list[Any]) -> list[str]:
    return sorted({str(value) for value in values})


def validate_case(case: dict[str, Any], root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    if set(case) != FIXTURE_KEYS:
        missing = sorted(FIXTURE_KEYS - set(case))
        unexpected = sorted(set(case) - FIXTURE_KEYS)
        if missing:
            errors.append("fixture missing field(s): " + ", ".join(missing))
        if unexpected:
            errors.append("fixture has unexpected field(s): " + ", ".join(unexpected))
    if case.get("fixture_type") != FIXTURE_TYPE:
        errors.append(f"fixture_type must be {FIXTURE_TYPE}")
    if case.get("scenario") not in {"feature_requirement", "bug_investigation"}:
        errors.append("scenario must be feature_requirement or bug_investigation")
    if case.get("simulation_status") != "synthetic_reference":
        errors.append("public conformance fixture must remain simulation_status=synthetic_reference")
    if case.get("downstream_adoption_status") != "not_observed":
        errors.append("synthetic conformance cannot claim real downstream adoption")
    if _contains_private_locator(case):
        errors.append("public-safe handoff fixture contains a private locator, path, or email")
    forbidden_discovery = _all_keys(case) & FORBIDDEN_DISCOVERY_KEYS
    if forbidden_discovery:
        errors.append(
            "canonical handoff cannot require a workspace-specific Skill or discovery projection: "
            + ", ".join(sorted(forbidden_discovery))
        )

    policy = case.get("handoff_policy")
    if not isinstance(policy, dict):
        errors.append("handoff_policy must be an object")
        policy = {}
    elif set(policy) != POLICY_KEYS:
        errors.append("handoff_policy must contain exactly the workspace-neutral policy fields")
    expected_policy = {
        "source_surface": "google_workspace_candidate",
        "authority_ceiling": "candidate",
        "coverage_claim": "bounded_not_complete",
        "human_handoff_required": True,
        "automatic_orchestration_allowed": False,
        "capability_discovery_owner": "receiving_workspace",
        "shared_discovery_mechanism_required": False,
    }
    if policy != expected_policy:
        errors.append("handoff_policy must preserve candidate authority, human handoff, and workspace-native discovery")

    dcp = case.get("domain_context_pack")
    pcp = case.get("portable_case_pack")
    if not isinstance(dcp, dict):
        errors.append("domain_context_pack must be an object")
        dcp = {}
    if not isinstance(pcp, dict):
        errors.append("portable_case_pack must be an object")
        pcp = {}

    if dcp:
        errors.extend(_schema_errors(dcp, load_json(root / DCP_SCHEMA.relative_to(ROOT)), "domain_context_pack"))
        if not any(error.startswith("domain_context_pack schema:") for error in errors):
            dcp_validator = _load_dcp_validator()
            errors.extend(f"domain_context_pack semantic:{error}" for error in dcp_validator.semantic_errors(dcp))
    if pcp:
        errors.extend(_schema_errors(pcp, load_json(root / PCP_SCHEMA.relative_to(ROOT)), "portable_case_pack"))
        if not any(error.startswith("portable_case_pack schema:") for error in errors):
            errors.extend(f"portable_case_pack semantic:{error}" for error in validate_pack(pcp))

    if dcp and pcp:
        if dcp.get("scope_id") != pcp.get("case_id"):
            errors.append("Domain Context Pack scope_id and Portable Case Pack case_id must match")
        if dcp.get("task", {}).get("objective") != pcp.get("decision_requested"):
            errors.append("handoff target must match across Domain Context Pack and Portable Case Pack")
        if dcp.get("authorization", {}).get("data_classification") != pcp.get("data_classification"):
            errors.append("privacy classification must match across the two canonical packs")
        if dcp.get("simulation_status") != case.get("simulation_status"):
            errors.append("Domain Context Pack simulation status must match the fixture")
        if dcp.get("downstream_adoption_status") != case.get("downstream_adoption_status"):
            errors.append("Domain Context Pack adoption status must match the fixture")

        dcp_unknowns = {
            str(item.get("unknown_id"))
            for item in dcp.get("unknowns", [])
            if isinstance(item, dict) and item.get("unknown_id")
        }
        pcp_unknowns = {
            str(item.get("claim_id"))
            for item in pcp.get("claims", {}).get("unknown", [])
            if isinstance(item, dict) and item.get("claim_id")
        }
        if dcp_unknowns != pcp_unknowns:
            errors.append("UNKNOWN ids must be preserved between Domain Context Pack and Portable Case Pack")

        dcp_conflicts = {
            str(item.get("conflict_id")): item
            for item in dcp.get("conflicts", [])
            if isinstance(item, dict) and item.get("conflict_id")
        }
        pcp_conflict_ids = {
            str(item.get("conflict_id"))
            for item in pcp.get("conflicts", [])
            if isinstance(item, dict) and item.get("conflict_id")
        }
        if set(dcp_conflicts) != pcp_conflict_ids:
            errors.append("CONFLICT ids must be preserved between Domain Context Pack and Portable Case Pack")
        if any(item.get("status") != "unresolved" for item in dcp_conflicts.values()):
            errors.append("cross-workspace conformance fixture conflicts must remain unresolved")

        evidence_uri_to_id = {
            str(item.get("uri")): str(item.get("id"))
            for item in pcp.get("evidence_refs", [])
            if isinstance(item, dict) and item.get("uri") and item.get("id")
        }
        for item in dcp.get("context_items", []):
            if not isinstance(item, dict):
                continue
            for ref in item.get("evidence_refs", []):
                if ref not in evidence_uri_to_id:
                    errors.append(f"Domain Context Pack evidence_ref is not traceable in Portable Case Pack: {ref}")

    verifications = case.get("required_coding_verification")
    if not isinstance(verifications, list) or not verifications:
        errors.append("required_coding_verification must be a non-empty list")
        verifications = []
    claim_records = _claim_records(pcp)
    claim_ids = {str(item.get("claim_id")) for item in claim_records if item.get("claim_id")}
    derived_or_judged = {
        str(item.get("claim_id"))
        for item in claim_records
        if item.get("status") in {"derived", "judged"} and item.get("claim_id")
    }
    verification_ids: list[str] = []
    verified_claims: set[str] = set()
    for index, request in enumerate(verifications):
        if not isinstance(request, dict):
            errors.append(f"required_coding_verification[{index}] must be an object")
            continue
        required_keys = {"verification_id", "claim_refs", "verification_kind", "request", "required_evidence"}
        if set(request) != required_keys:
            errors.append(f"required_coding_verification[{index}] must contain exactly the verification request fields")
        verification_ids.append(str(request.get("verification_id", "")))
        refs = request.get("claim_refs", []) if isinstance(request.get("claim_refs"), list) else []
        verified_claims.update(str(ref) for ref in refs)
        for ref in refs:
            if str(ref) not in claim_ids:
                errors.append(f"required_coding_verification[{index}] references unknown claim: {ref}")
        if request.get("verification_kind") not in VERIFICATION_KINDS:
            errors.append(f"required_coding_verification[{index}] has unsupported verification_kind")
        if not isinstance(request.get("request"), str) or not request["request"].strip():
            errors.append(f"required_coding_verification[{index}].request must be non-empty")
        required_evidence = request.get("required_evidence")
        if not isinstance(required_evidence, list) or not required_evidence:
            errors.append(f"required_coding_verification[{index}].required_evidence must be non-empty")
    if len(verification_ids) != len(set(verification_ids)):
        errors.append("verification_id values must be unique")
    missing_verification = derived_or_judged - verified_claims
    if missing_verification:
        errors.append(
            "Google-derived or judged claims require independent coding verification: "
            + ", ".join(sorted(missing_verification))
        )

    stop_conditions = case.get("stop_conditions")
    if not isinstance(stop_conditions, list) or not stop_conditions:
        errors.append("stop_conditions must be a non-empty list")
    return errors


def build_receipt(case: dict[str, Any]) -> dict[str, Any]:
    dcp = case["domain_context_pack"]
    pcp = case["portable_case_pack"]
    sources = [item for item in dcp["sources"] if isinstance(item, dict)]
    claims = _claim_records(pcp)
    conflicts = [item for item in pcp["conflicts"] if isinstance(item, dict)]
    evidence_ids = _sorted_unique([item["id"] for item in pcp["evidence_refs"]])
    verifications = sorted(
        (copy.deepcopy(item) for item in case["required_coding_verification"]),
        key=lambda item: item["verification_id"],
    )
    required_claims = _sorted_unique(
        [claim_ref for item in verifications for claim_ref in item["claim_refs"]]
    )
    return {
        "$schema": "schemas/capability/workspace-handoff-verification-request.v1.schema.json",
        "contract": "lat.workspace_handoff_verification_request.v1",
        "receipt_id": f"{pcp['case_id']}/workspace-verification-request",
        "case_ref": pcp["case_id"],
        "target": pcp["decision_requested"],
        "source_scope": {
            "selected_source_ids": _sorted_unique(
                [item["source_id"] for item in sources if item.get("selection_status") == "selected"]
            ),
            "conditional_source_ids": _sorted_unique(
                [item["source_id"] for item in sources if item.get("selection_status") == "conditional"]
            ),
            "excluded_source_ids": _sorted_unique(
                [item["source_id"] for item in sources if item.get("selection_status") == "excluded"]
            ),
            "unavailable_or_unknown_source_ids": _sorted_unique(
                [item["source_id"] for item in sources if item.get("access_status") in {"denied", "unknown"}]
            ),
            "coverage_claim": case["handoff_policy"]["coverage_claim"],
            "evidence_ref_ids": evidence_ids,
        },
        "incoming_claims": sorted(
            [
                {
                    "claim_id": item["claim_id"],
                    "incoming_status": item["status"],
                    "evidence_ref_ids": _sorted_unique(item.get("evidence_refs", [])),
                    "confirmation_state": "unknown" if item["status"] == "unknown" else "candidate_only",
                }
                for item in claims
            ],
            key=lambda item: item["claim_id"],
        ),
        "claims_requiring_repo_verification": required_claims,
        "unknown_ids": _sorted_unique(
            [item["claim_id"] for item in claims if item["status"] == "unknown"]
        ),
        "conflicts": sorted(
            [
                {
                    "conflict_id": item["conflict_id"],
                    "status": "unresolved",
                    "claim_refs": _sorted_unique(item["claim_refs"]),
                    "evidence_ref_ids": _sorted_unique(item["evidence_refs"]),
                }
                for item in conflicts
            ],
            key=lambda item: item["conflict_id"],
        ),
        "strongest_counterevidence": sorted(
            [
                {
                    "statement": item["statement"],
                    "evidence_ref_ids": _sorted_unique(item["evidence_refs"]),
                    "impact": item["impact"],
                }
                for item in pcp["strongest_counterevidence"]
            ],
            key=lambda item: item["statement"],
        ),
        "evidence_ref_ids": evidence_ids,
        "authority_ceiling": case["handoff_policy"]["authority_ceiling"],
        "privacy_classification": pcp["data_classification"],
        "required_coding_verification": verifications,
        "evidence_confirmation_basis": "independent_repo_runtime_evidence_required",
        "required_output": copy.deepcopy(pcp["required_output"]),
        "stop_conditions": sorted(case["stop_conditions"]),
        "handoff_boundary": {
            "human_handoff_required": case["handoff_policy"]["human_handoff_required"],
            "automatic_orchestration_allowed": case["handoff_policy"]["automatic_orchestration_allowed"],
        },
        "capability_discovery": {
            "owner": case["handoff_policy"]["capability_discovery_owner"],
            "shared_mechanism_required": case["handoff_policy"]["shared_discovery_mechanism_required"],
        },
        "readiness": "verification_required",
        "simulation_status": case["simulation_status"],
        "downstream_adoption_status": case["downstream_adoption_status"],
    }


def _preserved_value_errors(label: str, expected: Any, actual: Any) -> list[str]:
    if actual != expected:
        return [f"{label} must be preserved exactly during handoff"]
    return []


def validate_receipt(case: dict[str, Any], receipt: dict[str, Any], root: Path = ROOT) -> list[str]:
    errors = _schema_errors(receipt, load_json(root / RECEIPT_SCHEMA.relative_to(ROOT)), "receipt")
    expected = build_receipt(case)
    if _contains_private_locator(receipt):
        errors.append("public-safe projection cannot contain a private locator, path, or email")
    if receipt.get("case_ref") != expected["case_ref"]:
        errors.append("case_ref must not change during handoff")
    if receipt.get("target") != expected["target"]:
        errors.append("target must not change during handoff")
    if receipt.get("authority_ceiling") != "candidate":
        errors.append("authority cannot increase during handoff")
    if receipt.get("readiness") != "verification_required":
        errors.append("candidate handoff cannot be promoted to work_ready")
    if receipt.get("evidence_confirmation_basis") != "independent_repo_runtime_evidence_required":
        errors.append("model confidence cannot confirm repository or runtime evidence")
    source_scope = receipt.get("source_scope") if isinstance(receipt.get("source_scope"), dict) else {}
    if source_scope.get("coverage_claim") != "bounded_not_complete":
        errors.append("receiving workspace cannot claim all relevant sources were searched")
    capability_discovery = (
        receipt.get("capability_discovery")
        if isinstance(receipt.get("capability_discovery"), dict)
        else {}
    )
    if capability_discovery != {"owner": "receiving_workspace", "shared_mechanism_required": False}:
        errors.append("canonical handoff cannot require a shared or workspace-specific discovery mechanism")
    if receipt.get("simulation_status") == "synthetic_reference" and receipt.get("downstream_adoption_status") != "not_observed":
        errors.append("synthetic conformance cannot claim real downstream adoption")
    incoming = receipt.get("incoming_claims") if isinstance(receipt.get("incoming_claims"), list) else []
    for item in incoming:
        if not isinstance(item, dict):
            continue
        if item.get("incoming_status") not in {"observed", "derived", "judged", "unknown"}:
            errors.append("Google hypothesis cannot be promoted to root_cause_verified or another confirmed status")
        if item.get("confirmation_state") not in {"candidate_only", "unknown"}:
            errors.append("incoming Google claims must remain candidate-only or unknown")
    for item in receipt.get("conflicts", []) if isinstance(receipt.get("conflicts"), list) else []:
        if isinstance(item, dict) and item.get("status") != "unresolved":
            errors.append("unresolved CONFLICT cannot be silently resolved during handoff")

    errors.extend(_preserved_value_errors("source_scope", expected["source_scope"], receipt.get("source_scope")))
    errors.extend(_preserved_value_errors("incoming_claims", expected["incoming_claims"], receipt.get("incoming_claims")))
    errors.extend(
        _preserved_value_errors(
            "claims_requiring_repo_verification",
            expected["claims_requiring_repo_verification"],
            receipt.get("claims_requiring_repo_verification"),
        )
    )
    errors.extend(_preserved_value_errors("UNKNOWN ids", expected["unknown_ids"], receipt.get("unknown_ids")))
    errors.extend(_preserved_value_errors("CONFLICT state", expected["conflicts"], receipt.get("conflicts")))
    errors.extend(
        _preserved_value_errors(
            "strongest counterevidence",
            expected["strongest_counterevidence"],
            receipt.get("strongest_counterevidence"),
        )
    )
    errors.extend(_preserved_value_errors("evidence_ref ids", expected["evidence_ref_ids"], receipt.get("evidence_ref_ids")))
    errors.extend(
        _preserved_value_errors(
            "required coding verification",
            expected["required_coding_verification"],
            receipt.get("required_coding_verification"),
        )
    )
    errors.extend(_preserved_value_errors("stop conditions", expected["stop_conditions"], receipt.get("stop_conditions")))
    for field in (
        "$schema",
        "contract",
        "receipt_id",
        "privacy_classification",
        "required_output",
        "handoff_boundary",
    ):
        if receipt.get(field) != expected[field]:
            errors.append(f"{field} must match the deterministic canonical projection")
    return sorted(set(errors))


def canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--receipt", type=Path, help="committed deterministic receipt to validate")
    parser.add_argument("--print-receipt", action="store_true", help="print the deterministic receipt")
    args = parser.parse_args()
    try:
        case = load_json(args.fixture)
        errors = validate_case(case, ROOT)
        generated = build_receipt(case) if not errors else {}
        if not errors:
            errors.extend(validate_receipt(case, generated, ROOT))
        if args.receipt and not errors:
            receipt = load_json(args.receipt)
            errors.extend(validate_receipt(case, receipt, ROOT))
            if canonical_json(receipt) != canonical_json(generated):
                errors.append("committed receipt bytes do not match the deterministic reference consumer")
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        errors = [str(exc)]
        generated = {}
    if errors:
        for error in sorted(set(errors)):
            print(f"error: {error}", file=sys.stderr)
        return 1
    if args.print_receipt:
        print(canonical_json(generated), end="")
    else:
        print(f"cross-workspace handoff conformance: valid ({args.fixture})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
