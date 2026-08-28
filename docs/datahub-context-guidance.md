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

Classify the evidence question before selecting a context path.

```text
code-originated: "did this code produce the expected runtime effect?"
  -> context-mastery
  -> system-mental-model
  -> targeted code and configuration inspection
  -> Expected Effect Contract
  -> domain-context-pack and DataHub only for a named orientation gap
  -> approved live-source interface
  -> effect-path verification or falsification

data-originated: "what data exists and where should I look?"
  -> context-mastery
  -> domain-context-pack
  -> authorized DataHub discovery
  -> approved live-source interface when current evidence is required

modeling-decision-originated: "what Silver model candidate is supported?"
  -> context-mastery
  -> domain-context-pack
  -> Gold Consumer Contract
  -> Modeling Question Contract
  -> minimum relevant DataHub context
  -> targeted live-data investigation
  -> cross-source reconciliation and adversarial checks
  -> candidate / partial / blocked
  -> accountable human review
```

Use `skills/context-mastery/SKILL.md` to select the smallest understanding capability.

Use `skills/domain-context-pack/SKILL.md` to assemble only the context required for the current task.

Use `skills/hybrid-knowledge-retrieval-builder/SKILL.md` only if the task is actually to build or evaluate retrieval and an existing DataHub capability has first been shown insufficient. Do not invoke it merely because DataHub is present.

Seeing Elasticsearch, Kafka, a database, or another data-bearing system does not by itself make a question data-originated. If code declares the expected side effect, inspect the bounded code path first. Conversely, do not inspect unrelated code when the task is only asset discovery.

A Silver-model request is modeling-decision-originated even when source code is available. Use `system-mental-model` only for a named uncertainty about implemented behavior; code behavior is evidence, not automatic desired business semantics.

## Contracts Before Silver Modeling

Do not begin from "clean the Bronze tables." Establish two compact task-scoped contracts using the existing Domain Context Pack artifact structure. These are decision inputs, not new permanent schemas.

### Gold Consumer Contract

Capture only what is needed to judge whether a Silver candidate is usable:

- consumer and workflow or question;
- required business entity or event and grain;
- required identifiers, dimensions, and relationships;
- required history and temporal behavior;
- freshness, completeness, and correctness expectations;
- security and governance boundary;
- explicit unusable conditions.

### Modeling Question Contract

Name the unresolved decisions before loading broad metadata or raw data:

- entity or event boundary and record grain;
- candidate identifiers and what would disprove uniqueness;
- legitimate joins, expected cardinality, and fanout risk;
- field-level source authority and reconciliation behavior;
- event, ingest, update, and effective-time semantics;
- retry, replay, late-arrival, duplicate, and deduplication behavior;
- normalization versus business interpretation;
- valid nulls versus defects;
- history representation and schema-evolution scope;
- known ambiguity, counterevidence, and evidence still needed.

Load a context item only when it can change one of these decisions, the live-data test, the candidate, or the stop boundary.

## Evidence and Authority Boundaries for Modeling

Keep these evidence classes separate:

```text
business requirement or definition
!= implemented code behavior
!= DataHub metadata, lineage, profile, or historical context
!= observed live-data behavior
!= accountable human or domain-owner authority
```

Apply these hard boundaries:

```text
DataHub relationship != verified join
DataHub profiling != proven grain
historical query != business rule
apparent uniqueness != durable primary key
current distribution != future schema contract
code behavior != desired business semantics
```

Do not resolve a conflict by majority vote across evidence classes. Preserve the conflict, identify the decision it blocks, and route it to the accountable authority.

## Source-Role Classification

Classify source roles at the field or decision scope, not only once per dataset:

```text
authoritative source
event source
reference or enrichment source
derived source
supporting source
unknown authority
```

One source may be authoritative for identity while another is authoritative for event time. "Contains a value" does not establish authority. Record authority, freshness, and observed behavior separately.

## Silver Model Candidate Boundary

The reviewable output is an **evidence-backed Silver Model Candidate**, never an automatically approved table. It should state:

- candidate entity or event boundary, grain, and key candidates;
- relationships and expected cardinality;
- temporal, history, late-arrival, and deduplication semantics;
- field-level source roles and reconciliation rules;
- normalization rules and quality constraints;
- schema-evolution assumptions and version/time scope;
- live evidence used, counterevidence, ambiguity, and missing evidence;
- Gold consumer fit and unusable conditions;
- candidate status and the accountable human review needed.

Use `candidate`, `partial`, `unknown`, or `blocked` when evidence is incomplete. Do not promote the result to verified semantic truth, approved architecture, production Silver, or Gold.

## Adversarial Modeling Checks

Challenge the candidate before presenting it for review:

1. **False uniqueness**: test candidate keys against targeted live data, duplicates, time ranges, and relevant schema versions. A profile is only a hypothesis.
2. **Join fanout**: measure both-side cardinality and row multiplication at the required grain. Reject joins that double count the Gold consumer's facts.
3. **Temporal mismatch**: distinguish event, ingest, update, and effective time; do not choose a timestamp by availability.
4. **Conflicting authority**: preserve disagreement among requirement, code, DataHub context, and live behavior for human resolution.
5. **Late or duplicate events**: expose retry, replay, late-arrival, and deduplication decisions.
6. **Schema evolution**: check historical/current versions and bound the candidate's version or time scope.
7. **Gold consumer mismatch**: reject a technically tidy candidate that cannot satisfy required grain, history, identifiers, or metric behavior.
8. **Insufficient evidence**: keep DataHub-suggested relationships, keys, or meanings partial or unknown until target-relevant evidence exists.

After the candidate exists, `unasked-questions-generator` may be used for a named consequential gap. It does not approve or automatically block the model, and it is not a replacement Silver validator.

## Expected Effect Before Retrieval

For a code-originated runtime-verification task, state what exactly should have happened before selecting an asset or issuing a live query. Use a compact, task-scoped Expected Effect Contract rather than a new permanent schema.

Capture only applicable fields:

- emitter and evidence-linked code location;
- trigger and branch conditions;
- expected event, message, write, call, or metric;
- level, status, or outcome semantics;
- serialized fields and correlation identifiers;
- service, component, deployment, environment, version, and destination;
- expected time window, timezone, buffering, or delivery delay;
- relevant feature flags, runtime configuration, sampling, throttling, and suppression conditions;
- live interface and query needed to prove or falsify the effect;
- facts, inferences, counterevidence, unknowns, and evidence references.

The contract is a hypothesis derived from code and configuration until runtime evidence verifies it. A logger statement, producer call, database client call, or metric declaration proves intent or reachable behavior, not execution.

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

### 5. Evidence question first; context narrows; live evidence decides

For data-originated discovery, prefer:

```text
orientation
-> likely assets and relationships
-> hypothesis
-> targeted query
-> live evidence
-> verify or reject
```

Avoid blind broad scans when existing context can narrow the search.

For code-originated runtime verification, prefer:

```text
evidence question
-> bounded code and configuration
-> Expected Effect Contract
-> named orientation gap
-> minimum DataHub context, if needed
-> narrow live query
-> expected-versus-observed comparison
-> verify, falsify, or preserve unknown
```

Do not call DataHub merely because the live destination is a data system.

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

The default is **not** to send an entire DataHub catalog or context graph to the model. Start from the Evidence Question and, for a code-originated task, the Expected Effect Contract. The ladder below is an escalation menu, not a mandatory sequence beginning at Level 0.

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

For Pre-Silver/Silver work, do not enter Level 4 until the Gold Consumer Contract and Modeling Question Contract are bounded. Level 4 is selected question by question; it is not a requirement to load Levels 0 through 3 in sequence.

## Context Selection Test

For every candidate context item, ask:

```text
Will this item change dataset selection,
query design,
hypothesis or cross-boundary mapping,
verification,
the next effect-path check,
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

Stop expanding context when the next action is already a bounded live query, a specific code/configuration check, a permission request, or an accountable human decision.

## Context Plane and Live Evidence Plane

DataHub and a live source have different authority.

| Plane | Can establish | Cannot establish by itself |
| --- | --- | --- |
| DataHub context | asset identity, schema, descriptions, ownership, lineage, usage, historical query patterns, profiling, quality/trust signals, likely field or deployment mapping | that a current event occurred, a current value exists, an exact current count, or a runtime path executed |
| Live source | current events or values within the queried scope, exact observed fields, timestamps, counts, and correlation matches | why code should have produced the effect or whether an unqueried path was correct |
| Code/configuration | intended effect, trigger, serialization, destination, suppression and routing logic | that a particular runtime execution or downstream storage actually occurred |
| Business requirement/definition | desired consumer outcome, declared business meaning, acceptance constraints | that code implements it or current data conforms to it |
| Accountable human/domain owner | approve semantic and architecture decisions within their authority | replace missing evidence or silently broaden source access |

Use only an approved source-native API, CLI, UI, MCP, or runtime tool for live verification. DataHub MCP availability is neither a live-query interface nor a source permission grant. Record the interface actually used; do not say a live source was checked when only metadata was inspected.

A positive match must bind enough of the Expected Effect Contract to avoid correlation collision. Do not verify from a correlation identifier alone when that value can be reused across event types, environments, tenants, attempts, or time windows. A negative result is strong only to the extent that the query had the necessary field-level/document-level visibility, destination coverage, deployment-version mapping, retention, time completeness, and known sampling/drop behavior.

## Cross-Boundary Evidence Mapping

Build a temporary mapping only when names or identities cross boundaries:

```text
code symbol -> serialized field -> transformed/indexed field
code component -> deployment -> destination index, stream, topic, table, or service
correlation value -> runtime search key
```

For example, `requestId` may serialize or transform to `request.id`, `trace.id`, `labels.request_id`, or another indexed field. A message such as `Upload completed` may become a structured `event.action=upload_complete` record.

Mark each mapping edge `OBSERVED`, `INFERRED`, `UNKNOWN`, or `VERIFIED` and attach an evidence reference. Keep it task-scoped. Do not promote a one-run mapping into durable truth without governed evidence, scope, review, version, and expiry.

## Expected Effect Path

An empty or mismatched live query is evidence about that query scope, not automatic proof that emission failed. Check the smallest next layer that can distinguish competing explanations:

```text
code path executed?
-> trigger satisfied?
-> emitter call executed?
-> level / flag / runtime configuration allowed it?
-> serialization or formatting produced the expected shape?
-> transport / exporter accepted it?
-> collector / consumer received it?
-> ingest pipeline accepted or dropped it?
-> transformation renamed or removed fields?
-> correct destination, environment, deployment version, and tenant?
-> correct event time, ingest time, timezone, buffer, and search window?
-> query uses the correct field, value, syntax, and permissions?
-> sampling, throttling, retention, deduplication, or delay affected it?
```

This path applies to logs, Kafka events, database writes, HTTP effects, metrics, and other external side effects. Skip inapplicable stages, but do not collapse `emitted`, `transported`, `ingested`, `stored`, and `found by this query` into one state.

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

For code-originated runtime verification, also report:

- the Expected Effect Contract;
- the task-scoped cross-boundary mapping;
- live interface, environment, deployment version, time window, query, and result scope;
- effect-path stages checked and the earliest supported failure boundary;
- `FACT`, `INFERENCE`, `COUNTEREVIDENCE`, `UNKNOWN`, and `VERDICT` as separate sections.

Use `VERIFIED` only when target-relevant live evidence supports the Expected Effect Contract. Use `FALSIFIED` only when evidence rules out the expected effect within the bounded scope. Otherwise return a narrower failure-boundary verdict or `UNKNOWN`; absence from one query is not a pipeline verdict.

Do not claim that DataHub was used when it was only described conceptually.

For a Pre-Silver/Silver modeling decision, also report:

- the Gold Consumer Contract and Modeling Question Contract;
- relevant source roles by field or decision scope;
- minimum DataHub context selected and material context excluded;
- targeted live-data checks for grain, keys, joins, time, duplicates, and schema versions;
- reconciled facts, conflicts, counterevidence, unknowns, and assumptions;
- the Silver Model Candidate and Gold-fit result;
- candidate/partial/unknown/blocked status and required human review.

## Stop Conditions

Stop or defer when:

- DataHub already provides the requested capability and the task was only to decide whether to build it;
- required DataHub or source permission is missing;
- the requested context would cross a privacy, IP, or data-governance boundary;
- the current deployment cannot establish the required DataHub feature;
- metadata or inferred context is being treated as current source truth;
- a profile, historical query, code path, or DataHub relationship is being treated as durable semantic proof;
- a modeling conflict needs accountable authority or the candidate lacks evidence for grain, key, join, time, deduplication, schema scope, or Gold fit;
- the task is drifting into building a duplicate data platform without an evidence-backed gap;
- the smallest sufficient context has been assembled and the next step is live verification or human review.
