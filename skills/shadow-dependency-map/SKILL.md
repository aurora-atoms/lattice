---
name: shadow-dependency-map
description: Use to expose hidden delivery dependencies that are absent from architecture diagrams or formal plans, including approvals, scarce experts, data access, environments, operational handoffs, and cross-team waits. Input is a bounded Delivery Case, workflow events, wait evidence, review history, ownership boundaries, dependencies, deadlines, and available alternatives; output is an evidence-linked dependency map with bottlenecks, single points of delay, substitute paths, coordination actions, and owners. Do not use for personnel scoring, surveillance, blame, or unsupported escalation; preserve privacy, least privilege, uncertainty, and human authority.
---

# Shadow Dependency Map

## Goal

Reveal the real technical, organizational, approval, data, environment, and expertise dependencies that can delay a bounded delivery before the team reaches them unexpectedly.

## Use When

Use when a plan repeatedly waits despite appearing complete, a change crosses ownership boundaries, a scarce expert or approval may become a bottleneck, or release timing depends on informal coordination.

## Do Not Use When

Do not use to measure employee performance, infer intent from communication volume, map unrelated social relationships, or disclose sensitive personnel information beyond the authorized task boundary.

## Inputs

Require a bounded Delivery Case or change, current stage and next gate, formal dependencies, workflow and wait evidence, review and approval history, accountable roles, deadlines, privacy boundary, and known alternative paths.

## Outputs

Write by default to:

```text
artifacts/shadow-dependencies/<case-id>/<run-id>/dependency-map.v1.json
artifacts/shadow-dependencies/<case-id>/<run-id>/review.md
artifacts/capability-runs/shadow-dependency-map/<run-id>/run-result.json
```

When write permission is unavailable, return the complete artifact inline with `write_status=returned_inline`.

Include:

- dependency nodes and directed wait relationships;
- dependency type: technical, approval, expertise, data, environment, vendor, operational, or coordination;
- evidence and observation window;
- single points of delay and capacity constraints;
- earliest-needed and latest-safe engagement times;
- substitute path, delegation, pre-approval, batching, or sequencing options;
- minimum coordination action, owner, and confirmation point;
- privacy exclusions and confidence limits.

## Evidence

Separate fact from inference. Record uncertainty, unknown dependencies, assumptions about availability or authority, source date, scope, and conflicting evidence. Communication frequency alone is not proof of dependency or bottleneck status.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- hidden dependencies are linked to observable wait or gate evidence;
- the map distinguishes system constraints from individual blame;
- single points and substitute paths are explicit;
- coordination can begin before the dependency becomes blocking;
- owners and confirmation times are actionable;
- privacy and disclosure limits are preserved.

## Stop Conditions

Stop when the requested dependency map or next reviewable stage is complete. Stop for missing permission, insufficient evidence, unavailable owners, unresolved privacy or security constraints, compliance or personnel-risk boundaries, scope expansion, or a human authority decision. State the missing item and smallest next step.

## Workflow

1. Bound the case, stage, gate, observation window, and disclosure boundary.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Normalize formal and observed dependencies without inferring personal motives.
4. Build directed wait paths and identify single points, queue pressure, and latest-safe engagement times.
5. Test substitute paths, delegation, pre-approval, sequencing, and minimum coordination options.
6. Produce the map and stop for accountable-owner confirmation.

## Rules

SDM.001 | MUST | scope | bind every dependency to one delivery case stage and gate
SDM.002 | MUST | evidence | link dependency claims to observable wait approval ownership or access evidence
SDM.003 | MUST | alternatives | identify substitute paths or state why none are known
SDM.004 | MUST | timing | state earliest-needed and latest-safe coordination times
SDM.005 | MUST | privacy | minimize personnel data and disclose only task-relevant roles
SDM.006 | SHOULD | action | recommend the smallest coordination action that reduces delay exposure
SDM.007 | SHOULD | token | optimize quality-adjusted token ROI after dependency fidelity passes
SDM.008 | SHOULD | prompt | keep mapping rules stable and case evidence dynamic
SDM.009 | NEVER | blame | convert system bottlenecks into personnel scoring or fault attribution
SDM.010 | NEVER | escalation | escalate an inferred dependency without evidence and owner review

## Verification

- Each edge has type, evidence, timing, owner, and scope.
- Bottlenecks distinguish capacity, authority, access, and sequencing causes.
- Alternatives and minimum coordination actions are present.
- Sensitive details are excluded or role-abstracted.

## Failure Modes

- reproducing the formal architecture diagram without real waits;
- equating a named person with the problem;
- listing dependencies without timing or alternatives;
- inviting every stakeholder by default;
- inferring dependency from message counts or calendar density.
