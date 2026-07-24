---
name: delivery-capability-conductor
description: use for routing a Feature Delivery Case to the smallest necessary public Lattice delivery skill or agent based on role, lifecycle stage, state change, evidence, permissions, and desired visible outcome; do not use to execute production changes, approve releases, make business or compliance decisions, evaluate personnel, or invoke the entire capability catalog by default; input is a Feature Delivery Case, task request, role, stage, event, available evidence, capability registry, and permission boundary; output is a bounded routing decision, selected capability chain, required context, stop conditions, human confirmations, evidence expectations, and write-back plan that preserves behavioral constraints, least privilege, explicit uncertainty, delivery value, and quality-adjusted token ROI.
---

# Delivery Capability Conductor

## Goal
Route a Feature Delivery Case to the minimum capability set that can produce the requested visible delivery outcome.

## Use When
Use for feature-delivery routing across understanding, kickoff, implementation, review, release, outcome, and learning stages. Use when a user should not need to know the full skill catalog.

## Do Not Use When
Do not use for direct production writes, release approval, business commitments, compliance rulings, personnel scoring, or unrelated generic orchestration. Do not activate all skills or agents for completeness.

## Inputs
Required: request or state change, current role, lifecycle stage, available evidence, permissions, desired outcome, and current Feature Delivery Case when available.

Optional: capability registry records, prior routing history, domain context index, risk signals, and token budget.

## Outputs
Produce:

```text
route_status = routed | needs_input | human_decision_required | complete
selected_capabilities = ordered minimal skill/agent ids
selection_reason = direct visible outcome and evidence fit
required_context = bounded files, records, symbols, tests, risks, evidence refs
human_confirmations = approvals or decisions that cannot be delegated
stop_conditions = explicit reasons to halt
write_back = Feature Delivery Case fields or candidate records to update
uncertainty = facts, inferences, unknowns
```

## Workflow
1. Identify the user role and requested state change.
2. Identify lifecycle stage: understand, prepare, implement, review, release, outcome, or learn.
3. Classify the dominant condition: blocked, unknown, conflicting, risk accumulating, decision needed, communication needed, or complete.
4. Query ConPort before loading or searching the full skill text when ConPort is available; then query the capability registry before loading full capability instructions.
5. Select the smallest capability that can create a direct, verifiable result.
6. Add a second capability only when its output is a required input or quality gate for the first.
7. Load only the required Domain Context and least-privilege tools.
8. Define evidence expected from each capability and the condition for continuing.
9. Stop for missing evidence, conflicting sources, high-risk actions, or required human judgment.
10. Write facts, inferences, unknowns, artifacts, and next actions back to the Feature Delivery Case.
11. End when the requested visible result is reached; do not expand the chain for catalog coverage.

## Rules
DCC.001 | MUST | unit | route around the Feature Delivery Case | enforce
DCC.002 | MUST | selection | choose the smallest capability set for a direct visible outcome | enforce
DCC.003 | MUST | evidence | separate fact, inference, and unknown, and require source refs | enforce
DCC.004 | MUST | context | load a task-scoped context pack instead of a raw repository or catalog dump | enforce
DCC.005 | MUST | registry | query the capability registry before full skill loading | enforce
DCC.006 | MUST | control | preserve human decisions for business, compliance, security, architecture, and release | enforce
DCC.007 | MUST | stop | stop when input or permission is insufficient or the goal is reached | enforce
DCC.008 | MUST | writeback | emit a Feature Delivery Case write-back plan | enforce
DCC.009 | SHOULD | token | optimize quality-adjusted token ROI | prefer
DCC.010 | SHOULD | cache | keep routing rules in a stable prefix and case material in the dynamic suffix | prefer
DCC.011 | NEVER | catalog | invoke the entire capability tree by default | block
DCC.012 | NEVER | authority | approve delivery, merge, release, or production change | block
DCC.013 | NEVER | people | use routing telemetry for personnel ranking | block
DCC.014 | NEVER | certainty | convert unverified inference into fact | block

## Reference Routing
The hard routing, evidence, authority, and stop rules are defined above. Read `references/routing-map.md` only for detailed role-stage-condition examples. Read `references/output-contract.md` only when producing a machine-checkable routing record.

## Verification
Verify:

```text
- one dominant requested outcome is identified
- selected capabilities are necessary and ordered
- no unrelated skill or agent is activated
- required context is bounded
- facts, inferences, and unknowns are separated
- human decisions and approvals are explicit
- stop conditions are present
- Feature Delivery Case write-back is defined
- stable routing rules remain separate from dynamic case context
```

Run repository validation when available:

```bash
python scripts/validate_skill_package.py --root skills/delivery-capability-conductor
python scripts/estimate_skill_tokens.py --root skills/delivery-capability-conductor
```

## Failure Modes
- Selecting a broad pack when one atomic skill is sufficient.
- Treating orchestration as authority to approve or execute high-impact actions.
- Loading full repositories, logs, or capability catalogs into prompt context.
- Routing from role labels alone without lifecycle state and evidence.
- Continuing after the requested visible result has already been produced.
- Hiding uncertainty or conflicting evidence to make the route appear complete.
