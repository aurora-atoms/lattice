---
name: implementation-plan
description: Use to turn a confirmed Ticket Ready Package and system evidence into an editable implementation plan with work decomposition, dependencies, sequence, critical path, validation checkpoints, risks, parallel work, unknowns, and expert decision points. Input is a bounded Feature Delivery Case, approved scope, code and architecture maps, constraints, team capability, owners, deadlines, and evidence; output is a reviewable plan and explicit gaps. Do not use to command developers, assign people or dates without authority, replace task-packet-builder, or treat a suggested sequence as mandatory; preserve behavior, validation boundaries, uncertainty, and human control.
---

# Implementation Plan

## Goal

Externalize the work, dependencies, order, validation, and unknowns required to move an approved ticket into coordinated execution.

## Use When

Use when a task spans modules, requires decomposition, has multiple contributors, contains uncertain dependencies, or needs a critical-path discussion before implementation.

## Do Not Use When

Do not use to invent scope, allocate people without authority, force one implementation strategy, or convert unresolved architecture or product decisions into hidden assumptions.

## Inputs

Require a confirmed Ticket Ready Package or equivalent approved scope, Feature Delivery Case, system and code maps, repository constraints, dependencies, acceptance criteria, existing tests, risks, owners, deadlines, and permission boundary.

## Outputs

Write by default to:

```text
artifacts/implementation-plans/<case-id>/<run-id>/implementation-plan.v1.json
artifacts/implementation-plans/<case-id>/<run-id>/plan.md
artifacts/capability-runs/implementation-plan/<run-id>/run-result.json
```

When write permission is unavailable, return the complete artifact inline with `write_status=returned_inline`.

Include:

- work breakdown by user-visible slice and technical enabler;
- dependency and sequencing graph;
- critical path and latest-safe decision points;
- validation checkpoints and expected evidence;
- parallelizable work and merge or integration points;
- risks, assumptions, unknowns, and fallback options;
- expert decisions with smallest required context and owner;
- recommended task boundaries and completion evidence;
- explicit plan gaps and confirmation requests.

## Evidence

Separate facts from inference. Record citations, uncertainty, unknowns, assumptions, conflicts, source dates, and applicability scope. Proposed sequencing and effort are recommendations until confirmed by accountable engineers.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- the team can explain the critical path and what can proceed in parallel;
- every planned slice has a validation point and completion evidence;
- material unknowns and expert decisions are visible before implementation;
- dependencies and integration points are explicit;
- developers can edit or reject the plan without losing source evidence;
- the plan does not create unauthorized staffing or schedule commitments.

## Stop Conditions

Stop when the requested implementation plan or next reviewable stage is complete. Stop for missing permission, insufficient evidence, unresolved scope authority, architecture or security risk, absent owners, material contradictions, or a required expert decision. State the gap, responsible role, and smallest next step.

## Workflow

1. Bound the case, approved scope, stage, next gate, and authority.
2. Query ConPort first when available; otherwise use targeted authorized sources.
3. Decompose by user-visible slices, enabling work, and validation boundaries.
4. Map dependencies, critical path, integration points, and parallel work.
5. Identify unknowns and expert decisions without filling them with guesses.
6. Define validation evidence for each slice and the whole feature.
7. Produce the editable plan and stop for engineering confirmation.

## Collaboration Boundaries

- `ticket-ready-package` supplies confirmed scope and acceptance.
- `system-mental-model` supplies bounded system topology and change impact.
- `decision-question-builder` prepares expert decision requests.
- `task-packet-builder` may convert an approved plan into executable task packets.
- `feature-delivery-case` remains the canonical lifecycle record.

## Rules

IPL.001 | MUST | decomposition | separate user-visible slices from enabling work
IPL.002 | MUST | dependency | expose order critical path integration points and parallel work
IPL.003 | MUST | validation | attach expected evidence to every planned slice
IPL.004 | MUST | unknowns | keep unresolved decisions explicit with owner and latest-safe time
IPL.005 | MUST | human | preserve developer architecture staffing and schedule authority
IPL.006 | SHOULD | plan | prefer the smallest plan sufficient for coordination
IPL.007 | SHOULD | token | optimize quality-adjusted token ROI after plan fidelity passes
IPL.008 | SHOULD | prompt | keep rules and output contract in a stable prefix
IPL.009 | NEVER | certainty | present estimates or sequencing guesses as confirmed facts
IPL.010 | NEVER | authority | assign people dates architecture or implementation strategy without confirmation

## Verification

- Work items map to acceptance or a named enabling dependency.
- Critical path, parallel work, validation, risks, and expert decisions are explicit.
- Proposed and confirmed content are distinguishable.
- The plan links to rather than replaces the Feature Delivery Case.

## Failure Modes

- producing a generic checklist unrelated to the codebase;
- decomposing by files instead of delivery and validation boundaries;
- hiding unknowns inside implementation tasks;
- treating the plan as an immutable command;
- omitting integration and end-to-end validation.
