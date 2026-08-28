from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "replay_operational_evidence_guidance.py"
SPEC = importlib.util.spec_from_file_location("operational_evidence_replay", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class OperationalEvidenceGuidanceReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.replay = MODULE.run_replay()

    def test_all_synthetic_scenarios_pass(self) -> None:
        self.assertTrue(self.replay["all_passed"], self.replay["passes"])

    def test_replay_does_not_claim_real_systems_or_adoption(self) -> None:
        self.assertEqual("synthetic_reference", self.replay["simulation_status"])
        self.assertEqual("not_observed", self.replay["downstream_adoption_status"])
        self.assertTrue(self.replay["limitations"])

    def test_code_and_expected_effect_precede_context_and_live_query(self) -> None:
        actions = self.replay["scenarios"]["healthy"]["actions"]
        self.assertLess(actions.index("inspect_code"), actions.index("build_expected_effect_contract"))
        self.assertLess(actions.index("build_expected_effect_contract"), actions.index("select_minimum_context"))
        self.assertLess(actions.index("select_minimum_context"), actions.index("query_live_source"))

    def test_empty_initial_query_corrects_field_mapping(self) -> None:
        result = self.replay["scenarios"]["transformation_mismatch"]
        self.assertEqual("VERIFIED", result["VERDICT"])
        self.assertIn("correct_cross_boundary_field_mapping", result["actions"])
        self.assertTrue(result["COUNTEREVIDENCE"])

    def test_empty_initial_query_corrects_environment_destination(self) -> None:
        result = self.replay["scenarios"]["wrong_environment_destination"]
        self.assertEqual("VERIFIED", result["VERDICT"])
        self.assertIn("correct_environment_destination_mapping", result["actions"])

    def test_absence_does_not_collapse_failure_boundaries(self) -> None:
        self.assertEqual(
            "TRIGGER_NOT_EXECUTED",
            self.replay["scenarios"]["trigger_not_executed"]["VERDICT"],
        )
        self.assertEqual(
            "SUPPRESSED_BY_CONFIG",
            self.replay["scenarios"]["logging_suppressed"]["VERDICT"],
        )
        self.assertEqual("INGEST_DROP", self.replay["scenarios"]["ingest_drop"]["VERDICT"])
        self.assertEqual(
            "UNKNOWN_AFTER_QUERY",
            self.replay["scenarios"]["unlocated_after_bounded_query"]["VERDICT"],
        )
        self.assertTrue(self.replay["scenarios"]["unlocated_after_bounded_query"]["UNKNOWN"])

    def test_positive_match_binds_event_environment_and_correlation(self) -> None:
        facts = " ".join(self.replay["scenarios"]["healthy"]["FACT"])
        self.assertIn("event=upload_complete", facts)
        self.assertIn("correlation=req-42", facts)
        self.assertIn("environment=test", facts)

    def test_output_keeps_evidence_classes_separate(self) -> None:
        for result in self.replay["scenarios"].values():
            self.assertEqual(
                {"actions", "FACT", "INFERENCE", "COUNTEREVIDENCE", "UNKNOWN", "VERDICT"},
                set(result),
            )


if __name__ == "__main__":
    unittest.main()
