#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate Skill package structure with dependency-light checks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = [
    "Goal",
    "Use When",
    "Do Not Use When",
    "Inputs",
    "Outputs",
    "Workflow",
    "Rules",
    "Verification",
    "Failure Modes",
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


def estimate_tokens(text: str) -> int:
    return max(1, (len(text) + 3) // 4) if text else 0


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


def has_conport_first_policy(text: str) -> bool:
    return "query_ConPort_MCP_before_loading_or_searching_full_skill_text" in text or bool(
        re.search(r"(?is)ConPort.+before.+(loading|searching).+full.+skill", text)
    )


def has_token_roi_policy(text: str) -> bool:
    return "quality_adjusted_output_per_token_cost" in text or "quality-adjusted token ROI" in text or "high-quality output per token cost" in text


def has_stable_prefix_guidance(text: str) -> bool:
    return "stable prefix" in text.lower() or "CACHE.001" in text


def likely_renamed_key(missing_key: str, added_keys: set[str]) -> bool:
    normalized_missing = re.sub(r"[^a-z0-9]", "", missing_key.lower())
    for key in added_keys:
        normalized_added = re.sub(r"[^a-z0-9]", "", key.lower())
        if normalized_missing == normalized_added:
            return True
    return False


def has_heading(text: str, heading: str) -> bool:
    pattern = r"(?im)^#{1,6}\s+(.+?)\s*$"
    for match in re.finditer(pattern, text):
        found = match.group(1).strip().lower()
        wanted = heading.lower()
        if found == wanted or wanted in found:
            return True
    return False


def find_skill_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    if root.is_file():
        return [root] if root.name == "SKILL.md" else []
    direct = root / "SKILL.md"
    if direct.exists():
        return [direct]
    return sorted(root.rglob("SKILL.md"))


def referenced_local_files(text: str) -> set[str]:
    refs = set(re.findall(r"`([^`\n]+?\.(?:md|json|jsonl|py|sh|ps1))`", text))
    refs.update(re.findall(r"\(([^)\n]+?\.(?:md|json|jsonl|py|sh|ps1))\)", text))
    return {ref for ref in refs if not re.match(r"^[a-z]+://", ref)}


def validate_file(path: Path, baseline_frontmatter_keys: set[str] | None = None) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)
    errors: list[str] = []
    warnings: list[str] = []

    if not frontmatter:
        errors.append("missing YAML frontmatter")
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if not name:
        errors.append("frontmatter missing name")
    elif name.lower() != name:
        errors.append("frontmatter name must be lowercase")
    if not description:
        errors.append("frontmatter missing description")
    elif len(description) > 900:
        warnings.append("description is excessively large")
    if description:
        if not has_use_boundary(description):
            errors.append("description missing when-to-use guidance")
        if not has_do_not_use_boundary(description):
            errors.append("description missing when-not-to-use guidance")
        if not mentions_input_or_source(description):
            errors.append("description missing expected source/input type")
        if not mentions_output_or_result(description):
            errors.append("description missing expected output/result type")
        if not mentions_behavior_preservation(description):
            errors.append("description missing behavior-preservation requirement")

    disallowed_keys = sorted(key for key in frontmatter if key in DISALLOWED_NEW_FRONTMATTER_KEYS)
    if disallowed_keys:
        errors.append("frontmatter contains unsupported new refactor fields: " + ", ".join(disallowed_keys))
    if baseline_frontmatter_keys is not None:
        current_keys = set(frontmatter)
        missing_keys = sorted(baseline_frontmatter_keys - current_keys)
        added_keys = current_keys - baseline_frontmatter_keys
        if missing_keys:
            errors.append("frontmatter properties deleted from baseline: " + ", ".join(missing_keys))
        renamed_keys = sorted(key for key in missing_keys if likely_renamed_key(key, added_keys))
        if renamed_keys:
            errors.append("frontmatter properties may have been renamed from baseline: " + ", ".join(renamed_keys))

    missing = [section for section in REQUIRED_SECTIONS if not has_heading(text, section)]
    if missing:
        errors.append("missing required sections: " + ", ".join(missing))

    if estimate_tokens(text) > 3000 or len(text.splitlines()) > 500:
        warnings.append("SKILL.md may be a huge knowledge dump")
    if re.search(r"(?i)(raw transcript|assistant:|user:|otel|span_id|trace_id|timestamp=.*level=)", text):
        errors.append("obvious raw transcript/log dump pattern")
    if len(re.findall(r"(?m)^\|.*\|$", text)) > 20:
        warnings.append("possible bulk Markdown table in machine-facing context")
    if re.search(r"(?m)^#{5,6}\s+", text):
        warnings.append("deeply nested heading structure")
    if len(re.findall(r"(?m)^\s*[-*]\s+", text)) > 100:
        warnings.append("excessive repeated bullets")
    if references_contain_hidden_rules(path, text):
        warnings.append("references may contain hard rules not surfaced in SKILL.md")
    if not has_conport_first_policy(text):
        warnings.append("missing ConPort-first retrieval policy")
    if not has_token_roi_policy(text):
        warnings.append("missing token ROI policy")
    if not has_stable_prefix_guidance(text):
        warnings.append("missing stable-prefix/token-cache guidance")

    for ref in referenced_local_files(text):
        target = (path.parent / ref).resolve()
        if not target.exists():
            warnings.append(f"referenced local file missing: {ref}")

    return errors, warnings


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


def references_contain_hidden_rules(path: Path, text: str) -> bool:
    if "References" in text and re.search(r"(?i)\b(MUST|NEVER|SHOULD)\b", text):
        return False
    ref_dir = path.parent / "references"
    if not ref_dir.is_dir():
        return False
    for ref in ref_dir.rglob("*.md"):
        ref_text = ref.read_text(encoding="utf-8")
        if re.search(r"(?i)\b(MUST|NEVER|SHOULD|required|forbidden)\b", ref_text):
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Skill root or single skill directory.")
    parser.add_argument("--baseline-inventory", help="Optional prior inventory JSONL for frontmatter schema comparison.")
    args = parser.parse_args()

    root = Path(args.root)
    skill_files = find_skill_files(root)
    if not root.exists():
        print(f"warning: root does not exist: {root}")
        return 0
    if not skill_files:
        print(f"warning: no SKILL.md files found under {root}")
        return 0

    all_errors: list[str] = []
    all_warnings: list[str] = []
    baselines = load_baseline_frontmatter_keys(Path(args.baseline_inventory) if args.baseline_inventory else None)
    for path in skill_files:
        try:
            relative_path = str(path.relative_to(root))
        except ValueError:
            relative_path = str(path)
        errors, warnings = validate_file(path, baselines.get(relative_path))
        all_errors.extend(f"{path}: {message}" for message in errors)
        all_warnings.extend(f"{path}: {message}" for message in warnings)

    if all_warnings:
        print("Warnings:")
        for warning in all_warnings:
            print(f"- {warning}")
    if all_errors:
        print("Errors:", file=sys.stderr)
        for error in all_errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"validated {len(skill_files)} skill package(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
