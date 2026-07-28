# Public–Private Operating Model

## Decision

Lattice is a public, evidence-grounded delivery capability reference and governance repository. It publishes reusable public contracts that private downstream repositories pin and execute locally. It does not operate as a private delivery database, runtime orchestration platform, or system of record for company evidence.

```text
Public Lattice
  contracts / Skills / Agents / schemas / validators
  reference workflows / profiles / templates / synthetic fixtures
                                |
                                | pinned dependency
                                v
Private downstream repository
  real feature_delivery_case / source / business context
  real evidence / private extensions / human review
  reusable assets / adoption observations / manager deliverables
```

## Public Responsibilities

Public Lattice owns:

```text
architecture principles
public Skills and Agents
capability identity and semantic versioning
Feature Delivery Case contracts
evidence and claim contracts
reusable asset lifecycle contracts
reference workflows and Capability Profile templates
manager credibility rules and manager-facing templates
synthetic conformance fixtures
validators, negative tests, compatibility tests, and CI gates
downstream consumption contracts
```

Public artifacts may define structure, behavior, evidence classes, failure rules, compatibility, and safe example wording. Public validators may be downloaded and run locally against private paths.

## Private Responsibilities

A private downstream repository owns:

```text
real feature_delivery_case records
private source code and business context
real Jira, Issue, PR, CI, Incident, review, merge, and release evidence
private capability extensions
raw human contributions and failure-point feedback
reusable asset candidates, reviews, and usage observations
real manager-ready asset packs and internal Capability Profiles
private adoption, ownership, and governance decisions
```

The private repository is the system of record for these artifacts. Its accountable owners decide whether evidence is sufficient, an extension is safe, an asset may be promoted, a manager claim is credible, or a capability is team-available.

## Prohibited Public Content

Do not commit, upload, copy, or reproduce in public Lattice:

- company-specific business logic or private source;
- real tickets, PRs, incidents, review comments, employee feedback, or manager reports;
- secrets, tokens, credentials, customer or employee data, or private repository paths;
- complete private runtime traces, evidence ledgers, adoption records, or internal ROI;
- sanitized material whose re-identification, licensing, or publication approval is unresolved.

`real_sanitized` still represents real downstream evidence and remains private unless a separate accountable publication review explicitly authorizes a public contribution. Public Lattice does not infer that authorization.

## Consumption and Extension

A downstream repository must:

1. pin an immutable Lattice tag or commit;
2. pin every consumed contract version;
3. select the smallest Capability Profile and explicit public capabilities;
4. keep evidence and outputs in private paths;
5. name private extensions so they cannot be mistaken for public packages;
6. declare whether each extension extends, overrides, or composes a public capability;
7. run the pinned validators locally;
8. review compatibility before changing the pin.

Public behavior has lower precedence than a valid private extension only inside the private repository and only within the extension's declared scope. A private extension cannot alter the identity, release state, or public contract of the capability it references.

## Evidence and State Boundaries

Public Lattice may validate private evidence in process without receiving or retaining it. Validation reports and manager packs remain private. Only synthetic fixtures are stored publicly.

```text
public_package_status =
  draft | contract_validated | conformance_validated | released | deprecated

downstream_adoption_status =
  not_observed | imported | task_scoped | used_once | reused | team_available | deprecated
```

Only real private evidence and human review can produce an adoption state above `not_observed`. `team_available` requires an explicit private governance approval. No state may be skipped.

Every public fixture declares:

```text
simulation_status = synthetic_reference
downstream_adoption_status = not_observed
```

Synthetic review proves only format and conformance. It does not prove actual use, reuse, team endorsement, manager acceptance, or business value.

## Public Claims Boundary

Public Lattice may claim that a contract, fixture, validator, or compatibility projection passed a named public conformance check at a named version.

It may not claim that:

- a private repository has adopted a capability;
- a synthetic capability was used once or reused;
- a team or manager accepted an asset;
- green CI, PR count, Skill count, Agent count, or token count demonstrates user or manager value;
- a precise ROI, success rate, productivity gain, or organization-level outcome exists without real private evidence and accountable review.

Conformance is necessary evidence about public contracts. It is not proof of private business value.
