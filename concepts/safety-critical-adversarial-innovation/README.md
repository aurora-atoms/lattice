# Safety-Critical Adversarial Innovation

## Use this concept when

A public or fully synthetic product question spans all or part of this chain:

```text
Safety-Critical Product Review
  -> Adversarial Innovation Mining
  -> Systematic Invention Research
```

The concept exists so an unfamiliar agent does not need to infer that chain from `docs/`, `schemas/`, `scripts/`, `templates/`, `tests/`, and CI files.

Do not use the whole composition when only one bounded stage is needed:

- release/safety review only -> start at Safety-Critical Product Review;
- reproduced mechanism gap that needs innovation mining -> start at Adversarial Innovation Mining;
- an already bounded public invention candidate that only needs prior art -> start at Systematic Invention Research.

## Agent quickstart

1. Read `concept.json` only to understand stage relationships and artifact-loading rules.
2. Select the current stage from the evidence already available.
3. Read that stage's reference workflow.
4. Do not load validator source, tests, or CI into normal model context.
5. When a structured artifact is required, load its schema and execute the named validator.
6. Follow the next-stage handoff only when the handoff evidence condition is satisfied.

### Stage 1 - Safety review

Start here when no valid review record exists.

```text
entrypoint: docs/safety-critical-product-review.md
output:     lat.safety-critical-review.v1
```

The stage answers whether a competent system can still reach a consequential wrong-world result and what invariant, enforcement, evidence, test, and release gate are required.

### Stage 2 - Innovation mining

Start here when a competent-baseline hard case is already reproduced or strongly evidenced and the question is whether the gap reveals a reusable technical mechanism.

```text
entrypoint: docs/adversarial-innovation-mining.md
output:     lat.adversarial-innovation-handoff.v1
```

The stage must preserve customer pain, measurable value, strongest simpler counter-control, kill criteria, and uncertainty. A severe defect is not automatically an invention candidate.

The portable Skill under `templates/adversarial-innovation-mining-agent-skill/` is optional runtime packaging. The concept does not make that template an active Lattice Skill.

### Stage 3 - Prior-art research

Start here when the handoff is valid and prior-art work remains.

```text
entrypoint: docs/systematic-invention-research-stack.md
output:     bounded prior-art challenge + retain/revise/reject research state
```

This stage remains separate because a bounded search is evidence, not a legal patentability, novelty, FTO, or infringement conclusion.

## Loading model

```text
LOAD INTO TASK CONTEXT
  current stage entrypoint
  current bounded evidence

LOAD ONLY WHEN OUTPUT REQUIRES IT
  schema
  portable Skill template
  synthetic example

EXECUTE, DO NOT NORMALLY LOAD
  deterministic validator

NEVER BY DEFAULT
  validator implementation as prose context
  tests
  CI YAML
  unrelated stage bodies
```

## Authority

This composition is navigation and handoff metadata. It does not override the authority of any referenced workflow or contract, does not alter a safety release verdict, does not create a new product module, and does not establish legal IP conclusions.
