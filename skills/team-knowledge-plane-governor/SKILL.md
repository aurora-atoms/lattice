---
name: team-knowledge-plane-governor
description: Govern a public, vendor-neutral Team Knowledge and Agent Control Plane Lite from source inventories, policies, knowledge contracts, registry records, architecture proposals, and lifecycle evidence. Query ConPort first when available. Use when defining system-of-record boundaries, canonical knowledge metadata, provenance, ACL, freshness, candidate-to-approved promotion, memory boundaries, or POC sequencing; output is a bounded architecture decision, machine-readable contract or registry design, ownership map, and promotion verdict preserving source authority, privacy, validation, and rebuildable projections. Do not use to implement a retriever, tune ranking, create a task capability profile, expose write tools, publish private context, or turn chats and model output directly into organizational truth.
---

# Team Knowledge Plane Governor

## Goal

Govern the smallest useful shared-knowledge control plane without replacing source systems, capability governance, retrieval engines, or human approval.

## Use When

Use for knowledge contracts, source authority, registry/lifecycle design, privacy and ownership boundaries, POC scope, promotion rules, and architecture reviews spanning knowledge and agent access.

## Do Not Use When

Do not build retrieval internals; route that work to `hybrid-knowledge-retrieval-builder`. Do not author task profiles or eval suites; route them to `knowledge-profile-evaluator`. Do not ingest private material into a public package, operate a graph by default, or approve autonomous writes.

## Inputs

Use the smallest relevant set of source inventories, owner and reviewer lists, source policies, classifications, ACL groups, freshness requirements, task types, golden questions, existing registries, and current implementation evidence.

## Outputs

Return one or more of:

- a Project Knowledge Contract;
- knowledge-object or source-registry records;
- a source-to-authority and projection map;
- lifecycle and approval decisions;
- a POC boundary with measurable gates;
- a `promote | revise | reject | defer` verdict with evidence gaps.

## Workflow

1. Query_ConPort_MCP_before_loading_or_searching_full_skill_text when available; otherwise inspect registries and targeted source metadata before long documents.
2. Name the users, tasks, protected domains, business outcome, and forbidden knowledge sources.
3. Identify each system of record and its owner. Treat indexes, graphs, summaries, context packs, chats, and model output as derived or candidate artifacts unless a reviewed contract says otherwise.
4. Create or validate the Project Knowledge Contract before designing ingestion.
5. Register pointers and governance metadata, not bulk source copies. Use `schemas/project-knowledge-contract.schema.json` and `schemas/knowledge-object.schema.json` as the public baseline.
6. Apply lifecycle states: `candidate -> verified -> active -> superseded | expired | revoked`; allow `rejected` from review. Never skip verification for model-created knowledge.
7. Define ACL, classification, valid/effective time, review deadline, provenance, conflict, and supersession behavior before projection.
8. Route projection work to the retrieval builder and activation/eval work to the profile evaluator.
9. Keep Graph, A2A, and write-capable autonomy deferred until the same eval set proves a need and governance is ready.
10. Return the narrowest executable POC and list unresolved authority, permission, or evidence decisions.

## Rules

TKPG.001 | MUST | authority | preserve each source system as authority unless an explicit migration decision changes it
TKPG.002 | MUST | registry | store governed identifiers metadata state and source pointers
TKPG.003 | MUST | provenance | preserve source version derivation activity responsible actor and evidence locator
TKPG.004 | MUST | access | define classification and ACL before projection or retrieval
TKPG.005 | MUST | lifecycle | require review before candidate knowledge becomes active
TKPG.006 | MUST | freshness | define effective time review time expiry and supersession behavior
TKPG.007 | MUST | conflict | retain conflicting active claims until an authorized resolution is recorded
TKPG.008 | MUST | projection | keep keyword vector and graph stores derived and rebuildable
TKPG.009 | NEVER | memory | promote chat trace tool output or model inference directly into authority
TKPG.010 | NEVER | privacy | copy private downstream material into public Lattice artifacts
TKPG.011 | SHOULD | token | optimize for quality-adjusted token ROI through metadata-first progressive loading
TKPG.012 | SHOULD | cache | keep invariant contracts and rules in a stable prefix and changing task data in a dynamic suffix
TKPG.013 | MAY | graph | add graph projection only after measured multi-hop or global-query gain
TKPG.014 | MAY | a2a | add agent delegation only when independently operated agents must exchange tasks and artifacts

## References

- Read `references/control-plane-contract.md` for plane boundaries, lifecycle, registry fields, and POC decisions.
- Read `references/industry-evidence.md` when a design claim or technology choice needs current primary-source evidence.
- Use `schemas/project-knowledge-contract.schema.json` for project-level authority and governance declarations.
- Use `schemas/knowledge-object.schema.json` for canonical knowledge registry records.
- Load downstream skill references only after routing the task.

## Verification

Validate the package and machine-readable artifacts:

```bash
python3 scripts/validate_skill_package.py --root skills/team-knowledge-plane-governor
python3 scripts/estimate_skill_tokens.py --root skills/team-knowledge-plane-governor
python3 -m json.tool skills/team-knowledge-plane-governor/schemas/knowledge-object.schema.json >/dev/null
python3 -m json.tool skills/team-knowledge-plane-governor/schemas/project-knowledge-contract.schema.json >/dev/null
git diff --check
```

Before promotion, require positive and negative trigger cases, output assertions, public/private boundary review, and evidence that no hard rule is hidden only in a reference.

## Failure Modes

- source-collapse: a projection or chat workspace is treated as the authority;
- registry-dump: full documents are copied into registry rows or prompts;
- memory-laundering: model output becomes approved knowledge without review;
- ACL-late-binding: access policy is added only after indexing;
- freshness-blindness: records have no effective, review, expiry, or supersession semantics;
- graph-first: ontology and graph cost precede a measured query need;
- control-plane-collision: knowledge lifecycle silently absorbs capability, delivery, or product-runtime ownership.
