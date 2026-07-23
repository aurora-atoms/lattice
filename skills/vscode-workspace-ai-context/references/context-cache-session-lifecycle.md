# Context, Cache, Compaction, and Session Lifecycle

Last source verification: 2026-07-23.

Use this reference for `/compact`, automatic compaction, output compression, prompt-cache behavior, resume, fork, subagents, Agent Host, Cowork, or long-running coding-agent design. Recheck official sources because product behavior and cache retention change.

## Distinguish the mechanisms

```text
compact UI layout   = visual arrangement only
context compaction  = lossy replacement of older chat history
output compression  = reduction of terminal diff or tool output
prompt caching      = provider reuse of an unchanged request prefix
checkpoint          = exact task state stored outside chat history
```

Session persistence is not cache persistence. A resumed or Agent Host session can outlive provider cache. A worktree can persist while conversational state becomes stale.

## Prompt layers

```text
L0 stable kernel      security privacy authority routing output contract
L1 workspace profile project map architecture commands capability catalog
L2 task profile       selected model effort tools MCP skills schemas permissions
L3 dynamic suffix     request files diffs logs failures current evidence
```

Keep L0 and stable L1 deterministic. Select L2 before starting a task. Put timestamps, branches, logs, diffs, temporary paths, and other volatile state in L3.

Cache is commonly invalidated by model, effort, context-window, instruction, tool/MCP, schema order, provider, or early-prefix changes. Measure the first divergence in Cache Explorer or runtime telemetry when available.

Do not transfer direct API TTL, write pricing, or retention assumptions to Copilot, Codex, Claude Code, Cowork, or another subscription harness without product-specific evidence.

## Compact decision

Compact when:

```text
an accepted phase is complete and exact checkpoint exists
obsolete exploration or repeated tool output dominates context
automatic compaction is near
cache is already cold and old history is large
model tools or task profile must change for the next phase
```

Delay compact when:

```text
cache is warm and history is directly relevant
exact decisions commands failures or approvals are not checkpointed
debugging depends on distributed earlier evidence
a fork or subagent would isolate the branch more safely
```

Before compact, create `PRE_COMPACT_CHECKPOINT_V1` containing objective, scope, hard constraints, decisions, branch/worktree, changed files, validation, failures, open hypotheses, approvals, next actions, and source references.

After compact, re-anchor from repository state and the checkpoint. Treat the generated summary as a navigation aid, not the sole source of truth.

Recommended manual instruction:

```text
/compact Preserve objective, scope, hard constraints, approvals, accepted decisions
and reasons, branch/worktree state, changed files, validation, current failures,
unresolved hypotheses, next actions, and source refs. Discard duplicate discussion,
raw tool logs, rejected hypotheses, superseded plans, and progress narration. Do not
convert uncertainty into fact.
```

## Continue, compact, fork, subagent, or new session

```text
continue  same objective and profile; history remains useful
compact   same objective; context is noisy; exact state is checkpointed
fork      bounded alternative needs shared history and a short independent future
subagent  isolated research or verification can return a compact result
new       objective security boundary model tool profile or repository changed materially
```

A fork can reuse history and possibly a warm prefix for the next request, but both branches incur future context and tool cost. Prefer checkpoint-boundary forks over copying an entire noisy session. Assign one hypothesis or deliverable per branch and define a stop condition.

Parallel editing requires isolated worktrees unless the runtime explicitly guarantees safe ownership. Reconcile through diffs, tests, and structured artifacts instead of full transcripts.

Subagents are preferable when the parent needs only a result. Limit fanout and include reconciliation cost in evaluation.

## Agent Host

Agent Host separates session lifecycle from the VS Code window. Sessions may continue without a connected editor, and multiple clients can observe them. Verify current rollout and policy.

Important consequences:

```text
closing a window may not terminate work
client-contributed tools can appear or disappear with client connection
tool changes alter prompt assembly and can invalidate cache
remote host workspace and local client filesystem are separate boundaries
shared hosting does not make Copilot Codex and Claude semantics identical
```

## Cowork

Cowork is a separate knowledge-work harness, not a VS Code or Claude Code setting surface. Audit mounted folders, read/write/delete mode, VM containment, connectors, credentials, and audit export separately. Do not assume coding worktree, compact, or cache behavior applies.

## Harness engineering

Store durable state in the repository:

```text
AGENTS.md                  short map and hard rules
ARCHITECTURE.md            system map
skills/                    task-scoped procedures
schemas/                   deterministic boundaries
scripts/ and CI            validation and recovery
docs/exec-plans/active/    current long-task state
docs/exec-plans/completed/ durable decision history
```

A good harness makes application state, tests, logs, and invariants agent-legible. It reduces prompt size and model dependence more reliably than a larger instruction file.

## Measurement

Compare strategies on frozen tasks and record:

```text
model effort active instructions skills tools MCP
input cached-input cache-write output and reasoning tokens
cache hit and first divergence
compaction fork subagent and tool-call counts
first-pass and final validation
unrelated edits regressions human correction and reconciliation time
total cost credits and wall-clock time
```

Optimize accepted delivery per total cost, not cache hit rate alone.

## Official evidence

- https://code.visualstudio.com/docs/chat/copilot-chat-context
- https://code.visualstudio.com/docs/chat/chat-sessions
- https://code.visualstudio.com/docs/agents/agent-troubleshooting/cache-explorer
- https://code.visualstudio.com/docs/agents/concepts/agent-host
- https://code.visualstudio.com/docs/agents/concepts/agents
- https://code.visualstudio.com/docs/agent-customization/hooks
- https://code.visualstudio.com/docs/agents/reference/hooks-reference
- https://code.visualstudio.com/docs/agents/guides/optimize-usage
- https://docs.github.com/en/copilot/tutorials/optimize-ai-usage
- https://developers.openai.com/api/docs/guides/latest-model
- https://openai.com/index/harness-engineering/
- https://docs.anthropic.com/en/docs/claude-code/memory
- https://docs.anthropic.com/en/docs/claude-code/settings
- https://www.anthropic.com/engineering/how-we-contain-claude
