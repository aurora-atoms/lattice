# Architecture Reference

## Target Pattern

```text
Databricks batch preprocessing or existing source data
  -> PostgreSQL D-1 snapshot / approved bi_* serving tables
  -> Power BI Import semantic model
  -> explicit measures + calculation groups + selectors + display metadata
  -> Metric Explorer + thin dashboards
```

Allowed for v0.1: Databricks batch/offline preprocessing that writes delayed snapshots or aggregates.
Blocked for v0.1: Databricks Serverless SQL, Databricks DirectQuery, live Databricks BI serving, dual-source DirectQuery.

## Scale Tracks

### 1. Future source migration

Current path:

```text
Parquet/Delta/raw analytical files -> Databricks batch -> PostgreSQL snapshot -> Power BI Import
```

Future paths may include Databricks governed catalog, DataWorks, Fabric Lakehouse/Warehouse, or Direct Lake. Migration rule:

```text
Change source bindings, not semantic names.
```

Preserve table names, measure names, display names, folders, selector keys, and report visual bindings. Use `source-catalog.yaml` or `source_policy` to map current and future profiles.

Future Fabric/Direct Lake targets should be star-shaped Delta tables. Avoid assuming SQL views will map cleanly to Direct Lake; declare fallback/DirectQuery risk.

### 2. Dashboard reuse

Build the second dashboard as a thin consumer:

```text
existing semantic model -> new report blueprint -> thin/live-connected report when available
```

Before adding a measure, check metric, display, and selector catalogs. Do not copy a PBIX and modify its semantic model unless a fork is explicitly accepted.

### 3. Governed user semantic requests

User input is a request, not executable model code:

```text
semantic-request.yaml -> validation -> catalog patches -> TMDL/DAX -> BI review -> PBIX/shared release
```

Allow users to define business names, definitions, aggregation intent, display names, selector eligibility, and dashboard use. Block direct user publishing of DAX, credentials, raw field exposure, hidden fields, or breaking name changes.

Lifecycle: `draft -> validated -> compiled -> reviewed -> approved -> published`; use `deprecated` or `rejected` for removal/denial.

## Source Placement

### Databricks batch

Use for heavy preparation: Parquet/Delta reads, large joins, window logic, deduplication, cleansing, component/score preparation, aggregates, snapshots, writes to PostgreSQL/import tables. Declare latency, for example `snapshot_latency: D-1 daily`.

### PostgreSQL serving

Use as the quick-win Import source. Expose stable `bi_*` tables/views:

```text
bi_metric_snapshot_daily
bi_metric_component_daily
bi_entity
bi_component
bi_target
bi_mapping
```

These should emulate future Gold/semantic serving tables: stable grain, business names, and star-shaped structure. Avoid raw operational dumps.

### Power BI semantic layer

Use for filter-context analytics: explicit measures, calculation groups, time intelligence, variance, simple bands, contribution, rank, Top N, selectors, dynamic titles, display folders, descriptions, and hidden raw fields.

Do not use DAX as ETL. Heavy joins, deduplication, cleansing, or snapshot creation belong upstream or outside the MVP.

## Modeling Guardrails

Prefer star schema. Each table must declare role, grain, key/relationship path, and fact/dimension intent. Each public metric must declare `aggregation_semantics` and `time_behavior`.

Use a governed Date table/date role before Time View calculation groups. For multiple date roles, declare the active role and avoid uncontrolled `USERELATIONSHIP` proliferation.

## Storage Mode Guardrails

Current quick-win mode: Import.
Future candidates: Import or Direct Lake.
Avoid DirectQuery by default. DirectQuery requires explicit approval, predictable source performance, few visuals, controlled queries, and no cross-source joins.
