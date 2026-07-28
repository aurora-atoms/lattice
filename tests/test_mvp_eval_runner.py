from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "feature-delivery-harness-mvp" / "scripts" / "run_mvp_evals.py"
SPEC = importlib.util.spec_from_file_location("run_mvp_evals", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def case_manifest(case_id: str, case_type: str = "feature_delivery") -> dict:
    return {
        "contract": "lat.eval-case.v1",
        "schema_version": "1.0.0",
        "case_id": case_id,
        "case_type": case_type,
        "required_files": ["input.jsonl", "expected.json"],
    }


class MvpEvalRunnerTests(unittest.TestCase):
    def prepare(self, root: Path, name: str = "case_001") -> Path:
        case = root / name
        case.mkdir()
        (case / "input.jsonl").write_text("{}\n", encoding="utf-8")
        (case / "expected.json").write_text("{}\n", encoding="utf-8")
        return case

    def test_unknown_case_type_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            case = self.prepare(Path(temp))
            value = case_manifest(case.name, "unknown_kind")
            (case / "case.json").write_text(json.dumps(value), encoding="utf-8")
            ok, note, case_type = MODULE.dispatch_case(case)
            self.assertFalse(ok)
            self.assertEqual("unknown", case_type)
            self.assertIn("unknown case_type", note)

    def test_malformed_case_manifest_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            case = self.prepare(Path(temp))
            (case / "case.json").write_text("{broken", encoding="utf-8")
            ok, note, _ = MODULE.dispatch_case(case)
            self.assertFalse(ok)
            self.assertIn("malformed case.json", note)

    def test_incompatible_case_schema_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            case = self.prepare(Path(temp))
            value = case_manifest(case.name)
            value["schema_version"] = "2.0.0"
            (case / "case.json").write_text(json.dumps(value), encoding="utf-8")
            ok, note, _ = MODULE.dispatch_case(case)
            self.assertFalse(ok)
            self.assertIn("incompatible case schema version", note)

    def test_missing_required_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            case = self.prepare(Path(temp))
            value = case_manifest(case.name)
            value["required_files"].append("missing.json")
            (case / "case.json").write_text(json.dumps(value), encoding="utf-8")
            ok, note, _ = MODULE.dispatch_case(case)
            self.assertFalse(ok)
            self.assertIn("missing required file", note)

    def test_missing_case_manifest_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            case = self.prepare(Path(temp))
            ok, note, _ = MODULE.dispatch_case(case)
            self.assertFalse(ok)
            self.assertIn("missing required case.json", note)

    def test_malformed_handler_input_becomes_visible_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            case = self.prepare(Path(temp))
            (case / "case.json").write_text(
                json.dumps(case_manifest(case.name)), encoding="utf-8"
            )
            (case / "expected.json").write_text("{broken", encoding="utf-8")
            ok, note, case_type = MODULE.dispatch_case(case)
            self.assertFalse(ok)
            self.assertEqual("feature_delivery", case_type)
            self.assertIn("handler failed", note)

    def test_failure_still_writes_machine_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            case = self.prepare(root)
            value = case_manifest(case.name, "unknown_kind")
            (case / "case.json").write_text(json.dumps(value), encoding="utf-8")
            summary = root / "summary.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--eval-dir",
                    str(root),
                    "--summary-out",
                    str(summary),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(1, result.returncode)
            report = json.loads(summary.read_text(encoding="utf-8"))
            self.assertEqual("lat.conformance-summary.v1", report["contract"])
            self.assertEqual(1, report["failed"])
            self.assertEqual("fail", report["results"][0]["status"])


if __name__ == "__main__":
    unittest.main()
