# Evidence Wayfinding Reference Workflow

## Purpose

Evidence Wayfinding is a portable reference workflow for moving one bounded decision from uncertainty to a reviewable, evidence-grounded delivery state. It is not a new Lattice module, a mega Skill, or an autonomous research Agent.

The workflow reuses the existing `feature_delivery_case`, `delivery-capability-conductor`, understanding, challenge, judgment, delivery-artifact, outcome-review, and governed-evolution capabilities. Its north star is verified team-usable decisions and artifacts per unit of scarce human attention, subject to correctness, visible unknowns, preserved human authority, and real delivery-state change.

## Blueprint Preservation

The complete 2026-08-07 source blueprint, including the original capability matrix, artifact contracts, claim lifecycle, VDY model, EIR/ECR model, cross-runtime adapter design, rollout roadmap, failure pre-mortem, acceptance criteria, source IDs, and deferred work, is preserved at:

- `docs/evidence-wayfinding/blueprint-preserved.md`
- `docs/evidence-wayfinding/frontier-practice-scout-candidate.md`
- `docs/evidence-wayfinding/runtime-conformance.md`
- `docs/evidence-wayfinding/evaluation-and-evolution.md`

These documents preserve design intent without silently promoting deferred ideas into active capabilities.

### Current implementation decision

`frontier-practice-scout` remains a **candidate, not an active Skill**. Merging the contract phase did not create the second-use / independent-value evidence required by the Direction Investment Gate. Existing capabilities plus on-demand current-source research remain the smaller valid composition until replay or real cases prove a stable, distinct capability boundary.

Do not edit existing generic Skills merely to mention Evidence Wayfinding. Change a Skill only when observed delivery evidence shows a behavior, trigger, output, or authority gap that the workflow contract cannot solve through composition.

## Mission Anchor

Every run carries a short, versioned mission anchor:

```text
goal_id: lat.goal.verified-decision-yield.v1
goal: increase verified, team-usable delivery decisions and artifacts per minute of scarce human attention
non_goals:
  - maximize agent activity, tool count, document count, or autonomy
  - optimize tokens before correctness
invariants:
  - correctness_before_speed
  - visible_unknowns
  - human_authority
  - real_delivery_state_change
  - governed_learning
mutation_rule: human_owner_approval + version_bump
```

New evidence may change claims, route, priority, or plan. It must not silently change goal, scope, authority, or acceptance observer.

## Ordered Workflow

The reference path has stages `0` through `10` (eleven state transitions including orientation and evolution):

| Stage | Action | Minimum artifact | Stop / pass condition |
|---|---|---|---|
| 0 Orient | Freeze one user, one bounded decision, scope, non-goals, deadline, and falsification condition. | Wayfinding Contract | If one `decision_requested` cannot be stated, stop for human clarification. |
| 1 Route | `delivery-capability-conductor` chooses the smallest sufficient capability set. | Route Receipt | Reuse an existing valid artifact instead of repeating work. |
| 2 Sense | Collect bounded project, code, historical decision, and source evidence. | Portable Case Pack | Sources, cutoff, permission gaps, and unknowns are explicit. |
| 3 Model | Build the smallest system slice and evidence-linked claim map needed for the decision. | Evidence Map | Sufficient understanding is reached for the named decision. |
| 4 Challenge | Seek contradictions, counterexamples, hidden dependencies, stale assumptions, and stakeholder surprise. | Challenge Receipt | Strongest counterevidence is explicit. |
| 5 Frontier scan | Search current external primary sources only when a named gap could materially change the decision. | Frontier Evidence Brief | Skip when no decision-changing search question exists. |
| 6 Verify | Prefer deterministic checks, then independent semantic review and accountable human review when required. | Verification Receipt | Applicable verification passes or the run stops/degrades. |
| 7 Decide | Compress the unresolved fork into a bounded human decision. | Decision Strip / Card | A human can decide with minimal sufficient context. |
| 8 Deliver | Produce the team-usable artifact that changes real work state. | Delivery Artifact | Owner and next action are explicit. |
| 9 Settle | Record observed outcome, human corrections, failure points, and remaining unknowns. | Outcome Receipt | Facts, derivations, judgments, and unknowns remain distinct. |
| 10 Evolve | Create candidate improvements with scope, evidence, replay set, holdout evaluation, and rollback conditions. | Evolution Proposal | No promotion without governed review. |

Continuous retries are not the design. Stop after two consecutive rounds with no new evidence, no risk reduction, and no delivery-state change.

## Minimal Capability Composition

Default or conditional reuse:

- Entry and routing: `delivery-capability-conductor`.
- Shared object: `feature_delivery_case`.
- Understanding: `feature-understanding-loop`, `context-mastery`.
- System slice: `system-mental-model`.
- Challenge: `unasked-questions-generator`, `contradiction-adjudication`, `negative-knowledge-pack`.
- Human decision: `decision-question-builder`.
- Delivery projection: `delivery-artifact-builder`.
- Blocked delivery only: `delivery-rescue`.
- Outcome learning: `feature-outcome-review`.
- Reuse candidates after multiple cases: `reusable-delivery-pattern`, `delivery-judgment-playbook`.
- Evolution governance: existing Helixion and capability governance/harness boundaries.

Do not load all of these by default. The active Capability Profile makes only the bounded set available, and the Agent selects the next action.

## Frontier Practice Scout Decision

The current public repository does not yet contain enough second-use evidence to justify promoting a new `frontier-practice-scout` Skill under the Direction Investment Gate. Therefore frontier research remains a workflow stage and a preserved candidate contract, not a new active Skill.

Promotion requires all of the following:

1. at least two real or replayable decision cases where current external primary-source research materially changed the decision or prevented a stale recommendation;
2. a stable input/output boundary distinct from `context-mastery`, `feature-understanding-loop`, and generic web research;
3. a maintainer and review/retirement trigger;
4. trigger and output eval cases showing when the capability must run and when it must be skipped;
5. no automatic write, promotion, or policy authority.

Until then, runtime-specific research remains an on-demand tool action under the active profile and evidence contract.

## Portable Case Pack

Cross-Agent and cross-runtime handoff uses `lat.portable_case_pack.v1` rather than free-form reasoning transcripts. Required fields preserve:

- case and mission identity;
- one bounded decision;
- in-scope and out-of-scope boundaries;
- evidence cutoff;
- observed, derived, judged, and unknown claims;
- conflicts and strongest counterevidence;
- rejected directions and their evidence;
- addressable evidence references;
- source gaps;
- the next named tool task;
- required output contract;
- falsification condition;
- data classification.

The schema is `schemas/capability/portable-case-pack.v1.schema.json`. A public synthetic example is under `examples/evidence-wayfinding/`.

Capability discovery remains native to each receiving workspace. The Portable Case Pack preserves shared semantics; it does not require two runtimes to share a Skill directory, Agent configuration, or discovery mechanism. Google-to-coding conservation and independent verification rules are defined in [Cross-Workspace Handoff](cross-workspace-handoff.md).

### Structural and semantic validation authority

The published Draft 2020-12 schema is the authoritative structural gate for Portable Case Pack v1. It owns required fields, types, enums/constants, `additionalProperties`, nested shape, and declared formats such as `date-time`.

`scripts/validate_portable_case_pack.py` remains the semantic gate for cross-field invariants such as evidence-reference resolution, duplicate identifiers, classification compatibility, observed-claim evidence, and mission/contract rules. It does not replace schema execution.

Run structural validation before semantic validation. Negative mutation fixtures under `tests/fixtures/evidence-wayfinding/invalid/` protect this parity. A derived claim with empty `evidence_refs` remains an explicit v1 semantic-contract decision; do not silently tighten it as part of structural parity work.

## Human Attention Surfaces

Use progressive disclosure:

- **Decision Strip**: 5-10 seconds; one recommendation, decision needed, largest risk, deadline.
- **Decision Card**: 30-60 seconds; two to four comparable options, evidence, unknowns, counterevidence, reversibility.
- **Evidence Map**: 3-5 minutes; claims, evidence chain, conflicts, gaps, system slice.
- **Evidence Pack**: deep read only when needed; primary sources, snapshots, evaluation results, and bounded logs.

Do not use background narrative or method detail as the first human surface.

## Verification and Authority

Evidence priority is:

```text
schema / compiler / static analysis
-> reproduction / target test
-> regression anchors
-> integration or runtime evidence
-> independent semantic review
-> accountable human gate
```

Model agreement is not proof. A model may not self-confirm user-usable delivery, broaden scope, accept material risk, promote a team-wide asset, merge, release, deploy, or change the mission anchor.

## Governed Evolution

Self-improvement means governed capability evolution, not self-rewriting.

```text
failure point or repeated gap
-> evidence-linked candidate
-> replay set
-> holdout / counterexample evaluation
-> human review
-> versioned promotion or rejection
-> rollback condition
```

A single successful case, a persuasive model explanation, token savings, or increased activity is insufficient promotion evidence.

## Public / Private Boundary

Public Lattice contains only the workflow contract, profile template, schema, validator/test logic, synthetic fixtures, and public-safe preservation documents. Real `feature_delivery_case` records, private source references, proprietary evidence, model bindings, observed human feedback, adoption state, and manager-facing business claims remain in downstream private repositories.

## Validation

Run:

```bash
python -m pip install -r requirements-validation.txt
python scripts/validate_capability_profile.py --root .
python -m json.tool schemas/capability/portable-case-pack.v1.schema.json >/dev/null
python -m json.tool examples/evidence-wayfinding/portable-case-pack.synthetic.v1.json >/dev/null
python scripts/validate_json_schema_instance.py \
  schemas/capability/portable-case-pack.v1.schema.json \
  examples/evidence-wayfinding/portable-case-pack.synthetic.v1.json
python scripts/validate_portable_case_pack.py examples/evidence-wayfinding/portable-case-pack.synthetic.v1.json
python -m unittest discover -s tests -p 'test_portable_case_pack_schema.py' -v
python -m unittest discover -s tests -p 'test_evidence_wayfinding.py' -v
```
