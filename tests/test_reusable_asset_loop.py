from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "feature-delivery-harness-mvp" / "scripts" / "run_reusable_asset_loop.py"
FIXTURE = ROOT / "feature-delivery-harness-mvp" / "evals" / "reusable_asset_loop_case_001" / "input.jsonl"
SPEC = importlib.util.spec_from_file_location("run_reusable_asset_loop", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ReusableAssetLoopTests(unittest.TestCase):
    def records(self) -> list[dict]:
        return MODULE.load_jsonl(FIXTURE)

    def test_valid_reviewed_vertical_slice(self) -> None:
        records = self.records()
        self.assertEqual([], MODULE.validate(records))
        dossier = MODULE.render_dossier(records)
        self.assertIn("# Reusable Asset Dossier v0.1", dossier)
        self.assertIn("Decision: `approved`", dossier)
        self.assertIn("Activation: `task_scoped`", dossier)

    def test_unapproved_candidate_cannot_be_task_scoped_or_used(self) -> None:
        records = self.records()
        review = next(item for item in records if item["type"] == "reusable_asset.review")
        review["payload"]["decision"] = "needs_changes"
        errors = MODULE.validate(records)
        self.assertTrue(any("never_by_default" in item for item in errors))
        self.assertTrue(any("cannot claim qualified or used maturity" in item for item in errors))

    def test_originating_comment_must_be_preserved(self) -> None:
        records = self.records()
        candidate = next(item for item in records if item["type"] == "reusable_asset.candidate")
        candidate["payload"]["created_from_contribution_refs"] = []
        errors = MODULE.validate(records)
        self.assertTrue(any("originating contribution" in item for item in errors))

    def test_cli_matches_golden(self) -> None:
        expected = ROOT / "feature-delivery-harness-mvp" / "evals" / "reusable_asset_loop_case_001" / "expected_dossier.md"
        with tempfile.TemporaryDirectory() as temp_dir:
            out = Path(temp_dir) / "dossier.md"
            result = MODULE.main_from_args([str(FIXTURE), "--out", str(out), "--expected", str(expected)]) if hasattr(MODULE, "main_from_args") else None
            if result is None:
                dossier = MODULE.render_dossier(self.records())
                out.write_text(dossier, encoding="utf-8", newline="\n")
                self.assertEqual(expected.read_text(encoding="utf-8").strip(), dossier.strip())
            else:
                self.assertEqual(0, result)


if __name__ == "__main__":
    unittest.main()
