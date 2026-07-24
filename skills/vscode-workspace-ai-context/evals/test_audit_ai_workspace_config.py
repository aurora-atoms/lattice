#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "audit_ai_workspace_config.py"
SPEC = importlib.util.spec_from_file_location("audit_ai_workspace_config", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class AuditWorkspaceConfigTests(unittest.TestCase):
    def finding_ids(self, root: Path) -> set[str]:
        return {item["id"] for item in MODULE.audit(root)["findings"]}

    def test_detects_duplicate_instruction_import_and_skill_discovery_gap(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".vscode").mkdir()
            (root / "skills" / "sample").mkdir(parents=True)
            (root / "AGENTS.md").write_text("# Shared\n", encoding="utf-8")
            (root / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
            (root / ".vscode" / "settings.json").write_text(
                '{"chat.useAgentsMdFile": true, "chat.useClaudeMdFile": true}', encoding="utf-8"
            )
            ids = self.finding_ids(root)
            self.assertIn("VSAI.CONTEXT.DUPLICATE_IMPORT", ids)
            self.assertIn("VSAI.SKILLS.DISCOVERY_GAP", ids)

    def test_detects_dangerous_codex_and_claude_permissions(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".codex").mkdir()
            (root / ".claude").mkdir()
            (root / ".codex" / "config.toml").write_text(
                'sandbox_mode = "danger-full-access"\napproval_policy = "never"\n'
                '[sandbox_workspace_write]\nnetwork_access = true\n',
                encoding="utf-8",
            )
            (root / ".claude" / "settings.json").write_text(
                json.dumps(
                    {
                        "permissions": {"defaultMode": "bypassPermissions", "allow": ["Bash"]},
                        "env": {"ANTHROPIC_API_KEY": "literal-secret"},
                    }
                ),
                encoding="utf-8",
            )
            ids = self.finding_ids(root)
            self.assertIn("VSAI.CODEX.DANGER_FULL_ACCESS", ids)
            self.assertIn("VSAI.CLAUDE.BYPASS_PERMISSIONS", ids)
            self.assertIn("VSAI.CLAUDE.BROAD_ALLOW", ids)
            self.assertIn("VSAI.CLAUDE.SECRET_LITERAL", ids)

    def test_detects_compaction_and_cache_instability(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".vscode").mkdir()
            (root / "AGENTS.md").write_text(
                "# Rules\nUse /Users/alice/project and refresh this status on 2026-07-23.\n" * 40,
                encoding="utf-8",
            )
            (root / ".vscode" / "settings.json").write_text(
                json.dumps(
                    {
                        "github.copilot.chat.summarizeAgentConversationHistory.enabled": False,
                        "chat.tools.compressOutput.enabled": False,
                        "github.copilot.chat.editor.temporalContext.enabled": True,
                        "chat.useCustomizationsInParentRepositories": True,
                        "chat.agent.maxRequests": 30,
                    }
                ),
                encoding="utf-8",
            )
            ids = self.finding_ids(root)
            self.assertIn("VSAI.COMPACT.AUTO_DISABLED", ids)
            self.assertIn("VSAI.COMPACT.TOOL_OUTPUT", ids)
            self.assertIn("VSAI.CACHE.TEMPORAL_CONTEXT", ids)
            self.assertIn("VSAI.CACHE.PARENT_CUSTOMIZATIONS", ids)
            self.assertIn("VSAI.COMPACT.CHECKPOINT_GAP", ids)
            self.assertIn("VSAI.CACHE.MACHINE_PATH", ids)
            self.assertIn("VSAI.CACHE.VOLATILE_DATE", ids)

    def test_detects_model_pins_mcp_sprawl_and_subagent_fanout(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".codex").mkdir()
            (root / ".claude").mkdir()
            mcp_entries = "\n".join(f'[mcp_servers.server{i}]\ncommand = "tool{i}"' for i in range(9))
            (root / ".codex" / "config.toml").write_text(
                'model = "example-model"\nsandbox_mode = "workspace-write"\n'
                '[agents]\nmax_concurrent_threads_per_session = 8\n' + mcp_entries + "\n",
                encoding="utf-8",
            )
            (root / ".claude" / "settings.json").write_text(
                json.dumps({"model": "example-claude", "enabledMcpjsonServers": [f"s{i}" for i in range(9)]}),
                encoding="utf-8",
            )
            (root / ".mcp.json").write_text(
                json.dumps({"mcpServers": {f"s{i}": {"command": "x"} for i in range(9)}}),
                encoding="utf-8",
            )
            ids = self.finding_ids(root)
            self.assertIn("VSAI.CODEX.PROJECT_MODEL_PIN", ids)
            self.assertIn("VSAI.CODEX.SUBAGENT_FANOUT", ids)
            self.assertIn("VSAI.CODEX.MCP_SPRAWL", ids)
            self.assertIn("VSAI.CLAUDE.PROJECT_MODEL_PIN", ids)
            self.assertIn("VSAI.CLAUDE.MCP_SPRAWL", ids)
            self.assertIn("VSAI.TOOLS.MCP_FILE_SPRAWL", ids)

    def test_detects_substantially_duplicated_runtime_adapters(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shared = "\n".join(
                [
                    "- Inspect the smallest relevant file set before editing.",
                    "- Preserve public APIs unless explicitly asked to change them.",
                    "- Run the narrowest relevant validation command first.",
                    "- Require confirmation before external writes or deployment.",
                    "- Report changed files, validation, and unresolved risks.",
                ]
            )
            (root / "AGENTS.md").write_text("# Shared\n" + shared, encoding="utf-8")
            (root / "CLAUDE.md").write_text("# Claude\n" + shared, encoding="utf-8")
            ids = self.finding_ids(root)
            self.assertIn("VSAI.CONTEXT.DUPLICATE_CONTENT", ids)

    def test_bounded_configuration_has_no_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".vscode").mkdir()
            (root / ".codex").mkdir()
            (root / ".claude").mkdir()
            (root / "skills" / "sample").mkdir(parents=True)
            (root / "AGENTS.md").write_text("# Shared\n", encoding="utf-8")
            (root / "CLAUDE.md").write_text("# Claude-specific\n", encoding="utf-8")
            (root / ".vscode" / "settings.json").write_text(
                json.dumps(
                    {
                        "chat.useAgentsMdFile": True,
                        "chat.useClaudeMdFile": False,
                        "chat.agentSkillsLocations": {"skills": True},
                        "chat.mcp.discovery.enabled": False,
                        "github.copilot.chat.summarizeAgentConversationHistory.enabled": True,
                        "chat.tools.compressOutput.enabled": True,
                    }
                ),
                encoding="utf-8",
            )
            (root / ".codex" / "config.toml").write_text(
                'sandbox_mode = "workspace-write"\napproval_policy = "on-request"\n'
                'model_reasoning_effort = "medium"\n'
                '[sandbox_workspace_write]\nnetwork_access = false\n',
                encoding="utf-8",
            )
            (root / ".claude" / "settings.json").write_text(
                json.dumps(
                    {
                        "effortLevel": "medium",
                        "permissions": {
                            "defaultMode": "plan",
                            "allow": ["Bash(git status)", "Bash(git diff *)"],
                            "deny": ["Read(./.env)", "Bash(git push *)"],
                        },
                    }
                ),
                encoding="utf-8",
            )
            result = MODULE.audit(root)
            self.assertEqual(0, result["summary"]["error"])


if __name__ == "__main__":
    unittest.main()
