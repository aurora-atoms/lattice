<!-- generated_from: runtime-adapters/google-workspace/senior-attention/adapter-source.v1.json -->
<!-- adapter_version: 1.1.1 -->
<!-- adapter_source_hash: sha256:1a2f0a73c4f6a3dc755755f87f9ac0a851c216f25d5cbcddb95cdc2faa0c6cdb -->
<!-- target: notebook -->

# NotebookLM Setup — Source-Grounded Synthesis Station

## Purpose

Use one restricted notebook for one bounded delivery/decision case or tightly related evidence set. NotebookLM is a synthesis surface, not a global enterprise search layer, code executor, or delivery authority.

## Source selection

Before adding sources, record the source owner, purpose, authority scope, freshness, access state, and selection reason in the private downstream source manifest. Keep stale, inaccessible, excluded, and superseded sources visible instead of silently deleting their status.

Recommended source set is intentionally small: the minimum approved documents needed to answer the target question. Do not mirror an entire Drive, mailbox, repository, or chat history.

## Notebook configuration

1. Give the notebook a case-scoped name.
2. Add only approved sources for that case.
3. Paste the generated custom-chat template into NotebookLM customization when supported.
4. Use the prompt cards for the selected Senior Attention task family.
5. Require citations for source-supported claims.
6. If a material claim is unsupported, mark it UNKNOWN or request another approved source.
7. Export only a candidate synthesis and explicit repository/runtime verification request to the private human-handoff step. The receiving coding workspace chooses capabilities through its own native discovery.

## Stop conditions

Stop when source access is missing, source freshness is unresolved, material sources conflict, a prompt asks to override the candidate authority ceiling, or the requested conclusion requires code execution / private system verification outside NotebookLM.
