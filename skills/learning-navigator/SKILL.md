---
name: learning-navigator
description: Use for turning an unfamiliar system or domain into a layered, task-relevant learning path that preserves global orientation, must-understand control points, a golden path, failure paths, exceptions, and comprehension checks. Input is a bounded learner goal, current experience, available system map or evidence, source material, role, and time budget; output is an evidence-linked learning plan, practice sequence, quiz, teach-back rubric, and progress result. Do not use for generic reading lists, passive summaries, credentialing, or claims that exposure equals understanding; preserve source provenance, uncertainty, validation behavior, critical exceptions, and human judgment.
---

# Learning Navigator

## Goal

Help a learner gain usable understanding quickly without losing the global map, critical controls, failure behavior, or evidence boundaries.

## Use When

Use for onboarding, preparing for a change or incident, or learning a technical domain for a concrete task.

## Do Not Use When

Do not use for generic curricula detached from a task, passive summaries, or replacing hands-on verification with generated explanation.

## Inputs

Require a bounded learning objective, learner role and baseline, time budget, target task or decision, and evidence-linked sources. Prefer a verified system map for software systems.

## Outputs

Produce `learning-path.v1.json`, a concise Markdown companion, and `lat.capability.run_result.v1`.

Default writeback:

```text
artifacts/learning/<scope-id>/<run-id>/learning-path.v1.json
artifacts/learning/<scope-id>/<run-id>/summary.md
artifacts/capability-runs/learning-navigator/<run-id>/run-result.json
```

When write permission is unavailable, return the complete structured result inline with `write_status=returned_inline`.

The path must contain a global map, layered sequence, must-understand controls, golden path, failure paths, critical exceptions, why each item matters, evidence, practice, comprehension questions, teach-back, and deferred branches.

## Evidence

Separate source-supported facts from inference. Preserve resolvable citations, source scope and version or observation time, uncertainty, unknowns, assumptions, conflicts, and guesses. Do not continue beyond the evidence boundary. A plausible explanation, generated summary, or repeated statement is not proof. Link every required item to the workflow, control point, incident, test, schema, or decision that makes it important. Separate factual system behavior from pedagogical inference about learning order.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- learner can state purpose and global topology before local detail;
- learner can explain must-understand control points;
- learner can trace the golden path;
- learner can explain or diagnose a representative failure path;
- learner can explain why critical items matter and name key exceptions;
- learner passes evidence-linked application and teach-back checks.

A generated curriculum is only a partial result.

## Stop Conditions

Stop at the requested artifact or next reviewable stage. Stop without repeated probing when required permission, source access, critical facts, or sufficient evidence is unavailable; when a security, privacy, compliance, data-governance, architecture, production, or other high-risk boundary is reached; when validation fails after one bounded corrective retry; or when the goal, stage gate, retry budget, or user stop condition is reached. State the exact missing permission or evidence, accountable owner, reason, and resumable next step.

## Workflow

1. Bound learner, task, baseline, time, and required decision.
2. Query ConPort first when available; otherwise inspect the verified map and compact metadata.
3. Layer 0: purpose, users, global topology, entry points, vocabulary.
4. Layer 1: must-understand policy, permission, state, validation, routing, and side-effect controls.
5. Layer 2: golden path and why each step matters.
6. Layer 3: failure paths, detection, recovery, and diagnostic mistakes.
7. Layer 4: critical exceptions and required alternate branches.
8. Layer 5: guided practice, validation commands, and teach-back.
9. Defer optional branches with explicit future triggers.
10. Score explanation and application rather than copying.
11. Keep the learning framework stable and learner evidence dynamic.

## Rules

LNAV.001 | MUST | orientation | teach purpose and global map before isolated detail
LNAV.002 | MUST | control | identify controls the learner must personally understand
LNAV.003 | MUST | path | teach one evidence-linked golden path end to end
LNAV.004 | MUST | failure | include failure paths detection and recovery boundaries
LNAV.005 | MUST | value | explain why each required item matters
LNAV.006 | MUST | exception | identify material exceptions and applicability limits
LNAV.007 | MUST | assessment | use application teach-back and diagnosis checks
LNAV.008 | SHOULD | token | optimize quality-adjusted token ROI after comprehension quality passes
LNAV.009 | NEVER | learning | equate reading or artifact generation with demonstrated understanding
LNAV.010 | NEVER | scope | create an exhaustive curriculum when a bounded path is sufficient

## References

Use `../system-mental-model/SKILL.md` when a verified map is missing. Apply `../../docs/capability-context-contract.md` for evidence and run-result behavior.

## Verification

```bash
python scripts/validate_skill_package.py --root skills/learning-navigator
```

## Failure Modes

- curriculum-bloat;
- detail-first learning without a map;
- happy-path-only learning;
- control-point outsourcing to AI;
- quizzes answerable by copying;
- false mastery before teach-back.
