---
type: test
automated: true
key: HARBOR-43
title: The free berths come back in the marina's own order
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-03T16:00:00Z
updated: 2026-07-27T16:00:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-BKG-005
parent: "[[HARBOR-19 Berth booking]]"
tests: ["[[HARBOR-6 Show which berths are free for a chosen week]]"]
run_by: ["[[HARBOR-52 The free berths come back in the marina's own order]]", "[[HARBOR-71 The free berths come back in the marina's own order]]", "[[HARBOR-93 The free berths come back in the marina's own order]]", "[[HARBOR-109 The free berths come back in the marina's own order]]"]
included_in: ["[[HARBOR-19 Berth booking]]"]
---

## Scenario

```gherkin
  Given the marina has berths B7, A2 and A1
  When the office asks which berths are free from 2026-07-02 to 2026-07-04
  Then the free berths are A1, A2 and B7
```

From `Berth booking` in `booking.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-6 — the commit that wrote it
