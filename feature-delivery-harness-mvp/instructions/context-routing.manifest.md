# Context Routing

```text
CTX.001 | MUST  | handoff | use_jsonl_plus_json_schema_for_agent_handoff | enforce
CTX.002 | MUST  | runtime | use_append_only_jsonl_for_runtime_ledgers | enforce
CTX.003 | SHOULD| report  | use_markdown_for_manager_facing_dossiers | prefer
CTX.004 | NEVER | prompt  | expose_raw_logs_traces_diffs_or_bulk_tool_output_by_default | block
CTX.005 | MUST  | prompt  | use_bounded_context_projection_before_model_visible_context | enforce
```
