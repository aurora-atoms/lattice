---
name: delivery-readiness-card
description: Use to summarize a bounded feature's delivery state into an editable evidence-linked card showing the goal, current state, remaining gaps, launch risks, critical evidence, next actions, owners, and confirmation points. Input is a Feature Delivery Case with ticket, PR, tests, dependencies, risks, compliance, decisions, rollout, and release evidence; output is a scoped readiness status and an explicit answer to what remains before delivery. Do not use to replace release authority, hide gaps behind a score, fabricate evidence, or equate task completion with user-usable delivery; preserve behavior, validation boundaries, uncertainty, and human control.
---

# Delivery Readiness Card

## Goal

Give the team and managers one evidence-linked answer to: what is the intended delivery, where is it now, and exactly what remains before it can be released safely.

## Use When

Use at milestones, release-candidate preparation, management review, cross-team handoff, or whenever delivery status is fragmented across tickets, PRs, tests, risks, and decisions.

## Do Not Use When

Do not use to approve release, compress readiness into a percentage, treat merged code as delivery, or conceal missing evidence to produce a favorable status.

## Inputs

Require a bounded Feature Delivery Case, intended user outcome, current lifecycle stage and target gate, ticket and acceptance, implementation and PR evidence, tests, dependencies, risks, compliance or security review state, unresolved decisions, rollout and rollback plan, owners, dates, and permission boundary.

## Outputs

Write by default to:

```text
artifacts/delivery-readiness/<case-id>/<run-id>/readiness-card.v1.json
artifacts/delivery-readiness/<case-id>/<run-id>/readiness-card.md
artifacts/capability-runs/delivery-readiness-card/<run-id>/run-result.json
```

When write permission is unavailable, return the complete artifact inline with `write_status=returned_inline`.

Use one scoped status:

- `ready_for_owner_review`;
- `conditionally_ready`;
- `not_ready`;
- `insufficient_evidence`.

Include:

- delivery goal and target gate;
- current state supported by evidence;
- completed evidence and unresolved gaps;
- launch, migration, operational, support, security, privacy, compliance, and dependency risks;
- critical evidence links and freshness;
- next action, owner, latest-safe time, and expected closure evidence;
- conditions attached to conditional readiness;
- explicit release authority and required confirmations;
- a plain-language statement of what is still missing before delivery.

## Evidence

Separate facts from inference. Record citations, uncertainty, unknowns, assumptions, conflicts, source dates, scope, and evidence freshness. Activity completion, PR merge, or test count alone does not prove user-usable delivery.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- the team can state exactly what remains before the target gate;
- managers can reuse the card without reconstructing technical activity;
- every material gap has an owner, next action, and expected evidence;
- readiness status is explainable from evidence without a black-box score;
- launch and operational risk remain visible;
- accountable humans retain release and risk-acceptance authority.

## Stop Conditions

Stop when the requested readiness card or next reviewable stage is complete. Stop for missing permission, insufficient evidence, stale or conflicting status, security privacy compliance or production risk, absent owner, unresolved release decision, or scope expansion. State the gap and smallest next step.

## Workflow

1. Bound the case, target gate, status time, audience, and authority.
2. Query ConPort first when available; otherwise use targeted authorized sources.
3. Gather only current evidence needed to establish state, gaps, and risks.
4. Distinguish completed activity from validated delivery evidence.
5. Assign the narrowest supported status and conditions.
6. Convert each material gap into a next action, owner, time, and closure evidence.
7. Produce the card and stop before release approval.

## Rules

DRC.001 | MUST | goal | state the user-usable outcome and target delivery gate
DRC.002 | MUST | state | support status with current addressable evidence
DRC.003 | MUST | gaps | name missing evidence decision dependency or control precisely
DRC.004 | MUST | action | attach owner next action latest-safe time and closure evidence to material gaps
DRC.005 | MUST | human | preserve release risk acceptance product and operational authority
DRC.006 | SHOULD | audience | keep the main card management-usable and link technical detail
DRC.007 | SHOULD | token | optimize quality-adjusted token ROI after readiness fidelity passes
DRC.008 | SHOULD | prompt | keep rules and output contract in a stable prefix
DRC.009 | NEVER | score | replace readiness composition with an unexplained percentage or score
DRC.010 | NEVER | approval | declare a release approved or safe beyond the evidence and authority boundary

## Verification

- Goal, current state, gaps, risks, evidence, next actions, owners, and confirmations are present.
- Status follows from evidence and stated conditions.
- The card says what is missing before delivery in plain language.
- Release approval remains explicitly outside the Skill.

## Failure Modes

- reporting activity instead of delivery state;
- using green CI as the only readiness signal;
- assigning a percentage without composition;
- omitting owner and closure evidence from gaps;
- presenting conditional readiness as approval.
