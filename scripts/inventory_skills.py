#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Inventory Markdown-based skill packages."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_SECTIONS = {
    "goal": "has_goal",
    "use when": "has_use_when",
    "do not use when": "has_do_not_use_when",
    "inputs": "has_inputs",
    "outputs": "has_outputs",
    "workflow": "has_workflow",
    "rules": "has_rules",
    "verification": "has_verification",
    "failure modes": "has_failure_modes",
}

KNOWN_RISK_FLAGS = [
    "missing_frontmatter",
    "missing_description",
    "missing_goal",
    "missing_use_when",
    "missing_workflow",
    "missing_verification",
    "missing_failure_modes",
    "large_skill_md",
    "possible_knowledge_dump",
    "raw_log_or_transcript_pattern",
    "vague_description",
    "markdown_table_bulk_context",
    "verbose_json_bulk_context",
    "hidden_hard_rules_in_references",
    "long_prose_explanations",
    "repeated_bullets",
    "deeply_nested_headings",
    "repeated_examples",
    "conport_record_missing",
    "conport_record_stale",
    "conport_unavailable",
    "source_verification_needed",
    "raw_file_loaded_without_conport_first",
    "frontmatter_schema_changed",
    "frontmatter_property_deleted",
    "frontmatter_property_renamed",
    "frontmatter_schema_change_review_needed",
    "description_missing_use_boundary",
    "description_missing_do_not_use_boundary",
    "description_not_progressive_disclosure_ready",
    "missing_conport_first_policy",
    "missing_token_roi_policy",
    "stable_prefix_guidance_missing",
    "human_prose_overused_in_control_plane",
]

DISALLOWED_NEW_FRONTMATTER_KEYS = {
    "use_when",
    "do_not_use_when",
    "required_inputs",
    "expected_outputs",
    "retrieval_policy",
    "token_policy",
    "x-lattice",
}


def estimate_tokens(text: str) -> int:
    return max(1, (len(text) + 3) // 4) if text else 0


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    match = re.match(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.DOTALL)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def has_heading(text: str, heading: str) -> bool:
    pattern = r"(?im)^#{1,6}\s+" + re.escape(heading) + r"\s*$"
    return bool(re.search(pattern, text))


def has_use_boundary(description: str) -> bool:
    return bool(re.search(r"(?i)\b(use for|use when|when to use|use to|use with|use if)\b", description))


def has_do_not_use_boundary(description: str) -> bool:
    return bool(re.search(r"(?i)\b(do not use|don't use|not use|avoid)\b", description))


def mentions_input_or_source(description: str) -> bool:
    return bool(re.search(r"(?i)\b(input|source|skill\.md|markdown|file|csv|json|instructions?)\b", description))


def mentions_output_or_result(description: str) -> bool:
    return bool(re.search(r"(?i)\b(output|result|package|report|optimized|rewrite|refactor)\b", description))


def mentions_behavior_preservation(description: str) -> bool:
    return bool(re.search(r"(?i)\b(preserv|behavior|constraint|safety|validation|rejection|failure)\b", description))


def mentions_conport(description: str) -> bool:
    return bool(re.search(r"(?i)\bConPort\b", description))


def likely_renamed_key(missing_key: str, added_keys: set[str]) -> bool:
    normalized_missing = re.sub(r"[^a-z0-9]", "", missing_key.lower())
    for key in added_keys:
        normalized_added = re.sub(r"[^a-z0-9]", "", key.lower())
        if normalized_missing == normalized_added:
            return True
    return False


def has_conport_first_policy(text: str) -> bool:
    return "query_ConPort_MCP_before_loading_or_searching_full_skill_text" in text or bool(
        re.search(r"(?is)ConPort.+before.+(loading|searching).+full.+skill", text)
    )


def has_token_roi_policy(text: str) -> bool:
    return "quality_adjusted_output_per_token_cost" in text or "quality-adjusted token ROI" in text or "high-quality output per token cost" in text


def has_stable_prefix_guidance(text: str) -> bool:
    return "stable prefix" in text.lower() or "CACHE.001" in text


def progressive_disclosure_ready(description: str, conport_relevant: bool) -> bool:
    checks = [
        has_use_boundary(description),
        has_do_not_use_boundary(description),
        mentions_input_or_source(description),
        mentions_output_or_result(description),
        mentions_behavior_preservation(description),
    ]
    if conport_relevant:
        checks.append(mentions_conport(description))
    return all(checks)


def count_children(skill_file: Path, dirname: str, patterns: tuple[str, ...]) -> int:
    folder = skill_file.parent / dirname
    if not folder.is_dir():
        return 0
    return sum(1 for path in folder.rglob("*") if path.is_file() and path.suffix.lower() in patterns)


def find_skill_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    files: list[Path] = []
    for path in root.rglob("*.md"):
        if path.name == "SKILL.md":
            files.append(path)
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="replace")
        frontmatter = parse_frontmatter(text)
        if "name" in frontmatter and "description" in frontmatter:
            files.append(path)
        elif re.search(r"(?im)^#\s+.*skill", text) and "Use When" in text:
            files.append(path)
    return sorted(set(files))


def detect_risks(
    path: Path,
    text: str,
    frontmatter: dict[str, str],
    section_flags: dict[str, bool],
    baseline_frontmatter_keys: set[str] | None = None,
) -> list[str]:
    flags: list[str] = []
    description = frontmatter.get("description", "")
    line_count = len(text.splitlines())
    token_count = estimate_tokens(text)

    if not frontmatter:
        flags.append("missing_frontmatter")
    if not description:
        flags.append("missing_description")
    if not section_flags["has_goal"]:
        flags.append("missing_goal")
    if not section_flags["has_use_when"]:
        flags.append("missing_use_when")
    if not section_flags["has_workflow"]:
        flags.append("missing_workflow")
    if not section_flags["has_verification"]:
        flags.append("missing_verification")
    if not section_flags["has_failure_modes"]:
        flags.append("missing_failure_modes")
    if token_count > 2000 or line_count > 350:
        flags.append("large_skill_md")
    if token_count > 1200 and count_children(path, "references", (".md", ".txt")) == 0:
        flags.append("possible_knowledge_dump")
    if re.search(r"(?i)(raw transcript|assistant:|user:|otel|span_id|trace_id|stack trace|timestamp=.*level=)", text):
        flags.append("raw_log_or_transcript_pattern")
    if description and (len(description) < 30 or re.search(r"(?i)\b(help|useful|various|things|stuff)\b", description)):
        flags.append("vague_description")
    if description and not has_use_boundary(description):
        flags.append("description_missing_use_boundary")
    if description and not has_do_not_use_boundary(description):
        flags.append("description_missing_do_not_use_boundary")
    if description and not progressive_disclosure_ready(description, "ConPort" in text):
        flags.append("description_not_progressive_disclosure_ready")
    if not has_conport_first_policy(text):
        flags.append("missing_conport_first_policy")
    if not has_token_roi_policy(text):
        flags.append("missing_token_roi_policy")
    if not has_stable_prefix_guidance(text):
        flags.append("stable_prefix_guidance_missing")
    if any(key in frontmatter for key in DISALLOWED_NEW_FRONTMATTER_KEYS):
        flags.append("frontmatter_schema_change_review_needed")
        flags.append("frontmatter_schema_changed")
    if baseline_frontmatter_keys is not None:
        current_keys = set(frontmatter)
        missing_keys = baseline_frontmatter_keys - current_keys
        added_keys = current_keys - baseline_frontmatter_keys
        if missing_keys:
            flags.append("frontmatter_property_deleted")
            flags.append("frontmatter_schema_changed")
        if any(likely_renamed_key(missing_key, added_keys) for missing_key in missing_keys):
            flags.append("frontmatter_property_renamed")
            flags.append("frontmatter_schema_changed")
    if len(re.findall(r"(?m)^\|.*\|$", text)) > 12:
        flags.append("markdown_table_bulk_context")
    if len(re.findall(r'(?m)^\s*"\w+"\s*:', text)) > 25:
        flags.append("verbose_json_bulk_context")
    if references_contain_rule_words(path) and "References" not in text:
        flags.append("hidden_hard_rules_in_references")
    if len(re.findall(r"(?m)^.{180,}$", text)) > 10:
        flags.append("long_prose_explanations")
        flags.append("human_prose_overused_in_control_plane")
    if len(re.findall(r"(?m)^\s*[-*]\s+", text)) > 80:
        flags.append("repeated_bullets")
    if re.search(r"(?m)^#{5,6}\s+", text):
        flags.append("deeply_nested_headings")
    if len(re.findall(r"(?i)\bexample\b", text)) > 12:
        flags.append("repeated_examples")

    flags.append("conport_unavailable")
    return flags


def references_contain_rule_words(skill_file: Path) -> bool:
    ref_dir = skill_file.parent / "references"
    if not ref_dir.is_dir():
        return False
    for path in ref_dir.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r"(?i)\b(MUST|NEVER|SHOULD|required|forbidden)\b", text):
            return True
    return False


def inventory_record(path: Path, root: Path, baseline_frontmatter_keys: set[str] | None = None) -> dict[str, object]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
    frontmatter = parse_frontmatter(text)
    lowered = text.lower()
    description = frontmatter.get("description", "")
    conport_relevant = "conport" in lowered
    section_flags = {
        out_key: (has_heading(text, heading) or heading in lowered)
        for heading, out_key in REQUIRED_SECTIONS.items()
    }
    record: dict[str, object] = {
        "path": str(path.relative_to(root.parent if root.name == path.parent.name else root) if path.is_relative_to(root) else path),
        "name": frontmatter.get("name") or path.parent.name,
        "description": frontmatter.get("description", ""),
        "line_count": len(text.splitlines()),
        "estimated_tokens": estimate_tokens(text),
        "has_frontmatter": bool(frontmatter),
        "frontmatter_keys": sorted(frontmatter.keys()),
        "frontmatter_key_count": len(frontmatter),
        "frontmatter_schema_preserved": (
            not any(key in frontmatter for key in DISALLOWED_NEW_FRONTMATTER_KEYS)
            and (baseline_frontmatter_keys is None or baseline_frontmatter_keys.issubset(set(frontmatter)))
        ),
        "description_has_use_boundary": has_use_boundary(description),
        "description_has_do_not_use_boundary": has_do_not_use_boundary(description),
        "description_mentions_inputs_or_source_type": mentions_input_or_source(description),
        "description_mentions_outputs_or_result_type": mentions_output_or_result(description),
        "description_mentions_behavior_preservation": mentions_behavior_preservation(description),
        "description_mentions_conport_when_relevant": (not conport_relevant) or mentions_conport(description),
        "description_progressive_disclosure_ready": progressive_disclosure_ready(description, conport_relevant),
        "has_conport_first_policy": has_conport_first_policy(text),
        "has_token_roi_policy": has_token_roi_policy(text),
        "has_stable_prefix_guidance": has_stable_prefix_guidance(text),
        **section_flags,
        "reference_count": count_children(path, "references", (".md", ".txt")),
        "script_count": count_children(path, "scripts", (".py", ".sh", ".ps1", ".md")),
        "schema_count": count_children(path, "schemas", (".json",)),
        "eval_count": count_children(path, "evals", (".jsonl", ".json", ".md")),
        "known_risk_flags": KNOWN_RISK_FLAGS,
    }
    record["risk_flags"] = detect_risks(path, text, frontmatter, section_flags, baseline_frontmatter_keys)
    return record


def load_baseline_frontmatter_keys(path: Path | None) -> dict[str, set[str]]:
    if path is None or not path.exists():
        return {}
    baselines: dict[str, set[str]] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            record_path = str(record.get("path", ""))
            keys = record.get("frontmatter_keys", [])
            if record_path and isinstance(keys, list):
                baselines[record_path] = {str(key) for key in keys}
    return baselines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Skills directory to scan.")
    parser.add_argument("--out", required=True, help="Output JSONL path.")
    parser.add_argument("--baseline-inventory", help="Optional prior inventory JSONL for frontmatter schema comparison.")
    args = parser.parse_args()

    root = Path(args.root)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True) if out.parent != Path("") else None
    baselines = load_baseline_frontmatter_keys(Path(args.baseline_inventory) if args.baseline_inventory else None)
    records = []
    for path in find_skill_files(root):
        temp_record = inventory_record(path, root)
        record_path = str(temp_record["path"])
        records.append(inventory_record(path, root, baselines.get(record_path)))
    with out.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
    print(f"wrote {len(records)} skill records to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
