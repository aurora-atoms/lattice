# DataHub Context Architecture Research — 2026-08-27

## Research Question

What parts of the desired pre-Silver/Gold data-understanding layer already exist in DataHub, what architectural ideas are worth reusing, and what should Lattice avoid rebuilding?

## Executive Summary

DataHub is not only a metadata catalog. Its current public codebase and adjacent official projects show a broader architecture built around:

- normalized metadata/context modeling;
- heterogeneous ingestion connectors;
- graph, search, lineage, usage, profiling, quality, and semantic retrieval;
- MCP and Agent Skills for external agent activation;
- an analytics-agent reference implementation that consumes context before executing live SQL;
- feedback/writeback patterns for improving context over time.

The most important conclusion is architectural:

> Lattice should not create a second metadata graph, connector framework, generic data agent, MCP layer, lineage engine, profiling engine, or vector-search catalog. It should consume DataHub as an existing context substrate and add only Lattice-specific bounded context projection, evidence discipline, public/private boundary, and any future gap that real delivery evidence proves is still missing.

## Primary Repositories Reviewed

The public research focused on:

- `datahub-project/datahub`
- `datahub-project/datahub-skills`
- `datahub-project/analytics-agent`

Official DataHub documentation and current product material were used to distinguish open-source capabilities from managed/cloud-only capabilities where relevant.

## Evidence Classes

This report distinguishes:

- `CODE_DIRECT`: directly evident from public repository implementation or repository documentation;
- `OFFICIAL_PRODUCT`: stated in current official DataHub documentation/product material;
- `INFERENCE`: architectural conclusion derived from the evidence above.

## 1. Unified Model Before Agent Consumption

### Finding

DataHub normalizes source-specific observations into a common metadata model instead of exposing every source's native representation directly to consumers.

### Evidence class

`CODE_DIRECT`

### Why it matters

A SQL database, Databricks workspace, BI tool, dbt project, streaming system, or file-oriented source can be ingested through source-specific connectors while downstream search, lineage, governance, and agent use operate over normalized context.

### Lattice implication

Reuse this architectural principle. Do not create source-specific agent knowledge formats for every database technology.

## 2. Connectors Are Translation Boundaries

### Finding

DataHub's ingestion architecture separates source extraction from the metadata platform's serving model. Source-specific connectors produce normalized metadata events/proposals rather than becoming independent context stores.

### Evidence class

`CODE_DIRECT`

### Lattice implication

For Databricks, SQL stores, BI tools, documentation, and other supported sources, prefer DataHub's connectors. A Lattice-specific connector should be a last resort and should exist only when a missing source signal is material to a real delivery case.

## 3. Canonical Context and Retrieval Are Different Layers

### Finding

DataHub exposes multiple ways to retrieve and navigate the same normalized knowledge: search, entity lookup, graph relationships, lineage, usage, and semantic/context mechanisms.

### Evidence class

`CODE_DIRECT` + `INFERENCE`

### Architectural lesson

Search index, vector index, graph traversal, or statistics should not become the authoritative knowledge record.

### Lattice implication

Keep canonical facts/evidence separate from their task-specific retrieval projection.

## 4. Useful Context Is Multi-Signal

### Finding

DataHub combines technical, operational, and business context instead of relying on embeddings alone. Current capabilities include schema, lineage, ownership, usage, query information, quality/profiling signals, glossary/documentation, domains, and semantic context.

### Evidence class

`CODE_DIRECT` + `OFFICIAL_PRODUCT`

### Lattice implication

Reject a design based on embedding all rows, all DDL, or all SQL and calling that a context index. The useful unit is an evidence-linked context model with several independent signals.

## 5. DataHub Skills Reuse the Existing Agent Ecosystem

### Finding

`datahub-project/datahub-skills` packages DataHub-oriented agent workflows for existing coding/agent runtimes rather than requiring a proprietary DataHub-only agent host.

### Evidence class

`CODE_DIRECT`

### Architectural lesson

Keep native coding agents native. Supply tools, context, and Skills.

### Lattice implication

Before creating any data-oriented Lattice Skill, check whether the corresponding DataHub Skill already performs the task. Avoid parallel Skills that simply search metadata, traverse lineage, or inspect data quality.

## 6. Analytics Agent Demonstrates Context-First Investigation

### Finding

`datahub-project/analytics-agent` is a public reference application that combines DataHub context with a live database connection. Its documented behavior includes plain-English-to-SQL execution, multi-turn reasoning, context-quality scoring, and context-improvement/writeback functions.

### Evidence class

`CODE_DIRECT`

### Architectural lesson

The agent should first use existing context to understand the domain and likely data assets, then execute targeted live queries.

### Lattice implication

Use this sequence:

```text
context orientation
-> dataset/relationship selection
-> hypothesis
-> targeted live query
-> evidence
-> verification
```

Do not treat catalog context as current truth.

## 7. Feedback Can Improve Context, But Promotion Must Be Governed

### Finding

The analytics-agent repository includes explicit context-quality and correction/publish concepts.

### Evidence class

`CODE_DIRECT`

### Architectural lesson

Agent usage can surface missing documentation or corrections and feed improvements back into the context system.

### Lattice implication

Preserve a stricter promotion boundary:

```text
observation
-> evidence-backed context candidate
-> review
-> optional durable promotion
```

No generated inference should automatically become an authoritative Lattice belief, memory, or company data definition.

## 8. DataHub and Unity Catalog Are Complementary

### Finding

DataHub has direct Databricks / Unity Catalog integration and is designed to aggregate broader cross-system context. Unity Catalog remains Databricks' technical governance plane for Databricks-managed data and permissions.

### Evidence class

`OFFICIAL_PRODUCT` + `INFERENCE`

### Recommended boundary

```text
DataHub
  cross-system discovery/context plane
          |
          v
Databricks / Unity Catalog
  governed Databricks technical/semantic plane
          |
          v
Bronze / Silver / Gold
```

Do not create a false product choice between DataHub and Unity Catalog when both can own different responsibilities.

## 9. Initial Data Context Before Silver/Gold

### What DataHub already covers

`KEEP`:

- source inventory and normalized metadata;
- schema and field-level information;
- lineage;
- ownership/domains/tags;
- search and semantic discovery;
- query-history and usage signals where source support exists;
- quality/profiling metadata where configured;
- business glossary/documentation/context documents;
- Databricks/Unity Catalog ingestion;
- MCP-based agent access;
- DataHub Agent Skills;
- analytics-agent reference pattern.

### What should be configured/composed

`ADAPT`:

- which DataHub sources are enabled;
- which context types are safe to ingest;
- which context reaches which coding-agent task;
- mapping DataHub output into a bounded Lattice context pack;
- private DataHub/Core/Cloud deployment profile;
- live verification tool boundary;
- evidence capture and context-candidate promotion.

### What remains unproven

`GAP_CANDIDATE`:

- reusable engineering investigation memory spanning issue, code, query, logs, evidence, rejected hypotheses, and root cause;
- deeper actual-data behavioral understanding for rare temporal/log patterns that metadata/profiling do not capture;
- automatic generation and verification of candidate Silver integration models.

These are not implementation commitments. Each must first be tested against DataHub's latest capabilities and a real downstream need.

## 10. Core vs Cloud

### Open-source/self-hosted direction

DataHub Core provides a substantial reusable substrate and can be deployed privately. It is attractive where privacy/IP exposure must be minimized and the organization is willing to operate the service and its dependencies.

### Managed/cloud direction

Current official product material adds managed context-intelligence, automation, and scoped agent-context capabilities beyond the OSS baseline.

### Lattice rule

The public integration contract must not make Cloud-only functionality mandatory. Downstream repositories should declare their deployment profile and optional extensions.

## 11. Privacy and IP

Metadata is not automatically non-sensitive. Schema, lineage, query history, business definitions, logs, samples, and investigation documents can reveal concentrated company IP or personal information.

Recommended classification:

### Low-risk/default context candidates

- schema and types;
- approved descriptions;
- lineage identifiers;
- aggregate profiling statistics;
- usage counts;
- quality status;
- sanitized query patterns.

### Controlled/private context

- raw query text;
- samples;
- logs;
- context documents;
- incident history;
- proprietary business semantics;
- code-linked investigation evidence.

### Never public

- credentials/secrets;
- raw restricted PII;
- customer free text;
- sensitive security telemetry;
- unpublished inventions or patent concepts;
- real proprietary schemas/lineage from a private downstream environment.

## 12. Lattice Fit

DataHub's architecture aligns with several Lattice principles:

- context is a budget, not a warehouse dump;
- native agents execute, external context systems provide bounded evidence;
- retrieval projection is distinct from authoritative evidence;
- evidence and inference must remain distinguishable;
- use existing native/vendor capability before creating a new platform;
- private business evidence remains downstream;
- learning should be candidate-scoped until governed promotion.

The direction does not require a new Lattice active module. It should begin as a reference workflow plus bounded contracts inside existing context/evidence boundaries.

## Recommended Implementation Sequence

```text
Phase 1
  document DataHub-backed context workflow
  define bounded projection contract
  add synthetic conformance example
  add privacy/evidence validator

Phase 2
  consume DataHub MCP / Skills directly in a private downstream implementation
  add a thin adapter only if the native runtime cannot consume the required surface

Phase 3
  collect real evidence of remaining gaps
  evaluate investigation-memory, behavioral-context, or Silver-model extensions separately
```

## Build Avoidance Rules

Do not build the following unless new evidence invalidates this research:

- generic metadata graph;
- generic catalog/search UI;
- duplicate source connector framework;
- generic lineage engine;
- generic profiling engine;
- generic vector catalog;
- generic data MCP server;
- generic analytics/data agent;
- duplicate DataHub Skills.

## Final Verdict

```text
DataHub = KEEP as existing context substrate
Unity Catalog = KEEP as Databricks governance/semantic substrate
DataHub + Unity Catalog = COMPOSE
Lattice bounded context projection = ADAPT
Lattice privacy/evidence guard = ADAPT
Engineering investigation memory = GAP_CANDIDATE
Actual-data behavioral intelligence = GAP_CANDIDATE
Silver-model recommendation = GAP_CANDIDATE
new generic data/context platform = STOP
```
