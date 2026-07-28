# Repository AI Guidance

Lattice is a public, evidence-grounded delivery capability reference and governance repository. Private downstream repositories own real business context, delivery evidence, extensions, adoption observations, and manager-ready assets.

## Native and Progressive Discovery

1. Use the active runtime's native agent loop, Skill discovery, context management, permissions, sandbox, and tools first.
2. Select the smallest sufficient capability. Do not load all Skills, Agents, knowledge, or workflows by default.
3. When compact metadata is needed, consult `registry/skill-context.catalog.json` or `registry/agent-context.catalog.json` before loading a capability body.
4. Load progressively:

```text
native name and description
-> compact capability context
-> selected Skill or Agent
-> named reference, schema, script, or bounded evidence
-> optional context only for a named quality gap
```

5. Use `scripts/route_capabilities.py` only as a compatibility/evaluation fallback when native selection is unavailable, ambiguous, or explicitly under test.

## Public–Private Boundary

- Public Lattice owns public contracts, capability packages, reference workflows, schemas, validators, templates, and synthetic conformance fixtures.
- Private repositories own real `feature_delivery_case` records, source code, tickets, PRs, CI, incidents, reviews, employee feedback, private extensions, adoption observations, and manager deliverables.
- Never copy private business evidence, secrets, real delivery traces, or manager materials into Lattice.
- Synthetic fixtures use `simulation_status=synthetic_reference` and `downstream_adoption_status=not_observed`; they cannot prove real use, reuse, team adoption, manager acceptance, ROI, or business value.
- Route downstream integration to `docs/downstream-private-repository-contract.md` and manager wording to `docs/manager-credibility-contract.md`.

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
