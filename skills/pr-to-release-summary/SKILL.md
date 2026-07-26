---
name: pr-to-release-summary
description: Use to translate a merged or release-candidate change into an editable cross-role summary explaining what changed, who or what is affected, how to validate it, known limitations, rollout and rollback, and support or operations notes. Input is a bounded Feature Delivery Case, PR Ready Package, merged diff, ticket, tests, configuration, user impact, rollout, rollback, and owner evidence; output is an evidence-linked release communication artifact with sensitive details filtered. Do not use to publish automatically, make unsupported public claims, approve release, or replace product, support, operations, and release owners; preserve behavior, validation boundaries, uncertainty, privacy, and human authority.
---

# PR-to-Release Summary

## Goal

Translate implementation evidence into release information that QA, product, support, operations, and affected teams can use directly.

## Use When

Use after PR merge, during release-candidate preparation, before rollout, or when release notes and support guidance require one consistent evidence-linked source.

## Do Not Use When

Do not use to announce an unapproved release, expose sensitive implementation or customer data, claim user impact without evidence, or replace role-specific final wording and publication authority.

## Inputs

Require a bounded Feature Delivery Case, PR Ready Package or equivalent, merged diff or release candidate, ticket and intended outcome, tests and validation evidence, configuration or migration changes, affected users and systems, rollout and rollback plan, known limitations, support and operations constraints, owners, audience, and permission boundary.

## Outputs

Write by default to:

```text
artifacts/release-summaries/<case-id>/<run-id>/release-summary.v1.json
artifacts/release-summaries/<case-id>/<run-id>/release-summary.md
artifacts/capability-runs/pr-to-release-summary/<run-id>/run-result.json
```

When write permission is unavailable, return the complete artifact inline with `write_status=returned_inline`.

Include:

- what changed and the intended user or operational outcome;
- affected users, roles, systems, integrations, data, and support paths;
- validation instructions and expected observable behavior;
- rollout sequence, feature flags, migration, monitoring, and rollback;
- known limitations, exclusions, and residual risks;
- support, incident-response, and operations notes;
- audience-specific wording candidates labeled draft;
- sensitive or internal details intentionally excluded;
- owner confirmations and publication or release authority.

## Evidence

Separate facts from inference. Record citations, uncertainty, unknowns, assumptions, conflicts, source dates, scope, and validation freshness. A merged PR is implementation evidence, not proof of deployment, adoption, or successful user outcome.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- affected roles can understand the change without reading the diff;
- validation, monitoring, limitations, rollback, and support actions are usable;
- internal and external claims remain within evidence and disclosure boundaries;
- different audiences receive consistent facts without unnecessary detail;
- owners can edit and confirm the summary;
- the artifact does not imply release or publication approval.

## Stop Conditions

Stop when the requested release summary or next reviewable stage is complete. Stop for missing permission, insufficient evidence, unresolved privacy security compliance or disclosure risk, unavailable rollout or rollback information, conflicting release state, absent owner, or required publication decision. State the gap and smallest next step.

## Workflow

1. Bound the release candidate, audience, disclosure class, target stage, and authority.
2. Query ConPort first when available; otherwise use targeted authorized sources.
3. Verify change, validation, configuration, rollout, rollback, and affected surfaces.
4. Separate implementation, deployment, release, and outcome states.
5. Draft one factual core and project only the minimum audience-specific detail.
6. Add limitations, support, monitoring, rollback, and excluded sensitive detail.
7. Produce the editable summary and stop before publication or release approval.

## Rules

PRS.001 | MUST | state | distinguish merged deployed released enabled and outcome-observed states
PRS.002 | MUST | audience | preserve one factual core while minimizing audience-specific detail
PRS.003 | MUST | operations | include validation monitoring rollback limitations and support notes
PRS.004 | MUST | privacy | filter secrets customer data vulnerabilities and unnecessary internal detail
PRS.005 | MUST | human | preserve product support operations publication and release authority
PRS.006 | SHOULD | reuse | link to PR Ready and readiness evidence instead of duplicating histories
PRS.007 | SHOULD | token | optimize quality-adjusted token ROI after communication fidelity passes
PRS.008 | SHOULD | prompt | keep rules and output contract in a stable prefix
PRS.009 | NEVER | claim | infer deployment adoption or outcome from merge alone
PRS.010 | NEVER | publish | send announce publish deploy or release without explicit authority

## Verification

- Change, impact, validation, limitations, rollout, rollback, support, and owners are present.
- Lifecycle states are correctly distinguished.
- Sensitive exclusions and audience boundary are explicit.
- The summary remains a draft until accountable confirmation.

## Failure Modes

- treating merge as completed delivery;
- copying commit messages into release notes without translation;
- omitting known limitations or rollback;
- exposing confidential implementation or customer details;
- publishing draft language without owner confirmation.
