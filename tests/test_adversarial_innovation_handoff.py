#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_adversarial_innovation_handoff.py"
FIXTURE = ROOT / "examples" / "adversarial-innovation" / "synthetic-target-binding.innovation-handoff.v1.json"


def load_module():
    spec = importlib.util.spec_from_file_location("validate_adversarial_innovation_handoff", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


HANDOFF = load_module()


class AdversarialInnovationHandoffTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def assertErrorContains(self, errors: list[str], text: str) -> None:
        self.assertTrue(any(text in error for error in errors), errors)

    def test_synthetic_fixture_is_valid(self) -> None:
        self.assertEqual([], HANDOFF.validate_record(self.record))

    def test_unknown_source_chain_is_rejected(self) -> None:
        record = copy.deepcopy(self.record)
        record["mechanism_candidates"][0]["source_chain_ids"] = ["CHAIN-NOT-IN-REVIEW"]
        self.assertErrorContains(HANDOFF.validate_record(record), "not present in source_review")

    def test_defeating_existing_control_forces_reject(self) -> None:
        record = copy.deepcopy(self.record)
        record["mechanism_candidates"][0]["counter_control"]["defeats_candidate"] = True
        self.assertErrorContains(HANDOFF.validate_record(record), "requires reject_existing_control + reject")

    def test_prior_art_equivalent_forces_reject(self) -> None:
        record = copy.deepcopy(self.record)
        candidate = record["mechanism_candidates"][0]
        candidate["prior_art_challenge"].update(
            {
                "status": "completed",
                "conclusion": "equivalent_or_broader_mechanism_found",
                "coverage_refs": ["public://prior-art/coverage-001"],
                "strongest_counterevidence": "A public reference describes the equivalent mechanism."
            }
        )
        self.assertErrorContains(HANDOFF.validate_record(record), "requires reject_prior_art + reject")

    def test_retained_candidate_requires_completed_bounded_prior_art_challenge(self) -> None:
        record = copy.deepcopy(self.record)
        candidate = record["mechanism_candidates"][0]
        candidate["status"] = "retain_candidate"
        candidate["decision"] = "retain_for_research"
        self.assertErrorContains(HANDOFF.validate_record(record), "requires all falsifiers to survive")
        self.assertErrorContains(HANDOFF.validate_record(record), "requires completed bounded prior-art challenge")

    def test_retained_candidate_is_valid_only_after_falsifiers_and_bounded_search(self) -> None:
        record = copy.deepcopy(self.record)
        candidate = record["mechanism_candidates"][0]
        for falsifier in candidate["falsifiers"]:
            falsifier["status"] = "survived"
        candidate["prior_art_challenge"].update(
            {
                "status": "completed",
                "conclusion": "no_equivalent_found_in_bounded_search",
                "coverage_refs": ["public://prior-art/coverage-001"],
                "strongest_counterevidence": "Nearest public mechanism lacks action-time physical-lineage binding."
            }
        )
        candidate["status"] = "retain_candidate"
        candidate["decision"] = "retain_for_research"
        candidate["rationale"] = "Retain as a patent-research candidate after the bounded challenger; coverage gaps remain explicit."
        self.assertEqual([], HANDOFF.validate_record(record))

    def test_unreproduced_hard_case_cannot_advance(self) -> None:
        record = copy.deepcopy(self.record)
        candidate = record["mechanism_candidates"][0]
        candidate["hard_case"]["reproducibility"] = "not_reproduced"
        self.assertErrorContains(HANDOFF.validate_record(record), "cannot advance beyond candidate/insufficient/reject")

    def test_unsupported_patentability_assertion_is_rejected(self) -> None:
        record = copy.deepcopy(self.record)
        record["mechanism_candidates"][0]["rationale"] = "This mechanism is patentable."
        self.assertErrorContains(HANDOFF.validate_record(record), "unsupported patentability/novelty/FTO assertion")

    def test_private_locator_is_rejected(self) -> None:
        record = copy.deepcopy(self.record)
        record["scope"]["case_ref"] = "file:/Users/example/private-case.json"
        self.assertErrorContains(HANDOFF.validate_record(record), "private locator")

    def test_cli_validates_fixture(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURE)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertIn("adversarial innovation handoff: valid", completed.stdout)


if __name__ == "__main__":
    unittest.main()
