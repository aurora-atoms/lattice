# Sealed Directory Bundle v1

## Purpose

`lat.sealed-directory-bundle.v1` is a small transport/storage format for an authorized private downstream repository that needs to preserve an entire directory tree as a set of reviewable Git-friendly shard files without using ZIP, tar.gz, or another compressed archive.

It is intentionally a **script + schema**, not a Skill, Agent, capability identity, or public asset-distribution mechanism.

## Direction fit

Primary value path: `strategic_asset`.

The bounded outcome is a verifiable encrypted directory-transfer protocol that can be reused by private downstream repositories. Existing Delivery Asset Pack contracts validate structured delivery evidence; they do not seal arbitrary directory trees. This protocol stays candidate-scoped as deterministic tooling and does not claim team adoption, business value, or a new Lattice capability.

## Public-private boundary

Public Lattice owns only this format, its implementation, schema, documentation, and synthetic tests.

**Do not commit a real sealed payload to public Lattice.** Encryption protects confidentiality against readers who do not possess the key; it does not grant permission to publish employer, client, private-repository, or otherwise restricted source material. A `.lsb64` shard created from real private source remains a private downstream artifact.

The public-private boundary validator rejects committed `.lsb64` payload shards in Lattice. Synthetic tests generate shards only in temporary directories.

## Shape

A sealed bundle is a directory, not a single archive:

```text
sealed-demo/
  bundle.manifest.json
  part-000001.lsb64
  part-000002.lsb64
  part-000003.lsb64
  ...
```

The source directory is serialized into a deterministic, **uncompressed** framed byte stream. The stream contains the original relative paths, file sizes, SHA-256 digests, and bytes. That stream is split into plaintext chunks, and each chunk is independently sealed with AES-256-GCM.

Each encrypted shard is Base64-encoded so it remains an ordinary text file for Git-compatible private repositories. Base64 is encoding, not compression.

The plaintext file catalog is inside the encrypted stream. The public manifest intentionally contains no source paths and no plaintext file hashes.

## Cryptography

```text
passphrase
  -> scrypt(n=32768, r=8, p=1, length=32, random 16-byte salt)
  -> 256-bit key
  -> AES-256-GCM per shard
```

Each shard uses a fresh random 12-byte nonce. Authenticated additional data binds the ciphertext to:

```text
format + bundle_id + shard_index + shard_count
```

The manifest records the nonce, ciphertext byte count, and ciphertext SHA-256 for every shard. AES-GCM provides authenticated decryption; the ciphertext hash provides an earlier corruption check and stable shard addressing.

The passphrase is never written to the bundle. The CLI reads it from an environment variable so it is not placed in shell history or process arguments.

## Private downstream usage

Install the pinned Lattice validation dependencies in the authorized private repository:

```bash
python -m pip install -r vendor/lattice/requirements-validation.txt
```

Set a strong passphrase through an approved secret source. The examples use an environment variable only to show the interface:

```bash
export LATTICE_BUNDLE_PASSPHRASE='<secret-from-approved-store>'
```

Seal a directory:

```bash
python vendor/lattice/scripts/sealed_directory_bundle.py seal \
  path/to/private-demo \
  private/bundles/private-demo \
  --passphrase-env LATTICE_BUNDLE_PASSPHRASE
```

Verify without extracting:

```bash
python vendor/lattice/scripts/sealed_directory_bundle.py verify \
  private/bundles/private-demo \
  --passphrase-env LATTICE_BUNDLE_PASSPHRASE
```

Restore the original directory tree:

```bash
python vendor/lattice/scripts/sealed_directory_bundle.py unseal \
  private/bundles/private-demo \
  restored/private-demo \
  --passphrase-env LATTICE_BUNDLE_PASSPHRASE
```

Use `--replace` only when replacing a known output location is intentional. The tool refuses to create the bundle inside the source directory and refuses symlink entries.

## Verification contract

A valid round trip must prove:

1. the manifest validates against `schemas/downstream/sealed-directory-bundle.v1.schema.json`;
2. `compression` is exactly `none`;
3. the manifest exposes no source-relative paths or plaintext file hashes;
4. every shard has the expected index, name, nonce size, ciphertext size, and ciphertext hash;
5. the passphrase-derived key authenticates every AES-GCM shard;
6. every restored relative path is canonical and cannot escape the destination root;
7. every restored file matches the encrypted inner size and SHA-256;
8. the restored file tree is byte-for-byte equal to the source tree.

Negative tests cover wrong passphrases, shard tampering, path traversal, source-contained output, symlinks, and attempts to change `payload_policy` to a public value.

## Non-goals

- compression or storage-size optimization;
- hiding that a bundle exists or how many shards/files it contains;
- key escrow, recovery, rotation, or enterprise secret management;
- authorization to move data across repository or employer boundaries;
- public distribution of encrypted private source;
- replacement for repository access control, licensing, IP review, or data classification.

## Source-governance rule

Before sealing a real directory, the owning private repository must already permit the intended destination and recipients. When permission or ownership is unknown, stop. Do not treat encryption as a workaround for a source-governance restriction.
