# DataHub × Pre-Silver/Silver Modeling Guidance Replay

## Verdict

`ADAPT / GUIDANCE HARDENED`.

The repository now treats Pre-Silver/Silver work as a **modeling-decision-originated** context task. It reuses `context-mastery` and `domain-context-pack`; it does not add a Data Modeling Skill, schema, platform, adapter, profiler, ETL generator, or approval authority.

The target behavior is:

```text
Gold consumer need
-> Gold Consumer Contract
-> Modeling Question Contract
-> minimum authorized DataHub context
-> targeted live-data evidence
-> field-level source roles and cross-source reconciliation
-> adversarial challenge
-> Gold-fit check
-> Silver Model Candidate / partial / unknown / blocked
-> accountable human review
```

## Behavioral Gap Closed

Before this hardening, Level 4 Modeling Context said which evidence was useful but did not make the consumer-first contracts, modeling-decision route, source-role discipline, adversarial gates, or candidate-only boundary explicit enough for a native agent.

The hardened guidance prevents this shortcut:

```text
Bronze shape -> schema/profile sample -> plausible Silver -> production claim
```

It enforces these separations:

```text
business requirement != implemented code behavior
DataHub context != observed live-data behavior
DataHub relationship != verified join
profiling uniqueness != durable key
historical query != business rule
current distribution != future schema contract
candidate != approved architecture or production model
```

## Sandbox Boundary

The replay is public-safe and declares:

```text
simulation_status=synthetic_reference
downstream_adoption_status=not_observed
```

Executed components:

- synthetic Gold Consumer and Modeling Question contracts;
- synthetic DataHub-shaped metadata and field-level source roles;
- in-memory bounded live-evidence flags and measurements;
- deterministic Silver-model guidance investigator;
- repository unit tests.

Not executed:

- real DataHub Core or Cloud;
- real DataHub MCP or Agent Skills;
- real Databricks, Unity Catalog, database, or production data;
- external Codex, Copilot, Claude Code, Gemini CLI, or other model runs;
- ETL, table creation, deployment, approval, or promotion.

The replay proves deterministic guidance conformance only. It does not prove a production integration or cross-model agent behavior.

## Scenario Results

| Scenario | Result | Guarded behavior |
| --- | --- | --- |
| Clean candidate | PASS / `CANDIDATE_FOR_HUMAN_REVIEW` | contracts preceded context; bounded evidence supported a candidate but not production approval |
| False uniqueness | PASS / `PARTIAL_KEY_REJECTED` | live duplicates defeated a profile-suggested key |
| Join fanout | PASS / `BLOCKED_JOIN_FANOUT` | measured row multiplication defeated a DataHub-suggested relationship |
| Temporal mismatch | PASS / `BLOCKED_TEMPORAL_SEMANTICS` | event, ingest, update, and effective time remained distinct |
| Conflicting authority | PASS / `BLOCKED_AUTHORITY_CONFLICT` | requirement/code/DataHub disagreement was routed to accountable human authority, not voted away |
| Late/duplicate events | PASS / `PARTIAL_DEDUP_REQUIRED` | retry, replay, late-arrival, and deduplication semantics remained explicit |
| Schema evolution | PASS / `PARTIAL_VERSION_SCOPED` | current profiling did not silently cover multiple schema versions |
| Gold consumer mismatch | PASS / `REJECTED_GOLD_MISMATCH` | a technically tidy candidate failed consumer grain/history requirements |
| Insufficient evidence | PASS / `INSUFFICIENT_EVIDENCE` | metadata-only relationship remained unknown without authorized live evidence |

All nine scenarios preserved:

```text
PRODUCTION_APPROVED=false
candidate_only=true
```

## Capability Changes

### `context-mastery`

- distinguishes code-originated runtime verification, data-originated discovery, and modeling decisions;
- routes modeling decisions to `domain-context-pack` first;
- requires Gold Consumer and Modeling Question contracts;
- makes `system-mental-model` conditional on a named implemented-semantics gap;
- rejects automatic Silver creation or approval.

### `domain-context-pack`

- reuses the current typed source/context-item contract rather than adding a second modeling schema;
- adds field-level source-role classification;
- keeps requirement, code, DataHub context, live behavior, and human authority separate;
- challenges keys, joins, time, duplicates, schema scope, and Gold fit;
- emits candidate/partial/unknown/blocked for human review.

### Root and DataHub guidance

- root `AGENTS.md` remains a routing map;
- detailed contracts, evidence boundaries, checks, and output expectations remain in `docs/datahub-context-guidance.md`;
- Scenario 1 behavior remains available and Scenario 3 interaction-driven analytics is not implemented.

## Validation

Targeted replay validation passed locally:

- JSON syntax for changed trigger and output evals;
- synthetic Silver-model replay: 9 scenarios passed;
- Silver-model replay unit tests: 10 passed.
- canonical registry projection, manifest, capability-context, composition, and public/private validators;
- changed Skill package validators and Domain Context Pack semantic tests: 17 passed;
- Scenario 1 operational-evidence replay regression tests: 8 passed;
- full repository suite: 321 passed.

The changed-Skill base/head contract gate is run after the implementation commit exists and is reported in the PR description.

## Remaining Unknowns

- No real authorized downstream DataHub/Unity Catalog environment was exercised.
- No real agent-model behavioral comparison was run.
- Field-level authority and live-query interfaces remain downstream configuration and permission concerns.
- The existing Domain Context Pack schema can carry the task-scoped evidence, but no claim is made that it is the final private modeling artifact for every downstream environment.
