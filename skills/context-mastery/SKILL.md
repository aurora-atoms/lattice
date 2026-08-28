---
name: context-mastery
description: Use for selecting and coordinating the smallest sufficient context-learning capability for system mental models, code-originated runtime-effect verification, layered learning, task-specific domain context, negative knowledge, similar work, expert decision-question preparation, and consequential missing-question discovery. Input is a bounded task, user role, repository or knowledge metadata, permissions, historical Delivery Cases, and current evidence; output is a routing decision plus an evidence-linked system map, learning path, domain context pack, negative-knowledge pack, analogous cases, decision-question packet, unasked-questions gap map, or teach-back checkpoint. Do not use as a raw repository dump, generic summarizer, retrieval implementation, blind live-system search, or substitute for personal understanding at critical control points; preserve behavior, provenance, uncertainty, validation, least privilege, and human authority.
---

# Context Mastery

## Goal

Route an unfamiliar-system, domain-learning, expert-question, or review-gap need to the smallest sufficient capability and return a bounded evidence-linked artifact.

## Use When

Select one primary capability first:

- B01 `system-mental-model`: runtime map, entry points, flows, controls, impact boundaries;
- B02 `learning-navigator`: layered path, golden and failure paths, exceptions, teach-back;
- B03 `domain-context-pack`: task-specific Skills, sources, rules, decisions, accountable roles, gaps, conflicts;
- B04 `negative-knowledge-pack`: failed attempts, do-not-do guidance, causal evidence, alternatives;
- B05: similar work finder remains in this category boundary;
- B06 `decision-question-builder`: evidence-backed options and a minimum-response question for a scarce expert or accountable leader;
- B07 `unasked-questions-generator`: impact-ranked questions missing from requirements, design, cross-system change, or release readiness.

For a question that begins with code and asks whether a runtime side effect occurred, select B01 first. The system mental model must establish an Expected Effect Contract from bounded code and configuration before optional data-context assembly or live-source verification. For a question that begins with unknown data assets, select B03 first. A destination name such as Elasticsearch or Kafka does not determine the route.

## Do Not Use When

Do not use for raw dumps, generic summaries, retrieval implementation, source-authority approval, exhaustive checklists, or unverified claims of understanding.

## Inputs

Require a bounded task or Feature Delivery Case, caller or learner role, expected output, source and capability metadata, permission boundary, evidence, and context budget.

For expert questions, also require the decision to unlock, intended respondent or authority, deadline, known facts, material unknowns, and candidate options or enough evidence to derive them.

For missing-question discovery, also require the reviewed artifact, delivery stage, next commitment gate, dependencies, business rules, assumptions, historical incidents, and accountable roles.

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

Separate source-supported facts from inference. Preserve resolvable citations, source scope and version or observation time, uncertainty, unknowns, assumptions, conflicts, and guesses. Do not continue beyond the evidence boundary. A plausible explanation, generated summary, repeated statement, or generic checklist is not proof. Keyword similarity alone does not prove a Skill, source, prior case, respondent, option, or missing question applies.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- one smallest sufficient primary capability is selected before composition;
- trigger and required inputs match the task;
- the specialist output is evidence-linked and within budget;
- controls, unknowns, conflicts, exclusions, and permission gaps remain visible;
- the user or reviewer can explain why the capability and context were selected;
- an expert-question task produces one bounded decision with comparable evidence-backed options and a minimum sufficient response;
- a missing-question task produces a small impact-ranked gap set with owners, latest safe answer times, and explicit human-controlled dispositions.

## Stop Conditions

Stop at the requested artifact or next reviewable stage. Stop without repeated probing when required permission, source access, critical facts, recipient authority, review boundary, gate authority, or sufficient evidence is unavailable; when a security, privacy, compliance, data-governance, architecture, production, or other high-risk boundary is reached; when validation fails after one bounded corrective retry; or when the goal, stage gate, retry budget, human decision, or user stop condition is reached. State the exact missing permission or evidence, accountable owner, reason, and resumable next step.

## Workflow

1. Bound task, caller, output, decision or review gate, permissions, and budget.
2. Query ConPort and compact capability or source metadata first.
3. Classify code-originated runtime verification versus data-originated discovery, then compare the task against B01-B07 and select one primary capability.
4. Invoke B01-B04, B06, or B07 dedicated Skills when applicable.
5. Add another capability only for a named dependency, independent check, conflict, or evidence gap.
6. Keep B05 bounded and evidence-linked.
7. Require teach-back at critical controls and exceptions.
8. For B06, resolve discoverable facts before escalating and require two to four comparable options that unlock one action.
9. For B07, remove generic or already-answered questions, rank retained gaps by impact and timing, and preserve human authority over blockers and accepted uncertainty.
10. Record plausible capabilities and sources intentionally excluded.
11. Keep routing rules stable and task evidence dynamic.

## Rules

BCAT.001 | MUST | routing | select one primary capability before composition
BCAT.002 | MUST | specialist | use dedicated B01 through B04 B06 and B07 Skills when available
BCAT.003 | MUST | context | output a bounded artifact instead of a raw dump
BCAT.004 | MUST | evidence | preserve provenance conflicts uncertainty assumptions and unknowns
BCAT.005 | MUST | learning | require teach-back for critical controls and exceptions
BCAT.006 | MUST | question | route bounded scarce-expert decisions to decision-question-builder
BCAT.007 | MUST | gap | route consequential missing-question reviews to unasked-questions-generator
BCAT.008 | MUST | exclusion | record material capabilities and sources intentionally not loaded
BCAT.009 | SHOULD | token | optimize quality-adjusted token ROI after task quality passes
BCAT.010 | NEVER | context | dump the full repository knowledge base or capability catalog
BCAT.011 | NEVER | composition | activate several Skills because selection evidence is weak
BCAT.012 | NEVER | escalation | send an expert a question answerable from already authorized evidence
BCAT.013 | NEVER | checklist | treat generic question coverage as evidence of a missing consequential question
BCAT.014 | MUST | runtime | route code-originated external-effect questions through system-mental-model before optional data-context assembly or live search
BCAT.015 | MUST | discovery | route data-originated asset-discovery questions through domain-context-pack before broad source inspection
BCAT.016 | NEVER | routing | infer the route solely from the destination technology name

## References

- Use `../system-mental-model/SKILL.md`, `../learning-navigator/SKILL.md`, `../domain-context-pack/SKILL.md`, `../negative-knowledge-pack/SKILL.md`, `../decision-question-builder/SKILL.md`, or `../unasked-questions-generator/SKILL.md`.
- Route authority to `../team-knowledge-plane-governor/SKILL.md`, retrieval implementation to `../hybrid-knowledge-retrieval-builder/SKILL.md`, repeated profiles to `../knowledge-profile-evaluator/SKILL.md`, conflicts and assumption expiry to `../knowledge-integrity/SKILL.md`, and expert-attention queue or stakeholder-risk management to the appropriate human-judgment or risk capability.

## Verification

```bash
python scripts/validate_skill_package.py --root skills/context-mastery
python scripts/validate_skill_package.py --root skills/decision-question-builder
python scripts/validate_skill_package.py --root skills/unasked-questions-generator
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
- a question that asks the recipient to reconstruct options or context;
- a generic review checklist presented as missing-question discovery;
- turning every unknown into an automatic blocker.
