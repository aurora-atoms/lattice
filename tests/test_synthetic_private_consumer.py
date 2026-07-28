from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "synthetic-private-consumer"
GOLDEN = EXAMPLE / "golden" / "manager-ready-delivery-asset-pack"


class SyntheticPrivateConsumerTests(unittest.TestCase):
    def test_one_command_generation_and_golden_check(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(EXAMPLE / "run_conformance.py"),
                "--root",
                str(EXAMPLE),
                "--lattice-root",
                str(ROOT),
                "--check",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("golden Manager-Ready Delivery Asset Pack matches", result.stdout)

    def test_golden_pack_preserves_synthetic_boundary(self) -> None:
        manifest = json.loads(
            (GOLDEN / "asset-pack.manifest.json").read_text(encoding="utf-8")
        )
        brief = json.loads((GOLDEN / "manager-brief.json").read_text(encoding="utf-8"))
        report = json.loads(
            (GOLDEN / "validation-report.json").read_text(encoding="utf-8")
        )
        self.assertEqual("synthetic_reference", manifest["simulation_status"])
        self.assertEqual("not_observed", manifest["downstream_adoption_status"])
        self.assertEqual("not_observed", brief["downstream_adoption_status"])
        self.assertIsNone(brief["human_review_ref"])
        self.assertIsNone(brief["governance_approval_ref"])
        self.assertEqual("pass", report["status"])
        self.assertEqual(
            {
                "dangling-evidence-ref",
                "synthetic-maturity-violation",
                "team-wide-overclaim",
                "unreviewed-promotion",
                "unsupported-private-extension",
            },
            set(report["negative_cases"]),
        )

    def test_unknown_business_claims_remain_unknown(self) -> None:
        brief = json.loads((GOLDEN / "manager-brief.json").read_text(encoding="utf-8"))
        classifications = {
            claim["claim_kind"]: claim["classification"] for claim in brief["claims"]
        }
        for kind in ("reuse", "team_adoption", "manager_acceptance", "roi"):
            self.assertEqual("UNKNOWN", classifications[kind])


if __name__ == "__main__":
    unittest.main()
