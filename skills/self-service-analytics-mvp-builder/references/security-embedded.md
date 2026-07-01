# Security and embedded analytics

## Embedding modes

Use `app owns data` for SaaS/customer-facing products. The app uses a service principal or embedding identity to generate embed tokens and passes the tenant/user context through RLS.

Use `user owns data` when users are employees who already have Power BI access and licensing.

## Tenant isolation choices

Start with the simplest safe model:

1. Shared semantic model + RLS by tenant/customer key for MVP and small customers.
2. Dedicated workspace or semantic model for large customers with performance, customization, or security needs.
3. Dedicated data store or tenant for regulated/high-compliance customers.

Do not defer the isolation key. Put `tenant_id` or equivalent into every product-facing fact/snapshot table from v1.

## RLS requirements

- Map app user -> tenant -> roles -> allowed entity scope.
- Apply RLS in the semantic model and validate with test users.
- Store role assignments in product DB.
- Keep a test matrix for admin, manager, viewer, and external customer roles.

## OLS and sensitive data

Use object-level security only when certain roles must not see tables or columns at all. Prefer not to expose sensitive raw columns in the semantic model.

## Power BI Embedded flow

Typical flow:

```text
react app -> backend -> auth/tenant lookup -> service principal -> generate embed token -> embedded report -> rls filters enforced by semantic model
```

Keep token generation on the backend. Do not expose secrets or service principal credentials to the frontend.

## Required checks before demoing to customers

- tenant A cannot see tenant B data
- viewer cannot access admin-only pages
- drill-through respects RLS
- exports respect RLS
- saved views cannot bypass RLS
- embed token lifetime and refresh behavior are understood
- audit logs capture user/report/action events
