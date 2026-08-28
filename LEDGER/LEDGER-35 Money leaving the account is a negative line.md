---
type: test
automated: true
key: LEDGER-35
title: Money leaving the account is a negative line
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-24T16:30:00Z
updated: 2026-08-28T16:30:00Z
labels: []
tags: []
aliases: []
automation_id: LEDGER-BNK-004
parent: "[[LEDGER-11 Importing a bank statement]]"
tests: ["[[LEDGER-30 A refund on the statement is imported as money coming in]]", "[[LEDGER-29 Match a bank line to the invoice it pays]]"]
run_by: ["[[LEDGER-47 Money leaving the account is a negative line]]", "[[LEDGER-71 Money leaving the account is a negative line]]", "[[LEDGER-102 Money leaving the account is a negative line]]"]
included_in: ["[[LEDGER-11 Importing a bank statement]]"]
---

## Scenario

```gherkin
  When the statement for account NO-1 is imported
  | date       | cents | direction | reference | counterparty |
  | 2026-07-01 | 45000 | credit    | 2026-0007 | Bergstrom    |
  | 2026-07-02 | 12000 | debit     | refund    | Havn AS      |
  Then the ledger's amounts are 45000 and -12000
```

From `Importing a bank statement` in `bankimport.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- LEDGER-30 — the commit that wrote it
- LEDGER-29 — the commit that wrote it
