# Repository AI Guidance

Lattice is a public, evidence-grounded delivery capability reference and governance repository. Private downstream repositories own real business context, delivery evidence, extensions, adoption observations, and manager-ready assets.

## Native and Progressive Discovery

1. Use the active runtime's native agent loop, Skill discovery, context management, permissions, sandbox, and tools first.
2. Select the smallest sufficient capability. Do not load all Skills, Agents, knowledge, or workflows by default.
3. `registry/capability-manifest.json` is the canonical identity, version, role, public-status, compatibility, and authority source. For compact discovery, consult its generated `registry/skill-context.catalog.json` or `registry/agent-context.catalog.json` projection before loading a capability body.
4. Load progressively:

```text
native name and description
-> compact capability context
-> selected Skill or Agent
-> named reference, schema, script, or bounded evidence
-> optional context only for a named quality gap
```

5. Use `scripts/route_capabilities.py` only as a compatibility/evaluation fallback when native selection is unavailable, ambiguous, or explicitly under test.

Native workspaces own capability discovery. Cross-workspace handoffs standardize bounded evidence, unknowns, conflicts, counterevidence, authority, privacy, and verification requirements; they must not require a shared or runtime-specific discovery projection.

## Concept Composition Discovery

Capability identity and multi-stage composition are separate. Do not infer a concept from folder adjacency.

- For one bounded atomic task, continue to use native discovery and `registry/capability-manifest.json`.
- When a goal spans multiple workflow stages, or when the relationship among `docs/`, schemas, validators, templates, examples, tests, and CI is unclear, consult `registry/capability-compositions.index.jsonl`.
- Each compact row points to a concept entrypoint. `concepts/<concept-id>/concept.json` is authoritative only for stage composition, handoff conditions, artifact roles, and activation scopes; it is not a second capability identity source.
- Load `task_scoped` artifacts only for the current stage. Load `reference_only` artifacts only when the current output requires them. Do not load `never_by_default` artifacts into ordinary model context.
- A validator may be `never_by_default` with action `execute`: run it when required without reading its implementation as task knowledge. Tests and CI are maintainer evidence, not runtime context.
- Composition metadata never changes evidence strength, capability package status, safety/release verdicts, IP/legal conclusions, or human authority.

For public or fully synthetic safety-critical innovation work, start with `concepts/safety-critical-adversarial-innovation/README.md`. The concept explicitly connects Safety-Critical Product Review -> Adversarial Innovation Mining -> Systematic Invention Research and tells the agent when to enter or stop each stage.

## Direction Before Capability

Before creating a new Skill, Agent, capability profile, reference workflow, governance surface, or internal platform—or materially expanding an existing one—apply the [Direction Investment Gate](docs/direction-investment-gate.md).

1. Select exactly one primary value path:
   - `current_product_delivery`: a specific user-usable product, customer, defect, or delivery outcome;
   - `strategic_asset`: a verifiable company-advantaged dataset, benchmark, prototype, protocol, decision model, or intellectual-property candidate with at least a second use;
   - `team_reuse`: a reusable internal capability backed by observed second-use demand and an accountable adoption owner.
2. Prefer the sequence `current_product_delivery -> strategic_asset_candidate -> proven_second_use -> optional_team_distribution`. Do not build a team reuse system first and search for demand later.
3. Treat PRs, Skills, registries, profiles, dashboards, and platform components as means, not value outcomes.
4. A new capability must state why existing active capabilities, modules, scripts, schemas, or workflows are insufficient.
5. When evidence supports only a plausible idea, keep it candidate-scoped and bind it to a real delivery or validation case. Do not promote it by assertion.
6. Stop or defer when the primary beneficiary, user outcome, proprietary advantage, verification method, second use, maintenance owner, or authority boundary cannot be established.

For newly created Skill packages, include the machine-checkable `## Direction Fit` block from `templates/direction-fit.template.md`. The Skill authoring validator rejects a new package without it.

## Public–Private Boundary

- Public Lattice owns public contracts, capability packages, reference workflows, schemas, validators, templates, and synthetic conformance fixtures.
- Private repositories own real `feature_delivery_case` records, source code, tickets, PRs, CI, incidents, reviews, employee feedback, private extensions, adoption observations, and manager deliverables.
- Never copy private business evidence, secrets, real delivery traces, or manager materials into Lattice.
- Synthetic fixtures use `simulation_status=synthetic_reference` and `downstream_adoption_status=not_observed`; they cannot prove real use, reuse, team adoption, manager acceptance, ROI, or business value.
- Route downstream integration to `docs/downstream-private-repository-contract.md` and manager wording to `docs/manager-credibility-contract.md`.

## Data Context / DataHub Entry

For tasks that require understanding heterogeneous databases, Databricks, Parquet/data-lake assets, Elasticsearch/log data, BI models, lineage, query history, profiling, or pre-Silver/Gold data context, do **not** start by designing a new Lattice data platform.

First classify the question. Use the existing context capabilities and the [DataHub Context Guidance](docs/datahub-context-guidance.md):

```text
code-originated runtime question
  -> context-mastery -> system-mental-model -> inspect code
  -> expected effect contract
  -> task-scoped DataHub orientation only when needed
  -> approved live-source query -> verify or falsify

data-originated discovery question
  -> context-mastery -> domain-context-pack
  -> authorized DataHub discovery
  -> approved live-source query when current evidence is required

modeling decision: "what evidence supports a Silver model candidate?"
  -> context-mastery -> domain-context-pack
  -> Gold Consumer Contract + Modeling Question Contract
  -> minimum authorized DataHub context
  -> targeted live-data evidence and cross-source reconciliation
  -> adversarial challenge + Gold-fit check
  -> candidate / partial / blocked -> human review

interaction-driven analytics: "a user selected an existing visual and wants deeper information"
  -> self-service-analytics-mvp-builder
  -> Interaction Snapshot + Analytical Intent
  -> Parent Visual Semantic Contract
  -> Existing Semantic Reuse Gate
  -> named code/data gap only -> bounded context-mastery or DataHub/live evidence
  -> Interaction-Scoped Analytical Projection
  -> semantic/filter/security/grain/cost validation
  -> compute plan + result validation
  -> reusable candidate only -> human review
```

The default rules are:

- prefer existing DataHub metadata, lineage, usage, query-history, quality, search, MCP, and published Agent Skills before proposing custom retrieval, catalog, profiler, lineage, MCP, or generic data-agent infrastructure;
- keep DataHub as prior orientation, not source truth; verify consequential claims against live source data or runtime evidence;
- for a code-originated side-effect question, establish what the code should emit, write, publish, call, or measure before searching a data or observability system;
- when expected evidence is absent, inspect the complete effect path, including trigger, configuration, serialization, transport, ingestion, transformation, destination, environment, time, and query correctness, before attributing failure;
- tool or MCP availability does not grant source permission, and DataHub access does not grant permission to query a live source;
- load context progressively: discovery -> relevant schema/lineage -> query/usage/quality signals only when they change the next decision -> raw values only for a named evidence gap and with permission;
- never load the full catalog, graph, query history, logs, samples, or raw data by default;
- use `skills/context-mastery/SKILL.md` to select the understanding path and `skills/domain-context-pack/SKILL.md` to enforce the smallest sufficient authorized context;
- for a modeling decision, start from the downstream consumer and named modeling questions; classify field-level source roles, verify grain/key/join/time/dedup assumptions against targeted live evidence, and keep the result candidate-scoped;
- use `system-mental-model` in a modeling task only when bounded code inspection is needed to establish implemented semantics; source code does not automatically determine the route or desired business meaning;
- treat DataHub relationships as candidate joins, profiling uniqueness as a hypothesis, and historical queries as usage evidence rather than business authority;
- for an interaction-driven request, treat the click as intent evidence rather than a complete specification; reuse governed analytics before composing a temporary projection;
- preserve the parent metric, material filters, authorization ceiling, time semantics, grain, and aggregation behavior; do not treat successful generated SQL as semantic validation;
- use `self-service-analytics-mvp-builder` as the primary owner; use context capabilities only for a named evidence gap, and never promote an interaction projection directly to Gold or a durable metric;
- use `skills/hybrid-knowledge-retrieval-builder/SKILL.md` only for an actual retrieval-build/evaluation task after an existing DataHub capability is shown insufficient;
- keep real schemas, lineage, queries, samples, incidents, business semantics, credentials, and endpoints private downstream.

Do not create a new DataHub-specific Lattice module or duplicate DataHub Skill merely to expose these rules. The guidance is a task-scoped reference for existing context capabilities.

## Senior Attention Entry

For a bounded feature-requirement, risk-preflight, bug/rescue, decision-support, or management-translation task that genuinely requires scarce expert judgment, start with [Senior Attention](docs/senior-attention.md) and the registered `workspaces/templates/senior-attention-runtime-profile.v1.json` profile. Treat that profile as an allowlist for progressive discovery, not an instruction to load every listed Skill. Keep real task evidence, owners, outcomes, attention measurements, and proprietary extensions in the private downstream repository.

Do not create a parallel Senior Attention Skill, Agent, module, fact store, or always-on conductor. `senior-attention-queue` is only for multiple competing expert requests; a single decision follows the normal bounded decision path.

## Safety-Critical Product Review Entry

For a safety-critical or consequential cyber-physical product requirement, architecture/code review, runtime-evidence review, adversarial test, failure classification, or release recommendation, start with [Safety-Critical Product Review](docs/safety-critical-product-review.md). Use the Senior Attention profile as the runtime allowlist and select only the smallest existing capability for the current evidence gap; do not create a parallel safety Skill, Agent, module, or automated release authority.

- Evaluate and normalize the source requirement before tracing it.
- Preserve the complete `Requirement -> Invariant -> Enforcement -> Runtime Evidence -> Adversarial Test -> Failure Classification -> Release Gate` chain.
- Keep severity, evidence status, reproducibility, finding status, and release impact separate.
- Treat missing load-bearing evidence and every non-closed S0/S1 finding as release-blocking.
- Run adversarial tests only in explicitly authorized, isolated environments.
- Treat `pass_candidate` as a recommendation only; humans retain safety, regulatory, architecture, deployment, and release authority.
- Keep real product requirements, code, telemetry, incidents, owners, and release decisions in the private downstream repository.
- When a reproduced public/synthetic hard case is being mined for a reusable technical mechanism or patent-research candidate, route through `concepts/safety-critical-adversarial-innovation/README.md` rather than jumping directly from a release finding to patent language.

## Public Research and Invention Learning Entry

For public-only patent learning, technique mining, systematic invention training, or creation of a portable research Agent Skill, start with [Systematic Invention Research Stack](docs/systematic-invention-research-stack.md).

- Treat the workflow as evidence-first research, not a patentability, FTO, infringement, or novelty opinion.
- Accept only published/public sources, user-confirmed public material, or fully synthetic examples.
- Stop concrete analysis for employer/client confidential material, internal source code or architecture, private experiments/data, or an unpublished real invention; do not bypass the boundary by anonymizing or paraphrasing.
- Preserve `FACT`, `INFERENCE`, `HYPOTHESIS`, and `UNKNOWN` separately; every load-bearing fact needs a source reference.
- De-duplicate by patent family and inspect independent claims for high-value samples.
- Challenge apparent gaps before retaining them.
- Keep large corpora and examples outside `SKILL.md`; use progressive disclosure and deterministic scripts for normalization, validation, statistics, and report scaffolding where practical.
- Use `templates/systematic-invention-research-agent-skill/` as a portable downstream Skill template for GitHub Copilot, Gemini CLI, and other Agent-Skills-compatible runtimes. Re-verify current vendor documentation before installation.
- Store compact evidence receipts and structured artifacts rather than raw transcripts or hidden chain-of-thought.
- When the candidate originates from a safety-critical hard case, preserve the `lat.adversarial-innovation-handoff.v1` boundary and enter through the matching concept composition instead of treating the safety finding itself as novelty evidence.

This reference workflow does not create a new active Lattice module or automatically promote a downstream Skill to `team_available`.

## Skill Authoring Gate

Any change under `skills/<name>/` must follow:

```text
root AGENTS.md
-> skills/lattice-governor/SKILL.md
-> docs/skill-authoring-gate.md
-> docs/capability-context-contract.md
-> registry/skill-context.catalog.json
-> registry/capability-context-policy.json
-> target SKILL.md and bounded supporting files
```

Use `skill-token-refactor` additionally for an existing Skill rewrite, compression, split, or migration.

For every changed Skill package:

- increase its semantic version in `registry/capability-context-policy.json`;
- preserve or update its catalog and compatibility projections;
- keep non-empty `Outputs`, `Evidence`, `Success Signals`, and `Stop Conditions`;
- define visible structured output and writeback;
- run `scripts/validate_skill_change_contract.py` against the PR base and head refs;
- stop for review when compatibility, source behavior, permission, evidence, or authority cannot be established.

Do not create a parallel governance Skill or a new control module. Extend `lattice-governor`, the authoring gate, templates, schemas, validators, or existing modules within their owned boundaries.

## Identity, Version, and Compatibility

- Project identity is `Lattice`, `lattice`, and `lat`; do not use `lattice` as a module, Agent, Schema, Artifact, or Record name.
- Capability identity uses `skill:<name>@<semver>` or `agent:<name>@<semver>`.
- Version changes to required inputs, permissions, outputs, evidence, success, stop behavior, authority, or behavior semantics under `docs/capability-context-contract.md`.
- Public package status and private downstream adoption status are separate lifecycles.
- Regenerate registry projections with `scripts/generate_capability_registry_projections.py`; never hand-edit a generated capability record.
- Regenerate concept composition projections with `scripts/generate_capability_composition_registry.py`; never treat a composition projection as capability identity.
- Run `scripts/validate_capability_manifest.py`, `scripts/validate_capability_compositions.py`, and `scripts/validate_public_private_boundary.py` before finalizing identity, composition, role, status, profile, or fixture changes.
- Preserve compatibility entrances or publish an explicit migration note; do not silently rename, remove, or reclassify a public capability.

## Required Result and Human Authority

Every selected Skill or Agent emits a visible result conforming to `schemas/capability/capability-run-result.v1.schema.json`, normally at:

```text
artifacts/capability-runs/<capability-name>/<run-id>/run-result.json
```

Separate facts, inference, citations, uncertainty, unknowns, and assumptions; evaluate success signals; state stop reason, retries, permission gap, and next step. Return the full result inline if write permission is unavailable.

Humans retain authority for private business conclusions, scope, security, compliance, architecture, asset promotion, `team_available`, manager wording, merge, release, deployment, and production. DeliveryYield signals never approve delivery or promotion.

## Stop Conditions

Stop at the requested result or next reviewable stage unless end-to-end continuation is explicit. Default to one bounded retry. Stop without bypass attempts for missing input, permission, source access, evidence, failed validation, high-risk boundaries, or required human decisions.

The Feature Delivery Case remains the primary user-value and evidence boundary. Do not supersede Helixion, AegisFlow, Memexa, FlowGuard, OpenClaw, DeliveryYield, or another active module.
