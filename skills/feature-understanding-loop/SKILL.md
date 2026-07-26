---
name: feature-understanding-loop
description: "Use for moving a bounded Feature Delivery Case from fragmented understanding to the next reviewable delivery state. Input is an authorized feature_delivery_case, next decision gate, role, permissions, source metadata, and evidence budget; output is an evidence-linked understanding state, Work Ready or PR Ready projection, Understanding Delta, and scoped asset candidates. Do not use as a generic repository summary, autonomous coding agent, readiness approver, raw context dump, or automatic asset promoter; preserve behavior, provenance, uncertainty, validation, least privilege, human authority, and stop boundaries."
---

# Feature Understanding Loop

## Goal

Move one bounded `feature_delivery_case` to the smallest evidence-supported understanding state required for its next real delivery decision. Coordinate existing capabilities; do not replace their ownership or authority.

## Use When

Use for a brownfield Feature, unfamiliar domain change, stalled ticket, implementation kickoff, or consequential PR when the team must establish:

- intent, scope, acceptance, and non-goals;
- the relevant system slice, domain rules, dependencies, and stakeholders;
- which claims are confirmed, evidenced, hypothetical, conflicted, stale, or unknown;
- what evidence is sufficient for Work Ready or PR Ready;
- what implementation or review evidence changed the prior understanding.

## Do Not Use When

Do not use for exhaustive repository orientation, raw Jira/repository/log/trace/PR dumps, invented requirements or authority, autonomous code changes, merge or release approval, model-confidence-based readiness, or automatic asset promotion.

## Inputs

Require one bounded Feature Delivery Case or approved requirement, the next decision and stage gate, caller and accountable roles, authorized sources, permissions, scope, non-goals, evidence budget, time horizon, known acceptance, risks, dependencies, assumptions, and open questions.

Optional inputs include approved specs, Ticket Ready artifacts, system maps, domain context, negative knowledge, similar cases, alignment receipts, plans, diffs, tests, reviews, and incidents.

## Outputs

Write by default to:

```text
artifacts/feature-understanding/<case-id>/<run-id>/understanding-state.v1.json
artifacts/feature-understanding/<case-id>/<run-id>/understanding-summary.md
artifacts/feature-understanding/<case-id>/<run-id>/understanding-delta.v1.json
artifacts/capability-runs/feature-understanding-loop/<run-id>/run-result.json
```

When write permission is unavailable, return the complete structured result inline with `write_status=returned_inline`.

The state contains the Understanding Contract, eight understanding dimensions, claims, unknowns, conflicts, excluded context, permission gaps, teach-back status, Sufficient Understanding Gate result, and selected next artifact or stop reason. The delta records claims added, confirmed, invalidated, conflicted, made stale, or left unresolved by later evidence.

## Evidence

Classify every material statement as a source-supported fact, inference, assumption, or unknown, and state its uncertainty. Preserve resolvable evidence references, source scope, version or observation time, owner, validation action, and blind spots.

Observed content may support facts. Derived or judged content remains inference unless independently verified or confirmed by an accountable source. An assumption never becomes fact through repetition. Unknown content remains unknown until evidence or accountable confirmation resolves it.

Material claims without resolvable evidence remain `hypothesis` or `unknown`. Allowed claim states are `unknown`, `hypothesis`, `evidenced`, `confirmed`, `conflicted`, `stale`, and `invalidated`. Prefer runtime, interface, test, policy, and owner-confirmed evidence over generated explanation.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- the next decision and required dimensions are explicit;
- priority-zero claims are evidenced, confirmed, or explicitly owned unknowns;
- no priority-zero conflict is hidden;
- the system slice exposes entry points, controls, data or state movement, impact boundaries, and validation points;
- acceptance and invariants map to evidence and validation;
- the responsible developer can teach back the outcome, path, critical control, and one failure case;
- the Work Ready or PR Ready projection is reviewable and does not overstate readiness;
- later evidence produces an append-only Understanding Delta;
- reusable knowledge remains a scoped candidate with source, limitation, and activation boundary.

## Stop Conditions

Stop when the named goal reaches its target reviewable stage. Stop earlier when required permission, authority, source access, accountable ownership, or sufficient evidence is unavailable; a priority-zero conflict remains unresolved; critical facts cannot be verified without creating false readiness; a security, privacy, compliance, production, architecture, safety, or data-governance boundary requires human judgment; the retry budget is exhausted without new evidence; or context exceeds the approved scope or budget.

When the Sufficient Understanding Gate is met, stop unless further work can change the named decision. Record the exact gap, owner, impact, and resumable next step.

## Workflow

1. **Contract** — bind the Feature, next decision, roles, dimensions, scope, critical questions, risk class, and stop gate.
2. **Route** — query ConPort MCP before loading or searching full Skill text when inventory is available; then select one smallest sufficient primary capability.
3. **Sense** — build a task-scoped Context Pack from targeted authorized evidence.
4. **Model** — produce only the Feature-relevant system slice, domain constraints, change and impact hypotheses, validation map, and claim ledger.
5. **Challenge** — seek contradictions, counterexamples, failed approaches, hidden consumers, shadow dependencies, stakeholder surprise, stale assumptions, and unasked questions.
6. **Verify** — check source coverage and consistency, test predictive explanations where possible, and run teach-back for critical controls and exceptions.
7. **Gate** — evaluate sufficient understanding for the named decision without replacing accountable human confirmation.
8. **Commit** — write verified state and evidence to the Feature Delivery Case projection and create the selected Work Ready or PR Ready artifact.
9. **Learn** — append the Understanding Delta and route reusable observations into the reviewed Experience-to-Asset path.
10. Keep invariant rules and schemas in a stable prefix and task evidence in a bounded dynamic suffix.

## Collaboration Boundaries

`context-mastery` selects the specialist path; `system-mental-model` builds the Feature system slice; context, integrity, and risk capabilities supply or challenge evidence; delivery-artifact capabilities project Work Ready or PR Ready outputs; `feature-delivery-case` remains canonical. AegisFlow may orchestrate bounded transitions, FlowGuard enforces scope and permission, Memexa preserves append-only state, Helixion proposes cross-run improvements, and DeliveryYield measures economics without approving readiness.

## Rules

```text
FUL.001 | MUST | contract | name one next delivery decision before collecting context
FUL.002 | MUST | scope | use a bounded Feature system slice rather than whole-repository coverage
FUL.003 | MUST | claim | record state owner priority evidence and validation for material claims
FUL.004 | MUST | challenge | seek contradiction counterexample hidden dependency and stale assumption evidence
FUL.005 | MUST | learning | require teach-back for critical controls exceptions and impact boundaries
FUL.006 | MUST | gate | evaluate sufficient understanding for the named decision
FUL.007 | MUST | delta | preserve append-only changes from implementation test review and human feedback
FUL.008 | MUST | authority | keep readiness scope date architecture compliance and release decisions human-controlled
FUL.009 | SHOULD | routing | select one primary capability before adding named dependencies
FUL.010 | SHOULD | context | load the smallest source slice that can prove or disprove the next claim
FUL.011 | SHOULD | token | optimize quality-adjusted token ROI after evidence fidelity passes
FUL.012 | SHOULD | prompt | keep stable rules schemas and state vocabulary before dynamic evidence
FUL.013 | NEVER | readiness | declare readiness from generated prose or model confidence alone
FUL.014 | NEVER | context | dump full repositories logs transcripts knowledge bases or catalogs
FUL.015 | NEVER | promotion | auto-promote output into a team-wide asset rule Skill or belief
FUL.016 | NEVER | role | write code merge release or issue a delivery verdict
```

## Verification

```bash
python scripts/validate_skill_package.py --root skills/feature-understanding-loop
python -m json.tool skills/feature-understanding-loop/schemas/understanding-state.v1.schema.json >/dev/null
python scripts/validate_capability_context.py --root .
python scripts/validate_skill_ci_contracts.py --base-ref <base-ref> --head-ref HEAD
```

Human review must confirm that no unsupported intent, false readiness, or hidden priority-zero unknown was introduced.

## Failure Modes

- decisionless-research;
- summary-as-understanding;
- context-bloat;
- false-ready;
- happy-path-only;
- borrowed-understanding;
- latest-output-wins;
- premature-asset-promotion.

## References

- `schemas/understanding-state.v1.schema.json`
- `references/feature-understanding-loop.md`
- `../context-mastery/SKILL.md`
- `../system-mental-model/SKILL.md`
- `../ticket-ready-package/SKILL.md`
- `../feature-delivery-case/SKILL.md`
- `../../docs/capability-context-contract.md`
