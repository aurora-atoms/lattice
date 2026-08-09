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
```

It does not prove private downstream adoption, team reuse, manager value, or self-evolving Harness quality.

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

Case 0 records the future mandatory-gate shape without promoting it into a general authoritative contract yet.

The replay requires all five conditions to pass:

1. `bounded_decision` — one explicit decision exists;
2. `evidence` — addressable repository evidence exists;
3. `counterevidence` — the compatibility risk of strict schema execution is explicit;
4. `authority` — repository maintainers retain the contract decision;
5. `delivery_state_change` — the decision changes executable CI behavior.

Result:

```text
READY
```

There is no `4-of-5` waiver in this replay.

## Evidence Map

The Portable Case Pack preserves three evidence anchors:

```text
EV-001
  Portable Case Pack v1 schema before the parity fix

EV-002
  pre-fix capability-profile validation workflow

EV-003
  merged parity repair commit from PR 36
```

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

The replay target is limited to the known false-ready mutations:

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

Observed state transition:

```text
BEFORE
published structural contract not executed against instances

AFTER
published structural contract executes before semantic validation
and four negative mutation anchors protect the repaired boundary
```

Earliest failure point:

```text
CI validated schema-document syntax but did not execute schema-instance conformance.
```

The accepted repository artifact is merged commit:

```text
863ceb307416975ddb43ec3fba2606648b2c0c59
```

Remaining unknowns are preserved rather than filled in:

- whether future Portable Case Pack semantics should require evidence for every derived claim;
- whether Evidence Wayfinding improves scarce Senior Attention in a private live case.

## What Case 0 proves

Case 0 provides public evidence that the workflow can preserve one bounded decision, evidence, counterevidence, verification, human authority, and an observed repository state change in one linked case spine.

It also provides one failure point that is eligible to become a Harness mutation candidate.

It does **not** grant promotion authority from this single replay.

## What Case 0 does not justify

Do not use this replay to justify:

- a new Lattice module;
- `frontier-practice-scout` promotion;
- automatic Skill or rule mutation;
- team-wide capability promotion;
- Portable Case Pack v2 without a separate compatibility decision;
- claims of measured Senior Attention ROI;
- claims of private downstream adoption.

## Next gate

The next implementation step may formalize the two contracts whose need is now visible in an executed case:

1. a deterministic **Attention Admission** contract with mandatory invariants and `READY | BLOCKED | ESCALATE` outcomes;
2. an **Outcome Receipt** contract that preserves before/after state, human correction, claim outcomes, earliest failure point, and remaining unknowns.

Those contracts should remain projections around the Feature Delivery Case rather than becoming a second canonical lifecycle object.
