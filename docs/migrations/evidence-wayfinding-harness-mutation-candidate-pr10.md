# Evidence Wayfinding Harness Mutation Candidate — PR 10

## Source and sequencing

This change follows the case-calibrated Senior Attention sequence after merged PR 38:

```text
Case 0
-> executable Admission and Outcome contracts
-> earliest failure point
-> one session-local Harness Mutation Candidate
-> later blind evaluation
-> later human canary/promotion decision
```

The preceding PR intentionally stopped before Harness mutation. This PR crosses only the next boundary: encoding one candidate from one observed failure point.

## Direction Investment Gate

```yaml
primary_value_path: current_product_delivery
direction_verdict: proceed_as_candidate
evidence_refs:
  - repo://examples/evidence-wayfinding/case-0-schema-parity/outcome-receipt.json
  - repo://examples/evidence-wayfinding/case-0-schema-parity/portable-case-pack.json
existing_capability_gap: >
  Lattice can now settle Case 0 through an authoritative Outcome Receipt, but it
  has no machine-checkable bridge from earliest_failure_point to one bounded,
  expiring, non-promoted Harness challenger.
user_outcome: >
  A maintainer can inspect exactly what mechanism Case 0 suggests changing,
  why that mechanism is linked to the observed failure, how it would be tested,
  and why it cannot become a team default from this case alone.
```

The value is not a new schema by itself. The value is making the first evolution proposal reviewable and rejectable without granting it runtime authority.

## Source-derived controls

The Senior Attention research requires the Promotion Firewall to preserve five controls:

1. **Case linkage** — candidate cites Case, Claim/evidence, Verification/Outcome, and earliest failure.
2. **One primary delta** — one mechanism per experiment.
3. **Blind evaluation** — target, allocation, evaluator identity, and reserved outcome handling are frozen before comparison.
4. **Protected metrics** — no critical false-ready, authority drift, or private-to-public leakage may be traded for attention/token gains.
5. **Human ownership** — owner, scope, expiry, version, rollback, and later human approval are mandatory.

This PR implements those controls in `lat.harness_mutation_candidate.v1` and its semantic validator.

## Candidate selected from Case 0

Case 0's earliest observed failure is a `verification_gap`:

```text
schema-document syntax was checked,
but schema-instance conformance was not executed.
```

The first allowed mutation target is therefore `verifier_change`.

The candidate compares:

```text
incumbent:
  JSON syntax -> handwritten semantic validator

challenger:
  authoritative schema-instance conformance
  -> handwritten semantic validator
```

No other Harness mechanism is changed by this candidate.

## Evaluation boundary

The candidate contains a frozen allocation with:

- one representative public fixture;
- one hard semantic-boundary fixture;
- one valid counterexample;
- one reserved downstream case whose oracle is not committed to public Lattice.

Because the reserved oracle is external and withheld, the candidate must remain:

```text
blocked_pending_reserved_oracle
```

This PR does **not** claim a blind evaluation was executed.

That distinction is deliberate. A public repository cannot provide a credible hidden outcome to an author who can read the repository. A private downstream or controlled evaluator must supply the reserved oracle later.

## Failure-point taxonomy

The initial mapping is intentionally narrow:

```text
context_selection_gap            -> context_selection_change
low_value_attention_request      -> attention_gate_change
routing_or_tool_selection_error  -> routing_change | tool_surface_change
no_new_evidence_loop             -> stop_rule_change
verification_gap                 -> verifier_change
knowledge_freshness_gap          -> knowledge_freshness_change
recurring_skill_rule_gap         -> skill_or_rule_candidate
evaluator_too_permissive         -> eval_change
```

The validator rejects a candidate that uses one failure category to justify an unrelated primary mechanism.

## Architectural boundaries

This PR preserves:

- `feature_delivery_case` as the primary user-value and evidence boundary;
- Evidence Wayfinding as workflow/profile rather than active module;
- existing Helixion, AegisFlow, Memexa, FlowGuard, OpenClaw, and DeliveryYield tracks;
- `lattice-governor` as governance authority rather than creating a parallel governance Skill;
- candidate-only evolution with no auto-promotion;
- public-safe synthetic evidence only.

## Not implemented

This PR does not:

- modify any `skills/<name>/` package;
- create `frontier-practice-scout`;
- build a general mutation engine;
- create a team-wide evaluation service;
- expose a hidden reserved oracle in public source;
- execute canary or rollback orchestration;
- grant merge/release/deploy authority;
- infer private adoption, Senior Attention ROI, or manager value from public conformance.

## Acceptance checks

The PR is acceptable only if:

```text
candidate schema executes against the committed instance
candidate links exactly to Case 0 earliest failure
failure category permits the selected mechanism
incumbent and challenger are distinct
one-primary-delta structure is enforced
representative + hard + reserved allocations are present
reserved oracle remains evaluator-only and external
critical protected metrics cannot be dropped
candidate has owner + expiry + rollback
candidate cannot grant auto-promotion or team_available
CI runs structural, semantic, and negative tests
```

## Next gate

The next bounded PR should implement the **blind challenge execution contract**, not team promotion.

It should consume a Harness Mutation Candidate plus externally supplied reserved oracle, run incumbent/challenger under frozen target/evaluator/allocation, and emit one evaluation verdict from:

```text
reject
revise
continue_shadow
scoped_canary
```

The public implementation should be able to run without receiving private business content, while private downstream evaluation keeps real live/reserved evidence local.
