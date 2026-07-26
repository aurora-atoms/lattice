---
name: negative-knowledge-pack
description: Use for finding and packaging evidence about what not to do, why an approach failed, where it is unsafe or ineffective, and what safer alternatives or revalidation conditions apply. Input is a bounded task, failed attempts, incidents, rejected designs, test results, decisions, scope and version metadata, and authorized owner explanations; output is an evidence-linked negative-knowledge pack with avoid guidance, causal basis, applicability, exceptions, alternatives, owners, expiry, and revalidation triggers. Do not use to turn anecdotes into universal prohibitions, shame people, preserve stale constraints, or block experimentation without evidence; preserve provenance, uncertainty, validation behavior, human authority, and scope limits.
---

# Negative Knowledge Pack

## Goal

Prevent repeated mistakes by making failed approaches and do-not-do guidance evidence-backed, scoped, actionable, and reviewable.

## Use When

Use before repeating a prior approach, during incident learning, architecture or implementation review, or when a task may cross a known trap.

## Do Not Use When

Do not use for personnel judgment, permanent prohibition from one anecdote, or replacing current tests and owner review with historical memory.

## Inputs

Require a bounded task and at least one failed-attempt, incident, rejected-design, test, decision, or owner-approved evidence source with scope and time context.

## Outputs

Produce `negative-knowledge-pack.v1.json`, a concise Markdown companion, and `lat.capability.run_result.v1`.

Default writeback:

```text
artifacts/negative-knowledge/<scope-id>/<run-id>/negative-knowledge-pack.v1.json
artifacts/negative-knowledge/<scope-id>/<run-id>/summary.md
artifacts/capability-runs/negative-knowledge-pack/<run-id>/run-result.json
```

When write permission is unavailable, return the complete structured result inline with `write_status=returned_inline`.

The pack must include the attempted approach, observed outcome, established and unestablished causes, avoid guidance, why it matters, applicability scope, exceptions, safer alternatives, owner, evidence, expiry, and revalidation triggers.

## Evidence

Separate source-supported facts from inference. Preserve resolvable citations, source scope and version or observation time, uncertainty, unknowns, assumptions, conflicts, and guesses. Do not continue beyond the evidence boundary. A plausible explanation, generated summary, or repeated statement is not proof. Distinguish the fact that an attempt failed from the inference about why it failed. Preserve counterevidence, changed conditions, and unknown causes. A single incident or opinion cannot establish a universal prohibition.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- each avoid rule is linked to an observed outcome or authoritative decision;
- causal claims distinguish established, inferred, conflicting, and unknown;
- scope, version, environment, and expiry are explicit;
- key exceptions and changed-condition triggers are explicit;
- at least one safer alternative or validation path is supplied when possible;
- the pack prevents repetition without blocking justified re-experimentation.

## Stop Conditions

Stop at the requested artifact or next reviewable stage. Stop without repeated probing when required permission, source access, critical facts, or sufficient evidence is unavailable; when a security, privacy, compliance, data-governance, architecture, production, or other high-risk boundary is reached; when validation fails after one bounded corrective retry; or when the goal, stage gate, retry budget, or user stop condition is reached. State the exact missing permission or evidence, accountable owner, reason, and resumable next step.

## Workflow

1. Bound the current task and the candidate repeated approach.
2. Query compact incident, decision, test, and Delivery Case metadata before long records.
3. Identify attempted approach, context, expected outcome, observed outcome, and impact.
4. Separate established cause from inferred cause, conflict, and unknown.
5. Define avoid guidance and explain why it applies to the current task.
6. Record scope, version, environment, owners, exceptions, alternatives, expiry, and revalidation triggers.
7. Route stale or conflicting decisions to knowledge-integrity and promotion to the appropriate knowledge governor.
8. Stop rather than generalize when evidence cannot support the prohibition.
9. Keep the negative-knowledge contract stable and case evidence dynamic.

## Rules

NKP.001 | MUST | evidence | link every avoid rule to an observed outcome or authoritative decision
NKP.002 | MUST | causality | separate failure fact established cause inference conflict and unknown
NKP.003 | MUST | scope | record version environment applicability exceptions and expiry
NKP.004 | MUST | alternative | provide a safer alternative or validation path when evidence supports one
NKP.005 | MUST | review | define owner and revalidation trigger
NKP.006 | SHOULD | token | prefer compact high-signal failure evidence over full incident dumps
NKP.007 | NEVER | people | use negative knowledge for personnel ranking blame or shame
NKP.008 | NEVER | universal | convert one anecdote into a permanent universal prohibition
NKP.009 | NEVER | stale | apply superseded constraints without current validation

## References

Route stale or conflicting decisions to `../knowledge-integrity/SKILL.md` and governed promotion to `../team-knowledge-plane-governor/SKILL.md`.

## Verification

```bash
python scripts/validate_skill_package.py --root skills/negative-knowledge-pack
```

## Failure Modes

- anecdote-to-law;
- post-hoc-causality;
- stale prohibition;
- missing exceptions;
- no safer alternative;
- person-focused blame instead of system learning;
- incident dump without actionable guidance.
