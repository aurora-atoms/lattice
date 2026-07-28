# Manager Credibility Contract

## Purpose

This contract governs manager-facing delivery materials generated inside private downstream repositories. Public Lattice defines and tests the contract; it does not store real manager briefs or assert their business conclusions.

## Required Claim Model

Every material claim is classified:

```text
OBSERVED = directly supported by an addressable evidence record
DERIVED  = deterministically computed from cited observed evidence
JUDGED   = bounded human or model judgment with cited basis and named owner
UNKNOWN  = not established by available evidence
```

Every `OBSERVED`, `DERIVED`, or `JUDGED` claim has at least one resolvable `evidence_ref`. A material statement without a resolvable evidence reference is forced to `UNKNOWN` and cannot be presented as fact. `UNKNOWN` is preserved, not rewritten optimistically.

## Required Brief Content

A manager-ready brief, together with its enclosing asset-pack and reusable-asset manifests, states:

- current delivery and user-usable outcome;
- reusable asset created or changed;
- observable before/after state;
- evidence classification and evidence references;
- evidence origin: `synthetic`, `real_sanitized`, or `real_restricted`;
- version, scope, activation mode, owner, and applicable capability pin;
- whether an accountable human challenged or reviewed the asset;
- known limitations and unresolved unknowns;
- next-use entry and what must be revalidated;
- one narrow manager decision, if a decision is needed.

The brief must not hide the fact that an example is synthetic. `real_sanitized` and `real_restricted` remain private evidence classifications.

## Claim Strength and Adoption

```text
not_observed  -> no real downstream use established
imported      -> package present, use not established
task_scoped   -> human-approved for one bounded task
used_once     -> one evidenced completed private use
reused        -> at least one separately evidenced later use
team_available -> explicit private governance approval plus required evidence
```

No state may be skipped. A synthetic fixture always remains `not_observed`. One use is not reuse. One case is not team-wide adoption. `team_available` cannot be inferred from usage count, CI, popularity, or DeliveryYield.

## Human Challenge

The brief records:

```text
challenge_present
challenger_role
challenge_summary
resulting_change_or_open_issue
review_ref
```

A synthetic human review proves only that the format and workflow support review. A real human review must be stored privately and does not become public evidence.

## Before, After, and Limitations

Before/after statements name the same scoped object and comparable versions or times. If the baseline is missing, the change remains `UNKNOWN`. A brief must show known limitations even when validation passes.

Examples of limitations:

- validated only against one private case;
- no second-use observation;
- applicable only to a named language, repository, or workflow;
- human review was task-scoped rather than team governance;
- evidence is incomplete, sanitized, stale, or inaccessible to the reader.

## Safe and Forbidden Wording

Safe:

```text
OBSERVED: In case FDC-123, validator V rejected a dangling evidence reference.
DERIVED: The asset changed from version 1.1.0 to 1.2.0; the cited diff adds rule R.
JUDGED: The named reviewer approved task-scoped activation for repository X only.
UNKNOWN: No second private use has been observed, so reuse is not established.
This synthetic example demonstrates contract conformance only.
```

Forbidden:

```text
The team adopted this capability.
This asset is proven reusable.
Managers accepted the result.
Green CI proves delivery value.
More Skills, PRs, or tokens prove productivity.
This single use produced a precise ROI or success rate.
The synthetic review establishes real human acceptance.
DeliveryYield approved promotion.
```

Replace forbidden wording only when sufficient real private evidence and the accountable human authority exist. Otherwise preserve `UNKNOWN` or use a narrower factual statement.

## Manager Brief Opening

Lead with:

```text
current delivery
reusable asset left behind
observable state change
human challenge
evidence boundary
known limitations
next-use path
one narrow manager decision
```

Do not lead with schemas, Agent or Skill counts, token data, registries, databases, MCP, or tool-call counts. Those may appear only as supporting technical detail.

## Machine Validation

Structured claims use `schemas/evidence/evidence-claim.v1.schema.json`; the complete structured brief uses `schemas/manager/manager-delivery-brief.v1.schema.json`. Validate locally:

```bash
python vendor/lattice/scripts/validate_manager_claims.py \
  manager-brief.json \
  --evidence-ledger evidence-ledger.jsonl \
  --rendered-brief manager-brief.md
```

The validator reads only the supplied local files. When `--rendered-brief` is supplied, it requires the Markdown to match the canonical structured projection exactly, preventing extra claims or omitted limitations. It emits rule failures, not evidence content, and performs no network calls.

## Deterministic Rejection Conditions

The validator rejects:

- `OBSERVED`, `DERIVED`, or `JUDGED` claims with missing or dangling evidence refs;
- an `UNKNOWN` rewritten as fact;
- affirmative reuse, team, manager-acceptance, or ROI wording hidden under another claim kind;
- rendered Markdown that diverges from the structured brief;
- hidden known limitations;
- synthetic `used_once`, `reused`, or `team_available`;
- one use described as reuse;
- one case described as team-wide;
- activation without the required human review;
- `team_available` without separate governance approval;
- a team-level manager decision without `team_available` and governance approval;
- DeliveryYield used as an approval authority;
- exact ROI or success claims unsupported by private evidence and a declared method.
