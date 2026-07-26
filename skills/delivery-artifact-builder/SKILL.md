---
name: delivery-artifact-builder
description: Use to route a bounded Feature Delivery Case to the smallest evidence-linked specialist that produces a visible Ticket Ready, implementation-plan, reviewer-rehearsal, PR Ready, test-asset, delivery-readiness, or PR-to-release artifact. Input is lifecycle stage, requested audience and decision, requirements, context, diff, decisions, tests, risks, release constraints, owners, and evidence; output is a specialist selection and editable delivery artifact with explicit gaps and confirmations. Do not use to perform all seven analyses by default, commit scope or dates, approve merge or release, fabricate evidence, or replace accountable owners; preserve behavior, validation boundaries, facts, uncertainty, and human authority.
---

# Delivery Artifact Builder

## Goal

Route delivery work to the smallest specialist that converts individual understanding into a visible, actionable, auditable artifact.

## Use When

Select exactly one primary specialist:

- E01 `ticket-ready-package` — turn a requirement into goals, non-goals, acceptance, impact, tests, risks, questions, and suggested splits.
- E02 `implementation-plan` — externalize work decomposition, dependencies, critical path, validation, parallel work, and expert decisions.
- E03 `reviewer-rehearsal` — rehearse material reviewer challenges and missing evidence before review.
- E04 `pr-ready-package` — explain a change's intent, rationale, impact, evidence, risks, monitoring, and rollback.
- E05 `test-asset-package` — produce focused executable validation assets and explicit coverage gaps.
- E06 `delivery-readiness-card` — state goal, current state, delivery gaps, launch risks, evidence, next actions, and owners.
- E07 `pr-to-release-summary` — translate merged or release-candidate changes into usable QA, product, support, and operations information.

## Do Not Use When

Do not use this selector to conduct deep specialist analysis itself, compose every artifact by default, commit scope or dates, approve merge or release, or fabricate completion evidence.

## Inputs

Require a bounded Feature Delivery Case or change, lifecycle stage and next gate, requested audience and decision, source metadata, permission boundary, owners, dates, and the minimum evidence needed to select a specialist.

## Outputs

Write the selected specialist result to its declared artifact path and write the routing result to:

```text
artifacts/capability-runs/delivery-artifact-builder/<run-id>/run-result.json
```

When write permission is unavailable, return the routing decision and selected artifact inline with `write_status=returned_inline`.

Include the selected specialist, selection reason, excluded specialists, required inputs, evidence gaps, human confirmations, and stop reason.

## Evidence

Separate facts from inference. Record citations, uncertainty, unknowns, assumptions, conflicts, source dates, and scope. Artifact selection must follow lifecycle need and evidence, not a desire to generate more documentation.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- one smallest sufficient specialist is selected;
- the result matches the lifecycle stage and intended audience;
- evidence and gaps are explicit;
- the artifact is editable, traceable, and actionable;
- unnecessary artifacts and duplicated context are avoided;
- scope, date, merge, release, and risk authority remain human-controlled.

## Stop Conditions

Stop when the requested visible artifact or next reviewable stage is complete. Stop for missing permission, insufficient evidence, unresolved security privacy compliance or production risk, unavailable owners, conflicting lifecycle state, human decision requirements, or scope expansion. State what is missing and the smallest next step.

## Workflow

1. Bound the Feature Delivery Case, lifecycle stage, next gate, audience, decision need, and authority.
2. Query ConPort first when available; otherwise use targeted authorized sources.
3. Select one primary E01–E07 specialist based on the state transition required.
4. Activate only the selected Skill and task-critical sources.
5. Add a second specialist only for a named dependency, evidence gap, or independent validation need.
6. Record excluded capabilities and avoid duplicating source artifacts.
7. Return the specialist artifact and stop before approval or commitment authority.

## Routing Rules

- Route unclear or unstartable requirements to `ticket-ready-package`.
- Route approved, complex, cross-module, or multi-contributor work to `implementation-plan`.
- Route an important change before review to `reviewer-rehearsal`.
- Route a reviewable diff or PR needing shared context to `pr-ready-package`.
- Route missing executable validation to `test-asset-package`.
- Route milestone, release-candidate, handoff, or management status needs to `delivery-readiness-card`.
- Route merged or release-candidate changes needing cross-role communication to `pr-to-release-summary`.

## Rules

ECAT.001 | MUST | routing | select one primary specialist before composition
ECAT.002 | MUST | lifecycle | route by required state transition audience and next gate
ECAT.003 | MUST | evidence | distinguish verified evidence from missing claimed or planned evidence
ECAT.004 | MUST | artifact | make output editable traceable actionable and linked to the Feature Delivery Case
ECAT.005 | MUST | human | preserve scope date staffing merge release publication and risk authority
ECAT.006 | SHOULD | composition | add a second specialist only for a named dependency or evidence gap
ECAT.007 | SHOULD | token | optimize quality-adjusted token ROI after artifact fidelity passes
ECAT.008 | SHOULD | prompt | keep rules and output contract in a stable prefix
ECAT.009 | NEVER | breadth | compose all seven specialists by default
ECAT.010 | NEVER | authority | approve merge release scope commitment or publication
ECAT.011 | NEVER | evidence | fabricate tests readiness decisions deployment or completion
ECAT.012 | NEVER | selector | perform deep specialist analysis instead of routing

## Verification

- The selected Skill is the smallest sufficient capability for the requested state change.
- Excluded Skills and any composition reason are explicit.
- The artifact matches lifecycle stage, audience, evidence, and authority.
- Owners can edit and confirm the result.

## Failure Modes

- generating a document bundle instead of solving the current delivery need;
- routing by keyword rather than lifecycle state;
- using activity lists instead of delivery evidence;
- duplicating the Feature Delivery Case into every artifact;
- claiming tests, readiness, deployment, or approval without evidence.
