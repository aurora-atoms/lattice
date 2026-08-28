# Data Context via DataHub: Research Summary and Integration Plan

## Status

This document is a public-safe research and planning artifact. It does not define a new active Lattice module and does not copy private company data, schemas, logs, incidents, queries, or business logic into this repository.

## Decision

Use DataHub as the primary existing context substrate for heterogeneous enterprise data discovery before building new catalog, metadata graph, lineage, profiling, query-history, semantic-retrieval, MCP, or generic analytics-agent infrastructure.

Lattice should integrate around DataHub rather than reimplementing DataHub.

The target operating principle is:

```text
heterogeneous data sources
-> existing DataHub ingestion and context capabilities
-> bounded, task-specific context projection
-> native coding agent
-> live evidence verification
-> evidence-backed learning candidate
```

The DataHub index or catalog is a prior and orientation surface, not ground truth. Live source data remains the verification boundary.

## Research Basis

The research reviewed the public DataHub organization and related official repositories, especially:

- `datahub-project/datahub`
- `datahub-project/datahub-skills`
- `datahub-project/analytics-agent`

The public implementation and documentation support the following reusable design ideas.

## Reusable Design Principles

### 1. Unified context model rather than source-specific agent knowledge

DataHub normalizes heterogeneous sources into a common metadata model. Connectors are responsible for extraction and translation, while the serving and retrieval layers operate on normalized entities and relationships.

Lattice should preserve that separation. A database, Parquet lake, Elasticsearch cluster, Databricks workspace, BI tool, or documentation system should not require a different agent mental model.

### 2. Connectors are adapters, not the knowledge architecture

A connector should observe and translate source-specific facts. It should not create a parallel context platform.

For this direction, prefer existing DataHub connectors and ingestion contracts before considering any custom adapter. A custom adapter is justified only when an important source or signal is not supported by DataHub and the missing signal matters to a real delivery case.

### 3. Canonical context is separate from retrieval projections

Search indexes, graph traversal, semantic retrieval, and statistics are projections over canonical context. They should not become the authoritative knowledge source.

This matches the Lattice rule that context is a budget and a projection, not a warehouse dump.

### 4. Useful data context is multi-signal, not vector-only

Useful orientation combines signals such as:

- schema and field definitions;
- lineage;
- ownership and domains;
- usage and query history;
- data quality and profiling;
- business glossary and documentation;
- trusted or popular assets;
- relationships and common query patterns.

Do not build an architecture that assumes embedding all rows or all raw database artifacts is sufficient.

### 5. Keep the coding agent native

DataHub already provides MCP, Skills, and an analytics-agent implementation. Generic runtimes such as Codex, GitHub Copilot, Claude Code, Cursor, or other MCP/Agent-Skills-compatible tools should remain the execution plane.

Lattice must not create a new generic data agent merely to call DataHub.

### 6. Context first, live evidence second

The desired investigation sequence is:

```text
context orientation
-> candidate datasets and relationships
-> hypothesis
-> targeted source query
-> live evidence
-> verification or falsification
```

This reduces blind exploration while preserving source truth.

### 7. Context can improve through validated use

DataHub's public agent work includes context-quality and correction/writeback concepts. Lattice should reuse this pattern but preserve its own evidence and promotion rules:

```text
observed investigation result
-> evidence-linked candidate
-> scoped review
-> optional promotion
```

A generated correction, inferred relationship, or agent conclusion is never automatically promoted to authoritative context.

## What to Reuse Directly

The default verdict for the following capabilities is `KEEP`:

| Capability | Default | Rationale |
|---|---|---|
| metadata model and metadata graph | KEEP | mature DataHub responsibility |
| source ingestion framework | KEEP | avoid connector duplication |
| Databricks / Unity Catalog ingestion | KEEP | existing integration boundary |
| SQL-source ingestion | KEEP | existing connector model |
| lineage capture and traversal | KEEP | core DataHub capability |
| usage and query-history ingestion | KEEP | core context signal |
| profiling / quality metadata | KEEP | use existing capabilities where supported |
| search and semantic retrieval | KEEP | retrieval substrate already exists |
| glossary / documentation / context documents | KEEP | use DataHub model rather than parallel docs DB |
| MCP surface | KEEP | native agent integration already exists |
| DataHub Agent Skills | KEEP | use before authoring Lattice-specific duplicates |
| Analytics Agent reference implementation | KEEP | reference and optional runtime, not a Lattice replacement |

## What May Need Adaptation

The following are `ADAPT`, not rebuild targets:

### Task-specific context projection

DataHub can contain more context than a coding task should receive. Lattice should define a bounded projection contract that selects the smallest sufficient DataHub context for the current delivery or investigation task.

The projection should preserve:

- source identity;
- source type;
- asset identity;
- schema or field scope;
- lineage or relationship evidence;
- freshness or observation time where available;
- confidence or trust signal where available;
- access boundary;
- evidence reference;
- explicit unknowns.

It must not copy the full DataHub graph, large query history, raw logs, or unbounded sample data into model context.

### Public-private boundary

Public Lattice should contain only contracts, reference workflow, schemas, validators, templates, and synthetic examples for the integration pattern.

Private downstream repositories or approved private services own:

- DataHub endpoint and credentials;
- private source identifiers;
- real schemas and metadata;
- query history;
- sample values;
- real lineage;
- incidents;
- investigation history;
- proprietary business semantics;
- manager-ready findings.

### DataHub Core versus Cloud

The integration contract must not assume Cloud-only functionality unless explicitly selected downstream.

A downstream implementation should declare which profile it uses:

```text
datahub_core
or
datahub_cloud
```

Cloud-only or preview capabilities must remain optional extensions rather than public Lattice requirements.

## Current Gaps to Validate Before Building

These remain `GAP_CANDIDATE`, not approved implementation work.

### 1. Engineering investigation memory

Potential missing capability:

```text
issue
-> hypothesis
-> query or inspection
-> evidence
-> rejected hypothesis
-> root cause
-> verified reusable lesson
```

Before building this, evaluate whether DataHub Context Documents, incidents, query entities, annotations, or existing APIs can represent enough of the workflow.

### 2. Actual-data behavioral understanding

Metadata, lineage, profiling, and query history may still be insufficient for rare temporal behavior, operational logs, or unusual cross-source patterns.

Do not build a generic behavioral index until a real case demonstrates that existing DataHub plus live-query capability cannot provide sufficient orientation.

### 3. Silver-model recommendation

A future capability may infer candidate entities, grains, keys, joins, normalization, quality constraints, and Silver transformations from discovered context.

This is downstream of context acquisition. It should not be merged with DataHub ingestion or metadata modeling.

## Relationship to Databricks and Unity Catalog

Do not frame the architecture as `DataHub versus Unity Catalog`.

Use a layered responsibility model:

```text
DataHub
  cross-system discovery and context plane
          |
          v
Databricks / Unity Catalog
  governed Databricks technical and semantic plane
          |
          v
Bronze / Silver / Gold
```

DataHub may ingest Unity Catalog metadata and other heterogeneous systems. Unity Catalog remains authoritative for Databricks governance, permissions, lineage, and curated Databricks data products within its scope.

Silver and Gold modeling should be informed by discovered context, but the DataHub catalog itself must not be treated as proof that inferred semantics or joins are correct.

## Recommended Lattice Operating Flow

```text
1. Direction gate
2. Identify real delivery or investigation scope
3. Use native runtime and existing DataHub capability first
4. Retrieve bounded DataHub context
5. Produce a task-scoped context pack
6. Let the native coding agent form a hypothesis or investigation plan
7. Query live sources through approved tools
8. Record evidence and counterevidence
9. Verify or reject the hypothesis
10. Create a learning/context candidate only when reuse is plausible
11. Human or governed promotion decides whether the candidate becomes durable context
```

## Proposed Public Lattice Artifacts

Implementation should remain small and compositional.

### Phase 1 — Reference contract only

Create:

- a public reference workflow for `DataHub-backed data context`;
- a task-scoped context projection schema;
- a synthetic example showing DataHub metadata projected into a bounded coding-agent context pack;
- a validator checking public/private boundaries and required evidence fields.

Do not create:

- a new active Lattice module;
- a generic data agent;
- a metadata graph;
- a DataHub fork;
- a new MCP server when DataHub MCP is sufficient;
- a new catalog UI;
- a duplicate profiling or lineage engine.

### Phase 2 — Thin runtime adapter only if needed

If a real downstream runtime cannot consume DataHub MCP or Skills directly, add the smallest adapter necessary to translate from DataHub's native interface to the existing Lattice context-pack boundary.

The adapter must not own source truth or duplicate DataHub storage.

### Phase 3 — Validate gap candidates

Only after real downstream evidence should Lattice consider bounded extensions for:

- investigation-memory projection;
- behavioral-context projection;
- Silver-model candidate generation.

Each extension must pass the Direction Investment Gate and demonstrate why DataHub or Databricks native capability is insufficient.

## Privacy and IP Rules

Use context minimization by default.

### Public-safe

Public Lattice may contain:

- generic schemas;
- generic DataHub integration contracts;
- synthetic metadata examples;
- generic workflow and validation logic;
- public references to DataHub capabilities.

### Private-only

Keep downstream:

- credentials and endpoints;
- raw PII;
- raw customer data;
- restricted logs;
- real query history containing sensitive values;
- proprietary schema and lineage;
- private engineering incidents;
- unreleased invention or patent material;
- company-specific business semantics.

The downstream context projection should prefer aggregate metadata, statistics, identifiers, and evidence references over raw data values. Samples and raw queries require explicit private policy approval.

## Success Criteria

This direction succeeds when a downstream coding agent can use existing DataHub capabilities to obtain bounded orientation across heterogeneous data sources without Lattice recreating catalog or data-platform infrastructure.

Evidence should show:

- DataHub capability was reused rather than duplicated;
- context supplied to the agent was task-scoped;
- live evidence was used for verification;
- private data remained in the downstream boundary;
- any custom extension corresponds to an observed gap;
- the result improves a real feature-delivery or engineering-investigation outcome.

## Stop Conditions

Stop implementation when:

- DataHub already provides the requested capability with acceptable cost and risk;
- the proposal creates a parallel catalog, MCP server, generic data agent, or metadata graph without a demonstrated gap;
- private evidence would need to be committed to public Lattice;
- a Cloud-only feature is being treated as a mandatory Core capability;
- inferred metadata is being treated as current source truth;
- no real downstream delivery or validation path can justify a custom extension.

## Plan Verdict

```text
DataHub platform capabilities     = KEEP
DataHub native MCP / Skills       = KEEP
DataHub + Unity Catalog           = COMPOSE
Lattice task context projection   = ADAPT
Lattice public/private guard      = ADAPT
Investigation memory              = GAP_CANDIDATE
Behavioral data understanding     = GAP_CANDIDATE
Silver model recommendation       = GAP_CANDIDATE
new generic data platform         = STOP
new generic data agent            = STOP
```
