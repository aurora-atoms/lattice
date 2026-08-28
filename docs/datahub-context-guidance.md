# DataHub Context Guidance

## Purpose

This is a public, vendor-aware guidance document for agents that need to understand or investigate heterogeneous enterprise data before or during delivery work.

It is **not** an implementation plan for a new Lattice data platform. It does not define a new active module, metadata graph, MCP server, catalog, profiler, data agent, or runtime service.

Use the existing Lattice context capabilities to decide what context is needed, and use DataHub's existing context, metadata, lineage, usage, query-history, quality, search, MCP, and Agent Skill surfaces when they are available and authorized.

The governing principle is:

> Prefer DataHub as the existing data-context substrate; use Lattice to select the smallest sufficient context and preserve evidence, privacy, and live verification.

For the research basis and source notes, see `../reports/datahub-context-architecture-research-2026-08-27.md`.

## When an Agent Should Read This

Read this guidance only when the current task includes one or more of the following:

- an unfamiliar database, lake, Parquet estate, Elasticsearch/log estate, Databricks workspace, BI model, or mixed data environment;
- a coding or engineering investigation that depends on understanding data shape, lineage, usage, joins, ownership, freshness, quality, or historical query patterns;
- data-model or Silver/Gold design where the agent needs prior orientation before proposing transformations;
- a request to build or improve "database context", "data context index", "data understanding", or similar capability;
- a proposal to build custom catalog, metadata graph, retrieval, profiling, lineage, MCP, or generic data-agent infrastructure.

For ordinary code-only tasks, do not load this document.

## Existing Lattice Capability Path

Do not create a separate DataHub Skill or new Lattice module by default.

Use the existing capability path:

```text
context-mastery
  -> domain-context-pack
  -> authorized DataHub context, when relevant
  -> native coding agent
  -> live verification
```

Use `skills/context-mastery/SKILL.md` to select the smallest understanding capability.

Use `skills/domain-context-pack/SKILL.md` to assemble only the context required for the current task.

Use `skills/hybrid-knowledge-retrieval-builder/SKILL.md` only if the task is actually to build or evaluate retrieval and an existing DataHub capability has first been shown insufficient. Do not invoke it merely because DataHub is present.

## DataHub-First Decision Rule

Before proposing custom data-context infrastructure, determine whether the authorized DataHub environment already provides the required function.

Default to direct reuse for:

- source ingestion and metadata normalization;
- dataset, table, field, domain, glossary, owner, and documentation context;
- lineage capture and traversal;
- usage and query-history context;
- profiling, quality, and trust signals where supported;
- search and semantic discovery;
- Databricks / Unity Catalog metadata integration;
- DataHub Context Documents and related governed context;
- DataHub MCP access;
- DataHub-provided Agent Skills;
- the public Analytics Agent as a reference or optional runtime.

Do not rebuild these capabilities inside Lattice unless a concrete, evidence-backed gap remains after checking the current DataHub capability.

## Mental Model

Treat DataHub as a **context substrate**, not as unquestionable source truth.

```text
heterogeneous data sources
        |
        v
DataHub
metadata / lineage / usage / query history / quality / semantics
        |
        v
bounded task context
        |
        v
native coding agent
        |
        v
live source query or runtime evidence
        |
        v
verification / falsification
```

The important separation is:

```text
DataHub context = prior orientation
live source evidence = current verification
```

An inferred join, generated description, historical query, popularity signal, profile, semantic match, or context document can guide investigation. It must not silently become proof that current data behaves that way.

## Architecture Principles to Reuse

### 1. Normalize context, not agents

Different data sources should not require separate agent mental models. Let source-specific connectors translate into a common context plane and let the coding agent remain native to its runtime.

### 2. Keep source adapters separate from knowledge semantics

A connector observes a source. It should not define a second context architecture.

### 3. Keep canonical context separate from retrieval projections

Search, graph traversal, semantic retrieval, rankings, embeddings, and statistics are retrieval views over governed context. They are not automatically authoritative facts.

### 4. Use multiple context signals

Prefer combined evidence from:

- schema and fields;
- descriptions and business meaning;
- ownership and domain;
- lineage and relationships;
- usage and popularity;
- query history;
- freshness;
- quality or profiling;
- trusted datasets;
- contextual documents.

Do not assume vector similarity alone is sufficient.

### 5. Context first, live evidence second

Preferred investigation sequence:

```text
orientation
-> likely assets and relationships
-> hypothesis
-> targeted query
-> live evidence
-> verify or reject
```

Avoid blind broad scans when existing context can narrow the search.

### 6. Reuse native DataHub surfaces

If DataHub MCP or DataHub Agent Skills are available in the active runtime, use those before creating an adapter, wrapper, parallel MCP server, or duplicate Skill.

Tool availability still does not grant permission.

## Where to Call DataHub

The exact tool name varies by runtime and deployment. Do not hard-code one provider-specific invocation into Lattice.

When DataHub is configured and authorized, prefer its native surfaces in this order:

1. DataHub search / discovery for candidate assets;
2. asset metadata and schema for relevant tables and fields;
3. lineage for only the hops needed to understand the current question;
4. usage, quality, trust, owner, glossary, and documentation signals when they change confidence or selection;
5. historical query examples only when they materially reduce uncertainty about joins, filters, aggregation, or business interpretation;
6. live database, Databricks, Elastic, or other source query only after the prior context has narrowed the question.

If the runtime exposes DataHub through MCP, use the DataHub MCP surface.

If the runtime supports DataHub's published Agent Skills, prefer those Skills rather than copying their behavior into a Lattice-specific duplicate.

If neither surface is available, use an approved DataHub API or UI only within the current permission boundary. Do not infer that an unavailable DataHub tool should be replaced with a new Lattice service.

## Minimum Context Rule

The default is **not** to send an entire DataHub catalog or context graph to the model.

Select the smallest context that can change the next decision or investigation step.

### Level 0 — Discovery

Use when the agent only needs to answer "where should I look?"

Include only:

- candidate asset identity;
- concise description or domain;
- owner or accountable source when relevant;
- trust / quality / freshness signal when it affects selection;
- why the asset is relevant.

Do not load full schemas, query history, samples, or broad lineage yet.

### Level 1 — Structural Orientation

Use when the agent needs to understand how the relevant data is shaped.

Add only:

- relevant tables or datasets;
- relevant columns and types;
- likely keys or identifiers if source-supported;
- immediate upstream/downstream lineage needed for the task;
- grain or temporal meaning when documented or observed;
- explicit unknowns.

Do not load unrelated columns or full graph neighborhoods.

### Level 2 — Investigation Context

Use when the task requires forming a query or testing a hypothesis.

Add only the signals that can change the query plan:

- known joins or relationships with evidence;
- relevant historical query patterns;
- usage or trusted-asset signals;
- relevant quality/profiling summaries;
- freshness or observed time boundary;
- task-specific documentation or business definitions.

Prefer aggregate profiles and query patterns over raw row samples.

### Level 3 — Live Evidence

Use only when the task cannot be answered reliably from context alone.

Query the authoritative source for:

- current values;
- anomalous rows;
- exact counts;
- current distributions;
- rare cases;
- current log events;
- evidence needed to verify or falsify the hypothesis.

Raw samples, logs, free text, or sensitive query literals require the applicable private-data policy and permission.

### Level 4 — Modeling Context

Use for Silver/Gold or semantic-model decisions after the relevant sources are understood.

Include only evidence needed to assess:

- entity and event boundaries;
- grain;
- candidate keys;
- stable joins;
- temporal behavior;
- deduplication or normalization needs;
- quality constraints;
- semantic definitions;
- unresolved ambiguity.

Modeling recommendations remain proposals until verified against live data and accountable domain knowledge.

## Context Selection Test

For every candidate context item, ask:

```text
Will this item change dataset selection,
query design,
hypothesis confidence,
verification,
or a modeling decision?
```

If no, do not load it now.

Also exclude the item when:

- it is outside caller authorization;
- it is stale and cannot safely support the task;
- its authority is unknown;
- it duplicates stronger context already selected;
- its token cost is high relative to expected information gain;
- it is raw data when metadata or an aggregate profile is sufficient.

## Privacy and IP Boundary

Metadata can contain proprietary information. Query history, lineage, schema, runbooks, context documents, and business definitions may reveal internal architecture or business logic even when no raw rows are copied.

Prefer, in order:

```text
identity / metadata
-> aggregate statistics
-> bounded query patterns
-> selected evidence references
-> raw values only when required
```

Never put the following in public Lattice:

- credentials or private endpoints;
- real customer or employee data;
- raw PII;
- restricted logs;
- real sensitive query history;
- proprietary company schemas or lineage;
- private incidents;
- unpublished invention material;
- company-specific business semantics.

Those belong to the private downstream repository or approved private systems.

## Databricks and Unity Catalog Boundary

Do not frame the choice as DataHub versus Unity Catalog.

Use the systems for different scopes:

```text
DataHub
  cross-system context and discovery plane
        |
        v
Databricks / Unity Catalog
  governed Databricks data and semantic plane
```

Unity Catalog remains authoritative for Databricks permissions and governed assets within its scope.

DataHub can provide cross-system orientation and reuse Unity Catalog metadata alongside other sources.

Silver and Gold modeling may be informed by DataHub context, but DataHub metadata alone is not proof that inferred joins, grain, or business semantics are correct.

## Core and Cloud

Do not assume a Cloud-only or preview DataHub feature exists in every deployment.

Before relying on a capability, establish:

- `datahub_core` or `datahub_cloud`;
- deployed version;
- enabled connectors or context features;
- MCP / Skill availability;
- access policy;
- whether the feature is GA, preview, beta, or unavailable in that environment.

If the feature is unavailable, report the gap. Do not automatically turn the gap into a Lattice implementation task.

## What Lattice Should Not Build by Default

Do not create a new Lattice implementation for:

- metadata graph;
- source connector framework;
- lineage engine;
- profiler;
- query-history store;
- semantic search layer;
- context catalog UI;
- generic DataHub wrapper;
- duplicate MCP server;
- generic database/data agent;
- copied DataHub Agent Skills.

A proposal for one of these must first show that the existing DataHub capability is unavailable or insufficient for the current bounded need.

## Candidate Gaps, Not Commitments

The following may be legitimate future gaps but are not assumed to require Lattice implementation:

- reusable engineering-investigation memory spanning code, data, logs, hypotheses, counterevidence, and root cause;
- behavior-oriented understanding of rare temporal or operational patterns that normal metadata and profiling cannot capture;
- candidate Silver-model recommendations from discovered cross-source context.

Before treating any of these as a build target, re-check current DataHub capability and require concrete evidence that the missing behavior matters.

## Agent Output Expectations

For a DataHub-backed context task, return a concise record of:

- task scope;
- DataHub availability and deployment assumptions;
- DataHub surfaces actually used;
- selected assets and why;
- selected context level and why;
- material context intentionally excluded;
- freshness / authority / permission limitations;
- live evidence still required;
- unsupported gaps, if any.

Do not claim that DataHub was used when it was only described conceptually.

## Stop Conditions

Stop or defer when:

- DataHub already provides the requested capability and the task was only to decide whether to build it;
- required DataHub or source permission is missing;
- the requested context would cross a privacy, IP, or data-governance boundary;
- the current deployment cannot establish the required DataHub feature;
- metadata or inferred context is being treated as current source truth;
- the task is drifting into building a duplicate data platform without an evidence-backed gap;
- the smallest sufficient context has been assembled and the next step is live verification or human review.
