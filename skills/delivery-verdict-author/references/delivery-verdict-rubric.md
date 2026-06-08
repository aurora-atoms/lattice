# Delivery Verdict Rubric

```text
usable                 | acceptance evidence supports user-usable outcome
not_user_usable        | acceptance or user-usability evidence fails
requires_human_review  | material risk requires human decision
insufficient_evidence  | required evidence is missing or inconclusive
blocked                | dependency prevents validation or delivery

```text
TESTS_PASS_ACCEPTANCE_FAIL | verdict=not_user_usable
MISSING_MANUAL_ACCEPTANCE  | verdict=insufficient_evidence
BLOCKED_DEPENDENCY         | verdict=blocked
```
```
