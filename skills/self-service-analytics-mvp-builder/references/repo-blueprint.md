# Repo Blueprint

## Recommended structure

```text
repo/
  apps/
    web/                         # react/next.js product shell
  packages/
    analytics-contracts/          # metric, gold table, semantic model contracts
    shared/                       # shared types and utilities
  db/
    migrations/                   # product database schema
  fabric/                         # pipeline/lakehouse/warehouse contracts
  powerbi/
    reports/                      # report inventory, not binary pbix unless desired
    semantic-model/               # semantic model documentation and measure inventory
  docs/
    000-product-scope.md
    010-metric-contract.md
    020-semantic-model.md
    030-security-multitenancy.md
    040-delivery-plan.md
    050-validation-checklist.md
```

## Product database tables

Use a product DB for app state and workflow, separate from analytics facts:

- tenants
- users
- tenant_memberships
- roles
- metric_definitions
- saved_views
- insight_events
- action_items
- notes
- audit_events
- embed_sessions
- usage_events

## Analytics contract files

Keep analytics contracts in repo even when Fabric assets are managed in the Fabric workspace:

- Gold table grain, columns, and tenant key
- RLS fields
- metric definitions and versions
- allowed dimensions
- semantic model naming conventions
- report page inventory
- refresh cadence
- ownership

## Generated scaffold intent

The scaffold should not pretend to be a complete app. It creates repo shape and product contracts so implementation starts from business semantics, tenant safety, and action loops instead of ad hoc dashboards.
