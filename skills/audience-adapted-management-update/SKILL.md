---
name: audience-adapted-management-update
description: Use to project the same validated Feature Delivery Case evidence into an audience- and channel-appropriate management update, including a one-page brief, oral-update outline, risk package, or decision record. Input is authoritative delivery facts, lifecycle state, business purpose, evidence, risks, unknowns, decisions, audience role, communication channel, time limit, sensitivity, owner, and source references; output is a concise traceable projection with preserved meaning, explicit omissions, decision context, and owner review. Do not use to alter facts for persuasion, hide uncertainty, create commitments, expose unnecessary detail, or publish without approval; preserve behavior, evidence fidelity, privacy, and human authority.
---

# Audience Adapted Management Update

## Goal

Use one evidence base to produce the right management format for the audience without changing delivery state, material risk, uncertainty, or decision ownership.

## Use When

Use when the same feature or delivery issue must be communicated to different management levels or channels, such as a one-page brief, a short oral update, a risk review, or a durable decision record.

## Do Not Use When

Do not use when source facts are unresolved, to optimize persuasion by suppressing material information, to substitute generated wording for approved commitments, or to expose technical or sensitive detail the audience does not need.

## Inputs

Require a bounded Feature Delivery Case or management source packet, business purpose, current lifecycle state, authoritative facts and evidence references, material risks and unknowns, next milestone, decision context, audience role, channel and time limit, sensitivity classification, required and prohibited details, accountable owner, and permission boundary.

## Outputs

Write by default to:

```text
artifacts/management-updates/<case-id>/<run-id>/audience-update.v1.json
artifacts/management-updates/<case-id>/<run-id>/update.md
artifacts/capability-runs/audience-adapted-management-update/<run-id>/run-result.json
```

When write permission is unavailable, return the complete update inline with `write_status=returned_inline`.

State the selected format, audience need, business purpose, current state, evidence, material risks, next milestone, decisions or asks, unknowns, intentionally omitted detail with reason, source references, owner review status, and publication authority. Oral updates must include a concise opening, evidence-backed status, risk or decision point, and close with the required action.

## Evidence

Separate facts from inference. Record uncertainty, unknowns, assumptions, conflicts, source dates, lifecycle state, metric definitions, and source scope. The projection may reduce detail but must not change claim strength, status, risk, or decision meaning. Record material omissions explicitly rather than silently deleting them.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- the selected format matches the audience, channel, and decision need;
- all claims remain traceable to the same source evidence;
- material risk, uncertainty, and required decisions remain visible;
- unnecessary technical and sensitive detail is minimized;
- the accountable owner can review and approve the projection without reconstructing its evidence base.

## Stop Conditions

Stop when the requested projection or owner-review stage is complete. Stop for missing permission, insufficient evidence, unresolved source conflict, privacy or compliance boundaries, unclear audience or decision need, absent owner, or publication and commitment authority. Do not send or publish automatically.

## Workflow

1. Bound the source evidence, audience, channel, time limit, sensitivity, decision need, and owner authority.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Establish the invariant facts, lifecycle state, material risks, and decision context.
4. Select the smallest suitable format: one-page brief, oral update, risk package, or decision record.
5. Project only audience-relevant evidence and record material omissions.
6. Check that claim strength, uncertainty, risk, and ownership remain unchanged.
7. Return the projection for owner review; stop before publication or commitment.

## Rules

AMU.001 | MUST | source | use one authoritative evidence base for every audience projection
AMU.002 | MUST | fidelity | preserve claim strength lifecycle state material risk and uncertainty
AMU.003 | MUST | audience | minimize detail according to audience channel and decision need
AMU.004 | MUST | omission | record material omissions and their reasons
AMU.005 | MUST | human | require accountable owner review before publication or commitment
AMU.006 | SHOULD | token | optimize quality-adjusted token ROI after factual fidelity passes
AMU.007 | SHOULD | prompt | keep projection rules and output contract in a stable prefix
AMU.008 | NEVER | persuasion | alter or suppress material facts to improve narrative appearance
AMU.009 | NEVER | action | send publish or commit without explicit authority

## Verification

- Format, audience, purpose, status, risks, decision need, and source references are present.
- Claims match the source evidence and lifecycle terminology.
- Material omissions and sensitivity handling are explicit.
- Owner review and publication authority are stated.

## Failure Modes

- using one generic update for every audience;
- shortening content by removing the decision context;
- changing an uncertain claim into a confident statement;
- exposing implementation details that do not affect management action;
- treating generated wording as approved communication.
