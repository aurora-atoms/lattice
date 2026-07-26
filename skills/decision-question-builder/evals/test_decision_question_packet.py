from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_decision_question_packet.py"
spec = importlib.util.spec_from_file_location("decision_question_validator", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class DecisionQuestionPacketTests(unittest.TestCase):
    def load_valid(self) -> dict:
        return json.loads((ROOT / "evals" / "fixtures" / "valid-decision-question.json").read_text(encoding="utf-8"))

    def test_valid_packet(self) -> None:
        self.assertEqual(module.validate(self.load_valid()), [])

    def test_requires_two_options(self) -> None:
        packet = self.load_valid()
        packet["options"] = packet["options"][:1]
        self.assertTrue(any("two to four" in item for item in module.validate(packet)))

    def test_requires_option_evidence_and_risk(self) -> None:
        packet = self.load_valid()
        packet["options"][0]["evidence_refs"] = []
        packet["options"][0]["risks"] = []
        errors = module.validate(packet)
        self.assertTrue(any("evidence_refs" in item for item in errors))
        self.assertTrue(any("risks" in item for item in errors))

    def test_minimum_response_exposes_options(self) -> None:
        packet = self.load_valid()
        packet["minimum_response"] = "Reply with your preference."
        self.assertTrue(any("every selectable option" in item for item in module.validate(packet)))


if __name__ == "__main__":
    unittest.main()
