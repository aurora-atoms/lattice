# Agentic Data Context Scenarios — Industry Patterns, Proposals, and Patent-Screening Notes

## Status

This is a public-safe research and ideation artifact for PR #56.

It does not implement a DataHub integration, data platform, data agent, dashboard runtime, Databricks job, Elasticsearch agent, MCP server, schema, validator, or new Lattice module.

It does not contain private endpoints, credentials, schemas, business logic, incidents, query history, samples, logs, customer data, or unpublished invention detail.

Patent discussion is preliminary innovation screening only. It is not legal advice, patentability analysis, freedom-to-operate analysis, or an instruction to file. Any real invention analysis belongs in a private downstream process with counsel review.

## Research Question

Given three Lattice/DataHub application scenarios, what existing industry patterns, product capabilities, and public patent literature should influence the guidance in PR #56?

The three scenarios are:

1. **Code-declared operational evidence verification**
   - Code declares an expected runtime effect, such as a structured log, Kafka event, database write, metric, or downstream call.
   - The agent must verify whether the effect actually occurred using DataHub as context and a live source as evidence.

2. **Pre-Silver / Silver data modeling**
   - Requirements and code explain business intent.
   - DataHub, profiling, lineage, query history, and targeted live data evidence help infer candidate entities, grain, keys, joins, temporal behavior, and quality constraints.
   - The goal is an evidence-backed Silver model candidate, not automatic table creation.

3. **Dashboard interaction-driven dynamic analytics**
   - A user clicks an existing chart and wants deeper information.
   - The agent must combine user-interaction context, codebase knowledge, DataHub/database context, and live data evidence.
   - The result should usually be an interaction-scoped analytical projection, not a permanent new Gold model.

## Executive Verdict

The best direction is not to build a new Lattice data platform or generic analytics agent.

The strongest architecture is:

```text
native coding / analytics agent
        |
        | uses
        v
Lattice routing, evidence, and context-minimization guidance
        |
        | composes with
        v
DataHub / Unity Catalog / governed semantic assets
        |
        | narrows
        v
approved live source or compute evidence
        |
        v
verified result, candidate learning, or governed stop
```

The three scenarios should be treated as related evidence-and-context workflows, not as separate platform products:

```text
Scenario 1: Code -> Expected Effect -> Live Evidence
Scenario 2: Business/Code -> Data Context -> Silver Candidate
Scenario 3: User Interaction -> Existing Semantics -> Temporary Projection
```

The reusable Lattice value is the reasoning discipline:

- distinguish context from source truth;
- preserve code, metadata, user interaction, and live data as different evidence classes;
- select minimum sufficient context;
- verify consequential claims against live evidence;
- avoid automatic promotion from inference to durable semantic truth;
- reuse DataHub, Databricks, Unity Catalog, and native agent capabilities first.

## Source and Evidence Classes

This report uses three evidence classes.

- `PUBLIC_SOURCE`: public product documentation, blogs, customer stories, or public patent publications.
- `ARCHITECTURAL_INFERENCE`: a design conclusion derived from public-source patterns.
- `PATENT_SCREENING`: public patent-literature observation that may affect novelty or claim framing.

## Industry Pattern 1 — Context Platform Before Agent Reasoning

### Finding

DataHub's current public positioning and customer stories show a shift from traditional data catalog to a broader context layer for AI agents.

The most relevant public pattern is Pinterest's DataHub use case. Pinterest describes a large data estate, governed context, AI-generated documentation, and query-history mining so agents can reason over trusted context rather than raw tables. Historical SQL is treated as evidence of how analysts solved real questions, and retrieval is ranked by governance and usage signals rather than embeddings alone.

### Lattice implication

Do not make the agent learn every database from scratch and do not build a parallel Lattice context platform.

Use DataHub as the primary cross-system context substrate when authorized, especially for:

- dataset discovery;
- schema and field context;
- lineage;
- ownership, domains, and glossary terms;
- usage and historical query patterns;
- quality/profiling where configured;
- context documents;
- MCP or published DataHub Agent Skills.

Lattice should add only the task-scoped selection and evidence discipline.

### Scenario impact

| Scenario | Effect |
|---|---|
| Operational evidence | DataHub narrows the destination, field mapping, owner, lineage, and likely index/table; live source proves occurrence. |
| Silver modeling | DataHub provides source inventory, profiling, lineage, query history, and context before model hypotheses. |
| Dynamic analytics | DataHub provides available governed semantic assets and source context before generating a temporary analytical projection. |

## Industry Pattern 2 — Governed Semantics Before Dynamic Analytics

### Finding

Databricks Unity Catalog Semantics and Metric Views indicate that governed business semantics, KPIs, metrics, and agent metadata are becoming first-class data-platform assets.

Databricks dashboard data modeling and local metric views also show a useful distinction: some modeling logic belongs in governed Unity Catalog, while exploratory or not-yet-hardened modeling can remain local to a dashboard or analysis until it is ready to promote.

### Lattice implication

Do not call every user-specific dynamic query a Gold model.

Use this distinction:

```text
Durable Gold / governed semantic model
  = reusable, reviewed, governed business semantics

Interaction-scoped analytical projection
  = temporary, bounded analytical shape for one user interaction or investigation
```

Only promote a temporary projection when there is evidence of stable semantics, repeated use, review, and a clear second-use path.

### Scenario impact

This is most important for dashboard-driven dynamic analytics. The default behavior should be:

```text
interaction
-> infer analytical intent
-> reuse existing governed semantic model if sufficient
-> create temporary projection only for a named gap
-> validate semantic continuity, security, grain, cost, and result
-> optional governed promotion candidate
```

## Industry Pattern 3 — Code-to-Operational-Evidence Mapping Has Prior Art

### Finding

Public patent literature includes examples of using source code to derive log-message patterns or to drill back from logs to source code. This means broad claims like "use code to understand logs" or "link log data to source code" are likely crowded.

### Lattice implication

For operational evidence, avoid framing the invention or architecture as generic code-to-log matching.

The stronger Lattice-specific pattern is:

```text
code-derived expected effect contract
-> bounded context orientation
-> live-source verification
-> positive-evidence identity gate
-> negative-evidence completeness gate
-> effect-path boundary attribution
-> candidate learning with no automatic promotion
```

The novelty, if any, is in the multi-plane evidence discipline and guarded attribution, not in simply mapping log text to code.

## Industry Pattern 4 — Automatic Schema / Ontology / Star-Model Generation Has Prior Art

### Finding

Public patents cover ontology induction from profiling and reference schemas, automatic transformation from normalized database structures to denormalized/star-like models, and semantic-layer query/model generation.

### Lattice implication

Do not claim that Lattice is inventing automatic Silver or star schema generation in general.

The safer distinction is:

```text
requirements + code semantics
+ DataHub context
+ observed data behavior
+ adversarial modeling questions
+ evidence-backed Silver candidate
+ governed promotion boundary
```

This keeps Lattice focused on evidence-backed decision support rather than automatic model generation.

## Industry Pattern 5 — Dashboard Drilldown and Semantic Query Are Mature, But Continuity Gates Remain Important

### Finding

Public patents and BI systems already include dashboard drilldown, interaction-driven filtering, natural-language drilldown, and semantic query generation from selected visual elements.

### Lattice implication

Do not claim generic dashboard drilldown or NL visual exploration.

The more useful pattern is:

```text
interaction snapshot
-> analytical intent contract
-> existing semantic reuse gate
-> semantic continuity gate
-> security continuity gate
-> temporary analytical projection
-> compute plan
-> result validation
-> optional promotion candidate
```

The key hard problems are:

- preserving metric semantics from the parent visual;
- inheriting hidden filters and tenant/security scope;
- avoiding fanout and double counting;
- separating analytical model from generated SQL;
- validating result consistency before UI display;
- preventing temporary analysis from becoming unreviewed Gold semantics.

## Proposal A — Compose Existing Context Substrates

### Summary

Use DataHub and Unity Catalog as existing substrate. Use Lattice only for routing, task-scoped projection, evidence discipline, and stop conditions.

```text
DataHub = cross-system context plane
Unity Catalog = Databricks governance and governed semantic plane
Native coding/analytics agents = reasoning and execution plane
Live sources/compute engines = current evidence plane
Lattice = context/evidence/authority discipline
```

### Strengths

- Lowest build risk.
- Best alignment with PR #56 guidance-only scope.
- Avoids duplicating DataHub and Databricks capabilities.
- Supports all three scenarios.

### Weaknesses

- Does not itself solve missing DataHub connectors, bad metadata, or poor source permissions.
- Depends on downstream environment configuration.
- Needs scenario-specific guidance so agents do not overuse DataHub or skip live evidence.

### Verdict

`KEEP / DEFAULT`.

This should be the baseline architecture.

## Proposal B — Evidence-Gated Operational Verification

### Summary

For code-declared external effects, use a code-derived expected effect contract and verify through a live-source evidence path.

```text
code/config
-> Expected Effect Contract
-> DataHub context only for orientation gaps
-> approved live evidence query
-> expected-vs-observed comparison
-> effect-path attribution or unknown
```

### Best suited for

- logging verification;
- Kafka/event publication;
- metrics emission;
- database writes;
- downstream API calls;
- workflow side effects.

### Innovation angle

Potentially interesting only if framed narrowly around:

- multi-plane evidence separation;
- negative-evidence qualification;
- effect-path boundary attribution;
- no automatic promotion from a single observed mapping.

### Patent risk

Broad code-to-log or log-to-code claims likely face prior art. The candidate must avoid those broad claims.

### Verdict

`KEEP / HARDENED IN PR #56`.

This is the first scenario already being strengthened.

## Proposal C — Evidence-Backed Silver Model Decision Harness

### Summary

Before building Silver, establish a modeling decision contract.

```text
Gold consumer need
-> business/code semantics
-> modeling questions
-> DataHub source context
-> targeted live data investigation
-> cross-source reconciliation
-> Silver model hypothesis
-> adversarial validation
-> Gold fit check
```

### Must distinguish

```text
Business rule != implemented code behavior != observed data behavior != DataHub context != live source evidence
```

### Key gates

- Gold consumer contract;
- modeling question contract;
- source-role classification;
- entity/grain/key validation;
- temporal semantics validation;
- schema-evolution review;
- cross-source completeness and authority checks;
- adversarial validation before Silver candidate approval.

### Innovation angle

The likely differentiator is not automatic model generation. It is the evidence-gated process for agent-assisted model decisions across requirements, code, metadata, and live data.

### Patent risk

Automatic ETL/star schema generation, ontology induction, and semantic mapping have substantial public prior art. Any claim should be narrow and mechanism-specific.

### Verdict

`ADAPT / NEXT GUIDANCE CASE`.

Worth adding as scenario guidance, not as platform code.

## Proposal D — Interaction-Scoped Analytical Projection

### Summary

For dashboard clicks, do not create a new durable Gold model by default. Create a temporary analytical projection only when existing semantics cannot answer the interaction.

```text
user interaction
-> interaction snapshot
-> analytical intent contract
-> existing semantic reuse gate
-> context fusion: code + DataHub + live data
-> temporary analytical projection
-> semantic/security/grain/cost validation
-> compute plan
-> result validation
-> UI response
-> optional reusable candidate
```

### Key gates

- interaction snapshot;
- analytical intent contract;
- existing semantic reuse gate;
- parent visual semantic contract;
- semantic continuity gate;
- security continuity gate;
- grain/cardinality/fanout validation;
- compute budget gate;
- result validation before UI display;
- promotion boundary.

### Innovation angle

This is the strongest product concept among the three scenarios.

However, generic dashboard drilldown and semantic query generation have substantial prior art. The possible novelty is the combination of:

- preserving parent visual semantics and security scope;
- using codebase + DataHub + live data + interaction context;
- generating a temporary projection rather than durable Gold;
- validating semantic continuity before compute/result display;
- promoting only through governed reuse evidence.

### Verdict

`ADAPT / HIGH-VALUE DESIGN PATTERN`.

Good candidate for further private invention review, but keep claim detail out of public Lattice.

## Cross-Scenario Unifying Pattern

The three scenarios can be unified as:

```text
Trigger / intent source
        |
        v
Task-specific contract
        |
        v
Minimum context orientation
        |
        v
Targeted live evidence
        |
        v
Verification / candidate / stop
```

Where the task-specific contract differs:

| Scenario | Contract |
|---|---|
| Code-declared operational evidence | Expected Effect Contract |
| Pre-Silver modeling | Modeling Question Contract / Gold Consumer Contract |
| Dashboard dynamic analytics | Interaction Snapshot / Analytical Intent Contract |

This suggests Lattice should not create three separate platforms. It should teach agents to recognize the contract type and then compose existing capabilities.

## Patent-Screening Notes

### Public prior-art signals

The following public publications are relevant and reduce the novelty of broad claims:

- `US20250291700A1` — code-derived log-message patterns and anomaly detection.
- `US20210303440A1` — contextual drill-back from log data to source code/resources.
- `US20250291837A1` — consistent semantic layer for disparate data sources, selective or late-binding indexed context.
- `US20260119520A1` — automatic ETL generation from normalized source tables to denormalized/star schema structures.
- `US20180052870A1` — ontology induction using statistical profiling and schema matching.
- `US9396474B2` — dashboard drill-down hierarchy and filter behavior.
- `US11429253B2` — integrated drill-down in natural-language visual analysis.
- `US11227018B2` — visual selection to semantic/reasoning query.
- `US20100017379A1` — semantic layer generating continuous queries from GUI input and semantic information.
- `US20180032216A1` — guided root-cause exploration through dashboard widgets and related entities.

### Avoid claiming

Avoid broad claims to:

- use AI to inspect a catalog;
- use code to find logs;
- generate SQL from natural language;
- generate a star schema from tables;
- dashboard drill-down;
- create a semantic layer over multiple sources;
- run live queries after metadata search.

These are crowded areas.

### Potential private invention-candidate directions

The following are only candidates for private counsel-guided review:

1. **Evidence-gated external-effect verification**
   - Code-derived expected effect contract;
   - DataHub/context orientation;
   - live-source verification;
   - positive identity and negative completeness gates;
   - effect-path attribution without premature failure assignment.

2. **Governed agent-assisted Silver modeling**
   - Gold consumer contract;
   - modeling question contract;
   - source-role and cross-source reconciliation;
   - adversarial model validation;
   - candidate status with no automatic promotion.

3. **Interaction-scoped analytical projection**
   - dashboard interaction snapshot;
   - parent visual semantic contract;
   - semantic and security continuity gates;
   - temporary projection compiled to compute plan;
   - result validation and governed promotion candidate.

### Patent verdict

`POSSIBLE BUT NARROW`.

The most promising direction appears to be the dashboard interaction pattern, followed by operational evidence verification. The Silver modeling direction has more crowded adjacent prior art around schema/ontology/model generation.

Any patent work should move to a private invention process. Public Lattice should keep only generic design patterns and avoid unpublished claim detail.

## Recommended Lattice Guidance Impact

### Add now

- Keep PR #56 guidance-only.
- Preserve DataHub as context substrate, not source truth.
- Preserve code/context/live evidence separation.
- Keep first scenario operational-evidence guidance.

### Add next, if continuing this PR

- A modeling-decision branch for Silver/Gold design.
- An interaction-driven analytics branch for dashboard dynamic projections.
- A compact scenario-router that distinguishes:

```text
code-originated runtime verification
modeling decision
interaction-driven analytics
data-originated discovery
```

### Do not add now

- new active module;
- new Skill by default;
- new DataHub adapter;
- new MCP server;
- new semantic model runtime;
- new patent/invention schema;
- public claim language.

## Source Notes

Public sources reviewed include:

- DataHub Pinterest customer story: https://datahub.com/customer-stories/pinterest/
- DataHub context-aware AI agents article: https://datahub.com/blog/context-aware-ai-agents/
- DataHub trusted context for talk-to-data town hall: https://datahub.com/blog/trusted-context-for-talk-to-data-april-2026-town-hall-highlights/
- DataHub Cloud 2.0 context intelligence notes: https://datahub.com/blog/datahub-cloud-2-0/
- DataHub context platform / June 2026 town hall material: https://datahub.com/blog/inside-the-context-platform-june-2026-town-hall-highlights/
- Databricks Unity Catalog Semantics: https://docs.databricks.com/aws/en/uc-semantics/
- Databricks Metric Views: https://docs.databricks.com/aws/en/uc-semantics/metric-views
- Databricks dashboard data modeling and local metric view documentation.
- Public Google Patents pages for the patent publications listed above.

## Final Recommendation

Use the research as strategic guidance only.

For PR #56, the best near-term outcome is:

```text
KEEP DataHub reuse guidance
KEEP code/runtime/live-evidence separation
ADD scenario awareness only when behaviorally validated
DEFER patent-detail and product-runtime work to private downstream processes
```
