# Evidence Wayfinding Evaluation and Governed Evolution

## Purpose

This document preserves the evaluation, correctness, learning, rollout, and rollback parts of the 2026-08-07 Evidence Wayfinding blueprint. It is a design reference. Thresholds must come from replay baselines and real usage evidence; this document does not invent unsupported precision.

## Evaluation order

Quality is evaluated before economics.

```text
contract validity
-> evidence integrity
-> target-relevant verification
-> human/production outcome where required
-> learning quality
-> human attention / token / tool economics
```

DeliveryYield may measure cost and waste after correctness evidence is available. It does not approve readiness, promotion, or delivery.

## North star

```text
Verified Decision Yield (VDY)
= verified_team_usable_deliverables / scarce_human_attention_minutes
```

A counted deliverable must be:

- evidence traceable;
- validated against the named target;
- directly usable by the team;
- associated with a real delivery-state change;
- bounded by preserved human authority.

Activity, tool calls, token count, code volume, or document count are not substitutes.

## Metric hierarchy

| Layer | Metrics | Failure prevented |
|---|---|---|
| North star | VDY | optimizing activity rather than usable delivery |
| Correctness | false-pass rate, unsupported-claim rate, conflict escape, target drift | fluent but wrong completion |
| Judgment | human override, decision reversal, decision latency, strongest-counterevidence coverage | fast but fragile decisions |
| Delivery | accepted artifact, review rework, escaped defect, time-to-state-change | artifacts that do not change real work |
| Learning | EIR, ECR, candidate-to-qualified, rollback rate, reuse success | “self-improvement” that introduces regressions |
| Economics | human minutes, token/tool cost, latency per accepted artifact | cost optimization before quality |

## Claim lifecycle

```text
UNKNOWN
  -> HYPOTHESIS
  -> EVIDENCED
  -> CONFIRMED
```

Any state may instead become:

```text
CONFLICTED
STALE
INVALIDATED
```

Rules:

- `UNKNOWN`: evidence insufficient; preserve visibly.
- `HYPOTHESIS`: falsifiable explanation; define verifier and counterexample.
- `EVIDENCED`: source-supported but not target-verified; may enter challenge.
- `CONFIRMED`: passed target-related validation within scope and cutoff.
- `CONFLICTED`: credible evidence disagrees; escalate, do not average.
- `STALE`: time/environment changed; revalidate before reuse.
- `INVALIDATED`: counterevidence or outcome disproved claim; preserve lineage.

## Verification ladder

| Priority | Verifier | What it can establish | What it cannot establish alone |
|---|---|---|---|
| 1 | schema / compiler / type / lint | structural validity | user outcome |
| 2 | reproducible failure / target test | behavior at target boundary | broad regression safety |
| 3 | regression / integration / static analysis | covered adjacent behavior | uncovered paths |
| 4 | independent evidence / semantic challenge | alternative explanations and blind spots | proof by model agreement |
| 5 | accountable human / production result | real decision or outcome acceptance | universal applicability |

Maker and Checker should be separated. If one model performs both roles, independent tests or data are mandatory. High-risk cases require a distinct role or human gate.

## Loop contract

Before a bounded loop starts, define:

```yaml
loop_contract:
  user_outcome: <named outcome>
  include: []
  exclude: []
  acceptance_observer: <human/system>
  forbidden_actions: []
  verifier: <named mechanism>
  allowed_state_changes: []
  max_iterations: <bounded integer>
  no_progress_condition: >
    two consecutive rounds with no new evidence, risk reduction,
    failure-surface reduction, or delivery-state change
```

The loop stops instead of spending more tokens when external feedback is missing.

## Error introduction and correction

The source blueprint uses this conceptual model:

```text
A(k+1) = A(k) * (1 - EIR) + (1 - A(k)) * ECR
```

Where:

- `EIR` is Error Introduction Rate: previously correct behavior becomes wrong because of the change loop.
- `ECR` is Error Correction Rate: previously wrong behavior becomes correct.

Implication: when baseline accuracy is already high, even a small EIR can dominate. More iteration is not automatically better.

## Candidate asset lifecycle

| State | Required evidence | Routing / authority |
|---|---|---|
| `idea` | one useful observation | case-local |
| `draft` | owner, scope, expected use | not auto-routed |
| `runnable` | complete executable/checkable contract | shadow only |
| `qualified_for_scope` | representative cases pass, risks bounded | assisted explicit use |
| `used_once` | one real success + Outcome Receipt | still not reusable proof |
| `reused` | second distinct success and stable boundary | eligible for team proposal |
| `team_available` | human review, version, rollback, expiry | task/profile-scoped availability |
| `deprecated` | regression, staleness, replacement | preserve lineage; stop routing |

No DeliveryYield asset candidate, model suggestion, or single case may skip this progression.

## Evolution Proposal

A reusable change should be represented before implementation as:

```yaml
proposal_id: <stable-id>
failure_point: <earliest observed failure>
affected_cases: []
proposed_asset_type: skill|rule|script|schema|example|eval|profile
proposed_diff: <bounded change>
expected_improvement: <metric + scope>
risk_of_regression: <false-pass / authority / drift risk>
representative_cases: []
reserved_cases: []
promotion_thresholds: {}
rollback_thresholds: {}
owner: <accountable human>
expiry: <review date>
status: candidate
```

## Evaluation design

### Freeze before comparison

Freeze:

- target contract;
- evidence cutoff;
- acceptance criteria;
- authority boundary;
- evaluation dataset split.

### Representative vs reserved cases

Representative cases may be used to develop and debug the candidate. Reserved cases are held back to estimate whether the candidate generalizes and whether its apparent gain is caused by outcome leakage.

The source blueprint suggested an initial target of roughly:

- 8-12 representative replay cases;
- 4-6 hidden/reserved cases.

These are rollout planning ranges, not stable kernel constants.

### Blind challenger comparison

For meaningful changes to methods, prompts, Skills, tools, context packs, routing, or profiles:

```text
incumbent
vs
challenger
```

The reviewer should not know which version generated the artifact when practical.

Evaluate both:

- final artifact quality;
- evidence support;
- target drift;
- authority violations;
- conflict/unknown preservation;
- repeated no-progress behavior;
- outcome leakage;
- human attention cost.

### Promotion and rollback

Thresholds must be written before promotion decisions. A strong anecdote becomes a hard case, not proof of general value.

A promoted candidate must have a rollback trigger, such as:

- false-pass rate exceeds baseline tolerance;
- unsupported claims increase;
- human overrides or reversals increase materially;
- the candidate causes scope or authority drift;
- required provider behavior becomes stale;
- the second-use boundary disappears;
- maintenance owner is no longer available.

## Failure-point corpus

Every failed or corrected case should preserve the earliest observed failure point. Add it to a hard-case corpus when legally and operationally allowed.

Do not:

- delete failed evidence because the final answer was corrected;
- train or tune against the reserved outcome and then still call that case a holdout;
- universalize a one-off reviewer preference;
- hide human corrections from later evaluation.

## Human feedback semantics

Human feedback is **failure-point discovery**, not generic approval.

Useful review prompts include:

```text
Which claim would you challenge first?
What is the strongest counterevidence missing here?
What would make you refuse to use this artifact?
Where is this likely to fail in three months?
What did the system assume that you had to correct?
```

A negative response is evidence about the system or asset. It is not a personnel score.

## Rollout sequence

The blueprint proposes:

```text
contract
-> shadow
-> assisted
-> cross-runtime task-scoped
-> governed growth
```

### Contract phase

Define Mission Anchor, workflow, profile, handoff contract, and replay cases. If the target cannot be stated or verifier is unreliable, stop before automation.

### Shadow phase

Run read-only beside existing work. Do not change real decisions. The goal is to expose real failure points, false passes, and drift.

### Assisted phase

A senior engineer explicitly invokes the workflow. Require bounded Decision Card and delivery artifact. Roll back when correctness worsens or human effort rises without compensating verified value.

### Cross-runtime phase

Add only adapters that pass the common conformance suite. Disable an adapter that loses goal, evidence, unknown, permission, or citation semantics.

### Governed growth

Promote only capabilities with repeated evidence, ownership, versioning, expiry, and rollback.

## Pre-mortem regression checklist

Before any Evidence Wayfinding capability change, ask:

- Could late context change the mission without a recorded decision?
- Could a one-case success modify global behavior?
- Could more tools be mistaken for better evidence?
- Could model consensus upgrade a claim without a verifier?
- Could compression remove counterevidence or unknowns?
- Could lower token cost hide higher review rework?
- Could an existing atomic capability become a mega Skill through scope expansion?
- Could a synthesis runtime be mistaken for an execution runtime?
- Could private evidence enter the public package?
- Could growth in activity be described as growth in capability?

Any `yes` answer requires an explicit control or a narrower change.
