---
type: test
automated: true
key: HARBOR-25
title: The morning a boat leaves, its berth is somebody else's night
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-06-23T11:20:00Z
updated: 2026-06-23T11:20:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-BKG-003
parent: "[[HARBOR-19 Berth booking]]"
included_in: ["[[HARBOR-19 Berth booking]]"]
---

## Scenario

```gherkin
  Given Kittiwake has berth A1 from 2026-07-01 to 2026-07-05 as H-1001
  When Puffin books berth A1 from 2026-07-05 to 2026-07-09 as H-1002
  Then the booking is taken
```

From `Berth booking` in `booking.feature`.

Identity is the case id, not this title: a title gets improved.
