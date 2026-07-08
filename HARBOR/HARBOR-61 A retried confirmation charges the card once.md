---
type: test_run
result: failed
ran_at:
evidence: 'ASSERT FAILED: [Charge(reference=''ch-1'', booking_ref=''H-1001'', amount_cents=18000, intent=''conf-1''), Charge(reference=''ch-2'', booking_ref=''H-1043'', amount_cents=9000, intent=''conf-'
key: HARBOR-61
title: A retried confirmation charges the card once
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-03T16:00:00Z
updated: 2026-07-08T11:40:00Z
labels: []
tags: []
aliases: []
parent: "[[HARBOR-47 Cucumber on staging at 043ed64]]"
automation_id: HARBOR-PAY-005
runs: ["[[HARBOR-46 A retried confirmation charges the card once]]"]
found: ["[[HARBOR-64 A retried confirmation charges the card twice]]"]
---

## What happened

**Failed** on staging at `043ed64`.

```
ASSERT FAILED: [Charge(reference='ch-1', booking_ref='H-1001', amount_cents=18000, intent='conf-1'), Charge(reference='ch-2', booking_ref='H-1043', amount_cents=9000, intent='conf-2'), Charge(reference='ch-3', booking_ref='H-1001', amount_cents=18000, intent='conf-1')]
```

Case `HARBOR-PAY-005`, from the Cucumber report — nothing here was typed by hand.

## Comments

**mateo · 2026-07-08 11:40** — The Friday run had already caught this. Linking the failing run to the bug so the history says when we first saw it rather than when we noticed we had seen it.
