# Evidence Wayfinding Reserved Attestation Trust Boundary — PR 13

## Audit trigger

The post-Case-0A audit returned `CONDITIONAL PASS` and identified a P1 trust gap in `lat.reserved_evaluation_handoff.v1`:

```text
evaluated_by        = arbitrary non-empty string
attestation_hash    = arbitrary SHA-256-looking string
variant_bundle_ref  = arbitrary controlled:// string
```

The v1 validator could still accept those fields because it checked transport shape and lineage, not evaluator authorization or cryptographic content integrity.

This PR addresses only that failure boundary.

## Direction Investment Gate

```yaml
primary_value_path: current_product_delivery
direction_verdict: proceed
beneficiary: maintainers and controlled downstream evaluators
blocked_outcome: trustworthy real reserved evaluation evidence
existing_gap: >
  V1 can carry a safe attestation projection but cannot prove who signed it,
  whether the digest matches its content, whether the result is bound to the
  exact frozen blinded bundle, or whether a request nonce has already been used.
smallest_sufficient_change: >
  Add a v2 handoff generation with bundle digest, nonce/expiry, trusted evaluator
  public-key authorization, canonical digest verification, and Ed25519 signature
  verification while retaining v1 as an explicit compatibility entrance.
```

No new Skill, Agent, module, dashboard, mutation engine, or promotion surface is introduced.

## Compatibility decision

The trust changes add required fields and materially change attestation acceptance semantics. They are therefore published as:

```text
lat.reserved_evaluation_handoff.v2
schemas/capability/reserved-evaluation-handoff-record.v2.schema.json
```

V1 remains in the repository with its existing validator and fixtures for compatibility. New real reserved attestations must not use v1 as proof of trusted evaluator identity.

## V2 trust invariants

A request now freezes:

```text
issued_at
expires_at
request_nonce
variant_bundle_ref
variant_bundle_digest
```

An attestation must return the same nonce, reference, and digest and adds:

```text
evaluator_identity.evaluator_id
evaluator_identity.key_id
evaluator_identity.algorithm = ed25519
attestation_canonical_digest
signature
```

The validator independently recomputes the canonical digest and verifies the detached signature with a caller-supplied trusted evaluator public-key store.

## Evaluator authority

A trusted key record must authorize the exact:

```text
evaluator_id + key_id
evaluator_version
mission_anchor_ref
reserved_case_id
validity time window
```

Unknown, duplicate, inactive, expired, or unauthorized keys fail validation.

Only public keys enter the validation trust store. Private keys remain inside the controlled evaluator boundary.

## Content integrity

Canonical attestation material is the complete attestation record with only these two generated fields removed:

```text
payload.attestation_canonical_digest
payload.signature
```

The validator then performs:

```text
SHA-256(canonical bytes) == attestation_canonical_digest
Ed25519.verify(signature, canonical bytes, trusted public key)
```

Any post-signing change to result content, scope, evaluator identity, timestamps, evidence projections, bundle binding, or constraints invalidates the attestation.

## Bundle identity

A `controlled://` reference is no longer sufficient by itself. V2 requires a SHA-256 digest of the exact blinded variant bundle bytes.

The request builder can hash a local blinded bundle directly or accept a precomputed digest supplied by the controlled coordinator.

The attestation must return both the exact reference and exact digest from the request.

## Replay boundary

V2 requires a request nonce and expiry interval. A completed attestation must satisfy:

```text
issued_at <= evaluated_at <= expires_at
```

For any attestation-bearing stream, CLI validation also requires a consumed-nonce ledger. A previously consumed nonce is rejected.

The validator remains read-only and does not mutate the nonce ledger; downstream controlled infrastructure owns the transactional write after accepting an attestation.

## Synthetic fixtures

The repository includes only synthetic conformance material:

```text
tests/fixtures/evidence-wayfinding/reserved-evaluation/
  variant-bundle.synthetic.json
  trusted-evaluators.synthetic.json
  consumed-nonces.empty.txt
  handoff.synthetic-complete.v2.jsonl
```

The committed trust store contains only a synthetic public key. No private signing key is committed.

The signed fixture demonstrates digest/signature verification only and cannot be cited as real reserved evaluation evidence.

## Negative coverage

Tests explicitly reject:

- an arbitrary evaluator identity;
- an inactive trusted key;
- a changed frozen bundle digest;
- mutated signed attestation content;
- an arbitrary canonical digest;
- an arbitrary signature;
- request/attestation nonce drift;
- replay of an already consumed nonce;
- evaluation after request expiry;
- non-`controlled://` bundle references;
- unsafe or undersized request nonces.

## Deferred by design

This PR does not address the separate audit findings for:

- `downstream_observed` evidence completeness;
- `scoped_canary` requiring verified attestation evidence;
- a single authoritative Case bundle validator;
- deterministic attestation ingestion into Blind Challenge Execution;
- the Case 0 EV-002 placeholder hash;
- Case 0 documentation status drift;
- real Case 0B Senior Attention measurements.

Those remain separate reviewable changes so one PR corresponds to one failure boundary.

## Stop condition

After this PR, do not broaden the public evolution architecture. The next change should only address the observed-evidence gate, and real Case 0B still requires private downstream execution and human outcome evidence.
