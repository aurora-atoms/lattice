---
name: human-judgment-amplifier
description: Use for scarce-expert decision queues, real-case mentorship, and evidence-backed invisible-work receipts; do not use to automate final expert judgment, rank personnel, infer performance from activity, or expose sensitive collaboration data; input is a bounded question, evidence, options, risks, review history, learning goal, and participant-confirmed contribution evidence; output is a prioritized decision packet, teach-back case, mentorship exercise, or impact receipt with human confirmation, privacy controls, uncertainty boundaries, behavior preservation, and quality-adjusted token ROI.
---

# Human Judgment Amplifier

## Goal
Increase the leverage of expert attention and team learning without replacing people or creating surveillance incentives.

## Use When
Select the smallest sufficient atomic capability:
- G01 Senior Attention Amplifier
- G02 Mentorship Without Meetings
- G03 Invisible Work Credit

## Do Not Use When
Do not use for personnel ranking, automated final judgment, or unconfirmed sensitive contribution claims.

## Inputs
Use a bounded question, evidence, options, risks, time limits, review history, learning goal, and participant-confirmed impact evidence.

## Outputs
Return a prioritized expert decision packet, minimum context, teach-back case, mentorship exercise, or evidence-backed impact receipt.

## Workflow
1. Identify whether the need is expert routing, mentorship, or impact visibility.
2. Query ConPort before loading or searching the full skill text when ConPort is available; otherwise use targeted source reads.
3. Select one atomic capability first.
4. Compress context without hiding uncertainty.
5. Preserve final expert and participant authority.
6. Produce a confirmable artifact, not an activity score.

## Rules
GCAT.001 | MUST | routing | select one atomic capability before composing | enforce
GCAT.002 | MUST | evidence | link claims to delivery outcome and participant confirmation | enforce
GCAT.003 | MUST | human | preserve final expert judgment | enforce
GCAT.004 | MUST | privacy | minimize sensitive collaboration data | enforce
GCAT.005 | MUST | token | optimize quality-adjusted token ROI | enforce
GCAT.006 | SHOULD | prompt | keep rules and the output contract in a stable prefix | prefer
GCAT.007 | NEVER | personnel | rank, score, or monitor people | block
GCAT.008 | NEVER | authority | automate the final expert decision | block

## Verification
- The artifact helps a real decision, learning task, or recognized delivery outcome.
- Sensitive claims are confirmed by participants.
- No personnel score or surveillance signal is produced.

## Failure Modes
- Treating reviewer style as universal truth.
- Crediting activity instead of changed delivery outcome.
- Monitoring individuals rather than fixing system bottlenecks.
