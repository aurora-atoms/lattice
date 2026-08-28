from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "replay_silver_modeling_guidance.py"
SPEC = importlib.util.spec_from_file_location("silver_modeling_replay", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class SilverModelingGuidanceReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.replay = MODULE.run_replay()

    def test_all_synthetic_scenarios_pass(self) -> None:
        self.assertTrue(self.replay["all_passed"], self.replay["passes"])

    def test_replay_does_not_claim_real_systems_or_adoption(self) -> None:
        self.assertEqual("synthetic_reference", self.replay["simulation_status"])
        self.assertEqual("not_observed", self.replay["downstream_adoption_status"])
        self.assertTrue(self.replay["limitations"])

    def test_consumer_and_modeling_questions_precede_context_and_live_evidence(self) -> None:
        actions = self.replay["scenarios"]["clean_candidate"]["actions"]
        self.assertLess(
            actions.index("define_gold_consumer_contract"),
            actions.index("define_modeling_question_contract"),
        )
        self.assertLess(
            actions.index("define_modeling_question_contract"),
            actions.index("select_minimum_datahub_context"),
        )
        self.assertLess(
            actions.index("select_minimum_datahub_context"),
            actions.index("inspect_targeted_live_evidence"),
        )
        self.assertNotIn("build_system_mental_model", actions)

    def test_false_uniqueness_rejects_profiled_key(self) -> None:
        result = self.replay["scenarios"]["false_uniqueness"]
        self.assertEqual("PARTIAL_KEY_REJECTED", result["STATUS"])
        self.assertIsNone(result["SILVER_MODEL_CANDIDATE"]["candidate_key"])
        self.assertTrue(result["COUNTEREVIDENCE"])

    def test_join_fanout_and_gold_mismatch_are_rejected(self) -> None:
        self.assertEqual(
            "BLOCKED_JOIN_FANOUT",
            self.replay["scenarios"]["join_fanout"]["STATUS"],
        )
        self.assertEqual(
            "REJECTED_GOLD_MISMATCH",
            self.replay["scenarios"]["gold_consumer_mismatch"]["STATUS"],
        )

    def test_temporal_and_authority_conflicts_remain_blocking(self) -> None:
        temporal = self.replay["scenarios"]["temporal_mismatch"]
        conflict = self.replay["scenarios"]["conflicting_authority"]
        self.assertEqual("BLOCKED_TEMPORAL_SEMANTICS", temporal["STATUS"])
        self.assertEqual("BLOCKED_AUTHORITY_CONFLICT", conflict["STATUS"])
        self.assertTrue(temporal["UNKNOWN"])
        self.assertTrue(conflict["COUNTEREVIDENCE"])

    def test_duplicates_and_schema_evolution_limit_candidate(self) -> None:
        self.assertEqual(
            "PARTIAL_DEDUP_REQUIRED",
            self.replay["scenarios"]["late_duplicate_events"]["STATUS"],
        )
        self.assertEqual(
            "PARTIAL_VERSION_SCOPED",
            self.replay["scenarios"]["schema_evolution"]["STATUS"],
        )

    def test_insufficient_evidence_stops_unknown(self) -> None:
        result = self.replay["scenarios"]["insufficient_evidence"]
        self.assertEqual("INSUFFICIENT_EVIDENCE", result["STATUS"])
        self.assertEqual("unknown", result["SILVER_MODEL_CANDIDATE"]["status"])
        self.assertTrue(result["UNKNOWN"])

    def test_no_scenario_approves_production(self) -> None:
        for result in self.replay["scenarios"].values():
            self.assertFalse(result["PRODUCTION_APPROVED"])
            self.assertTrue(result["SILVER_MODEL_CANDIDATE"]["candidate_only"])

    def test_output_keeps_evidence_classes_separate(self) -> None:
        required = {
            "actions",
            "FACT",
            "INFERENCE",
            "COUNTEREVIDENCE",
            "UNKNOWN",
            "SOURCE_ROLES",
            "SILVER_MODEL_CANDIDATE",
            "STATUS",
            "PRODUCTION_APPROVED",
        }
        for result in self.replay["scenarios"].values():
            self.assertEqual(required, set(result))


if __name__ == "__main__":
    unittest.main()
