---
name: route-capabilities
description: Diagnose or explicitly route a task when native Skill selection is unavailable, ambiguous, or appears incorrect; do not use as mandatory preflight for every task.
argument-hint: "[task request; optional stage, role, desired output, and observed native selection]"
agent: delivery-capability-conductor
tools: ['execute/runInTerminal', 'search/codebase']
---

Use the active runtime's native Skill discovery first for ordinary work. Invoke this prompt only to:

- debug a suspected false positive or false negative;
- compare an observed native selection with the expected repository route;
- route in a runtime that lacks native Skill discovery;
- generate deterministic expected-route evidence for an evaluation.

Read the thin guidance in `AGENTS.md`, then run:

```bash
python scripts/route_capabilities.py --root . --request "${input:task}" --mode assist
```

Return:

```text
observed_native_selection
expected_route
comparison = match | false_positive | false_negative | ambiguous | unnecessary_composition | unknown
selected_or_recommended_skill
matched_signals
alternative_candidates
progressive_load_plan
human_confirmations
stop_conditions
warnings
```

Do not execute the routed domain task, edit unrelated files, load unselected Skill bodies, or imply that the fallback router overrides native permissions or human authority.
