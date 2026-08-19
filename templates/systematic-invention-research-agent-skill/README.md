# Systematic Invention Research Agent Skill Template

This directory is a portable template for creating a public-only patent and technical-research Agent Skill in compatible runtimes.

It is intentionally not registered as a Lattice runtime Skill. The template is a downstream projection source: copy it into the target runtime's native Skill directory, keep the research method stable, and put runtime-specific behavior in thin local adapters.

## Canonical files

```text
SKILL.md
research-evidence-receipt.schema.json
```

Recommended downstream additions:

```text
references/
  public-source-policy.md
  research-topic-specific references
scripts/
  validate_evidence_receipt.py
  normalize_patent_family.py
  build_corpus_manifest.py
assets/
  patent-card.template.json
  technique-pattern.template.json
  eval-case.template.json
```

Do not place a complete patent corpus or raw research history inside `SKILL.md`.

## GitHub Copilot / VS Code

At the time this template was added, official GitHub and VS Code documentation supports repository Agent Skills in locations including:

```text
.github/skills/<skill-name>/SKILL.md
.agents/skills/<skill-name>/SKILL.md
```

A practical projection is:

```text
.github/skills/systematic-invention-research/
  SKILL.md
  research-evidence-receipt.schema.json
  references/
  scripts/
```

Then use Copilot's native Skill discovery. Do not add a mandatory repository router in front of every task.

Before deployment, verify the current GitHub/VS Code Agent Skills documentation and enterprise policy because supported paths, permissions, and consent behavior can change.

## Gemini CLI

At the time this template was added, official Gemini CLI documentation supports workspace Agent Skills in:

```text
.gemini/skills/<skill-name>/SKILL.md
.agents/skills/<skill-name>/SKILL.md
```

A practical portable projection is:

```text
.agents/skills/systematic-invention-research/
  SKILL.md
  research-evidence-receipt.schema.json
  references/
  scripts/
```

Gemini CLI also provides native Skill listing, installation, linking, enable/disable, and reload workflows. Prefer those native mechanisms over inventing a parallel Skill loader.

Before deployment, verify the current Gemini CLI Agent Skills documentation and local policy.

## Why `.agents/skills/` is useful

When multiple runtimes implement the Agent Skills open directory convention, `.agents/skills/` can be the shared workspace projection. This reduces drift between Copilot, Gemini CLI, and other compatible agents.

Do not force a common directory when a runtime needs materially different permissions, tools, hooks, or activation semantics. In that case keep the shared `SKILL.md` logic canonical and add a thin runtime-specific projection.

## Evidence collection

Each research run should append one compact evidence receipt rather than preserve raw chat history as the authoritative record.

Example:

```json
{
  "record_type": "research.evidence_receipt",
  "run_id": "sir-2026-08-18-001",
  "runtime": "gemini-cli",
  "research_question": "How do published systems implement bounded retry with external verification?",
  "public_scope_confirmed": true,
  "sources": [
    {
      "source_ref": "US-EXAMPLE-PUBLICATION",
      "source_type": "patent",
      "family_id": "family-example-1",
      "locator": "independent claim 1; figure 3"
    }
  ],
  "claims": [
    {
      "statement": "The claimed system requires an external verification signal before the next retry.",
      "status": "FACT",
      "source_refs": ["US-EXAMPLE-PUBLICATION"],
      "confidence": "high"
    },
    {
      "statement": "This mechanism may define a reusable bounded-retry pattern.",
      "status": "INFERENCE",
      "source_refs": ["US-EXAMPLE-PUBLICATION"],
      "confidence": "medium"
    }
  ],
  "artifacts": ["patent_cards.jsonl"],
  "challenge_tasks": ["Search earlier CPC neighbors for equivalent verification-gated retry mechanisms."],
  "eval_case_refs": [],
  "limitations": ["Only one independent family has been reviewed so far."],
  "stop_reason": "stage_gate_reached"
}
```

The example identifiers above are synthetic.

## Minimum evaluation set

Before treating a copied Skill as reliable, test at least:

1. a normal public patent-research request;
2. a request that should not trigger;
3. a same-family duplicate-publication trap;
4. an abstract-only trap where independent claims change the interpretation;
5. a claim-vs-description confusion case;
6. a weak apparent gap with an older counterexample;
7. an unsupported request to declare something patentable/novel;
8. a confidential or unpublished real-invention input that must stop;
9. a case with insufficient source access;
10. a held-out case not used while authoring the Skill.

Record failures as evidence and revise the Skill before broader use.
