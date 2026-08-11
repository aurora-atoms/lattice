<!-- generated_from: runtime-adapters/google-workspace/senior-attention/adapter-source.v1.json -->
<!-- adapter_version: 1.1.1 -->
<!-- adapter_source_hash: sha256:1a2f0a73c4f6a3dc755755f87f9ac0a851c216f25d5cbcddb95cdc2faa0c6cdb -->
<!-- target: workspace_studio -->

# Senior Attention Manual / Shadow Skill — Workspace Studio

## Operating mode

Use this as a manual or shadow workflow. A user explicitly starts the run and reviews the candidate before any downstream action. `Ask a Gem` may be used only when the target account actually exposes it.

## Default action policy

- automatic send: **off**
- automatic share: **off**
- automatic delete: **off**
- ticket or file write: **off**
- manager post: **off**
- cross-domain or irreversible action: **off**
- web or broad external source expansion: **off unless the user explicitly authorizes it for the case**

## Steps

1. Capture one bounded target and one Senior Attention task family.
2. Record which Workspace sources are selected, unavailable, excluded, and unknown.
3. Gather only the minimum authorized evidence.
4. Separate source-supported claims from inference.
5. Preserve conflicts, unknowns, and strongest counterevidence.
6. Draft a candidate artifact plus the repository/runtime verification required after handoff.
7. Stop for human review. Do not send, write, approve, or publish as part of this public projection.

## Candidate output

Return only a candidate. Preserve these sections explicitly:

1. TARGET — the bounded question or task.
2. SOURCE SCOPE — selected, unavailable, excluded, and not-searched/unknown sources.
3. CLAIMS — source-supported facts separated from inference.
4. UNKNOWNS — missing evidence or access.
5. CONFLICTS — incompatible source statements that could change the answer.
6. STRONGEST COUNTEREVIDENCE — the best evidence against the leading interpretation.
7. PROPOSALS — required repository/runtime verification and any draft artifact, clearly labeled as proposed and not verified.
8. AUTHORITY — `candidate`; human confirmation required.
9. PRIVACY — keep private locators, content, and real case evidence downstream.

If a material claim lacks support, downgrade it to UNKNOWN or stop. Never claim complete enterprise search. The receiving coding workspace owns capability discovery and must independently verify repository, test, configuration, dependency, reproduction, runtime, root-cause, and readiness claims.
