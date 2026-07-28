# Lattice

Lattice is a public, evidence-grounded delivery capability reference and governance repository.

It publishes reusable Skills, schemas, validators, reference workflows, capability profiles, templates, and synthetic conformance fixtures. Private downstream repositories pin these public contracts to collect real delivery evidence, evolve reusable capability assets, and generate manager-ready deliverables without exposing private business context.

Lattice does **not** store real company logic, source code, tickets, pull requests, incidents, reviews, employee feedback, delivery traces, adoption data, ROI, or manager-ready business materials.

License: Apache-2.0.

```text
project_display_name = Lattice
project_id = lattice
namespace = lat
```

## Operating Boundary

```text
Public Lattice
  contracts / Skills / schemas / validators / templates / synthetic fixtures
                                |
                                | pinned tag or commit
                                v
Private downstream repository
  real feature_delivery_case / private evidence / private extensions
  reusable asset evolution / human review / manager-ready asset packs
```

The Feature Delivery Case (`feature_delivery_case`) is the primary user-value and evidence boundary. Jira, Issue, PR, commit, CI, review, merge, and release records are evidence; they are not the final value unit.

Read the [Public–Private Operating Model](docs/public-private-operating-model.md), [Downstream Private Repository Contract](docs/downstream-private-repository-contract.md), and [Manager Credibility Contract](docs/manager-credibility-contract.md) before integrating Lattice.

## Capability Portfolio

Do not discover Lattice through a hand-maintained shortlist of Skills. Use native runtime discovery first, then the smallest relevant registry projection:

| Portfolio view | Capability type | Version source | Status source | Entry |
|---|---|---|---|---|
| Canonical portfolio | Atomic, selector, workflow, profile, projection, validator, template, or governance contract | `registry/capability-manifest.json` | `registry/capability-manifest.json` | `registry/capability-manifest.json` |
| Skill context projection | Public Skill packages | Canonical manifest | Canonical manifest | `registry/skill-context.catalog.json` |
| Agent context projection | Public Agent packages | Canonical manifest | Canonical manifest | `registry/agent-context.catalog.json` |
| Cross-runtime projection | Agent, Skill, MCP, knowledge pack, or workspace template | Canonical manifest | Canonical manifest | `registry/capabilities.index.jsonl` |
| Fallback routing | Selector compatibility entry | Referenced Skill version | Routing policy | `registry/capability-routing.index.jsonl` |
| Workflow/Profile extensions | Reference workflow or capability profile | Owning public capability version | Owning public capability status | `registry/skill-context.extensions/` |

The role definitions are normative in [Capability Taxonomy](docs/capability-taxonomy.md). Registry files are deterministic compatibility projections generated from the canonical manifest; legacy `status` fields remain for compatibility while `public_package_status` controls dependency readiness.

Current inventory and context validation:

```bash
python scripts/inventory_skills.py --root skills --out skill_inventory.jsonl
python scripts/validate_skill_package.py --root skills
python scripts/validate_capability_context.py --root .
python scripts/generate_capability_registry_projections.py --root . --check
python scripts/validate_capability_manifest.py --root .
python scripts/validate_public_private_boundary.py --root .
python scripts/validate_capability_routing.py --root .
```

## Downstream Quickstart

1. Pin Lattice by immutable tag or commit SHA. A floating `main` reference is invalid.

   ```bash
   git submodule add https://github.com/aurora-atoms/lattice.git vendor/lattice
   git -C vendor/lattice checkout <tag-or-full-commit-sha>
   ```

2. Create a private downstream consumer manifest following [Downstream Private Repository Contract](docs/downstream-private-repository-contract.md). Record the Lattice ref and commit, contract versions, the smallest selected Capability Profile, explicit public capabilities, private extensions, local evidence paths, manager projection, validation commands, and compatibility policy.

3. Create one real `feature_delivery_case` in the private repository. Keep real source, Jira, PR, CI, incident, review, secrets, and business context local.

4. Collect a bounded Evidence Pack. Classify claims as `OBSERVED`, `DERIVED`, `JUDGED`, or `UNKNOWN`; attach evidence references and preserve limitations and human challenge.

5. Run the pinned public validators locally against private paths. Validators may read local evidence during the run, but public Lattice must not receive or persist it.

6. Generate a **Manager-Ready Delivery Asset Pack** in the private repository. Review it against the Manager Credibility Contract before sharing it.

7. On a Lattice upgrade, rerun schema, capability-version, extension, evidence, asset-pack, manager-claim, and compatibility checks before changing the pin.

PR 1 establishes the normative operating contracts. The downstream schemas and validator CLIs are intentionally reserved for PR 3, and the executable synthetic downstream example for PR 4. Until those land, downstream manifests and packs are contract drafts and must not be represented as validator-conformant.

## Public Package and Private Adoption Lifecycles

These are separate concepts:

```text
public_package_status =
  draft | contract_validated | conformance_validated | released | deprecated

downstream_adoption_status =
  not_observed | imported | task_scoped | used_once | reused | team_available | deprecated
```

Public synthetic fixtures use:

```text
simulation_status = synthetic_reference
downstream_adoption_status = not_observed
```

Synthetic conformance cannot establish private use, reuse, team availability, manager acceptance, or business value. The canonical manifest, lifecycle schemas, registry projections, fixture markers, and parity validation enforce this separation.

## Reference Workflows and Profiles

Lattice keeps complex delivery flows out of mega Skills. The portfolio distinguishes:

```text
reference workflow
capability profile
selector entry
atomic capabilities
schemas
validators
templates
```

The initial logical families are Experience-to-Asset, Feature Understanding, Manager Evidence Projection, and Reusable Asset Review. They compose existing capabilities and preserve the boundaries of Helixion, AegisFlow, Memexa, FlowGuard, OpenClaw, and DeliveryYield. DeliveryYield may provide evidence signals; it does not approve delivery or asset promotion.

## Repository Navigation

```text
skills/                         public capability packages
agents/                         public Agent packages
registry/                       discovery and compatibility projections
registry/capability-manifest.json canonical public capability identity source
schemas/                        public machine contracts
feature-delivery-harness-mvp/   Feature Delivery Case conformance testbed
templates/                      public-safe authoring templates
examples/                       synthetic examples only
scripts/                        deterministic validators and projections
tests/                          positive, negative, and compatibility tests
docs/                           operating, governance, and migration contracts
```

## Release and Compatibility

Capability identity uses versioned, typed IDs such as `skill:<name>@<semver>` and `agent:<name>@<semver>`. Public package maturity and private adoption are never encoded in one ambiguous `status` field. See [Release and Compatibility Policy](docs/release-and-compatibility-policy.md), [Capability Context Contract](docs/capability-context-contract.md), the [PR 1 Migration Note](docs/migrations/public-reference-layer-pr1.md), and the [PR 2 Canonical Manifest Migration](docs/migrations/canonical-manifest-pr2.md).

No registry score, green CI run, synthetic fixture, Skill count, PR count, or token count proves private business value. Human owners retain authority over private evidence, architecture, security, compliance, asset promotion, manager wording, merge, release, deployment, and production decisions.
