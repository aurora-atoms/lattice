# Domain Context Pack machine-contract migration

## Decision

`domain-context-pack` advances from public Skill package version `1.0.0` to `1.1.0`.

The change does not create a new capability family. It converts behavior already required by the existing Skill into a public JSON Schema, deterministic semantic validator, synthetic conformance fixture, trigger evals, output evals, and CI checks.

## Compatibility

The visible artifact name remains:

```text
domain-context-pack.v1.json
```

The Skill trigger, primary user, public/private boundary, and authority boundary remain unchanged. The new package version is classified as a backward-compatible minor hardening because the machine contract formalizes existing obligations rather than adding a new source-approval or retrieval capability.

Downstream consumers pinned to `skill:domain-context-pack@1.0.0` may continue to use that contract. Consumers choosing `1.1.0` should validate generated packs with:

```bash
python skills/domain-context-pack/scripts/validate_domain_context_pack.py <pack.json>
```

## New deterministic gates

Version `1.1.0` rejects a pack when any of these conditions hold:

- selected source access is not authorized;
- selected source freshness is stale or unknown;
- a selected source is expired at the pack evidence cutoff;
- a context item's information class is outside the selected source's declared authority;
- evidence references are not addressable URI-like references;
- selected-token accounting does not equal admitted context-item cost or exceeds the declared budget;
- a conditional source has no permission, refresh, conditional-load, or human-review activation action;
- a blocking unknown or unresolved blocking conflict is compressed into an `answerable` result;
- authorization is denied while selected context remains;
- a public `synthetic_reference` fixture claims downstream adoption.

## Public/private boundary

The public schema and synthetic fixture contain no real company context, private source path, live owner, business conclusion, adoption observation, or manager-ready artifact.

Real task evidence, ACL decisions, source contents, accountable owners, private extensions, outcomes, and Senior Attention measurements remain in the downstream private repository. Passing the public validator proves contract conformance only; it does not prove source truth, private use, owner acceptance, or business value.

## Rollback

Rollback is version pinning. A downstream consumer that cannot yet satisfy the `1.1.0` machine contract can remain on `skill:domain-context-pack@1.0.0` while preparing an explicit upgrade. Do not silently relabel a `1.0.0` artifact as `1.1.0`.
