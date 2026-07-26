---
name: domain-context-pack
description: Use for assembling the smallest authorized task-specific context from a large knowledge base, Skills, documents, codebases, schemas, decisions, incidents, and governed owner directories. Input is a bounded task and output contract, caller role, knowledge inventory, access policy, context budget, and source metadata; output is an evidence-linked domain context pack containing business rules, system constraints, historical decisions, accountable contacts or roles, selected capabilities and sources, unknowns, conflicts, exclusions, and an activation plan. Do not use to dump the knowledge base, approve source authority, implement retrieval, expose restricted content, or load every related resource; preserve least privilege, provenance, freshness, uncertainty, validation behavior, and source-system authority.
---

# Domain Context Pack

## Goal

Activate the smallest useful knowledge and capability set for one task so stored knowledge becomes operational rather than passive.

## Use When

Use when a task needs relevant Skills, documents, code, rules, decisions, incidents, accountable roles, or research selected from a much larger inventory.

## Do Not Use When

Do not use to approve sources, build ingestion or ranking, copy full repositories, or expose content outside the caller authorization.

## Inputs

Require a bounded task, expected output, caller role, knowledge and capability inventory, source authority and access metadata, context budget, and freshness requirements.

## Outputs

Produce `domain-context-pack.v1.json`, a concise Markdown companion, and `lat.capability.run_result.v1`.

Default writeback:

```text
artifacts/domain-context/<scope-id>/<run-id>/domain-context-pack.v1.json
artifacts/domain-context/<scope-id>/<run-id>/summary.md
artifacts/capability-runs/domain-context-pack/<run-id>/run-result.json
```

When write permission is unavailable, return the complete structured result inline with `write_status=returned_inline`.

The pack must include business rules, system constraints, historical decisions, accountable contacts or roles, selected Skills, documents and code surfaces, unknowns, conflicts, excluded sources, activation order, evidence, and expiry or refresh conditions.

## Evidence

Separate source-supported facts from inference. Preserve resolvable citations, source scope and version or observation time, uncertainty, unknowns, assumptions, conflicts, and guesses. Do not continue beyond the evidence boundary. Selection must be justified by task relevance, source authority, permission, freshness, and expected information gain. A retrieved or similar source is not automatically applicable. Accountable contacts must come from authorized directories or source ownership metadata and must not be invented.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- every selected source or Skill has a task-specific reason;
- business rules, constraints, decisions, accountable roles, unknowns, and conflicts are represented;
- access and freshness checks pass;
- excluded high-cost or unrelated context is explicit;
- the activation plan tells the runtime what to load now, later, or never;
- the pack supports the task without a raw dump.

## Stop Conditions

Stop at the requested artifact or next reviewable stage. Stop without repeated probing when required permission, source access, critical facts, or sufficient evidence is unavailable; when a security, privacy, compliance, data-governance, architecture, production, or other high-risk boundary is reached; when validation fails after one bounded corrective retry; or when the goal, stage gate, retry budget, or user stop condition is reached. State the exact missing permission or evidence, accountable owner, reason, and resumable next step.

## Workflow

1. Bound the task, output contract, caller role, permissions, and token budget.
2. Query compact knowledge and capability metadata before source bodies.
3. Identify required information classes: rules, constraints, decisions, accountable roles, code, examples, negative knowledge, or research.
4. Select the smallest authorized sources and Skills by relevance, authority, freshness, and expected information gain.
5. Load only bounded excerpts, symbols, line ranges, records, or governed summaries needed now.
6. Record business rules, constraints, decisions, accountable roles, unknowns, conflicts, and applicability limits.
7. Record excluded sources and why they were not loaded.
8. Produce an activation plan: load now, discover conditionally, request permission, human review, or exclude.
9. Route source authority to team-knowledge-plane-governor, retrieval implementation to hybrid-knowledge-retrieval-builder, repeated profile evaluation to knowledge-profile-evaluator, and conflicts to knowledge-integrity.
10. Keep invariant policy stable and task content dynamic.

## Rules

DCP.001 | MUST | task | bind every selected context item to the current task and output
DCP.002 | MUST | access | apply caller authorization and source policy before loading content
DCP.003 | MUST | assembly | include rules constraints decisions accountable roles unknowns and conflicts when applicable
DCP.004 | MUST | activation | state what loads now later after a trigger or not at all
DCP.005 | MUST | provenance | preserve source locator owner version freshness and applicability
DCP.006 | MUST | exclusion | record material sources and capabilities intentionally excluded
DCP.007 | SHOULD | token | maximize evidence value per context token after safety passes
DCP.008 | NEVER | context | dump the knowledge base repository or capability catalog
DCP.009 | NEVER | authority | treat a context pack index summary or model output as source authority
DCP.010 | NEVER | privacy | invent accountable contacts or include unauthorized personal information

## References

Route authority, retrieval, evaluation, and conflict work to the existing knowledge-plane Skills named in the workflow.

## Verification

```bash
python scripts/validate_skill_package.py --root skills/domain-context-pack
```

## Failure Modes

- knowledge-dump;
- relevance-by-keyword without task fit;
- authority-collapse from source to summary;
- stale-decision activation;
- invented accountable contacts;
- hidden source conflicts;
- context selected without an activation condition.
