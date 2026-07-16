# Profile and Access Contract

## Task Profile

Compose only:

```text
profile ID and version
task types and caller roles
knowledge contract and allowed scopes
projection IDs
skill and tool allowlists
read write and approval policy
context budget and citation policy
output schema
eval dataset and baseline
```

Exclude private task content and secrets from the profile. Resolve environment-specific endpoints in deployment configuration.

## Stable Hash

Canonicalize sorted JSON with stable IDs and versions. Hash invariant fields only:

```text
task types roles scopes projection IDs skills tools policy output schema eval version
```

Do not hash timestamps, absolute local paths, random run IDs, user questions, retrieved chunks, or secrets into the profile identity.

## MCP Boundary

- Start with read-only resources and tools.
- Name every allowed tool; reject wildcard capability groups when finer scopes exist.
- Bind the user and target resource in authorization.
- For HTTP authorization, validate token audience and use a separate token for downstream APIs.
- Require explicit elevation for write, deploy, secret, shell, and destructive operations.
- Log decisions and identifiers; redact content unless an approved diagnostic mode requires it.

MCP connects an agent to tools and resources. It does not define which organizational knowledge is authoritative or how all prompt context is managed.

## Context Pack

Select evidence after authorization and before generation. Preserve:

```text
profile and query IDs
caller role and access decision reference
knowledge object and chunk IDs
source locators and versions
rank and retrieval stage
status freshness and conflict state
token count and truncation reason
```

If the context budget excludes material evidence, return the omission explicitly or abstain.
