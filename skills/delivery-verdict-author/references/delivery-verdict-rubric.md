# Delivery Verdict Rubric

```text
usable                 | acceptance evidence supports user-usable outcome
not_user_usable        | acceptance or user-usability evidence fails
requires_human_review  | material risk requires human decision
insufficient_evidence  | required evidence is missing or inconclusive
blocked                | dependency prevents validation or delivery

tests pass, acceptance fails | verdict=not_user_usable
missing manual acceptance   | verdict=insufficient_evidence
blocked dependency          | verdict=blocked
```
