# ESP32 Demo Source-Free Rebuild Contract

## Purpose

This public example preserves the minimum machine-readable behavior needed to rebuild a synthetic ESP32 swarm demo without copying or depending on the original implementation source.

The target is behavioral compatibility, not source compatibility.

A presentation/evidence addendum defines the audience-facing continuous-mission demo and a screenshot-only Playwright evidence boundary. The rebuild contract remains authoritative for telemetry truth, role ownership, lifecycle, session, and Geo semantics.

## Boundary

This package contains:

- one public rebuild contract;
- one presentation/evidence addendum;
- JSON Schemas for both contracts;
- semantic validators;
- public mutation tests.

It intentionally does **not** contain original source code, original repository coordinates/history, private CI/telemetry/screenshots/runtime evidence, or company-internal material.

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

## Core truth contract

The core rebuild contract freezes these load-bearing boundaries:

- Controller intent is separate from ESP32 execution;
- accepted ESP32 telemetry is the only actual displayed state;
- Operator and Drone are independent telemetry entities;
- readable run-scoped identity rotates on Start;
- WF / BT / WB emission classification is separate from UDP/WiFi telemetry transport;
- freshness is per entity;
- stale / last-known / source-disconnected states remain distinct;
- Geo observation uses accepted telemetry and cannot lock from stale pre-Geo or partial entity coverage;
- single-target silence/recovery remains the next required deferred scenario until downstream implementation evidence exists.

## One continuous mission

The presentation is **one swarm completing one mission**, not a playlist of unrelated test cases.

The roster is created once at mission start. Later stages inherit the previous stage's last accepted telemetry. The demo must not restart, rotate runtime identity, reseed the swarm, or reset config between stages.

```text
multi-point takeoff
-> ASMR-like Stroke Drawing
-> interrupt one active stroke
-> recover the same Drone and continue the stroke
-> one Drone lands / another disappears while airborne
-> duplicate signal + shared-Remote-ID identity conflict
-> Geo coast patrol
-> Phoenix
-> distributed landing
```

Landed or disconnected Drones remain part of mission history but leave the active-flying subset. Later stages use the remaining active members.

## ASMR-like Stroke Drawing

`ASMR-like` describes the visual feel. `Stroke Drawing` is the implementation contract.

The Controller precomputes ordered strokes and continuous 3D waypoints. The same airborne swarm traces those strokes over time instead of snapping directly into a final formation.

```text
precomputed ordered strokes
        -> time-ordered 3D waypoints
        -> same mission Drones
        -> accepted ESP32 telemetry
        -> telemetry-derived visual trail
```

The visual trail may use accepted telemetry history, but it must never invent missing motion.

Therefore, when a Drone is silenced during an active stroke:

- peers continue drawing;
- the silent Drone keeps its last-known point;
- the trail must not visually bridge the unobserved interval as if it were observed;
- recovery uses the same runtime Drone ID, config, and board boot identity;
- the remaining stroke continues without respawning the swarm;
- the missing interval is not rewritten as observed telemetry.

This makes the visual effect useful for assurance: an interrupted stroke becomes a human-readable representation of a telemetry interruption without allowing the UI to fabricate continuity.

## 3D shape / horizontal projection rule

All formations remain genuinely 3D, but the **XY horizontal projection must still be clearly recognizable** so the simulated source state can be compared directly with a planar product map.

The design rule is:

```text
3D formation
  = recognizable XY shape signature
  + Z-axis depth variation
```

not:

```text
unrecognizable XY overlap
  + Z separation that is required to understand the shape
```

Concretely:

- the top-down XY projection is the primary visual signature for comparison;
- altitude may add depth, layering, or 3D structure but must not be the only reason the formation is recognizable;
- ignoring Z must not destroy the essential outline or key distinguishing features;
- projected self-overlap must not collapse important parts of the figure into an ambiguous cluster;
- ASMR Stroke Drawing paths must remain legible in XY even while their Z values vary;
- Phoenix must keep a recognizable Phoenix silhouette from above;
- a 3D Right Square Pyramid must still present a clear square-base footprint with the apex projecting near the intended center rather than degenerating into an unreadable point cloud.

This rule exists specifically because the comparison surface on the real product may be a 2D map. The 3D source geometry should add information without making the 2D comparison harder.

## Phoenix boundary

Phoenix is retained and now appears **inside the same mission** after Geo coast patrol and before distributed landing.

Its role is `mission_climax_showcase`:

- it uses the remaining active members of the same swarm;
- the transition from patrol to Phoenix is continuous in 3D;
- its XY projection remains recognizable from a planar/top-down view;
- it may still be run independently as a showcase;
- it is not, by itself, product validation proof.

## Playwright boundary

Playwright is screenshot-only evidence capture.

At each mission checkpoint:

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

The combined side-by-side screenshot is the required checkpoint evidence. Both panels must
appear in the same capture frame with a visible shared run clock and checkpoint ID. Separate
panel captures are supplemental diagnostics only; they cannot replace the combined frame.

Playwright must not:

- read product DOM state as semantic evidence;
- inspect product APIs, WebSocket payloads, or network payloads;
- derive an automated product pass/fail verdict;
- mutate the product to make a checkpoint pass;
- mutate simulator truth to match product output.

Screenshots are evidence, not ground truth. Pixel/image diff is not an authoritative product verdict. Real product screenshots and runtime evidence remain private/downstream.

## Visual-first, log-confirmed evidence

The demo is intentionally smaller than a human-factors study. It may claim only that a
correct visual divergence was noticed before raw-log confirmation in one recorded run.

Three checkpoints carry this proof burden:

- one Drone becomes silent during an active stroke;
- one Drone lands while another disappears airborne;
- multiple truth entities claim one Remote ID.

At each checkpoint, the observer first reviews the unannotated side-by-side view. The
observer's first-notice time and interpretation are frozen before raw logs are opened.
Annotations may be added only after that record is frozen. The downstream evidence record
then links the same stimulus, combined screenshot, visual observation, and later log
confirmation under one run and checkpoint identity.

The downstream record stays private and must include enough identity and timing metadata to
attest that the source state and product view concern the same delivered stimulus. The public
contract does not contain product payloads, private screenshots, or product interfaces.

This bounded evidence may not be generalized into a claim that visual comparison is always
superior to log analysis.

## Proof versus showcase

Stroke interruption/recovery, landing-versus-disconnect, and identity conflict form the
proof segment. Geo patrol, Phoenix, and distributed landing form the showcase outro. The
outro completes the same continuous mission but must not be reported as product-validation
evidence.

## Identity stress semantics

Two related but different conditions remain separate while using the same mission roster:

```text
duplicate observation:
  many observations -> one existing simulated truth entity

shared Remote ID conflict:
  multiple existing truth entities -> one claimed Remote ID
```

Runtime Drone identity remains the simulated truth-entity identity. A claimed Remote ID is test stimulus and must not change or collapse mission truth entities.

## Minimal Agent instruction

```text
Implement the ESP32 synthetic swarm demo described by rebuild-contract.v1.json.
Treat the core contract as the authority for truth, telemetry, role, lifecycle, session,
and Geo semantics.

Use presentation-evidence-addendum.v1.json for one continuous mission. Create the swarm
roster once, preserve config/runtime identity between stages, and continue each stage from
the previous stage's last accepted telemetry.

Use ASMR-like Stroke Drawing: Controller-owned ordered strokes -> continuous 3D waypoints
-> accepted ESP32 telemetry -> telemetry-derived visual trail. Do not snap directly to a
final formation and do not draw motion that was not observed in accepted telemetry.
A silence fault occurs during an active stroke; recovery continues the same Drone and the
same unfinished stroke.

For every 3D formation, keep the XY/top-down projection clearly recognizable. Z may add
depth but must not be required to identify the shape. Do not allow projected overlap to
destroy key silhouette features. This rule applies to Stroke Drawing, Phoenix, the Right
Square Pyramid, and other 3D formations used for planar comparison.

Keep the visual comparison left=Simulated Source State and right=Real Product.
Playwright is screenshot-only. Capture both panels in one required combined frame with a
visible shared run clock and checkpoint ID; separate panel captures are supplemental only.
Do not use DOM/API/WebSocket/network inspection as semantic evidence and do not generate an
automated product verdict.

For the three proof checkpoints, freeze the observer's unannotated visual interpretation
before opening raw logs. Preserve a private downstream record tying the same delivered
stimulus, combined screenshot, visual notice time, interpretation, and log confirmation to
one run/checkpoint. Claim only what that recorded run demonstrates.

After identity/lifecycle stress, continue the same active swarm into Geo coast patrol,
then form Phoenix as the mission climax, then land the remaining active Drones at distributed
points. Phoenix is visually important but is not validation proof by itself.

Do not request or use original implementation source, private repository history, private
runtime evidence, or company-internal material. Preserve the existing baseline acceptance
cases. Implement and validate single-target-silence-recovery as the first new scenario gate
before activating later new presentation stages. Do not claim PHYSICAL_READY or real-product
detection quality from software contracts or screenshots alone.
```

## Validation

Run:

```bash
python scripts/validate_esp32_demo_rebuild_contract.py
python scripts/validate_esp32_demo_presentation_evidence_addendum.py
python -m unittest discover -s tests -p 'test_esp32_demo_rebuild_contract.py' -v
python -m unittest discover -s tests -p 'test_esp32_demo_presentation_evidence_addendum.py' -v
```

The validators reject, among other things:

- Controller targets becoming displayed actual state;
- Browser UI inventing missing motion;
- resetting or respawning a new swarm between presentation stages;
- an instant final formation replacing Stroke Drawing;
- a 3D formation whose identity depends on Z-only separation;
- a top-down projection that loses the key shape signature;
- a visual trail bridging an unobserved interval as observed motion;
- changing runtime identity during recovery;
- allowing identity stress to rewrite the mission truth roster;
- moving Phoenix out of the continuous mission or treating it as validation proof;
- using Playwright DOM/API/WebSocket/network inspection as semantic evidence;
- allowing screenshot/pixel diff to become an automatic product verdict;
- replacing a combined same-frame comparison with separately timed panel screenshots;
- opening raw logs or highlighting the fault before the visual observation is frozen;
- omitting downstream attestation that both sides concern the same delivered stimulus;
- generalizing one recorded run into universal visual superiority;
- reporting the Phoenix showcase outro as product-validation evidence;
- committing private runtime screenshots to this public package.

## Readiness boundary

Passing these contracts proves only contract conformance and software parity against the
public specification. `CONTRACT_VALID` does not mean runtime evidence was captured. Runtime
capture does not mean a human reviewed it. Human review does not automatically confirm a
product issue. Target-board execution, intended-screen visual acceptance, repeat-run
physical reliability, and real product detection quality require separate downstream
evidence and authority.
