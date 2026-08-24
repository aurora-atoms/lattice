# Safety-Critical Product Review

## Decision

Use one evidence-linked review record to connect each consequential requirement to the cross-system invariant that prevents harm, the exact enforcement point, runtime proof, an adversarial test, a multi-axis failure classification, and a fail-closed release recommendation.

```text
Requirement
-> Cross-System Invariant
-> Architecture / Code Enforcement Point
-> Runtime Evidence
-> Adversarial Test
-> Failure Classification
-> Release Gate
```

This is a public Lattice reference workflow and machine contract. It is not a new Skill, Agent, module, safety case, regulatory interpretation, certification standard, or release authority. Use the existing Senior Attention entry and select only the smallest relevant capability for the current gap.

## Direction Fit

```text
primary_value_path: current_product_delivery
direction_verdict: bind_to_delivery
beneficiary: downstream safety-critical feature owner and accountable safety or release authority
observable_state_change: a prose safety claim becomes a reviewable requirement-to-gate chain with explicit gaps and a deterministic release recommendation
verification: JSON Schema validation, semantic gate validation, negative conformance tests, and one downstream review against real authorized evidence
existing_capability_gap: existing Lattice capabilities discover context, risk, contradictions, and decisions, but do not define this safety-specific trace and fail-closed gate contract
current_evidence: two user-supplied draft standards, public official reference sources, and synthetic conformance only
unknown: downstream domain applicability, regulatory interpretation, product evidence, independent reviewer acceptance, and operational value
next_use: one private downstream feature_delivery_case with an accountable safety owner
maintenance_owner: Lattice capability governance owner for the public contract; downstream safety owner for each real review
```

`bind_to_delivery` is deliberate. The public contract is only useful when a private downstream team applies it to a bounded consequential action and supplies real requirements, code, tests, telemetry, owners, hazards, and authority.

## Source Evaluation

Two user-supplied draft standards were evaluated outside the public repository. Their strongest common contribution is the invariant-based chain above, especially the competent-baseline principle, identity and state-transition attacks, separation of command acknowledgement from physical outcome, and deterministic replay.

The longer engineering draft is stronger on concrete identity, concurrency, common-mode, action-conditioned-state, test-oracle, and kill-test mechanics. The v1 review draft is stronger on the compact operating chain, joint-validity witnesses, lifecycle and cross-workflow composition, negative evidence, and evidence terminology. Neither is sufficient as a general safety-engineering or certification standard: they do not establish a complete hazard-analysis method, assurance independence, configuration-control regime, development-assurance level, tool qualification, operational safety case, or jurisdiction-specific compliance path. The Lattice artifact is therefore named and scoped as a product-review workflow, not an engineering or certification standard.

The drafts required these corrections before becoming a Lattice contract:

1. Replace competing `P0-P3` and `S0-S4` scales with separate axes for severity, evidence status, reproducibility, finding status, and release impact. Priority is not severity.
2. Treat absent load-bearing evidence as a release blocker, not a neutral `UNKNOWN` verdict.
3. Require the input requirement to be evaluated and normalized before tracing it. A detailed but unapproved requirement cannot support release.
4. Make the chain many-to-many through stable IDs. A requirement may support several invariants, and one invariant may be enforced at several boundaries.
5. Require evidence from the actual enforcement decision and relevant postcondition. Logs reconstructed after the fact do not prove prevention.
6. Constrain adversarial testing to an authorized, isolated environment. This workflow grants no permission to probe a live system or create a physical effect.
7. Make `CONDITIONAL` unavailable for open catastrophic or critical findings. A risk acceptance does not turn an invariant violation into passing evidence.
8. Keep the automated result at `pass_candidate`; only the accountable downstream human may decide release.
9. Bind each invariant to an intended use, operating context, excluded use, consequential action, and harm; a technically precise control without a hazard boundary is not a safety claim.
10. Require mapping to applicable domain regulations, standards, assurance plans, configuration management, independence, and tool qualification. This generic contract does not replace them.

## Entry Contract

Start only when the review has:

- one bounded product or feature and one consequential action;
- intended use, operating context, excluded use, and evidence cutoff;
- the human roles that own the requirement, safety judgment, and release decision;
- authorized, addressable source references;
- an identified test environment that cannot create unapproved harm;
- an applicability owner for external regulatory and certification obligations.

If the target is still broad, use `domain-context-pack` or `feature-understanding-loop` to bound it. Use `unasked-questions-generator` for a named review gap, `contradiction-adjudication` for conflicting evidence, `risk-ahead` for one preventive-risk question, and `decision-question-builder` for one human decision. Do not load all of them by default.

## 1. Requirement Evaluation

Preserve the original requirement through an addressable `source_ref`; do not copy private source material into public Lattice. Evaluate whether the requirement can be satisfied while the real-world result is unsafe.

An effective consequential requirement must identify:

```text
WHEN <trigger>
GIVEN <state, identity, authority, evidence, and version context>
THE SYSTEM SHALL <deterministic behavior>
BEFORE / UNTIL <time or state constraint>
AND SHALL EMIT <observable enforcement and outcome evidence>
AND SHALL NOT <unsafe fallback, transfer, replay, retry, or success attribution>
```

It must also name the acceptance observer, authority owner, ambiguity behavior, stale-state behavior, unknown-outcome behavior, cancellation or partial-failure semantics, lifecycle termination, and safe state. Use `accept`, `amend`, `reject`, or `unknown` for the evaluation verdict. Only an `approved` normalized requirement can support a non-blocking release recommendation.

Reject or amend the requirement if a competent implementation could satisfy its words while violating a catastrophic or critical invariant.

## 2. Cross-System Invariant

State the property that must remain true across component, identity, time, authority, workflow, and physical-world boundaries. Bind it to the harm or hazard it prevents.

Common invariant families include:

- approved physical target equals actuated physical target;
- all action predicates share a coherent state cut or joint validity witness;
- authorization remains valid for the exact action, object, purpose, policy, and state at execution;
- state or identity translation is invalidated after material handoff, split, merge, restart, reacquisition, or source change;
- transport acknowledgement, device acknowledgement, physical state, outcome attribution, and mission result remain distinct;
- unknown physical outcome is not converted into failure, success, or blind retry;
- residual physical effects survive administrative closure until reconciled;
- two locally valid workflows cannot create an unsafe combined state over a shared resource;
- absence is action-grade evidence only when coverage, health, and detection capability support it;
- probabilistic advice cannot bypass a deterministic consequential-effect boundary.

Record applicability explicitly. `not_applicable` requires a product-specific rationale and review owner; it is not a shortcut around missing evidence.

## 3. Architecture / Code Enforcement Point

Name the smallest exact boundary that prevents or contains the violation. A diagram, checklist, UI confirmation, or audit-only event is not an enforcement point.

Each point records:

- stable locator to the architecture decision, interface, function, policy, configuration, or broker;
- identity and state versions consumed;
- deterministic predicate or state-machine transition enforced;
- credential and authority owner;
- failure behavior such as `HOLD`, `DENY`, `REBIND`, `REAUTHORIZE`, `VERIFY`, `TRANSFER`, or `ESCALATE`;
- owner role and version or commit under review.

Prefer typed identities, explicit binding objects, versioned immutable snapshots, compare-and-swap preconditions, one-shot capabilities, conflict-aware reconciliation, and structured effect receipts where the product semantics justify them. The contract requires the mechanism and evidence, not a particular implementation pattern.

## 4. Runtime Evidence

Runtime evidence must show what the enforcement point actually decided and, when relevant, what physical or operational postcondition was observed. It must not rely solely on API success or a human-readable log line.

Record:

- evidence type and producer;
- addressable source reference;
- event time, observation time, ingestion time, sequence or state version, and clock assumptions as applicable;
- target, authority, action, binding, and policy lineage;
- expected signal and actual observation status;
- retention and integrity protection;
- independence and common-mode dependencies;
- contradiction, supersession, and late-correction behavior.

Use `observed`, `planned`, `missing`, or `contradicted`. A load-bearing record with planned, missing, stale, or contradicted runtime evidence cannot be `pass_candidate`.

## 5. Adversarial Test

Test the transition or composition while keeping local components plausibly correct. Each load-bearing invariant requires at least one L3 system-composition or L4 adversarial-invariant test.

Record:

- competent baseline controls assumed present;
- preconditions and bounded attack surface;
- one identity, time, authority, state, retry, outcome, lifecycle, coverage, or composition mutation;
- externally meaningful wrong-world outcome;
- deterministic oracle and expected safe response;
- test result and evidence reference;
- replay fixture;
- execution-safety controls.

Tests run only in an authorized simulator, test bench, digital twin, sandbox, or otherwise controlled environment. Stop when a test could affect a live person, vehicle, device, mission, facility, production service, or third-party asset without explicit authority and domain safety controls.

## 6. Failure Classification

Classify separate axes; never compress them into one score.

### Severity

- `S0 catastrophic`: wrong physical target or action, unauthorized irreversible effect, loss of control, death or serious injury potential, or equivalent intolerable harm.
- `S1 critical`: invariant violation plausibly capable of serious safety, security, privacy, or mission harm but bounded recovery may remain.
- `S2 major`: stale-state, traceability, reconciliation, or verification failure that prevents reliable action-grade use.
- `S3 moderate`: degraded availability, observability, recovery, or excessive false hold without demonstrated high-severity consequence.
- `S4 minor`: non-load-bearing documentation, UI, ergonomics, or maintainability defect.

### Evidence and disposition

- evidence status: `OBSERVED`, `DERIVED`, `JUDGED`, or `UNKNOWN`;
- reproducibility: `deterministic`, `intermittent`, `not_reproduced`, or `unknown`;
- finding status: `open`, `contained_pending_verification`, `verified_closed`, or `accepted_exception`;
- failure mode: product-specific category such as wrong-target, stale-state, authority drift, duplicate effect, outcome misattribution, unsafe composition, or audit gap.

Human risk acceptance remains visible as `accepted_exception`; it does not change the severity or count as verified closure.

## 7. Release Gate

The validator emits a recommendation, not a release decision.

### `block`

Use when any of these is true:

- a normalized load-bearing requirement is not approved;
- an applicable invariant lacks an exact enforcement point, observed runtime evidence, or passed L3/L4 adversarial test;
- an S0 or S1 finding is not `verified_closed`, including an accepted exception;
- identity, state, authority, or outcome ambiguity can fail open;
- a required external obligation is pending or applicability is unknown;
- a blocking unknown, contradiction, unsafe test boundary, or stale evidence remains.

### `conditional`

Allowed only when there is no block condition and every open S2 has a bounded compensating control, accountable owner, expiry, operational observability, and retest reference. Conditional release remains a human decision and must expire.

### `pass_candidate`

Allowed only when all mandatory chain checks pass, all S0/S1 findings are verified closed, no open S2 remains, and required external obligations are mapped. Open S3/S4 items remain visible with owners. `pass_candidate` is not certification, regulatory approval, safety approval, deployment approval, or release authorization.

No aggregate score can override a mandatory gate.

## Artifact Contract

Use:

```text
schemas/capability/safety-critical-review.v1.schema.json
scripts/validate_safety_critical_review.py
examples/safety-critical-review/synthetic-target-binding.review.v1.json
```

A real downstream record belongs beside its private `feature_delivery_case`, for example:

```text
artifacts/safety-critical-reviews/<case-id>/<review-id>/review.v1.json
artifacts/capability-runs/<selected-capability>/<run-id>/run-result.json
```

Keep public fixtures at `simulation_status=synthetic_reference` and `downstream_adoption_status=not_observed`. Public schema or validator success proves contract conformance only.

Validate with:

```bash
python scripts/validate_safety_critical_review.py \
  examples/safety-critical-review/synthetic-target-binding.review.v1.json
python -m unittest tests.test_safety_critical_review -v
python scripts/validate_capability_manifest.py --root .
python scripts/validate_public_private_boundary.py --root .
```

## External Assurance Boundary

Before using this workflow for a real product, the accountable downstream owner must identify applicable jurisdictional, sector, safety, security, quality-system, and certification obligations. Useful public starting points include:

- [NASA System Safety](https://sma.nasa.gov/sma-disciplines/system-safety) for system-safety lifecycle concepts and handbook references;
- [FAA AC 20-115D](https://www.faa.gov/regulations_policies/advisory_circulars/index.cfm/go/document.information/documentID/1032046) for one accepted airborne-software compliance means and its recognized assurance supplements;
- [NIST SP 800-160 Vol. 1 Rev. 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) for trustworthy systems security engineering across the lifecycle;
- [ISO 26262-9:2018](https://www.iso.org/standard/68391.html) as one automotive functional-safety analysis reference whose scope is explicitly domain-specific;
- [FDA Digital Health Guidances](https://www.fda.gov/medical-devices/digital-health-center-excellence/guidances-digital-health-content) for current medical-device software guidance routing;
- [NIST AI RMF 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10) when AI risk is material, without treating that voluntary framework as product authorization.

This list is illustrative, not complete or automatically applicable. Record exact version, applicability, owner, and mapping status in the private review. Obtain qualified legal, regulatory, safety, security, and certification review where required.

## Public / Private Boundary

Public Lattice owns this generic workflow, schema, validator, synthetic fixture, routing metadata, and conformance tests.

Private downstream repositories own real requirements, source paths, architecture, code, hazards, telemetry, incidents, adversarial traces, owner identities, risk acceptances, regulatory mappings, safety cases, release decisions, and operational outcomes. Do not place the supplied draft files, local file paths, private product facts, or real test traces in public Lattice.

## Stop Conditions

Stop at the review record and deterministic recommendation. Stop sooner for missing permission, source access, safety owner, release authority, applicable-obligation owner, test isolation, required evidence, or a high-risk human decision. Do not bypass a block by weakening the requirement, invariant, oracle, severity, evidence status, or test.
