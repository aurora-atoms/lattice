# Recurrence Guard V1

Recurrence Guard is a deliberately narrow, read-only quality capability. It reviews a current change only for evidence-backed failure patterns that a repository already knows it should not repeat.

It does **not** recommend the best implementation, perform broad code review, approve a merge, or claim that a change is safe or correct.

## Minimal package

```text
.github/
├── agents/
│   └── recurrence-guard.agent.md
└── skills/
    └── recurrence-guard/
        ├── SKILL.md
        ├── guards.example.jsonl
        ├── evals/
        │   └── replay-cases.jsonl
        └── scripts/
            └── validate_catalog.py
```

The public Lattice package contains synthetic examples only. It intentionally contains no company code, incident details, proprietary rules, private URLs, or internal evidence.

## Downstream adoption

For the fastest team pilot, copy the package into the affected code repository rather than creating a separate platform repository.

Then:

1. Keep the agent and skill generic.
2. Copy `guards.example.jsonl` to `guards.jsonl`.
3. Replace all demo entries with 5-8 repository-local known failure patterns backed by evidence that is allowed to remain in that repository.
4. Add positive, negative, exception, and insufficient-evidence replay cases.
5. Run the validator with `--authoritative` so synthetic evidence cannot accidentally become a real blocking rule.
6. Start read-only and manually invoked. Do not add automatic hooks, PR blocking, MCP, RAG, dashboards, or a separate service until repeated use shows a specific need.

## Guard lifecycle

Only three states are required for V1:

- `candidate`: may warn; never blocks.
- `active`: may block when scope, applicability, evidence, and exception checks all succeed.
- `retired`: retained for history; ignored by review.

Use precision over recall. A small number of high-confidence guards is preferable to a large noisy catalog.

## Outcome contract

Recurrence Guard returns one of:

- `BLOCK`
- `WARN`
- `UNKNOWN`
- `NO_KNOWN_MATCH`

It never returns `PASS`, `SAFE`, or `READY`.

`NO_KNOWN_MATCH` means only that the inspected change did not match a loaded known-failure guard. It is not a quality approval.

## Native GitHub Copilot usage

The repository custom agent lives in `.github/agents`, and the reusable skill lives in `.github/skills`. These are native GitHub Copilot customization surfaces. Lattice does not provide a separate agent runtime for Recurrence Guard.

The agent profile intentionally exposes only the portable `read` and `search` tool aliases, so the native host retains repository-reading and search capabilities without an edit or shell capability.

### GitHub Copilot app

Open the repository as a project in the GitHub Copilot app. Repository skills are available to the app automatically. In a session, use `/agent` and choose **Recurrence Guard**, then ask:

```text
Review my current changes for known recurrence risks.
```

Because `disable-model-invocation: true`, the custom agent is manually selected rather than silently inferred for unrelated tasks.

### VS Code / Agent Host

Open the repository in VS Code and choose **Recurrence Guard** from the agent picker. The `.github/agents/recurrence-guard.agent.md` profile is the configuration; the built-in Agent Host is the runtime that supplies session management, repository context, and the allowed tools.

A minimal starting request is:

```text
Review my current changes for known recurrence risks.
```

No Lattice router, service, MCP server, or separate UI is required.

### Copilot cloud agent on GitHub.com

After the custom agent profile is available in the target repository and branch, choose **Recurrence Guard** from the custom-agent selector for Copilot cloud agent. The same profile can therefore be reused rather than reimplemented as a separate cloud service.

For V1, use it as a review/investigation role. Do not assign it an implementation expectation: the role is intentionally non-editing and non-implementing.

## Validation

The public repository includes a small CI workflow that validates the synthetic catalog and replay set whenever the Recurrence Guard package changes. Downstream teams can keep the same deterministic validator and replace only the example catalog and replay evidence.

## Promotion path

Do not build a plugin or centralized service first. Promote only after a credible second use:

1. repository-local agent + skill + 5-8 guards;
2. second developer uses it without special coaching;
3. at least one useful real finding or a convincing historical replay with low false-positive rate;
4. only then consider organization-level agent sharing, a shared validator, PR integration, hooks, or external evidence retrieval.
