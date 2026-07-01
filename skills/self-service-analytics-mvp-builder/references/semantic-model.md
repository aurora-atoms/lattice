# Semantic model guidance

## Model intent

The semantic model is the analytics API. Business users, reports, embedded analytics, and AI assistants should consume the semantic model rather than raw source tables.

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

## Naming rules

- Use business names in the model: `Account`, `Product`, `Usage`, `Revenue`, `Risk`, `Opportunity`, `Action`.
- Hide technical keys unless needed for drill-through or RLS.
- Prefix raw/staging artifacts outside the model, not inside the user-facing semantic layer.
- Use measure names that read like business concepts, such as `active accounts`, `usage rate`, `risk accounts`, `expansion opportunity value`.

## Dimensional model defaults

Prefer a star schema:

- facts: event counts, daily snapshots, balances, opportunities, action outcomes
- dimensions: date, tenant, account, product, segment, owner, region, plan, channel

Do not let many-to-many relationships or ambiguous filter paths leak into the MVP unless they are essential and documented.

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

Start with explanation and summarization over curated metrics before supporting open-ended text-to-SQL.
