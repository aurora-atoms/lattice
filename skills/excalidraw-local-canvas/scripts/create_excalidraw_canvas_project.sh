#!/usr/bin/env bash
set -euo pipefail

PROJECT_NAME="${1:-excalidraw-story-canvas}"

mkdir -p "$PROJECT_NAME"/{canvas/source,canvas/exports,inputs,private,prompts,reviews}

cat > "$PROJECT_NAME/.gitignore" <<'GITIGNORE'
private/
*.local.*
.env
.env.*
secrets.*
canvas/exports/draft-*
.DS_Store
GITIGNORE

cat > "$PROJECT_NAME/docker-compose.yml" <<'COMPOSE'
services:
  excalidraw:
    image: excalidraw/excalidraw:latest
    ports:
      - "5000:80"
    restart: unless-stopped
COMPOSE

cat > "$PROJECT_NAME/prompts/canvas-spec.md" <<'CANVAS'
# Canvas Spec

Audience:
Goal:
Sensitivity level:
Allowed sources:
Disallowed sources:

## Global thesis

## Regions

### Region 1:
Purpose:
Key message:
Visual elements:
Evidence:
Speaker notes:

### Region 2:
Purpose:
Key message:
Visual elements:
Evidence:
Speaker notes:

## Zoom path
1. Start at global overview.
2. Zoom into region 1.
3. Return to global thesis.
4. Zoom into region 2.
5. End at decision or next actions.

## Export targets
- editable: .excalidraw
- review: pdf
- sharing: png/svg
CANVAS

cat > "$PROJECT_NAME/reviews/security-review.md" <<'SECURITY'
# Security Review

## Sensitive content check
- [ ] no secrets, tokens, keys, passwords
- [ ] no customer names unless approved
- [ ] no emails, tenant IDs, account IDs, private URLs
- [ ] no raw production logs
- [ ] no restricted HR/legal/M&A/regulated data

## Export check
- [ ] zoomed into all small text
- [ ] screenshots reviewed
- [ ] export label chosen: public / internal / confidential / restricted
- [ ] sharing channel approved
SECURITY

cat > "$PROJECT_NAME/inputs/sanitized-notes.md" <<'NOTES'
# Sanitized Notes

Put sanitized source notes here. Do not paste raw secrets, customer identifiers, private URLs, or production logs.
NOTES

echo "created $PROJECT_NAME"
echo "next: cd $PROJECT_NAME && docker compose up -d"
