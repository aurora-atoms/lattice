---
name: adversarial-innovation-mining
description: Use for public-only or fully synthetic technical product research where the goal is to turn a reproducible adversarial failure, cross-system invariant violation, or safety-critical hard case into a reusable technical mechanism hypothesis, commercial-value hypothesis, and prior-art research handoff. Trigger when asked to mine innovation or patent-research candidates from product attacks, architecture reviews, system-boundary failures, state/identity/authority transitions, or safety-critical review records. Do not use for confidential employer/client material, unpublished real inventions, legal patentability/FTO/infringement conclusions, or unsupported novelty claims.
---

# Adversarial Innovation Mining

## Goal

Convert a **reproducible wrong-world failure** into a **missing reusable technical mechanism** and then into a **bounded invention-research candidate** without confusing customer need, product defect, engineering best practice, or prior-art gaps with patent novelty.

Default sequence:

```text
public/synthetic scope
-> bounded consequential claim
-> competent baseline
-> identity/state/action lineage
-> adversarial hard case
-> reproducible failure trace
-> missing mechanism
-> commercial-value test
-> counter-control + kill test
-> innovation handoff
-> prior-art challenger
-> retain / revise / reject
```

Use the repository's Safety-Critical Product Review contract when a structured review record already exists. Use Systematic Invention Research for the prior-art phase. This Skill owns the bridge between the two; it does not replace either workflow.

## Public-Only Gate

Allowed technical inputs:

- published patents and patent applications;
- public standards, papers, product documentation, public repositories, public incident material, and other public technical sources;
- information explicitly marked public by the user;
- fully synthetic scenarios and replay traces.

Stop concrete mechanism mining if the task contains or plausibly contains:

- employer/client confidential source code, architecture, requirements, telemetry, roadmap, or incident data;
- an unfiled or unpublished real invention concept;
- NDA, privileged, export-controlled, or otherwise restricted material.

Do not bypass this boundary by anonymizing, paraphrasing, or abstracting the private material. Replace it with a public or fully synthetic case first.

## Evidence Taxonomy

Keep review evidence separate from invention status:

```text
review evidence: OBSERVED | DERIVED | JUDGED | UNKNOWN
invention status: CANDIDATE | PRIOR_ART_PENDING | CHALLENGED | RETAIN_CANDIDATE | REJECT
```

When prior-art research begins, the downstream research workflow may use `FACT / INFERENCE / HYPOTHESIS / UNKNOWN`. Do not silently translate a `DERIVED` product failure into a `FACT` about prior art or novelty.

## Inputs

Minimum:

- one bounded product capability or consequential action;
- one load-bearing claim or invariant;
- public/synthetic evidence boundary and cutoff;
- competent baseline assumptions;
- customer or operator who bears the failure cost.

Preferred:

- a `lat.safety-critical-review.v1` record or equivalent Product Attack Card;
- replayable hard case or deterministic event trace;
- exact enforcement boundary and identity/state domains;
- current controls and strongest counter-control;
- measurable operational or commercial consequence.

## Workflow

### 1. Freeze the target

Define exactly one consequential claim. Do not start from a vague theme such as "AI safety" or "better drone security."

### 2. Steelman the competent baseline

Assume normal mature controls already exist unless evidence says otherwise: typed validation, deduplication, RBAC, retries/timeouts, health checks, logging, ordinary fusion, and normal failover.

Reject attack ideas that only beat a naive strawman.

### 3. Map the action lineage

Trace:

```text
observation / claim
-> fused or operational state
-> decision
-> authorization
-> selected resource / node
-> native handle
-> effect boundary
-> world state
-> outcome observation / attribution
```

Mark every change in identity, state version, time basis, authority, ownership, coordinate frame, source, or physical effect.

### 4. Construct hard cases

Prefer transitions where local components remain correct but the system can still produce the wrong real-world result: handoff/failover, split/merge/reacquisition, stale/out-of-order updates, target crossing, queued action after state/policy change, timeout with unknown physical outcome, retry/cancel races, cross-workflow composition, common-mode failure, effect-induced identity change, and wrong-target outcome attribution.

Each hard case must state the trigger, preconditions, locally-correct components, cross-boundary failure, externally meaningful consequence, and oracle.

### 5. Reproduce before inventing

Prefer deterministic synthetic replay, simulator, test bench, or controlled public test evidence. If the hard case is not reproduced, keep the mechanism as `CANDIDATE` or `UNKNOWN`; do not promote it as an innovation signal.

A strong replay compares the same event trace under competent baseline versus guarded mechanism and shows a consequential decision difference.

### 6. Extract the missing mechanism

Ask: **What technical mechanism is absent that allows the hard case to survive a competent baseline?**

A mechanism candidate should have:

- explicit inputs and state/identity contract;
- enforcement boundary;
- deterministic predicate or state-machine behavior where feasible;
- invalidation/rebinding/reverification semantics;
- observable output or receipt;
- failure behavior;
- variation dimensions.

Reject as an invention candidate when the fix is only a UI warning, operator training/checklist, generic logging, generic RBAC, ordinary retry/timeout, a local bug fix with no reusable mechanism, or an architecture layer with no measurable reduction in wrong-world outcomes.

The rejected item may still remain a valid product-review rule.

### 7. Test mechanism generality

Generalize only as far as the failure mechanism supports. Record the mechanism core, required preconditions, non-goals, domain adapters, at least two plausible contexts when available, and what evidence would show the mechanism is merely standard engineering practice.

### 8. Apply the commercial-value filter

Every retained candidate must identify:

- customer/operator pain;
- measurable wrong-world cost or operational limitation;
- measurable outcome the mechanism could improve;
- plausible monetization path or product attach point;
- why the customer would pay or adopt rather than accept existing controls.

Commercial value does **not** imply novelty.

### 9. Attack the candidate before prior art

Find the strongest existing control that could make the new mechanism unnecessary.

Required questions:

- Can a competent baseline already enforce the invariant with existing versioning, transaction, state-machine, or verification primitives?
- Is this only a renamed standard pattern?
- Does the proposed mechanism reduce wrong-world outcomes better than simpler controls?
- What false-HOLD, latency, availability, operator-load, or implementation cost does it add?

Define at least one **kill criterion**. If the baseline passes the same hard case without the proposed mechanism, reject the candidate.

### 10. Emit the innovation handoff

Create an `adversarial-innovation-handoff.v1` record containing source review/chain IDs, hard case and replay reference, missing mechanism, customer pain and measurable value, strongest counter-control, falsifiers/kill criteria, prior-art challenge status, and retain/revise/reject decision.

Do not put hidden chain-of-thought into the record. Store observable evidence, structured claims, artifact references, uncertainty, and decisions.

### 11. Route prior-art work

A candidate can become `PRIOR_ART_PENDING` after the mechanism survives product/control kill tests. Then route it to the repository's **Systematic Invention Research** workflow.

Require a bounded prior-art challenge using multiple retrieval paths, patent-family de-duplication, independent-claim inspection for high-value families, alternate terminology, classifications, citation chains, and neighboring problem formulations.

Even after a bounded search finds no equivalent, use wording such as `retain as patent-research candidate`, `no equivalent found in bounded search`, and explicit coverage gaps. Never state `patentable`, `novel`, `FTO clear`, `non-infringing`, or `no prior art` as a legal/absolute conclusion.

### 12. Decide

Use one of:

- `RETAIN_CANDIDATE`: reproduced mechanism gap, commercial value, kill tests survived, and bounded prior-art challenge did not find an equivalent or broader mechanism;
- `PRIOR_ART_PENDING`: product/mechanism case is strong but prior-art challenge is incomplete;
- `CHALLENGED`: significant counter-control or prior-art evidence exists and needs resolution;
- `REJECT`: baseline already solves it, mechanism is ordinary practice, hard case is not reproducible, commercial value is weak, or prior art defeats the candidate;
- `CANDIDATE`: evidence is incomplete.

## Required Output Shape

For each candidate produce a compact card:

```text
Candidate ID
Source hard case / review chain
Load-bearing invariant
Reproduced wrong-world outcome
Missing technical mechanism
Enforcement boundary
Why competent baseline is insufficient
Customer pain
Measurable value
Monetization / attach point
Strongest counter-control
Kill criterion
Prior-art challenge status
Strongest counterevidence
Evidence class
Unknowns
Decision
Next falsification step
```

Prefer the repository machine contract when available:

```text
schemas/capability/adversarial-innovation-handoff.v1.schema.json
```

## Success Signals

A run is successful only when observable evidence supports the bridge from failure to mechanism:

- at least one hard case preserves competent-baseline local correctness;
- the wrong-world outcome is reproducible or explicitly not reproduced;
- the missing mechanism is technical and enforceable, not only procedural;
- the candidate names customer pain and measurable value;
- the strongest counter-control is recorded;
- at least one kill criterion exists;
- retained candidates are routed through prior-art challenge;
- prior-art results preserve strongest counterevidence and coverage gaps;
- no private technical material or unsupported legal conclusion is emitted.

## Stop Conditions

Stop when the public-only gate fails, the consequential claim cannot be bounded, no competent-baseline hard case can be constructed, the hard case cannot be reproduced/evidenced, the fix is only procedural/local, an existing control kills the mechanism, commercial value is generic, prior-art access is insufficient, or a legal IP conclusion is requested.

A valid result is `REJECT` or `insufficient_evidence`.
