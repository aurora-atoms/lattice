---
name: executive-feature-brief
description: Use to turn a bounded Feature Delivery Case into a one-page, evidence-backed executive brief that answers why the feature matters, what has actually been delivered, what comes next, which risks are material, what decision is needed, and what quantified evidence supports the status. Input is business purpose, lifecycle state, readiness and outcome evidence, milestones, risks, unknowns, resource or decision requests, audience, sensitivity, and owner; output is a concise traceable brief and structured record. Do not use to replace source evidence, hide uncertainty, report engineering activity as business value, invent dates or commitments, or publish without approval; preserve factual accuracy, behavior, privacy, and human authority.
---

# Executive Feature Brief

## Goal

Give management a concise, decision-useful view of a feature's purpose, evidence-backed state, next milestone, material risks, and required action.

## Use When

Use for weekly or milestone updates, leadership reviews, portfolio discussions, cross-functional synchronization, or a request for a one-page feature status grounded in a Feature Delivery Case.

## Do Not Use When

Do not use when the underlying delivery state or evidence is unavailable, to turn technical activity into an unsupported value claim, to remove material risk for presentation quality, or to make commitments on behalf of accountable owners.

## Inputs

Require a bounded Feature Delivery Case, business or user purpose, target outcome, non-goals, current lifecycle state, delivered capabilities, readiness and outcome evidence, next milestone and prerequisites, material risks and unknowns, decision or resource requests, metric definitions, audience level, sensitivity classification, accountable owner, and permission boundary.

## Outputs

Write by default to:

```text
artifacts/management-briefs/<case-id>/<run-id>/executive-feature-brief.v1.json
artifacts/management-briefs/<case-id>/<run-id>/brief.md
artifacts/capability-runs/executive-feature-brief/<run-id>/run-result.json
```

When write permission is unavailable, return the complete brief inline with `write_status=returned_inline`.

The one-page brief must include: business purpose; current delivery state; what is delivered and usable; next milestone and prerequisites; top material risks and mitigations; quantified evidence with definitions; decisions or resources needed; latest-safe decision time when applicable; owner; and known unknowns. Distinguish merged, deployed, released, enabled, exposed, and outcome-observed states.

## Evidence

Separate facts from inference. Record uncertainty, unknowns, assumptions, conflicts, source dates, metric definitions, observation windows, and applicability scope. Commits, pull requests, token count, and agent activity may support traceability but are not the primary value statement. Quantification without a reliable denominator or definition must be marked not evaluated.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- the brief explains purpose and user or business relevance before technical activity;
- current lifecycle state and delivered capability are evidence-backed;
- next milestone, material risks, and required decisions are explicit;
- quantified evidence includes definitions and limitations;
- an accountable owner can use the brief with light editing rather than reconstructing source material.

## Stop Conditions

Stop when the brief is reviewable or the requested management stage is complete. Stop for missing permission, insufficient evidence, unresolved lifecycle state, unreliable metrics, privacy or compliance boundaries, conflicting sources, absent owner, or a scope, date, funding, staffing, release, or executive decision requiring human authority. Do not publish automatically.

## Workflow

1. Bound the Feature Delivery Case, audience, decision need, sensitivity, and owner authority.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Confirm the business purpose, target outcome, and current lifecycle state.
4. Select only evidence that changes management understanding or action.
5. State delivered capability, next milestone, material risks, quantified evidence, and required decisions.
6. Remove unnecessary implementation detail without changing facts or uncertainty.
7. Return the brief for owner review; stop before publication or commitment.

## Rules

EFB.001 | MUST | purpose | lead with user or business purpose rather than engineering activity
EFB.002 | MUST | state | distinguish merged deployed released enabled exposed and outcome-observed states
EFB.003 | MUST | evidence | preserve sources metric definitions uncertainty and unknowns
EFB.004 | MUST | decision | make required management action and owner explicit
EFB.005 | MUST | human | require accountable owner review before publication or commitment
EFB.006 | SHOULD | token | optimize quality-adjusted token ROI after factual fidelity passes
EFB.007 | SHOULD | prompt | keep brief rules and output contract in a stable prefix
EFB.008 | NEVER | narrative | hide material risk or uncertainty to improve appearance
EFB.009 | NEVER | metric | treat commits pull requests tokens or agent activity as final value

## Verification

- Purpose, delivery state, delivered capability, next milestone, risks, evidence, and decision need are present.
- Lifecycle terminology and metrics match source evidence.
- Unknowns and limitations remain visible.
- Owner review and publication authority are explicit.

## Failure Modes

- producing an engineering activity list;
- calling a merged change delivered to users;
- presenting unsupported numbers without definitions;
- burying the decision request;
- omitting risk to make status appear green.
