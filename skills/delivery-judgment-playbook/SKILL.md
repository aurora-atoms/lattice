---
name: delivery-judgment-playbook
description: Use to turn repeated, evidence-backed delivery decisions into a scoped playbook that states when a judgment applies, which evidence is required, which steps cannot be skipped, who decides, and when the guidance must be reviewed. Input is a bounded set of Feature Delivery Cases, decisions, outcomes, incidents, controls, exceptions, and owner annotations; output is a versioned playbook candidate with triggers, criteria, mandatory steps, failure signals, exceptions, owners, and expiry. Do not use to universalize one case, replace accountable judgment, or auto-promote policy; preserve behavior, validation boundaries, uncertainty, and human authority.
---

# Delivery Judgment Playbook

## Goal

Capture repeatable judgment without pretending that every future case is identical.

## Use When

Use when multiple delivery cases show a recurring decision, teams repeatedly ask when a review or safeguard is required, or a known step must not be skipped under named conditions.

## Do Not Use When

Do not use for one-off advice, unsupported best practices, universal rules from a single case, personnel evaluation, or final policy approval.

## Inputs

Require bounded Feature Delivery Case references, decision and outcome evidence, incident or defect evidence when applicable, current controls, known exceptions, accountable roles, applicability scope, and review authority.

## Outputs

Write by default to:

```text
artifacts/delivery-playbooks/<playbook-id>/<run-id>/playbook-candidate.v1.json
artifacts/delivery-playbooks/<playbook-id>/<run-id>/playbook.md
artifacts/capability-runs/delivery-judgment-playbook/<run-id>/run-result.json
```

When write permission is unavailable, return the complete artifact inline with `write_status=returned_inline`.

Include:

- decision or judgment to be made;
- applicability conditions and explicit non-applicability conditions;
- required evidence and minimum confidence;
- decision criteria and accountable role;
- mandatory steps that cannot be skipped, with rationale;
- optional steps and allowed tailoring;
- exception and override path;
- failure signals and escalation triggers;
- source cases and contradictory cases;
- owner, version, review date, expiry, and promotion status.

## Evidence

Separate facts from inference. Record uncertainty, unknowns, assumptions, conflicts, source dates, case scope, and outcome quality. A repeated practice is not evidence of effectiveness by itself. A single successful case cannot establish a general rule.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- the playbook states when it applies and when it does not;
- mandatory steps are justified by evidence or explicit governance authority;
- exceptions and human override remain possible;
- source cases and contrary evidence are visible;
- future users can identify the required owner and review trigger;
- candidate status is distinct from approved policy or Skill status.

## Stop Conditions

Stop when the requested playbook candidate or next reviewable stage is complete. Stop for missing permission, insufficient or contradictory evidence, undefined decision authority, safety or compliance boundaries, unresolved scope, or a required governance decision. State the missing evidence or authority and the smallest next step.

## Workflow

1. Bound the judgment, source cases, target scope, and authority.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Compare cases for common conditions, decisions, outcomes, and exceptions.
4. Distinguish mandatory controls from optional tactics and historical habit.
5. Write triggers, criteria, non-skippable steps, failure signals, and override paths.
6. Mark the result as a candidate and stop for owner or governance review.

## Rules

DJP.001 | MUST | scope | state applicability and non-applicability conditions
DJP.002 | MUST | evidence | link every mandatory step to evidence or explicit authority
DJP.003 | MUST | decision | identify the accountable role and required evidence
DJP.004 | MUST | exception | provide an exception override and review path
DJP.005 | MUST | lifecycle | version the playbook and define review or expiry triggers
DJP.006 | SHOULD | reuse | prefer the smallest reusable judgment unit
DJP.007 | SHOULD | token | optimize quality-adjusted token ROI after evidence fidelity passes
DJP.008 | SHOULD | prompt | keep rules and output contract in a stable prefix
DJP.009 | NEVER | promotion | auto-promote a candidate into policy rule Skill or automation
DJP.010 | NEVER | authority | replace accountable human judgment

## Verification

- Trigger, scope, criteria, mandatory steps, exceptions, and owners are explicit.
- Source cases and contrary evidence are linked.
- Promotion status is `candidate`, `approved`, `rejected`, `superseded`, or `expired`.
- The artifact does not claim policy authority it does not have.

## Failure Modes

- converting one lesson into a universal rule;
- preserving ritual without evidence;
- omitting non-applicability conditions;
- making every step mandatory;
- hiding exceptions or review triggers.
