# Vendor Configuration Surfaces

Last source verification: 2026-07-23.

Use this file as an evidence map, not as a permanent snapshot. Recheck official documentation before emitting exact setting names, model lists, prices, release status, or defaults.

## VS Code and GitHub Copilot

Primary sources:

- https://code.visualstudio.com/docs/agents/reference/ai-settings
- https://code.visualstudio.com/docs/agent-customization/custom-instructions
- https://code.visualstudio.com/docs/agent-customization/agent-skills
- https://code.visualstudio.com/docs/agents/best-practices
- https://docs.github.com/en/copilot/reference/ai-models/supported-models
- https://docs.github.com/en/copilot/reference/ai-models/model-comparison
- https://docs.github.com/en/copilot/tutorials/optimize-ai-usage
- https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing

Verified configuration facts:

```text
AGENTS.md support -> chat.useAgentsMdFile
CLAUDE.md support -> chat.useClaudeMdFile
nested AGENTS.md -> chat.useNestedAgentsMdFiles and experimental status at verification time
path instructions -> chat.instructionsFilesLocations plus applyTo or Claude paths format
skills -> chat.useAgentSkills and chat.agentSkillsLocations
prompts -> chat.promptFilesLocations
custom agents -> chat.agentFilesLocations
MCP discovery -> chat.mcp.discovery.enabled
agent loop budget -> chat.agent.maxRequests
tool output compression -> chat.tools.compressOutput.enabled and preview status at verification time
```

VS Code loads both AGENTS.md and CLAUDE.md when enabled. If CLAUDE.md imports AGENTS.md, the same shared rules can enter VS Code context twice. Audit the actual references shown in a chat response or debug log before claiming duplication in an unusual setup.

Documented default project skill locations include `.github/skills`, `.claude/skills`, and `.agents/skills`. A repository-level `skills/` directory requires an explicit `chat.agentSkillsLocations` entry.

GitHub recommends task-based model selection, lean context, cache preservation, bounded sessions, and cheaper focused subagents. Model availability, prices, plan allowances, release status, and Auto routing behavior change; never copy an old table into permanent rules without a verification date.

## OpenAI Codex

Primary sources:

- https://developers.openai.com/codex/config-reference
- https://developers.openai.com/codex/guides/agents-md
- https://developers.openai.com/api/docs/guides/latest-model

Verified configuration facts:

```text
user config -> ~/.codex/config.toml
trusted project config -> .codex/config.toml
project instructions -> AGENTS.override.md then AGENTS.md then configured fallback names
combined project instruction cap -> project_doc_max_bytes and 32 KiB default at verification time
reasoning values -> minimal low medium high xhigh in Codex config
sandbox values -> read-only workspace-write danger-full-access
approval policy -> untrusted on-request never or granular table
workspace network -> sandbox_workspace_write.network_access
```

Project-local config cannot override provider, authentication, profile, notification, and telemetry-routing keys listed by the current Codex reference. Audit those keys as ignored rather than pretending the project file applies them.

The API model family can support reasoning values or features that the Codex configuration surface does not expose. Audit the Codex reference, not only the API model guide.

## Anthropic Claude Code

Primary sources:

- https://docs.anthropic.com/en/docs/claude-code/settings
- https://docs.anthropic.com/en/docs/claude-code/memory
- https://docs.anthropic.com/en/docs/claude-code/cli-usage

Verified configuration facts:

```text
project shared settings -> .claude/settings.json
project local settings -> .claude/settings.local.json
project memory -> CLAUDE.md
path-scoped rules -> .claude/rules with paths frontmatter
imports -> @path/to/import in CLAUDE.md
persistent effort -> effortLevel with low medium high xhigh
permission mode -> permissions.defaultMode
permission evaluation -> deny then ask then allow
bypass prevention -> disableBypassPermissionsMode
```

At verification time, project settings cannot grant themselves `auto` permission mode. `bypassPermissions` and unrestricted tool allow rules require explicit risk review. Literal API keys, tokens, passwords, and credentials must not be committed in project settings.

## Audit Interpretation

Use three evidence classes:

```text
verified fact -> current official source or parser result
local inference -> repository files plus documented behavior
recommendation -> risk and cost tradeoff requiring user or team choice
```

A public benchmark, vendor model comparison, or price table does not prove the best model for a repository. Freeze representative tasks and compare first-pass test success, regression count, unrelated edits, tool calls, input and cached tokens, output tokens, credits or cost, latency, and human correction time.
