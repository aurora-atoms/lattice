# Capability Profile Runtime Contract

## Purpose

This contract separates the role that decides what to do next from the runtime configuration that determines how that role is allowed to operate.

```text
Agent
  owns role, state assessment, next-action selection, stop, and escalation.

Capability Profile
  owns model routing, Skills, tools, knowledge, permissions, token budget,
  cache policy, telemetry, and verification requirements for one task class.
```

A runtime session is therefore:

```text
Agent role
+ Capability Profile
+ current Feature Delivery Case or task evidence
= bounded execution
```

The profile is not an Agent and does not act. The Agent is not a permission bundle and does not grant itself models, tools, knowledge, or delivery authority.

## Why this refactor is needed

The existing repository already distinguishes `agent` as a packaging/runtime record from `capability_profile` as a capability role. It also contains workspace templates, Agent manifests, MCP policies, cache controls, and progressive-disclosure rules. The missing contract was an enforceable boundary between them.

Without that boundary, the following failures remain possible:

- an Agent definition silently becomes the owner of tool permissions or model selection;
- a cheap model is trusted because it is in an approved Agent rather than because its output is externally verified;
- a flagship model is treated as delivery authority;
- model handoffs pass persuasive summaries without claims, conflicts, unknowns, and evidence references;
- a cache key is reused across different models or toolsets;
- telemetry intended for system improvement becomes personnel monitoring;
- Capability Profiles promise emotional outcomes that have not been observed.

This contract adds deterministic checks without introducing a new module or a new mega Skill.

## Authority model

Model price, size, or product label never establishes evidence status.

```text
observed
  deterministic tool or directly addressable source result

derived
  deterministic transformation of observed evidence

candidate
  model-generated extraction, classification, summary, or option

candidate_change
  bounded proposed code or configuration change

judged
  model or human evaluation that names evidence and blind spots

human_decision
  accountable approval, risk acceptance, exception, or delivery decision
```

A cheaper model can produce a highly reliable result when a deterministic check establishes it. A flagship model remains `judged` unless external evidence or an accountable human gate confirms the result.

No model may self-confirm user-usable delivery.

## Model lanes

Capability Profiles use vendor-neutral model classes. Runtime adapters may bind these classes to current provider models.

### Economy lane

Use for high-volume work whose errors are easy to detect:

- metadata extraction;
- classification;
- log summarization;
- context candidate generation;
- schema filling.

Maximum authority: `candidate`.

Required controls:

- source references;
- schema or deterministic validation;
- escalation on ambiguity or missing evidence.

Forbidden authority:

- delivery approval;
- P0 conflict resolution;
- scope expansion.

### Coding lane

Use for bounded code reasoning and candidate changes:

- localized debugging;
- mechanical migration;
- test candidate generation;
- patch review.

Maximum authority: `candidate_change`.

Required controls:

- bounded diff;
- target tests;
- regression anchors;
- no test weakening;
- no scope expansion.

### Flagship lane

Use for ambiguity, large impact, or weak observability:

- requirement reconstruction;
- architecture trade-offs;
- cross-system impact;
- high-risk semantic review;
- conflict analysis.

Maximum authority: `judged`.

The flagship lane must independently reconstruct the problem before relying on an economy-model summary. It cannot override machine failures or self-confirm delivery.

### Human lane

Reserved for decisions that cannot be delegated:

- business intent;
- risk acceptance;
- policy exceptions;
- material scope changes;
- delivery and release decisions.

## Escalation policy

The default routing rule is `lowest_authority_sufficient`, not cheapest-model-first at any cost.

Escalate when any of the following is present:

- ambiguity;
- high blast radius;
- irreversibility;
- low observability;
- conflicting evidence;
- security, privacy, compliance, or policy impact.

Routing quality is measured by false-pass rate, high-risk escalation recall, unnecessary escalation rate, and final verified delivery quality. Model-use percentage is not a value metric.

## Cross-model handoff

A model handoff must contain:

```text
decision_required
verified_facts
conflicts
unknowns
evidence_refs
reason_for_escalation
```

A free-form summary or full reasoning transcript is not an authoritative handoff. The receiving lane must be able to reopen the cited evidence and independently reconstruct P0 assumptions.

## Verification

Model agreement is not proof. The profile must require applicable deterministic checks and independent review.

Typical order:

```text
schema / compiler / static analysis
-> target test or reproduction
-> regression anchors
-> integration or runtime evidence
-> independent semantic review
-> accountable human gate when required
```

A Capability Profile may require an evidence gate or an evidence-plus-human gate. It may not declare `model_only` as a delivery verdict mechanism.

## Cache contract

Caches are scoped to the model lane and profile version.

```text
cache identity includes:
  profile_id
  profile_version
  model_lane
  toolset_hash
  schema_version
```

Do not assume cross-model cache reuse.

Stable prefix candidates:

- kernel rules;
- profile contract;
- stable tool schemas;
- output schema.

Dynamic suffix candidates:

- current task request;
- current repository evidence;
- current diff;
- fresh tests and runtime state.

Create a cache write only when at least two uses are expected. Invalidate on profile, toolset, schema, or policy changes. Correctness and current policy take precedence over cache hit rate.

## Human factors contract

Human outcomes are design hypotheses until observed in real use. A profile may target:

- controllability;
- competence;
- cognitive clarity;
- safe dissent;
- collective efficacy.

It must avoid:

- choice overload from excessive profiles;
- approval fatigue from unnecessary gates;
- surveillance or personnel ranking;
- replacement framing;
- zero-error promises.

The profile should ask for failure-point discovery rather than general approval:

> Identify the most likely failure point for the next user.

Telemetry is for improving the system, not ranking people.

## Relationship to existing Lattice components

This contract does not create or replace a module.

- AegisFlow may orchestrate state transitions and routing.
- FlowGuard may enforce permissions, scope, and approval boundaries.
- Memexa may preserve source-scoped state and append-only events.
- Helixion may analyze repeated failures and propose validated improvements.
- DeliveryYield may measure model-stage cost, cache use, waste, and verified delivery outcome.
- OpenClaw and other active modules retain their current development tracks.

The Capability Profile supplies the bounded runtime configuration. It does not approve delivery, promote assets, or override active module boundaries.

## Public and private boundary

The public repository may contain:

- the contract;
- schema;
- validator;
- synthetic profiles;
- generic model classes;
- public-safe routing and human-factor hypotheses.

Private downstream repositories own:

- real model bindings;
- private repository scopes;
- private knowledge packs;
- real delivery evidence;
- observed user feedback;
- adoption and outcome records.

A synthetic profile proves contract shape only. It does not prove quality, team adoption, emotional impact, ROI, or transferability.

## Validation

Run:

```bash
python scripts/validate_capability_profile.py --root .
python -m unittest discover -s tests -p 'test_capability_profile_runtime.py' -v
python -m json.tool schemas/capability/capability-profile-runtime.v1.schema.json >/dev/null
```

The committed example is:

```text
examples/capability-profiles/pr-review-runtime-profile.v1.json
```
