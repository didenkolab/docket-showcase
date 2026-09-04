---
type: test
automated: true
key: LEDGER-33
title: The same statement twice is the same statement
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-24T16:30:00Z
updated: 2026-09-04T15:20:00Z
labels: []
tags: []
aliases: []
automation_id: LEDGER-BNK-002
parent: "[[LEDGER-11 Importing a bank statement]]"
tests: ["[[LEDGER-25 Importing the same statement twice does not produce two of everything]]", "[[LEDGER-24 Import a statement from a CSV file when the bank has no feed]]"]
run_by: ["[[LEDGER-45 The same statement twice is the same statement]]", "[[LEDGER-69 The same statement twice is the same statement]]", "[[LEDGER-100 The same statement twice is the same statement]]", "[[LEDGER-124 The same statement twice is the same statement]]"]
included_in: ["[[LEDGER-11 Importing a bank statement]]"]
---

## Scenario

```gherkin
  Given the statement for account NO-1 is imported
  | date       | cents | reference | counterparty |
  | 2026-07-01 | 45000 | 2026-0007 | Bergstrom    |
  When the statement for account NO-1 is imported
  | date       | cents | reference | counterparty |
  | 2026-07-01 | 45000 | 2026-0007 | Bergstrom    |
  Then the import is recognised as one we already have
  And the ledger holds lines dated 2026-07-01
```

From `Importing a bank statement` in `bankimport.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- LEDGER-25 — the commit that wrote it
- LEDGER-24 — the commit that wrote it
