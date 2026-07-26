---
name: management-translation
description: Use to select the smallest evidence-backed management communication capability for a Feature Delivery Case: an executive feature brief, a decision-ready risk escalation, or an audience-adapted update. Input is bounded delivery state, business purpose, outcome and readiness evidence, risks, options, milestones, deadlines, resource or decision requests, source references, and audience level; output is one traceable management artifact focused on purpose, delivered state, next milestone, material risk, quantified evidence, and required decision. Do not use to hide uncertainty, beautify status, invent commitments, or expose unnecessary technical or sensitive detail; preserve factual accuracy, behavior, validation boundaries, human approval, and quality-adjusted token ROI.
---

# Management Translation

## Goal

Turn technical delivery evidence into concise, accurate, actionable management material without losing uncertainty, risk, or decision ownership.

## Use When

Select one primary capability:

- H01 `executive-feature-brief`: create a one-page feature brief covering business purpose, evidence-backed delivery state, next milestone, material risks, required decisions, and quantified evidence.
- H02 `risk-escalation-packet`: turn an unresolved blocker, cross-team conflict, or material risk into a decision-ready request with impact, options, tradeoffs, recommendation, latest-safe decision time, and no-decision consequence.
- H03 `audience-adapted-management-update`: project validated source material into an audience- and channel-specific one-page brief, oral update, decision record, or status narrative without changing the underlying facts or risk.

## Do Not Use When

Do not use to hide risk, create unauthorized commitments, replace source evidence, publish without owner approval, or expose unnecessary sensitive detail.

## Inputs

Require a bounded Feature Delivery Case or management question, business purpose, current lifecycle state, evidence and source references, next milestone, material risks and unknowns, decisions or resource requests, audience and channel, sensitivity classification, accountable owner, and permission boundary.

## Outputs

Write the selector record to:

```text
artifacts/management-translation/<run-id>/capability-selection.v1.json
artifacts/capability-runs/management-translation/<run-id>/run-result.json
```

When write permission is unavailable, return the selector decision and selected artifact inline with `write_status=returned_inline`.

The selector record must include the selected capability, excluded capabilities, audience, decision need, source scope, expected artifact, owner review point, sensitivity boundary, and authority boundary.

## Evidence

Separate facts from inference. Record uncertainty, unknowns, assumptions, conflicts, source dates, metric definitions, and lifecycle state. Distinguish merged, deployed, released, enabled, exposed, and outcome-observed states. Commits, PR count, token count, and agent activity are engineering evidence or operating signals, not the primary value statement.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- one primary H01-H03 specialist matches the audience and decision need;
- business purpose, delivery state, next milestone, material risk, evidence, and decision request remain visible;
- the material can be used with light owner editing rather than source reconstruction;
- recommendation strength matches evidence quality;
- no risk, uncertainty, or sensitive boundary is silently removed.

## Stop Conditions

Stop when the requested artifact or next reviewable stage is complete. Stop for missing permission, insufficient evidence, unresolved metric or lifecycle state, privacy or compliance boundaries, conflicting sources, absent owner, or a commitment, escalation, publication, or executive decision requiring accountable human authority.

## Workflow

1. Bound the Feature Delivery Case, audience, communication channel, decision need, sensitivity, and authority.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Select one primary H01-H03 specialist and record why the others are excluded.
4. Project only the evidence needed by that audience.
5. Preserve lifecycle state, uncertainty, material risks, options, and decision ownership.
6. Add another specialist only for a named dependency or independent validation gap.
7. Stop before publication, commitment, escalation, or final management decision.

## Rules

HCAT.001 | MUST | routing | select one primary H01 through H03 specialist before composing
HCAT.002 | MUST | evidence | preserve source traceability lifecycle state and uncertainty
HCAT.003 | MUST | audience | minimize detail without removing decision context
HCAT.004 | MUST | human | require owner confirmation for recommendations commitments and publication
HCAT.005 | SHOULD | composition | add another specialist only for a named dependency or validation gap
HCAT.006 | SHOULD | token | optimize quality-adjusted token ROI after factual fidelity passes
HCAT.007 | SHOULD | prompt | keep selector rules and output contract in a stable prefix
HCAT.008 | NEVER | narrative | hide material risk or unknowns for presentation quality
HCAT.009 | NEVER | metric | lead with commits PR count tokens or agent activity as final value

## Verification

- The selected specialist matches the audience, format, and decision need.
- Purpose, lifecycle state, evidence, risk, milestone, and decision request remain traceable.
- Sensitive details are minimized rather than concealed inconsistently.
- Owner review and publication authority are explicit.

## Failure Modes

- leading with engineering activity instead of user or business delivery state;
- removing risk to make status look better;
- presenting generated wording as an approved commitment;
- mixing source facts with inferred narrative;
- using one format for every audience.
