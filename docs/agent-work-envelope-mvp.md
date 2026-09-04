# Agent Work Envelope MVP

## Status

```text
classification: task_scoped_reference
maturity: mvp
primary_value_path: team_reuse
public_scope: generic execution guidance only
private_scope: real task evidence, owners, source paths, outcomes, and adoption observations remain downstream
source_basis: 2026-09-04 Skill x Contract x Context MVP research
```

This document records the minimum runtime envelope for using existing Agent capabilities with less repeated explanation, less scope drift, and better continuity across sessions or Agent hosts.

It is **not** a new Lattice module, Agent, Skill, schema, orchestrator, verification service, or fact store. It does not supersede the Feature Delivery Case, Capability Profile, capability run result, Senior Attention workflow, or any active module.

The MVP deliberately shrinks the broader Contract architecture into four runtime blocks:

```text
Skill + Task Contract + Context Input
                |
                v
              Agent
                |
                v
       Work Output + Context Output
```

The goal is to make the next Agent able to understand what capability is being used, what must be achieved, where the task currently stands, and what evidence or unresolved state should survive the handoff.

## 1. Core Principle

Use contracts to narrow the **success and safety space**, not the implementation space.

A good Contract defines:

- what observable state should change;
- what scope is in bounds;
- what must not be violated;
- what evidence is sufficient to stop;
- what authority the Agent has and where a human decision is required.

It should **not** prescribe a detailed implementation plan unless the path itself is a required policy, safety, migration, or compatibility constraint.

```text
narrow success space
+ explicit boundaries
+ wide solution space
= strong-Agent-friendly execution
```

Plan, To-do, decomposition, tool choice, hypotheses, and implementation details are runtime scaffolding. They may change freely inside the Contract boundary and should not become durable governance merely because they were useful in one run.

## 2. When to Use This MVP

Use the full envelope when at least one is true:

- the task is expected to span multiple Agent turns or sessions;
- a handoff to another Agent, model, IDE, or workspace is likely;
- the task is easy to misunderstand or repeatedly reconstruct;
- scope drift would be costly;
- the result needs evidence that another Agent or human can reopen;
- the current work depends on decisions already made that should not be re-litigated.

For a simple one-shot question with no meaningful handoff, state, or risk of reconstruction, do not force this envelope.

## 3. Block A — Skill

The Skill block states the primary reusable capability used for the current step.

MVP rules:

1. Prefer native runtime Skill discovery.
2. Select **one primary Skill** for the named gap.
3. If no useful Skill exists, write `none` and continue; do not create a new Skill just to satisfy the template.
4. Load references progressively and only when the selected Skill reaches a named evidence or quality gap.
5. Do not inject the full Skill catalog or all potentially relevant references.

Record only:

```text
selected_skill
version                 # when known
why_selected
loaded_references
```

Example:

```yaml
skill:
  selected_skill: delivery-rescue
  version: 1.0.0
  why_selected: reproduce and isolate the pagination regression before proposing a fix
  loaded_references:
    - references/bug-reproduction.md
```

The Skill block is a runtime declaration, not a new capability identity source. Canonical identity and version remain in the existing capability registry.

## 4. Block B — Task Contract

The MVP Task Contract has exactly five load-bearing fields:

```text
goal
scope
must_not
done_when
authority
```

### `goal`

Describe the observable state change, not the implementation steps.

Good:

```text
Pagination returns every item exactly once for 19, 20, and 21 item datasets.
```

Weak:

```text
Edit PaginationService.cs and add an if statement.
```

### `scope`

State the bounded surface the current run may inspect or change.

Example:

```text
Pagination service, its direct tests, and the API response mapping used by this endpoint.
```

### `must_not`

List only load-bearing boundaries whose violation would invalidate the result.

Example:

```text
Do not change the public response contract or silently reduce page size.
```

### `done_when`

State observable stopping conditions. Prefer external state, deterministic checks, behavioral evidence, or reopenable evidence over model self-assertion.

Example:

```text
19/20/21 item regression cases pass, existing pagination tests pass, and no duplicate or missing item is observed.
```

### `authority`

State what the Agent may decide or change autonomously and what requires a human.

Example:

```text
May modify implementation and tests on the isolated branch. Ask before changing the public API, shared schema, or deployment configuration.
```

## 5. Contract Stability and Amendment

The Task Contract is stable across a run unless new evidence shows one of its five load-bearing fields is wrong or impossible to satisfy.

The Agent may freely change:

- plan;
- To-do list;
- decomposition;
- hypotheses;
- context selection;
- tool choice within granted authority;
- implementation.

The Agent must **not silently change**:

- `goal`;
- `scope`;
- `must_not`;
- `done_when`;
- `authority`.

If one must change, stop and request an explicit Contract amendment with:

```text
observed_conflict
contract_field_affected
evidence_ref
proposed_change
impact
human_decision_needed
```

Example:

```yaml
contract_amendment_request:
  observed_conflict: current schema cannot represent the required state
  contract_field_affected: scope
  evidence_ref: src/schema/order-state.json#L22-L41
  proposed_change: allow a backward-compatible schema migration
  impact: shared consumer compatibility must be re-verified
  human_decision_needed: approve scope expansion
```

Amendment is allowed; silent drift is not.

## 6. Block C — Context Input

Context Input answers one question:

> What does this Agent need to know **now** to avoid doing the wrong work or repeating already-settled work?

Use only:

```text
current_state
relevant_inputs
decisions_already_made
unknowns
current_focus
previous_evidence
```

### Rules

- Do not treat Context Input as a knowledge warehouse.
- Do not copy full chat history, full logs, the full repository, or the full evidence corpus.
- Use pointers, bounded excerpts, symbols, line ranges, tests, revisions, and evidence refs.
- Remove a field if deleting it would not materially increase the chance of a wrong decision, repeated work, or scope drift.
- Preserve source authority, freshness, conflicts, and unknowns when they matter.

Example:

```yaml
context_input:
  current_state: regression reproduced only at exact page boundary
  relevant_inputs:
    - issue: BUG-142
    - file: src/PaginationService.cs
    - test: tests/PaginationBoundaryTests.cs
  decisions_already_made:
    - public API shape must remain unchanged
  unknowns:
    - whether the duplicate originates before or after response mapping
  current_focus: isolate the first incorrect state transition
  previous_evidence:
    - evidence://run-17/repro-20-items
```

## 7. Block D — Context Output

Context Output is the compact candidate state for the next turn or next Agent. It is **not** an append-only transcript and is not automatically promoted to memory, belief, Skill, rule, or team asset.

Return:

```text
state_after
decisions_made
changes_made
ai_evidence
unresolved
next_context
```

### `state_after`

What is now true, false, reproduced, fixed, blocked, or still unknown?

### `decisions_made`

Record only decisions made during this run and their bounded reason.

### `changes_made`

State what changed. Use `none` when nothing was modified.

### `ai_evidence`

Use the four-field evidence shape in the next section.

### `unresolved`

Keep only unknowns, conflicts, blockers, or unverified assumptions that can still change the next action.

### `next_context`

State the minimum information the next Agent needs plus the `next_safe_action`.

The next run should **select** relevant Context Output fields and use them as the next Context Input. Do not automatically accumulate all prior outputs.

## 8. AI Evidence — Minimal Reopenable Record

Each AI Evidence entry has four fields:

```text
observed
source_ref
supports
limitation
```

Example:

```yaml
ai_evidence:
  - observed: the 20-item regression test now passes after the boundary calculation change
    source_ref: tests/PaginationBoundaryTests.cs::exact_page_boundary
    supports: done_when[0]
    limitation: 21-item case has not yet been executed
```

Rules:

1. `observed` records what the Agent actually saw, ran, read, or received.
2. `source_ref` must be reopenable when the environment supports it.
3. `supports` names the judgment, action, or `done_when` condition the evidence bears on.
4. `limitation` states what the evidence does **not** establish.
5. Do not replace evidence with statements such as `verified`, `looks correct`, or model confidence.
6. Do not dump raw logs or transcripts into Context Output; retain them at their source and reference them.

This MVP does not create a separate Verifier Agent. Use the strongest existing checks available in the task environment and record the resulting evidence honestly.

## 9. Runtime Loop

The minimum loop is:

```text
Prompt N
  = selected Skill
  + Task Contract
  + Context Input

Agent
  -> explores and changes its plan as needed
  -> executes inside authority
  -> checks done_when using available evidence
  -> stops, escalates, or requests Contract amendment

Return
  = requested work output
  + Context Output

Prompt N+1
  = selected Skill for the next named gap
  + same or explicitly amended Task Contract
  + compressed Context Output selected as new Context Input
```

The session may be disposable. Goal, boundary, current state, evidence, unresolved decisions, and next safe action must remain reconstructable without relying on hidden chain-of-thought or the complete conversation.

## 10. Stop Rules

Stop when any of these is true:

- `done_when` is supported by sufficient current evidence;
- the next action requires a human decision under `authority`;
- required source access, permission, or evidence is missing;
- continuing would exceed `scope` or violate `must_not`;
- the Contract itself must change;
- a bounded retry produces no new evidence, risk reduction, or state change;
- the active Skill's existing stop condition is reached;
- the user says stop.

Do not continue merely to make the analysis longer or the To-do list complete.

## 11. Relationship to Existing Lattice Contracts

This MVP is a thin runtime projection over existing Lattice boundaries.

It does not create a second source of truth.

- `AGENTS.md` remains the repository-level behavior map.
- `registry/capability-manifest.json` remains canonical for capability identity and version.
- Capability Profiles remain authoritative for allowed Skills, tools, permissions, budgets, and verification gates when a Profile is active.
- `feature_delivery_case` remains the primary user-value and evidence boundary.
- `lat.capability.run_result.v1` remains required for an executed registered Skill or Agent run under the existing capability contract.
- Senior Attention, Portable Case Pack, Domain Context Pack, Outcome Receipt, and other existing contracts remain authoritative in their owned scopes.

When both apply:

```text
Agent Work Envelope
  = compact runtime input / handoff projection

Capability Run Result or domain contract
  = authoritative structured result required by that existing capability
```

Do not duplicate authoritative facts into a second incompatible record.

## 12. Non-Goals for the MVP

Do **not** create these merely to implement this document:

- a new orchestrator;
- a Contract Agent;
- a Verifier Agent;
- a new database or state platform;
- GraphDB or vector retrieval;
- a dashboard;
- a new risk taxonomy;
- automatic Skill promotion;
- an always-on multi-Agent conductor;
- a new Lattice module;
- a new permanent Skill for every task type.

Add infrastructure only after repeated real cases identify a specific load-bearing gap that simpler native runtime behavior cannot solve.

## 13. 10-Task MVP Evaluation

Use this envelope on ten real downstream tasks before expanding the architecture.

For each task, record only enough private downstream evidence to answer:

1. Did it reduce repeated explanation or context reconstruction?
2. Did it reduce scope drift or repeated wrong work?
3. Did the next Agent or next session resume faster with less human re-explanation?

Also note any case where the envelope itself created noticeable overhead or hid important information.

If benefit is not obvious, remove fields before adding services, Agents, schemas, or governance.

The public repository may contain only synthetic examples and generic templates. Real task outcomes and adoption observations remain private downstream.

## 14. Copy-Ready Template

Use [`templates/agent-work-envelope-mvp.template.md`](../templates/agent-work-envelope-mvp.template.md).

The template is intentionally prose-friendly for existing Codex, Claude Code, GitHub Copilot, Gemini CLI, and other Agent hosts. It is not a new machine protocol.

## 15. Compact Example — Pagination Bug

```yaml
skill:
  selected_skill: delivery-rescue
  why_selected: reproduce and isolate a bounded delivery-blocking regression
  loaded_references: none

task_contract:
  goal: pagination returns every item exactly once at and around page boundaries
  scope: pagination service, response mapping, and direct tests
  must_not:
    - do not change the public API contract
    - do not reduce the configured page size
  done_when:
    - 19, 20, and 21 item regression cases pass
    - existing pagination regression suite passes
    - no duplicate or missing item is observed
  authority: may change implementation and tests on the isolated branch; ask before public API or shared schema changes

context_input:
  current_state: 20-item boundary failure reproduced
  relevant_inputs:
    - src/PaginationService.cs
    - tests/PaginationBoundaryTests.cs
  decisions_already_made:
    - response shape stays backward compatible
  unknowns:
    - first incorrect state transition is not yet known
  current_focus: isolate cause before implementing the fix
  previous_evidence:
    - evidence://run-17/exact-boundary-repro

context_output:
  state_after: root cause isolated to inclusive upper-bound calculation; fix candidate implemented
  decisions_made:
    - retained existing response mapping because it matches expected semantics
  changes_made:
    - corrected boundary calculation
    - added 19/20/21 item regression coverage
  ai_evidence:
    - observed: 19, 20, and 21 item tests pass
      source_ref: tests/PaginationBoundaryTests.cs
      supports: task_contract.done_when
      limitation: full repository test suite not yet executed
  unresolved:
    - full regression suite remains to run
  next_context:
    next_safe_action: run repository regression suite and inspect any pagination-adjacent failures
```

Notice what is intentionally absent: a permanent To-do list, a separate Contract Agent, a separate Verifier Agent, the full conversation, and the entire repository context.

## 16. Maintainer Rule

Treat every extra field, planner, reviewer, memory object, or workflow step as a hypothesis about a current Agent limitation.

When a stronger model, better native memory, improved Agent host, or better tool removes that limitation, re-test the component's marginal value and delete or demote it when the lift no longer justifies the cost.

Build around invariants. Scaffold around limitations. Remove obsolete scaffolding.
