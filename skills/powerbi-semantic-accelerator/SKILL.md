---
name: powerbi-semantic-accelerator
description: "Catalog-first Power BI semantic model engineering for PBIP/TMDL, DAX measures, calculation groups, star-schema contracts, metric/display/selector/source catalogs, semantic requests, reusable dashboards, and quick-win self-service workflows. Use Databricks batch -> PostgreSQL snapshot -> Power BI Import. Do not use for Databricks Serverless/DirectQuery serving, semantic forks, ad hoc report JSON rewrites, uncataloged user DAX, or non-Power BI analytics. Output patches, validation commands, smoke-test DAX, and dependency notes."
---

# Power BI Semantic Accelerator

## Goal

Build AI-maintained Power BI semantic-layer MVPs: accurate, catalog-governed, quick to ship, safe to evolve; optimize for quality-adjusted token ROI.

## Use When

```text
PBIP/TMDL semantic model
DAX measure/calculation group
model/source/metric/display/selector catalog
user semantic request -> governed catalog patch
Metric Explorer/thin dashboard reuse
Databricks batch -> PostgreSQL snapshot -> Power BI Import
```

## Do Not Use When

```text
Databricks Serverless/DirectQuery BI serving
dual-source DirectQuery
semantic model fork without reuse proof
uncataloged user DAX/model edit
large undocumented PBIP report JSON rewrite
non-Power BI analytics work
```

## Inputs

```text
PBIP/TMDL path
spec catalog path
user semantic request
source binding details
validation/publish constraints
```

## Outputs

```text
catalog-first patch plan
TMDL/DAX patch or generator command
validation command/result
smoke-test DAX query
unresolved dependency list
```

Default path:

```text
Databricks batch preprocessing, if needed
  -> PostgreSQL D-1 snapshot / approved bi_* import tables
  -> Power BI Import semantic model
  -> PBIP/TMDL + governed DAX + selectors
  -> Metric Explorer + thin dashboards
```

## Core Principle

Semantic model = product. Reports = thin consumers.

Source of truth:

```text
spec catalogs + PBIP/TMDL in Git
  -> generated/reviewed DAX/TMDL
  -> local PBIX publish allowed for v0.1
  -> shared semantic model / thin reports when reuse is proven
```

## Rules

```text
PBI.001 | MUST  | metrics      | every business KPI = explicit measure
PBI.002 | NEVER | visuals      | business KPI visual -> raw numeric column
PBI.003 | MUST  | catalog      | metric-catalog.yaml precedes public measure
PBI.004 | MUST  | display      | display-catalog.yaml precedes public field/measure exposure
PBI.005 | MUST  | metadata     | public measure has description + format string + display folder
PBI.006 | NEVER | exposure     | expose technical IDs/raw values/ETL/staging/source-system fields
PBI.007 | SHOULD| dax          | approved pattern before custom DAX
PBI.008 | NEVER | report       | broad undocumented PBIP report JSON rewrite
PBI.009 | MUST  | contract     | reference model-contract.yaml fields only
PBI.010 | MUST  | validate     | run spec validation before final model change
PBI.011 | MUST  | source       | v0.1 quick-win model uses Power BI Import
PBI.012 | NEVER | source       | v0.1 depends on Databricks Serverless SQL/DirectQuery/dual-source DirectQuery/live Databricks BI serving
PBI.013 | MAY   | source       | Databricks batch -> delayed PostgreSQL snapshots/import tables when latency is declared
PBI.014 | MUST  | migration    | source migration preserves semantic object names
PBI.015 | MUST  | self-service | Metric Explorer + governed selectors = primary quick-win proof
PBI.016 | MUST  | selectors    | selector option maps to governed measure/calculation item/visible field
PBI.017 | SHOULD| reuse        | second dashboard = thin/live-connected before model fork
PBI.018 | MUST  | user-defined | user semantic request -> catalogs before publish
PBI.019 | SHOULD| publish      | PBIP/TMDL/catalogs = source of truth; PBIX publish allowed for v0.1
PBI.020 | SHOULD| scope        | keep heavy joins/windowing/cleansing/snapshot upstream or shrink MVP; avoid DAX ETL
PBI.021 | MUST  | modeling     | table declares role + grain + key/relationship path + fact/dimension intent
PBI.022 | SHOULD| modeling     | star schema preferred; wide-table shortcut = non-shared POC debt
PBI.023 | SHOULD| selectors    | Field Parameters for visual switching; disconnected selectors for semantic logic
PBI.024 | MUST  | user-defined | request lifecycle: draft -> validated -> compiled -> reviewed -> approved/published/deprecated
PBI.025 | MUST  | metrics      | public self-service metric declares aggregation_semantics + time_behavior
PBI.026 | MUST  | date         | governed date table/date role before time-intelligence calculation groups
PBI.027 | MUST  | migration    | Fabric/Direct Lake binding preserves star-shaped semantic tables + declares fallback/DirectQuery risk
PBI.028 | SHOULD| source       | PostgreSQL snapshots emulate future Gold/semantic serving tables, not raw exports, to keep source migratable
```

## Workflow

1. Query ConPort before loading or searching full skill/reference text when inventory exists.
2. Classify change: source adapter, source binding, model contract, metric, display, selector, DAX/TMDL, report shell, or user request.
3. Patch the smallest upstream artifact first, usually a catalog/request file.
4. Generate or patch TMDL/DAX only from declared catalog entries and model-contract fields.
5. Validate with `scripts/validate_powerbi_semantic_specs.py <specs-dir>` when specs exist.
6. Generate starter measures with `scripts/generate_measures_tmdl.py <specs-dir> --out <file>` when useful; review before applying.
7. Provide a smoke-test DAX query for changed public measures.
8. State unresolved dependencies: gateway, PostgreSQL credentials, Databricks batch job, snapshot latency, or USGov feature availability.

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

## Verification

```text
spec validation: scripts/validate_powerbi_semantic_specs.py <specs-dir>
measure smoke: DAX query for changed public measures
catalog check: metric/display/selector/source/model contract names align
stable prefix: keep global semantic rules stable; vary only target paths/spec excerpts
```

## Failure Modes

```text
missing-spec: required catalog/model contract absent
uncataloged-measure: public measure lacks metric/display entry
unsafe-source: DirectQuery/Serverless dependency appears in v0.1 path
unsafe-report-json: broad undocumented report JSON rewrite requested
blocked-dependency: credentials/gateway/snapshot latency/USGov capability unresolved
```

## References

Load only as needed:

- `references/architecture.md`: source path, migration, reuse, lifecycle, star/Fabric guardrails.
- `references/catalog-contracts.md`: YAML shapes for model/source/metric/display/selector/user-request specs.
- `references/dax-patterns.md`: approved DAX and self-service patterns.
- `references/report-boundary.md`: safe report edits, thin-dashboard reuse, PBIX/PBIP release boundary.

## Output Style

Separate advice into `now`, `next`, and `later`. For code tasks, return only changed files or patches unless the user requests a full skeleton.
