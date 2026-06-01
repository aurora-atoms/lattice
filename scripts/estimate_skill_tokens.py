#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Estimate token usage for skill packages."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def estimate_tokens(text: str) -> int:
    return max(1, (len(text) + 3) // 4) if text else 0


def find_skill_dirs(root: Path) -> list[Path]:
    if not root.exists():
        return []
    if (root / "SKILL.md").exists():
        return [root]
    return sorted(path.parent for path in root.rglob("SKILL.md"))


def file_tokens(path: Path) -> int:
    try:
        return estimate_tokens(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        return estimate_tokens(path.read_text(encoding="utf-8", errors="replace"))


def package_record(skill_dir: Path) -> dict[str, object]:
    files = [path for path in skill_dir.rglob("*") if path.is_file()]
    skill_md = skill_dir / "SKILL.md"
    reference_files = [
        path for path in (skill_dir / "references").rglob("*")
        if path.is_file()
    ] if (skill_dir / "references").is_dir() else []
    script_files = [
        path for path in (skill_dir / "scripts").rglob("*")
        if path.is_file()
    ] if (skill_dir / "scripts").is_dir() else []
    skill_tokens = file_tokens(skill_md) if skill_md.exists() else 0
    reference_tokens = sum(file_tokens(path) for path in reference_files)
    return {
        "path": str(skill_dir),
        "estimated_tokens": sum(file_tokens(path) for path in files),
        "file_count": len(files),
        "skill_md_tokens": skill_tokens,
        "reference_tokens": reference_tokens,
        "script_count": len(script_files),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Skill root or single skill directory.")
    args = parser.parse_args()

    records = [package_record(path) for path in find_skill_dirs(Path(args.root))]
    for record in records:
        print(json.dumps(record, sort_keys=True))
    if not records:
        print("warning: no SKILL.md files found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
