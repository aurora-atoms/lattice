# Capability Taxonomy

## Purpose

This taxonomy keeps discovery, composition, execution, projection, and validation roles distinct. A path or package may expose a compatibility entry, but every canonical public capability has one primary `capability_role`.

## Roles

```text
atomic_capability
  Performs one bounded, independently evaluable capability.

selector
  Chooses the smallest justified capability or profile; it is not outcome evidence.

reference_workflow
  Describes an ordered composition and handoffs; it is not eagerly loaded runtime context.

capability_profile
  Declares a task-scoped minimum set of capabilities and contracts.

projection
  Deterministically transforms canonical records for an audience or runtime.

validator
  Deterministically checks a contract and emits machine-readable pass/fail evidence.

template
  Provides a public-safe starting shape; it is not proof that a real artifact exists.

governance_contract
  Defines identity, compatibility, evidence, authority, lifecycle, or release rules.
```

Agent is a packaging/runtime record type, not a substitute for `capability_role`. Workflow, profile, selector, atomic capability, schema, validator, and template must not be counted as equivalent outcome capabilities.

## Composition Rules

- A selector returns a decision and bounded handoff; it does not perform every selected capability.
- A reference workflow names order, inputs, outputs, review gates, and stop conditions; it is not a mega Skill.
- A Capability Profile is least-privilege context selection, not a bundle that loads all optional capabilities.
- An atomic capability owns one reviewable result.
- A projection cannot alter canonical evidence or increase claim strength.
- A validator cannot approve business value, asset promotion, release, or `team_available`.
- A template and synthetic fixture prove shape only.
- A governance contract preserves human authority and cannot become a new control module.

## Capability Composition Layer

Capability identity and multi-stage concept composition are separate contracts.

`registry/capability-manifest.json` remains the canonical identity source. It answers what a public capability is, its version, role, package status, compatibility, and authority boundary.

`concepts/<concept-id>/concept.json` answers a different question: how already-existing workflows, schemas, validators, templates, examples, tests, and CI form one agent-readable concept. It may reference multiple capability roles and repository layers without creating a new module or changing any referenced capability's identity.

The compact discovery projection is `registry/capability-compositions.index.jsonl`. Consuming agents use it only when a task spans multiple stages or when upstream/downstream relationships are otherwise ambiguous.

Composition activation semantics are:

```text
always            stable concept routing only when explicitly justified
task_scoped       load for the selected current stage
reference_only    load only when the current output requires it
never_by_default  do not load into ordinary model context
```

A deterministic validator may be marked `never_by_default` with action `execute`: the agent should run it when required without treating its implementation source as task knowledge. Tests and CI remain maintainer evidence and are never normal task context.

Composition metadata cannot promote a Skill template to an active capability, alter a release or safety verdict, increase evidence strength, or grant human authority.

## Agent and Capability Profile Boundary

An Agent and a Capability Profile are composed at runtime but own different concerns.

```text
Agent owns:
  role
  state assessment
  next-action selection
  stop
  escalation

Capability Profile owns:
  model routing
  Skill activation
  tool and MCP exposure
  knowledge loading
  permissions and approvals
  token budget
  cache policy
  telemetry requirements
  verification gates
```

Existing Agent manifests may retain Skills, MCP, knowledge, token, cache, install, and telemetry fields as compatibility defaults. They do not grant runtime authority. The selected task Capability Profile is authoritative and may only narrow, not silently broaden, the effective runtime boundary.

A Profile does not act or decide the next step. An Agent does not self-assign models, tools, permissions, or delivery authority.

The enforceable runtime contract is defined in `docs/capability-profile-runtime-contract.md` and `schemas/capability/capability-profile-runtime.v1.schema.json`.

## Model Authority Is Not Model Tier

Model price, size, or product label does not determine evidence status. Capability Profiles must state the maximum authority of each vendor-neutral model lane and require external verification.

```text
economy -> candidate
coding -> candidate_change
flagship -> judged
human -> human_decision
```

A cheaper model may produce a reliable result when deterministic evidence establishes it. A flagship model cannot self-confirm delivery or override failed machine checks.

## Human Factors Are Design Hypotheses

Capability Profiles may target controllability, competence, cognitive clarity, safe dissent, and collective efficacy, but these outcomes remain hypotheses until observed in real use.

Profiles must avoid choice overload, approval fatigue, surveillance, replacement framing, and zero-error promises. Telemetry is for system improvement, not personnel ranking.

## Initial Workflow Families

```text
Experience-to-Asset
  workflow: contribution -> candidate -> proposal -> review -> scoped activation -> observation
  profile: smallest assets/evidence/review capabilities for one case
  selectors: native discovery or thin compatibility routing
  atomic capabilities: bounded contribution, candidate, review, observation, dossier work

Feature Understanding
  workflow: contract -> bounded context -> model -> challenge -> verify -> commit
  profile: task-scoped understanding capabilities
  selector: thin compatibility entry
  atomic capabilities: domain-context-pack, system-mental-model,
    contradiction-adjudication, unasked-questions-generator, reviewer-rehearsal

Evidence Wayfinding
  workflow: orient -> route -> sense -> model -> challenge -> frontier -> verify -> decide -> deliver -> settle -> evolve
  profile: senior-decision-wayfinding synthetic reference profile
  selector: delivery-capability-conductor
  shared object: feature_delivery_case
  atomic capabilities: existing understanding, challenge, decision, delivery, outcome, and learning capabilities
  candidate capability: frontier-practice-scout remains non-active until the Direction Investment Gate is satisfied
  reference: docs/evidence-wayfinding.md and docs/evidence-wayfinding/blueprint-preserved.md

Manager Evidence Projection
  workflow: evidence -> claim classification -> limitations -> wording review -> brief
  profile: bounded evidence and management projection capabilities
  selector: thin compatibility entry
  atomic capabilities: management-translation and relevant specialist packages

Reusable Asset Review
  workflow: candidate -> compatibility -> evidence -> human review -> activation decision
  profile: review and governance capabilities only
  selector: thin compatibility entry
  atomic capabilities: existing review, judgment, and evidence specialists
```

These are logical classifications, not new modules or mega Skills. Existing paths remain compatibility entrances until a reviewed migration says otherwise.

## Canonical Metadata

`registry/capability-manifest.json` is the single identity source for:

```text
capability_id
family_name
version
capability_role
public_package_status
path
description
primary_user
secondary_audience
trigger
minimum_inputs
outputs
evidence_contract
success_signals
stop_conditions
authority_boundary
compatibility
deprecated_by
```

Current registries are deterministic compatibility projections. `scripts/validate_capability_manifest.py` rejects missing roles, status or version drift, missing paths, native-description drift, description/trigger conflict, adoption state in public records, and deprecated capabilities referenced by active routing or profiles.
