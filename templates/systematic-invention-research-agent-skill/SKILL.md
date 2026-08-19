---
name: systematic-invention-research
description: Use for public-only patent and technical-literature research that builds an evidence-backed corpus, reconstructs independent claims and mechanisms, mines recurring technique patterns, challenges apparent gaps, creates deliberate-practice material, and evaluates reusable research Skills. Inputs must be published/public or fully synthetic. Do not use for employer/client confidential material, unpublished real inventions, legal patentability/FTO/infringement conclusions, or unsupported novelty claims.
---

# Systematic Invention Research

## Goal

Convert public technical evidence into reusable mechanism knowledge and validated research procedure without jumping directly from search results to invention claims.

Default sequence:

```text
scope
-> corpus
-> triage
-> claims/mechanisms
-> technique patterns
-> challenged gap hypotheses
-> deliberate practice
-> held-out evaluation
-> synthesis
```

## Public-Only Gate

Allowed inputs:

- published patents and patent applications;
- public papers, standards, public product documentation, and public repositories;
- information explicitly marked public by the user;
- fully synthetic examples.

Stop if the task contains or plausibly contains confidential employer/client material, internal source code or architecture, private experiments/data, an unpublished real invention, or material governed by NDA/confidentiality obligations.

Do not continue by anonymizing, paraphrasing, or abstracting the private material. Ask for a public or synthetic replacement.

## Inputs

Minimum:

- research topic;
- research question;
- confirmation that concrete technical inputs are public or synthetic;
- desired jurisdictions or source domains when relevant.

Optional:

- time window;
- target corpus size;
- depth budget;
- existing seed publications;
- prior public corpus manifest;
- held-out evaluation set.

## Workflow

### 1. Scope

Freeze the research question, evidence boundary, search scope, and stopping criteria before broad retrieval.

### 2. Build the corpus

Use multiple independent retrieval paths when possible:

- keyword / semantic;
- CPC / IPC classification;
- backward / forward citations;
- assignee / inventor / patent-family neighborhood.

Record search queries and coverage gaps. De-duplicate by patent family.

### 3. Triage before deep reading

Read metadata, title/abstract, independent claims, representative figures, and only then the detailed description needed to explain the mechanism.

Rank deep-read priority by relevance, uniqueness, representativeness, and information gain.

### 4. Reverse engineer claims and mechanisms

For high-value samples:

- decompose independent claims into atomic limitations;
- model relationships among elements;
- map limitations to described mechanisms and figures;
- keep `CLAIMED`, `DESCRIBED`, `BACKGROUND`, and `OPTIONAL` separate;
- identify constraints, failure modes, dependencies, and design variables.

Never substitute an abstract for the independent claims when the claim scope matters.

### 5. Mine technique patterns

A stable pattern should normally be supported by multiple independent patent families. If not, mark it `single_example_candidate`.

Describe the mechanism, not merely the topic.

### 6. Build and challenge gap hypotheses

A gap is a `HYPOTHESIS`, not a conclusion.

Before retaining it, search for the strongest counterexample using alternate terminology, nearby classifications, citations, older mechanisms, and neighboring problem formulations.

### 7. Create deliberate practice

Create exercises that require the human learner to reconstruct claims, identify mechanisms, compare neighbors, generate public/synthetic alternatives, and falsify weak gap hypotheses.

### 8. Evaluate the procedure

Use held-out cases that were not used to write this Skill. Include should-not-trigger, private-input, family-duplicate, abstract-only, claim/description-confusion, weak-gap, and unsupported-legal-conclusion cases.

### 9. Synthesize

For each important pattern, hypothesis, or workflow element choose:

```text
promote
revise
retain_candidate
reject
```

Do not auto-promote from one run.

## Outputs

Prefer compact, durable artifacts:

```text
patent_corpus_manifest.jsonl
patent_cards.jsonl
technique_patterns.jsonl
landscape_map.md
invention_gap_hypotheses.jsonl
deliberate_practice_set.md
eval_cases.jsonl
synthesis_report.md
research_evidence_receipts.jsonl
```

When filesystem write access is available, write to the user-selected research workspace. Otherwise return the smallest complete structured result inline.

## Evidence

For each load-bearing technical statement record:

- `FACT`, `INFERENCE`, `HYPOTHESIS`, or `UNKNOWN`;
- one or more `source_ref` values when evidence exists;
- a stable locator such as publication ID, claim, figure, page/paragraph, standard section, or commit;
- confidence and important uncertainty;
- patent-family identity where double-counting is possible.

Do not store hidden chain-of-thought as evidence. Store observable source material, tool results, structured claims, artifacts, failures, and decisions.

## Success Signals

A run is successful only to the extent that observable evidence supports it. Evaluate at least:

- the corpus has recorded retrieval paths and coverage gaps;
- duplicate family publications are not counted as independent evidence;
- high-value patent analysis checks independent claims;
- claimed content is not conflated with merely described/background/optional content;
- technique patterns expose supporting independent families and limitations;
- each retained gap hypothesis has a challenger result or is explicitly pending challenge;
- important statements have source refs or are marked `UNKNOWN`;
- held-out failures are recorded rather than hidden;
- no legal patentability/FTO/infringement conclusion is asserted.

## Stop Conditions

Stop when:

- the public-only gate fails;
- required source access is unavailable;
- evidence is insufficient for the requested confidence;
- family identity cannot be resolved enough to avoid material double-counting;
- independent claims required for the conclusion are unavailable;
- a challenger search cannot be performed for a gap that depends on it;
- the user requests a legal conclusion about patentability, FTO, infringement, or claim construction;
- a held-out case exposes a critical false-ready behavior that must be fixed before promotion;
- the requested research stage is complete.

A valid terminal result is `insufficient_evidence`.

## Runtime Notes

Keep this `SKILL.md` runtime-neutral. Put vendor-specific permissions, hooks, tools, model selections, or session rules in thin adapters.

For current runtime installation locations and commands, verify official documentation before deployment. Common portable project layouts include `.agents/skills/systematic-invention-research/`, with runtime-native alternatives such as `.github/skills/` for GitHub Copilot-compatible environments and `.gemini/skills/` for Gemini CLI.
