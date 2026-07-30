# Direction Investment Gate

## Decision

Lattice work must choose direction before capability design. A technically valid Skill, Agent, profile, workflow, dashboard, or platform is still the wrong investment when it lacks a defensible value path.

The gate prevents this failure sequence:

```text
interesting method
-> reusable framework
-> internal platform
-> adoption effort
-> search for a real problem
```

Prefer this sequence:

```text
real user, product, defect, or strategic uncertainty
-> observable outcome and evidence
-> smallest sufficient delivery capability
-> strategic asset candidate when proprietary leverage exists
-> team distribution only after second-use demand
```

This contract governs direction selection. It does not replace product authority, architecture review, security review, verification, asset promotion, or active module boundaries.

## Primary Value Paths

Select exactly one primary path for the proposed investment.

### 1. `current_product_delivery`

Use when the work directly advances a specific user-usable outcome, product capability, customer problem, defect correction, validated technical experiment, or delivery decision.

Minimum evidence:

- named beneficiary or user;
- observable before and after state;
- verification method;
- bounded delivery case or accountable owner;
- reason the result matters independently of reuse.

This is the default priority because it produces the clearest validation environment and the most direct value.

### 2. `strategic_asset`

Use when the main result is a company-advantaged asset that can support multiple future delivery decisions or products.

Valid asset forms include:

- proprietary or high-quality dataset;
- benchmark or evaluation environment;
- reproducible experiment or simulator;
- validated prototype or reference implementation;
- failure catalog or behavior model;
- protocol or interoperability specification;
- invention disclosure, patent candidate, or other intellectual-property candidate;
- decision model that materially changes future product choices.

Minimum evidence:

- proprietary or difficult-to-copy input;
- concrete and verifiable artifact;
- at least two plausible uses, one of which is not the current task;
- maintenance owner, expected half-life, and refresh or retirement trigger;
- data, license, privacy, IP, and company-ownership boundary;
- reason a general-purpose vendor will not naturally provide the company-specific portion.

A document titled “knowledge base,” “benchmark,” or “prototype” is not automatically a strategic asset.

### 3. `team_reuse`

Use when the main result is a reusable internal capability for other team members.

Minimum evidence:

- an observed second use, repeated demand, or explicit accountable sponsor;
- a known future user and entry point;
- independent-use boundary and support owner;
- validation showing that another user can obtain the intended result without the original author's private context;
- maintenance and retirement plan.

Team reuse is not rejected. It is intentionally downstream of real delivery evidence because its value depends on adoption and ongoing quality responsibility.

## Direction Priority

The default portfolio sequence is:

```text
P0 current product or customer delivery
P1 strategic asset discovery from real delivery
P2 team reuse after demonstrated second use
```

This is a sequencing rule, not a claim that internal tools or strategic research have no value. An accountable owner may select another primary path, but the decision must satisfy that path's evidence contract.

## Required Direction Questions

Before implementation, answer:

1. What exact state will change, for whom, and how will it be observed?
2. Which primary value path applies?
3. Why is this result valuable even if no new Skill, Agent, profile, dashboard, or platform is created?
4. Which existing capability, module, script, schema, workflow, or vendor feature was evaluated first?
5. Why is the smallest existing combination insufficient?
6. What is the concrete artifact or delivery result?
7. What evidence is available now, and what remains `UNKNOWN`?
8. What is the second use or next-use path?
9. Who owns validation, maintenance, support, and retirement?
10. What authority, privacy, IP, compliance, or public/private boundary applies?

## Direction Verdicts

Use one verdict:

- `proceed`: evidence supports an independently valuable bounded investment;
- `bind_to_delivery`: the idea is plausible but must first run inside a real delivery or validation case;
- `retain_candidate`: preserve the idea and evidence, but do not allocate implementation effort yet;
- `stop`: value path, ownership, verification, or authority is insufficient or contradicted.

A `proceed` verdict is not a delivery, security, architecture, release, or asset-promotion approval.

## Capability Creation Rules

```text
LAT.DIR.001 | MUST  | direction | select_exactly_one_primary_value_path_before_capability_design | enforce
LAT.DIR.002 | MUST  | outcome   | define_beneficiary_observable_state_change_and_verification | reject_invalid
LAT.DIR.003 | MUST  | reuse     | evaluate_existing_capabilities_before_creating_a_new_one | reject_invalid
LAT.DIR.004 | NEVER | value     | treat_skill_agent_profile_pr_dashboard_or_platform_creation_as_final_value | block
LAT.DIR.005 | MUST  | candidate | keep_unsupported_ideas_candidate_scoped_or_bind_to_delivery | enforce
LAT.DIR.006 | MUST  | strategy  | strategic_asset_requires_proprietary_input_verifiable_artifact_second_use_and_owner | reject_invalid
LAT.DIR.007 | MUST  | team      | team_reuse_requires_second_use_evidence_or_accountable_sponsor | reject_invalid
LAT.DIR.008 | NEVER | sequence  | build_team_distribution_system_first_and_search_for_demand_later | block
LAT.DIR.009 | MUST  | boundary  | preserve_active_module_public_private_ip_security_and_human_authority_boundaries | enforce
LAT.DIR.010 | MUST  | stop      | stop_or_defer_when_value_owner_verification_or_authority_cannot_be_established | enforce
```

## New Skill Direction Fit Block

Every newly created `skills/<name>/SKILL.md` must include a machine-checkable `## Direction Fit` section. Copy `templates/direction-fit.template.md` and complete every field.

The validator requires:

- `primary_value_path` and `direction_verdict`;
- `evidence_refs` and `existing_capability_gap`;
- path-specific fields;
- no placeholder values.

Existing Skill packages do not need the block solely because they are edited. Add it when a change materially expands purpose, authority, or investment scope.

## Stop Conditions

Stop or defer when:

- the proposed work has no named beneficiary or observable result;
- the value argument depends only on expected adoption, future reuse, or AI novelty;
- an existing capability already satisfies the need with lower cost or risk;
- the strategic asset lacks proprietary leverage, verification, second use, or ownership rights;
- team reuse lacks a second user, sponsor, support owner, or independent-use evidence;
- the work crosses product, architecture, security, compliance, data, IP, public/private, or release authority;
- required evidence remains unavailable after one bounded investigation.

Preserve the decision, evidence, unknowns, and stop reason. Do not turn a stopped proposal into a hidden implementation task.