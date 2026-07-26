---
name: feature-outcome-review
description: Use to compare a delivered feature's intended user or business outcome with observed results and produce an evidence-backed continue, adjust, expand, pause, or stop recommendation plus the learning that should update the Feature Delivery Case. Input is goals, success criteria, assumptions, release and enablement evidence, metrics, qualitative feedback, observation windows, guardrails, and costs; output is a scoped outcome review with gaps, failed assumptions, confidence limits, next decision, owner, and review trigger. Do not use to infer causality from weak data, equate release with success, or replace product authority; preserve behavior, validation boundaries, uncertainty, and human judgment.
---

# Feature Outcome Review

## Goal

Close the loop on whether the team delivered the right outcome, not merely whether it completed the planned work.

## Use When

Use after a feature has been released or enabled for a defined observation window, when a product decision depends on actual adoption, behavior, value, risk, or operational evidence.

## Do Not Use When

Do not use before meaningful exposure exists, when release and enablement status are unknown, when the observation window is too short for the stated outcome, or to replace accountable product decisions.

## Inputs

Require a Feature Delivery Case, original goal and non-goals, success criteria, leading and lagging indicators, assumptions, release and enablement evidence, affected cohort, observation window, guardrails, qualitative feedback, costs, incidents, and accountable owner.

## Outputs

Write by default to:

```text
artifacts/feature-outcomes/<case-id>/<run-id>/outcome-review.v1.json
artifacts/feature-outcomes/<case-id>/<run-id>/review.md
artifacts/capability-runs/feature-outcome-review/<run-id>/run-result.json
```

When write permission is unavailable, return the complete artifact inline with `write_status=returned_inline`.

Include:

- intended outcome, success criteria, and original assumptions;
- release, deployment, enablement, exposure, and observation status;
- observed leading, lagging, guardrail, cost, and qualitative evidence;
- target-versus-result comparison;
- unmet or invalidated assumptions;
- alternative explanations and causal confidence;
- segment, environment, and time-window limitations;
- recommendation: `continue`, `adjust`, `expand`, `pause`, `stop`, or `insufficient_evidence`;
- next action, owner, decision authority, and next review trigger;
- learning candidates and proposed Feature Delivery Case updates.

## Evidence

Separate facts from inference. Record uncertainty, unknowns, assumptions, conflicts, source dates, metric definitions, exposure quality, and applicability scope. Distinguish correlation from causal evidence. Missing or delayed metrics must not be treated as zero impact.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- the review compares intended outcomes with observed evidence rather than delivery activity;
- release, enablement, exposure, and observation states are distinct;
- assumptions and alternative explanations are explicit;
- recommendation strength matches evidence quality;
- learning is linked back to the Feature Delivery Case;
- accountable product authority retains the final continue, adjust, or stop decision.

## Stop Conditions

Stop when the requested outcome review or next reviewable stage is complete. Stop for missing permission, insufficient exposure, unreliable metrics, unresolved metric definitions, privacy or safety boundaries, material confounding, absent owner, or a product decision. State what evidence or time window is still required.

## Workflow

1. Bound the Feature Delivery Case, intended outcome, cohort, window, and decision authority.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Confirm deployed, released, enabled, and exposed states before evaluating outcomes.
4. Compare targets with leading, lagging, guardrail, cost, and qualitative evidence.
5. Test original assumptions and plausible alternative explanations.
6. Calibrate confidence and produce the smallest justified recommendation.
7. Propose case updates and learning candidates; stop for product-owner decision.

## Rules

FOR.001 | MUST | outcome | compare observed user or business outcomes with original goals
FOR.002 | MUST | states | distinguish deployed released enabled exposed and observed
FOR.003 | MUST | assumptions | identify confirmed invalidated and untested assumptions
FOR.004 | MUST | confidence | match recommendation strength to evidence quality and window
FOR.005 | MUST | authority | preserve product continue adjust expand pause and stop authority
FOR.006 | SHOULD | segments | inspect material cohort and environment differences
FOR.007 | SHOULD | token | optimize quality-adjusted token ROI after outcome fidelity passes
FOR.008 | SHOULD | prompt | keep rules and output contract in a stable prefix
FOR.009 | NEVER | causality | claim causal impact from correlation alone
FOR.010 | NEVER | completion | equate merge release or task closure with product success

## Verification

- Goal, result, assumptions, alternative explanations, confidence, and recommendation are present.
- Metric definitions and observation windows are explicit.
- Missing evidence leads to `insufficient_evidence`, not a guessed conclusion.
- Proposed learning does not auto-promote into memory, rules, or Skills.

## Failure Modes

- reviewing output volume instead of user outcome;
- evaluating before sufficient exposure;
- treating missing data as failure or success;
- using one aggregate metric while guardrails deteriorate;
- rewriting the original goal after seeing the result.
