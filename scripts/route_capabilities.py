#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Route a task from compact metadata without loading full Skill bodies."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

HIGH_IMPACT = (
    "approve merge", "approve release", "deploy production", "delete production",
    "automatic compliance ruling", "rank employees", "批准发布", "生产部署", "人员排名",
)


def norm(value: str) -> str:
    return " ".join(value.casefold().replace("_", " ").split())


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{number}: expected object")
            rows.append(value)
    return rows


def score(rule: dict[str, Any], text: str, stage: str) -> tuple[int, list[str]]:
    value = 0
    signals: list[str] = []
    for term in rule.get("terms", []):
        if norm(str(term)) in text:
            value += 3
            signals.append(str(term))
    stages = {norm(str(item)) for item in rule.get("stages", [])}
    if stage and stage in stages:
        value += 2
        signals.append(f"stage:{stage}")
    return value, signals


def route(root: Path, request: str, stage: str, mode: str) -> dict[str, Any]:
    text = norm(request)
    stage_value = norm(stage)
    ranked: list[tuple[int, int, dict[str, Any], list[str]]] = []
    for rule in load_jsonl(root / "registry" / "capability-routing.index.jsonl"):
        value, signals = score(rule, text, stage_value)
        if value >= int(rule.get("min_score", 1)):
            ranked.append((value, int(rule.get("priority", 0)), rule, signals))
    ranked.sort(key=lambda item: (-item[0], -item[1], str(item[2].get("route_id", ""))))

    base = {
        "schema": "capability.routing_decision.v1",
        "mode": mode,
        "request_summary": request[:240],
        "selected": [],
        "candidates": [],
        "load_plan": {"metadata": ["registry/capability-routing.index.jsonl"], "skill_bodies": [], "resources": [], "task_context": ["scope", "files and symbols", "tests", "risks", "decisions", "evidence refs", "permissions"]},
        "human_confirmation": [],
        "stop_conditions": ["requested visible outcome reached", "missing permission or evidence", "conflicting evidence", "accountable human judgment required"],
        "warnings": [],
    }
    if not ranked:
        return {**base, "status": "no_match", "human_confirmation": ["clarify the desired visible outcome or invoke the conductor manually"]}

    top_score, _, top, signals = ranked[0]
    second = ranked[1][0] if len(ranked) > 1 else 0
    margin = top_score - second
    candidates = [
        {"skill_id": item[2]["skill_id"], "score": item[0], "matched_signals": item[3]}
        for item in ranked[:3]
    ]
    selected = {"skill_id": top["skill_id"], "score": top_score, "matched_signals": signals}
    high_impact = [phrase for phrase in HIGH_IMPACT if norm(phrase) in text]
    ambiguous = margin < int(top.get("min_margin", 0))
    policy = str(top.get("policy", "recommend"))
    confirmation = bool(top.get("requires_confirmation", False))

    if high_impact:
        status = "ask"
        base["warnings"].append("high-impact authority language detected")
        base["human_confirmation"].append("confirm accountable owner approval")
    elif ambiguous:
        status = "ask" if mode == "auto" else "recommend"
        base["human_confirmation"].append("choose between closely matched capabilities or clarify the outcome")
    elif mode == "auto" and policy == "auto" and not confirmation:
        status = "auto_invoke"
    else:
        status = "recommend"
        if confirmation:
            base["human_confirmation"].append("confirm scope and permission before execution")

    base["selected"] = [selected]
    base["candidates"] = candidates
    base["load_plan"]["skill_bodies"] = [f"skills/{top['skill_id']}/SKILL.md"]
    return {**base, "status": status}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--request", required=True)
    parser.add_argument("--stage", default="")
    parser.add_argument("--role", default="")
    parser.add_argument("--desired-output", default="")
    parser.add_argument("--mode", choices=["manual", "assist", "auto"], default="assist")
    args = parser.parse_args()
    try:
        request = " ".join(part for part in [args.request, args.desired_output] if part)
        result = route(Path(args.root).resolve(), request, args.stage, args.mode)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
