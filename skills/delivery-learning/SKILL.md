---
name: delivery-learning
description: Use to select the smallest evidence-backed organizational-learning capability for a Feature Delivery Case: maintain the canonical case, capture a scoped judgment playbook, extract a reusable delivery pattern, convert a validated lesson into a control proposal, review feature outcomes, or define a measurement plan. Input is bounded lifecycle intent, decisions, tests, incidents, releases, outcomes, metrics, user feedback, and owner annotations; output is one versioned learning artifact with scope, evidence, owner, review, expiry, and promotion status. Do not use to auto-promote memory, rules, Skills, tests, or automation, approve delivery, or replace product judgment; preserve behavior, validation boundaries, uncertainty, and human authority.
---

# Delivery Learning

## Goal

Make one delivery improve the next while keeping the Feature Delivery Case as the canonical lifecycle object and separating learning candidates from approved organizational assets.

## Use When

Select one primary capability:

- F01 `feature-delivery-case`: maintain intent, change history, decisions, assumptions, evidence, responsibilities, readiness, release path, and learning across the lifecycle.
- F02 `delivery-judgment-playbook`: record when a recurring judgment applies, required evidence, mandatory steps, exceptions, owner, and review trigger.
- F03 `reusable-delivery-pattern`: extract a reusable pattern, checklist, failure signals, and transferable versus non-transferable parts from multiple cases.
- F04 `delivery-immune-conversion`: convert a validated lesson, defect, incident, escaped risk, or expired assumption into a proposed test, rule, check, knowledge update, monitor, or trigger.
- F05 `feature-outcome-review`: compare intended outcomes with observed results and recommend continue, adjust, expand, pause, stop, or insufficient evidence.
- F06 `measurement-plan-pack`: define success criteria, leading and lagging indicators, instrumentation, observation windows, guardrails, and decision rules.

## Do Not Use When

Do not use to store verbatim conversation history, generalize from one case, auto-promote candidates, approve delivery or policy, or reduce product value to one metric.

## Inputs

Require a bounded Feature Delivery Case or learning target, lifecycle stage, source evidence, target decision or reuse need, accountable owner, applicability scope, and permission boundary. Use only the additional evidence required by the selected specialist.

## Outputs

Write the selected specialist artifact to its declared path and write the run result to:

```text
artifacts/capability-runs/delivery-learning/<run-id>/run-result.json
```

When write permission is unavailable, return the selector decision and specialist artifact inline with `write_status=returned_inline`.

The selector record must include the selected capability, excluded capabilities, reason, source scope, expected artifact, owner, review point, and authority boundary.

## Evidence

Separate facts from inference. Record uncertainty, unknowns, assumptions, conflicts, source dates, case scope, and outcome quality. Preserve source IDs and lifecycle history. A repeated practice, released feature, or successful case is not by itself proof of transferability or value.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- one primary specialist matches the lifecycle learning need;
- learning is linked to a Feature Delivery Case;
- candidate, approved, rejected, superseded, and expired states remain distinct;
- applicability, owner, review, expiry, and evidence are explicit;
- outcome and measurement work preserves multiple indicators and product judgment;
- no memory, rule, test, Skill, or automation is promoted without accountable review.

## Stop Conditions

Stop when the selected artifact or next reviewable stage is complete. Stop for missing permission, insufficient evidence, unresolved ownership, privacy or safety boundaries, conflicting learning, undefined promotion authority, or an accountable product or governance decision. State the exact blocker and smallest next step.

## Workflow

1. Bound the Feature Delivery Case, lifecycle event, learning target, evidence window, and authority.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Select one primary F01-F06 specialist based on the required organizational change or decision.
4. Record why other specialists are excluded.
5. Activate only task-critical sources and tools.
6. Invoke a second specialist only for a named dependency, evidence gap, or independent validation need.
7. Preserve candidate status, applicability, owner, review, and expiry.
8. Stop before promotion, approval, or automated action.

## Rules

FCAT.001 | MUST | object | use the Feature Delivery Case as the primary lifecycle learning unit
FCAT.002 | MUST | routing | select one primary F01 through F06 specialist before composing
FCAT.003 | MUST | evidence | preserve source scope result and uncertainty
FCAT.004 | MUST | promotion | separate candidates from approved memory rules Skills tests and automation
FCAT.005 | MUST | lifecycle | require owner review and expiry or reopen conditions
FCAT.006 | MUST | metrics | preserve multi-metric product judgment
FCAT.007 | SHOULD | composition | add a second specialist only for a named dependency or validation gap
FCAT.008 | SHOULD | token | optimize quality-adjusted token ROI after learning fidelity passes
FCAT.009 | SHOULD | prompt | keep selector rules and output contract in a stable prefix
FCAT.010 | NEVER | memory | store unfiltered conversations logs or traces as organizational memory
FCAT.011 | NEVER | promotion | auto-promote single-case learning
FCAT.012 | NEVER | authority | approve delivery policy product continuation or control implementation

## Verification

- The selected specialist matches the stated learning need.
- Learning is linked to a Feature Delivery Case and source evidence.
- Candidate status, applicability, owner, review, and expiry are explicit.
- Excluded specialists and authority boundaries are recorded.

## Failure Modes

- treating learning as a retrospective document rather than a changed future behavior;
- storing raw history instead of high-signal records;
- universalizing one successful case;
- creating controls without validation or removal conditions;
- equating release with product success;
- selecting metrics after seeing the result.
