---
type: test
automated: true
key: FIELD-35
title: The depot is both ends of the day
status: Backlog
status_category: todo
priority: normal
assignee:
created: 2026-07-27T17:00:00Z
updated: 2026-08-28T17:00:00Z
labels: []
tags: []
aliases: []
automation_id: FIELD-RTE-003
parent: "[[FIELD-10 Ordering a crew's day]]"
tests: ["[[FIELD-22 Treat the depot and the last stop as fixed ends of the day]]", "[[FIELD-97 The planner sends a crew across the fjord after the last ferry]]"]
run_by: ["[[FIELD-44 The depot is both ends of the day]]", "[[FIELD-63 The depot is both ends of the day]]", "[[FIELD-80 The depot is both ends of the day]]", "[[FIELD-117 The depot is both ends of the day]]"]
included_in: ["[[FIELD-10 Ordering a crew's day]]"]
---

## Scenario

```gherkin
  Given where the stops are
  | stop  | x  | y  |
  | depot | 0  | 0  |
  | north | 0  | 20 |
  | west  | 30 | 0  |
  | east  | 40 | 40 |
  When the day through north, west and east is planned from depot
  Then the plan is depot, north, west, east and depot
```

From `Ordering a crew's day` in `routes.feature`.

Identity is the case id, not this title: a title gets improved.

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- FIELD-22 — the commit that wrote it

## What this covers

Derived, not declared — correct it by editing the `tests:` links above.

- FIELD-97 — the commit that wrote it
