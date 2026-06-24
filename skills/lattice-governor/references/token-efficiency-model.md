# Token Efficiency Model

## Definition

Token efficiency means quality-adjusted output per token cost. Do not optimize by deleting behavior-critical constraints, rejection rules, safety rules, or verification steps.

## Progressive Loading

```text
metadata description -> SKILL.md control plane -> targeted reference/schema/eval/script -> broader search only if needed
```

## Context Placement

TOKEN.001 | MUST  | skill      | keep SKILL.md as control plane, not knowledge dump
TOKEN.002 | SHOULD | reference | move background, examples, variants, rationale to topic-scoped references
TOKEN.003 | SHOULD | schema    | use JSON Schema or Structured Outputs for machine boundaries
TOKEN.004 | SHOULD | eval      | keep eval cases machine-readable + small
TOKEN.005 | NEVER | prompt    | dump entire skill library when inventory or targeted lookup suffices
TOKEN.006 | NEVER | rewrite   | reduce tokens by deleting safety or failure behavior
Use stable prefix content for repeated batch work:

```text
project identity
current scope and non-goals
format routing policy
frontmatter preservation policy
description trigger policy
registry contract
eval contract
validation gates
output format
```

Use dynamic suffix content for:

```text
target skill path
inventory record
targeted source excerpts
validator output
eval output
requested change
```

## Compact Rule Form

Prefer:

```text
ID | LEVEL | SCOPE | STATEMENT | ENFORCEMENT
```

Avoid long paragraphs for machine-facing control rules.

## Bulk Context Projection

When passing many registry records or eval cases into a model, use schema-once compact rows:

```text
@skillreg:v1 id,status,path,risk,trigger,output,notes
s1,active,skills/example,low,pass,pass,"validated"
s2,candidate,candidates/new,medium,pending,pending,"needs review"
```

Keep full JSONL as storage; use compact rows only as model-visible projection when appropriate.

## Refactor Heuristic

```text
if content changes behavior -> keep or move with explicit reference
if content is background -> references
if content is repeated deterministic procedure -> script
if content is machine boundary -> schema
if content is quality evidence -> eval
if content is historical narrative -> report or archive
```
