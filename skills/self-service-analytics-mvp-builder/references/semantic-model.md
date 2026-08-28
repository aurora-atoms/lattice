# Semantic Model Guidance

## Model intent

The semantic model is the analytics API for business users, embedded reports, and AI summaries. Do not expose raw source tables.

## Interaction-originated analysis

An interaction with an existing visual is a bounded request signal, not a complete analytical specification. Capture the dashboard, visual, selected mark, metric and version, current filters, time range, authorization scope, and interaction time before deciding what analysis is intended.

Reconstruct the parent visual's semantic contract before creating a child analysis. Preserve its metric identity, calculation rule, population, aggregation behavior, unit, time semantics, material filters, tenant scope, and semantic-model version. A syntactically valid query that changes any of these is not a valid drill result.

Apply this order:

```text
interaction snapshot -> analytical intent -> parent semantic contract
-> existing governed semantic reuse -> bounded projection only for a named gap
-> semantic, filter, security, grain, cost, and result validation
```

Use `references/interaction-driven-analytics.md` and the task-scoped projection contract for the detailed boundary. The projection is an execution input, not SQL and not a durable Gold model.

## Metric contract

Each metric must include:

- metric_id
- display_name
- business_definition
- formula or calculation rule
- grain
- source_gold_table
- allowed_dimensions
- default_filters
- refresh_cadence
- owner
- version
- quality_notes
- rls_impact

Minimum v1 metrics should fit one decision loop. Prefer five trusted metrics over twenty ambiguous ones.

## Naming rules

- Use business names in the model: `Account`, `Product`, `Usage`, `Revenue`, `Risk`, `Opportunity`, `Action`.
- Hide technical keys unless needed for drill-through or RLS.
- Keep raw/staging prefixes outside the user-facing semantic layer.
- Use measure names that read like business concepts: `active accounts`, `usage rate`, `risk accounts`, `expansion opportunity value`.

## Dimensional model defaults

Prefer a star schema:

- facts: event counts, daily snapshots, balances, opportunities, action outcomes
- dimensions: date, tenant, account, product, segment, owner, region, plan, channel

Avoid many-to-many relationships and ambiguous filter paths unless essential and documented.

## Gold table defaults

Good first Gold tables:

- `gold_[entity]_daily_snapshot`
- `gold_[entity]_metric_snapshot`
- `gold_[entity]_risk_signal`
- `gold_[entity]_opportunity_signal`
- `gold_action_queue`

Include:

- `tenant_id`
- entity key
- date or snapshot timestamp
- metric columns
- dimension keys
- quality/status columns

## AI-ready semantic model

If AI insights are needed, add:

- table and column descriptions
- metric descriptions and synonyms
- example questions
- disallowed interpretations
- business glossary
- calculation caveats
- safe response patterns

Start with explanations and summaries over curated metrics before open-ended text-to-SQL.
