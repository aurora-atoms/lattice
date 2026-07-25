from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from route_capabilities import route  # noqa: E402


class RoutingTests(unittest.TestCase):
    def test_ci_failure_auto_invokes_rescue(self) -> None:
        result = route(ROOT, "Diagnose this CI failure and failing test", "implement", "auto")
        self.assertEqual(result["status"], "auto_invoke")
        self.assertEqual(result["selected"][0]["skill_id"], "delivery-rescue")
        self.assertEqual(result["load_plan"]["skill_bodies"], ["skills/delivery-rescue/SKILL.md"])

    def test_context_request_auto_invokes_context_skill(self) -> None:
        result = route(ROOT, "Help me understand codebase and build a context pack", "understand", "auto")
        self.assertEqual(result["status"], "auto_invoke")
        self.assertEqual(result["selected"][0]["skill_id"], "context-mastery")

    def test_side_effectful_artifact_is_recommended(self) -> None:
        result = route(ROOT, "Create a PR ready package and release summary", "review", "auto")
        self.assertEqual(result["status"], "recommend")
        self.assertEqual(result["selected"][0]["skill_id"], "delivery-artifact-builder")

    def test_high_impact_action_asks(self) -> None:
        result = route(ROOT, "Create a release summary and approve release", "release", "auto")
        self.assertEqual(result["status"], "ask")

    def test_unknown_request_loads_no_skill(self) -> None:
        result = route(ROOT, "Choose an office wall color", "", "auto")
        self.assertEqual(result["status"], "no_match")
        self.assertEqual(result["load_plan"]["skill_bodies"], [])

    def test_chinese_context_request_routes(self) -> None:
        result = route(ROOT, "先帮我理解代码库并建立领域上下文", "understand", "auto")
        self.assertEqual(result["selected"][0]["skill_id"], "context-mastery")


if __name__ == "__main__":
    unittest.main()
