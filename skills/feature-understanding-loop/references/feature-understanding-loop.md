# Feature Understanding Loop Reference

## Purpose

This reference defines a bounded workflow for turning fragmented Feature knowledge into a reviewable delivery state. It is not a new module, a generic knowledge base, an autonomous coding agent, or a delivery verdict mechanism.

```text
Feature Delivery Case
-> Understanding Contract
-> bounded Context Pack
-> evidence-linked system and domain model
-> adversarial challenge
-> source, consistency, prediction, and teach-back verification
-> Work Ready or PR Ready projection
-> implementation and review evidence
-> Understanding Delta
-> reviewed reusable-asset candidate
```

## Three Nested Loops

### Evidence-grounded understanding inner loop

```text
contract -> sense -> model -> challenge -> verify -> commit
```

The inner loop stops when the named decision has sufficient evidence. It does not seek complete repository knowledge.

### Feature Delivery middle loop

```text
Ticket -> Work Ready -> Implementation -> PR Ready -> delivery evidence
```

Understanding is tested by the real work. New dependencies, review objections, test failures, and corrected assumptions become an Understanding Delta.

### Experience-to-Asset outer loop

```text
real use -> failure point -> candidate -> review -> scoped activation -> later reuse
```

A useful output is still only a candidate until source, scope, limitations, review, and activation are explicit.

## Sufficient Understanding Gate

For the named next decision:

1. every P0 claim is `evidenced` or `confirmed`, or is an explicit owned unknown;
2. no unresolved P0 conflict is hidden;
3. high-impact unknowns have an owner, latest-safe answer time, or explicit risk acceptance;
4. validation covers the user outcome and critical invariants;
5. the accountable role can explain the outcome, execution path, key control, and representative failure case;
6. generated interpretation remains distinguishable from confirmed requirement or runtime fact.

When these conditions are met, stop. More context is not automatically more understanding.

## Understanding Dimensions

| Dimension | Decision question | Typical evidence |
| --- | --- | --- |
| Intent | Why does this Feature exist and for whom? | requirement, product goal, user signal |
| Scope | What is included, excluded, and observable? | acceptance, non-goals, boundary cases |
| Domain | Which rules, terms, history, and prohibitions apply? | policy, ADR, incident, expert confirmation |
| System slice | Which entry points, modules, flows, and controls matter? | code, schema, config, trace, tests |
| Change model | What may change and in what order? | implementation plan, design decision, diff |
| Impact | Which consumers, teams, data, and operations may be affected? | call graph, ownership, contract, history |
| Evidence | How will outcome and invariants be verified? | tests, static analysis, logs, UAT |
| Operations | How are release, rollback, support, and communication handled? | runbook, owner confirmation, release plan |

## Claim Discipline

Use discrete states rather than a black-box understanding score:

- `unknown`: no sufficient information;
- `hypothesis`: plausible but unverified;
- `evidenced`: supported by a resolvable source;
- `confirmed`: confirmed by the accountable role or independent verification;
- `conflicted`: sources materially disagree;
- `stale`: evidence may no longer represent current behavior;
- `invalidated`: later evidence disproved the claim.

Every material claim records priority, evidence class, owner, evidence references, validation action, and blind spots.

## Challenge Set

The challenge phase must try to reject the current model rather than only enrich it:

- requirement, documentation, code, test, and decision contradictions;
- historical failed approaches and conditions under which they failed;
- hidden API, event, data, shared-library, operational, or human dependencies;
- stakeholders who may first see the impact late;
- stale assumptions caused by scale, dependency, organization, or policy changes;
- counterexamples across roles, regions, permissions, failure paths, retries, concurrency, and partial state;
- questions that must be answered before the next commitment gate.

A generic checklist is not evidence that a consequential gap exists.

## Verification Levels

- **V0 Source coverage:** material claims have evidence references or remain unknown.
- **V1 Consistency:** requirement, implementation, test, documentation, and decision sources do not hide conflicts.
- **V2 Predictive check:** the model can correctly predict a selected path, control, result, or impact.
- **V3 Teach-back:** the learner explains the Feature without copying the artifact.
- **V4 Delivery feedback:** implementation, tests, and review confirm or invalidate claims.

No model may self-certify readiness. A second model is another sensor, not proof.

## Understanding Delta

Record changes append-only:

```json
{
  "schema": "lat.understanding.delta.v1",
  "case_ref": "feature_delivery_case/fdc_example",
  "trigger": "pr_review",
  "added": ["claim_consumer_03"],
  "confirmed": ["claim_auth_01"],
  "invalidated": ["claim_single_consumer_02"],
  "conflicted": [],
  "stale": [],
  "remaining_unknowns": ["unknown_support_01"],
  "evidence_refs": ["github://example/repo/pull/42#review-comment-7"]
}
```

The delta preserves learning without rewriting history or promoting memory into belief.

## Module Boundaries

- AegisFlow orchestrates bounded transitions, retry, stop, and escalation.
- FlowGuard enforces path, tool, permission, risk, and human-gate policy.
- Memexa preserves source-scoped state and append-only events.
- Helixion aggregates completed traces and proposes improvement candidates; it does not modify production policy directly.
- DeliveryYield measures stage-level token or cost and waste after evidence is available; it does not approve readiness or delivery.
- Existing active modules remain valid development tracks.

## Initial Pilot Boundary

Use one team and 15 to 30 real brownfield Feature or PR cases. Phase 1 is read-only or draft-write only. It may generate Understanding State, Ticket Ready, Implementation Plan, PR Ready, and asset candidates. It may not edit code, merge, release, or auto-promote assets.

Primary pilot measures:

- false-ready rate;
- critical claim evidence coverage;
- P0 unknowns discovered before implementation or review;
- reviewer challenges already anticipated;
- repeated explanation or clarification events;
- human correction rate for factual claims;
- reuse of a scoped understanding asset in a later Feature.

Token and lead time remain secondary until evidence fidelity and false-ready controls pass.
