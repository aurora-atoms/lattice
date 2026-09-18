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

The visual trail may use accepted telemetry history, but it must never invent missing motion. When a Drone is silenced during an active stroke, peers continue drawing, the silent Drone keeps its last-known point, and the trail must not bridge the unobserved interval as if it were observed. Recovery uses the same runtime Drone ID, config, and board boot identity and continues the unfinished stroke.

## 3D shape / horizontal projection rule

All formations remain genuinely 3D, but the **XY horizontal projection must still be clearly recognizable** so the simulated source state can be compared directly with a planar product map.

```text
3D formation
  = recognizable XY shape signature
  + Z-axis depth variation
```

The top-down XY projection is the primary visual signature. Z may add depth or layering but must not be required to identify the shape. Projected self-overlap must not destroy key features. This applies to Stroke Drawing, Phoenix, Right Square Pyramid, and other 3D formations.

## Phoenix boundary

Phoenix appears inside the same mission after Geo coast patrol and before distributed landing. It uses the remaining active members and transitions continuously in 3D. Its XY projection must remain recognizable. Phoenix is a visual climax, not product-validation proof by itself.

## Playwright boundary: separate browser pages

The real product is a **separate browser page/window** from the simulated source view. Therefore the contract does not require an impossible same-frame browser screenshot.

At each checkpoint:

```text
Browser/page A                    Browser/page B
Simulated Source State            Real Product
        |                              |
        +---- screenshot A             +---- screenshot B
                  \                    /
                   \-- timing/pairing-/
                           |
                           v
                side-by-side composition
```

Playwright is still screenshot-only. It may:

- capture the source page;
- capture the real-product page;
- record checkpoint ID and both capture times;
- record capture-time skew/pairing metadata;
- compose the already captured images side by side **without semantic mutation**.

The composed image is a presentation artifact, not a claim that both pages were captured in one instant. The downstream record must attest that both captures concern the same delivered stimulus.

Playwright must not:

- read product DOM state as semantic evidence;
- inspect product APIs, WebSocket payloads, or network payloads;
- derive an automated product pass/fail verdict;
- mutate product or simulator state to manufacture a match;
- suppress, add, remove, or alter product-native alerts/highlights during composition.

## Visual discovery, log confirmation

The proof model is intentionally simple:

```text
side-by-side visual comparison
        ↓
human identifies a divergence
        ↓
freeze the observation
        ↓
raw log independently confirms or refutes it
```

**Logs are confirmation, not a deliberately delayed speed competitor.** This demo does not claim that visual comparison is faster than log analysis. A separate controlled experiment would be required for that claim.

The proof checkpoints are:

- one Drone becomes silent during an active stroke;
- one Drone lands while another disappears airborne;
- duplicate observations of one existing truth entity;
- multiple existing truth entities claim one Remote ID.

Before the visual observation is frozen, the test harness may not add a fault arrow, annotation, circle, label, or other clue that tells the observer where the problem is. This restriction does **not** apply to the real product's own native alert, marker change, LOST state, identity warning, or highlight. Those are part of the product behavior and must remain visible and unmodified.

After the observation is frozen, test-added annotation may be used to explain the finding.

The private downstream evidence record is deliberately small. It records the run/checkpoint/stimulus identity, left and right screenshot references with pairing metadata, same-stimulus attestation, the frozen visual observation, and the log evidence/confirmation.

The permitted claim is bounded to:

> A visual divergence was identified and independently confirmed by logs in the same recorded run.

It does not establish general visual superiority, visual-versus-log speed advantage, or product detection quality from screenshots alone.

## Proof versus showcase

Stroke interruption/recovery, landing-versus-disconnect, duplicate observation, and identity conflict form the proof segment. Geo patrol, Phoenix, and distributed landing form the showcase outro. The outro completes the same continuous mission but must not be reported as product-validation evidence.

## Identity stress semantics

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

Use ASMR-like Stroke Drawing with Controller-owned ordered strokes, continuous 3D waypoints,
accepted ESP32 telemetry, and telemetry-derived trails. Never invent missing motion.
Keep every 3D formation recognizable in its XY/top-down projection.

The Simulated Source State and Real Product run in separate browser pages. Capture each page
separately, record both capture times and their skew, then compose the captured images side
by side without semantic mutation. Do not pretend the composition is a same-frame capture.
Playwright remains screenshot-only; do not inspect DOM/API/WebSocket/network data.

For proof checkpoints, let the observer see the unmodified product UI, including any native
alerts/highlights. Do not add test annotations before the visual observation is frozen.
Then use raw logs only to independently confirm or refute the frozen visual finding. Do not
claim that visual comparison is faster than log analysis from this workflow.

Continue the same swarm into Geo coast patrol, Phoenix, and distributed landing. Phoenix is
a showcase climax, not validation proof by itself.
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

- using Controller targets as displayed actual state;
- Browser UI inventing missing motion;
- resetting or respawning the swarm between stages;
- a 3D formation whose identity depends on Z-only separation;
- requiring a false same-frame screenshot across separate browser pages;
- failing to record capture pairing/skew;
- semantically changing either screenshot during side-by-side composition;
- test-added fault highlighting before the observation is frozen;
- suppressing or altering product-native alerts/highlights;
- treating log confirmation as evidence that visual comparison is faster;
- omitting duplicate-signal from the proof checkpoints;
- using Playwright DOM/API/WebSocket/network inspection as semantic evidence;
- reporting the showcase outro as product-validation evidence.

## Readiness boundary

Passing these contracts proves only contract conformance and software parity against the public specification. `CONTRACT_VALID` does not mean runtime evidence was captured. Runtime capture does not mean a human reviewed it. Human review does not automatically confirm a product issue. Target-board execution, intended-screen visual acceptance, repeat-run physical reliability, and real product detection quality require separate downstream evidence and authority.
