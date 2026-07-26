---
name: pr-ready-package
description: Use to turn a bounded code change and its delivery evidence into an editable PR Ready Package explaining what changed, why, affected scope, acceptance mapping, tests, risks, monitoring, rollback, unresolved items, and owner confirmations. Input is a diff or branch, ticket, implementation plan, decisions, test results, contracts, risks, and release constraints; output is an evidence-linked package for reviewers, QA, product, and maintainers. Do not use to fabricate tests, approve merge, conceal risk, or replace the PR author; preserve behavior, validation boundaries, facts, uncertainty, and human authority.
---

# PR Ready Package

## Goal

Make a pull request understandable and reviewable without requiring each role to reconstruct intent and evidence from the diff.

## Use When

Use when a change is ready to request review or when an existing PR lacks sufficient intent, validation, impact, risk, or rollback context.

## Do Not Use When

Do not use to claim tests passed without records, approve merge, rewrite disputed intent as fact, or hide unresolved issues to make a PR appear complete.

## Inputs

Require a bounded diff or branch, Feature Delivery Case, ticket and acceptance criteria, implementation plan, decisions and assumptions, contracts and affected consumers, test and CI evidence, risks, rollout or rollback constraints, owners, and permission boundary.

## Outputs

Write by default to:

```text
artifacts/pr-ready/<case-id>/<run-id>/pr-ready.v1.json
artifacts/pr-ready/<case-id>/<run-id>/pr-ready.md
artifacts/capability-runs/pr-ready-package/<run-id>/run-result.json
```

When write permission is unavailable, return the complete artifact inline with `write_status=returned_inline`.

Include:

- concise change summary and intended user or system outcome;
- design rationale and alternatives relevant to review;
- affected modules, contracts, consumers, data, operations, and users;
- acceptance-criterion-to-evidence mapping;
- tests executed, results, environment, and evidence locations;
- tests or validation still missing;
- risks, known limitations, monitoring, rollout, and rollback;
- unresolved decisions and required reviewers or owners;
- author confirmation fields and links to source artifacts.

## Evidence

Separate facts from inference. Record citations, uncertainty, unknowns, assumptions, conflicts, source dates, and scope. Claimed or planned validation must not be represented as executed evidence.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- reviewers can explain what changed, why, and which outcomes or contracts are affected;
- acceptance criteria map to actual or explicitly missing evidence;
- test results are reproducible and distinguish executed from planned validation;
- risks, limitations, monitoring, and rollback are visible;
- unresolved decisions are routed to accountable roles;
- the package remains editable and does not imply merge approval.

## Stop Conditions

Stop when the requested PR Ready Package or next reviewable stage is complete. Stop for missing permission, insufficient evidence, security or privacy risk, unavailable diff or test records, unresolved scope authority, material contract conflict, or required human judgment. State the gap and smallest next step.

## Workflow

1. Bound the PR, case, acceptance, review stage, and authority.
2. Query ConPort first when available; otherwise use targeted authorized sources.
3. Compare the diff with the ticket, plan, decisions, contracts, and affected surfaces.
4. Map acceptance and risks to executed evidence and explicit gaps.
5. Add rationale, monitoring, rollback, limitations, and owner confirmations.
6. Reuse relevant reviewer-rehearsal and test-asset outputs without duplicating them wholesale.
7. Produce the editable package and stop before merge approval.

## Rules

PRP.001 | MUST | intent | explain change outcome rationale and affected scope
PRP.002 | MUST | evidence | distinguish executed passed failed planned and missing validation
PRP.003 | MUST | acceptance | map criteria to addressable evidence or explicit gaps
PRP.004 | MUST | operations | include monitoring rollout rollback and known limitations when applicable
PRP.005 | MUST | human | preserve author reviewer merge release and product authority
PRP.006 | SHOULD | context | link to detailed artifacts instead of duplicating large histories
PRP.007 | SHOULD | token | optimize quality-adjusted token ROI after package fidelity passes
PRP.008 | SHOULD | prompt | keep rules and output contract in a stable prefix
PRP.009 | NEVER | evidence | fabricate test results decisions or reviewer confirmations
PRP.010 | NEVER | approval | claim merge or release approval

## Verification

- Summary, rationale, impact, evidence, gaps, risks, and rollback are present.
- Test states and evidence locations are explicit.
- The package matches the actual diff and ticket scope.
- Human confirmations and unresolved decisions remain visible.

## Failure Modes

- paraphrasing the diff without explaining intent;
- listing tests without results or evidence locations;
- suppressing known limitations;
- treating a generated PR description as approval;
- duplicating entire source documents instead of linking them.
