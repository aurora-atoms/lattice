# MVP Workflow

## Scope rule

Keep v1 narrow enough that one user role can make one recurring decision.

A feasible MVP has:

- one target role
- one high-value decision loop
- three to five business questions
- five to ten certified metrics
- two to four dimensions
- one overview page
- one detail page
- one action queue or insight feed
- one tenant/security path

Avoid:

- generic report builders
- open-ended data exploration over raw tables
- complex custom metric authoring in v1
- AI chat before the metric contract exists
- building every connector before validating the product loop

## Decision filter

Before adding a feature, ask:

- Does it help the target role decide or act?
- Does it rely on certified metrics instead of raw tables?
- Can it be secured by tenant/role in v1?
- Can usage or outcome be measured?

If not, defer it.

## Build sequence

1. Business scenario contract
   - user role
   - decision cadence
   - current workflow
   - output required to act
   - first success metric

2. Metric contract
   - define each metric in business language
   - specify source, grain, filters, dimensions, owner, refresh cadence, and version
   - separate raw events from product-facing metrics

3. Gold layer
   - create decision-oriented Gold tables
   - prefer snapshot and aggregate tables for v1
   - include tenant/customer isolation keys
   - design tables around report pages and action queues

4. Semantic model
   - expose business entities, metrics, and approved dimensions
   - hide technical columns
   - apply friendly names and descriptions
   - implement RLS mapping
   - document measure definitions

5. Product shell
   - embed Power BI reports where visual analysis is needed
   - keep workflow, notes, tasks, alerts, configuration, and audit outside Power BI

6. Action loop
   - convert insights into decisions or tasks
   - include owner, priority, status, due date, and outcome
   - track whether users acted on insights

7. Observability
   - log refresh success/failure
   - log semantic model/report usage
   - log insight clicks and action completion
   - version metrics and report releases

## Definition of done for v1

- A user can open the product and understand the most important change or risk.
- The user can filter/drill into the entities driving the change.
- The user can create or accept a next action.
- The product stores action history, notes, and audit events.
- Metrics are named, defined, versioned, and safe for self-service.
- Tenant data cannot leak across users or customers.
- Demo path is repeatable with realistic sample data.
