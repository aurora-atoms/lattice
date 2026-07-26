---
name: unasked-questions-generator
description: Use to identify important questions a team has not yet asked during requirement review, system design, release readiness, or cross-system change. Input is a bounded requirement or design, dependencies, business rules, current assumptions, historical incidents, evidence, delivery stage, owners, and deadlines; output is an evidence-linked gap map with impact-ranked missing questions, why each matters, who should answer, the latest safe answer time, and an explicit disposition of must-answer, non-blocking, accepted uncertainty, or excluded. Do not use as a generic checklist, brainstorming prompt, automatic blocker, or substitute for expert judgment; preserve behavior, provenance, human control, privacy, and stage-gate authority.
---

# Unasked Questions Generator

## Goal

Expose consequential questions missing from the current problem frame before they become implementation rework, release surprises, or production incidents.

The capability does not maximize the number of questions. It finds the smallest set of questions whose answers could materially change scope, design, validation, rollout, ownership, or risk acceptance.

## Use When

Use during:

- requirement or acceptance review;
- architecture and detailed design;
- cross-system, data-contract, or dependency changes;
- implementation readiness and pull-request planning;
- release, migration, cutover, or operational readiness;
- incident follow-up when recurrence assumptions may be incomplete.

Use B07 through `context-mastery` when the broader need is context-learning capability selection. Use this Skill directly when the review artifact, stage, and decision boundary are already known.

## Do Not Use When

Do not use to:

- generate a broad checklist without evidence of relevance;
- repeat questions already answered by authoritative sources;
- convert every uncertainty into a blocker;
- replace architecture, product, security, compliance, or release authority;
- infer stakeholder views without evidence;
- rank people or attribute blame for missing questions;
- continue searching after the requested review stage or evidence boundary is reached.

Route a selected question that needs scarce expert attention to `decision-question-builder`. Route assumption validity and expiry to `knowledge-integrity`. Route stakeholder surprise and commitment risk analysis to `risk-ahead`.

## Inputs

Require:

- bounded requirement, design, change, or Feature Delivery Case;
- current delivery stage and next commitment gate;
- intended user outcome and acceptance criteria;
- systems, data, interfaces, dependencies, and affected boundaries;
- business rules and non-functional constraints;
- current assumptions, known unknowns, and accepted risks;
- relevant historical incidents, failed attempts, or prior delivery cases;
- accountable roles and response deadlines;
- authorized source access and disclosure boundary.

Optional inputs include rollout plans, test evidence, monitoring, support model, migration state, dependency service levels, and stakeholder map.

## Outputs

Produce:

```text
artifacts/unasked-questions/<review-id>/<run-id>/unasked-questions.v1.json
artifacts/unasked-questions/<review-id>/<run-id>/review.md
artifacts/capability-runs/unasked-questions-generator/<run-id>/run-result.json
```

The JSON artifact must conform to `schemas/unasked-questions.v1.schema.json`. The Markdown companion must be concise enough for a requirement, design, or release review.

When write permission is unavailable, return the complete structured result inline and set `write_status=returned_inline`.

A complete gap map contains:

1. **Review boundary**: artifact reviewed, delivery stage, next gate, scope, non-scope, and evidence cutoff.
2. **Coverage map**: which question domains were relevant, covered, missing, not applicable, or not assessable.
3. **Ranked missing questions**: only questions that could change a decision or execution path.
4. **Disposition** for every question:
   - `must_answer_now`;
   - `must_answer_before_implementation`;
   - `must_answer_before_merge`;
   - `must_answer_before_release`;
   - `answer_by_observation`;
   - `accepted_uncertainty`;
   - `non_blocking_follow_up`;
   - `excluded`.
5. **Control summary**: questions proposed as blockers, questions explicitly accepted without answers, and the accountable human decisions.
6. **Handoff candidates**: selected questions suitable for `decision-question-builder`, assumption review, or stakeholder-risk review.

Each missing-question record must state:

- one precise question;
- question domain;
- why the current frame omitted or obscured it;
- why the answer matters;
- evidence and historical signals supporting relevance;
- affected systems, users, data, controls, or stakeholders;
- consequence if unanswered or answered incorrectly;
- answer owner or accountable role;
- latest safe answer time and related gate;
- disposition and blocking rationale;
- expected answer form;
- next action after the answer;
- linked assumptions, conflicts, and unknowns;
- confidence and disconfirming evidence.

## Question Domains

Assess only domains relevant to the bounded change:

- user outcome and requirement ambiguity;
- business rules and exceptional cases;
- system boundaries and ownership;
- data source, contract, lineage, retention, and quality;
- dependency behavior, service levels, and version compatibility;
- authorization, privacy, security, compliance, and audit;
- failure modes, degradation, recovery, and manual operations;
- migration, rollout, rollback, coexistence, and reversibility;
- observability, alerting, support, and incident response;
- performance, capacity, cost, and scaling limits;
- testability, acceptance evidence, and production validation;
- stakeholder impact, communication, training, and surprise risk;
- assumptions, expiry conditions, and environmental drift;
- historical incident recurrence and rejected alternatives.

Do not include a domain merely because it appears in this list. Record why it is applicable or mark it not applicable.

## Impact Ranking

Rank questions using evidence-backed ordinal factors rather than false numerical precision:

- impact severity;
- blast radius;
- reversibility;
- likelihood or recurrence signal;
- time sensitivity;
- uncertainty that can change the decision;
- distance to the next commitment gate.

Assign `critical`, `high`, `medium`, or `low` and include a short ranking rationale. A question is not critical merely because it concerns an important system; it must have a plausible path to material harm or blocked delivery.

## Human Control

The team retains authority over whether a question blocks work.

For each proposed blocker:

- name the gate it protects;
- state the evidence for blocking;
- identify the accountable role that can answer, accept, defer, or waive it;
- record the consequence and expiry of any waiver.

For accepted uncertainty:

- state why proceeding is reasonable;
- define monitoring or validation;
- define the trigger that reopens the question;
- identify who accepted the uncertainty and within what scope.

Never treat a generated question, missing answer, or model confidence as automatic authority to stop delivery.

## Evidence

Separate:

- source-supported facts;
- inference used to identify the missing question;
- resolvable citations and observation time;
- uncertainty and confidence;
- known unknowns;
- assumptions and expiry conditions;
- conflicting evidence;
- historical signals and their applicability limits;
- guesses, which must not support blocking status.

A question is evidence-linked when at least one of the following is present:

- an unresolved requirement or acceptance dependency;
- a system, data, or control boundary without an owner or contract;
- a historical incident or failed attempt with applicable similarity;
- an assumption whose failure changes behavior or risk;
- a dependency or stakeholder consequence not represented in the current artifact;
- missing validation for a material claim.

Do not claim a question is missing until the reviewed artifacts and available authoritative sources have been checked. Do not ask questions that are already answered unless the answer is stale, conflicting, unverified, or outside its original scope.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- the review finds a small evidence-linked set of consequential missing questions rather than a generic checklist;
- every question can change a named decision, gate, validation activity, or execution path;
- questions are ranked by impact and time sensitivity with explicit rationale;
- each question names an accountable answer role and latest safe answer time;
- already-answered, irrelevant, and duplicate questions are excluded;
- must-answer questions are separated from accepted uncertainty and non-blocking follow-up;
- human owners retain explicit authority to answer, defer, accept, waive, or exclude;
- selected expert questions can be handed to `decision-question-builder` without reconstructing context;
- material assumption-expiry and stakeholder-surprise gaps are visible.

Artifact generation alone is not success. Mark the run partial or blocked when evidence coverage is too weak to distinguish consequential gaps from speculation.

## Stop Conditions

Stop at the requested review artifact or next reviewable stage. Do not send questions, assign owners, change gates, or stop delivery unless explicitly authorized.

Stop without repeated probing when:

- the reviewed artifact, stage, next gate, or scope is missing;
- required sources, incident evidence, business rules, or permissions are unavailable;
- the available evidence cannot distinguish missing questions from generic possibilities;
- ownership or gate authority requires human adjudication;
- a privacy, security, compliance, personnel, architecture, production, or other high-risk boundary is reached;
- validation fails after one bounded corrective retry;
- the goal, stage gate, retry budget, human decision, or user stop condition is reached.

For a blocked run, state the exact missing evidence or permission, accountable owner, why it matters, and the smallest resumable next step.

## Workflow

1. Bound the artifact, stage, next gate, affected systems, evidence cutoff, and authority.
2. Query compact governed context before broad source loading; use targeted authorized reads for named gaps.
3. Extract explicit decisions, assumptions, dependencies, business rules, risks, owners, tests, rollout, and operations already covered.
4. Build a coverage map across only relevant question domains.
5. Compare the current frame with runtime boundaries, historical incidents, cross-system dependencies, and stakeholder consequences.
6. Generate candidate missing questions, then remove generic, duplicate, already-answered, non-actionable, and unsupported items.
7. Link each retained question to evidence, impact boundary, answer owner, latest safe answer time, and next action.
8. Rank questions and propose a disposition without assigning automatic blocking authority.
9. Mark accepted uncertainty, monitoring, waiver expiry, and reopen triggers.
10. Route selected questions to `decision-question-builder`, assumption-expiry review to `knowledge-integrity`, and stakeholder-surprise review to `risk-ahead` only when a named gap exists.
11. Validate the artifact and stop for human review.

## Rules

UQG.001 | MUST | boundary | define the reviewed artifact stage next gate scope and evidence cutoff
UQG.002 | MUST | evidence | link each retained question to a concrete gap signal and resolvable source
UQG.003 | MUST | value | retain only questions that can change a decision gate validation or execution path
UQG.004 | MUST | priority | rank by impact reversibility uncertainty and time sensitivity
UQG.005 | MUST | ownership | name who should answer and the latest safe answer time
UQG.006 | MUST | control | separate must-answer non-blocking accepted uncertainty and excluded questions
UQG.007 | MUST | authority | preserve human authority over blockers waivers deferrals and risk acceptance
UQG.008 | MUST | lifecycle | define next action monitoring expiry and reopen triggers where applicable
UQG.009 | SHOULD | handoff | route one selected expert decision to decision-question-builder
UQG.010 | SHOULD | collaboration | use assumption-expiry or stakeholder-surprise review only for named evidence gaps
UQG.011 | SHOULD | token | optimize quality-adjusted prevention value before question count or token reduction
UQG.012 | NEVER | checklist | emit a generic exhaustive review list without relevance evidence
UQG.013 | NEVER | duplication | ask questions already answered by current authoritative evidence
UQG.014 | NEVER | blocking | turn every unknown into a blocker or infer authority from model confidence
UQG.015 | NEVER | personnel | rank blame monitor or infer individual performance

## References

- Use `schemas/unasked-questions.v1.schema.json` for the machine-readable output.
- Use `scripts/validate_unasked_questions.py` for semantic checks beyond JSON syntax.
- Use `../decision-question-builder/SKILL.md` to prepare one selected question for a scarce expert.
- Use `../knowledge-integrity/SKILL.md` for assumption validity, expiry, conflict, and review triggers.
- Use `../risk-ahead/SKILL.md` for stakeholder surprise, latent commitment risk, and risk controls.

## Verification

```bash
python scripts/validate_skill_package.py --root skills/unasked-questions-generator
python skills/unasked-questions-generator/scripts/validate_unasked_questions.py skills/unasked-questions-generator/evals/fixtures/valid-unasked-questions.json
python -m unittest discover -s skills/unasked-questions-generator/evals -p 'test_*.py' -v
python -m json.tool skills/unasked-questions-generator/schemas/unasked-questions.v1.schema.json >/dev/null
python scripts/validate_capability_context.py --root .
python scripts/validate_skill_change_contract.py --base-ref <base-sha> --head-ref HEAD
```

## Failure Modes

- producing a generic checklist instead of evidence-linked gaps;
- restating known unknowns without finding omissions in the frame;
- asking questions that available evidence already answers;
- ranking by dramatic wording rather than impact and timing;
- omitting the answer owner or latest safe answer time;
- treating all questions as release blockers;
- accepting uncertainty without monitoring or a reopen trigger;
- confusing stakeholder speculation with stakeholder evidence;
- routing a broad question set to an expert instead of selecting one decision;
- hiding the evidence boundary or uncertainty behind confident language.
