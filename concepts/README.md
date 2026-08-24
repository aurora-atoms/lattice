# Capability Compositions

Lattice keeps capability identity separate from capability composition.

- `registry/capability-manifest.json` remains authoritative for public capability identity, version, role, package status, compatibility, and authority.
- `concepts/<concept-id>/concept.json` is authoritative only for how already-existing workflows, contracts, templates, validators, examples, tests, and CI relate inside one logical concept.
- `registry/capability-compositions.index.jsonl` is the compact generated discovery projection for agents. It is not a second capability manifest.

## Agent discovery

Use a composition when the request spans multiple stages or when repository files are physically separated and their relationship is not obvious.

```text
user goal
  -> native capability discovery
  -> composition registry when a multi-stage concept is needed
  -> concept entrypoint
  -> current stage only
  -> handoff condition
  -> next stage only when justified
```

Do not infer workflow relationships from folder adjacency.

For a matched composition:

1. Read the compact composition registry row.
2. Open the concept `entrypoint`.
3. Select the current stage from its entry conditions.
4. Load only `task_scoped` artifacts for that stage.
5. Load `reference_only` artifacts only when the current output requires them.
6. Treat `never_by_default` artifacts as non-context. Validators may be executed; validator source, tests, and CI should not be loaded into ordinary task context.
7. Follow a handoff only when its evidence condition is satisfied.
8. Stop at a human authority boundary rather than inferring permission from a green validator or CI run.

## Maintainer contract

Composition files are public navigation contracts, not new modules or mega Skills. They may point to artifacts owned by different repository layers while preserving those layers' separate authority.

After editing a composition, run:

```bash
python scripts/generate_capability_composition_registry.py --root .
python scripts/validate_capability_compositions.py --root .
python -m unittest discover -s tests -p 'test_capability_composition.py' -v
```

The validator checks schema conformance, repository-path resolution, stage graph integrity, handoff edges, progressive-loading semantics, and projection parity.
