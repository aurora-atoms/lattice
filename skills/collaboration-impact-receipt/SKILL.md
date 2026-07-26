---
name: collaboration-impact-receipt
description: Use to make evidence-backed collaboration contributions visible when they changed a real delivery outcome, such as unblocking work, preventing risk, clarifying a decision, or enabling another team. Input is a bounded Feature Delivery Case, contribution description, before-and-after delivery state, evidence references, affected people or teams, participant confirmation, attribution limits, sensitivity, and owner; output is a confirmable impact receipt with changed outcome, evidence, shared contributions, uncertainty, and permitted audience. Do not use to rank people, infer performance from activity, claim sole credit, expose sensitive collaboration data, or publish without confirmation; preserve privacy, factual accuracy, behavior, and human authority.
---

# Collaboration Impact Receipt

## Goal

Make delivery-enabling collaboration visible without converting teamwork into surveillance, competition, or mechanical performance scoring.

## Use When

Use after a contribution materially changed a delivery state: removed a blocker, prevented a risk, resolved a cross-team dependency, improved evidence, enabled a decision, or helped another person complete work.

## Do Not Use When

Do not use for routine activity logging, personnel ranking, inferred attribution from messages or commits, unconfirmed claims, or contributions whose disclosure would create privacy, security, or organizational harm.

## Inputs

Require a Feature Delivery Case or bounded task, contribution and timing, prior delivery state, changed state, affected outcome, evidence references, participants and shared contributions, beneficiary or participant confirmation, attribution limits, sensitivity classification, intended audience, accountable owner, and permission boundary.

## Outputs

Write by default to:

```text
artifacts/collaboration-impact/<case-id>/<run-id>/impact-receipt.v1.json
artifacts/collaboration-impact/<case-id>/<run-id>/receipt.md
artifacts/capability-runs/collaboration-impact-receipt/<run-id>/run-result.json
```

When write permission is unavailable, return the complete receipt inline with `write_status=returned_inline`.

Include the contribution, delivery state before and after, affected user or team outcome, evidence references, participant confirmation status, shared and enabling contributions, attribution limits, uncertainty, permitted audience, owner, and correction path. Do not emit a score, rank, or comparative performance claim.

## Evidence

Separate observed facts from derived outcome links and judged attribution. Record uncertainty, unknowns, assumptions, conflicting accounts, source dates, and applicability scope. Message volume, meeting count, commit count, seniority, and model inference are not sufficient evidence of impact. Preserve participant corrections and disputed attribution.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- the receipt links a contribution to a real delivery-state change;
- affected participants can confirm, correct, or dispute the account;
- shared contributions and attribution limits are visible;
- sensitive details are minimized for the intended audience;
- the artifact supports recognition or learning without becoming a personnel score.

## Stop Conditions

Stop when the receipt is reviewable or the requested recognition stage is complete. Stop for missing permission, insufficient evidence, absent participant confirmation, unresolved attribution conflict, privacy or compliance boundaries, or any personnel decision requiring accountable human authority. Do not publish, distribute, or attach the receipt to performance processes automatically.

## Workflow

1. Bound the Feature Delivery Case, contribution, audience, sensitivity, and authority.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Establish the delivery state before and after the contribution.
4. Link only evidence-supported contribution effects and identify shared contributors.
5. Request or record participant confirmation, correction, dispute, or not-evaluated status.
6. Minimize sensitive detail and state attribution limits.
7. Return the receipt for owner review; stop before publication or personnel use.

## Rules

CIR.001 | MUST | outcome | link recognition to a changed delivery outcome rather than activity volume
CIR.002 | MUST | evidence | distinguish observed events derived links judged attribution and unknowns
CIR.003 | MUST | confirmation | preserve participant confirmation correction and dispute states
CIR.004 | MUST | attribution | represent shared contributions and attribution limits
CIR.005 | MUST | privacy | minimize sensitive collaboration and personnel data
CIR.006 | SHOULD | token | optimize quality-adjusted token ROI after factual fidelity passes
CIR.007 | SHOULD | prompt | keep evidence and output rules in a stable prefix
CIR.008 | NEVER | personnel | rank score monitor or infer individual performance
CIR.009 | NEVER | publication | publish or use the receipt for personnel decisions without explicit authority

## Verification

- The receipt names a real delivery-state change and supporting evidence.
- Confirmation, dispute, unknowns, and attribution limits are explicit.
- No activity-based score, ranking, or hidden personnel inference is present.
- Audience and correction path are defined.

## Failure Modes

- crediting visible activity instead of changed outcomes;
- assigning sole credit to a shared result;
- treating silence as confirmation;
- exposing sensitive interpersonal details;
- turning recognition artifacts into surveillance or rankings.
