---
name: context-mastery
description: Use for selecting and coordinating the smallest sufficient context-learning capability for system mental models, layered learning, task-specific domain context, negative knowledge, similar work, expert decision-question preparation, and missing-question discovery. Input is a bounded task, user role, repository or knowledge metadata, permissions, historical Delivery Cases, and current evidence; output is a routing decision plus an evidence-linked system map, learning path, domain context pack, negative-knowledge pack, analogous cases, decision-question packet, or teach-back checkpoint. Do not use as a raw repository dump, generic summarizer, retrieval implementation, or substitute for personal understanding at critical control points; preserve provenance, uncertainty, validation behavior, least privilege, and human authority.
---

# Context Mastery

## Goal

Route an unfamiliar-system, domain-learning, or expert-question need to the smallest sufficient capability and return a bounded evidence-linked artifact.

## Use When

Select one primary capability first:

- B01 `system-mental-model`: runtime map, entry points, flows, controls, impact boundaries;
- B02 `learning-navigator`: layered path, golden and failure paths, exceptions, teach-back;
- B03 `domain-context-pack`: task-specific Skills, sources, rules, decisions, accountable roles, gaps, conflicts;
- B04 `negative-knowledge-pack`: failed attempts, do-not-do guidance, causal evidence, alternatives;
- B05: similar work finder remains in this category boundary;
- B06 `decision-question-builder`: evidence-backed options and a minimum-response question for a scarce expert or accountable leader;
- B07: unasked-questions generator remains in this category boundary.

## Do Not Use When

Do not use for raw dumps, generic summaries, retrieval implementation, source-authority approval, or unverified claims of understanding.

## Inputs

Require a bounded task or Feature Delivery Case, caller or learner role, expected output, source and capability metadata, permission boundary, evidence, and context budget.

For expert questions, also require the decision to unlock, intended respondent or authority, deadline, known facts, material unknowns, and candidate options or enough evidence to derive them.

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

Separate source-supported facts from inference. Preserve resolvable citations, source scope and version or observation time, uncertainty, unknowns, assumptions, conflicts, and guesses. Do not continue beyond the evidence boundary. A plausible explanation, generated summary, or repeated statement is not proof. Keyword similarity alone does not prove a Skill, source, prior case, respondent, or option applies.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- one smallest sufficient primary capability is selected before composition;
- trigger and required inputs match the task;
- the specialist output is evidence-linked and within budget;
- controls, unknowns, conflicts, exclusions, and permission gaps remain visible;
- the user or reviewer can explain why the capability and context were selected;
- an expert-question task produces one bounded decision with comparable evidence-backed options and a minimum sufficient response.

## Stop Conditions

Stop at the requested artifact or next reviewable stage. Stop without repeated probing when required permission, source access, critical facts, recipient authority, or sufficient evidence is unavailable; when a security, privacy, compliance, data-governance, architecture, production, or other high-risk boundary is reached; when validation fails after one bounded corrective retry; or when the goal, stage gate, retry budget, human decision, or user stop condition is reached. State the exact missing permission or evidence, accountable owner, reason, and resumable next step.

## Workflow

1. Bound task, caller, output, decision, permissions, and budget.
2. Query ConPort and compact capability or source metadata first.
3. Compare the task against B01-B07 and select one primary capability.
4. Invoke B01-B04 or B06 dedicated Skills when applicable.
5. Add another capability only for a named dependency, independent check, conflict, or evidence gap.
6. Keep B05 and B07 bounded and evidence-linked.
7. Require teach-back at critical controls and exceptions.
8. For B06, resolve discoverable facts before escalating and require two to four comparable options that unlock one action.
9. Record plausible capabilities and sources intentionally excluded.
10. Keep routing rules stable and task evidence dynamic.

## Rules

BCAT.001 | MUST | routing | select one primary capability before composition
BCAT.002 | MUST | specialist | use dedicated B01 through B04 and B06 Skills when available
BCAT.003 | MUST | context | output a bounded artifact instead of a raw dump
BCAT.004 | MUST | evidence | preserve provenance conflicts uncertainty assumptions and unknowns
BCAT.005 | MUST | learning | require teach-back for critical controls and exceptions
BCAT.006 | MUST | question | route bounded scarce-expert decisions to decision-question-builder
BCAT.007 | MUST | exclusion | record material capabilities and sources intentionally not loaded
BCAT.008 | SHOULD | token | optimize quality-adjusted token ROI after task quality passes
BCAT.009 | NEVER | context | dump the full repository knowledge base or capability catalog
BCAT.010 | NEVER | composition | activate several Skills because selection evidence is weak
BCAT.011 | NEVER | escalation | send an expert a question answerable from already authorized evidence

## References

- Use `../system-mental-model/SKILL.md`, `../learning-navigator/SKILL.md`, `../domain-context-pack/SKILL.md`, `../negative-knowledge-pack/SKILL.md`, or `../decision-question-builder/SKILL.md`.
- Route authority to `../team-knowledge-plane-governor/SKILL.md`, retrieval implementation to `../hybrid-knowledge-retrieval-builder/SKILL.md`, repeated profiles to `../knowledge-profile-evaluator/SKILL.md`, conflicts to `../knowledge-integrity/SKILL.md`, and expert-attention queue management to `../human-judgment-amplifier/SKILL.md`.

## Verification

```bash
python scripts/validate_skill_package.py --root skills/context-mastery
python scripts/validate_skill_package.py --root skills/decision-question-builder
python scripts/validate_capability_context.py --root .
```

## Failure Modes

- category-monolith;
- routing by keyword alone;
- eager composition;
- borrowed understanding;
- context bloat;
- hidden selection tie;
- expert escalation before resolving available evidence;
- a question that asks the recipient to reconstruct options or context.
