---
name: reusable-delivery-pattern
description: Use to extract a reusable, evidence-bounded delivery pattern from multiple Feature Delivery Cases, including the conditions, checklist, failure signals, transferable elements, non-transferable elements, examples, counterexamples, owners, and review triggers. Input is a bounded case set, decisions, implementations, tests, incidents, outcomes, environments, and human annotations; output is a versioned pattern candidate and applicability matrix. Do not use to copy one solution broadly, erase local constraints, or auto-promote memory, rule, Skill, or automation; preserve behavior, validation boundaries, uncertainty, provenance, and human authority.
---

# Reusable Delivery Pattern

## Goal

Turn repeated delivery experience into a reusable pattern without stripping away the conditions that made it work.

## Use When

Use when several delivery cases share a solution shape, checklist, failure signal, or coordination pattern that may reduce future effort under comparable conditions.

## Do Not Use When

Do not use for one-off implementation notes, generic best-practice summaries, unsupported template creation, or direct promotion into policy, Skill, automation, or memory.

## Inputs

Require multiple bounded Feature Delivery Cases or an explicit exception approved by the owner, including goals, constraints, decisions, implementation evidence, tests, outcomes, failures, environments, affected modules, and human annotations.

## Outputs

Write by default to:

```text
artifacts/delivery-patterns/<pattern-id>/<run-id>/pattern-candidate.v1.json
artifacts/delivery-patterns/<pattern-id>/<run-id>/pattern.md
artifacts/capability-runs/reusable-delivery-pattern/<run-id>/run-result.json
```

When write permission is unavailable, return the complete artifact inline with `write_status=returned_inline`.

Include:

- pattern intent and user-visible problem addressed;
- required preconditions and environmental assumptions;
- reusable sequence, checklist, and validation points;
- expected benefits and known costs;
- leading failure signals and stop conditions;
- transferable components and why they transfer;
- non-transferable components and why they do not;
- examples, counterexamples, and contradictory evidence;
- owner, candidate status, review date, expiry, and promotion path.

## Evidence

Separate fact from inference. Record uncertainty, unknown applicability, assumptions, conflicts, source dates, case diversity, and outcome quality. Similar implementation shape alone does not establish a reusable pattern. Distinguish correlation from demonstrated causal contribution.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- applicability conditions are precise enough to reject unsuitable cases;
- transferable and non-transferable parts are explicit;
- examples and counterexamples are linked to source cases;
- the checklist contains verification and failure signals, not only steps;
- promotion remains a separate accountable decision;
- future users can tell what must be adapted locally.

## Stop Conditions

Stop when the requested pattern candidate or next reviewable stage is complete. Stop for missing permission, insufficient case diversity, weak outcome evidence, unresolved contradictions, safety or compliance boundaries, absent owner, or a promotion decision. State the exact evidence gap and smallest next step.

## Workflow

1. Bound the source cases, target problem, environments, and promotion authority.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Normalize case conditions, actions, outcomes, failures, and constraints.
4. Identify common mechanisms while preserving material differences.
5. Separate transferable structure from local implementation and organizational context.
6. Produce the candidate, applicability matrix, and review conditions.
7. Stop before promotion into approved memory, rule, Skill, or automation.

## Rules

RDP.001 | MUST | cases | link every pattern claim to source cases
RDP.002 | MUST | applicability | state required conditions and explicit exclusions
RDP.003 | MUST | transfer | separate transferable from non-transferable elements
RDP.004 | MUST | validation | include checks failure signals and stop conditions
RDP.005 | MUST | lifecycle | set owner candidate status review and expiry
RDP.006 | SHOULD | diversity | require more than one materially distinct case when possible
RDP.007 | SHOULD | token | optimize quality-adjusted token ROI after fidelity passes
RDP.008 | SHOULD | prompt | keep rules and output contract in a stable prefix
RDP.009 | NEVER | generalize | universalize one successful case
RDP.010 | NEVER | promotion | auto-promote the candidate into memory rule Skill or automation

## Verification

- The artifact includes conditions, checklist, failure signals, transfer boundaries, and evidence.
- Counterexamples and uncertainty are visible.
- Candidate and approved statuses are distinct.
- No local implementation detail is presented as universally required without evidence.

## Failure Modes

- extracting a template from only superficial similarity;
- dropping environmental or organizational constraints;
- presenting correlation as causal proof;
- omitting counterexamples;
- promoting a pattern because it sounds plausible.
