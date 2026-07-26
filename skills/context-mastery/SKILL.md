---
name: context-mastery
description: Use for selecting and coordinating the smallest sufficient context-learning capability for system mental models, layered learning, task-specific domain context, negative knowledge, similar work, expert-question preparation, and missing-question discovery. Input is a bounded task, user role, repository or knowledge metadata, permissions, historical Delivery Cases, and current evidence; output is a routing decision plus an evidence-linked system map, learning path, domain context pack, negative-knowledge pack, analogous cases, question set, or teach-back checkpoint. Do not use as a raw repository dump, generic summarizer, retrieval implementation, or substitute for personal understanding at critical control points; preserve provenance, uncertainty, validation behavior, least privilege, and human authority.
---

# Context Mastery

## Goal

Route an unfamiliar-system or domain-learning need to the smallest sufficient capability and return a bounded evidence-linked artifact.

## Use When

Select one primary capability first:

- B01 `system-mental-model`: runtime map, entry points, flows, controls, impact boundaries;
- B02 `learning-navigator`: layered path, golden and failure paths, exceptions, teach-back;
- B03 `domain-context-pack`: task-specific Skills, sources, rules, decisions, accountable roles, gaps, conflicts;
- B04 `negative-knowledge-pack`: failed attempts, do-not-do guidance, causal evidence, alternatives;
- B05-B07: similar work, question builder, and unasked-questions remain in this category boundary.

## Do Not Use When

Do not use for raw dumps, generic summaries, retrieval implementation, source-authority approval, or unverified claims of understanding.

## Inputs

Require a bounded task or Feature Delivery Case, caller or learner role, expected output, source and capability metadata, permission boundary, evidence, and context budget.

## Outputs

Produce `context-mastery-selection.json`, a concise Markdown companion, and `lat.capability.run_result.v1`.

Default writeback:

```text
artifacts/context-mastery/<scope-id>/<run-id>/context-mastery-selection.json
artifacts/context-mastery/<scope-id>/<run-id>/summary.md
artifacts/capability-runs/context-mastery/<run-id>/run-result.json
```

When write permission is unavailable, return the complete structured result inline with `write_status=returned_inline`.

The selection states the primary capability, trigger evidence, required inputs, gaps, expected artifact, optional dependencies, exclusions, and stop boundary.

## Evidence

Separate source-supported facts from inference. Preserve resolvable citations, source scope and version or observation time, uncertainty, unknowns, assumptions, conflicts, and guesses. Do not continue beyond the evidence boundary. A plausible explanation, generated summary, or repeated statement is not proof. Keyword similarity alone does not prove a Skill, source, or prior case applies.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- one smallest sufficient primary capability is selected before composition;
- trigger and required inputs match the task;
- the specialist output is evidence-linked and within budget;
- controls, unknowns, conflicts, exclusions, and permission gaps remain visible;
- the user or reviewer can explain why the capability and context were selected.

## Stop Conditions

Stop at the requested artifact or next reviewable stage. Stop without repeated probing when required permission, source access, critical facts, or sufficient evidence is unavailable; when a security, privacy, compliance, data-governance, architecture, production, or other high-risk boundary is reached; when validation fails after one bounded corrective retry; or when the goal, stage gate, retry budget, or user stop condition is reached. State the exact missing permission or evidence, accountable owner, reason, and resumable next step.

## Workflow

1. Bound task, caller, output, decision, permissions, and budget.
2. Query ConPort and compact capability or source metadata first.
3. Compare the task against B01-B07 and select one primary capability.
4. Invoke B01-B04 dedicated Skills when applicable.
5. Add another capability only for a named dependency, independent check, conflict, or evidence gap.
6. Keep B05-B07 bounded and evidence-linked.
7. Require teach-back at critical controls and exceptions.
8. Record plausible capabilities and sources intentionally excluded.
9. Keep routing rules stable and task evidence dynamic.

## Rules

BCAT.001 | MUST | routing | select one primary capability before composition
BCAT.002 | MUST | specialist | use dedicated B01 through B04 Skills when available
BCAT.003 | MUST | context | output a bounded artifact instead of a raw dump
BCAT.004 | MUST | evidence | preserve provenance conflicts uncertainty assumptions and unknowns
BCAT.005 | MUST | learning | require teach-back for critical controls and exceptions
BCAT.006 | MUST | exclusion | record material capabilities and sources intentionally not loaded
BCAT.007 | SHOULD | token | optimize quality-adjusted token ROI after task quality passes
BCAT.008 | NEVER | context | dump the full repository knowledge base or capability catalog
BCAT.009 | NEVER | composition | activate several Skills because selection evidence is weak

## References

- Use `../system-mental-model/SKILL.md`, `../learning-navigator/SKILL.md`, `../domain-context-pack/SKILL.md`, or `../negative-knowledge-pack/SKILL.md`.
- Route authority to `../team-knowledge-plane-governor/SKILL.md`, retrieval implementation to `../hybrid-knowledge-retrieval-builder/SKILL.md`, repeated profiles to `../knowledge-profile-evaluator/SKILL.md`, and conflicts to `../knowledge-integrity/SKILL.md`.

## Verification

```bash
python scripts/validate_skill_package.py --root skills/context-mastery
python scripts/validate_capability_context.py --root .
```

## Failure Modes

- category-monolith;
- routing by keyword alone;
- eager composition;
- borrowed understanding;
- context bloat;
- hidden selection tie.
