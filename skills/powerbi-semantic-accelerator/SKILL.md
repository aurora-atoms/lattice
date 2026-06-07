---
name: powerbi-semantic-accelerator
description: catalog-driven Power BI semantic model engineering for AI coding agents. Use when creating, reviewing, or modifying PBIP/TMDL projects, DAX measures, calculation groups, star-schema model contracts, metric/display/selector/source catalogs, user semantic requests, reusable dashboards, or quick-win self-service semantic-layer workflows using Databricks batch preprocessing to PostgreSQL snapshots and Power BI Import while avoiding Databricks Serverless, DirectQuery, semantic forks, and uncontrolled report JSON edits.
---

# Power BI Semantic Accelerator

Use this skill to build an AI-maintained Power BI semantic-layer MVP that is quick to ship and safe to evolve.

Default path:

```text
Databricks batch preprocessing, if needed
  -> PostgreSQL D-1 snapshot / approved bi_* import tables
  -> Power BI Import semantic model
  -> PBIP/TMDL + governed DAX + selectors
  -> Metric Explorer + thin dashboards
```

## Core Principle

Treat the semantic model as the product. Treat reports as thin consumers.

Source of truth:

```text
spec catalogs + PBIP/TMDL in Git
  -> generated/reviewed DAX/TMDL
  -> local PBIX publish allowed for v0.1
  -> shared semantic model / thin reports when reuse is proven
```

## Rules

```text
PBI.001 | MUST  | metrics      | Define every business KPI as an explicit measure. | reject implicit KPI use
PBI.002 | NEVER | visuals      | Bind visuals directly to raw numeric columns for business KPIs. | block
PBI.003 | MUST  | catalog      | Update metric-catalog.yaml before adding public measures. | reject uncataloged measures
PBI.004 | MUST  | display      | Update display-catalog.yaml before exposing public fields/measures. | reject ungoverned objects
PBI.005 | MUST  | metadata     | Give every public measure description, format string, and display folder. | reject incomplete metadata
PBI.006 | NEVER | exposure     | Expose technical IDs, raw values, ETL fields, staging fields, or source-system fields. | hide
PBI.007 | SHOULD| dax          | Reuse approved DAX patterns before custom DAX. | prefer pattern reuse
PBI.008 | NEVER | report       | Freely rewrite undocumented PBIP report JSON. | block except approved small patch
PBI.009 | MUST  | contract     | Reference only fields declared in model-contract.yaml. | reject
PBI.010 | MUST  | validate     | Run spec validation before final model changes. | enforce
PBI.011 | MUST  | source       | Use Power BI Import for v0.1 quick-win semantic models. | block DirectQuery unless approved
PBI.012 | NEVER | source       | Depend on Databricks Serverless SQL, Databricks DirectQuery, dual-source DirectQuery, or live Databricks BI serving for v0.1. | block
PBI.013 | MAY   | source       | Use Databricks batch preprocessing to create delayed PostgreSQL snapshots/import tables. | allow with latency declared
PBI.014 | MUST  | migration    | Preserve semantic object names across source migrations. | enforce stable contract
PBI.015 | MUST  | self_service | Treat Metric Explorer and governed selectors as the primary quick-win proof. | enforce
PBI.016 | MUST  | selectors    | Map every selector option to a governed measure, calculation item, or visible field. | reject unsafe options
PBI.017 | SHOULD| reuse        | Build second dashboards as thin reports/live-connected reuse before model forks. | prefer shared model reuse
PBI.018 | MUST  | user_defined | Convert user semantic requests into catalogs first; never publish arbitrary user DAX/model edits. | enforce compilation
PBI.019 | SHOULD| publish      | Keep PBIP/TMDL/catalogs as source of truth; allow PBIX publish for v0.1. | pragmatic release
PBI.020 | SHOULD| scope        | Push heavy joins, windowing, cleansing, and snapshot creation upstream or shrink MVP scope. | avoid ETL in DAX
PBI.021 | MUST  | modeling     | Each model table declares role, grain, key/relationship path, and fact/dimension intent. | enforce star contract
PBI.022 | SHOULD| modeling     | Prefer star schema; mark wide-table shortcuts as non-shared POC debt. | prevent future debt
PBI.023 | SHOULD| selectors    | Prefer Field Parameters for visual measure/dimension switching; use disconnected selectors for custom semantic logic. | prefer native self-service
PBI.024 | MUST  | user_defined | Move user requests through draft -> validated -> compiled -> reviewed -> approved/published/deprecated. | enforce lifecycle
PBI.025 | MUST  | metrics      | Declare aggregation_semantics and time_behavior for every self-service public metric. | prevent wrong aggregation
PBI.026 | MUST  | date         | Define governed date table/date role before time-intelligence calculation groups. | prevent ambiguity
PBI.027 | MUST  | migration    | Future Fabric/Direct Lake bindings preserve star-shaped semantic tables and declare fallback/DirectQuery risk. | future-proof migration
PBI.028 | SHOULD| source       | PostgreSQL snapshots emulate future Gold/semantic serving tables, not raw exports. | keep source migratable
```

## Workflow

1. Classify the change: source adapter, source binding, model contract, metric, display, selector, DAX/TMDL, report shell, or user request.
2. Patch the smallest upstream artifact first, usually a catalog/request file.
3. Generate or patch TMDL/DAX only from declared catalog entries and model-contract fields.
4. Validate with `scripts/validate_powerbi_semantic_specs.py <specs-dir>` when specs exist.
5. Generate starter measures with `scripts/generate_measures_tmdl.py <specs-dir> --out <file>` when useful; review before applying.
6. Provide a smoke-test DAX query for changed public measures.
7. State unresolved dependencies: gateway, PostgreSQL credentials, Databricks batch job, snapshot latency, or USGov feature availability.

## Routing

```text
new KPI                  -> metric + display catalogs -> TMDL/DAX -> smoke test
new dimension            -> model + display + selector catalogs -> TMDL
new import source        -> source/model contract first; no raw messy binding
future source migration  -> source binding first; keep semantic names stable
new dashboard            -> reuse existing semantic model; add report blueprint first
user semantic request    -> semantic-request.yaml -> validation -> catalog patches -> TMDL/DAX
```

## MVP Boundary

```text
source: PostgreSQL snapshot / approved import tables, optionally produced by Databricks batch
model: one PBIP/TMDL semantic model
shape: star-schema-aware contract with grain, keys, date role, aggregation semantics
metrics: 8-10 explicit measures
calculation groups: one Time View group
self-service: Metric Explorer first, Manager Overview second
release: Git source + optional local PBIX publish
reuse proof: one second thin dashboard using the same semantic model
```

Do not escalate to certified models, separate workspaces, full deployment pipelines, DAX UDFs, multi-agent orchestration, or report JSON generation unless the user asks for v1+ governance.

## References

Load only as needed:

- `references/architecture.md`: source path, migration, reuse, lifecycle, star/Fabric guardrails.
- `references/catalog-contracts.md`: YAML shapes for model/source/metric/display/selector/user-request specs.
- `references/dax-patterns.md`: approved DAX and self-service patterns.
- `references/report-boundary.md`: safe report edits, thin-dashboard reuse, PBIX/PBIP release boundary.

## Output Style

Separate advice into `now`, `next`, and `later`. For code tasks, return only changed files or patches unless the user requests a full skeleton.
