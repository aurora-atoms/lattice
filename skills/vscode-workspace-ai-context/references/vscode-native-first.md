# VS Code Native-First Capability Matrix

Last source verification: 2026-07-23. Recheck current VS Code documentation before treating lifecycle labels, defaults, agent availability, or policy scope as durable.

## Decision Rule

Use the first layer that satisfies the requirement:

```text
stable built-in default
stable built-in setting or customization
native Preview or Experimental feature with rollback
first-party provider session exposed by VS Code
official provider extension or CLI
third-party extension or MCP
repository script hook or external service
```

More configuration is not automatically more control. Lower layers add installation, permissions, update, prompt-prefix, compatibility, and support cost.

## Native Session Surfaces

```text
Chat view       -> code-first work inside the open workspace
Agents Window   -> agent-first orchestration across projects and sessions
local Agent     -> interactive editor-centered coding
Plan            -> research and structured plan before implementation
Ask             -> explanation or investigation without edits
Copilot CLI     -> local background execution and worktree isolation
Copilot Cloud   -> remote GitHub-backed implementation and PR workflow
Claude agent    -> Anthropic harness through VS Code when enabled
Codex agent     -> OpenAI harness through VS Code when enabled
```

Prefer handoff between native session types over restating the full task in a separate extension chat. Verify which session types are enabled by organization policy and which are supported in the current VS Code channel.

## Native Customization Routing

Need | Native mechanism | Avoid by default
---|---|---
Project-wide standards | concise always-on instructions | repeated prompt boilerplate
File or folder standards | scoped `.instructions.md` | one huge global instruction file
Portable multi-step workflow | Agent Skill | always-loading a workflow body
Repeatable explicit command | prompt file | copying prompts from notes
Bounded persona and tools | custom agent | broad global tool access
Lifecycle action | hook | asking the model to remember deterministic enforcement
External API or data | MCP after built-in tool or CLI review | global MCP discovery and overlapping servers
Packaged workflow | agent plugin after component review | installing a bundle without inventorying its contents

VS Code customizations combine. Every added instruction, tool definition, MCP server, hook, plugin, and extension can change effective context, permissions, latency, and cache behavior.

## Native Context and Session Features

```text
/compact and automatic summarization -> reduce conversation history when context is full
/fork or checkpoint fork             -> branch a conversation with inherited history
Agent Skills context isolation       -> run a skill in a forked context when configured
New Worktree                          -> isolate concurrent implementation changes
Agent Debug Logs                      -> inspect prompts tools calls tokens and loaded context
Cache Explorer                        -> inspect cache hit rate and first divergence
context-window control                -> inspect context use and trigger compaction
session sync exclusions               -> keep selected repository sessions local
```

Forked sessions inherit history and can preserve prompt cache for the next request, but future turns duplicate context and tool costs. Copilot CLI forks using worktree isolation continue in the same worktree unless a new isolated worktree is created.

## Settings Policy

Commit a workspace setting only when it:

```text
changes a default intentionally
fixes a nondefault discovery path
establishes a reproducible team policy
reduces a verified repository-specific risk
is required by a supported extension that the repository intentionally adopts
```

Prefer omission for settings that merely repeat the current default. Explicit defaults can be valid governance, but they increase drift when VS Code changes behavior.

Current examples of documented defaults that are often redundant when copied into a workspace:

```text
chat.agent.enabled = true
chat.agent.maxRequests = 25
chat.mcp.discovery.enabled = false
chat.permissions.default = default
chat.tools.global.autoApprove = false
chat.tools.terminal.ignoreDefaultAutoApproveRules = false
github.copilot.chat.summarizeAgentConversationHistory.enabled = true
chat.includeApplyingInstructions = true
chat.includeReferencedInstructions = false
github.copilot.chat.codeGeneration.useInstructionFiles = true
chat.useAgentSkills = true
chat.useCustomizationsInParentRepositories = false
chat.viewSessions.enabled = true
chat.viewSessions.orientation = sideBySide
chat.plugins.enabled = false
```

Some are organization-managed or non-stable. Do not rely on repository settings to override enterprise policy.

## Preview and Experimental Gate

For every non-stable setting record:

```text
setting and lifecycle
owner
verification date and VS Code channel
measured benefit
known failure mode
rollback value
review date or removal condition
```

Examples requiring lifecycle review at this verification date include tool-output compression, default permission levels, advanced Autopilot, automatic conversation summarization, virtual tools, nested AGENTS discovery, Agents controls, plugin marketplace settings, Agent Host BYOK models, and some Agent Host preference settings.

Do not recommend enabling a Preview feature merely because it might reduce tokens. Require evidence that it preserves required terminal output, diffs, citations, and validation state.

## Native Security Baseline

Use native controls together:

```text
Workspace Trust
Default Approvals
scoped terminal URL and edit approval rules
agent sandboxing where supported
network allow and deny domains
MCP trust and enterprise allow or deny lists
reviewable diffs and worktree isolation
session sync exclusions for sensitive repositories
```

Worktree isolation prevents edit collisions; it is not a security boundary. Search exclusions and context compression are not authorization. Sandbox and approvals do not replace repository review, CI, secret scanning, or branch protection.

## Extension Retention Test

Retain an extension only when all are true:

```text
native feature gap is named
extension capability is materially different or better on frozen repository tasks
permissions and data flow are reviewed
settings and tool contributions are inventoried
Agent Host or Agents Window behavior is tested
worktree ownership is clear
update owner and rollback path exist
removal condition is documented
```

Examples of valid gaps may include provider account access, features not exposed by the native integration, unsupported local harness behavior, or organization policy that requires the provider extension. Do not infer a gap from a different UI alone.

## Agent Host and Agents Window

Agent Host can run supported harnesses in a separate process and can support multi-chat sessions. Chats in the same Agent Host session have separate conversation histories but share the session workspace and worktree.

The Agents Window is a native orchestration surface. Prefer it for cross-project session management, worktree creation, review, tasks, and parallel tracking. It is still subject to lifecycle and organization-policy differences. Enabling an extension inside the Agents Window through `extensions.supportAgentsWindow` should be an explicit allow decision because the extension may contribute tools or modify the session environment.

Do not assume Agent Host makes Copilot CLI, Claude, and Codex prompts, compact behavior, permissions, tool schemas, or billing identical.

## Source Map

Primary official sources:

- https://code.visualstudio.com/docs/agents/overview
- https://code.visualstudio.com/docs/agents/agents-window
- https://code.visualstudio.com/docs/chat/chat-sessions
- https://code.visualstudio.com/docs/agents/reference/ai-settings
- https://code.visualstudio.com/docs/agents/approvals
- https://code.visualstudio.com/docs/agents/security
- https://code.visualstudio.com/docs/agents/sessions/session-sync
- https://code.visualstudio.com/docs/agent-customization/overview
- https://code.visualstudio.com/docs/agent-customization/custom-instructions
- https://code.visualstudio.com/docs/agent-customization/agent-skills
- https://code.visualstudio.com/docs/agents/agent-types/copilot-cli
- https://code.visualstudio.com/docs/enterprise/policies
