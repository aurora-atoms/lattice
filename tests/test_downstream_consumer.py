from __future__ import annotations

import importlib.util
import json
import subprocess
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
            "lat.canonical-capability-manifest.v1": "1.0.0",
            "lat.downstream-adoption-lifecycle.v1": "1.0.0",
            "lat.downstream-consumer-manifest.v1": "1.0.0",
            "lat.delivery-asset-pack-validation-report.v1": "1.0.0",
            "lat.delivery-evidence-asset-pack.v1": "1.0.0",
            "lat.evidence-claim.v1": "1.0.0",
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
            value["contract_versions"][
                "lat.private-capability-extension.v1"
            ] = "1.0.0"
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

    def test_missing_consumed_contract_version_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            value = consumer()
            del value["contract_versions"]["lat.evidence-claim.v1"]
            errors = self.validate(value, Path(temp))
            self.assertTrue(any("lat.evidence-claim.v1" in item for item in errors))

    def test_checkout_commit_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            value = consumer()
            errors = MODULE.validate_consumer(
                value,
                ROOT,
                Path(temp),
                validate_extension_files=False,
                verify_checkout_pin=True,
            )
            self.assertTrue(any("does not match the local" in item for item in errors))

    def test_checkout_commit_pin_resolves_locally(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            checkout_sha = subprocess.run(
                ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            value = consumer()
            value["lattice_source"]["ref"] = checkout_sha
            value["lattice_source"]["commit_sha"] = checkout_sha
            errors = MODULE.validate_consumer(
                value,
                ROOT,
                Path(temp),
                validate_extension_files=False,
                verify_checkout_pin=True,
            )
            self.assertEqual([], errors)

    def test_only_explicit_synthetic_sentinel_skips_checkout_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            value = consumer()
            value["simulation_status"] = "synthetic_reference"
            value["evidence_storage"]["classification"] = "synthetic"
            value["lattice_source"]["ref"] = "v0.0.0-synthetic"
            value["lattice_source"]["commit_sha"] = "0" * 40
            errors = MODULE.validate_consumer(
                value,
                ROOT,
                Path(temp),
                validate_extension_files=False,
                verify_checkout_pin=True,
            )
            self.assertEqual([], errors)

            value["lattice_source"]["ref"] = "v1.0.0"
            value["lattice_source"]["commit_sha"] = SHA
            errors = MODULE.validate_consumer(
                value,
                ROOT,
                Path(temp),
                validate_extension_files=False,
                verify_checkout_pin=True,
            )
            self.assertTrue(any("does not match the local" in item for item in errors))

    def test_simulation_and_evidence_classification_must_agree(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            value = consumer()
            value["simulation_status"] = "synthetic_reference"
            errors = self.validate(value, Path(temp))
            self.assertTrue(any("must use synthetic classification" in item for item in errors))

            value = consumer()
            value["evidence_storage"]["classification"] = "synthetic"
            errors = self.validate(value, Path(temp))
            self.assertTrue(any("cannot use synthetic classification" in item for item in errors))

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

    def test_extension_simulation_must_match_consumer(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            ext = extension()
            ext["simulation_status"] = "synthetic_reference"
            path = root / "extensions" / "governance.json"
            path.parent.mkdir()
            path.write_text(json.dumps(ext), encoding="utf-8")
            value = consumer()
            value["private_extensions"] = [
                {
                    "extension_id": ext["extension_id"],
                    "manifest_path": "extensions/governance.json",
                }
            ]
            value["contract_versions"][
                "lat.private-capability-extension.v1"
            ] = "1.0.0"
            errors = self.validate(value, root)
            self.assertTrue(any("differs from the consumer" in item for item in errors))

    def test_manager_brief_path_must_stay_inside_pack(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            value = consumer()
            value["manager_projection"]["brief_path"] = "private/other/brief.json"
            errors = self.validate(value, Path(temp))
            self.assertTrue(any("brief_path must be inside" in item for item in errors))

    def test_declared_commands_must_include_all_local_validators(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            value = consumer()
            value["validation_commands"] = ["true", "true", "true"]
            errors = self.validate(value, Path(temp))
            self.assertTrue(any("missing required local validators" in item for item in errors))

    def test_real_evidence_cannot_write_inside_lattice_checkout(self) -> None:
        value = consumer()
        errors = MODULE.validate_consumer(
            value,
            ROOT,
            ROOT,
            validate_extension_files=False,
        )
        self.assertTrue(any("public Lattice checkout" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
