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
updated: 2026-07-03T16:00:00Z
labels: []
tags: []
aliases: []
parent: "[[HARBOR-47 Cucumber on staging at 043ed64]]"
automation_id: HARBOR-PAY-005
runs: ["[[HARBOR-46 A retried confirmation charges the card once]]"]
---

## What happened

**Failed** on staging at `043ed64`.

```
ASSERT FAILED: [Charge(reference='ch-1', booking_ref='H-1001', amount_cents=18000, intent='conf-1'), Charge(reference='ch-2', booking_ref='H-1043', amount_cents=9000, intent='conf-2'), Charge(reference='ch-3', booking_ref='H-1001', amount_cents=18000, intent='conf-1')]
```

Case `HARBOR-PAY-005`, from the Cucumber report — nothing here was typed by hand.
