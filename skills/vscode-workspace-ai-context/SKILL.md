---
name: vscode-workspace-ai-context
description: "Maintain VS Code .code-workspace files, workspace settings JSON, AI customization files, Agent Skills discovery, custom instructions, prompt/agent locations, and context-exclude policy from official VS Code setting sources. Use when editing workspace files, fixing Unknown Configuration Setting warnings, configuring chat.agentSkillsLocations/chat.instructionsFilesLocations/search.exclude/files.watcherExclude/git discovery, or producing output results such as workspace-setting patches, instruction-file patches, and registry-first/progressive-disclosure guidance while preserving supported-setting validity, behavior, public/private boundaries, and quality-adjusted token ROI. Do not use for private repo-specific skill content, product runtime code, unsupported custom settings without an extension, or stale VS Code AI settings without verification."
---

# VS Code Workspace AI Context

## Goal

Maintain VS Code workspace files so AI agents can discover the right instructions and skills without loading unrelated context.

Keep this skill public and generic. It may describe patterns for downstream private repos, but must not include private skill content, private paths as defaults, or product-specific policy beyond examples supplied by the user.

## Use When

```text
.code-workspace update
settings.json update
Unknown Configuration Setting warning
chat.agentSkillsLocations / chat.instructionsFilesLocations change
repository and path-scoped instruction-file routing
search.exclude / files.watcherExclude context hygiene
git.scanRepositories / git.openRepositoryInParentFolders tuning
progressive-disclosure or registry-first agent context setup
```

## Do Not Use When

```text
private skill content should be written into public Lattice
product runtime code or app features are requested
the task requires a custom VS Code setting without also creating/using an extension that contributes it
the user asks for old Copilot settings and current docs have not been checked
workspace changes would hide intentional tracked artifacts without review
```

## Inputs

```text
*.code-workspace
.vscode/settings.json
VS Code user settings excerpts
repository instruction files
path-scoped instruction files
agent instruction files
skill registry files
current official VS Code AI/settings docs
validator or Unknown Configuration Setting diagnostics
```

## Outputs

```text
workspace settings patch
instruction-file patch
agent-skill discovery configuration
context-exclude policy
Git repository discovery settings
unsupported-setting replacement plan
validation commands and evidence summary
```

## Workflow

1. Query_ConPort_MCP_before_loading_or_searching_full_skill_text when available; otherwise read the targeted workspace/settings file before broad search.
2. Identify whether the desired behavior belongs in supported VS Code settings, instruction files, Agent Skills locations, prompt/agent locations, Git discovery settings, or an external helper script.
3. Verify current VS Code setting names from official docs when adding or replacing AI customization settings.
4. Remove or replace unknown settings unless a VS Code extension contributes them through `contributes.configuration`.
5. Prefer file-based instructions over deprecated settings-based code/test generation instructions when current docs say so.
6. Configure Agent Skills with `chat.agentSkillsLocations` when the workspace should auto-discover skills.
7. Configure instructions with `chat.instructionsFilesLocations` plus concise instruction files when the policy should be always-on or file-scoped.
8. Use `search.exclude` and `files.watcherExclude` for noisy or bulky paths, but do not confuse these with security boundaries.
9. Preserve Source Control ergonomics with `git.scanRepositories`, `git.autoRepositoryDetection`, and `git.openRepositoryInParentFolders` when a narrow workspace needs multiple repos visible.
10. Validate JSON, run relevant project validators, and report any setting that is editor-recognized versus agent-convention-only.

Optimize for quality-adjusted token ROI. Keep stable prefix context across repeated workspace maintenance: supported-setting rule, instruction/skill discovery model, progressive-disclosure policy, public/private boundary, and validation commands. Put workspace-specific paths, active folders, and diagnostics in the dynamic suffix.

## Rules

```text
VSAI.001 | MUST   | settings | use_only_supported_VS_Code_settings_unless_extension_contributes_configuration | enforce
VSAI.002 | MUST   | verify   | verify_fast_moving_AI_setting_names_from_official_docs_before_new_guidance | enforce
VSAI.003 | MUST   | skills   | use_chat.agentSkillsLocations_for_workspace_agent_skill_discovery | enforce
VSAI.004 | MUST   | instr    | use_instruction_files_for_general_agent_guidance_when_supported | enforce
VSAI.005 | MUST   | boundary | keep_private_downstream_context_out_of_public_Lattice | block
VSAI.006 | SHOULD | context  | use_registry_or_index_first_then_selected_SKILL_md_then_routed_references | prefer
VSAI.007 | SHOULD | exclude  | exclude_noisy_generated_or_bulk_context_from_search_and_watchers | prefer
VSAI.008 | SHOULD | git      | use_explicit_git_scan_roots_for_narrow_multi_repo_workspaces | prefer
VSAI.009 | NEVER  | custom   | leave_unknown_custom_setting_in_workspace_as_if_VS_Code_enforces_it | block
VSAI.010 | NEVER  | privacy  | treat_search_exclude_or_watcher_exclude_as_a_security_boundary | block
```

## Verification

```text
workspace JSON parses
no Unknown Configuration Setting remains for intended native VS Code settings
instruction file path is inside chat.instructionsFilesLocations
skill folder path is inside chat.agentSkillsLocations
selected skill package validates when skills are changed
search/watch excludes do not hide intentional source artifacts from review
git status shows only intended workspace/instruction changes
```

Useful commands:

```powershell
Get-Content <workspace.code-workspace> | ConvertFrom-Json | Out-Null
git diff --check
python3.14 scripts\validate_skill_package.py --root skills
```

## Failure Modes

```text
unknown-setting: workspace contains a setting not contributed by VS Code or an installed extension
deprecated-setting: old AI instruction setting used when file-based instructions are current guidance
autoload-sprawl: workspace causes all skills/references/assets to load instead of routing progressively
false-security: exclude setting is treated as access control
source-control-sprawl: broad folder opened only to make Git repositories visible
private-leak: private downstream skill content copied into public Lattice
stale-docs: AI customization settings changed without checking current official docs
```

## References

Consult official VS Code docs when setting names matter:

- VS Code settings reference for `chat.*`, `github.copilot.*`, Git, search, and watcher settings.
- VS Code custom instructions docs for repository, path-scoped, and agent instruction files.
- VS Code Agent Skills docs for `chat.agentSkillsLocations`.
- VS Code extension contribution docs for custom settings via `contributes.configuration`.
