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


CASE_VALIDATOR = load_module(
    "validate_evidence_wayfinding_case",
    SCRIPTS / "validate_evidence_wayfinding_case.py",
)
SCHEMA_VALIDATOR = load_module(
    "validate_json_schema_instance",
    SCRIPTS / "validate_json_schema_instance.py",
)
PACK_VALIDATOR = load_module(
    "validate_portable_case_pack",
    SCRIPTS / "validate_portable_case_pack.py",
)

CASE_DIR = ROOT / "examples" / "evidence-wayfinding" / "case-0-schema-parity"
PACK = CASE_DIR / "portable-case-pack.json"
PACK_SCHEMA = ROOT / "schemas" / "capability" / "portable-case-pack.v1.schema.json"
ADMISSION_SCHEMA = ROOT / "schemas" / "capability" / "attention-admission-receipt.v1.schema.json"
OUTCOME_SCHEMA = ROOT / "schemas" / "capability" / "outcome-receipt.v1.schema.json"


class EvidenceWayfindingCase0Tests(unittest.TestCase):
    def test_case_spine_is_cross_file_consistent(self) -> None:
        self.assertEqual([], CASE_VALIDATOR.validate_case(CASE_DIR))

    def test_case_pack_passes_authoritative_structural_schema(self) -> None:
        self.assertEqual([], SCHEMA_VALIDATOR.validate_instance(PACK_SCHEMA, PACK))

    def test_admission_and_outcome_pass_authoritative_schemas(self) -> None:
        self.assertEqual(
            [],
            SCHEMA_VALIDATOR.validate_instance(
                ADMISSION_SCHEMA, CASE_DIR / "admission-receipt.json"
            ),
        )
        self.assertEqual(
            [],
            SCHEMA_VALIDATOR.validate_instance(
                OUTCOME_SCHEMA, CASE_DIR / "outcome-receipt.json"
            ),
        )

    def test_case_pack_passes_semantic_validator_after_schema(self) -> None:
        record = PACK_VALIDATOR.load_json(PACK)
        self.assertEqual([], PACK_VALIDATOR.validate_pack(record))

    def test_case_preserves_public_synthetic_boundary(self) -> None:
        for filename in [
            "case-contract.json",
            "admission-receipt.json",
            "decision-card.json",
            "verification-receipt.json",
            "outcome-receipt.json",
        ]:
            record = CASE_VALIDATOR.load_json(CASE_DIR / filename)
            self.assertEqual("synthetic_reference", record["simulation_status"])
            self.assertEqual("not_observed", record["downstream_adoption_status"])
            self.assertEqual("public", record["data_classification"])

    def test_case_does_not_grant_promotion_authority(self) -> None:
        outcome = CASE_VALIDATOR.load_json(CASE_DIR / "outcome-receipt.json")
        candidate = outcome["failure_point_candidate"]
        self.assertTrue(candidate["eligible_for_harness_candidate"])
        self.assertEqual("none_from_outcome_receipt", candidate["promotion_authority"])

    def mutate_case(self, filename: str, mutator) -> list[str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            copied = Path(temp_dir) / "case"
            shutil.copytree(CASE_DIR, copied)
            path = copied / filename
            record = json.loads(path.read_text(encoding="utf-8"))
            mutator(record)
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            return CASE_VALIDATOR.validate_case(copied)

    def test_ready_admission_cannot_waive_mandatory_check(self) -> None:
        def remove_check(record):
            del record["mandatory_checks"]["M3_counterevidence"]

        errors = self.mutate_case("admission-receipt.json", remove_check)
        self.assertTrue(any("missing mandatory admission check" in error for error in errors))

    def test_receipt_cannot_reference_unknown_case_evidence(self) -> None:
        def add_unknown(record):
            record["options"][0]["evidence_refs"].append("EV-NOT-IN-PACK")

        errors = self.mutate_case("decision-card.json", add_unknown)
        self.assertTrue(any("unknown evidence" in error for error in errors))

    def test_single_replay_cannot_grant_promotion_authority(self) -> None:
        def promote(record):
            record["failure_point_candidate"]["promotion_authority"] = "team_available"

        errors = self.mutate_case("outcome-receipt.json", promote)
        self.assertTrue(any("cannot grant Harness promotion authority" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
