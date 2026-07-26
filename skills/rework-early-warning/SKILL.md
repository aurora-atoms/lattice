---
name: rework-early-warning
description: Use to detect when a bounded delivery is entering a high-rework zone because requirements, acceptance criteria, decisions, assumptions, dependencies, or implementation keep changing without convergence. Input is a Delivery Case, requirement and decision history, PR and test changes, unresolved questions, owners, deadlines, and evidence; output is an evidence-linked warning with rework drivers, convergence gaps, the single highest-leverage clarification, and options to pause, narrow, sequence, or continue with accepted risk. Do not use to treat change itself as failure, score people, or automatically halt delivery; preserve behavior, validation boundaries, uncertainty, and human authority.
---

# Rework Early Warning

## Goal

Expose the smallest unresolved cause likely to invalidate completed work before more implementation accumulates around it.

## Use When

Use when the same area changes repeatedly, acceptance criteria move, decisions reopen without new evidence, dependencies remain unstable, or implementation and tests churn around an unresolved boundary.

## Do Not Use When

Do not use to penalize exploration, label teams as inefficient, infer intent from commit counts, or stop work without an accountable decision.

## Inputs

Require a bounded case, stage and next gate, requirement versions, decision and assumption history, PR and test changes, unresolved questions, dependencies, owners, deadlines, and authorized evidence.

## Outputs

Write by default to:

```text
artifacts/rework-warning/<case-id>/<run-id>/rework-warning.v1.json
artifacts/rework-warning/<case-id>/<run-id>/review.md
artifacts/capability-runs/rework-early-warning/<run-id>/run-result.json
```

When write permission is unavailable, return the complete artifact inline with `write_status=returned_inline`.

Include rework drivers, supporting evidence, affected work, convergence status, the single highest-leverage clarification or decision, options to pause, narrow, sequence, or continue, owner, latest-safe time, and validation of the intervention.

## Evidence

Separate facts from inference. Record uncertainty, unknown causes, assumptions, conflicting evidence, source dates, and scope. Change volume alone does not prove waste or rework risk.

## Success Signals

Evaluate as `met`, `not_met`, or `not_evaluated`:

- the warning is tied to a bounded repeated-change pattern;
- the underlying convergence gap is explicit;
- one highest-leverage clarification or decision is identified;
- intervention options and consequences are reviewable;
- the team can consciously continue with accepted risk;
- no personnel judgment is produced.

## Stop Conditions

Stop when the warning or next reviewable stage is complete. Stop for missing permission, insufficient evidence, unavailable owners, privacy, security, compliance, safety, production-risk, or human-decision boundaries, or when scope must expand. State the smallest next step.

## Workflow

1. Bound the case, stage, gate, evidence window, and authority.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Compare requirement, decision, implementation, and test changes over time.
4. Distinguish healthy learning from unresolved convergence failure.
5. Identify the highest-leverage clarification and bounded intervention options.
6. Stop for owner review.

## Rules

REW.001 | MUST | evidence | link warnings to repeated bounded change and affected work
REW.002 | MUST | cause | distinguish symptoms from the unresolved convergence gap
REW.003 | MUST | leverage | identify one highest-leverage clarification or decision
REW.004 | MUST | options | provide pause narrow sequence and continue options where applicable
REW.005 | MUST | authority | preserve team authority to accept risk and continue
REW.006 | SHOULD | token | optimize quality-adjusted token ROI after warning fidelity passes
REW.007 | SHOULD | prompt | keep detection rules stable and case evidence dynamic
REW.008 | NEVER | metric | infer rework from commit count or discussion volume alone
REW.009 | NEVER | blame | use the warning for personnel scoring or attribution
REW.010 | NEVER | halt | automatically stop delivery without accountable authority

## Verification

- Drivers, evidence, affected work, owner, timing, and intervention are present.
- Healthy discovery is separated from uncontrolled churn.
- The recommendation is smaller than a broad replanning exercise.

## Failure Modes

- calling all requirement change rework;
- listing symptoms without the unresolved decision;
- recommending a project-wide pause;
- using activity counts as proof;
- hiding accepted-risk continuation as an option.
