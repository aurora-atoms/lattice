# Repository AI Guidance

This file is a small cross-runtime map, not a replacement for the native GitHub Copilot, VS Code, Codex, Claude, or other agent harnesses.

## Native-First Operation

1. Use the active runtime's built-in agent loop, Skill discovery, context management, permissions, sandbox, and tool selection first.
2. Let the runtime match task intent against Skill `name` and `description`; do not run a repository router before every normal task.
3. When compact capability metadata is useful, consult `registry/skill-context.catalog.json` or `registry/agent-context.catalog.json` before loading a Skill or Agent body. Use its stable ID/version, intended change, users, trigger, minimum inputs, outputs, and optional-context guidance.
4. Load progressively:

```text
native name + description
-> compact capability context
-> selected SKILL.md or Agent instruction
-> named references or scripts
-> bounded task evidence
-> optional related capability or source only for a named quality gap
```

5. Use native custom agents, subagents or forked Skill contexts, handoffs, worktrees, and hooks when the runtime supports them and the task justifies them.
6. Select the smallest sufficient capability. Add another capability only for a required dependency, independent check, lifecycle gate, or explicit optional-context gap.
7. Keep context packs bounded to scope, files and line ranges, symbols, tests, risks, decisions, validation commands, evidence refs, and permission boundaries.
8. Optional context is advisory discovery guidance. It does not grant tools, permissions, network access, repository writes, or approval authority.
9. Preserve human authority for scope, security, compliance, architecture, merge, release, deployment, and production decisions.

## Required Run Result

Every selected Skill or Agent must produce a visible structured result conforming to `schemas/capability/capability-run-result.v1.schema.json`.

Default writeback:

```text
artifacts/capability-runs/<capability-name>/<run-id>/run-result.json
```

When write permission is unavailable, return the complete result inline and record that it was not written.

The result must separate facts, inference, citations, uncertainty, unknowns, and assumptions; evaluate success signals; and state the stop reason, retry count, permission gap, and next step.

## Stop and Retry

Stop when the requested goal or next reviewable stage is reached. Unless the user explicitly requests end-to-end continuation, pause for review before proceeding to the next stage.

Stop without repeated probing when required input, permission, source access, internet access, or sufficient evidence is unavailable; when validation remains failed after the bounded retry; or when a security, privacy, compliance, data-governance, architecture, production, or other high-risk boundary is reached.

For a permission stop, identify the exact permission, accountable owner, reason, and resumable next step. Never attempt bypasses. Default to one bounded retry after the initial attempt unless the user or selected capability explicitly authorizes a different deterministic retry policy.

## Compatibility

Capability identity uses `skill:<name>@<semver>` or `agent:<name>@<semver>`. Treat changes to required inputs, permissions, outputs, evidence, success signals, stop behavior, authority boundaries, or behavior semantics as compatibility decisions under `docs/capability-context-contract.md`.

## Fallback and Evaluation

Use `scripts/route_capabilities.py` only when:

- the runtime lacks native Skill discovery;
- native selection is ambiguous or appears wrong;
- an expected route is needed for CI or regression evaluation;
- comparing actual native selection against repository policy;
- explicitly debugging routing behavior.

The fallback routing policy lives in `registry/capability-routing.index.jsonl`. It is an evaluation oracle and compatibility layer, not a mandatory preflight for every prompt.

## Stable Boundaries

- Feature Delivery Case is the primary user-value and evidence boundary.
- Distinguish facts, inferences, conflicts, assumptions, uncertainty, and unknowns.
- Do not load the full Skill, Agent, tool, knowledge, log, or repository catalog by default.
- Do not use routing, token, or agent activity for personnel ranking.
- Do not supersede Helixion, AegisFlow, Memexa, FlowGuard, OpenClaw, DeliveryYield, or another active module without explicit instruction.
