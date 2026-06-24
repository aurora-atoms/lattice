#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate a Markdown quality report from skill inventory JSONL."""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path


MISSING_FIELDS = [
    ("has_frontmatter", "missing frontmatter"),
    ("frontmatter_schema_preserved", "frontmatter schema not preserved"),
    ("description_progressive_disclosure_ready", "description not progressive-disclosure ready"),
    ("has_goal", "missing goal"),
    ("has_use_when", "missing use when"),
    ("has_workflow", "missing workflow"),
    ("has_verification", "missing verification"),
    ("has_failure_modes", "missing failure modes"),
    ("has_conport_first_policy", "missing ConPort-first policy"),
    ("has_token_roi_policy", "missing token ROI policy"),
    ("has_stable_prefix_guidance", "missing stable-prefix guidance"),
]


def load_inventory(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    records: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_number}: invalid JSONL: {exc}") from exc
    return records


def table(rows: list[list[object]]) -> str:
    if not rows:
        return "_None._\n"
    widths = [max(len(str(row[index])) for row in rows) for index in range(len(rows[0]))]
    lines = []
    for row in rows:
        lines.append(" | ".join(str(cell).ljust(widths[index]) for index, cell in enumerate(row)).rstrip())
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", required=True, help="Inventory JSONL path.")
    parser.add_argument("--out", required=True, help="Output Markdown report path.")
    args = parser.parse_args()

    records = load_inventory(Path(args.inventory))
    out = Path(args.out)
    if out.parent != Path(""):
        out.parent.mkdir(parents=True, exist_ok=True)

    risk_counts: collections.Counter[str] = collections.Counter()
    for record in records:
        risk_counts.update(record.get("risk_flags", []))

    largest = sorted(records, key=lambda item: int(item.get("estimated_tokens", 0)), reverse=True)[:10]
    missing_rows: list[list[object]] = []
    for field, label in MISSING_FIELDS:
        paths = [str(record.get("path", "")) for record in records if not record.get(field)]
        if paths:
            missing_rows.append([label, len(paths), ", ".join(paths[:5])])

    candidate_flags = {
        "large_skill_md",
        "possible_knowledge_dump",
        "missing_description",
        "description_not_progressive_disclosure_ready",
        "frontmatter_schema_change_review_needed",
        "missing_workflow",
        "missing_verification",
        "source_verification_needed",
        "hidden_hard_rules_in_references",
        "missing_conport_first_policy",
        "missing_token_roi_policy",
        "stable_prefix_guidance_missing",
        "human_prose_overused_in_control_plane",
    }
    candidates = [
        record for record in records
        if candidate_flags.intersection(set(record.get("risk_flags", [])))
    ]
    candidates = sorted(candidates, key=lambda item: int(item.get("estimated_tokens", 0)), reverse=True)[:20]

    lines = [
        "# Skill Quality Report",
        "",
        "## Summary",
        "",
        f"- total skills: {len(records)}",
        f"- total risk flags: {sum(risk_counts.values())}",
        "",
        "## Largest Skills",
        "",
        table([["path", "tokens", "lines"]] + [
            [record.get("path", ""), record.get("estimated_tokens", 0), record.get("line_count", 0)]
            for record in largest
        ] if largest else []),
        "## Missing Sections",
        "",
        table([["issue", "count", "examples"]] + missing_rows if missing_rows else []),
        "## Risk Flags",
        "",
        table([["flag", "count"]] + [[flag, count] for flag, count in risk_counts.most_common()] if risk_counts else []),
        "## Top Refactor Candidates",
        "",
        table([["path", "tokens", "risk_flags"]] + [
            [record.get("path", ""), record.get("estimated_tokens", 0), ", ".join(record.get("risk_flags", []))]
            for record in candidates
        ] if candidates else []),
        "## Review Queue",
        "",
        table([["path", "reason"]] + [
            [record.get("path", ""), ", ".join(record.get("risk_flags", []))]
            for record in records
            if record.get("risk_flags")
        ] if any(record.get("risk_flags") for record in records) else []),
    ]
    with out.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))
    print(f"wrote report for {len(records)} skill records to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
