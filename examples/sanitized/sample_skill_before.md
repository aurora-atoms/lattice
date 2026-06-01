---
name: sample-data-cleaner
description: Clean up tabular files and explain what changed.
allowed-tools: Read Write Bash
model: sonnet
---

# Sample Data Cleaner

This deliberately verbose skill describes data cleanup in a narrative way. It explains why messy data is hard, why validation matters, and why users often need consistent rows before importing CSV or JSON files into another system.

## Use When

- The user has a CSV or JSON file that needs normalization.
- The user wants deterministic validation checks.

## Do Not Use When

- The user wants unrelated statistical analysis.
- The source rules are missing.

## Workflow

1. Read the user's data file.
2. Infer cleanup steps from the prose.
3. Normalize headers, trim whitespace, and validate required columns.
4. Tell the user what changed.

## Important Constraints

Do not remove validation behavior. Do not delete rows unless the source rules explicitly allow it. Preserve rejection behavior when required columns are missing.

## Long Example

Input: CSV with repeated spaces, inconsistent header case, and missing required fields.

Output: normalized CSV plus validation report.

## Script Candidate

Header normalization, whitespace trimming, and required-column checks are deterministic and should move to a script.
