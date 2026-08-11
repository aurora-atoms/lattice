# Senior Attention

## Purpose

Senior Attention is Lattice's public reference workflow for turning scattered delivery evidence into one bounded, evidence-grounded decision or work-ready state while preserving human authority and private-data boundaries.

It is not a Senior Engineer role simulation, a mega Skill, a new Agent, or a new module. It composes existing public capabilities around the existing `feature_delivery_case` evidence boundary.

The public contract optimizes for verified, owner-accepted delivery state change per minute of scarce human attention. It does not treat Agent activity, output volume, tool count, Skill count, PR count, or token reduction as final value.

Canonical runtime profile:

```text
workspaces/templates/senior-attention-runtime-profile.v1.json
```

Historical Evidence Wayfinding design material remains useful context, but this document is the compact public operating entry for downstream Senior Attention integrations.

## Direction Fit

```text
primary_value_path: current_product_delivery
direction_verdict: bind_to_delivery
beneficiary: downstream Senior Attention pilot integrator and accountable delivery owner
observable_state_change: scattered public capability entry points become one bounded workflow and one validated task profile
verification: five task-family discovery probes, profile validation, registry projection parity, public/private boundary validation
existing_capability_gap: existing capabilities perform the work but there is no single canonical public entry or registered cross-family profile
current_evidence: public contracts and synthetic conformance only
unknown: real downstream adoption, attention reduction, owner acceptance, and business value
next_use: one private downstream pilot pinned to an immutable Lattice ref
maintenance_owner: Lattice capability governance owner
```

This is intentionally `bind_to_delivery`, not proof of `team_reuse` or business value. A public green check or synthetic fixture cannot establish private adoption.

## Public / Private Boundary

### Public Lattice owns

- this reference workflow;
- the registered task profile;
- public Skills and capability metadata;
- schemas, validators, routing metadata, templates, and synthetic conformance fixtures;
- public-safe extension fields and opaque reference conventions.

### Private downstream owns

- real source code and repositories;
- tickets, PRs, CI, incidents, reviews, chat, logs, and telemetry;
- employee, customer, business, security, compliance, and proprietary context;
- real `feature_delivery_case` records;
- ACL filtering, source authority, purpose limitation, and private evidence storage;
- real human decisions, work-object changes, Outcome Receipts, attention measurements, and adoption evidence.

Public Lattice must never require a private source name, private path, employee identity, proprietary schema, or real case to validate this workflow. Downstream systems pass private material only as bounded dynamic context or opaque references under their own authorization policy.

## Operating Definition

Use Senior Attention when an engineering task has one or more of these characteristics:

- evidence is distributed across sources;
- impact or scope is uncertain;
- a human owner must accept risk or make a value judgment;
- error cost is material;
- several plausible explanations or options remain;
- a decision or handoff is blocked by low-value search, reconstruction, or repeated explanation.

Do not use it merely because a Senior Engineer is involved. If documented policy, a deterministic validator, or a clearly authorized owner can resolve the task directly, use that simpler path.

## Stable State Machine

```text
INTAKE
  -> CONTEXT_READY
  -> INVESTIGATING
  -> DECISION_READY
  -> WORK_READY
  -> SETTLED

Any state
  -> BLOCKED
  -> ESCALATED
```

### INTAKE

Required:

- one bounded target or question;
- accountable owner or owner role;
- scope and explicit non-scope;
- evidence cutoff when freshness matters;
- expected visible output.

Allowed action: ask one smallest clarifying question or select one task family.

Exit evidence: a frozen target contract or an explicit blocker.

### CONTEXT_READY

Required:

- authorized evidence references are parseable;
- source authority and freshness are distinguishable;
- relevant conflicts and missing evidence are visible;
- context is bounded to the current decision.

Allowed action: load only the smallest useful evidence and capability set.

Exit evidence: bounded context pack plus evidence refs, or a permission/evidence blocker.

### INVESTIGATING

Required:

- at least one named claim, hypothesis, failure mechanism, or decision gap can be falsified or verified;
- the next capability is selected for a named gap rather than because it exists in the profile.

Allowed action: activate one primary capability, then add at most a small number of conditional capabilities when a named dependency or independent validation gap exists.

Exit evidence: target-relevant claim state changes, risk is reduced, or the investigation stops for no new evidence.

### DECISION_READY

Required:

- target is bounded;
- load-bearing claims have evidence or are explicitly downgraded;
- strongest counterevidence or alternative explanation is visible;
- authority and irreversible-risk boundaries are explicit;
- the requested decision produces a concrete next state or artifact.

Allowed action: generate a Decision Strip, Decision Card, and Evidence Map projection as needed and request one human Decision Turn.

Exit evidence: human decision event, bounded request for more evidence, or explicit no-go.

### WORK_READY

Required:

- selected action or artifact has owner, scope, acceptance observer, verification, and stop boundary;
- human decision has not been silently expanded into merge, release, deployment, architecture, compliance, security, or business authority.

Allowed action: hand off a reversible work-ready artifact to the authorized downstream executor.

Exit evidence: real work object changes or the owner rejects/corrects the artifact.

### SETTLED

Required:

- downstream can observe the actual result;
- accepted, corrected, rejected, partially completed, blocked, or unknown states remain distinguishable;
- claim settlement and earliest failure point are recorded when available.

Allowed action: create or update a private Outcome Receipt and, only when evidence warrants it, a bounded improvement candidate.

SETTLED does not imply reusable asset promotion or `team_available`.

### BLOCKED / ESCALATED

Enter when permission, evidence, source access, authority, security, compliance, privacy, scope, verification, or required human judgment prevents safe continuation.

Return only the smallest missing evidence, permission, owner decision, or next action. Do not bypass the gate or keep looping without new evidence.

## Five Task Families

Senior Attention provides one public entry with five task paths. The families share the state machine and evidence discipline but have different work-ready outputs.

### 1. Feature Requirement / Work Ready

Use when a feature or requirement is not yet sufficiently understood to begin implementation or review safely.

Primary public capabilities:

```text
feature-understanding-loop
context-mastery
```

Conditional capabilities:

```text
domain-context-pack
unasked-questions-generator
contradiction-adjudication
delivery-artifact-builder
```

Typical output:

- bounded target and scope;
- evidence-linked context;
- material unknowns and contradictions;
- acceptance observer;
- implementation or PR-ready handoff.

Do not infer that a requirement is work-ready from document completeness alone.

### 2. Risk Preflight

Use when a commitment, implementation, review, or release may contain a material hidden dependency, accumulated risk, control boundary, rework trigger, or stakeholder surprise.

Primary public capability:

```text
risk-ahead
```

The run must select the smallest relevant risk specialist rather than activate every risk capability.

Typical output:

- one material failure mechanism or exposure;
- evidence and counterevidence;
- minimal preventive action;
- owner and escalation threshold.

Risk models and counts cannot issue final legal, security, compliance, architecture, release, or business rulings.

### 3. Bug / Delivery Rescue

Use when a CI failure, failing test, environment problem, reproducibility gap, or contract break blocks delivery.

Primary public capability:

```text
delivery-rescue
```

Typical output:

- reproduction state;
- observed facts versus hypotheses;
- competing explanations when material;
- minimum falsification or repair step;
- validation command;
- explicit fix-readiness boundary.

A correlated log line or intermittent symptom is not a proven root cause.

### 4. Decision Support

Use when a bounded owner must choose among options, accept a risk, or decide whether more evidence is required.

Primary public capability:

```text
decision-question-builder
```

Conditional challenge capabilities:

```text
unasked-questions-generator
contradiction-adjudication
```

Typical output:

- one decision question;
- two to four bounded options when applicable;
- recommendation or abstention state;
- load-bearing evidence;
- strongest reversal risk;
- unknowns, reversibility, deadline, and owner.

Use `senior-attention-queue` only when multiple bounded expert decisions compete for the same scarce attention window. A single decision must not be converted into a queue merely because the Skill exists.

### 5. Management Translation

Use when validated delivery state must be projected for a manager or executive audience without changing the underlying evidence strength.

Primary public capability:

```text
management-translation
```

Typical output:

- business or user purpose;
- actual lifecycle state;
- accepted or verified progress;
- material risk and unknowns;
- next milestone;
- decision or resource request;
- evidence references and owner review point.

Do not lead with PR count, commit count, token count, Agent activity, or generated-document volume as final value.

## Capability Selection Rules

1. Use native runtime discovery first.
2. Select one primary capability for the named gap.
3. Load full Skill bodies only after selection.
4. Use `scripts/route_capabilities.py` only as a compatibility or evaluation fallback.
5. `delivery-capability-conductor` may assess state, choose a bounded next action, stop, or escalate when native selection is unavailable or ambiguous; it is not an always-on orchestration monopoly.
6. A Capability Profile constrains what may be used. It does not instruct the runtime to load every listed Skill.
7. `activation=on_demand` means the capability remains absent from active context until a named task gap justifies it.
8. `activation=explicit` means a human-facing decision artifact is requested deliberately rather than inferred from weak signals.

## Cross-Workspace Handoff

Native workspaces execute and discover capabilities locally. Lattice standardizes the bounded handoff semantics, not how Google, Copilot, Gemini CLI, Codex, Claude Code, or another runtime discovers its Skills, Agents, tools, or repository instructions.

The current Google-to-coding boundary is a human handoff:

```text
Google candidate evidence
-> human source / authority / privacy confirmation
-> Domain Context Pack + Portable Case Pack + required verification
-> receiving workspace native discovery
-> independent repository / runtime verification
```

Google summaries, citations, hypotheses, and recommendations remain candidate evidence. Claims about code, tests, reproduction, configuration, dependencies, runtime behavior, root cause, work readiness, or delivery readiness must be re-verified by the receiving coding workspace. Authority cannot increase during transfer; unknowns, unresolved conflicts, strongest counterevidence, evidence refs, privacy, and required verification cannot be compressed away.

Human-readable and machine-readable views are projections of the same bounded case state, not independent fact stores. Automatic cross-runtime invocation, send, writeback, execution, or approval requires a separate Direction Investment Gate.

The canonical rules, deterministic receipt, public/private ownership, and conformance commands are in [Cross-Workspace Handoff](cross-workspace-handoff.md).

## Attention Admission

Before consuming scarce human judgment, verify all five invariants:

```text
M1 target
M2 evidence
M3 counterevidence
M4 risk / authority
M5 delivery
```

Any mandatory failure blocks READY. There is no 4-of-5 score.

### M1 Target

The decision or next state has one owner, bounded scope, cutoff where relevant, and acceptance observer.

### M2 Evidence

Load-bearing claims have resolvable evidence refs or are visibly downgraded to hypothesis/unknown.

### M3 Counterevidence

The strongest currently known evidence or alternative explanation capable of reversing the recommendation is visible, or a bounded search with known blind spots is recorded.

### M4 Risk / Authority

Security, compliance, architecture, business intent, risk acceptance, merge, release, deployment, and production authority remain with accountable humans and owning systems.

### M5 Delivery

The requested judgment changes a real downstream state or produces a concrete work-ready artifact. A long report is not sufficient by itself.

## Human Projections

Decision Strip, Decision Card, and Evidence Map are projections from the Case Spine. They do not own facts.

### Decision Strip

Target reading time: roughly 5–10 seconds.

Must answer:

- what decision is required;
- current recommendation / abstain / block;
- why now;
- maximum reversal risk;
- deadline and owner;
- where to expand evidence.

### Decision Card

Target reading time: roughly 30–60 seconds for a bounded case.

Must show:

- decision requested;
- options and tradeoffs;
- recommendation strength;
- evidence and counterevidence;
- unknowns and conflicts;
- reversibility;
- owner and next step.

### Evidence Map

Loaded only when needed. It preserves claim state, evidence refs, conflicts, blind spots, rejected directions, and validation state.

Deleting and regenerating a projection must not change canonical evidence or claim strength.

## Context Discipline

Use a small stable public prefix and a bounded private dynamic suffix.

```text
PUBLIC STABLE PREFIX
AGENTS boundary
-> this reference workflow
-> registered capability profile
-> compact capability metadata
-> public schemas and output contracts

PRIVATE DYNAMIC SUFFIX
private task contract
-> ACL-filtered evidence refs
-> bounded excerpts / test results
-> owners and unknowns
-> live outcome
```

Never copy the private suffix back into public Lattice.

The public profile exposes only read-oriented GitHub MCP access by default. Write, merge, deploy, secret, and destructive authority remain denied.

## Private Extension Interface

Downstream implementations may bind opaque private references through task-scoped dynamic context, for example:

```text
private_task_contract_ref
private_evidence_refs
owner_confirmation_ref
source_authority
private_policy_version
```

These names define an interface shape only. Public Lattice does not resolve or validate the private location, organization, person, business schema, or proprietary contents behind the reference.

A downstream coordinator is responsible for ACL enforcement, source-system authority, purpose limitation, retention, audit, and safe evidence projection before model-visible context is assembled.

## Stop Conditions

Stop when:

- the requested visible state or artifact is reached;
- the next step requires a human owner decision;
- permission or source access is missing;
- critical evidence is unavailable;
- claims conflict and the authoritative owner cannot be resolved;
- scope, blast radius, or irreversibility expands;
- security, privacy, compliance, architecture, production, or personnel boundaries are reached;
- a verification gate fails;
- a second iteration produces no new evidence, risk reduction, or state change;
- the user or downstream contract says stop.

Do not continue simply to produce more analysis.

## Outcome and Learning Boundary

A real run is not complete because a Card was generated. Private downstream settlement should capture observable state change, accepted or corrected artifact, human correction, remaining unknowns, and earliest failure point.

A failure point may create a session-local or candidate-scoped Harness improvement proposal. It cannot directly mutate a team default or promote a Skill.

Any team-level capability change remains subject to the existing governed path:

```text
failure point
-> single-delta candidate
-> representative / hard / reserved evaluation
-> human review
-> scoped canary when justified
-> rollback-capable promotion decision
```

DeliveryYield may measure token, cost, latency, waste, and attention economics only after quality and authority gates. It does not approve delivery or promotion.

## Public Conformance and Private Value

Public conformance can prove:

- the workflow is discoverable;
- the profile is structurally and semantically valid;
- task families route to bounded public capabilities;
- private references remain opaque;
- permissions and human authority remain bounded.

It cannot prove:

- a real Senior saved time;
- an owner accepted a recommendation;
- a private defect was prevented;
- team reuse occurred;
- manager value, ROI, or business impact.

Those claims require real downstream cases.

## Canonical References

Use these public contracts rather than duplicating them here:

- `AGENTS.md`
- `docs/capability-taxonomy.md`
- `docs/capability-profile-runtime-contract.md`
- `docs/direction-investment-gate.md`
- `docs/evidence-wayfinding.md`
- `docs/cross-workspace-handoff.md`
- `docs/downstream-private-repository-contract.md`
- `docs/public-private-operating-model.md`
- `docs/manager-credibility-contract.md`
- `schemas/capability/capability-profile-runtime.v1.schema.json`
- `schemas/capability/portable-case-pack.v1.schema.json`
- `schemas/capability/attention-admission-receipt.v1.schema.json`
- `schemas/capability/outcome-receipt.v1.schema.json`

## Verification

```bash
python scripts/validate_capability_profile.py \
  workspaces/templates/senior-attention-runtime-profile.v1.json \
  --root .
python scripts/validate_capability_manifest.py --root .
python scripts/generate_capability_registry_projections.py --root . --check
python scripts/validate_capability_routing.py --root .
python scripts/validate_public_private_boundary.py --root .
python -m unittest discover -s tests -p 'test_senior_attention_entrypoint.py' -v
```

Passing these commands establishes only public contract conformance.
