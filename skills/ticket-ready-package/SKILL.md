---
name: ticket-ready-package
description: Use to turn a bounded requirement and supporting delivery context into an editable Ticket Ready Package with goals, non-goals, acceptance criteria, affected modules, risks, test needs, open questions, evidence, owners, and suggested splits. Input is a requirement or Feature Delivery Case, domain context, system evidence, decisions, dependencies, historical cases, deadlines, and authority boundaries; output is a reviewable readiness artifact and explicit gaps. Do not use to invent requirements, commit scope or dates, approve readiness, or replace feature-spec-author and accountable product or engineering owners; preserve behavior, validation boundaries, facts, uncertainty, and human authority.
---

# Ticket Ready Package

## Goal

Convert a requirement from understood-in-conversation into a visible package that developers can start from and reviewers can challenge.

## Use When

Use when a new requirement enters development, a ticket remains unable to start, several interpretations exist, or the team needs one evidence-linked scope and validation view.

## Do Not Use When

Do not use to create business intent without an authorized source, convert unresolved disagreements into commitments, assign dates without authority, or declare a ticket ready on generated text alone.

## Inputs

Require a bounded requirement or Feature Delivery Case, target user outcome, current stage and next gate, authoritative requirement sources, domain and system context, known decisions and assumptions, dependencies, risks, owners, deadlines, and permission boundary.

Optional inputs include similar delivery cases, negative knowledge, alignment receipts, unasked-question reports, architecture maps, support constraints, and release policies.

## Outputs

Write by default to:

```text
artifacts/ticket-ready/<case-id>/<run-id>/ticket-ready.v1.json
artifacts/ticket-ready/<case-id>/<run-id>/ticket-ready.md
artifacts/capability-runs/ticket-ready-package/<run-id>/run-result.json
```

When write permission is unavailable, return the complete artifact inline with `write_status=returned_inline`.

Include:

- user outcome, goals, and explicitly excluded non-goals;
- acceptance criteria linked to source evidence;
- affected modules, interfaces, data, users, and operational surfaces;
- dependencies, assumptions, risks, constraints, and unknowns;
- test and validation checklist, including human validation;
- unresolved questions with owner and latest-safe answer time;
- suggested ticket split with rationale and dependency order;
- readiness gaps and required confirmations;
- links back to the Feature Delivery Case and source artifacts.

## Evidence

Separate source-supported facts from inference. Record citations, uncertainty, unknowns, assumptions, conflicts, source dates, and scope. A requirement statement without an accountable source remains unconfirmed. A generated acceptance criterion must be labeled proposed until confirmed.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- a developer can identify the intended outcome, scope, validation path, and remaining blockers;
- acceptance criteria are testable or explicitly marked as requiring human validation;
- reviewers can distinguish confirmed scope from proposed interpretation;
- affected modules, dependencies, risks, and unknowns are visible;
- accountable owners can edit and confirm the package;
- the package does not create an unauthorized delivery commitment.

## Stop Conditions

Stop when the requested Ticket Ready Package or next reviewable stage is complete. Stop for missing permission, insufficient evidence, unresolved requirement authority, security or privacy boundaries, material contradictions, absent accountable owners, or a product or engineering decision. State the exact gap, who can resolve it, and the smallest next step.

## Workflow

1. Bound the Feature Delivery Case, stage, next gate, sources, and authority.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Reuse an approved feature specification when present; do not duplicate or silently replace it.
4. Separate confirmed intent, proposed interpretation, non-goals, and unresolved questions.
5. Map acceptance, affected surfaces, dependencies, risks, and validation needs.
6. Suggest splits only when each slice preserves user-visible value or reduces a named delivery risk.
7. Produce the editable package and stop for product and engineering confirmation.

## Collaboration Boundaries

- `feature-spec-author` authors an approved feature specification; this Skill projects confirmed and proposed information into a ticket-readiness view.
- `domain-context-pack` supplies task-specific internal rules and constraints.
- `unasked-questions-generator` discovers consequential missing questions.
- `decision-alignment-receipt` records confirmed decisions and non-decisions.
- `implementation-plan` consumes a confirmed Ticket Ready Package.
- `feature-delivery-case` remains the canonical lifecycle record.

## Rules

TRP.001 | MUST | scope | separate goals non-goals and proposed interpretations
TRP.002 | MUST | acceptance | link each acceptance criterion to evidence or mark it proposed
TRP.003 | MUST | impact | identify affected modules interfaces data users and operations
TRP.004 | MUST | gaps | name missing evidence decisions owners and latest-safe times
TRP.005 | MUST | human | preserve product and engineering scope and date authority
TRP.006 | SHOULD | split | recommend only value-preserving or risk-reducing ticket splits
TRP.007 | SHOULD | token | optimize quality-adjusted token ROI after artifact fidelity passes
TRP.008 | SHOULD | prompt | keep rules and output contract in a stable prefix
TRP.009 | NEVER | evidence | fabricate requirements tests readiness or confirmations
TRP.010 | NEVER | authority | commit scope priority date or readiness

## Verification

- Goals, non-goals, acceptance, impact, risks, tests, questions, and splits are explicit.
- Confirmed facts and proposed content are visually distinguishable.
- Every blocking gap has an owner or an explicit owner-needed state.
- The package references rather than replaces the canonical Feature Delivery Case.

## Failure Modes

- rewriting a vague ticket into confident but unsupported detail;
- presenting a feature specification and Ticket Ready Package as competing truths;
- treating a checklist as proof of readiness;
- splitting work by file count rather than user value and dependency boundaries;
- hiding unresolved questions to make the ticket appear ready.
