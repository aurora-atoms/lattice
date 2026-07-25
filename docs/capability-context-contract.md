# Capability Context Contract

## Purpose

The capability context contract gives every reusable Skill and Agent a stable, versioned, machine-readable identity and a compact discovery profile without expanding runtime YAML frontmatter or copying full instructions into an always-on prompt.

The native runtime still discovers a Skill primarily from its `name` and `description`. The context registry is a governance, compatibility, evaluation, and progressive-discovery layer.

## Contract Location

- `registry/skill-context.index.jsonl`: one record for every `skills/**/SKILL.md` package.
- `registry/agent-context.index.jsonl`: one record for every Agent instruction registered in `registry/agents.index.jsonl`.
- `schemas/capability/capability-context.v1.schema.json`: shared record schema.
- `scripts/validate_capability_context.py`: semantic and inventory-drift validator.

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

Each record states:

- `changes`: the state, process, artifact, or delivery result the capability attempts to change.
- `primary_user`: the principal invoking role, usually an Agent or accountable practitioner.
- `secondary_audience`: reviewers, operators, managers, downstream agents, or other consumers.
- `triggers`: events, states, and request forms that support accurate native discovery, plus exclusions that reduce false positives.

The Skill `description` remains the primary runtime trigger. The registry must agree with it and may add structured trigger evidence for validators, routing evals, and runtime adapters.

## Required Inputs and Permissions

`required_inputs` identifies the smallest safe starting set:

- `minimum`: facts, artifacts, or decisions required to begin;
- `permissions`: required read, write, network, external-action, or approval boundaries;
- `tools`: critical tool classes, not an exhaustive catalog.

An empty permission or tool list means the capability requires no special permission or tool beyond the active runtime's normal safe context. It never grants permission.

## Optional Context

`optional_context` is progressive discovery guidance, not an eager dependency list.

Use it when the current evidence cannot meet the requested quality, confidence, or scope. It may direct the runtime to:

- discover a related Skill or Agent through native capability discovery;
- inspect a bounded neighboring codebase or project surface;
- retrieve similar cases, negative knowledge, decisions, or governed knowledge packs;
- perform deeper official-source research;
- request a human decision or domain review.

Optional context must remain bounded, source-aware, and permission-aware. Do not load every suggested capability or source by default.

## Agent Alignment

Agent context records use the same fields so orchestration can compare a Skill and its task-role Agent without duplicating full instructions. The Agent record must identify what state it changes, its primary user, secondary audience, triggers, minimum inputs, permission boundaries, optional discovery paths, and outputs.

## Compatibility and Authority

The contract standardizes discovery and handoff metadata. It does not:

- replace native runtime orchestration;
- authorize tool use, repository writes, merge, release, deployment, or production actions;
- turn optional context into automatic broad retrieval;
- supersede active Lattice modules;
- make a registry score an approval decision.
