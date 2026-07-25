---
name: capability-harness-engineer
description: Use for designing, auditing, or evolving a native-first capability harness across VS Code GitHub Copilot Codex and other agent runtimes while preserving behavior, progressive disclosure, permissions, evidence, and quality-adjusted token ROI. Prefer built-in Skill discovery, custom agents, subagents or forked contexts, handoffs, hooks, worktrees, sandboxing, and runtime context management before repository scripts. Use the deterministic route registry and scripts only as evaluation oracles, compatibility fallbacks, and regression tools. Do not use to perform the routed domain task, approve high-impact actions, replace accountable owners, force a repository router before every prompt, or copy changing vendor internals into static instructions.
---

# Capability Harness Engineer

## Goal

Improve how native agent runtimes discover, select, compose, and validate repository capabilities without rebuilding their evolving internal orchestrators.

Keep harness engineering separate from task execution. Use this Skill to improve the harness; let the active runtime and selected delivery capabilities perform the task.

## Use When

Use for native Skill-selection quality, advanced context engineering, progressive disclosure, custom-agent and subagent design, handoffs, hooks, permissions, prompt caching, context projection, runtime adapters, route evaluations, compatibility fallbacks, and bounded rollout decisions.

## Do Not Use When

Do not use to solve the routed task directly, approve merge or release decisions, grant tools or permissions, execute production changes, rank personnel, or make every task pass through a repository script. Do not freeze vendor-specific implementation details into the stable kernel.

## Inputs

Use current official runtime documentation, runtime version and policy, Skill descriptions, custom-agent contracts, task examples, observed native selections, lifecycle stages, side effects, permissions, token and context evidence, and positive, negative, ambiguous, multilingual, and high-risk evaluation cases.

## Outputs

Produce:

```text
native capability map
thin stable repository kernel
Skill metadata improvements
custom-agent or handoff design when justified
runtime adapter boundary
expected-route evaluation oracle
routing regression cases
context-load plan
permission and stop policy
validation evidence
bounded rollout recommendation
```

## Native-First Decision Order

```text
N0 stable built-in runtime behavior
N1 stable native setting or customization
N2 native Preview or Experimental capability after verification
N3 first-party provider integration exposed by the runtime
N4 official provider extension or CLI for a documented gap
N5 third-party extension or MCP
N6 repository routing script or external orchestrator
```

Move down only when the higher level cannot meet a documented requirement.

## Workflow

1. Verify current runtime capabilities from official sources before changing shared policy.
2. Inventory the active runtime's Skill discovery, custom agents, subagents or forked contexts, handoffs, hooks, permissions, sandbox, worktrees, context compaction, and debugging surfaces.
3. Treat the native runtime as the execution plane and Lattice registries, evals, validators, and evidence as the governance plane.
4. Keep `AGENTS.md` or equivalent shared guidance short and invariant; do not put the complete route table or vendor state machine there.
5. Improve Skill names and descriptions first so native discovery can select the smallest sufficient capability.
6. Use native custom agents for bounded roles, native delegation for multi-role work, handoffs for human-reviewed stage transitions, and hooks or CI for deterministic enforcement.
7. Apply progressive disclosure: metadata, selected `SKILL.md`, named resources, then bounded task evidence.
8. Keep provider-specific permissions, models, tools, hooks, and session behavior in thin runtime adapters rather than the shared kernel.
9. Use `registry/capability-routing.index.jsonl` and `scripts/route_capabilities.py` as an expected-route oracle, regression evaluator, debugging aid, or fallback for runtimes without native Skill discovery.
10. Compare expected and actual native selections; classify correct, false positive, false negative, ambiguous, unnecessary composition, and context-overload outcomes.
11. Add deterministic validation and representative regression cases before broadening automation.
12. Remove custom machinery when a stable native capability replaces it without weakening governance or evidence.

## Rules

CHE.001 | MUST | boundary | keep harness engineering separate from routed domain execution
CHE.002 | MUST | native | use the active runtime's maintained harness before bespoke orchestration
CHE.003 | MUST | routing | select the smallest sufficient capability before composing a chain
CHE.004 | MUST | context | apply progressive disclosure from metadata to body to resources to bounded evidence
CHE.005 | MUST | control | preserve human authority for scope security compliance architecture merge release and production
CHE.006 | MUST | evidence | compare expected and actual selection with observable evidence
CHE.007 | MUST | fallback | keep deterministic routing as an oracle fallback or compatibility layer rather than mandatory preflight
CHE.008 | MUST | token | optimize quality-adjusted output per token cost
CHE.009 | SHOULD | prompt | keep invariant policy stable and task material dynamic
CHE.010 | SHOULD | runtime | use native custom agents delegation handoffs hooks permissions worktrees and debugging surfaces
CHE.011 | SHOULD | eval | test positive negative ambiguous multilingual and high-risk cases
CHE.012 | NEVER | catalog | load all Skill bodies or references by default
CHE.013 | NEVER | authority | treat native or fallback routing as approval for a high-impact action
CHE.014 | NEVER | vendor | copy unstable vendor internals into the shared kernel as permanent truth
CHE.015 | NEVER | modules | supersede Helixion AegisFlow Memexa FlowGuard OpenClaw DeliveryYield or another active module
CHE.016 | NEVER | telemetry | rank or monitor people from routing token or agent-activity data

## References

The hard native-first, authority, context, fallback, and evaluation rules are defined above. Read current official runtime documentation at execution time before making claims about changing built-in behavior. Use `registry/capability-routing.index.jsonl` only for expected-route policy and `scripts/route_capabilities.py` only for regression, diagnosis, compatibility, or fallback routing.

## Verification

Run:

```bash
python scripts/validate_skill_package.py --root skills/capability-harness-engineer
python scripts/validate_capability_routing.py --root .
python -m unittest discover -s tests -p 'test_route_capabilities.py' -v
```

Verify that normal tasks can use native Skill discovery without mandatory script pre-routing; the fallback still produces deterministic expected routes; ambiguous or side-effectful cases remain advisory; and high-impact authority remains human-controlled.

## Failure Modes

- Reimplementing the vendor's agent loop with a weaker static keyword router.
- Requiring a routing command before every ordinary task.
- Loading every Skill description, body, reference, tool, and repository file into each request.
- Using semantic similarity without lifecycle, risk, permission, or ambiguity controls.
- Treating a custom agent recommendation as approval.
- Failing to revisit custom mechanisms after native capabilities improve.
- Calling the harness complete without observed native-selection evals and recovery paths.
