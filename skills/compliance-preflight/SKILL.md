---
name: compliance-preflight
description: Use to identify likely security, privacy, legal, regulatory, audit, data-governance, regional, payment, access-control, or customer-commitment review points while a design is still cheap to change. Input is a bounded requirement or design, data flows, permissions, regions, policies, prior review findings, affected users, owners, deadlines, and available evidence; output is an evidence-linked preflight packet with potential review points, required evidence, optional design adjustments, responsible reviewers, timing, and unresolved questions. Do not use to issue final legal or compliance rulings, invent policy, or automatically block delivery; preserve behavior, validation boundaries, uncertainty, and human authority.
---

# Compliance Preflight

## Goal

Expose likely review and evidence needs early enough to avoid last-minute rejection while minimizing unnecessary approval work.

## Use When

Use when a bounded change affects data, identity, permissions, regions, payment, retention, auditability, regulated workflows, customer commitments, or security-sensitive behavior.

## Do Not Use When

Do not use as legal advice, final compliance approval, a substitute for policy owners, or a reason to involve every control function without evidence.

## Inputs

Require the bounded change, stage and next gate, data and control flows, permissions, affected regions and users, policies and historical review findings, current design, owners, deadlines, and evidence access boundary.

## Outputs

Write by default to:

```text
artifacts/compliance-preflight/<case-id>/<run-id>/preflight.v1.json
artifacts/compliance-preflight/<case-id>/<run-id>/review.md
artifacts/capability-runs/compliance-preflight/<run-id>/run-result.json
```

When write permission is unavailable, return the complete artifact inline with `write_status=returned_inline`.

Include:

- potential review point and triggering feature;
- applicable policy or historical evidence;
- required evidence and evidence owner;
- earliest useful consultation and latest-safe decision time;
- optional design adjustment and tradeoff;
- responsible review role and authority boundary;
- unresolved interpretation, uncertainty, and escalation condition;
- final approval status as `not_requested`, `pending_human_review`, or `outside_skill_authority`.

## Evidence

Separate facts from inference. Record uncertainty, unknown policy applicability, assumptions, conflicting guidance, source date, version, jurisdiction, and scope. Historical review outcomes are precedents, not automatic rulings.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- likely review points are linked to concrete design or data-flow evidence;
- required evidence can be prepared before the formal review;
- optional design adjustments are specific and reversible where possible;
- only necessary accountable roles are engaged;
- unresolved interpretation is escalated explicitly;
- no final legal, compliance, security, or privacy ruling is fabricated.

## Stop Conditions

Stop when the requested preflight packet or next reviewable stage is complete. Stop for missing permission, insufficient evidence, unavailable policy sources, unresolved security, privacy, legal, compliance, data-governance, safety, or production-risk boundaries, or a required human ruling. State what is missing, who can decide, and the smallest next step.

## Workflow

1. Bound the change, stage, gate, jurisdictions, data classes, and authority.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Trace data, identity, permission, regional, audit, and customer-commitment effects.
4. Match only evidence-supported policy and historical review signals.
5. Define required evidence, optional design adjustments, reviewer, and timing.
6. Produce the packet and stop for accountable review.

## Rules

CPF.001 | MUST | trigger | link each review point to a concrete feature flow or obligation
CPF.002 | MUST | evidence | cite policy history and design evidence with date and scope
CPF.003 | MUST | timing | state earliest useful consultation and latest-safe decision time
CPF.004 | MUST | options | provide design adjustments without treating them as approved
CPF.005 | MUST | authority | reserve final legal compliance security and privacy judgment for accountable roles
CPF.006 | SHOULD | minimality | involve only roles needed for the evidenced review points
CPF.007 | SHOULD | token | optimize quality-adjusted token ROI after preflight fidelity passes
CPF.008 | SHOULD | prompt | keep review rules stable and design evidence dynamic
CPF.009 | NEVER | ruling | present model output as final legal or compliance approval
CPF.010 | NEVER | expansion | turn a bounded preflight into a broad policy audit without authorization

## Verification

- Every review point has trigger, evidence, owner, timing, and authority boundary.
- Required evidence and optional design adjustments are explicit.
- Unknown applicability remains visible.
- Final approval is not implied.

## Failure Modes

- copying a generic compliance checklist;
- treating historical precedent as binding policy;
- involving every control function by default;
- giving final approval language;
- identifying a concern without the evidence needed to resolve it.
