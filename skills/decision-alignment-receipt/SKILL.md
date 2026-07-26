---
name: decision-alignment-receipt
description: Use to create a durable alignment receipt after a requirement, design, architecture, operational, or governance discussion. Input is the bounded decision topic, participants or accountable roles, evidence sources, options considered, decided and undecided items, assumptions, scope, dates, and next review point; output is an evidence-linked receipt that distinguishes decisions, non-decisions, assumptions, owners, rationale, applicability, and confirmation triggers. Do not use to invent consensus, silently approve unresolved matters, or replace formal authority; preserve behavior, provenance, uncertainty, privacy, and human decision control.
---

# Decision Alignment Receipt

## Goal

Create a shared, reviewable baseline for what the team decided, did not decide, assumed, assigned, and must confirm later.

The receipt exists to prevent later disagreement from being reconstructed from memory, chat fragments, or conflicting local interpretations.

## Use When

Use after a requirement review, design discussion, architecture decision, incident decision, cross-team agreement, risk acceptance, or release-readiness meeting where later execution depends on a common interpretation.

Use directly when the discussion boundary and accountable roles are known. Use `knowledge-integrity` when the category must first select among several integrity capabilities.

## Do Not Use When

Do not use to:

- infer agreement from silence or attendance;
- convert a proposal into an approved decision;
- replace an ADR, policy approval, compliance sign-off, or other required system of record;
- publish sensitive participant details beyond the authorized disclosure boundary;
- merge unrelated decisions into one ambiguous receipt.

## Inputs

Require:

- one bounded decision topic and business or delivery consequence;
- evidence sources and observation dates;
- decision authority and accountable roles;
- options considered and material tradeoffs;
- explicit decisions and explicit non-decisions;
- assumptions, dependencies, exceptions, and unresolved questions;
- scope, non-scope, effective date, and next confirmation point.

## Outputs

Default writeback paths:

```text
artifacts/decision-alignment/<decision-id>/<run-id>/alignment-receipt.v1.json
artifacts/decision-alignment/<decision-id>/<run-id>/receipt.md
artifacts/capability-runs/decision-alignment-receipt/<run-id>/run-result.json
```

When write permission is unavailable, return the complete receipt inline with `write_status=returned_inline`.

A complete receipt includes:

- decision topic and intended outcome;
- status for each item: `decided`, `not_decided`, `assumed`, `deferred`, or `superseded`;
- approved option and rationale where applicable;
- rejected or deferred options and why;
- owner or accountable role for each unresolved item;
- applicability scope and explicit exclusions;
- evidence references and confirmation source;
- effective date, review date, expiry trigger, and next confirmation point;
- consequences for implementation, validation, rollout, and support;
- known conflicts, uncertainty, and dissent that remain material.

## Evidence

Separate source-supported facts, participant-confirmed decisions, inference, assumptions, unresolved questions and unknowns, uncertainty, and conflicts. Preserve source, observation date, authority, applicability scope, and confirmation status. A receipt may state `not_confirmed` when participant or authority confirmation is unavailable. Do not promote meeting notes, model summaries, or repeated statements into confirmed decisions without evidence of authority.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- decided and undecided items are visibly separated;
- every assumption has an owner or validation path;
- every unresolved item has a next confirmation point;
- rationale and alternatives are preserved without rewriting history;
- scope and applicability are explicit;
- an authorized reviewer can confirm or correct the receipt quickly;
- future disputes can refer to one bounded baseline without treating it as permanent truth.

## Stop Conditions

Stop when the requested receipt or confirmation stage is complete. Stop earlier when required permission, authority, evidence, scope, participant confirmation, privacy permission, or the next review point is missing; when conflicting evidence requires adjudication; when a security, privacy, compliance, safety, or other high-risk boundary is reached; or when validation fails after one bounded corrective retry. Do not publish, approve, execute, or continue beyond the target stage without explicit authorization.

State the missing item, accountable role, reason, and smallest resumable next step.

## Workflow

1. Bound the decision topic, scope, authority, and evidence cutoff.
2. Query ConPort before loading or searching full Skill text when ConPort is available; otherwise use targeted authorized sources.
3. Extract proposed, decided, rejected, deferred, and unresolved items.
4. Separate participant-confirmed decisions from notes and inference.
5. Capture assumptions, owners, effective dates, review points, and expiry triggers.
6. Preserve material dissent, exceptions, and conflicts.
7. Produce the receipt and request bounded confirmation from the accountable role.
8. Stop at the requested review stage.

## Rules

DAR.001 | MUST | status | distinguish decisions non-decisions assumptions deferrals and superseded items
DAR.002 | MUST | authority | identify the accountable role and confirmation evidence
DAR.003 | MUST | rationale | preserve why the decision was made and which alternatives were considered
DAR.004 | MUST | lifecycle | record effective date review point and reopening trigger
DAR.005 | MUST | scope | state applicability and exclusions
DAR.006 | MUST | evidence | preserve source date uncertainty conflicts and confirmation state
DAR.007 | SHOULD | token | optimize quality-adjusted token ROI after receipt completeness passes
DAR.008 | SHOULD | prompt | keep the receipt contract in a stable prefix and meeting evidence dynamic
DAR.009 | NEVER | consensus | infer approval from silence attendance or repeated wording
DAR.010 | NEVER | authority | replace a formal approval or silently resolve a disputed decision

## Verification

- Every receipt item has a status.
- Every unresolved item has an owner and next confirmation point.
- Decisions have authority evidence, rationale, scope, and effective date.
- Assumptions and conflicts remain visible.

## Failure Modes

- recording only the final answer and losing why;
- omitting what remains undecided;
- treating meeting notes as approval;
- assigning a named person without evidence or authorization;
- leaving assumptions without review triggers;
- allowing one receipt to become permanent truth outside its scope.
