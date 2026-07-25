# Repository Capability Harness

Use this file as the small always-on routing kernel. Do not copy full Skill bodies, reference documents, tool catalogs, or repository context into this file.

## Before Substantive Work

1. Identify the requested visible outcome, lifecycle stage, role, evidence state, permission boundary, and action risk.
2. Run or consume the deterministic route:

```bash
python scripts/route_capabilities.py --root . --request "<task request>" --stage "<stage>" --role "<role>" --desired-output "<outcome>" --mode assist
```

3. Handle the result:
   - `auto_invoke`: load only the selected `SKILL.md`; continue only within its permissions.
   - `recommend`: tell the user which Skill is recommended and why; continue after scope is clear.
   - `ask`: stop for the named human decision, permission, or ambiguity.
   - `no_match`: do not load the catalog; clarify the outcome or use the conductor manually.
4. Apply progressive disclosure:

```text
routing metadata -> selected SKILL.md -> named references/scripts on demand -> bounded task context
```

5. Build a context pack containing only scope, files and line ranges, symbols, tests, risks, decisions, validation commands, and evidence refs needed for this task.
6. Re-route only after a meaningful state change, failed gate, or completed capability output.
7. Stop when the visible result is reached.

## Control Rules

HARNESS.001 | MUST | selection | choose one smallest sufficient capability before composing a chain
HARNESS.002 | MUST | context | keep stable policy separate from dynamic task evidence
HARNESS.003 | MUST | evidence | distinguish facts, inferences, conflicts, and unknowns
HARNESS.004 | MUST | control | preserve human authority for scope, security, compliance, architecture, merge, release, and production
HARNESS.005 | NEVER | catalog | load all Skills, Agents, tools, knowledge, logs, or repository files by default
HARNESS.006 | NEVER | modules | supersede Helixion, AegisFlow, Memexa, FlowGuard, OpenClaw, DeliveryYield, or another active module
HARNESS.007 | NEVER | metric | use routing, token, or agent activity for personnel ranking

Canonical routing policy lives in `registry/capability-routing.index.jsonl`; validation and decisions live in `scripts/validate_capability_routing.py` and `scripts/route_capabilities.py`.
