---
name: human-judgment-amplifier
description: Use to select the smallest evidence-backed capability for scarce-expert attention, real-case mentorship, or participant-confirmed collaboration impact. Input is a bounded decision request, Feature Delivery Case evidence, options, risks, deadlines, review history, learning goals, and confirmed contribution outcomes; output is one governed decision queue, mentorship case, or impact receipt with source traceability, uncertainty, privacy controls, and human confirmation. Do not use to automate final expert judgment, rank or monitor people, infer performance from activity, or expose sensitive collaboration data; preserve behavior, authority, validation boundaries, and quality-adjusted token ROI.
---

# Human Judgment Amplifier

## Goal

Increase the leverage of expert attention, judgment transfer, and collaboration evidence without replacing people or creating surveillance incentives.

## Use When

Select one primary capability:

- G01 `senior-attention-queue`: prioritize expert decisions by material impact, latest-safe decision time, reversibility, and required expertise; provide the minimum sufficient context and identify delegable preparation.
- G02 `mentorship-case-builder`: convert a real decision, review, or delivery case into a teach-back exercise with clues, alternatives, boundary conditions, and an expert-reviewed rationale.
- G03 `collaboration-impact-receipt`: make unblock, risk-prevention, mentoring, or cross-team help visible through participant-confirmed changes in delivery state rather than activity volume.

## Do Not Use When

Do not use for personnel ranking, performance scoring, automated final decisions, unconfirmed attribution, or collection of unnecessary private collaboration data.

## Inputs

Require a bounded decision, learning, or impact-visibility need; Feature Delivery Case or source context; evidence and source references; applicable options, risks, and time limits; accountable owner; participant or expert confirmation requirements; and the permission boundary.

## Outputs

Write the selector record to:

```text
artifacts/human-judgment/<run-id>/capability-selection.v1.json
artifacts/capability-runs/human-judgment-amplifier/<run-id>/run-result.json
```

When write permission is unavailable, return the selector decision and selected artifact inline with `write_status=returned_inline`.

The selector record must include the selected capability, excluded capabilities, reason, source scope, expected artifact, accountable owner, confirmation point, privacy boundary, and authority boundary.

## Evidence

Separate facts from inference. Record uncertainty, unknowns, assumptions, conflicts, source dates, participant confirmation status, and applicability scope. Message volume, meeting count, review count, seniority, or model confidence is not evidence of impact or decision priority.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- one primary G01-G03 specialist matches the need;
- the artifact reduces avoidable expert preparation, creates a reusable learning case, or documents a confirmed delivery-state change;
- final judgment and attribution remain human-controlled;
- sensitive information is minimized;
- no personnel score, ranking, or surveillance signal is produced.

## Stop Conditions

Stop when the selected artifact or next reviewable stage is complete. Stop for missing permission, insufficient evidence, unresolved ownership, absent participant or expert confirmation, privacy or safety boundaries, conflicting attribution, or a decision that requires accountable human authority. State the blocker and smallest next step.

## Workflow

1. Bound the Feature Delivery Case, decision or learning target, evidence window, audience, and authority.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Select one primary G01-G03 specialist and record why the others are excluded.
4. Activate only task-critical evidence and tools.
5. Add a second specialist only for a named dependency or independent validation gap.
6. Preserve human confirmation, privacy, and final decision authority.
7. Stop before contacting people, assigning credit, or making a final expert decision.

## Rules

GCAT.001 | MUST | routing | select one primary G01 through G03 specialist before composing
GCAT.002 | MUST | evidence | link priority learning and impact claims to bounded delivery evidence
GCAT.003 | MUST | human | preserve final expert judgment and participant confirmation
GCAT.004 | MUST | privacy | minimize sensitive collaboration and personnel data
GCAT.005 | SHOULD | composition | add another specialist only for a named dependency or validation gap
GCAT.006 | SHOULD | token | optimize quality-adjusted token ROI after evidence fidelity passes
GCAT.007 | SHOULD | prompt | keep selector rules and output contract in a stable prefix
GCAT.008 | NEVER | personnel | rank score or monitor people
GCAT.009 | NEVER | authority | automate final expert decisions attribution or performance conclusions

## Verification

- The selected specialist matches the stated decision, learning, or impact need.
- Evidence, uncertainty, confirmation, privacy, and authority boundaries are explicit.
- Excluded specialists are recorded.
- The artifact can be reviewed without reconstructing the full conversation history.

## Failure Modes

- prioritizing the loudest requester instead of the most material decision;
- treating one reviewer style as universal judgment;
- crediting activity instead of a confirmed delivery-state change;
- exposing sensitive collaboration details;
- producing a hidden personnel score.
