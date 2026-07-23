#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Augment the cross-runtime audit with VS Code native-first policy checks."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

CORE_PATH = Path(__file__).with_name("audit_ai_workspace_config.py")
SPEC = importlib.util.spec_from_file_location("audit_ai_workspace_config_core", CORE_PATH)
CORE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = CORE
SPEC.loader.exec_module(CORE)

NATIVE_DEFAULTS: dict[str, Any] = {
    "chat.agent.enabled": True,
    "chat.agent.maxRequests": 25,
    "chat.mcp.discovery.enabled": False,
    "chat.permissions.default": "default",
    "chat.tools.global.autoApprove": False,
    "chat.tools.terminal.ignoreDefaultAutoApproveRules": False,
    "github.copilot.chat.summarizeAgentConversationHistory.enabled": True,
    "chat.includeApplyingInstructions": True,
    "chat.includeReferencedInstructions": False,
    "github.copilot.chat.codeGeneration.useInstructionFiles": True,
    "chat.useAgentSkills": True,
    "chat.useCustomizationsInParentRepositories": False,
    "chat.viewSessions.enabled": True,
    "chat.viewSessions.orientation": "sideBySide",
    "chat.plugins.enabled": False,
}

NON_STABLE_SETTINGS = {
    "chat.tools.compressOutput.enabled": "Preview",
    "chat.permissions.default": "Experimental",
    "chat.autopilot.advanced.enabled": "Experimental",
    "github.copilot.chat.summarizeAgentConversationHistory.enabled": "Experimental",
    "github.copilot.chat.virtualTools.threshold": "Experimental",
    "chat.useNestedAgentsMdFiles": "Experimental",
    "chat.agentsControl.enabled": "Experimental",
    "chat.unifiedAgentsBar.enabled": "Experimental",
    "chat.plugins.marketplaces": "Experimental",
    "chat.plugins.strictMarketplaces": "Experimental",
    "chat.pluginLocations": "Experimental",
    "chat.agentHost.byokModels.enabled": "Experimental",
    "chat.agents.claude.preferAgentHost": "Experimental",
}

EXTENSION_PREFIXES = {
    "claudeCode.": "Claude Code extension",
}


def finding(id: str, severity: str, path: str, message: str, evidence: str,
            recommendation: str, confidence: str = "medium") -> dict[str, str]:
    return {
        "id": id,
        "severity": severity,
        "surface": "vscode-native",
        "path": path,
        "message": message,
        "evidence": evidence,
        "recommendation": recommendation,
        "confidence": confidence,
    }


def settings_sources(root: Path) -> list[tuple[Path, dict[str, Any]]]:
    sources: list[tuple[Path, dict[str, Any]]] = []
    for path in [root / ".vscode/settings.json", *sorted(root.glob("*.code-workspace"))]:
        if not path.exists():
            continue
        try:
            document = CORE.load_jsonc(path)
            settings = document.get("settings", {}) if path.suffix == ".code-workspace" else document
            if isinstance(settings, dict):
                sources.append((path, settings))
        except Exception:
            # The core auditor emits the syntax finding.
            continue
    return sources


def native_findings(root: Path) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    for path, settings in settings_sources(root):
        target = CORE.rel(path, root)
        for key, default in NATIVE_DEFAULTS.items():
            if key in settings and settings[key] == default:
                results.append(finding(
                    "VSAI.NATIVE.REDUNDANT_DEFAULT", "info", target,
                    "Workspace setting repeats the documented VS Code default.",
                    f"{key}={json.dumps(default)}",
                    "Remove it unless the repository intentionally enforces the value as team policy.",
                ))
        for key, lifecycle in NON_STABLE_SETTINGS.items():
            if key in settings:
                results.append(finding(
                    "VSAI.NATIVE.NON_STABLE_SETTING", "info", target,
                    f"Workspace uses a {lifecycle} VS Code setting.",
                    f"{key}={json.dumps(settings[key])}",
                    "Record an owner, verification date, measured benefit, rollback path, and stabilization review.",
                ))
        for prefix, owner in EXTENSION_PREFIXES.items():
            keys = sorted(key for key in settings if key.startswith(prefix))
            if keys:
                results.append(finding(
                    "VSAI.NATIVE.EXTENSION_OVERLAP_REVIEW", "info", target,
                    f"Workspace contains settings for the {owner}.", ", ".join(keys),
                    "Compare the requirement with native Claude or Codex sessions, Agent Host, worktrees, permissions, hooks, and session management; retain the extension only for a documented gap.",
                ))
        if settings.get("chat.tools.global.autoApprove") is True or settings.get("chat.permissions.default") in {"autoApprove", "autopilot"}:
            results.append(finding(
                "VSAI.NATIVE.BROAD_AUTONOMY", "error", target,
                "Workspace enables broad native agent autonomy.",
                f"global={settings.get('chat.tools.global.autoApprove')}; permission={settings.get('chat.permissions.default')}",
                "Use Default Approvals and scoped terminal, URL, edit, and sandbox rules unless an isolated environment is proven.",
                "high",
            ))
        if settings.get("github.copilot.chat.claudeAgent.allowDangerouslySkipPermissions") is True:
            results.append(finding(
                "VSAI.NATIVE.CLAUDE_PERMISSION_BYPASS", "error", target,
                "Native Claude agent permission checks are bypassed.",
                "github.copilot.chat.claudeAgent.allowDangerouslySkipPermissions=true",
                "Disable it except in an isolated disposable sandbox.",
                "high",
            ))
        if settings.get("extensions.supportAgentsWindow"):
            results.append(finding(
                "VSAI.NATIVE.AGENTS_WINDOW_EXTENSION", "info", target,
                "Extensions are explicitly enabled inside the native Agents Window.",
                f"extensions.supportAgentsWindow={json.dumps(settings['extensions.supportAgentsWindow'], sort_keys=True)}",
                "Enable only extensions required by the agent-first workflow and review their permissions and tool contributions.",
            ))
    return results


def audit(root: Path) -> dict[str, Any]:
    result = CORE.audit(root)
    combined = list(result["findings"]) + native_findings(root)
    order = {"error": 0, "warning": 1, "info": 2}
    combined.sort(key=lambda item: (order[item["severity"]], item["id"], item["path"], item["evidence"]))
    result["findings"] = combined
    result["summary"] = {
        severity: sum(item["severity"] == severity for item in combined)
        for severity in order
    }
    result["surfaces"]["native_policy_audit"] = True
    return result


def markdown(result: dict[str, Any]) -> str:
    summary = result["summary"]
    lines = [
        "# Native-First AI Configuration Audit", "",
        f"Schema: `{result['schema']}`", f"Root: `{result['root']}`", "",
        f"Errors: {summary['error']} | Warnings: {summary['warning']} | Info: {summary['info']}", "",
    ]
    if not result["findings"]:
        return "\n".join(lines + ["No high-confidence configuration findings.", ""])
    for item in result["findings"]:
        lines.extend([
            f"## {item['severity'].upper()} | {item['id']}", "",
            f"- Surface: `{item['surface']}`", f"- Path: `{item['path']}`",
            f"- Problem: {item['message']}", f"- Evidence: {item['evidence']}",
            f"- Recommendation: {item['recommendation']}",
            f"- Confidence: `{item['confidence']}`", "",
        ])
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
