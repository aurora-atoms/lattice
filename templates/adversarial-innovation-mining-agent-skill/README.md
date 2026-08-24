# Adversarial Innovation Mining Agent Skill Template

This portable public-only Skill turns a reproducible cross-system hard case into a challenged technical-mechanism research candidate.

It is intentionally a bridge, not a replacement for the two owning workflows:

```text
Safety-Critical Product Review
-> Adversarial Innovation Mining
-> Systematic Invention Research
```

## What it preserves

- competent-baseline adversarial review;
- identity/state/authority/effect transition attacks;
- replayable wrong-world outcomes;
- missing technical mechanism extraction;
- customer pain, measurable value, and monetization/attach point;
- strongest counter-control and kill criteria;
- public-only prior-art challenge;
- strongest counterevidence and explicit coverage gaps;
- retain/revise/reject rather than unsupported novelty claims.

## Public-only requirement

Do not use this Skill with employer/client confidential designs, internal source code or architecture, private telemetry/experiments, or unpublished real inventions. Do not attempt to sanitize private inputs by removing names.

## Recommended runtime projection

Copy the Skill into the runtime's native Agent Skills directory, for example:

```text
.agents/skills/adversarial-innovation-mining/
  SKILL.md
  references/
```

Re-check current runtime documentation and enterprise policy before installation. Keep tool permissions and runtime-specific behavior in thin adapters rather than forking the method.

## Machine contract

When used inside Lattice, emit the canonical handoff record:

```text
schemas/capability/adversarial-innovation-handoff.v1.schema.json
```

Validate with:

```text
scripts/validate_adversarial_innovation_handoff.py
```

The machine record is a research handoff, not a patentability, novelty, FTO, infringement, safety, or release decision.
