import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_unasked_questions.py"
FIXTURE = ROOT / "evals" / "fixtures" / "valid-unasked-questions.json"


class UnaskedQuestionsValidationTests(unittest.TestCase):
    def run_validator(self, payload):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
            json.dump(payload, handle)
            path = Path(handle.name)
        try:
            return subprocess.run([sys.executable, str(VALIDATOR), str(path)], capture_output=True, text=True)
        finally:
            path.unlink(missing_ok=True)

    def test_valid_fixture(self):
        result = subprocess.run([sys.executable, str(VALIDATOR), str(FIXTURE)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_requires_evidence(self):
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        payload["questions"][0]["evidence"] = []
        result = self.run_validator(payload)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("evidence", result.stderr)

    def test_blocker_requires_rationale(self):
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        payload["questions"][0]["blocking_rationale"] = ""
        result = self.run_validator(payload)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("blocking_rationale", result.stderr)

    def test_accepted_uncertainty_requires_control(self):
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        payload["questions"][1]["monitoring"] = ""
        result = self.run_validator(payload)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("monitoring", result.stderr)


if __name__ == "__main__":
    unittest.main()
