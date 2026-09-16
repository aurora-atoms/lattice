from __future__ import annotations

import base64
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "sealed_directory_bundle.py"
SPEC = importlib.util.spec_from_file_location("sealed_directory_bundle", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SealedDirectoryBundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.passphrase = "correct horse battery staple for tests"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def make_source(self) -> Path:
        source = self.root / "source-demo"
        (source / "nested").mkdir(parents=True)
        (source / "empty").mkdir()
        (source / "README.md").write_text("demo\n", encoding="utf-8")
        (source / "nested" / "config.json").write_text(
            '{"ok":true}\n',
            encoding="utf-8",
        )
        (source / "nested" / "payload.bin").write_bytes(bytes(range(256)) * 40)
        (source / ".hidden").write_bytes(b"hidden")
        run = source / "run.sh"
        run.write_text("#!/bin/sh\necho demo\n", encoding="utf-8")
        run.chmod(0o755)
        return source

    def test_round_trip_complete_directory_without_compression(self) -> None:
        source = self.make_source()
        bundle = self.root / "sealed"
        restored = self.root / "restored"
        manifest = MODULE.seal_directory(
            source,
            bundle,
            self.passphrase,
            chunk_bytes=4096,
            schema_root=ROOT,
        )
        self.assertEqual(manifest["compression"], "none")
        self.assertGreater(manifest["sharding"]["count"], 1)
        self.assertEqual(manifest["sealed_entry_count"], 7)
        self.assertEqual(manifest["sealed_file_count"], 5)
        self.assertEqual(manifest["sealed_directory_count"], 2)
        result = MODULE.verify_bundle(bundle, self.passphrase, schema_root=ROOT)
        self.assertTrue(result["verified"])
        self.assertEqual(result["file_count"], 5)
        self.assertEqual(result["directory_count"], 2)
        MODULE.unseal_directory(
            bundle,
            restored,
            self.passphrase,
            schema_root=ROOT,
        )
        source_files = {
            p.relative_to(source).as_posix(): p.read_bytes()
            for p in source.rglob("*")
            if p.is_file()
        }
        restored_files = {
            p.relative_to(restored).as_posix(): p.read_bytes()
            for p in restored.rglob("*")
            if p.is_file()
        }
        self.assertEqual(restored_files, source_files)
        self.assertTrue((restored / "empty").is_dir())
        self.assertEqual((restored / "run.sh").stat().st_mode & 0o777, 0o755)

    def test_public_manifest_does_not_expose_source_paths_or_plaintext_hashes(self) -> None:
        source = self.make_source()
        bundle = self.root / "sealed"
        MODULE.seal_directory(source, bundle, self.passphrase, schema_root=ROOT)
        text = (bundle / MODULE.MANIFEST_NAME).read_text(encoding="utf-8")
        self.assertNotIn("README.md", text)
        self.assertNotIn("config.json", text)
        self.assertNotIn("source-demo", text)
        self.assertEqual(
            json.loads(text)["public_metadata_policy"],
            "no_source_paths_or_plaintext_hashes",
        )

    def test_wrong_passphrase_fails(self) -> None:
        source = self.make_source()
        bundle = self.root / "sealed"
        MODULE.seal_directory(source, bundle, self.passphrase, schema_root=ROOT)
        with self.assertRaisesRegex(MODULE.BundleError, "decryption failed"):
            MODULE.verify_bundle(
                bundle,
                "wrong passphrase but long enough",
                schema_root=ROOT,
            )

    def test_tampered_shard_fails_before_decryption(self) -> None:
        source = self.make_source()
        bundle = self.root / "sealed"
        manifest = MODULE.seal_directory(
            source,
            bundle,
            self.passphrase,
            schema_root=ROOT,
        )
        shard = bundle / manifest["shards"][0]["file"]
        raw = bytearray(
            base64.b64decode(
                shard.read_text(encoding="ascii").strip(),
                validate=True,
            )
        )
        raw[0] ^= 0x01
        shard.write_text(
            base64.b64encode(raw).decode("ascii") + "\n",
            encoding="ascii",
        )
        with self.assertRaisesRegex(MODULE.BundleError, "ciphertext hash mismatch"):
            MODULE.verify_bundle(bundle, self.passphrase, schema_root=ROOT)

    def test_rejects_output_inside_source(self) -> None:
        source = self.make_source()
        with self.assertRaisesRegex(MODULE.BundleError, "must not be inside"):
            MODULE.seal_directory(
                source,
                source / "bundle",
                self.passphrase,
                schema_root=ROOT,
            )

    def test_rejects_symlink(self) -> None:
        source = self.make_source()
        link = source / "nested" / "link"
        try:
            link.symlink_to(source / "README.md")
        except OSError:
            self.skipTest("symlinks unavailable")
        with self.assertRaisesRegex(MODULE.BundleError, "symlinks are not supported"):
            MODULE.seal_directory(
                source,
                self.root / "sealed",
                self.passphrase,
                schema_root=ROOT,
            )

    def test_rejects_path_traversal(self) -> None:
        for unsafe in ("../escape", "/absolute", "a/../escape", "./x"):
            with self.assertRaises(MODULE.BundleError):
                MODULE._safe_rel_path(unsafe)

    def test_manifest_schema_rejects_public_payload_policy(self) -> None:
        source = self.make_source()
        bundle = self.root / "sealed"
        manifest = MODULE.seal_directory(
            source,
            bundle,
            self.passphrase,
            schema_root=ROOT,
        )
        manifest["payload_policy"] = "public_payload_allowed"
        errors = MODULE.validate_manifest(manifest, schema_root=ROOT)
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
