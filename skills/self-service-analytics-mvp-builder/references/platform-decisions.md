# Platform Decisions

Use this reference only when the stack choice is still open or a Fabric/Power BI tradeoff affects the MVP.

## Fabric Lakehouse vs Warehouse

Use Lakehouse when:

- source data is file/event/log-heavy
- Spark or notebook transformations are useful
- Direct Lake over Delta tables is desired
- medallion architecture is central

Use Warehouse when:

- SQL-first transformations and serving are preferred
- team is more comfortable with T-SQL
- BI serving and relational modeling dominate

Most MVPs should start with one serving pattern and evolve later. Avoid duplicating every table into both unless needed.

## Direct Lake vs Import vs DirectQuery

Use Import when:

- MVP speed matters most
- data volume is small to medium
- refresh cadence is daily/hourly

Use Direct Lake when:

- data is in Fabric/OneLake Delta tables
- interactive performance over larger data matters
- avoiding duplicated BI storage matters

Use DirectQuery when:

- data cannot be imported/copied
- freshness requirements are strict
- source system can handle query load

Do not default to DirectQuery for dashboards.

## Transformation defaults

- Use Dataflow Gen2 for straightforward ingestion/transform work.
- Use Pipelines for orchestration.
- Use Notebooks/Spark for complex joins, event processing, or advanced transformations.
- Use SQL for Gold serving logic when simpler and more maintainable.

## Environments

Use at least:

- dev workspace
- test workspace
- prod workspace

Track Fabric items in Git when possible and use deployment pipelines for controlled promotion.

## Cost and capacity

Track:

- refresh duration
- interactive report performance
- capacity usage
- number of tenants
- embedded sessions
- report queries
- data volume growth

Capacity surprises can break SaaS margins. Add basic cost telemetry early.
