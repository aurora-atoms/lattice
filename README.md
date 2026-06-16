# Lattice

Lattice is a project workspace for repo-native tooling. This phase focuses on the Skill Rewrite / Skill Refactor System and public skill governance standards.

License: Apache-2.0.

```text
project_display_name = Lattice
project_id = lattice
namespace = lat
```

## Scope

This phase builds generic standards, schemas, examples, scripts, and agent instructions for converting existing Markdown-based skills into optimized Skill packages.

Pipeline:

```text
old Markdown skill -> ConPort-first retrieval -> inventory -> classification -> token-friendly rewrite plan -> optimized SKILL.md -> moved content plan -> validation report
```

Governance pipeline:

```text
candidate skill -> registry record -> trigger eval -> output eval -> validator -> release recommendation
```

Deferred: rewriting large skill libraries, implementing active modules, and integrating a hard ConPort adapter into local scripts.

## Current Skills

- `skills/lattice-governor`: public Lattice governance skill for skill registry design, trigger/output evals, token-efficient refactor plans, validator workflows, and release gates.

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

```bash
python scripts/inventory_skills.py --root skills --out skill_inventory.jsonl
python scripts/validate_skill_package.py --root skills
python scripts/generate_skill_refactor_report.py --inventory skill_inventory.jsonl --out skill_quality_report.md
```

Optional token estimate:

```bash
python scripts/estimate_skill_tokens.py --root skills
```

## Registry

Public skill records live in `registry/skills.index.jsonl`. Public records must not contain private downstream project context.

## Outputs

`skill_inventory.jsonl` contains one JSON record per detected skill package.

`skill_quality_report.md` summarizes largest skills, missing sections, risk flags, top refactor candidates, and review queue items.

Validation exits nonzero when package errors are found and prints warnings for token-risk patterns.
