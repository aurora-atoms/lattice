# Implementation Options

Select after freezing the corpus and eval set.

## Managed Baseline

OpenAI File Search supplies semantic plus keyword search, metadata filtering, configurable result inclusion, and file citations. Validate whether its file-level attributes and access model can enforce the project's query-time ACL requirements before use.

Source: https://developers.openai.com/api/docs/guides/tools-file-search

## Postgres Baseline

Postgres full-text search plus pgvector keeps registry metadata, lexical search, vector search, and transactional state near each other for a small POC. pgvector documents hybrid search with full-text search, Reciprocal Rank Fusion, cross-encoder reranking, approximate indexes, and exact reranking.

Source: https://github.com/pgvector/pgvector

## Search Cluster

OpenSearch supports hybrid query pipelines that normalize and combine lexical and neural results. Use when operational search scale or existing search infrastructure justifies cluster complexity.

Source: https://github.com/opensearch-project/neural-search

## Graph Experiment

Microsoft GraphRAG offers local entity search, global community-report search, DRIFT, and a basic vector comparison. Its index extracts entities, relationships, claims, communities, and summaries and may be expensive. Start with a bounded subset and the same queries as the non-graph baseline.

Source: https://github.com/microsoft/graphrag

## Decision Record

For every implementation, record:

```text
why this corpus and query mix need it
data and access model
rebuild procedure
version and license
measured quality latency and cost
exit and migration plan
```
