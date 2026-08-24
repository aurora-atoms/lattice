#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from generate_capability_composition_registry import render  # noqa: E402
from validate_capability_compositions import (  # noqa: E402
    SCHEMA_PATH,
    load_json,
    validate_all,
    validate_concept,
)

CONCEPT_PATH = ROOT / "concepts" / "safety-critical-adversarial-innovation" / "concept.json"
REGISTRY_PATH = ROOT / "registry" / "capability-compositions.index.jsonl"


class CapabilityCompositionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = load_json(ROOT / SCHEMA_PATH)
        self.concept = load_json(CONCEPT_PATH)

    def errors_for(self, concept: dict) -> list[str]:
        return validate_concept(ROOT, CONCEPT_PATH, concept, self.schema)

    def test_reference_concept_is_valid(self) -> None:
        self.assertEqual([], validate_all(ROOT))

    def test_agent_can_discover_expected_stage_chain(self) -> None:
        stages = {stage["stage_id"]: stage for stage in self.concept["stages"]}
        self.assertEqual("safety_review", self.concept["first_stage"])
        self.assertEqual(["innovation_mining"], stages["safety_review"]["next_stages"])
        self.assertEqual(["prior_art_research"], stages["innovation_mining"]["next_stages"])
        self.assertEqual([], stages["prior_art_research"]["next_stages"])
        self.assertEqual("docs/safety-critical-product-review.md", stages["safety_review"]["entrypoint"])
        self.assertEqual("docs/adversarial-innovation-mining.md", stages["innovation_mining"]["entrypoint"])
        self.assertEqual("docs/systematic-invention-research-stack.md", stages["prior_art_research"]["entrypoint"])

    def test_progressive_loading_keeps_implementation_noise_out_of_context(self) -> None:
        for stage in self.concept["stages"]:
            for artifact in stage["artifacts"]:
                if artifact["role"] in {"validator", "maintainer_test", "ci_enforcement"}:
                    self.assertEqual("never_by_default", artifact["activation"])
                if artifact["role"] == "validator":
                    self.assertEqual("execute", artifact["action"])
                if artifact["role"] in {"maintainer_test", "ci_enforcement"}:
                    self.assertEqual("none", artifact["action"])

    def test_compact_registry_projection_is_in_sync(self) -> None:
        self.assertEqual(render(ROOT), REGISTRY_PATH.read_text(encoding="utf-8"))
        rows = [
            json.loads(line)
            for line in REGISTRY_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        row = next(item for item in rows if item["concept_id"] == self.concept["concept_id"])
        self.assertEqual(self.concept["entrypoint"], row["entrypoint"])
        self.assertEqual(self.concept["trigger"], row["trigger"])

    def test_unknown_next_stage_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.concept)
        candidate["stages"][0]["next_stages"] = ["missing_stage"]
        errors = self.errors_for(candidate)
        self.assertTrue(any("unknown next_stage" in error for error in errors))

    def test_ci_cannot_be_promoted_into_task_context(self) -> None:
        candidate = copy.deepcopy(self.concept)
        mining = next(stage for stage in candidate["stages"] if stage["stage_id"] == "innovation_mining")
        ci = next(item for item in mining["artifacts"] if item["role"] == "ci_enforcement")
        ci["activation"] = "task_scoped"
        errors = self.errors_for(candidate)
        self.assertTrue(any("ci_enforcement must be never_by_default" in error for error in errors))

    def test_validator_source_cannot_become_read_context(self) -> None:
        candidate = copy.deepcopy(self.concept)
        mining = next(stage for stage in candidate["stages"] if stage["stage_id"] == "innovation_mining")
        validator = next(item for item in mining["artifacts"] if item["role"] == "validator")
        validator["action"] = "read"
        errors = self.errors_for(candidate)
        self.assertTrue(any("validator must be executed" in error for error in errors))

    def test_missing_artifact_path_is_rejected(self) -> None:
        candidate = copy.deepcopy(self.concept)
        candidate["stages"][1]["artifacts"][0]["path"] = "docs/does-not-exist.md"
        errors = self.errors_for(candidate)
        self.assertTrue(any("artifact path does not exist" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
