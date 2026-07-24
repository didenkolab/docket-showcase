---
type: test
automated: true
key: LEDGER-39
title: The totals underneath add the lines up
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-24T16:30:00Z
updated: 2026-07-24T16:30:00Z
labels: []
tags: []
aliases: []
automation_id: LEDGER-INV-004
parent: "[[LEDGER-10 Invoice numbers and the lines under them]]"
tests: ["[[LEDGER-19 Show the tax for every line and the totals underneath them]]", "[[LEDGER-22 Two invoices issued in the same minute get the same number]]"]
run_by: ["[[LEDGER-55 The totals underneath add the lines up]]"]
included_in: ["[[LEDGER-10 Invoice numbers and the lines under them]]"]
---

## Scenario

```gherkin
  When an invoice is composed for Bergstrom Accounting
  | description | quantity | unit_cents | tax_percent |
  | Bookkeeping | 10       | 8000       | 25          |
  | Year end    | 1        | 45000      | 25          |
  Then the invoice totals 125000 net, 31250 tax and 156250 gross
```

From `Invoice numbers and the lines under them` in `invoices.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- LEDGER-19 — the commit that wrote it
- LEDGER-22 — the commit that wrote it
