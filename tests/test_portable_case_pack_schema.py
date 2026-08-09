from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

SPEC = importlib.util.spec_from_file_location(
    "validate_json_schema_instance",
    SCRIPTS / "validate_json_schema_instance.py",
)
assert SPEC and SPEC.loader
SCHEMA_VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCHEMA_VALIDATOR)

SCHEMA = ROOT / "schemas" / "capability" / "portable-case-pack.v1.schema.json"
FIXTURES = ROOT / "tests" / "fixtures" / "evidence-wayfinding"
VALID = FIXTURES / "valid" / "portable-case-pack.minimal.v1.json"
INVALID = FIXTURES / "invalid"
SEMANTIC_DECISION = FIXTURES / "semantic-decision" / "derived-claim-without-evidence.json"
PUBLIC_EXAMPLE = ROOT / "examples" / "evidence-wayfinding" / "portable-case-pack.synthetic.v1.json"


class PortableCasePackSchemaParityTests(unittest.TestCase):
    def test_valid_minimal_fixture_passes_authoritative_schema(self) -> None:
        self.assertEqual([], SCHEMA_VALIDATOR.validate_instance(SCHEMA, VALID))

    def test_committed_public_example_passes_authoritative_schema(self) -> None:
        self.assertEqual([], SCHEMA_VALIDATOR.validate_instance(SCHEMA, PUBLIC_EXAMPLE))

    def test_structural_mutations_are_rejected(self) -> None:
        fixtures = sorted(INVALID.glob("*.json"))
        self.assertEqual(4, len(fixtures))
        for fixture in fixtures:
            with self.subTest(fixture=fixture.name):
                errors = SCHEMA_VALIDATOR.validate_instance(SCHEMA, fixture)
                self.assertTrue(errors, f"schema unexpectedly accepted {fixture.name}")

    def test_unknown_top_level_field_is_rejected(self) -> None:
        errors = SCHEMA_VALIDATOR.validate_instance(SCHEMA, INVALID / "unknown-top-level.json")
        self.assertTrue(any("Additional properties are not allowed" in error for error in errors))

    def test_required_fields_are_rejected_when_missing(self) -> None:
        for name, field in [
            ("missing-audience.json", "audience"),
            ("missing-required-output.json", "required_output"),
        ]:
            with self.subTest(fixture=name):
                errors = SCHEMA_VALIDATOR.validate_instance(SCHEMA, INVALID / name)
                self.assertTrue(any(field in error and "required property" in error for error in errors))

    def test_date_time_format_is_enforced(self) -> None:
        errors = SCHEMA_VALIDATOR.validate_instance(SCHEMA, INVALID / "malformed-evidence-date.json")
        self.assertTrue(any("date-time" in error for error in errors))

    def test_derived_claim_without_evidence_remains_explicit_semantic_decision(self) -> None:
        # v1 structurally permits an empty evidence_refs array on derived claims.
        # Tightening that rule requires an explicit contract/version decision rather than
        # silently expanding the structural validator in this parity fix.
        self.assertEqual([], SCHEMA_VALIDATOR.validate_instance(SCHEMA, SEMANTIC_DECISION))


if __name__ == "__main__":
    unittest.main()
