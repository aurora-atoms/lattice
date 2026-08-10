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

Produce `domain-context-pack.v1.json` conforming to `schemas/domain-context-pack.v1.schema.json`, a concise Markdown companion, and `lat.capability.run_result.v1`.

Default writeback:

```text
artifacts/domain-context/<scope-id>/<run-id>/domain-context-pack.v1.json
artifacts/domain-context/<scope-id>/<run-id>/summary.md
artifacts/capability-runs/domain-context-pack/<run-id>/run-result.json
```

When write permission is unavailable, return the complete structured result inline with `write_status=returned_inline`.

The pack must include task scope, caller authorization, context budget, source inventory and selection state, evidence-linked context items, unknowns, conflicts, activation order, answerability, evidence, and expiry or refresh conditions. Business rules, system constraints, historical decisions, accountable contacts or roles, selected Skills, documents, and code surfaces are represented through the typed source and context-item records rather than a raw source dump.

## Machine Contract

`schemas/domain-context-pack.v1.schema.json` is the public machine shape. `scripts/validate_domain_context_pack.py` applies structural and semantic gates that prose alone cannot enforce.

The validator must establish all of the following before the pack may report `answerability.status=answerable`:

- every selected source is authorized, current at `as_of_at`, and unexpired when an expiry exists;
- each context item references a selected source whose declared authority covers the item's information class;
- every evidence citation is an addressable URI-like reference rather than an unresolvable label;
- `context_budget.selected_tokens` equals the deterministic sum of selected context-item token estimates and does not exceed `max_tokens`;
- every conditional source has an explicit activation action such as permission request, refresh, conditional load, or human review;
- blocking unknowns and unresolved blocking conflicts remain visible and prevent `answerable`;
- an authorization decision of `deny` cannot carry selected context and must stop as `blocked`;
- public synthetic fixtures remain `synthetic_reference` with downstream adoption `not_observed`.

The contract does not grant source authority, access permission, private adoption, or human approval. It only proves that a context pack obeys the declared public shape and fail-closed semantics.

## Evidence

Separate source-supported facts from inference. Preserve resolvable citations, source scope and version or observation time, uncertainty, unknowns, assumptions, conflicts, and guesses. Do not continue beyond the evidence boundary. Selection must be justified by task relevance, source authority, permission, freshness, and expected information gain. A retrieved or similar source is not automatically applicable. Accountable contacts must come from authorized directories or source ownership metadata and must not be invented.

For machine-valid packs, each selected source declares the information classes for which it is authoritative or supporting, and each context item cites addressable evidence from that selected source. Stale, denied, unknown-access, or authority-mismatched sources may remain visible as conditional or excluded evidence but may not silently enter selected context.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- every selected source or Skill has a task-specific reason;
- business rules, constraints, decisions, accountable roles, unknowns, and conflicts are represented;
- access, authority, freshness, and expiry checks pass for selected sources;
- excluded or conditional high-cost, stale, unauthorized, or unrelated context is explicit;
- selected-token accounting is deterministic and within the declared context budget;
- the activation plan tells the runtime what to load now, later, after permission or refresh, or never;
- the schema and semantic validator pass;
- the pack supports the task without a raw dump.

## Stop Conditions

Stop at the requested artifact or next reviewable stage. Stop without repeated probing when required permission, source access, critical facts, or sufficient evidence is unavailable; when a security, privacy, compliance, data-governance, architecture, production, or other high-risk boundary is reached; when validation fails after one bounded corrective retry; or when the goal, stage gate, retry budget, or user stop condition is reached. State the exact missing permission or evidence, accountable owner, reason, and resumable next step.

When blocking unknowns, unresolved material conflicts, denied required sources, or stale required evidence prevent a reliable pack, preserve them and return `answerability.status=partial`, `abstain`, or `blocked` rather than converting them into factual context.

## Workflow

1. Bound the task, output contract, caller role, permissions, and token budget.
2. Query compact knowledge and capability metadata before source bodies.
3. Identify required information classes: rules, constraints, decisions, accountable roles, code, examples, negative knowledge, research, or runtime evidence.
4. Select the smallest authorized sources and Skills by relevance, authority, freshness, and expected information gain.
5. Load only bounded excerpts, symbols, line ranges, records, or governed summaries needed now.
6. Record source access, authority scope, observation time, expiry, selection state, and the evidence-linked context items actually admitted.
7. Record unknowns, conflicts, applicability limits, and material sources intentionally excluded or held conditional.
8. Produce an activation plan: load now, discover conditionally, request permission, request refresh, human review, or exclude.
9. Compute selected-token accounting and set answerability from the remaining evidence, permission, freshness, unknown, and conflict state.
10. Validate the JSON artifact with `scripts/validate_domain_context_pack.py`; perform at most one bounded corrective retry.
11. Route source authority to team-knowledge-plane-governor, retrieval implementation to hybrid-knowledge-retrieval-builder, repeated profile evaluation to knowledge-profile-evaluator, and conflicts to knowledge-integrity.
12. Keep invariant policy stable and task content dynamic.

## Rules

DCP.001 | MUST | task | bind every selected context item to the current task and output
DCP.002 | MUST | access | apply caller authorization and source policy before loading content
DCP.003 | MUST | assembly | include rules constraints decisions accountable roles unknowns and conflicts when applicable
DCP.004 | MUST | activation | state what loads now later after a trigger or not at all
DCP.005 | MUST | provenance | preserve source locator owner version freshness and applicability
DCP.006 | MUST | exclusion | record material sources and capabilities intentionally excluded or conditional
DCP.007 | SHOULD | token | maximize evidence value per context token after safety passes
DCP.008 | NEVER | context | dump the knowledge base repository or capability catalog
DCP.009 | NEVER | authority | treat a context pack index summary or model output as source authority
DCP.010 | NEVER | privacy | invent accountable contacts or include unauthorized personal information
DCP.011 | MUST | selection | selected sources are authorized current unexpired and authoritative for admitted information classes
DCP.012 | MUST | budget | declared selected token count equals admitted context token sum and does not exceed the declared maximum token budget
DCP.013 | MUST | uncertainty | preserve blocking unknowns and unresolved blocking conflicts and prevent answerable while either remains
DCP.014 | NEVER | selection | admit denied stale unknown-access or authority-mismatched source content into selected context
DCP.015 | MUST | validation | fail closed when schema or semantic validation does not pass after one bounded corrective retry

## References

Route authority, retrieval, evaluation, and conflict work to the existing knowledge-plane Skills named in the workflow.

Machine contract files:

```text
schemas/domain-context-pack.v1.schema.json
scripts/validate_domain_context_pack.py
evals/trigger_queries.json
evals/output_cases.json
evals/fixtures/valid-domain-context-pack.synthetic.json
```

## Verification

```bash
python scripts/validate_skill_package.py --root skills/domain-context-pack
python -m json.tool skills/domain-context-pack/schemas/domain-context-pack.v1.schema.json >/dev/null
python skills/domain-context-pack/scripts/validate_domain_context_pack.py \
  skills/domain-context-pack/evals/fixtures/valid-domain-context-pack.synthetic.json
python -m unittest discover -s skills/domain-context-pack/evals -p 'test_*.py' -v
```

## Failure Modes

- knowledge-dump;
- relevance-by-keyword without task fit;
- authority-collapse from source to summary;
- stale-decision activation;
- selected denied or unknown-access source;
- context item outside source authority scope;
- token-budget drift or understated selected-token cost;
- blocking unknown or conflict compressed away;
- invented accountable contacts;
- hidden source conflicts;
- context selected without an activation condition;
- schema-green but semantic-invalid pack.
