#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate capability-composition contracts and progressive-loading semantics."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from generate_capability_composition_registry import REGISTRY_PATH, render  # noqa: E402

SCHEMA_PATH = Path("schemas/capability/capability-composition.v1.schema.json")
NEVER_CONTEXT_ROLES = {"maintainer_test", "ci_enforcement"}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def structural_errors(schema: dict[str, Any], concept: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(concept), key=lambda error: list(error.path))
    return [f"schema: {error.message}" for error in errors]


def graph_cycle(stage_map: dict[str, dict[str, Any]], first_stage: str) -> tuple[set[str], bool]:
    visited: set[str] = set()
    active: set[str] = set()
    cycle = False

    def visit(stage_id: str) -> None:
        nonlocal cycle
        if stage_id in active:
            cycle = True
            return
        if stage_id in visited or stage_id not in stage_map:
            return
        active.add(stage_id)
        for target in stage_map[stage_id].get("next_stages", []):
            visit(str(target))
        active.remove(stage_id)
        visited.add(stage_id)

    visit(first_stage)
    return visited, cycle


def validate_concept(
    root: Path,
    concept_path: Path,
    concept: dict[str, Any],
    schema: dict[str, Any],
) -> list[str]:
    errors = structural_errors(schema, concept)
    if errors:
        return errors

    concept_id = str(concept["concept_id"])
    if concept_path.parent.name != concept_id:
        errors.append("concept_id must match its concepts/<concept-id>/ directory")

    entrypoint = root / str(concept["entrypoint"])
    if not entrypoint.is_file():
        errors.append(f"entrypoint does not exist: {concept['entrypoint']}")

    stages = concept["stages"]
    stage_ids = [str(stage["stage_id"]) for stage in stages]
    if len(stage_ids) != len(set(stage_ids)):
        errors.append("duplicate stage_id")
    stage_map = {str(stage["stage_id"]): stage for stage in stages}
    first_stage = str(concept["first_stage"])
    if first_stage not in stage_map:
        errors.append(f"unknown first_stage: {first_stage}")

    for stage in stages:
        stage_id = str(stage["stage_id"])
        stage_entrypoint = str(stage["entrypoint"])
        if not (root / stage_entrypoint).is_file():
            errors.append(f"{stage_id}: stage entrypoint does not exist: {stage_entrypoint}")

        artifact_paths: set[str] = set()
        has_stage_entrypoint = False
        for artifact in stage["artifacts"]:
            path = str(artifact["path"])
            if path in artifact_paths:
                errors.append(f"{stage_id}: duplicate artifact path: {path}")
            artifact_paths.add(path)
            if not (root / path).is_file():
                errors.append(f"{stage_id}: artifact path does not exist: {path}")
            if path == stage_entrypoint and artifact["action"] == "read":
                has_stage_entrypoint = True

            role = str(artifact["role"])
            activation = str(artifact["activation"])
            action = str(artifact["action"])
            if role in NEVER_CONTEXT_ROLES and activation != "never_by_default":
                errors.append(f"{stage_id}: {role} must be never_by_default: {path}")
            if role in NEVER_CONTEXT_ROLES and action != "none":
                errors.append(f"{stage_id}: {role} must not be a consuming-agent action: {path}")
            if role == "validator":
                if activation != "never_by_default":
                    errors.append(f"{stage_id}: validator source must be never_by_default: {path}")
                if action != "execute":
                    errors.append(f"{stage_id}: validator must be executed, not read as context: {path}")
            if role == "machine_contract" and activation == "always":
                errors.append(f"{stage_id}: machine contract cannot be always-loaded: {path}")
            if role == "portable_skill_template" and activation == "always":
                errors.append(f"{stage_id}: portable Skill template cannot be always-loaded: {path}")

        if not has_stage_entrypoint:
            errors.append(f"{stage_id}: stage entrypoint must appear as a readable artifact")

        for target in stage["next_stages"]:
            if target not in stage_map:
                errors.append(f"{stage_id}: unknown next_stage: {target}")
            if target == stage_id:
                errors.append(f"{stage_id}: self-loop is not allowed")

    if first_stage in stage_map:
        reachable, cycle = graph_cycle(stage_map, first_stage)
        if cycle:
            errors.append("stage graph must be acyclic")
        unreachable = sorted(set(stage_map) - reachable)
        if unreachable:
            errors.append(f"unreachable stage(s): {', '.join(unreachable)}")

    handoff_edges: set[tuple[str, str]] = set()
    for handoff in concept["handoffs"]:
        source = str(handoff["from_stage"])
        target = str(handoff["to_stage"])
        edge = (source, target)
        if edge in handoff_edges:
            errors.append(f"duplicate handoff edge: {source}->{target}")
        handoff_edges.add(edge)
        if source not in stage_map:
            errors.append(f"handoff has unknown from_stage: {source}")
        if target not in stage_map:
            errors.append(f"handoff has unknown to_stage: {target}")
        if source in stage_map and target not in stage_map[source]["next_stages"]:
            errors.append(f"handoff edge is not declared by stage graph: {source}->{target}")

    graph_edges = {
        (stage_id, str(target))
        for stage_id, stage in stage_map.items()
        for target in stage["next_stages"]
    }
    missing_handoffs = sorted(graph_edges - handoff_edges)
    for source, target in missing_handoffs:
        errors.append(f"stage edge has no handoff contract: {source}->{target}")

    return errors


def validate_all(root: Path) -> list[str]:
    schema = load_json(root / SCHEMA_PATH)
    errors: list[str] = []
    concept_paths = sorted((root / "concepts").glob("*/concept.json"))
    if not concept_paths:
        return ["no capability compositions found"]

    seen: set[str] = set()
    for concept_path in concept_paths:
        try:
            concept = load_json(concept_path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(str(exc))
            continue
        concept_id = str(concept.get("concept_id", ""))
        if concept_id in seen:
            errors.append(f"duplicate concept_id: {concept_id}")
        seen.add(concept_id)
        for error in validate_concept(root, concept_path, concept, schema):
            errors.append(f"{concept_path.relative_to(root)}: {error}")

    expected = render(root)
    registry_path = root / REGISTRY_PATH
    actual = registry_path.read_text(encoding="utf-8") if registry_path.exists() else ""
    if actual != expected:
        errors.append(f"projection drift: {REGISTRY_PATH}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    try:
        errors = validate_all(root)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        errors = [str(exc)]

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    count = len(list((root / "concepts").glob("*/concept.json")))
    print(f"validated {count} capability composition(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
