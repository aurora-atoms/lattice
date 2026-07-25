# Capability Context Contract

## Purpose

The capability context contract gives every reusable Skill and Agent a stable, versioned, machine-readable identity and a compact discovery profile without expanding runtime YAML frontmatter or copying full instructions into an always-on prompt.

The native runtime still discovers a Skill primarily from its `name` and `description`. The context catalogs are a governance, compatibility, evaluation, and progressive-discovery layer.

## Contract Location

- `registry/skill-context.catalog.json`: one compact context entry for every `skills/**/SKILL.md` package.
- `registry/agent-context.catalog.json`: one compact context entry for every Agent instruction registered in `registry/agents.index.jsonl`.
- `schemas/capability/capability-context.v1.schema.json`: expanded context-record contract used by adapters and projections.
- `scripts/validate_capability_context.py`: semantic and inventory-drift validator.

Catalog defaults provide the contract name, contract version, default capability version, semantic-version policy, and shared optional-context discovery instruction. A runtime adapter may expand each compact entry into the full schema without changing its meaning.

## Identity and Versioning

Use stable identifiers:

```text
skill:<skill-name>@<semantic-version>
agent:<agent-name>@<semantic-version>
```

The unversioned name remains the stable family identifier. Apply semantic versioning to the behavior contract:

- **Patch**: wording, examples, discovery clarity, or validation fixes that do not change required inputs, permissions, outputs, or externally observable behavior.
- **Minor**: backward-compatible trigger additions, optional context, outputs, tools, or workflow capabilities.
- **Major**: incompatible trigger narrowing, required-input or permission changes, removed outputs, changed authority boundary, or changed behavior semantics.

A new version does not silently delete the prior contract. Deprecation must be explicit, and compatibility consumers must be able to identify the prior stable family and version.

## Discovery Fields

Each entry states:

- `changes`: the state, process, artifact, or delivery result the capability attempts to change.
- `primary_user`: the principal invoking role, usually an Agent or accountable practitioner.
- `secondary_audience`: reviewers, operators, managers, downstream agents, or other consumers.
- `trigger`: the event, state, or request condition that should make native discovery consider the capability.

The Skill `description` remains the primary runtime trigger. The catalog must agree with it and adds structured evidence for validators, routing evals, and runtime adapters.

## Required Inputs and Permissions

`minimum` identifies the smallest safe facts, artifacts, or decisions required to begin. Permission and tool authority still come from the Skill body, Agent manifest, active runtime, and current user approval; the catalog never grants access.

Runtime adapters may project explicit `permissions` and `tools` arrays when the target runtime needs them. Empty arrays mean no additional grant, not unrestricted access.

## Optional Context

`optional_context_discovery` is progressive discovery guidance, not an eager dependency list.

Use it only when current evidence cannot meet the requested quality, confidence, or scope. It may direct the runtime to:

- discover a related Skill or Agent through native capability discovery;
- inspect a bounded neighboring codebase or project surface;
- retrieve similar cases, negative knowledge, decisions, or governed knowledge packs;
- perform deeper official-source research;
- request a human decision or domain review.

Optional context must remain bounded, source-aware, and permission-aware. Do not load every possible capability or source by default.

## Agent Alignment

Agent entries use the same semantic fields so orchestration can compare a Skill and its task-role Agent without duplicating full instructions. Agent entries additionally name their canonical instruction path.

## Compatibility and Authority

The contract standardizes discovery and handoff metadata. It does not:

- replace native runtime orchestration;
- authorize tool use, repository writes, merge, release, deployment, or production actions;
- turn optional context into automatic broad retrieval;
- supersede Helixion, AegisFlow, Memexa, FlowGuard, OpenClaw, DeliveryYield, or another active module;
- make a registry score an approval decision.
