---
type: test
automated: true
key: HARBOR-28
title: The rate on the day of the booking, not today's
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-06-23T11:20:00Z
updated: 2026-09-04T15:00:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-PAY-002
parent: "[[HARBOR-20 What a stay costs and who pays for it]]"
included_in: ["[[HARBOR-20 What a stay costs and who pays for it]]"]
tests: ["[[HARBOR-7 Send the guest an invoice when a booking is confirmed]]", "[[HARBOR-33 Take the card payment when a booking is confirmed]]"]
run_by: ["[[HARBOR-59 The rate on the day of the booking, not today's]]", "[[HARBOR-78 The rate on the day of the booking, not today's]]", "[[HARBOR-100 The rate on the day of the booking, not today's]]", "[[HARBOR-116 The rate on the day of the booking, not today's]]", "[[HARBOR-139 The rate on the day of the booking, not today's]]", "[[HARBOR-174 The rate on the day of the booking, not today's]]", "[[HARBOR-211 The rate on the day of the booking, not today's]]", "[[HARBOR-236 The rate on the day of the booking, not today's]]"]
---

## Scenario

```gherkin
  Given the marina charges 5200 cents a night from 2026-08-01
  And Kittiwake has berth A1 from 2026-07-01 to 2026-07-05 as H-1001
  When the invoice for H-1001 is made out as 2026-0002
  Then the invoice totals 18000 cents
```

From `What a stay costs and who pays for it` in `payments.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-7 — the commit that wrote it

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-33 — the commit that wrote it
