#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate changed Skill packages against incremental CI quality contracts."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_skill_package import estimate_tokens, validate_file  # noqa: E402

REPORT_CONTRACT = "lat.skill-ci-contract-report.v1"
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
ARTIFACT_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])(artifacts/[A-Za-z0-9._<>/-]+\.(?:jsonl|json|md))(?![A-Za-z0-9_.-])"
)
ROUTED_SKILL_RE = re.compile(r"(?m)^\s*-\s+[A-Z]\d+\s+`([a-z0-9][a-z0-9-]*)`\s*:")
GENERIC_OUTPUT_NAMES = {
    "output.json",
    "result.json",
    "latest.json",
    "output.md",
    "result.md",
    "latest.md",
}

WARNING_CODES = {
    "description is excessively large": "SKILL.DESCRIPTION.SIZE",
    "SKILL.md may be a huge knowledge dump": "SKILL.CONTEXT.HUGE",
    "possible bulk Markdown table in machine-facing context": "SKILL.CONTEXT.BULK_TABLE",
    "deeply nested heading structure": "SKILL.STRUCTURE.DEEP_HEADINGS",
    "excessive repeated bullets": "SKILL.STRUCTURE.REPEATED_BULLETS",
    "references may contain hard rules not surfaced in SKILL.md": "SKILL.REFERENCE.HIDDEN_RULES",
    "missing ConPort-first retrieval policy": "SKILL.RETRIEVAL.CONPORT_FIRST_MISSING",
    "missing token ROI policy": "SKILL.TOKEN.ROI_MISSING",
    "missing stable-prefix/token-cache guidance": "SKILL.TOKEN.STABLE_PREFIX_MISSING",
}


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    path: str
    message: str


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


def changed_paths(base_ref: str, head_ref: str, root: Path) -> list[str]:
    output = run_git("diff", "--name-only", f"{base_ref}...{head_ref}", cwd=root)
    return sorted({line.strip() for line in output.splitlines() if line.strip()})


def changed_skill_names(paths: Iterable[str]) -> set[str]:
    names: set[str] = set()
    for raw in paths:
        parts = PurePosixPath(raw).parts
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


def warning_code(message: str) -> str:
    if message.startswith("referenced local file missing:"):
        return "SKILL.REFERENCE.LOCAL_FILE_MISSING"
    return WARNING_CODES.get(message, "SKILL.WARNING.UNCLASSIFIED")


def declared_artifact_paths(outputs: str) -> list[str]:
    return sorted(set(ARTIFACT_PATH_RE.findall(outputs)))


def validate_output_contract(skill_name: str, text: str, relative_path: str) -> list[Finding]:
    findings: list[Finding] = []
    outputs = section_body(text, "Outputs") or ""
    paths = declared_artifact_paths(outputs)
    if not paths:
        findings.append(
            Finding(
                "OUTPUT.PATH.MISSING",
                "error",
                relative_path,
                "Outputs must declare at least one governed path under artifacts/.",
            )
        )
        return findings

    expected_run_result = f"artifacts/capability-runs/{skill_name}/<run-id>/run-result.json"
    if expected_run_result not in paths:
        findings.append(
            Finding(
                "OUTPUT.RUN_RESULT.PATH",
                "error",
                relative_path,
                f"Outputs must declare the standard run-result path: {expected_run_result}",
            )
        )

    for value in paths:
        path = PurePosixPath(value)
        if value.startswith("/") or "\\" in value or any(part in {"", ".", ".."} for part in path.parts):
            findings.append(
                Finding("OUTPUT.PATH.UNSAFE", "error", relative_path, f"Unsafe artifact path: {value}")
            )
        if path.parts[0] != "artifacts":
            findings.append(
                Finding(
                    "OUTPUT.PATH.ROOT",
                    "error",
                    relative_path,
                    f"Artifact path must start with artifacts/: {value}",
                )
            )
        if "<run-id>" not in path.parts:
            findings.append(
                Finding(
                    "OUTPUT.PATH.RUN_SCOPE",
                    "error",
                    relative_path,
                    f"Artifact path must be run-scoped: {value}",
                )
            )
        if path.name in GENERIC_OUTPUT_NAMES:
            findings.append(
                Finding(
                    "OUTPUT.PATH.GENERIC_NAME",
                    "error",
                    relative_path,
                    f"Artifact filename is too generic to be a stable contract: {value}",
                )
            )

    if "inline" in outputs.lower() and "write_status=returned_inline" not in outputs:
        findings.append(
            Finding(
                "OUTPUT.INLINE.STATUS",
                "error",
                relative_path,
                "Inline fallback must declare write_status=returned_inline.",
            )
        )
    return findings


def load_policy(root: Path) -> dict[str, str]:
    value = json.loads(
        (root / "registry/capability-context-policy.json").read_text(encoding="utf-8")
    )
    versions = value.get("skill_versions", {})
    if not isinstance(versions, dict):
        raise ValueError(
            "registry/capability-context-policy.json skill_versions must be an object"
        )
    return {str(key): str(version) for key, version in versions.items()}


def load_registry_entries(root: Path) -> tuple[set[str], dict[Path, set[str]]]:
    names: set[str] = set()
    by_extension: dict[Path, set[str]] = {}
    base = json.loads(
        (root / "registry/skill-context.catalog.json").read_text(encoding="utf-8")
    )
    names.update(
        str(entry["name"])
        for entry in base.get("skills", [])
        if isinstance(entry, dict) and entry.get("name")
    )
    extension_dir = root / "registry/skill-context.extensions"
    if extension_dir.exists():
        for path in sorted(extension_dir.glob("*.json")):
            value = json.loads(path.read_text(encoding="utf-8"))
            extension_names = {
                str(entry["name"])
                for entry in value.get("skills", [])
                if isinstance(entry, dict) and entry.get("name")
            }
            names.update(extension_names)
            by_extension[path] = extension_names
    return names, by_extension


def path_exists_at_ref(ref: str, path: str, root: Path) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{ref}:{path}"],
        cwd=root,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def text_at_ref(ref: str, path: str, root: Path) -> str | None:
    if not path_exists_at_ref(ref, path, root):
        return None
    return run_git("show", f"{ref}:{path}", cwd=root)


def validate_registry_alignment(
    root: Path,
    base_ref: str,
    changed: set[str],
    changed_files: set[str],
) -> list[Finding]:
    findings: list[Finding] = []
    versions = load_policy(root)
    registered, extension_entries = load_registry_entries(root)

    for name in sorted(changed):
        skill_path = root / "skills" / name / "SKILL.md"
        relative = f"skills/{name}/SKILL.md"
        if not skill_path.exists():
            findings.append(
                Finding(
                    "REGISTRY.PACKAGE.MISSING",
                    "error",
                    relative,
                    "Changed package has no SKILL.md.",
                )
            )
            continue
        if name not in registered:
            findings.append(
                Finding(
                    "REGISTRY.SKILL.MISSING",
                    "error",
                    relative,
                    "Changed Skill is not registered.",
                )
            )
        version = versions.get(name)
        if version is None or not SEMVER_RE.fullmatch(version):
            findings.append(
                Finding(
                    "REGISTRY.VERSION.MISSING",
                    "error",
                    relative,
                    "Changed Skill has no valid semantic version.",
                )
            )
        elif not path_exists_at_ref(base_ref, relative, root) and version != "1.0.0":
            findings.append(
                Finding(
                    "REGISTRY.VERSION.NEW_SKILL",
                    "error",
                    relative,
                    f"New Skill packages must start at 1.0.0, found {version}.",
                )
            )

        routes = set(ROUTED_SKILL_RE.findall(skill_path.read_text(encoding="utf-8")))
        for route in sorted(routes):
            route_path = root / "skills" / route / "SKILL.md"
            if not route_path.exists():
                findings.append(
                    Finding(
                        "SELECTOR.TARGET.PACKAGE_MISSING",
                        "error",
                        relative,
                        f"Selector target does not exist: {route}",
                    )
                )
            if route not in registered:
                findings.append(
                    Finding(
                        "SELECTOR.TARGET.REGISTRY_MISSING",
                        "error",
                        relative,
                        f"Selector target is not registered: {route}",
                    )
                )
            if route not in versions:
                findings.append(
                    Finding(
                        "SELECTOR.TARGET.VERSION_MISSING",
                        "error",
                        relative,
                        f"Selector target has no version: {route}",
                    )
                )

        matching_extensions = [
            entries for entries in extension_entries.values() if name in entries and routes
        ]
        if matching_extensions and not any(
            entries == routes | {name} for entries in matching_extensions
        ):
            findings.append(
                Finding(
                    "SELECTOR.EXTENSION.MISMATCH",
                    "error",
                    relative,
                    "Selector routes do not match any registry extension containing the selector.",
                )
            )

    for path, entries in extension_entries.items():
        relative = path.relative_to(root).as_posix()
        if relative not in changed_files:
            continue
        for name in sorted(entries):
            if not (root / "skills" / name / "SKILL.md").exists():
                findings.append(
                    Finding(
                        "EXTENSION.PACKAGE.MISSING",
                        "error",
                        relative,
                        f"Extension references missing Skill package: {name}",
                    )
                )
            if name not in versions:
                findings.append(
                    Finding(
                        "EXTENSION.VERSION.MISSING",
                        "error",
                        relative,
                        f"Extension references unversioned Skill: {name}",
                    )
                )
    return findings


def token_delta_findings(
    root: Path,
    base_ref: str,
    skill_name: str,
    text: str,
) -> list[Finding]:
    relative = f"skills/{skill_name}/SKILL.md"
    previous = text_at_ref(base_ref, relative, root)
    current_tokens = estimate_tokens(text)
    findings: list[Finding] = []
    if current_tokens > 2500:
        findings.append(
            Finding(
                "TOKEN.ABSOLUTE.HIGH",
                "warning",
                relative,
                f"Estimated Skill size is {current_tokens} tokens; review progressive disclosure and references.",
            )
        )
    if previous is not None:
        previous_tokens = estimate_tokens(previous)
        growth = current_tokens - previous_tokens
        if previous_tokens > 0 and growth >= 500 and current_tokens / previous_tokens > 1.30:
            findings.append(
                Finding(
                    "TOKEN.DELTA.LARGE",
                    "warning",
                    relative,
                    f"Estimated Skill size increased from {previous_tokens} to {current_tokens} tokens; verify the added context changes user-visible quality.",
                )
            )
    return findings


def write_report(
    path: Path | None,
    base_ref: str,
    head_ref: str,
    changed: set[str],
    findings: list[Finding],
) -> None:
    if path is None:
        return
    payload = {
        "contract": REPORT_CONTRACT,
        "base_ref": base_ref,
        "head_ref": head_ref,
        "changed_skills": sorted(changed),
        "summary": {
            "errors": sum(item.severity == "error" for item in findings),
            "warnings": sum(item.severity == "warning" for item in findings),
        },
        "findings": [asdict(item) for item in findings],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--head-ref", default="HEAD")
    parser.add_argument("--report-out")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    findings: list[Finding] = []
    changed: set[str] = set()
    try:
        paths = changed_paths(args.base_ref, args.head_ref, root)
        changed_files = set(paths)
        changed = changed_skill_names(paths)

        for name in sorted(changed):
            skill_path = root / "skills" / name / "SKILL.md"
            relative = f"skills/{name}/SKILL.md"
            if not skill_path.exists():
                continue
            errors, warnings = validate_file(skill_path)
            findings.extend(
                Finding("SKILL.PACKAGE.INVALID", "error", relative, message)
                for message in errors
            )
            findings.extend(
                Finding(warning_code(message), "error", relative, message)
                for message in warnings
            )
            text = skill_path.read_text(encoding="utf-8")
            findings.extend(validate_output_contract(name, text, relative))
            findings.extend(token_delta_findings(root, args.base_ref, name, text))

        findings.extend(
            validate_registry_alignment(root, args.base_ref, changed, changed_files)
        )
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        findings.append(Finding("CI.CONTRACT.INTERNAL", "error", "repository", str(exc)))

    write_report(
        Path(args.report_out) if args.report_out else None,
        args.base_ref,
        args.head_ref,
        changed,
        findings,
    )

    for finding in findings:
        stream = sys.stderr if finding.severity == "error" else sys.stdout
        print(
            f"{finding.severity}: {finding.code}: {finding.path}: {finding.message}",
            file=stream,
        )

    errors = [finding for finding in findings if finding.severity == "error"]
    if errors:
        return 1
    print(
        f"validated incremental CI contracts for {len(changed)} changed Skill package(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
