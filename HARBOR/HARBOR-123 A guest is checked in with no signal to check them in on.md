---
type: test
automated: true
key: HARBOR-123
title: A guest is checked in with no signal to check them in on
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-05T16:00:00Z
updated: 2026-08-14T16:00:00Z
labels: []
tags: []
aliases: []
automation_id: HARBOR-CHK-001
parent: "[[HARBOR-21 Checking a guest in from the pontoon]]"
tests: ["[[HARBOR-103 Check a guest in from the pontoon with no signal]]", "[[HARBOR-120 Flush the queue when the phone comes back]]"]
run_by: ["[[HARBOR-132 A guest is checked in with no signal to check them in on]]", "[[HARBOR-165 A guest is checked in with no signal to check them in on]]"]
included_in: ["[[HARBOR-21 Checking a guest in from the pontoon]]"]
---

## Scenario

```gherkin
  Given the phone has no signal
  When ola checks H-1001 in at 09:40
  Then the phone is holding H-1001
  When the phone finds a signal
  Then the office has H-1001 as arrived
```

From `Checking a guest in from the pontoon` in `checkin.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- HARBOR-103 — the commit that wrote it
- HARBOR-120 — the commit that wrote it
