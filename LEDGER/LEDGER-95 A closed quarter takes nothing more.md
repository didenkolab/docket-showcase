---
type: test
automated: true
key: LEDGER-95
title: A closed quarter takes nothing more
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-28T16:30:00Z
updated: 2026-09-04T15:20:00Z
labels: []
tags: []
aliases: []
automation_id: LEDGER-TAX-003
parent: "[[LEDGER-12 Tax rates, quarters, and closing one]]"
tests: ["[[LEDGER-85 Close a quarter so nothing can be booked into it afterwards]]", "[[LEDGER-84 Keep the tax rate that applied on the day, not the one that applies now]]"]
run_by: ["[[LEDGER-117 A closed quarter takes nothing more]]", "[[LEDGER-141 A closed quarter takes nothing more]]"]
included_in: ["[[LEDGER-12 Tax rates, quarters, and closing one]]"]
---

## Scenario

```gherkin
  Given the quarter 2026-Q3 is closed
  When an entry dated 2026-08-15 is booked
  Then the entry is refused because 2026-Q3 is closed
```

From `Tax rates, quarters, and closing one` in `tax.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- LEDGER-85 — the commit that wrote it
- LEDGER-84 — the commit that wrote it
