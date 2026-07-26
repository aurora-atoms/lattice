---
name: assumption-expiry-radar
description: Use to identify assumptions that may have silently expired because code, dependencies, business rules, traffic, ownership, policy, or operating conditions changed. Input is a bounded assumption set, source evidence, affected systems, validation history, owners, dates, and change signals; output is an evidence-linked expiry review containing trigger evidence, affected areas, current status, validation recommendation, owner, deadline, and reopen conditions. Do not use to declare assumptions false without evidence or automatically block delivery; preserve behavior, uncertainty, scope, and human risk authority.
---

# Assumption Expiry Radar

## Goal

Expose when a previously reasonable assumption may no longer be safe before the resulting failure is misdiagnosed as sudden code breakage.

## Use When

Use before implementation, merge, release, migration, architecture review, or incident follow-up when delivery depends on assumptions about dependencies, scale, data, policy, ownership, user behavior, or operating environment.

## Do Not Use When

Do not use to invent assumptions not grounded in artifacts, to mark every old assumption invalid, or to replace the accountable owner’s decision to validate, accept, defer, or retire it.

## Inputs

Require bounded assumptions, original rationale, source and date, applicability scope, affected behavior, owner or accountable role, last validation, and available change evidence.

## Outputs

Produce:

```text
artifacts/assumption-expiry/<scope-id>/<run-id>/assumption-expiry.v1.json
artifacts/assumption-expiry/<scope-id>/<run-id>/review.md
artifacts/capability-runs/assumption-expiry-radar/<run-id>/run-result.json
```

Each record contains:

- assumption statement and original scope;
- original evidence and last validation time;
- expiry trigger or change signal;
- affected code, systems, users, data, controls, or decisions;
- status: `current`, `at_risk`, `expired`, `superseded`, `unknown`, or `accepted_without_revalidation`;
- consequence if false;
- recommended validation method and evidence threshold;
- accountable owner and latest safe validation time;
- accepted-risk scope, expiry, monitoring, and reopen trigger when validation is deferred.

## Evidence

Separate observed change evidence from inference that the assumption may have expired. Age alone is not proof. A recently edited document is not proof of current validity. Preserve uncertainty and disconfirming evidence.

## Success Signals

Evaluate as `met`, `not_met`, or `not_evaluated`:

- assumptions are explicit and scoped;
- each risk status has trigger evidence;
- affected areas and consequences are named;
- validation is concrete and proportional;
- owner and latest safe review time are explicit;
- deferred validation includes monitoring and reopen conditions;
- the output does not automatically block delivery.

## Stop Conditions

Stop at a reviewable expiry report. Stop when original assumption evidence, scope, owner, or relevant change signals are unavailable; when risk acceptance requires human authority; or when validation fails after one retry.

## Workflow

1. Bound assumptions, scope, original evidence, and next gate.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted sources.
3. Identify changes in code, dependencies, policy, business rules, volume, environment, or ownership.
4. Link change signals to assumptions and affected behavior.
5. Classify status without treating age as failure.
6. Define validation, owner, deadline, monitoring, and reopen triggers.
7. Stop for owner review.

## Rules

AER.001 | MUST | scope | bind every assumption to source date and applicability
AER.002 | MUST | trigger | attach concrete change evidence to expiry risk
AER.003 | MUST | impact | identify affected behavior and consequence if false
AER.004 | MUST | validation | recommend a specific validation method and threshold
AER.005 | MUST | ownership | record owner and latest safe confirmation time
AER.006 | MUST | deferral | require monitoring expiry and reopen trigger for accepted uncertainty
AER.007 | SHOULD | token | optimize quality-adjusted token ROI after risk coverage passes
AER.008 | SHOULD | prompt | keep classification rules stable and change evidence dynamic
AER.009 | NEVER | age | declare an assumption expired solely because it is old
AER.010 | NEVER | authority | automatically block delivery or accept risk

## Verification

- Every at-risk or expired assumption has trigger evidence.
- Every deferred validation has human acceptance, monitoring, and reopening conditions.
- Owners, deadlines, impacts, and validation methods are complete.

## Failure Modes

- treating assumption age as invalidity;
- failing to preserve original scope;
- vague advice to “recheck later”;
- marking assumptions false without validation;
- accepting uncertainty without monitoring or expiry.
