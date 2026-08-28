# Interaction-Driven Analytics Guidance

## Boundary

This reference governs analysis that begins with a user selecting a bar, point, line segment, category, entity, metric, or time bucket in an existing dashboard. It defines the analytical decision boundary; it does not implement a dashboard runtime, query service, DataHub adapter, or Databricks job.

The click is evidence of what happened in the UI. It is not, by itself, a complete analytical question.

## Ordered decision path

```text
interaction snapshot
-> analytical intent
-> parent visual semantic contract
-> existing semantic reuse gate
-> named code or data gap only
-> bounded context and targeted live evidence
-> interaction-scoped analytical projection
-> semantic, filter, security, grain, cost, and result gates
-> bounded compute plan
-> downstream execution
-> result validation
-> UI response or reusable candidate
```

The default is `REUSE` before `COMPOSE`. A temporary projection is not a Gold model, metric definition, semantic rule, SQL statement, or production approval.

## Minimum interaction snapshot

Capture only what can affect the next decision:

- dashboard/report identity and deployed version;
- visual identity and type;
- selected mark, category, or entity;
- metric identity and version;
- current drill level;
- visible and material hidden/page/report filters;
- time range and sort or top-N state when relevant;
- tenant, role, and row-level security scope;
- semantic-model version and interaction timestamp.

Do not store unnecessary personal information. Keep observed interaction state separate from inferred intent.

## Analytical intent

Classify the intent as observed, inferred, ambiguous, or unknown. Common choices include breakdown, contributors, trend, comparison, underlying authorized detail, or driver exploration. If materially different intents remain plausible, offer two to four bounded choices or ask one minimum clarification. Do not silently select a root-cause analysis because a user clicked a spike.

## Parent visual semantic contract

Before composing a child analysis, bind the parent metric and version, business definition, calculation rule, population, aggregation semantics, dimensions, filters, time semantics, unit, tenant/security semantics, freshness, governed source, and relevant implementation/version evidence.

Preserve metric meaning. For example, a failure rate defined as failed completed requests divided by all completed requests, excluding cancelled requests, must not become failed rows divided by all rows. Correct SQL is still wrong analytics when semantic continuity is lost.

## Reuse gate

Check for an existing governed metric, dimension, hierarchy, drill path, detail page, certified query, metric view, or semantic relationship. If one supports the request, return `reuse_existing` and do not create a projection. This prevents metric forks, duplicate models, unnecessary context retrieval, and unnecessary compute.

## Projection contract

Create an interaction-scoped projection only for a named remaining gap. It should express the analytical question, parent metric reference, output grain, dimensions, inherited filters, relationships, source and evidence references, security scope, freshness, expected cardinality, compute budget, assumptions, unknowns, and result checks. It should reference existing governed metrics rather than redefine them.

Generated SQL, Spark, DuckDB, or Databricks SQL is a compiled execution projection. It is not the canonical analytical model.

## Fail-closed gates

Before display, validate:

- semantic continuity: parent metric identity, version, calculation, population, aggregation, unit, and time meaning are preserved;
- filter continuity: all material hidden, page, report, tenant, environment, feature, and security filters are inherited or explicitly narrowed;
- security continuity: authority never expands; aggregate visibility does not imply row-level detail permission;
- grain and cardinality: one-to-many, many-to-many, duplicate facts, snapshots, slowly changing dimensions, and fanout are checked;
- compute budget: latency, scan scope, result size, timeout, reuse/cache, and interactive versus asynchronous mode are explicit;
- result validation: freshness, completeness, null/explosion anomalies, expected cardinality, and metric-appropriate reconciliation pass.

If a material gate is failed or unknown, return `partial`, `blocked`, or `async_required`. Do not label the output display-ready merely because execution succeeded.

## Evidence boundaries

Keep evidence families separate:

```text
interaction evidence = what happened in the UI
code evidence = implemented visual behavior
governed context = available semantic and metadata orientation
live evidence = current bounded data behavior
```

DataHub is prior orientation, not current source truth. Code proves implemented behavior, not business meaning. Use either only for a named gap and only within permission and context budgets. Distinguish repository state from deployed dashboard version.

## Promotion

Repeated successful use may create a `reusable_candidate`. It must retain its evidence, scope, version, unknowns, and validation record and require accountable human/semantic review. Keep `production_approved=false` and `gold_promotion_approved=false`; no interaction run automatically creates Gold, a metric, a Skill, a belief, or an architecture standard.

## Machine contract

Use `schemas/interaction-analytics-projection.v1.schema.json` for the smallest structured decision record. Validate instances with `scripts/validate_interaction_projection.py`. The JSON Schema handles shape and whitelists; the validator handles cross-field gates such as reuse-versus-projection exclusivity, parent metric continuity, security non-expansion, fanout, compute, result readiness, and promotion boundaries.
