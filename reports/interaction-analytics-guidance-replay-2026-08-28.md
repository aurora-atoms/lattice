# Interaction-Driven Analytics Guidance Replay — 2026-08-28

## Evidence boundary

`replay_kind=deterministic_guidance_conformance`
`agent_behavior_status=not_evaluated`
`simulation_status=synthetic_reference`
`downstream_adoption_status=not_observed`

The replay uses a public-safe synthetic Service Operations Dashboard. It does not claim to exercise a real BI runtime, DataHub, Unity Catalog, Databricks, live database, or external coding agent.

## Baseline on main

Baseline commit: `cda3278f255296336976457eff0a9de4a4ed4390`.

The existing analytics capability preserved static MVP semantics and tenant controls but did not express or machine-check:

- interaction snapshot and observed-versus-inferred intent;
- governed semantic reuse before composition;
- parent metric, filter, security, grain, compute, and result continuity;
- temporary projection versus durable Gold boundary;
- interaction-specific routing from `AGENTS.md`.

Observed baseline verdict: `SCENARIO_3_NOT_EXPRESSIBLE`.

## Scenario results

| Scenario | Expected | Observed | Result |
|---|---|---|---|
| Existing semantic model | `reuse_existing` | `reuse_existing` | PASS |
| Valid temporary breakdown | `projection_candidate` | `projection_candidate` | PASS |
| Semantic drift | `blocked` | `blocked` | PASS |
| Hidden filter loss | `blocked` | `blocked` | PASS |
| Security expansion | `blocked` | `blocked` | PASS |
| Grain/fanout | `blocked` | `blocked` | PASS |
| Non-additive metric misuse | `blocked` | `blocked` | PASS |
| Ambiguous click | `ambiguous` | `ambiguous` | PASS |
| Compute budget exceeded | `async_required` | `async_required` | PASS |
| Stale semantic version | `blocked` | `blocked` | PASS |
| Failed parent-child reconciliation | `blocked` | `blocked` | PASS |
| Repeated successful use | `reusable_candidate` | `reusable_candidate` | PASS |
| Compound failures | `blocked` | `blocked` | PASS |

## What is proven

- The existing analytics capability can represent interaction-originated decisions without creating a new Skill or runtime.
- The projection schema rejects unknown fields and requires the interaction snapshot, parent semantic contract, continuity gates, bounded compute plan, result validation, evidence references, and fail-closed promotion fields.
- The semantic validator rejects reuse-plus-projection conflicts, parent metric drift, security expansion, unresolved grain/fanout, compute-budget violations, result failures, hidden unknowns, and automatic Gold approval.
- The compound case retains multiple failed gate results rather than hiding later failures behind the first one.

## Remaining unknowns

- No context-isolated Codex/Copilot/Claude/Gemini run was executed; agent behavior remains not evaluated.
- No real Power BI, React, DataHub, Unity Catalog, Databricks, or live-source permission path was exercised.
- Deployed-version binding, tenant-policy resolution, query compilation, and latency measurements remain downstream integration work.
