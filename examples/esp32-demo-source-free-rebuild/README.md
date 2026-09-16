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

## Boundary

This package contains:

- one public rebuild contract;
- one JSON Schema;
- one semantic validator;
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

schemas/downstream/
  esp32-demo-rebuild-contract.v1.schema.json

scripts/
  validate_esp32_demo_rebuild_contract.py

tests/
  test_esp32_demo_rebuild_contract.py
```

## What is frozen

The contract freezes only behavior that a downstream implementation must preserve:

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
Treat the contract as the behavior authority.
Do not request or use any original implementation source, private repository history,
private runtime evidence, or company-internal material.
You may choose implementation language, frameworks, file layout, classes, and internal
algorithms freely unless the contract explicitly constrains observable behavior.
Do not invent missing behavior. If the contract is insufficient, stop and identify the
smallest missing contract fact.
Implement only the baseline-required acceptance cases. Keep
single-target-silence-recovery classified as the next required DEFERRED case unless a
separate explicit contract change authorizes implementation.
Do not claim PHYSICAL_READY from software tests.
```

This prompt is intentionally short because the contract carries the stable context.

## Validation

Run:

```bash
python scripts/validate_esp32_demo_rebuild_contract.py
python -m unittest discover -s tests -p 'test_esp32_demo_rebuild_contract.py' -v
```

The validator checks both JSON Schema and load-bearing semantics.

Negative tests reject, among other things:

- changing actual state from accepted telemetry to Controller targets;
- moving formation planning into ESP32 responsibility;
- allowing Browser UI to render Controller targets as actual state;
- weakening Geo camera complete-coverage or mid-route reacquisition rules;
- promoting the deferred silence/recovery case without an explicit contract change;
- silently adding a new scenario or acceptance case;
- claiming source code or private repository coordinates are included;
- claiming this artifact proves legal clean-room status.

## Readiness boundary

Passing this contract proves only that a new implementation is a `SOFTWARE_PARITY_CANDIDATE` against the public behavioral specification.

It does not prove:

- target-board execution;
- intended-screen visual acceptance;
- repeat-run physical reliability;
- real product detection quality;
- permission to use or distribute any separate source code;
- legal clean-room status.

Those require separate evidence and authority.
