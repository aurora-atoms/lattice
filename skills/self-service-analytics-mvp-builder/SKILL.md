---
name: self-service-analytics-mvp-builder
description: build or extend a code repository for a commercial, scenario-specific self-service analytics mvp. use when the user wants to turn a known customer/use case into a fast implementation plan, repo scaffold, fabric/power bi architecture, semantic model, embedded analytics design, multi-tenant security model, gold layer contract, action queue, insight feed, or mvp delivery checklist. optimized for microsoft fabric, power bi embedded, react/next.js, semantic models, rls, and productized analytics workflows.
---

# Self-service analytics MVP builder

Use this skill to help create or extend a repo for a productized analytics MVP after the customer, paid scenario, and first use case are already known.

## Core principle

Do not design a generic BI platform. Build a narrow decision product:

`business scenario -> metric contract -> gold layer -> semantic model -> embedded BI -> workflow/action loop -> telemetry`

Optimize for speed, correctness, tenant safety, and commercial validation.

## Default architecture

Use this default unless the user gives a different stack:

- Frontend: React or Next.js product shell.
- Product database: PostgreSQL or Azure SQL for tenants, users, roles, configuration, notes, actions, audit logs, and metric metadata.
- Data platform: Microsoft Fabric Lakehouse or Warehouse.
- Transformation: Dataflow Gen2 and Fabric Pipeline first; Notebook/Spark only for complex logic.
- BI: Power BI semantic model plus report pages; Direct Lake when using Fabric tables and performance needs justify it, Import for earliest prototypes, DirectQuery only when required.
- Embedding: Power BI Embedded app-owns-data for SaaS/external customers; user-owns-data for internal enterprise scenarios.
- Security: tenant_id/customer_id in every product-facing fact table, RLS by default, OLS only for sensitive columns/tables, workspace isolation for large or regulated customers.
- AI: add after semantic model is stable; start with chart explanation, metric-change explanation, curated insight summaries, and rule-based recommendations.

## First-response workflow

When asked to implement, extend, or design a repo:

1. Identify the scenario boundary:
   - target user role
   - first decision/job-to-be-done
   - first 3-5 questions the product must answer
   - first 5-10 metrics
   - first 2-4 dimensions
   - first action loop
2. If the user has not provided these, make a best-effort placeholder instead of blocking unless the missing detail would make implementation impossible.
3. Recommend an MVP scope that fits one vertical scenario, not a generic dashboard builder.
4. Produce a repo-level implementation plan and file/module changes.
5. Use `scripts/create_mvp_repo.py` when the user wants a scaffold or wants files added to an existing repo.

## Repo creation workflow

For a new or existing repo, follow this sequence:

1. Create or update documentation first:
   - product scope
   - metric contract
   - semantic model plan
   - security/multi-tenancy plan
   - delivery checklist
2. Create product metadata and workflow storage:
   - tenants
   - users
   - roles
   - metric definitions
   - saved views
   - insights
   - actions
   - notes
   - audit events
3. Create analytics contracts:
   - gold table contract
   - metric definitions
   - semantic model naming conventions
   - RLS requirements
4. Create app shell placeholders:
   - dashboard route
   - entity detail route
   - action queue route
   - admin/config route
5. Add Power BI Embedded guidance:
   - app-owns-data flow
   - service principal/embed token boundary
   - tenant filters/RLS mapping
6. Add deployment and observability checklist:
   - dev/test/prod environments
   - refresh logs
   - usage telemetry
   - metric versioning
   - semantic model versioning

## Using the scaffold script

Run the bundled script when the user wants starter files:

```bash
python scripts/create_mvp_repo.py --target /path/to/repo --scenario "usage intelligence" --mode extend
```

Options:

- `--target`: repo root or target directory.
- `--scenario`: short use case name.
- `--mode new|extend`: use `extend` for existing repos.
- `--force`: overwrite files created by the scaffold.

After running it, inspect the generated files and explain what to customize next.

## Critical design rules

- Start from the business questions, not from available data tables.
- Do not expose raw tables to business users.
- Treat the semantic model as the product API for analytics.
- Keep Gold tables page-oriented and decision-oriented.
- Make every metric explicit: name, definition, grain, owner, source, refresh cadence, allowed dimensions, RLS impact, version.
- Put `tenant_id` or equivalent isolation key into every product-facing fact table.
- Separate product workflow data from analytics source data.
- Do not put notes, tasks, comments, subscriptions, or audit logs only inside Power BI; store them in the product database.
- Avoid unrestricted custom BI in v1. Offer filters, drill-through, configurable views, and certified model exploration first.
- Add AI only on top of curated data and metric definitions.
- Track product usage from day one.

## MVP output template

When producing a plan, use this structure unless the user asks for another format:

1. MVP boundary
2. Architecture choice
3. Repo changes
4. Data model and Gold layer
5. Semantic model and metrics
6. Power BI/Embedded design
7. Security and multi-tenancy
8. Action loop and product workflow
9. Observability and CI/CD
10. Next implementation steps

## References

Load these only when relevant:

- `references/mvp-workflow.md`: end-to-end build sequence and MVP scope control.
- `references/repo-blueprint.md`: recommended repo structure and generated file purposes.
- `references/semantic-model.md`: metric contract, semantic model, DAX and naming conventions.
- `references/security-embedded.md`: Power BI Embedded, RLS, tenant isolation and workspace strategy.
- `references/platform-decisions.md`: Fabric/Power BI implementation tradeoffs.
