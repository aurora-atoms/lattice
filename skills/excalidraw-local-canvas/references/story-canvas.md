# Zoomable Story Canvas Design

Use this reference when the user wants one large Excalidraw canvas rather than traditional slides.

## Canvas Anatomy

```text
[global frame]
  center: core thesis
  ring 1: main narrative regions
  ring 2: evidence, examples, screenshots, tradeoffs
  bottom/right edge: next actions or decision request
```

Recommended region count:

- 1 center thesis.
- 4 to 7 main regions.
- 2 to 5 local details per region.

## Standard Canvas Spec

```markdown
# Canvas Spec

Audience:
Goal:
Sensitivity level:
Allowed sources:
Disallowed sources:

## Global thesis
<one sentence>

## Regions
### Region 1: <name>
Purpose:
Key message:
Visual elements:
Evidence:
Speaker notes:

## Zoom path
1. Start at global overview.
2. Zoom into <region> to explain <point>.
3. Return to global thesis.
4. Zoom into <region> to show <evidence>.
5. End at next actions.

## Export targets
- editable: .excalidraw
- review: pdf
- sharing: png/svg
```

## Layout Guidance

- Left: context, background, problem.
- Center: thesis, operating model, core frame.
- Right: future state, solution, decision.
- Top: strategic drivers, why now.
- Bottom: implementation, risks, next steps.

Use nested frames:

- Outer frame: full story.
- Region frames: major topics.
- Detail frames: screenshots, examples, evidence.

Use visual hierarchy:

- Big text for thesis and region titles.
- Medium text for key messages.
- Small text only for local evidence; never for required reading at full zoom.

## Talk Track Pattern

For each zoom stop:

1. Orient: where are we on the canvas?
2. Claim: what is the point of this region?
3. Evidence: what supports it?
4. Implication: why does it matter?
5. Return: how does it connect back to the global thesis?

## Anti-Patterns

Avoid:

- Slide-by-slide numbering.
- Dense workflow diagrams as the main story.
- Too many arrows crossing the whole canvas.
- Tiny text that is impossible to navigate.
- Raw customer screenshots or internal logs.
- Making the canvas the system of record for sensitive source data.
