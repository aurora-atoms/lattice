# Capability Profile Runtime Contract Migration

## Scope

This migration audits the current public Lattice repository against three questions:

1. What is the enforceable difference between an Agent and a Capability Profile?
2. How should economy, coding, flagship, and human lanes be mixed without converting model tier into trust?
3. How should cache and human-factor concerns be represented without weakening evidence or turning telemetry into personnel monitoring?

## Current-state findings

### Existing strengths

The repository already provides:

- a canonical capability taxonomy with distinct `agent` record types and `capability_profile` roles;
- workspace templates that bind Agents, Skills, MCP, knowledge, validation, and source-control settings;
- Agent manifests containing risk, context, token, cache, install, and telemetry fields;
- progressive disclosure and stable-prefix guidance;
- least-privilege MCP policies;
- evidence, stop, authority, public/private, and no-auto-promotion contracts;
- deterministic validators and CI.

### Gap 1: ownership was distributed but not explicit

The repository stated that an Agent is not a substitute for a capability role, but it did not deterministically define which runtime concerns belong to the Agent and which belong to the Profile.

This left a structural ambiguity:

```text
Agent manifest contains Skills, MCP, knowledge, token, cache, install, and telemetry.
Workspace template also contains Agents, Skills, MCP, knowledge, and validation.
```

The new contract resolves this without breaking current records:

- existing Agent manifest fields remain compatibility/default declarations;
- the selected Capability Profile is authoritative for the current task runtime;
- the Agent owns state assessment and action selection, not self-granted runtime authority.

A later migration may reduce duplicated Agent defaults after downstream compatibility evidence exists. This PR does not silently rewrite every Agent record.

### Gap 2: model trust was implicit

The existing architecture covered quality-adjusted token ROI and cache controls but did not encode model-lane authority.

The new contract adds:

- vendor-neutral economy, coding, flagship, and human lanes;
- maximum authority for each lane;
- mandatory escalation triggers;
- evidence-based verification independent of model price;
- a prohibition on model-only delivery verdicts.

### Gap 3: cross-model handoff was under-specified

The new contract requires structured handoffs containing facts, conflicts, unknowns, evidence references, and the reason for escalation. Full reasoning transcripts are explicitly non-authoritative.

### Gap 4: cache identity did not explicitly include model lane

The new contract requires cache keys to include profile version, model lane, toolset hash, and schema version. Cross-model cache reuse is denied by default.

### Gap 5: human outcomes lacked an evidence state

The conversation identified plausible human outcomes such as control, competence, cognitive clarity, safe dissent, and collective efficacy. These are not proven repository effects.

The contract therefore records them as design hypotheses and adds anti-patterns:

- choice overload;
- approval fatigue;
- surveillance;
- replacement framing;
- zero-error promises.

## Changes in this migration

- Add `docs/capability-profile-runtime-contract.md`.
- Add `schemas/capability/capability-profile-runtime.v1.schema.json`.
- Add `scripts/validate_capability_profile.py`.
- Add `tests/test_capability_profile_runtime.py`.
- Add a synthetic PR-review profile example.
- Add dedicated CI for the contract.
- Update the taxonomy and context contract to make Profile authority explicit.

## Compatibility decision

This migration does not:

- create a new Skill;
- create a new Agent;
- create a new module;
- deprecate an existing Agent or Skill;
- rewrite the canonical capability manifest;
- claim that the synthetic profile has been used by a team;
- bind public profiles to a current vendor model name;
- change DeliveryYield into a quality gate;
- overlap with the direction-investment gate proposed in PR #32.

## Follow-up candidates

These are candidates, not automatically approved work:

1. Add a downstream private profile extension for real provider model bindings.
2. Migrate selected Agent manifests from duplicated runtime defaults to profile requirements after compatibility evaluation.
3. Add profile rendering adapters for Codex, GitHub Copilot, Claude Code, and VS Code.
4. Add DeliveryYield records for cost and quality by model lane.
5. Run representative profile-routing evaluations against a flagship-only baseline.
6. Collect observed human failure-point feedback before changing `human_factors.evidence_status`.
