#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Audit high-confidence VS Code, Codex, and Claude Code configuration risks."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

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
ABSOLUTE_USER_PATH_RE = re.compile(r"(?:/Users/[^/\s]+|/home/[^/\s]+|[A-Za-z]:\\Users\\[^\\\s]+)")
VOLATILE_DATE_RE = re.compile(r"\b20\d{2}-\d{2}-\d{2}(?:[T ][0-2]\d:[0-5]\d(?::[0-5]\d)?)?\b")
IMPORT_RE = re.compile(r"(?m)(?<!`)@([^\s`]+)")


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


def normalized_instruction_lines(path: Path) -> set[str]:
    if not path.exists():
        return set()
    result: set[str] = set()
    in_fence = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not line or line.startswith("#") or line.startswith("---"):
            continue
        line = re.sub(r"^[-*+]\s+", "", line)
        line = re.sub(r"\s+", " ", line).lower()
        if len(line) >= 18:
            result.add(line)
    return result


def instruction_overlap(a: Path, b: Path) -> tuple[float, int]:
    left, right = normalized_instruction_lines(a), normalized_instruction_lines(b)
    if min(len(left), len(right)) < 4:
        return 0.0, 0
    shared = left & right
    return len(shared) / min(len(left), len(right)), len(shared)


def count_mcp_servers(data: Any) -> int:
    if not isinstance(data, dict):
        return 0
    for key in ("servers", "mcpServers", "mcp_servers"):
        value = data.get(key)
        if isinstance(value, dict):
            return len(value)
    return 0


def iter_hook_files(root: Path, configured: Iterable[str]) -> Iterable[Path]:
    seen: set[Path] = set()
    candidates = [root / ".github/hooks"]
    for item in configured:
        if item.startswith("~") or "*" in item:
            continue
        path = Path(item)
        candidates.append(path if path.is_absolute() else root / path)
    for path in candidates:
        files = sorted(path.glob("*.json")) if path.is_dir() else [path]
        for file in files:
            if file.exists() and file not in seen:
                seen.add(file)
                yield file


def has_precompact_hook(root: Path, settings: dict[str, Any]) -> bool:
    configured = enabled_paths(settings.get("chat.hookFilesLocations"))
    for path in iter_hook_files(root, configured):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if re.search(r'"PreCompact"\s*:', text) or re.search(r'"event"\s*:\s*"PreCompact"', text):
            return True
    return False


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
    location_keys = (
        "chat.instructionsFilesLocations", "chat.agentSkillsLocations",
        "chat.promptFilesLocations", "chat.agentFilesLocations", "chat.hookFilesLocations",
    )
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
        ("github.copilot.chat.editor.temporalContext.enabled", True, "VSAI.CACHE.TEMPORAL_CONTEXT",
         "Recently viewed and edited files are injected as volatile inline-chat context.",
         "Disable for cache-sensitive or reproducible workflows; attach relevant files explicitly."),
        ("chat.useCustomizationsInParentRepositories", True, "VSAI.CACHE.PARENT_CUSTOMIZATIONS",
         "Parent-repository customizations can change the prompt prefix when the opened folder changes.",
         "Enable only for an intentional monorepo policy and verify loaded customizations in Agent Debug Logs."),
    ]
    for key, bad, id, message, recommendation in checks:
        if merged.get(key) is bad:
            add(findings, id, "warning", "vscode", ".vscode/settings.json", message,
                f"{key}={str(bad).lower()}", recommendation)

    if merged.get("github.copilot.chat.summarizeAgentConversationHistory.enabled") is False:
        add(findings, "VSAI.COMPACT.AUTO_DISABLED", "warning", "vscode", ".vscode/settings.json",
            "Automatic conversation compaction is disabled.",
            "github.copilot.chat.summarizeAgentConversationHistory.enabled=false",
            "Enable automatic compaction unless a tested external checkpoint and manual compaction workflow replaces it.")

    if merged and merged.get("chat.tools.compressOutput.enabled") is not True:
        add(findings, "VSAI.COMPACT.TOOL_OUTPUT", "info", "vscode", ".vscode/settings.json",
            "Large tool output compression is not enabled.",
            f"chat.tools.compressOutput.enabled={merged.get('chat.tools.compressOutput.enabled', 'unset')}",
            "Consider enabling the Preview setting after validating that compressed terminal and diff output preserves required evidence.",
            "medium")

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

    if merged.get("github.copilot.chat.organizationInstructions.enabled") is True:
        add(findings, "VSAI.CACHE.ORG_PREFIX", "info", "vscode", ".vscode/settings.json",
            "Organization instructions may add an external always-on prompt prefix.",
            "github.copilot.chat.organizationInstructions.enabled=true",
            "Keep them enabled when required, but inspect effective instructions and cache divergence in Agent Debug Logs.",
            "medium")

    precompact = has_precompact_hook(root, merged)
    if requests and isinstance(requests, int) and requests > 15 and not precompact:
        add(findings, "VSAI.COMPACT.CHECKPOINT_GAP", "info", "vscode", ".vscode/settings.json",
            "Long agent loops have no detected PreCompact checkpoint hook.",
            f"chat.agent.maxRequests={requests}; PreCompact hook not found",
            "For long-horizon work, add a bounded PreCompact hook or require a PRE_COMPACT_CHECKPOINT_V1 artifact before compaction.",
            "medium")
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
    if isinstance(budget, int) and budget > 32768:
        add(findings, "VSAI.CODEX.INSTRUCTION_BUDGET", "warning", "codex", target,
            "Project instruction budget exceeds the documented default.", f"project_doc_max_bytes={budget}",
            "Use AGENTS.md as a short map and route deeper knowledge through repository documents and skills.", "medium")
    if data.get("model"):
        add(findings, "VSAI.CODEX.PROJECT_MODEL_PIN", "info", "codex", target,
            "The shared project configuration pins a Codex model.", f"model={data.get('model')}",
            "Keep a project model pin only when team access and frozen repository evals justify it; otherwise prefer user or task selection.",
            "medium")
    agents = data.get("agents", {})
    if isinstance(agents, dict):
        threads = agents.get("max_concurrent_threads_per_session")
        if isinstance(threads, int) and threads > 4:
            add(findings, "VSAI.CODEX.SUBAGENT_FANOUT", "warning", "codex", target,
                "Codex subagent concurrency can multiply independent context and tool cost.",
                f"agents.max_concurrent_threads_per_session={threads}",
                "Limit concurrency to independently useful workstreams and measure total cost, not only wall-clock time.",
                "medium")
    mcp_count = count_mcp_servers(data)
    if mcp_count > 8:
        add(findings, "VSAI.CODEX.MCP_SPRAWL", "warning", "codex", target,
            "Many Codex MCP servers are enabled in one project profile.", f"mcp_server_count={mcp_count}",
            "Split MCP exposure into task profiles and keep the active tool prefix stable within each session.", "medium")
    return data


def audit_claude(root: Path, findings: list[Finding]) -> tuple[int, bool]:
    count = 0
    precompact = False
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
        if data.get("model"):
            add(findings, "VSAI.CLAUDE.PROJECT_MODEL_PIN", "info", "claude", target,
                "The shared project settings pin a Claude model.", f"model={data.get('model')}",
                "Keep a project pin only when provider mapping, team entitlement, and repository evals are controlled.", "medium")
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
        hooks = data.get("hooks", {})
        if isinstance(hooks, dict) and "PreCompact" in hooks:
            precompact = True
        enabled = data.get("enabledMcpjsonServers")
        if isinstance(enabled, list) and len(enabled) > 8:
            add(findings, "VSAI.CLAUDE.MCP_SPRAWL", "warning", "claude", target,
                "Many project MCP servers are enabled for Claude Code.", f"enabledMcpjsonServers={len(enabled)}",
                "Create task-specific MCP profiles and disable unrelated servers before starting a session.", "medium")
    return count, precompact


def audit_mcp_files(root: Path, findings: list[Finding]) -> int:
    total = 0
    for path in (root / ".mcp.json", root / ".vscode/mcp.json"):
        if not path.exists():
            continue
        try:
            data = load_jsonc(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            parse_error(findings, "mcp", path, root, exc)
            continue
        count = count_mcp_servers(data)
        total += count
        if count > 8:
            add(findings, "VSAI.TOOLS.MCP_FILE_SPRAWL", "warning", "mcp", rel(path, root),
                "The project MCP file exposes many servers in one profile.", f"mcp_server_count={count}",
                "Split by task and enable only servers required for the current workflow.", "medium")
    return total


def audit_instruction_files(root: Path, findings: list[Finding]) -> int:
    paths = [root / "AGENTS.md", root / "CLAUDE.md", root / ".github/copilot-instructions.md"]
    existing = [path for path in paths if path.exists()]
    for path in existing:
        text = path.read_text(encoding="utf-8")
        size = path.stat().st_size
        if size > 32768:
            add(findings, "VSAI.CONTEXT.FILE_SIZE", "warning", "instructions", rel(path, root),
                "Always-on instruction file exceeds 32 KiB.", f"size_bytes={size}",
                "Move workflows and long references into routed files or skills.", "medium")
        match = ABSOLUTE_USER_PATH_RE.search(text)
        if match:
            add(findings, "VSAI.CACHE.MACHINE_PATH", "warning", "instructions", rel(path, root),
                "Always-on instructions contain a machine-specific user path.", match.group(0),
                "Move machine-local paths to user configuration or a late-bound task context.", "medium")
        date_match = VOLATILE_DATE_RE.search(text)
        if date_match and size > 2048:
            add(findings, "VSAI.CACHE.VOLATILE_DATE", "info", "instructions", rel(path, root),
                "Always-on instructions contain a dated value that can churn the stable prompt prefix.", date_match.group(0),
                "Keep fast-changing dates and status in task artifacts or dynamic context, not the stable kernel.", "medium")
        if path.name == "CLAUDE.md":
            for imported in IMPORT_RE.findall(text):
                if imported.startswith("~") or "://" in imported:
                    continue
                target = (path.parent / imported).resolve()
                if target.exists() and target.is_file() and target.stat().st_size > 16384:
                    add(findings, "VSAI.CLAUDE.LARGE_IMPORT", "warning", "claude", rel(path, root),
                        "CLAUDE.md imports a large file into the session prefix.",
                        f"{imported}: size_bytes={target.stat().st_size}",
                        "Import a short index and let Claude retrieve the detailed reference only when needed.", "medium")

    for index, left in enumerate(existing):
        for right in existing[index + 1:]:
            overlap, shared = instruction_overlap(left, right)
            if overlap >= 0.70:
                add(findings, "VSAI.CONTEXT.DUPLICATE_CONTENT", "warning", "cross-runtime",
                    f"{rel(left, root)} + {rel(right, root)}",
                    "Always-on instruction files substantially duplicate the same rule text.",
                    f"overlap={overlap:.0%}; shared_lines={shared}",
                    "Keep one canonical shared rule source and make each runtime adapter contain only deltas.",
                    "medium")
    return len(existing)


def audit(root: Path) -> dict[str, Any]:
    findings: list[Finding] = []
    vscode = audit_vscode(root, findings)
    codex = audit_codex(root, findings)
    claude_count, claude_precompact = audit_claude(root, findings)
    mcp_count = audit_mcp_files(root, findings)
    instruction_count = audit_instruction_files(root, findings)
    findings.sort(key=lambda f: (ORDER[f.severity], f.id, f.path))
    summary = {s: sum(f.severity == s for f in findings) for s in ORDER}
    return {
        "schema": SCHEMA,
        "root": str(root.resolve()),
        "summary": summary,
        "surfaces": {
            "vscode_settings_found": bool(vscode),
            "codex_project_config_found": codex is not None,
            "claude_project_configs_found": claude_count,
            "instruction_files_found": instruction_count,
            "mcp_servers_found": mcp_count,
            "vscode_precompact_hook_found": has_precompact_hook(root, vscode),
            "claude_precompact_hook_found": claude_precompact,
            "agents_md_found": (root / "AGENTS.md").exists(),
            "claude_md_found": (root / "CLAUDE.md").exists(),
        },
        "findings": [asdict(f) for f in findings],
    }


def markdown(result: dict[str, Any]) -> str:
    s = result["summary"]
    lines = [
        "# AI Configuration Audit", "", f"Schema: `{result['schema']}`",
        f"Root: `{result['root']}`", "",
        f"Errors: {s['error']} · Warnings: {s['warning']} · Info: {s['info']}", "",
    ]
    if not result["findings"]:
        return "\n".join(lines + ["No high-confidence configuration findings.", ""])
    for f in result["findings"]:
        lines += [
            f"## {f['severity'].upper()} · {f['id']}", "",
            f"- Surface: `{f['surface']}`", f"- Path: `{f['path']}`",
            f"- Problem: {f['message']}", f"- Evidence: {f['evidence']}",
            f"- Recommendation: {f['recommendation']}", f"- Confidence: `{f['confidence']}`", "",
        ]
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
