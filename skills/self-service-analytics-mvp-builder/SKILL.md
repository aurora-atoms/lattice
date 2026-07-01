---
name: self-service-analytics-mvp-builder
description: Build or extend a commercial, scenario-specific self-service analytics MVP. Use when a customer/use case is known and the user wants a practical plan, repo scaffold, Fabric/Power BI architecture, semantic model, embedded analytics design, tenant security model, Gold layer contract, action loop, or delivery checklist.
---

# Self-service analytics MVP builder

Use after the customer segment, paid scenario, or first use case is known. Build a narrow decision product:

```text
scenario -> metric contract -> Gold layer -> semantic model -> embedded BI -> action loop -> telemetry
```

Optimize for validation, metric trust, tenant safety, and speed.

## Priority Order

1. Narrow the first decision loop.
2. Make metrics explicit and versioned.
3. Enforce tenant isolation from the first data contract.
4. Store workflow state in the product app/database, not only Power BI.
5. Ship a useful embedded experience before adding broad self-service or AI.
6. Track refresh, usage, actions, and metric changes.

## First pass

For any implementation or design request:

1. Identify or assume: target role, one recurring decision, 3-5 business questions, 5-10 metrics, 2-4 dimensions, and one action loop.
2. If details are missing, make plausible placeholders and mark them `TODO` unless the missing fact blocks implementation.
3. Recommend the smallest feasible scope for one vertical scenario.
4. Produce concrete repo/file changes or run the scaffold script when files are requested.

Avoid long platform surveys. Explain alternatives only when they affect the immediate MVP decision.

## Defaults

Use unless the user specifies otherwise:

- App: React or Next.js.
- Product DB: PostgreSQL or Azure SQL for tenants, users, roles, configuration, workflow, audit, embed/usage events, and metric metadata.
- Platform: Microsoft Fabric Lakehouse or Warehouse; Dataflow Gen2 and Pipelines first; Spark only for complex logic.
- BI: Power BI semantic model and reports. Start Import; move to Direct Lake for Fabric scale; use DirectQuery only when required.
- Embed: app-owns-data for SaaS/external customers; user-owns-data for internal enterprise.
- Security: tenant key on every product-facing fact/snapshot, RLS by default, OLS only for sensitive objects, workspace isolation only when needed.
- AI: defer until the semantic model is stable.

## Build Sequence

When creating or extending a repo, work in this order:

1. Docs/contracts: product scope, metric contract, Gold layer contract, semantic model plan, security plan, delivery checklist.
2. Product storage: tenants, users, roles, metric definitions, saved views, insights, actions, notes, audit, embed/usage events.
3. Analytics contracts: Gold grain/columns, metrics, allowed dimensions, RLS fields, model naming, report page inventory.
4. App shell: overview/dashboard, entity detail, action queue or insight feed, admin/configuration.
5. Embed: backend token generation, app user -> tenant/role -> RLS mapping, report/page/filter boundaries.
6. Validate: RLS test matrix, refresh/usage telemetry, metric/model versioning, demo path.

## Scaffold script

Use for starter files or a repo scaffold:

```bash
python3 scripts/create_mvp_repo.py --target /path/to/repo --scenario "usage intelligence" --mode extend
```

Options: `--target`, `--scenario`, `--mode new|extend`, `--force`. After running it, inspect generated files and summarize the next customization points.

## Hard rules

- Start from business questions, not available source tables.
- Do not expose raw tables to business users.
- Treat the semantic model as the analytics API; keep Gold tables decision-oriented and report/action-loop friendly.
- Every metric needs name, definition, grain, owner, source, refresh cadence, allowed dimensions, RLS impact, and version.
- Every product-facing fact/snapshot table needs a tenant/customer isolation key.
- Store notes, tasks, comments, subscriptions, configuration, and audit logs in the product database.
- Keep v1 self-service constrained: filters, drill-through, configurable views, and certified model exploration before custom BI.
- Add AI only over curated metrics and governed semantic model metadata; track product usage from day one.

## Response template

Use for plans unless a shorter answer or code edit is better:

MVP boundary; architecture choice; repo changes; data and Gold layer; semantic model and metrics; embedded BI; security and multi-tenancy; action loop; observability; next steps.

Keep sections brief and actionable.

## Reference routing

Load only the reference needed for the current request:

- `references/mvp-workflow.md`: scope control, build sequence, definition of done.
- `references/repo-blueprint.md`: repo structure and generated file purposes.
- `references/semantic-model.md`: metric contract, Gold tables, DAX/model naming, AI-ready metadata.
- `references/security-embedded.md`: Power BI Embedded, RLS, tenant isolation, workspace strategy.
- `references/platform-decisions.md`: Fabric, storage mode, transformation, environment, and cost tradeoffs.
