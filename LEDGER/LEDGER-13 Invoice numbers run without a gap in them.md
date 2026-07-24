---
type: test
automated: true
key: LEDGER-13
title: Invoice numbers run without a gap in them
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-06-23T11:20:00Z
updated: 2026-07-24T16:30:00Z
labels: []
tags: []
aliases: []
automation_id: LEDGER-INV-001
parent: "[[LEDGER-10 Invoice numbers and the lines under them]]"
included_in: ["[[LEDGER-10 Invoice numbers and the lines under them]]"]
tests: ["[[LEDGER-4 Number invoices in one unbroken sequence per business year]]"]
run_by: ["[[LEDGER-52 Invoice numbers run without a gap in them]]"]
---

## Scenario

```gherkin
  When 3 invoices are numbered for 2026
  Then the numbers are 2026-0001, 2026-0002 and 2026-0003
```

From `Invoice numbers and the lines under them` in `invoices.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- LEDGER-4 — the commit that wrote it
