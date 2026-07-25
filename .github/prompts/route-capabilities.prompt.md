---
name: route-capabilities
description: Route a task to the smallest sufficient repository Skill without executing the routed task.
argument-hint: "[task request; optional stage, role, and desired output]"
agent: delivery-capability-conductor
tools: ['execute/runInTerminal', 'search/codebase']
---

Read the small routing kernel in `AGENTS.md`. Use the complete user request as input and run:

```bash
python scripts/route_capabilities.py --root . --request "${input:task}" --mode assist
```

Return the routing status, selected Skill, matched signals, alternative candidates, progressive load plan, human confirmations, stop conditions, and warnings.

Do not execute the routed domain task, edit unrelated files, or load unselected Skill bodies.
