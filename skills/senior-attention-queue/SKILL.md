---
name: senior-attention-queue
description: Use to turn multiple bounded expert requests into a transparent, evidence-backed decision queue that lets scarce senior attention resolve the most material blockers first. Input is decision requests, Feature Delivery Case context, impact, urgency, reversibility, options, evidence, latest-safe decision times, required expertise, owners, and delegation candidates; output is a prioritized queue with a one-line ask, minimum sufficient context, evidence references, options, recommendation status, delegable preparation, and final decision owner. Do not use to automate expert judgment, prioritize by requester seniority or message volume, rank people, or contact experts without approval; preserve uncertainty, privacy, behavior, and human authority.
---

# Senior Attention Queue

## Goal

Use scarce expert time on decisions where informed judgment changes delivery outcomes, while delegating preparation that does not require the expert.

## Use When

Use when expert requests, reviews, or architecture and domain decisions are accumulating; several delivery cases are waiting; or a manager needs a decision queue rather than an undifferentiated backlog.

## Do Not Use When

Do not use when the request can be resolved by documented policy, deterministic validation, or an already-authorized owner; to infer urgency from communication volume; or to make the final expert decision.

## Inputs

Require each decision request's Feature Delivery Case or source scope, one-line question, affected outcome, evidence, options, risks, reversibility, decision owner, required expertise, latest-safe decision time, no-decision consequence, privacy classification, and known delegable preparation.

## Outputs

Write by default to:

```text
artifacts/expert-decisions/<queue-id>/<run-id>/senior-attention-queue.v1.json
artifacts/expert-decisions/<queue-id>/<run-id>/queue.md
artifacts/capability-runs/senior-attention-queue/<run-id>/run-result.json
```

When write permission is unavailable, return the complete queue inline with `write_status=returned_inline`.

For each item include the one-line ask, impact, latest-safe decision time, reversibility, required expertise, minimum context, evidence references, options and tradeoffs, recommendation status, delegable preparation, responsible preparer, final decision owner, and unresolved unknowns. Explain ordering with visible criteria; do not emit a black-box priority score.

## Evidence

Separate facts from inference. Record uncertainty, unknowns, assumptions, conflicts, source dates, and applicability scope. Priority evidence may include safety or compliance exposure, user impact, delivery blocking, irreversible commitment, decision expiry, and dependency fan-out. Requester seniority, repetition, message count, and meeting count are not priority evidence.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- each queued item has a decision-ready one-line ask and minimum sufficient context;
- ordering is explainable from material impact and timing;
- non-expert preparation is delegated explicitly;
- the expert can decide, delegate, or ask one bounded follow-up;
- final judgment remains with the named expert or accountable owner.

## Stop Conditions

Stop when the queue is decision-ready or the requested triage stage is complete. Stop for missing permission, insufficient evidence, no accountable decision owner, unresolved sensitive-data boundaries, conflicting impact evidence, or a safety, compliance, architecture, product, or personnel decision requiring human authority. Do not send or escalate the queue automatically.

## Workflow

1. Bound the queue, decision window, expert role, and authority.
2. Query ConPort before loading or searching full Skill text when available; otherwise read only targeted authorized sources.
3. Normalize each request into one decision, impact, deadline, evidence set, and owner.
4. Remove items answerable by existing policy or deterministic evidence and route them to the proper owner.
5. Order remaining items by material impact, latest-safe time, reversibility, and dependency fan-out.
6. Compress each item to minimum sufficient context without hiding uncertainty.
7. Identify delegable research, evidence collection, or drafting.
8. Return the queue for expert or manager review; stop before final decisions or outreach.

## Rules

SAQ.001 | MUST | decision | express each queue item as one bounded decision request
SAQ.002 | MUST | evidence | make ordering criteria evidence-backed and visible
SAQ.003 | MUST | context | provide minimum sufficient context and source references
SAQ.004 | MUST | delegation | separate expert judgment from delegable preparation
SAQ.005 | MUST | authority | preserve the named final decision owner
SAQ.006 | SHOULD | token | optimize quality-adjusted token ROI after decision fidelity passes
SAQ.007 | SHOULD | prompt | keep ordering rules and output contract in a stable prefix
SAQ.008 | NEVER | personnel | rank people or infer priority from status or communication volume
SAQ.009 | NEVER | action | contact escalate assign or decide without applicable authority

## Verification

- Every item has impact, timing, options, evidence, unknowns, and a named decision owner.
- Queue order can be explained without a hidden score.
- Delegable work is distinct from expert judgment.
- Sensitive details are minimized.

## Failure Modes

- turning the inbox into a new opaque score;
- prioritizing loudness instead of material impact;
- including full project history instead of minimum context;
- asking the expert to perform evidence collection others can do;
- treating queue order as the final decision.
