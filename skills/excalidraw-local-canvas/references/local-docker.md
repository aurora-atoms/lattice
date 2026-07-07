# Local and Docker Excalidraw Workflow

Use this reference when the user asks how to run Excalidraw locally, use Docker Desktop, use Docker Compose, self-host the client, or manage editable canvas files.

## Docker Desktop

Use Docker Desktop when the user wants local Excalidraw without installing the Node/Yarn development toolchain.

Prerequisites:

- Docker Desktop installed and running.
- Port `5000` available, or choose another host port.

Published image:

```bash
docker pull excalidraw/excalidraw:latest
docker run --rm --name local-excalidraw -p 5000:80 excalidraw/excalidraw:latest
```

Open:

```text
http://localhost:5000
```

Stop:

```bash
docker stop local-excalidraw
```

If port `5000` is busy:

```bash
docker run --rm --name local-excalidraw -p 5001:80 excalidraw/excalidraw:latest
```

Open `http://localhost:5001`.

## Docker Compose

Use this when the project should keep a repeatable Docker Desktop launcher.

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

## Build From Local Source

Use this only when the user needs local Excalidraw source changes.

```bash
cd /path/to/excalidraw
docker build -t local-excalidraw .
docker run --rm --name local-excalidraw -p 5000:80 local-excalidraw
```

Open `http://localhost:5000`.

## Local Development Mode

Use this when the user wants to modify Excalidraw itself or test the upstream app locally.

```bash
git clone https://github.com/excalidraw/excalidraw.git
cd excalidraw
yarn
yarn start
```

Open the URL printed by Vite, usually `http://localhost:3000` or `http://localhost:3001`.

Prerequisites: Node.js 18 or later, Yarn, and Git.

## Caveats

- Self-hosting the Excalidraw client is not the same as Excalidraw+.
- A self-hosted client does not automatically provide share links, cloud storage, or real-time collaboration.
- Browser local storage is convenient but fragile. Export `.excalidraw` files into the project directory.
- Docker Desktop runs the client locally, but the browser still stores unsaved work locally unless the user exports files.

## Recommended Project Structure

```text
project-name/
  canvas/source/
  canvas/exports/
  inputs/
  private/
  prompts/
  reviews/
  docker-compose.yml
  .gitignore
```

Use `.excalidraw` as editable source and keep PNG/SVG/PDF exports separate.
