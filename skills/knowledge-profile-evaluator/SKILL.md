---
name: knowledge-profile-evaluator
description: Create and evaluate public, vendor-neutral task knowledge profiles. Query ConPort first when available. Input is approved contracts, capability registries, MCP inventories, caller roles, output schemas, golden questions, traces, citations, costs, and outcomes. Use to select the minimum skills, knowledge scopes, read-only tools, context budget, output contract, and eval suite for a bounded task; output is a deterministic profile, least-privilege MCP policy, golden dataset, metric contract, regression verdict, and expansion gate preserving authorization behavior, citations, no-answer handling, stable hashes, privacy, and denominators. Do not use to approve sources, implement retrieval, expose wildcard tools, capture sensitive content by default, publish private evals, or infer quality from a demo alone.
---

# Knowledge Profile Evaluator

## Goal

Activate the minimum authorized knowledge and tools for one task, then prove retrieval, answer, permission, freshness, cost, and task-outcome behavior with a versioned eval set.

## Use When

Use for task profiles, context-pack selection, read-only MCP allowlists, output contracts, golden questions, component and end-to-end metrics, regression gates, observability fields, or decisions to add graph, A2A, or write autonomy.

## Do Not Use When

Do not decide source authority; route to `team-knowledge-plane-governor`. Do not implement ingestion, chunking, fusion, or reranking; route to `hybrid-knowledge-retrieval-builder`. Do not allow broad tool scopes, use production secrets in evals, or reduce a task result to token cost alone.

## Inputs

Require a Project Knowledge Contract, approved knowledge and capability metadata, caller role, bounded task and output contract, MCP/tool inventory, golden questions with expected sources and permission outcomes, retrieval/answer traces, baseline, and cost or delivery evidence.

## Outputs

Return one or more of:

- a task-profile manifest and stable hash inputs;
- an explicit read-only MCP/tool allowlist and approval policy;
- a versioned golden-question dataset;
- retrieval, grounded-answer, citation, permission, freshness, latency, cost, and task-success metrics;
- a regression result and `promote | revise | reject | defer` verdict;
- a measured expansion decision for graph, A2A, or writes.

## Workflow

1. Query_ConPort_MCP_before_loading_or_searching_full_skill_text when available; otherwise inspect profile, registry, and dataset metadata before long references or traces.
2. State the task, caller role, allowed outputs, source scope, and prohibited side effects.
3. Select the smallest required skills, knowledge collections, retrieval projections, and tools. Deny undeclared capabilities.
4. Bind caller identity through the access path. For remote MCP, use audience-bound authorization and separate downstream credentials; never pass through the client token.
5. Keep the POC read-only. Prompt for approved elevation and preserve audit and rollback requirements before any write surface.
6. Order stable profile fields deterministically; exclude timestamps, random IDs, absolute paths, and task content from the stable hash.
7. Freeze golden questions before tuning. Include exact lookup, paraphrase, multi-hop, conflict, stale, unauthorized, no-answer, and prompt-injection-bearing cases.
8. Evaluate retrieval separately from answer generation, then evaluate the end-to-end task and delivery outcome.
9. Report every rate with numerator, denominator, dataset version, and subset. Report latency distribution and cost method.
10. Record low-cardinality telemetry by default. Treat queries, prompts, retrieved content, tool arguments, and results as sensitive opt-in data.
11. Promote only when safety gates pass and the candidate beats or preserves the frozen baseline. Defer graph, A2A, and writes unless the same dataset and workflow demonstrate need.

## Rules

KPEV.001 | MUST | profile | select the minimum task-specific skills knowledge tools and output contract
KPEV.002 | MUST | identity | bind retrieval and tools to authenticated caller identity
KPEV.003 | MUST | tools | use explicit allowlists and deny undeclared capabilities
KPEV.004 | MUST | authorization | use audience-bound tokens and separate downstream credentials for remote MCP
KPEV.005 | MUST | eval | freeze versioned cases and baseline before tuning
KPEV.006 | MUST | metrics | report numerator denominator subset dataset version and measurement method
KPEV.007 | MUST | safety | require zero critical permission leakage for promotion
KPEV.008 | MUST | citation | test material claim coverage and source locator validity
KPEV.009 | MUST | outcome | distinguish retrieval answer quality task success and delivery outcome
KPEV.010 | NEVER | telemetry | capture sensitive query prompt content tool arguments or source text by default
KPEV.011 | NEVER | score | hide critical failures inside one aggregate quality number
KPEV.012 | SHOULD | token | optimize quality-adjusted token ROI after safety and task quality pass
KPEV.013 | SHOULD | cache | keep invariant profile policy and schemas in a stable prefix and task data in a dynamic suffix
KPEV.014 | MAY | expansion | approve graph A2A or writes only after a versioned gate passes

## References

- Read `references/profile-and-access-contract.md` for profile composition, hashing, MCP boundaries, and context budgeting.
- Read `references/evaluation-contract.md` for datasets, metrics, thresholds, telemetry, and promotion decisions.
- Use `schemas/task-knowledge-profile.schema.json` and `schemas/golden-question.schema.json` for machine-readable artifacts.
- Load retrieval-builder references only for a failed retrieval component.

## Verification

```bash
python3 scripts/validate_skill_package.py --root skills/knowledge-profile-evaluator
python3 scripts/estimate_skill_tokens.py --root skills/knowledge-profile-evaluator
python3 -m json.tool skills/knowledge-profile-evaluator/schemas/task-knowledge-profile.schema.json >/dev/null
python3 -m json.tool skills/knowledge-profile-evaluator/schemas/golden-question.schema.json >/dev/null
git diff --check
```

Before promotion, validate schema shape, deterministic profile hashing, allowlist enforcement, unauthorized and no-answer cases, citation locators, metric denominators, baseline comparison, content-redacted telemetry, and approval behavior for attempted writes.

## Failure Modes

- profile-bloat: every skill, source, or tool is installed for every task;
- identity-loss: retrieval uses a service identity without caller policy context;
- token-passthrough: an MCP client token is reused against a downstream API;
- golden-after-tuning: test cases are selected to match the implementation;
- metric-blending: permission leaks disappear inside an average score;
- judge-monoculture: one LLM judge is treated as objective ground truth;
- observability-leak: prompts, source text, or tool arguments enter telemetry by default;
- demo-promotion: a polished answer substitutes for replayable evaluation.
