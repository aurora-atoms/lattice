# Evidence Wayfinding Blind Challenge Execution — PR 11

## Source decision

Merged PR 39 introduced one bounded Harness Mutation Candidate from Case 0's verified earliest failure point. That candidate intentionally stopped at:

```text
evaluation_plan.status = blocked_pending_reserved_oracle
```

This change implements the next gate recorded by that PR: define an executable blind-evaluation contract without pretending the public repository contains a credible hidden reserved oracle.

## Direction Investment Gate

```yaml
primary_value_path: current_product_delivery
direction_verdict: proceed
evidence_refs:
  - repo://examples/evidence-wayfinding/case-0-schema-parity/harness-mutation-candidate.json@cc78f6f8c41512d2006644bfe4cdcb224c949706
  - repo://examples/evidence-wayfinding/case-0-schema-parity/outcome-receipt.json@cc78f6f8c41512d2006644bfe4cdcb224c949706
existing_capability_gap: >
  Lattice can now create a failure-linked single-delta Harness candidate, but it
  has no executable contract proving that evaluation target, case allocation,
  blindness, protected metrics, reserved-oracle handling, and verdict authority
  remain frozen across incumbent/challenger comparison.
user_outcome: >
  A maintainer or controlled downstream evaluator can determine whether one
  candidate should be rejected, revised, kept in shadow, or considered for a
  bounded human-approved canary without exposing the reserved oracle or granting
  team-level promotion authority.
```

The value path is still the same Case 0 delivery defect and its governed evolution evidence. This PR does not create a general benchmark product.

## Implemented slice

This PR adds:

```text
schemas/capability/blind-challenge-execution.v1.schema.json
scripts/validate_blind_challenge_execution.py
examples/evidence-wayfinding/case-0-schema-parity/
  blind-challenge-execution.blocked.json
tests/fixtures/evidence-wayfinding/blind-challenge/
  evaluated.synthetic-conformance.json
tests/test_blind_challenge_execution.py
docs/evidence-wayfinding/blind-challenge-execution.md
```

CI validates both the blocked public Case 0 preflight and a test-only synthetic evaluated conformance fixture.

## Why the public Case 0 execution remains blocked

A reserved case is only useful if the candidate author cannot inspect the oracle before evaluation. Putting the oracle answer into the public repository would destroy that property.

Therefore the public Case 0 receipt preserves:

```text
status = blocked_pending_reserved_oracle
reserved_oracle.status = unavailable
reserved_oracle.oracle_visibility = evaluator_only
reserved_oracle.oracle_content_included = false
decision = null
variant_mapping = null
```

This is a deliberate success condition for the public contract, not missing implementation.

## Frozen target and allocation

Blind Challenge v1 binds to the candidate with two deterministic hashes:

```text
target_hash
case_allocations_hash
```

The semantic validator recomputes both from the Harness Mutation Candidate. A changed hypothesis, primary delta, failure point, protected metric, non-regression constraint, or case allocation invalidates the previous execution binding.

This prevents evaluating a moving target while keeping the receipt compact.

## Blindness and post-evaluation mapping

During evaluation, the evaluator sees anonymous variants `A` and `B`. The reserved oracle stays evaluator-only and is represented in the receipt only by attestation metadata.

After evaluation is complete, the receipt may reveal:

```text
A -> incumbent or challenger variant id
B -> incumbent or challenger variant id
```

The validator requires the reveal timestamp to be at or after the evaluation completion timestamp and requires the mapping to contain exactly the candidate's incumbent and challenger.

This makes the evaluation auditable without leaking identity before judgments are frozen.

## Verdict boundary

The contract allows exactly:

```text
reject
revise
continue_shadow
scoped_canary
```

It explicitly does not contain `promote` or `team_available`.

Critical protected-metric failure allows only `reject` or `revise`. `scoped_canary` additionally requires the reserved challenger target to pass, all protected metrics to be evaluated, a non-inconclusive reserved comparison, explicit bounded scope, and later human approval.

## Synthetic evaluated fixture

The evaluated fixture under `tests/fixtures/` exists only to exercise the completed-state contract and negative tests.

It is marked:

```text
simulation_status = synthetic_reference
downstream_adoption_status = not_observed
```

Its oracle attestation is synthetic. It is not evidence that a real blind reserved evaluation occurred and must not be cited as private adoption, team reuse, Senior Attention ROI, or canary approval.

## Boundaries preserved

This PR intentionally does not:

- create or modify an active Skill;
- create a new Agent or module;
- change the Case 0 challenger into a default verifier;
- implement a generic benchmark platform;
- add automatic mutation generation;
- expose a private reserved oracle;
- grant `team_available`;
- implement automatic canary/promotion/rollback orchestration;
- claim a real blind evaluation from synthetic fixtures.

`feature_delivery_case` remains the primary delivery/value boundary. Existing active modules remain valid development tracks.

## Next gate

After this contract lands, the next step is not automatic promotion.

A future change should add a **controlled downstream reserved-evaluation adapter/protocol** that:

1. accepts the public candidate plus frozen execution contract;
2. keeps the reserved oracle private from the candidate author;
3. produces anonymous A/B evidence;
4. reveals mapping only after evaluation completion;
5. returns only the permitted receipt projection;
6. does not upload private oracle content into public Lattice.

Only a real controlled reserved result can justify deciding between `reject`, `revise`, `continue_shadow`, and a proposed `scoped_canary`.
