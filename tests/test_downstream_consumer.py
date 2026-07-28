from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_downstream_consumer.py"
SPEC = importlib.util.spec_from_file_location("validate_downstream_consumer", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

PROFILE_ID = "workspace:pr-review-template@1.0.0"
SKILL_ID = "skill:lattice-governor@1.2.0"
SHA = "1" * 40


def consumer() -> dict:
    return {
        "contract": "lat.downstream-consumer-manifest.v1",
        "contract_version": "1.0.0",
        "consumer_id": "private.delivery",
        "consumer_repository": {
            "repository_id": "private/delivery",
            "visibility": "private",
        },
        "simulation_status": "real_downstream",
        "lattice_source": {
            "repository": "https://github.com/aurora-atoms/lattice.git",
            "ref": "v1.0.0",
            "commit_sha": SHA,
        },
        "contract_versions": {
            "lat.downstream-consumer-manifest.v1": "1.0.0",
            "lat.private-capability-extension.v1": "1.0.0",
            "lat.delivery-evidence-asset-pack.v1": "1.0.0",
            "lat.manager-delivery-brief.v1": "1.0.0",
        },
        "capability_profiles": [
            {"capability_id": PROFILE_ID, "purpose": "bounded PR review"}
        ],
        "public_capabilities": [
            {"capability_id": SKILL_ID, "purpose": "public governance"}
        ],
        "private_extensions": [],
        "evidence_storage": {
            "root": "private/evidence",
            "classification": "real_restricted",
            "public_upload_prohibited": True,
        },
        "manager_projection": {
            "asset_pack_root": "private/manager-ready-delivery-asset-pack",
            "brief_path": "private/manager-ready-delivery-asset-pack/manager-brief.json",
            "human_review_required": True,
        },
        "validation_commands": [
            "python vendor/lattice/scripts/validate_downstream_consumer.py consumer.json",
            "python vendor/lattice/scripts/validate_delivery_asset_pack.py pack",
            "python vendor/lattice/scripts/validate_manager_claims.py brief.json --evidence-ledger evidence.jsonl",
        ],
        "compatibility_policy": {
            "missing_capability": "fail",
            "deprecated_capability": "human_review",
            "major_version_change": "human_review",
            "authority_change": "human_review",
        },
    }


def extension() -> dict:
    return {
        "contract": "lat.private-capability-extension.v1",
        "contract_version": "1.0.0",
        "extension_id": "private:delivery/governance@1.0.0",
        "extension_version": "1.0.0",
        "private_namespace": "delivery",
        "simulation_status": "real_downstream",
        "relationship": "extends",
        "public_capability_id": SKILL_ID,
        "scope": {
            "repositories": ["private/delivery"],
            "task_types": ["feature_delivery"],
            "excluded_uses": ["public publication"],
        },
        "required_permissions": ["read private evidence"],
        "authority_boundary": "Accountable private owner approves local conclusions.",
        "preserves_public_safety_boundaries": True,
        "compatibility": {
            "public_version_range": ">=1.2.0,<2.0.0",
            "on_incompatible": "human_review",
        },
        "governance_review_ref": None,
        "content_path": "extensions/delivery-governance.md",
    }


class DownstreamConsumerTests(unittest.TestCase):
    def validate(self, value: dict, root: Path) -> list[str]:
        return MODULE.validate_consumer(
            value, ROOT, root, validate_extension_files=True
        )

    def test_valid_consumer_and_extension(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            ext = extension()
            path = root / "extensions" / "governance.json"
            path.parent.mkdir()
            path.write_text(json.dumps(ext), encoding="utf-8")
            value = consumer()
            value["private_extensions"] = [
                {"extension_id": ext["extension_id"], "manifest_path": "extensions/governance.json"}
            ]
            self.assertEqual([], self.validate(value, root))

    def test_floating_ref_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            value = consumer()
            value["lattice_source"]["ref"] = "main"
            errors = self.validate(value, Path(temp))
            self.assertTrue(any("immutable" in item for item in errors))

    def test_unknown_capability_version_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            value = consumer()
            value["public_capabilities"][0]["capability_id"] = (
                "skill:lattice-governor@9.9.9"
            )
            errors = self.validate(value, Path(temp))
            self.assertTrue(any("does not exist" in item for item in errors))

    def test_unbounded_wildcard_selection_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            value = consumer()
            value["public_capabilities"][0]["capability_id"] = "skill:*@1.0.0"
            errors = self.validate(value, Path(temp))
            self.assertTrue(any("exact version" in item for item in errors))

    def test_private_extension_cannot_use_public_namespace(self) -> None:
        capabilities = MODULE.canonical_capabilities(ROOT)
        value = extension()
        value["extension_id"] = "private:lat/governance@1.0.0"
        value["private_namespace"] = "lat"
        errors = MODULE.validate_extension(value, capabilities)
        self.assertTrue(any("namespace is prohibited" in item for item in errors))

    def test_override_requires_governance_review(self) -> None:
        capabilities = MODULE.canonical_capabilities(ROOT)
        value = extension()
        value["relationship"] = "overrides"
        errors = MODULE.validate_extension(value, capabilities)
        self.assertTrue(any("governance_review_ref" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
