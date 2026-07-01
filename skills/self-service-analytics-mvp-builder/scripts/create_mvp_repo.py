#!/usr/bin/env python3
"""Create a repo scaffold for a scenario-specific self-service analytics MVP.

The scaffold is intentionally lightweight. It creates contracts, docs, and
placeholders that help teams build Fabric/Power BI/React analytics products
without starting from an ad hoc dashboard.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from textwrap import dedent


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "analytics-mvp"


def titleize(value: str) -> str:
    return " ".join(part.capitalize() for part in re.split(r"[-_\s]+", value.strip()) if part)


def write_file(path: Path, content: str, force: bool) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return f"skip existing: {path}"
    path.write_text(content.strip() + "\n", encoding="utf-8")
    return f"write: {path}"


def scenario_context(scenario: str) -> dict[str, str]:
    slug = slugify(scenario)
    title = titleize(slug)
    return {"slug": slug, "title": title}


def files_for(ctx: dict[str, str]) -> dict[str, str]:
    slug = ctx["slug"]
    title = ctx["title"]
    return {
        "docs/000-product-scope.md": f"""
# {title} MVP product scope

## Target user

- Role: TODO
- Company/customer type: TODO
- Decision cadence: daily / weekly / monthly / event-driven

## First decision loop

Describe the recurring business decision this MVP improves.

## First business questions

1. What changed?
2. Why did it change?
3. Which entities are most affected?
4. What is the risk or opportunity?
5. What action should the user take next?

## MVP pages

- Overview dashboard
- Entity detail page
- Trend/breakdown page
- Action queue
- Admin/configuration page

## Out of scope for v1

- Generic dashboard builder over raw data
- Open-ended custom metric authoring
- Unrestricted AI text-to-SQL
- Complex multi-source connector marketplace
""",
        "docs/010-metric-contract.md": f"""
# Metric contract for {title}

Use this file as the source of truth for MVP metrics.

| metric_id | display_name | business_definition | grain | source_gold_table | allowed_dimensions | refresh_cadence | owner | version |
|---|---|---|---|---|---|---|---|---|
| metric_001 | TODO | TODO | daily/entity | gold_{slug.replace('-', '_')}_daily_snapshot | date, segment, owner | daily | TODO | 0.1 |

## Metric rules

- Every metric must have one business owner.
- Every metric must identify its grain.
- Every metric must identify allowed dimensions.
- Every metric must be versioned when the definition changes.
- Measures in Power BI must map back to this contract.
""",
        "docs/020-semantic-model.md": f"""
# Semantic model plan

## Business entities

- Tenant
- Account / Customer / Entity
- Product / Feature / Item
- User / Owner
- Date
- Action

## Fact tables

- gold_{slug.replace('-', '_')}_daily_snapshot
- gold_{slug.replace('-', '_')}_risk_signal
- gold_action_queue

## Dimensions

- dim_date
- dim_tenant
- dim_account
- dim_product
- dim_owner
- dim_segment

## Measures

- TODO: primary KPI
- TODO: secondary KPI
- TODO: risk count
- TODO: opportunity value
- TODO: action completion rate

## User-facing model rules

- Hide technical keys unless required for drill-through or RLS.
- Use business-friendly table and column names.
- Add descriptions and synonyms for AI-readiness.
- Do not expose raw staging tables.
""",
        "docs/030-security-multitenancy.md": f"""
# Security and multi-tenancy plan

## Isolation model for MVP

Default: shared semantic model with RLS on `tenant_id`.

## Required roles

- platform_admin
- tenant_admin
- manager
- viewer

## RLS checks

- User from tenant A cannot see tenant B.
- Viewer cannot edit/administer configuration.
- Exports and drill-through respect RLS.
- Saved views cannot bypass RLS.

## Embedded analytics

Default SaaS mode: Power BI Embedded app-owns-data.

Backend responsibilities:

- authenticate product user
- resolve tenant and role
- request embed token
- pass effective identity/RLS context
- log embed sessions and report usage
""",
        "docs/040-delivery-plan.md": f"""
# MVP delivery plan

## Phase 1: Contract and prototype

- Confirm target user and first decision loop.
- Define first 5-10 metrics.
- Create sample Gold tables or views.
- Build first Power BI report over certified semantic model.

## Phase 2: Product shell

- Add React/Next.js routes.
- Embed report.
- Add action queue and notes.
- Add tenant/role model.

## Phase 3: Security and telemetry

- Add RLS test cases.
- Add refresh and usage logs.
- Add action completion tracking.

## Phase 4: Customer demo

- Use realistic sample data.
- Show overview -> drill-down -> action loop.
- Collect feedback on metric trust, workflow fit, and willingness to pay.
""",
        "packages/analytics-contracts/gold_layer_contract.yml": f"""
scenario: {slug}
gold_tables:
  - name: gold_{slug.replace('-', '_')}_daily_snapshot
    grain: one row per tenant, entity, and day
    required_columns:
      - tenant_id
      - entity_id
      - snapshot_date
      - primary_metric_value
      - risk_level
      - owner_id
    rls_key: tenant_id
    refresh_cadence: daily
  - name: gold_{slug.replace('-', '_')}_risk_signal
    grain: one row per tenant, entity, signal, and detected timestamp
    required_columns:
      - tenant_id
      - entity_id
      - signal_id
      - detected_at
      - severity
      - explanation
      - recommended_action
    rls_key: tenant_id
    refresh_cadence: daily
""",
        "db/migrations/001_product_core.sql": """
create table if not exists tenants (
  tenant_id text primary key,
  tenant_name text not null,
  status text not null default 'active',
  created_at timestamptz not null default now()
);

create table if not exists users (
  user_id text primary key,
  email text not null unique,
  display_name text,
  created_at timestamptz not null default now()
);

create table if not exists tenant_memberships (
  tenant_id text not null references tenants(tenant_id),
  user_id text not null references users(user_id),
  role_name text not null,
  created_at timestamptz not null default now(),
  primary key (tenant_id, user_id)
);

create table if not exists metric_definitions (
  metric_id text primary key,
  display_name text not null,
  business_definition text not null,
  formula text,
  grain text not null,
  source_gold_table text not null,
  allowed_dimensions jsonb not null default '[]',
  refresh_cadence text not null,
  owner text,
  version text not null default '0.1',
  created_at timestamptz not null default now()
);

create table if not exists saved_views (
  view_id text primary key,
  tenant_id text not null references tenants(tenant_id),
  user_id text not null references users(user_id),
  name text not null,
  config jsonb not null,
  created_at timestamptz not null default now()
);

create table if not exists insight_events (
  insight_id text primary key,
  tenant_id text not null references tenants(tenant_id),
  entity_id text,
  insight_type text not null,
  severity text,
  title text not null,
  explanation text,
  recommended_action text,
  status text not null default 'new',
  created_at timestamptz not null default now()
);

create table if not exists action_items (
  action_id text primary key,
  tenant_id text not null references tenants(tenant_id),
  insight_id text references insight_events(insight_id),
  owner_user_id text references users(user_id),
  title text not null,
  status text not null default 'open',
  priority text,
  due_at timestamptz,
  completed_at timestamptz,
  created_at timestamptz not null default now()
);

create table if not exists notes (
  note_id text primary key,
  tenant_id text not null references tenants(tenant_id),
  entity_id text,
  author_user_id text references users(user_id),
  body text not null,
  created_at timestamptz not null default now()
);

create table if not exists audit_events (
  audit_id text primary key,
  tenant_id text,
  user_id text,
  event_type text not null,
  event_payload jsonb not null default '{}',
  created_at timestamptz not null default now()
);
""",
        "powerbi/semantic-model/README.md": f"""
# Power BI semantic model for {title}

## Required conventions

- Use certified semantic model as the only user-facing analytics layer.
- Hide raw keys and staging fields.
- Add descriptions for tables, columns, and measures.
- Add RLS role mapped to tenant_id.
- Keep measure names aligned with `docs/010-metric-contract.md`.

## First report pages

1. Overview
2. Top movers / exceptions
3. Trend and breakdown
4. Entity detail
5. Action queue

## Storage mode decision

- Start with Import if fastest.
- Move to Direct Lake when Fabric Delta tables and performance needs justify it.
- Avoid DirectQuery unless freshness or source constraints require it.
""",
        "apps/web/README.md": f"""
# Web product shell for {title}

## Suggested routes

- `/` insight feed / executive overview
- `/dashboard` embedded Power BI overview
- `/entities/[id]` entity detail page
- `/actions` action queue
- `/admin/metrics` metric definitions and configuration
- `/admin/security` tenants, users, roles, and RLS mapping

## Keep in the app, not only in Power BI

- authentication and tenant context
- notes
- actions
- saved views
- alerts
- audit logs
- subscriptions and entitlements
- usage telemetry
""",
        ".env.example": """
DATABASE_URL=
AZURE_TENANT_ID=
AZURE_CLIENT_ID=
AZURE_CLIENT_SECRET=
POWERBI_WORKSPACE_ID=
POWERBI_REPORT_ID=
POWERBI_DATASET_ID=
POWERBI_EMBED_URL=
""",
        "README.md": f"""
# {title} analytics MVP

This repo scaffold is organized around a commercial, scenario-specific self-service analytics product.

Core flow:

```text
source data -> fabric lakehouse/warehouse -> gold layer -> semantic model -> embedded report -> action queue
```

Start by editing:

1. `docs/000-product-scope.md`
2. `docs/010-metric-contract.md`
3. `packages/analytics-contracts/gold_layer_contract.yml`
4. `powerbi/semantic-model/README.md`
5. `docs/030-security-multitenancy.md`

Do not expose raw source tables directly to customers. Build the MVP around certified metrics and a tenant-safe semantic model.
""",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a self-service analytics MVP repo scaffold.")
    parser.add_argument("--target", required=True, help="Target repo directory.")
    parser.add_argument("--scenario", default="analytics mvp", help="Short scenario name.")
    parser.add_argument("--mode", choices=["new", "extend"], default="extend", help="Scaffold intent. Does not delete files.")
    parser.add_argument("--force", action="store_true", help="Overwrite generated files if they already exist.")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    if args.mode == "new":
        target.mkdir(parents=True, exist_ok=True)
    elif not target.exists():
        raise SystemExit(f"target does not exist for --mode extend: {target}")

    ctx = scenario_context(args.scenario)
    messages = []
    for rel_path, content in files_for(ctx).items():
        messages.append(write_file(target / rel_path, dedent(content), args.force))

    print("\n".join(messages))
    print(f"\nscaffold complete: {target}")
    print("next: customize docs/000-product-scope.md and docs/010-metric-contract.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
