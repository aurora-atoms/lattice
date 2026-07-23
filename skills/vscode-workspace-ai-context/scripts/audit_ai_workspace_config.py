#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Audit high-confidence VS Code, Codex, and Claude Code config risks."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

SCHEMA = "lattice.ai_config_audit.v1"
ORDER = {"error": 0, "warning": 1, "info": 2}
CODEX_IGNORED_PROJECT_KEYS = {
    "openai_base_url", "chatgpt_base_url", "apps_mcp_product_sku",
    "model_provider", "model_providers", "notify", "profile", "profiles",
    "experimental_realtime_ws_base_url", "otel",
}
CODEX_EFFORT = {"minimal", "low", "medium", "high", "xhigh"}
CODEX_SANDBOX = {"read-only", "workspace-write", "danger-full-access"}
CLAUDE_EFFORT = {"low", "medium", "high", "xhigh"}
CLAUDE_MODES = {"default", "manual", "acceptEdits", "plan", "auto", "dontAsk", "bypassPermissions"}
SECRET_RE = re.compile(r"(?:api[_-]?key|token|secret|password|credential)", re.I)


@dataclass(frozen=True)
class Finding:
    id: str
    severity: str
    surface: str
    path: str
    message: str
    evidence: str
    recommendation: str
    confidence: str = "high"


def strip_jsonc(text: str) -> str:
    out: list[str] = []
    i = 0
    string = escaped = False
    while i < len(text):
        c, n = text[i], text[i + 1] if i + 1 < len(text) else ""
        if string:
            out.append(c)
            if escaped:
                escaped = False
            elif c == "\\":
                escaped = True
            elif c == '"':
                string = False
            i += 1
        elif c == '"':
            string = True
            out.append(c)
            i += 1
        elif c == "/" and n == "/":
            i += 2
            while i < len(text) and text[i] not in "\r\n":
                i += 1
        elif c == "/" and n == "*":
            i += 2
            while i + 1 < len(text) and text[i:i + 2] != "*/":
                if text[i] in "\r\n":
                    out.append(text[i])
                i += 1
            i += 2
        else:
            out.append(c)
            i += 1
    cleaned = "".join(out)
    previous = None
    while cleaned != previous:
        previous, cleaned = cleaned, re.sub(r",(?=\s*[}\]])", "", cleaned)
    return cleaned


def load_jsonc(path: Path) -> Any:
    return json.loads(strip_jsonc(path.read_text(encoding="utf-8")))


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def enabled_paths(value: Any) -> set[str]:
    return {str(k).rstrip("/") for k, v in value.items() if v is True} if isinstance(value, dict) else set()


def add(findings: list[Finding], id: str, severity: str, surface: str, path: str,
        message: str, evidence: str, recommendation: str, confidence: str = "high") -> None:
    findings.append(Finding(id, severity, surface, path, message, evidence, recommendation, confidence))


def parse_error(findings: list[Finding], surface: str, path: Path, root: Path, exc: Exception) -> None:
    add(findings, "VSAI.SYNTAX.INVALID", "error", surface, rel(path, root),
        "Configuration file cannot be parsed.", str(exc),
        "Fix syntax before applying configuration recommendations.")


def audit_vscode(root: Path, findings: list[Finding]) -> dict[str, Any]:
    sources: list[tuple[Path, dict[str, Any]]] = []
    for path in [root / ".vscode/settings.json", *sorted(root.glob("*.code-workspace"))]:
        if not path.exists():
            continue
        try:
            doc = load_jsonc(path)
            settings = doc.get("settings", {}) if path.suffix == ".code-workspace" else doc
            if not isinstance(settings, dict):
                raise ValueError("settings must be an object")
            sources.append((path, settings))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            parse_error(findings, "vscode", path, root, exc)

    merged: dict[str, Any] = {}
    location_keys = ("chat.instructionsFilesLocations", "chat.agentSkillsLocations",
                     "chat.promptFilesLocations", "chat.agentFilesLocations")
    for path, settings in sources:
        merged.update(settings)
        for key in location_keys:
            for configured in enabled_paths(settings.get(key)):
                if configured.startswith("~") or "*" in configured:
                    continue
                candidate = Path(configured)
                exists = candidate.exists() if candidate.is_absolute() else (
                    (path.parent / candidate).exists() or (root / candidate).exists()
                )
                if not exists:
                    add(findings, "VSAI.PATH.MISSING", "warning", "vscode", rel(path, root),
                        f"Enabled {key} location does not exist.", configured,
                        "Create the directory, correct the path, or disable the location.")

    claude = root / "CLAUDE.md"
    imports_agents = claude.exists() and bool(re.search(r"(?m)(?<!`)@(?:\./)?AGENTS\.md\b", claude.read_text(encoding="utf-8")))
    if (root / "AGENTS.md").exists() and imports_agents and merged.get("chat.useAgentsMdFile", True) is not False and merged.get("chat.useClaudeMdFile", True) is not False:
        add(findings, "VSAI.CONTEXT.DUPLICATE_IMPORT", "warning", "cross-runtime", "CLAUDE.md",
            "VS Code can load AGENTS.md directly while CLAUDE.md imports it again.",
            "AGENTS.md exists; CLAUDE.md imports it; both VS Code loaders are enabled",
            "Keep AGENTS.md as shared source and disable CLAUDE.md loading in VS Code, or remove the import for that path.")

    checks = [
        ("chat.includeReferencedInstructions", True, "VSAI.CONTEXT.REFERENCE_EXPANSION",
         "Referenced instruction files are automatically expanded into context.",
         "Set false unless every linked instruction is intentionally always loaded."),
        ("chat.mcp.discovery.enabled", True, "VSAI.TOOLS.MCP_DISCOVERY",
         "Automatic MCP discovery can expose unrelated tool definitions.",
         "Disable discovery and enable only task-required MCP servers."),
    ]
    for key, bad, id, message, recommendation in checks:
        if merged.get(key) is bad:
            add(findings, id, "warning", "vscode", ".vscode/settings.json", message, f"{key}={str(bad).lower()}", recommendation)

    requests = merged.get("chat.agent.maxRequests")
    if isinstance(requests, int) and requests > 25:
        add(findings, "VSAI.AGENT.REQUEST_BUDGET", "warning", "vscode", ".vscode/settings.json",
            "Agent request budget is unusually high and increases loop cost.", f"chat.agent.maxRequests={requests}",
            "Lower it unless repository eval evidence requires more turns.", "medium")

    if merged.get("chat.useNestedAgentsMdFiles") is True and len(list(root.rglob("AGENTS.md"))) <= 1:
        add(findings, "VSAI.CONTEXT.NESTED_UNUSED", "info", "vscode", ".vscode/settings.json",
            "Nested AGENTS.md discovery is enabled but no nested file was found.", "AGENTS.md count <= 1",
            "Disable the experimental setting until nested instructions are used.", "medium")

    if (root / ".github/copilot-instructions.md").exists() and merged.get("github.copilot.chat.codeGeneration.useInstructionFiles") is False:
        add(findings, "VSAI.CONTEXT.COPILOT_DISABLED", "warning", "vscode", ".vscode/settings.json",
            "A Copilot instruction file exists but loading is disabled.",
            "github.copilot.chat.codeGeneration.useInstructionFiles=false",
            "Enable it or remove the unused file to prevent drift.")

    if (root / "skills").is_dir():
        paths = enabled_paths(merged.get("chat.agentSkillsLocations"))
        if not ({"skills", "./skills"} & paths):
            add(findings, "VSAI.SKILLS.DISCOVERY_GAP", "warning", "vscode", ".vscode/settings.json",
                "Repository skills are outside documented default skill locations.",
                "skills/ exists but chat.agentSkillsLocations does not enable it",
                'Add "chat.agentSkillsLocations": {"skills": true} or move skills to a documented default location.')
    return merged


def audit_codex(root: Path, findings: list[Finding]) -> dict[str, Any] | None:
    path = root / ".codex/config.toml"
    if not path.exists():
        return None
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        parse_error(findings, "codex", path, root, exc)
        return None
    target = rel(path, root)
    for key in sorted(CODEX_IGNORED_PROJECT_KEYS & data.keys()):
        add(findings, "VSAI.CODEX.PROJECT_KEY_IGNORED", "warning", "codex", target,
            "Codex ignores this key in project-local config.", key,
            "Move it to ~/.codex/config.toml or remove it from the project file.")
    sandbox = data.get("sandbox_mode")
    if sandbox is not None and sandbox not in CODEX_SANDBOX:
        add(findings, "VSAI.CODEX.SANDBOX_INVALID", "error", "codex", target,
            "Unsupported sandbox_mode.", str(sandbox), "Use read-only, workspace-write, or danger-full-access after risk review.")
    elif sandbox == "danger-full-access":
        add(findings, "VSAI.CODEX.DANGER_FULL_ACCESS", "error", "codex", target,
            "Project grants unrestricted execution scope.", 'sandbox_mode="danger-full-access"',
            "Use read-only or workspace-write and require explicit escalation.")
    if data.get("approval_policy") == "never" and sandbox != "read-only":
        add(findings, "VSAI.CODEX.NO_APPROVAL", "warning", "codex", target,
            "Codex can execute inside its sandbox without approval.", f"sandbox_mode={sandbox or 'default'}; approval_policy=never",
            "Use on-request for interactive work or document the bounded non-interactive case.", "medium")
    workspace = data.get("sandbox_workspace_write", {})
    if isinstance(workspace, dict) and workspace.get("network_access") is True:
        add(findings, "VSAI.CODEX.NETWORK_ENABLED", "warning", "codex", target,
            "workspace-write permits outbound network access.", "sandbox_workspace_write.network_access=true",
            "Disable by default and enable only for documented external dependencies.")
    effort = data.get("model_reasoning_effort")
    if effort is not None and effort not in CODEX_EFFORT:
        add(findings, "VSAI.CODEX.EFFORT_INVALID", "error", "codex", target,
            "Unsupported model_reasoning_effort.", str(effort), "Use minimal, low, medium, high, or xhigh.")
    elif effort in {"high", "xhigh"}:
        add(findings, "VSAI.CODEX.EFFORT_COST", "info", "codex", target,
            "High reasoning is persisted for routine tasks.", f"model_reasoning_effort={effort}",
            "Keep only when repository evals show a quality gain; otherwise escalate per task.", "medium")
    budget = data.get("project_doc_max_bytes")
    if isinstance(budget, int) and budget > 65536:
        add(findings, "VSAI.CODEX.INSTRUCTION_BUDGET", "warning", "codex", target,
            "Project instruction budget is unusually large.", f"project_doc_max_bytes={budget}",
            "Split by directory and compress always-loaded guidance before raising the cap.", "medium")
    return data


def audit_claude(root: Path, findings: list[Finding]) -> int:
    count = 0
    for path in (root / ".claude/settings.json", root / ".claude/settings.local.json"):
        if not path.exists():
            continue
        count += 1
        try:
            data = load_jsonc(path)
            if not isinstance(data, dict):
                raise ValueError("settings must be an object")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            parse_error(findings, "claude", path, root, exc)
            continue
        target = rel(path, root)
        effort = data.get("effortLevel")
        if effort is not None and effort not in CLAUDE_EFFORT:
            add(findings, "VSAI.CLAUDE.EFFORT_INVALID", "error", "claude", target,
                "Unsupported effortLevel.", str(effort), "Use low, medium, high, or xhigh for supported models.")
        elif effort == "xhigh":
            add(findings, "VSAI.CLAUDE.EFFORT_COST", "info", "claude", target,
                "xhigh is persisted as default effort.", 'effortLevel="xhigh"',
                "Use only when repository evals justify the cost.", "medium")
        permissions = data.get("permissions", {})
        if isinstance(permissions, dict):
            mode = permissions.get("defaultMode")
            if mode is not None and mode not in CLAUDE_MODES:
                add(findings, "VSAI.CLAUDE.MODE_INVALID", "error", "claude", target,
                    "Unsupported permission defaultMode.", str(mode), "Use a documented mode.")
            elif mode == "bypassPermissions":
                add(findings, "VSAI.CLAUDE.BYPASS_PERMISSIONS", "error", "claude", target,
                    "Permission prompts are bypassed.", 'permissions.defaultMode="bypassPermissions"',
                    'Use plan, manual/default, or acceptEdits; set disableBypassPermissionsMode="disable" where required.')
            elif mode == "auto" and path.name == "settings.json":
                add(findings, "VSAI.CLAUDE.AUTO_PROJECT_IGNORED", "warning", "claude", target,
                    "Claude Code ignores auto mode in project settings.", 'permissions.defaultMode="auto"',
                    "Set auto only in user settings, or use a project-safe mode.")
            allow = permissions.get("allow", [])
            broad = sorted({str(x) for x in allow if str(x) in {"Bash", "Read", "Edit", "Write"}}) if isinstance(allow, list) else []
            if broad:
                add(findings, "VSAI.CLAUDE.BROAD_ALLOW", "warning", "claude", target,
                    "Allowlist contains unrestricted tool rules.", ", ".join(broad),
                    "Replace them with command-, path-, or tool-specific rules and secret denies.")
        env = data.get("env", {})
        exposed = sorted(str(k) for k, v in env.items() if SECRET_RE.search(str(k)) and v not in (None, "")) if isinstance(env, dict) else []
        if exposed:
            add(findings, "VSAI.CLAUDE.SECRET_LITERAL", "error", "claude", target,
                "Project settings contain literal secret-like values.", ", ".join(exposed),
                "Remove secrets and use managed or local environment injection.")
    return count


def audit(root: Path) -> dict[str, Any]:
    findings: list[Finding] = []
    vscode = audit_vscode(root, findings)
    codex = audit_codex(root, findings)
    claude_count = audit_claude(root, findings)
    for path in (root / "AGENTS.md", root / "CLAUDE.md", root / ".github/copilot-instructions.md"):
        if path.exists() and path.stat().st_size > 32768:
            add(findings, "VSAI.CONTEXT.FILE_SIZE", "warning", "instructions", rel(path, root),
                "Always-on instruction file exceeds 32 KiB.", f"size_bytes={path.stat().st_size}",
                "Move workflows and long references into routed files or skills.", "medium")
    findings.sort(key=lambda f: (ORDER[f.severity], f.id, f.path))
    summary = {s: sum(f.severity == s for f in findings) for s in ORDER}
    return {
        "schema": SCHEMA, "root": str(root.resolve()), "summary": summary,
        "surfaces": {
            "vscode_settings_found": bool(vscode), "codex_project_config_found": codex is not None,
            "claude_project_configs_found": claude_count, "agents_md_found": (root / "AGENTS.md").exists(),
            "claude_md_found": (root / "CLAUDE.md").exists(),
        },
        "findings": [asdict(f) for f in findings],
    }


def markdown(result: dict[str, Any]) -> str:
    s = result["summary"]
    lines = ["# AI Configuration Audit", "", f"Schema: `{result['schema']}`", f"Root: `{result['root']}`", "",
             f"Errors: {s['error']} · Warnings: {s['warning']} · Info: {s['info']}", ""]
    if not result["findings"]:
        return "\n".join(lines + ["No high-confidence configuration findings.", ""])
    for f in result["findings"]:
        lines += [f"## {f['severity'].upper()} · {f['id']}", "", f"- Surface: `{f['surface']}`",
                  f"- Path: `{f['path']}`", f"- Problem: {f['message']}", f"- Evidence: {f['evidence']}",
                  f"- Recommendation: {f['recommendation']}", f"- Confidence: `{f['confidence']}`", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--strict", action="store_true", help="Exit nonzero when error findings exist.")
    args = parser.parse_args()
    root = Path(args.root)
    if not root.is_dir():
        print(f"error: root is not a directory: {root}", file=sys.stderr)
        return 2
    result = audit(root)
    print(json.dumps(result, indent=2, sort_keys=True) if args.format == "json" else markdown(result), end="\n")
    return 1 if args.strict and result["summary"]["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
