# Evidence Wayfinding Blueprint — Preserved Source and Implementation Map

## Status

- Source blueprint: `Evidence_Wayfinding_Blueprint_CN(1).docx`
- Source evidence cutoff: `2026-08-07`
- Preservation status: source-aligned reference, not automatic runtime authority
- Repository status at preservation: PR #34 merged as commit `22c0ff6ce3a3b2f3d62b6bad5f1456415f867cf7`
- Active implementation entry: `docs/evidence-wayfinding.md`
- Public/private rule: this document preserves public-safe architecture, contracts, source identifiers, and deferred ideas. It does not vendor private source content or promote candidate ideas into active capabilities.

This file exists so later refactors do not silently lose the full design intent behind Evidence Wayfinding. It distinguishes three things:

1. **Source blueprint** — what the 2026-08-07 design explicitly proposed.
2. **Current repository state** — what is already implemented after PR #34.
3. **Deferred candidate work** — ideas intentionally retained without being promoted into active Skills or module boundaries.

## 1. Decision Summary

The blueprint recommends the public name **Evidence Wayfinding / 循证领航**. The metaphor is literal: define the destination, establish orientation, triangulate with independent landmarks, let humans choose at consequential forks, leave a trace, and update the map only after evidence supports reuse.

The source blueprint's central design decision is:

> Turn `decision-ready investigation mode` into a portable reference workflow rather than a new large module. Reuse existing capabilities for orientation, evidence gathering, challenge, adjudication, delivery, and learning. Add only one new atomic Skill, `frontier-practice-scout`, if the Direction Gate is actually satisfied. All self-improvement remains candidate-scoped, evaluated, human-promoted, versioned, and rollback-capable.

### 1.1 Minimum change set from the source blueprint

| Object | Source action | Why | Current repository status |
|---|---|---|---|
| Reference workflow | `evidence-wayfinding` | Unify cross-Skill ordering, handoff, stop, and escalation | **Implemented** as `docs/evidence-wayfinding.md` |
| Capability profile | `senior-decision-wayfinding` | Bind model lanes, Skills, tools, budget, verification, and permissions | **Implemented** as synthetic reference profile under `examples/capability-profiles/` |
| Atomic Skill | `frontier-practice-scout` | Investigate one named gap using current external primary evidence | **Deferred / candidate only**; Direction Gate not yet satisfied |
| Agent | `delivery-capability-conductor` | Existing minimum-capability routing and stop logic | **Reused; no new Agent** |
| Core object | `feature_delivery_case` | Shared key for intent, evidence, delivery, and outcome | **Reused** |
| Cross-runtime handoff | Portable Case Pack + adapters | Schema/projection concern, not a Skill | **Portable Case Pack implemented**; adapter conformance remains future work |

### 1.2 Four explicit non-additions

The source blueprint explicitly says not to:

1. create a new Lattice module named Evidence Wayfinding;
2. create a universal research Agent;
3. embed Gemini, NotebookLM, Copilot, Codex, or other vendor compatibility logic inside every Skill;
4. write every case lesson directly into global rules.

Those boundaries remain valid. Helixion, AegisFlow, Memexa, FlowGuard, OpenClaw, and DeliveryYield remain active modules with independent development tracks.

## 2. Name, Metaphor, and North Star

### 2.1 Wayfinding metaphor

| Real-world wayfinding behavior | System action | Failure avoided |
|---|---|---|
| Determine destination | Freeze user outcome, bounded decision, and invariants | Investigation becoming the goal |
| Observe landmarks | Collect first-party evidence, code, cases, and runtime results | Model opinion treated as fact |
| Triangulate | Use independent sources, counterevidence, and reproducible checks | Consensus treated as proof |
| Decide at forks | Send only high-value bounded choices to accountable humans | Humans forced to read all material |
| Leave a trail | Preserve artifact, outcome receipt, failure point, and scope | Document count mistaken for value |
| Update the map | Promote only evaluated reusable candidates | Self-rewriting mistaken for learning |

### 2.2 Verified Decision Yield

The source blueprint defines the north-star concept as:

> **Verified Decision Yield (VDY)** — the number of evidence-traceable, verified, team-usable decisions or delivery artifacts that change real work state per unit of scarce human attention.

Conceptual expression:

```text
VDY = verified_team_usable_deliverables / scarce_human_attention_minutes
```

Quality constraints must dominate the numerator:

```text
false_pass_rate <= preregistered_threshold
unsupported_claim_rate <= preregistered_threshold
human_authority_preserved = true
delivery_state_changed = true
```

The blueprint explicitly rejects Agent activity, tool-call count, token reduction, document count, or apparent depth as primary success measures. Token and cost optimization are downstream of a quality verdict.

## 3. Mission Anchor and Goal-Drift Control

The blueprint requires a short, versioned Mission Anchor carried through stable context, Case Contract, handoff, Decision Card, Run Result, and Evolution Proposal.

```yaml
goal_id: lat.goal.verified-decision-yield.v1
goal: >
  Increase verified, team-usable delivery decisions and artifacts
  per minute of scarce human attention.
non_goals:
  - maximize agent activity, tool count, document count, or autonomy
  - optimize tokens before correctness
invariants:
  - correctness_before_speed
  - visible_unknowns
  - human_authority
  - real_delivery_state_change
  - governed_learning
mutation_rule: human_owner_approval + version_bump
```

Every meaningful state transition should be able to answer:

```yaml
goal_alignment:
  goal_ref: lat.goal.verified-decision-yield.v1
  changed_state: <what real state changed>
  user_value: <why the human attention was worth spending>
  drift_risk: <whether new information is pulling goal/scope/authority>
  stop_if_no_change: true|false
```

Rules preserved from the blueprint:

- New evidence may change claims, route, priority, and plan.
- New evidence must not silently change goal, scope, authority, or acceptance observer.
- Competing goals create a human Decision Card rather than an Agent-authored compromise.
- Two consecutive rounds with no new evidence, risk reduction, or delivery-state change trigger stop and reorientation.
- Context compression must preserve Mission Anchor, material decisions, counterexamples, unknowns, and evidence index while removing repeated narrative.

## 4. Capability Reuse Matrix

The blueprint is intentionally composition-first and does not load the full catalog.

| Layer | Default / conditional | Existing capability | Evidence Wayfinding responsibility |
|---|---|---|---|
| Entry | Default | `delivery-capability-conductor` | Route one Case to the minimum justified capability set; stop when sufficient |
| Shared object | Default | `feature_delivery_case` | Bind intent, scope, evidence, decisions, risks, artifacts, and outcome |
| Understanding | On demand | `feature-understanding-loop`, `context-mastery` | Reach sufficient understanding, not complete understanding |
| System map | On demand | `system-mental-model` | Model runtime path, failure path, controls, and impact boundary |
| Challenge | On demand | `unasked-questions-generator`, `contradiction-adjudication`, `negative-knowledge-pack` | Surface missing questions, contradictions, counterexamples, and known failures |
| Human adjudication | Default when a consequential fork exists | `decision-question-builder` | Compress ambiguity into one evidence-bounded decision |
| Multi-request attention | Multi-case only | `senior-attention-queue` | Protect scarce senior attention across multiple requests |
| Delivery | Default | `delivery-artifact-builder` and its specialists | Produce team-usable delivery artifacts |
| Recovery | Blocked delivery only | `delivery-rescue` | Recover from real execution or validation blockers |
| Outcome learning | After delivery | `feature-outcome-review` | Compare intent with observed outcome |
| Reuse candidates | Cross-case only | `reusable-delivery-pattern`, `delivery-judgment-playbook` | Propose reusable candidates; do not auto-promote |
| Evolution governance | Controlled | Helixion + capability harness / governor | Evaluate, promote, modify, deprecate, and roll back candidates |

The source blueprint requires the Conductor to select no more than one primary capability plus one optional supporting capability by default, and to explain why other capabilities are not loaded.

## 5. Ordered Workflow

The full source workflow is eleven stages numbered `0` through `10`.

| Stage | Action | Minimum artifact | Pass / stop condition |
|---|---|---|---|
| 0 Orient | Confirm real user, one decision, purpose, non-goals, deadline, falsification | Wayfinding Contract | Cannot write one `decision_requested` -> ask human |
| 1 Route | Conductor selects minimum capabilities and tools | Route Receipt | Existing valid artifact is reusable -> do not repeat work |
| 2 Sense | Collect project, code, historical decisions, evidence, and unknowns | Portable Case Pack | Sources, cutoff, permissions, and gaps visible |
| 3 Model | Build smallest system slice, material claims, and causal chain | Evidence Map | Sufficient Understanding Gate met for named decision |
| 4 Challenge | Seek contradiction, counterexample, shadow dependency, alternative explanation | Challenge Receipt | Strongest counterevidence explicit |
| 5 Frontier | Search current first-party practice only for a named decision-changing gap | Frontier Evidence Brief | Skip when search cannot materially change decision or verification plan |
| 6 Verify | Prefer deterministic verifier; then independent model or human | Verification Receipt | Target-relevant validation passes, otherwise degrade/stop |
| 7 Decide | Compress to one bounded decision with few comparable options | Decision Strip / Card | Human can decide in roughly 30-60 seconds |
| 8 Deliver | Produce team-executable, verifiable artifact | Delivery Artifact | Real work state changes and owner is explicit |
| 9 Settle | Record outcome, human correction, earliest failure, value, remaining unknowns | Outcome Receipt | Fact / derivation / judgment / unknown remain separated |
| 10 Evolve | Form candidate and enter evaluation/promotion path | Evolution Proposal | No reuse evidence -> retain as case, do not promote |

### 5.1 Three entry paths

| Entry | Use when | Priority capabilities | Typical result |
|---|---|---|---|
| Decision Spike | Need fast `whether/how` judgment | `decision-question-builder` + `context-mastery` | Decision Card + bounded plan |
| Feature Understanding | Scope, dependency, or risk is unclear | `feature-understanding-loop` + `system-mental-model` | Evidence Map + Work/PR-ready brief |
| Delivery Rescue | Implementation, review, release, or cross-team state is blocked | `delivery-rescue` + artifact builder | State-change plan + owner handoff |

## 6. Intermediate Artifact Contracts

The source blueprint says artifacts exist to transfer verifiable state across people, Agents, and runtimes. Every artifact should answer: **what can the next actor do with this?**

### 6.1 Portable Case Pack

The source shape is preserved here for lineage. The active machine-readable contract is `lat.portable_case_pack.v1` in `schemas/capability/portable-case-pack.v1.schema.json`.

```yaml
schema_version: lat.portable_case_pack.v1
case_id: <feature_delivery_case_id>
mission_anchor_ref: lat.goal.verified-decision-yield.v1
decision_requested: <one bounded decision>
audience: senior_engineer
scope:
  in: []
  out: []
evidence_cutoff: <timestamp>
claims:
  observed: []
  derived: []
  judged: []
  unknown: []
conflicts: []
strongest_counterevidence: []
rejected_directions:
  - direction: <candidate>
    reason: <why rejected>
    evidence_ref: <ref>
evidence_refs:
  - id: <stable-id>
    uri: <addressable-source>
    date: <observation-date>
    access: <access-status>
    content_hash: <optional-stable-hash>
source_gaps: []
next_tool_task: <named claim or state change>
required_output: <artifact contract>
falsification: <what would reverse the recommendation>
data_classification: public|private|restricted
```

### 6.2 Human-attention layers

| Surface | Expected read time | Must contain | Must not contain |
|---|---:|---|---|
| Decision Strip | 5-10 seconds | One recommendation, decision needed, largest risk, deadline | Background narrative, full method |
| Decision Card | 30-60 seconds | 2-4 comparable options, evidence, unknowns, counterevidence, reversibility | Large question lists, false precision |
| Evidence Map | 3-5 minutes | Claims, evidence chain, conflicts, gaps, system slice | Unsourced model summaries |
| Evidence Pack | Deep read on demand | First-party sources, snapshots, bounded logs, eval results | Material unrelated to the current decision |

### 6.3 Receipts

| Artifact | Required content | Purpose |
|---|---|---|
| Compression Receipt | `found / inspected / unavailable`, preserved claims, omitted items and reason, cutoff | Distinguish not-found, not-authorized, and deliberately omitted context |
| Challenge Receipt | Strongest counterexample, hidden dependency, stakeholder surprise, unresolved conflict | Prevent fluent output from hiding uncertainty |
| Verification Receipt | Target, verifier, command/data, result, blind spots, false-pass risk | Prevent Agent self-certification |
| Outcome Receipt | Original decision, final artifact, human corrections, state change, failure point, next entry | Turn real outcome into evidence for future work |

## 7. Correctness Model

The blueprint's position is:

> The goal is not to guarantee the first answer is correct. The goal is to make errors visible, bounded, and correctable, and to improve only when external verification is reliable, the target contract is stable, and failure evidence is retained.

### 7.1 Evidence and verification priority

| Priority | Verifier | Typical question | Authority boundary |
|---|---|---|---|
| 1 | Compiler / schema / type / lint | Is structure valid? | Does not prove user outcome |
| 2 | Repro / target test | Is failure reproducible and removed? | Must not confuse implementation detail with target |
| 3 | Regression / integration / static analysis | Did another path break? | Conclusion limited by coverage |
| 4 | Independent evidence or model challenge | Is the explanation missing alternatives? | Model agreement is not proof |
| 5 | Human or production result | Did real state and value change? | Highest value, highest cost and delay |

### 7.2 Claim state machine

| State | Meaning | Allowed action |
|---|---|---|
| `UNKNOWN` | Evidence insufficient | Gather evidence, ask, or retain unknown explicitly |
| `HYPOTHESIS` | Falsifiable explanation | Define verifier and counterexample |
| `EVIDENCED` | Source-supported but not target-verified | Enter challenge; do not treat as final fact |
| `CONFIRMED` | Passed target-related validation | Use in decision within scope/cutoff |
| `CONFLICTED` | Reliable evidence disagrees | Escalate; do not average |
| `STALE` | Environment or evidence window changed | Revalidate; do not silently reuse |
| `INVALIDATED` | Counterevidence or outcome disproved claim | Preserve failure; stop propagation |

### 7.3 Loop Contract and stop rules

Each loop should predeclare:

- user outcome;
- include/exclude boundary;
- acceptance observer;
- forbidden actions;
- verifier;
- allowed small state changes;
- maximum iteration count;
- no-progress condition.

Maker and Checker should be separated. When one model performs both, independent tests/data are required; higher-risk cases require a distinct role or human review.

Any high-permission, irreversible, externally sent, or scope-expanding action stops at a Human Gate before execution.

### 7.4 Error-introduction / correction intuition

The source blueprint uses the following conceptual recurrence:

```text
A(k+1) = A(k) * (1 - EIR) + (1 - A(k)) * ECR
```

Where:

- `EIR` = Error Introduction Rate — previously correct behavior made wrong by the loop.
- `ECR` = Error Correction Rate — previously wrong behavior corrected by the loop.

At high baseline accuracy, EIR must be extremely low. More iterations can reduce quality when change introduces errors faster than verification removes them.

## 8. Governed Evolution

The blueprint defines self-evolution as closed-loop engineering, not automatic prompt or Skill rewriting.

```text
failure point or repeated gap
-> candidate
-> representative replay set
-> reserved / holdout evaluation
-> human review
-> versioned promote | modify | retain | deprecate
-> rollback condition
```

### 8.1 Asset lifecycle

| State | Entry condition | Visibility / authority |
|---|---|---|
| `idea` | One valuable observation | Case-local only |
| `draft` | Owner, scope, expected use | Never auto-routed |
| `runnable` | Contract complete and executable/checkable | Shadow only |
| `qualified_for_scope` | Representative set passes and risk controlled | Assisted, explicit selection |
| `used_once` | One real case succeeds with Outcome Receipt | Not yet reusable proof |
| `reused` | A different case succeeds and boundary remains stable | Eligible for team proposal |
| `team_available` | Human review, version, rollback, expiry complete | Task/profile-scoped activation |
| `deprecated` | Regression, staleness, or replacement | Lineage preserved, not routed |

### 8.2 Evolution Proposal minimum contract

```yaml
proposal_id: <stable-id>
failure_point: <earliest observed failure>
affected_cases: []
proposed_asset_type: skill|rule|script|schema|example|eval|profile
proposed_diff: <bounded change>
expected_improvement: <metric + scope>
risk_of_regression: <false-pass / authority / drift risk>
representative_cases: []
reserved_cases: []
promotion_thresholds: {}
rollback_thresholds: {}
owner: <accountable human>
expiry: <review date>
status: candidate
```

Helixion may detect cross-case patterns and propose candidates. It may not directly change production Skills, permission boundaries, Mission Anchor, or verifier. DeliveryYield measures economics only after quality evaluation and cannot approve delivery or promotion.

## 9. Frontier Practice Scout — Preserved Candidate

The source blueprint identified one capability gap:

> Existing Skills can handle internal context, conflict, unknowns, system understanding, and delivery, but no narrow public capability is dedicated to the question: “For this named evidence or capability gap, as of a defined time, what current external first-party practice, tool, or counterexample could materially change the present decision?”

The blueprint's proposed atomic Skill is `frontier-practice-scout`.

### 9.1 Source Direction Fit rationale

| Question | Source blueprint answer |
|---|---|
| Why existing composition may be insufficient | Generic web research does not itself enforce cutoff, authority, counterevidence, applicability, expiry, and decision-impact contracts |
| Minimum reuse path | Conductor / Context Mastery first names the gap; scout runs only if current external evidence could alter the decision |
| Primary direction | `current_product_delivery`; secondary future value may become `strategic_asset` or `team_reuse` only after evidence |
| Forbidden behavior | Trend browsing, popularity-as-evidence, automatic purchase recommendation, automatic asset promotion |
| Output | `Frontier Evidence Brief` and candidate practices/tools, all candidate-only |

### 9.2 Preserved proposed Skill contract

```yaml
name: frontier-practice-scout
role: atomic_capability
trigger: >
  A named evidence or capability gap may be changed by current external practice.
inputs:
  - decision_requested
  - named_gap
  - evidence_cutoff
  - allowed_data_classification
workflow:
  - define what finding would change the decision
  - search open-endedly beyond a pre-listed tool set
  - prioritize primary / official / reproducible sources
  - record dates, access gaps, counterevidence, and expiry
  - compare candidates against the target contract
output: frontier_evidence_brief
stop:
  - decision-changing evidence found and triangulated
  - source frontier exhausted within budget
  - no authorized access
  - no material decision impact
authority: candidate_only
```

### 9.3 Expansion and convergence

| Expansion loop | Convergence loop |
|---|---|
| Start from the problem, not a fixed tool list | Every candidate must map to a named claim or gap |
| Search new practice, tools, papers, and cases | Prefer first-party evidence with version/date/expiry |
| Preserve unexpected findings and dissent | Compare target fit, evidence quality, risk, reversibility, total cost |
| Produce multiple candidates without premature convergence | Only decision-changing evidence enters primary context |

### 9.4 Current repository decision

**Do not create the Skill yet.** PR #34 already recorded that the required second-use / independent-value evidence and run/skip evals do not exist. The Direction Investment Gate still requires demonstrated value before team-reuse capability investment. No new evidence has appeared merely because PR #34 was merged.

The candidate is preserved in detail in `docs/evidence-wayfinding/frontier-practice-scout-candidate.md` so it cannot be forgotten while remaining non-active.

## 10. Cross-runtime Execution Model

The source blueprint rejects a universal prompt. It proposes one vendor-neutral contract plus thin runtime adapters validated by common conformance cases.

| Runtime | Stable entry | Task entry | Execution boundary | Required return |
|---|---|---|---|---|
| GitHub Copilot | repo instructions / custom Agent | Agent Skill + Case Pack | code, tests, PR under tool/permission boundary | Verification / Delivery / Outcome Receipt |
| ChatGPT / Codex | project instructions / stable context | Skill + Capability Profile + sources | research, code, docs, tools under permissions | same Portable Case Pack + evidence refs |
| Gemini CLI / Code Assist | `GEMINI.md` / rules | custom command or extension + Case Pack | code, MCP, shell under approval/sandbox | structured handoff + verifier result |
| NotebookLM | topic notebook + authoritative sources | upload Case Pack / Evidence Pack | source-grounded synthesis; no repository Skill execution | cited candidate conclusions, questions, conflicts |
| Generic LLM | short system contract | Portable Case Pack JSON/Markdown | only explicitly authorized actions | claim state, evidence, unknowns, next step, stop reason |

Provider interfaces are time-sensitive. The original blueprint evidence cutoff is 2026-08-07. Runtime adapters must carry owner, `evidence_cutoff`, and expiry/reverification rules rather than freezing current vendor behavior into permanent kernel rules.

Common conformance checks:

1. goal preservation;
2. evidence references remain addressable;
3. unknowns remain visible;
4. permission stop behavior is preserved;
5. handoff/output schema remains compatible.

## 11. Evaluation and Evolution Dashboard

### 11.1 Metric hierarchy

| Layer | Metric family | Why it matters |
|---|---|---|
| North Star | Verified Decision Yield | Verified team-usable delivery per scarce human attention |
| Correctness | false pass, unsupported claim, conflict escape, target drift | Prevent apparent completion |
| Judgment | human override, reversal, decision latency, strongest-counterevidence coverage | Determine whether judgment is faster and more stable |
| Delivery | accepted artifact, review rework, escaped defect, time-to-state-change | Measure real work-state change |
| Learning | EIR, ECR, candidate->qualified, rollback rate, reuse success | Determine whether the system actually improves |
| Economics | human minutes, token/tool cost, latency per accepted artifact | Optimize only after quality holds |

### 11.2 Evaluation design

The source blueprint requires:

1. freeze target contract, evidence cutoff, and acceptance criteria;
2. separate representative cases from reserved/holdout cases;
3. compare challenger vs incumbent blind, including Prompt, Skill, tool, method, or context-pack changes;
4. evaluate both final artifact and process integrity: authority violations, drift, conflict omission, repeated no-progress, outcome leakage;
5. pre-register promotion and rollback thresholds;
6. treat one excellent case as a hard case/candidate, not distributional proof;
7. add the earliest failure point to the hard-case corpus without leaking holdout outcomes into future evaluations.

## 12. Governance and Boundaries

| Boundary | Allowed | Forbidden / gated |
|---|---|---|
| Mission | Human owner makes versioned change | Agent silently changes target |
| Evidence | Preserve source, time, hash, access gap | Model summary presented as fact |
| Tools | Tool call bound to named claim/state change | Unbounded calls for completeness |
| Permissions | Least privilege, read-only first, stop before irreversible action | Skill expands its own authority or crosses data domain |
| Public/private | Public generic rules and synthetic examples; private real cases | Private evidence copied into public Skill |
| Evolution | Candidate, blind eval, human promotion, version, rollback | One-case feedback changes team rules automatically |
| Metrics | Cost measured after quality verdict | Token/call volume drives objective |

Manager-facing claims should use `OBSERVED / DERIVED / JUDGED / UNKNOWN` and state current delivery, state change, human corrections, evidence boundary, limitations, next-use path, and one narrow decision. Public conformance cannot establish real downstream adoption, manager acceptance, or business value.

## 13. Source 90-day Rollout Roadmap

The source blueprint proposed the following sequence without changing existing module boundaries.

| Phase | Scope | Done definition | Stop / rollback |
|---|---|---|---|
| Weeks 0-2: Contract | Mission Anchor, workflow, profile, Case Pack, 8-12 replay cases | Two existing Agents independently produce compatible handoff | Target unclear or verifier unreliable -> do not automate |
| Weeks 3-4: Shadow | Run beside existing cases; read-only, no real decision impact | Find at least one real failure point and record false-pass/drift | Critical errors remain invisible -> return to contract |
| Weeks 5-8: Assisted | Senior engineer explicitly invokes; Decision Card + artifact | VDY no worse than baseline; at least one credible state change | Correctness declines or human effort increases -> rollback |
| Weeks 9-12: Cross-runtime | Copilot/Codex/Gemini adapters; NotebookLM synthesis | Same Case Pack passes conformance suite | Any runtime loses permission/unknown/citation semantics -> disable adapter |
| Then: Governed growth | Promote only evidence-supported candidates | version, expiry, owner, rollback present | no reuse, staleness, or regression -> deprecate |

### 13.1 First ten source implementation items

1. Approve Evidence Wayfinding as the public workflow name and confirm it is not a module.
2. Freeze Mission Anchor v1 and a computable VDY definition.
3. Use `feature-understanding-loop` as the understanding backbone rather than copying it.
4. Define reference workflow state, next step, stop, escalation, and handoff.
5. Define Capability Profile model lanes, Skill allowlist, tools, permissions, budgets, verification, telemetry.
6. Define Portable Case Pack / Decision Card / Outcome Receipt schemas.
7. Prepare `frontier-practice-scout` Direction Fit, Skill contract, source strategy, and negative tests **only when its gate is satisfied**.
8. Establish 8-12 representative cases and 4-6 reserved cases including goal drift, proxy optimization, stale information, and unavailable sources.
9. Roll out shadow -> assisted -> task-scoped; do not default-auto-activate.
10. Review assets every two weeks: promote / modify / retain candidate / deprecate with rollback record.

Current status after PR #34:

- Items 1, 3, 4, and 5 are materially represented.
- Portable Case Pack from item 6 is implemented; Decision Card and Outcome Receipt remain concept-level or are covered by existing specialist artifacts rather than new schemas.
- Item 7 remains intentionally deferred.
- Items 2, 8, 9, and 10 require real replay/usage evidence and should not be declared complete from public repository shape alone.

## 14. Pre-mortem: Most Likely Failure Modes

| Failure mode | Early signal | Mechanistic defense |
|---|---|---|
| Latest context hijacks original purpose | scope/user/success metric changes without decision record | Mission Anchor + goal alignment + human version bump |
| “Continuous evolution” becomes auto-rewrite | one case changes global rule | candidate-only + reserved eval + human promotion |
| More tools becomes the objective | tool calls rise without claim/state change | every call bound to named claim/state change |
| Multi-model consensus becomes truth | no external evidence but claim becomes confirmed | agreement remains `JUDGED`; target verifier required |
| Compression loses counterexample | summary retains recommendation but not counterevidence | Compression Receipt preserves counterevidence/unknown/cutoff |
| Proxy objective is optimized | tokens fall while review rework rises | quality gate before DeliveryYield |
| Mega Skill swallows catalog | broad trigger, constant invocation, context growth | reference workflow + atomic Skill + profile separation |
| NotebookLM treated as execution Agent | asked to write repo/run verifier despite inability | source-grounded synthesis only; output remains candidate |
| Public/private boundary breaks | real private cases enter public asset | classification + projection + review gate |
| “Exponential growth” becomes a promise | activity growth reported as capability growth | report VDY, EIR/ECR, reuse success, rollback |

## 15. Blueprint Acceptance Criteria

The original blueprint says the design is acceptable when:

1. any participating Agent can restate real goal, non-goals, and human authority from Mission Anchor in under one minute;
2. for a new Case, the Conductor chooses at most one primary and one optional supporting capability and explains why the rest are not loaded;
3. every important claim has an explicit state plus `evidence_ref` or remains `UNKNOWN`;
4. every external search records named gap, cutoff, decision impact, and stop condition;
5. Decision Card asks for one narrow judgment and includes strongest counterevidence, unknowns, and reversibility;
6. final artifact changes real work state and is directly usable by the next engineer/reviewer;
7. Outcome Receipt preserves human corrections and earliest failure point rather than deleting failure history;
8. improvements begin as candidates and cannot promote without representative/holdout evidence, thresholds, and rollback;
9. Copilot, Codex, Gemini, and NotebookLM adapters preserve goal, evidence, unknown, permission, and handoff semantics;
10. cost/token optimization only applies after correctness does not regress;
11. the system does not claim inevitable exponential improvement.

## 16. Suggested Logical Ownership from the Source Blueprint

The source blueprint suggested the following conceptual layout. The repository may use different physical paths where current governance requires it.

```text
workflows/evidence-wayfinding/
  workflow.md
  states.yaml
  handoff-examples/

profiles/senior-decision-wayfinding/
  profile.yaml
  runtime-adapters/
    github-copilot.md
    codex.md
    gemini-cli.md
    notebooklm.md

skills/frontier-practice-scout/
  SKILL.md
  references/source-quality.md
  evals/

schemas/
  portable-case-pack.schema.json
  decision-card.schema.json
  outcome-receipt.schema.json
  evolution-proposal.schema.json
```

This is a preservation of design intent, **not** an instruction to create these directories blindly. Current repository taxonomy and Direction Investment Gate take precedence.

## 17. Compressed Rules

| Rule | Short form |
|---|---|
| Purpose | Use limited human attention to produce verified, team-usable delivery |
| Routing | Choose minimum capability first; stop when sufficient |
| Evidence | Separate fact / derivation / judgment / unknown; model cannot self-prove |
| Expansion | Search from a named gap, not a fixed tool list |
| Convergence | Only decision-changing evidence enters primary context |
| Human | Humans handle high-value forks and retain final authority |
| Delivery | Artifact must change real state and be usable by the team |
| Learning | Real outcome -> candidate -> blind eval -> human promotion -> rollback |
| Goal retention | New evidence may update the map but cannot silently change destination |

## 18. Source Ledger

The source IDs are preserved because later evaluations and merges must be able to distinguish internal source material, repository evidence, and external first-party evidence.

### 18.1 Internal source material

These identifiers came from the source blueprint. Their contents are **not** vendored by this public document.

- `I1` — `Lattice_Skill_Architecture_Report_CN.docx`
- `I2` — `Loop_Engineering_Accuracy_First_Playbook_CN.docx`
- `I3` — `Loop_Engineering_Accuracy_First_Research_Report_CN.docx`
- `I4` — `Lattice 团队经验资产化与技能演进任务.docx`
- `I5` — `Lattice_讨论复盘与经理汇报框架_可打印研读版(1).docx`
- `I6` — `Feature_Understanding_Loop_Deep_Research_Report_CN(1).docx`
- `I7` — `Lattice_Right_Context_First_AI_Coding_Pilot_CN(1).docx`

### 18.2 Repository evidence IDs

- `R1` — Repository README
- `R2` — Repository operating rules (`AGENTS.md`)
- `R3` — Capability taxonomy (`docs/capability-taxonomy.md`)
- `R4` — Capability Profile runtime contract (`docs/capability-profile-runtime-contract.md`)
- `R5` — Skill authoring gate (`docs/skill-authoring-gate.md`)
- `R6` — Direction investment gate (`docs/direction-investment-gate.md`)
- `R7` — Public/private operating model (`docs/public-private-operating-model.md`)
- `R8` — Manager credibility contract (`docs/manager-credibility-contract.md`)
- `R9` — Feature Understanding Loop (`skills/feature-understanding-loop/`)
- `R10` — Delivery Capability Conductor (`skills/delivery-capability-conductor/`)

### 18.3 External first-party evidence IDs from the source blueprint

These are preserved as dated source references and must be reverified before implementation decisions because vendor behavior changes.

- `E1` — GitHub Copilot Agent Skills — `https://docs.github.com/en/copilot/concepts/agents/about-agent-skills`
- `E2` — GitHub custom agents — `https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/create-custom-agents`
- `E3` — Gemini CLI context files — `https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html`
- `E4` — Gemini CLI custom commands — `https://google-gemini.github.io/gemini-cli/docs/cli/custom-commands.html`
- `E5` — Gemini Code Assist agent mode — `https://developers.google.com/gemini-code-assist/docs/agent-mode`
- `E6` — NotebookLM overview — `https://support.google.com/notebooklm/answer/16164461`
- `E7` — NotebookLM mind maps — `https://support.google.com/notebooklm/answer/16212283`
- `E8` — Anthropic effective context engineering — `https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents`
- `E9` — Anthropic agent evals — `https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents`
- `E10` — Anthropic writing tools for agents — `https://www.anthropic.com/engineering/writing-tools-for-agents`
- `E11` — OpenAI evaluation guide — `https://platform.openai.com/docs/guides/evals`

## 19. Evidence Boundary and Unresolved Items

The source blueprint itself recorded these limits:

- It inspected the public GitHub repository and supplied source material, not private downstream repositories, real customer data, or unpublished cases.
- Snapshot counts such as numbers of Skills or Agents are not stable rules and should be generated by registry tooling rather than copied into kernel instructions.
- Cross-runtime product behavior changes; adapters require owner, evidence cutoff, and expiry.
- Evaluation thresholds should be determined from replay-case baselines. The blueprint intentionally does not invent precise thresholds without data.

Current unresolved items remain:

1. collect representative and reserved replay cases;
2. compute a baseline for VDY and correctness metrics;
3. observe whether frontier research produces distinct decision-changing value;
4. establish runtime adapter conformance with fresh provider evidence;
5. decide whether separate Decision Card, Outcome Receipt, or Evolution Proposal schemas are necessary or whether existing specialist contracts remain sufficient;
6. only then reconsider active Skill creation or broader automatic routing.
