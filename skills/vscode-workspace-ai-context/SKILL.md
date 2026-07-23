---
name: vscode-workspace-ai-context
description: "Guide, audit, and improve VS Code, Copilot, Codex, Claude Code, Agent Host, and Cowork configuration from current official evidence. Use for configuration file input, AGENTS.md, CLAUDE.md, runtime config, skills, hooks, MCP/tools, context compaction, output compression, prompt caching, resume/fork/subagents, worktrees, prompt or harness engineering, model defaults, shared versus tool-specific configuration, token cost, and Unknown Configuration Setting diagnostics; output AI_CONFIG_AUDIT_V1 findings, PRE_COMPACT_CHECKPOINT_V1 guidance, bounded patches, and validation that preserves behavior, security, exact task state, public/private boundaries, and quality-adjusted token ROI. Do not use for product code, private content in public Lattice, unsupported settings without extension evidence, assumed cross-product cache semantics, stale model rankings, or unapproved user-home edits."
---

# VS Code Workspace AI Context

## Goal

Configure and audit repository AI surfaces so each coding harness receives the smallest correct stable prefix, relevant dynamic context, bounded tools, safe permissions, and a deliberate session lifecycle.

Optimize accepted work per total model cost and human correction time. Do not optimize cache hits or token count by sacrificing exact state, validation evidence, safety, or task correctness.

Keep this skill public and generic. Do not include private downstream policy, credentials, personal machine paths, or product-specific content beyond user-supplied examples.

## Use When

```text
VS Code workspace and Copilot configuration
Codex config AGENTS sandbox approvals tools or thread lifecycle
Claude Code settings CLAUDE rules permissions hooks compact or resume
Agent Host session ownership client tools worktrees or parallel agents
Cowork workspace mounts permissions and boundary with Claude Code
prompt caching lifetime prefix divergence or cache measurement
manual or automatic context compaction and tool-output compression
continue versus compact versus fork versus subagent versus new session
shared project rules versus runtime-specific adapter configuration
prompt and harness engineering for repository-native coding agents
```

## Do Not Use When

```text
product runtime implementation is requested
private downstream content would enter public Lattice
exact user-home edits are claimed without reading the source
an extension-contributed setting is rejected without extension evidence
direct API cache lifetime is assumed to equal IDE or subscription behavior
session persistence is treated as proof that prompt cache still exists
a visual compact chat layout is confused with context compaction
a public benchmark is treated as repository-specific model proof
search watcher or context excludes are treated as access control
```

## Inputs

```text
*.code-workspace and .vscode/settings.json
AGENTS.md AGENTS.override.md CLAUDE.md and runtime-scoped instruction files
.github instructions prompts agents skills and hooks
.codex/config.toml plus supplied user-level excerpts
.claude/settings.json settings.local.json rules hooks and commands
.mcp.json .vscode/mcp.json tool and skill registries
Agent Debug Logs Cache Explorer context meters and usage reports
session resume fork subagent worktree and Agent Host metadata
Cowork selected folders mount permissions and task artifacts
representative tasks validation results tokens credits latency and correction time
current official VS Code GitHub OpenAI and Anthropic documentation
```

## Outputs

```text
AI_CONFIG_AUDIT_V1 report
PRE_COMPACT_CHECKPOINT_V1 artifact or generation guidance
shared-kernel versus runtime-adapter decision
continue compact fork subagent or new-session recommendation
cache lifecycle and first-divergence analysis
configuration and instruction patches
permission sandbox worktree and tool-scope report
model and reasoning routing recommendation with current-source caveat
validation commands unresolved assumptions and evidence gaps
```

`AI_CONFIG_AUDIT_V1`:

```text
schema root summary surfaces findings
finding = id severity surface path message evidence recommendation confidence
severity = error | warning | info
```

`PRE_COMPACT_CHECKPOINT_V1` must preserve exact task state outside conversational history. Use `schemas/pre-compact-checkpoint.v1.schema.json`.

## Context Model

Use four layers:

```text
L0 stable kernel    = security privacy project identity authority routing
L1 workspace profile = architecture map commands constraints capability catalog
L2 task profile     = selected tools skills MCP model effort scope and acceptance tests
L3 dynamic suffix   = request files diffs logs tool results failures and current decisions
```

Keep L0 and the stable part of L1 deterministic. Load L2 only for the task. Keep volatile evidence in L3 or external artifacts.

Distinguish five mechanisms:

```text
visual compact layout       = UI only
context compaction          = lossy replacement of older conversation history
output compression          = reduction of large tool results
prompt caching              = provider reuse of an unchanged request prefix
external checkpoint         = durable exact state used to survive compact fork or restart
```

## Workflow

1. Query_ConPort_MCP_before_loading_or_searching_full_skill_text when available; otherwise inspect only targeted configuration and instruction files before broad repository search.
2. Inventory each harness separately: VS Code/Copilot, Codex, Claude Code, Agent Host, and Cowork when used. Record user, workspace, project, organization, and managed-policy precedence.
3. Run `scripts/audit_ai_workspace_config.py`. Treat findings as deterministic first-pass evidence, not a complete schema or runtime validator.
4. Verify fast-moving keys, defaults, release status, model availability, billing, cache behavior, compact behavior, fork semantics, and permission rules against current official sources. Record the date and product surface.
5. Map the effective prompt in order: platform prefix, organization rules, repository rules, runtime adapter, selected tools and schemas, conversation history, dynamic task evidence. Use Agent Debug Logs or equivalent when available.
6. Identify the first unstable prefix segment. Audit duplicate rules, imports, absolute paths, dates, changing tool catalogs, MCP sprawl, model changes, effort changes, temporal context, parent customizations, and client-contributed Agent Host tools.
7. Evaluate cache lifecycle separately from session lifecycle. Do not infer cache validity from an open, resumed, or remotely hosted session.
8. Choose session action mechanically:
   - continue when task and evidence remain coherent and cache is useful;
   - compact at a verified phase boundary after external checkpointing;
   - fork for a bounded alternative that genuinely needs shared history;
   - use a subagent for isolated research or verification whose full trace is not needed by the parent;
   - start new for unrelated work, polluted history, stale cache, or a different tool/model profile.
9. Before lossy compaction, create or update `PRE_COMPACT_CHECKPOINT_V1` with objective, scope, constraints, decisions, worktree and branch, changed files, validation, failures, open items, next actions, approvals, and source references.
10. Compare one shared semantic kernel with separate runtime adapters. Share project facts and validation contracts; keep settings, permissions, hooks, models, compact commands, tool profiles, and session mechanics runtime-specific.
11. Audit parallelism. Count total active contexts, future fork cost, subagent fanout, duplicated tool prefixes, shared-worktree conflicts, and merge/reconciliation cost. Wall-clock reduction alone is not efficiency.
12. Apply the smallest supported patch. Preserve user intent, behavior, organization policy, security, worktree isolation, public/private boundaries, and exact task evidence.
13. Validate syntax, effective settings, skill discovery, hook behavior, runtime diagnostics, checkpoint schema, targeted repository tasks, cache metrics, and total quality-adjusted cost.

## Compact Policy

Compact deliberately, not on a fixed message count.

Good triggers:

```text
accepted phase complete and exact checkpoint exists
context window is near automatic compaction
large obsolete exploration or tool output dominates context
provider cache is already cold or the prefix must change
switch from investigation to implementation after decisions are frozen
resume after a long inactivity period with verified task state
```

Delay compact when:

```text
cache hit remains high and history is relevant
unresolved evidence is distributed across prior messages
exact commands diffs test failures or approvals are not checkpointed
summary quality cannot be verified against repository state
a fork or subagent would isolate the branch more safely
```

After compact, re-anchor from the checkpoint and repository state. Do not trust the summary as the sole source of truth.

## Fork and Parallel Session Policy

A fork can reuse history and may preserve a warm prefix for the next request, but it duplicates future context and tool cost when both branches continue.

Prefer a checkpointed fork at the decision boundary instead of forking an entire noisy session. Assign one hypothesis or deliverable per branch. Verify whether branches share a worktree; use isolated worktrees for concurrent edits. Reconcile through explicit artifacts, tests, and diffs rather than copying full transcripts.

Use subagents instead of forks when the parent needs only a bounded result. Limit concurrency unless independent workstreams produce measurable net gain after reconciliation cost.

## Shared Versus Runtime-Specific Configuration

Share:

```text
project identity and architecture map
source-of-truth locations and authority order
security privacy and IP constraints
canonical build test lint and validation commands
public API and compatibility rules
output and completion contract
stable capability catalog metadata
```

Keep separate:

```text
VS Code discovery settings Agent Host toggles UI and debug settings
Copilot path instructions prompts custom agents hooks and model routing
Codex sandbox approvals MCP profiles model effort and AGENTS overrides
Claude permissions hooks rules commands model effort compact and resume behavior
Cowork folder mounts write/delete permissions and knowledge-work artifacts
provider credentials entitlements pricing and personal preferences
```

AGENTS.md may be the canonical shared semantic map. CLAUDE.md may import it and add Claude-only deltas, but disable redundant VS Code loading when that would inject the same rules twice. Copilot path instructions, Codex nested AGENTS.md, and Claude path rules should express scoped deltas, not full copies.

## Prompt and Harness Engineering

Prefer repository legibility over increasingly long prompts:

```text
short architecture map and source-of-truth pointers
deterministic commands and narrow acceptance tests
progressive disclosure through skills and routed references
structured task plans and checkpoints committed or stored outside chat
small stable tool profiles instead of global MCP exposure
worktree isolation for parallel edits
machine-readable logs and evals rather than transcript memory
```

Prompt engineering defines the request and constraints. Harness engineering defines what context, tools, permissions, execution loop, state, validation, and recovery the model receives. Audit both.

## Rules

```text
VSAI.001 | MUST   | settings | use supported settings or identify the extension that contributes them
VSAI.002 | MUST   | verify   | verify fast-moving settings models compact cache and fork claims from current official sources
VSAI.003 | MUST   | runtime  | audit each harness as a separate configuration and session surface
VSAI.004 | MUST   | evidence | attach file evidence confidence product surface and verification status to each finding
VSAI.005 | MUST   | compact  | checkpoint exact task state before intentional lossy compaction
VSAI.006 | MUST   | cache    | distinguish prompt cache lifetime from chat session persistence
VSAI.007 | MUST   | fork     | account for duplicated future cost and worktree isolation before recommending a fork
VSAI.008 | MUST   | skills   | configure nondefault skill folders through documented discovery settings
VSAI.009 | MUST   | boundary | keep private context credentials personal paths and user preferences out of public Lattice
VSAI.010 | MUST   | safety   | flag unrestricted sandbox permissions network tools destructive actions and literal secrets
VSAI.011 | SHOULD | context  | keep one shared stable semantic kernel plus small runtime-specific adapters
VSAI.012 | SHOULD | routing  | use path task and capability scoped instructions skills prompts hooks and agents
VSAI.013 | SHOULD | cache    | keep stable prefix order tool profile model and effort fixed within one task session
VSAI.014 | SHOULD | compact  | compact at verified phase boundaries rather than by arbitrary message count
VSAI.015 | SHOULD | output   | compress large tool output only when required evidence remains recoverable
VSAI.016 | SHOULD | agent    | use subagents for isolated evidence and forks for bounded alternative continuations
VSAI.017 | SHOULD | host     | verify Agent Host ownership client tool availability persistence and worktree semantics
VSAI.018 | SHOULD | cowork   | treat Cowork as a separate workspace and permission harness from Claude Code
VSAI.019 | SHOULD | model    | select models and reasoning from current availability price and frozen repository evals
VSAI.020 | SHOULD | metric   | optimize accepted delivery per total tokens credits latency reconciliation and human correction
VSAI.021 | NEVER  | cache    | transfer direct API cache lifetime or pricing assumptions to another product without evidence
VSAI.022 | NEVER  | compact  | treat a compact summary as the sole source of exact repository state
VSAI.023 | NEVER  | host     | assume Agent Host makes Copilot Codex and Claude behavior identical
VSAI.024 | NEVER  | custom   | claim arbitrary custom settings are enforced without extension evidence
VSAI.025 | NEVER  | security | treat search watcher context or compact controls as authorization boundaries
VSAI.026 | NEVER  | model    | publish a permanent best-model ranking from stale names prices or benchmarks
VSAI.027 | NEVER  | write    | overwrite user-home configuration without explicit source and approval
```

## References

- Read `references/context-cache-session-lifecycle.md` for compaction, cache lifetime, fork, Agent Host, Cowork, checkpoint, and harness decisions.
- Read `references/shared-vs-runtime-config.md` before choosing canonical shared rules and tool-specific adapters.
- Read `references/vendor-config-surfaces.md` before auditing exact keys, precedence, models, billing, or product behavior.
- Use `schemas/pre-compact-checkpoint.v1.schema.json` for durable pre-compaction state.
- Consult current official VS Code, GitHub, OpenAI, and Anthropic sources whenever fast-moving facts matter.

## Scripts

```bash
python3 skills/vscode-workspace-ai-context/scripts/audit_ai_workspace_config.py --root . --format markdown
python3 skills/vscode-workspace-ai-context/scripts/audit_ai_workspace_config.py --root . --format json --strict
```

The auditor checks high-confidence syntax, paths, instruction duplication, unstable prefix content, compaction support, checkpoint gaps, permissions, sandbox, secrets, discovery, MCP fanout, model pinning, and token-risk patterns. It does not observe live cache hits, validate every extension key, prove compact summary quality, or replace organization policy and current vendor documentation.

## Verification

```bash
python3 -m unittest discover -s skills/vscode-workspace-ai-context/evals -p 'test_*.py' -v
python3 scripts/validate_skill_package.py --root skills/vscode-workspace-ai-context
python3 skills/vscode-workspace-ai-context/scripts/audit_ai_workspace_config.py --root . --format json
python3 -m json.tool skills/vscode-workspace-ai-context/schemas/pre-compact-checkpoint.v1.schema.json >/dev/null
python3 -m json.tool skills/vscode-workspace-ai-context/evals/trigger_queries.json >/dev/null
python3 -m json.tool skills/vscode-workspace-ai-context/evals/output_cases.json >/dev/null
git diff --check
```

Also verify:

```text
no unintended Unknown Configuration Setting diagnostics
effective instructions match the intended shared and adapter design
first prompt-cache divergence is understood or measured
checkpoint rehydrates objective decisions changes tests failures and approvals
compact summary agrees with repository state and checkpoint
forks and concurrent agents use intended worktree isolation
project-local Codex keys are active rather than silently ignored
Claude permission and hook precedence matches the effective settings view
Cowork mounts and delete/write boundaries match the task
skills prompts agents hooks and MCP paths resolve
recommendations distinguish verified fact local inference and engineering choice
```

## Failure Modes

```text
ui-compact-confusion: compact chat layout is mistaken for context compaction
premature-compaction: useful warm coherent history is summarized before a checkpoint
summary-loss: decisions failures commands approvals or file state disappear after compaction
compact-cargo-cult: compaction is triggered by message count without lifecycle evidence
session-cache-conflation: an open resumed or hosted session is assumed to retain provider cache
cache-lifecycle-transfer: direct API TTL or pricing is copied to an IDE harness without proof
prefix-churn: models effort tools instructions or volatile data change inside one task session
fork-fanout: multiple branches duplicate future context with no bounded independent outcome
shared-worktree-divergence: parallel sessions edit one worktree and corrupt attribution
subagent-sprawl: isolated contexts cost more to reconcile than the work they save
agent-host-equivalence: shared hosting is treated as identical runtime semantics
client-tool-drift: Agent Host prompt changes as connected clients contribute or remove tools
cowork-cross-surface: Cowork mounts or permissions are treated as Claude Code settings
instruction-double-load: shared rules enter context directly and through an adapter import
runtime-copy-sprawl: complete shared rules are copied into every tool-specific file
unknown-setting: native support or extension contribution is unverified
ignored-project-key: a runtime silently ignores a project-local key
permission-bypass: sandbox approvals or tool rules exceed task need
secret-literal: committed configuration contains token key credential or password values
model-staleness: renamed unavailable preview or repriced model is recommended as current
benchmark-transfer: public benchmark is treated as repository-specific proof
false-security: context reduction settings are presented as authorization controls
script-overclaim: deterministic heuristic output is presented as full runtime validation
```
