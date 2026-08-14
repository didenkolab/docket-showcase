---
type: test
automated: true
key: LEDGER-38
title: Every line shows the tax it is charged
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-24T16:30:00Z
updated: 2026-08-14T16:30:00Z
labels: []
tags: []
aliases: []
automation_id: LEDGER-INV-003
parent: "[[LEDGER-10 Invoice numbers and the lines under them]]"
tests: ["[[LEDGER-15 Write an invoice line by line with the tax shown separately]]", "[[LEDGER-19 Show the tax for every line and the totals underneath them]]"]
run_by: ["[[LEDGER-54 Every line shows the tax it is charged]]", "[[LEDGER-80 Every line shows the tax it is charged]]"]
included_in: ["[[LEDGER-10 Invoice numbers and the lines under them]]"]
---

## Scenario

```gherkin
  When an invoice is composed for Bergstrom Accounting
  | description | quantity | unit_cents | tax_percent |
  | Bookkeeping | 10       | 8000       | 25          |
  | Year end    | 1        | 45000      | 25          |
  Then line 1 shows 80000 net, 20000 tax and 100000 gross
```

From `Invoice numbers and the lines under them` in `invoices.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- LEDGER-15 — the commit that wrote it
- LEDGER-19 — the commit that wrote it
