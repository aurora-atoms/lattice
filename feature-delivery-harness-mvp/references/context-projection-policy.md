# Context Projection Policy

```text
PROJ.001 | MUST  | input  | summarize_raw_sources_into_bounded_records_before_model_visible_use | enforce
PROJ.002 | NEVER | input  | include_full_logs_full_diffs_full_traces_or_raw_exports | block
PROJ.003 | MUST  | refs   | preserve_source_refs_without_copying_raw_source | enforce
PROJ.004 | SHOULD| size   | prefer_small_task_specific_context_over_broad_repo_context | prefer
```
