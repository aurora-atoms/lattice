---
name: vscode-workspace-ai-context
description: "Guide, audit, and improve VS Code, GitHub Copilot, Codex, and Claude Code workspace AI configuration from current official settings and model guidance. Use when reviewing .code-workspace or settings JSON/JSONC, AGENTS.md, CLAUDE.md, Copilot instructions, .codex/config.toml, .claude/settings files, Agent Skills discovery, permissions, MCP/tool scope, model or reasoning defaults, context duplication, token cost, cache stability, or Unknown Configuration Setting diagnostics; output an evidence-backed AI_CONFIG_AUDIT_V1 report, bounded patches, and validation commands that preserve behavior, security, public/private boundaries, and quality-adjusted token ROI. Do not use for product runtime code, private repo content in public Lattice, unsupported settings without extension evidence, static model rankings without current verification, or automatic writes to user-home configuration without explicit input and approval."
---

# VS Code Workspace AI Context

## Goal

Configure and audit repository AI surfaces so VS Code, Copilot, Codex, and Claude Code receive relevant instructions, bounded tools, safe permissions, and task-appropriate model guidance without duplicate or stale context.

Keep this skill public and generic. It may describe downstream patterns but must not include private skill content, private paths as defaults, credentials, or product-specific policy beyond user-supplied examples.

## Use When

```text
VS Code workspace or settings review
Copilot instruction, agent, prompt, or skill discovery
Codex config.toml, AGENTS.md, sandbox, approval, or reasoning review
Claude Code settings, CLAUDE.md, rules, permissions, or effort review
Unknown Configuration Setting diagnosis
AI context duplication, MCP sprawl, token waste, or cache instability
model-routing guidance based on current availability, price, and repository evals
```

## Do Not Use When

```text
product runtime implementation is requested
private downstream content would enter public Lattice
user-home settings are unavailable but exact edits are claimed
an extension-contributed setting is declared invalid without extension evidence
a model is ranked from memory instead of current sources and local task evals
search or watcher excludes are treated as access control
```

## Inputs

```text
*.code-workspace
.vscode/settings.json
.github/copilot-instructions.md
.github/instructions/*.instructions.md
AGENTS.md and AGENTS.override.md
CLAUDE.md and .claude/rules/*.md
.claude/settings.json and settings.local.json
.codex/config.toml and supplied user-level excerpts
skill, prompt, agent, hook, MCP, and tool locations
VS Code diagnostics and installed extension list
current official VS Code, GitHub, OpenAI, and Anthropic documentation
representative tasks, token or credit data, and validation outcomes
```

## Outputs

```text
AI_CONFIG_AUDIT_V1 report
configuration and instruction patches
finding severity, evidence, confidence, and recommendation
unsupported or ignored setting replacement plan
permission and sandbox risk report
context duplication and discovery-path report
model and reasoning routing recommendation with current-source caveat
validation commands and unresolved evidence gaps
```

`AI_CONFIG_AUDIT_V1` fields:

```text
schema root summary surfaces findings
finding = id severity surface path message evidence recommendation confidence
severity = error | warning | info
```

## Workflow

1. Query_ConPort_MCP_before_loading_or_searching_full_skill_text when available; otherwise inspect only the targeted workspace and configuration files before broad repository search.
2. Inventory each runtime separately: VS Code/Copilot, Codex, and Claude Code. Do not assume one runtime's settings configure another runtime.
3. Run `scripts/audit_ai_workspace_config.py` when repository files are available. Treat its findings as deterministic first-pass evidence, not a complete vendor schema validator.
4. Confirm syntax, active scope, configuration precedence, installed extensions, and whether each setting is native, extension-contributed, ignored, deprecated, experimental, preview, or organization-managed.
5. Verify fast-moving setting names, model availability, reasoning values, billing behavior, and permission semantics against current official sources. Record the verification date.
6. Audit instruction composition: always-on files, imports, nested rules, path-scoped rules, size, duplication, contradictions, discovery paths, and stable-prefix impact.
7. Audit tool and permission scope: MCP discovery, allowed tools, network access, sandbox mode, approvals, secret exposure, destructive actions, and user versus project configuration boundaries.
8. Separate findings into syntax, unsupported or ignored configuration, security, context duplication, discovery mismatch, tool sprawl, token cost, cache stability, and model routing.
9. Recommend the smallest supported patch. Preserve user intent, existing behavior, security boundaries, organization policy, and public/private separation.
10. Validate with parsers, the audit script, runtime diagnostics, narrow task evals, and targeted repository tests. Report unverified assumptions instead of inventing certainty.

For model guidance, use task classes rather than permanent vendor rankings:

```text
routine bounded work -> available lightweight or low-reasoning option
normal implementation -> balanced model and regular reasoning
architecture or difficult debugging -> stronger reasoning model after planning
subagents -> cheaper focused models when task isolation preserves quality
final choice -> current runtime availability + price + frozen repository eval results
```

## Rules

```text
VSAI.001 | MUST   | settings | use supported settings or identify the extension that contributes them
VSAI.002 | MUST   | verify   | verify fast-moving settings and model claims from current official sources
VSAI.003 | MUST   | runtime  | audit VS Code Codex and Claude Code as separate configuration surfaces
VSAI.004 | MUST   | evidence | attach file evidence confidence and verification status to each finding
VSAI.005 | MUST   | skills   | configure nondefault skill folders through documented discovery settings
VSAI.006 | MUST   | boundary | keep private downstream context credentials and local paths out of public Lattice
VSAI.007 | MUST   | safety   | flag unrestricted sandbox permission network and literal secret configuration
VSAI.008 | SHOULD | context  | use one shared stable rule source plus runtime-specific adapters
VSAI.009 | SHOULD | routing  | use path-scoped instructions skills prompts and agents instead of one giant file
VSAI.010 | SHOULD | tools    | expose only task-required MCP servers tools and subagents
VSAI.011 | SHOULD | model    | select model and reasoning by task evidence availability and cost
VSAI.012 | SHOULD | cache    | keep stable rules tools and model choice fixed within a task session
VSAI.013 | SHOULD | exclude  | exclude generated and noisy content from search and watchers after review
VSAI.014 | NEVER  | custom   | claim arbitrary custom settings are enforced without extension evidence
VSAI.015 | NEVER  | security | treat search watcher or context excludes as access-control boundaries
VSAI.016 | NEVER  | model    | publish a permanent best-model ranking from stale names or benchmarks
VSAI.017 | NEVER  | write    | overwrite user-home configuration without explicit source and approval
```

## References

- Read `references/vendor-config-surfaces.md` before auditing vendor-specific keys, precedence, model availability, or billing claims.
- Consult current official VS Code settings, customization, and Agent Skills documentation when native setting names matter.
- Consult current OpenAI Codex configuration and AGENTS.md documentation for Codex-specific behavior.
- Consult current Anthropic Claude Code settings and memory documentation for Claude-specific behavior.
- Consult current GitHub Copilot supported-model, comparison, optimization, and billing documentation for model and credit guidance.

## Scripts

Run a deterministic first-pass audit:

```bash
python3 skills/vscode-workspace-ai-context/scripts/audit_ai_workspace_config.py --root . --format markdown
python3 skills/vscode-workspace-ai-context/scripts/audit_ai_workspace_config.py --root . --format json --strict
```

The script checks high-confidence syntax, path, duplication, permission, sandbox, secret, discovery, and token-risk patterns. It does not replace VS Code schema diagnostics, extension manifests, organization policy, or current vendor documentation.

## Verification

```bash
python3 -m unittest discover -s skills/vscode-workspace-ai-context/evals -p 'test_*.py' -v
python3 scripts/validate_skill_package.py --root skills/vscode-workspace-ai-context
python3 skills/vscode-workspace-ai-context/scripts/audit_ai_workspace_config.py --root . --format json
python3 -m json.tool skills/vscode-workspace-ai-context/evals/trigger_queries.json >/dev/null
python3 -m json.tool skills/vscode-workspace-ai-context/evals/output_cases.json >/dev/null
git diff --check
```

Also verify:

```text
VS Code reports no unintended Unknown Configuration Setting diagnostics
runtime displays the expected active instruction and settings sources
project-local Codex keys are not silently ignored
Claude permission precedence matches the effective settings view
skills instructions prompts agents and MCP paths resolve
no secret or private downstream content appears in the patch
recommendations distinguish current fact from local-eval inference
```

## Failure Modes

```text
unknown-setting: native support or extension contribution is unverified
ignored-project-key: a runtime silently ignores a project-local key
cross-runtime-assumption: VS Code setting is assumed to configure Codex or Claude Code
instruction-double-load: AGENTS.md is loaded directly and again through CLAUDE.md
context-sprawl: always-on rules imports tools or generated files dominate context
permission-bypass: sandbox approvals or tool rules are broader than task need
secret-literal: committed configuration contains token key credential or password values
model-staleness: renamed unavailable preview or repriced model is recommended as current
benchmark-transfer: public benchmark is treated as repository-specific proof
false-security: exclude settings are presented as authorization controls
home-config-guess: exact user settings are modified without inspecting their source
script-overclaim: deterministic heuristic output is presented as complete vendor validation
```
