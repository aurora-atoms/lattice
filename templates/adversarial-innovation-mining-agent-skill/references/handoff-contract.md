# Adversarial Innovation Handoff Contract

Use this reference when converting a safety-critical review finding into an invention-research candidate.

## Boundary

The safety review remains authoritative for the product finding and release gate. The invention handoff is a separate research artifact and MUST NOT revise the underlying safety verdict.

## Required lineage

Every candidate must link to one or more source review chains or equivalent public/synthetic hard-case records. Preserve the replay reference and evidence cutoff.

## Candidate state

```text
CANDIDATE
-> PRIOR_ART_PENDING
-> CHALLENGED
-> RETAIN_CANDIDATE | REJECT
```

Do not skip from a product defect directly to `RETAIN_CANDIDATE`.

## Mechanism test

A candidate mechanism must answer:

1. What cross-system invariant fails?
2. What exact boundary permits the failure?
3. What new or differently composed technical mechanism would enforce the invariant?
4. Why does a competent baseline not already provide an equivalent control?
5. What replayable trace shows a different consequential result with the mechanism enabled?
6. What simpler control would kill the need for the mechanism?

## Commercial-value test

Record customer, pain, measurable outcome, monetization/attach point, and adoption reason. Reject generic claims such as "improves safety" unless they are tied to a measurable operational state change.

## Prior-art handoff

Route surviving candidates to a public-only prior-art workflow. Preserve:

- query/retrieval coverage;
- patent-family de-duplication;
- independent-claim evidence for high-value families;
- strongest equivalent or broader mechanism found;
- alternate terminology and classification search;
- coverage gaps.

The allowed terminal language is bounded research language, e.g. `no equivalent found in bounded search`; never convert this to an absolute novelty or legal conclusion.
