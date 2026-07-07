---
name: excalidraw-local-canvas
description: Create, maintain, render, repair, and govern public-safe local-first Excalidraw story-canvas artifacts while preserving existing canvas behavior, source boundaries, and export paths. Use when the user wants a secure zoomable presentation, `.excalidraw` JSON source file, canvas spec, Docker Desktop or self-hosted Excalidraw workflow, local setup command, export path, privacy review, or AI-tool-to-canvas workflow. The output can be a `.excalidraw` file, canvas spec, Docker Desktop setup, export instruction, project wrapper, or security review. Do not use for ordinary slide decks, unrelated drawing tools, cloud-only whiteboards for confidential material, or artifacts requiring raw secrets, regulated data, unrestricted logs, or unsupported private dumps.
---

# Excalidraw Local Canvas

## Goal

Create local-first Excalidraw story canvases: one macro canvas, local detail zones, explicit zoom path, controlled exports, and clear data-boundary decisions.

Prefer concrete artifacts over advice when the user asks to create or update a canvas.

## Use When

Use this skill for:

- Creating or updating `.excalidraw` source files.
- Turning a topic, repo, research loop, or architecture into a zoomable story canvas.
- Repairing Excalidraw JSON while preserving existing layout and element behavior.
- Running Excalidraw with Docker Desktop, Docker Compose, local Node/Yarn, or a self-hosted static client.
- Reviewing privacy, company-boundary, and sharing risks before using online whiteboards or exports.
- Creating canvas specs, talk tracks, prompt templates, and local project wrappers.

## Do Not Use When

Do not use this skill for ordinary Marp/Slidev/PowerPoint slide decks unless the user explicitly asks to convert a canvas into slides. Do not use it for unrelated diagram formats when Mermaid, Figma, HTML, or static SVG is the better target. Do not send confidential, restricted, credential, raw-log, HR/legal/M&A, or regulated material to online Excalidraw or prompt contexts. Do not replace an existing canvas layout wholesale when a scoped repair is requested.

## Inputs

Expected inputs include topic notes, source summaries, repo docs, existing `.excalidraw` JSON, desired audience, canvas goal, security boundary, local Excalidraw repo path, export target, or runtime preference.

If details are missing, make conservative placeholders marked `TODO` unless missing sensitivity or export boundary would make the artifact unsafe.

## Outputs

Prefer concrete artifacts:

- Editable `.excalidraw` JSON files.
- Canvas specs and zoom paths.
- Local project wrappers.
- Docker Desktop, Docker Compose, or local Node/Yarn setup commands.
- Export instructions for PNG, SVG, PDF, or HTML embedding.
- Security and sharing review notes.

For existing canvases, preserve element IDs, layout intent, zoom path, and user-authored text unless the user asks for a redesign.

## Core Rule

Do not default to traditional slide decks. When the user asks for a presentation in this context, produce or maintain a zoomable story-canvas specification unless they explicitly ask for slides.

Use this model:

```text
sources -> sanitized notes -> canvas spec -> .excalidraw source -> exported png/svg/pdf -> presentation or recording
```

## Workflow

1. Classify content sensitivity.
2. Choose runtime: online Excalidraw for low-sensitivity work, Docker Desktop/self-hosted for local confidential workflows, local development repo for app customization.
3. Create or update artifacts. Use `scripts/create_excalidraw_canvas_project.sh` for a repeatable folder wrapper.
4. Create the story map before drawing. Use `references/story-canvas.md`.
5. Give setup commands only after choosing runtime. Use `references/local-docker.md`.
6. Run security review before sharing. Use `references/security.md`.

## Docker Desktop Quick Start

Use Docker Desktop when the user wants local Excalidraw without installing the Node/Yarn development toolchain.

Published image path:

```bash
docker pull excalidraw/excalidraw:latest
docker run --rm --name local-excalidraw -p 5000:80 excalidraw/excalidraw:latest
```

Open:

```text
http://localhost:5000
```

Docker Compose path:

```yaml
services:
  excalidraw:
    image: excalidraw/excalidraw:latest
    ports:
      - "5000:80"
    restart: unless-stopped
```

Run:

```bash
docker compose up -d
docker compose logs -f excalidraw
docker compose down
```

Build from local source only when the user needs local Excalidraw source changes:

```bash
cd /path/to/excalidraw
docker build -t local-excalidraw .
docker run --rm --name local-excalidraw -p 5000:80 local-excalidraw
```

Self-hosting the Excalidraw client does not automatically provide Excalidraw+ features, share links, cloud storage, or real-time collaboration. Export `.excalidraw` source files into the project directory.

## Excalidraw File Rules

When generating `.excalidraw` directly:

- Write JSON with top-level `type: "excalidraw"`, `version`, `source`, `elements`, `appState`, and `files`.
- Use simple primitives first: `frame`, `rectangle`, `text`, `arrow`, `line`, `ellipse`, and `diamond`.
- Give every element a stable unique `id`, numeric bounds, `version`, `versionNonce`, `seed`, `updated`, `groupIds`, `frameId`, `boundElements`, `link`, and `locked`.
- For text, include `fontSize`, `fontFamily`, `text`, `originalText`, `textAlign`, `verticalAlign`, `containerId`, `lineHeight`, and `autoResize`.
- Avoid embedding raw private screenshots or full source dumps. Use labels, bounded summaries, placeholders, or separately reviewed image assets.
- Validate generated files with `python3 -m json.tool <file>` and a lightweight structural check before returning.

## Verification

Before returning:

- Confirm the canvas is local-first and does not contain secrets, raw logs, credentials, or unrestricted private dumps.
- Confirm the `.excalidraw` file parses as JSON and has non-empty `elements`.
- Confirm generated exports are separated from editable source.
- Confirm Docker Desktop instructions include port, URL, stop command, and the self-hosting caveat.
- If a local Excalidraw source repo is provided, prefer its format conventions and run commands from that repo only when needed.

## Failure Modes

Watch for:

- Producing a slide deck when the request needs a zoomable canvas.
- Creating invalid `.excalidraw` JSON or omitting required element fields.
- Embedding raw screenshots, secrets, credentials, logs, or private source dumps.
- Treating browser local storage as durable source control.
- Mixing company, personal, customer, or tenant boundaries in one canvas.
- Exporting reviewed and unreviewed content into the same shareable artifact.
- Replacing existing canvas structure instead of making a scoped edit.
- Making tiny text that is unreadable at the intended zoom stop.

## Resources

- `references/story-canvas.md`: spatial presentation design, canvas region model, zoom-path template, prompt templates.
- `references/local-docker.md`: local Excalidraw, Docker Desktop, Docker Compose, export, and version-control workflow.
- `references/security.md`: company usage risks, data classification, account boundaries, AI prompt safety, sharing/export controls.
- `scripts/create_excalidraw_canvas_project.sh`: creates a local project wrapper for Excalidraw canvas work.
