---
type: test
automated: true
key: LEDGER-14
title: A new business year starts the sequence again
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-06-23T11:20:00Z
updated: 2026-08-14T16:30:00Z
labels: []
tags: []
aliases: []
automation_id: LEDGER-INV-002
parent: "[[LEDGER-10 Invoice numbers and the lines under them]]"
included_in: ["[[LEDGER-10 Invoice numbers and the lines under them]]"]
tests: ["[[LEDGER-4 Number invoices in one unbroken sequence per business year]]", "[[LEDGER-15 Write an invoice line by line with the tax shown separately]]"]
run_by: ["[[LEDGER-53 A new business year starts the sequence again]]", "[[LEDGER-79 A new business year starts the sequence again]]"]
---

## Scenario

```gherkin
  Given 2 invoices are numbered for 2026
  When 1 invoice is numbered for 2027
  Then the numbers are 2026-0001, 2026-0002 and 2027-0001
```

From `Invoice numbers and the lines under them` in `invoices.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- LEDGER-4 — the commit that wrote it

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- LEDGER-15 — the commit that wrote it
