#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "audit_native_vscode_config.py"
SPEC = importlib.util.spec_from_file_location("audit_native_vscode_config", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class NativeVSCodeAuditTests(unittest.TestCase):
    def finding_ids(self, root: Path) -> set[str]:
        return {item["id"] for item in MODULE.audit(root)["findings"]}

    def test_flags_redundant_defaults_nonstable_settings_and_extension_overlap(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".vscode").mkdir()
            (root / ".vscode/settings.json").write_text(
                json.dumps(
                    {
                        "chat.agent.maxRequests": 25,
                        "chat.mcp.discovery.enabled": False,
                        "chat.permissions.default": "default",
                        "claudeCode.useTerminal": False,
                    }
                ),
                encoding="utf-8",
            )
            ids = self.finding_ids(root)
            self.assertIn("VSAI.NATIVE.REDUNDANT_DEFAULT", ids)
            self.assertIn("VSAI.NATIVE.NON_STABLE_SETTING", ids)
            self.assertIn("VSAI.NATIVE.EXTENSION_OVERLAP_REVIEW", ids)

    def test_flags_broad_native_autonomy_and_claude_bypass(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".vscode").mkdir()
            (root / ".vscode/settings.json").write_text(
                json.dumps(
                    {
                        "chat.tools.global.autoApprove": True,
                        "chat.permissions.default": "autopilot",
                        "github.copilot.chat.claudeAgent.allowDangerouslySkipPermissions": True,
                    }
                ),
                encoding="utf-8",
            )
            ids = self.finding_ids(root)
            self.assertIn("VSAI.NATIVE.BROAD_AUTONOMY", ids)
            self.assertIn("VSAI.NATIVE.CLAUDE_PERMISSION_BYPASS", ids)

    def test_lattice_minimal_native_settings_have_no_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".vscode").mkdir()
            (root / "skills/sample").mkdir(parents=True)
            (root / ".vscode/settings.json").write_text(
                json.dumps({"chat.agentSkillsLocations": {"skills": True}}),
                encoding="utf-8",
            )
            result = MODULE.audit(root)
            self.assertEqual(0, result["summary"]["error"])
            self.assertTrue(result["surfaces"]["native_policy_audit"])


if __name__ == "__main__":
    unittest.main()
