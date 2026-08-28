# DataHub × Pre-Silver/Silver Modeling Deterministic Guidance Conformance Replay

## Verdict

`ADAPT / GUIDANCE HARDENED`.

The repository treats Pre-Silver/Silver work as a **modeling-decision-originated** context task. It reuses `context-mastery` and `domain-context-pack`; it does not add a Data Modeling Skill, platform, adapter, profiler, ETL generator, or approval authority.

The target behavior remains:

```text
Gold consumer need
-> Gold Consumer Contract
-> Modeling Question Contract
-> minimum authorized DataHub context
-> targeted live-data evidence
-> field/decision-scoped source roles and cross-source reconciliation
-> adversarial challenge
-> Gold-fit / freshness / governance checks
-> Silver Model Candidate / partial / unknown / blocked
-> accountable human review
```

## Machine-Contract Hardening

The Scenario 2 semantics are no longer prose-only.

The existing `lat.domain_context_pack.v1` contract now supports an optional typed `modeling_decision` section. When `task.origin=modeling_decision`, the schema requires:

- a machine-visible Gold Consumer Contract;
- a non-empty Modeling Question Contract;
- field/decision-scoped source roles;
- a Silver Model Candidate result whose status is `candidate`, `partial`, `unknown`, or `blocked`;
- `production_approved=false`.

The semantic validator additionally checks:

- core modeling-question coverage;
- source-role references and evidence references;
- authoritative source roles are not merely inferred;
- relationships require a join-cardinality question;
- candidate unknown references point to declared unknowns;
- candidate status is consistent with pack answerability;
- a candidate cannot remain `candidate` while blocking modeling questions, unknowns, or conflicts remain;
- `status=candidate` requires `gold_fit=candidate_fit` and at least one candidate key;
- `gold_fit=failed` requires a blocked candidate.

This extends the existing Domain Context Pack machine contract. It does not introduce a parallel modeling schema.

## Behavioral Gap Closed

Before hardening, Level 4 Modeling Context identified useful evidence but did not make the consumer-first contracts, modeling-decision route, source-role discipline, adversarial gates, candidate-only boundary, or machine validation explicit enough for a native agent.

The guidance prevents this shortcut:

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

## Replay Classification

The synthetic replay is explicitly classified as:

```text
simulation_status=synthetic_reference
downstream_adoption_status=not_observed
replay_kind=deterministic_guidance_conformance
agent_behavior_status=not_evaluated
```

It is **not** described as proof of native-agent behavior.

Executed components:

- synthetic Gold Consumer and Modeling Question contracts;
- synthetic DataHub-shaped metadata and source-role signals;
- in-memory bounded live-evidence flags and measurements;
- deterministic Silver-model guidance investigator;
- repository unit tests.

Not executed:

- real DataHub Core or Cloud;
- real DataHub MCP or Agent Skills;
- real Databricks, Unity Catalog, database, or production data;
- external Codex, Copilot, Claude Code, Gemini CLI, or other context-isolated model run;
- ETL, table creation, deployment, approval, or promotion.

Therefore this replay proves deterministic rule conformance only. A future isolated-agent replay remains separate evidence.

## Scenario Results

| Scenario | Result | Guarded behavior |
| --- | --- | --- |
| Clean candidate | PASS / `CANDIDATE_FOR_HUMAN_REVIEW` | contracts preceded context; bounded evidence supported a candidate but not production approval |
| False uniqueness | PASS / `PARTIAL_KEY_REJECTED` | live duplicates defeated a profile-suggested key |
| Join fanout | PASS / `BLOCKED_JOIN_FANOUT` | measured row multiplication defeated a DataHub-suggested relationship |
| Temporal mismatch | PASS / `BLOCKED_TEMPORAL_SEMANTICS` | event, ingest, update, and effective time remained distinct |
| Conflicting authority | PASS / `BLOCKED_AUTHORITY_CONFLICT` | disagreement was routed to accountable authority instead of voted away |
| Late/duplicate events | PASS / `PARTIAL_DEDUP_REQUIRED` | retry, replay, late-arrival, and deduplication semantics remained explicit |
| Schema evolution | PASS / `PARTIAL_VERSION_SCOPED` | current profiling did not silently cover multiple schema versions |
| Gold consumer mismatch | PASS / `REJECTED_GOLD_MISMATCH` | a technically tidy candidate failed consumer grain/history requirements |
| Insufficient evidence | PASS / `INSUFFICIENT_EVIDENCE` | metadata-only relationship remained unknown without authorized live evidence |
| Freshness mismatch | PASS / `BLOCKED_FRESHNESS_MISMATCH` | a model that could not satisfy the consumer freshness requirement was blocked |
| Governance mismatch | PASS / `BLOCKED_GOVERNANCE_MISMATCH` | a model that could not preserve the consumer governance boundary was blocked |
| Compound failures | PASS / `BLOCKED_MULTIPLE_MODELING_CONSTRAINTS` | duplicate key, fanout, temporal ambiguity, and schema-scope failures were preserved together rather than stopping at the first failure |

Every scenario preserves:

```text
PRODUCTION_APPROVED=false
candidate_only=true
```

## Compound-Failure Behavior

The deterministic investigator no longer returns immediately after the first ordinary modeling failure. It evaluates the bounded gate set and preserves all observed failures in `GATE_RESULTS` before deciding the candidate state.

This matters because real modeling failures can coexist. A false key, fanout, time ambiguity, and schema drift should not disappear merely because one of them was discovered first.

Missing live-data authorization is still a valid early stop because the evidence boundary itself prevents the downstream checks from being established.

## Capability Changes

### `context-mastery`

- distinguishes code-originated runtime verification, data-originated discovery, and modeling decisions;
- routes modeling decisions to `domain-context-pack` first;
- requires Gold Consumer and Modeling Question contracts;
- makes `system-mental-model` conditional on a named implemented-semantics gap;
- rejects automatic Silver creation or approval.

### `domain-context-pack`

- uses the existing `lat.domain_context_pack.v1` contract with a typed optional modeling section;
- keeps requirements, code, DataHub context, live behavior, and human authority separate;
- supports field/decision-scoped source-role assertions with evidence;
- challenges keys, joins, time, duplicates, schema scope, Gold fit, freshness, and governance;
- emits candidate/partial/unknown/blocked for human review;
- keeps production approval structurally impossible in the modeling candidate.

### Root and DataHub guidance

- root `AGENTS.md` remains a routing map;
- detailed contracts, evidence boundaries, checks, and output expectations remain in `docs/datahub-context-guidance.md`;
- Scenario 1 behavior remains available;
- Scenario 3 interaction-driven analytics is not implemented.

## Validation Expectations

The repository validation should include:

- JSON syntax for changed schemas and evals;
- Domain Context Pack schema and semantic tests, including modeling-contract failures;
- deterministic Silver-model conformance replay covering 12 scenarios;
- Scenario 1 operational-evidence replay regression tests;
- changed Skill package validation;
- canonical registry projection, manifest, capability-context, composition, and public/private validators;
- full repository suite.

GitHub Actions provide the remote validation result for the final PR head. Local claims from the earlier PR head are not carried forward automatically after this repair.

## Remaining Unknowns

- No real authorized downstream DataHub/Unity Catalog environment was exercised.
- No context-isolated external coding-agent replay was executed; `agent_behavior_status=not_evaluated` is explicit.
- Field-level authority resolution and live-query interfaces remain downstream configuration and permission concerns.
- The typed public modeling section is intentionally compact; downstream repositories may carry richer private modeling artifacts without changing the public Lattice contract.
