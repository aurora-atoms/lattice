---
name: future-maintainer-note
description: Use to leave a concise evidence-linked explanation of why a non-obvious implementation, boundary, exception, workaround, or architecture choice exists for future maintainers. Input is a bounded code or system surface, decision and incident evidence, constraints, rejected alternatives, owners, dates, and review triggers; output is a maintenance-intent note containing purpose, rationale, constraints, assumptions, alternatives, safe-change boundaries, validation, owner, and reopen conditions. Do not use as a code summary, permanent justification, or substitute for current documentation and tests; preserve behavior, provenance, uncertainty, and future reviewability.
---

# Future Maintainer Note

## Goal

Give a maintainer six months later enough evidence to understand why the system is this way, what must remain true, and when the choice should be reconsidered.

## Use When

Use for non-obvious architecture choices, compatibility constraints, operational workarounds, unusual validations, temporary exceptions, incident-driven safeguards, or code whose apparent simplification could reintroduce known failure.

## Do Not Use When

Do not use to narrate obvious code, defend an unapproved workaround, preserve obsolete intent indefinitely, duplicate full design documents, or hide missing tests behind prose.

## Inputs

Require the bounded system or code surface, current behavior, decision or incident evidence, constraints, assumptions, alternatives considered, owner or accountable role, validation evidence, and review or removal trigger.

## Outputs

Produce:

```text
artifacts/maintainer-intent/<surface-id>/<run-id>/maintainer-note.v1.json
artifacts/maintainer-intent/<surface-id>/<run-id>/note.md
artifacts/capability-runs/future-maintainer-note/<run-id>/run-result.json
```

A complete note contains:

- what the unusual choice does;
- why it exists and which outcome or failure it protects;
- evidence and decision references;
- constraints and assumptions that must remain true;
- alternatives considered and why they were not selected;
- safe and unsafe change boundaries;
- validation commands, tests, metrics, or runtime checks;
- owner or accountable role;
- review date, expiry condition, removal trigger, and related superseding records;
- uncertainty and known gaps.

## Evidence

Rationale must be supported by a decision, incident, test, runtime observation, business rule, or constraint. Do not invent historical intent from code shape. Mark reconstructed explanations as inference until confirmed.

## Success Signals

Evaluate as `met`, `not_met`, or `not_evaluated`:

- the note explains why, not merely what;
- behavior protected by the choice is explicit;
- constraints, assumptions, and alternatives are preserved;
- safe-change boundaries and validation are actionable;
- owner and review triggers prevent permanent folklore;
- the note is concise enough to remain useful near the maintained surface.

## Stop Conditions

Stop at a reviewable note. Do not insert it into code, documentation, or a system of record without explicit authority. Stop when rationale evidence, scope, owner, or validation is unavailable; when conflicting history needs adjudication; or when one bounded retry fails.

## Workflow

1. Bound the maintained surface and intended audience.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted sources.
3. Gather decisions, incidents, constraints, tests, and runtime evidence.
4. Separate confirmed rationale from reconstructed inference.
5. Record alternatives, assumptions, safe-change boundaries, and validation.
6. Add owner, review date, expiry, and removal triggers.
7. Produce a concise note and stop for owner confirmation.

## Rules

FMN.001 | MUST | rationale | explain why the choice exists and what it protects
FMN.002 | MUST | evidence | link rationale to decisions incidents tests rules or runtime evidence
FMN.003 | MUST | boundaries | state safe and unsafe change boundaries
FMN.004 | MUST | alternatives | preserve material alternatives and rejection reasons
FMN.005 | MUST | validation | provide actionable checks for future changes
FMN.006 | MUST | lifecycle | record owner review date expiry and removal triggers
FMN.007 | SHOULD | token | optimize quality-adjusted token ROI and keep the note concise
FMN.008 | SHOULD | prompt | keep note fields stable and surface evidence dynamic
FMN.009 | NEVER | invention | infer historical intent from code without labeling it inference
FMN.010 | NEVER | permanence | use the note to make a temporary constraint permanent

## Verification

- Purpose, rationale, evidence, assumptions, alternatives, boundaries, and validation are present.
- Owner and review or removal triggers are explicit.
- Reconstructed intent is labeled and awaits confirmation.

## Failure Modes

- summarizing code rather than explaining intent;
- omitting rejected alternatives;
- documenting a workaround without expiry;
- claiming rationale not supported by evidence;
- creating a long historical essay that maintainers will not use.
