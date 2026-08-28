# DataHub × Code × Operational Evidence Guidance Replay

## Verdict

`KEEP + HARDEN`.

PR #56's DataHub-as-context-substrate architecture remains valid. The behavior gap was origin-aware routing and external-effect verification: a code-originated question could reach DataHub before the agent established what the code should have produced, and one empty live query could be overinterpreted.

This change does not create a DataHub integration, data platform, database agent, Elasticsearch agent, wrapper, MCP server, or active module.

## Behavior Change

```text
code-originated question
-> bounded code/config inspection
-> Expected Effect Contract
-> minimum task-scoped context, only for a named gap
-> approved narrow live query
-> effect-path verification / falsification / unknown

data-originated question
-> bounded context selection
-> authorized DataHub discovery
-> approved live query only when current evidence is required
```

The guidance now keeps these states distinct:

```text
intended -> triggered -> emitted -> transported -> ingested -> transformed
-> stored -> visible to this caller -> found by this query
```

## Sandbox Boundary

The replay is public-safe and declares:

```text
simulation_status=synthetic_reference
downstream_adoption_status=not_observed
```

Executed components:

- Python `SyntheticUploadService` with a conditional structured event;
- synthetic DataHub-shaped field and deployment mappings;
- in-memory Elasticsearch-like exact-match store;
- deterministic operational-evidence investigator;
- repository unit tests.

Not executed:

- real DataHub Core or Cloud;
- real DataHub MCP or Agent Skills;
- real Elasticsearch;
- external Codex, Copilot, Claude Code, Gemini CLI, or other model runs.

Therefore the replay proves deterministic guidance conformance only. It does not prove production integration or cross-model agent behavior.

## Behavioral Iterations

### Iteration 1

The six requested scenarios passed. Review exposed two remaining false-verification surfaces:

1. correlation-only matches could collide with another event, environment, tenant, attempt, or time window;
2. an empty corrected query remained weak negative evidence when visibility, retention, completeness, sampling, or destination coverage was unknown.

### Iteration 2

Guidance and replay were hardened to:

- bind positive matches to expected event/action, environment, correlation, and bounded time identity;
- qualify negative evidence by caller visibility, destination/version coverage, retention, time completeness, and sampling/drop behavior;
- preserve `UNKNOWN_AFTER_QUERY` when a bounded corrected query still cannot locate the event.

All seven scenarios and eight replay assertions passed.

## Scenario Results

| Scenario | Result | Observed behavior |
| --- | --- | --- |
| Healthy | PASS / `VERIFIED` | inspected code, built expected effect, selected minimum context, then matched bounded live evidence |
| Trigger not executed | PASS / `TRIGGER_NOT_EXECUTED` | stopped at trigger evidence; did not blame logging pipeline |
| Logging suppressed | PASS / `SUPPRESSED_BY_CONFIG` | separated code-path execution from runtime level/config allowance |
| Transformation mismatch | PASS / `VERIFIED` | retained the empty initial query as counterevidence, corrected `requestId -> request.id`, and retried narrowly |
| Wrong environment/destination | PASS / `VERIFIED` | corrected the deployment-to-destination mapping before retry |
| Ingest/drop failure | PASS / `INGEST_DROP` | separated observed application emission from downstream storage |
| Unlocated after bounded query | PASS / `UNKNOWN_AFTER_QUERY` | did not convert a remaining negative query into emission or pipeline failure |

## Newly Discovered Gaps

- Positive evidence needs composite expected-effect identity; correlation alone is insufficient.
- Negative evidence needs an explicit observability-completeness boundary, including caller-visible documents and fields.
- DataHub or deployment mappings can be correct for one version and stale for another; deployment version belongs in the task scope.
- A query can be syntactically correct but evidentially weak because retention, sampling, tenant filtering, or delayed ingestion is unknown.

## Validation

Passed locally:

- deterministic registry projection check;
- canonical capability manifest validation;
- capability context validation;
- public/private boundary validation;
- capability composition validation;
- changed Skill package validation;
- Domain Context Pack schema/semantic tests: 17 passed;
- repository tests: 311 passed;
- operational-evidence replay tests: 8 passed within the repository suite.

CI and a real authorized downstream integration remain separate evidence.
