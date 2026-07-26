---
name: feature-understanding-loop
description: "Use for moving a bounded Feature Delivery Case from fragmented or assumed understanding to the next reviewable delivery state through an understanding contract, task-scoped evidence, system and domain claims, adversarial challenge, teach-back, and explicit verification. Input is an authorized feature_delivery_case, next decision gate, source metadata, role, permissions, and evidence budget; output is an evidence-linked understanding state, Work Ready or PR Ready projection, Understanding Delta, and scoped reusable-asset candidates. Do not use as a generic repository summary, autonomous coding agent, readiness approver, raw knowledge dump, or automatic asset promoter; preserve behavior, provenance, uncertainty, least privilege, human authority, and stop boundaries."
---

# Feature Understanding Loop

## Goal

Move one bounded `feature_delivery_case` from fragmented, assumed, or conflicting understanding to the smallest evidence-supported state needed for the next real delivery decision.

The Skill coordinates existing capabilities. It does not replace `context-mastery`, `system-mental-model`, `ticket-ready-package`, `implementation-plan`, review capabilities, or delivery learning.

## Use When

Use when a brownfield Feature, cross-module change, unfamiliar domain task, stalled ticket, implementation kickoff, or consequential PR requires a shared answer to:

- why the Feature exists and what outcome it must create;
- what is in scope, excluded, and observable;
- which system slice, rules, dependencies, and stakeholders matter;
- which claims are confirmed, evidenced, hypothetical, conflicted, stale, or unknown;
- what evidence is sufficient for Work Ready or PR Ready;
- what later implementation or review evidence changed the original understanding.

## Do Not Use When

Do not use for:

- exhaustive repository orientation without a named Feature or decision;
- raw Jira, repository, log, trace, PR, knowledge-base, or transcript dumps;
- inventing business intent, acceptance, ownership, dates, or authority;
- autonomous code modification, merge, release, or delivery approval;
- treating generated summaries or model confidence as proof of understanding;
- automatic promotion of a successful output into a team-wide Skill, rule, or belief.

## Inputs

Require:

- one bounded `feature_delivery_case` or approved Feature requirement;
- the next decision to support, such as start implementation, request review, or resolve a named risk;
- caller and accountable roles;
- authorized source and capability metadata;
- scope, non-goals, permission boundary, evidence budget, and time horizon;
- known acceptance, invariants, risks, dependencies, assumptions, and open questions.

Optional inputs include approved feature specs, Ticket Ready artifacts, system maps, domain context, negative knowledge, similar Delivery Cases, alignment receipts, implementation plans, diffs, tests, review comments, incidents, and reusable-asset observations.

## Outputs

Produce:

```text
artifacts/feature-understanding/<case-id>/<run-id>/understanding-state.v1.json
artifacts/feature-understanding/<case-id>/<run-id>/understanding-summary.md
artifacts/feature-understanding/<case-id>/<run-id>/understanding-delta.v1.json
artifacts/capability-runs/feature-understanding-loop/<run-id>/run-result.json
```

When write permission is unavailable, return the complete structured result inline with `write_status=returned_inline`.

The understanding state must contain:

- an Understanding Contract naming the next decision and stop gate;
- dimensions for intent, scope, domain, system slice, change model, impact, evidence, and operations;
- evidence-linked claims with state, priority, owner, source, confidence boundary, and validation action;
- conflicts, counterexamples, unknowns, excluded context, and permission gaps;
- a Sufficient Understanding Gate result;
- teach-back prompts and evaluation status;
- the selected next artifact or explicit stop reason.

The Understanding Delta must state which claims were added, confirmed, invalidated, conflicted, made stale, or left unresolved by implementation, test, review, or human feedback.

## Evidence

Separate `observed`, `derived`, `judged`, and `unknown` content. Every material claim must have a resolvable evidence reference or remain `hypothesis` or `unknown`.

Use these claim states:

```text
unknown
hypothesis
evidenced
confirmed
conflicted
stale
invalidated
```

Prefer authoritative runtime, interface, test, policy, and owner-confirmed evidence over generated explanation. Documentation alone does not prove current runtime behavior. Similarity does not prove applicability. A repeated statement does not become confirmed by repetition.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- the next decision and required understanding dimensions are explicit;
- all priority-zero claims are evidenced or confirmed, or remain explicitly owned unknowns;
- no unresolved priority-zero conflict is hidden;
- the system slice identifies entry points, control points, data or state movement, impact boundaries, and validation points;
- acceptance and invariants are connected to evidence and validation;
- the learner or accountable developer can explain the outcome, path, critical control, and one failure case without copying the artifact;
- the next Work Ready or PR Ready artifact is reviewable and does not overstate readiness;
- real implementation or review feedback produces an append-only Understanding Delta;
- reusable knowledge is emitted only as a scoped candidate with source, limitation, and activation boundary.

## Stop Conditions

Stop at the next reviewable delivery state. Stop without repeated probing when:

- the decision to support is missing or keeps changing;
- required authority, source access, permission, or accountable owner is unavailable;
- a priority-zero conflict cannot be resolved in the current scope;
- critical facts remain unverifiable and proceeding would create false readiness;
- security, privacy, compliance, production, architecture, or data-governance boundaries require human judgment;
- no new evidence appears in a bounded retry;
- context expansion exceeds the approved scope or budget;
- the Sufficient Understanding Gate is met and further exploration would not change the next decision.

State the exact missing evidence or authority, owner, impact, and resumable next step.

## Workflow

1. **Contract** — bind the Feature, next decision, roles, required dimensions, scope, non-goals, critical questions, risk class, and stop gate.
2. **Route** — query ConPort and compact capability metadata first; select one smallest sufficient primary capability before composition.
3. **Sense** — assemble a task-scoped Context Pack from targeted code, configuration, tests, history, decisions, policies, incidents, and authorized human sources.
4. **Model** — build only the Feature-relevant system slice, domain constraints, change hypothesis, impact hypothesis, validation map, and claim ledger.
5. **Challenge** — seek contradictory evidence, negative knowledge, counterexamples, hidden consumers, shadow dependencies, stakeholder surprise, stale assumptions, and unasked questions.
6. **Verify** — verify source coverage and consistency, test predictive explanations where possible, and run teach-back for critical controls and exceptions.
7. **Gate** — evaluate the Sufficient Understanding Gate for the named next decision; do not replace accountable human confirmation.
8. **Commit** — write verified state and evidence into the Feature Delivery Case projection and generate the selected Work Ready or PR Ready artifact.
9. **Use** — let implementation, testing, and review generate external evidence; never let the latest model output overwrite the last verified state.
10. **Learn** — create an append-only Understanding Delta and route reusable observations into the reviewed Experience-to-Asset path.
11. Keep invariant routing, state definitions, and output contracts in a stable prefix; keep task evidence in a bounded dynamic suffix.

## Collaboration Boundaries

- `context-mastery` selects the smallest specialist capability and bounded context path.
- `system-mental-model` builds the evidence-linked Feature system slice.
- `domain-context-pack`, `negative-knowledge-pack`, and similar-work capability add task-specific organizational context.
- `unasked-questions-generator`, knowledge integrity, and risk capabilities challenge the current model.
- `ticket-ready-package` and `implementation-plan` project confirmed and proposed understanding into a Work Ready path.
- review capabilities project implementation evidence into PR Ready and reviewer challenge.
- `feature-delivery-case` remains the canonical lifecycle value and evidence boundary.
- AegisFlow may orchestrate bounded transitions; FlowGuard enforces scope and permission; Memexa preserves append-only state; Helixion proposes cross-run improvements only; DeliveryYield measures economics after delivery evidence and never approves readiness.

## Rules

```text
FUL.001 | MUST | contract | name one next delivery decision before collecting context
FUL.002 | MUST | scope | use a bounded Feature system slice rather than whole-repository coverage
FUL.003 | MUST | claim | record state owner priority evidence and validation for material claims
FUL.004 | MUST | challenge | actively seek contradiction counterexample hidden dependency and stale assumption evidence
FUL.005 | MUST | learning | require teach-back for critical controls exceptions and impact boundaries
FUL.006 | MUST | gate | evaluate sufficient understanding for the named decision rather than claiming complete understanding
FUL.007 | MUST | delta | preserve append-only understanding changes from implementation test review and human feedback
FUL.008 | MUST | authority | keep readiness scope date architecture compliance and release decisions human-controlled
FUL.009 | SHOULD | routing | select one primary capability before adding named dependencies
FUL.010 | SHOULD | context | load the smallest source slice that can prove or disprove the next material claim
FUL.011 | SHOULD | token | optimize quality-adjusted token ROI only after evidence fidelity passes
FUL.012 | SHOULD | prompt | keep stable rules schemas and state vocabulary before dynamic Feature evidence
FUL.013 | NEVER | readiness | declare Work Ready or PR Ready from generated prose or model confidence alone
FUL.014 | NEVER | context | dump the full repository logs transcripts knowledge base or capability catalog
FUL.015 | NEVER | promotion | auto-promote an understanding output into a team-wide asset rule Skill or belief
FUL.016 | NEVER | role | write code merge release or issue a delivery verdict
```

## Verification

```bash
python scripts/validate_skill_package.py --root skills/feature-understanding-loop
python -m json.tool skills/feature-understanding-loop/schemas/understanding-state.v1.schema.json >/dev/null
python scripts/validate_capability_context.py --root .
```

Human review must also confirm that the sample does not create unsupported intent, false readiness, or hidden priority-zero unknowns.

## Failure Modes

- decisionless-research: the system explores without a named next decision;
- summary-as-understanding: fluent explanation is accepted without evidence or prediction;
- context-bloat: the repository or knowledge base is loaded instead of a Feature slice;
- false-ready: unknowns, conflicts, or proposed acceptance are hidden to make the task appear ready;
- happy-path-only: failure paths, control points, and counterexamples are omitted;
- borrowed-understanding: the learner repeats the artifact but cannot explain why or when it fails;
- latest-output-wins: later unverified prose overwrites a previously verified state;
- premature-asset-promotion: one successful case becomes team guidance without review and scope qualification.

## References

- `schemas/understanding-state.v1.schema.json`
- `references/feature-understanding-loop.md`
- `../context-mastery/SKILL.md`
- `../system-mental-model/SKILL.md`
- `../ticket-ready-package/SKILL.md`
- `../feature-delivery-case/SKILL.md`
- `../../docs/capability-context-contract.md`
