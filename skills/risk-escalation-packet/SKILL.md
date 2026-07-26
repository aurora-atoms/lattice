---
name: risk-escalation-packet
description: Use to turn a blocker, cross-team conflict, or material delivery risk that the current team cannot resolve into a decision-ready escalation packet. Input is a bounded Feature Delivery Case, one-line decision need, impact, affected users or systems, evidence, options, costs and tradeoffs, recommendation, confidence, latest-safe decision time, no-decision consequence, owner, audience, sensitivity, and authority boundary; output is a traceable packet and concise decision request. Do not use for routine status, automatic escalation, blame, unsupported urgency, or unauthorized commitments; preserve evidence, uncertainty, privacy, behavior, and final human decision authority.
---

# Risk Escalation Packet

## Goal

Convert “we are blocked” into the smallest complete package an accountable leader can use to decide, delegate, or request one bounded clarification.

## Use When

Use when a delivery blocker, cross-team dependency, material risk, resource conflict, or policy boundary cannot be resolved within the current team's authority and delay has a meaningful consequence.

## Do Not Use When

Do not use for routine status, low-impact issues with an existing owner, personnel blame, urgency inferred from message volume, or to bypass established security, compliance, architecture, product, or management authority.

## Inputs

Require a Feature Delivery Case or bounded issue, one-line decision request, current state, impact and affected scope, supporting evidence, material unknowns, options and tradeoffs, recommendation and confidence, latest-safe decision time, no-decision consequence, attempted resolution, accountable requester and decision owner, audience, sensitivity classification, and permission boundary.

## Outputs

Write by default to:

```text
artifacts/risk-escalations/<case-id>/<run-id>/risk-escalation-packet.v1.json
artifacts/risk-escalations/<case-id>/<run-id>/packet.md
artifacts/capability-runs/risk-escalation-packet/<run-id>/run-result.json
```

When write permission is unavailable, return the complete packet inline with `write_status=returned_inline`.

Include the one-line ask, impact, affected outcome, evidence, unknowns, latest-safe decision time, options and tradeoffs, recommendation with confidence and dissent, no-decision consequence, actions already attempted, requester, decision owner, and permitted audience. Keep background to the minimum needed to decide.

## Evidence

Separate facts from inference. Record uncertainty, unknowns, assumptions, conflicts, source dates, risk scope, and evidence quality. A deadline must be tied to an observable consequence. Recommendations must identify their evidentiary basis and residual risk. Communication volume, requester seniority, and generalized concern are not proof of urgency.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- the packet begins with one bounded decision request;
- impact and latest-safe decision time are evidence-backed;
- materially distinct options and tradeoffs are visible;
- recommendation strength matches evidence and uncertainty;
- the decision owner can decide or ask one bounded follow-up without rebuilding context.

## Stop Conditions

Stop when the packet is decision-ready or the requested escalation-preparation stage is complete. Stop for missing permission, insufficient evidence, unsupported urgency, unresolved decision ownership, privacy or compliance boundaries, conflicting impact evidence, or a high-risk decision requiring specialist or executive authority. Do not send, publish, or escalate automatically.

## Workflow

1. Bound the issue, impact, decision authority, audience, sensitivity, and latest-safe time.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Verify that the current team cannot resolve the issue within existing authority or policy.
4. State the one-line ask and evidence-backed consequence of delay.
5. Present materially distinct options, tradeoffs, and the smallest justified recommendation.
6. Compress background to decision-critical context and preserve unknowns or dissent.
7. Return the packet for requester and owner review; stop before escalation or commitment.

## Rules

REP.001 | MUST | request | lead with one bounded and answerable decision request
REP.002 | MUST | impact | connect urgency to evidence-backed consequence and latest-safe time
REP.003 | MUST | options | present materially distinct options and tradeoffs
REP.004 | MUST | recommendation | state confidence evidence basis dissent and residual risk
REP.005 | MUST | authority | preserve requester decision owner and specialist authority boundaries
REP.006 | SHOULD | token | optimize quality-adjusted token ROI after decision fidelity passes
REP.007 | SHOULD | prompt | keep escalation rules and output contract in a stable prefix
REP.008 | NEVER | action | send publish escalate or commit without explicit authority
REP.009 | NEVER | blame | use the packet for personnel blame ranking or pressure tactics

## Verification

- One-line ask, impact, options, recommendation, deadline, no-decision consequence, and owner are present.
- Urgency and recommendation are traceable to evidence.
- Unknowns, dissent, and residual risk remain visible.
- No automatic outreach or commitment is implied.

## Failure Modes

- describing only the problem;
- inventing urgency without a latest-safe consequence;
- offering several cosmetic variants of the same option;
- hiding uncertainty behind a strong recommendation;
- escalating before the responsible owner reviews the packet.
