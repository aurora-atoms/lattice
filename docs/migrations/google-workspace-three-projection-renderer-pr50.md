# PR50: Deterministic Google Workspace Three-Projection Renderer

## Decision

Advance the existing Google Workspace Senior Attention adapter from a canonical contract only to deterministic, copy-ready public projections for three distinct runtime surfaces:

```text
gem
workspace_studio
notebook
```

This remains a provider projection layer over the existing Senior Attention workflow. It does not create a new task Skill, Agent, module, fact store, private source bridge, or autonomous action plane.

## Direction Fit

```text
primary_value_path: current_product_delivery
direction_verdict: bind_to_delivery
```

The bounded value is practical installation guidance for a private Senior Attention shadow pilot. The public repository can now prove that the three runtime templates derive from one source and preserve the same authority/source boundaries. It still cannot prove real account availability, usefulness, adoption, attention savings, or business value.

## Version

The canonical adapter source advances:

```text
1.0.0 -> 1.1.0
```

The change is additive at the adapter layer: deterministic rendered projections, source/render hashes, copy-ready templates, and drift validation are added. The underlying Senior Attention task semantics and existing Skill versions do not change.

## Deterministic Source and Render Binding

Canonical source:

```text
runtime-adapters/google-workspace/senior-attention/adapter-source.v1.json
```

Renderer:

```text
scripts/render_google_workspace_senior_attention_adapters.py
```

Generated set manifest:

```text
runtime-adapters/google-workspace/senior-attention/projection-manifest.v1.json
```

The renderer computes:

```text
adapter_source_hash = sha256(canonical sorted compact JSON)
render_hash = sha256(ordered generated path + bytes set)
```

Each generated Markdown/YAML template carries the source hash. Generated JSON templates and the projection manifest carry the same source binding. CI runs the renderer in `--check` mode; manual drift from the canonical source fails validation.

## Generated Public Projections

Gem:

```text
gem/gem-instructions.template.md
gem/gem-knowledge-pack.manifest.json
gem/starter-prompts.md
```

Workspace Studio:

```text
workspace-studio/skill-instructions.template.md
workspace-studio/manual-shadow-flow.template.yaml
```

NotebookLM:

```text
notebook/notebook-setup.md
notebook/notebook-custom-chat.template.md
notebook/notebook-source-manifest.template.json
notebook/prompt-cards.md
```

These files are public-safe templates, not live product configuration and not evidence of enabled Google features in any specific account.

## Invariants Preserved Across All Projections

```text
authority_ceiling = candidate
human_confirmation_required = true
coverage_claim = bounded_not_complete
private source binding = downstream_only
automatic action default = false
```

Every runtime projection must preserve selected/unavailable/excluded/not-searched source scope, visible unknowns, conflicts, strongest counterevidence, and a private downstream verification handoff.

Workspace Studio remains manual/shadow by default. The public flow explicitly disables automatic send/share/delete, ticket/file writes, manager posts, irreversible action, and silent permission expansion.

NotebookLM remains a source-grounded synthesis surface rather than global enterprise search, code execution, Lattice Skill execution, or final decision authority.

Gem remains an interactive intake/scouting surface rather than a verified fact system or action authority.

## Public / Private Boundary

Public Lattice contains only reusable adapter contracts, deterministic render logic, templates, schemas, tests, and synthetic-safe placeholders.

Private downstream owns all real Workspace account settings, Gmail/Drive/Chat/Notebook sources, source permissions, private locators, live cases, source manifests, candidate outputs, corrections, decisions, actions, outcomes, and attention measurements.

The Notebook source manifest file is a template. Values such as `DOWNSTREAM_PRIVATE_LOCATOR` must be replaced only in the private downstream environment and must never be committed back into public Lattice.

## Compatibility

This PR does not change:

- `docs/senior-attention.md` task-family semantics;
- `senior-attention-runtime@1.0.0` authority or permissions;
- `domain-context-pack` or `delivery-rescue` behavior;
- active module status or boundaries;
- Evidence Wayfinding / reserved evaluation contracts;
- human authority for private business conclusions, manager commitments, merge, release, or deployment.

The Google adapter remains intentionally outside the canonical capability registry because it is a provider projection contract, not an independently routable task capability.

## Validation

CI validates:

```text
canonical adapter schema + semantics
projection manifest schema
renderer --check
source hash / render hash binding
nine generated target files
authority and source-coverage invariants
manual-action defaults
projection drift mutation
existing Senior Attention regressions
public/private boundary
```

## Next Gate

Do not add more provider architecture by default. The next bounded public contract may be the runtime-neutral Source Synthesis Candidate only if it is required to make the generated projections interoperable with private verification. Otherwise use the templates in a private manual/shadow pilot first and let observed conversion failures determine the next repair.
