---
type: test
automated: true
key: HARBOR-44
title: The card is charged when the booking is confirmed
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-03T16:00:00Z
updated: 2026-08-28T16:00:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-PAY-003
parent: "[[HARBOR-20 What a stay costs and who pays for it]]"
tests: ["[[HARBOR-33 Take the card payment when a booking is confirmed]]", "[[HARBOR-35 Carry the 3-D Secure redirect back to the booking]]"]
run_by: ["[[HARBOR-60 The card is charged when the booking is confirmed]]", "[[HARBOR-79 The card is charged when the booking is confirmed]]", "[[HARBOR-101 The card is charged when the booking is confirmed]]", "[[HARBOR-117 The card is charged when the booking is confirmed]]", "[[HARBOR-140 The card is charged when the booking is confirmed]]", "[[HARBOR-175 The card is charged when the booking is confirmed]]", "[[HARBOR-212 The card is charged when the booking is confirmed]]"]
included_in: ["[[HARBOR-20 What a stay costs and who pays for it]]"]
---

## Scenario

```gherkin
  When H-1001 is confirmed for 18000 cents
  Then the card has been charged 18000 cents for H-1001
```

From `What a stay costs and who pays for it` in `payments.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-33 — the commit that wrote it
- HARBOR-35 — the commit that wrote it
