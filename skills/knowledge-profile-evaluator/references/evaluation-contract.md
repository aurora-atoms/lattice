# Evaluation Contract

## Dataset

Create 20-30 cases for a small POC and version them. Suggested subsets:

```text
exact identifier and title lookup
semantic paraphrase
multi-document synthesis
conflicting active sources
stale or superseded source
unauthorized source
no supported answer
instruction or prompt injection inside a source
tool selection and argument boundary
task artifact completion
```

Each case identifies caller role, expected source IDs, prohibited source IDs, answer assertions, citation assertions, and expected abstention or permission result.

## Component Metrics

- Retrieval recall@k: relevant authorized items retrieved / relevant authorized items labeled.
- Retrieval precision@k or contextual precision: relevant authorized retrieved items / retrieved items.
- Citation validity: citations resolving to the expected source version / citations emitted.
- Material-claim citation coverage: supported material claims with valid citations / material claims requiring evidence.
- Permission correctness: cases with expected allow or deny result / permission cases.
- Freshness/conflict detection: correct typed result / corresponding cases.
- No-answer correctness: abstentions without unsupported claims / no-answer cases.

Use deterministic labels where possible. Version model-based graders and retain a human-reviewed sample because judge outputs are estimates.

## System Metrics

- task success against an explicit output contract;
- human correction or rework;
- p50, p95, and timeout rate;
- prompt, cached, retrieval, reranking, tool, and output cost;
- delivery outcome appropriate to the workflow.

Token reduction is not success if permission, citation, or task quality regresses.

## Promotion Gate

```text
critical permission leak = 0
schema and deterministic checks = pass
baseline delta reported for every critical subset
no-answer and stale/conflict behavior = pass threshold
source citations = resolvable
latency and cost = within declared budget
human review = complete for high-impact tasks
```

Thresholds are project choices. Never label suggested percentages as industry standards.

## Expansion Gates

- Graph: key multi-hop or global cases fail baseline and graph projection improves the frozen subset after added indexing/runtime cost.
- A2A: separately operated agents require discovery, task ownership, state, and artifact exchange; ordinary tool calls remain MCP.
- Writes: read-only quality is stable and each write has authorization, approval policy, idempotency, audit, rollback, and failure tests.

## Telemetry

Pin the OpenTelemetry semantic-convention version. Record profile, projection, model, tool, operation, token, cost, latency, outcome, and evaluation identifiers with low cardinality. Treat queries, retrieved documents, prompts, tool arguments, and results as sensitive opt-in fields.
