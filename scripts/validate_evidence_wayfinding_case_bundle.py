#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate an Evidence Wayfinding case through one authoritative entrypoint.

The bundle validator composes the existing structural schemas, semantic validators,
cross-file Case Spine checks, repository evidence integrity, and optional governed
evolution artifacts. It does not replace those lower-level contracts; it fixes the
consumer failure mode where running only one apparently-complete validator can create
a false green.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import validate_blind_challenge_execution as BLIND
import validate_evidence_wayfinding_case as CASE_SPINE
import validate_harness_mutation_candidate as MUTATION
import validate_json_schema_instance as SCHEMA
import validate_portable_case_pack as PACK
import validate_reserved_evaluation_handoff as HANDOFF_V1
import validate_reserved_evaluation_handoff_v2 as HANDOFF_V2

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas" / "capability"

STRUCTURAL_CONTRACTS = {
    "portable-case-pack.json": SCHEMA_DIR / "portable-case-pack.v1.schema.json",
    "admission-receipt.json": SCHEMA_DIR / "attention-admission-receipt.v1.schema.json",
    "outcome-receipt.json": SCHEMA_DIR / "outcome-receipt.v1.schema.json",
    "harness-mutation-candidate.json": SCHEMA_DIR / "harness-mutation-candidate.v1.schema.json",
    "blind-challenge-execution.blocked.json": SCHEMA_DIR / "blind-challenge-execution.v1.schema.json",
}

REQUIRED_CORE_FILES = {
    "case-contract.json",
    "portable-case-pack.json",
    "admission-receipt.json",
    "decision-card.json",
    "verification-receipt.json",
    "outcome-receipt.json",
}

EVOLUTION_DEPENDENCIES = {
    "harness-mutation-candidate.json": {"outcome-receipt.json", "portable-case-pack.json"},
    "blind-challenge-execution.blocked.json": {"harness-mutation-candidate.json"},
}

HEX40 = re.compile(r"^[0-9a-f]{40}$")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def _prefix(label: str, errors: list[str]) -> list[str]:
    return [f"{label}: {error}" for error in errors]


def _git(repo_root: Path, *args: str) -> tuple[str | None, str | None]:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return None, str(exc)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "git command failed"
        return None, detail
    return completed.stdout.strip(), None


def validate_repo_evidence(pack: dict[str, Any], repo_root: Path) -> list[str]:
    """Verify repo:// evidence references against immutable Git objects."""
    errors: list[str] = []
    evidence = pack.get("evidence_refs", [])
    if not isinstance(evidence, list):
        return ["portable-case-pack evidence_refs must be a list before integrity validation"]

    for index, item in enumerate(evidence):
        if not isinstance(item, dict):
            continue
        evidence_id = str(item.get("id", f"index-{index}"))
        uri = str(item.get("uri", ""))
        content_hash = str(item.get("content_hash", ""))
        if not uri.startswith("repo://"):
            continue

        if uri.startswith("repo://commit/"):
            commit = uri.removeprefix("repo://commit/")
            if not HEX40.fullmatch(commit):
                errors.append(f"{evidence_id} repo commit reference must use a full 40-hex SHA")
                continue
            _, git_error = _git(repo_root, "cat-file", "-e", f"{commit}^{{commit}}")
            if git_error:
                errors.append(f"{evidence_id} referenced commit is not resolvable: {git_error}")
            if content_hash != f"git:{commit}":
                errors.append(
                    f"{evidence_id} commit content_hash must equal git:{commit}; got {content_hash or '<empty>'}"
                )
            continue

        raw = uri.removeprefix("repo://")
        if "@" not in raw:
            errors.append(f"{evidence_id} repo file evidence must use repo://<path>@<commit>")
            continue
        path_text, commit = raw.rsplit("@", 1)
        if not path_text or not HEX40.fullmatch(commit):
            errors.append(f"{evidence_id} repo file evidence requires a path and full 40-hex commit SHA")
            continue
        if not content_hash.startswith("git:") or not HEX40.fullmatch(content_hash.removeprefix("git:")):
            errors.append(f"{evidence_id} repo file evidence requires content_hash=git:<40-hex-blob-sha>")
            continue

        blob_sha, git_error = _git(repo_root, "rev-parse", f"{commit}:{path_text}")
        if git_error or blob_sha is None:
            errors.append(f"{evidence_id} referenced Git blob is not resolvable: {git_error}")
            continue
        expected = f"git:{blob_sha}"
        if content_hash != expected:
            errors.append(
                f"{evidence_id} content_hash does not match referenced Git blob: expected {expected}, got {content_hash}"
            )

    return errors


def _validate_structural(case_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    validated: list[str] = []
    for filename, schema_path in STRUCTURAL_CONTRACTS.items():
        instance = case_dir / filename
        if not instance.exists():
            continue
        try:
            schema_errors = SCHEMA.validate_instance(schema_path, instance)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            schema_errors = [str(exc)]
        errors.extend(_prefix(f"structural/{filename}", schema_errors))
        if not schema_errors:
            validated.append(filename)
    return errors, validated


def _validate_handoffs(
    case_dir: Path,
    candidate: dict[str, Any],
    blocked_execution: dict[str, Any],
    *,
    trust_store: dict[str, Any] | None,
    consumed_nonces: set[str] | None,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    validated: list[str] = []
    for path in sorted(case_dir.glob("reserved-evaluation-handoff*.jsonl")):
        try:
            records = HANDOFF_V2.load_jsonl(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"handoff/{path.name}: {exc}")
            continue
        if not records:
            errors.append(f"handoff/{path.name}: handoff JSONL must not be empty")
            continue

        schema_id = records[0].get("schema")
        if schema_id == HANDOFF_V1.SCHEMA_ID:
            schema_path = SCHEMA_DIR / "reserved-evaluation-handoff-record.v1.schema.json"
            handoff_errors = HANDOFF_V1.validate_handoff(
                records,
                candidate,
                blocked_execution,
                HANDOFF_V1.load_json(schema_path),
            )
        elif schema_id == HANDOFF_V2.SCHEMA_ID:
            schema_path = SCHEMA_DIR / "reserved-evaluation-handoff-record.v2.schema.json"
            handoff_errors = HANDOFF_V2.validate_handoff(
                records,
                candidate,
                blocked_execution,
                HANDOFF_V2.load_json(schema_path),
                trust_store=trust_store,
                consumed_nonces=consumed_nonces,
            )
        else:
            handoff_errors = [f"unsupported reserved handoff schema: {schema_id!r}"]

        errors.extend(_prefix(f"handoff/{path.name}", handoff_errors))
        if not handoff_errors:
            validated.append(path.name)
    return errors, validated


def validate_bundle(
    case_dir: Path,
    *,
    repo_root: Path = ROOT,
    trust_store: dict[str, Any] | None = None,
    consumed_nonces: set[str] | None = None,
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    summary: dict[str, Any] = {
        "case_dir": str(case_dir),
        "layers": {
            "structural": [],
            "semantic": [],
            "cross_file": [],
            "evidence_integrity": [],
            "evolution": [],
            "handoff": [],
        },
    }

    missing = sorted(filename for filename in REQUIRED_CORE_FILES if not (case_dir / filename).exists())
    if missing:
        errors.extend(f"bundle: missing required core file: {filename}" for filename in missing)
        summary["status"] = "fail"
        return errors, summary

    for filename, dependencies in EVOLUTION_DEPENDENCIES.items():
        if not (case_dir / filename).exists():
            continue
        for dependency in dependencies:
            if not (case_dir / dependency).exists():
                errors.append(f"bundle: {filename} requires {dependency}")

    structural_errors, structurally_validated = _validate_structural(case_dir)
    errors.extend(structural_errors)
    summary["layers"]["structural"] = structurally_validated

    pack_path = case_dir / "portable-case-pack.json"
    pack = load_json(pack_path)
    pack_errors = PACK.validate_pack(pack)
    errors.extend(_prefix("semantic/portable-case-pack.json", pack_errors))
    if not pack_errors:
        summary["layers"]["semantic"].append("portable-case-pack.json")

    spine_errors = CASE_SPINE.validate_case(case_dir)
    errors.extend(_prefix("cross-file/case-spine", spine_errors))
    if not spine_errors:
        summary["layers"]["cross_file"].append("case-spine")

    integrity_errors = validate_repo_evidence(pack, repo_root)
    errors.extend(_prefix("evidence-integrity", integrity_errors))
    if not integrity_errors:
        summary["layers"]["evidence_integrity"] = [
            str(item.get("id"))
            for item in pack.get("evidence_refs", [])
            if isinstance(item, dict) and str(item.get("uri", "")).startswith("repo://")
        ]

    candidate_path = case_dir / "harness-mutation-candidate.json"
    blind_path = case_dir / "blind-challenge-execution.blocked.json"
    candidate: dict[str, Any] | None = None
    blocked_execution: dict[str, Any] | None = None

    if candidate_path.exists():
        candidate = load_json(candidate_path)
        outcome = load_json(case_dir / "outcome-receipt.json")
        candidate_errors = MUTATION.validate_candidate(candidate, outcome, pack)
        errors.extend(_prefix("evolution/harness-mutation-candidate.json", candidate_errors))
        if not candidate_errors:
            summary["layers"]["evolution"].append("harness-mutation-candidate.json")

    if blind_path.exists():
        if candidate is None:
            errors.append("evolution: blind-challenge-execution.blocked.json requires harness-mutation-candidate.json")
        else:
            blocked_execution = load_json(blind_path)
            blind_errors = BLIND.validate_execution(blocked_execution, candidate)
            errors.extend(_prefix("evolution/blind-challenge-execution.blocked.json", blind_errors))
            if not blind_errors:
                summary["layers"]["evolution"].append("blind-challenge-execution.blocked.json")

    handoff_paths = list(case_dir.glob("reserved-evaluation-handoff*.jsonl"))
    if handoff_paths:
        if candidate is None or blocked_execution is None:
            errors.append("handoff: reserved evaluation handoff requires candidate and blocked Blind Challenge execution")
        else:
            handoff_errors, validated_handoffs = _validate_handoffs(
                case_dir,
                candidate,
                blocked_execution,
                trust_store=trust_store,
                consumed_nonces=consumed_nonces,
            )
            errors.extend(handoff_errors)
            summary["layers"]["handoff"] = validated_handoffs

    summary["status"] = "fail" if errors else "pass"
    return errors, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_dir", help="Evidence Wayfinding case bundle directory")
    parser.add_argument(
        "--repo-root",
        default=str(ROOT),
        help="Git repository root used to verify repo:// evidence content hashes",
    )
    parser.add_argument(
        "--trust-store",
        help="Trusted evaluator public-key store when the bundle includes a completed v2 attestation",
    )
    parser.add_argument(
        "--consumed-nonces",
        help="Consumed request nonce ledger when the bundle includes a completed v2 attestation",
    )
    args = parser.parse_args()

    try:
        trust_store = HANDOFF_V2.load_json(Path(args.trust_store)) if args.trust_store else None
        consumed_nonces = (
            HANDOFF_V2.load_consumed_nonces(Path(args.consumed_nonces))
            if args.consumed_nonces
            else None
        )
        errors, summary = validate_bundle(
            Path(args.case_dir),
            repo_root=Path(args.repo_root),
            trust_store=trust_store,
            consumed_nonces=consumed_nonces,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
        summary = {"case_dir": args.case_dir, "status": "fail", "layers": {}}

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(json.dumps(summary, sort_keys=True), file=sys.stderr)
        return 1

    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
