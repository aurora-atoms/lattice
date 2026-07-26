---
name: test-asset-package
description: Use to convert acceptance criteria, implementation evidence, historical defects, domain constraints, and delivery risks into a focused Test Asset Package containing executable test candidates, test data, boundary and negative cases, manual validation, expected outcomes, and evidence mapping. Input is a bounded Feature Delivery Case, code or design, existing tests, incidents, risks, environments, and owner priorities; output is an editable validation asset and explicit coverage gaps. Do not use to claim tests ran, generate low-value test volume, approve quality, or replace engineering judgment; preserve behavior, validation boundaries, facts, uncertainty, and human authority.
---

# Test Asset Package

## Goal

Turn testing ideas into focused, executable, reusable quality assets linked to acceptance criteria and material delivery risks.

## Use When

Use during implementation, bug fixing, PR preparation, release readiness, or whenever critical behavior lacks executable or clearly assigned validation.

## Do Not Use When

Do not use to maximize test count, duplicate existing coverage without evidence, claim execution results, or decide coverage priorities without engineering and product authority.

## Inputs

Require a bounded Feature Delivery Case, acceptance criteria, code or design evidence, existing test inventory, relevant incidents and defects, domain rules, contracts, risks, target environments, test-data constraints, owners, and permission boundary.

## Outputs

Write by default to:

```text
artifacts/test-assets/<case-id>/<run-id>/test-assets.v1.json
artifacts/test-assets/<case-id>/<run-id>/test-plan.md
artifacts/capability-runs/test-asset-package/<run-id>/run-result.json
```

When write permission is unavailable, return the complete artifact inline with `write_status=returned_inline`.

Include:

- acceptance and risk coverage map;
- executable unit, integration, contract, end-to-end, regression, or failing-test candidates;
- test data and environment prerequisites;
- boundary, negative, failure, recovery, and permission cases;
- expected outcomes and evidence-capture instructions;
- manual or expert validation items;
- existing coverage reused and duplication intentionally avoided;
- coverage gaps, priorities, owners, and next validation action.

## Evidence

Separate facts from inference. Record citations, uncertainty, unknown behavior, assumptions, conflicting requirements, source dates, and scope. Generated tests are candidates until implemented; implemented tests are not execution evidence until results are available.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- material acceptance criteria and risks map to executable or assigned validation;
- generated assets have expected outcomes and reproducible prerequisites;
- existing coverage is reused rather than duplicated;
- boundary and failure behavior are visible;
- execution state is accurately distinguished from test design state;
- engineers retain coverage and quality authority.

## Stop Conditions

Stop when the requested Test Asset Package or next reviewable stage is complete. Stop for missing permission, insufficient evidence, unavailable environments or data, privacy or security risk, unresolved expected behavior, unsafe test execution, or required human prioritization. State the gap and smallest next step.

## Workflow

1. Bound the feature, acceptance, risks, environments, and execution permissions.
2. Query ConPort first when available; otherwise use targeted authorized sources.
3. Inventory existing coverage before proposing new assets.
4. Map criteria and material risks to the smallest sufficient validation set.
5. Define data, prerequisites, expected outcomes, and evidence capture.
6. Separate executable automation candidates from manual or expert checks.
7. Produce the package and stop before execution or quality approval unless explicitly authorized.

## Rules

TAP.001 | MUST | mapping | link every asset to acceptance risk incident or contract evidence
TAP.002 | MUST | state | distinguish proposed implemented executed passed failed and blocked
TAP.003 | MUST | reproducibility | state prerequisites data environment expected result and evidence capture
TAP.004 | MUST | efficiency | inventory and reuse existing coverage before adding tests
TAP.005 | MUST | human | preserve engineering product security and quality authority
TAP.006 | SHOULD | coverage | prioritize material boundaries failures and regressions over test volume
TAP.007 | SHOULD | token | optimize quality-adjusted token ROI after validation fidelity passes
TAP.008 | SHOULD | prompt | keep rules and output contract in a stable prefix
TAP.009 | NEVER | evidence | claim execution or passing status without test records
TAP.010 | NEVER | volume | generate repetitive tests solely to increase count

## Verification

- Every proposed asset has a source reason and expected outcome.
- Test state and evidence location are explicit.
- Data, environment, permission, and privacy constraints are visible.
- Gaps and manual checks have owners or owner-needed status.

## Failure Modes

- generating a large generic test list;
- confusing written test cases with executed tests;
- ignoring existing coverage;
- omitting failure recovery and permission boundaries;
- using synthetic test volume as proof of quality.
