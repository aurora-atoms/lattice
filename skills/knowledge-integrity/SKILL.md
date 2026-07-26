---
name: knowledge-integrity
description: Use to select the smallest sufficient capability for decision alignment, contradiction adjudication, assumption expiry, knowledge trust, decision half-life, architecture drift, or future-maintainer intent. Input is a bounded requirement, design, code surface, decision, assumption, knowledge claim, owners, dates, scope, and evidence references; output is a routing decision plus one evidence-linked specialist artifact. Do not use to make unilateral business, architecture, compliance, risk, or ownership decisions; preserve behavior, provenance, uncertainty, review triggers, least privilege, and human authority.
---

# Knowledge Integrity

## Goal

Route a knowledge, decision, or consistency problem to the smallest sufficient specialist so the team knows what to trust, why, within which scope, and when to review it again.

## Use When

Select one primary capability first:

- C01 `decision-alignment-receipt`: decided, not decided, assumed, owner, rationale, and next confirmation point;
- C02 `contradiction-adjudication`: conflicting claims, impact, evidence, adjudicator, and single-source-of-truth recommendation;
- C03 `assumption-expiry-radar`: assumptions at risk from changed evidence, affected areas, and validation;
- C04 `knowledge-trust-assessor`: transparent trust factors, applicability, conflicts, and recommended validation;
- C05 `decision-half-life-review`: continue, revalidate, reopen, or supersede an existing decision;
- C06 `architecture-drift-radar`: compare design intent with current structure and assess cumulative drift;
- C07 `future-maintainer-note`: preserve why a non-obvious choice exists and when it should change.

## Do Not Use When

Do not use for generic summaries, bulk knowledge ingestion, retrieval implementation, automatic source promotion, or unilateral business, architecture, compliance, risk, or ownership rulings.

## Inputs

Require a bounded target object, intended use, source and owner metadata, dates and versions, applicability scope, current evidence, authority boundary, and expected review artifact.

## Outputs

Produce `knowledge-integrity-selection.json`, a concise Markdown companion, and `lat.capability.run_result.v1`.

```text
artifacts/knowledge-integrity/<scope-id>/<run-id>/knowledge-integrity-selection.json
artifacts/knowledge-integrity/<scope-id>/<run-id>/summary.md
artifacts/capability-runs/knowledge-integrity/<run-id>/run-result.json
```

The selection records the chosen capability, trigger evidence, required inputs, gaps, expected artifact, exclusions, optional dependencies, and stop boundary.

## Evidence

Separate facts, inference, conflicts, unknowns, assumptions, and authority. Preserve source, version, observation date, owner, scope, validation state, and superseding evidence. Do not treat document location, recency, code state, or seniority as truth by itself.

## Success Signals

Evaluate each signal as `met`, `not_met`, or `not_evaluated`:

- one smallest sufficient specialist is selected before composition;
- the target object, intended use, scope, and authority are explicit;
- the specialist output is evidence-linked and reviewable;
- decisions, non-decisions, assumptions, conflicts, and unknowns remain distinguishable;
- owner, validation, review, expiry, or reopening conditions are visible;
- human authority is preserved.

## Stop Conditions

Stop at the requested specialist artifact or next reviewable stage. Stop when source access, scope, owner, authority, critical evidence, or validation is unavailable; when high-risk adjudication is required; when one bounded corrective retry fails; or when the goal, stage gate, or user stop condition is reached.

## Workflow

1. Bound the target object, intended use, scope, evidence cutoff, and authority.
2. Query ConPort before loading or searching full Skill text when available; otherwise use targeted authorized sources.
3. Compare the task against C01 through C07 and select one primary capability.
4. Invoke the dedicated specialist.
5. Add another specialist only for a named dependency, conflict, or independent validation gap.
6. Record plausible capabilities and sources intentionally excluded.
7. Stop at the specialist artifact for human review.

## Rules

CCAT.001 | MUST | routing | select one primary capability before composition
CCAT.002 | MUST | specialist | use dedicated C01 through C07 Skills when available
CCAT.003 | MUST | scope | bind analysis to a versioned source intended use and applicability
CCAT.004 | MUST | evidence | expose source owner date scope validation conflicts and uncertainty
CCAT.005 | MUST | lifecycle | preserve review expiry reopening and supersession conditions
CCAT.006 | MUST | human | preserve accountable owner and governance authority
CCAT.007 | SHOULD | token | optimize quality-adjusted token ROI after integrity quality passes
CCAT.008 | SHOULD | prompt | keep routing rules stable and evidence dynamic
CCAT.009 | NEVER | authority | silently replace a decision source of truth or architecture intent
CCAT.010 | NEVER | composition | activate several specialists because selection evidence is weak

## References

- Use `../decision-alignment-receipt/SKILL.md`, `../contradiction-adjudication/SKILL.md`, `../assumption-expiry-radar/SKILL.md`, `../knowledge-trust-assessor/SKILL.md`, `../decision-half-life-review/SKILL.md`, `../architecture-drift-radar/SKILL.md`, or `../future-maintainer-note/SKILL.md`.
- Route knowledge-source governance to `../team-knowledge-plane-governor/SKILL.md` and retrieval implementation to `../hybrid-knowledge-retrieval-builder/SKILL.md`.

## Verification

```bash
python scripts/validate_skill_package.py --root skills/knowledge-integrity
python scripts/validate_capability_context.py --root .
```

## Failure Modes

- category monolith;
- routing by keyword alone;
- black-box trust scoring;
- treating historical decisions as permanent truth;
- resolving contradictions without authority;
- equating architecture drift with automatic failure;
- leaving rationale without review or expiry conditions.
