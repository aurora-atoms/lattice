# Repository AI Guidance

This file is a small cross-runtime map, not a replacement for the native GitHub Copilot, VS Code, Codex, Claude, or other agent harnesses.

## Native-First Operation

1. Use the active runtime's built-in agent loop, Skill discovery, context management, permissions, sandbox, and tool selection first.
2. Let the runtime match task intent against Skill `name` and `description`; do not run a repository router before every normal task.
3. Load progressively:

```text
Skill metadata -> selected SKILL.md -> named references or scripts -> bounded task evidence
```

4. Use native custom agents, subagents or forked Skill contexts, handoffs, worktrees, and hooks when the runtime supports them and the task justifies them.
5. Select the smallest sufficient capability. Add another capability only for a required dependency, independent check, or lifecycle gate.
6. Keep context packs bounded to scope, files and line ranges, symbols, tests, risks, decisions, validation commands, evidence refs, and permission boundaries.
7. Preserve human authority for scope, security, compliance, architecture, merge, release, deployment, and production decisions.
8. Stop when the requested visible result is reached.

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
- Distinguish facts, inferences, conflicts, and unknowns.
- Do not load the full Skill, Agent, tool, knowledge, log, or repository catalog by default.
- Do not use routing, token, or agent activity for personnel ranking.
- Do not supersede Helixion, AegisFlow, Memexa, FlowGuard, OpenClaw, DeliveryYield, or another active module without explicit instruction.
