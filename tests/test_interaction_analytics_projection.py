from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "skills" / "self-service-analytics-mvp-builder" / "schemas" / "interaction-analytics-projection.v1.schema.json"
VALIDATOR_PATH = ROOT / "skills" / "self-service-analytics-mvp-builder" / "scripts" / "validate_interaction_projection.py"
REPLAY_PATH = ROOT / "scripts" / "replay_interaction_analytics_guidance.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_module("interaction_projection_validator", VALIDATOR_PATH)
REPLAY = load_module("interaction_analytics_replay", REPLAY_PATH)


class InteractionAnalyticsProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = REPLAY.mutate_cases()

    def test_schema_is_strict_and_valid_case_passes(self) -> None:
        case = self.cases["valid_projection"]
        self.assertEqual([], VALIDATOR.validate_instance(case))
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertIs(schema["additionalProperties"], False)

    def test_missing_interaction_snapshot_fails(self) -> None:
        case = copy.deepcopy(self.cases["valid_projection"])
        del case["interaction_snapshot"]
        self.assertTrue(VALIDATOR.validate_instance(case))

    def test_ambiguous_intent_cannot_become_projection(self) -> None:
        case = copy.deepcopy(self.cases["ambiguous_click"])
        case["projection_candidate"] = copy.deepcopy(self.cases["valid_projection"]["projection_candidate"])
        self.assertTrue(any("ambiguous or unknown intent" in error for error in VALIDATOR.validate_instance(case)))

    def test_reuse_and_projection_are_exclusive(self) -> None:
        case = copy.deepcopy(self.cases["reuse_existing"])
        case["projection_candidate"] = copy.deepcopy(self.cases["valid_projection"]["projection_candidate"])
        self.assertTrue(any("reuse_existing cannot contain" in error for error in VALIDATOR.validate_instance(case)))

    def test_parent_metric_version_must_be_preserved(self) -> None:
        case = copy.deepcopy(self.cases["valid_projection"])
        case["projection_candidate"]["parent_metric_ref"]["metric_version"] = "v2"
        self.assertTrue(any("metric_version" in error for error in VALIDATOR.validate_instance(case)))

    def test_failed_gates_cannot_claim_display_ready(self) -> None:
        for name in ("semantic_drift", "hidden_filter_loss", "security_expansion", "fanout", "compute_budget"):
            case = copy.deepcopy(self.cases[name])
            case["status"] = "display_ready"
            self.assertTrue(VALIDATOR.validate_instance(case), name)

    def test_result_failure_cannot_be_display_ready(self) -> None:
        case = copy.deepcopy(self.cases["result_reconciliation"])
        case["status"] = "display_ready"
        self.assertTrue(any("result validation failure" in error for error in VALIDATOR.validate_instance(case)))

    def test_unknowns_are_visible_and_promotion_is_fail_closed(self) -> None:
        case = copy.deepcopy(self.cases["stale_version"])
        case["unknowns"] = []
        self.assertTrue(any("visible blocking unknown" in error for error in VALIDATOR.validate_instance(case)))
        candidate = self.cases["repeated_use"]
        self.assertFalse(candidate["production_approved"])
        self.assertFalse(candidate["promotion_boundary"]["gold_promotion_approved"])
        self.assertTrue(candidate["promotion_boundary"]["human_review_required"])

    def test_replay_covers_required_scenario_families(self) -> None:
        replay = REPLAY.run_replay()
        self.assertTrue(replay["all_passed"], replay["failures"])
        self.assertEqual("deterministic_guidance_conformance", replay["replay_kind"])
        self.assertEqual("not_evaluated", replay["agent_behavior_status"])
        self.assertEqual(
            {
                "reuse_existing", "valid_projection", "semantic_drift", "hidden_filter_loss",
                "security_expansion", "fanout", "non_additive", "ambiguous_click", "compute_budget",
                "stale_version", "result_reconciliation", "repeated_use", "compound_failures",
            },
            set(replay["scenarios"]),
        )


if __name__ == "__main__":
    unittest.main()
