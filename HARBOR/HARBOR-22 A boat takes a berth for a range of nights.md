---
type: test
automated: true
key: HARBOR-22
title: A boat takes a berth for a range of nights
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-06-23T11:20:00Z
updated: 2026-06-23T11:20:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-BKG-001
parent: "[[HARBOR-19 Berth booking]]"
included_in: ["[[HARBOR-19 Berth booking]]"]
---

## Scenario

```gherkin
  When Kittiwake books berth A1 from 2026-07-01 to 2026-07-05 as H-1001
  Then the booking is taken
  And the calendar holds H-1001
```

From `Berth booking` in `booking.feature`.

Identity is the case id, not this title: a title gets improved.
