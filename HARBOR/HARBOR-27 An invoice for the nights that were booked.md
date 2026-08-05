---
type: test
automated: true
key: HARBOR-27
title: An invoice for the nights that were booked
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-06-23T11:20:00Z
updated: 2026-08-05T16:00:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-PAY-001
parent: "[[HARBOR-20 What a stay costs and who pays for it]]"
included_in: ["[[HARBOR-20 What a stay costs and who pays for it]]"]
tests: ["[[HARBOR-7 Send the guest an invoice when a booking is confirmed]]"]
run_by: ["[[HARBOR-58 An invoice for the nights that were booked]]", "[[HARBOR-77 An invoice for the nights that were booked]]", "[[HARBOR-99 An invoice for the nights that were booked]]", "[[HARBOR-115 An invoice for the nights that were booked]]", "[[HARBOR-138 An invoice for the nights that were booked]]"]
---

## Scenario

```gherkin
  Given Kittiwake has berth A1 from 2026-07-01 to 2026-07-05 as H-1001
  When the invoice for H-1001 is made out as 2026-0001
  Then the invoice totals 18000 cents
  And the invoice is numbered 2026-0001
```

From `What a stay costs and who pays for it` in `payments.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-7 — the commit that wrote it
