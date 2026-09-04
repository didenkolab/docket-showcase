---
type: test
automated: true
key: LEDGER-34
title: A statement that arrives as a file
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-24T16:30:00Z
updated: 2026-09-04T15:20:00Z
labels: []
tags: []
aliases: []
automation_id: LEDGER-BNK-003
parent: "[[LEDGER-11 Importing a bank statement]]"
tests: ["[[LEDGER-24 Import a statement from a CSV file when the bank has no feed]]", "[[LEDGER-30 A refund on the statement is imported as money coming in]]"]
run_by: ["[[LEDGER-46 A statement that arrives as a file]]", "[[LEDGER-70 A statement that arrives as a file]]", "[[LEDGER-101 A statement that arrives as a file]]", "[[LEDGER-125 A statement that arrives as a file]]"]
included_in: ["[[LEDGER-11 Importing a bank statement]]"]
---

## Scenario

```gherkin
  When this file is read as a statement
  """
  date,amount,message
  2026-07-01,450.00,2026-0007
  2026-07-02,120.00,2026-0008
  """
  Then the file gives lines dated 2026-07-01 and 2026-07-02
  And the first line of the file is 45000 cents
```

From `Importing a bank statement` in `bankimport.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- LEDGER-24 — the commit that wrote it
- LEDGER-30 — the commit that wrote it
