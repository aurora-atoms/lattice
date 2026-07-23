---
name: vscode-workspace-ai-context
description: "Guide, audit, and improve VS Code AI configuration with a native-first policy. Use for VS Code settings, Chat and Agents Window sessions, Agent Host, local/background/cloud or Claude/Codex agents, AGENTS.md, CLAUDE.md, instructions, prompts, custom agents, skills, hooks, MCP/tools, worktrees, permissions, sandboxing, context compaction, output compression, prompt caching, fork/subagent/session lifecycle, and shared versus runtime-specific configuration; output AI_CONFIG_AUDIT_V1 findings, PRE_COMPACT_CHECKPOINT_V1 guidance, bounded patches, and validation that preserves behavior, security, exact task state, public/private boundaries, and quality-adjusted token ROI. Do not use for product code, private content in public Lattice, unsupported settings without extension evidence, automatic replacement of stable native behavior with plugins, assumed cross-product cache semantics, stale model rankings, or unapproved user-home edits."
---

# VS Code Workspace AI Context

## Goal

Configure and audit AI-assisted development by using the smallest sufficient VS Code-native capability first, then an official provider integration, then an extension, and only then custom scripts or bespoke infrastructure.

Optimize accepted work per total tokens, credits, latency, reconciliation, security exposure, and human correction. Do not maximize cache hits or reduce tokens by weakening validation, exact task state, or safety.

Keep this skill public and generic. Never include credentials, private downstream policy, personal machine paths, or proprietary repository content.

## Use When

```text
VS Code workspace settings and native AI feature review
Chat view versus Agents Window selection
local Agent Plan Ask background Copilot CLI cloud Claude or Codex session choice
Agent Host worktree handoff fork subagent compact or session lifecycle
instructions prompts agents skills hooks MCP and tool routing
Codex and Claude provider-specific configuration after native capability review
prompt caching context management output compression and token cost
shared project rules versus runtime-specific adapters
Unknown Configuration Setting and extension-contributed setting diagnostics
```

## Do Not Use When

```text
product runtime implementation is requested
private downstream content would enter public Lattice
exact user-home edits are claimed without reading the source
an extension setting is rejected without checking its manifest
a native Preview feature is treated as stable without verification
a provider API cache lifetime is assumed to equal a VS Code product surface
session persistence is treated as proof that prompt cache still exists
search excludes compact settings or worktrees are treated as authorization
```

## Inputs

```text
VS Code version channel and organization policy
*.code-workspace and .vscode/settings.json
installed extension list and extension configuration manifests
AGENTS.md CLAUDE.md and scoped instruction files
.github prompts agents skills hooks and workflow files
.codex/config.toml and .claude/settings files when provider harnesses are used
.mcp.json .vscode/mcp.json and active tool picker state
Agent Debug Logs Cache Explorer usage and context-window reports
session type model permission worktree fork and handoff metadata
representative tasks tests tokens credits latency and correction time
current official VS Code GitHub OpenAI and Anthropic documentation
```

## Outputs

```text
AI_CONFIG_AUDIT_V1 report
native-capability replacement or retention decision
minimal settings patch with defaults omitted where possible
PRE_COMPACT_CHECKPOINT_V1 artifact or guidance
continue compact fork subagent handoff or new-session recommendation
shared-kernel versus runtime-adapter decision
cache first-divergence and context-lifecycle analysis
permission sandbox tool MCP worktree and extension-risk report
validation commands and unresolved evidence gaps
```

`AI_CONFIG_AUDIT_V1`:

```text
schema root summary surfaces findings
finding = id severity surface path message evidence recommendation confidence
severity = error | warning | info
```

Use `schemas/pre-compact-checkpoint.v1.schema.json` before intentional lossy compaction in long-running work.

## Native-First Decision Order

Apply this order for every requested capability:

```text
N0 existing stable VS Code default or built-in feature
N1 stable VS Code setting or built-in customization
N2 VS Code-native Preview or Experimental feature after explicit validation
N3 first-party provider integration exposed through VS Code
N4 official provider extension or CLI for a capability missing from VS Code
N5 third-party extension or MCP server
N6 repository script hook or external service
```

Do not move down the list merely because a lower-level option has more settings. Move down only when the higher level cannot meet a documented requirement.

Prefer omission over restating a native default. Commit a setting when it enforces a deliberate team policy, changes a default, fixes discovery, or provides reproducibility. Keep user preferences, credentials, provider accounts, and personal model choices out of shared workspace configuration.

## Native Capability Map

Use VS Code-native features before recreating them:

```text
interactive coding             -> Chat view with Agent Plan or Ask
multi-project orchestration     -> Agents Window
background local execution      -> Copilot CLI session
team or PR collaboration        -> cloud agent session
provider-specific harness       -> native Claude or Codex session when available
parallel edit isolation         -> New Worktree and Git worktree controls
alternative continuation        -> /fork or checkpoint fork
context reduction               -> automatic compaction or /compact
large terminal output reduction -> chat.tools.compressOutput.enabled after validation
cache diagnosis                 -> Agent Debug Logs and Cache Explorer
specialized workflow            -> Agent Skill
project-wide rules              -> one concise instruction source
file or folder rules            -> scoped .instructions.md or runtime-native rules
repeatable user command         -> prompt file
bounded role and tool set       -> custom agent
lifecycle enforcement           -> native hooks then CI for authoritative enforcement
external systems                -> MCP only when built-in tools or CLI are insufficient
security                         -> Workspace Trust permissions sandbox trusted domains and MCP trust
code understanding              -> language services IntelliSense tests debugger tasks SCM and search
```

Do not install a separate extension to obtain functionality already provided by the active VS Code version unless the extension supplies a verified missing capability or materially better repository results.

## Context Model

```text
L0 stable kernel      = security privacy project identity authority and output contract
L1 workspace profile = architecture map canonical commands and capability catalog
L2 task profile       = selected session type model tools skills MCP scope and tests
L3 dynamic suffix     = request files diffs logs failures decisions and current evidence
```

Keep L0 and stable L1 deterministic. Load L2 only for the task. Keep volatile information in L3 or durable task artifacts.

Distinguish:

```text
visual compact layout = UI only
context compaction    = lossy replacement of older conversation history
output compression    = filtering of large tool results
prompt caching        = provider reuse of an unchanged request prefix
checkpoint            = durable exact state outside chat history
```

## Workflow

1. Query_ConPort_MCP_before_loading_or_searching_full_skill_text when available; otherwise inspect targeted files before broad search.
2. Record VS Code version, Stable or Insiders channel, enabled organization policies, Workspace Trust, and installed extensions.
3. Inventory the requested capability and check `references/vscode-native-first.md` before recommending any plugin, provider-specific setting, or custom script.
4. Run `scripts/audit_ai_workspace_config.py`. Treat its results as deterministic first-pass evidence, not complete runtime validation.
5. Classify every active configuration item as native stable, native Preview, native Experimental, organization-managed, first-party provider integration, extension-contributed, provider-local, or custom.
6. Remove settings that only repeat defaults unless they intentionally enforce a team policy. Never remove required discovery paths or security controls merely to reduce file size.
7. Prefer built-in session types and handoffs over running multiple overlapping extensions against one worktree.
8. Prefer built-in instructions, prompts, custom agents, skills, hooks, MCP management, worktrees, permissions, sandboxing, Agent Debug Logs, and Cache Explorer over parallel custom mechanisms.
9. Audit the effective prompt order and locate the first cache divergence. Keep model, reasoning, instructions, tool profile, and MCP set stable within one task session.
10. Choose continue, compact, fork, subagent, handoff, background/cloud session, or new session from task boundaries and measured context quality.
11. Before lossy compaction, write `PRE_COMPACT_CHECKPOINT_V1` with objective, scope, decisions, worktree, changed files, validation, failures, approvals, sources, and next actions.
12. Share stable repository semantics across tools. Keep permissions, hooks, models, provider credentials, session mechanics, sandbox, and tool profiles runtime-specific.
13. Add an extension, provider CLI, custom MCP, or script only when the native gap is explicit. Record the gap, lifecycle cost, permissions, update owner, and removal condition.
14. Validate in VS Code Settings UI, effective instruction menus, Agent Debug Logs, Cache Explorer, extension manifests, targeted tests, and CI.

## Settings Policy

Recommended shared workspace settings should be minimal.

Set only when needed:

```text
chat.agentSkillsLocations for nondefault skill folders
chat.instructionsFilesLocations for nondefault instruction folders
chat.promptFilesLocations and chat.agentFilesLocations for nondefault paths
chat.hookFilesLocations for nondefault hook paths
search.exclude or files.exclude for reviewed noisy content
chat.useAgentsMdFile or chat.useClaudeMdFile to avoid duplicate loading
chat.useCustomizationsInParentRepositories for intentional monorepo inheritance
chat.tools.compressOutput.enabled after evidence-preservation testing
chat.agent.maxRequests when the repository needs a bounded loop budget
chat.sessionSync.excludeRepositories for sensitive repositories
```

Usually keep native defaults rather than committing them:

```text
chat.agent.enabled
chat.mcp.discovery.enabled=false
chat.permissions.default=default
github.copilot.chat.summarizeAgentConversationHistory.enabled=true
chat.useAgentSkills=true
chat.includeReferencedInstructions=false
chat.agent.sandbox.enabled=true where supported and managed
chat.tools.global.autoApprove=false
chat.tools.terminal.ignoreDefaultAutoApproveRules=false
```

Do not commit organization-managed Agent Host, Claude, Codex, network-filter, or entitlement settings unless the repository is explicitly the policy source and the setting scope supports it.

Use Preview or Experimental settings only with a verification date, owner, measured benefit, rollback path, and expected removal or stabilization review.

## Session and Compact Policy

Continue when one goal, one worktree, and one tool/model profile remain coherent.

Compact when the task continues but obsolete exploration dominates context, automatic compaction is near, the cache is already cold, or an accepted phase is complete and checkpointed. Use native `/compact` or the context control before inventing a summarization script.

Fork when a bounded alternative genuinely needs shared history. A fork copies history and can preserve cache on the next request, but both branches accumulate future context and may share the same worktree. Prefer checkpoint forks and isolated worktrees for divergent edits.

Use subagents or `context: fork` skills for investigations whose intermediate trace should not enter the parent context. Use background or cloud agents for well-defined independent work. Start a new session for unrelated work or a materially different tool/model/security profile.

## Shared Versus Tool-Specific Configuration

Share:

```text
project identity architecture and authority
security privacy IP and compatibility constraints
canonical build test lint and validation commands
public API rules and completion contract
stable capability and source-of-truth metadata
```

Keep separate:

```text
VS Code session type Agent Host Agents Window and discovery settings
Copilot model routing prompts custom agents hooks and native tool profile
Codex sandbox approvals AGENTS overrides MCP provider and reasoning settings
Claude permissions hooks rules commands compact and provider settings
Cowork mounts write delete and knowledge-work boundaries
credentials entitlements pricing and personal preferences
```

Use one canonical shared semantic source where practical. Runtime adapters contain only deltas. Prevent VS Code from loading the same `AGENTS.md` rules directly and again through `CLAUDE.md`.

## Rules

```text
VSAI.001 | MUST   | native   | check current VS Code native capability before adding a plugin or custom mechanism
VSAI.002 | MUST   | settings | use supported settings or identify the extension that contributes them
VSAI.003 | MUST   | verify   | verify lifecycle status defaults compact cache fork and agent claims from current official sources
VSAI.004 | MUST   | evidence | attach file evidence confidence surface and verification status to each finding
VSAI.005 | MUST   | compact  | checkpoint exact task state before intentional lossy compaction
VSAI.006 | MUST   | cache    | distinguish prompt cache lifetime from chat and Agent Host session persistence
VSAI.007 | MUST   | safety   | flag unrestricted approvals sandbox network tools extensions and literal secrets
VSAI.008 | MUST   | boundary | keep private context credentials personal paths and user preferences out of public Lattice
VSAI.009 | SHOULD | defaults | omit settings that only repeat native defaults unless enforcing policy
VSAI.010 | SHOULD | context  | keep one stable semantic kernel plus small runtime-specific adapters
VSAI.011 | SHOULD | routing  | use native scoped instructions prompts agents skills hooks and tool selection
VSAI.012 | SHOULD | session  | use native worktrees forks handoffs background and cloud sessions before custom orchestration
VSAI.013 | SHOULD | cache    | keep prefix order model effort tools and MCP stable within one task session
VSAI.014 | SHOULD | output   | use native output compression only after required evidence remains recoverable
VSAI.015 | SHOULD | metric   | optimize accepted delivery per total cost and human correction rather than raw cache rate
VSAI.016 | NEVER  | plugin   | install or retain an overlapping extension without a documented native gap
VSAI.017 | NEVER  | cache    | transfer direct API cache lifetime or pricing assumptions to a VS Code surface without evidence
VSAI.018 | NEVER  | host     | assume Agent Host makes Copilot Codex and Claude behavior identical
VSAI.019 | NEVER  | security | treat excludes compaction worktrees or sandbox alone as authorization
VSAI.020 | NEVER  | model    | publish a permanent best-model ranking from stale names prices or benchmarks
VSAI.021 | NEVER  | write    | overwrite user-home configuration without explicit source and approval
```

## References

- Read `references/vscode-native-first.md` first for the native capability and settings matrix.
- Read `references/context-cache-session-lifecycle.md` for compaction, cache, fork, Agent Host, Cowork, and checkpoint decisions.
- Read `references/shared-vs-runtime-config.md` for canonical shared rules and provider-specific adapters.
- Read `references/vendor-config-surfaces.md` only when exact provider keys, billing, or behavior matters.
- Use `schemas/pre-compact-checkpoint.v1.schema.json` for durable state.

## Scripts

```bash
python3 skills/vscode-workspace-ai-context/scripts/audit_ai_workspace_config.py --root . --format markdown
python3 skills/vscode-workspace-ai-context/scripts/audit_ai_workspace_config.py --root . --format json --strict
```

The auditor detects high-confidence syntax, path, duplication, native-default overrides, overlapping extension configuration, compaction, checkpoint, permissions, sandbox, secrets, discovery, MCP fanout, model pinning, and token-risk patterns. It does not replace VS Code Settings validation, organization policy, extension manifests, live runtime telemetry, or vendor documentation.

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
native capability was considered before every extension or custom recommendation
workspace settings contain only intentional overrides and discovery paths
effective instructions match the shared-kernel and adapter design
Agent Host and Agents Window support is organization-enabled before relying on it
first cache divergence is measured when Cache Explorer is available
checkpoint rehydrates decisions changes tests failures approvals and next actions
forks and parallel agents use intended worktree isolation
provider-specific configuration remains active and does not duplicate native behavior
no private content secret or personal preference enters shared configuration
```

## Failure Modes

```text
native-bypass: plugin or script is recommended before reviewing built-in capability
settings-cargo-cult: shared settings restate defaults without policy value
preview-as-stable: Preview or Experimental behavior is treated as a durable contract
overlapping-agent-extensions: multiple harnesses edit the same worktree for one task
instruction-double-load: shared rules enter context directly and through an adapter import
premature-compaction: coherent warm context is summarized before exact checkpointing
summary-loss: decisions failures commands approvals or file state disappear after compact
session-cache-conflation: a resumed or hosted session is assumed to retain provider cache
fork-fanout: branches duplicate future context without independent bounded outcomes
shared-worktree-divergence: parallel sessions edit one worktree and corrupt attribution
client-tool-drift: Agent Host prompt changes as connected clients add or remove extension tools
unknown-setting: native support or extension contribution is unverified
ignored-project-key: a provider runtime silently ignores a project-local key
permission-bypass: approvals sandbox or tool rules exceed task need
secret-literal: committed configuration contains credentials
model-staleness: renamed unavailable preview or repriced model is recommended as current
false-security: context or isolation controls are presented as authorization
script-overclaim: deterministic audit is presented as full runtime validation
```
