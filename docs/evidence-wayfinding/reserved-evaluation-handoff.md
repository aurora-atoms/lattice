# Controlled Reserved Evaluation Handoff

## Decision

Blind Challenge v1 deliberately stops when its reserved oracle is unavailable to the public repository. The next boundary is therefore not another evaluator inside the public Harness. It is a narrow handoff protocol between two trust zones:

```text
public repository
  owns candidate + frozen plan + public preflight
        |
        | eval.reserved_request
        v
controlled private evaluator
  owns reserved case + oracle + blinded execution
        |
        | eval.reserved_attestation
        v
public repository
  receives only a safe attestation projection
```

The protocol is **not** a new Lattice module, Agent, Skill, or second delivery lifecycle. It is a JSONL + JSON Schema handoff around the existing Harness Mutation Candidate and Blind Challenge Execution contracts.

Contract:

```text
lat.reserved_evaluation_handoff.v1
```

Schema:

```text
schemas/capability/reserved-evaluation-handoff-record.v1.schema.json
```

Each line is one authoritative handoff record with the standard fields:

```text
type
id
schema
source
target
scope
payload
constraints
```

## Why a separate trust boundary is required

A reserved case is useful only while the proposal path cannot inspect its oracle before the comparison is complete. Putting the reserved input, expected answer, private evidence, or A/B mapping into the same public repository as the candidate destroys the holdout.

The public repository can safely know:

- which candidate and version are under test;
- the blocked Blind Challenge execution id;
- the opaque reserved case id;
- frozen target and case-allocation hashes;
- evaluator protocol version;
- primary and protected metrics;
- an opaque `controlled://` blinded variant-bundle reference.

It must not receive during evaluation:

- raw reserved input or oracle content;
- private source artifacts;
- the incumbent/challenger mapping behind A/B;
- a promotion decision produced by the evaluator;
- credentials or access tokens.

## Request record

A request uses:

```text
type = eval.reserved_request
source.boundary = public_repository
target.boundary = controlled_private_evaluator
```

The request is a deterministic projection of the frozen Harness Mutation Candidate and blocked Blind Challenge Execution.

It carries:

```text
candidate_id / version
execution_id
reserved_case_id
mission_anchor_ref
target_hash
case_allocations_hash

evaluator_version
primary_metric
protected_metrics
variant_bundle_ref
variant_labels = [A, B]
```

`variant_bundle_ref` is intentionally opaque. The public request builder only accepts `controlled://...`. The trusted coordinator is responsible for constructing the actual blinded execution bundle outside the public repository.

Case 0 publishes only the request:

```text
examples/evidence-wayfinding/case-0-schema-parity/
  reserved-evaluation-handoff.request.jsonl
```

That is the correct current state because no real controlled reserved evaluator has supplied an attestation.

## Attestation record

A completed evaluator returns:

```text
type = eval.reserved_attestation
source.boundary = controlled_private_evaluator
target.boundary = public_repository
```

The safe attestation may expose only post-evaluation anonymous results:

```text
A target result
B target result
A/B comparison
protected metric statuses
safe evidence digests / attestation refs
evaluator identity/version/time
attestation ref/hash
```

It explicitly states:

```text
oracle_used = true
oracle_content_included = false
variant_mapping_included = false
governed_verdict_included = false
```

The evaluator may use the oracle privately. The public receipt never contains that oracle.

Safe evidence references are restricted to public projections such as:

```text
attestation://...
digest://...
redacted://...
```

They identify evidence without copying private evidence into the public repository.

## Blindness lifecycle

The intended sequence is:

```text
1. candidate target and allocations freeze
2. Blind Challenge becomes blocked_pending_reserved_oracle
3. trusted coordinator creates opaque A/B execution bundle
4. public request is emitted
5. controlled evaluator receives reserved case + private oracle
6. evaluator judges anonymous A/B outputs
7. evaluator freezes attestation
8. safe attestation returns to public boundary
9. only after evaluation may the coordinator reveal A/B mapping
10. Blind Challenge produces reject | revise | continue_shadow | scoped_canary
11. human approval is still required for scoped_canary
```

The candidate author must not see the reserved oracle or mapping while evaluation is running. A safe aggregate attestation may become visible after the evaluator has frozen its result; that does not expose the raw oracle.

## Promotion Firewall

Both request and attestation hard-code:

```text
oracle_visibility = evaluator_only
oracle_content_allowed = false
raw_private_evidence_allowed = false
variant_mapping_allowed = false
governed_verdict_allowed = false
automatic_promotion_allowed = false
team_available_allowed = false
```

Therefore the private evaluator cannot grant promotion through this handoff.

The handoff answers only:

> What did anonymous A and B do on the controlled reserved case, under the frozen metrics?

The existing Blind Challenge contract remains responsible for combining representative, hard, counterexample, and reserved results into a governed verdict. Human ownership remains outside both contracts.

## Deterministic validation

Validator:

```text
scripts/validate_reserved_evaluation_handoff.py
```

It checks:

- every JSONL line against Draft 2020-12 JSON Schema;
- exactly one request and at most one attestation;
- request-before-attestation order;
- candidate/version/execution/mission lineage;
- exact frozen `target_hash` and `case_allocations_hash` parity;
- exact evaluator version, primary metric, and protected metrics;
- exactly one external evaluator-only reserved allocation;
- anonymous A/B result shape;
- no unsafe evidence references in returned projection;
- no raw oracle, A/B mapping, governed verdict, auto-promotion, or team-availability authority.

Request builder:

```text
scripts/prepare_reserved_evaluation_request.py
```

It creates only the public-safe request projection. It cannot ingest an oracle or emit a verdict.

## Synthetic conformance versus real evidence

The repository contains a synthetic completed JSONL fixture solely to prove that the protocol and validator can represent a completed handoff:

```text
tests/fixtures/evidence-wayfinding/reserved-evaluation/
  handoff.synthetic-complete.jsonl
```

It is **not** a real reserved evaluation and must not be cited as evidence that the Case 0 challenger wins.

The public Case 0 request remains request-only until a controlled private evaluator returns a real attestation.

## Module and authority boundaries

Existing boundaries remain unchanged:

- `feature_delivery_case` remains the primary delivery/value lifecycle;
- Helixion may use settled multi-case evidence to propose candidates but cannot promote from this handoff;
- AegisFlow may orchestrate a future controlled evaluation but does not own the oracle truth;
- FlowGuard may enforce boundary and permission policy but does not choose the verdict;
- Memexa may retain approved high-signal lineage, not raw private oracle material;
- DeliveryYield may analyze evaluation/delivery economics only after quality settlement;
- OpenClaw remains within its existing execution boundary.

No active module is replaced or reclassified.

## Next gate

After this protocol is merged, the next evidence requirement is external to the public repository:

```text
one controlled reserved case
+ one evaluator-only oracle
+ one opaque A/B bundle
+ one valid eval.reserved_attestation
```

Only after that real attestation exists should the public side implement or exercise the ingestion step that completes `lat.blind_challenge_execution.v1` and selects one governed verdict.

Do not create another synthetic PR merely to simulate that evidence.
