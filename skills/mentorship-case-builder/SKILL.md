---
name: mentorship-case-builder
description: Use to convert a real delivery decision, review exchange, incident, or implementation change into a bounded mentorship case that teaches judgment without requiring another meeting. Input is a source case, learning objective, decision context, evidence, alternatives, review comments, outcome, known limits, target learner, and expert annotations; output is a teach-back case with scenario, signals, tempting wrong options, decision point, explanation, feedback rubric, applicability boundary, and expert review status. Do not use to present one reviewer preference as universal truth, generate personnel evaluation, expose sensitive comments, or replace live mentoring where stakes or ambiguity require it; preserve evidence, uncertainty, privacy, behavior, and human judgment.
---

# Mentorship Case Builder

## Goal

Turn authentic team decisions into reusable judgment practice so learners can recognize signals and explain why, while experts retain control over what is taught.

## Use When

Use after a meaningful review, design choice, production issue, implementation tradeoff, or repeated coaching question can become a short practice case for onboarding, cross-domain learning, or review follow-up.

## Do Not Use When

Do not use when the source is unverified, the case would expose sensitive personnel information, the expert cannot review the interpretation, or the decision is too context-dependent to teach as a bounded example.

## Inputs

Require a source Feature Delivery Case or evidence set, learning objective, target learner, decision context, relevant signals, options considered, chosen action, outcome evidence, expert annotations, known exceptions, privacy classification, and accountable curator.

## Outputs

Write by default to:

```text
artifacts/mentorship-cases/<case-id>/<run-id>/mentorship-case.v1.json
artifacts/mentorship-cases/<case-id>/<run-id>/exercise.md
artifacts/capability-runs/mentorship-case-builder/<run-id>/run-result.json
```

When write permission is unavailable, return the complete case inline with `write_status=returned_inline`.

Include the scenario, learning objective, evidence available to the learner, hidden or staged information, decision point, plausible options, tempting wrong options and why they fail, expected reasoning, teach-back questions, feedback rubric, applicability boundary, counterexample, expert review status, and next review trigger.

## Evidence

Separate observed case facts from derived teaching structure and judged inference or interpretation. Record uncertainty, unknowns, assumptions, conflicts, source dates, outcome quality, and expert annotations. A single successful review or individual style preference is not universal policy.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- the learner must reason from authentic evidence rather than memorize an answer;
- the case teaches a transferable signal and an explicit boundary;
- wrong options are plausible and explain common failure modes;
- an expert or accountable curator reviewed the interpretation;
- learner feedback can reveal misunderstanding without becoming personnel scoring.

## Stop Conditions

Stop when the case is reviewable or the requested learning stage is complete. Stop for missing permission, insufficient source evidence, absent curator, privacy or compliance boundaries, unresolved disagreement about the lesson, or a high-stakes judgment that requires live expert guidance. Do not publish or assign the exercise automatically.

## Workflow

1. Bound the source case, learner, learning objective, sensitivity, and curator authority.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Identify the decision signal that is worth learning, not merely the final answer.
4. Separate case facts, expert judgment, outcome evidence, and unresolved alternatives.
5. Construct a compact scenario with plausible choices and a teach-back prompt.
6. Add failure explanations, applicability limits, and at least one counterexample.
7. Obtain or request curator review; stop before publication or learner evaluation.

## Rules

MCB.001 | MUST | source | anchor the exercise in a real evidence-linked case
MCB.002 | MUST | judgment | teach signals reasoning and boundaries rather than answer memorization
MCB.003 | MUST | evidence | distinguish observed facts derived structure judged interpretation and unknowns
MCB.004 | MUST | human | require accountable curator review before team availability
MCB.005 | MUST | privacy | remove unnecessary personal and sensitive detail
MCB.006 | SHOULD | token | optimize quality-adjusted token ROI after learning fidelity passes
MCB.007 | SHOULD | prompt | keep exercise rules and output contract in a stable prefix
MCB.008 | NEVER | personnel | use learner results for hidden ranking or performance scoring
MCB.009 | NEVER | universalize | treat one reviewer style or one case as universal truth

## Verification

- Source evidence, learning objective, expected reasoning, boundary, and counterexample are present.
- The exercise can be completed without revealing the answer prematurely.
- Curator status and unresolved disagreements are explicit.
- No personnel score or surveillance output is produced.

## Failure Modes

- turning review comments into trivia;
- teaching the final choice without the evidence signals;
- preserving identifying or sensitive conversation detail;
- presenting one expert preference as policy;
- using the exercise as covert performance evaluation.
