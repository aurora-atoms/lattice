# Evidence Wayfinding Blind Challenge Execution

## Decision

`lat.blind_challenge_execution.v1` is the governed boundary after `lat.harness_mutation_candidate.v1`.

It exists to answer one question:

> Did a frozen challenger reduce the named failure on representative, hard, counterexample, and reserved cases without violating protected behavior strongly enough to justify a bounded next step?

It does **not** promote a capability. It produces only one of four evaluation verdicts:

```text
reject
revise
continue_shadow
scoped_canary
```

`team_available` is not a Blind Challenge verdict.

## Why this contract exists

A Harness Mutation Candidate is still only a hypothesis. Case 0 showed why a locally convincing fix is not sufficient evidence for team-level evolution: the same author, same case, same model, or same visible oracle can all create evaluation leakage.

The Blind Challenge contract makes the evaluation boundary executable:

```text
Outcome Receipt
-> one Harness Mutation Candidate
-> frozen target + frozen case allocation
-> anonymous variant A / B evaluation
-> externally supplied reserved oracle
-> authenticated reserved attestation
-> post-evaluation mapping reveal
-> governed verdict
-> human-controlled next step
```

The contract is intentionally narrower than a generic benchmark platform.

## Frozen evaluation surface

Before comparison begins, the execution receipt binds to the candidate's:

- evaluator version;
- primary metric;
- protected metrics;
- four allowed verdicts;
- failure point and one primary delta;
- non-regression constraints;
- complete case allocation.

Two canonical hashes protect this boundary:

```text
target_hash
case_allocations_hash
```

`target_hash` covers the candidate identity/version, source failure, changed mechanism, primary delta, hypothesis, primary metric, protected metrics, and non-regression constraints.

`case_allocations_hash` covers the complete frozen allocation, including the withheld reserved case reference.

If either changes, a previously started execution no longer validates against the candidate.

## Blindness contract

During evaluation:

```text
incumbent/challenger identities -> hidden behind A / B
reserved oracle                 -> evaluator_only
candidate author                 -> cannot view reserved outcome
oracle contents                  -> never copied into the public receipt
```

After evaluation completes, the A/B mapping may be revealed for adjudication. The receipt records `variant_mapping.revealed_at`; the semantic validator requires it to occur at or after `completed_at`.

This keeps two ideas separate:

1. evaluator blindness while judgments are produced;
2. transparent lineage after the evaluation is frozen.

## Reserved oracle handling

Public Lattice cannot honestly manufacture a hidden reserved oracle that remains hidden from the author. Therefore the public Case 0 execution remains:

```text
status = blocked_pending_reserved_oracle
```

until a controlled/private downstream evaluator supplies the reserved oracle.

The public fixture records only:

```text
reserved case identity
oracle visibility = evaluator_only
oracle content included = false
status = unavailable
```

No public file contains the oracle answer.

`lat.reserved_evaluation_handoff.v2` is the trust-bearing transport for a real reserved result. It binds the frozen request to:

```text
request_nonce
variant_bundle_ref
variant_bundle_digest
evaluator_identity / key_id
attestation_canonical_digest
Ed25519 signature
```

The Blind Challenge validator does not reimplement cryptography. For a real observed execution or `scoped_canary`, it invokes the v2 handoff validator and requires the authenticated attestation to match the reserved result projected into the execution receipt.

A separate test-only `synthetic_reference` evaluated fixture still exercises the basic completed-state contract. It is conformance evidence only; it is not a real blind benchmark, downstream adoption signal, or promotion signal.

## Evaluated state

An evaluated execution must have:

```text
all frozen case allocations settled
exactly A and B per case
all protected metrics represented
reserved oracle attestation present
reserved oracle contents absent
post-evaluation A/B mapping
exactly one governed verdict
```

The reserved oracle is represented by attestation metadata, not by copying its contents:

```text
attestation_ref
attestation_hash
evaluated_by
evaluated_at
```

For an execution that claims `downstream_observed`, those four values must match a successfully authenticated v2 attestation. The reserved `case_result` must also exactly match the attestation's public-safe `reserved_case_result` projection.

## Observed Evidence Gate

A syntactically valid `downstream_observed` label is not evidence.

When:

```text
simulation_status = downstream_observed
```

semantic validation additionally requires:

```text
status = evaluated
downstream_adoption_status = observed_once | reused
execution.evidence_refs != []
each case_result.evidence_refs != []
each variant_outcome.evidence_refs != []
each protected_metric.evidence_refs != []
all evidence refs are URI-like
authenticated Reserved Evaluation Handoff v2 is supplied and verifies
```

This closes the audit mutation in which a synthetic execution could be relabeled as observed while retaining empty evidence arrays.

The gate is deliberately semantic rather than a breaking structural rewrite of `blind-challenge-execution.v1`: synthetic conformance fixtures may still use empty evidence arrays because they explicitly do not claim observed downstream facts.

The public/private boundary remains unchanged. Real private evidence stays in the downstream repository; public-safe projections may use refs such as `attestation://`, `digest://`, `redacted://`, `artifact://`, or another URI-like evidence locator permitted by the owning downstream policy.

## Protected metrics

The candidate defines the metrics that must not regress. Case 0 currently protects at least:

```text
critical_false_ready
authority_drift
private_to_public_leakage
```

The Blind Challenge validator requires every evaluated case to report every frozen protected metric exactly once.

Any failure in a critical protected metric constrains the verdict to:

```text
reject
or
revise
```

It cannot yield `continue_shadow` or `scoped_canary`.

## Scoped canary gate

`scoped_canary` is deliberately harder than `continue_shadow`.

It requires:

- all protected metrics evaluated;
- no critical protected failure;
- an explicit bounded canary scope;
- a valid post-evaluation challenger identity;
- challenger passes the reserved target;
- reserved comparison is not inconclusive;
- a successfully authenticated Reserved Evaluation Handoff v2 attestation;
- the execution's reserved result and attestation metadata exactly match that authenticated attestation;
- the authenticated `attestation_ref` appears in execution evidence;
- later human approval.

Even after these checks:

```text
team_available_allowed = false
```

A scoped canary only authorizes a human to consider a bounded canary under the candidate's existing authority and rollback rules.

## Verdict semantics

### `reject`

The challenger fails the target, violates protected behavior, or has evidence strong enough to stop further investment.

### `revise`

The failure mechanism remains plausible, but the candidate, evaluator, allocation, or delta needs a new version before another frozen evaluation.

A revision is a new candidate/evaluation identity; do not silently edit a completed execution.

### `continue_shadow`

The challenger shows signal without sufficient evidence for a canary. Typical reasons include synthetic-only evidence, inconclusive reserved comparison, insufficient live evidence, or remaining uncertainty.

### `scoped_canary`

The challenger passes the protected blind-evaluation boundary strongly enough to request a bounded human-approved canary. It is not team promotion.

## Promotion Firewall

Blind Challenge v1 hard-codes:

```text
automatic_promotion_allowed = false
team_available_allowed = false
human_owner_required = true
scoped_canary_requires_human_approval = true
```

This contract cannot:

- modify an active Skill;
- change a Capability Profile default;
- change routing globally;
- grant merge/release/deploy authority;
- grant `team_available`;
- convert synthetic evidence into private adoption evidence.

`synthetic_reference` is additionally forbidden from claiming `observed_once` or `reused` downstream adoption.

## Relationship to Feature Delivery Case

The Feature Delivery Case remains the primary user-value and evidence boundary.

Blind Challenge is an evolution/evaluation projection produced after a settled Outcome Receipt. It is not a new delivery lifecycle.

Module boundaries remain unchanged:

- Helixion may aggregate settled failure patterns and propose candidates;
- AegisFlow may orchestrate bounded evaluation work;
- FlowGuard owns scope/permission enforcement;
- Memexa preserves evidence and lineage under its existing scope;
- OpenClaw remains a bounded execution surface;
- DeliveryYield may analyze economics only after quality verdicts and cannot alter this verdict.

## Public Case 0 state

The Case 0 public execution is intentionally blocked because no valid hidden reserved oracle exists inside the public repository:

```text
examples/evidence-wayfinding/case-0-schema-parity/
  blind-challenge-execution.blocked.json
```

The contract can be structurally and semantically verified without pretending the evaluation happened.

## Validation

Basic blocked/synthetic conformance remains:

```bash
python scripts/validate_json_schema_instance.py \
  schemas/capability/blind-challenge-execution.v1.schema.json \
  examples/evidence-wayfinding/case-0-schema-parity/blind-challenge-execution.blocked.json

python scripts/validate_blind_challenge_execution.py \
  examples/evidence-wayfinding/case-0-schema-parity/blind-challenge-execution.blocked.json \
  examples/evidence-wayfinding/case-0-schema-parity/harness-mutation-candidate.json
```

A downstream-observed execution or `scoped_canary` must additionally provide the authenticated v2 trust context:

```bash
python scripts/validate_blind_challenge_execution.py \
  <evaluated-execution.json> \
  <candidate.json> \
  --reserved-handoff-v2 <request-plus-attestation.jsonl> \
  --blocked-execution <blocked-source-execution.json> \
  --handoff-schema-v2 schemas/capability/reserved-evaluation-handoff-record.v2.schema.json \
  --trust-store <trusted-evaluators.json> \
  --consumed-nonces <consumed-nonces.txt>
```

Tests:

```bash
python -m unittest discover -s tests -p 'test_blind_challenge_execution.py' -v
```

## Next gate

Do not build automatic promotion next.

After this evidence gate, the next public hardening step is to provide one authoritative Case bundle validation entrypoint so downstream consumers do not have to infer structural/semantic/integrity validator ordering themselves.

Deterministic attestation ingestion and a real private Case 0B remain separate later gates. No synthetic fixture should be used to claim that either has happened.
