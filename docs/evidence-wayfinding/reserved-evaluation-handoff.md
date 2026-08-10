# Controlled Reserved Evaluation Handoff

## Decision

Blind Challenge v1 deliberately stops when its reserved oracle is unavailable to the public repository. The handoff between the public repository and a controlled private evaluator therefore has two distinct contract generations:

```text
v1 = compatibility / transport shape
v2 = trusted-attestation boundary required for real reserved evidence
```

New real reserved evaluations must use:

```text
lat.reserved_evaluation_handoff.v2
schemas/capability/reserved-evaluation-handoff-record.v2.schema.json
```

The v1 schema and validator remain available so existing synthetic fixtures and downstream experiments do not break silently. A v1 attestation is **not** sufficient evidence for a real Blind Challenge decision because it does not authenticate evaluator identity or bind the attestation cryptographically to its content and blinded bundle.

This protocol is not a new Lattice module, Agent, Skill, or second delivery lifecycle. It remains a JSONL handoff around the existing Harness Mutation Candidate and Blind Challenge Execution contracts.

## Trust zones

```text
public repository
  candidate + frozen plan + public preflight
        |
        | eval.reserved_request v2
        v
controlled private evaluator
  reserved case + oracle + blinded A/B execution
        |
        | signed eval.reserved_attestation v2
        v
public repository
  verifies safe attestation projection only
```

The public repository may know candidate identity, frozen target/allocation hashes, evaluator protocol version, metrics, an opaque `controlled://` bundle reference, and the SHA-256 digest of the exact blinded bundle bytes.

It must not receive raw reserved input, oracle content, private source artifacts, the A/B-to-incumbent/challenger mapping, private signing keys, or a promotion decision produced by the evaluator.

## Why v2 is required

V1 verified shape and lineage but allowed an attestation to contain any non-empty evaluator string and any SHA-256-looking attestation hash. That meant a record could be structurally valid without proving:

- which authorized evaluator signed it;
- whether the attestation hash was actually derived from the record;
- whether the result referred to the exact blinded bundle frozen at request time;
- whether the request was still valid;
- whether the same request nonce had already been consumed.

V2 closes those gaps without moving the oracle or private evidence into the public repository.

## Request v2

A v2 request carries the frozen lineage plus:

```text
issued_at
expires_at
request_nonce
variant_bundle_ref
variant_bundle_digest
```

`variant_bundle_digest` is the SHA-256 digest of the exact blinded bundle bytes. The coordinator may compute it directly from a local bundle file with:

```text
scripts/prepare_reserved_evaluation_request_v2.py
```

The request nonce is supplied by the trusted coordinator and must be unique for the intended evaluation attempt. The public repository does not generate or store the private bundle itself.

The current Case 0 v2 request remains explicitly synthetic:

```text
examples/evidence-wayfinding/case-0-schema-parity/
  reserved-evaluation-handoff.request.v2.synthetic.jsonl
```

It demonstrates the contract only. It is not a real reserved evaluation.

## Attestation v2

A completed attestation must include:

```text
evaluator_identity:
  evaluator_id
  key_id
  algorithm = ed25519

evaluated_at
request_nonce
variant_bundle_ref
variant_bundle_digest
reserved_case_result
attestation_ref
attestation_canonical_digest
signature
```

The evaluator identity is accepted only when the `(evaluator_id, key_id)` pair exists in a caller-supplied trusted public-key store, is active for the evaluation timestamp, and is authorized for the evaluator version, mission anchor, and reserved case.

The trusted key store contains public keys only. Private signing keys stay in the controlled evaluator boundary.

## Canonical digest and signature

The validator creates canonical JSON from the complete attestation record after removing only:

```text
payload.attestation_canonical_digest
payload.signature
```

Canonicalization uses sorted keys, compact JSON separators, UTF-8 encoding, and no hidden reasoning fields. It then:

```text
canonical attestation bytes
  -> SHA-256
  -> compare with attestation_canonical_digest

canonical attestation bytes
  + trusted evaluator Ed25519 public key
  + detached signature
  -> verify
```

Changing evaluator identity, result content, evidence references, bundle digest, scope, timestamps, or constraints after signing therefore invalidates the attestation.

## Bundle binding

Both request and attestation must carry exactly the same:

```text
variant_bundle_ref
variant_bundle_digest
request_nonce
```

The opaque reference identifies the controlled object. The digest binds the evaluation result to the exact bytes that the coordinator froze before evaluation.

A reference string alone is not sufficient evidence of bundle identity.

## Replay and expiry boundary

A real attestation validation requires a consumed-nonce ledger. The v2 validator rejects an attestation when its request nonce is already present in that ledger.

It also requires:

```text
issued_at < evaluated_at <= expires_at
```

The validator is intentionally read-only: it checks the supplied nonce ledger but does not mutate operational state. The controlled coordinator is responsible for recording the nonce after accepting an attestation transactionally with its own downstream state change.

This separation avoids turning the public reference repository into a private execution database.

## Safe returned evidence

The private evaluator may use the reserved oracle internally. The public attestation still cannot serialize that oracle.

Safe evidence references remain limited to projections such as:

```text
attestation://...
digest://...
redacted://...
```

The handoff continues to hard-code:

```text
oracle_visibility = evaluator_only
oracle_content_allowed = false
raw_private_evidence_allowed = false
variant_mapping_allowed = false
governed_verdict_allowed = false
automatic_promotion_allowed = false
team_available_allowed = false
```

Authentication does not grant promotion authority.

## Validation

V1 compatibility remains available through:

```text
scripts/validate_reserved_evaluation_handoff.py
```

Trusted v2 validation uses:

```text
scripts/validate_reserved_evaluation_handoff_v2.py
```

Request-only validation needs no trust store because no evaluator claim has yet been made.

Any stream containing an attestation requires both:

```text
--trust-store <trusted-public-keys.json>
--consumed-nonces <nonce-ledger.txt>
```

The v2 validator checks:

- Draft 2020-12 record structure;
- candidate/version/execution/mission lineage;
- frozen target and case-allocation hashes;
- request expiry and nonce shape;
- exact blinded bundle reference and digest parity;
- evaluator authorization and key validity window;
- canonical SHA-256 attestation digest;
- Ed25519 detached signature;
- replay against the consumed nonce ledger;
- anonymous A/B result shape and protected metrics;
- safe evidence-reference schemes;
- no oracle, mapping, governed verdict, auto-promotion, or team-availability authority.

## Synthetic conformance only

The repository contains a synthetic blinded bundle, public key, signed attestation, and empty nonce ledger only under `tests/fixtures/` so CI can prove the cryptographic verification path.

The synthetic private key is intentionally not stored in the repository. The committed signature was generated offline from a deterministic test key and only the corresponding public key is retained for verification.

These fixtures prove contract behavior, not evaluator trust in production and not that the Case 0 challenger wins a real reserved case.

## Module and authority boundaries

Existing boundaries remain unchanged:

- `feature_delivery_case` remains the primary delivery/value lifecycle;
- Helixion may consume settled evidence but cannot promote from this handoff;
- AegisFlow may coordinate controlled evaluation but does not own oracle truth;
- FlowGuard may enforce permission and boundary rules but does not choose the verdict;
- Memexa may retain approved high-signal lineage, never raw oracle material;
- DeliveryYield may analyze economics only after quality settlement;
- OpenClaw remains within its existing execution boundary.

No active module is replaced or reclassified.

## Next gate

PR 42 intentionally stops after establishing a trustworthy attestation boundary.

The next public change may strengthen the **observed evidence gate** so a `downstream_observed` Blind Challenge cannot reach `scoped_canary` eligibility with empty evidence or an unverified attestation.

A real reserved evaluation is still external to the public repository. No synthetic fixture in Lattice should be promoted as real Case 0B evidence.
