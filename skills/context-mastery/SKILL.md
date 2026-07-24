---
name: context-mastery
description: Use for codebase understanding, controlled learning, task-specific domain context, negative knowledge, similar delivery work, expert-question preparation, and missing-question discovery; do not use as a raw repository dump, generic summarizer, or substitute for human understanding of critical control points; input is a bounded task, repository map, internal rules, decisions, incidents, historical Delivery Cases, and user experience level; output is a compact context pack, system map, learning path, known traps, analogous cases, verification questions, and teach-back checkpoints that preserve behavioral constraints, provenance, and quality-adjusted token ROI.
---

# Context Mastery

## Goal
Build a task-bounded mental model without flooding context or outsourcing critical understanding.

## Use When
Select the smallest sufficient atomic capability:
- B01 Codebase Understanding Assistant
- B02 Learning Navigator
- B03 Domain Context Pack
- B04 Negative Knowledge Pack
- B05 Similar Work Finder
- B06 Question Builder
- B07 Unasked Questions Generator

## Do Not Use When
Do not use for raw repository dumps, generic summaries, or unverified claims of understanding.

## Inputs
Use a bounded task, relevant code map, decisions, business rules, incidents, historical Delivery Cases, permissions, and user experience level.

## Outputs
Return a system map, must-know control points, task context pack, known traps, analogous cases, high-quality questions, unknowns, and teach-back checkpoints.

## Workflow
1. Bound the task and user role.
2. Query ConPort before loading or searching the full skill text when ConPort is available; otherwise use targeted source reads.
3. Select one atomic capability first.
4. Build the map before detail.
5. Load only necessary sources and cite provenance.
6. Separate critical control points from optional branches.
7. Require teach-back for high-risk understanding.

## Rules
BCAT.001 | MUST | scope | bind context to the current Feature Delivery Case | enforce
BCAT.002 | MUST | routing | select one atomic capability before composing | enforce
BCAT.003 | MUST | context | output a context pack instead of a raw dump | enforce
BCAT.004 | MUST | evidence | preserve source provenance, conflicts, and unknowns | enforce
BCAT.005 | MUST | learning | require teach-back for critical control points | enforce
BCAT.006 | MUST | token | optimize quality-adjusted token ROI | enforce
BCAT.007 | SHOULD | prompt | keep rules and the output contract in a stable prefix | prefer
BCAT.008 | NEVER | context | dump the full repository, logs, or knowledge base | block

## Verification
- Context is task-scoped and source-linked.
- Critical control points are explicit.
- Applicability limits and conflicts are visible.
- The user can verify or teach back the core model.

## Failure Modes
- Presenting summaries as verified understanding.
- Hiding source conflicts or applicability limits.
- Loading unrelated knowledge for completeness.
