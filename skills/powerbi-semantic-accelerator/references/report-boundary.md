# Report Boundary

## Safe AI Edits

- TMDL semantic files
- catalog YAML files
- DAX measures
- calculation groups
- selector definitions
- display folders, descriptions, format strings
- documentation and report blueprints
- validation scripts

## Risky AI Edits

Do not rewrite PBIP report visual JSON unless the patch is explicit, small, reversible, and the PBIP can be opened in Power BI Desktop immediately after.

## Release Stages

### v0.1 quick win

- Create initial report shell in Power BI Desktop.
- Keep pages minimal: Metric Explorer, then Manager Overview.
- Use PBIP/TMDL/catalogs as source of truth.
- Allow local PBIX save/publish as release carrier.
- Let AI maintain semantic model/catalogs first, not visual layout JSON.

### v0.2 reuse proof

- Create a second thin dashboard using the same semantic model.
- Do not duplicate or fork measures.
- Add missing reusable measures through catalogs/TMDL only if needed.

### v0.3 user-defined semantic request

- Accept one controlled `semantic-request.yaml`.
- Compile to catalog patches, then TMDL/DAX.
- Publish after review through the same PBIX/shared semantic path.

## Thin Dashboard Flow

```text
1. Define dashboard purpose and required metrics/dimensions.
2. Check metric/display/selector catalogs for reuse.
3. Add missing reusable measures only when necessary.
4. Build/report a blueprint using existing measures/selectors.
5. Publish as thin/live-connected report when possible.
6. Reject model forks unless explicitly requested.
```

## User Request Publishing Flow

```text
business input
  -> semantic-request.yaml
  -> validate fields, measures, display names, selector eligibility
  -> compile to model/metric/display/selector patches
  -> generate TMDL/DAX
  -> BI review + PBIP/PBIX validation
  -> quick-win PBIX or shared-model release
```

Users may define business definitions, display names, selector intent, and dashboard usage. Users may not directly publish DAX, credentials, raw field exposure, or hidden-field changes.

## Blueprint Example

```yaml
pages:
  - id: metric_explorer
    display_name: Metric Explorer
    purpose: controlled self-service exploration
    controls: [metric selector, dimension selector, time selector, top n selector]
  - id: manager_overview
    display_name: Manager Overview
    purpose: executive summary
    visuals:
      - { id: card_score, type: card, measure: PowerScore }
      - { id: trend_score, type: line_chart, x: Dim_Date[Month], y: PowerScore }
  - id: second_dashboard
    display_name: Operations Dashboard
    purpose: reuse proof
    semantic_model: shared_metric_model
    reuse_requirement: no duplicated semantic model
```
