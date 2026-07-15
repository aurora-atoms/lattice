---
name: self-service-analytics-mvp-builder
description: Build or extend a commercial, scenario-specific self-service analytics MVP from input sources such as customer requirements, existing repo files, metric definitions, data contracts, and architecture constraints while preserving existing behavior, metric semantics, tenant isolation, validation, and safety. Use when a customer or use case is known and the user wants output such as a practical plan, repo scaffold, Fabric or Power BI architecture, semantic model, embedded analytics design, tenant security model, Gold layer contract, action loop, or delivery checklist. Do not use for broad platform surveys, raw-table exposure, unbounded BI transformation, production deployment without approval, or AI features before the semantic model is governed.
---

# Self-service analytics MVP builder

## Goal

Build a narrow, trustworthy decision product for one paid scenario. Prefer a runnable vertical slice over a broad analytics platform plan.

Use after the customer segment, paid scenario, or first use case is known. Build a narrow decision product:

```text
scenario -> metric contract -> Gold layer -> semantic model -> embedded BI -> action loop -> telemetry
```

Optimize for validation, metric trust, tenant safety, and speed.

## Use When

Use this skill when the target customer or use case is known and the request involves one or more of these outcomes:

- Bound an analytics MVP around a recurring business decision.
- Plan or scaffold a repo for Fabric, Power BI, embedded analytics, or a supporting product app.
- Define Gold-layer, semantic-model, metric, tenant-security, action-loop, or delivery contracts.
- Extend an existing MVP while preserving its established behavior and interfaces.

## Do Not Use When

Do not use this skill for generic platform comparisons, unconstrained enterprise data-platform design, direct exposure of raw source tables, or production deployment without explicit approval. Do not add AI over ungoverned metrics or bypass tenant isolation, semantic contracts, validation, or human review boundaries.

## Inputs

Use the smallest available input set needed for the requested outcome:

- Customer segment, user role, paid scenario, and recurring decision.
- Existing repo files, architecture constraints, source summaries, and delivery requirements.
- Business questions, metric definitions, Gold-layer contracts, semantic-model artifacts, security constraints, and action-loop needs.
- Approved placeholders when details are missing and implementation is not blocked.

Query ConPort before loading or searching full skill or reference text when a relevant inventory exists. If ConPort is unavailable, stale, or incomplete, inspect only the targeted repo files and routed references needed for the task.

## Outputs

Produce only the artifacts required by the request, such as:

- A bounded MVP plan, architecture decision, or delivery checklist.
- Concrete repo changes or a runnable scaffold.
- Metric, Gold-layer, semantic-model, embedded-BI, tenant-security, telemetry, or action-loop contracts.
- A validation summary with assumptions, unresolved risks, and next customization points.

## Priority Order

1. Narrow the first decision loop.
2. Make metrics explicit and versioned.
3. Enforce tenant isolation from the first data contract.
4. Store workflow state in the product app/database, not only Power BI.
5. Ship a useful embedded experience before adding broad self-service or AI.
6. Track refresh, usage, actions, and metric changes.

## Workflow

For any implementation or design request:

1. Retrieve only relevant prior context and targeted source files.
2. Identify or assume the target role, one recurring decision, 3-5 business questions, 5-10 metrics, 2-4 dimensions, and one action loop.
3. Mark plausible placeholders `TODO` when details are missing unless the missing fact blocks safe implementation.
4. Recommend the smallest feasible scope for one vertical scenario.
5. Select only the references needed for the immediate design or implementation decision.
6. Produce concrete repo changes or run the scaffold script when files are requested.
7. Verify contracts, tenant isolation, metric semantics, runnable behavior, and the demo path before reporting completion.

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

## Rules

SSAMVP.001 | MUST | scope | start from business questions and one recurring decision
SSAMVP.002 | NEVER | exposure | expose raw source tables directly to business users
SSAMVP.003 | MUST | model | treat the semantic model as the analytics API and keep Gold tables decision-oriented
SSAMVP.004 | MUST | metrics | define each metric with name, definition, grain, owner, source, refresh cadence, allowed dimensions, RLS impact, and version
SSAMVP.005 | MUST | security | include a tenant or customer isolation key on every product-facing fact or snapshot
SSAMVP.006 | MUST | state | store workflow state, configuration, and audit records in the product database
SSAMVP.007 | SHOULD | self-service | constrain v1 to governed filters, drill-through, configurable views, and certified model exploration
SSAMVP.008 | NEVER | AI | add AI over uncurated metrics or ungoverned semantic metadata
SSAMVP.009 | MUST | quality | preserve existing behavior, metric semantics, tenant boundaries, validation, and safety
SSAMVP.010 | MUST | tokens | optimize quality-adjusted token ROI and load only task-relevant references
SSAMVP.011 | SHOULD | prompt | keep a stable prefix for shared rules and put scenario-specific inputs in the dynamic suffix
SSAMVP.012 | NEVER | completion | claim completion without runnable evidence or a clearly identified documentation-only outcome

## Response template

Use for plans unless a shorter answer or code edit is better:

MVP boundary; architecture choice; repo changes; data and Gold layer; semantic model and metrics; embedded BI; security and multi-tenancy; action loop; observability; next steps.

Keep sections brief and actionable.

## Verification

Before returning:

- Confirm the output traces to one target role, recurring decision, bounded scenario, and action loop.
- Confirm every proposed public metric has explicit semantics and every product-facing fact or snapshot has tenant isolation.
- Confirm generated repo files exist and run the narrowest relevant checks; inspect generated output before summarizing it.
- Confirm embedded access maps app users to tenant and role boundaries without exposing raw source data.
- Confirm assumptions, `TODO` placeholders, unresolved risks, and production actions requiring approval are explicit.
- Run `python3 scripts/validate_skill_package.py --root skills/self-service-analytics-mvp-builder` after editing this skill package.

## Failure Modes

- Broadening the MVP into a platform roadmap without a first decision loop.
- Starting from available tables instead of business questions and metric contracts.
- Treating a dashboard as complete while omitting the action loop, telemetry, or user-usable demo path.
- Mixing tenant data, weakening RLS, or treating workspace separation as the only security control.
- Putting workflow state only in Power BI or making raw source fields part of the public semantic surface.
- Adding AI before metric definitions and semantic metadata are curated and governed.
- Loading every reference or producing long platform surveys when a targeted decision is sufficient.
- Reporting generated scaffolding as complete without inspecting files and running relevant checks.

## References

Load only the reference needed for the current request:

- `references/mvp-workflow.md`: scope control, build sequence, definition of done.
- `references/repo-blueprint.md`: repo structure and generated file purposes.
- `references/semantic-model.md`: metric contract, Gold tables, DAX/model naming, AI-ready metadata.
- `references/security-embedded.md`: Power BI Embedded, RLS, tenant isolation, workspace strategy.
- `references/platform-decisions.md`: Fabric, storage mode, transformation, environment, and cost tradeoffs.
