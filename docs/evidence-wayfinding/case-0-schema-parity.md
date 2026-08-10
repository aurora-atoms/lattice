# Evidence Wayfinding Case 0 — Schema Parity Replay

## Purpose

Case 0 is the first public, repository-grounded replay of the Evidence Wayfinding workflow. It uses the Portable Case Pack structural-validation defect identified by the 2026-08-08 case-calibrated Senior Attention audit and repaired by merged PR 36.

This case is intentionally narrow. It demonstrates that one bounded repository defect can move through:

```text
Case Contract
-> Portable Case Pack
-> Attention Admission
-> Decision Card
-> Verification Receipt
-> Outcome Receipt
-> Harness Mutation Candidate
-> Blind Challenge preflight
-> Reserved Evaluation request
```

It does not prove private downstream adoption, team reuse, manager value, real reserved-evaluation performance, or Senior Attention value.

## Case identity

```text
case_id = synthetic/evidence-wayfinding-schema-parity-case-0
mission = lat.goal.verified-decision-yield.v1
value_path = current_product_delivery
simulation_status = synthetic_reference
downstream_adoption_status = not_observed
```

The public fixture lives at:

```text
examples/evidence-wayfinding/case-0-schema-parity/
```

The Feature Delivery Case remains the primary user-value and evidence boundary. The Case 0 JSON files are public replay projections and governed evaluation artifacts; they do not create a second delivery lifecycle.

## Current implementation status

The original Case 0 document stopped at a future-looking description of Attention Admission and Outcome Receipt. That is no longer current. The repository now contains executable contracts for:

```text
Portable Case Pack structural schema + semantic validator
Attention Admission mandatory gate
Outcome Receipt settlement
Harness Mutation Candidate
Blind Challenge preflight
Reserved Evaluation Handoff v1 compatibility
Reserved Evaluation Handoff v2 authenticated-attestation trust boundary
Observed Evidence Gate for downstream_observed/scoped_canary claims
Authoritative Case bundle validation
Deterministic authenticated reserved-attestation ingestion
```

The public Case 0 remains correctly blocked before a real reserved oracle:

```text
Blind Challenge status = blocked_pending_reserved_oracle
simulation_status = synthetic_reference
downstream_adoption_status = not_observed
```

The ingestion implementation can consume the signed synthetic v2 conformance fixture, but that does not change public Case 0 state. With no non-reserved preflight results in the blocked execution, the correct synthetic ingest projection remains:

```text
all_allocations_settled = false
ready_for_governed_adjudication = false
```

No public fixture is evidence of a real reserved evaluation or live Senior Attention outcome.

## Before state

Portable Case Pack v1 published a Draft 2020-12 JSON Schema containing required fields, closed shapes, enum/const rules, and date-time formats. The pre-fix CI path checked that the schema document itself was valid JSON, then relied on a narrower handwritten semantic validator.

The failure was therefore not “the schema is wrong.” The failure was that the published structural contract was not the runtime structural authority.

## Decision Strip

```text
Recommendation:
  Execute the published Draft 2020-12 schema before semantic validation.

Decision needed:
  Which layer owns Portable Case Pack structural validity?

Largest risk:
  Mistaking structural conformance for semantic correctness.

Latest safe point:
  Before another runtime or downstream consumer relies on v1 validation behavior.
```

## Decision Card

Two bounded choices were preserved:

### Option A — schema-first structural authority

```text
Draft 2020-12 JSON Schema
-> structural PASS
-> Portable Case Pack semantic validator
-> cross-field semantic PASS
```

Benefits:

- published structural rules become executable;
- compatibility failures become visible instead of silently tolerated;
- structural and semantic responsibilities stop competing.

Risk:

- previously tolerated but schema-invalid instances may require compatibility review.

### Option B — handwritten validator remains the only runtime gate

Benefit:

- avoids immediately exposing schema-validation failures.

Risk:

- preserves the false-ready condition in which runtime validity can contradict the published contract.

The repository outcome selected Option A through merged PR 36.

## Attention Admission

Attention Admission is now an executable contract rather than a future proposal. Case 0 requires every mandatory invariant to pass before it can be `READY`; there is no `4-of-5` waiver.

The gate preserves bounded decision, traceable evidence, strongest counterevidence, authority/risk, and delivery consequence. Any mandatory failure blocks or escalates instead of relying on an average score.

## Evidence Map

The Portable Case Pack preserves three evidence anchors:

```text
EV-001
  Portable Case Pack v1 schema before the parity fix
  git blob = 31dbb1d1e720ee42da864203727ce06a2ad85ecf

EV-002
  pre-fix capability-profile validation workflow
  git blob = 4e194dfa76d2e990d07a1fbf8cc349704cc60638

EV-003
  merged parity repair commit from PR 36
  commit = 863ceb307416975ddb43ec3fba2606648b2c0c59
```

`EV-002` previously carried a placeholder hash. The bundle-validation change replaces it with the actual Git blob SHA and verifies `repo://<path>@<commit>` references against the repository object database.

Key claims:

```text
OBS-001
  the v1 schema declares executable structural constraints

OBS-002
  pre-fix CI did not execute those constraints against instances

OBS-003
  PR 36 added schema instance validation and mutation coverage

DER-001
  schema-first structural validation removes the observed mismatch
  for the covered mutation classes

JDG-001
  schema owns structure; semantic validator owns cross-field domain semantics

UNK-001
  derived-claim evidence requirements remain unresolved in v1
```

The strongest counterevidence is compatibility: a closed schema can reject shapes that a narrower validator previously tolerated. That risk is preserved rather than used as a reason to weaken the published contract silently.

## Verification Receipt

The replay target remains limited to the known false-ready mutations:

```text
valid Portable Case Pack              -> PASS
unknown top-level field               -> REJECTED
missing audience                      -> REJECTED
missing required_output               -> REJECTED
malformed evidence date-time          -> REJECTED
semantic cross-field validator        -> PASS after schema
```

This does not establish complete semantic correctness. It establishes the Case 0 target only.

## Outcome Receipt

Outcome Receipt is now an executable contract and records the observed repository transition:

```text
BEFORE
published structural contract not executed against instances

AFTER
published structural contract executes before semantic validation
and negative mutation anchors protect the repaired boundary
```

Earliest failure point:

```text
CI validated schema-document syntax but did not execute schema-instance conformance.
```

The accepted repository artifact remains merged commit:

```text
863ceb307416975ddb43ec3fba2606648b2c0c59
```

Remaining unknowns are preserved rather than filled in:

- whether future Portable Case Pack semantics should require evidence for every derived claim;
- whether Evidence Wayfinding improves scarce Senior Attention in a private live case;
- whether a real controlled reserved evaluator confirms the candidate without protected-metric regression.

## Governed evolution state

Case 0 has progressed beyond Outcome Receipt, but only into governed candidate/evaluation preparation:

```text
Outcome Receipt
-> session_local Harness Mutation Candidate
-> frozen Blind Challenge target/allocation
-> blocked public preflight
-> controlled Reserved Evaluation request
```

The trust boundary requires authenticated v2 attestations for real downstream-observed or scoped-canary claims. The deterministic ingestion boundary can validate such an attestation, copy only its public-safe reserved result, calculate frozen-allocation settlement, and persist nonce consumption when requested.

Authentication and ingestion do not grant promotion authority. They also do not reveal A/B mapping or produce a governed verdict.

## Authoritative bundle validation

Do not use `scripts/validate_evidence_wayfinding_case.py` as the only validation command. It is retained as the cross-file Case Spine component for compatibility, but it does not execute every child JSON Schema.

The authoritative Case 0 entrypoint is:

```bash
python scripts/validate_evidence_wayfinding_case_bundle.py \
  examples/evidence-wayfinding/case-0-schema-parity
```

The bundle validator executes, in one ordered entrypoint:

```text
structural JSON Schemas
-> semantic validators
-> cross-file Case Spine lineage
-> repo:// evidence Git-object integrity
-> Harness Mutation Candidate validation when present
-> Blind Challenge validation when present
-> Reserved Evaluation handoff validation when present
-> deterministic summary
```

This prevents a downstream consumer from obtaining a false green by calling only the cross-file validator while skipping child structural schemas.

## Reserved attestation ingestion boundary

A completed v2 handoff is consumed through:

```text
scripts/ingest_reserved_evaluation_attestation.py
```

The script reuses the authenticated handoff validator and emits `lat.reserved_evaluation_ingest_result.v1` with:

```text
request nonce + bundle ref/digest
authorized evaluator + attestation digest
public-safe reserved case result
safe evidence refs
merged/missing frozen case ids
ready_for_governed_adjudication
canonical ingest digest
fixed human/promotion firewall
```

The output contract deliberately contains no `decision` or `variant_mapping` field.

A trusted reserved result is therefore treated as evidence that can unlock later adjudication, not as permission to adjudicate or promote.

## What Case 0 proves

Case 0 provides public evidence that the repository can preserve one bounded decision, evidence, counterevidence, verification, human authority, observed repository state change, a local mutation candidate, a blocked blind-evaluation handoff, and an authenticated-ingestion protocol without pretending synthetic evidence is real adoption.

It does **not** grant promotion authority from this single replay.

## What Case 0 does not justify

Do not use this replay to justify:

- a new Lattice module;
- `frontier-practice-scout` promotion;
- automatic Skill or rule mutation;
- team-wide capability promotion;
- Portable Case Pack v2 without a separate compatibility decision;
- claims of measured Senior Attention ROI;
- claims of private downstream adoption;
- claims that Reserved Evaluation has executed in a real controlled environment.

## Next gate

The public contract stack now covers the known Case 0A false-green and trust-boundary findings far enough to support a controlled downstream run.

Do not add another generic public evolution layer merely because a next abstraction can be designed. The evidence-bearing milestone moves to private/downstream execution:

```text
real representative/hard/counterexample results
+ real controlled reserved evaluation
+ authenticated attestation
-> deterministic ingest
-> human-controlled adjudication candidate
```

That private Case 0B/live Senior case should record actual attention minutes, review/correction minutes, accepted artifact, real state change, correction count, and `critical_false_ready = 0`.

Only evidence from that execution should justify another public workflow or promotion-contract change.
