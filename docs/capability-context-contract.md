# Capability Context Contract

## Purpose

The capability context contract gives every reusable Skill and Agent a stable, versioned, machine-readable identity and a compact discovery profile without expanding runtime YAML frontmatter or copying full instructions into an always-on prompt.

The native runtime still discovers a Skill primarily from its `name` and `description`. The context catalogs are a governance, compatibility, evaluation, and progressive-discovery layer.

Lattice is the public reference and governance layer. Private downstream repositories pin these public identities and contracts while retaining all real business evidence, private extensions, adoption observations, and manager-ready artifacts.

## Contract Location

- `registry/skill-context.catalog.json`: one compact context entry for every `skills/**/SKILL.md` package.
- `registry/agent-context.catalog.json`: one compact context entry for every Agent instruction registered in `registry/agents.index.jsonl`.
- `schemas/capability/capability-context.v1.schema.json`: expanded context-record contract used by adapters and projections.
- `schemas/capability/capability-run-result.v1.schema.json`: mandatory structured run-result contract.
- `scripts/validate_capability_context.py`: semantic and inventory-drift validator.

Catalog defaults provide the contract name, contract version, default capability version, semantic-version policy, optional-context discovery instruction, structured run-result schema, evidence policy, success policy, and stop policy. Every cataloged Skill and Agent inherits these mandatory run requirements.

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

A new version does not silently delete the prior contract. Deprecation must be explicit.

## Discovery Fields

Each entry states:

- `changes`: the state, process, artifact, or delivery result the capability attempts to change.
- `primary_user`: the principal invoking role.
- `secondary_audience`: reviewers, operators, managers, downstream agents, or other consumers.
- `trigger`: the event, state, or request condition that should make native discovery consider the capability.
- `minimum`: the smallest safe facts, artifacts, or decisions required to begin.
- `outputs`: the capability-specific visible products expected from a successful or partial run.

The Skill `description` remains the primary runtime trigger. The catalog must agree with it.

## Structured Output and Writeback

Every run must emit a `lat.capability.run_result.v1` object. It must be written to:

```text
artifacts/capability-runs/<capability-name>/<run-id>/run-result.json
```

When write permission is unavailable, return the full structured object inline and mark the artifact `write_status=returned_inline`.

A run result must identify:

- status;
- visible artifacts, formats, locations, and write status;
- evidence;
- success signals;
- stop reason, retry state, and next step;
- generation time.

A hidden internal conclusion is not a completed output.

## Evidence Contract

Every run result must separate:

```text
facts
inference_summary
citations
uncertainty
unknowns
assumptions
```

Facts require addressable source references. Inferences must name the facts or evidence they rely on. Guesses, incomplete information, stale information, and inaccessible sources must be recorded explicitly rather than blended into factual claims.

When the evidence boundary prevents reliable further analysis, prediction, comparison, or recommendation, stop with `insufficient_evidence` rather than continue speculative reasoning.

## Success Signals

Every capability must evaluate at least one declared success signal. Each signal returns:

```text
met
not_met
not_evaluated
```

Producing a file is not automatically success. Success requires the capability-specific output, validation, acceptance, quality, or readiness criteria to be supported by evidence.

## Stop Conditions and Retry Boundaries

The default retry budget is one bounded retry after the initial attempt. More retries require explicit user instruction or a deterministic retry policy declared by the selected capability.

Stop when:

- the requested goal is reached;
- the next reviewable stage gate is reached and continuation was not explicitly authorized;
- required input is missing;
- permission is missing;
- a required source, repository, tool, or internet connection is unavailable;
- evidence is insufficient;
- validation fails after the bounded retry;
- a security, privacy, compliance, data-governance, architecture, production, or other high-risk boundary is reached;
- a human decision is required;
- the retry budget is exhausted;
- the user explicitly stops the task.

For a permission stop, state the exact permission, system owner or accountable role, reason it is needed, and the step that can resume after access is granted. Do not repeatedly probe or attempt bypasses.

Unless the user explicitly requests end-to-end autonomous continuation, stop at the next meaningful reviewable artifact or stage and request review before proceeding.

## Required Inputs, Permissions, and Tools

Permission and tool authority come from the Skill body, Agent manifest, active runtime, and current user approval; the catalog never grants access. Tool availability does not imply permission.

## Optional Context

`optional_context_discovery` is progressive discovery guidance, not an eager dependency list. Use it only when current evidence cannot meet the requested quality, confidence, or scope. Optional context must remain bounded, source-aware, and permission-aware.

## Compatibility and Authority

The contract standardizes discovery, outputs, evidence, success assessment, and stopping behavior. It does not:

- replace native runtime orchestration;
- authorize tool use, repository writes, merge, release, deployment, or production actions;
- turn optional context into automatic broad retrieval;
- authorize endless retry;
- supersede Helixion, AegisFlow, Memexa, FlowGuard, OpenClaw, DeliveryYield, or another active module;
- make a registry score or success signal an approval decision.

## Public and Downstream Ownership

Public Lattice owns public capability identities, behavior contracts, package versions, reference workflows, profile templates, schemas, validators, synthetic fixtures, and compatibility projections.

Private repositories own real `feature_delivery_case` records, source and business context, delivery evidence, private extensions, human feedback, adoption state, reusable assets, and manager deliverables. Catalog discovery never grants access to those artifacts.

```text
public_package_status =
  draft | contract_validated | conformance_validated | released | deprecated

downstream_adoption_status =
  not_observed | imported | task_scoped | used_once | reused | team_available | deprecated
```

These lifecycles must not share one ambiguous status field. Public synthetic fixtures declare `simulation_status=synthetic_reference` and `downstream_adoption_status=not_observed`. Public conformance cannot establish use, reuse, team availability, manager acceptance, ROI, or private business value.

Capability roles follow `docs/capability-taxonomy.md`. A selector, reference workflow, profile, projection, validator, or template cannot be counted as an executed atomic outcome capability.

Downstream consumers follow `docs/downstream-private-repository-contract.md`; manager-facing claims follow `docs/manager-credibility-contract.md`. DeliveryYield, validators, selectors, registries, and success signals provide evidence only and do not approve delivery, asset promotion, manager wording, release, or private adoption.
