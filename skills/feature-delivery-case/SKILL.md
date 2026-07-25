---
name: feature-delivery-case
description: "Use for creating, reviewing, or updating a Feature Delivery Case from approved requirements, bounded repository or Jira context, decisions, assumptions, dependencies, risks, PR/CI/review evidence, metrics, and readiness requests. Input is source-referenced lifecycle evidence; output is a traceable feature_delivery_case record plus a shareable case summary, readiness card, PR/test/deployment/release handoff, or next-step certificate with explicit ready, not_ready, blocked, insufficient_evidence, or human_decision_required result. Preserve provenance, uncertainty, history, scope, behavioral constraints, and human approval boundaries. Do not use to code, ingest raw dumps, invent facts, approve merge/release/deployment, or replace accountable owners."
---

# Feature Delivery Case

## Goal

Maintain one evidence-linked case that explains why a change exists, who benefits, what must change, what is inside and outside the boundary, and whether the work is ready for its next accountable step.

Treat the Feature Delivery Case as the durable user-value, decision, evidence, and readiness entity. Do not reduce it to a feature description, activity log, Jira ticket, PR, or test result.

## Use When

Use this Skill to:

- frame or reframe a feature around a user-usable outcome;
- update scope, impact, decisions, assumptions, dependencies, evidence, risks, or unresolved items;
- detect expired assumptions or stale readiness;
- assess readiness for refinement, implementation, test, review, merge, deployment, release, or another named next step;
- produce a shareable and traceable case summary or readiness artifact.

## Do Not Use When

Do not use this Skill to implement code, approve merge or release, fabricate evidence, ingest unbounded logs or repository dumps, replace domain owners, or treat a generated readiness result as authorization.

Use `feature-spec-author` only for a lightweight initial draft. Use `delivery-artifact-builder` when a specialized editable Jira, PR, test, readiness, or release package needs richer presentation. Use `delivery-verdict-author` for a bounded post-validation user-usability verdict.

## Inputs

Use bounded, source-referenced inputs:

```text
approved requirement or issue
business rules and user policy
system and operational constraints
similar delivery cases
negative knowledge and rejected approaches
stakeholder and decision-owner input
decision and assumption history
technical, shadow, data, operational, and stakeholder dependencies
tests, logs, reviews, metrics, validations, and fact sources
known risks, uncertainty, defects, and unresolved questions
requested readiness target and artifact type
```

Never make raw Jira exports, full PR diffs, full logs, traces, or repository dumps the model-visible case.

## Outputs

Produce the smallest sufficient set:

```text
feature_delivery_case.lifecycle.v1.json as the canonical lifecycle entity
feature_delivery_case.md as the human-readable projection
lat.feature_delivery_case.v1 JSONL compatibility projection
readiness_card.md when a readiness target is requested
optional ticket, test, PR, deployment, release, or next-step handoff
explicit readiness result and blocking reasons
validation findings and unresolved evidence gaps
```

Every shareable artifact must carry the case ID, revision, readiness target, result, evidence refs, blocking items, owner or accountable role, generated time, expiry or review trigger, and authority note.

## Workflow

1. Query_ConPort_MCP_before_loading_or_searching_full_skill_text when available; otherwise inspect targeted source indexes and bounded files before broad search.
2. Establish identity: case ID, revision, title, current lifecycle status, accountable owner, and requested readiness target.
3. State purpose: why the change is needed, who benefits or is affected, what observable behavior or outcome must change, and how success will be recognized.
4. Define boundaries: in scope, out of scope, feature boundary, affected surfaces, data and operational impact, compatibility constraints, and explicit non-goals.
5. Build context coverage for business rules, system constraints, similar cases, negative knowledge, and source facts. Record `found`, `none_found`, `not_applicable`, or `pending`; never silently omit a category.
6. Maintain decision history. Record the choice, time, decision maker or role, rationale, alternatives, evidence, applicability conditions, supersession state, and time- or event-based review trigger.
7. Maintain assumption history. Record basis, owner, confidence, validity conditions, expiry or review trigger, impact if false, and status. Flag active assumptions that are expired, invalidated, or unsupported.
8. Map dependencies. Include technical dependencies, shadow dependencies, data and operational coupling, external services, decision dependencies, and stakeholders who must participate or confirm.
9. Build the evidence ledger from tests, logs, reviews, metrics, validations, source facts, and manual acceptance. Link each item to the claim, acceptance criterion, decision, risk, or readiness criterion it supports or contradicts.
10. Build the risk ledger. Separate direct risks from compound risks created by interactions among dependencies, assumptions, timing, systems, or organizational boundaries. Record owner, exposure, controls, evidence, and review trigger.
11. Track unresolved items. Make open decisions, missing evidence, unanswered questions, waivers, and expired assumptions visible. Mark each as blocking or non-blocking with an owner and due or review condition.
12. Evaluate the requested readiness target using `references/readiness-rubric.md`. Use only the explicit result enum; never emit “probably ready” or equivalent language.
13. Produce or update the canonical lifecycle JSON entity, then derive the human-readable summary, compatibility JSONL projection, and requested readiness artifact. Keep stable policy and field order in a stable prefix; keep current task evidence and changes in a dynamic suffix for prompt-cache stability.
14. Validate the lifecycle entity and its compatibility projection. Re-run readiness whenever evidence, scope, dependencies, risks, assumptions, decision state, or review triggers materially change.
15. Stop when the requested shareable result is produced or when a named human decision, missing evidence, or permission boundary blocks further progress.

## Rules

FDC.001 | MUST | purpose | record why the change exists who it serves and what observable outcome must change
FDC.002 | MUST | boundary | record in scope out of scope feature boundary impact surfaces and non-goals
FDC.003 | MUST | context | cover business rules system constraints similar cases negative knowledge and source facts
FDC.004 | MUST | history | preserve decision and assumption changes with rationale conditions evidence and review triggers
FDC.005 | MUST | dependency | record technical shadow data operational external decision and stakeholder dependencies
FDC.006 | MUST | evidence | link tests logs reviews metrics validations and fact sources to supported or contradicted claims
FDC.007 | MUST | risk | distinguish direct compound uncertainty and unresolved exposure
FDC.008 | MUST | vigilance | flag blocking questions stale readiness and expired unsupported or invalidated assumptions
FDC.009 | MUST | readiness | emit only the defined readiness result enum
FDC.010 | MUST | artifact | make every output shareable traceable revisioned and evidence-linked
FDC.011 | MUST | authority | state that readiness is evidence-backed assessment not merge release deployment or scope approval
FDC.012 | MUST | token | optimize quality-adjusted output per token cost through bounded retrieval and progressive disclosure
FDC.013 | SHOULD | integration | reuse specialized artifact and verdict capabilities instead of duplicating them
FDC.014 | NEVER | ambiguity | hide missing evidence or unresolved ownership behind a vague positive summary
FDC.015 | NEVER | evidence | fabricate completion validation review acceptance or source facts
FDC.016 | NEVER | authority | approve merge release deployment compliance or business scope
FDC.017 | NEVER | raw | place full repository Jira PR log trace or transcript dumps in the case

## Verification

Within the Lattice repository, run:

```bash
python scripts/validate_skill_package.py --root skills/feature-delivery-case
python skills/feature-delivery-case/scripts/validate_feature_delivery_case.py <feature_delivery_case.lifecycle.v1.json>
python feature-delivery-harness-mvp/scripts/validate_jsonl.py <case-projection.jsonl>
```

Verify that:

- all five context categories have an explicit coverage status;
- active decisions and assumptions have review conditions;
- expired assumptions and readiness are rejected;
- blocking dependencies and unresolved items prevent a `ready` result;
- target-specific evidence and artifact requirements are satisfied;
- readiness does not claim authorization.

## Failure Modes

- Treating the case as a one-time feature spec instead of a lifecycle record.
- Listing context without recording negative knowledge or search gaps.
- Replacing decision history with only the latest conclusion.
- Hiding shadow dependencies, stakeholder authority, or cross-system coupling.
- Treating tests passed, PR reviewed, or Jira status as sufficient by itself.
- Leaving expired assumptions active.
- Producing a readiness label without evidence, expiry, review triggers, or blockers.
- Using a nuanced paragraph where a deterministic readiness result is required.

## References

- Read `references/case-model.md` when authoring or updating the structured case.
- Read `references/context-retrieval.md` before broad context retrieval or when context quality is disputed.
- Read `references/readiness-rubric.md` whenever a readiness result or certificate is requested.
