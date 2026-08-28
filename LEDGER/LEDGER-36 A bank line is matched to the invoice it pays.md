---
type: test
automated: true
key: LEDGER-36
title: A bank line is matched to the invoice it pays
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-24T16:30:00Z
updated: 2026-08-28T16:30:00Z
labels: []
tags: []
aliases: []
automation_id: LEDGER-BNK-005
parent: "[[LEDGER-11 Importing a bank statement]]"
tests: ["[[LEDGER-29 Match a bank line to the invoice it pays]]"]
run_by: ["[[LEDGER-48 A bank line is matched to the invoice it pays]]", "[[LEDGER-72 A bank line is matched to the invoice it pays]]", "[[LEDGER-103 A bank line is matched to the invoice it pays]]"]
included_in: ["[[LEDGER-11 Importing a bank statement]]"]
---

## Scenario

```gherkin
  Given the ledger is owed
  | number    | cents |
  | 2026-0007 | 45000 |
  | 2026-0008 | 12000 |
  When these lines are matched
  | date       | cents | reference           |
  | 2026-07-01 | 45000 | payment 2026-0007   |
  | 2026-07-02 | 12000 | 2026-0008 thank you |
  Then the lines are matched to 2026-0007 and 2026-0008
```

From `Importing a bank statement` in `bankimport.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- LEDGER-29 — the commit that wrote it
