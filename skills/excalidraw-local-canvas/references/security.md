# Security and Company Use Review

Use this reference when Excalidraw, NotebookLM, ChatGPT, Claude Code, or similar tools touch company material.

## Data Classification

| Category | Examples | Handling |
|---|---|---|
| Public | public docs, blogs, public screenshots | online tools acceptable |
| Low internal | training notes, generic process | Workspace tools usually acceptable |
| Confidential | roadmap, customer references, architecture, usage analytics | prefer local/self-hosted; sanitize before AI |
| Restricted | credentials, raw logs, regulated data, HR/legal/M&A | do not place in canvas or prompts |

## AI Prompt Safety

- Prefer sanitized summaries over raw documents.
- Replace customer names, domains, emails, account IDs, tenant IDs, internal URLs, and credentials with placeholders.
- Ask AI to generate a canvas spec, talk track, or visual hierarchy, not to ingest raw sensitive sources.
- Review generated output before export.

## Online Whiteboard Risks

For online Excalidraw, tldraw, Prezi, Canva, Gamma, or similar tools, check:

- Can anyone with the link access it?
- Are external users allowed?
- Are exports detached from access control?
- Is there SSO, admin control, audit log, retention, and DLP?
- Does the company allow this tool for the data class involved?

If these answers are unknown, use local Excalidraw or a sanitized canvas.

## Local-First Rules

- Use local Docker Desktop or local development for confidential diagrams.
- Save `.excalidraw` source files in a private repository or approved storage.
- Put raw notes in `private/` and exclude them from Git.
- Export only reviewed PNG/SVG/PDF versions.
- Do not assume browser local storage is compliant durable storage.

## Pre-Share Checklist

1. Search visually for customer references, emails, account IDs, internal URLs, tickets, screenshots, keys, or tokens.
2. Zoom into small text and screenshot corners.
3. Confirm the export belongs to the correct account or repo.
4. Confirm no hidden raw source file is bundled with the export.
5. Label the artifact: public, internal, confidential, or restricted.
6. Share through the approved channel for that label.
