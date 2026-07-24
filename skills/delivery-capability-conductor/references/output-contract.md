# Routing Output Contract

Emit compact JSON or equivalent structured Markdown with these fields:

```json
{
  "route_status": "routed|needs_input|human_decision_required|complete",
  "feature_delivery_case_id": "string|unknown",
  "role": "string",
  "stage": "understand|prepare|implement|review|release|outcome|learn",
  "condition": "blocked|unknown|conflicting|risk_accumulating|decision_needed|communication_needed|complete",
  "desired_outcome": "string",
  "selected_capabilities": [
    {"id":"string","kind":"skill|agent|pack","reason":"string","required":true}
  ],
  "required_context": {
    "files": [], "line_ranges": [], "symbols": [], "tests": [], "risks": [], "evidence_refs": []
  },
  "human_confirmations": [],
  "stop_conditions": [],
  "write_back": [],
  "evidence": {"facts": [], "inferences": [], "unknowns": []}
}
```

CONTRACT.001 | MUST | reject_unknown_top_level_fields_when_schema_validation_is_enabled | enforce
CONTRACT.002 | MUST | keep_selected_capabilities_ordered_and_minimal | enforce
CONTRACT.003 | MUST | include_reason_for_each_selected_capability | enforce
CONTRACT.004 | MUST | include_stop_conditions_and_human_confirmations | enforce
CONTRACT.005 | NEVER | encode_raw_logs_or_full_documents_in_routing_record | block
