---
type: test
automated: true
key: LEDGER-96
title: The rate that applied on the day of the invoice
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-28T16:30:00Z
updated: 2026-08-28T16:30:00Z
labels: []
tags: []
aliases: []
automation_id: LEDGER-TAX-004
parent: "[[LEDGER-12 Tax rates, quarters, and closing one]]"
tests: ["[[LEDGER-84 Keep the tax rate that applied on the day, not the one that applies now]]", "[[LEDGER-90 An invoice dated the last day of the quarter falls into the next one]]"]
run_by: ["[[LEDGER-118 The rate that applied on the day of the invoice]]"]
included_in: ["[[LEDGER-12 Tax rates, quarters, and closing one]]"]
---

## Scenario

```gherkin
  Given the tax rate was 25 from 2020-01-01 and 22 from 2026-09-01
  When the rate for 2026-08-31 is looked up
  Then the rate is 25
```

From `Tax rates, quarters, and closing one` in `tax.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- LEDGER-84 — the commit that wrote it
- LEDGER-90 — the commit that wrote it
