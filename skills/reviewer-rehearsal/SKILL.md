---
name: reviewer-rehearsal
description: Use to rehearse the material challenges a reviewer is likely to raise about a bounded design or change using architecture intent, domain rules, historical incidents, review evidence, tests, and risk. Input is a proposed change or diff, Ticket Ready Package, implementation plan, decisions, system context, test evidence, and owner boundaries; output is an evidence-linked challenge set, missing evidence, recommended tests or explanations, and unresolved human decisions. Do not use as lint duplication, secret personnel evaluation, merge approval, or fabricated reviewer opinion; preserve behavior, validation boundaries, uncertainty, privacy, and human authority.
---

# Reviewer Rehearsal

## Goal

Prepare a change for high-value review by surfacing the design, risk, contract, and validation questions that matter before review begins.

## Use When

Use before requesting review for a complex, cross-module, user-sensitive, contract-changing, or high-risk change.

## Do Not Use When

Do not use to simulate a named person's private preferences, evaluate author performance, repeat automated lint findings, or claim that review has occurred.

## Inputs

Require a bounded change or diff, Feature Delivery Case, ticket and acceptance, implementation plan, architecture and domain context, decisions and assumptions, existing test evidence, historical incidents or review findings, risks, owners, and permission boundary.

## Outputs

Write by default to:

```text
artifacts/reviewer-rehearsal/<case-id>/<run-id>/rehearsal.v1.json
artifacts/reviewer-rehearsal/<case-id>/<run-id>/review-prep.md
artifacts/capability-runs/reviewer-rehearsal/<run-id>/run-result.json
```

When write permission is unavailable, return the complete artifact inline with `write_status=returned_inline`.

Include:

- material reviewer challenge and why it matters;
- evidence already available;
- missing evidence, test, explanation, migration note, or rollback detail;
- affected contract, boundary, user behavior, or operational control;
- recommended author action and validation;
- question requiring architecture, product, security, domain, or release judgment;
- non-material automated findings intentionally excluded;
- readiness for actual review, without approval.

## Evidence

Separate facts from inference. Record citations, uncertainty, unknowns, assumptions, conflicting evidence, source dates, and scope. Historical review patterns are context, not proof that a current reviewer will object.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- material design and delivery questions are surfaced before review;
- missing evidence is linked to a concrete author action;
- automated style or lint noise is excluded;
- unresolved authority decisions are routed to the correct role;
- the author can improve the PR package without rewriting the implementation blindly;
- no personnel judgment or false approval is produced.

## Stop Conditions

Stop when the requested rehearsal or next reviewable stage is complete. Stop for missing permission, insufficient evidence, privacy or security risk, absent design intent, unresolved scope, conflicting sources, or a required human decision. State the gap and smallest next step.

## Workflow

1. Bound the change, review objective, stage, evidence window, and privacy boundary.
2. Query ConPort first when available; otherwise use targeted authorized sources.
3. Exclude issues already enforced by deterministic tooling unless they reveal a larger delivery risk.
4. Compare the change with acceptance, architecture intent, contracts, incidents, and validation evidence.
5. Rank only material challenges by affected outcome and evidence gap.
6. Produce author actions and human decision requests.
7. Stop before approval or reviewer impersonation.

## Rules

RRH.001 | MUST | materiality | focus on design contract risk validation and user-impact challenges
RRH.002 | MUST | evidence | link each challenge to current change evidence and governing context
RRH.003 | MUST | action | state the smallest evidence test or explanation needed
RRH.004 | MUST | privacy | use role patterns not private judgments about named reviewers
RRH.005 | MUST | human | preserve reviewer merge architecture and product authority
RRH.006 | SHOULD | noise | exclude deterministic lint findings unless materially connected
RRH.007 | SHOULD | token | optimize quality-adjusted token ROI after challenge fidelity passes
RRH.008 | SHOULD | prompt | keep rules and output contract in a stable prefix
RRH.009 | NEVER | performance | score authors reviewers or teams
RRH.010 | NEVER | approval | claim review approval or merge readiness without actual evidence

## Verification

- Every challenge has evidence, impact, requested action, and authority boundary.
- Lint duplication and speculative reviewer psychology are absent.
- Missing tests or explanations map to a real delivery concern.
- The result is editable and clearly labeled as rehearsal.

## Failure Modes

- producing generic code-review advice;
- inventing what a named reviewer thinks;
- flooding the author with low-value style comments;
- treating historical incidents as certain recurrence;
- presenting rehearsal completion as review approval.
