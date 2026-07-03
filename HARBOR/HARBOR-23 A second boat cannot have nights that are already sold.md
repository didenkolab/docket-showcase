---
type: test
automated: true
key: HARBOR-23
title: A second boat cannot have nights that are already sold
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-06-23T11:20:00Z
updated: 2026-07-03T16:00:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-BKG-002
parent: "[[HARBOR-19 Berth booking]]"
included_in: ["[[HARBOR-19 Berth booking]]"]
tests: ["[[HARBOR-6 Show which berths are free for a chosen week]]"]
run_by: ["[[HARBOR-49 A second boat cannot have nights that are already sold]]"]
---

## Scenario

```gherkin
  Given Kittiwake has berth A1 from 2026-07-01 to 2026-07-05 as H-1001
  When Puffin books berth A1 from 2026-07-03 to 2026-07-08 as H-1002
  Then the booking is refused because berth taken
  And the refusal names H-1001
```

From `Berth booking` in `booking.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-6 — the commit that wrote it
