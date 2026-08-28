---
type: test
automated: true
key: LEDGER-93
title: The tax is rounded on every line
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-28T16:30:00Z
updated: 2026-08-28T16:30:00Z
labels: []
tags: []
aliases: []
automation_id: LEDGER-TAX-001
parent: "[[LEDGER-12 Tax rates, quarters, and closing one]]"
tests: ["[[LEDGER-83 Round the tax per line or per invoice, whichever the country says]]"]
run_by: ["[[LEDGER-115 The tax is rounded on every line]]"]
included_in: ["[[LEDGER-12 Tax rates, quarters, and closing one]]"]
---

## Scenario

```gherkin
  When the tax on these lines is worked out per-line
  | net_cents | tax_percent |
  | 333       | 25          |
  | 333       | 25          |
  | 333       | 25          |
  Then the tax comes to 249 cents
```

From `Tax rates, quarters, and closing one` in `tax.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- LEDGER-83 — the commit that wrote it
