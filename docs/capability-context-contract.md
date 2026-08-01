# Capability Context Contract

## Purpose

The capability context contract gives every reusable Skill and Agent a stable, versioned, machine-readable identity and a compact discovery profile without expanding runtime YAML frontmatter or copying full instructions into an always-on prompt.

The native runtime still discovers a Skill primarily from its `name` and `description`. The context catalogs are a governance, compatibility, evaluation, and progressive-discovery layer.

Lattice is the public reference and governance layer. Private downstream repositories pin these public identities and contracts while retaining all real business evidence, private extensions, adoption observations, and manager-ready artifacts.

## Contract Location

- `registry/capability-manifest.json`: canonical identity, version, role, public package status, path, behavior, evidence, success, stop, authority, compatibility, and projection metadata.
- `registry/skill-context.catalog.json`: one compact context entry for every `skills/**/SKILL.md` package.
- `registry/agent-context.catalog.json`: one compact context entry for every Agent instruction registered in `registry/agents.index.jsonl`.
- `schemas/capability/capability-context.v1.schema.json`: expanded context-record contract used by adapters and projections.
- `schemas/capability/capability-run-result.v1.schema.json`: mandatory structured run-result contract.
- `scripts/validate_capability_context.py`: semantic and inventory-drift validator.
- `scripts/generate_capability_registry_projections.py`: deterministic compatibility projection generator and drift check.
- `scripts/validate_capability_manifest.py`: canonical identity, role, status, path, description/trigger, deprecation, and parity validator.
- `schemas/capability/capability-profile-runtime.v1.schema.json`: task-scoped runtime authority, model-lane, verification, cache, handoff, human-factor, and telemetry contract.
- `scripts/validate_capability_profile.py`: deterministic Capability Profile boundary validator.

The canonical manifest is the source of truth. Catalogs, version policy, legacy indexes, and the cross-runtime capability index are generated compatibility projections. Catalog defaults still provide optional-context discovery and shared run requirements.

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

Permission and tool authority come from the Skill body, Agent manifest, active runtime, current user approval, and selected Capability Profile. The catalog never grants access. Tool availability does not imply permission.

For a task using a Capability Profile, the Profile is authoritative for effective model lanes, Skills, tools, knowledge, permissions, budgets, cache, and telemetry. Existing Agent manifest fields are compatibility defaults and may not silently broaden the selected Profile.

## Agent and Profile Runtime Boundary

The Agent owns role behavior:

```text
assess current state
select next action
stop
escalate
```

The Capability Profile owns the bounded execution environment:

```text
model routing
Skill activation
tool and MCP exposure
knowledge loading
permissions and approvals
token budget
cache policy
telemetry
verification gates
```

A Profile does not act. An Agent does not self-grant runtime authority. Runtime adapters must preserve this boundary even if a provider packages both concepts in one configuration surface.

## Model-Lane Context Rules

Model tier is not evidence status. Public profiles use vendor-neutral classes such as economy, coding, flagship, and human. Private runtime adapters may bind them to current provider models.

Cross-model handoffs must preserve:

```text
decision_required
verified_facts
conflicts
unknowns
evidence_refs
reason_for_escalation
```

Free-form summaries and full reasoning transcripts are not authoritative state. The receiving lane must be able to reopen evidence and independently reconstruct high-impact assumptions.

## Cache Context Rules

Cache identity is scoped by model lane and Profile version. At minimum it includes:

```text
profile_id
profile_version
model_lane
toolset_hash
schema_version
```

Do not assume cross-model cache reuse. Keep stable kernel, Profile, tool-schema, and output-schema content in the stable prefix. Keep current task, repository evidence, diff, tests, and runtime facts in the dynamic suffix.

A cache optimization cannot justify stale policy, excess tool exposure, or loading unrelated Skills and knowledge.

## Human-Factor Context Rules

Controllability, competence, cognitive clarity, safe dissent, and collective efficacy are design hypotheses until observed. Public profiles must not claim these outcomes as proven.

Telemetry must not be used for personnel ranking. Profile design should avoid choice overload, approval fatigue, surveillance, replacement framing, and zero-error promises.

## Optional Context

`optional_context_discovery` is progressive discovery guidance, not an eager dependency list. Use it only when current evidence cannot meet the requested quality, confidence, or scope. Optional context must remain bounded, source-aware, and permission-aware.

## Compatibility and Authority

The contract standardizes discovery, outputs, evidence, success assessment, stopping behavior, and Profile runtime boundaries. It does not:

- replace native runtime orchestration;
- authorize tool use, repository writes, merge, release, deployment, or production actions;
- turn optional context into automatic broad retrieval;
- authorize endless retry;
- supersede Helixion, AegisFlow, Memexa, FlowGuard, OpenClaw, DeliveryYield, or another active module;
- make a registry score, model tier, model consensus, or success signal an approval decision.

## Public and Downstream Ownership

Public Lattice owns public capability identities, behavior contracts, package versions, reference workflows, profile templates, schemas, validators, synthetic fixtures, and compatibility projections.

Private repositories own real `feature_delivery_case` records, source and business context, delivery evidence, private extensions, human feedback, adoption state, reusable assets, provider model bindings, and manager deliverables. Catalog discovery never grants access to those artifacts.

```text
public_package_status =
  draft | contract_validated | conformance_validated | released | deprecated

downstream_adoption_status =
  not_observed | imported | task_scoped | used_once | reused | team_available | deprecated
```

These lifecycles must not share one ambiguous status field. Public synthetic fixtures declare `simulation_status=synthetic_reference` and `downstream_adoption_status=not_observed`. Public conformance cannot establish use, reuse, team availability, manager acceptance, ROI, emotional impact, or private business value.

Capability roles follow `docs/capability-taxonomy.md`. A selector, reference workflow, profile, projection, validator, or template cannot be counted as an executed atomic outcome capability.

Downstream consumers follow `docs/downstream-private-repository-contract.md`; manager-facing claims follow `docs/manager-credibility-contract.md`. DeliveryYield, validators, selectors, registries, and success signals provide evidence only and do not approve delivery, asset promotion, manager wording, release, or private adoption.
