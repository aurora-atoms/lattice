# Frontier Practice Scout — Deferred Capability Candidate

## Status

```yaml
candidate_name: frontier-practice-scout
candidate_type: atomic_capability
status: retain_candidate
active_skill: false
runtime_authority: none
source_blueprint: Evidence_Wayfinding_Blueprint_CN(1).docx
source_evidence_cutoff: 2026-08-07
```

This document preserves the source blueprint's only proposed new Skill without promoting it into `skills/`.

The current decision remains **do not create the active Skill yet**. PR #34 established the initial Evidence Wayfinding contract and explicitly deferred this capability because the public repository does not yet contain second-use / independent-value evidence or run/skip evaluations. Merging that PR did not create the missing evidence.

## Direction Fit — Current Verdict

This is a candidate record, not a machine-validated `SKILL.md` Direction Fit block.

```yaml
primary_value_path: current_product_delivery
direction_verdict: retain_candidate
evidence_refs:
  - docs/evidence-wayfinding.md
  - docs/evidence-wayfinding/blueprint-preserved.md
  - docs/direction-investment-gate.md
  - docs/migrations/evidence-wayfinding-contract-pr5.md
existing_capability_gap: >
  Existing capabilities can name internal context gaps, reason about system evidence,
  find contradictions, and prepare decisions, but the blueprint hypothesizes a distinct
  need for current external first-party evidence with explicit cutoff, authority,
  counterevidence, applicability, expiry, and decision-impact semantics. The repository
  does not yet contain enough cases to prove that this requires a maintained Skill
  instead of an on-demand tool action inside the existing workflow.
user_outcome: >
  Prevent a bounded delivery decision from relying on stale or incomplete practice
  when current external primary evidence could materially change the decision or
  verification plan.
```

The Direction Investment Gate requires a real value path before capability investment. The missing evidence is not syntax; it is whether this capability produces independently valuable decision changes often enough to justify team-maintained behavior.

## Source-defined gap

The source blueprint framed the unresolved question as:

> For one named evidence or capability gap, as of a defined time, which current external first-party practices, tools, or counterexamples could materially change the current decision?

Generic search can retrieve information, but the candidate proposes a stronger operational contract:

- a named gap before search;
- a defined evidence cutoff;
- first-party / official / reproducible sources preferred;
- explicit counterevidence and source gaps;
- applicability and expiry recorded;
- output remains candidate evidence;
- search stops when the decision cannot be materially changed within budget.

## Preserved proposed contract

```yaml
name: frontier-practice-scout
role: atomic_capability
trigger: >
  A named evidence or capability gap may be changed by current external practice.
inputs:
  - decision_requested
  - named_gap
  - evidence_cutoff
  - allowed_data_classification
workflow:
  - define what finding would change the decision
  - search open-endedly beyond a pre-listed tool set
  - prioritize primary / official / reproducible sources
  - record dates, access gaps, counterevidence, and expiry
  - compare candidates against the target contract
output: frontier_evidence_brief
stop:
  - decision-changing evidence found and triangulated
  - source frontier exhausted within budget
  - no authorized access
  - no material decision impact
authority: candidate_only
```

## Candidate output contract

A future `Frontier Evidence Brief` should minimally contain:

```yaml
record_type: lat.frontier_evidence_brief.v1
case_id: <feature-delivery-case>
decision_requested: <one bounded decision>
named_gap: <what is unknown or potentially stale>
evidence_cutoff: <timestamp>
what_would_change_the_decision: <explicit condition>
search_scope:
  included: []
  excluded: []
sources:
  - source_ref: <addressable ref>
    source_type: primary|official|reproducible|secondary
    observed_at: <timestamp>
    version: <if applicable>
    access_status: inspected|unavailable|partial
claims:
  observed: []
  derived: []
  judged: []
  unknown: []
strongest_counterevidence: []
applicability:
  fits: []
  does_not_fit: []
  assumptions: []
expiry:
  trigger: <what invalidates or requires recheck>
  review_by: <optional date>
recommendation_status: candidate_only
decision_impact: changed|verification_changed|no_material_change
stop_reason: <bounded reason>
```

This shape is intentionally **not** a committed schema yet. A schema should be added only when replay evidence shows stable fields and downstream consumers.

## Expansion / convergence behavior

### Expansion loop

- Start from the named problem, not a fixed tool catalog.
- Permit newly discovered practices, tools, research, cases, and counterexamples.
- Preserve surprising findings and dissent.
- Produce multiple candidates when evidence supports alternatives.

### Convergence loop

- Map every candidate to the named gap or claim.
- Prefer first-party sources and record date/version/expiry.
- Compare target fit, evidence quality, risk, reversibility, and total cost.
- Put only decision-changing or verification-changing evidence into primary context.
- Stop when additional search cannot change the bounded decision within budget.

## Forbidden behavior

A future Skill must never:

- browse trends without a named decision gap;
- treat popularity, vendor marketing, or model consensus as evidence of fit;
- recommend procurement automatically;
- expose restricted/private source material into public context;
- expand the case scope because search found an interesting adjacent topic;
- auto-promote a tool, practice, rule, Skill, profile, or policy;
- claim delivery success;
- change the Mission Anchor;
- continue searching merely to appear comprehensive.

## Promotion gate

Create `skills/frontier-practice-scout/` only after all conditions below are satisfied.

### Required value evidence

1. At least **two governed real or replayable cases** in which current external research materially changed the delivery decision or validation plan, or prevented a stale recommendation.
2. At least one case must show value that is not merely generic web summarization.
3. A known future user and entry point exist.
4. A named maintainer owns validation, source policy, expiry, and retirement.

### Required capability evidence

5. Trigger boundary is stable enough to distinguish `run` from `skip`.
6. Output boundary is stable enough that downstream work can consume it without private author context.
7. `context-mastery`, `feature-understanding-loop`, `unasked-questions-generator`, and ordinary on-demand search were evaluated as the smaller composition first.
8. The capability can remain candidate-only and least-privilege.

### Required evaluation evidence

9. Positive trigger evals cover stale vendor/product behavior, new external practice, and explicit decision-changing gaps.
10. Negative trigger evals cover generic curiosity, already-sufficient internal evidence, no decision impact, unauthorized data, and fixed-tool shopping without a delivery question.
11. Output evals verify cutoff, source authority, counterevidence, applicability, expiry, and stop reason.
12. Reserved/holdout cases exist before promotion.
13. Rollback thresholds are predeclared.

## Seed run/skip eval cases

These are preservation candidates, not evidence that the Skill should exist.

### Must run candidates

- A repository integration depends on a vendor API whose current supported authentication behavior may have changed since the internal design was written.
- A design decision depends on whether a newly released first-party tool now supports a required isolation or validation feature.
- Two current internal options both work, but a current official standard or vendor deprecation notice could invalidate one.

### Must skip candidates

- The user asks for a general list of popular AI coding tools without a bounded delivery decision.
- Existing repository evidence and deterministic tests already answer the question.
- The named gap concerns private company policy that cannot be resolved from public sources.
- Search would not change the decision, verification plan, or stop condition.
- A user asks the system to keep browsing indefinitely for anything interesting.

## Future Skill authoring checklist

If the promotion gate is satisfied later, a new Skill PR should include at minimum:

```text
skills/frontier-practice-scout/
  SKILL.md
  references/source-quality.md
  evals/trigger-cases.*
  evals/output-cases.*
```

And the `SKILL.md` must include the current repository's machine-checkable `## Direction Fit` section, semantic version, evidence contract, success signals, stop conditions, authority boundary, public/private boundary, and validator coverage.

The candidate must be reviewed against the then-current official product documentation. The source blueprint's 2026-08-07 provider facts are not permanent runtime truth.
