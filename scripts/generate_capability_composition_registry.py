#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate the compact capability-composition discovery projection."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REGISTRY_PATH = Path("registry/capability-compositions.index.jsonl")


def load_concepts(root: Path) -> list[dict[str, Any]]:
    concepts: list[dict[str, Any]] = []
    for path in sorted((root / "concepts").glob("*/concept.json")):
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError(f"{path}: expected JSON object")
        concepts.append(value)
    return concepts


def project(concept: dict[str, Any]) -> dict[str, Any]:
    return {
        "concept_id": concept["concept_id"],
        "display_name": concept["display_name"],
        "status": concept["status"],
        "public_only": concept["public_only"],
        "trigger": concept["trigger"],
        "entrypoint": concept["entrypoint"],
        "first_stage": concept["first_stage"],
        "stages": [
            {
                "stage_id": stage["stage_id"],
                "display_name": stage["display_name"],
                "entrypoint": stage["entrypoint"],
                "next_stages": stage["next_stages"],
            }
            for stage in concept["stages"]
        ],
        "authority_boundary": concept["authority_boundary"],
    }


def render(root: Path) -> str:
    records = sorted(
        (project(concept) for concept in load_concepts(root)),
        key=lambda item: item["concept_id"],
    )
    return "".join(
        json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
        for record in records
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    expected = render(root)
    path = root / REGISTRY_PATH

    if args.check:
        actual = path.read_text(encoding="utf-8") if path.exists() else ""
        if actual != expected:
            print(f"error: projection drift: {REGISTRY_PATH}", file=sys.stderr)
            return 1
        print(f"validated composition projection: {REGISTRY_PATH}")
        return 0

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(expected, encoding="utf-8")
    print(f"wrote composition projection: {REGISTRY_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
