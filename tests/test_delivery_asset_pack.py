from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_delivery_asset_pack.py"
SPEC = importlib.util.spec_from_file_location("validate_delivery_asset_pack", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
MANAGER_SCRIPT = ROOT / "scripts" / "validate_manager_claims.py"
MANAGER_SPEC = importlib.util.spec_from_file_location(
    "validate_manager_claims_for_asset_pack_tests", MANAGER_SCRIPT
)
assert MANAGER_SPEC and MANAGER_SPEC.loader
MANAGER_MODULE = importlib.util.module_from_spec(MANAGER_SPEC)
MANAGER_SPEC.loader.exec_module(MANAGER_MODULE)


def evidence() -> dict:
    return {
        "evidence_id": "ev-1",
        "evidence_type": "validation",
        "source_ref": "synthetic://validation",
        "relation": "supports",
        "observed_at": "2026-07-28T00:00:00Z",
        "source_authority": "synthetic fixture",
        "evidence_origin": "synthetic",
        "feature_delivery_case_id": "SYN-FDC-1",
        "summary": "Synthetic conformance evidence.",
        "integrity_sha256": None,
    }


def claim(claim_id: str, kind: str, classification: str = "OBSERVED") -> dict:
    return {
        "claim_id": claim_id,
        "classification": classification,
        "claim_kind": kind,
        "statement": (
            f"{kind} is not established."
            if classification == "UNKNOWN"
            else f"Synthetic {kind} conformance statement."
        ),
        "presentation": "unknown" if classification == "UNKNOWN" else "qualified",
        "evidence_refs": [] if classification == "UNKNOWN" else ["ev-1"],
        "evidence_origin": "synthetic",
        "scope": "SYN-FDC-1",
        "method": "Compared synthetic states." if classification == "DERIVED" else None,
        "judgment_owner": "synthetic reviewer" if classification == "JUDGED" else None,
        "unknown_reason": "No real downstream evidence." if classification == "UNKNOWN" else None,
        "limitations": ["Synthetic conformance only."],
        "approval_authority": None,
    }


def prepare_pack(root: Path) -> None:
    artifacts = root / "artifacts"
    reusable = root / "reusable-assets" / "asset-1"
    artifacts.mkdir(parents=True)
    reusable.mkdir(parents=True)
    (artifacts / "feature-delivery-case.json").write_text(
        json.dumps({"case_id": "SYN-FDC-1"}), encoding="utf-8"
    )
    (artifacts / "evidence-ledger.jsonl").write_text(
        json.dumps(evidence()) + "\n", encoding="utf-8"
    )
    (artifacts / "contribution-ledger.jsonl").write_text(
        json.dumps(
            {
                "contribution_id": "contrib-1",
                "feature_delivery_case_id": "SYN-FDC-1",
                "simulation_status": "synthetic_reference",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (artifacts / "reusable-asset-dossier.md").write_text(
        "# Synthetic Reusable Asset Dossier\n", encoding="utf-8"
    )
    brief = {
        "contract": "lat.manager-delivery-brief.v1",
        "contract_version": "1.0.0",
        "brief_id": "brief-1",
        "asset_pack_id": "pack-1",
        "simulation_status": "synthetic_reference",
        "downstream_adoption_status": "not_observed",
        "evidence_origin": "synthetic",
        "scope": "SYN-FDC-1",
        "version": "1.0.0",
        "claims": [
            claim("c-current", "current_delivery"),
            claim("c-asset", "reusable_asset"),
            claim("c-before", "before_state"),
            claim("c-after", "after_state", "DERIVED"),
            claim("c-next", "next_use", "JUDGED"),
        ],
        "human_challenge": {
            "challenge_present": True,
            "challenger_role": "synthetic reviewer",
            "challenge_summary": "Synthetic challenge.",
            "resulting_change_or_open_issue": "Synthetic scope narrowed.",
            "review_ref": "ev-1",
        },
        "known_limitations": ["Synthetic conformance only; no real use."],
        "unresolved_unknowns": ["Real adoption is unknown."],
        "next_use_entry": "Replace synthetic evidence in a private repository.",
        "manager_decision": None,
        "human_review_ref": None,
        "governance_approval_ref": None,
    }
    (artifacts / "manager-brief.json").write_text(
        json.dumps(brief), encoding="utf-8"
    )
    (artifacts / "manager-brief.md").write_text(
        MANAGER_MODULE.render_manager_brief_markdown(brief), encoding="utf-8"
    )
    reusable_records = {
        "asset-manifest.json": {
            "asset_id": "asset-1",
            "asset_version": "1.0.0",
            "feature_delivery_case_id": "SYN-FDC-1",
            "created_from_contribution_refs": ["contrib-1"],
            "activation_mode": "never_by_default",
            "simulation_status": "synthetic_reference",
            "downstream_adoption_status": "not_observed",
        },
        "change-proposal.json": {
            "proposal_id": "proposal-1",
            "asset_id": "asset-1",
            "simulation_status": "synthetic_reference",
            "downstream_adoption_status": "not_observed",
            "evidence_refs": ["ev-1"],
        },
        "review.json": {
            "proposal_id": "proposal-1",
            "asset_id": "asset-1",
            "simulation_status": "synthetic_reference",
            "downstream_adoption_status": "not_observed",
            "evidence_refs": ["ev-1"],
            "review_mode": "synthetic_conformance",
            "decision": "format_validated",
            "human_review_claim": False,
            "activation_approved": False,
        },
    }
    for name, value in reusable_records.items():
        (reusable / name).write_text(json.dumps(value), encoding="utf-8")
    (reusable / "usage-observations.jsonl").write_text("", encoding="utf-8")
    manifest = {
        "contract": "lat.delivery-evidence-asset-pack.v1",
        "contract_version": "1.0.0",
        "pack_id": "pack-1",
        "pack_version": "1.0.0",
        "simulation_status": "synthetic_reference",
        "downstream_adoption_status": "not_observed",
        "feature_delivery_case_id": "SYN-FDC-1",
        "accountable_owner": "synthetic fixture owner",
        "lattice_pin": {
            "ref": "v0.0.0-synthetic",
            "commit_sha": "0" * 40,
        },
        "public_capabilities": ["skill:lattice-governor@1.2.0"],
        "evidence_origin": "synthetic",
        "artifacts": {
            "feature_delivery_case": "artifacts/feature-delivery-case.json",
            "evidence_ledger": "artifacts/evidence-ledger.jsonl",
            "contribution_ledger": "artifacts/contribution-ledger.jsonl",
            "reusable_asset_dossier": "artifacts/reusable-asset-dossier.md",
            "manager_brief": "artifacts/manager-brief.json",
            "manager_brief_rendered": "artifacts/manager-brief.md",
            "validation_report": "artifacts/validation-report.json",
        },
        "reusable_assets": [
            {
                "asset_id": "asset-1",
                "asset_version": "1.0.0",
                "manifest_path": "reusable-assets/asset-1/asset-manifest.json",
                "change_proposal_path": "reusable-assets/asset-1/change-proposal.json",
                "review_path": "reusable-assets/asset-1/review.json",
                "usage_observations_path": "reusable-assets/asset-1/usage-observations.jsonl",
            }
        ],
        "generated_at": "2026-07-28T00:00:00Z",
    }
    (root / "asset-pack.manifest.json").write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    (artifacts / "validation-report.json").write_text(
        json.dumps(MODULE.validation_report([], manifest)), encoding="utf-8"
    )


class DeliveryAssetPackTests(unittest.TestCase):
    def test_valid_synthetic_contract_pack(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            prepare_pack(root)
            errors, _ = MODULE.validate_asset_pack(root, ROOT)
            self.assertEqual([], errors)

    def test_missing_required_artifact_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            prepare_pack(root)
            (root / "artifacts" / "reusable-asset-dossier.md").unlink()
            errors, _ = MODULE.validate_asset_pack(root, ROOT)
            self.assertTrue(any("missing artifacts/reusable" in item for item in errors))

    def test_case_identity_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            prepare_pack(root)
            (root / "artifacts" / "feature-delivery-case.json").write_text(
                json.dumps({"case_id": "OTHER"}), encoding="utf-8"
            )
            errors, _ = MODULE.validate_asset_pack(root, ROOT)
            self.assertTrue(any("case ID does not match" in item for item in errors))

    def test_missing_validation_report_fails_completed_pack(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            prepare_pack(root)
            (root / "artifacts" / "validation-report.json").unlink()
            errors, _ = MODULE.validate_asset_pack(root, ROOT)
            self.assertTrue(any("missing artifacts/validation-report" in item for item in errors))

    def test_cli_creates_and_revalidates_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            prepare_pack(root)
            report = root / "artifacts" / "validation-report.json"
            report.unlink()
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(root),
                    "--lattice-root",
                    str(ROOT),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            value = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual("pass", value["status"])
            errors, _ = MODULE.validate_asset_pack(root, ROOT)
            self.assertEqual([], errors)

    def test_evidence_case_identity_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            prepare_pack(root)
            record = evidence()
            record["feature_delivery_case_id"] = "OTHER"
            (root / "artifacts" / "evidence-ledger.jsonl").write_text(
                json.dumps(record) + "\n", encoding="utf-8"
            )
            errors, _ = MODULE.validate_asset_pack(root, ROOT)
            self.assertTrue(any("evidence[0]: feature delivery case mismatch" in item for item in errors))

    def test_manager_scope_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            prepare_pack(root)
            path = root / "artifacts" / "manager-brief.json"
            value = json.loads(path.read_text(encoding="utf-8"))
            value["scope"] = "OTHER"
            path.write_text(json.dumps(value), encoding="utf-8")
            errors, _ = MODULE.validate_asset_pack(root, ROOT)
            self.assertTrue(any("manager brief scope does not match" in item for item in errors))

    def test_rendered_brief_cannot_strengthen_claims(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            prepare_pack(root)
            path = root / "artifacts" / "manager-brief.md"
            path.write_text(
                path.read_text(encoding="utf-8")
                + "\nThe team adopted this capability.\n",
                encoding="utf-8",
            )
            errors, _ = MODULE.validate_asset_pack(root, ROOT)
            self.assertTrue(any("canonical structured projection" in item for item in errors))

    def test_reusable_asset_identity_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            prepare_pack(root)
            path = root / "reusable-assets" / "asset-1" / "asset-manifest.json"
            value = json.loads(path.read_text(encoding="utf-8"))
            value["asset_id"] = "other"
            path.write_text(json.dumps(value), encoding="utf-8")
            errors, _ = MODULE.validate_asset_pack(root, ROOT)
            self.assertTrue(any("asset manifest asset_id mismatch" in item for item in errors))

    def test_non_sentinel_pin_must_match_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            prepare_pack(root)
            path = root / "asset-pack.manifest.json"
            value = json.loads(path.read_text(encoding="utf-8"))
            value["lattice_pin"] = {"ref": "1" * 40, "commit_sha": "1" * 40}
            path.write_text(json.dumps(value), encoding="utf-8")
            errors, _ = MODULE.validate_asset_pack(root, ROOT)
            self.assertTrue(any("does not match the local" in item for item in errors))

    def test_synthetic_review_cannot_approve_activation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            prepare_pack(root)
            path = root / "reusable-assets" / "asset-1" / "review.json"
            value = json.loads(path.read_text(encoding="utf-8"))
            value["activation_approved"] = True
            path.write_text(json.dumps(value), encoding="utf-8")
            errors, _ = MODULE.validate_asset_pack(root, ROOT)
            self.assertTrue(any("cannot approve activation" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
