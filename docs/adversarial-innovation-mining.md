# Adversarial Innovation Mining

## Agent Entry Point

If you arrived at this file without prior Lattice context, do not infer the surrounding workflow from repository folders. Start with the compact composition record in `registry/capability-compositions.index.jsonl`, then open `concepts/safety-critical-adversarial-innovation/README.md`.

The logical concept is:

```text
Safety-Critical Product Review
  -> Adversarial Innovation Mining
  -> Systematic Invention Research
```

Select only the stage supported by the evidence already available. For this stage, read this workflow as task context. Load the handoff schema only when emitting or checking a structured handoff. Execute the deterministic validator when required, but do not load validator source, tests, or CI YAML into ordinary task context. The machine-readable stage graph, artifact roles, activation scopes, and handoff conditions are in `concepts/safety-critical-adversarial-innovation/concept.json`.

This composition metadata is navigation only. It does not change capability identity, safety/release authority, or IP/legal conclusions.

## Decision

Use a **separate public-only bridge** between safety-critical product review and systematic invention research.

Do not add patent language to the authoritative safety-review verdict. First prove the product/mechanism gap; then create a bounded invention-research handoff; then attack that handoff with prior art.

```text
Safety-Critical Review
  requirement / invariant / hard case / replay / release gate
            |
            | only if a reproducible gap survives competent baseline
            v
Adversarial Innovation Handoff
  missing reusable mechanism
  + customer pain / measurable value
  + strongest counter-control
  + kill criteria
            |
            | public-only prior-art challenge
            v
Systematic Invention Research
  corpus / claims / mechanism neighbors / challenger
            |
            v
retain as research candidate | revise | reject
```

This workflow does **not** decide patentability, novelty, freedom to operate, infringement, claim scope, safety approval, or release.

## Why the bridge is separate

The Safety-Critical Product Review contract answers:

> Can a competent product still reach a wrong-world consequence, and what invariant/control/test/release gate is required?

Systematic Invention Research answers:

> What do published patents and public technical sources already disclose, and does an apparent mechanism gap survive a bounded challenger search?

The missing step is:

> Does the reproduced product failure reveal a reusable technical mechanism that is worth challenging as an invention-research candidate?

Keeping these artifacts separate prevents four category errors:

1. **Need-to-novelty error** — serious customer pain is not evidence of novelty.
2. **Bug-to-invention error** — a local defect or missing check is not automatically a reusable mechanism.
3. **Safety-to-IP coupling** — changing an invention hypothesis must never rewrite the safety verdict or release gate.
4. **Search-to-legal-conclusion error** — a bounded search that finds no equivalent is not a legal conclusion that no prior art exists.

## Public / IP Boundary

This public workflow may use only:

- published patents and applications;
- public standards, papers, repositories, product documentation, and public incident material;
- user-confirmed public technical material;
- fully synthetic products, traces, and examples.

Stop concrete mechanism mining for employer/client confidential material, unpublished real inventions, private source code or architecture, private experiments/data, NDA material, or restricted technical information.

Do not make private material public-safe by removing names or paraphrasing it. Replace the case with public or fully synthetic evidence.

## Entry Gate

Start only with one bounded consequential claim and one of:

- a valid `lat.safety-critical-review.v1` review chain;
- an equivalent public Product Attack Card;
- a fully synthetic replayable hard case.

The hard case should preserve a competent baseline. Ordinary validation, RBAC, logging, retry/timeout, health monitoring, normal failover, and basic typed interfaces should be assumed unless the evidence says otherwise.

If the attack only works because the baseline is obviously naive, stop: it is not an invention signal.

## 1. Prove the hard case

Record:

- load-bearing invariant;
- trigger and preconditions;
- local components that remain correct;
- cross-boundary failure;
- wrong-world physical/operational consequence;
- deterministic oracle;
- replay reference;
- evidence status `OBSERVED / DERIVED / JUDGED / UNKNOWN`.

Prefer the same event trace under baseline and guarded systems. A mechanism should change a consequential decision or outcome, not only produce a nicer explanation.

A non-reproduced hard case cannot advance beyond `candidate` or `insufficient_evidence`.

## 2. Extract the missing technical mechanism

Ask:

> What enforceable mechanism is missing that lets the hard case survive a competent baseline?

A useful candidate names:

- exact identity/state/action inputs;
- enforcement boundary;
- deterministic predicate or state-machine behavior where feasible;
- invalidation, rebinding, reverification, or unknown-outcome semantics;
- observable enforcement/effect receipt;
- safe failure behavior;
- generalization scope and non-goals.

Reject as an invention candidate when the fix is only a UI warning, training, checklist, generic audit, generic RBAC, ordinary retry/timeout, local bug fix, or a new architecture layer with no measurable reduction in wrong-world outcomes.

Such items may remain valuable product-review rules.

## 3. Generalize only the mechanism

Generalization must preserve the technical load-bearing property. Do not inflate a specific failure into an abstract slogan.

Prefer a candidate that can explain at least two plausible contexts, for example:

```text
approved object -> vendor/native execution handle
mission state -> shared physical resource action
authorization -> state-changing actuator
command -> target-specific physical outcome
```

Record which domain adapters change and which mechanism elements remain invariant.

## 4. Commercial-value gate

Every candidate must name:

- customer/operator;
- concrete pain or wrong-world cost;
- measurable outcome the mechanism could improve;
- plausible monetization or product attach point;
- why the customer would adopt/pay instead of relying on existing controls.

Track costs too: false HOLD, latency, availability, operator load, integration complexity, and recovery burden.

Commercial value is a product-priority signal only. It does not increase novelty confidence.

## 5. Counter-control and kill test

Before prior-art research, identify the strongest simpler control that could make the new mechanism unnecessary.

Examples:

- typed IDs plus explicit translation;
- ordinary compare-and-swap/version checks;
- standard transaction or lease semantics;
- existing state-machine isolation;
- read-after-write verification;
- normal revocation propagation;
- generic provenance/audit.

For each candidate define at least one kill criterion.

```text
If a competent baseline with the simpler control passes the identical hard case
without the proposed mechanism,
REJECT the invention candidate.
```

The product-review invariant may remain useful even after the invention candidate is rejected.

## 6. Emit a machine handoff

Use:

```text
schemas/capability/adversarial-innovation-handoff.v1.schema.json
scripts/validate_adversarial_innovation_handoff.py
examples/adversarial-innovation/synthetic-target-binding.innovation-handoff.v1.json
```

Candidate states:

```text
candidate
-> prior_art_pending
-> challenged
-> retain_candidate | reject_*
```

Required handoff content:

- source review/chain lineage;
- replayed hard case;
- missing mechanism;
- commercial value;
- strongest counter-control;
- falsifiers / kill criteria;
- prior-art challenge state and coverage refs;
- strongest counterevidence;
- retain/reject decision and next falsification step.

The validator rejects premature retain states, unknown source-chain lineage, private locators, unsupported absolute IP assertions, and candidates defeated by existing controls or equivalent/broader prior art.

## 7. Prior-art challenger

Route `prior_art_pending` candidates to [Systematic Invention Research](systematic-invention-research-stack.md).

Use multiple public retrieval paths:

- keyword and semantic variants;
- CPC/IPC neighbors;
- backward/forward citations;
- assignee/inventor/family neighborhoods;
- older terminology and neighboring problem formulations;
- public standards, papers, repositories, and product mechanisms.

De-duplicate patent families and inspect independent claims for high-value candidates.

The strongest counterevidence is mandatory. Missing evidence is not counterevidence.

Allowed bounded conclusion:

```text
no equivalent found in bounded search
```

Disallowed absolute/legal conclusions include:

```text
is patentable
is novel
no prior art
FTO clear
non-infringing
```

## 8. Decision rules

### `retain_candidate`

Allowed only when:

- the hard case is reproduced;
- the mechanism is technical and reusable;
- the strongest simpler control does not kill it;
- all current falsifiers survived;
- the commercial-value gate is non-generic;
- the bounded prior-art challenge is complete;
- no equivalent or broader mechanism was found in that bounded search;
- coverage gaps and strongest counterevidence remain visible.

This means only **retain for further patent/research evaluation**.

### `reject_existing_control`

Use when a competent existing control passes the same hard case or makes the proposed mechanism unnecessary.

### `reject_prior_art`

Use when public prior art discloses an equivalent or broader mechanism for the candidate's load-bearing elements.

### `reject_not_reproducible` / `reject_not_commercial`

Use when the product mechanism cannot be demonstrated or when product value remains generic/unmeasurable.

### `insufficient_evidence`

Use when source access, replay fidelity, mechanism evidence, or prior-art coverage is inadequate.

## Portable Agent Skill

Use:

```text
templates/adversarial-innovation-mining-agent-skill/
```

as a runtime-neutral Skill template. The Skill orchestrates the bridge only. It should call or route to the Safety-Critical Product Review and Systematic Invention Research workflows rather than copying their full bodies into one mega Skill.

Keep runtime-specific permissions, tool bindings, and installation details in thin adapters. Prefer native Skill discovery.

## Research discipline

- A high-severity defect is not automatically a valuable invention.
- A commercially valuable mechanism is not automatically novel.
- A new object/graph/AI layer is not innovation unless it changes a measured wrong-world outcome.
- Human approval does not prove downstream identity binding.
- Auditability does not prove prevention.
- Model agreement does not prove novelty.
- One successful synthetic case does not establish downstream adoption or product ROI.
- A prior-art challenger may demote an invention hypothesis while preserving the engineering review rule.

## Stop Conditions

Stop or reject when:

- the public/IP gate fails;
- the consequential claim is not bounded;
- the attack depends on a strawman baseline;
- the hard case cannot be reproduced or evidenced;
- the proposed mechanism is only procedural/local;
- a simpler competent control kills it;
- commercial value cannot be made measurable;
- prior-art coverage is insufficient for the requested research state;
- the request asks for a definitive legal IP conclusion.

A correct output may be `reject` or `insufficient_evidence`.
