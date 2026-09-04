---
type: test
automated: true
key: LEDGER-32
title: A statement is imported into the ledger
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-24T16:30:00Z
updated: 2026-09-04T15:20:00Z
labels: []
tags: []
aliases: []
automation_id: LEDGER-BNK-001
parent: "[[LEDGER-11 Importing a bank statement]]"
tests: ["[[LEDGER-23 Fetch a statement from the three banks our first accountants use]]", "[[LEDGER-25 Importing the same statement twice does not produce two of everything]]"]
run_by: ["[[LEDGER-44 A statement is imported into the ledger]]", "[[LEDGER-68 A statement is imported into the ledger]]", "[[LEDGER-99 A statement is imported into the ledger]]", "[[LEDGER-123 A statement is imported into the ledger]]"]
included_in: ["[[LEDGER-11 Importing a bank statement]]"]
---

## Scenario

```gherkin
  When the statement for account NO-1 is imported
  | date       | cents | reference | counterparty |
  | 2026-07-01 | 45000 | 2026-0007 | Bergstrom    |
  | 2026-07-02 | 12000 | 2026-0008 | Havn AS      |
  Then the ledger holds lines dated 2026-07-01 and 2026-07-02
```

From `Importing a bank statement` in `bankimport.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- LEDGER-23 — the commit that wrote it
- LEDGER-25 — the commit that wrote it
