---
name: hybrid-knowledge-retrieval-builder
description: Build or review a public, vendor-neutral governed retrieval projection from approved knowledge contracts, corpus samples, relevance labels, queries, and implementation code. Query ConPort first when available. Use for ingestion, chunking, lexical and vector candidates, fusion, ACL filtering, reranking, citation resolution, freshness, and measured graph experiments; output is a code or design patch, projection manifest, query trace, citation contract, and comparison that preserves source behavior, provenance, access, abstention, and rebuildability. Do not use for source approval, knowledge promotion, task profiles, datastore selection without a dataset, private-data publication, or claims that hybrid or graph retrieval is always superior.
---

# Hybrid Knowledge Retrieval Builder

## Goal

Build a rebuildable retrieval projection that finds authorized evidence, resolves citations to the original source, and can be evaluated independently from answer generation.

## Use When

Use for corpus ingestion, document normalization, chunking, contextual enrichment, lexical/vector candidate generation, fusion, reranking, filtering, citation resolution, freshness refresh, query tracing, or a measured graph comparison.

## Do Not Use When

Do not decide source authority or promote candidates; route governance to `team-knowledge-plane-governor`. Do not create capability profiles or final release scorecards; route them to `knowledge-profile-evaluator`. Do not bypass ACLs, copy restricted corpora into public fixtures, or choose a datastore without workload evidence.

## Inputs

Require a Project Knowledge Contract, source registry records, caller identity and permitted scope, representative corpus samples, golden queries with relevance labels, latency/cost constraints, and the current retrieval implementation when one exists.

## Outputs

Return one or more of:

- ingestion and chunk contracts;
- a projection manifest;
- bounded implementation code and tests;
- query traces with lexical, semantic, fused, filtered, and reranked stages;
- source-resolvable citations;
- a baseline comparison with dataset version, denominators, latency, and cost.

## Workflow

1. Query_ConPort_MCP_before_loading_or_searching_full_skill_text when available; otherwise read the knowledge contract, source metadata, and golden-query labels before corpus bodies.
2. Refuse projection when source authority, classification, ACL, or allowed use is unresolved.
3. Snapshot the source version and content hash. Normalize deterministically and preserve the original bytes or resolvable source pointer.
4. Deduplicate by content and source identity. Record derivation rather than silently dropping conflicting versions.
5. Chunk by document structure and query needs. Keep original text, source locator, section path, version, classification, ACL, effective time, and content hash on every chunk.
6. If contextualizing a chunk, store context separately as derived text and forbid invented facts.
7. Apply identity, ACL, scope, status, and freshness filters before candidates can enter the answer context. Defense-in-depth filtering after fusion is allowed but not sufficient alone.
8. Generate lexical and semantic candidates separately; record ranks and scores. Fuse deterministically, deduplicate, and rerank only when the dataset justifies its latency and cost.
9. Resolve citations to the system-of-record locator, not merely a vector-store file ID.
10. Return no-answer or insufficient-evidence when authorized support is absent.
11. Compare retrieval stages on the same frozen dataset. Add graph only for identified multi-hop or corpus-global failures and measure net gain.

## Rules

HKRB.001 | MUST | authority | index only allowed source versions with resolvable authority metadata
HKRB.002 | MUST | access | apply identity ACL scope status and time filters before answer context assembly
HKRB.003 | MUST | provenance | retain original locator version hash chunk offsets and derivation
HKRB.004 | MUST | text | preserve original chunk text separately from generated context
HKRB.005 | MUST | fusion | record lexical semantic and fused ranks with deterministic configuration
HKRB.006 | MUST | citation | resolve material claims to original source locators
HKRB.007 | MUST | abstain | return insufficient evidence when authorized support is absent
HKRB.008 | MUST | evaluation | compare components on one versioned relevance dataset
HKRB.009 | NEVER | leakage | retrieve or log content outside caller authorization
HKRB.010 | NEVER | overwrite | replace source text with generated contextualization or summary
HKRB.011 | NEVER | graph | treat graph extraction as canonical source truth
HKRB.012 | SHOULD | token | optimize quality-adjusted token ROI by retrieving compact source-grounded chunks
HKRB.013 | SHOULD | cache | keep schema ranking and citation rules in a stable prefix and query data in a dynamic suffix
HKRB.014 | MAY | rerank | add reranking when measured quality gain exceeds latency and cost tradeoffs

## References

- Read `references/retrieval-contract.md` for ingestion, chunk, query-stage, citation, and no-answer contracts.
- Read `references/implementation-options.md` only when selecting or comparing concrete libraries.
- Use `schemas/projection-manifest.schema.json` for a machine-readable projection build record.
- Read the governor's industry evidence only when a claim needs primary-source verification.

## Verification

```bash
python3 scripts/validate_skill_package.py --root skills/hybrid-knowledge-retrieval-builder
python3 scripts/estimate_skill_tokens.py --root skills/hybrid-knowledge-retrieval-builder
python3 -m json.tool skills/hybrid-knowledge-retrieval-builder/schemas/projection-manifest.schema.json >/dev/null
git diff --check
```

For implementation work, also test deterministic rebuilds, unauthorized-query denial, stale and superseded filtering, exact-identifier queries, semantic paraphrases, duplicate sources, citation resolution, no-answer behavior, and stage-level recall/precision/latency.

## Failure Modes

- vector-only-default: exact identifiers, names, or error codes are missed;
- context-invention: generated chunk context adds unsupported facts;
- post-retrieval-ACL: unauthorized content enters candidates before filtering;
- citation-proxy: citations point only to an index object rather than the source;
- score-collapse: incomparable lexical and vector scores are summed without a defined fusion;
- answer-only-eval: retrieval failures cannot be separated from generation failures;
- graph-canon: extracted entities and edges become authority without source review;
- silent-empty: the system improvises an answer after authorized retrieval returns nothing.
