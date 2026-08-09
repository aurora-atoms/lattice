# Evidence Wayfinding Attention Admission and Outcome Contracts

## Decision

Case 0 demonstrated two contract needs strongly enough to move them from replay-only candidate shapes into executable public contracts:

- `lat.attention_admission_receipt.v1`
- `lat.outcome_receipt.v1`

They are projections around the Feature Delivery Case and Portable Case Pack. They do not become a second canonical delivery-state object, a new Skill, an Agent, or a module.

The purpose of this change is not to add process. It is to make two failure-sensitive boundaries deterministic:

1. a question cannot consume scarce Senior attention while a mandatory decision-readiness invariant is missing;
2. a completed case cannot enter the evolution path without preserving what actually changed, how each Claim settled, what the human corrected, and where the earliest failure occurred.

## 1. Attention Admission v1

### Contract

Schema:

```text
schemas/capability/attention-admission-receipt.v1.schema.json
```

Semantic validator:

```text
scripts/validate_attention_admission.py
```

The receipt projects one Case Contract and one Portable Case Pack. It never owns the underlying facts.

### Mandatory invariants

The gate has exactly five mandatory checks:

| ID | Invariant | READY requirement | Failure behavior |
|---|---|---|---|
| `M1_target` | target | one decision, accountable owner, in/out scope, evidence cutoff, acceptance criteria, acceptance observer | `BLOCKED` and ask one bounded clarification |
| `M2_evidence` | evidence | every non-UNKNOWN observed/derived/judged Claim has at least one resolvable evidence reference | `BLOCKED`; attach evidence or downgrade the Claim |
| `M3_counterevidence` | counterevidence | strongest counterevidence is recorded, or a bounded no-counterevidence search explicitly records search scope and blind spots | `BLOCKED`; do not use a positive recommendation without this boundary |
| `M4_risk_authority` | risk / authority | final decision owner exists and reversibility is known | missing authority -> `BLOCKED`; unknown reversibility -> `ESCALATE` |
| `M5_delivery` | delivery | required output contract, verifier, and expected real state change are explicit | `BLOCKED`; analysis-only work is not decision-ready |

There is no score and no `4-of-5` waiver.

Overall status is deterministic:

```text
any escalate -> ESCALATE
else any fail -> BLOCKED
else -> READY
```

`READY` means the question is fit to consume Senior attention. It does not mean the recommendation is correct, approved, safe to merge, or authorized for an irreversible action.

### Counterevidence basis

`M3_counterevidence` cannot pass merely because some generic source gap exists. The receipt records one explicit mode:

```text
recorded_counterevidence
```

or:

```text
bounded_search_no_counterevidence
```

The second mode requires a named search scope and non-empty blind spots. It records that the search was bounded; it does not prove counterevidence is impossible.

### Derived Claims and Portable Case Pack v1

Portable Case Pack v1 intentionally still permits a `derived` Claim with no evidence reference at the structural schema level. Attention Admission v1 resolves the Senior-attention safety boundary without silently rewriting Portable Case Pack v1:

```text
derived Claim without evidence
-> M2_evidence = fail
-> admission = BLOCKED
```

A future Portable Case Pack contract may tighten Claim semantics through a separate compatibility decision.

## 2. Outcome Receipt v1

### Contract

Schema:

```text
schemas/capability/outcome-receipt.v1.schema.json
```

Semantic validator:

```text
scripts/validate_outcome_receipt.py
```

Outcome Receipt is the settlement projection for one bounded Case. It records what was observed after the decision and delivery action. It does not retroactively rewrite the original Case Pack.

### Required settlement state

Every receipt preserves:

- decision owner and selected decision reference;
- evidence-backed `state_before` and `state_after`;
- whether a delivery state actually changed;
- accepted artifact reference;
- human corrections and their disposition;
- every Portable Case Pack Claim outcome;
- earliest failure point;
- remaining unknowns and next evidence;
- whether the failure point is eligible to create a Harness candidate;
- explicit absence of promotion authority from the receipt itself.

### Claim lifecycle

Outcome status is independent from the Portable Case Pack provenance bucket. A Claim can originate as `OBSERVED`, `DERIVED`, `JUDGED`, or `UNKNOWN`, while its outcome lifecycle uses:

```text
UNKNOWN
HYPOTHESIS
EVIDENCED
CONFIRMED
CONFLICTED
STALE
INVALIDATED
```

Each Claim outcome has:

```text
claim_id
version
status
evidence_refs
cutoff
status_history
```

The semantic validator enforces:

- every Case Pack Claim has exactly one outcome;
- every non-`UNKNOWN` outcome has evidence;
- `version` equals the number of recorded status-history events;
- history is continuous and the final event equals the current status;
- history timestamps and Claim cutoff cannot occur after `observed_at`;
- a remaining unknown linked to a Claim must still be `UNKNOWN` or `HYPOTHESIS`.

The current v1 history starts with `from: null` for version 1. Future revisions append events rather than silently rewriting the initial outcome.

### Failure point does not equal promotion

An Outcome Receipt may state:

```text
eligible_for_harness_candidate = true
```

but it must also state:

```text
promotion_authority = none_from_outcome_receipt
```

The receipt only supplies evidence for the next governed step. It cannot change a Skill, router, verifier, schema, policy, profile, or team default by itself.

## 3. Case 0 migration

The public Case 0 replay now uses both v1 contracts. Its Decision Card and Verification Receipt remain case-scoped candidate projections; they are not promoted by this change.

The Case 0 target remains the schema-parity defect repaired by merged PR 36. PR 37 proved the linked case spine. This change makes the two failure-sensitive receipt boundaries reusable and executable without broadening the workflow into a self-evolution platform.

## 4. Authority and ownership boundaries

These contracts preserve existing Lattice ownership:

- `feature_delivery_case` remains the primary user-value and delivery lifecycle boundary;
- Portable Case Pack remains the cross-runtime evidence handoff projection;
- human owners retain final product, architecture, security, compliance, risk, promotion, merge, release, and deployment authority;
- Helixion may later use settled failure evidence to propose candidates, but cannot infer promotion from one Outcome Receipt;
- DeliveryYield may analyze cost and attention economics after quality settlement; it does not change admission or delivery verdicts;
- no active module is replaced or reclassified.

## 5. Next gate

After this contract PR, the next bounded step is **not** a generic Mutation Engine.

The next evidence requirement is to take the Case 0 earliest failure point and represent exactly one local Harness Mutation Candidate with:

- one mechanism changed;
- explicit incumbent and challenger;
- scope and expiry;
- representative cases;
- at least one hard/counterexample case;
- one frozen reserved case;
- target metric and non-regression constraints;
- human promotion boundary and rollback condition.

The candidate should remain session/local or evaluation-scoped until blind evaluation shows that it improves the named failure without degrading protected behavior.
