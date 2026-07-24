---
type: test
automated: true
key: LEDGER-37
title: A line nobody can match is left for a person
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-24T16:30:00Z
updated: 2026-07-24T16:30:00Z
labels: []
tags: []
aliases: []
automation_id: LEDGER-GEN-CF286D
generated: true
parent: "[[LEDGER-11 Importing a bank statement]]"
tests: ["[[LEDGER-29 Match a bank line to the invoice it pays]]"]
run_by: ["[[LEDGER-51 A line nobody can match is left for a person]]"]
included_in: ["[[LEDGER-11 Importing a bank statement]]"]
---

## Scenario

```gherkin
  Given the ledger is owed
  | number    | cents |
  | 2026-0007 | 45000 |
  When these lines are matched
  | date       | cents | reference |
  | 2026-07-01 | 45000 | inv 7     |
  Then line 0 is left unmatched
```

From `Importing a bank statement` in `bankimport.feature`.

**No case id in the automation**, so this one was derived from the feature file and the scenario name. Rename the scenario and it becomes a different test; tag the scenario `@LEDGER-GEN-CF286D` to settle it.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- LEDGER-29 — the commit that wrote it
