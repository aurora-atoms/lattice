# Agent Work Envelope MVP

Use this template only for tasks that benefit from multi-turn continuity, handoff, bounded scope, or reopenable evidence. For simple one-shot work, use the active runtime normally.

## SKILL

```yaml
selected_skill: <skill-name | none>
version: <semver | unknown>
why_selected: <why this is the smallest sufficient capability for the current gap>
loaded_references:
  - <reference actually loaded | none>
```

Rules:

- Prefer native Skill discovery.
- Declare one primary Skill for the current step.
- Do not load the full Skill catalog or unrelated references.
- If no useful Skill exists, use `none`; do not invent a new Skill to satisfy the template.

## TASK CONTRACT

```yaml
goal: <observable state change>
scope: <bounded surface this run may inspect or change>
must_not:
  - <load-bearing boundary>
done_when:
  - <observable stopping condition>
authority: <what the Agent may decide/change autonomously; what requires a human>
```

Rules:

- Narrow success and safety boundaries, not implementation freedom.
- Do not silently change `goal`, `scope`, `must_not`, `done_when`, or `authority`.
- Plan, To-do, tool choice, decomposition, hypotheses, and implementation may change inside the Contract.
- If a load-bearing Contract field must change, stop and request an explicit amendment with evidence and impact.

## CONTEXT INPUT

```yaml
current_state: <what is currently true / reproduced / complete / blocked>
relevant_inputs:
  - <file, issue, symbol, line range, link, artifact, test, or evidence ref>
decisions_already_made:
  - <decision that should not be re-litigated>
unknowns:
  - <unknown or conflict that can still change the next action>
current_focus: <the one bounded step this run should advance>
previous_evidence:
  - <evidence_ref | none>
```

Rules:

- Include only information whose removal would materially increase wrong work, repeated work, or scope drift.
- Prefer references and bounded excerpts over full chat history, full logs, or repository dumps.
- Preserve material unknowns, conflicts, authority, and freshness.

## RETURN CONTEXT OUTPUT

Return the requested work product plus this compact state:

```yaml
state_after: <what is now true / false / fixed / reproduced / blocked / unknown>
decisions_made:
  - decision: <new bounded decision | none>
    reason: <evidence-linked reason>
changes_made:
  - <change | none>
ai_evidence:
  - observed: <what was actually read, run, observed, or received>
    source_ref: <reopenable source>
    supports: <judgment, action, or done_when condition>
    limitation: <what this evidence does not establish>
unresolved:
  - <remaining unknown, conflict, blocker, or unverified assumption | none>
next_context:
  minimum_needed:
    - <only what the next Agent/session needs>
  next_safe_action: <smallest justified next action>
```

Rules:

- Context Output is a candidate for the next Context Input, not an append-only transcript.
- Do not replace evidence with model confidence or self-assertions such as `verified` without a source.
- Do not auto-promote Context Output into memory, belief, Skill, rule, or team asset.
- Existing capability/domain output contracts remain authoritative where they apply.

## CONTRACT AMENDMENT REQUEST

Use only when one of the five Task Contract fields must change:

```yaml
contract_amendment_request:
  observed_conflict: <what new evidence makes the current Contract wrong or unsatisfiable>
  contract_field_affected: <goal | scope | must_not | done_when | authority>
  evidence_ref: <reopenable source>
  proposed_change: <minimum change>
  impact: <what must be re-verified or reconsidered>
  human_decision_needed: <bounded approval question>
```

Never silently drift the Contract.
