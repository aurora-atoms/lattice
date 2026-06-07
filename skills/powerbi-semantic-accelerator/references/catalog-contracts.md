# Catalog Contracts

YAML is a human/AI manifest, not the final database schema. Validate YAML, then generate or patch TMDL.

## Files

```text
model-contract.yaml   -> Power BI-facing tables/fields, star contract, date role, source policy
source-catalog.yaml   -> optional current/future source profiles and bindings
metric-catalog.yaml   -> public measures and patterns
display-catalog.yaml  -> visibility, names, descriptions, folders
selector-catalog.yaml -> governed self-service selectors
semantic-request.yaml -> governed user change request
```

## model-contract.yaml

```yaml
source_policy:
  powerbi_mode: import
  serving_source: postgresql_snapshot
  upstream_preprocessing: databricks_batch_allowed
  snapshot_latency: D-1 daily
  directquery_allowed: false
  databricks_runtime_dependency: false
  future_rebind_allowed: true

semantic_contract:
  stability_level: stable_for_reports
  preserve_object_names: true
  breaking_change_policy: require_review

tables:
  - name: Fact_MetricSnapshot
    source_view: bi_metric_snapshot_daily
    source_profile: current_postgres_snapshot
    role: fact
    grain: one row per entity per metric date
    key: Metric Snapshot Id
    date_role: Metric Date
    additive_behavior: mixed
    relationship_path:
      - Dim_Date[Date] -> Fact_MetricSnapshot[Metric Date]
      - Dim_Entity[Entity Id] -> Fact_MetricSnapshot[Entity Id]
    migration_key: metric_snapshot
    columns:
      - name: Entity Id
        role: key
        data_type: string
        hidden: true
        source_column: entity_id
      - name: Metric Date
        role: date
        data_type: date
        source_column: metric_date
      - name: Score Value
        role: numeric_raw
        data_type: decimal
        hidden: true
        source_column: score_value
      - name: Entity Weight
        role: numeric_raw
        data_type: decimal
        hidden: true
        source_column: entity_weight

  - name: Dim_Entity
    source_view: bi_entity
    source_profile: current_postgres_snapshot
    role: dimension
    grain: one row per entity
    key: Entity Id
    relationship_path:
      - Dim_Entity[Entity Id] -> Fact_MetricSnapshot[Entity Id]
    migration_key: entity
    columns:
      - name: Entity Id
        role: key
        data_type: string
        hidden: true
        source_column: entity_id
      - name: Entity Name
        role: label
        data_type: string
        source_column: entity_name
```

Rules: declare table role, grain, key/relationship path, date role for facts, source profile, and hidden technical fields.

## source-catalog.yaml

```yaml
source_profiles:
  - id: current_postgres_snapshot
    type: postgresql
    powerbi_mode: import
    snapshot_latency: D-1 daily
    runtime_dependency: true
    directquery_allowed: false

  - id: future_fabric_directlake
    type: fabric_directlake
    runtime_dependency: false
    storage_mode_candidate: direct_lake
    expected_shape: star_delta_tables
    fallback_risk: must_be_assessed
    directquery_allowed: false

bindings:
  - semantic_table: Fact_MetricSnapshot
    migration_key: metric_snapshot
    active_profile: current_postgres_snapshot
    active_object: bi_metric_snapshot_daily
    future_bindings:
      - profile: future_fabric_directlake
        object: MetricSnapshotDaily
```

Rules: active profiles must exist; future bindings must preserve semantic names and declare fallback risk when Fabric/Direct Lake is involved.

## metric-catalog.yaml

```yaml
metrics:
  - id: powerscore
    object_name: PowerScore
    display_name: PowerScore
    type: base_measure
    pattern: weighted_average
    fact_table: Fact_MetricSnapshot
    value_column: Score Value
    weight_column: Entity Weight
    format: "0.0"
    display_folder: Metric/Core
    description: Weighted score across selected entities.
    self_service: true
    reuse_scope: shared_model
    aggregation_semantics: weighted_average
    time_behavior: snapshot

  - id: entity_count
    object_name: Entity Count
    display_name: Entity Count
    type: base_measure
    pattern: distinct_count
    table: Fact_MetricSnapshot
    column: Entity Id
    format: "#,##0"
    display_folder: Metric/Core
    description: Count of entities in the current filter context.
    self_service: true
    reuse_scope: shared_model
    aggregation_semantics: distinct_count
    time_behavior: snapshot
```

Rules: unique ids/names; public metrics require description, format, folder, aggregation semantics, and time behavior. Supported semantics: `additive`, `semi_additive`, `non_additive`, `ratio`, `weighted_average`, `distinct_count`, `count`. Supported time behavior: `flow`, `balance`, `snapshot`, `period_end`, `average_over_period`, `point_in_time`.

## display-catalog.yaml

```yaml
objects:
  - object: "[PowerScore]"
    display_name: PowerScore
    visible: true
    folder: Metric/Core
    description: Weighted score across selected entities.
  - object: Fact_MetricSnapshot[Score Value]
    visible: false
    reason: Raw numeric column exposed only through measures.
```

Rules: visible objects need display name and description; visible measures need folder; hidden objects need reason.

## selector-catalog.yaml

```yaml
selectors:
  - id: metric_selector
    table_name: Metric Selector
    selector_type: metric
    implementation: field_parameter
    fallback_implementation: disconnected_selector
    options:
      - key: score
        display_name: PowerScore
        measure: PowerScore
        default: true
      - key: entity_count
        display_name: Entity Count
        measure: Entity Count

  - id: dimension_selector
    table_name: Dimension Selector
    selector_type: dimension
    implementation: field_parameter
    options:
      - key: entity
        display_name: Entity
        field: Dim_Entity[Entity Name]
```

Rules: selector options must map to governed measures or visible fields. Prefer Field Parameters for visual switching; use disconnected selectors for custom semantic logic.

## semantic-request.yaml

```yaml
request:
  id: req_metric_001
  status: draft
  requested_by: business_user
  purpose: Add a self-service risk count metric.
  lifecycle:
    current_state: draft
    allowed_next_states: [validated, rejected]
  requested_metric:
    display_name: Risk Count
    business_definition: Count entities with risk events in the current filter context.
    desired_pattern: distinct_count
    source_requirements:
      table: Fact_MetricSnapshot
      column: Entity Id
    self_service: true
    dashboard_usage: [Metric Explorer]
```

Rules: requests compile into catalog patches after validation. Users do not publish arbitrary DAX/model changes.
