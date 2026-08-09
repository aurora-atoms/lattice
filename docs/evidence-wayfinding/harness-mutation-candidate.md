# Harness Mutation Candidate — Case 0

## Purpose

This contract is the first governed bridge from a verified Evidence Wayfinding outcome to a future Harness change.

It does **not** make the Harness self-modifying. It records one bounded, expiring, session-local challenger that can be evaluated later under the Promotion Firewall.

The source sequence is:

```text
Outcome Receipt
-> earliest failure point
-> one mutation target
-> session-local Harness Mutation Candidate
-> representative / hard / reserved blind evaluation
-> human decision
-> optional scoped canary
```

Only the first four steps are implemented by this change.

## Source case

```text
case_id = synthetic/evidence-wayfinding-schema-parity-case-0
candidate_id = hmc.case0.contract-parity-verifier
status = session_local_candidate
```

The source Outcome Receipt identifies the earliest failure as:

```text
verification stage:
CI validated schema-document syntax but did not execute
schema-instance conformance.
```

That failure is classified as:

```text
verification_gap
```

The permitted primary mutation target is therefore:

```text
verifier_change
```

The candidate does not also change routing, prompts, tools, schema semantics, Skills, or evaluation rules.

## Failure-point taxonomy

The initial taxonomy is intentionally small and maps observed failure to the first mechanism that should be tested.

| earliest failure | candidate target |
| --- | --- |
| required context or rule was not selected | `context_selection_change` |
| Senior was asked a low-value question | `attention_gate_change` |
| wrong Skill/tool path was selected | `routing_change` or `tool_surface_change` |
| repeated analysis produced no new evidence | `stop_rule_change` |
| a fluent conclusion escaped without target-related verification | `verifier_change` |
| a historical rule remained active after it became stale | `knowledge_freshness_change` |
| the same scoped delivery defect repeats across cases | `skill_or_rule_candidate` |
| an evaluator is too permissive | `eval_change` |

The mapping is enforced by `scripts/validate_harness_mutation_candidate.py`. A candidate cannot use an unrelated failure category as justification for changing another mechanism.

## Candidate delta

### Incumbent

```text
schema document is valid JSON
-> handwritten semantic validator
-> acceptance
```

### Challenger

```text
schema document is valid
-> authoritative schema-instance conformance
   - known-valid fixture
   - bounded negative fixtures
-> handwritten semantic validator
-> acceptance
```

The hypothesis is narrow: the challenger should detect contract/runtime parity failures earlier without creating valid-case regressions or confusing semantic failures with structural failures.

The PR does not activate this challenger as a team default. The Case 0 fix already repaired Portable Case Pack parity directly; this candidate tests whether the **verification pattern** deserves reuse elsewhere.

## One-primary-delta rule

`mutation` contains exactly one `mechanism` and one `primary_delta`.

The schema rejects extra mutation fields. The semantic validator additionally checks that the selected mechanism is compatible with the classified earliest failure.

This prevents an apparent improvement from simultaneously changing prompt, routing, tools, schema, verifier, and evaluator so that the cause of improvement cannot be identified.

## Evaluation allocation

The candidate freezes an evaluation plan but does not claim evaluation success.

```text
representative
  missing required audience

hard
  derived Claim without evidence:
  structural schema accepts the shape,
  Attention Admission must still BLOCK it

counterexample
  known-valid minimal Portable Case Pack

reserved
  external case with evaluator-only oracle
```

The candidate therefore remains:

```text
evaluation_plan.status = blocked_pending_reserved_oracle
```

### Why the reserved oracle is not committed here

A public repository cannot honestly claim a blind reserved evaluation when both proposer and evaluator can read the committed oracle.

The public contract records:

```text
case_ref = downstream://reserved/...
oracle_ref = withheld://reserved/...
oracle_visibility = evaluator_only
candidate_author_can_view_reserved_outcome = false
```

A real downstream or controlled evaluation environment must supply the frozen reserved case and oracle. Until then the candidate cannot be described as blind-evaluated and cannot proceed to a scoped canary.

This preserves the public/private boundary instead of creating a fake holdout.

## Protected metrics

A challenger is not allowed to win because it is faster, shorter, or cheaper while quality degrades.

The minimum protected set is:

```text
critical_false_ready
= 0 allowed regressions

authority_drift
= 0 allowed regressions

private_to_public_leakage
= 0 allowed regressions
```

Optional additional protection can include unsupported claims and conflict escape.

Token, latency, tool count, or attention savings do not override these correctness boundaries.

## Human ownership and expiry

Every candidate requires:

```text
owner
version
created_at
expires_at
rollback trigger
action
revalidation plan
```

The Case 0 candidate expires after 30 days if it has not been evaluated or renewed deliberately.

Expiry prevents one local failure diagnosis from becoming an immortal pseudo-rule.

## Promotion Firewall

The candidate hard-codes:

```text
automatic_promotion_allowed = false
team_available_allowed = false
human_owner_required = true
reserved_non_regression_required = true
live_case_required_before_team_available = true
```

A valid candidate is therefore **not** a promoted capability.

The only allowed later evaluation decisions are:

```text
reject
revise
continue_shadow
scoped_canary
```

A later PR may implement a blind challenger/incumbent evaluation protocol. Team-level promotion remains outside this contract and requires a separate human-owned decision with version, scope, canary, and rollback.

## What this PR does not do

It does not:

- create a new Lattice module;
- create or modify an active Skill;
- build a generic mutation generator;
- automatically synthesize negative tests for arbitrary schemas;
- activate the Case 0 challenger in default routing;
- provide a public fake reserved oracle;
- run a blind incumbent/challenger benchmark;
- grant `team_available`;
- merge, release, deploy, or modify production behavior.

## Validation

```bash
python scripts/validate_json_schema_instance.py \
  schemas/capability/harness-mutation-candidate.v1.schema.json \
  examples/evidence-wayfinding/case-0-schema-parity/harness-mutation-candidate.json

python scripts/validate_harness_mutation_candidate.py \
  examples/evidence-wayfinding/case-0-schema-parity/harness-mutation-candidate.json \
  examples/evidence-wayfinding/case-0-schema-parity/outcome-receipt.json \
  examples/evidence-wayfinding/case-0-schema-parity/portable-case-pack.json

python -m unittest discover -s tests -p 'test_harness_mutation_candidate.py' -v
```
