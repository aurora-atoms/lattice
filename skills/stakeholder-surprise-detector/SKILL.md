---
name: stakeholder-surprise-detector
description: Use to identify accountable roles likely to encounter a material change too late and object because user behavior, data, operations, support, compliance, architecture, contracts, or cross-team responsibilities are affected. Input is a bounded change, affected behaviors and systems, dependencies, historical reviewers, ownership boundaries, customer commitments, rollout timing, and evidence; output is an evidence-linked minimal-engagement plan naming potentially surprised roles, why, when to involve them, what decision or feedback is needed, and the smallest notification material. Do not use to invite everyone, infer personal reactions, rank people, or automatically escalate; preserve behavior, privacy, validation boundaries, and human authority.
---

# Stakeholder Surprise Detector

## Goal

Bring the smallest necessary accountable roles into a bounded change while feedback is still cheap, without expanding the process into broad consensus seeking.

## Use When

Use when a change affects external behavior, shared data, operations, support, compliance, architecture boundaries, another team's service, or a customer or policy commitment.

## Do Not Use When

Do not use to predict personalities, monitor individuals, invite all potentially interested people, infer objection from silence, or replace formal ownership and approval rules.

## Inputs

Require the bounded change, stage and next gate, affected users and behaviors, systems and dependencies, ownership boundaries, historical review evidence, customer or policy commitments, rollout timing, known decisions, and authorized stakeholder data.

## Outputs

Write by default to:

```text
artifacts/stakeholder-surprise/<case-id>/<run-id>/engagement-plan.v1.json
artifacts/stakeholder-surprise/<case-id>/<run-id>/review.md
artifacts/capability-runs/stakeholder-surprise-detector/<run-id>/run-result.json
```

When write permission is unavailable, return the complete artifact inline with `write_status=returned_inline`.

Include:

- accountable role or team boundary, not speculative personality labels;
- evidence that the change affects that role's responsibility or commitment;
- likely surprise reason and consequence if engagement is late;
- required decision, feedback, acknowledgement, or information only;
- earliest useful and latest-safe engagement time;
- smallest sufficient briefing material;
- owner for outreach and confirmation status;
- intentionally excluded roles and rationale.

## Evidence

Separate facts from inference. Record uncertainty, unknown ownership, assumptions, conflicting responsibility records, source dates, and scope. Historical participation and communication frequency are signals, not proof that a person must be involved.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- every proposed role is linked to a material responsibility or commitment;
- unnecessary participants are explicitly excluded;
- timing precedes the low-cost decision boundary;
- the requested involvement is specific and minimal;
- briefing material is sufficient without a full context dump;
- no personal reaction, blame, or performance judgment is inferred.

## Stop Conditions

Stop when the engagement plan or next reviewable stage is complete. Stop for missing permission, insufficient evidence, unclear ownership, privacy, security, compliance, safety, personnel-risk, or high-impact escalation boundaries, or when a human authority must decide participation. State the smallest next step.

## Workflow

1. Bound the change, affected outcomes, stage, gate, and disclosure boundary.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Map affected responsibilities, commitments, operations, and service boundaries.
4. Test each candidate role for material impact and required involvement type.
5. Minimize the participant set and prepare the smallest briefing material.
6. Stop for delivery-owner confirmation before outreach.

## Rules

SSD.001 | MUST | impact | link every proposed role to a material affected responsibility
SSD.002 | MUST | minimality | distinguish decision feedback acknowledgement and information-only needs
SSD.003 | MUST | timing | state earliest useful and latest-safe engagement times
SSD.004 | MUST | briefing | provide the smallest material needed for useful participation
SSD.005 | MUST | privacy | use role-level data and minimize personal details
SSD.006 | SHOULD | exclusions | record plausible roles intentionally excluded and why
SSD.007 | SHOULD | token | optimize quality-adjusted token ROI after engagement fidelity passes
SSD.008 | SHOULD | prompt | keep selection rules stable and change evidence dynamic
SSD.009 | NEVER | reaction | infer how a named person will feel or behave
SSD.010 | NEVER | broadcast | invite everyone because ownership evidence is incomplete

## Verification

- Each role has impact evidence, involvement type, timing, outreach owner, and briefing.
- Exclusions demonstrate participant minimization.
- Formal approval requirements remain distinct from courtesy notification.
- No outreach occurs without explicit authority.

## Failure Modes

- producing a broad stakeholder list;
- predicting objections from personality or seniority;
- involving roles after the decision is effectively irreversible;
- sending a full document dump instead of a minimal brief;
- confusing notification with approval.
