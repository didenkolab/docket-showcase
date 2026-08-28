---
type: test
automated: true
key: HARBOR-24
title: The berths that are free for a week
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-06-23T11:20:00Z
updated: 2026-08-28T16:00:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-BKG-004
parent: "[[HARBOR-19 Berth booking]]"
included_in: ["[[HARBOR-19 Berth booking]]"]
tests: ["[[HARBOR-6 Show which berths are free for a chosen week]]"]
run_by: ["[[HARBOR-51 The berths that are free for a week]]", "[[HARBOR-70 The berths that are free for a week]]", "[[HARBOR-92 The berths that are free for a week]]", "[[HARBOR-108 The berths that are free for a week]]", "[[HARBOR-129 The berths that are free for a week]]", "[[HARBOR-162 The berths that are free for a week]]", "[[HARBOR-198 The berths that are free for a week]]"]
---

## Scenario

```gherkin
  Given Kittiwake has berth A1 from 2026-07-01 to 2026-07-05 as H-1001
  When the office asks which berths are free from 2026-07-02 to 2026-07-04
  Then the free berths are A2 and B7
```

From `Berth booking` in `booking.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-6 — the commit that wrote it
