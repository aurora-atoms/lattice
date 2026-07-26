from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_skill_ci_contracts.py"
spec = importlib.util.spec_from_file_location("validate_skill_ci_contracts", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class SkillCiContractTests(unittest.TestCase):
    def skill_text(self, outputs: str) -> str:
        return f"""---
name: sample-skill
description: Use for markdown input to output a report while preserving behavior. Do not use for coding.
---
# Sample
## Goal
Do work.
## Use When
Use it.
## Do Not Use When
Do not.
## Inputs
Input.
## Outputs
{outputs}
## Workflow
1. Query ConPort before loading or searching full Skill text.
2. Keep rules in a stable prefix.
## Rules
SAMPLE.001 | SHOULD | token | optimize quality-adjusted token ROI
## Verification
Verify.
## Failure Modes
Failure.
"""

    def test_output_contract_accepts_scoped_paths(self):
        text = self.skill_text(
            """```text
artifacts/sample-items/<item-id>/<run-id>/sample.v1.json
artifacts/capability-runs/sample-skill/<run-id>/run-result.json
```
When writing is unavailable, return inline with `write_status=returned_inline`."""
        )
        self.assertEqual(
            [],
            module.validate_output_contract(
                "sample-skill", text, "skills/sample-skill/SKILL.md"
            ),
        )

    def test_output_contract_rejects_generic_and_missing_run_result(self):
        text = self.skill_text(
            """```text
artifacts/output.json
```
Return inline."""
        )
        codes = {
            item.code
            for item in module.validate_output_contract(
                "sample-skill", text, "skills/sample-skill/SKILL.md"
            )
        }
        self.assertIn("OUTPUT.RUN_RESULT.PATH", codes)
        self.assertIn("OUTPUT.PATH.RUN_SCOPE", codes)
        self.assertIn("OUTPUT.PATH.GENERIC_NAME", codes)
        self.assertIn("OUTPUT.INLINE.STATUS", codes)

    def test_routed_skill_parser(self):
        text = "- F01 `first-skill`: first\n- F02 `second-skill`: second\n"
        self.assertEqual(
            {"first-skill", "second-skill"},
            set(module.ROUTED_SKILL_RE.findall(text)),
        )

    def test_warning_codes_are_stable(self):
        self.assertEqual(
            "SKILL.TOKEN.ROI_MISSING",
            module.warning_code("missing token ROI policy"),
        )
        self.assertEqual(
            "SKILL.REFERENCE.LOCAL_FILE_MISSING",
            module.warning_code("referenced local file missing: sample.json"),
        )

    def test_report_is_machine_readable(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "report.json"
            finding = module.Finding("TEST.CODE", "warning", "path", "message")
            module.write_report(
                path,
                "base",
                "head",
                {"sample-skill"},
                [finding],
            )
            text = path.read_text(encoding="utf-8")
            self.assertIn(module.REPORT_CONTRACT, text)
            self.assertIn('"warnings": 1', text)


if __name__ == "__main__":
    unittest.main()
