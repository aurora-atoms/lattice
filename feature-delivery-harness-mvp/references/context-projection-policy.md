# Context Projection Policy

```text
PROJ.001 | MUST  | input  | summarize raw sources into bounded records before model-visible use
PROJ.002 | NEVER | input  | include full logs, diffs, traces, or raw exports
PROJ.003 | MUST  | refs   | preserve source_refs without copying raw source
PROJ.004 | SHOULD| size   | prefer small task-specific context over broad repo context
```
