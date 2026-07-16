# Industry Evidence Map

Checked: 2026-07-16. Reverify version-sensitive claims before implementation.

## Primary Standards and Product Documentation

- W3C PROV-O defines Entity, Activity, Agent, derivation, generation, attribution, revision, and primary-source relations. Apply it as a provenance vocabulary, not as a requirement to deploy RDF: https://www.w3.org/TR/prov-o/
- MCP authorization requires audience-bound tokens; its security guidance forbids token passthrough, recommends narrow scopes, and describes confused-deputy and SSRF controls: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization and https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices
- OpenAI File Search combines semantic and keyword search, returns file citations, and supports metadata filters. Treat it as one replaceable projection implementation: https://developers.openai.com/api/docs/guides/tools-file-search
- OpenAI prompt caching requires exact prefix matches; keep static rules before variable task data: https://developers.openai.com/api/docs/guides/prompt-caching
- OpenTelemetry GenAI conventions include retrieval operations and retrieval-document identifiers/scores, but several fields are experimental or privacy-sensitive. Pin the semantic-convention version and avoid recording content by default: https://opentelemetry.io/docs/specs/semconv/ and https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/
- A2A models discovery, tasks, messages, and artifacts between independently operated agents. Do not substitute it for agent-to-tool access: https://a2a-protocol.org/dev/specification/

## Maintained Implementations

- pgvector documents Postgres vector similarity, Postgres full-text hybrid search, Reciprocal Rank Fusion, and reranking: https://github.com/pgvector/pgvector
- Microsoft GraphRAG separates indexing from local, global, DRIFT, and basic search; its repository warns that indexing may be expensive and recommends starting small: https://github.com/microsoft/graphrag
- DeepEval separates retriever and generator evaluation and supports contextual precision, recall, relevance, faithfulness, tool correctness, and CI execution: https://github.com/confident-ai/deepeval
- Ragas provides alternative RAG metric implementations. Treat LLM-judge metrics as versioned evaluators, not ground truth: https://github.com/vibrantlabsai/ragas

## Evidence-Based Defaults

- Baseline with lexical plus semantic retrieval, deterministic fusion, metadata/ACL filtering, citations, and optional reranking.
- Preserve original chunk text and source locator; any contextualized text is a derived field.
- Evaluate retrieval separately from answer generation.
- Use graph only when the query mix needs entity-centric multi-hop or corpus-wide synthesis and the same dataset shows net gain.
- Keep observability metadata low-cardinality and content capture opt-in because prompts, queries, and retrieved text may be sensitive.

Anthropic reports improved recall from contextual embeddings plus contextual BM25 and further improvement from reranking, but its results are dataset-specific rather than a universal guarantee: https://www.anthropic.com/engineering/contextual-retrieval
