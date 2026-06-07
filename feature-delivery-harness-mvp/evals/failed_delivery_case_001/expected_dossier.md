# Token Economics Dossier: CLI todo-filter failed usability fixture

Feature Case: fdc_failed_001
Delivery Status: not_user_usable

## Token And Cost

Total Tokens: 14000 tokens (estimated)
Total Cost: 0.42 usd (estimated)

## Stage Breakdown

- implementation_repair_loop: 14000 tokens (estimated); cost 0.42 usd (estimated); refs task_failed_001, validation_failed_auto_001, validation_failed_manual_001

## Waste Patterns

- failed_repair_loop: error; Return to acceptance criteria before another repair loop.; refs validation_failed_manual_001
- review_loop_without_progress: warning; Require new evidence before another review pass.; refs task_failed_001

## Optimization Signals

- acceptance_before_economics: Keep usability verdict separate from token economics summaries.; status candidate; refs delivery_failed_001

## Limitations

- Manual acceptance failed for documented CLI behavior.

## Claim Ledger

- Delivery status is not_user_usable. evidence_refs=delivery_failed_001 status=supported
- Detected 2 waste pattern(s). evidence_refs=waste_fdc_failed_001_failed_repair_loop,waste_fdc_failed_001_review_loop_without_progress status=supported
- Total token usage is 14000 tokens (estimated). evidence_refs=stage_failed_dev_001 status=supported
