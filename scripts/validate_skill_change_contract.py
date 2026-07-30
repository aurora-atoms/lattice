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
DIRECTION_PRIMARY_VALUES = {
    "current_product_delivery",
    "strategic_asset",
    "team_reuse",
}
DIRECTION_VERDICTS = {
    "proceed",
    "bind_to_delivery",
    "retain_candidate",
    "stop",
}
DIRECTION_COMMON_FIELDS = (
    "primary_value_path",
    "direction_verdict",
    "evidence_refs",
    "existing_capability_gap",
)
DIRECTION_PATH_FIELDS = {
    "current_product_delivery": ("user_outcome",),
    "strategic_asset": (
        "proprietary_input",
        "verifiable_artifact",
        "second_use",
        "maintenance_owner",
    ),
    "team_reuse": ("second_use_evidence", "adoption_owner"),
}
PLACEHOLDER_VALUES = {"", "none", "n/a", "na", "tbd", "todo", "unknown"}


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


def path_exists_at(ref: str, path: str, root: Path) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{ref}:{path}"],
        cwd=root,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


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


def direction_fields(text: str) -> dict[str, str]:
    body = section_body(text, "Direction Fit")
    if body is None:
        return {}
    fields: dict[str, str] = {}
    for line in body.splitlines():
        match = re.match(r"^([a-z][a-z0-9_]*):\s*(.*?)\s*$", line.strip())
        if match:
            fields[match.group(1)] = match.group(2)
    return fields


def is_placeholder(value: str) -> bool:
    normalized = value.strip().lower()
    return (
        normalized in PLACEHOLDER_VALUES
        or "<" in value
        or ">" in value
        or " | " in value
    )


def validate_direction_fit(text: str) -> list[str]:
    errors: list[str] = []
    body = section_body(text, "Direction Fit")
    if body is None:
        return ["missing required section '## Direction Fit' for new Skill package"]
    if not body:
        return ["section '## Direction Fit' must be non-empty"]

    fields = direction_fields(text)
    for field in DIRECTION_COMMON_FIELDS:
        value = fields.get(field)
        if value is None:
            errors.append(f"Direction Fit missing field '{field}'")
        elif is_placeholder(value):
            errors.append(f"Direction Fit field '{field}' contains a placeholder")

    primary = fields.get("primary_value_path")
    if primary and primary not in DIRECTION_PRIMARY_VALUES:
        errors.append(
            "Direction Fit primary_value_path must be one of "
            + ", ".join(sorted(DIRECTION_PRIMARY_VALUES))
        )

    verdict = fields.get("direction_verdict")
    if verdict and verdict not in DIRECTION_VERDICTS:
        errors.append(
            "Direction Fit direction_verdict must be one of "
            + ", ".join(sorted(DIRECTION_VERDICTS))
        )
    elif verdict and verdict != "proceed":
        errors.append(
            "new Skill package requires direction_verdict 'proceed'; "
            "bind_to_delivery, retain_candidate, and stop decisions must remain outside skills/"
        )

    if primary in DIRECTION_PATH_FIELDS:
        for field in DIRECTION_PATH_FIELDS[primary]:
            value = fields.get(field)
            if value is None:
                errors.append(
                    f"Direction Fit for {primary} missing field '{field}'"
                )
            elif is_placeholder(value):
                errors.append(
                    f"Direction Fit field '{field}' contains a placeholder"
                )

    return errors


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
            is_new_skill = not path_exists_at(
                args.base_ref,
                f"skills/{name}/SKILL.md",
                root,
            )
            if is_new_skill:
                for error in validate_direction_fit(text):
                    errors.append(f"skills/{name}/SKILL.md: {error}")

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