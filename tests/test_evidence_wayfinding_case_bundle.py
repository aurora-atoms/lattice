from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BUNDLE = load_module(
    "validate_evidence_wayfinding_case_bundle",
    SCRIPTS / "validate_evidence_wayfinding_case_bundle.py",
)

CASE_DIR = ROOT / "examples" / "evidence-wayfinding" / "case-0-schema-parity"


class EvidenceWayfindingCaseBundleTests(unittest.TestCase):
    def validate(self, case_dir: Path):
        return BUNDLE.validate_bundle(case_dir, repo_root=ROOT)

    def copy_case(self) -> tuple[tempfile.TemporaryDirectory, Path]:
        temp_dir = tempfile.TemporaryDirectory()
        copied = Path(temp_dir.name) / "case"
        shutil.copytree(CASE_DIR, copied)
        return temp_dir, copied

    def test_case0_bundle_passes_authoritative_entrypoint(self) -> None:
        errors, summary = self.validate(CASE_DIR)
        self.assertEqual([], errors)
        self.assertEqual("pass", summary["status"])
        self.assertIn("portable-case-pack.json", summary["layers"]["structural"])
        self.assertIn("case-spine", summary["layers"]["cross_file"])
        self.assertIn("EV-002", summary["layers"]["evidence_integrity"])
        self.assertIn("harness-mutation-candidate.json", summary["layers"]["evolution"])
        self.assertIn("blind-challenge-execution.blocked.json", summary["layers"]["evolution"])
        self.assertTrue(summary["layers"]["handoff"])

    def test_outcome_unknown_top_level_field_cannot_hide_behind_case_spine(self) -> None:
        temp_dir, copied = self.copy_case()
        try:
            path = copied / "outcome-receipt.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            record["unexpected_field"] = "would previously pass the cross-file-only validator"
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            errors, _ = self.validate(copied)
            self.assertTrue(
                any("structural/outcome-receipt.json" in error and "Additional properties" in error for error in errors),
                errors,
            )
        finally:
            temp_dir.cleanup()

    def test_harness_candidate_structural_drift_is_rejected_by_same_entrypoint(self) -> None:
        temp_dir, copied = self.copy_case()
        try:
            path = copied / "harness-mutation-candidate.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            record["unexpected_field"] = True
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            errors, _ = self.validate(copied)
            self.assertTrue(
                any("structural/harness-mutation-candidate.json" in error and "Additional properties" in error for error in errors),
                errors,
            )
        finally:
            temp_dir.cleanup()

    def test_repo_evidence_hash_drift_is_rejected(self) -> None:
        temp_dir, copied = self.copy_case()
        try:
            path = copied / "portable-case-pack.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            ev2 = next(item for item in record["evidence_refs"] if item["id"] == "EV-002")
            ev2["content_hash"] = "git:" + "0" * 40
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            errors, _ = self.validate(copied)
            self.assertTrue(
                any("evidence-integrity" in error and "EV-002" in error and "does not match" in error for error in errors),
                errors,
            )
        finally:
            temp_dir.cleanup()

    def test_reserved_handoff_schema_drift_is_rejected_by_same_entrypoint(self) -> None:
        temp_dir, copied = self.copy_case()
        try:
            path = copied / "reserved-evaluation-handoff.request.v2.synthetic.jsonl"
            lines = path.read_text(encoding="utf-8").splitlines()
            record = json.loads(lines[0])
            record["unexpected_field"] = True
            lines[0] = json.dumps(record, sort_keys=True, separators=(",", ":"))
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            errors, _ = self.validate(copied)
            self.assertTrue(
                any("handoff/" in error and "Additional properties" in error for error in errors),
                errors,
            )
        finally:
            temp_dir.cleanup()


if __name__ == "__main__":
    unittest.main()
