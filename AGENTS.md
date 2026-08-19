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

## Senior Attention Entry

For a bounded feature-requirement, risk-preflight, bug/rescue, decision-support, or management-translation task that genuinely requires scarce expert judgment, start with [Senior Attention](docs/senior-attention.md) and the registered `workspaces/templates/senior-attention-runtime-profile.v1.json` profile. Treat that profile as an allowlist for progressive discovery, not an instruction to load every listed Skill. Keep real task evidence, owners, outcomes, attention measurements, and proprietary extensions in the private downstream repository.

Do not create a parallel Senior Attention Skill, Agent, module, fact store, or always-on conductor. `senior-attention-queue` is only for multiple competing expert requests; a single decision follows the normal bounded decision path.

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
- Run `scripts/validate_capability_manifest.py` and `scripts/validate_public_private_boundary.py` before finalizing identity, role, status, profile, or fixture changes.
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
