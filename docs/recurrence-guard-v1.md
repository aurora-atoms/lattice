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

## GitHub Copilot and VS Code

The repository custom agent lives in `.github/agents`, and the reusable skill lives in `.github/skills`. Current GitHub Copilot and VS Code agent surfaces can discover these locations natively.

### VS Code / Agent Host

Open the repository in VS Code, open the Agents or Chat view, and choose **Recurrence Guard** from the agent picker. A minimal starting request is:

```text
Review my current changes for known recurrence risks.
```

The custom agent is read-only by tool configuration. It uses the native agent host for repository context and search; no separate Lattice runtime is required.

### GitHub Copilot cloud agent

After the custom agent is merged into the repository default branch, it can appear in the custom-agent selector for Copilot cloud agent on GitHub. Select **Recurrence Guard** instead of the default agent and ask it to review a branch, pull request context, or issue task for known recurrence risk.

For V1, prefer interactive review rather than assigning this agent to implement an issue: the role is intentionally non-editing and non-implementing.

## Promotion path

Do not build a plugin or centralized service first. Promote only after a credible second use:

1. repository-local agent + skill + 5-8 guards;
2. second developer uses it without special coaching;
3. at least one useful real finding or a convincing historical replay with low false-positive rate;
4. only then consider organization-level agent sharing, a shared validator, PR integration, hooks, or external evidence retrieval.
