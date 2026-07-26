---
name: delivery-immune-conversion
description: Use to convert a validated delivery lesson, defect, incident, escaped risk, expired assumption, or recurring failure into a proposed test, rule, preflight check, knowledge update, assumption expiry, monitoring trigger, or future review trigger with owner and validation. Input is a bounded Feature Delivery Case, failure evidence, root-contributing conditions, existing controls, affected scope, and human annotations; output is a traceable control-change proposal and closure plan. Do not use to auto-apply controls, punish teams, infer root cause without evidence, or bypass governance; preserve behavior, validation boundaries, uncertainty, and human authority.
---

# Delivery Immune Conversion

## Goal

Close the learning loop by turning validated lessons into bounded preventive or detective controls that can improve the next delivery.

## Use When

Use after an incident, escaped defect, near miss, recurring review finding, invalidated assumption, or verified delivery friction reveals a concrete gap in tests, rules, checks, knowledge, monitoring, or lifecycle triggers.

## Do Not Use When

Do not use for speculative lessons, automatic policy changes, personnel blame, broad process expansion, or controls whose cost and applicability have not been considered.

## Inputs

Require a bounded Feature Delivery Case, observed failure or lesson, evidence and observation window, contributing conditions, affected users or systems, existing controls and gaps, recurrence risk, proposed owner, and governance boundary.

## Outputs

Write by default to:

```text
artifacts/delivery-immune/<case-id>/<run-id>/control-proposal.v1.json
artifacts/delivery-immune/<case-id>/<run-id>/closure-plan.md
artifacts/capability-runs/delivery-immune-conversion/<run-id>/run-result.json
```

When write permission is unavailable, return the complete artifact inline with `write_status=returned_inline`.

Include:

- lesson or failure statement and affected outcome;
- evidence, contributing conditions, uncertainty, and root-cause status;
- current control and explicit gap;
- proposed control type: test, rule, check, preflight, knowledge update, assumption expiry, monitor, or trigger;
- insertion point in the lifecycle;
- scope, exceptions, owner, and approval authority;
- validation method and expected detection or prevention signal;
- control cost, false-positive risk, and removal or review trigger;
- implementation, verification, rollout, and closure evidence required;
- residual risk if the proposal is rejected or deferred.

## Evidence

Separate facts from inference. Record uncertainty, unknown causal links, assumptions, conflicting evidence, source dates, affected scope, and outcome impact. Distinguish root cause, contributing factor, detection gap, and process symptom. A painful event does not by itself justify a permanent control.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- the proposal addresses a demonstrated failure mechanism or detection gap;
- the smallest effective control is preferred over broad process expansion;
- lifecycle insertion point, owner, validation, and removal conditions are explicit;
- false-positive and operational costs are considered;
- implementation and promotion require accountable approval;
- closure depends on evidence, not creation of a tracking item.

## Stop Conditions

Stop when the requested control proposal or next reviewable stage is complete. Stop for missing permission, insufficient causal or failure evidence, safety or compliance boundaries, unresolved ownership, unacceptable control cost, conflicting controls, or an approval decision. State the exact gap and smallest next step.

## Workflow

1. Bound the case, lesson, outcome impact, control scope, and authority.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Distinguish the observed failure, contributing conditions, existing controls, and detection gap.
4. Generate the smallest plausible control options across test, rule, check, knowledge, expiry, monitor, and trigger categories.
5. Compare prevention value, detection value, cost, false positives, and transferability.
6. Select a recommended proposal with validation and removal conditions.
7. Stop before implementation or promotion unless separately authorized.

## Rules

DIC.001 | MUST | trace | link each control proposal to a Feature Delivery Case and failure evidence
DIC.002 | MUST | mechanism | identify the failure mechanism or detection gap addressed
DIC.003 | MUST | minimum | prefer the smallest effective control
DIC.004 | MUST | lifecycle | define insertion point owner validation and removal trigger
DIC.005 | MUST | authority | preserve implementation promotion and policy authority
DIC.006 | SHOULD | options | compare multiple control types before recommending one
DIC.007 | SHOULD | token | optimize quality-adjusted token ROI after control fidelity passes
DIC.008 | SHOULD | prompt | keep rules and output contract in a stable prefix
DIC.009 | NEVER | blame | use controls as punishment or personnel scoring
DIC.010 | NEVER | promotion | auto-apply or auto-promote the proposed control

## Verification

- Failure evidence, mechanism, current gap, and proposed control are linked.
- Owner, approval, validation, cost, residual risk, and removal trigger exist.
- Root cause and contributing factor are not conflated.
- Closure requires observed implementation and validation evidence.

## Failure Modes

- adding a checklist item after every incident;
- calling correlation a root cause;
- creating permanent controls without expiry or removal criteria;
- measuring closure by issue status rather than control effectiveness;
- proposing controls broader than the demonstrated risk.
