# Shared Configuration vs Runtime-Specific Configuration

Last source verification: 2026-07-23.

## Decision rule

Share semantics; separate mechanics.

```text
shared layer owns:
project facts architecture vocabulary commands constraints acceptance criteria

runtime layer owns:
discovery settings models effort tools MCP permissions sandbox hooks compact and session behavior
```

## Shared semantic kernel

Use a compact `AGENTS.md` as the canonical vendor-neutral map when Codex and VS Code are targets.

Share:

```text
repository purpose and source-of-truth map
supported environment and deployment boundaries
architecture and dependency invariants
safe local actions and approval boundaries
build lint test and validation commands
completion report contract
links to task-scoped skills and references
```

Do not share:

```text
personal model or provider choice
credentials and machine paths
current issue branch or transient status
runtime permission syntax
large examples raw logs prices or fast-changing model names
```

## Runtime adapters

### VS Code and Copilot

Owns instruction, prompt, agent, skill, hook, and MCP discovery; Agent Host behavior; debug logs and Cache Explorer; automatic conversation compaction; tool-output compression; temporal context; model selection; fork and worktree UI.

Use `.github/instructions/*.instructions.md` for path-scoped deltas and `.github/prompts/*.prompt.md` for repeatable task suffixes.

### Codex

Owns `.codex/config.toml`, user provider/profile configuration, AGENTS discovery, sandbox, approvals, network, MCP profiles, model effort, subagents, and Codex thread/worktree behavior.

Keep provider, authentication, telemetry, and personal model preferences out of the project file when the documented precedence requires user configuration.

### Claude Code

Owns `CLAUDE.md`, `.claude/rules`, `.claude/settings.json`, local settings, permissions, hooks, commands, model effort, `/compact`, resume, and provider mapping.

A minimal `CLAUDE.md` may import `AGENTS.md` and add only Claude-specific deltas. When VS Code loads both files, prevent duplicate injection.

### Cowork

Owns mounted folders, read/write/delete mode, connectors, desktop application access, VM containment, and enterprise audit controls. Treat it as a separate harness from Claude Code.

## Recommended layout

```text
AGENTS.md                                  canonical shared map
CLAUDE.md                                  @AGENTS.md plus Claude deltas
.github/instructions/*.instructions.md     Copilot path deltas
.github/prompts/*.prompt.md                 reusable task suffixes
.github/hooks/*.json                        reviewed VS Code lifecycle hooks
.claude/rules/*.md                          Claude path deltas
.claude/settings.json                       shared Claude mechanics
.codex/config.toml                          shared Codex mechanics
skills/*/SKILL.md                           progressive task workflows
schemas/pre-compact-checkpoint.v1.schema.json
```

## VS Code cache-sensitive baseline

Verify each key and Preview/Experimental status against the installed release before applying.

```jsonc
{
  "github.copilot.chat.summarizeAgentConversationHistory.enabled": true,
  "chat.tools.compressOutput.enabled": true,
  "chat.includeReferencedInstructions": false,
  "chat.mcp.discovery.enabled": false,
  "github.copilot.chat.editor.temporalContext.enabled": false,
  "chat.useCustomizationsInParentRepositories": false,
  "chat.useAgentsMdFile": true,
  "chat.useClaudeMdFile": false,
  "chat.includeApplyingInstructions": true,
  "chat.agentSkillsLocations": {"skills": true},
  "chat.instructionsFilesLocations": {
    ".github/instructions": true,
    ".claude/rules": false
  },
  "chat.promptFilesLocations": {".github/prompts": true}
}
```

Automatic compaction protects the context budget but is lossy. Tool-output compression should be validated against required terminal and diff evidence. Temporal context and parent customizations improve convenience but can make prompt assembly less reproducible and reduce cache stability.

Agent Debug Logs and Cache Explorer are diagnostic tools and may contain sensitive prompt, file, and tool data. Enable temporarily and protect exported data.

Agent Host is an architecture and rollout capability. Do not invent or persist undocumented settings; verify the current VS Code release and organization policy.

UI compact layout settings affect presentation only and do not compact model context.

## Anti-patterns

```text
three complete copies of the same rules
one giant AGENTS.md containing architecture history
project files pinning personal providers credentials or models
changing model effort tools or MCP every turn
forks used as permanent parallel work in one worktree
assuming session persistence means cache persistence
compacting without an exact checkpoint
exposing every available tool to improve capability
using cache hit rate as the only metric
```
