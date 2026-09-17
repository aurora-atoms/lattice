# ESP32 Demo Source-Free Rebuild Contract

## Purpose

This public example preserves the minimum machine-readable behavior needed to rebuild a synthetic ESP32 swarm demo without copying or depending on the original implementation source.

It exists to reduce repeated reasoning and token cost during a downstream reimplementation.

The target is:

```text
public behavior contract
        -> source-isolated implementation Agent
        -> new implementation
        -> acceptance tests
```

The target is **behavioral compatibility**, not source compatibility.

A presentation/evidence addendum now also defines the intended audience-facing demo sequence and a screenshot-only Playwright evidence boundary. It extends presentation behavior only; the rebuild contract remains authoritative for telemetry truth, role ownership, lifecycle, session, and Geo semantics.

## Boundary

This package contains:

- one public rebuild contract;
- one presentation/evidence addendum;
- JSON Schemas for both contracts;
- semantic validators;
- public mutation tests.

It intentionally does **not** contain:

- original source code;
- original repository coordinates or history;
- private CI, telemetry, screenshots, or runtime evidence;
- company-internal code, interfaces, documents, data, tickets, logs, architecture, or credentials.

The term "source-free rebuild" is technical workflow language only. This package does not establish a legal clean-room conclusion, ownership determination, open-source permission, patent conclusion, or employer-IP conclusion.

## Direction Fit

Primary value path: `strategic_asset`.

The bounded value is preserving expensive reasoning as a small executable contract so a later Agent can reconstruct the demo without reconstructing the full conversation or implementation history.

This is not a new Skill, Agent, orchestration layer, or generic application-rebuild platform.

## Files

```text
examples/esp32-demo-source-free-rebuild/
  README.md
  rebuild-contract.v1.json
  presentation-evidence-addendum.v1.json

schemas/downstream/
  esp32-demo-rebuild-contract.v1.schema.json
  esp32-demo-presentation-evidence-addendum.v1.schema.json

scripts/
  validate_esp32_demo_rebuild_contract.py
  validate_esp32_demo_presentation_evidence_addendum.py

tests/
  test_esp32_demo_rebuild_contract.py
  test_esp32_demo_presentation_evidence_addendum.py
```

## What is frozen by the core rebuild contract

The core contract freezes only behavior that a downstream implementation must preserve:

- Controller intent is separate from ESP32 execution;
- accepted ESP32 telemetry is the only actual displayed state;
- Operator and Drone are independent telemetry entities;
- readable run-scoped identity rotates on Start;
- WF / BT / WB emission classification is separate from UDP/WiFi telemetry transport;
- protocol semantics and session lifecycle are preserved;
- freshness is per entity;
- stale / last-known / source-disconnected states remain distinct;
- Geo observation camera acquisition cannot use stale pre-Geo or partial entity coverage;
- refresh or Operator reselection during patrol reacquires near the current path segment;
- fixed-camera one-second visible-motion acceptance is preserved;
- the current baseline scenarios remain bounded;
- single-target silence/recovery remains the next required but deferred scenario.

## Presentation and screenshot evidence addendum

The addendum defines an audience-facing main sequence without changing the core truth contract:

```text
multi-point takeoff
-> perfect progressive drawing
-> single-target silence/recovery
-> landing vs airborne disconnect
-> duplicate-observation dedup
-> shared-Remote-ID identity conflict
-> Geo visible patrol
-> distributed landing
```

The sequence is deliberately progressive: first establish an intuitive normal motion baseline, then introduce controlled failure or ambiguity, then return to a recognizable geospatial motion pattern before landing.

`single-target-silence-recovery` remains the first new scenario gate. The addendum does not claim that the deferred case has already been implemented or validated. Later new stages activate only after that first gate passes in the downstream implementation.

### Phoenix boundary

Phoenix remains a supported formation and may still be run as a standalone showcase.

It is intentionally **not** part of the main demo sequence, not the theme of the evidence story, and not validation proof. Removing Phoenix is also not required.

### Playwright boundary

Playwright is screenshot-only evidence capture.

At each named checkpoint the presentation uses the same visual structure:

```text
LEFT:  Simulated Source State
       browser rendering of accepted ESP32 telemetry only

RIGHT: Real Product
       real product UI
```

Allowed Playwright behavior is limited to:

- capture the left panel;
- capture the right panel;
- capture the combined side-by-side view;
- record checkpoint identity and capture time.

Playwright must not:

- read product DOM state as semantic evidence;
- inspect product APIs, WebSocket payloads, or network payloads;
- derive an automated product pass/fail verdict;
- mutate the product to make a checkpoint pass;
- mutate simulator truth to match product output.

Screenshots are evidence, not ground truth. Pixel/image diff is not an authoritative product verdict. Real product screenshots and runtime evidence remain private/downstream and are not committed to public Lattice.

### Identity stress semantics

Two cases that can look similar are deliberately kept separate:

```text
duplicate observation:
  many observations -> one simulated truth entity

shared Remote ID conflict:
  multiple simulated truth entities -> one claimed Remote ID
```

The simulated truth entity is identified by its runtime Drone identity. A claimed Remote ID is test stimulus and must not by itself collapse distinct simulated truth entities. The addendum does not prescribe how the real product must resolve an identity conflict; it records the real product UI by screenshot for later review.

## What may be rewritten

A downstream implementation may independently choose:

- programming language;
- web/server framework;
- directory and module layout;
- classes and function names;
- internal abstractions;
- internal algorithms that do not change observable behavior;
- wire encoding, provided both rebuilt endpoints implement the required protocol semantics.

A new implementation should usually be smaller than the source from which the behavior was originally learned. Reproducing internal structure is not a goal.

## Minimal Agent instruction

A downstream Agent can be given only this public package and the following instruction:

```text
Implement the ESP32 synthetic swarm demo described by rebuild-contract.v1.json.
Treat the core contract as the authority for truth, telemetry, role, lifecycle, session,
and Geo semantics.

Use presentation-evidence-addendum.v1.json for the staged audience-facing demo and
visual evidence plan. Playwright is screenshot-only: do not use DOM/API/WebSocket/network
inspection as semantic evidence and do not generate an automated product verdict.
Keep the visual comparison left=Simulated Source State and right=Real Product.

Phoenix remains available only as a separate showcase and does not enter the main demo
sequence or validation proof.

Do not request or use any original implementation source, private repository history,
private runtime evidence, or company-internal material.
You may choose implementation language, frameworks, file layout, classes, and internal
algorithms freely unless the contracts explicitly constrain observable behavior.
Do not invent missing behavior. If the contracts are insufficient, stop and identify the
smallest missing contract fact.

Preserve the existing baseline acceptance cases. Implement and validate
single-target-silence-recovery as the first new scenario before activating the later new
presentation stages. Do not claim that a deferred scenario passed until downstream
evidence exists.
Do not claim PHYSICAL_READY or real-product detection quality from software contracts or
screenshots alone.
```

This prompt is intentionally short because the contracts carry the stable context.

## Validation

Run:

```bash
python scripts/validate_esp32_demo_rebuild_contract.py
python scripts/validate_esp32_demo_presentation_evidence_addendum.py
python -m unittest discover -s tests -p 'test_esp32_demo_rebuild_contract.py' -v
python -m unittest discover -s tests -p 'test_esp32_demo_presentation_evidence_addendum.py' -v
```

The validators check both JSON Schema and load-bearing semantics.

Negative tests reject, among other things:

- changing actual state from accepted telemetry to Controller targets;
- moving formation planning into ESP32 responsibility;
- allowing Browser UI to render Controller targets as actual state;
- weakening Geo camera complete-coverage or mid-route reacquisition rules;
- silently claiming deferred silence/recovery is already implemented;
- using Playwright DOM/API/WebSocket/network inspection as product semantic evidence;
- allowing screenshot or pixel diff to become an automatic product verdict;
- moving Phoenix into the main evidence sequence;
- conflating duplicate observations with multiple truth entities sharing one Remote ID;
- committing private runtime screenshots to this public package;
- claiming source code or private repository coordinates are included;
- claiming this artifact proves legal clean-room status.

## Readiness boundary

Passing the core rebuild contract proves only that a new implementation is a `SOFTWARE_PARITY_CANDIDATE` against the public behavioral specification.

Passing the presentation addendum proves only conformance to the staged demo/evidence contract. It does not prove the real product passed any scenario.

Neither contract proves:

- target-board execution;
- intended-screen visual acceptance;
- repeat-run physical reliability;
- real product detection quality;
- permission to use or distribute any separate source code;
- legal clean-room status.

Those require separate downstream evidence and authority.
