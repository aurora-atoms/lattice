# Systematic Invention Research Stack

## Decision

Use a public-only, evidence-first research workflow to convert published patents and other public technical sources into reusable technique knowledge, deliberate-practice material, and portable Agent Skills.

This is a reference workflow and authoring guide, not a new Lattice module and not a claim that a generated idea is patentable, novel, non-infringing, or free of prior art.

```text
public scope
-> corpus and coverage
-> triage
-> claim/mechanism reconstruction
-> technique patterns
-> challenger-backed gap hypotheses
-> deliberate practice
-> portable Agent Skill
-> held-out evaluation
-> synthesis / revise / reject
```

The workflow follows Lattice's existing rules: evidence before assertion, smallest sufficient capability, progressive disclosure, deterministic validation where possible, human authority, and no automatic promotion from one successful run.

## Global IP Firewall

This workflow may process only:

- published patents and patent applications;
- public papers, standards, product documentation, and public repositories;
- information the user explicitly marks as public;
- fully synthetic examples.

Stop concrete technical analysis when an input contains or plausibly contains:

- an employer's or client's non-public design, source code, architecture, experiment, dataset, roadmap, or invention;
- an unfiled or unpublished real invention concept;
- NDA, confidential, privileged, export-controlled, or otherwise restricted material.

Do not try to bypass the boundary by removing a company name, paraphrasing, or "making it abstract." Replace the input with a public or synthetic version first.

Every research output must distinguish:

- `FACT`: directly supported by a cited public source;
- `INFERENCE`: derived from one or more cited facts;
- `HYPOTHESIS`: an unverified gap, design opportunity, or research proposition.

Never convert `HYPOTHESIS` into a legal conclusion such as "patentable," "novel," "no prior art," "FTO clear," or "non-infringing."

## Phase Contract

### P00 — Research Orchestrator

Freeze:

- `research_topic`;
- `research_question`;
- jurisdictions and time window;
- target corpus size and depth budget;
- output workspace;
- public-source boundary.

Do not jump directly to invention generation.

### P01 — Corpus Builder

Build recall through multiple independent paths:

1. keywords and semantic search;
2. CPC/IPC classification;
3. backward/forward citation chains;
4. assignee, inventor, and patent-family neighborhoods.

De-duplicate by patent family. Record `query_log`, `retrieval_paths`, `inclusion_reason`, and explicit coverage gaps.

Primary outputs:

```text
patent_corpus_manifest.jsonl
search_coverage_report.md
```

### P02 — Triage Reader

Read broadly before reading deeply. Recommended order:

```text
bibliographic metadata
-> title and abstract
-> independent claims
-> representative figures/descriptions
-> relevant background/summary
-> detailed description only when needed
```

Do not count multiple publications from the same patent family as independent technical evidence.

Primary output: Patent Card L1 with relevance, uniqueness, deep-read priority, evidence refs, and uncertainty.

### P03 — Claim & Mechanism Reverse Engineer

For high-value families:

- decompose each independent claim into atomic limitations;
- model sequence, dependency, data flow, control flow, structural relation, and conditions;
- map claim elements to mechanism descriptions and figures;
- separate `CLAIMED`, `DESCRIBED`, `BACKGROUND`, and `OPTIONAL` content;
- identify design variables and addressed failure modes.

Primary output: Patent Card L2 / mechanism model.

### P04 — Technique Pattern Miner

Promote a mechanism pattern only when multiple independent patent families support it, unless explicitly marked `single_example_candidate`.

A technique pattern should describe:

```text
problem class
mechanism
preconditions
constraints
tradeoffs
failure modes
variation dimensions
supporting independent families
counterexamples / limits
```

Do not reduce the pattern to a theme, buzzword, assignee, or citation count.

### P05 — Landscape & Gap Finder

Map both:

- problem space;
- mechanism space.

A gap is only a `HYPOTHESIS`. Every gap hypothesis requires a challenger task that searches for counterexamples, alternate terminology, neighboring classifications, citation paths, and older mechanisms.

Primary outputs:

```text
landscape_map.md
invention_gap_hypotheses.jsonl
```

### P06 — Deliberate Practice

Turn stable patterns into exercises that train a human to:

- identify a mechanism from evidence;
- reconstruct a claim into atomic elements;
- compare nearest mechanisms;
- propose an alternate mechanism using synthetic/public inputs;
- search for the strongest counterexample;
- explain what evidence would falsify a gap hypothesis.

Primary output: `deliberate_practice_set.md`.

### P07 — Portable Agent Skill Builder

Create a Skill only after the workflow is stable enough to repeat.

The Skill should contain control logic, triggers, evidence discipline, stop rules, and output contracts. Keep large patent corpora, cases, and references outside `SKILL.md` and load them progressively.

Use `templates/systematic-invention-research-agent-skill/SKILL.md` as the portable starting point.

### P08 — Held-Out Evaluation

A Skill is not a trusted research tool because its instructions look good.

Evaluate on held-out cases that were not used to author the Skill. Include:

- should-trigger and should-not-trigger cases;
- public/private boundary cases;
- same-family duplicate traps;
- abstract-only traps;
- claim-vs-description traps;
- weak-gap / prior-art counterexample traps;
- unsupported novelty/legal-conclusion traps;
- multilingual or alternate-terminology cases when relevant.

Record failures, not only scores.

### P09 — Synthesis

Periodically decide for each pattern, hypothesis, and Skill:

```text
promote
revise
retain_candidate
reject
```

Promotion requires bounded scope, source lineage, successful held-out behavior, visible limitations, and human review.

## Evidence Package

Recommended durable outputs:

```text
patent_corpus_manifest.jsonl
patent_cards.jsonl
technique_patterns.jsonl
landscape_map.md
invention_gap_hypotheses.jsonl
deliberate_practice_set.md
skill_pack/
eval_cases.jsonl
synthesis_report.md
```

For every important claim, retain a `source_ref`. Prefer publication identifiers, stable public URLs, claim numbers, figure numbers, page/paragraph locators, or repository commit references over prose such as "the patent says."

## Cross-Runtime Agent Skill Deployment

Keep one canonical portable Skill body and use thin runtime projections. Re-verify vendor behavior from current official documentation before installation because paths and runtime semantics can change.

### GitHub Copilot / VS Code

Current GitHub and VS Code documentation supports project Agent Skills under `.github/skills/<skill-name>/SKILL.md`, `.agents/skills/<skill-name>/SKILL.md`, or compatible skill locations. Copilot loads matching skills on demand rather than requiring the whole body in every prompt.

Recommended project projection:

```text
.github/skills/systematic-invention-research/
  SKILL.md
  references/
  scripts/
  assets/
```

Use the runtime's native Skill discovery first. Do not require a custom router before every research task.

### Gemini CLI

Current Gemini CLI documentation supports workspace Agent Skills under `.gemini/skills/<skill-name>/SKILL.md` and the portable `.agents/skills/<skill-name>/SKILL.md` alias. Gemini CLI also supports user-scoped skills and native Skill management/discovery.

Recommended portable projection:

```text
.agents/skills/systematic-invention-research/
  SKILL.md
  references/
  scripts/
  assets/
```

Use `.agents/skills/` when the same package is intended to be shared across compatible runtimes; use a runtime-specific directory only when a runtime-specific behavior is genuinely required.

### Other Agent-Skills-Compatible Runtimes

Prefer the open Agent Skills directory contract:

```text
<skill-name>/
  SKILL.md
  references/
  scripts/
  assets/
```

Keep vendor-specific permissions, hooks, model choices, tools, or session behavior in a thin adapter. Do not fork the research method into multiple independent versions unless behavior actually differs.

## Skill Authoring Rules

A portable research Skill should have:

- narrow `name` and discovery-oriented `description`;
- explicit public-only input contract;
- `FACT / INFERENCE / HYPOTHESIS` discipline;
- patent-family de-duplication rule;
- independent-claim requirement for high-value samples;
- challenger requirement before gap claims;
- visible structured outputs and evidence refs;
- held-out evaluation cases;
- clear stop conditions.

Large reference knowledge belongs in `references/` or external evidence files. Deterministic normalization, family de-duplication, schema checks, statistics, and report scaffolding belong in scripts when practical.

## Evidence Collection Contract

For each run, collect a compact research receipt rather than a raw transcript. At minimum record:

```json
{
  "record_type": "research.evidence_receipt",
  "run_id": "...",
  "capability": "systematic-invention-research",
  "runtime": "github-copilot|gemini-cli|other",
  "research_question": "...",
  "public_scope_confirmed": true,
  "sources": [
    {
      "source_ref": "...",
      "source_type": "patent|paper|standard|public_product|public_repo",
      "family_id": "optional",
      "locator": "claim/figure/page/paragraph/commit"
    }
  ],
  "claims": [
    {
      "statement": "...",
      "status": "FACT|INFERENCE|HYPOTHESIS|UNKNOWN",
      "source_refs": ["..."],
      "confidence": "high|medium|low"
    }
  ],
  "artifacts": ["..."],
  "challenge_tasks": ["..."],
  "eval_case_refs": ["..."],
  "limitations": ["..."],
  "stop_reason": "..."
}
```

Do not store hidden chain-of-thought or raw model reasoning as evidence. Store observable sources, structured claims, tool results, artifact references, uncertainty, failures, and decisions.

## Promotion Rules

A technique pattern, gap hypothesis, or Skill must never be promoted merely because:

- many documents were read;
- the model sounded confident;
- several agents agreed;
- a patent was highly cited;
- one example worked;
- a long report was generated.

Promotion should be based on source-backed mechanism understanding, independent-family support where required, challenger results, held-out evaluation, known limitations, and accountable human review.

## Stop Conditions

Stop and request a public/synthetic replacement when the IP firewall fails.

Stop or downgrade to `UNKNOWN` when:

- independent claims needed for a key conclusion are unavailable;
- family identity cannot be resolved sufficiently to avoid double-counting;
- a key claim lacks a source reference;
- a gap has not received a meaningful challenger search;
- the requested conclusion is legal rather than technical/research-oriented;
- the held-out evaluation exposes a critical false-ready behavior;
- source access, language coverage, or search coverage is insufficient for the requested confidence.

The correct result can be `insufficient_evidence`; do not fill missing evidence with plausible prose.
