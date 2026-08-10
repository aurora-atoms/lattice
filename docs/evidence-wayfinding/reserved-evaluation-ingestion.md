# Deterministic Reserved Evaluation Ingestion

## Decision

`lat.reserved_evaluation_ingest_result.v1` is the public-safe transition output between an authenticated Reserved Evaluation Handoff v2 and later human Blind Challenge adjudication.

It answers one bounded question:

> After the controlled evaluator has signed the reserved result, what exactly may the public coordinator ingest without inventing a verdict, revealing the A/B mapping, or granting promotion authority?

The ingestion path is:

```text
blocked Blind Challenge Execution
+ frozen Harness Mutation Candidate
+ authenticated Reserved Evaluation Handoff v2
+ trusted evaluator key store
+ replay nonce ledger
-> deterministic ingest result
-> readiness projection
-> STOP for later governed adjudication
```

This is not a new delivery lifecycle. The Feature Delivery Case remains the primary user-value and evidence boundary.

## Why ingestion is separate from the verdict

The v2 handoff proves that a named authorized evaluator signed one exact request, variant bundle digest, and reserved result. That does not authorize the public coordinator to decide whether the challenger should be rejected, revised, kept in shadow, or considered for a scoped canary.

Therefore ingestion explicitly stops before:

```text
variant mapping reveal
governed verdict
scoped canary approval
team_available
automatic promotion
merge / release / deployment
```

The ingest result contains a fixed `human_gate` with all of those authorities disabled.

## Deterministic inputs

`scripts/ingest_reserved_evaluation_attestation.py` requires:

- the completed two-record `lat.reserved_evaluation_handoff.v2` JSONL;
- the frozen Harness Mutation Candidate;
- the source Blind Challenge Execution in `blocked_pending_reserved_oracle`;
- the v2 handoff schema;
- a trusted evaluator public-key store;
- the consumed-request-nonce ledger;
- the ingest-result schema.

Before producing any result it reuses the existing validators to verify:

1. the blocked source execution is still valid against the frozen candidate;
2. request and attestation lineage match exactly;
3. the request has not expired or been consumed;
4. variant bundle reference and SHA-256 digest match;
5. evaluator identity/key is authorized for the evaluator version, mission, and reserved case;
6. the canonical attestation digest matches the signed content;
7. the Ed25519 signature verifies;
8. reserved evidence remains a safe projection and does not expose raw oracle/private evidence.

The ingestion layer does not reimplement the trust boundary.

## Output contract

The ingest result records only:

```text
source execution + candidate lineage
request nonce + frozen bundle ref/digest
authenticated attestation ref/digest/evaluator identity
public-safe reserved case result
safe evidence refs
allocation-settlement projection
human/promotion firewall
canonical ingest digest
```

It deliberately contains no `decision` or `variant_mapping` fields.

## Allocation settlement

The authenticated reserved result is not enough by itself to say the whole Blind Challenge has been evaluated.

The ingest script compares:

```text
case results already present in the blocked execution
+ authenticated reserved case result
```

against the candidate's complete frozen allocation.

It emits:

```text
merged_case_ids
missing_case_ids
all_allocations_settled
ready_for_governed_adjudication
```

`ready_for_governed_adjudication=true` only when every frozen allocation is settled. It still does not produce a verdict.

For the current public Case 0 fixture, the blocked execution contains no representative/hard/counterexample results. Ingesting the synthetic signed reserved attestation therefore remains:

```text
all_allocations_settled = false
ready_for_governed_adjudication = false
```

That is intentional. Synthetic cryptographic conformance must not be converted into a completed Blind Challenge.

## Replay protection

The v2 validator checks the request nonce against the consumed ledger before ingestion.

The ingestion CLI can additionally persist the nonce after a successful result with:

```bash
--commit-nonce
```

This operation appends the nonce atomically to the supplied ledger. Private coordinators should keep the authoritative replay ledger in their controlled environment.

## Canonical digest

The ingest result includes:

```text
ingest_canonical_digest = sha256(canonical JSON excluding the digest field)
```

This protects the public-safe projection from silent mutation after authenticated ingestion. It does not replace the evaluator's Ed25519 signature; the two digests protect different boundaries.

## Synthetic validation

The repository contains a signed synthetic v2 handoff only for protocol conformance. CI runs it through ingestion and validates the emitted result against:

```text
schemas/capability/reserved-evaluation-ingest-result.v1.schema.json
```

This proves deterministic contract behavior only. It does not prove a real reserved evaluation, downstream adoption, Senior Attention value, or promotion eligibility.

## Example

```bash
python scripts/ingest_reserved_evaluation_attestation.py \
  tests/fixtures/evidence-wayfinding/reserved-evaluation/handoff.synthetic-complete.v2.jsonl \
  examples/evidence-wayfinding/case-0-schema-parity/harness-mutation-candidate.json \
  examples/evidence-wayfinding/case-0-schema-parity/blind-challenge-execution.blocked.json \
  --handoff-schema schemas/capability/reserved-evaluation-handoff-record.v2.schema.json \
  --trust-store tests/fixtures/evidence-wayfinding/reserved-evaluation/trusted-evaluators.synthetic.json \
  --consumed-nonces tests/fixtures/evidence-wayfinding/reserved-evaluation/consumed-nonces.empty.txt \
  --output /tmp/reserved-evaluation-ingest-result.json

python scripts/validate_json_schema_instance.py \
  schemas/capability/reserved-evaluation-ingest-result.v1.schema.json \
  /tmp/reserved-evaluation-ingest-result.json
```

## Next gate

After this boundary exists, the public repository should not add another generic evolution layer merely because it can.

The evidence-bearing next step is a controlled/private execution that supplies real non-reserved results plus one real authenticated reserved attestation. Only then can a later human-controlled adjudication produce one of:

```text
reject
revise
continue_shadow
scoped_canary
```

No result from this ingestion contract can directly grant `team_available`.
