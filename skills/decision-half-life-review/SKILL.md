---
name: decision-half-life-review
description: Use to determine whether an existing decision should continue, be revalidated, or be reopened after evidence, constraints, ownership, dependencies, or business conditions change. Input is a bounded decision record, original rationale, alternatives, owner, effective scope, review date, assumptions, and current change evidence; output is a review packet with decision status, changed evidence, continue-or-reopen recommendation, owner, deadline, and required validation. Do not use to silently overturn a decision or treat age alone as invalidation; preserve behavior, provenance, uncertainty, and accountable human authority.
---

# Decision Half-Life Review

## Goal

Prevent past decisions from becoming permanent truth after the conditions that justified them have changed.

## Use When

Use at scheduled review points, before major change, after incidents, when dependencies or constraints shift, or when a decision is repeatedly questioned without a current evidence baseline.

## Do Not Use When

Do not use to rewrite decision history, reopen decisions without material change evidence, or replace the accountable owner’s authority.

## Inputs

Require the decision, original rationale, alternatives, effective date, scope, owner, assumptions, review or expiry conditions, current evidence, and known consequences of changing or retaining it.

## Outputs

Produce:

```text
artifacts/decision-review/<decision-id>/<run-id>/decision-review.v1.json
artifacts/decision-review/<decision-id>/<run-id>/review.md
artifacts/capability-runs/decision-half-life-review/<run-id>/run-result.json
```

Return:

- current status: `continue`, `continue_with_conditions`, `revalidate`, `reopen`, `superseded`, or `insufficient_evidence`;
- original rationale and scope;
- changed and unchanged evidence;
- assumptions still valid, at risk, or expired;
- consequences of continuing versus reopening;
- recommendation and confidence;
- accountable owner, decision deadline, and next review point;
- required validation and records to update after adjudication.

## Evidence

Age is a trigger for review, not proof of invalidity. Separate changed facts from interpretation. Preserve original rationale and alternatives so the review does not judge the past using only current knowledge.

## Success Signals

Evaluate as `met`, `not_met`, or `not_evaluated`:

- original conditions and current conditions are compared;
- changed evidence is material to the decision;
- continue and reopen consequences are explicit;
- recommendation preserves uncertainty and authority;
- owner, deadline, validation, and next review point are present;
- decision history remains intact.

## Stop Conditions

Stop at a review packet. Do not overturn or continue the decision on behalf of the owner. Stop when the original record, current evidence, owner, or scope is missing; when authority conflicts require adjudication; or when one bounded retry fails.

## Workflow

1. Bound the decision, scope, authority, and original evidence.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted sources.
3. Reconstruct the original rationale without rewriting history.
4. Compare current constraints, assumptions, dependencies, and outcomes.
5. Identify material change evidence and unchanged evidence.
6. Recommend continue, revalidate, reopen, or supersede.
7. Define owner action, deadline, validation, and next review point.
8. Stop for adjudication.

## Rules

DHR.001 | MUST | history | preserve the original rationale alternatives and context
DHR.002 | MUST | change | link review recommendations to material change evidence
DHR.003 | MUST | comparison | state consequences of continuing and reopening
DHR.004 | MUST | ownership | identify decision owner deadline and next review point
DHR.005 | MUST | validation | define evidence required to confirm the next status
DHR.006 | SHOULD | token | optimize quality-adjusted token ROI after review completeness passes
DHR.007 | SHOULD | prompt | keep review rules stable and current evidence dynamic
DHR.008 | NEVER | age | invalidate a decision solely because it is old
DHR.009 | NEVER | history | rewrite the original decision using hindsight
DHR.010 | NEVER | authority | silently overturn continue or supersede the decision

## Verification

- Original and current conditions are both represented.
- Material changes support the recommendation.
- Owner, deadline, validation, and next review point are complete.

## Failure Modes

- treating age as expiry;
- losing the original rationale;
- reopening from preference rather than evidence;
- recommending continuation without checking assumptions;
- omitting records that must change after adjudication.
