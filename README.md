# Lattice

Lattice is a public, generic AI capability control-plane workspace for repo-native agents, skills, registries, validators, and runtime adapter contracts.

License: Apache-2.0.

```text
project_display_name = Lattice
project_id = lattice
namespace = lat
```

## Scope

This phase keeps the existing Skill Rewrite / Skill Refactor System and adds an executable capability-control-plane MVP for generic agents, skills, workspaces, MCP records, knowledge packs, validation, and deterministic runtime rendering contracts.

Skill refactor pipeline:

```text
old Markdown skill -> ConPort-first retrieval -> inventory -> classification -> token-friendly rewrite plan -> optimized SKILL.md -> moved content plan -> validation report
```

Governance pipeline:

```text
candidate skill -> registry record -> trigger eval -> output eval -> validator -> release recommendation
```

Capability-control-plane pipeline:

```text
registry metadata -> generic agent -> workspace manifest -> selected skills/MCP/knowledge -> adapter render plan -> install manifest -> validation
```

MVP in this repo:

```text
generic agent schema
workspace template schema
MCP registry schema
knowledge-pack registry schema
render manifest schema
agent validator
workspace manifest validator
MCP registry validator
global overinstall detector
seed pr-reviewer and python-expert agents
seed PR review workspace template
```

Deferred: full renderers, installer CLI, remote registry service, UI, GraphDB, automatic orchestration, and non-MVP runtime adapters.

## Current Skills

- `skills/lattice-governor`: public Lattice governance skill for skill registry design, trigger/output evals, token-efficient refactor plans, validator workflows, and release gates.
- `skills/vscode-workspace-ai-context`: public VS Code workspace AI context skill for supported instruction and skill discovery settings.

## Capability Control Plane

Canonical sources:

```text
agents/<agent-name>/agent.json
agents/<agent-name>/<agent-name>.agent.md
workspaces/templates/*.json
registry/*.index.jsonl
schemas/capability/*.schema.json
```

Core registries:

```text
registry/skills.index.jsonl
registry/agents.index.jsonl
registry/capabilities.index.jsonl
registry/mcp_servers.index.jsonl
registry/knowledge_packs.index.jsonl
registry/workspace_templates.index.jsonl
registry/release_log.jsonl
```

Rules:

```text
agents are generic role packages, not feature or ticket context
workspace manifests hold scenario-specific repo context
runtime configs are rendered outputs unless explicitly marked source
MCP exposure requires explicit toolsets and approval policy
global installs must not expose all skills, tools, or knowledge by default
public Lattice records must not contain private downstream context
```

## Revision 1 Rules

Current policy enforces:

```text
preserve existing frontmatter schemas during refactor
do not add use_when or do_not_use_when YAML fields
put when-to-use and when-not-to-use guidance inside description
query ConPort before loading or searching full skill text
prioritize machine readability over human readability in control planes
define token efficiency as quality-adjusted output per token cost
use stable prompt prefixes to improve token caching and batch repeatability
```

## Format Policy

Use `docs/skill_format_policy.md` as the source of truth.

Core routing:

```text
Always-loaded project rules | Markdown container + compact rule manifest
Skill control plane | SKILL.md + references/scripts/schemas/evals
Agent handoff | JSONL + JSON Schema
Tool/function input/output | JSON Schema / Structured Outputs
Runtime event log | Append-only JSONL
Bulk context into LLM | LATPACK / schema-once compact rows
Manager report | Markdown
```

Markdown is allowed for instructions, module contracts, `SKILL.md`, references, architecture notes, and manager-facing reports. It is not appropriate for raw logs, telemetry dumps, token records, event ledgers, or bulk machine records.

Human-readable prose is not required by default in control planes. Use compact rule lines and structured blocks when precision matters.

Skill refactor agents must prefer:

```text
ConPort MCP -> targeted source file read -> broader file search
```

Local scripts remain dependency-light and work without ConPort.

## Quickstart

Recommended interpreter: Python 3.14.6.

```bash
python3.14 scripts/inventory_skills.py --root skills --out skill_inventory.jsonl
python3.14 scripts/validate_skill_package.py --root skills
python3.14 scripts/generate_skill_refactor_report.py --inventory skill_inventory.jsonl --out skill_quality_report.md
```

Optional token estimate:

```bash
python3.14 scripts/estimate_skill_tokens.py --root skills
```

Capability-control-plane validation:

```bash
python3.14 scripts/validate_agent.py --root .
python3.14 scripts/validate_workspace_manifest.py --root .
python3.14 scripts/validate_mcp_registry.py --root .
python3.14 scripts/detect_global_overinstall.py --root .
```

## Registry

Public skill records live in `registry/skills.index.jsonl`. Public records must not contain private downstream project context.

Public capability records extend this with agents, MCP servers, knowledge packs, workspace templates, and a denormalized `capabilities.index.jsonl` search surface. Existing skill registry records remain compatible.

## Outputs

`skill_inventory.jsonl` contains one JSON record per detected skill package.

`skill_quality_report.md` summarizes largest skills, missing sections, risk flags, top refactor candidates, and review queue items.

Validation exits nonzero when package errors are found and prints warnings for token-risk patterns.
