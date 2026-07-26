#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
REQUIRED_SECTIONS = ("Outputs", "Evidence", "Success Signals", "Stop Conditions")


def run_git(*args: str, cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout


def parse_semver(value: str) -> tuple[int, int, int]:
    if not SEMVER_RE.fullmatch(value):
        raise ValueError(f"invalid semantic version: {value}")
    core = value.split("-", 1)[0].split("+", 1)[0]
    major, minor, patch = core.split(".")
    return int(major), int(minor), int(patch)


def load_json_at(ref: str, path: str, root: Path) -> dict:
    text = run_git("show", f"{ref}:{path}", cwd=root)
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError(f"{path} at {ref} must be an object")
    return value


def changed_skill_names(base_ref: str, head_ref: str, root: Path) -> set[str]:
    output = run_git("diff", "--name-only", f"{base_ref}...{head_ref}", cwd=root)
    names: set[str] = set()
    for raw in output.splitlines():
        parts = Path(raw.strip()).parts
        if len(parts) >= 3 and parts[0] == "skills":
            names.add(parts[1])
    return names


def section_body(text: str, heading: str) -> str | None:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group("body").strip() if match else None


def catalog_names(root: Path) -> set[str]:
    path = root / "registry/skill-context.catalog.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    names = {
        str(entry.get("name"))
        for entry in value.get("skills", [])
        if isinstance(entry, dict) and entry.get("name")
    }
    extension_dir = root / "registry/skill-context.extensions"
    if extension_dir.exists():
        for extension_path in sorted(extension_dir.glob("*.json")):
            extension = json.loads(extension_path.read_text(encoding="utf-8"))
            names.update(
                str(entry.get("name"))
                for entry in extension.get("skills", [])
                if isinstance(entry, dict) and entry.get("name")
            )
    return names


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate contracts for newly created or modified Skill packages.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--head-ref", default="HEAD")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors: list[str] = []

    try:
        changed = changed_skill_names(args.base_ref, args.head_ref, root)
        if not changed:
            print("no Skill package changes detected")
            return 0

        head_policy = json.loads((root / "registry/capability-context-policy.json").read_text(encoding="utf-8"))
        head_versions = head_policy.get("skill_versions", {})
        try:
            base_policy = load_json_at(args.base_ref, "registry/capability-context-policy.json", root)
            base_versions = base_policy.get("skill_versions", {})
        except RuntimeError:
            base_versions = {}

        registered = catalog_names(root)

        for name in sorted(changed):
            skill_path = root / "skills" / name / "SKILL.md"
            if not skill_path.exists():
                errors.append(f"skills/{name}: changed package has no SKILL.md")
                continue
            if name not in registered:
                errors.append(f"skills/{name}: missing Skill context registry entry")

            version = head_versions.get(name)
            if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
                errors.append(f"skills/{name}: missing or invalid semantic version in capability-context-policy.json")
            else:
                previous = base_versions.get(name)
                if isinstance(previous, str) and SEMVER_RE.fullmatch(previous):
                    if parse_semver(version) <= parse_semver(previous):
                        errors.append(
                            f"skills/{name}: version must increase for package changes ({previous} -> {version})"
                        )

            text = skill_path.read_text(encoding="utf-8")
            for heading in REQUIRED_SECTIONS:
                body = section_body(text, heading)
                if body is None:
                    errors.append(f"skills/{name}/SKILL.md: missing required section '## {heading}'")
                elif not body:
                    errors.append(f"skills/{name}/SKILL.md: section '## {heading}' must be non-empty")

            outputs = section_body(text, "Outputs") or ""
            if not any(token in outputs.lower() for token in ("writeback", "write back", "path", "inline")):
                errors.append(
                    f"skills/{name}/SKILL.md: Outputs must state a writeback path or inline fallback"
                )

            evidence = section_body(text, "Evidence") or ""
            for token in ("fact", "inference", "uncert", "unknown", "assumption"):
                if token not in evidence.lower():
                    errors.append(f"skills/{name}/SKILL.md: Evidence must address {token}")

            success = section_body(text, "Success Signals") or ""
            if not any(token in success.lower() for token in ("met", "not_met", "not met", "not_evaluated", "not evaluated")):
                errors.append(
                    f"skills/{name}/SKILL.md: Success Signals must define explicit evaluated outcomes"
                )

            stop = section_body(text, "Stop Conditions") or ""
            stop_lower = stop.lower()
            for token in ("permission", "evidence"):
                if token not in stop_lower:
                    errors.append(f"skills/{name}/SKILL.md: Stop Conditions must address {token}")
            if not any(token in stop_lower for token in ("risk", "security", "privacy", "compliance", "data-governance", "safety")):
                errors.append(
                    f"skills/{name}/SKILL.md: Stop Conditions must address a risk or safety boundary"
                )
            if not any(token in stop_lower for token in ("goal", "target", "stage")):
                errors.append(
                    f"skills/{name}/SKILL.md: Stop Conditions must address goal, target, or stage completion"
                )

    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        errors.append(str(exc))

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"validated authoring contract for {len(changed)} changed Skill package(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
