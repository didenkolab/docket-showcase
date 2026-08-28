---
type: test
automated: true
key: FIELD-105
title: A stop the crew would reach after the last ferry is handed back
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-08-28T17:00:00Z
updated: 2026-08-28T17:00:00Z
labels: []
tags: []
aliases: []
automation_id: FIELD-RTE-004
parent: "[[FIELD-10 Ordering a crew's day]]"
tests: ["[[FIELD-97 The planner sends a crew across the fjord after the last ferry]]"]
run_by: ["[[FIELD-118 A stop the crew would reach after the last ferry is handed back]]"]
included_in: ["[[FIELD-10 Ordering a crew's day]]"]
---

## Scenario

```gherkin
  Given the crew get there at
  | stop | at    |
  | west | 15:20 |
  | isle | 18:40 |
  And the last crossings are
  | stop | at    |
  | isle | 17:45 |
  When the day is checked against the ferries
  Then the crossing to isle is missed
```

From `Ordering a crew's day` in `routes.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- FIELD-97 — the commit that wrote it
