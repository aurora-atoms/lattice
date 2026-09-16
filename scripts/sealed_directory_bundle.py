#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Seal and restore a directory as encrypted, non-compressed text shards.

The format is intended for authorized private downstream repositories. Public
Lattice may host the format, validator, and synthetic tests, but not real
private payload shards.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import shutil
import struct
import sys
import uuid
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from jsonschema import Draft202012Validator

FORMAT = "lat.sealed-directory-bundle.v1"
MAGIC = b"LAT-SEAL-DIR-V1\n"
DEFAULT_CHUNK_BYTES = 256 * 1024
MIN_CHUNK_BYTES = 4 * 1024
MAX_CHUNK_BYTES = 16 * 1024 * 1024
SCRYPT_N = 2**15
SCRYPT_R = 8
SCRYPT_P = 1
KEY_BYTES = 32
SALT_BYTES = 16
NONCE_BYTES = 12
MANIFEST_NAME = "bundle.manifest.json"
SHARD_PREFIX = "part-"
SHARD_SUFFIX = ".lsb64"


class BundleError(ValueError):
    """Raised when a sealed bundle is invalid or cannot be safely processed."""


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _derive_key(passphrase: str, salt: bytes) -> bytes:
    raw = passphrase.encode("utf-8")
    if len(raw) < 16:
        raise BundleError("passphrase must be at least 16 UTF-8 bytes")
    kdf = Scrypt(
        salt=salt,
        length=KEY_BYTES,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
    )
    return kdf.derive(raw)


def _validate_chunk_bytes(value: int) -> None:
    if not MIN_CHUNK_BYTES <= value <= MAX_CHUNK_BYTES:
        raise BundleError(
            f"chunk_bytes must be between {MIN_CHUNK_BYTES} and {MAX_CHUNK_BYTES}"
        )


def _safe_rel_path(raw: str) -> PurePosixPath:
    if not isinstance(raw, str) or not raw:
        raise BundleError("bundle path must be a non-empty string")
    path = PurePosixPath(raw)
    if path.is_absolute():
        raise BundleError(f"absolute path is not allowed: {raw}")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise BundleError(f"unsafe relative path: {raw}")
    normalized = path.as_posix()
    if normalized != raw:
        raise BundleError(f"non-canonical relative path: {raw}")
    return path


def _iter_source_files(source: Path) -> Iterable[tuple[str, bytes]]:
    if not source.is_dir():
        raise BundleError(f"source is not a directory: {source}")
    for path in sorted(
        source.rglob("*"),
        key=lambda item: item.relative_to(source).as_posix(),
    ):
        if path.is_symlink():
            raise BundleError(f"symlinks are not supported: {path}")
        if path.is_dir():
            continue
        if not path.is_file():
            raise BundleError(f"unsupported filesystem entry: {path}")
        rel = path.relative_to(source).as_posix()
        _safe_rel_path(rel)
        yield rel, path.read_bytes()


def _encode_stream(source: Path) -> tuple[bytes, int]:
    entries = list(_iter_source_files(source))
    meta = {
        "format": FORMAT,
        "root_label": source.name,
        "file_count": len(entries),
        "encoding": "framed-bytes",
        "compression": "none",
    }
    meta_bytes = _canonical_json(meta)
    out = bytearray(MAGIC)
    out.extend(struct.pack(">I", len(meta_bytes)))
    out.extend(meta_bytes)
    for rel, data in entries:
        header = {
            "path": rel,
            "size": len(data),
            "sha256": _sha256(data),
        }
        header_bytes = _canonical_json(header)
        out.extend(struct.pack(">I", len(header_bytes)))
        out.extend(header_bytes)
        out.extend(data)
    return bytes(out), len(entries)


def _read_u32(data: bytes, offset: int) -> tuple[int, int]:
    end = offset + 4
    if end > len(data):
        raise BundleError("truncated frame length")
    return struct.unpack(">I", data[offset:end])[0], end


def _parse_stream(data: bytes) -> tuple[dict[str, Any], list[tuple[str, bytes]]]:
    if not data.startswith(MAGIC):
        raise BundleError("invalid sealed directory stream magic")
    offset = len(MAGIC)
    meta_len, offset = _read_u32(data, offset)
    if meta_len <= 0 or offset + meta_len > len(data):
        raise BundleError("invalid stream metadata length")
    try:
        meta = json.loads(data[offset : offset + meta_len].decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BundleError(f"invalid stream metadata: {exc}") from exc
    offset += meta_len
    if not isinstance(meta, dict) or meta.get("format") != FORMAT:
        raise BundleError("stream format mismatch")
    if meta.get("compression") != "none":
        raise BundleError("compressed streams are not supported by this format")
    expected_count = meta.get("file_count")
    if not isinstance(expected_count, int) or expected_count < 0:
        raise BundleError("invalid file_count in stream metadata")

    entries: list[tuple[str, bytes]] = []
    seen: set[str] = set()
    for _ in range(expected_count):
        header_len, offset = _read_u32(data, offset)
        if header_len <= 0 or offset + header_len > len(data):
            raise BundleError("invalid file header length")
        try:
            header = json.loads(data[offset : offset + header_len].decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise BundleError(f"invalid file header: {exc}") from exc
        offset += header_len
        if not isinstance(header, dict) or set(header) != {"path", "size", "sha256"}:
            raise BundleError("file header fields are invalid")
        rel = _safe_rel_path(header["path"]).as_posix()
        if rel in seen:
            raise BundleError(f"duplicate path in stream: {rel}")
        seen.add(rel)
        size = header["size"]
        digest = header["sha256"]
        if not isinstance(size, int) or size < 0:
            raise BundleError(f"invalid file size for {rel}")
        if not isinstance(digest, str) or len(digest) != 64:
            raise BundleError(f"invalid file sha256 for {rel}")
        end = offset + size
        if end > len(data):
            raise BundleError(f"truncated file payload for {rel}")
        payload = data[offset:end]
        offset = end
        if _sha256(payload) != digest:
            raise BundleError(f"file hash mismatch for {rel}")
        entries.append((rel, payload))
    if offset != len(data):
        raise BundleError("unexpected trailing bytes in stream")
    return meta, entries


def _aad(bundle_id: str, index: int, count: int) -> bytes:
    return f"{FORMAT}|{bundle_id}|{index}|{count}".encode("ascii")


def _schema_path(root: Path | None = None) -> Path:
    if root is not None:
        return root / "schemas" / "downstream" / "sealed-directory-bundle.v1.schema.json"
    return (
        Path(__file__).resolve().parents[1]
        / "schemas"
        / "downstream"
        / "sealed-directory-bundle.v1.schema.json"
    )


def validate_manifest(
    manifest: dict[str, Any],
    *,
    schema_root: Path | None = None,
) -> list[str]:
    schema_file = _schema_path(schema_root)
    try:
        schema = json.loads(schema_file.read_text(encoding="utf-8"))
    except OSError as exc:
        return [f"cannot read bundle schema: {exc}"]
    validator = Draft202012Validator(schema)
    errors: list[str] = []
    for error in sorted(
        validator.iter_errors(manifest),
        key=lambda item: list(item.path),
    ):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"{location}: {error.message}")
    return errors


def _prepare_output_dir(output: Path, *, replace: bool) -> None:
    if output.exists():
        if not replace:
            raise BundleError(f"output already exists: {output}")
        if output.is_symlink():
            raise BundleError(f"refusing to replace symlink output: {output}")
        if output.is_dir():
            shutil.rmtree(output)
        else:
            output.unlink()
    output.parent.mkdir(parents=True, exist_ok=True)


def seal_directory(
    source: Path,
    output: Path,
    passphrase: str,
    *,
    chunk_bytes: int = DEFAULT_CHUNK_BYTES,
    replace: bool = False,
    schema_root: Path | None = None,
) -> dict[str, Any]:
    source = source.resolve()
    output = output.resolve()
    _validate_chunk_bytes(chunk_bytes)
    if source == output or source in output.parents:
        raise BundleError("bundle output must not be inside the source directory")
    stream, file_count = _encode_stream(source)
    chunks = [
        stream[index : index + chunk_bytes]
        for index in range(0, len(stream), chunk_bytes)
    ]
    if not chunks:
        chunks = [b""]

    salt = os.urandom(SALT_BYTES)
    key = _derive_key(passphrase, salt)
    bundle_id = uuid.uuid4().hex
    aes = AESGCM(key)
    count = len(chunks)
    shards: list[dict[str, Any]] = []
    encoded_shards: list[tuple[str, str]] = []
    for index, chunk in enumerate(chunks):
        nonce = os.urandom(NONCE_BYTES)
        ciphertext = aes.encrypt(nonce, chunk, _aad(bundle_id, index, count))
        filename = f"{SHARD_PREFIX}{index + 1:06d}{SHARD_SUFFIX}"
        shard_text = base64.b64encode(ciphertext).decode("ascii") + "\n"
        encoded_shards.append((filename, shard_text))
        shards.append(
            {
                "index": index,
                "file": filename,
                "nonce_b64": base64.b64encode(nonce).decode("ascii"),
                "ciphertext_sha256": _sha256(ciphertext),
                "ciphertext_bytes": len(ciphertext),
            }
        )

    manifest = {
        "schema": FORMAT,
        "bundle_id": bundle_id,
        "payload_policy": "private_downstream_only",
        "encoding": "base64",
        "compression": "none",
        "cipher": {
            "name": "AES-256-GCM",
            "kdf": {
                "name": "scrypt",
                "salt_b64": base64.b64encode(salt).decode("ascii"),
                "n": SCRYPT_N,
                "r": SCRYPT_R,
                "p": SCRYPT_P,
                "length": KEY_BYTES,
            },
        },
        "sharding": {
            "plaintext_chunk_bytes": chunk_bytes,
            "count": count,
        },
        "shards": shards,
        "sealed_file_count": file_count,
        "public_metadata_policy": "no_source_paths_or_plaintext_hashes",
    }
    errors = validate_manifest(manifest, schema_root=schema_root)
    if errors:
        raise BundleError(
            "generated manifest failed schema validation: " + "; ".join(errors)
        )

    _prepare_output_dir(output, replace=replace)
    tmp = output.with_name(output.name + f".tmp-{uuid.uuid4().hex}")
    tmp.mkdir(parents=False)
    try:
        (tmp / MANIFEST_NAME).write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
        )
        for filename, text in encoded_shards:
            (tmp / filename).write_text(text, encoding="ascii")
        tmp.replace(output)
    except Exception:
        shutil.rmtree(tmp, ignore_errors=True)
        raise
    return manifest


def _load_manifest(
    bundle: Path,
    *,
    schema_root: Path | None = None,
) -> dict[str, Any]:
    manifest_path = bundle / MANIFEST_NAME
    try:
        value = json.loads(manifest_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise BundleError(f"cannot read bundle manifest: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise BundleError(f"invalid bundle manifest JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise BundleError("bundle manifest must be an object")
    errors = validate_manifest(value, schema_root=schema_root)
    if errors:
        raise BundleError("bundle manifest validation failed: " + "; ".join(errors))
    return value


def _decrypt_stream(
    bundle: Path,
    passphrase: str,
    *,
    schema_root: Path | None = None,
) -> bytes:
    bundle = bundle.resolve()
    manifest = _load_manifest(bundle, schema_root=schema_root)
    kdf = manifest["cipher"]["kdf"]
    if (kdf["n"], kdf["r"], kdf["p"], kdf["length"]) != (
        SCRYPT_N,
        SCRYPT_R,
        SCRYPT_P,
        KEY_BYTES,
    ):
        raise BundleError("unsupported scrypt parameters")
    try:
        salt = base64.b64decode(kdf["salt_b64"], validate=True)
    except ValueError as exc:
        raise BundleError("invalid scrypt salt encoding") from exc
    if len(salt) != SALT_BYTES:
        raise BundleError("invalid scrypt salt length")
    key = _derive_key(passphrase, salt)
    aes = AESGCM(key)
    bundle_id = manifest["bundle_id"]
    count = manifest["sharding"]["count"]
    shards = manifest["shards"]
    if len(shards) != count:
        raise BundleError("manifest shard count mismatch")

    plaintext = bytearray()
    for expected_index, shard in enumerate(shards):
        if shard["index"] != expected_index:
            raise BundleError("manifest shard ordering/index mismatch")
        shard_path = bundle / shard["file"]
        try:
            encoded = shard_path.read_text(encoding="ascii").strip()
        except OSError as exc:
            raise BundleError(f"cannot read shard {shard['file']}: {exc}") from exc
        try:
            ciphertext = base64.b64decode(encoded, validate=True)
            nonce = base64.b64decode(shard["nonce_b64"], validate=True)
        except (ValueError, UnicodeEncodeError) as exc:
            raise BundleError(f"invalid base64 in shard {shard['file']}") from exc
        if len(nonce) != NONCE_BYTES:
            raise BundleError(f"invalid nonce length for shard {shard['file']}")
        if len(ciphertext) != shard["ciphertext_bytes"]:
            raise BundleError(f"ciphertext size mismatch for shard {shard['file']}")
        if _sha256(ciphertext) != shard["ciphertext_sha256"]:
            raise BundleError(f"ciphertext hash mismatch for shard {shard['file']}")
        try:
            chunk = aes.decrypt(
                nonce,
                ciphertext,
                _aad(bundle_id, expected_index, count),
            )
        except InvalidTag as exc:
            raise BundleError(
                "decryption failed: wrong passphrase or tampered bundle"
            ) from exc
        plaintext.extend(chunk)
    return bytes(plaintext)


def verify_bundle(
    bundle: Path,
    passphrase: str,
    *,
    schema_root: Path | None = None,
) -> dict[str, Any]:
    stream = _decrypt_stream(bundle, passphrase, schema_root=schema_root)
    meta, entries = _parse_stream(stream)
    return {
        "schema": FORMAT,
        "verified": True,
        "file_count": len(entries),
        "root_label": meta["root_label"],
    }


def unseal_directory(
    bundle: Path,
    output: Path,
    passphrase: str,
    *,
    replace: bool = False,
    schema_root: Path | None = None,
) -> dict[str, Any]:
    stream = _decrypt_stream(bundle, passphrase, schema_root=schema_root)
    meta, entries = _parse_stream(stream)
    output = output.resolve()
    _prepare_output_dir(output, replace=replace)
    tmp = output.with_name(output.name + f".tmp-{uuid.uuid4().hex}")
    tmp.mkdir(parents=False)
    try:
        for rel, payload in entries:
            rel_path = _safe_rel_path(rel)
            target = tmp.joinpath(*rel_path.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
        tmp.replace(output)
    except Exception:
        shutil.rmtree(tmp, ignore_errors=True)
        raise
    return {
        "schema": FORMAT,
        "restored": True,
        "file_count": len(entries),
        "root_label": meta["root_label"],
    }


def _passphrase_from_env(name: str) -> str:
    value = os.environ.get(name)
    if value is None:
        raise BundleError(
            f"required passphrase environment variable is not set: {name}"
        )
    return value


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    seal = sub.add_parser("seal", help="seal a directory into encrypted text shards")
    seal.add_argument("source", type=Path)
    seal.add_argument("output", type=Path)
    seal.add_argument("--passphrase-env", default="LATTICE_BUNDLE_PASSPHRASE")
    seal.add_argument("--chunk-bytes", type=int, default=DEFAULT_CHUNK_BYTES)
    seal.add_argument("--replace", action="store_true")

    verify = sub.add_parser(
        "verify",
        help="decrypt and verify a sealed bundle without extraction",
    )
    verify.add_argument("bundle", type=Path)
    verify.add_argument("--passphrase-env", default="LATTICE_BUNDLE_PASSPHRASE")

    unseal = sub.add_parser("unseal", help="restore a sealed bundle into a directory")
    unseal.add_argument("bundle", type=Path)
    unseal.add_argument("output", type=Path)
    unseal.add_argument("--passphrase-env", default="LATTICE_BUNDLE_PASSPHRASE")
    unseal.add_argument("--replace", action="store_true")
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    try:
        passphrase = _passphrase_from_env(args.passphrase_env)
        if args.command == "seal":
            result = seal_directory(
                args.source,
                args.output,
                passphrase,
                chunk_bytes=args.chunk_bytes,
                replace=args.replace,
            )
            print(
                json.dumps(
                    {
                        "sealed": True,
                        "bundle_id": result["bundle_id"],
                        "shards": result["sharding"]["count"],
                    }
                )
            )
        elif args.command == "verify":
            print(
                json.dumps(
                    verify_bundle(args.bundle, passphrase),
                    sort_keys=True,
                )
            )
        elif args.command == "unseal":
            print(
                json.dumps(
                    unseal_directory(
                        args.bundle,
                        args.output,
                        passphrase,
                        replace=args.replace,
                    ),
                    sort_keys=True,
                )
            )
        else:  # pragma: no cover
            parser.error("unknown command")
    except (BundleError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
