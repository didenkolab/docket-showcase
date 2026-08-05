---
type: test
automated: true
key: HARBOR-124
title: A morning's queue goes up in the order it happened
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-05T16:00:00Z
updated: 2026-08-05T16:00:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-CHK-002
parent: "[[HARBOR-21 Checking a guest in from the pontoon]]"
tests: ["[[HARBOR-120 Flush the queue when the phone comes back]]"]
run_by: ["[[HARBOR-133 A morning's queue goes up in the order it happened]]"]
included_in: ["[[HARBOR-21 Checking a guest in from the pontoon]]"]
---

## Scenario

```gherkin
  Given the phone has no signal
  When ola checks H-1003 in at 16:30
  And ola checks H-1001 in at 09:40
  And ola checks H-1002 in at 11:15
  And the phone finds a signal
  Then the office has H-1001, H-1002 and H-1003 as arrived
```

From `Checking a guest in from the pontoon` in `checkin.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-120 — the commit that wrote it
