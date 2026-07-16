# Retrieval Contract

## Chunk Record

Every indexed unit should retain:

```text
chunk_id document_id knowledge_object_id
source_uri source_version source_content_hash
section_path start_offset end_offset original_text
derived_context derived_by derived_at
classification ACL scope status valid_from review_by expires_at
embedding_model lexical_analyzer projection_version
```

Keep `derived_context` nullable. Never concatenate it irreversibly into `original_text`.

## Query Stages

```text
authenticated identity
  -> policy and metadata filter
  -> lexical candidates + vector candidates
  -> deterministic fusion and deduplication
  -> optional rerank
  -> final authorization and freshness guard
  -> context budget selection
  -> citation resolver
```

Record stage ranks rather than pretending heterogeneous raw scores are comparable. Reciprocal Rank Fusion is a reasonable baseline; a learned combiner requires held-out data and versioning.

## Citation Contract

A citation must resolve:

```text
knowledge_object_id
source_uri and source_version
human-usable locator or line/page/section
content hash
retrieved chunk ID
access decision reference
```

The answer may cite a derived projection identifier for diagnostics, but it must also identify the original source.

## No-Answer Contract

Return a typed result:

```json
{
  "status": "insufficient_evidence",
  "reason": "no_authorized_support",
  "query_id": "...",
  "filters_applied": ["acl", "scope", "status", "effective_time"],
  "candidate_count": 0,
  "missing": ["approved source covering requested fact"]
}
```

Distinguish no authorized support, stale-only support, conflicting support, source unavailable, and retrieval-system failure.

## Evaluation Unit

Freeze:

```text
dataset version and split
corpus snapshot and projection version
query and expected relevant source/chunk IDs
caller identity and ACL expectation
retrieval configuration
top-k and context budget
latency and cost measurement method
```

Report exact-match lookup, paraphrase, multi-hop, conflict, stale, ACL-denied, injection-bearing, and no-answer subsets separately.
