from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_delivery_asset_pack.py"
SPEC = importlib.util.spec_from_file_location("validate_delivery_asset_pack", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


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
        "statement": f"Synthetic {kind} conformance statement.",
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
    for name in ("asset-manifest.json", "change-proposal.json", "review.json"):
        (reusable / name).write_text("{}\n", encoding="utf-8")
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
        "lattice_pin": {"ref": "v1.0.0", "commit_sha": "1" * 40},
        "public_capabilities": ["skill:lattice-governor@1.2.0"],
        "evidence_origin": "synthetic",
        "artifacts": {
            "feature_delivery_case": "artifacts/feature-delivery-case.json",
            "evidence_ledger": "artifacts/evidence-ledger.jsonl",
            "contribution_ledger": "artifacts/contribution-ledger.jsonl",
            "reusable_asset_dossier": "artifacts/reusable-asset-dossier.md",
            "manager_brief": "artifacts/manager-brief.json",
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


if __name__ == "__main__":
    unittest.main()
