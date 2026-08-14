---
name: recurrence-guard
description: Use for reviewing a code change against a small repository-local catalog of evidence-backed known failure patterns and returning a short BLOCK, WARN, UNKNOWN, or NO_KNOWN_MATCH result. Input is the current diff, relevant code, and guard catalog; output is a read-only finding with evidence and exceptions. Do not use for broad code review, implementation advice, architecture design, or quality approval.
---

# Recurrence Guard

## Goal

Prevent repeat failures without pretending to know the best implementation. The skill only identifies documented directions that should not be repeated when the current change matches a known failure pattern.

Optimize for precision over recall. A missed unknown risk is preferable to repeated false alarms that cause developers to ignore the guard.

## Use When

Use when a developer asks whether the current change repeats a known failure, historical regression, false-ready state, weakened verification, or another repository-local prohibited pattern with evidence.

## Do Not Use When

Do not use for general code review, design recommendations, code generation, architecture selection, merge approval, release approval, or claims that a change is safe or correct.

## Inputs

Load only what is necessary:

1. Current diff or changed files.
2. Minimum surrounding code needed to test guard applicability.
3. `.github/skills/recurrence-guard/guards.example.jsonl` for this public example, or a repository-local `guards.jsonl` created by a downstream adopter.
4. Referenced evidence only for guards that might apply.

Do not load unrelated repository history or a broad knowledge base.

## Outputs

Return the result inline. Use exactly one of these outcomes:

- `BLOCK`: an active blocking guard directly matches, required evidence is available, and no exception applies.
- `WARN`: a candidate guard or lower-confidence historical pattern may apply, but it cannot justify blocking.
- `UNKNOWN`: the guard might apply, but scope, evidence, or exception status cannot be established.
- `NO_KNOWN_MATCH`: no active or candidate guard matches the inspected change. This is not a quality approval.

For `BLOCK` or `WARN`, include only:

```text
<OUTCOME> — <guard id>: <title>
Current change: <what matched>
Why it applies: <applicability condition>
Evidence: <evidence refs>
Known exception: <exception or none known>
Boundary: This finding does not recommend an alternative implementation or approve overall quality.
```

## Workflow

1. Identify the changed components and change kinds.
2. Select only guard entries whose scope could plausibly match.
3. For each selected guard, verify the prohibited change and applicability condition against current evidence.
4. Check documented exceptions before raising a finding.
5. Enforce lifecycle:
   - `candidate` may produce `WARN` or `UNKNOWN`, never `BLOCK`.
   - `active` may produce `BLOCK` only when evidence and applicability are established.
   - `retired` does not participate in review.
6. Prefer a single load-bearing finding. Add a second finding only when it is independent and similarly high confidence.
7. If evidence is missing, stop at `UNKNOWN` instead of inferring.
8. If nothing matches, return `NO_KNOWN_MATCH` and the fixed non-approval boundary.

## Rules

RG.001 | MUST | evidence | require evidence before a blocking finding
RG.002 | MUST | lifecycle | allow only active guards to block
RG.003 | MUST | exception | test documented exceptions before reporting a match
RG.004 | MUST | precision | prefer high precision over broad speculative coverage
RG.005 | MUST | boundary | report prohibited directions without recommending an implementation
RG.006 | MUST | authority | never treat no known match as quality approval
RG.007 | SHOULD | context | inspect only the smallest context needed to establish applicability
RG.008 | SHOULD | output | keep findings short and evidence linked
RG.009 | NEVER | invention | invent a guard evidence reference incident or local rule
RG.010 | NEVER | action | edit code approve merge release deploy or expand permissions

## Evidence

Treat current diff or code inspection as facts only when directly observed. Treat guard applicability as an inference that must cite the observed change and guard conditions. Keep assumptions visible. If a required fact is unavailable, mark the result `UNKNOWN`. Never convert uncertainty into a blocking result.

Public example evidence uses `synthetic://` references and is not authoritative for a downstream repository. A real repository should replace example entries with locally approved evidence locators that remain within that repository's IP and access boundary.

## Success Signals

- `met`: a replay that should block is blocked for the documented reason, and a similar-but-safe replay does not trigger.
- `not_met`: a false positive, unsupported block, implementation recommendation, or incorrect exception handling occurs.
- `not_evaluated`: the guard has not been replayed against a representative positive and negative case.

The first team-use success signal is not catalog size. It is a second developer using the guard without special coaching and finding the result useful in a real change.

## Stop Conditions

Stop and return `UNKNOWN` when required evidence or permission is missing. Stop when the current change falls outside all guard scopes. Stop rather than expanding into broad security, privacy, compliance, architecture, or product-risk review. Stop after the goal of classifying known recurrence risk is met; do not continue into implementation advice.

## Verification

Validate the public example catalog and replay set:

```bash
python .github/skills/recurrence-guard/scripts/validate_catalog.py
```

For a downstream repository with real evidence:

```bash
python .github/skills/recurrence-guard/scripts/validate_catalog.py \
  --catalog .github/skills/recurrence-guard/guards.jsonl \
  --authoritative
```

Replay at least one expected `BLOCK`, one expected `NO_KNOWN_MATCH`, one exception case, and one insufficient-evidence case before team rollout.

## Failure Modes

- Calling a stylistic preference a historical failure.
- Turning a candidate lesson into a hard blocker.
- Blocking because a file path matches while the applicability condition does not.
- Ignoring a documented exception.
- Producing a long generic risk list instead of a precise evidence-backed finding.
- Recommending the replacement design after identifying what should not be repeated.
- Saying `PASS`, `safe`, `correct`, or `ready` when no known guard matches.
