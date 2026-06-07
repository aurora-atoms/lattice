# Feature Delivery Harness Kernel Rules

```text
FDH.KER.001 | MUST  | naming | Lattice is project display name only; project_id=lattice; namespace=lat; never use lattice as module, agent, schema, artifact, skill, or record name. | block
FDH.KER.002 | MUST  | primary-object | feature_delivery_case is the primary value unit and core artifact for delivery analysis. | reject
FDH.KER.003 | MUST  | evidence | PR, commit, CI, review, merge, and release are evidence attached to feature_delivery_case, not final value units. | reject
FDH.KER.004 | NEVER | metrics | PR count, code volume, token count, test count, or agent activity are not final value metrics. | block
FDH.KER.005 | MUST  | architecture | Separate instruction, skill, reference, schema, script, eval, runtime ledger, and report layers. | block
FDH.KER.006 | NEVER | prompt-context | Raw repo dumps, Jira exports, OTel spans, logs, PR diffs, CI logs, or bulk tool output do not enter default prompt context. | block
FDH.KER.007 | MUST  | context-projection | Project raw sources into bounded context packs before model-visible use. | reject
FDH.KER.008 | MUST  | agent-io | Runtime and handoff records use JSONL; one line is one record. | reject
FDH.KER.009 | MUST  | agent-io | Every record includes type, id, schema, source, target, scope, payload, constraints. | reject
FDH.KER.010 | MUST  | schema | Unknown type, schema mismatch, missing required field, invalid enum, unknown field, duplicate id, and raw dump markers are rejected. | reject
FDH.KER.011 | MUST  | deliveryyield | DeliveryYield only produces token economics, stage breakdowns, waste patterns, optimization signals, and dossier output. | block
FDH.KER.012 | NEVER | deliveryyield | DeliveryYield must not approve delivery, override verifier verdicts, execute coding, route models, or replace verifier boundaries. | block
FDH.KER.013 | MUST  | token-cost | Token and cost values preserve status: unknown, estimated, provider_reported, known. | reject
FDH.KER.014 | MUST  | report-claims | Every material report claim cites evidence_refs or renders unknown/insufficient_evidence. | reject
FDH.KER.015 | MUST  | promotion | Candidates remain candidate-scoped until explicit reviewed promotion. | review
FDH.KER.016 | NEVER | promotion | Do not automatically promote candidates into long-term artifacts. | block
FDH.KER.017 | MUST  | ip-boundary | Personal/generalized artifacts use synthetic or open examples by default. | review
FDH.KER.018 | NEVER | ip-boundary | Do not store or reuse raw company code, Jira, PRs, architecture, traces, logs, screenshots, customer data, or metrics. | block
FDH.KER.019 | MUST  | mvp | MVP acceptance requires a runnable feature_delivery_case loop, not a documentation pack. | block
FDH.KER.020 | SHOULD | sequencing | Implement validators and fixtures before polishing skills, references, dashboards, or orchestration. | prefer
```
