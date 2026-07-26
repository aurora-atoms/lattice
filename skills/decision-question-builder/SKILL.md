---
name: decision-question-builder
description: Use to turn an unclear architecture, product, operational, or delivery decision into one evidence-backed option question for a scarce expert, architect, or senior leader. Input is a bounded decision, target respondent and authority, current state, known facts with source references, material unknowns, constraints, candidate options, risks, deadline, and the action that follows an answer; output is a decision-question packet with two to four comparable options, evidence and uncertainty for each option, a minimal-response contract, recommendation when justified, and executable next steps. Do not use for open-ended brainstorming, questions answerable from available sources, personnel evaluation, automatic final judgment, or advocacy disguised as neutral options; preserve evidence, option symmetry, human authority, privacy, and stop boundaries.
---

# Decision Question Builder

## Goal

Convert a context-poor request for expert attention into the smallest answerable question that can unlock a concrete next action.

Optimize expert-answer latency, not question volume. Do the discoverable work before asking the scarce expert to reconstruct context.

## Use When

Use when a bounded decision requires expertise or authority that the current caller does not possess, especially for architecture, system boundaries, business rules, risk acceptance, prioritization, or cross-team ownership.

Use B06 through `context-mastery` when the broader category selected question preparation. Use this Skill directly when the decision and intended respondent are already clear.

## Do Not Use When

Do not use when:

- the answer is available from authorized code, tests, documentation, logs, decisions, or named owners and has not been researched;
- the request is broad discovery or brainstorming rather than a decision;
- options cannot yet be made meaningfully distinct;
- the recipient does not own the required knowledge or authority;
- the question asks the expert to perform the caller's analysis;
- the output would rank people, expose unnecessary sensitive context, or automate final human judgment.

Route missing task context to `domain-context-pack`, system uncertainty to `system-mental-model`, conflicting claims to `knowledge-integrity`, option risk analysis to `risk-ahead`, and expert queue or mentorship orchestration to `human-judgment-amplifier`.

## Inputs

Require:

- one bounded decision and the execution action it unlocks;
- target respondent role, why that role is authoritative, and response deadline;
- current state, scope, constraints, and non-goals;
- source-supported known facts;
- material unknowns and assumptions;
- two to four candidate options, or enough evidence to derive them without inventing facts;
- implementation owner and next step for each selectable answer;
- permission boundary and allowed disclosure level.

If the decision contains independent choices, split it into separate packets and ask only the first blocking decision.

## Outputs

Produce:

```text
artifacts/decision-questions/<decision-id>/<run-id>/decision-question.v1.json
artifacts/decision-questions/<decision-id>/<run-id>/ask.md
artifacts/capability-runs/decision-question-builder/<run-id>/run-result.json
```

The JSON artifact must conform to `schemas/decision-question-packet.v1.schema.json`. The Markdown companion must be ready to paste into the approved communication channel without requiring the recipient to open the full evidence set.

When write permission is unavailable, return the complete artifacts inline and set `write_status=returned_inline`.

A complete packet contains:

1. **Decision needed**: one sentence naming the answer required and the action it unlocks.
2. **Why now**: deadline, blocking impact, and consequence of delay.
3. **Scope**: included and excluded surfaces.
4. **Known facts**: concise claims with resolvable source references.
5. **Material unknowns**: only unknowns that could change the decision.
6. **Options**: two to four mutually distinguishable choices. Each option states:
   - what would be done;
   - evidence supporting viability;
   - benefits and tradeoffs;
   - risks and affected boundaries;
   - assumptions and important exceptions;
   - reversibility or rollback;
   - action and validation after selection.
7. **Recommendation**: include only when evidence supports it; otherwise state `no_recommendation` and why.
8. **Minimum response contract**: make a one-line answer sufficient, such as `A`, `B`, `C`, `defer until <fact>`, or `none: <blocking reason>`.
9. **Fallback behavior**: state what happens if no answer arrives by the deadline; never invent approval by silence for high-risk decisions.
10. **Follow-up budget**: at most two conditional follow-ups, each tied to an answer that changes execution.

## Evidence

Separate:

- facts with source references, scope, version, and observation time;
- inference used to derive options or recommendation;
- citations supporting each material option claim;
- uncertainty and confidence;
- unknowns that can change the decision;
- assumptions and the impact if false;
- conflicts between sources or stakeholders;
- guesses, which must not be presented as evidence.

Each option must have sufficient evidence to show that it is viable or must be explicitly labeled `insufficiently_supported`. Do not create false symmetry by padding a preferred option with detail while leaving alternatives vague.

Evidence is insufficient when the decision boundary, respondent authority, material constraints, or viability of at least two options cannot be established. Stop rather than send a speculative question.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- one primary answer can unlock a named executable next step;
- the correct scarce expert or accountable role is identified;
- discoverable context has been resolved before escalation;
- two to four options are comparable and materially distinct;
- every option exposes evidence, risks, assumptions, exceptions, and execution consequences;
- known facts, unknowns, inference, and recommendation are visibly separated;
- the recipient can answer with one line without reconstructing the background;
- the packet does not hide a high-risk approval, unrelated second decision, or unresolved prerequisite.

Artifact creation alone is not success. Mark the run partial or blocked when the packet still transfers avoidable analysis work to the recipient.

## Stop Conditions

Stop at a reviewable decision-question packet. Do not send it or continue into execution unless explicitly authorized.

Stop without repeated probing when:

- the target respondent, authority, decision, execution consequence, or deadline is missing;
- required source or permission access is unavailable;
- evidence cannot establish at least two viable, meaningfully distinct options;
- a material conflict requires owner adjudication before option framing;
- evidence is insufficient for comparative risk or recommendation;
- privacy, security, compliance, data-governance, architecture, production, personnel, or other high-risk boundaries would be crossed;
- validation fails after one bounded corrective retry;
- the goal, stage gate, retry budget, human decision, or user stop condition is reached.

For a blocked packet, state the exact missing fact or permission, accountable owner, why it matters, and the smallest resumable next step.

## Workflow

1. Define the decision, execution action, recipient, authority, and deadline.
2. Query ConPort and compact source metadata before loading broad context; use authorized targeted sources when ConPort is unavailable.
3. Answer questions that can be resolved from existing evidence instead of escalating them.
4. Separate one blocking decision from adjacent discussion topics.
5. Build two to four options from evidence. Include `defer` only when waiting has a concrete trigger and cost.
6. Normalize option detail so evidence, risks, assumptions, exceptions, reversibility, action, and validation are comparable.
7. Recommend an option only when the evidence advantage is explicit; expose confidence and disconfirming evidence.
8. Write one primary question and the minimum response contract.
9. Remove background that does not change the answer; retain citations for material claims.
10. Validate with `scripts/validate_decision_question_packet.py` and stop for review.

## Rules

DQB.001 | MUST | decision | ask one blocking decision that unlocks a named action
DQB.002 | MUST | research | resolve discoverable questions before consuming scarce expert attention
DQB.003 | MUST | options | provide two to four materially distinct comparable options
DQB.004 | MUST | evidence | attach facts citations uncertainty unknowns assumptions and conflicts
DQB.005 | MUST | risk | state option-specific risks boundaries exceptions and reversibility
DQB.006 | MUST | response | make a one-line minimum sufficient answer possible
DQB.007 | MUST | action | state owner next step and validation for every selectable option
DQB.008 | MUST | authority | preserve final expert and accountable-owner judgment
DQB.009 | SHOULD | recommendation | recommend only when evidence is asymmetric and disclose why
DQB.010 | SHOULD | token | optimize decision quality and expert time before token reduction
DQB.011 | SHOULD | prompt | keep the option and evidence contract in a stable prefix and task facts dynamic
DQB.012 | NEVER | burden | ask the recipient to reconstruct context or perform avoidable analysis
DQB.013 | NEVER | bias | disguise advocacy as balanced options or hide disconfirming evidence
DQB.014 | NEVER | silence | treat missing response as approval for a high-risk decision
DQB.015 | NEVER | personnel | score rank monitor or infer individual performance

## References

- Use `schemas/decision-question-packet.v1.schema.json` for the machine-readable output shape.
- Use `scripts/validate_decision_question_packet.py` for semantic checks beyond JSON syntax.
- Compose with `../domain-context-pack/SKILL.md` only for a named context gap.
- Compose with `../human-judgment-amplifier/SKILL.md` when prioritizing or routing a queue of expert-attention requests; this Skill only prepares one decision question.

## Verification

```bash
python scripts/validate_skill_package.py --root skills/decision-question-builder
python skills/decision-question-builder/scripts/validate_decision_question_packet.py skills/decision-question-builder/evals/fixtures/valid-decision-question.json
python -m unittest discover -s skills/decision-question-builder/evals -p 'test_*.py' -v
python -m json.tool skills/decision-question-builder/schemas/decision-question-packet.v1.schema.json >/dev/null
python scripts/validate_capability_context.py --root .
python scripts/validate_skill_change_contract.py --base-ref <base-sha> --head-ref HEAD
```

## Failure Modes

- asking “what do you think?” without an executable decision;
- escalating before checking available evidence;
- presenting one real option plus weak straw alternatives;
- mixing several independent decisions into one request;
- hiding unknowns or recommendation bias;
- listing risks without the affected boundary or mitigation;
- omitting what happens after each answer;
- requiring a meeting when a one-line response would suffice;
- interpreting silence or ambiguity as approval.
