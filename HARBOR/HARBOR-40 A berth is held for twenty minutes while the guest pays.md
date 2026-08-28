---
type: test
automated: true
key: HARBOR-40
title: A berth is held for twenty minutes while the guest pays
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-03T16:00:00Z
updated: 2026-08-28T16:00:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-BKG-006
parent: "[[HARBOR-19 Berth booking]]"
tests: ["[[HARBOR-30 Hold a berth for twenty minutes while the guest pays]]", "[[HARBOR-31 Cancel a booking and give the berth back]]"]
run_by: ["[[HARBOR-53 A berth is held for twenty minutes while the guest pays]]", "[[HARBOR-72 A berth is held for twenty minutes while the guest pays]]", "[[HARBOR-94 A berth is held for twenty minutes while the guest pays]]", "[[HARBOR-110 A berth is held for twenty minutes while the guest pays]]", "[[HARBOR-131 A berth is held for twenty minutes while the guest pays]]", "[[HARBOR-164 A berth is held for twenty minutes while the guest pays]]", "[[HARBOR-200 A berth is held for twenty minutes while the guest pays]]"]
included_in: ["[[HARBOR-19 Berth booking]]"]
---

## Scenario

```gherkin
  When Puffin holds berth A2 from 2026-07-01 to 2026-07-03 as H-1003 at 10:00
  Then the hold is taken
  And the hold runs out at 10:20
```

From `Berth booking` in `booking.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-30 — the commit that wrote it
- HARBOR-31 — the commit that wrote it
